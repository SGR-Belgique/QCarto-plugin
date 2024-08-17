# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Utilitaires pour la Gestion des Couches Parcours-GR et Parcours-RB
# ========================================================================================

from qgis.core import *
from qgis.gui import *

import importlib

import QCarto_Tools_Coding as TCOD
importlib.reload(TCOD)

import QCarto_Parameters_Global
importlib.reload(QCarto_Parameters_Global)
QGP = QCarto_Parameters_Global.globalParameters()


# ========================================================================================
# Générer une liste triée d'itinéraires GR // GRP // GRT
#  >>> type							[str]				List of Itinerary Type : 'GR' 'GRP' 'GRT'
#  >>> dicoTracksGRFeatures			Dict					 
# ========================================================================================

def getOrderedListItineraryGR(types, dicoTracksGRFeatures ):
	listGRCodes = list({'-'.join(code.split('-')[0:2]) for code in dicoTracksGRFeatures if len(code.split('-')) >= 2 and code.split('-')[0] in types})
	listGRCodes = sorted(listGRCodes, key = lambda x: ('00000' + x.split('-')[1])[-5:] if x.split('-')[1].isdigit() else x.split('-')[1])
	return listGRCodes


# ========================================================================================
# Générer une liste triée d'itinéraires RB // RF // RL // IR - En fait les itinéraires ici ne comprennent que les deux premiers champs (e.g. RB-Na)
#  >>> types						[str]				List of Itinerary Type : 'RB', 'RL', 'RF', 'RI', 'IR'
#  >>> dicoTracksRBFeatures			Dict		
#  >>> itineraryFolderMode			Bool				If True : renvoie la liste des folders : les deux premiers champs (e.g. RB-Na)
#														if False : renvoie la liste des itinéraires - les 3 champs (e.g. RB-Na-02)			 
# ========================================================================================

def getOrderedListItineraryRB(types, dicoTracksRBFeatures, itineraryFolderMode = True ):

	if itineraryFolderMode :
		listRBCodes = list({TCOD.itineraryFolderFromTrackCode(code) for code in dicoTracksRBFeatures if TCOD.itineraryFolderFromTrackCode(code) != '' and TCOD.itineraryTypeFromTrackCode(code) in types})
		listRBCodes = sorted(listRBCodes, key = lambda x: x.split('-')[0:2])
	else:
		listRBCodes = list({TCOD.itineraryFromTrackCode(code) for code in dicoTracksRBFeatures if TCOD.itineraryFromTrackCode(code) != '' and TCOD.itineraryTypeFromTrackCode(code) in types})
		listRBCodes = sorted(listRBCodes, key = lambda x: x.split('-')[0:3])
	return listRBCodes


# ========================================================================================
# Générer un dictionnaire des Tronçons par Parcours GR / RB
#  >>> type							str				Itinerary Type : ('GR' 'GRP' 'GRT') OR ('RB' 'RF' 'RL' 'RI' 'IR') 
#  >>> dicoTracksFeatures 			dict			codeTrack : feature 'Parcours-GR' or 'Parcours-RB'
#  >>> dicoSectionsFeatures 		dict			idSection : feature 'Tronçons-GR'	
#  <<< dicoTracksSections 			dict			codeTrack : set(idSection)
# ========================================================================================
		
