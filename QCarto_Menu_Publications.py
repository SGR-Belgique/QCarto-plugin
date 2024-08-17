# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Gestion des Menus : Page Publications
# ========================================================================================


# ========================================================================================
# Global Variables
# ========================================================================================


# ========================================================================================
# Imports
# ========================================================================================

from PyQt5.QtCore import *
from PyQt5.QtGui import *

from qgis.core import *
from qgis.gui import *
from qgis.PyQt import QtWidgets

import webbrowser
import importlib
import os
import traceback 

import QCarto_Layers_Tracks as LTRK
importlib.reload(LTRK)

import QCarto_Tools_Buttons as TBUT
import QCarto_Tools_Coding as TCOD
import QCarto_Tools_CSV as TCSV
importlib.reload(TCSV)
import QCarto_Tools_Stats as TSTA
importlib.reload(TSTA)
import QCarto_Tools_Dates as TDAT
import QCarto_Tools_Files as TFIL
import QCarto_Tools_Help as THEL
import QCarto_Tools_Layers as TLAY
import QCarto_Tools_Progress as TPRO
import QCarto_Tools_Log as TLOG
importlib.reload(TLOG)

import QCarto_Definitions_Colors as DCOL
import QCarto_Definitions_Styles as DSTY
import QCarto_Definitions_Publications as DPUB
import QCarto_Definitions_TopoGuides as DTOP	

importlib.reload(DPUB)

import QCarto_Parameters_Global
QGP = QCarto_Parameters_Global.globalParameters()


# ========================================================================================
# Class : menuControlsFrame
# >>> iface
# >>> mainMenu 						: Widget of Main Menu
# >>> mainFrame 					: Main Menu Object
# ========================================================================================

class menuPublicationsFrame:

	def __init__(self, iface, mainMenu, mainFrame):

# 	Paramètres fournis

		self.iface = iface
		self.mainMenu = mainMenu
		self.mainFrame = mainFrame

#	Nom de la page

		self.pageName = 'Publications'

#	Accès aux Tables de la DB Carto

		self.layerTracksGR, 	self.layerTracksGRerror 	= self.mainFrame.layerTracksGR, 	self.mainFrame.layerTracksGRerror 	
		self.layerTracksRB, 	self.layerTracksRBerror 	= self.mainFrame.layerTracksRB, 	self.mainFrame.layerTracksRBerror 	
		self.layerSectionsGR, 	self.layerSectionsGRerror 	= self.mainFrame.layerSectionsGR, 	self.mainFrame.layerSectionsGRerror 	
		self.layerPointsGR, 	self.layerPointsGRError 	= self.mainFrame.layerPointsGR, 	self.mainFrame.layerPointsGRError 	
		self.layerCommunes, 	self.layerCommunesError		= self.mainFrame.layerCommunes, 	self.mainFrame.layerCommunesError		

#	Listes des Itinéraires

		self.listTracksGRCodes  = LTRK.getOrderedListItineraryGR({'GR'}, self.mainFrame.dicoTracksGRFeatures)
		self.listTracksGRPCodes = LTRK.getOrderedListItineraryGR({'GRP'}, self.mainFrame.dicoTracksGRFeatures)
		self.listTracksGRTCodes = LTRK.getOrderedListItineraryGR({'GRT'}, self.mainFrame.dicoTracksGRFeatures)
		self.listTracksRLCodes  = LTRK.getOrderedListItineraryRB({'RL'}, self.mainFrame.dicoTracksRBFeatures)
		self.listTracksRBCodes  = LTRK.getOrderedListItineraryRB({'RB'}, self.mainFrame.dicoTracksRBFeatures)
		self.listTracksRFCodes  = LTRK.getOrderedListItineraryRB({'RF'}, self.mainFrame.dicoTracksRBFeatures)
		self.listTracksIRCodes  = LTRK.getOrderedListItineraryRB({'IR'}, self.mainFrame.dicoTracksRBFeatures)

#	Variables globales de la classe

		self.publicTracksCodeSet = None

# 	Création des sous-menus

		self.boxesList = []
		self.createMenuBoxes()

		self.mainFrame.setStatusDone('Page des ' + self.pageName + ' créée !')
		
	def createMenuBoxes(self):

		self.groupBoxPublicationMapPublic = self.menuBoxPublicationMapPublic()
		DSTY.setBoxGeometry(self.groupBoxPublicationMapPublic, 1, 4, 4, 4)
		self.boxesList.append(self.groupBoxPublicationMapPublic)

		self.groupBoxPublicationCsvTracks = self.menuBoxPublicationCsvTracks()
		DSTY.setBoxGeometry(self.groupBoxPublicationCsvTracks, 5, 4, 4, 1)
		self.boxesList.append(self.groupBoxPublicationCsvTracks)
		
		self.groupBoxPublicationStats = self.menuBoxPublicationStats()
		DSTY.setBoxGeometry(self.groupBoxPublicationStats, 5, 6, 4, 1)
		self.boxesList.append(self.groupBoxPublicationStats)

		
# ========================================================================================
# Actions : A la demande de la fenêtre principale
# ========================================================================================

#	Show - Ouverture de cette fenêtre

	def show(self):
		for box in self.boxesList: box.show(), box.repaint()

#	Hide - Ouverture d'une autre fenêtre

	def hide(self):
		for box in self.boxesList: box.hide()

#	Close - Fermeture définitive

	def close(self):
		self.hide()
		for box in self.boxesList: del box

#	Help on this page

	def help(self):
		webbrowser.open_new_tab(QGP.configMenuHelpBasePath + 'QCarto - Page - ' + self.pageName + '.html')
	

