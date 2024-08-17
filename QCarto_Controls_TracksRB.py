# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Vérifications de la Table Parcours-RB
# ========================================================================================

from qgis.core import *
from qgis.gui import *

import math
import time
import importlib

import QCarto_Layers_Tracks as LTRK
importlib.reload(LTRK)

import QCarto_Tools_Coding as TCOD
import QCarto_Tools_Progress as TPRO

import QCarto_Parameters_Global
QGP = QCarto_Parameters_Global.globalParameters()


# ========================================================================================
# Analyser les Attributs de la couche Tracés RB et afficher les erreurs
# >>> mainFrame 		: mainMenuFrame				Main Menu Class Object
# >>> controlFrame 		: menuControlsFrame			Control Frame Object
# >>> dicoBoutonsErreur : Dico						Dictionnaire des boutons d'erreur à mettre à jour
# >>> globalFlag 		: Bool						Analyse globale iff True - Analyse de la sélection courante iff False
# ========================================================================================

def analyseTracksRB(mainFrame, controlFrame, dicoBoutonsErreur, globalFlag):

	startTime = time.time()

# 	Initialiser les boutons

	for label in dicoBoutonsErreur:
		dicoBoutonsErreur[label].reset()

#	Dictionnaires des Parcours à analyser

	dicoTracksViewFeatures = {code : mainFrame.dicoTracksRBFeatures[code] for code in mainFrame.dicoTracksRBFeatures}
	dicoTrackSections = LTRK.generateDicoTracksSections('RB', dicoTracksViewFeatures, mainFrame.dicoSectionsGRFeatures)

#	Définir la liste des features à analyser 

	featureAnalysedList = [feature for feature in (mainFrame.layerTracksRB.getFeatures() if globalFlag else mainFrame.layerTracksRB.getSelectedFeatures())]

# Create Progress Bar

	progressBar = TPRO.createProgressBar(controlFrame.buttonControlAllTracksRB if globalFlag else controlFrame.buttonControlSelectionTracksRB, len(featureAnalysedList), 'Normal')

#	Analyser les entités de la table

	for featureTrack in featureAnalysedList :

#		Infos de l'entité

		featureTrackCode = featureTrack[QGP.tableTracksFieldCode]
		valid, type, label, zone, number, itineraryCode, trackBaseCode, trackCode, modificationList, invalidationList, repeatCount, bifurcationNumber, direction = TCOD.elementsFromGrCode(featureTrackCode)
		trackStatus = featureTrack[QGP.tableTracksFieldStatus]

#		Calcul des Totaux par type d'itinéraire

		dicoBoutonsErreur['T-ENT'].addError()	
		if type == 'RI'  :  dicoBoutonsErreur['T-RI'].addError()	
		if type == 'RB'  :  dicoBoutonsErreur['T-RB'].addError()	
		if type == 'RL' : 	dicoBoutonsErreur['T-RL'].addError()	
		if type == 'RF' : 	dicoBoutonsErreur['T-RF'].addError()	
		if type == 'IR' : 	dicoBoutonsErreur['T-IR'].addError()	
		dicoBoutonsErreur['T-KM'].addValue(featureTrack[QGP.tableTracksFieldDistance] /1000 if featureTrack[QGP.tableTracksFieldDistance] != None else 0)

#		Calcul des Totaux par principal / variante / liasison / boucle

		if TCOD.isCodeBaseRB(trackCode) : 		dicoBoutonsErreur['T-P'].addError(featureTrack)	
		if TCOD.isCodeVariantRB(trackCode) : 	dicoBoutonsErreur['T-V'].addError(featureTrack)	
		if TCOD.isCodeElongationRB(trackCode) : dicoBoutonsErreur['T-A'].addError(featureTrack)	
		if TCOD.isCodeShorcutRB(trackCode) : 	dicoBoutonsErreur['T-R'].addError(featureTrack)	
		if TCOD.isCodeDayRB(trackCode) : 		dicoBoutonsErreur['T-J'].addError(featureTrack)	

#		Calcul des Totaux par principal / variante / liasison / boucle
 
		if 'T' in modificationList: dicoBoutonsErreur['T-MT'].addError(featureTrack)	
		if 'F' in modificationList: dicoBoutonsErreur['T-MF'].addError(featureTrack)	

#		Vérification du type d'itinéraire 

		if type not in QGP.typeSetTableRB:
			dicoBoutonsErreur['Typ-I'].addError(featureTrack)

