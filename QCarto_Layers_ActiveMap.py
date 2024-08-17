# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Utilitaires pour la Gestion des Couches de la Carte Active
# ========================================================================================

from qgis.core import *
from qgis.gui import *

import importlib

import QCarto_Tools_Coding as TCOD
importlib.reload(TCOD)

import QCarto_Parameters_Global
QGP = QCarto_Parameters_Global.globalParameters()


# ========================================================================================
# Déterminer les tronçons effectifs pour la carte active
#  >>> activeMapItineraryCode			: str						Code de l'itinéraire de la carte
#  >>> activeMapSectionFeaturesList 	: [QgsFeature]				Liste des tronçons dans l'emprise de la carte
#  >>> activeMapModifcationsList		: [[][]]					Liste de 2 listes : (1) modifications T / F sur itinéraire // (2) modifications sur autres GR
#  <<< itinerarySectionFeaturesList 	: [QgsFeature]				Tronçons sur l'itinéraire principal
#  <<< otherSectionFeaturesList 		: [QgsFeature]				Tronçons sur les autres GR.P.T
# ========================================================================================

def getActiveMapEffectiveSectionsFeatures(activeMapItineraryCode, activeMapSectionFeaturesList, activeMapModifcationsList):

	activeMapSectionFeaturesRemainingList = activeMapSectionFeaturesList.copy()
	itinerarySectionFeaturesList = []
	otherSectionFeaturesList = []

	for sectionFeature in activeMapSectionFeaturesList:
		codeList = TCOD.getCodeListALLFromSectionFeature(sectionFeature)
		for gr_code in codeList:
			valid, type, label, zone, number, itineraryCode, trackBaseCode, trackCode, modificationList, invalidationList, repeatCount, bifurcationNumber, direction = TCOD.elementsFromGrCode(gr_code)
			if not valid: continue
			if itineraryCode != activeMapItineraryCode: continue											# Not on itinerary
			if '0' in invalidationList: continue 															# -#0 always excluded
			if 'A' in invalidationList: continue 															# -#A always excluded
			if any(tag not in activeMapModifcationsList[0] for tag in modificationList) : continue			# Modification not requested on section
			if any(tag in invalidationList for tag in activeMapModifcationsList[0]) : continue				# Invalidation on section for requested modification
			itinerarySectionFeaturesList.append(sectionFeature)	
			activeMapSectionFeaturesRemainingList.remove(sectionFeature)
			break

	for sectionFeature in activeMapSectionFeaturesRemainingList:
		codeList = TCOD.getCodeListALLFromSectionFeature(sectionFeature)
		for gr_code in codeList:
			valid, type, label, zone, number, itineraryCode, trackBaseCode, trackCode, modificationList, invalidationList, repeatCount, bifurcationNumber, direction = TCOD.elementsFromGrCode(gr_code)
			if not valid: continue
			if itineraryCode == activeMapItineraryCode: continue											# Those on itinerary has been managed above (possible in case of modification)
			if type not in ('GR', 'GRP', 'GRT'): continue
			if '0' in invalidationList: continue 															# -#0 always excluded
			if 'A' in invalidationList: continue 															# -#A always excluded
			if any(tag not in activeMapModifcationsList[1] for tag in modificationList) : continue			# Modification not requested on section
			if any(tag in invalidationList for tag in activeMapModifcationsList[1]) : continue				# Invalidation on section for requested modification
			otherSectionFeaturesList.append(sectionFeature)	
			break

	return 	itinerarySectionFeaturesList, otherSectionFeaturesList		
	

# ========================================================================================
# Déterminer le type de parcours sur un tronçon
#  >>> sectionFeature	 	: QgsFeature			Tronçon à évaluer
#  >>> itineraryActiveMap	: str					Code de l'itinéraire évalué / None pour les autres GR
#  <<< type 				: char					Dans l'odre des priorités :
#														P : Parcours principal
#														V : Variante
#														A : Allongement
#														J : Jour
#														L : Liaison
#														R : Raccourci
#														B : Boucle
#														- : Non trouvé
# ========================================================================================	
	
