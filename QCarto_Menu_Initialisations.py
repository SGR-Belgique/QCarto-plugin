# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Gestion des Menus : Page Initialisations
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

import QCarto_Layers_Tracks as LTRK

import QCarto_Tools_Buttons as TBUT
import QCarto_Tools_Coding as TCOD
import QCarto_Tools_Dates as TDAT
import QCarto_Tools_Layers as TLAY
import QCarto_Tools_Progress as TPRO

import QCarto_Definitions_Colors as DCOL
import QCarto_Definitions_Styles as DSTY

import QCarto_Parameters_Global
QGP = QCarto_Parameters_Global.globalParameters()


# ========================================================================================
# Class : menuInitFrame
# >>> iface
# >>> mainMenu 						: Widget of Main Menu
# >>> mainFrame 					: Main Menu Object
# ========================================================================================

class menuInitFrame:

	def __init__(self, iface, mainMenu, mainFrame):

# 	Paramètres fournis

		self.iface = iface
		self.mainMenu = mainMenu
		self.mainFrame = mainFrame

#	Nom de la page

		self.pageName = 'Initialisations'

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

# 	Création des sous-menus

		self.boxesList = []
		self.createMenuBoxes()

		self.mainFrame.setStatusDone('Page des ' + self.pageName + ' créée !')
		
	def createMenuBoxes(self):

		self.groupBoxInitDescriptionGroup = self.menuBoxDescriptionGroup()
		DSTY.setBoxGeometry(self.groupBoxInitDescriptionGroup, 1, 4, 4, 4)
		self.boxesList.append(self.groupBoxInitDescriptionGroup)

		self.groupBoxInitDBCartoGroup = self.menuBoxDBCartoGroup()
		DSTY.setBoxGeometry(self.groupBoxInitDBCartoGroup, 1, 9, 4, 7)
		self.boxesList.append(self.groupBoxInitDBCartoGroup)

		self.groupBoxInitMmtGroup = self.menuBoxMntGroup()
		DSTY.setBoxGeometry(self.groupBoxInitMmtGroup, 1, 17, 4, 2)
		self.boxesList.append(self.groupBoxInitMmtGroup)

		self.groupBoxInitBorderGroup = self.menuBoxBorderGroup()
		DSTY.setBoxGeometry(self.groupBoxInitBorderGroup, 1, 20, 4, 2)
		self.boxesList.append(self.groupBoxInitBorderGroup)

		self.groupBoxInitGridGroup = self.menuBoxGridGroup()
		DSTY.setBoxGeometry(self.groupBoxInitGridGroup, 1, 23, 4, 2)
		self.boxesList.append(self.groupBoxInitGridGroup)

		self.groupBoxInitIgn50Group = self.menuBoxIgn50Group()
		DSTY.setBoxGeometry(self.groupBoxInitIgn50Group, 5, 4, 4, 2)
		self.boxesList.append(self.groupBoxInitIgn50Group)

		self.groupBoxInitIgn250Group = self.menuBoxIgn250Group()
		DSTY.setBoxGeometry(self.groupBoxInitIgn250Group, 5, 7, 4, 1)
		self.boxesList.append(self.groupBoxInitIgn250Group)

		self.groupBoxInitIgn400Group = self.menuBoxIgn400Group()
		DSTY.setBoxGeometry(self.groupBoxInitIgn400Group, 5, 9, 4, 1)
		self.boxesList.append(self.groupBoxInitIgn400Group)

		self.groupBoxInitCdnGroup = self.menuBoxCdnGroup()
		DSTY.setBoxGeometry(self.groupBoxInitCdnGroup, 5, 11, 4, 1)
		self.boxesList.append(self.groupBoxInitCdnGroup)

		self.groupBoxInitPrivateMapGroup = self.menuBoxPublicMapGroup()
		DSTY.setBoxGeometry(self.groupBoxInitPrivateMapGroup, 5, 13, 4, 1)
		self.boxesList.append(self.groupBoxInitPrivateMapGroup)

		self.groupBoxInitDBPOIsGroup = self.menuBoxDBPOIsGroup()
		DSTY.setBoxGeometry(self.groupBoxInitDBPOIsGroup, 5, 15, 4, 4)
		self.boxesList.append(self.groupBoxInitDBPOIsGroup)

		self.groupBoxInitDBBaliseursGroup = self.menuBoxDBBaliseursGroup()
		DSTY.setBoxGeometry(self.groupBoxInitDBBaliseursGroup, 5, 20, 4, 5)
		self.boxesList.append(self.groupBoxInitDBBaliseursGroup)


# ========================================================================================
# Actions : A la demande de la fenêtre principale
# ========================================================================================

