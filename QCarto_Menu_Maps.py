# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Gestion des Menus : Page Descriptifs
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

import os
import shutil
import webbrowser
import importlib

import QCarto_Layers_Tracks as LTRK
importlib.reload(LTRK)
import QCarto_Layers_Frames as LFRM
importlib.reload(LFRM)

import QCarto_Tools_QParam as TQCP
importlib.reload(TQCP)
import QCarto_Tools_Altitudes as TALT
importlib.reload(TALT)
import QCarto_Tools_Coding as TCOD
importlib.reload(TCOD)
import QCarto_Tools_Dates as TDAT
importlib.reload(TDAT)
import QCarto_Tools_Buttons as TBUT
importlib.reload(TBUT)
import QCarto_Tools_Files as TFIL
importlib.reload(TFIL)
import QCarto_Tools_Help as THEL
importlib.reload(THEL)
import QCarto_Tools_Layers as TLAY
importlib.reload(TLAY)
import QCarto_Tools_CSV as TCSV
importlib.reload(TCSV)
import QCarto_Tools_GPX as TGPX
importlib.reload(TGPX)
import QCarto_Tools_Ozi as TOZI
importlib.reload(TOZI)
import QCarto_Tools_Progress as TP
importlib.reload(TP)

import QCarto_Definitions_Colors as DCOL
importlib.reload(DCOL)
import QCarto_Definitions_Styles as DSTY
importlib.reload(DSTY)


import QCarto_Parameters_Global
importlib.reload(QCarto_Parameters_Global)

QGP = QCarto_Parameters_Global.globalParameters()

# ========================================================================================
# Class : menuMapsFrame
# >>> iface
# >>> mainMenu 						: Widget of Main Menu
# >>> mainFrame 					: Main Menu Object
# ========================================================================================

class menuMapsFrame:

	def __init__(self, iface, mainMenu, mainFrame):

# 	Paramètres fournis

		self.iface = iface
		self.mainMenu = mainMenu
		self.mainFrame = mainFrame

#	Nom de la page

		self.pageName = 'Cartes'

#	Accès aux Tables de la DB Carto

		self.layerTracksGR, 	self.layerTracksGRerror 	= self.mainFrame.layerTracksGR, 	self.mainFrame.layerTracksGRerror 	
		self.layerTracksRB, 	self.layerTracksRBerror 	= self.mainFrame.layerTracksRB, 	self.mainFrame.layerTracksRBerror 	
		self.layerSectionsGR, 	self.layerSectionsGRerror 	= self.mainFrame.layerSectionsGR, 	self.mainFrame.layerSectionsGRerror 	
		self.layerPointsGR, 	self.layerPointsGRError 	= self.mainFrame.layerPointsGR, 	self.mainFrame.layerPointsGRError 	
		self.layerCommunes, 	self.layerCommunesError		= self.mainFrame.layerCommunes, 	self.mainFrame.layerCommunesError		

#	Variables globales de la classe

		self.itinerarySelected = None
		self.createProjectActive = False
		self.selectedMapFeature = None
		self.highlightedMap = None
		self.automaticMapRefresh = True		
		self.deleteMapActive = False
		self.mapNewNameText = None
		self.mapNewNameRow = None

		self.configZoomMapScale = int(TQCP.retrieveQCartoParameter(self.mainFrame, 'USER', self.mainFrame.userFullName, 'ZoomCarte', 50000))

# 	Création des sous-menus

		self.boxesList = []
		self.createMenuBoxes()

		self.mainFrame.setStatusDone('Page des ' + self.pageName + ' créée !')

		
	def createMenuBoxes(self):

		self.groupBoxItinerary = self.menuBoxItinerary()
		DSTY.setBoxGeometry(self.groupBoxItinerary, 1, 4, 6, 2)
		self.boxesList.append(self.groupBoxItinerary)

		self.groupBoxCreateProject = self.menuBoxCreateProject()
		DSTY.setBoxGeometry(self.groupBoxCreateProject, 7, 4, 2, 2)
		self.boxesList.append(self.groupBoxCreateProject)

		self.groupBoxViewMap = self.menuBoxViewMap()
		DSTY.setBoxGeometry(self.groupBoxViewMap, 1, 7, 1, 2)
		self.boxesList.append(self.groupBoxViewMap)

		self.groupBoxCreateMap = self.menuBoxCreateMap()
		DSTY.setBoxGeometry(self.groupBoxCreateMap, 2, 7, 4, 2)
		self.boxesList.append(self.groupBoxCreateMap)
		
		self.groupBoxRenameMap = self.menuBoxRenameMap()
		DSTY.setBoxGeometry(self.groupBoxRenameMap, 6, 7, 1, 2)
		self.boxesList.append(self.groupBoxRenameMap)

		self.groupBoxFrameMap = self.menuBoxFrameMap()
		DSTY.setBoxGeometry(self.groupBoxFrameMap, 7, 7, 2, 2)
		self.boxesList.append(self.groupBoxFrameMap)

		self.groupBoxMapsFrame = self.menuBoxTableMapsFrame()
		DSTY.setBoxGeometry(self.groupBoxMapsFrame, 1, 10, 8, 17)
		self.boxesList.append(self.groupBoxMapsFrame)

		self.groupBoxMapsTable = self.menuBoxTableMapsView()
		DSTY.setBoxGeometry(self.groupBoxMapsTable, 1, 10, 8, 17, True)
		self.boxesList.append(self.groupBoxMapsTable)

		self.groupBoxMapsExportedTable = self.menuBoxTableMapsExportedView()
		DSTY.setBoxGeometry(self.groupBoxMapsExportedTable, 1, 10, 8, 17, True)
		self.boxesList.append(self.groupBoxMapsExportedTable)
		self.groupBoxMapsExportedTable.hide()


# ========================================================================================
# Actions : A la demande de la fenêtre principale
# ========================================================================================

#	Show - Ouverture de cette fenêtre

	def show(self):
		for box in self.boxesList: box.show(), box.repaint()
		self.groupBoxMapsExportedTable.hide()
		self.connectMapsLayer()
#		self.refreshMapsTable()											# Bad effect - clear map map when returning to the page
		self.refreshItineraryLists()
		self.deleteMapActive = False
		DSTY.setStyleMainButtonsInactive(self.buttonDeleteMap)

#	Hide - Ouverture d'une autre fenêtre

	def hide(self):
		for box in self.boxesList: box.hide()
		self.disconnectMapsLayer()

#	Close - Fermeture définitive

	def close(self):
		self.hide()
		for box in self.boxesList: del box

#	Help on this page

	def help(self):
		webbrowser.open_new_tab(QGP.configMenuHelpBasePath + 'QCarto - Page - ' + self.pageName + '.html')

	
# ========================================================================================
# Actions : Rafraichissement des listes d'itinéraires
# ========================================================================================

	def refreshItineraryLists(self):
		self.listTracksGRCodes  = LTRK.getOrderedListItineraryGR({'GR'}, self.mainFrame.dicoTracksGRFeatures)
		self.listTracksGRPCodes = LTRK.getOrderedListItineraryGR({'GRP'}, self.mainFrame.dicoTracksGRFeatures)
		self.listTracksGRTCodes = LTRK.getOrderedListItineraryGR({'GRT'}, self.mainFrame.dicoTracksGRFeatures)
		self.listTracksRICodes  = LTRK.getOrderedListItineraryRB({'RI'}, self.mainFrame.dicoTracksRBFeatures)
		self.listTracksRLCodes  = LTRK.getOrderedListItineraryRB({'RL'}, self.mainFrame.dicoTracksRBFeatures)
		self.listTracksRBCodes  = LTRK.getOrderedListItineraryRB({'RB'}, self.mainFrame.dicoTracksRBFeatures)
		self.listTracksRFCodes  = LTRK.getOrderedListItineraryRB({'RF'}, self.mainFrame.dicoTracksRBFeatures)
		self.listTracksIRCodes  = LTRK.getOrderedListItineraryRB({'IR'}, self.mainFrame.dicoTracksRBFeatures)
		self.listTracksZZCodes  = [ dir for dir in os.listdir(QGP.configPathProject) if os.path.isdir(QGP.configPathProject + dir) and dir[0:3] == 'ZZ-']
		
