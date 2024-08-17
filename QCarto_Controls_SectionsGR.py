# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Vérifications de la Table Tronçons-GR
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
# Analyser les Attributs de la couche Tronçons GR et afficher les erreurs
# >>> mainFrame 		: mainMenuFrame				Main Menu Class Object
# >>> controlFrame 		: menuControlsFrame			Control Frame Object
# >>> dicoBoutonsErreur : Dico						Dictionnaire des boutons d'erreur à mettre à jour
# >>> globalFlag 		: Bool						Analyse globale iff True - Analyse de la sélection courante iff False
# ========================================================================================

def analyseSectionsGR(mainFrame, controlFrame, dicoBoutonsErreur, globalFlag):

	startTime = time.time()

# 	Initialiser les boutons

	for label in dicoBoutonsErreur:
		dicoBoutonsErreur[label].reset()

#	Définir la liste des features à analyser 

	featureAnalysedList = [feature for feature in (mainFrame.layerSectionsGR.getFeatures() if globalFlag else mainFrame.layerSectionsGR.getSelectedFeatures())]

# Create Progress Bar

	progressBar = TPRO.createProgressBar(controlFrame.buttonControlAllSectionsGR if globalFlag else controlFrame.buttonControlSelectionSectionsGR, len(featureAnalysedList), 'Normal')

#	Analyser les entités de la table

	for featureSection in featureAnalysedList :

#		Infos de l'entité

		gr_list = TCOD.getCodeListALLFromSectionFeature(featureSection)

#		Vérifications des champs xx_list

		dicoBoutonsErreur['T-ENT'].addError()	

		if gr_list == []: dicoBoutonsErreur['Cod-0'].addError(featureSection)	

		allCodesValid = True; allTypesValid = True; allTracksValid = True; allSuffixesValid = True
		dicoType = {type : False for type in QGP.typeSetAll }
		dicoModification = {letter : False for letter in ('T', 'F') }
		dicoInvalidation = {letter : False for letter in ('T', 'F', '0', 'A') }

		for gr_code in gr_list:
			valid, type, label, zone, number, itineraryCode, trackBaseCode, trackCode, modificationList, invalidationList, repeatCount, bifurcationNumber, direction = TCOD.elementsFromGrCode(gr_code)
			if not valid: allCodesValid = False	
			if type in QGP.typeSetAll :
				dicoType[type] = True
			else :
				allTypesValid = False
			if trackCode not in mainFrame.dicoTracksGRFeatures and trackCode not in mainFrame.dicoTracksRBFeatures:
				allTracksValid = False

			for letter in modificationList: 
				if letter in dicoModification: dicoModification[letter] = True
			for letter in invalidationList: 
				if letter in dicoInvalidation: dicoInvalidation[letter] = True
	
			if type in QGP.typeSetModeGR : 
				for suffix in trackCode.split('-')[2:]:
					if suffix == '' or suffix[0] not in QGP.validSuffixGR: allSuffixesValid = False
			if type in QGP.typeSetModeRB : 
				for suffix in trackCode.split('-')[3:]:
					if suffix == '' or suffix[0] not in QGP.validSuffixRB: allSuffixesValid = False
	
		if not allCodesValid :    dicoBoutonsErreur['Cod-I'].addError(featureSection)	
		if not allTypesValid :    dicoBoutonsErreur['Typ-I'].addError(featureSection)	
		if not allTracksValid :   dicoBoutonsErreur['Par-I'].addError(featureSection)	
		if not allSuffixesValid : dicoBoutonsErreur['Suf-I'].addError(featureSection)	
	
		for type in QGP.typeSetAll : 
			if dicoType[type] : dicoBoutonsErreur['T-' + type].addError(featureSection)	
		for letter in dicoModification :
			if dicoModification[letter] : dicoBoutonsErreur['T-M' + letter].addError(featureSection)	
		for letter in dicoInvalidation :
			if dicoInvalidation[letter] : dicoBoutonsErreur['T-#' + letter].addError(featureSection)	

#		Vérification de la géométrie

		if not featureSection.hasGeometry(): 
			dicoBoutonsErreur['Geo-0'].addError(featureSection)	
		elif len(featureSection.geometry().asMultiPolyline()) > 1:
			dicoBoutonsErreur['Geo-M'].addError(featureSection)	
		else:	
			dicoBoutonsErreur['T-KM'].addValue(featureSection.geometry().length() / 1000)

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