#	Show - Ouverture de cette fenêtre

	def show(self):
		for box in self.boxesList: box.show(), box.repaint()
		self.initializeInfos()

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
# Initialisation des Informations
# 
# ========================================================================================
# ========================================================================================

	def initializeInfos(self):
		self.initializeGroupDescriptions()
		self.initializeGroupDBCarto()
		self.initializeGroupDBPOIs()
		self.initializeGroupDBBaliseurs()
		self.initializeGroupMnt()
		self.initializeGroupBorder()
		self.initializeGroupGrid()
		self.initializeGroupCdn()
		self.initializeGroupIgn50()
		self.initializeGroupIgn250()
		self.initializeGroupIgn400()
		self.initializeGroupPublicMap()

	def initializeGroupDescriptions(self):
		
		if TLAY.findGroup(QGP.configFrameGroupName)[0] != None:
			DSTY.setStyleOkLabelSmall(self.buttonGroupDescriptionInfo)
		else:
			DSTY.setStyleErrorLabelSmall(self.buttonGroupDescriptionInfo)

		if TLAY.findLayerInGroup(QGP.configFrameGroupName, QGP.configShapeMapDecorationCopyright)[0] != None:
			DSTY.setStyleOkLabelSmall(self.buttonLayerCopyrightInfo)
		else:
			DSTY.setStyleErrorLabelSmall(self.buttonLayerCopyrightInfo)

		if TLAY.findLayerInGroup(QGP.configFrameGroupName, QGP.configShapeMapDecorationNumber)[0] != None:
			DSTY.setStyleOkLabelSmall(self.buttonLayerNumeroInfo)
		else:
			DSTY.setStyleErrorLabelSmall(self.buttonLayerNumeroInfo)

		if TLAY.findLayerInGroup(QGP.configFrameGroupName, QGP.configShapeMapDecorationWhiteFrame)[0] != None:
			DSTY.setStyleOkLabelSmall(self.buttonLayerWhiteFrameInfo)
		else:
			DSTY.setStyleErrorLabelSmall(self.buttonLayerWhiteFrameInfo)

	def initializeGroupDBCarto(self):

		if TLAY.findGroup(QGP.configDBCartoGroupName)[0] != None:
			DSTY.setStyleOkLabelSmall(self.buttonGroupDBCartoInfo)
		else:
			DSTY.setStyleErrorLabelSmall(self.buttonGroupDBCartoInfo)

		for index, tableName in zip(range(len(QGP.tableNameDico)), QGP.tableNameDico) :
			if TLAY.findLayerInGroup(QGP.configDBCartoGroupName, tableName)[0] != None:
				DSTY.setStyleOkLabelSmall(self.buttonTableDBInfoList[index])
			else:
				DSTY.setStyleErrorLabelSmall(self.buttonTableDBInfoList[index])


	def initializeGroupDBPOIs(self):

		if TLAY.findGroup(QGP.configDBPOIsGroupName)[0] != None:
			DSTY.setStyleOkLabelSmall(self.buttonGroupDBPOIsInfo)
		else:
			DSTY.setStyleErrorLabelSmall(self.buttonGroupDBPOIsInfo)

		for tableName in QGP.tablePOIsNameDico:
			if TLAY.findLayerInGroup(QGP.configDBPOIsGroupName, tableName)[0] != None:
				DSTY.setStyleOkLabelSmall(self.buttonTableDBPOIsInfoList[QGP.tablePOIsNameDico[tableName][0]])
			else:
				DSTY.setStyleErrorLabelSmall(self.buttonTableDBPOIsInfoList[QGP.tablePOIsNameDico[tableName][0]])


	def initializeGroupDBBaliseurs(self):
	
		if TLAY.findGroup(QGP.configDBBaliseursGroupName)[0] != None:
			DSTY.setStyleOkLabelSmall(self.buttonGroupDBBaliseursInfo)
		else:
			DSTY.setStyleErrorLabelSmall(self.buttonGroupDBBaliseursInfo)

		for tableName in QGP.tableBaliseursNameDico:
			if TLAY.findLayerInGroup(QGP.configDBBaliseursGroupName, tableName)[0] != None:
				DSTY.setStyleOkLabelSmall(self.buttonTableDBBaliseursInfoList[QGP.tableBaliseursNameDico[tableName][0]])
			else:
				DSTY.setStyleErrorLabelSmall(self.buttonTableDBBaliseursInfoList[QGP.tableBaliseursNameDico[tableName][0]])
	

	def initializeGroupMnt(self):

		if TLAY.findGroup(QGP.configMntGroupName)[0] != None:
			DSTY.setStyleOkLabelSmall(self.buttonGroupMntInfo)
		else:
			DSTY.setStyleErrorLabelSmall(self.buttonGroupMntInfo)

		countTotal  = len(QGP.configMntShapesList)
		countRaster = sum (1 for rasterName in QGP.configMntShapesList if TLAY.findLayerInGroup(QGP.configMntGroupName, rasterName)[0] != None)
		self.buttonRasterMntInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%',str(countRaster) + ' / ' + str(countTotal) + ' rasters'))
		if countRaster == countTotal:
			DSTY.setStyleOkLabelSmall(self.buttonRasterMntInfo)		
		elif countRaster > 0:
			DSTY.setStyleWarningLabelSmall(self.buttonRasterMntInfo)		
		else:
			DSTY.setStyleErrorLabelSmall(self.buttonRasterMntInfo)		

	def initializeGroupBorder(self):

		if TLAY.findGroup(QGP.configBorderGroupName)[0] != None:
			DSTY.setStyleOkLabelSmall(self.buttonGroupBorderInfo)
		else:
			DSTY.setStyleErrorLabelSmall(self.buttonGroupBorderInfo)

		countTotal  = len(QGP.configBorderShapesList)
		countShape = sum (1 for shapeName in QGP.configBorderShapesList if TLAY.findLayerInGroup(QGP.configBorderGroupName, shapeName)[0] != None)
		self.buttonShapeBorderInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%',str(countShape) + ' / ' + str(countTotal) + ' rasters'))
		if countShape == countTotal:
			DSTY.setStyleOkLabelSmall(self.buttonShapeBorderInfo)		
		elif countShape > 0:
			DSTY.setStyleWarningLabelSmall(self.buttonShapeBorderInfo)		
		else:
			DSTY.setStyleErrorLabelSmall(self.buttonShapeBorderInfo)		

	def initializeGroupGrid(self):

		if TLAY.findGroup(QGP.configGridGroupName)[0] != None:
			DSTY.setStyleOkLabelSmall(self.buttonGroupGridInfo)
		else:
			DSTY.setStyleErrorLabelSmall(self.buttonGroupGridInfo)

		countTotal  = len(QGP.configGridShapesList)
		countShape = sum (1 for shapeName in QGP.configGridShapesList if TLAY.findLayerInGroup(QGP.configGridGroupName, shapeName)[0] != None)
		self.buttonShapeGridInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%',str(countShape) + ' / ' + str(countTotal) + ' shapes'))
		if countShape == countTotal:
			DSTY.setStyleOkLabelSmall(self.buttonShapeGridInfo)		
		elif countShape > 0:
			DSTY.setStyleWarningLabelSmall(self.buttonShapeGridInfo)		
		else:
			DSTY.setStyleErrorLabelSmall(self.buttonShapeGridInfo)		

	def initializeGroupCdn(self):

		if TLAY.findGroup(QGP.configCdnGroupName)[0] != None:
			DSTY.setStyleOkLabelSmall(self.buttonGroupCdnInfo)
		else:
			DSTY.setStyleErrorLabelSmall(self.buttonGroupCdnInfo)

		countTotal  = len(QGP.configCdnShapesList)
		countShape = sum (1 for shapeName in QGP.configCdnShapesList if TLAY.findLayerInGroup(QGP.configCdnGroupName, shapeName)[0] != None)
		self.buttonShaperCdnInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%',str(countShape) + ' / ' + str(countTotal) + ' rasters'))
		if countShape == countTotal:
			DSTY.setStyleOkLabelSmall(self.buttonShaperCdnInfo)		
		elif countShape > 0:
			DSTY.setStyleWarningLabelSmall(self.buttonShaperCdnInfo)		
		else:
			DSTY.setStyleErrorLabelSmall(self.buttonShaperCdnInfo)		

	def initializeGroupIgn50(self):
		if TLAY.findGroup(QGP.configIGN50Ed3GroupName)[0] != None:
			DSTY.setStyleOkLabelSmall(self.buttonGroupIgn50V3Info)
		else:
			DSTY.setStyleErrorLabelSmall(self.buttonGroupIgn50V3Info)

		countTotal  = len(QGP.configIgn50ShapesList)
		countRaster = sum (1 for rasterName in QGP.configIgn50ShapesList if TLAY.findLayerInGroup(QGP.configIGN50Ed3GroupName, 'Ed3-' + rasterName)[0] != None)
		self.buttonMapIgn50V3Info.setText(DSTY.textFormatBlackNormal.replace('%TEXT%',str(countRaster) + ' / ' + str(countTotal) + ' rasters'))
		if countRaster == countTotal:
			DSTY.setStyleOkLabelSmall(self.buttonMapIgn50V3Info)		
		elif countRaster > 0:
			DSTY.setStyleWarningLabelSmall(self.buttonMapIgn50V3Info)		
		else:
			DSTY.setStyleErrorLabelSmall(self.buttonMapIgn50V3Info)		

		if TLAY.findGroup(QGP.configIGN50Ed4GroupName)[0] != None:
			DSTY.setStyleOkLabelSmall(self.buttonGroupIgn50V4Info)
		else:
			DSTY.setStyleErrorLabelSmall(self.buttonGroupIgn50V4Info)

		countTotal  = len(QGP.configIgn50ShapesList)
		countRaster = sum (1 for rasterName in QGP.configIgn50ShapesList if TLAY.findLayerInGroup(QGP.configIGN50Ed4GroupName, 'Ed4-' + rasterName)[0] != None)
		self.buttonMapIgn50V4Info.setText(DSTY.textFormatBlackNormal.replace('%TEXT%',str(countRaster) + ' / ' + str(countTotal) + ' rasters'))
		if countRaster == countTotal:
			DSTY.setStyleOkLabelSmall(self.buttonMapIgn50V4Info)		
		elif countRaster > 0:
			DSTY.setStyleWarningLabelSmall(self.buttonMapIgn50V4Info)		
		else:
			DSTY.setStyleErrorLabelSmall(self.buttonMapIgn50V4Info)		

	def initializeGroupIgn250(self):
		if TLAY.findGroup(QGP.configIGN250GroupName)[0] != None:
			DSTY.setStyleOkLabelSmall(self.buttonGroupIgn250Info)
		else:
			DSTY.setStyleErrorLabelSmall(self.buttonGroupIgn250Info)

		countTotal  = len(QGP.configIgn250ShapesList)
		countRaster = sum (1 for rasterName in QGP.configIgn250ShapesList if TLAY.findLayerInGroup(QGP.configIGN250GroupName, rasterName)[0] != None)
		self.buttonMapIgn250Info.setText(DSTY.textFormatBlackNormal.replace('%TEXT%',str(countRaster) + ' / ' + str(countTotal) + ' rasters'))
		if countRaster == countTotal:
			DSTY.setStyleOkLabelSmall(self.buttonMapIgn250Info)		
		elif countRaster > 0:
			DSTY.setStyleWarningLabelSmall(self.buttonMapIgn250Info)		
		else:
			DSTY.setStyleErrorLabelSmall(self.buttonMapIgn250Info)		

	def initializeGroupIgn400(self):
		if TLAY.findGroup(QGP.configIGN400GroupName)[0] != None:
			DSTY.setStyleOkLabelSmall(self.buttonGroupIgn400Info)
		else:
			DSTY.setStyleErrorLabelSmall(self.buttonGroupIgn400Info)

		countTotal  = len(QGP.configIgn400ShapesList)
		countRaster = sum (1 for rasterName in QGP.configIgn400ShapesList if TLAY.findLayerInGroup(QGP.configIGN400GroupName, rasterName)[0] != None)
		self.buttonMapIgn400Info.setText(DSTY.textFormatBlackNormal.replace('%TEXT%',str(countRaster) + ' / ' + str(countTotal) + ' rasters'))
		if countRaster == countTotal:
			DSTY.setStyleOkLabelSmall(self.buttonMapIgn400Info)		
		elif countRaster > 0:
			DSTY.setStyleWarningLabelSmall(self.buttonMapIgn400Info)		
		else:
			DSTY.setStyleErrorLabelSmall(self.buttonMapIgn400Info)		

	def initializeGroupPublicMap(self):
		if TLAY.findGroup(QGP.configPublicMapGroupName)[0] != None:
			DSTY.setStyleOkLabelSmall(self.buttonGroupPublicMapInfo)
		else:
			DSTY.setStyleErrorLabelSmall(self.buttonGroupPublicMapInfo)

		countTotal  = len(QGP.tablePublicNameDico)
		countShape = sum (1 for shapeName in QGP.tablePublicNameDico if TLAY.findLayerInGroup(QGP.configPublicMapGroupName, shapeName)[0] != None)
		self.buttonPublicMapInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%',str(countShape) + ' / ' + str(countTotal) + ' tables'))
		if countShape == countTotal:
			DSTY.setStyleOkLabelSmall(self.buttonPublicMapInfo)		
		elif countShape > 0:
			DSTY.setStyleWarningLabelSmall(self.buttonPublicMapInfo)		
		else:
			DSTY.setStyleErrorLabelSmall(self.buttonPublicMapInfo)		