# ========================================================================================
# Connections au shape des emprises
# ========================================================================================
	
	def connectMapsLayer(self):
		if self.mainFrame.layerMaps == None: return
		self.mainFrame.layerMaps.featureAdded.connect(self.refreshMapsTable)
		self.mainFrame.layerMaps.featureDeleted.connect(self.refreshMapsTable)
		self.mainFrame.layerMaps.geometryChanged.connect(self.refreshMapsTable)
		self.mainFrame.layerMaps.attributeValueChanged.connect(self.refreshMapsTable)
		
	def disconnectMapsLayer(self):
		if self.mainFrame.layerMaps == None: return
		try:
			self.mainFrame.layerMaps.featureAdded.disconnect(self.refreshMapsTable)
			self.mainFrame.layerMaps.featureDeleted.disconnect(self.refreshMapsTable)
			self.mainFrame.layerMaps.geometryChanged.disconnect(self.refreshMapsTable)
			self.mainFrame.layerMaps.attributeValueChanged.disconnect(self.refreshMapsTable)
		except:
			pass
		
	def refreshMapsTable(self):
		if self.mainFrame.layerMaps == None: return
		if not self.automaticMapRefresh: return
		self.createMapsList()
		self.initializeMapsTable()
		self.initializeMapCreate()
	
	
# ========================================================================================
# Actions : Choix du Type d'itinéraire
# ========================================================================================
	
	def buttonRadioGR_clicked(self):
		self.itineraryCombo.clear()
		for code in self.listTracksGRCodes:
			self.itineraryCombo.addItem(code)
		self.typeSelected = 'GR'	
	
	def buttonRadioGRP_clicked(self):
		self.itineraryCombo.clear()
		for code in self.listTracksGRPCodes:
			self.itineraryCombo.addItem(code)
		self.typeSelected = 'GRP'	
	
	def buttonRadioGRT_clicked(self):
		self.itineraryCombo.clear()
		for code in self.listTracksGRTCodes:
			self.itineraryCombo.addItem(code)
		self.typeSelected = 'GRT'	

	def buttonRadioRI_clicked(self):
		self.itineraryCombo.clear()
		for code in self.listTracksRICodes:
			self.itineraryCombo.addItem(code)
		self.typeSelected = 'RI'	

	def buttonRadioRL_clicked(self):
		self.itineraryCombo.clear()
		for code in self.listTracksRLCodes:
			self.itineraryCombo.addItem(code)
		self.typeSelected = 'RL'	

	def buttonRadioRB_clicked(self):
		self.itineraryCombo.clear()
		for code in self.listTracksRBCodes:
			self.itineraryCombo.addItem(code)
		self.typeSelected = 'RB'	

	def buttonRadioRF_clicked(self):
		self.itineraryCombo.clear()
		for code in self.listTracksRFCodes:
			self.itineraryCombo.addItem(code)
		self.typeSelected = 'RF'	

	def buttonRadioIR_clicked(self):
		self.itineraryCombo.clear()
		for code in self.listTracksIRCodes:
			self.itineraryCombo.addItem(code)
		self.typeSelected = 'IR'	

	def buttonRadioZZ_clicked(self):
		self.itineraryCombo.clear()
		for code in self.listTracksZZCodes:
			self.itineraryCombo.addItem(code)
		self.typeSelected = 'ZZ'	

	
# ========================================================================================
# Actions : Afficher ! 		Définition de la liste affichée des cartes
#							Ajouter la couche des emprises
#							Ajouter les couches du groupe : projet actif
# ========================================================================================	
	
	def createMapsView(self):
		
		self.mainFrame.setStatusWorking('Affichage des cartes du projet - vérifications ...')
		self.deactivateCreationProject()

#		Déactiver la suppression de cartes

		self.deleteMapActive = False
		DSTY.setStyleMainButtonsInactive(self.buttonDeleteMap)

#		Déconnecter et effacer le nouveau nom 

		self.mapNewNameClear()
		try:
			self.groupBoxMapsTable.itemChanged.disconnect()
		except:
			pass

#		Vérifier si le répertoire des emprises du projet correspondant à l'itinéraire existe 		
	
		itinerarySelected = self.itineraryCombo.currentText()
		if (itinerarySelected.strip() == ''):
			self.mainFrame.setStatusWarning('Pas d\'itinéraire sélectionné !')
			return
	
		self.itinerarySelected = itinerarySelected
		projectsList = os.listdir(QGP.configPathProject)
		if itinerarySelected not in projectsList:
			self.activateCreationProject()
			self.mainFrame.setStatusWarning('Le répertoire projet : ' + QGP.configPathProject + self.itinerarySelected + ' n\'existe pas !') 
			return 
		
		projectFrameDir = QGP.configPathProjectFramesGeneric.replace('%PROJECT%', self.itinerarySelected)
		if not os.path.isdir(projectFrameDir):
			self.activateCreationProject()
			self.mainFrame.setStatusWarning('Le répertoire des emprises : ' + projectFrameDir + ' n\'existe pas !') 
			return		

#		Vérifier si le shape des emprises existe
			
		projectFrameFile = 	projectFrameDir + QGP.configShapeFrameName + '.shp'
		if not os.path.isfile(projectFrameFile):
			self.activateCreationProject()
			self.mainFrame.setStatusWarning('Le fichier shape des emprises : ' + projectFrameFile + ' n\'existe pas !') 
			return		
		
#		Vérifier si on ne va pas supprimer des couches encore en édition
			
		if TLAY.isLayerInGroupModified(QGP.configFrameGroupName):
			self.mainFrame.setStatusWarning('Le fichier actuel des emprises - qui serait supprimé - est ouvert en mode édition !')
			return		

		if TLAY.isLayerInGroupModified(QGP.configActiveProjectGroupName):
			self.mainFrame.setStatusWarning('Au moins un fichier - qui serait supprimé - est en mode édition dans le groupe : ' + QGP.configActiveProjectGroupName + ' !')
			return		

#		Afficher l'itinéraire

		self.viewMapItineraryInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%',self.itinerarySelected))
		DSTY.setStyleOkLabel(self.viewMapItineraryInfo, "Normal")

#		Enlever les couches du projet existant

		self.mainFrame.setStatusWorking('Affichage des cartes du projet - suppression des couches existantes ...')

		self.highlightedMap = None
		self.disconnectMapsLayer()
		TLAY.removeLayerFromGroup(QGP.configFrameGroupName, QGP.configShapeFrameName)
		TLAY.cleanLayerGroup(QGP.configActiveProjectGroupName)
		self.mainFrame.layerMaps = None

#		Ajouter la couche des emprises du projet

		self.mainFrame.setStatusWorking('Affichage des cartes du projet - ajout de la couche des emprises cartes ...')

		self.mainFrame.layerMaps, error = LFRM.addFrameShape(projectFrameDir)
		if error != None:
			self.mainFrame.setStatusWarning(error)
			return		

#		Ajouter les couches du projet actif

		self.mainFrame.setStatusWorking('Affichage des cartes du projet - ajout des couches TEC et SNCB ...')

		projectActiveDir = QGP.configPathProjectShapesGeneric.replace('%PROJECT%', self.itinerarySelected)
		self.mainFrame.layerTEC, error = TLAY.loadLayer(projectActiveDir, QGP.configShapeProjectNameTEC, QGP.configActiveProjectGroupName, QGP.configShapeProjectNameTEC, None, None, False)
		if error != None:
			self.mainFrame.setStatusWarning(error)
			return		

		self.mainFrame.layerSNCB, error = TLAY.loadLayer(projectActiveDir, QGP.configShapeProjectNameSNCB, QGP.configActiveProjectGroupName, QGP.configShapeProjectNameSNCB, None, None, False)
		if error != None:
			self.mainFrame.setStatusWarning(error)
			return		

#		Connecter la couche et afficher la table

		self.connectMapsLayer()
		self.createMapsList()
		self.initializeMapsTable()
		self.initializeMapCreate()
				
#		Connecter le changement de nom				
				
		self.groupBoxMapsTable.itemChanged.connect(self.mapNewNameChanged)				
				
#		Analyser la Tables des POIs pour les RF

		if TCOD.itineraryTypeFromTrackCode(self.itinerarySelected) == 'RF' :
			if self.mainFrame.layerPOIs == None:
				self.mainFrame.setStatusWarning('Affichage des cartes du projet - Sans accès à la Table des POIs')
				return
				
#		Terminé		

		self.mainFrame.setStatusDone('Affichage des cartes du projet - OK')
		
	def createMapsList(self):
		self.listMapsFeatures = [ mapFeature for mapFeature in self.mainFrame.layerMaps.getFeatures() ]
	

