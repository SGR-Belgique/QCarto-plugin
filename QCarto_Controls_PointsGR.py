# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Vérifications de la Table Repères-GR
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
# Analyser les Attributs de la couche Tracés GR et afficher les erreurs
# >>> mainFrame 		: mainMenuFrame				Main Menu Class Object
# >>> controlFrame 		: menuControlsFrame			Control Frame Object
# >>> dicoBoutonsErreur : Dico						Dictionnaire des boutons d'erreur à mettre à jour
# >>> globalFlag 		: Bool						Analyse globale iff True - Analyse de la sélection courante iff False
# ========================================================================================

def analysePointsGR(mainFrame, controlFrame, dicoBoutonsErreur, globalFlag):

	startTime = time.time()

# 	Initialiser les boutons

	for label in dicoBoutonsErreur:
		dicoBoutonsErreur[label].reset()

#	Définir la liste des features à analyser 

	featureAnalysedList = [feature for feature in (mainFrame.layerPointsGR.getFeatures() if globalFlag else mainFrame.layerPointsGR.getSelectedFeatures())]

# 	Create Progress Bar

	progressBar = TPRO.createProgressBar(controlFrame.buttonControlAllPointsGR if globalFlag else controlFrame.buttonControlSelectionPointsGR, len(featureAnalysedList), 'Normal')

#	Créer les dictionnaires nécessaires pour vérifier que les points sont attachés

	verificationGeometryFlag = controlFrame.checkGeometryPointsGR.isChecked() and not globalFlag

	if verificationGeometryFlag:
		dicoPointSectionIdList = { featurePoint[QGP.tablePointsFieldGRCode] : [] for featurePoint in featureAnalysedList }
		for featurePoint in featureAnalysedList:
			featurePointCode = TCOD.grCodeFromPointFeature(featurePoint)
			if featurePointCode == '': continue
			if not featurePoint.hasGeometry(): continue
			for idSection in mainFrame.dicoSectionsGRFeatures:
				for gr_code in TCOD.getCodeListALLFromSectionFeature(mainFrame.dicoSectionsGRFeatures[idSection]):
					if featurePointCode in gr_code: 
						dicoPointSectionIdList[featurePointCode].append(idSection)

#	Analyser les entités de la table

	for featurePoint in featureAnalysedList :

#		Infos de l'entité

		featurePointCode = featurePoint[QGP.tablePointsFieldGRCode]
		featurePointRepere = featurePoint[QGP.tablePointsFieldRepere]
		featurePointNom = featurePoint[QGP.tablePointsFieldNom]
		valid, type, label, zone, number, itineraryCode, trackBaseCode, trackCode, modificationList, invalidationList, repeatCount, bifurcationNumber, direction = TCOD.elementsFromGrCode(featurePointCode)

#		Vérification de la géométrie

		if not featurePoint.hasGeometry(): 
			dicoBoutonsErreur['Geo-0'].addError(featurePoint)

#		Calcul des Totaux par type d'itinéraire

		dicoBoutonsErreur['T-ENT'].addError()	
		if type == 'GR'  :  dicoBoutonsErreur['T-GR'].addError(featurePoint)	
		if type == 'GRP' : 	dicoBoutonsErreur['T-GRP'].addError(featurePoint)	
		if type == 'GRT' : 	dicoBoutonsErreur['T-GRT'].addError(featurePoint)	
		if type == 'RI' : 	dicoBoutonsErreur['T-RI'].addError(featurePoint)	
		if type == 'RL' : 	dicoBoutonsErreur['T-RL'].addError(featurePoint)	
		if type == 'RB' : 	dicoBoutonsErreur['T-RB'].addError(featurePoint)	
		if type == 'RF' : 	dicoBoutonsErreur['T-RF'].addError(featurePoint)	
		if type == 'IR' : 	dicoBoutonsErreur['T-IR'].addError(featurePoint)	

#		Cas des Points B2B

		if featurePointCode == QGP.tablePointsGRCodeB2B: 
			dicoBoutonsErreur['T-B2B'].addError(featurePoint)
			progressBar.setValue(progressBar.value() + 1)
			continue

#		Vérification du Code

		if featurePointCode == None or featurePointCode.strip() == '': 
			dicoBoutonsErreur['Cod-0'].addError(featurePoint)				
		elif not valid :
			dicoBoutonsErreur['Cod-I'].addError(featurePoint)				
		
#		Vérification du type d'itinéraire 

		if type not in QGP.typeSetTableGR and type not in QGP.typeSetTableRB:
			dicoBoutonsErreur['Typ-I'].addError(featurePoint)

#		Vérification des suffixes 
	
		if modificationList != [] or invalidationList != [] or repeatCount != 1 or bifurcationNumber != QGP.C_ComputeTrackBifurcationDefault or direction != None :
			dicoBoutonsErreur['Suf-I'].addError(featurePoint)	

#		Vérification que le Parcours existe

		if trackCode not in mainFrame.dicoTracksGRFeatures and trackCode not in mainFrame.dicoTracksRBFeatures:
			dicoBoutonsErreur['Par-I'].addError(featurePoint)	
		
#		Vérification des champs nulls

		if featurePointRepere == None or featurePointRepere.strip() == '': 	dicoBoutonsErreur['Rep-0'].addError(featurePoint)	
		if featurePointNom == None or featurePointNom.strip() == '':  dicoBoutonsErreur['Nom-0'].addError(featurePoint)	

#		Vérification de l'attachement au tracé correct	

		elif verificationGeometryFlag:

			featurePointXY = featurePoint.geometry().asPoint()
			attachedSummit = False

			for idSection in dicoPointSectionIdList[featurePointCode]:
				endPoints = mainFrame.dicoSectionsGRFeaturesEndPoints[idSection]
				if featurePointXY in endPoints:
					attachedSummit = True
					break
			if not attachedSummit : 
				dicoBoutonsErreur['Att-S'].addError(featurePoint)
				distance2Sections = min(mainFrame.dicoSectionsGRFeatures[idSection].geometry().closestVertex(featurePointXY)[4] for idSection in dicoPointSectionIdList[featurePointCode])
				if distance2Sections > QGP.configMatchWPDistance ** 2:
					dicoBoutonsErreur['Att-0'].addError(featurePoint)
				elif distance2Sections > 0:
					dicoBoutonsErreur['Att-D'].addError(featurePoint)
		
		else:
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