# ========================================================================================
# ========================================================================================
#
# Création des Groupes
# 
# ========================================================================================
# ========================================================================================

	def createGroupIfNeeded(self, groupName, canevasIndex = 999):
		if TLAY.findGroup(groupName)[0] == None:
			TLAY.createGroup(groupName, canevasIndex)
		TLAY.findGroup(groupName)[0].setExpanded(True)


	def createGroupDescriptions(self):
		self.mainFrame.setStatusWorking('Initialisation du groupe : ' + QGP.configFrameGroupName)
		self.createGroupIfNeeded(QGP.configFrameGroupName, 0)

		if TLAY.findLayerInGroup(QGP.configFrameGroupName, QGP.configShapeMapDecorationCopyright)[0] == None:
			TLAY.loadLayer(QGP.configPathFrame, QGP.configShapeMapDecorationCopyright, QGP.configFrameGroupName, QGP.configShapeMapDecorationCopyright, None, None, False)

		if TLAY.findLayerInGroup(QGP.configFrameGroupName, QGP.configShapeMapDecorationNumber)[0] == None:
			TLAY.loadLayer(QGP.configPathFrame, QGP.configShapeMapDecorationNumber, QGP.configFrameGroupName, QGP.configShapeMapDecorationNumber, None, None, False)
		
		if TLAY.findLayerInGroup(QGP.configFrameGroupName, QGP.configShapeMapDecorationWhiteFrame)[0] == None:
			TLAY.loadLayer(QGP.configPathFrame, QGP.configShapeMapDecorationWhiteFrame, QGP.configFrameGroupName, QGP.configShapeMapDecorationWhiteFrame, None, None, False)

		self.createGroupIfNeeded(QGP.configActiveMapGroupName, 1)
		self.createGroupIfNeeded(QGP.configActiveProjectGroupName, 2)
		self.createGroupIfNeeded(QGP.configOtherProjectGroupName, 3)

		self.initializeGroupDescriptions()
		self.mainFrame.setStatusDone('Initialisation du groupe : ' + QGP.configFrameGroupName + ' - OK')

	def addDBLayer(self, uri, groupName, tableName):
		layer = QgsVectorLayer(uri, tableName, "postgres")													# Ajouter la couche			
		if layer == None:
			self.mainFrame.setStatusError(tableName + ' : impossible de charger la couche ?')
			TDAT.sleep(2000)
			return False

		crs = layer.crs()																					# Define CRS - seems irrelvant
		crs.createFromId(3812)  			
		layer.setCrs(crs)					
					
		QgsProject.instance().addMapLayer(layer, False)														# Add layer to group
		TLAY.findGroup(groupName)[0].addLayer(layer)

		root = QgsProject.instance().layerTreeRoot()														# Replier les détails de la couche
		node = root.findLayer(layer)
		node.setExpanded(False)
		node.setItemVisibilityChecked(True)

		self.mainFrame.setStatusWorking(tableName + ' : ajoutée au Canevas !')
		TDAT.sleep(1000)


	def createGroupDB_Carto(self):
		self.mainFrame.setStatusWorking('Initialisation du groupe : ' + QGP.configDBCartoGroupName)
		self.createGroupIfNeeded(QGP.configDBCartoGroupName, 4)
		progressBar = TPRO.createProgressBar(self.buttonInstallDBCarto, len(QGP.tableNameDico), 'Normal')
	
		for tableName in QGP.tableNameDico:
			if TLAY.findLayerInGroup(QGP.configDBCartoGroupName, tableName)[0] == None:
				