# ========================================================================================
# Actions : Demande de la Page Carte Active
# ========================================================================================	

	def viewActiveMap(self):
	
#		Vérifier si on a bien une carte sélectionnée 	
	
		if self.selectedMapFeature == None:
			self.mainFrame.setStatusWarning('Sélectionner au préalable une - et une seule - carte dans la table !')
			return		
		
#		Déactiver la suppression de cartes

		self.deleteMapActive = False
		DSTY.setStyleMainButtonsInactive(self.buttonDeleteMap)

#		Vérifier si on ne va pas supprimer des couches encore en édition
			
		if TLAY.isLayerInGroupModified(QGP.configActiveMapGroupName):
			self.mainFrame.setStatusWarning('Au moins un fichier - qui serait supprimé - est en mode édition dans le groupe : ' + QGP.configActiveMapGroupName + ' !')
			return		

# 		Enlever les couches du groupe carte active

		self.mainFrame.setStatusWorking('Affichage des repères et parcours de la carte active cartes du projet - suppression des couches existantes ...')
		TLAY.cleanLayerGroup(QGP.configActiveMapGroupName)
		self.mainFrame.layerActiveMapPoints 		= None
		self.mainFrame.layerActiveMapPoisRF 		= None
		self.mainFrame.layerActiveMapSections 		= None
		self.mainFrame.layerActiveMapLabels			= None
		self.mainFrame.layerActiveMapLabelsSimple	= None

#		Vérifier si les shapes des repères, pois RF, parcours et labels existent

		mapFolder = self.selectedMapFeature[QGP.tableFramesFieldFolder] 		
		if not os.path.isfile(mapFolder + QGP.configShapeMapReperes + '.shp'):
			self.mainFrame.setStatusWarning('Le fichier shape des repères : ' + QGP.configShapeMapReperes + ' n\'existe pas dans ' + mapFolder + ' !') 
			return		
		if not os.path.isfile(mapFolder + QGP.configShapeMapLabels + '.shp'):
			self.mainFrame.setStatusWarning('Le fichier shape des étiquettes : ' + QGP.configShapeMapLabels + ' n\'existe pas dans ' + mapFolder + ' !') 
			return		
		if not os.path.isfile(mapFolder + QGP.configShapeMapLabelsSimple + '.shp'):													
			status, count = TFIL.copy_files(QGP.configPathActiveMap, mapFolder, QGP.configShapeMapLabelsSimple)								# Ajout automatique car pas présent au début de la Version 7
			if status:
				self.mainFrame.setStatusWorking('Etiquettes Simples : ' + QGP.configPathActiveMap + QGP.configShapeMapLabelsSimple + ' : ' + str(count) + ' fichiers créés !')
				TDAT.sleep(1000)
			else:			
				self.mainFrame.setStatusError('Etiquettes Simples : ajout du shape de référence des étiquettes simples impossible ?', False)
				return				
		if not os.path.isfile(mapFolder + QGP.configShapeMapSections + '.shp'):
			self.mainFrame.setStatusWarning('Le fichier shape des tronçons : ' + QGP.configShapeMapSections + ' n\'existe pas dans ' + mapFolder + ' !') 
			return		

		if TCOD.itineraryTypeFromTrackCode(self.itinerarySelected) == 'RF':																
			if not os.path.isfile(mapFolder + QGP.configShapeMapPoiRF + '.shp'):													
				status, count = TFIL.copy_files(QGP.configPathActiveMap, mapFolder, QGP.configShapeMapPoiRF)								# Ajout automatique car pas présent au début de la Version 7
				if status:
					self.mainFrame.setStatusWorking('Points Intéret RF : ' + QGP.configPathActiveMap + QGP.configShapeMapPoiRF + ' : ' + str(count) + ' fichiers créés !')
					TDAT.sleep(1000)
				else:			
					self.mainFrame.setStatusError('Points Intéret RF : ajout du shape de référence des Pois RF impossible ?', False)
					return				

#		Changer échelle pour les couches du projet actif

		QgsExpressionContextUtils.setLayerVariable(self.mainFrame.layerTEC, QGP.tableMapsActiveMapVariableScale,str(self.selectedMapFeature[QGP.tableFramesFieldEchelle]))
		QgsExpressionContextUtils.setLayerVariable(self.mainFrame.layerSNCB, QGP.tableMapsActiveMapVariableScale,str(self.selectedMapFeature[QGP.tableFramesFieldEchelle]))

#		Ajouter les shapes des repères, pois RF, parcours et labels

		self.mainFrame.layerActiveMapPoints, self.mainFrame.layerActiveMapPointsError = \
				TLAY.loadLayer(mapFolder, QGP.configShapeMapReperes, QGP.configActiveMapGroupName, QGP.configShapeMapReperes, None, None, False)
		if self.mainFrame.layerActiveMapPoints == None:
			self.mainFrame.setStatusError(self.mainFrame.layerActiveMapPointsError, False)
			return		
		QgsExpressionContextUtils.setLayerVariable(self.mainFrame.layerActiveMapPoints,QGP.tableMapsActiveMapVariableScale,str(self.selectedMapFeature[QGP.tableFramesFieldEchelle]))

		self.mainFrame.layerActiveMapLabels, self.mainFrame.layerActiveMapLabelsError = \
				TLAY.loadLayer(mapFolder, QGP.configShapeMapLabels, QGP.configActiveMapGroupName, QGP.configShapeMapLabels, None, None, False)
		if self.mainFrame.layerActiveMapLabels == None:
			self.mainFrame.setStatusError(self.mainFrame.layerActiveMapLabelsError, False)
			return		
		QgsExpressionContextUtils.setLayerVariable(self.mainFrame.layerActiveMapLabels,QGP.tableMapsActiveMapVariableScale,str(self.selectedMapFeature[QGP.tableFramesFieldEchelle]))

		self.mainFrame.layerActiveMapLabelsSimple, self.mainFrame.layerActiveMapLabelsSimpleError = \
				TLAY.loadLayer(mapFolder, QGP.configShapeMapLabelsSimple, QGP.configActiveMapGroupName, QGP.configShapeMapLabelsSimple, None, None, False)
		if self.mainFrame.layerActiveMapLabelsSimple == None:
			self.mainFrame.setStatusError(self.mainFrame.layerActiveMapLabelsSimpleError, False)
			return		
		QgsExpressionContextUtils.setLayerVariable(self.mainFrame.layerActiveMapLabelsSimple,QGP.tableMapsActiveMapVariableScale,str(self.selectedMapFeature[QGP.tableFramesFieldEchelle]))

		self.mainFrame.layerActiveMapSections, self.mainFrame.layerActiveMapSectionsError = \
				TLAY.loadLayer(mapFolder, QGP.configShapeMapSections, QGP.configActiveMapGroupName, QGP.configShapeMapSections, None, None, False)
		if self.mainFrame.layerActiveMapSections == None:
			self.mainFrame.setStatusError(self.mainFrame.layerActiveMapSectionsError, False)
			return		
		QgsExpressionContextUtils.setLayerVariable(self.mainFrame.layerActiveMapSections,QGP.tableMapsActiveMapVariableScale,str(self.selectedMapFeature[QGP.tableFramesFieldEchelle]))

		if TCOD.itineraryTypeFromTrackCode(self.itinerarySelected) == 'RF':																
			self.mainFrame.layerActiveMapPoisRF, self.mainFrame.layerActiveMapPoisRFError = \
				TLAY.loadLayer(mapFolder, QGP.configShapeMapPoiRF, QGP.configActiveMapGroupName, QGP.configShapeMapPoiRF, None, None, False)
			if self.mainFrame.layerActiveMapPoisRF == None:
				self.mainFrame.setStatusError(self.mainFrame.layerActiveMapPoisRFError, False)
				return		
			QgsExpressionContextUtils.setLayerVariable(self.mainFrame.layerActiveMapPoisRF,QGP.tableMapsActiveMapVariableScale,str(self.selectedMapFeature[QGP.tableFramesFieldEchelle]))

		TLAY.foldLayersGroup(QGP.configActiveMapGroupName)