# ========================================================================================
# ========================================================================================
#
# Actions de Publication
# 
# ========================================================================================
# ========================================================================================


# ========================================================================================
# Sentiers GR GRP GRT
# ========================================================================================

	def publishMapPublicTracks_clicked(self):
	
#	Barre de Progres
	
		progressBar = TPRO.createProgressBar(self.buttonPublishMapPublicTracks, 5 + 5 + 5 + 4 * 5 + len(self.mainFrame.dicoTracksGRFeatures) + 4 * 10 , 'Normal')

#	Vérifier que les Tables Publiques sont disponibles

		self.mainFrame.setStatusWorking('Vérification que les Tables Publiques sont sur le canevas ...')

		for tableName in ( _ for _ in QGP.tablePublicNameDico if QGP.tablePublicNameDico[_][3] in ('Track', 'Url')) :
			layer, errorText = TLAY.findLayerInGroup(QGP.configPublicMapGroupName, tableName)
			if layer == None:
				self.mainFrame.setStatusError(errorText, False)
				del progressBar
				return

		progressBar.setValue(progressBar.value() + 5)
		
#	Etablir le dictionnaire des url

		layerUrl = TLAY.openLayer(QGP.tableNamePublicUrlsGRSite)[0]
		dicoUrlsTopo = { feature[QGP.tablePublicFieldCode] : feature[QGP.tablePublicFieldUrlTopo]	for feature in layerUrl.getFeatures() }
		dicoUrlsPhoto = { feature[QGP.tablePublicFieldCode] : feature[QGP.tablePublicFieldUrlPhoto]	for feature in layerUrl.getFeatures() }
		if self.mainFrame.debugModeQCartoLevel >= 1 : 
			for code in dicoUrlsTopo : print('dicos Urls : ' + code + ' = ' + dicoUrlsTopo[code] + ' // ' + dicoUrlsPhoto[code])
	
		progressBar.setValue(progressBar.value() + 5)

#	Ouvrir les Tables Publiques

		self.mainFrame.setStatusWorking('Ouverture des Tables Publiques ...')
	
		dicoTablesLayer = {}
		for tableName in ( _ for _ in QGP.tablePublicNameDico if QGP.tablePublicNameDico[_][3] == 'Track') :
			dicoTablesLayer[tableName] = TLAY.openLayer(tableName)[0]
			dicoTablesLayer[tableName].startEditing()
	
		progressBar.setValue(progressBar.value() + 5)

#	Vider le contenu actuel des Tables

		self.mainFrame.setStatusWorking('Suppression des entités existantes ...')

		for tableName in ( _ for _ in QGP.tablePublicNameDico if QGP.tablePublicNameDico[_][3] == 'Track') :
			dicoTablesLayer[tableName].selectAll()	
			dicoTablesLayer[tableName].deleteSelectedFeatures()		
			progressBar.setValue(progressBar.value() + 5)

#	Définir les Tables des Parcours GR GRP GRT

		self.publicTracksCodeSet = set()

		self.mainFrame.setStatusWorking('Définition des nouvelles entités : Parcours GR GRP GRT ...')

		try:
			for code in self.mainFrame.dicoTracksGRFeatures:
				progressBar.setValue(progressBar.value() + 1)
				if not DPUB.isTrackGROnPublicMap(code, self.mainFrame.dicoTracksGRFeatures): continue
				if self.mainFrame.dicoTracksGRFeatures[code][QGP.tableTracksFieldDistance] == None : continue
				self.publicTracksCodeSet.add(TCOD.itineraryFromTrackCode(code))
				featureNew = QgsFeature()
				if TCOD.itineraryTypeFromTrackCode(code) == 'GR'  : featureNew.setFields(dicoTablesLayer[QGP.tableNamePublicTracksGR].fields())
				if TCOD.itineraryTypeFromTrackCode(code) == 'GRP' : featureNew.setFields(dicoTablesLayer[QGP.tableNamePublicTracksGRP].fields())
				if TCOD.itineraryTypeFromTrackCode(code) == 'GRT' : featureNew.setFields(dicoTablesLayer[QGP.tableNamePublicTracksGRT].fields())
				featureNew[QGP.tablePublicFieldCode] = code
				featureNew[QGP.tablePublicFieldLabel] = TCOD.labelGRFromTrackCode(code)
				featureNew[QGP.tablePublicFieldName] = self.mainFrame.dicoTracksGRFeatures[code][QGP.tableTracksFieldName]
				featureNew[QGP.tablePublicFieldDistance] 	= '{:.1f} km'.format(self.mainFrame.dicoTracksGRFeatures[code][QGP.tableTracksFieldDistance] / 1000).replace('.',',')
				featureNew[QGP.tablePublicFieldDPlus] 		= '{:d} m'.format(int(self.mainFrame.dicoTracksGRFeatures[code][QGP.tableTracksFieldDenivelePos]))
				featureNew[QGP.tablePublicFieldDMinus] 		= '{:d} m'.format(int(self.mainFrame.dicoTracksGRFeatures[code][QGP.tableTracksFieldDeniveleNeg]))