#				Create URI				
				
				uri = QGP.configReseauGRInstallUriGeom if QGP.tableNameDico[tableName][2] != None else QGP.configReseauGRInstallUriNoGeom
				uri = uri.replace('%KEY%',  QGP.tableNameDico[tableName][1])
				uri = uri.replace('%GEOM%', str(QGP.tableNameDico[tableName][2]))
				uri = uri.replace('%LAYER%', tableName)

#				Ajouter la couche	

				self.addDBLayer(uri, QGP.configDBCartoGroupName, tableName)

				self.mainFrame.setStatusWorking(tableName + ' : ajoutée au Canevas !')
				TDAT.sleep(1000)

				self.initializeGroupDBCarto()

			progressBar.setValue(progressBar.value() + 1)
			QgsApplication.processEvents()

		del progressBar
	
		self.initializeGroupDBCarto()
		self.mainFrame.setStatusDone('Initialisation du groupe : ' + QGP.configDBCartoGroupName + ' - OK mais Restart automatique nécessaire !')

		TDAT.sleep(1000)	
		self.mainFrame.requestRestart()


	def createGroupDB_POIs(self):
		self.mainFrame.setStatusWorking('Initialisation du groupe : ' + QGP.configDBPOIsGroupName)
		self.createGroupIfNeeded(QGP.configDBPOIsGroupName, 4)
		progressBar = TPRO.createProgressBar(self.buttonInstallDBPOIs, len(QGP.tablePOIsNameDico), 'Normal')
	
		for tableName in QGP.tablePOIsNameDico:
			if TLAY.findLayerInGroup(QGP.configDBPOIsGroupName, tableName)[0] == None:
				
#				Create URI				
				
				uri = QGP.configDBPOIsGRInstallUriGeom if QGP.tablePOIsNameDico[tableName][2] != None else QGP.configDBPOIsInstallUriNoGeom
				uri = uri.replace('%KEY%',  QGP.tablePOIsNameDico[tableName][1])
				if QGP.tablePOIsNameDico[tableName][2] != None : uri = uri.replace('%GEOM%', QGP.tablePOIsNameDico[tableName][2])
				uri = uri.replace('%LAYER%', tableName)

#				Ajouter la couche	

				self.addDBLayer(uri, QGP.configDBPOIsGroupName, tableName)
		
				self.mainFrame.setStatusWorking(tableName + ' : ajoutée au Canevas !')
				TDAT.sleep(250)

				self.initializeGroupDBPOIs()

			progressBar.setValue(progressBar.value() + 1)
			QgsApplication.processEvents()

		del progressBar
	
		self.initializeGroupDBPOIs()
		self.mainFrame.setStatusDone('Initialisation du groupe : ' + QGP.configDBPOIsGroupName + ' - OK !')


	def createGroupDB_Baliseurs(self):
		self.mainFrame.setStatusWorking('Initialisation du groupe : ' + QGP.configDBBaliseursGroupName)
		self.createGroupIfNeeded(QGP.configDBBaliseursGroupName, 4)
		progressBar = TPRO.createProgressBar(self.buttonInstallDBBaliseurs, len(QGP.tableBaliseursNameDico), 'Normal')
	
		for tableName in QGP.tableBaliseursNameDico:
			if TLAY.findLayerInGroup(QGP.configDBBaliseursGroupName, tableName)[0] == None:
				
#				Create URI				
				
				uri = QGP.configDBBaliseursGRInstallUriGeom if QGP.tableBaliseursNameDico[tableName][2] != None else QGP.configDBBaliseursInstallUriNoGeom
				uri = uri.replace('%KEY%',  QGP.tableBaliseursNameDico[tableName][1])
				if QGP.tableBaliseursNameDico[tableName][2] != None : uri = uri.replace('%GEOM%', QGP.tableBaliseursNameDico[tableName][2])
				uri = uri.replace('%LAYER%', tableName)