#		Définir la carte comme active

		QgsExpressionContextUtils.setProjectVariable(QgsProject.instance(),QGP.tableMapsActiveMapVariableHighlight,self.selectedMapFeature[QGP.tableFramesFieldName])
		QgsExpressionContextUtils.setProjectVariable(QgsProject.instance(),QGP.tableMapsActiveMapVariableScale,str(self.selectedMapFeature[QGP.tableFramesFieldEchelle]))
		QgsExpressionContextUtils.setProjectVariable(QgsProject.instance(),QGP.tableMapsActiveMapVariableEditMode,'Edition')
		self.highlightedMap = self.selectedMapFeature[QGP.tableFramesFieldName]

#		Zoomer sur cette carte

		self.iface.mapCanvas().setExtent(self.selectedMapFeature.geometry().boundingBox())
		self.iface.mapCanvas().zoomScale(min(self.configZoomMapScale, self.selectedMapFeature[QGP.tableFramesFieldEchelle]) if self.selectedMapFeature[QGP.tableFramesFieldEchelle] < 100000 else self.selectedMapFeature[QGP.tableFramesFieldEchelle])

#		Demander l'affichage de la page : Carte Active

		self.mainFrame.setStatusWorking('Demande de chargement de la page : Carte Active ...')
		self.mainFrame.selectedMapFeature = self.selectedMapFeature
		self.mainFrame.requestPage('Carte Active')


# ========================================================================================
# Actions : Création de Projet
# ========================================================================================	
		
	def createProject(self):
		if self.createProjectActive == False :
			self.mainFrame.setStatusWarning('Sélectionner au préalable un itinéraire encore sans projet !')
			return		

#		Créer le répertoire projet et celui des emprises

		projectFrameDir = QGP.configPathProjectFramesGeneric.replace('%PROJECT%', self.itinerarySelected)
		TFIL.ensure_dir(projectFrameDir)
		
#		Copier les fichiers du shape des emprises		

		status, count = TFIL.copy_files(QGP.configPathFrame, projectFrameDir, QGP.configShapeFrameName)
		if status:
			self.mainFrame.setStatusWorking('Fichiers : ' + QGP.configPathFrame + QGP.configShapeFrameName + ' : ' + str(count) + ' fichiers créés !')
			TDAT.sleep(600)
		else:			
			self.mainFrame.setStatusError(self.itinerarySelected + ' - ' + QGP.configShapeFrameName + ' : Copie du shape de référence des emprises impossible ?', False)
			return

		self.createProjectActive = False
		self.mainFrame.setStatusDone(self.itinerarySelected + ' : Shape des emprises initialisé - OK')
		
#		Copier les couches shape du projet actif 		
		
		projectActiveDir = QGP.configPathProjectShapesGeneric.replace('%PROJECT%', self.itinerarySelected)
		TFIL.ensure_dir(projectActiveDir)

		for shapeName in (QGP.configShapeProjectNameTEC, QGP.configShapeProjectNameSNCB):
			status, count = TFIL.copy_files(QGP.configPathActiveProject, projectActiveDir, shapeName)
		if status:
			self.mainFrame.setStatusWorking('Fichiers : ' + QGP.configPathActiveProject + shapeName + ' : ' + str(count) + ' fichiers créés !')
			TDAT.sleep(600)
		else:			
			self.mainFrame.setStatusError(self.itinerarySelected + ' - ' + QGP.configPathActiveProject + ' : Copie du shape de référence : ' + shapeName + ' impossible ?', False)
			return
		
#		Terminé		
		
		self.createProjectActive = False
		self.mainFrame.setStatusDone(self.itinerarySelected + ' : Shape des emprises et du projet initialisés - OK')
			
	def activateCreationProject(self):
		self.createProjectPath.setText(DSTY.textFormatBlackNormal.replace('%TEXT%',self.itinerarySelected))
		DSTY.setStyleOkLabel(self.createProjectPath, 'Normal')
		DSTY.setStyleMainButtons(self.buttonCreateProject)
		self.createProjectActive = True
		
	def deactivateCreationProject(self):
		self.createProjectPath.setText(DSTY.textFormatBlackNormal.replace('%TEXT%','. . .'))
		DSTY.setStyleWarningLabel(self.createProjectPath, 'Normal')
		DSTY.setStyleMainButtonsInactive(self.buttonCreateProject)
		self.createProjectActive = False


# ========================================================================================
# Actions : Création d'une Carte
# ========================================================================================	

	def initializeMapCreate(self):
		try:
			self.createMapItineraryCombo.currentTextChanged.disconnect()
		except:
			pass

		self.createMapItineraryCombo.clear()
		if self.typeSelected in QGP.typeSetModeGR :
			self.createMapItineraryCombo.addItem(self.itinerarySelected)	
		if self.typeSelected in QGP.typeSetModeRB.union(QGP.typeSetModeIR) :
			itineraryList = list({code for code in self.mainFrame.dicoTracksRBFeatures if self.itinerarySelected in code and TCOD.isCodeBaseRB(code)})
			if itineraryList == []: itineraryList = [self.itinerarySelected]										#¨Patch added for cases like SGR65 when no base RB
			itineraryList = [self.itinerarySelected + '-T1', self.itinerarySelected + '-T2', self.itinerarySelected + '-T3'] + itineraryList
			itineraryList.sort()
			for code in itineraryList:
				self.createMapItineraryCombo.addItem(code)	
			self.createMapItineraryCombo.currentTextChanged.connect(self.setNewMapDefaultName)
		if  self.typeSelected in QGP.typeSetModeNone :
			self.createMapItineraryCombo.addItem(self.itinerarySelected)	
		self.setNewMapDefaultName()
	
	def setNewMapDefaultName(self):
		newMapItinerary = self.createMapItineraryCombo.currentText()
		if newMapItinerary[-3:] not in ('-T1', '-T2', '-T3') : 
			try:
				self.createMapName.setText(self.mainFrame.dicoTracksRBFeatures[newMapItinerary][QGP.tableTracksFieldName].split(' - ')[1])
			except:
				pass
		else:
			self.createMapName.setText('Globale')
	
	def createNewMap(self):
	
#		Retrouver les paramètres de la nouvelle carte

		newMapItinerary = self.createMapItineraryCombo.currentText()
		newMapName = self.createMapName.text()
		newMapScale = int(self.createMapScaleCombo.currentText())
		newMapFormat = self.createMapFormatCombo.currentText()
		newMapWidth = QGP.dicoPaperFormats[newMapFormat][0] * newMapScale / 1000
		newMapHeight = QGP.dicoPaperFormats[newMapFormat][1] * newMapScale / 1000
		newMapBackground = QGP.exportBackgroundIGN50Ed4
		newMapFolder = QGP.configPathMapShapes.replace('%PROJECT%', TCOD.itineraryFolderFromTrackCode(newMapItinerary)) + newMapItinerary + ' - ' + newMapName + '/'
		
#		Vérifier si la couche des emprises existe

		if self.mainFrame.layerMaps == None: 
			self.mainFrame.setStatusWarning('Il n\'y a pas encore de shape des emprises sur le canevas !')
			return		
	
#		Vérifier si le nom est défini

		if newMapName == '':
			self.mainFrame.setStatusWarning('Le nom de la carte n\'est pas défini !')
			return		

#		Vérifier si la carte n'existe pas déjà 

		for mapFeature in self.listMapsFeatures:
			if mapFeature[QGP.tableFramesFieldItineraryCode] == newMapItinerary and mapFeature[QGP.tableFramesFieldName] == newMapName:
				self.mainFrame.setStatusWarning('La carte demandée existe déjà !')
				return		

#		Vérifier si le canevas n'est pas trop large. Uniquement pour les cartes au 1:50000 ou plus grand

		if newMapScale <= 50000:
			if self.iface.mapCanvas().scale() > QGP.configCreateMapMaxScale + 10:									
				self.mainFrame.setStatusWarning('Centrer le canavas Qgis avec une échelle de maximum 1:' +  str(QGP.configCreateMapMaxScale) + ' !')
				return		
		
#		Créer les 4 points d'un rectangle au centre du canevas

		centerPoint = self.iface.mapCanvas().center()
		PNO = QgsPointXY(centerPoint.x() - newMapWidth / 2, centerPoint.y() + newMapHeight / 2)
		PNE = QgsPointXY(centerPoint.x() + newMapWidth / 2, centerPoint.y() + newMapHeight / 2)
		PSE = QgsPointXY(centerPoint.x() + newMapWidth / 2, centerPoint.y() - newMapHeight / 2)
		PSO = QgsPointXY(centerPoint.x() - newMapWidth / 2, centerPoint.y() - newMapHeight / 2)