def generateDicoTracksSections(type, dicoTracksFeatures, dicoSectionsFeatures):

	if 	type in QGP.typeSetComputeGRMode :
		dicoTrackSections = { trackCode : set() for trackCode in dicoTracksFeatures }
		for idSection in dicoSectionsFeatures:
			for gr_code in TCOD.grCodeListFromSectionFeature(dicoSectionsFeatures[idSection], 'GR-P-T'):
				valid, type, label, zone, number, itineraryCode, trackBaseCode, trackCode, modificationList, invalidationList, repeatCount, bifurcationNumber, direction = TCOD.elementsFromGrCode(gr_code)		
				if trackCode in dicoTrackSections:
					dicoTrackSections[trackCode].add(dicoSectionsFeatures[idSection][QGP.tableSectionsFieldId])
		
	if 	type in QGP.typeSetComputeRBMode :
		dicoTrackSections = { TCOD.trackBaseCodeFromTrackCode(trackCode) : set() for trackCode in dicoTracksFeatures }
		for idSection in dicoSectionsFeatures:
			for gr_code in TCOD.grCodeListFromSectionFeature(dicoSectionsFeatures[idSection], 'RB-F-L-IR'):
				valid, type, label, zone, number, itineraryCode, trackBaseCode, trackCode, modificationList, invalidationList, repeatCount, bifurcationNumber, direction = TCOD.elementsFromGrCode(gr_code)		
				if trackCode in dicoTrackSections:
					dicoTrackSections[trackCode].add(dicoSectionsFeatures[idSection][QGP.tableSectionsFieldId])
				elif trackBaseCode in dicoTrackSections:
					dicoTrackSections[trackBaseCode].add(dicoSectionsFeatures[idSection][QGP.tableSectionsFieldId])
				else:
					continue

	return dicoTrackSections


# ========================================================================================
# Déterminer l'ordre des sections d'un tracé 
#  >>> codeToCompute 				: str				code du Tracé comme dns la table affichée - avec -M et -# éventuels
#  >>> dicoTrackSections			: dictionnaire		trackCode > [sectionId]
#  >>> dicoSectionsFeatures 		: dictionnaire		id : Section Feature
#  >>> dicoSectionsFeaturesEndPoints: dictionnaire		id : [PointA, PointZ]
#  <<< idListSectionsOrdered		: [idSection]		liste ordonnée des sections du tracé :
#															id positif : le section est dans le bon sens
#															id négatif : le section est en sens inverse du tracé
#      idListSectionsRemaining 		: [idSection]			liste non ordonnée des sections "perdus" / en cas Y : alternatives / en cas de débutS : alternatives
# 	   errorCode					: 0					Pas d'erreur
#							  		  1					Tracé vide
#							  		  2					Tracé sans début
#							  		  3					Tracé avec multiples débuts
#									  4					Tracé incomplet - il reste des sections non accrochés
#									  5					Tracé incomplet - Y non résolu 
#							  		  13				Tracé variante avec multiples débuts
#									  14				Tracé variante incomplet - il reste des sections non accrochés
#									  15				Tracé variante incomplet - Y non résolu 
#									  9					Code tracé invalide
#	   gapList						: [gap]				Gap = [idSection, idSection, pointGap, int] - Id's not joined + distance
#	   modificationSet				: set				Ensemble des codes de modification détectés
#	   idListSectionsModified		: [idSection]		Liste des sections avec code modification
# ========================================================================================
		
def computeTracksOrderedSections(codeToBeComputed, dicoTrackSections, dicoSectionsFeatures, dicoSectionsFeaturesEndPoints):				
				
# ========================================================================================	
#  Trouver les sections qui s'attachent au dernier point
# ========================================================================================	
	def retrieveSectionsAttached(idSectionsList, lastPoint):
		idSectionsListDirect = [idSection for idSection in idSectionsList if dicoSectionsFeaturesEndPoints[idSection][0].distance(lastPoint) <= 1]
		idSectionsListIndirect = [idSection for idSection in idSectionsList if dicoSectionsFeaturesEndPoints[idSection][1].distance(lastPoint) <= 1]
		if idSectionsListDirect == [] and idSectionsListIndirect == []:
			idSectionsListDirect = [idSection for idSection in idSectionsList if dicoSectionsFeaturesEndPoints[idSection][0].distance(lastPoint) <= QGP.configMatchDistanceShort]
			idSectionsListIndirect = [idSection for idSection in idSectionsList if dicoSectionsFeaturesEndPoints[idSection][1].distance(lastPoint) <= QGP.configMatchDistanceShort]
		return idSectionsListDirect, idSectionsListIndirect			