#				Ajouter la couche	

				self.addDBLayer(uri, QGP.configDBBaliseursGroupName, tableName)
		
				self.mainFrame.setStatusWorking(tableName + ' : ajoutée au Canevas !')
				TDAT.sleep(250)

				self.initializeGroupDBBaliseurs()

			progressBar.setValue(progressBar.value() + 1)
			QgsApplication.processEvents()

		del progressBar
	
		self.initializeGroupDBBaliseurs()
		self.mainFrame.setStatusDone('Initialisation du groupe : ' + QGP.configDBBaliseursGroupName + ' - OK !')


	def addRastersToGroup(self, groupName, path, rasterList, prefix, crsString, progressBar):
		crsRaster = QgsCoordinateReferenceSystem()
		crsRaster.createFromString(crsString)

		for rasterName in rasterList:
			canevasName = prefix + rasterName
			if TLAY.findLayerInGroup(groupName, canevasName)[0] == None:
				layer, errorText = TLAY.loadRaster(path, rasterName, groupName, canevasName, crsRaster, QGP.configIgn50InstallOpacity)
				if layer == None:
					self.mainFrame.setStatusError(errorText, False)
					TDAT.sleep(1000)
			progressBar.setValue(progressBar.value() + 1)


	def createGroupMnt(self):
		self.mainFrame.setStatusWorking('Initialisation du groupe : ' + QGP.configMntGroupName)
		self.createGroupIfNeeded(QGP.configMntGroupName, 999)
		progressBar = TPRO.createProgressBar(self.buttonInstallMnt, len(QGP.configMntShapesList), 'Normal')

		self.addRastersToGroup(QGP.configMntGroupName, QGP.configPathMntShapes, QGP.configMntShapesList, '', 'EPSG:3812', progressBar)
		groupRaster = TLAY.findGroup( QGP.configMntGroupName)[0]
		groupRaster.setItemVisibilityCheckedRecursive(True)
		groupRaster.setItemVisibilityChecked(False)
		groupRaster.setExpanded(False)
		
		del progressBar
		
		self.initializeGroupMnt()
		self.mainFrame.setStatusDone('Initialisation des groupes : ' + QGP.configMntGroupName + ' - OK')


	def createGroupBorder(self):
		self.mainFrame.setStatusWorking('Initialisation du groupe : ' + QGP.configBorderGroupName)
		self.createGroupIfNeeded(QGP.configBorderGroupName, 5)

		for shapeName in QGP.configBorderShapesList:
			if TLAY.findLayerInGroup(QGP.configFrameGroupName, shapeName)[0] == None:
				TLAY.loadLayer(QGP.configPathBorderShapes, shapeName, QGP.configBorderGroupName, shapeName, None, None, False)

		groupBorder = TLAY.findGroup( QGP.configBorderGroupName)[0]
		groupBorder.setItemVisibilityCheckedRecursive(True)
		groupBorder.setItemVisibilityChecked(False)
		groupBorder.setExpanded(False)
		
		self.initializeGroupBorder()
		self.mainFrame.setStatusDone('Initialisation du groupe : ' + QGP.configBorderGroupName + ' - OK')


	def createGroupGrid(self):
		self.mainFrame.setStatusWorking('Initialisation du groupe : ' + QGP.configGridGroupName)
		self.createGroupIfNeeded(QGP.configGridGroupName, 999)

		for shapeName in QGP.configGridShapesList:
			if TLAY.findLayerInGroup(QGP.configGridGroupName, shapeName)[0] == None:
				TLAY.loadLayer(QGP.configPathGridShapes, shapeName, QGP.configGridGroupName, shapeName, None, None, False)

		groupGrid = TLAY.findGroup( QGP.configGridGroupName)[0]
		groupGrid.setItemVisibilityCheckedRecursive(True)
		groupGrid.setItemVisibilityChecked(False)
		groupGrid.setExpanded(False)
		
		self.initializeGroupGrid()
		self.mainFrame.setStatusDone('Initialisation du groupe : ' + QGP.configGridGroupName + ' - OK')


	def createGroupCdn(self):
		self.mainFrame.setStatusWorking('Initialisation du groupe : ' + QGP.configCdnGroupName)
		self.createGroupIfNeeded(QGP.configCdnGroupName, 999)

		for shapeName in QGP.configCdnShapesList:
			if TLAY.findLayerInGroup(QGP.configFrameGroupName, shapeName)[0] == None:
				TLAY.loadLayer(QGP.configPathCdnShapes, shapeName, QGP.configCdnGroupName, shapeName, None, None, False)

		groupCdn = TLAY.findGroup( QGP.configCdnGroupName)[0]
		groupCdn.setItemVisibilityCheckedRecursive(True)
		groupCdn.setItemVisibilityChecked(False)
		groupCdn.setExpanded(False)
		
		self.initializeGroupCdn()
		self.mainFrame.setStatusDone('Initialisation des groupes : ' + QGP.configCdnGroupName + ' - OK')


	def createGroupIgn50(self):
		self.mainFrame.setStatusWorking('Initialisation du groupe : ' + QGP.configIGN50Ed3GroupName)
		self.createGroupIfNeeded(QGP.configIGN50Ed3GroupName, 999)
		self.createGroupIfNeeded(QGP.configIGN50Ed4GroupName, 999)
		progressBar = TPRO.createProgressBar(self.buttonInstallIgn50, 2 * len(QGP.configIgn50ShapesList), 'Normal')

		self.addRastersToGroup(QGP.configIGN50Ed3GroupName, QGP.configPathIgn50Ed3Shapes, QGP.configIgn50ShapesList, 'Ed3-', 'EPSG:3812', progressBar)
		groupRaster = TLAY.findGroup( QGP.configIGN50Ed3GroupName)[0]
		groupRaster.setExpanded(False)
		groupRaster.setItemVisibilityCheckedRecursive(True)
		groupRaster.setItemVisibilityChecked(False)

		self.addRastersToGroup(QGP.configIGN50Ed4GroupName, QGP.configPathIgn50Ed4Shapes, QGP.configIgn50ShapesList, 'Ed4-', 'EPSG:3812', progressBar)
		groupRaster = TLAY.findGroup( QGP.configIGN50Ed4GroupName)[0]
		groupRaster.setItemVisibilityCheckedRecursive(True)
		groupRaster.setItemVisibilityChecked(False)
		groupRaster.setExpanded(False)
		
		del progressBar
		
		self.initializeGroupIgn50()
		self.mainFrame.setStatusDone('Initialisation des groupes : ' + QGP.configIGN50Ed3GroupName + ' et ' + QGP.configIGN50Ed4GroupName + ' - OK')


	def createGroupIgn250(self):
		self.mainFrame.setStatusWorking('Initialisation du groupe : ' + QGP.configIGN250GroupName)
		self.createGroupIfNeeded(QGP.configIGN250GroupName, 999)
		progressBar = TPRO.createProgressBar(self.buttonInstallIgn250, len(QGP.configIgn250ShapesList), 'Normal')

		self.addRastersToGroup(QGP.configIGN250GroupName, QGP.configPathIgn250Shapes, QGP.configIgn250ShapesList, '', 'EPSG:3812', progressBar)
		groupRaster = TLAY.findGroup( QGP.configIGN50Ed3GroupName)[0]
		groupRaster.setItemVisibilityCheckedRecursive(True)
		groupRaster.setItemVisibilityChecked(False)
		groupRaster.setExpanded(False)
		
		del progressBar
		
		self.initializeGroupIgn250()
		self.mainFrame.setStatusDone('Initialisation des groupes : ' + QGP.configIGN250GroupName + ' - OK')


	def createGroupIgn400(self):
		self.mainFrame.setStatusWorking('Initialisation du groupe : ' + QGP.configIGN400GroupName)
		self.createGroupIfNeeded(QGP.configIGN400GroupName, 999)
		progressBar = TPRO.createProgressBar(self.buttonInstallIgn400, len(QGP.configIgn400ShapesList), 'Normal')

		self.addRastersToGroup(QGP.configIGN400GroupName, QGP.configPathIgn400Shapes, QGP.configIgn400ShapesList, '', 'EPSG:31370', progressBar)
		groupRaster = TLAY.findGroup( QGP.configIGN50Ed3GroupName)[0]
		groupRaster.setItemVisibilityCheckedRecursive(True)
		groupRaster.setItemVisibilityChecked(False)
		groupRaster.setExpanded(False)
		
		del progressBar
		
		self.initializeGroupIgn400()
		self.mainFrame.setStatusDone('Initialisation des groupes : ' + QGP.configIGN400GroupName + ' - OK')


	def createGroupPublicMap(self):
	
		self.mainFrame.setStatusWorking('Initialisation du groupe : ' + QGP.configPublicMapGroupName)
		self.createGroupIfNeeded(QGP.configPublicMapGroupName, 999)
		progressBar = TPRO.createProgressBar(self.buttonInstallPublicMap, len(QGP.tablePublicNameDico), 'Normal')
	
		for tableName in QGP.tablePublicNameDico:
			if TLAY.findLayerInGroup(QGP.configPublicMapGroupName, tableName)[0] == None:
				