#		Créer la nouvelle entité

		newMapFeature = QgsFeature()
		newMapFeature.setFields(self.mainFrame.layerMaps.fields())
		newMapFeature[QGP.tableFramesFieldItineraryCode] 	= newMapItinerary
		newMapFeature[QGP.tableFramesFieldName] 		 	= newMapName
		newMapFeature[QGP.tableFramesFieldFormat] 		 	= newMapFormat
		newMapFeature[QGP.tableFramesFieldEchelle] 		 	= newMapScale
		newMapFeature[QGP.tableFramesFieldBackground]	 	= newMapBackground
		newMapFeature[QGP.tableFramesFieldFolder] 			= newMapFolder
		newMapFeature.setGeometry(QgsGeometry.fromMultiPolygonXY([[[PNO,PNE,PSE,PSO]]]))

#		Ajouter l'entité

		self.automaticMapRefresh = False		
		self.mainFrame.layerMaps.startEditing()
		self.mainFrame.layerMaps.addFeature(newMapFeature)
		self.mainFrame.layerMaps.commitChanges()
		self.automaticMapRefresh = True		

#		Définir la carte active 

		QgsExpressionContextUtils.setProjectVariable(QgsProject.instance(),QGP.tableMapsActiveMapVariableHighlight,newMapName)	

#		Créer le folder des shapes de la carte

		TFIL.ensure_dir(newMapFolder)

#		Copier les fichiers du shape des Points Repères

		status, count = TFIL.copy_files(QGP.configPathActiveMap, newMapFolder, QGP.configShapeMapReperes)
		if status:
			self.mainFrame.setStatusWorking(newMapItinerary + ' - ' + newMapName + ' : Fichiers ' + QGP.configPathActiveMap + QGP.configShapeMapReperes + ' : ' + str(count) + ' fichiers créés !')
			TDAT.sleep(600)
		else:			
			self.mainFrame.setStatusError(newMapItinerary + ' - ' + newMapName + ' : Copie du shape de référence des repères impossible ?', False)
			return

#		Copier les fichiers du shape des Etiquettes

		status, count = TFIL.copy_files(QGP.configPathActiveMap, newMapFolder, QGP.configShapeMapLabels)
		if status:
			self.mainFrame.setStatusWorking(newMapItinerary + ' - ' + newMapName + ' : Fichiers ' + QGP.configPathActiveMap + QGP.configShapeMapLabels + ' : ' + str(count) + ' fichiers créés !')
			TDAT.sleep(600)
		else:			
			self.mainFrame.setStatusError(newMapItinerary + ' - ' + newMapName + ' : Copie du shape de référence des étiquettes impossible ?', False)
			return

		status, count = TFIL.copy_files(QGP.configPathActiveMap, newMapFolder, QGP.configShapeMapLabelsSimple)
		if status:
			self.mainFrame.setStatusWorking(newMapItinerary + ' - ' + newMapName + ' : Fichiers ' + QGP.configPathActiveMap + QGP.configShapeMapLabelsSimple + ' : ' + str(count) + ' fichiers créés !')
			TDAT.sleep(600)
		else:			
			self.mainFrame.setStatusError(newMapItinerary + ' - ' + newMapName + ' : Copie du shape de référence des étiquettes simples impossible ?', False)
			return

#		Copier les fichiers du shape des Tronçons

		status, count = TFIL.copy_files(QGP.configPathActiveMap, newMapFolder, QGP.configShapeMapSections)
		if status:
			self.mainFrame.setStatusWorking(newMapItinerary + ' - ' + newMapName + ' : Fichiers ' + QGP.configPathActiveMap + QGP.configShapeMapSections + ' : ' + str(count) + ' fichiers créés !')
			TDAT.sleep(600)
		else:			
			self.mainFrame.setStatusError(newMapItinerary + ' - ' + newMapName + ' : Copie du shape de référence des tronçons impossible ?', False)
			return

#		Copier les fichiers du shape des Pois RF

		if TCOD.itineraryTypeFromTrackCode(self.itinerarySelected) == 'RF':																
			status, count = TFIL.copy_files(QGP.configPathActiveMap, newMapFolder, QGP.configShapeMapPoiRF)
			if status:
				self.mainFrame.setStatusWorking(newMapItinerary + ' - ' + newMapName + ' : Fichiers ' + QGP.configPathActiveMap + QGP.configShapeMapPoiRF + ' : ' + str(count) + ' fichiers créés !')
				TDAT.sleep(600)
			else:			
				self.mainFrame.setStatusError(newMapItinerary + ' - ' + newMapName + ' : Copie du shape de référence des Pois RF impossible ?', False)
				return

#		Terminé

		self.refreshMapsTable()									
		self.mainFrame.setStatusDone('La carte : ' + newMapName + ' a été ajoutée - OK')
	

# ========================================================================================
# Actions : Recadrage d'une Carte / Recadrage rectangulaire
# ========================================================================================	

	def reframeMap(self):
	
#		Vérifier si on a bien une carte sélectionnée 	
	
		if self.selectedMapFeature == None:
			self.mainFrame.setStatusWarning('Sélectionner au préalable une - et une seule - carte dans la table !')
			return
		
#		Retrouver les paramètres de la nouvelle carte

		newMapScale = int(self.reframeMapScaleCombo.currentText())
		newMapFormat = self.reframeMapFormatCombo.currentText()
		newMapWidth = QGP.dicoPaperFormats[newMapFormat][0] * newMapScale / 1000
		newMapHeight = QGP.dicoPaperFormats[newMapFormat][1] * newMapScale / 1000

#		Créer les 4 points du nouveau rectangle en gardant le même centre

		centerPoint = self.selectedMapFeature.geometry().boundingBox().center()
		PNO = QgsPointXY(centerPoint.x() - newMapWidth / 2, centerPoint.y() + newMapHeight / 2)
		PNE = QgsPointXY(centerPoint.x() + newMapWidth / 2, centerPoint.y() + newMapHeight / 2)
		PSE = QgsPointXY(centerPoint.x() + newMapWidth / 2, centerPoint.y() - newMapHeight / 2)
		PSO = QgsPointXY(centerPoint.x() - newMapWidth / 2, centerPoint.y() - newMapHeight / 2)

#		Modifier la géométrie de l'entité

		self.automaticMapRefresh = False		
		self.mainFrame.layerMaps.startEditing()
		self.mainFrame.layerMaps.changeAttributeValue(self.selectedMapFeature.id(), self.selectedMapFeature.fieldNameIndex(QGP.tableFramesFieldEchelle), newMapScale)
		self.mainFrame.layerMaps.changeAttributeValue(self.selectedMapFeature.id(), self.selectedMapFeature.fieldNameIndex(QGP.tableFramesFieldFormat), newMapFormat)
		self.mainFrame.layerMaps.changeGeometry(self.selectedMapFeature.id(), QgsGeometry.fromMultiPolygonXY([[[PNO,PNE,PSE,PSO]]]))
		self.mainFrame.layerMaps.commitChanges()
		self.automaticMapRefresh = True

#		Terminé

		self.refreshMapsTable()																	
		self.mainFrame.setStatusDone('La carte a été recadrée - OK')
		
		
	def reframeMapRectangle(self):
	
#		Vérifier si on a bien une carte sélectionnée 	
	
		if self.selectedMapFeature == None:
			self.mainFrame.setStatusWarning('Sélectionner au préalable une - et une seule - carte dans la table !')
			return
		
#		Vérifier si la carte est déjà rectangulaire

		geometry = self.selectedMapFeature.geometry()
		if geometry.isNull(): self.mainFrame.setStatusWarning('Cette carte n\'a pas de géométrie définie ?') ; return
		if geometry.length() == geometry.boundingBox().width() * 2 + geometry.boundingBox().height() * 2: self.mainFrame.setStatusWarning('Cette carte a déjà une géométrie rectangulaire ?') ; return

#		Déterminer la nouvelle géométrie

		newGeometry = geometry.boundingBox()
		PNO = QgsPointXY(newGeometry.xMinimum(), newGeometry.yMaximum())
		PNE = QgsPointXY(newGeometry.xMaximum(), newGeometry.yMaximum())
		PSE = QgsPointXY(newGeometry.xMaximum(), newGeometry.yMinimum())
		PSO = QgsPointXY(newGeometry.xMinimum(), newGeometry.yMinimum())