#				featureNew[QGP.tablePublicFieldAltMin] 		= '{:d} m'.format(int(self.mainFrame.dicoTracksGRFeatures[code][QGP.tableTracksFieldAltmin]))
#				featureNew[QGP.tablePublicFieldAltMax] 		= '{:d} m'.format(int(self.mainFrame.dicoTracksGRFeatures[code][QGP.tableTracksFieldAltmax]))
				itinerary = TCOD.itineraryFromTrackCode(code)
				featureNew[QGP.tablePublicFieldUrlTopo] = dicoUrlsTopo[itinerary if itinerary in dicoUrlsTopo else 'URL-NONE']
				featureNew[QGP.tablePublicFieldUrlPhoto] = dicoUrlsPhoto[itinerary if itinerary in dicoUrlsPhoto else 'URL-NONE']
				featureNew.setGeometry(self.mainFrame.dicoTracksGRFeatures[code].geometry())
				if TCOD.itineraryTypeFromTrackCode(code) == 'GR'  : dicoTablesLayer[QGP.tableNamePublicTracksGR].addFeature(featureNew)
				if TCOD.itineraryTypeFromTrackCode(code) == 'GRP' : dicoTablesLayer[QGP.tableNamePublicTracksGRP].addFeature(featureNew)
				if TCOD.itineraryTypeFromTrackCode(code) == 'GRT' : dicoTablesLayer[QGP.tableNamePublicTracksGRT].addFeature(featureNew)
				QgsApplication.processEvents()
		except:
			self.mainFrame.setStatusWarning('Une erreur s\'est produite lors de la création des tables Sentiers - Annulation des modifications ...', 2000)
			for tableName in ( _ for _ in QGP.tablePublicNameDico if QGP.tablePublicNameDico[_][3] == 'Track') :
				dicoTablesLayer[tableName].rollBack()
			del progressBar
			self.mainFrame.setStatusError('Les Tables de la Carte Publique n\'ont pas été mises-à-jour', False)
			return

#	Commit les Tables des Parcours GR GRP GRT

		self.mainFrame.setStatusWorking('Commit des Tables : Parcours GR GRP GRT ...')
		
		for tableName in ( _ for _ in QGP.tablePublicNameDico if QGP.tablePublicNameDico[_][3] == 'Track') :
			dicoTablesLayer[tableName].commitChanges()
			progressBar.setValue(progressBar.value() + 10)
			QgsApplication.processEvents()

#  	Terminé

		TLOG.appendInfoInLogfile('PublicMap', ['Parcours GR GRP GRT'])
		del progressBar
		self.mainFrame.setStatusDone('Les Tables de la Carte Publique sont mises-à-jour')


# ========================================================================================
# Repères GR GRP
# ========================================================================================

	def publishMapPublicPoints_clicked(self):

		if self.publicTracksCodeSet == None:
			self.mainFrame.setStatusWarning('La publication des sentiers au préalable est nécéssaire !')
			return

#	Barre de Progres
	
		progressBar = TPRO.createProgressBar(self.buttonPublishMapPublicPoints, 5 + 5 + 2 * 5 + len(self.mainFrame.dicoPointsGRFeatures) + 2 * 400 , 'Normal')

#	Vérifier que les Tables Publiques sont disponibles

		self.mainFrame.setStatusWorking('Vérification que les Tables Publiques sont sur le canevas ...')

		for tableName in ( _ for _ in QGP.tablePublicNameDico if QGP.tablePublicNameDico[_][3] == 'Point') :
			layer, errorText = TLAY.findLayerInGroup(QGP.configPublicMapGroupName, tableName)
			if layer == None:
				self.mainFrame.setStatusError(errorText, False)
				del progressBar
				return

		progressBar.setValue(progressBar.value() + 5)
	
#	Ouvrir les Tables Publiques

		self.mainFrame.setStatusWorking('Ouverture des Tables Publiques ...')
	
		dicoTablesLayer = {}
		for tableName in ( _ for _ in QGP.tablePublicNameDico if QGP.tablePublicNameDico[_][3] == 'Point') :
			dicoTablesLayer[tableName] = TLAY.openLayer(tableName)[0]
			dicoTablesLayer[tableName].startEditing()
	
		progressBar.setValue(progressBar.value() + 5)

#	Vider le contenu actuel des Tables

		self.mainFrame.setStatusWorking('Suppression des entités existantes ...')

		for tableName in ( _ for _ in QGP.tablePublicNameDico if QGP.tablePublicNameDico[_][3] == 'Point') :
			dicoTablesLayer[tableName].selectAll()	
			dicoTablesLayer[tableName].deleteSelectedFeatures()		
			progressBar.setValue(progressBar.value() + 5)

#	Définir les Tables des Repères GR GRP

		self.mainFrame.setStatusWorking('Définition des nouvelles entités : Repères GR GRP ...')

		try:
			for id in self.mainFrame.dicoPointsGRFeatures:
				progressBar.setValue(progressBar.value() + 1)
				code = self.mainFrame.dicoPointsGRFeatures[id][QGP.tablePointsFieldGRCode]
				if code not in self.publicTracksCodeSet: continue
				if TCOD.itineraryTypeFromTrackCode(code) == 'GRT'   : continue
				featureNew = QgsFeature()
				if TCOD.itineraryTypeFromTrackCode(code) == 'GR'  : featureNew.setFields(dicoTablesLayer[QGP.tableNamePublicPointsGR].fields())
				if TCOD.itineraryTypeFromTrackCode(code) == 'GRP' : featureNew.setFields(dicoTablesLayer[QGP.tableNamePublicPointsGRP].fields())
				featureNew[QGP.tablePublicPointFieldId] 		= id 	
				featureNew[QGP.tablePublicPointFieldCode] 		= code
				featureNew[QGP.tablePublicPointFieldRepere] 	= self.mainFrame.dicoPointsGRFeatures[id][QGP.tablePointsFieldRepere]
				featureNew[QGP.tablePublicPointFieldNom] 		= self.mainFrame.dicoPointsGRFeatures[id][QGP.tablePointsFieldNom] 
				featureNew.setGeometry(self.mainFrame.dicoPointsGRFeatures[id].geometry())
				if TCOD.itineraryTypeFromTrackCode(code) == 'GR'  : dicoTablesLayer[QGP.tableNamePublicPointsGR].addFeature(featureNew)
				if TCOD.itineraryTypeFromTrackCode(code) == 'GRP' : dicoTablesLayer[QGP.tableNamePublicPointsGRP].addFeature(featureNew)
				QgsApplication.processEvents()
		except:
			self.mainFrame.setStatusWarning('Une erreur s\'est produite lors de la création des tables Repères - Annulation des modifications ...')
			for tableName in ( _ for _ in QGP.tablePublicNameDico if QGP.tablePublicNameDico[_][3] == 'Point') :
				dicoTablesLayer[tableName].rollBack()
			del progressBar
			self.mainFrame.setStatusError('Les Tables de la Carte Publique n\'pas été mises-à-jour', False)
			return