# ========================================================================================
#  Ajouter la section suivante au tracé de base
# ========================================================================================	
	def appendNextBaseSection(idSectionCurrent, lastPointCurrent, idSection, direct):												
		if idSectionCurrent != None:
			distance = dicoSectionsFeaturesEndPoints[idSection][0].distance(lastPointCurrent) if direct else dicoSectionsFeaturesEndPoints[idSection][-1].distance(lastPointCurrent)
			if distance > 0: gapList.append([idSectionCurrent, idSection, (dicoSectionsFeaturesEndPoints[idSection][0] if direct else dicoSectionsFeaturesEndPoints[idSection][-1]), distance])
		idSectionCurrentNew = idSection
		lastPointCurrentNew = dicoSectionsFeaturesEndPoints[idSectionCurrentNew][1] if direct else dicoSectionsFeaturesEndPoints[idSectionCurrentNew][0]
		idListSectionsOrdered.append(idSectionCurrentNew if direct else -idSectionCurrentNew)
		if dicoGrListInfos[idSectionCurrentNew][C_repeatCount] > 1:
			dicoGrListInfos[idSectionCurrentNew][C_repeatCount] -= 1
			if dicoGrListInfos[idSectionCurrentNew][C_bifurcationNum] < QGP.C_ComputeTrackBifurcationDefault : dicoGrListInfos[idSectionCurrentNew][C_bifurcationNum] += 3 									# Trick for RB-BR cases with -X3
		else:	
			idListSectionsRemaining.pop(idListSectionsRemaining.index(idSectionCurrentNew))
		return idSectionCurrentNew, lastPointCurrentNew

# ========================================================================================
#  Ajouter la section suivante au tracé de la variante
# ========================================================================================	
	def appendNextVariantSection(idSectionCurrent, lastPointCurrent, idSection, direct):		
		distance = dicoSectionsFeaturesEndPoints[idSection][0].distance(lastPointCurrent) if direct else dicoSectionsFeaturesEndPoints[idSection][-1].distance(lastPointCurrent)
		if distance > 0: gapList.append([idSectionCurrent, idSection, (dicoSectionsFeaturesEndPoints[idSection][0] if direct else dicoSectionsFeaturesEndPoints[idSection][-1]), distance])
		idSectionCurrentNew = idSection
		lastPointCurrentNew = dicoSectionsFeaturesEndPoints[idSectionCurrentNew][1] if direct else dicoSectionsFeaturesEndPoints[idSectionCurrentNew][0]
		idListSectionsOrderedVariantTrack.append(idSectionCurrentNew if direct else -idSectionCurrentNew)
		if priorityDicoGrListInfos[code][idSectionCurrentNew][C_repeatCount] > 1:
			priorityDicoGrListInfos[code][idSectionCurrentNew][C_repeatCount] -= 1
		else:	
			priorityDicoidSectionsList[code].remove(idSectionCurrentNew)
		return idSectionCurrentNew, lastPointCurrentNew

# ========================================================================================
# Code de la fonction
# ========================================================================================
				
#	Déterminer le code tracé demandé et les modifications correspondantes

	trackValid, trackType, u3, u4, u5, u6, trackBaseCode, trackCode, trackModifTags, trackInvalidTags, u11, u12, u13 = TCOD.elementsFromGrCode(codeToBeComputed)
	if not trackValid : return [], [], 9, [], set(), []

#	Déterminer le parcours à calculer d'abord	

	if trackType in QGP.typeSetComputeGRMode :
		codeComputed = trackCode
		computeTrackVariant = False
	elif trackCode[-1] == '$':																							# Les codes RB se terminant par $ sont toujours calculés directement
		codeComputed = trackCode[0:-1]
		computeTrackVariant = False
	else:																												# Case in RB Mode
		codeComputed = trackBaseCode
		computeTrackVariant = trackBaseCode != trackCode
	