#		Modifier la géométrie de l'entité

		self.automaticMapRefresh = False		
		self.mainFrame.layerMaps.startEditing()
		self.mainFrame.layerMaps.changeGeometry(self.selectedMapFeature.id(), QgsGeometry.fromMultiPolygonXY([[[PNO,PNE,PSE,PSO]]]))
		self.mainFrame.layerMaps.commitChanges()
		self.automaticMapRefresh = True

#		Terminé

		self.refreshMapsTable()																	
		self.mainFrame.setStatusDone('La carte a été rectangularisée - OK')
		
		
# ========================================================================================
# Actions : Suppression d'une Carte
# ========================================================================================	
		
	def deleteMap(self):

		if not self.deleteMapActive:
			self.mainFrame.setStatusWarning('La fonction n\'est pas activée - Cliquez droit - Attention : irréversible !')
			return
		
		if self.selectedMapFeature == None:
			self.mainFrame.setStatusWarning('Sélectionnez au préalable une - et une seule - carte dans la table !')
			return

		self.deleteMapActive = False
		DSTY.setStyleMainButtonsInactive(self.buttonDeleteMap)

		try:
			shutil.rmtree(self.selectedMapFeature[QGP.tableFramesFieldFolder])
		except:
			self.mainFrame.setStatusError('Le répertoire de la carte n\'existe plus ?', False)
			TDAT.sleep(2000)		

		self.automaticMapRefresh = False		
		self.mainFrame.layerMaps.startEditing()
		self.mainFrame.layerMaps.deleteFeature(self.selectedMapFeature.id())
		self.mainFrame.layerMaps.commitChanges()
		self.automaticMapRefresh = True
		
		self.refreshMapsTable()																	
		self.mainFrame.setStatusDone('La carte a été supprimée définitivement - OK')
	
	def activateDeleteMap(self):
		self.deleteMapActive = True
		DSTY.setStyleWarningButton(self.buttonDeleteMap)


# ========================================================================================
# Actions : Renommage d'une Carte
# ========================================================================================	

	def mapNewNameClear(self):
		self.mapNewNameText = None
		self.mapNewNameRow = None
		self.viewMapNewnameInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%','. . .'))
		DSTY.setStyleWarningLabel(self.viewMapNewnameInfo, "Normal")
		DSTY.setStyleMainButtonsInactive(self.buttonRenameMap)

	def mapNewNameChanged(self, item):
		self.mapNewNameText = item.text()
		self.mapNewNameRow = item.row()
		self.viewMapNewnameInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%',self.mapNewNameText))
		DSTY.setStyleOkLabel(self.viewMapNewnameInfo, "Normal")
		DSTY.setStyleNormalButton(self.buttonRenameMap)

	def renameMap(self, item):
		if self.mapNewNameText == None:
			self.mainFrame.setStatusWarning('Vous n\'avez pas défini de nouveau nom pour la carte !')
			return
			
		if TLAY.isLayerInGroupModified(QGP.configActiveMapGroupName):
			self.mainFrame.setStatusWarning('Au moins un fichier - qui serait supprimé - est en mode édition dans le groupe : ' + QGP.configActiveMapGroupName + ' !')
			return		
			
		self.mainFrame.setStatusWorking('Changement du nom de la carte ...')
			
		TLAY.cleanLayerGroup(QGP.configActiveMapGroupName)
		self.mainFrame.layerActiveMapPoints 		= None
		self.mainFrame.layerActiveMapPoisRF 		= None
		self.mainFrame.layerActiveMapSections 		= None
		self.mainFrame.layerActiveMapLabels			= None
		self.mainFrame.layerActiveMapLabelsSimple	= None
		self.mainFrame.selectedMapFeature 			= None
		self.selectedMapFeature 					= None
		TDAT.sleep(2000)

		mapFeature = self.listMapsViewFeatures[self.mapNewNameRow]
		itinerary = mapFeature[QGP.tableFramesFieldItineraryCode]
		oldName = mapFeature[QGP.tableFramesFieldName]
		newName = self.mapNewNameText		
		oldFolder = mapFeature[QGP.tableFramesFieldFolder]		
		oldFolderParts = oldFolder.split('/')
		oldFolderParts[-2] = itinerary + ' - ' + newName
		newFolder = '/'.join(oldFolderParts)
		
		self.mainFrame.setStatusWorking('Changement du nom de la carte : ' + str(oldName) + ' >>> ' + str(newName) + ' ...')
		
		try: 
			os.rename(oldFolder, newFolder)
		except:
			self.mainFrame.setStatusError('Impossible de renommer le répertoire de la carte ?', False)
			TDAT.sleep(2000)	
			return	
	
		self.automaticMapRefresh = False		
		self.mainFrame.layerMaps.startEditing()
		self.mainFrame.layerMaps.changeAttributeValue(mapFeature.id(), mapFeature.fieldNameIndex(QGP.tableFramesFieldName), newName)
		self.mainFrame.layerMaps.changeAttributeValue(mapFeature.id(), mapFeature.fieldNameIndex(QGP.tableFramesFieldFolder), newFolder)
		self.mainFrame.layerMaps.commitChanges()
		self.automaticMapRefresh = True
		
		self.mapNewNameClear()
		self.createMapsView()																	
		self.mainFrame.setStatusDone('La carte a été renommée : ' + oldName + ' >>> ' + newName + ' !')


# ========================================================================================
# Opérations sur la Table des Cartes
# ========================================================================================	

#	Changement de sélection dans la table

	def mapsTable_SelectionChanged(self):
		self.listMapsSelectedRows = list({item.row() for item in self.groupBoxMapsTable.selectedItems()})

		if len(self.listMapsSelectedRows) == 1:																						# Just on Map selected !
			selectedMapRow = self.listMapsSelectedRows[0]
			self.selectedMapFeature = self.listMapsViewFeatures[selectedMapRow]
			self.viewMapNameInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%',str(self.selectedMapFeature[QGP.tableFramesFieldName])))
			DSTY.setStyleOkLabel(self.viewMapNameInfo, "Normal")
			DSTY.setStyleMainButtons(self.buttonViewMap)
		else:																														# Several lines selected - cannot view map		
			self.selectedMapFeature = None
			self.viewMapNameInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%','. . .'))
			DSTY.setStyleWarningLabel(self.viewMapNameInfo, "Normal")
			DSTY.setStyleMainButtonsInactive(self.buttonViewMap)

#	Clic sur un élement de la table

	def mapsTable_itemClicked(self, item):
		label = QGP.mapsTableQView[item.column()][0]
		self.showMapsTableElementInfo(item, label)


#	Définition d'un item de la table

	def createItem(self, value, changeable = False):

		itemFont = QFont()
		itemFont.setPixelSize(DSTY.tableItemFontSize)
		
		itemText = str(value)

		item = QtWidgets.QTableWidgetItem(itemText)
		item.setFont(itemFont)
		if not changeable : item.setFlags(item.flags() & ~Qt.ItemIsEditable)

		return item

#	Initialisation de la table des cartes

	def initializeMapsTable(self):
	
		def getMapNote(feature):
			geometry = feature.geometry()
			if geometry.isNull(): return 'Cette carte n\'a pas de géométrie définie ?'
			if geometry.length() != geometry.boundingBox().width() * 2 + geometry.boundingBox().height() * 2: return 'Cette carte n\'a pas une géométrie rectangulaire ?'
			if (geometry.boundingBox().width() * 1000 / feature[QGP.tableFramesFieldEchelle] > QGP.mapsExportMaxSize[0]) or \
				(geometry.boundingBox().height() * 1000 / feature[QGP.tableFramesFieldEchelle] > QGP.mapsExportMaxSize[1]) :
					return 'Cette carte comporte plusieurs pavés !'
			return ''
		
		self.listMapsViewFeatures = self.listMapsFeatures.copy()
		self.listMapsViewFeatures = sorted(self.listMapsViewFeatures, key = lambda f: str(f[QGP.tableFramesFieldItineraryCode]) + \
																						('-A-' if 'Global' in str(f[QGP.tableFramesFieldName]) else '-Z-') + \
																						'{:03d}'.format(int('0' + ''.join([c for c in str(f[QGP.tableFramesFieldName]) if c.isdigit()]))))
	
		self.groupBoxMapsTable.setSortingEnabled(False)									# Table cannot be sorted because row selected is important 
		self.groupBoxMapsTable.clearContents()
		self.groupBoxMapsTable.setRowCount(len(self.listMapsViewFeatures))

		tableFields = QGP.mapsTableQView
		for row in range(self.groupBoxMapsTable.rowCount()): 
			feature = self.listMapsViewFeatures[row]
			mapName = feature[QGP.tableFramesFieldName]
			mapNote = getMapNote(feature)
			for col in range(len(tableFields)):
				columnName = tableFields[col][QGP.C_framesTableQView_ColName]
				value = feature[columnName] if columnName != QGP.tableFramesQFieldNote else mapNote
				item = self.createItem(value, columnName == QGP.tableFramesFieldName)
				if mapName == self.highlightedMap: item.setBackground(DCOL.bgTableOk)
				if mapNote[-1:] == '?': 
					item.setBackground(DCOL.bgTableError)
				elif mapNote[-1:] != '': 
					item.setBackground(DCOL.bgTableWarning)
				self.groupBoxMapsTable.setItem(row, col, item)