#	Commit les Tables des Repères GR GRP

		self.mainFrame.setStatusWorking('Commit des Tables : Repères GR GRP ...')

		for tableName in ( _ for _ in QGP.tablePublicNameDico if QGP.tablePublicNameDico[_][3] == 'Point') :
			dicoTablesLayer[tableName].commitChanges()
			progressBar.setValue(progressBar.value() + 400)
			QgsApplication.processEvents()

#  	Terminé

		TLOG.appendInfoInLogfile('PublicMap', ['Repères GR GRP'])
		del progressBar
		self.mainFrame.setStatusDone('Les Tables de la Carte Publique sont mises-à-jour')


# ========================================================================================
# Sections #
# ========================================================================================

	def publishMapPublicSections_clicked(self):

		if self.publicTracksCodeSet == None:
			self.mainFrame.setStatusWarning('La publication des sentiers au préalable est nécéssaire !')
			return

#	Barre de Progres
	
		progressBar = TPRO.createProgressBar(self.buttonPublishMapPublicSections, 5 + 5 + 1 * 5 + int(len(self.mainFrame.dicoSectionsGRFeatures) / 10) + 1 * 10 , 'Normal')

#	Vérifier que les Tables Publiques sont disponibles

		self.mainFrame.setStatusWorking('Vérification que les Tables Publiques sont sur le canevas ...')

		for tableName in ( _ for _ in QGP.tablePublicNameDico if QGP.tablePublicNameDico[_][3] == 'Section') :
			layer, errorText = TLAY.findLayerInGroup(QGP.configPublicMapGroupName, tableName)
			if layer == None:
				self.mainFrame.setStatusError(errorText, False)
				del progressBar
				return

		progressBar.setValue(progressBar.value() + 5)
	
#	Ouvrir les Tables Publiques

		self.mainFrame.setStatusWorking('Ouverture des Tables Publiques ...')
	
		dicoTablesLayer = {}
		for tableName in ( _ for _ in QGP.tablePublicNameDico if QGP.tablePublicNameDico[_][3] == 'Section') :
			dicoTablesLayer[tableName] = TLAY.openLayer(tableName)[0]
			dicoTablesLayer[tableName].startEditing()
	
		progressBar.setValue(progressBar.value() + 5)

#	Vider le contenu actuel des Tables

		self.mainFrame.setStatusWorking('Suppression des entités existantes ...')

		for tableName in ( _ for _ in QGP.tablePublicNameDico if QGP.tablePublicNameDico[_][3] == 'Section') :
			dicoTablesLayer[tableName].selectAll()	
			dicoTablesLayer[tableName].deleteSelectedFeatures()		
			progressBar.setValue(progressBar.value() + 5)

#	Définir les Tables des Sections Modifiées

		self.mainFrame.setStatusWorking('Définition des nouvelles entités : Sections Modifiées ...')

		try:
			for id in self.mainFrame.dicoSectionsGRFeatures:
				progressBar.setValue(progressBar.value() + 1)
				feature = self.mainFrame.dicoSectionsGRFeatures[id]
				gr_list = TCOD.grCodeListFromSectionFeature(feature, 'GR-P-T')
				if gr_list == [] : continue
				sectionIsModified = False
				for code in gr_list:
					valid, type, label, zone, number, itineraryCode, trackBaseCode, trackCode, modificationList, invalidationList, repeatCount, bifurcationNumber, direction = TCOD.elementsFromGrCode(code)		
					if not valid : continue
					if trackBaseCode not in self.publicTracksCodeSet: continue
					if 'T' in invalidationList: sectionIsModified = True; continue
					if invalidationList == []: sectionIsModified = False; break
				if not sectionIsModified : continue
				featureNew = QgsFeature()
				featureNew.setFields(dicoTablesLayer[QGP.tableNamePublicSectionsClosed].fields())
				featureNew[QGP.tablePublicFieldId] = id
				featureNew[QGP.tablePublicFieldCode] = '- - -'
				featureNew[QGP.tablePublicFieldName] = '- - -'
				featureNew.setGeometry(self.mainFrame.dicoSectionsGRFeatures[id].geometry())
				dicoTablesLayer[QGP.tableNamePublicSectionsClosed].addFeature(featureNew)
				QgsApplication.processEvents()
		except:
			self.mainFrame.setStatusWarning('Une erreur s\'est produite lors de la création des tables Tronçons - Annulation des modifications ...')
			for tableName in ( _ for _ in QGP.tablePublicNameDico if QGP.tablePublicNameDico[_][3] == 'Section') :
				dicoTablesLayer[tableName].rollBack()
			del progressBar
			self.mainFrame.setStatusError('Les Tables de la Carte Publique n\'ont été mises-à-jour', False)
			return

