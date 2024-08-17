# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Utilitaires pour la Création du Plan des distances des RB
# ========================================================================================

from qgis.core import *
from qgis.gui import *

import importlib

import QCarto_Tools_Coding as TCOD
importlib.reload(TCOD)
import QCarto_Tools_SCR as TSCR
importlib.reload(TSCR)
import QCarto_Tools_IGN as TIGN
importlib.reload(TIGN)

import QCarto_Definitions_Symbologie as DSYM
importlib.reload(DSYM)

import QCarto_Parameters_Global
importlib.reload(QCarto_Parameters_Global)
QGP = QCarto_Parameters_Global.globalParameters()


# ========================================================================================
# Créer les dictionnaires utilisés pour générer le CSV du Plan des distances RB
# >>> mainFrame :								Main menu frame : pour messages
# >>> listTracksSelectedCodes 	: [trackCode]	Liste des codes sélectionnés à la page parcours
# >>> dicoTracksComputeResults 	: dico   		Résultats des calculs pour les parcours sélectionnés
# >>> dicoSectionsGRFeatures 	: dico			Dictionnaire des Tronçons
#
# <<< status : bool								Génération correcte ou non
# ========================================================================================

class infosRBPlan():

	def __init__(self, mainFrame, listTracksSelectedCodes, dicoTracksComputeResults, dicoSectionsGRFeatures):
		self.mainFrame = mainFrame
		self.listTracksSelectedCodes = listTracksSelectedCodes
		self.dicoTracksComputeResults = dicoTracksComputeResults
		self.dicoSectionsGRFeatures = dicoSectionsGRFeatures

		self.dicoTrack = {}									# Info totaux des parcours
		self.dicoSegmentInfo = {}							# Infos par parcours, par segment
		self.dicoSegmentGeometry = {}						# Géométries uniques
		self.itineraryRB = None								# Itineraire de la RB
		self.itineraryRBMain = None							# Parcours principal
		self.startingPoint = None							# Point de départ de la RB

		self.dicoRBPlanDistances = {}						# Dictionnaire résultat
		self.dicoRBPlanCommonTracksList = {}				# Parcours Commun


# ========================================================================================
# Définir l'itinéraire
# ========================================================================================

	def setItinerary(self):
		itineraryRBSet = set((TCOD.itineraryFromTrackCode(code)) for code in self.listTracksSelectedCodes)
		if len(itineraryRBSet) != 1: return	False																						# Works only for a single RB
		self.itineraryRB = itineraryRBSet.pop()
		if not TCOD.itineraryTypeFromTrackCode(self.itineraryRB) in QGP.typeSetComputeRBMode : return False								# Works only for RB or like
		if self.mainFrame.debugModeQCartoLevel >= 0 : print('infosRBPlan - itineraryRB : ' + self.itineraryRB)
		return True


# ========================================================================================
# Définir l'itinéraire de base
# ========================================================================================

	def setMainItinerary(self):
		if self.itineraryRB in self.listTracksSelectedCodes:
			self.itineraryRBMain = self.itineraryRB
		elif self.itineraryRB + '-MF' in self.listTracksSelectedCodes:
			self.itineraryRBMain = self.itineraryRB + '-MF'
		elif self.itineraryRB + '-MT' in self.listTracksSelectedCodes:
			self.itineraryRBMain = self.itineraryRB + '-MT'
		else:
			return False	

		if self.mainFrame.debugModeQCartoLevel >= 0 : print('infosRBPlan - itineraryRBMain : ' + self.itineraryRBMain)
		return True

# ========================================================================================
# Déterminer les infos de base par segment : repères 
# Condidérés comme tel si la distance de Hausdorff est > 10 m
# ========================================================================================

	def setTrackGeometries(self, code):
		self.dicoSegmentInfo[code] = {}
		reperePositions = self.dicoTracksComputeResults[code][QGP.tableTracksIFieldReperesPos]
		if code == self.itineraryRBMain: self.startingPoint = reperePositions[0][0] 
		trackLineXYZ = self.dicoTracksComputeResults[code][QGP.tableTracksIFieldTrackXYZ]
		for segmentNum in range(1, len(reperePositions)) :
			self.dicoSegmentInfo[code][segmentNum] = {}
			self.dicoSegmentInfo[code][segmentNum]['RepereFrom'] = reperePositions[segmentNum-1][0][QGP.tablePointsFieldRepere]
			self.dicoSegmentInfo[code][segmentNum]['RepereTo'] = reperePositions[segmentNum][0][QGP.tablePointsFieldRepere]
			self.dicoSegmentInfo[code][segmentNum]['Geometry'] = QgsGeometry.fromPolyline(trackLineXYZ[reperePositions[segmentNum-1][1]:reperePositions[segmentNum][1]+1])
			self.dicoSegmentInfo[code][segmentNum]['Length'] = self.dicoSegmentInfo[code][segmentNum]['Geometry'].length()
			if self.mainFrame.debugModeQCartoLevel >= 0 : print('infosRBPlan - Code = ' + code + ' : ' + self.dicoSegmentInfo[code][segmentNum]['RepereFrom'] + ' >>> ' + \
															self.dicoSegmentInfo[code][segmentNum]['RepereTo'] + ' = ' + str(round(self.dicoSegmentInfo[code][segmentNum]['Length'])))