def getSectionFeatureType(sectionFeature, itineraryActiveMap):

	sectionTypes = set()

	codeList = TCOD.getCodeListALLFromSectionFeature(sectionFeature)
	for gr_code in codeList:
		valid, type, label, zone, number, itineraryCode, trackBaseCode, trackCode, modificationList, invalidationList, repeatCount, bifurcationNumber, direction = TCOD.elementsFromGrCode(gr_code)
		if not valid: continue

		if itineraryActiveMap != None:											# Cas de la détermination pour l'itinéraire principal
			if itineraryActiveMap != itineraryCode: continue
			if type in ('GR', 'GRP', 'GRT'): 
				if TCOD.isCodePrincipalGR(trackCode) 	: sectionTypes.add('P')
				if TCOD.isCodeVarianteGR(trackCode) 	: sectionTypes.add('V')
				if TCOD.isCodeLiaisonGR(trackCode) 		: sectionTypes.add('L')
				if TCOD.isCodeBoucleGR(trackCode) 		: sectionTypes.add('B')
			if type in ('RB', 'RF', 'RL', 'RI', 'IR'): 
				if TCOD.isCodeBaseRB(trackCode) 		: sectionTypes.add('P')
				if TCOD.isCodeVariantRB(trackCode) 		: sectionTypes.add('V')
				if TCOD.isCodeElongationRB(trackCode) 	: sectionTypes.add('A')
				if TCOD.isCodeShorcutRB(trackCode) 		: sectionTypes.add('R')
				if TCOD.isCodeDayRB(trackCode) 			: sectionTypes.add('J')

		else:																	# Cas des Autres GR
			if type not in ('GR', 'GRP', 'GRT'): continue
			if TCOD.isCodePrincipalGR(trackCode) 	: sectionTypes.add('P')
			if TCOD.isCodeVarianteGR(trackCode) 	: sectionTypes.add('V')
			if TCOD.isCodeLiaisonGR(trackCode) 		: sectionTypes.add('L')
			if TCOD.isCodeBoucleGR(trackCode) 		: sectionTypes.add('B')

	for letter in ('P', 'R', 'V', 'A', 'J', 'L', 'B'):
		if letter in sectionTypes : return letter

	return '-'


# ========================================================================================
# Remplacer la géométrie des Tronçons par celle de ces mêmes tronçons sur une autre couche
# >>> layerActiveMapSections		: QgsVectorLayer			Couche des tronçons de la carte active
# >>> layerReplacementSections		: QgsVectorLayer			Couche des tronçons définis sur le fond de carte effectif
# <<< Nombre de tronçons remplacés
# ========================================================================================

def substituteActiveMapSections(layerActiveMapSections, layerReplacementSections):
	
	if layerReplacementSections == None: return None

# Scanner les entités, et remplacer si possible

	countReplace = 0
	layerActiveMapSections.startEditing()
	
	for feature in layerActiveMapSections.getFeatures():
		sectionId = feature[QGP.tableMapSectionsFieldSections]
		expression = '"' + QGP.tableSections50KFieldId + '"' + ' = ' + str(sectionId)
		featureList = [f for f in layerReplacementSections.getFeatures(expression)]
		if len(featureList) != 1: continue
		replacementFeature = featureList[0]
		replacementGeometry = replacementFeature.geometry()
		distance = feature.geometry().hausdorffDistance(replacementGeometry)
		if distance < 1: continue
		if distance > QGP.config50KDeltaMaxWarning: continue
		layerActiveMapSections.changeGeometry(feature.id(), replacementGeometry)
		countReplace += 1
	
	layerActiveMapSections.commitChanges()			

	return countReplace


# ========================================================================================
# Analyser les Features des Tronçons de la Carte Active et regrouper les lignes contigües de même symbologie
# >>> layerActiveMapSections		: QgsVectorLayer			Couche des tronçons de la carte active
# ========================================================================================

def mergeActiveMapSections(layerActiveMapSections):

#	Créer la liste des tronçons et le dictionnaire d'état

	dicoSectionsFeatures 		= {feature.id() : feature for feature in layerActiveMapSections.getFeatures()}
	dicoSectionsStates 			= {id : 'Available' for id in dicoSectionsFeatures}
	dicoSectionsLines 			= {id : dicoSectionsFeatures[id].geometry().asMultiPolyline()[0] for id in dicoSectionsFeatures}
	dicoSectionsSectionsList 	= {id : [int(dicoSectionsFeatures[id][QGP.tableMapSectionsFieldSections])] for id in dicoSectionsFeatures}