#	Commit les Tables des Repères GR GRP

		self.mainFrame.setStatusWorking('Commit des Tables : Tronçons # ...')

		for tableName in ( _ for _ in QGP.tablePublicNameDico if QGP.tablePublicNameDico[_][3] == 'Section') :
			dicoTablesLayer[tableName].commitChanges()
			progressBar.setValue(progressBar.value() + 10)
			QgsApplication.processEvents()

#  	Terminé

		TLOG.appendInfoInLogfile('PublicMap', ['Tronçons #'])
		del progressBar
		self.mainFrame.setStatusDone('Les Tables de la Carte Publique sont mises-à-jour')


# ========================================================================================
# Départs RB RL RI IR
# ========================================================================================

	def publishMapPublicRB_clicked(self):
		self.publishMapPublicRBRL('RB')

	def publishMapPublicRL_clicked(self):
		self.publishMapPublicRBRL('RL')
	
	def publishMapPublicRI_clicked(self):
		self.publishMapPublicRBRL('RI')
	
	def publishMapPublicIR_clicked(self):
		self.publishMapPublicRBRL('IR')

	def publishMapPublicRBRL(self, RBorRLorIR):
	
#	Barre de Progres
	
		count = 5 + 5 + 5 + (2 if RBorRLorIR == 'RB' else 1) * 5  + (2 if RBorRLorIR == 'RB' else 1) * len(self.mainFrame.dicoTracksRBFeatures) + (2 if RBorRLorIR == 'RB' else 1) * 10
		if RBorRLorIR == 'RB' : progressBar = TPRO.createProgressBar(self.buttonPublishMapPublicRB, count, 'Normal')
		if RBorRLorIR == 'RL' : progressBar = TPRO.createProgressBar(self.buttonPublishMapPublicRL, count, 'Normal')
		if RBorRLorIR == 'RI' : progressBar = TPRO.createProgressBar(self.buttonPublishMapPublicRI, count, 'Normal')
		if RBorRLorIR == 'IR' : progressBar = TPRO.createProgressBar(self.buttonPublishMapPublicIR, count, 'Normal')

#	Vérifier que les Tables Publiques sont disponibles

		self.mainFrame.setStatusWorking('Vérification que les Tables Publiques sont sur le canevas ...')

		for tableName in ( _ for _ in QGP.tablePublicNameDico if RBorRLorIR in QGP.tablePublicNameDico[_][3]) :
			layer, errorText = TLAY.findLayerInGroup(QGP.configPublicMapGroupName, tableName)
			if layer == None:
				self.mainFrame.setStatusError(errorText, False)
				del progressBar
				return

		progressBar.setValue(progressBar.value() + 5)
	
#	Etablir le dictionnaire des url

		layerUrl = TLAY.openLayer(QGP.tableNamePublicUrlsRBSite)[0]
		dicoUrlsTopo = { feature[QGP.tablePublicFieldCode] : feature[QGP.tablePublicFieldUrlTopo]	for feature in layerUrl.getFeatures() }
		dicoUrlsPhoto = { feature[QGP.tablePublicFieldCode] : feature[QGP.tablePublicFieldUrlPhoto]	for feature in layerUrl.getFeatures() }
		if self.mainFrame.debugModeQCartoLevel >= 1 : 
			for code in dicoUrlsTopo : print('dicos Urls : ' + code + ' = ' + dicoUrlsTopo[code] + ' // ' + dicoUrlsPhoto[code])

		progressBar.setValue(progressBar.value() + 5)

#	Ouvrir les Tables Publiques

		self.mainFrame.setStatusWorking('Ouverture des Tables Publiques ...')
	
		dicoTablesLayer = {}
		for tableName in ( _ for _ in QGP.tablePublicNameDico if RBorRLorIR in QGP.tablePublicNameDico[_][3]) :
			dicoTablesLayer[tableName] = TLAY.openLayer(tableName)[0]
			dicoTablesLayer[tableName].startEditing()
	
		progressBar.setValue(progressBar.value() + 5)

#	Vider le contenu actuel des Tables

		self.mainFrame.setStatusWorking('Suppression des entités existantes ...')

		for tableName in ( _ for _ in QGP.tablePublicNameDico if RBorRLorIR in QGP.tablePublicNameDico[_][3]) :
			dicoTablesLayer[tableName].selectAll()	
			dicoTablesLayer[tableName].deleteSelectedFeatures()		
			progressBar.setValue(progressBar.value() + 5)