#	Créer la liste des tronçons pour le tracé codeComputed
#	Créer un dictionaire des infos extraites du code gr_list pour toutes les sections du tracé codeComputed

	if codeComputed not in dicoTrackSections: return [], [], 1, [], set(), []

	dicoGrListInfos = {}
	idSectionsSet = set()
	modificationSet = set()

	for idSection in dicoTrackSections[codeComputed]:																	# Original set contains also variants 
		for grCode in TCOD.grCodeListFromSectionFeature(dicoSectionsFeatures[idSection], trackType):
			valid, u2, u3, u4, u5, u6, sectionTrackBaseCode, sectionTrackCode, sectionModifList, sectionInvalidationList, repeatCount, bifurcationNumber, direction = TCOD.elementsFromGrCode(grCode)
			if not valid: continue
			if sectionTrackCode == codeComputed:
				dicoGrListInfos[idSection] = [sectionModifList, sectionInvalidationList, repeatCount, bifurcationNumber, direction]
				idSectionsSet.add(idSection)
				modificationSet.update(set(sectionModifList + sectionInvalidationList))
				break		
	
	C_modifTagsList = 0 ; C_invalidTagsList = 1 ; C_repeatCount = 2 ; C_bifurcationNum = 3 ; C_direction = 4

#	Créer la liste des tronçons restants et la liste des tronçons arrangés

	idListSectionsRemaining = [idSection for idSection in idSectionsSet if TCOD.modificationCodesCompatibility( dicoGrListInfos[idSection][C_modifTagsList],  dicoGrListInfos[idSection][C_invalidTagsList],  trackModifTags, trackInvalidTags) ]
	idListSectionsModified = [idSection for idSection in idSectionsSet if dicoGrListInfos[idSection][C_modifTagsList] != [] or dicoGrListInfos[idSection][C_invalidTagsList] != [] ]
	idListSectionsOrdered = []
	
	if idListSectionsRemaining == []: return [], [], 1, [], modificationSet, idListSectionsModified						# Ce tracé est vide 
	
#	Rechercher le premier tronçon

	idFirst = [idSection for idSection in idListSectionsRemaining if dicoGrListInfos[idSection][C_direction] != None]
	if len(idFirst) == 0: return [], idListSectionsRemaining, 2, [], modificationSet, idListSectionsModified			# Ce tracé n'a pas de début
	if len(idFirst) > 1:  return [], idFirst, 3, [], modificationSet, idListSectionsModified							# Ce tracé a plusieurs débuts
	idFirst = idFirst[0]

#	Trouver le sens du premier tronçon

	direct = True
	if dicoGrListInfos[idFirst][C_direction] == 'N':
		if dicoSectionsFeaturesEndPoints[idFirst][1].y() < dicoSectionsFeaturesEndPoints[idFirst][0].y():
			direct = False
	if dicoGrListInfos[idFirst][C_direction] == 'S':
		if dicoSectionsFeaturesEndPoints[idFirst][1].y() > dicoSectionsFeaturesEndPoints[idFirst][0].y():
			direct = False
	if dicoGrListInfos[idFirst][C_direction] == 'E':
		if dicoSectionsFeaturesEndPoints[idFirst][1].x() < dicoSectionsFeaturesEndPoints[idFirst][0].x():
			direct = False
	if dicoGrListInfos[idFirst][C_direction] in ('O', 'W'):
		if dicoSectionsFeaturesEndPoints[idFirst][1].x() > dicoSectionsFeaturesEndPoints[idFirst][0].x():
			direct = False
	
	idSectionCurrent, lastPointCurrent = appendNextBaseSection(None, None, idFirst, direct)	
	
#	Boucler tant qu'il reste des tronçons

	gapList = []				

	while len(idListSectionsRemaining) > 0:
			
#	Chercher les tronçons accrochables : chercher d'abord à max 1 mètre, ensuite max 10 mètres)

		idSectionsListDirect, idSectionsListIndirect = retrieveSectionsAttached(idListSectionsRemaining, lastPointCurrent)

#	Eliminer retour direct si alternatives possibles

		if len(idSectionsListDirect + idSectionsListIndirect) > 1:
			if idSectionCurrent in idSectionsListDirect:
				idSectionsListDirect.pop(idSectionsListDirect.index(idSectionCurrent))
			if idSectionCurrent in idSectionsListIndirect:
				idSectionsListIndirect.pop(idSectionsListIndirect.index(idSectionCurrent))
			