#	Boucler tant qu'il est possible de combiner des tronçons A et B

	while True:
	
#		Trouver un tronçon candidat A	

		sectionId_A = None
		for sectionId in dicoSectionsFeatures:
			if dicoSectionsStates[sectionId] != 'Available': continue
			sectionId_A = sectionId
			break

		if sectionId_A == None: break

#		Trouver un tronçon candidat B

		sectionId_B = None
		for sectionId in dicoSectionsFeatures:
			if sectionId == sectionId_A: continue
			if dicoSectionsStates[sectionId] != 'Available': continue
			if dicoSectionsFeatures[sectionId_A][QGP.tableMapSectionsFieldSymbol] != dicoSectionsFeatures[sectionId][QGP.tableMapSectionsFieldSymbol]: continue
			sectionId_B = sectionId

			point_A_A = dicoSectionsLines[sectionId_A][0]
			point_A_Z = dicoSectionsLines[sectionId_A][-1]
			point_B_A = dicoSectionsLines[sectionId_B][0]
			point_B_Z = dicoSectionsLines[sectionId_B][-1]

#			Voir si A et B collent exactement

			if point_A_Z == point_B_A:
				dicoSectionsLines[sectionId_A] += dicoSectionsLines[sectionId_B][1:]
				dicoSectionsSectionsList[sectionId_A] += dicoSectionsSectionsList[sectionId_B]
				dicoSectionsStates[sectionId_B] = 'Removed'
				break
			if point_A_Z == point_B_Z:
				dicoSectionsLines[sectionId_A] += list(reversed(dicoSectionsLines[sectionId_B]))[1:]
				dicoSectionsSectionsList[sectionId_A] += dicoSectionsSectionsList[sectionId_B]
				dicoSectionsStates[sectionId_B] = 'Removed'
				break
			if point_A_A == point_B_Z:
				dicoSectionsLines[sectionId_A] = dicoSectionsLines[sectionId_B] + dicoSectionsLines[sectionId_A][1:]
				dicoSectionsSectionsList[sectionId_A] = dicoSectionsSectionsList[sectionId_B] + dicoSectionsSectionsList[sectionId_A]
				dicoSectionsStates[sectionId_B] = 'Removed'
				break
			if point_A_A == point_B_A:
				dicoSectionsLines[sectionId_A] = list(reversed(dicoSectionsLines[sectionId_B])) + dicoSectionsLines[sectionId_A][1:]
				dicoSectionsSectionsList[sectionId_A] = dicoSectionsSectionsList[sectionId_B] + dicoSectionsSectionsList[sectionId_A]
				dicoSectionsStates[sectionId_B] = 'Removed'
				break

#			Voir si A et B collent à courte distance

			if point_A_Z.distance(point_B_A) <= QGP.activeMapLinesMergeDistanceMax:
				dicoSectionsLines[sectionId_A] += dicoSectionsLines[sectionId_B]
				dicoSectionsSectionsList[sectionId_A] += dicoSectionsSectionsList[sectionId_B]
				dicoSectionsStates[sectionId_B] = 'Removed'
				break
			if point_A_Z.distance(point_B_Z) <= QGP.activeMapLinesMergeDistanceMax:
				dicoSectionsLines[sectionId_A] += dicoSectionsLines[sectionId_B][::-1]
				dicoSectionsSectionsList[sectionId_A] += dicoSectionsSectionsList[sectionId_B]
				dicoSectionsStates[sectionId_B] = 'Removed'
				break
			if point_A_A.distance(point_B_Z) <= QGP.activeMapLinesMergeDistanceMax:
				dicoSectionsLines[sectionId_A] = dicoSectionsLines[sectionId_B] + dicoSectionsLines[sectionId_A]
				dicoSectionsSectionsList[sectionId_A] = dicoSectionsSectionsList[sectionId_B] + dicoSectionsSectionsList[sectionId_A]
				dicoSectionsStates[sectionId_B] = 'Removed'
				break
			if point_A_A.distance(point_B_A) <= QGP.activeMapLinesMergeDistanceMax:
				dicoSectionsLines[sectionId_A] = dicoSectionsLines[sectionId_B][::-1] + dicoSectionsLines[sectionId_A]
				dicoSectionsSectionsList[sectionId_A] = dicoSectionsSectionsList[sectionId_B] + dicoSectionsSectionsList[sectionId_A]
				dicoSectionsStates[sectionId_B] = 'Removed'
				break
				
			sectionId_B = None
	