#				Create URI				
				
				uri = QGP.configReseauGRInstallUriGeom if QGP.tablePublicNameDico[tableName][2] != None else QGP.configReseauGRInstallUriNoGeom
				uri = uri.replace('%KEY%',  QGP.tablePublicNameDico[tableName][1])
				if QGP.tablePublicNameDico[tableName][2] != None : uri = uri.replace('%GEOM%', QGP.tablePublicNameDico[tableName][2])
				uri = uri.replace('%LAYER%', tableName)

#				Ajouter la couche			

				self.addDBLayer(uri, QGP.configPublicMapGroupName, tableName)

				self.mainFrame.setStatusWorking(tableName + ' : ajoutée au Canevas !')
				TDAT.sleep(1000)

				self.initializeGroupPublicMap()

			progressBar.setValue(progressBar.value() + 1)
			QgsApplication.processEvents()

		del progressBar
	
		self.initializeGroupPublicMap()
		self.mainFrame.setStatusDone('Initialisation du groupe : ' + QGP.configPublicMapGroupName + ' - OK')

	
# ========================================================================================
# ========================================================================================
#
# Création des différents cadres Menu
# 
# ========================================================================================
# ========================================================================================


# ========================================================================================
# Cadre : Groupe Descriptifs Cartes
# ========================================================================================

	def menuBoxDescriptionGroup(self):

		groupBoxDescription = QtWidgets.QGroupBox('Groupe: Descriptifs Cartes', self.mainMenu)
		groupBoxDescription.setStyleSheet(DSTY.styleBox)

# 	Ajouter Label et Info pour Groupe Description

		TBUT.createLabelBlackButton(groupBoxDescription, 1, 1, 'Groupe Qgis', 'Normal')
		self.buttonGroupDescriptionInfo = TBUT.createLabelGreenButton(groupBoxDescription, 2, 1, QGP.configFrameGroupName, 'Normal', 'Small')

# 	Ajouter Label et Info pour Copyright Cartes

		TBUT.createLabelBlackButton(groupBoxDescription, 1, 2, 'Couche Copyright', 'Normal')
		self.buttonLayerCopyrightInfo = TBUT.createLabelGreenButton(groupBoxDescription, 2, 2, QGP.configShapeMapDecorationCopyright, 'Normal', 'Small')

# 	Ajouter Label et Info pour Numéro Cartes

		TBUT.createLabelBlackButton(groupBoxDescription, 1, 3, 'Couche Numéro', 'Normal')
		self.buttonLayerNumeroInfo = TBUT.createLabelGreenButton(groupBoxDescription, 2, 3, QGP.configShapeMapDecorationNumber, 'Normal', 'Small')

# 	Ajouter Label et Info pour Cadre Blanc

		TBUT.createLabelBlackButton(groupBoxDescription, 1, 4, 'Couche Cadre', 'Normal')
		self.buttonLayerWhiteFrameInfo = TBUT.createLabelGreenButton(groupBoxDescription, 2, 4, QGP.configShapeMapDecorationWhiteFrame, 'Normal', 'Small')

#	Bouton Installer

		buttonInstall = TBUT.createActionButton(groupBoxDescription, 4, 4, 'Installer', 'Normal')
		buttonInstall.clicked.connect(self.createGroupDescriptions)

# 	Terminé

		groupBoxDescription.repaint()

		return groupBoxDescription


# ========================================================================================
# Cadre : Groupe DB Carto
# ========================================================================================

	def menuBoxDBCartoGroup(self):

		groupBoxDBCarto = QtWidgets.QGroupBox('Groupe: Base de Données Carto', self.mainMenu)
		groupBoxDBCarto.setStyleSheet(DSTY.styleBox)

# 	Ajouter Label et Info pour Groupe DB Carto

		TBUT.createLabelBlackButton(groupBoxDBCarto, 1, 1, 'Groupe Qgis', 'Normal')
		self.buttonGroupDBCartoInfo = TBUT.createLabelGreenButton(groupBoxDBCarto, 2, 1, QGP.configDBCartoGroupName, 'Normal', 'Small')

# 	Ajouter Label et Info pour les Tables de la DB

		self.buttonTableDBInfoList = []
		for index, tableName in zip(range(len(QGP.tableNameDico)), QGP.tableNameDico) :
			TBUT.createLabelBlackButton(groupBoxDBCarto, QGP.tableNameDico[tableName][0][1], 1 + QGP.tableNameDico[tableName][0][0], tableName, 'Normal')
			self.buttonTableDBInfoList.append(TBUT.createLabelGreenButton(groupBoxDBCarto, 1 + QGP.tableNameDico[tableName][0][1], 1 + QGP.tableNameDico[tableName][0][0], tableName, 'Normal', 'Small'))

#	Bouton Installer

		self.buttonInstallDBCarto = TBUT.createActionButton(groupBoxDBCarto, 4, 7, 'Installer', 'Normal')
		self.buttonInstallDBCarto.clicked.connect(self.createGroupDB_Carto)

# 	Terminé

		groupBoxDBCarto.repaint()

		return groupBoxDBCarto


# ========================================================================================
# Cadre : Groupe DB POIs
# ========================================================================================

	def menuBoxDBPOIsGroup(self):

		groupBoxDBPOIs = QtWidgets.QGroupBox('Groupe: Base de Données POIs', self.mainMenu)
		groupBoxDBPOIs.setStyleSheet(DSTY.styleBox)