#	Pas de tronçon accrochable

		if len(idSectionsListDirect) == 0 and len(idSectionsListIndirect) == 0:
			return idListSectionsOrdered, idListSectionsRemaining, 4, gapList, modificationSet, idListSectionsModified

#	Facile s'il n'y en a qu'une section possible

		if len(idSectionsListDirect + idSectionsListIndirect) == 1:
			idSection, direct = (idSectionsListDirect[0], True) if len(idSectionsListDirect) == 1 else (idSectionsListIndirect[0], False)
			idSectionCurrent, lastPointCurrent = appendNextBaseSection(idSectionCurrent, lastPointCurrent, idSection, direct)
			continue

#	Plusieurs possibilités - Calculer les priorités en fonction des codes Y

		priorityListDirect = [dicoGrListInfos[idSection][C_bifurcationNum] for idSection in idSectionsListDirect]
		priorityListIndirect = [dicoGrListInfos[idSection][C_bifurcationNum] for idSection in idSectionsListIndirect]
		priorityBest = min(priorityListDirect + priorityListIndirect)													# Min because -Y1 has priority on -Y2 ...
					
		if (priorityListDirect + priorityListIndirect).count(priorityBest) > 1:
			return idListSectionsOrdered, idSectionsListDirect + idSectionsListIndirect, 5, gapList, modificationSet, idListSectionsModified

		if priorityBest in priorityListDirect:
			idSectionCurrent, lastPointCurrent = appendNextBaseSection(idSectionCurrent, lastPointCurrent, idSectionsListDirect[priorityListDirect.index(priorityBest)], True)
		if priorityBest in 	priorityListIndirect:
			idSectionCurrent, lastPointCurrent = appendNextBaseSection(idSectionCurrent, lastPointCurrent, idSectionsListIndirect[priorityListIndirect.index(priorityBest)], False)
		continue
	
#	Done except for Track Variants	
	
	if not computeTrackVariant:  return idListSectionsOrdered, [], 0, gapList, modificationSet, idListSectionsModified
	
# ========================================================================================
#	Here for variant of base track in case of RB - trackCode is the full track code
#	Notice that there can be several variant active in the same time, e.g -R1-V1
# 	We consider the base track (idListSectionsOrdered) but deviate when requested
# ========================================================================================

# 	Build Priority List - Based on Full Track Code - Les suffixes terminés par * désignent les raccourcis / variantes inverses 

	baseCodeComputed = codeComputed
	codeComputed = trackCode

	priorityList = TCOD.trackPriorityListFromFromTrackCode(codeComputed)											# Ordered priorities - First in list is higher priority
	priorityDicoActive = {TCOD.purifyTrackCode(code) : code[-1] != '*' for code in priorityList}					# Priorities are immediately active except *
	priorityList = [TCOD.purifyTrackCode(code) for code in priorityList]											# Because * are not in tronçon-GR
	priorityDicoInside = {code : False for code in priorityList}													# To keep notice of first encounter

	priorityDicoGrListInfos = {code : {} for code in priorityList}	
	priorityDicoidSectionsList = {code : set() for code in priorityList}	

	for idSection in dicoTrackSections[baseCodeComputed]:															# Original set contains also variants 
		for grCode in TCOD.grCodeListFromSectionFeature(dicoSectionsFeatures[idSection], trackType):
			valid, u2, u3, u4, u5, u6, sectionTrackBaseCode, sectionTrackCode, sectionModifList, sectionInvalidationList, repeatCount, bifurcationNumber, direction = TCOD.elementsFromGrCode(grCode)
			if not valid: continue
			if baseCodeComputed != sectionTrackBaseCode: continue
			for code in priorityList:
				if code in TCOD.trackPriorityListFromFromTrackCode(sectionTrackCode) :
					priorityDicoGrListInfos[code][idSection] = [sectionModifList, sectionInvalidationList, repeatCount, bifurcationNumber, direction]
					priorityDicoidSectionsList[code].add(idSection)

	C_modifTagsList = 0 ; C_invalidTagsList = 1 ; C_repeatCount = 2 ; C_bifurcationNum = 3 ; C_direction = 4