#	Clic droit - zoomer sur la carte 

	def mapsTable_itemRightClicked(self, point):
		if point == None: return
		item = self.groupBoxMapsTable.itemAt(point)
		mapFeature = self.listMapsViewFeatures[item.row()]

		self.iface.mapCanvas().setExtent(mapFeature.geometry().boundingBox())
		self.iface.mapCanvas().zoomScale(self.configZoomMapScale)
		
		self.mainFrame.setStatusInfo('Le Canevas a été centré sur la carte !')


#	Affichage des informations quand une case est cliquée

	def showMapsTableElementInfo(self, item, label):

		if label == QGP.tableFramesFieldFolder:
			self.initializeMapsExportedTable(item)
			self.groupBoxMapsTable.hide()
			self.groupBoxMapsExportedTable.show()
			self.mainFrame.requestPageInfo('Cartes')
			self.mainFrame.setStatusInfo(self.selectedMapFeature[QGP.tableFramesFieldName] + ' : Liste des cartes que vous avez exporté')
			return


# ========================================================================================
# Opérations sur la Table des Cartes Exportées
# ========================================================================================	
	
	def initializeMapsExportedTable(self, item):

		mapsExportedPath = QGP.configPathExportImages.replace('%PROJECT%', self.itinerarySelected)
		if not os.path.isdir(mapsExportedPath) : return
		mapsExportedName = self.groupBoxMapsTable.item(item.row(), [x[QGP.C_framesTableQView_ColName] for x in QGP.mapsTableQView].index(QGP.tableFramesFieldName)).text()

		rowValuesList = []
		for fileName in sorted(os.listdir(mapsExportedPath), reverse=True):
			try:
				mapPrefix, mapItinerary, mapName, mapMode = fileName.split(' - ')[0:4]
				if mapName == mapsExportedName: rowValuesList.append([mapPrefix, mapItinerary, mapName, mapMode, fileName])
			except:
				pass

		self.groupBoxMapsExportedTable.setRowCount(len(rowValuesList))
		for row in range(len(rowValuesList)):
			for col in range(len(QGP.mapsExportedTableQView)):
				value = rowValuesList[row][col]
				item = self.createItem(value, False)
				self.groupBoxMapsExportedTable.setItem(row, col, item)	
				
	def mapsExportedTable_itemClicked(self, item):
		label = QGP.mapsExportedTableQView[item.column()][0]
		self.showMapsExportedTableElementInfo(item, label)

	def showMapsExportedTableElementInfo(self, item, label):
		if label == QGP.tableMapsExportedFieldFile :
			fileName = item.text()
			print('Help = ' + fileName)
			THEL.viewMapOnBrowser(self.mainFrame, fileName, QGP.configPathExportImages.replace('%PROJECT%', self.itinerarySelected) + fileName)


# ========================================================================================
# ========================================================================================
#
# Création des différents cadres Menu
# 
# ========================================================================================
# ========================================================================================


# ========================================================================================
# Cadre : Itinéraires
# ========================================================================================

	def menuBoxItinerary(self):
	
		groupBoxItinerary = QtWidgets.QGroupBox('Choix Itinéraire', self.mainMenu)
		groupBoxItinerary.setStyleSheet(DSTY.styleBox)
		
#	Créer un bouton Radio pour chaque type d'itinéraire

		TBUT.createLabelBlackButton(groupBoxItinerary, 1, 1, 'Type Itinéraire', 'Normal', 'Normal')

		buttonRadioGR  = TBUT.createRadioBoxButton(groupBoxItinerary, 2.6, 1, 'GR'  , 'Compact3_2')
		buttonRadioGRP = TBUT.createRadioBoxButton(groupBoxItinerary, 3.3, 1, 'GRP' , 'Compact3_2')
		buttonRadioGRT = TBUT.createRadioBoxButton(groupBoxItinerary, 4.1, 1, 'GRT' , 'Compact3_2')
		buttonRadioRI  = TBUT.createRadioBoxButton(groupBoxItinerary, 4.8, 1, 'RI'  , 'Compact3_2')
		buttonRadioRL  = TBUT.createRadioBoxButton(groupBoxItinerary, 5.6, 1, 'RL'  , 'Compact3_2')
		buttonRadioRB  = TBUT.createRadioBoxButton(groupBoxItinerary, 6.4, 1, 'RB'  , 'Compact3_2')
		buttonRadioRF  = TBUT.createRadioBoxButton(groupBoxItinerary, 7.2, 1, 'RF'  , 'Compact3_2')
		buttonRadioIR  = TBUT.createRadioBoxButton(groupBoxItinerary, 8.0, 1, 'IR'  , 'Compact3_2')
		buttonRadioZZ  = TBUT.createRadioBoxButton(groupBoxItinerary, 8.8, 1, 'ZZ'  , 'Compact3_2')

		buttonRadioGR.clicked.connect(self.buttonRadioGR_clicked)
		buttonRadioGRP.clicked.connect(self.buttonRadioGRP_clicked)
		buttonRadioGRT.clicked.connect(self.buttonRadioGRT_clicked)
		buttonRadioRI.clicked.connect(self.buttonRadioRI_clicked)
		buttonRadioRL.clicked.connect(self.buttonRadioRL_clicked)
		buttonRadioRB.clicked.connect(self.buttonRadioRB_clicked)
		buttonRadioRF.clicked.connect(self.buttonRadioRF_clicked)
		buttonRadioIR.clicked.connect(self.buttonRadioIR_clicked)
		buttonRadioZZ.clicked.connect(self.buttonRadioZZ_clicked)
		
#	Créer un menu déroulant pour le choix de l'itinéraire et la sélection

		TBUT.createLabelBlackButton(groupBoxItinerary, 1, 2, 'Choix Itinéraire', 'Normal', 'Normal')
		self.itineraryCombo = TBUT.createComboButton(groupBoxItinerary, 2, 2, 'Normal')

#	Itinéraire sélectionné

		self.viewMapItineraryInfo = TBUT.createLabelGreenButton(groupBoxItinerary, 6, 2, '. . .', 'Normal', 'Normal')
		DSTY.setStyleWarningLabel(self.viewMapItineraryInfo, "Normal")

#	Créer le bouton d'action		

		buttonShow = TBUT.createActionButton(groupBoxItinerary, 3, 2, 'Afficher !', 'Normal')
		buttonShow.clicked.connect(self.createMapsView)		
			
# 	Terminé

		groupBoxItinerary.repaint()

		return groupBoxItinerary


# ========================================================================================
# Cadre : Création Projet
# ========================================================================================

	def menuBoxCreateProject(self):
	
		groupBoxCreateProject = QtWidgets.QGroupBox('Création Projet', self.mainMenu)
		groupBoxCreateProject.setStyleSheet(DSTY.styleBox)

#	Label et nom du projet

		TBUT.createLabelBlackButton(groupBoxCreateProject, 1, 1, 'Répertoire', 'Normal', 'Normal')
		self.createProjectPath = TBUT.createLabelGreenButton(groupBoxCreateProject, 2, 1, '. . .', 'Normal', 'Normal')
		DSTY.setStyleWarningLabel(self.createProjectPath, "Normal")

#	Créer le bouton d'action		

		self.buttonCreateProject = TBUT.createActionButton(groupBoxCreateProject, 2, 2, 'Créer !', 'Normal')
		self.buttonCreateProject.clicked.connect(self.createProject)	
		DSTY.setStyleMainButtonsInactive(self.buttonCreateProject)