# 	Ajouter Label et Info pour Groupe DB Carto

		TBUT.createLabelBlackButton(groupBoxDBPOIs, 1, 1, 'Groupe Qgis', 'Normal')
		self.buttonGroupDBPOIsInfo = TBUT.createLabelGreenButton(groupBoxDBPOIs, 2, 1, QGP.configDBPOIsGroupName, 'Normal', 'Small')

# 	Ajouter Label et Info pour les Tables de la DB

		self.buttonTableDBPOIsInfoList = []
		for tableName in QGP.tablePOIsNameDico:
			index = QGP.tablePOIsNameDico[tableName][0]
			TBUT.createLabelBlackButton(groupBoxDBPOIs, 1, 2 + index, 'Table ' + tableName, 'Normal')
			self.buttonTableDBPOIsInfoList.append(TBUT.createLabelGreenButton(groupBoxDBPOIs, 2, 2 + index, tableName, 'Normal', 'Small'))

#	Bouton Installer

		self.buttonInstallDBPOIs = TBUT.createActionButton(groupBoxDBPOIs, 4, 4, 'Installer', 'Normal')
		self.buttonInstallDBPOIs.clicked.connect(self.createGroupDB_POIs)

# 	Terminé

		groupBoxDBPOIs.repaint()

		return groupBoxDBPOIs


# ========================================================================================
# Cadre : Groupe DB Baliseurs
# ========================================================================================

	def menuBoxDBBaliseursGroup(self):

		groupBoxDBBaliseurs = QtWidgets.QGroupBox('Groupe: Base de Données Baliseurs', self.mainMenu)
		groupBoxDBBaliseurs.setStyleSheet(DSTY.styleBox)

# 	Ajouter Label et Info pour Groupe DB Carto

		TBUT.createLabelBlackButton(groupBoxDBBaliseurs, 1, 1, 'Groupe Qgis', 'Normal')
		self.buttonGroupDBBaliseursInfo = TBUT.createLabelGreenButton(groupBoxDBBaliseurs, 2, 1, QGP.configDBBaliseursGroupName, 'Normal', 'Small')

# 	Ajouter Label et Info pour les Tables de la DB

		self.buttonTableDBBaliseursInfoList = []
		for tableName in QGP.tableBaliseursNameDico:
			index = QGP.tableBaliseursNameDico[tableName][0]
			TBUT.createLabelBlackButton(groupBoxDBBaliseurs, 1, 2 + index, 'Table ' + tableName, 'Normal')
			self.buttonTableDBBaliseursInfoList.append(TBUT.createLabelGreenButton(groupBoxDBBaliseurs, 2, 2 + index, tableName, 'Normal', 'Small'))

#	Bouton Installer

		self.buttonInstallDBBaliseurs = TBUT.createActionButton(groupBoxDBBaliseurs, 4, 5, 'Installer', 'Normal')
		self.buttonInstallDBBaliseurs.clicked.connect(self.createGroupDB_Baliseurs)

# 	Terminé

		groupBoxDBBaliseurs.repaint()

		return groupBoxDBBaliseurs


# ========================================================================================
# Cadre : Groupe des MNT
# ========================================================================================

	def menuBoxMntGroup(self):

		groupBoxMnt = QtWidgets.QGroupBox('Groupe: Modéles Numériques de Terrain pour le calcul des Altitude', self.mainMenu)
		groupBoxMnt.setStyleSheet(DSTY.styleBox)

# 	Ajouter Label et Info pour Groupe

		TBUT.createLabelBlackButton(groupBoxMnt, 1, 1, 'Groupe Qgis', 'Normal')
		self.buttonGroupMntInfo = TBUT.createLabelGreenButton(groupBoxMnt, 2, 1, QGP.configMntGroupName, 'Normal', 'Small')

		TBUT.createLabelBlackButton(groupBoxMnt, 1, 2, 'Rasters', 'Normal')
		self.buttonRasterMntInfo = TBUT.createLabelGreenButton(groupBoxMnt, 2, 2, '. . .', 'Normal', 'Small')

#	Bouton Installer

		self.buttonInstallMnt = TBUT.createActionButton(groupBoxMnt, 4, 2, 'Installer', 'Normal')
		self.buttonInstallMnt.clicked.connect(self.createGroupMnt)

# 	Terminé

		groupBoxMnt.repaint()

		return groupBoxMnt


# ========================================================================================
# Cadre : Groupe des Frontières
# ========================================================================================

	def menuBoxBorderGroup(self):

		groupBoxBorder = QtWidgets.QGroupBox('Groupe: Couches de définition des Frontières', self.mainMenu)
		groupBoxBorder.setStyleSheet(DSTY.styleBox)

# 	Ajouter Label et Info pour Groupe

		TBUT.createLabelBlackButton(groupBoxBorder, 1, 1, 'Groupe Qgis', 'Normal')
		self.buttonGroupBorderInfo = TBUT.createLabelGreenButton(groupBoxBorder, 2, 1, QGP.configBorderGroupName, 'Normal', 'Small')

		TBUT.createLabelBlackButton(groupBoxBorder, 1, 2, 'Couches', 'Normal')
		self.buttonShapeBorderInfo = TBUT.createLabelGreenButton(groupBoxBorder, 2, 2, '. . .', 'Normal', 'Small')

#	Bouton Installer

		self.buttonInstallBorder = TBUT.createActionButton(groupBoxBorder, 4, 2, 'Installer', 'Normal')
		self.buttonInstallBorder.clicked.connect(self.createGroupBorder)

# 	Terminé

		groupBoxBorder.repaint()

		return groupBoxBorder


# ========================================================================================
# Cadre : Groupe des Grilles
# ========================================================================================

	def menuBoxGridGroup(self):

		groupBoxGrid = QtWidgets.QGroupBox('Groupe: Couches des Grilles UTM', self.mainMenu)
		groupBoxGrid.setStyleSheet(DSTY.styleBox)

# 	Ajouter Label et Info pour Groupe

		TBUT.createLabelBlackButton(groupBoxGrid, 1, 1, 'Groupe Qgis', 'Normal')
		self.buttonGroupGridInfo = TBUT.createLabelGreenButton(groupBoxGrid, 2, 1, QGP.configGridGroupName, 'Normal', 'Small')

		TBUT.createLabelBlackButton(groupBoxGrid, 1, 2, 'Couches', 'Normal')
		self.buttonShapeGridInfo = TBUT.createLabelGreenButton(groupBoxGrid, 2, 2, '. . .', 'Normal', 'Small')

#	Bouton Installer

		self.buttonInstallGrid = TBUT.createActionButton(groupBoxGrid, 4, 2, 'Installer', 'Normal')
		self.buttonInstallGrid.clicked.connect(self.createGroupGrid)