#	Restart from start (D/A) of Base RB Track

	idListSectionsOrderedBaseTrack = idListSectionsOrdered
	idFirstBaseTrack = idListSectionsOrdered[0]
	idListSectionsOrderedVariantTrack =  []
	idSectionCurrentVariantTrack = None
	startPointCurrentVariantTrack = dicoSectionsFeaturesEndPoints[idFirstBaseTrack][0] if idFirstBaseTrack > 0 else dicoSectionsFeaturesEndPoints[abs(idFirstBaseTrack)][1]
	indexOnBaseTrack = 0
	indexOnBaseTrackAfterVariant = 0					

#	Loop until we reach base track starting point again
#	At each point, look for a priority track, if one match, take it but not directly if * indicated backward return
#	If none match, continue as base track

	lastPointCurrentVariantTrack = startPointCurrentVariantTrack
	backwardReturn = False
	anyVariantsectionFound = False
	
	while True:
	
		if len(idListSectionsOrderedVariantTrack) >= 100:	
			return idListSectionsOrderedVariantTrack, [], 16, [], modificationSet, idListSectionsModified		
	
#		Chercher les tronçons variants accrochables, par ordre de priorité  : chercher d'abord à max 1 mètre, ensuite max 10 mètres)	
	
		variantsectionFound = False
	
		for code in priorityList:

			idSectionsListDirect, idSectionsListIndirect = retrieveSectionsAttached(priorityDicoidSectionsList[code], lastPointCurrentVariantTrack)

#			Si aucun tronçon n'est possible avec ce code

			if len(idSectionsListDirect) == 0 and len(idSectionsListIndirect) == 0:
				if priorityDicoInside[code] :
					priorityDicoActive[code] = True																# Activer la priorité à la sortie
				continue																						# Continuer avec la priorité suivante

#			Si c'est un code de retour inverse qui n'est pas encore actif, noter qu'il a été rencontré
				
			if not priorityDicoActive[code]:
				priorityDicoInside[code] = True																	# Provoquera l'activation plus tard
				continue	

#			La priorité est active !

#			Eliminer un retour direct si autres possibilités

			if len(idSectionsListDirect + idSectionsListIndirect) > 1:
				if idSectionCurrentVariantTrack in idSectionsListDirect:
					idSectionsListDirect.pop(idSectionsListDirect.index(idSectionCurrentVariantTrack))
				if idSectionCurrentVariantTrack in idSectionsListIndirect:
					idSectionsListIndirect.pop(idSectionsListIndirect.index(idSectionCurrentVariantTrack))

#			Si encore au départ, gérer les cas -1x

			if idListSectionsOrderedVariantTrack == []:
				idSectionsListDirectStart = [idSection for idSection in idSectionsListDirect if priorityDicoGrListInfos[code][idSection][C_direction] != None]
				idSectionsListIndirectStart = [idSection for idSection in idSectionsListIndirect if priorityDicoGrListInfos[code][idSection][C_direction] != None]
				if len(idSectionsListDirectStart + idSectionsListIndirectStart) > 1:									
					return idListSectionsOrderedVariantTrack, idSectionsListDirect + idSectionsListIndirect, 13, gapList, modificationSet, idListSectionsModified	# Plusieurs codes -1 >>> erreur
				if len(idSectionsListDirectStart + idSectionsListIndirectStart) == 1:
					idSectionsListDirect = idSectionsListDirectStart.copy()																							# 1 seul code -1 >>> reduire à ce section
					idSectionsListIndirect = idSectionsListIndirectStart.copy()
	
#			Ajout facile s'il n'y en a qu'une section possible

			if len(idSectionsListDirect + idSectionsListIndirect) == 1:
				idSection, direct = (idSectionsListDirect[0], True) if len(idSectionsListDirect) == 1 else (idSectionsListIndirect[0], False)
				idSectionCurrentVariantTrack, lastPointCurrentVariantTrack = appendNextVariantSection(idSectionCurrentVariantTrack, lastPointCurrentVariantTrack, idSection, direct)