# ========================================================================================
# Déterminer quelles sont vraiment les segments différents
# Condidérés comme tel si la distance de Hausdorff est > 10 m
# ========================================================================================

	def analyseTrackGeometries(self):
		for code in self.dicoSegmentInfo:
			for segmentNum in self.dicoSegmentInfo[code] :
				geometry = self.dicoSegmentInfo[code][segmentNum]['Geometry']
				for wayNum in self.dicoSegmentGeometry:
					if geometry.hausdorffDistance(self.dicoSegmentGeometry[wayNum]['Geometry']) <= 10: 
						self.dicoSegmentInfo[code][segmentNum]['Waynum'] = wayNum
						break
				if 'Waynum'	not in self.dicoSegmentInfo[code][segmentNum] :
					wayNum = len(self.dicoSegmentGeometry)
					self.dicoSegmentGeometry[wayNum] = {}
					self.dicoSegmentGeometry[wayNum]['Geometry'] = geometry
					self.dicoSegmentInfo[code][segmentNum]['Waynum'] = wayNum
				if self.mainFrame.debugModeQCartoLevel >= 0 : print('infosRBPlan - Code = ' + code + ' : ' + self.dicoSegmentInfo[code][segmentNum]['RepereFrom'] + ' >>> ' + \
																self.dicoSegmentInfo[code][segmentNum]['RepereTo'] + ' - wayNum = ' + str(wayNum))
	
# ========================================================================================
# Déterminer les distances arrondies à l'hectomètre, par segment par segment unique
# ========================================================================================

	def initSegmentDistances(self):
		for wayNum in self.dicoSegmentGeometry:
			self.dicoSegmentGeometry[wayNum]['HmDist'] = int(self.dicoSegmentGeometry[wayNum]['Geometry'].length() / 100)
			self.dicoSegmentGeometry[wayNum]['HmFrac'] = (self.dicoSegmentGeometry[wayNum]['Geometry'].length() / 100) % 1
			self.dicoSegmentGeometry[wayNum]['Fixed'] = False
			self.dicoSegmentGeometry[wayNum]['Shown'] = False
			if self.mainFrame.debugModeQCartoLevel >= 0 : print('dicoGeometry - WayNum = ' + str(wayNum) + ' : ' + str(self.dicoSegmentGeometry[wayNum]['HmDist']) + ' hm ' + str(self.dicoSegmentGeometry[wayNum]['HmFrac']))

# ========================================================================================
# Déterminer les distances totales arrondies à l'hectomètre, pour chaque parcours
# ========================================================================================

	def initTrackTotals(self):
		for code in self.dicoSegmentInfo:
			distanceTotal = sum(self.dicoSegmentGeometry[self.dicoSegmentInfo[code][segmentNum]['Waynum']]['Geometry'].length() for segmentNum in self.dicoSegmentInfo[code])
			self.dicoTrack[code] = round(distanceTotal / 100)
			if self.mainFrame.debugModeQCartoLevel >= 0 : print('infosRBPlan - Code Total = ' + code + ' : ' + str(self.dicoTrack[code]) + ' hm ')