#		Si aucun tronçon B ne colle : A est terminé

		if sectionId_B == None:
			dicoSectionsStates[sectionId_A] = 'Merged'
			continue
			
#	Mettre la couche à jour

	layerActiveMapSections.startEditing()

	for feature in layerActiveMapSections.getFeatures():
		if dicoSectionsStates[feature.id()] == 'Removed':
			layerActiveMapSections.changeAttributeValue(feature.id(), feature.fieldNameIndex(QGP.tableMapSectionsFieldSymbol), 0)
		layerActiveMapSections.changeAttributeValue(feature.id(), feature.fieldNameIndex(QGP.tableMapSectionsFieldState), dicoSectionsStates[feature.id()])
		layerActiveMapSections.changeAttributeValue(feature.id(), feature.fieldNameIndex(QGP.tableMapSectionsFieldSections), str(dicoSectionsSectionsList[feature.id()]))
		layerActiveMapSections.changeGeometry(feature.id(), QgsGeometry.fromMultiPolylineXY([dicoSectionsLines[feature.id()]]))
		
	layerActiveMapSections.commitChanges()


# ========================================================================================
# Raccourcir la géométrie des Lignes aux deux extrémités pour améliorer la cartes aux intersections
# >>> layerActiveMapSections		: QgsVectorLayer			Couche des tronçons de la carte active
# >>> cuttingDistance				: int						Distance de raccourcissement en mètres
# ========================================================================================

def shortenActiveMapSections(layerActiveMapSections, cuttingDistance):
				
	densificationDistance = QGP.activeMapLinesDensificationDistance

# Scanner les entités, et supprimer les points aux extrémités

	layerActiveMapSections.startEditing()
	
	for feature in layerActiveMapSections.getFeatures():
		if feature[QGP.tableMapSectionsFieldSymbol] == 0: continue
		newGeometry = feature.geometry().densifyByDistance(densificationDistance)
		newLine = newGeometry.asPolyline()

		for i in range(1,len(newLine)):
			if newLine[0].distance(newLine[i]) > cuttingDistance: break
		newLine = newLine[i:]
	
		newLine.reverse()
		for i in range(1,len(newLine)):
			if newLine[0].distance(newLine[i]) > cuttingDistance: break
		newLine = newLine[i:]
	
		if len(newLine) >= 2:
			newGeometry = QgsGeometry.fromMultiPolylineXY([newLine])
		else:
			newGeometry = QgsGeometry()
		layerActiveMapSections.changeGeometry(feature.id(), newGeometry)
	
	layerActiveMapSections.commitChanges()			

				
# ========================================================================================
# Orienter les lignes pour mettre l'extrémité libre (par rapport aux autres lignes) de l'autre coté
# >>> layerActiveMapSections		: QgsVectorLayer			Couche des tronçons de la carte active
# ========================================================================================

def turnActiveMapSections(layerActiveMapSections):
				
	featuresList = 	[feature for feature in layerActiveMapSections.getFeatures() if feature[QGP.tableMapSectionsFieldState]	!= 'Removed' and not feature.geometry().isNull()]	
	featuresList = sorted(featuresList, key = lambda f : f.geometry().length())
	
	layerActiveMapSections.startEditing()
	
	for featureNumber in range(len(featuresList)-1) : 
		pointA = featuresList[featureNumber].geometry().asMultiPolyline()[0][0]
		pointZ = featuresList[featureNumber].geometry().asMultiPolyline()[0][-1]
		distanceA = min([QgsGeometry.fromPointXY(pointA).distance(featuresList[num].geometry()) for num in range(featureNumber + 1, len(featuresList))])
		distanceZ = min([QgsGeometry.fromPointXY(pointZ).distance(featuresList[num].geometry()) for num in range(featureNumber + 1, len(featuresList))])
		if distanceZ < distanceA:
			lineGeometry = featuresList[featureNumber].geometry().asMultiPolyline()[0]
			lineGeometry.reverse()
			layerActiveMapSections.changeGeometry(featuresList[featureNumber].id(), QgsGeometry.fromMultiPolylineXY([lineGeometry]))
			
	layerActiveMapSections.commitChanges()			
				
				
# ========================================================================================
# --- THE END ---
# ========================================================================================	
				
				
				