# 	Terminé

		groupBoxGrid.repaint()

		return groupBoxGrid


# ========================================================================================
# Cadre : Groupe Raster IGN-50
# ========================================================================================

	def menuBoxIgn50Group(self):

		groupBoxIgn50 = QtWidgets.QGroupBox('Groupe: Cartes Raster IGN 1:50.000', self.mainMenu)
		groupBoxIgn50.setStyleSheet(DSTY.styleBox)

# 	Ajouter Label et Info pour Groupe Edition 3

		TBUT.createLabelBlackButton(groupBoxIgn50, 1, 1, 'Groupe Qgis', 'Normal')
		self.buttonGroupIgn50V3Info = TBUT.createLabelGreenButton(groupBoxIgn50, 2, 1, QGP.configIGN50Ed3GroupName, 'Normal', 'Small')

		TBUT.createLabelBlackButton(groupBoxIgn50, 1, 2, 'Rasters', 'Normal')
		self.buttonMapIgn50V3Info = TBUT.createLabelGreenButton(groupBoxIgn50, 2, 2, '. . .', 'Normal', 'Small')


# 	Ajouter Label et Info pour Groupe Edition 4

		self.buttonGroupIgn50V4Info = TBUT.createLabelGreenButton(groupBoxIgn50, 3, 1, QGP.configIGN50Ed4GroupName, 'Normal', 'Small')
		self.buttonMapIgn50V4Info = TBUT.createLabelGreenButton(groupBoxIgn50, 3, 2, '. . .', 'Normal', 'Small')

#	Bouton Installer

		self.buttonInstallIgn50 = TBUT.createActionButton(groupBoxIgn50, 4, 2, 'Installer', 'Normal')
		self.buttonInstallIgn50.clicked.connect(self.createGroupIgn50)

# 	Terminé

		groupBoxIgn50.repaint()

		return groupBoxIgn50


# ========================================================================================
# Cadre : Groupe Raster IGN-250
# ========================================================================================

	def menuBoxIgn250Group(self):

		groupBoxIgn250 = QtWidgets.QGroupBox('Groupe: Cartes Raster IGN 1:250.000', self.mainMenu)
		groupBoxIgn250.setStyleSheet(DSTY.styleBox)

# 	Ajouter Label et Info pour Groupe

		TBUT.createLabelBlackButton(groupBoxIgn250, 1, 1, 'Groupe / Raster', 'Normal')
		self.buttonGroupIgn250Info = TBUT.createLabelGreenButton(groupBoxIgn250, 2, 1, QGP.configIGN250GroupName, 'Normal', 'Small')
		self.buttonMapIgn250Info = TBUT.createLabelGreenButton(groupBoxIgn250, 3, 1, '. . .', 'Normal', 'Small')

#	Bouton Installer

		self.buttonInstallIgn250 = TBUT.createActionButton(groupBoxIgn250, 4, 1, 'Installer', 'Normal')
		self.buttonInstallIgn250.clicked.connect(self.createGroupIgn250)

# 	Terminé

		groupBoxIgn250.repaint()

		return groupBoxIgn250


# ========================================================================================
# Cadre : Groupe Raster IGN-400
# ========================================================================================

	def menuBoxIgn400Group(self):

		groupBoxIgn400 = QtWidgets.QGroupBox('Groupe: Cartes Raster IGN 1:400.000', self.mainMenu)
		groupBoxIgn400.setStyleSheet(DSTY.styleBox)

# 	Ajouter Label et Info pour Groupe

		TBUT.createLabelBlackButton(groupBoxIgn400, 1, 1, 'Groupe / Raster', 'Normal')
		self.buttonGroupIgn400Info = TBUT.createLabelGreenButton(groupBoxIgn400, 2, 1, QGP.configIGN400GroupName, 'Normal', 'Small')
		self.buttonMapIgn400Info = TBUT.createLabelGreenButton(groupBoxIgn400, 3, 1, '. . .', 'Normal', 'Small')

#	Bouton Installer

		self.buttonInstallIgn400 = TBUT.createActionButton(groupBoxIgn400, 4, 1, 'Installer', 'Normal')
		self.buttonInstallIgn400.clicked.connect(self.createGroupIgn400)

# 	Terminé

		groupBoxIgn400.repaint()

		return groupBoxIgn400


# ========================================================================================
# Cadre : Groupe des Courbes de Niveau
# ========================================================================================

	def menuBoxCdnGroup(self):

		groupBoxCdn = QtWidgets.QGroupBox('Groupe: Couches des Courbes de Niveau', self.mainMenu)
		groupBoxCdn.setStyleSheet(DSTY.styleBox)

# 	Ajouter Label et Info pour Groupe

		TBUT.createLabelBlackButton(groupBoxCdn, 1, 1, 'Groupe / MNT', 'Normal')
		self.buttonGroupCdnInfo = TBUT.createLabelGreenButton(groupBoxCdn, 2, 1, QGP.configCdnGroupName, 'Normal', 'Small')
		self.buttonShaperCdnInfo = TBUT.createLabelGreenButton(groupBoxCdn, 3, 1, '. . .', 'Normal', 'Small')

#	Bouton Installer

		self.buttonInstallCdn = TBUT.createActionButton(groupBoxCdn, 4, 1, 'Installer', 'Normal')
		self.buttonInstallCdn.clicked.connect(self.createGroupCdn)

# 	Terminé

		groupBoxCdn.repaint()

		return groupBoxCdn


# ========================================================================================
# Cadre : Groupe Carte Publique
# ========================================================================================

	def menuBoxPublicMapGroup(self):

		groupBoxPrivateMap = QtWidgets.QGroupBox('Groupe: Tables de la Carte Publique', self.mainMenu)
		groupBoxPrivateMap.setStyleSheet(DSTY.styleBox)

# 	Ajouter Label et Info pour Groupe

		TBUT.createLabelBlackButton(groupBoxPrivateMap, 1, 1, 'Groupe / Couches', 'Normal')
		self.buttonGroupPublicMapInfo = TBUT.createLabelGreenButton(groupBoxPrivateMap, 2, 1, QGP.configPublicMapGroupName, 'Normal', 'Small')


		self.buttonPublicMapInfo = TBUT.createLabelGreenButton(groupBoxPrivateMap, 3, 1, '. . .', 'Normal', 'Small')

#	Bouton Installer

		self.buttonInstallPublicMap = TBUT.createActionButton(groupBoxPrivateMap, 4, 1, 'Installer', 'Normal')
		self.buttonInstallPublicMap.clicked.connect(self.createGroupPublicMap)

# 	Terminé

		groupBoxPrivateMap.repaint()

		return groupBoxPrivateMap


# ========================================================================================
# --- THE END ---
# ========================================================================================
	