# ========================================================================================
# Ajuster les distances
# ========================================================================================

	def adjustSegmentDistances(self):

		def increaseHigherFrac(code):
			wayNumList = [ self.dicoSegmentInfo[code][segmentNum]['Waynum'] for segmentNum in self.dicoSegmentInfo[code] ]
			wayTarget = max (wayNumList, key = lambda x : self.dicoSegmentGeometry[x]['HmFrac'] if not self.dicoSegmentGeometry[x]['Fixed'] else -999)
			if self.dicoSegmentGeometry[wayTarget]['Fixed'] : return False
			self.dicoSegmentGeometry[wayTarget]['Fixed'] = True					
			self.dicoSegmentGeometry[wayTarget]['HmDist'] += 1			
			if self.mainFrame.debugModeQCartoLevel >= 0 : print('increaseHigherFrac : ' + str(wayTarget) + ' = ' + str(self.dicoSegmentGeometry[wayTarget]['HmDist']) + ' hm')
			return True

		for code in [self.itineraryRBMain] + sorted([code for code in self.dicoTrack if code != self.itineraryRBMain]) :
			targetTotal = self.dicoTrack[code]
			while True :																																					# Loop until Total is OK
				currentTotal = sum(self.dicoSegmentGeometry[self.dicoSegmentInfo[code][segmentNum]['Waynum']]['HmDist'] for segmentNum in self.dicoSegmentInfo[code])
				if self.mainFrame.debugModeQCartoLevel >= 0 : print('infosRBPlan Adjust - Code Current / Total = ' + code + ' : ' + str(self.dicoTrack[code]) + ' / ' + str(currentTotal) + ' hm ')
				if currentTotal == targetTotal : break
				if currentTotal >  targetTotal : 
					self.dicoTrack[code] += 1; break
				if increaseHigherFrac(code)	: continue
				self.dicoTrack[code] = currentTotal; break
			for segmentNum in self.dicoSegmentInfo[code] : self.dicoSegmentGeometry[self.dicoSegmentInfo[code][segmentNum]['Waynum']]['Fixed'] = True				# 7.15 - Fix - Changes are no longer allowed

# ========================================================================================
# Définir le dictionnaire complet
# ========================================================================================

	def generateCompleteDicoPlan(self):
	
#	Informations Départ

		lat, lon = TSCR.convertPoint3812toWgs84(self.startingPoint.geometry().asPoint().x(), self.startingPoint.geometry().asPoint().y())
		latD, latM, latS = TSCR.latOrLong2DMS(lat) ; lonD, lonM, lonS = TSCR.latOrLong2DMS(lon)
		self.dicoRBPlanDistances[' Départ'] = {}																		# Warning index ' Départ' is with 255 space to be last when sorted
		self.dicoRBPlanDistances[' Départ']['Lat - Long'] = '{:d}° {:02d}\' {:04.1f}" N , {:d}° {:02d}\' {:04.1f}" E'.format(latD, latM, latS, lonD, lonM, lonS)
		self.dicoRBPlanDistances[' Départ']['Dénivelé'] = self.dicoTracksComputeResults[self.itineraryRBMain][QGP.tableTracksFieldDenivelePos]
		self.dicoRBPlanDistances[' Départ']['Altitude Min'] = self.dicoTracksComputeResults[self.itineraryRBMain][QGP.tableTracksFieldAltmin]
		self.dicoRBPlanDistances[' Départ']['Altitude Max'] = self.dicoTracksComputeResults[self.itineraryRBMain][QGP.tableTracksFieldAltmax]
	
#	Distances	
	
		indexShownList = []
	
		for code in [self.itineraryRBMain] + sorted([code for code in self.dicoTrack if code != self.itineraryRBMain]) :
			self.dicoRBPlanDistances[code] = {}																
			for segmentNum in self.dicoSegmentInfo[code] :
				wayNum = self.dicoSegmentInfo[code][segmentNum]['Waynum']
				index = self.dicoSegmentInfo[code][segmentNum]['RepereFrom'] + ' >>> ' + self.dicoSegmentInfo[code][segmentNum]['RepereTo']
				if code != self.itineraryRBMain and index in indexShownList and self.dicoSegmentGeometry[wayNum]['Shown'] : continue
				self.dicoSegmentGeometry[wayNum]['Shown'] = True
				self.dicoRBPlanDistances[code][index] = self.dicoSegmentGeometry[wayNum]['HmDist'] / 10
				indexShownList.append(index)
			self.dicoRBPlanDistances[code]['Total']	= self.dicoTrack[code] / 10
			if code != self.itineraryRBMain : self.dicoRBPlanDistances[code]['Différence'] = abs(self.dicoTrack[code] - self.dicoTrack[self.itineraryRBMain]) / 10

#	Cartes IGN

		listMapsIGN = []
		for code in self.listTracksSelectedCodes:
			for point in self.dicoTracksComputeResults[code][QGP.tableTracksIFieldReperesPos] :
				mapNumber, mapName = TIGN.convertPoint3812toTopo25(point[0])				
				if mapNumber != None and [mapNumber, mapName] not in listMapsIGN : listMapsIGN.append([mapNumber, mapName])

		self.dicoRBPlanDistances[' IGN 1:25000'] = {}																			
		for mapNum, map in zip(range(len(listMapsIGN)), listMapsIGN) :
			self.dicoRBPlanDistances[' IGN 1:25000']['Carte ' + str(mapNum + 1)] = map[0] + ' \u00AB' + ' ' + map[1] + ' \u00BB'			# Warning index ' IGN' is with 255 space to be last when sorted

		return self.dicoRBPlanDistances