# 	Terminé

		groupBoxCreateProject.repaint()

		return groupBoxCreateProject


# ========================================================================================
# Cadre : Voir Carte
# ========================================================================================

	def menuBoxViewMap(self):
	
		groupBoxViewMap = QtWidgets.QGroupBox('Voir Carte', self.mainMenu)
		groupBoxViewMap.setStyleSheet(DSTY.styleBox)

#	Nom de la carte

		self.viewMapNameInfo = TBUT.createLabelGreenButton(groupBoxViewMap, 1, 1, '. . .', 'Normal', 'Normal')
		DSTY.setStyleWarningLabel(self.viewMapNameInfo, "Normal")

#	Créer le bouton d'action		

		self.buttonViewMap = TBUT.createActionButton(groupBoxViewMap, 1, 2, 'Page Carte', 'Normal')
		self.buttonViewMap.clicked.connect(self.viewActiveMap)	
		DSTY.setStyleMainButtonsInactive(self.buttonViewMap)

# 	Terminé

		groupBoxViewMap.repaint()

		return groupBoxViewMap


# ========================================================================================
# Cadre : Renommer Carte
# ========================================================================================

	def menuBoxRenameMap(self):
	
		groupBoxRenameMap = QtWidgets.QGroupBox('Renommer Carte', self.mainMenu)
		groupBoxRenameMap.setStyleSheet(DSTY.styleBox)

#	Nouveau Nom de la carte

		self.viewMapNewnameInfo = TBUT.createLabelGreenButton(groupBoxRenameMap, 1, 1, '. . .', 'Normal', 'Normal')
		DSTY.setStyleWarningLabel(self.viewMapNewnameInfo, "Normal")

#	Bouton Créer

		self.buttonRenameMap = TBUT.createActionButton(groupBoxRenameMap, 1, 2, 'Renommer', 'Normal')
		DSTY.setStyleMainButtonsInactive(self.buttonRenameMap)
		self.buttonRenameMap.clicked.connect(self.renameMap)	

# 	Terminé

		groupBoxRenameMap.repaint()

		return groupBoxRenameMap

# ========================================================================================
# Cadre : Créer Carte
# ========================================================================================

	def menuBoxCreateMap(self):
	
		groupBoxCreateMap = QtWidgets.QGroupBox('Nouvelle Carte', self.mainMenu)
		groupBoxCreateMap.setStyleSheet(DSTY.styleBox)

#	Label Combo Itinéraire et Nom Carte

		TBUT.createLabelBlackButton(groupBoxCreateMap, 1, 1, 'Itinéraire / Nom', 'Normal', 'Normal')
		self.createMapItineraryCombo = TBUT.createComboButton(groupBoxCreateMap, 2, 1, 'Normal')
		self.createMapName = TBUT.createInputButton(groupBoxCreateMap, 3, 1, 'Normal')
		self.createMapName.setPlaceholderText('Nom de la Carte')

#	Label Combo Format et Combo Echelle

		TBUT.createLabelBlackButton(groupBoxCreateMap, 1, 2, 'Format / Echelle', 'Normal', 'Normal')

		self.createMapFormatCombo = TBUT.createComboButton(groupBoxCreateMap, 2, 2, 'Normal')
		for format in QGP.dicoPaperFormats:
			self.createMapFormatCombo.addItem(format)

		self.createMapScaleCombo = TBUT.createComboButton(groupBoxCreateMap, 3, 2, 'Normal')
		for scale in QGP.configMapScales:
			self.createMapScaleCombo.addItem(str(scale))

#	Bouton Créer

		self.buttonCreateMap = TBUT.createActionButton(groupBoxCreateMap, 4, 2, 'Créer Carte', 'Normal')
		self.buttonCreateMap.clicked.connect(self.createNewMap)	

# 	Terminé

		groupBoxCreateMap.repaint()

		return groupBoxCreateMap


# ========================================================================================
# Cadre : Cadrer Carte
# ========================================================================================

	def menuBoxFrameMap(self):
	
		groupBoxFrameeMap = QtWidgets.QGroupBox('Cadrer / Supprimer Carte', self.mainMenu)
		groupBoxFrameeMap.setStyleSheet(DSTY.styleBox)

#	Combo Format et Combo Echelle

		self.reframeMapFormatCombo = TBUT.createComboButton(groupBoxFrameeMap, 1, 1, 'Normal')
		for format in QGP.dicoPaperFormats:
			self.reframeMapFormatCombo.addItem(format)

		self.reframeMapScaleCombo = TBUT.createComboButton(groupBoxFrameeMap, 2, 1, 'Normal')
		for scale in QGP.configMapScales:
			self.reframeMapScaleCombo.addItem(str(scale))

#	Bouton Recadrer / Rectangulariser

		self.buttonReframeMap = TBUT.createActionButton(groupBoxFrameeMap, 2, 2, 'Recadrer Carte', 'Normal')
		self.buttonReframeMap.clicked.connect(self.reframeMap)	

		self.buttonReframeMap.setContextMenuPolicy(Qt.CustomContextMenu)
		self.buttonReframeMap.customContextMenuRequested.connect(self.reframeMapRectangle)

#	Bouton Supprimer

		self.buttonDeleteMap = TBUT.createActionButton(groupBoxFrameeMap, 1, 2, 'Supprimer Carte', 'Normal')
		self.buttonDeleteMap.clicked.connect(self.deleteMap)	
		DSTY.setStyleMainButtonsInactive(self.buttonDeleteMap)

		self.buttonDeleteMap.setContextMenuPolicy(Qt.CustomContextMenu)
		self.buttonDeleteMap.customContextMenuRequested.connect(self.activateDeleteMap)

# 	Terminé

		groupBoxFrameeMap.repaint()

		return groupBoxFrameeMap


# ========================================================================================
# Cadre : Cadre de la Table des Cartes
# ========================================================================================

	def menuBoxTableMapsFrame(self):
	
		groupBoxMapsFrame = QtWidgets.QGroupBox('Table des Cartes', self.mainMenu)
		groupBoxMapsFrame.setStyleSheet(DSTY.styleBox)

		groupBoxMapsFrame.repaint()

		return groupBoxMapsFrame


# ========================================================================================
# Cadre : Table des Cartes
# ========================================================================================

	def menuBoxTableMapsView(self):

		groupBoxMapsView = QtWidgets.QTableWidget(0,len(QGP.mapsTableQView), self.mainMenu)
		groupBoxMapsView.setStyleSheet(DSTY.styleBox)

		DSTY.setStyleTableTraces(groupBoxMapsView)

		tableFields = QGP.mapsTableQView
		for col in range(len(tableFields)):
			groupBoxMapsView.setHorizontalHeaderItem(col, QtWidgets.QTableWidgetItem(tableFields[col][0]))
			groupBoxMapsView.setColumnWidth(col, tableFields[col][1])

		groupBoxMapsView.itemSelectionChanged.connect(self.mapsTable_SelectionChanged)
		groupBoxMapsView.itemClicked.connect(self.mapsTable_itemClicked)

		groupBoxMapsView.setContextMenuPolicy(Qt.CustomContextMenu)
		groupBoxMapsView.customContextMenuRequested.connect(self.mapsTable_itemRightClicked)

		groupBoxMapsView.repaint()

		return groupBoxMapsView
	

# ========================================================================================
# Cadre : Table des Cartes Exportées
# ========================================================================================
	
	def menuBoxTableMapsExportedView(self):

		groupBoxMapsExportedView = QtWidgets.QTableWidget(0,len(QGP.mapsExportedTableQView), self.mainMenu)
		groupBoxMapsExportedView.setStyleSheet(DSTY.styleBox)

		DSTY.setStyleTableTraces(groupBoxMapsExportedView)

		tableFields = QGP.mapsExportedTableQView
		for col in range(len(tableFields)):
			groupBoxMapsExportedView.setHorizontalHeaderItem(col, QtWidgets.QTableWidgetItem(tableFields[col][0]))
			groupBoxMapsExportedView.setColumnWidth(col, tableFields[col][1])

		groupBoxMapsExportedView.itemClicked.connect(self.mapsExportedTable_itemClicked)

		groupBoxMapsExportedView.repaint()

		return groupBoxMapsExportedView	
	
	
# ========================================================================================
# --- THE END ---
# ========================================================================================
	