#	Définir la Table des Départs RB RL RI IR

		self.mainFrame.setStatusWorking('Définition des nouvelles entités : Départs RB / RL / RI / IR ...')

		try:
			for code in self.mainFrame.dicoTracksRBFeatures:
				progressBar.setValue(progressBar.value() + 1)
				if not DPUB.isTrackRBOnPublicMap(code, self.mainFrame.dicoTracksRBFeatures): continue
				if self.mainFrame.dicoTracksRBFeatures[code][QGP.tableTracksFieldDistance] == None : continue
				if TCOD.itineraryTypeFromTrackCode(code) != RBorRLorIR  : continue
				codeTopo = TCOD.projectFromTrackCode(code) + ' Tome ' + str(DTOP.getRBTome(code))
				featureNew = QgsFeature()
				if RBorRLorIR == 'RB' : featureNew.setFields(dicoTablesLayer[QGP.tableNamePublicStartRB].fields())
				if RBorRLorIR == 'RL' : featureNew.setFields(dicoTablesLayer[QGP.tableNamePublicStartRL].fields())
				if RBorRLorIR == 'RI' : featureNew.setFields(dicoTablesLayer[QGP.tableNamePublicStartRI].fields())
				if RBorRLorIR == 'IR' : featureNew.setFields(dicoTablesLayer[QGP.tableNamePublicStartIR].fields())
				label = code if code[-2:] != '_O' else code[0:-2]
				if RBorRLorIR == 'RL' : label = 'GG-' + DTOP.getGGZone(int(label[6:8])) + '-' + label[6:8]
				featureNew[QGP.tablePublicFieldCode] = code
				featureNew[QGP.tablePublicFieldLabel] = label
				featureNew[QGP.tablePublicFieldName] = self.mainFrame.dicoTracksRBFeatures[code][QGP.tableTracksFieldName]
				featureNew[QGP.tablePublicFieldDistance] 	= '{:.1f} km'.format(self.mainFrame.dicoTracksRBFeatures[code][QGP.tableTracksFieldDistance] / 1000).replace('.',',')
				featureNew[QGP.tablePublicFieldDPlus] 		= '{:d} m'.format(int(self.mainFrame.dicoTracksRBFeatures[code][QGP.tableTracksFieldDenivelePos]))
				featureNew[QGP.tablePublicFieldDMinus] 		= '{:d} m'.format(int(self.mainFrame.dicoTracksRBFeatures[code][QGP.tableTracksFieldDeniveleNeg]))
				featureNew[QGP.tablePublicFieldUrlTopo] = dicoUrlsTopo[code if code in dicoUrlsTopo else (codeTopo if codeTopo in dicoUrlsTopo else 'URL-NONE')]
				featureNew[QGP.tablePublicFieldUrlPhoto] = dicoUrlsPhoto[code if code in dicoUrlsPhoto else (codeTopo if codeTopo in dicoUrlsPhoto else 'URL-NONE')]
				startPointRB = self.mainFrame.dicoTracksRBFeatures[code].geometry().asMultiPolyline()[0][0]
				featureNew.setGeometry(QgsGeometry.fromPointXY(startPointRB))
				if RBorRLorIR == 'RB' : dicoTablesLayer[QGP.tableNamePublicStartRB].addFeature(featureNew)
				if RBorRLorIR == 'RL' : dicoTablesLayer[QGP.tableNamePublicStartRL].addFeature(featureNew)
				if RBorRLorIR == 'RI' : dicoTablesLayer[QGP.tableNamePublicStartRI].addFeature(featureNew)
				if RBorRLorIR == 'IR' : dicoTablesLayer[QGP.tableNamePublicStartIR].addFeature(featureNew)
				QgsApplication.processEvents()
		except:
			self.mainFrame.setStatusWarning('Une erreur s\'est produite lors de la création de la Table Start ' + RBorRLorIR + ' - Annulation des modifications ...', 2000)
			traceback.print_exc() 
			for tableName in ( _ for _ in QGP.tablePublicNameDico if RBorRLorIR in QGP.tablePublicNameDico[_][3]) :
				dicoTablesLayer[tableName].rollBack()
			del progressBar
			self.mainFrame.setStatusError('Les Tables de la Carte Publique n\'ont pas été mises-à-jour', False)
			return

#	Définir la table des Zones RB IR

		if RBorRLorIR == 'RB' or RBorRLorIR == 'IR':

			self.mainFrame.setStatusWorking('Définition des nouvelles entités : Zones RB IR ...')
	
			try:
				for code in self.mainFrame.dicoTracksRBFeatures:
					progressBar.setValue(progressBar.value() + 1)
					if not DPUB.isTrackRBOnPublicMap(code, self.mainFrame.dicoTracksRBFeatures): continue
					if self.mainFrame.dicoTracksRBFeatures[code][QGP.tableTracksFieldDistance] == None : continue
					if TCOD.itineraryTypeFromTrackCode(code) not in ('RB', 'IR')  : continue
					featureNew = QgsFeature()
					featureNew.setFields(dicoTablesLayer[QGP.tableNamePublicZoneRB].fields())
					featureNew[QGP.tablePublicFieldCode] = code
					featureNew[QGP.tablePublicFieldLabel] = code
					featureNew[QGP.tablePublicFieldName] = self.mainFrame.dicoTracksRBFeatures[code][QGP.tableTracksFieldName]
					featureNew.setGeometry(self.mainFrame.dicoTracksRBFeatures[code].geometry().centroid().buffer((QGP.tablePublicRadiusRB if TCOD.itineraryTypeFromTrackCode(code) == 'RB' else QGP.tablePublicRadiusIR),36))
					dicoTablesLayer[QGP.tableNamePublicZoneRB].addFeature(featureNew)
					QgsApplication.processEvents()
			except:
				self.mainFrame.setStatusWarning('Une erreur s\'est produite lors de la création de la Table Zone RB - Annulation des modifications ...', 2000)
				traceback.print_exc() 
				for tableName in ( _ for _ in QGP.tablePublicNameDico if RBorRLorIR in QGP.tablePublicNameDico[_][3]) :
					dicoTablesLayer[tableName].rollBack()
				del progressBar
				self.mainFrame.setStatusError('Les Tables de la Carte Publique n\'ont été pas mises-à-jour', False)
				return