#		Vérification de l'état du parcours

		if trackStatus == None:
			dicoBoutonsErreur['E-0'].addError(featureTrack)
		elif trackStatus == QGP.trackStatusProposal:	
			dicoBoutonsErreur['E-P'].addError(featureTrack)
		elif trackStatus == QGP.trackStatusProject:	
			dicoBoutonsErreur['E-PJ'].addError(featureTrack)
		elif trackStatus == QGP.trackStatusValidated:	
			dicoBoutonsErreur['E-VA'].addError(featureTrack)
		elif trackStatus == QGP.trackStatusPublished:	
			dicoBoutonsErreur['E-PU'].addError(featureTrack)
		elif trackStatus == QGP.trackStatusDeleted:	
			dicoBoutonsErreur['E-SU'].addError(featureTrack)
		elif trackStatus == QGP.trackStatusExternal:	
			dicoBoutonsErreur['E-EX'].addError(featureTrack)
		else:
			dicoBoutonsErreur['E-I'].addError(featureTrack)

#		Vérification des suffixes

		for suffix in featureTrackCode.split('-')[3:]:
			if suffix == '' or suffix[0] not in QGP.validSuffixRB.union(QGP.validSuffixModif): dicoBoutonsErreur['Suf-I'].addError(featureTrack)	

#		Vérification de la géométrie

		if not featureTrack.hasGeometry(): dicoBoutonsErreur['Geo-0'].addError(featureTrack)	

#		Vérification du calcul du parcours

		if trackStatus in QGP.trackStatusForVerificationList:

			sectionOrderedIdList, sectionLostIdList, errorCode, gapList, modificationSet, sectionModifiedIdList = \
					LTRK.computeTracksOrderedSections(featureTrackCode, dicoTrackSections, mainFrame.dicoSectionsGRFeatures, mainFrame.dicoSectionsGRFeaturesEndPoints)	
	
			if errorCode == 0   : dicoBoutonsErreur['C-OK'].addError()
			if errorCode == 1   : dicoBoutonsErreur['C-Vide'].addError(featureTrack)
			if errorCode == 2   : dicoBoutonsErreur['C-D-0'].addError(featureTrack)
			if errorCode == 3   : dicoBoutonsErreur['C-D-N'].addError(featureTrack)
			if errorCode == 4   : dicoBoutonsErreur['C-Inc'].addError(featureTrack)
			if errorCode == 5   : dicoBoutonsErreur['C-Y'].addError(featureTrack)
			if errorCode == 13  : dicoBoutonsErreur['CV-D-N'].addError(featureTrack)
			if errorCode == 14  : dicoBoutonsErreur['CV-Inc'].addError(featureTrack)
			if errorCode == 15  : dicoBoutonsErreur['CV-Y'].addError(featureTrack)
			
			if len(gapList) != 0:  	dicoBoutonsErreur['C-Trou'].addError(featureTrack)
	
#		Calcul de la géométrie
	
			if errorCode == 0:
	
				trackLine = []
				for sectionNumber in range(len(sectionOrderedIdList)):
					idSection = sectionOrderedIdList[sectionNumber]
					sectionLine = mainFrame.dicoSectionsGRFeatures[abs(idSection)].geometry().asMultiPolyline()[0]
					if idSection < 0: sectionLine.reverse()
					trackLine = sectionLine if sectionNumber == 0 else trackLine + sectionLine[1:]
					trackGeometry = QgsGeometry().fromMultiPolylineXY([trackLine])
	
#		Vérification de la distance de Hausdorff
	
				hausdorffDistance = None
				try:
					if type in QGP.typeSetTableRB : oldGeometry = dicoTracksViewFeatures[featureTrackCode].geometry()
					oldGeometry = QgsGeometry().fromPolylineXY(oldGeometry.asMultiPolyline()[0])
					hausdorffDistance = oldGeometry.hausdorffDistance(trackGeometry)
					if hausdorffDistance > 1 : dicoBoutonsErreur['D-1'].addError(featureTrack)			
					if hausdorffDistance > 10 : dicoBoutonsErreur['D-10'].addError(featureTrack)			
					if hausdorffDistance > 100 : dicoBoutonsErreur['D-100'].addError(featureTrack)			
					if hausdorffDistance > 1000 : dicoBoutonsErreur['D-1000'].addError(featureTrack)			
				except:
					pass

#		Avancement 

		progressBar.setValue(progressBar.value() + 1)
		QgsApplication.processEvents()

#	Affichage Final

	for label in dicoBoutonsErreur:
		dicoBoutonsErreur[label].showFinal()

	del progressBar


# ========================================================================================
# --- THE END ---
# ========================================================================================