#			Plusieurs possibilités - Calculer les priorités pour les cas Y 

			else:
				priorityListDirect = [priorityDicoGrListInfos[code][idSection][C_bifurcationNum] for idSection in idSectionsListDirect]
				priorityListIndirect = [priorityDicoGrListInfos[code][idSection][C_bifurcationNum] for idSection in idSectionsListIndirect]
				priorityBest = min(priorityListDirect + priorityListIndirect)													# Min because -Y1 has priority on -Y2 ...
					
				if (priorityListDirect + priorityListIndirect).count(priorityBest) > 1:
					return idListSectionsOrderedVariantTrack, idSectionsListDirect + idSectionsListIndirect, 15, gapList, modificationSet, idListSectionsModified

				idSection, direct = (idSectionsListDirect[priorityListDirect.index(priorityBest)], True) if priorityBest in priorityListDirect else (idSectionsListIndirect[priorityListIndirect.index(priorityBest)], False)
				idSectionCurrentVariantTrack, lastPointCurrentVariantTrack = appendNextVariantSection(idSectionCurrentVariantTrack, lastPointCurrentVariantTrack, idSection, direct)

			if priorityDicoInside[code] : backwardReturn = True
			anyVariantsectionFound = True
			variantsectionFound = True  																					
			break																										

#		Dans le cas ou le dernier section est sur variante, continuer la recherche

		if variantsectionFound: continue

#		Dans le cas ou on a encore trouvé aucune variante, continuer une section sur la RB de Base

		if not anyVariantsectionFound:
			idSectionCurrentVariantTrack, direct = idListSectionsOrderedBaseTrack[indexOnBaseTrack], idListSectionsOrderedBaseTrack[indexOnBaseTrack] > 0
			lastPointCurrentVariantTrack = dicoSectionsFeaturesEndPoints[abs(idSectionCurrentVariantTrack)][1] if direct else dicoSectionsFeaturesEndPoints[abs(idSectionCurrentVariantTrack)][0]
			idListSectionsOrderedVariantTrack.append(idSectionCurrentVariantTrack)
			indexOnBaseTrack += 1					
					
#			Terminer si on est revenu au début par la RB de Base - Sinon continuer la recherche			
					
			if indexOnBaseTrack == len(idListSectionsOrderedBaseTrack):
				return idListSectionsOrderedVariantTrack, [], 0, gapList, modificationSet, idListSectionsModified

			continue		

#		Note assertion : variantsectionFound == False  AND  anyVariantsectionFound == True

#		Terminer si on est de retour au départ

		if startPointCurrentVariantTrack.distance(lastPointCurrentVariantTrack) <= QGP.configMatchDistanceShort: 
			return idListSectionsOrderedVariantTrack, [], 0, gapList, modificationSet, idListSectionsModified	

#		Retrouver où on est sur le parcours de base (depuis le début car on peut être revenu en arrière)

		indexA = indexB = None
		for i in range(indexOnBaseTrackAfterVariant, len(idListSectionsOrderedBaseTrack)):
			idSection, direct = abs(idListSectionsOrderedBaseTrack[i]), idListSectionsOrderedBaseTrack[i] > 0
			pointA = dicoSectionsFeaturesEndPoints[idSection][0] if direct else dicoSectionsFeaturesEndPoints[idSection][1] 
			distance = pointA.distance(lastPointCurrentVariantTrack)
			if distance <= 1 : indexA = i; break											# Stop searching at first found
			if distance <= QGP.configMatchDistanceShort : indexB = i						# In case non close but continue searching
		indexA = indexB if indexA == None else indexA

#		Si on a pas retrouvé, c'est une erreur parce que ni variant ni tracé de base ne suit

		if indexA == None:
			idListLost = set(); 
			for code in priorityDicoidSectionsList: idListLost |= priorityDicoidSectionsList[code]
			idListLost = list(idListLost)
			return idListSectionsOrderedVariantTrack, idListLost, 14, gapList, modificationSet, idListSectionsModified