#	Commit les Tables des RB / RL / RI / IR

		self.mainFrame.setStatusWorking('Commit des Tables : Départs RB RL RI IR ...')

		for tableName in ( _ for _ in QGP.tablePublicNameDico if RBorRLorIR in QGP.tablePublicNameDico[_][3]) :
			dicoTablesLayer[tableName].commitChanges()
			progressBar.setValue(progressBar.value() + 10)
			QgsApplication.processEvents()

#  	Terminé

		TLOG.appendInfoInLogfile('PublicMap', ['Départs ' + RBorRLorIR])
		del progressBar
		self.mainFrame.setStatusDone('Les Tables de la Carte Publique sont mises-à-jour')


# ========================================================================================
# CSV des Parcours
# ========================================================================================

	def publishCsvTracks_clicked(self):
		
		self.mainFrame.setStatusWorking('Export des Parcours-GR et Parcours-RB en CSV ...')
		
		timeStamp = TDAT.getTimeStamp()
		timeStampCSV = ' (' + timeStamp + ')'

		pathCSV = QGP.pathDeliveryTracksTableCsv
		fileCSV = QGP.fileDeliveryTracksTableCsv + timeStampCSV + '.csv'

		TCSV.exportCsvTracksDico(pathCSV, fileCSV, self.mainFrame.dicoTracksGRFeatures, self.mainFrame.dicoTracksRBFeatures )

		self.mainFrame.setStatusDone(pathCSV + fileCSV + ' créé - OK')


	def viewCsvTracks_clicked(self):

		pathCSV = QGP.pathDeliveryTracksTableCsv
		fileCSV = QGP.fileDeliveryTracksTableCsv
	
		if not os.path.isdir(pathCSV):
			self.mainFrame.setStatusWarning('Le répertoire : ' + pathCSV + ' n\'existe pas')
			return
		
		for fileName in sorted(os.listdir(pathCSV), reverse=True):
			baseName, timeStamp, extension = TFIL.splitFileName(fileName)
			if baseName == fileCSV and extension == 'csv':
				THEL.viewCsvOnBrowser(self.mainFrame, 'Dernière version de la table des parcours - Publiée le ' +  timeStamp, pathCSV + fileName)
				self.mainFrame.setStatusDone('Votre navigateur montre le fichier CSV')
				return

		self.mainFrame.setStatusWarning('Le répertoire : ' + pathCSV + ' ne contient pas de fichier CSV valide')


# ========================================================================================
# CSV des Statistiques
# ========================================================================================

	def publishStats_clicked(self):

		self.mainFrame.setStatusWorking('Export des Statistiques ...')
		
		timeStamp = TDAT.getTimeStamp()
		timeStampCSV = ' (' + timeStamp + ')'

		pathCSV = QGP.pathDeliveryStatsCsv
		fileCSV = QGP.fileDeliveryStatsCsv + timeStampCSV + '.csv'

		TSTA.exportCsvStats(pathCSV, fileCSV, self.mainFrame, self.buttonPublishStats)

		self.mainFrame.setStatusDone(pathCSV + fileCSV + ' créé - OK')

	def viewCsvStats_clicked(self):

		pathCSV = QGP.pathDeliveryStatsCsv
		fileCSV = QGP.fileDeliveryStatsCsv
	
		if not os.path.isdir(pathCSV):
			self.mainFrame.setStatusWarning('Le répertoire : ' + pathCSV + ' n\'existe pas')
			return
		
		for fileName in sorted(os.listdir(pathCSV), reverse=True):
			baseName, timeStamp, extension = TFIL.splitFileName(fileName)
			if baseName == fileCSV and extension == 'csv':
				THEL.viewCsvOnBrowser(self.mainFrame, 'Dernière version des Statistiques - Publiée le ' +  timeStamp, pathCSV + fileName)
				self.mainFrame.setStatusDone('Votre navigateur montre le fichier CSV')
				TFIL.copy_files(QGP.configMenuHelpBasePath, pathCSV, QGP.exportSeeCsvHtmlFile, fileName.replace('.csv', '.html'))
				return

		self.mainFrame.setStatusWarning('Le répertoire : ' + pathCSV + ' ne contient pas de fichier CSV valide')


# ========================================================================================
# ========================================================================================
#
# Création des différents cadres Menu
# 
# ========================================================================================
# ========================================================================================


# ========================================================================================
# Cadre : Publication Carte Publique
# ========================================================================================

	def menuBoxPublicationMapPublic(self):
	
		groupBoxPublishMap = QtWidgets.QGroupBox('Publication : Carte Publique', self.mainMenu)
		groupBoxPublishMap.setStyleSheet(DSTY.styleBox)