# ========================================================================================
# Définir les parcours communs sur chaque segment
# ========================================================================================

	def generateSegmentCommonTracksDico(self):
		for code in self.listTracksSelectedCodes:
			self.dicoRBPlanCommonTracksList[code] = {}
			reperesPositions = self.dicoTracksComputeResults[code][QGP.tableTracksIFieldReperesPos]
			for pointNum in range(1, len(reperesPositions)) :
				index =  str(reperesPositions[pointNum-1][0][QGP.tablePointsFieldRepere]) + ' >>> ' + str(reperesPositions[pointNum][0][QGP.tablePointsFieldRepere])
				sectionList = self.dicoTracksComputeResults[code][QGP.tableTracksIFieldReperesSectionList][pointNum-1]
				if sectionList == None : self.dicoRBPlanCommonTracksList[code][index] = '--?--' ; continue
				repereTrackList = [] ; lastSectionTrackList = None
				for sectionId in sectionList:
					sectionTrackList = [] ; sectionFeature = self.dicoSectionsGRFeatures[abs(sectionId)]
					codeList = TCOD.getCodeListGRFromSectionFeature(sectionFeature)
					for gr_code in codeList: 
						valid, type, label, zone, number, itineraryCode, trackBaseCode, trackCode, modificationList, invalidationList, repeatCount, bifurcationNumber, direction = TCOD.elementsFromGrCode(gr_code)		
						if not valid : continue
						if not DSYM.isSectionGrCodeMarked(self.mainFrame, gr_code) : continue
						trackCodeParts = trackCode.split('-')
						if len(trackCodeParts) == 2 or (len(trackCodeParts) == 3 and trackCodeParts[2][0] == 'P') :	
							sectionTrackList.append(trackCodeParts[1])
						elif len(trackCodeParts) == 3 :
							sectionTrackList.append(trackCodeParts[1] + '-' + trackCodeParts[2][0])
						else:
							sectionTrackList.append('?')
					sectionTrackList = sorted(list(set(sectionTrackList)))
					if sectionTrackList != lastSectionTrackList : repereTrackList.append(sectionTrackList) ; lastSectionTrackList = sectionTrackList
				textList = []
				for sectionList in repereTrackList :
					textList.append(' '.join(gr for gr in sectionList) if sectionList != [] else '──')
				self.dicoRBPlanCommonTracksList[code][index] = (' ║ '.join(text for text in textList)) if any(text != '──' for text in textList) else '──'
				if self.mainFrame.debugModeQCartoLevel >= 0 : print('Common Tracks - Code / Index = ' + code + ' / ' + index + ' = ' + str(self.dicoRBPlanCommonTracksList[code][index]))
		return self.dicoRBPlanCommonTracksList		


# ========================================================================================
# Main Procédure
# ========================================================================================

def createRBPlan(mainFrame, listTracksSelectedCodes, dicoTracksComputeResults, dicoSectionsGRFeatures):

	if mainFrame.debugModeQCartoLevel >= 2 : print('createRBPlan : Start ...')
	if mainFrame.debugModeQCartoLevel >= 2 : print('createRBPlan : ' + str(listTracksSelectedCodes))
	
#	Rejeter la demande si les calculs ne sont pas corrects

	for code in listTracksSelectedCodes:
		if dicoTracksComputeResults[code][QGP.tableTracksIFieldErrorCode] != 0:   return {}, {}							# Works only if correctly computed
		if dicoTracksComputeResults[code][QGP.tableTracksIFieldReperesPos] == [] : return {}, {}						# Works only if points found

#	Créer la classe des distionnaires

	infosRB = infosRBPlan(mainFrame, listTracksSelectedCodes, dicoTracksComputeResults, dicoSectionsGRFeatures)

#	Déterminer la RB concernée 	

	if not infosRB.setItinerary() : return {}, {}	

#	Déterminer l'itinéraire principal - attention aux cas des modifications futures ou temporaires

	if not infosRB.setMainItinerary() : return {}, {}	

#	Extraire la géométrie pour chaque segment

	for code in listTracksSelectedCodes : infosRB.setTrackGeometries(code)

#	Déterminer les segments identiques
		
	infosRB.analyseTrackGeometries()

#	Déterminer les distances hectométriques de base

	infosRB.initSegmentDistances()

#	Définir les totaux par parcours

	infosRB.initTrackTotals()
	
#	Ajuster les distances des segments	

	infosRB.adjustSegmentDistances()
	
#	Générer le diconnaire complet

	dicoRBPlanDistances = infosRB.generateCompleteDicoPlan()

#	Générer le dico des parcours communs

	dicoRBPlanCommonTracksList = infosRB.generateSegmentCommonTracksDico()

	return dicoRBPlanDistances, dicoRBPlanCommonTracksList


# ========================================================================================
# --- THE END ---
# ========================================================================================