#		Terminer le parcours si on est en mode arrière en s'arretant si on passe au départ

		if backwardReturn:
			for idSection in reversed(idListSectionsOrderedBaseTrack[0:indexA]):
				if startPointCurrentVariantTrack.distance(lastPointCurrentVariantTrack) <= QGP.configMatchDistanceShort: break
				idListSectionsOrderedVariantTrack.append(-idSection)
				lastPointCurrentVariantTrack = dicoSectionsFeaturesEndPoints[abs(idSection)][1] if idSection < 0 else dicoSectionsFeaturesEndPoints[abs(idSection)][0]
			return idListSectionsOrderedVariantTrack, [], 0, gapList, modificationSet, idListSectionsModified		

#		Ajouter la section suivante du parcours principal

		indexOnBaseTrackAfterVariant = indexA
#		print ('computeTracksOrderedSections - indexOnBaseTrackAfterVariant = ' + str(indexOnBaseTrackAfterVariant))

		idSectionCurrentVariantTrack, direct = idListSectionsOrderedBaseTrack[indexOnBaseTrackAfterVariant], idListSectionsOrderedBaseTrack[indexOnBaseTrackAfterVariant] > 0
		lastPointCurrentVariantTrack = dicoSectionsFeaturesEndPoints[abs(idSectionCurrentVariantTrack)][1] if direct else dicoSectionsFeaturesEndPoints[abs(idSectionCurrentVariantTrack)][0]
		idListSectionsOrderedVariantTrack.append(idSectionCurrentVariantTrack)
		indexOnBaseTrackAfterVariant += 1					

#		Terminer si on est revenu au début par la RB de Base - Sinon continuer la recherche			
				
		if indexOnBaseTrackAfterVariant == len(idListSectionsOrderedBaseTrack):
			return idListSectionsOrderedVariantTrack, [], 0, gapList, modificationSet, idListSectionsModified	
				
				
# ========================================================================================
# Ajouter 1 Tracé à la Couche Parcours GR / Parcours RB 
#  >>> layerTrack	  		: QgsVectorLayer				Parcours-GR ou Parcours-RB
#  >>> trackBaseFeature 	: QgsFeature					Entité de base à copier avec le nouveau code
#  >>> trackNewCode			: str							Code du nouveau parcours
#  >>> trackNameSuffix		: str							A ajouter au nom du parcours
#  <<< status				: bool
# ========================================================================================
		
def addTrackFeatureToTable(layerTrack, trackBaseFeature, trackNewCode, trackNameSuffix = ''):

	newTrackFeature = QgsFeature(layerTrack.fields())																		# Définir la nouvelle entité
	newTrackFeature.setAttribute(QGP.tableTracksFieldCode, trackNewCode)													# Avec le nouveau code
	newTrackFeature.setAttribute(QGP.tableTracksFieldName, trackBaseFeature[QGP.tableTracksFieldName] + trackNameSuffix)	# Même Nom + suffixe
	newTrackFeature.setAttribute(QGP.tableTracksFieldStatus, trackBaseFeature[QGP.tableTracksFieldStatus])					# Même Statut
	newTrackFeature.setGeometry(QgsGeometry())																				# Mais définir une géommétrie nulle

	layerTrack.startEditing()
	status = layerTrack.addFeature(newTrackFeature)
	layerTrack.commitChanges()

	return status


# ========================================================================================
# Supprimer 1 Tracé à la Couche Parcours GR / Parcours RB 
#  >>> layerTrack	  		: QgsVectorLayer				Parcours-GR ou Parcours-RB
#  >>> trackBaseFeature 	: QgsFeature					Entité de base à copier avec le nouveau code
#  <<< status				: bool
# ========================================================================================
		
def removeTrackFeatureToTable(layerTrack, trackBaseFeature):

	layerTrack.startEditing()
	status = layerTrack.deleteFeature(trackBaseFeature.id())
	layerTrack.commitChanges()

	return status


# ========================================================================================
# --- THE END ---
# ========================================================================================