#	Boutons de Publication

		TBUT.createLabelBlackButton(groupBoxPublishMap, 1, 2, 'Publier GR', 'Normal', 'Normal')

		self.buttonPublishMapPublicTracks = TBUT.createActionButton(groupBoxPublishMap, 2, 2, 'Sentiers', 'Normal')
		DSTY.setStyleWarningButton(self.buttonPublishMapPublicTracks)
		self.buttonPublishMapPublicTracks.clicked.connect(self.publishMapPublicTracks_clicked)

		self.buttonPublishMapPublicPoints = TBUT.createActionButton(groupBoxPublishMap, 3, 2, 'Repères', 'Normal')
		DSTY.setStyleWarningButton(self.buttonPublishMapPublicPoints)
		self.buttonPublishMapPublicPoints.clicked.connect(self.publishMapPublicPoints_clicked)

		self.buttonPublishMapPublicSections = TBUT.createActionButton(groupBoxPublishMap, 4, 2, 'Tronçons #', 'Normal')
		DSTY.setStyleWarningButton(self.buttonPublishMapPublicSections)
		self.buttonPublishMapPublicSections.clicked.connect(self.publishMapPublicSections_clicked)
		
		TBUT.createLabelBlackButton(groupBoxPublishMap, 1, 3, 'Publier RB', 'Normal', 'Normal')		
		
		self.buttonPublishMapPublicRB = TBUT.createActionButton(groupBoxPublishMap, 2, 3, 'RB Départs', 'Normal')
		DSTY.setStyleWarningButton(self.buttonPublishMapPublicRB)
		self.buttonPublishMapPublicRB.clicked.connect(self.publishMapPublicRB_clicked)		

		self.buttonPublishMapPublicRL = TBUT.createActionButton(groupBoxPublishMap, 3, 3, 'RL Départs', 'Normal')
		DSTY.setStyleWarningButton(self.buttonPublishMapPublicRL)
		self.buttonPublishMapPublicRL.clicked.connect(self.publishMapPublicRL_clicked)		
		
		self.buttonPublishMapPublicRI = TBUT.createActionButton(groupBoxPublishMap, 4, 3, 'RI Départs', 'Normal')
		DSTY.setStyleWarningButton(self.buttonPublishMapPublicRI)
		self.buttonPublishMapPublicRI.clicked.connect(self.publishMapPublicRI_clicked)		
		
		self.buttonPublishMapPublicIR = TBUT.createActionButton(groupBoxPublishMap, 2, 4, 'IR Départs', 'Normal')
		DSTY.setStyleWarningButton(self.buttonPublishMapPublicIR)
		self.buttonPublishMapPublicIR.clicked.connect(self.publishMapPublicIR_clicked)		

#	Boutons Aide

		buttonHelpFiche = TBUT.createHelpButton(groupBoxPublishMap, 3, 1, 'Fiche', 'Normal')
		buttonHelpFiche.clicked.connect(lambda x : webbrowser.open_new_tab(QGP.configMenuHelpBasePath + 'QCarto - Fiche - Carte Publique.html'))	
		
		buttonHelpProcess = TBUT.createHelpButton(groupBoxPublishMap, 4, 1, 'Procédure', 'Normal')
		buttonHelpProcess.clicked.connect(lambda x : webbrowser.open_new_tab(QGP.configMenuHelpBasePath + 'QCarto - Procédure - Carte Publique.html'))	
			
# 	Terminé

		groupBoxPublishMap.repaint()

		return groupBoxPublishMap			


# ========================================================================================
# Cadre : Publication Csv Parcours
# ========================================================================================

	def menuBoxPublicationCsvTracks(self):
	
		groupBoxPublishCsv = QtWidgets.QGroupBox('Publication : Csv des Parcours', self.mainMenu)
		groupBoxPublishCsv.setStyleSheet(DSTY.styleBox)

#	Bouton de Publication

		TBUT.createLabelBlackButton(groupBoxPublishCsv, 1, 1, 'Publier CSV', 'Normal', 'Normal')

		self.buttonPublishCsvTracks = TBUT.createActionButton(groupBoxPublishCsv, 2, 1, 'Tous Parcours', 'Normal')
		DSTY.setStyleWarningButton(self.buttonPublishCsvTracks)
		self.buttonPublishCsvTracks.clicked.connect(self.publishCsvTracks_clicked)

#	Boutons Aide

		buttonHelpViewCsv = TBUT.createHelpButton(groupBoxPublishCsv, 3, 1, 'Voir CSV', 'Normal')
		buttonHelpViewCsv.clicked.connect(self.viewCsvTracks_clicked)

		buttonHelpFiche = TBUT.createHelpButton(groupBoxPublishCsv, 4, 1, 'Fiche', 'Normal')
		buttonHelpFiche.clicked.connect(lambda x : webbrowser.open_new_tab(QGP.configMenuHelpBasePath + 'QCarto - Fiche - Table Parcours.html'))	

# 	Terminé

		groupBoxPublishCsv.repaint()

		return groupBoxPublishCsv			


# ========================================================================================
# Cadre : Publication Csv Parcours
# ========================================================================================

	def menuBoxPublicationStats(self):
	
		groupBoxPublishCsv = QtWidgets.QGroupBox('Publication : Statistiques', self.mainMenu)
		groupBoxPublishCsv.setStyleSheet(DSTY.styleBox)

#	Bouton de Publication

		TBUT.createLabelBlackButton(groupBoxPublishCsv, 1, 1, 'Publier CSV', 'Normal', 'Normal')

		self.buttonPublishStats = TBUT.createActionButton(groupBoxPublishCsv, 2, 1, 'Statistiques', 'Normal')
		DSTY.setStyleWarningButton(self.buttonPublishStats)
		self.buttonPublishStats.clicked.connect(self.publishStats_clicked)

#	Boutons Aide

		buttonHelpViewCsv = TBUT.createHelpButton(groupBoxPublishCsv, 3, 1, 'Voir CSV', 'Normal')
		buttonHelpViewCsv.clicked.connect(self.viewCsvStats_clicked)

		buttonHelpFiche = TBUT.createHelpButton(groupBoxPublishCsv, 4, 1, 'Fiche', 'Normal')
#		buttonHelpFiche.clicked.connect(lambda x : webbrowser.open_new_tab(QGP.configMenuHelpBasePath + 'QCarto - Fiche - Table Parcours.html'))	

# 	Terminé

		groupBoxPublishCsv.repaint()

		return groupBoxPublishCsv			


# ========================================================================================
# --- THE END ---
# ========================================================================================
	