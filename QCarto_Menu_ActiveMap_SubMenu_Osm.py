# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Gestion des Menus : Page Carte Active - Sub Menu Osm
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
import ast
import os

import QCarto_Layers_Tracks as LTRK
import QCarto_Layers_ActiveMap as LMAP

import QCarto_Tools_Buttons as TBUT
import QCarto_Tools_Coding as TCOD
import QCarto_Tools_Dates as TDAT
import QCarto_Tools_Geometries as TGEO
import QCarto_Tools_Help as THEL
import QCarto_Tools_Files as TFIL
import QCarto_Tools_Layers as TLAY
import QCarto_Tools_Progress as TPRO

import QCarto_Definitions_Colors as DCOL
import QCarto_Definitions_Styles as DSTY
import QCarto_Definitions_Symbologie as DSYM
importlib.reload(DSYM)
import QCarto_Definitions_TopoGuides as DTOP	

import QCarto_Process_DownloadOsm as SOSMD
importlib.reload(SOSMD)
import QCarto_Process_CreateOsm as SOSMC
importlib.reload(SOSMC)

import QCarto_Process_Export as SEXP
importlib.reload(SEXP)


import QCarto_Parameters_Global
QGP = QCarto_Parameters_Global.globalParameters()


# ========================================================================================
# Class : subMenuActiveMapFrameOsm
# >>> iface
# >>> mainMenu 						: Widget of Main Menu
# >>> mainFrame 					: Main Menu Object
# >>> activeMapFrame 				: Active Map Menu Object
# >>> boxX , ...					: Position and dimensions of widget
# ========================================================================================

class subMenuActiveMapFrameOsm:

	def __init__(self, iface, mainMenu, mainFrame, activeMapFrame, boxPosX, boxPosY) :

# 	Paramètres fournis

		self.iface = iface
		self.mainMenu = mainMenu
		self.mainFrame = mainFrame
		self.activeMapFrame = activeMapFrame
		self.boxPosX = boxPosX
		self.boxPosY = boxPosY

#	Nom de la page

		self.pageName = 'Carte Active - Osm'

#	Variables globales de la classe
	
		self.scaleOsmLayers = 10000
		self.osmBackgroundPath = None
		self.recordStyleActive = False
	
# 	Création des sous-menus

		self.boxesList = []
		self.createMenuBoxes()

		
	def createMenuBoxes(self):
	
		self.groupBoxOsmDownload = self.menuBoxOsmDownload()
		DSTY.setBoxGeometry(self.groupBoxOsmDownload, self.boxPosX, self.boxPosY, 4, 1)
		self.boxesList.append(self.groupBoxOsmDownload)
	
		self.groupBoxOsmDisplay = self.menuBoxOsmDisplayLayers()
		DSTY.setBoxGeometry(self.groupBoxOsmDisplay, self.boxPosX, self.boxPosY + 2, 4, 3)
		self.boxesList.append(self.groupBoxOsmDisplay)
	
		self.groupBoxOsmLayers = self.menuBoxOsmLayers()
		DSTY.setBoxGeometry(self.groupBoxOsmLayers, self.boxPosX, self.boxPosY + 6, 4, 3)
		self.boxesList.append(self.groupBoxOsmLayers)
	
		self.groupBoxOsmExport = self.menuBoxOsmExport()
		DSTY.setBoxGeometry(self.groupBoxOsmExport, self.boxPosX, self.boxPosY + 10, 4, 1)
		self.boxesList.append(self.groupBoxOsmExport)

	
# ========================================================================================
# Actions : A la demande de la fenêtre principale
# ========================================================================================

#	Show - Ouverture de cette fenêtre

	def show(self):
		for box in self.boxesList: box.show(), box.repaint()
		self.refresh()
		
#	Hide - Ouverture d'une autre fenêtre

	def hide(self):
		for box in self.boxesList: box.hide()

#	Repaint 

	def repaint(self):
		for box in self.boxesList: box.repaint()

#	Close - Fermeture définitive

	def close(self):
		self.hide()
		for box in self.boxesList: del box

	def refresh(self):
		self.refreshActiveMapFeature()
		self.refreshDownloadCombo()
		self.refreshStyleCombo()
		self.refreshCanevasLayerCounts()
		self.refreshSavedFolderCombo()
		self.refreshExportListCombo()
		self.refreshExportOsmCombo()
	
	
# ========================================================================================
# ========================================================================================
#
# Initialisations et refresh
# 
# ========================================================================================
# ========================================================================================

	def refreshActiveMapFeature(self):
		self.activeMapFeature = self.mainFrame.selectedMapFeature
		self.activeMapItinerary = str(self.activeMapFeature[QGP.tableFramesFieldItineraryCode])
		self.activeMapName = str(self.activeMapFeature[QGP.tableFramesFieldName])
		self.activeMapGeometry = self.activeMapFeature.geometry()
		self.codeProject = TCOD.itineraryFolderFromTrackCode(self.activeMapItinerary)

	def refreshDownloadCombo(self):
		self.downloadListCombo.clear()
		self.downloadFolderPath = QGP.configPathOsmFiles.replace('%PROJECT%', self.codeProject)
		if not os.path.isdir(self.downloadFolderPath): return		
		for fileName in sorted(os.listdir(self.downloadFolderPath), reverse = True):
			if (self.activeMapItinerary + ' - ' + self.activeMapName) not in fileName : continue
			if fileName[-4:] != '.osm' : continue
			self.downloadListCombo.addItem(fileName)

	def refreshStyleCombo(self):
		self.styleListCombo.clear()
		if not os.path.isdir(QGP.configOsmStyles): return		
		for fileName in os.listdir(QGP.configOsmStyles) :
			if not os.path.isdir(QGP.configOsmStyles + fileName) : continue
			self.styleListCombo.addItem(fileName)

	def refreshCanevasLayerCounts(self):
		groupOsmName = QGP.configActiveMapOsmGroupName

		layerNamesList = [ coucheInfo[QGP.configLayerIndexName] for coucheInfo in QGP.configOsmLayers if coucheInfo[QGP.configLayerIndexType] == 'Points' ]
		layerCanevasSet = { TLAY.findLayerInGroup(groupOsmName, layerName)[0] for layerName in layerNamesList }
		layerCanevasSet.discard(None)
		text = '{:0d}: {:0d} points'.format(len(layerCanevasSet), sum(layer.featureCount() for layer in layerCanevasSet))
		self.canevasOsmPointsInfo.setText(DSTY.textFormatBlackSmall.replace('%TEXT%',text))
		DSTY.setStyleOkLabel(self.canevasOsmPointsInfo, 'Normal')	

		layerNamesList = [ coucheInfo[QGP.configLayerIndexName] for coucheInfo in QGP.configOsmLayers if coucheInfo[QGP.configLayerIndexType] == 'Lignes' ]
		layerCanevasSet = { TLAY.findLayerInGroup(groupOsmName, layerName)[0] for layerName in layerNamesList }
		layerCanevasSet.discard(None)
		text = '{:0d}: {:0d} lignes'.format(len(layerCanevasSet), sum(layer.featureCount() for layer in layerCanevasSet))
		self.canevasOsmLinesInfo.setText(DSTY.textFormatBlackSmall.replace('%TEXT%',text))
		DSTY.setStyleOkLabel(self.canevasOsmLinesInfo, 'Normal')	

		layerNamesList = [ coucheInfo[QGP.configLayerIndexName] for coucheInfo in QGP.configOsmLayers if coucheInfo[QGP.configLayerIndexType] == 'Aires' ]
		layerCanevasSet = { TLAY.findLayerInGroup(groupOsmName, layerName)[0] for layerName in layerNamesList }
		layerCanevasSet.discard(None)
		text = '{:0d}: {:0d} surfaces'.format(len(layerCanevasSet), sum(layer.featureCount() for layer in layerCanevasSet))
		self.canevasOsmAreasInfo.setText(DSTY.textFormatBlackSmall.replace('%TEXT%',text))
		DSTY.setStyleOkLabel(self.canevasOsmAreasInfo, 'Normal')	

	def refreshSavedFolderCombo(self):
		self.savedFolderListCombo.clear()
		savingPath = QGP.configPathMapShapesOsm.replace('%PROJECT%', self.codeProject)
		savingPath += self.activeMapItinerary + ' - ' + self.activeMapName + '/'
		if not os.path.isdir(savingPath) : return
		for fileName in sorted(os.listdir(savingPath), reverse = True):
			if not os.path.isdir(savingPath + fileName) : continue
			self.savedFolderListCombo.addItem(fileName)

	def refreshExportListCombo(self):
		self.exportListCombo.clear()
		savingPath = QGP.configPathExportOsm.replace('%PROJECT%', self.codeProject)
		if not os.path.isdir(savingPath) : return
		for fileName in sorted(os.listdir(savingPath), reverse = True):
			if not os.path.isfile(savingPath + fileName) : continue
			if not fileName.startswith(self.activeMapItinerary + ' - ' + self.activeMapName) : continue
			if fileName[-4:] != '.png' : continue
			self.exportListCombo.addItem(fileName)

	def refreshExportOsmCombo(self):
		self.activeMapFrame.exportOsmCombo.clear()
		groupOsmRasters, errorText = TLAY.findGroup(QGP.configActiveRasterOsmGroupName)
		if groupOsmRasters == None : return
		for child in groupOsmRasters.children():
			self.activeMapFrame.exportOsmCombo.addItem(child.name())


# ========================================================================================
# ========================================================================================
#
# Action Download and Create Layers
# 
# ========================================================================================
# ========================================================================================

	def buttonDownload_clicked(self):
		self.refreshActiveMapFeature()
		fileOsm = SOSMD.downloadMapArea(self.mainFrame, self.codeProject, self.activeMapFeature)
		self.refreshDownloadCombo()


	def buttonCreateLayers_clicked(self):
	
#	Vérifications préalables
	
		self.refreshActiveMapFeature()
		if self.downloadListCombo.currentText() == '':
			self.mainFrame.setStatusWarning('Vous devez sélectionner un fichier Osm !')
			return
		if not os.path.isfile(self.downloadFolderPath + self.downloadListCombo.currentText()) :
			self.mainFrame.setStatusWarning('Le fichier ' + self.downloadFolderPath + self.downloadListCombo.currentText() + ' est introuvable !')
			return
		groupName = QGP.configActiveMapOsmGroupName	
		if TLAY.isLayerInGroupEditable(groupName) :
			self.mainFrame.setStatusWarning('Le groupe ' + groupName + ' contient encore une couche ouverte en édition !')
			return

#	Créer et vider le groupe sur le Canevas

		groupName = QGP.configActiveMapOsmGroupName
		if TLAY.findGroup(groupName)[0] == None: TLAY.createGroup(groupName, 999)
		TLAY.findGroup(groupName)[0].setExpanded(False)
		TLAY.cleanLayerGroup(groupName)

		self.taskOsm = SOSMC.createMapShapesTask(self.iface, self.mainFrame, self.downloadFolderPath, self.downloadListCombo.currentText(), self.activeMapGeometry)
		self.taskOsm.start()

	
# ========================================================================================
# ========================================================================================
#
# Action Affichage et Styles
# 
# ========================================================================================
# ========================================================================================

	class buttonScaleAny_clicked:
		def __init__(self, iface, parentFrame, scale):
			self.iface = iface
			self.scale = scale
			self.parentFrame = parentFrame
		def __call__(self):
			self.iface.mapCanvas().zoomScale(self.scale)
			self.parentFrame.scaleOsmLayers = self.scale

	def buttonAddCDNLayers_clicked(self):
		groupOsmName = QGP.configActiveMapOsmGroupName
		groupOsm, errorText = TLAY.findGroup(groupOsmName)
		if groupOsm == None: return

		layerNamesList = [ coucheInfo[QGP.configLayerIndexName] for coucheInfo in QGP.configOsmLayers if coucheInfo[QGP.configLayerIndexType] == 'Courbes' ]

		for layerName in layerNamesList:
			layer, error = TLAY.findLayerInGroup(groupOsmName, layerName)
			if layer != None : continue
			layerCDN = self.findBestCDNLayer()
			if layerCDN == None : self.mainFrame.setStatusWarning('Aucune couche de courbe de niveau trouvée !') ; return 
			TLAY.loadLayer(QGP.configPathCdnShapes, layerCDN.name(), groupOsmName, layerName, None, None, False)
			self.buttonReorderLayers_clicked()

		for layerName in layerNamesList:
			layer, error = TLAY.findLayerInGroup(groupOsmName, layerName)
			if layer == None : continue
			node = QgsProject.instance().layerTreeRoot().findLayer(layer.id())
			if node : node.setItemVisibilityChecked(True)		

	def findBestCDNLayer(self):

# 		Trouver la couche : Frontière
	
		groupBorderName = QGP.configBorderGroupName
		layerBorderBel, errorText = TLAY.findLayerInGroup(groupBorderName, QGP.configBelgiumShapeName)
		if layerBorderBel == None : self.mainFrame.setStatusWarning(errorText) ; return None

# 		Trouver le groupe CDN

		groupCDNName = QGP.configCdnGroupName
		groupCDN, errorText = TLAY.findGroup(groupCDNName)
		if groupCDN == None: self.mainFrame.setStatusWarning(errorText) ; return None

#		Trouver les noms des couches CDN

		layerCDNNameList = 	QGP.configCdnShapesList

# 		Rechercher si la Carte déborde sur la frontière Belge et si oui, utiliser les XTRA

		borderBelGeometry = layerBorderBel.getFeature(0).geometry()
		if not borderBelGeometry.contains(self.activeMapGeometry) :
			layerCDN, errorText = TLAY.findLayerInGroup(groupCDNName, layerCDNNameList[0])
			if layerCDN == None : self.mainFrame.setStatusWarning(errorText) ; return None
			return layerCDN

# 		Trouver la Couche des Courbes adéquate

		for name in layerCDNNameList[1:] :
			layerCDN, errorText = TLAY.findLayerInGroup(groupCDNName, name)
			if layerCDN == None : self.mainFrame.setStatusWarning(errorText) ; return None
			if layerCDN.extent().contains(self.activeMapGeometry.boundingBox()) : return layerCDN


	def buttonReloadStyles_clicked(self):
		groupOsmName = QGP.configActiveMapOsmGroupName
		groupOsm, errorText = TLAY.findGroup(groupOsmName)
		if groupOsm == None: return

		self.mainFrame.setStatusWorking('Rechargement des styles ...')
		layerNamesList = [ coucheInfo[QGP.configLayerIndexName] for coucheInfo in QGP.configOsmLayers ]

		countOK = 0
		for layerName in layerNamesList:
			layer, error = TLAY.findLayerInGroup(groupOsmName, layerName)
			if layer == None : continue
			styleFullPath = QGP.configOsmStyles + self.styleListCombo.currentText() + '/' + layerName + '.qml'
			if not os.path.isfile(styleFullPath) : continue
			errorText, status = layer.loadNamedStyle(styleFullPath)
			if not status : self.mainFrame.setStatusWarning(errorText, 2000) ; continue
			countOK += 1

		self.mainFrame.setStatusDone(str(countOK) + ' styles rechargés sur ' + str(len(layerNamesList)))


	def buttonRecordStyles_rightClicked(self):
		DSTY.setStyleNormalButton(self.buttonRecordStyles)
		self.recordStyleActive = True

	def buttonRecordStyles_clicked(self):
		if not self.recordStyleActive : self.mainFrame.setStatusWarning('La fonction doit être activée (clic-droit) !') ; return
		groupOsmName = QGP.configActiveMapOsmGroupName
		groupOsm, errorText = TLAY.findGroup(groupOsmName)
		if groupOsm == None: return
		layerNamesList = [ coucheInfo[QGP.configLayerIndexName] for coucheInfo in QGP.configOsmLayers ]
		TFIL.ensure_dir(QGP.configOsmStyles + self.styleListCombo.currentText())

		countOK = 0
		for layerName in layerNamesList:
			layer, error = TLAY.findLayerInGroup(groupOsmName, layerName)
			if layer == None : continue
			styleFullPath = QGP.configOsmStyles + self.styleListCombo.currentText() + '/' + layerName + '.qml'
			errorText, status = layer.saveNamedStyle(styleFullPath)
			if not status : self.mainFrame.setStatusWarning(errorText, 2000) ; continue
			countOK += 1
	
		DSTY.setStyleMainButtonsInactive(self.buttonRecordStyles)
		self.recordStyleActive = False
		
		self.mainFrame.setStatusDone(str(countOK) + ' styles enregistrés sur ' + str(len(layerNamesList)))


	def buttonReorderLayers_clicked(self):
		groupName = QGP.configActiveMapOsmGroupName
		group, errorText = TLAY.findGroup(groupName)
		if group == None: return

		self.mainFrame.setStatusWorking('Remise des couches Osm dans le bon ordre ...')
		layerNamesList = [ coucheInfo[QGP.configLayerIndexName] for coucheInfo in QGP.configOsmLayers ]
		layerNamesList.reverse()

		for layerName in layerNamesList:
			for layerNode in group.findLayers():
				if layerNode.name() == layerName: 
					cloneNode = layerNode.clone()
					group.insertChildNode(999, cloneNode)
					group.removeChildNode(layerNode)
					break

		self.mainFrame.setStatusDone('Couches Osm remises en ordre !')


	def buttonSetLayersVisible_clicked(self):
		groupOsmName = QGP.configActiveMapOsmGroupName
		groupOsm, errorText = TLAY.findGroup(groupOsmName)
		if groupOsm == None: return
	
		groupCWName = QGP.configIGNCWGroupName
		groupCW, errorText = TLAY.findGroup(groupCWName)
		if groupCW == None: return

		groupCW.setItemVisibilityChecked (False)
		groupOsm.setItemVisibilityChecked (True)
	
	
	def buttonSetLayersHidden_clicked(self):
		groupOsmName = QGP.configActiveMapOsmGroupName
		groupOsm, errorText = TLAY.findGroup(groupOsmName)
		if groupOsm == None: return
	
		groupCWName = QGP.configIGNCWGroupName
		groupCW, errorText = TLAY.findGroup(groupCWName)
		if groupCW == None: return

		groupCW.setItemVisibilityChecked (True)
		groupOsm.setItemVisibilityChecked (False)
		
	
	def showRasterGroup(self):
		groupOsmName = QGP.configActiveMapOsmGroupName
		groupOsm, errorText = TLAY.findGroup(groupOsmName)
		if groupOsm == None: return
	
		groupCWName = QGP.configIGNCWGroupName
		groupCW, errorText = TLAY.findGroup(groupCWName)
		if groupCW == None: return

		groupOsmRasterName = QGP.configActiveRasterOsmGroupName
		groupRasterOsm, errorText = TLAY.findGroup(groupOsmRasterName)
		if groupOsmRasterName == None: return

		groupCW.setItemVisibilityChecked (False)
		groupOsm.setItemVisibilityChecked (False)
		groupRasterOsm.setItemVisibilityChecked (True)


# ========================================================================================
# ========================================================================================
#
# Action Couches
# 
# ========================================================================================
# ========================================================================================

	def buttonSaveLayers_clicked(self):
	
#		Retrouver le Path 	

		savingPath = QGP.configPathMapShapesOsm.replace('%PROJECT%', self.codeProject)
		savingPath += self.activeMapItinerary + ' - ' + self.activeMapName + '/'
		savingPath += self.activeMapName + ' (' + TDAT.getTimeStamp() + ')/'
		TFIL.ensure_dir(savingPath)

#		Enregistrer les couches		

		groupOsmName = QGP.configActiveMapOsmGroupName
		groupOsm, errorText = TLAY.findGroup(groupOsmName)
		if groupOsm == None: self.mainFrame.setStatusWarning(errorText) ; return

		self.mainFrame.setStatusWorking(savingPath + ' ...')

		layerNamesList = [ coucheInfo[QGP.configLayerIndexName] for coucheInfo in QGP.configOsmLayers ]
		countOK = 0
		for layerName in layerNamesList:
			layer, error = TLAY.findLayerInGroup(groupOsmName, layerName)
			if layer == None : continue
			status, errorText = QgsVectorFileWriter.writeAsVectorFormat(layer, savingPath + layerName, 'UTF-8', layer.crs(), 'ESRI Shapefile')
			if status != 0: self.mainFrame.setStatusWarning(errorText, 2000) ; continue
			countOK += 1
			qmlFileFullPath = savingPath + layerName + '.qml'
			file = open(qmlFileFullPath, 'w') ; file.close()
			layer.saveNamedStyle(qmlFileFullPath)
			
		self.refreshSavedFolderCombo()	
		self.mainFrame.setStatusDone(savingPath + ' : ' + str(countOK) + ' couches enregistrées sur ' + str(len(layerNamesList)))

	
	def buttonClearLayers_clicked(self):
		if TLAY.isLayerInGroupEditable(QGP.configActiveMapOsmGroupName) :
			self.mainFrame.setStatusWarning('Une ou plusieurs couches sont en mode édition !') ; return
		TLAY.cleanLayerGroup(QGP.configActiveMapOsmGroupName)


	def buttonLoadLayers_clicked(self):

		self.refreshActiveMapFeature()

#		Retrouver le Path 	
	
		loadingPath = QGP.configPathMapShapesOsm.replace('%PROJECT%', self.codeProject)
		loadingPath += self.activeMapItinerary + ' - ' + self.activeMapName + '/'
		loadingPath += self.savedFolderListCombo.currentText() + '/'

#		Vérifications préalables
	
		if self.savedFolderListCombo.currentText() == '':
			self.mainFrame.setStatusWarning('Vous devez sélectionner un répertoire !')
			return
		if not os.path.isdir(loadingPath) :
			self.mainFrame.setStatusWarning('Le répertoire ' + loadingPath + ' est introuvable !')
			return
			
		groupName = QGP.configActiveMapOsmGroupName	
		if TLAY.isLayerInGroupEditable(groupName) :
			self.mainFrame.setStatusWarning('Le groupe ' + groupName + ' contient encore une couche ouverte en édition !')
			return

		self.mainFrame.setStatusWorking('Rechargement des couches Osm ...')

#		Vider le groupe et le créer si nécessaire

		TLAY.cleanLayerGroup(groupName)
		TLAY.createGroup(groupName, 999)

#		Recharger les couches

		layerNamesList = [ coucheInfo[QGP.configLayerIndexName] for coucheInfo in QGP.configOsmLayers ]
		countOK = 0
		for layerName in layerNamesList:
			layer, errorText = TLAY.loadLayer(loadingPath, layerName, groupName, layerName, None, None, False)
			if layer == None :
				self.mainFrame.setStatusWarning(errorText, 2000) ; continue
			countOK += 1	
			
		self.buttonReorderLayers_clicked()
		self.refreshCanevasLayerCounts()
		self.mainFrame.setStatusDone(str(countOK) + ' couches rechargées sur ' + str(len(layerNamesList)))


# ========================================================================================
# ========================================================================================
#
# Action Export
# 
# ========================================================================================
# ========================================================================================

	def buttonExport_clicked(self):
	
#		Vérification du Groupe

		groupOsmName = QGP.configActiveMapOsmGroupName
		groupOsm, errorText = TLAY.findGroup(groupOsmName)
		if groupOsm == None: self.mainFrame.setStatusWarning(errorText) ; return
	
#		Détermination de la Liste des Couches
	
		osmLayersList = [child.layer() for child in groupOsm.children() if child.isVisible()]
		if osmLayersList == [] : self.mainFrame.setStatusWarning('Le groupe ' + groupOsmName + ' est vide !') ; return
		
#		Export

		self.osmBackgroundPath =  SEXP.process_Export(self.iface, self.mainFrame, self.activeMapFrame, 'OSM',
										QGP.configExportTextOsmLayers,  '', 
										self.scaleOsmLayers, 0,
										100, 0, 0, 
										False, False, osmLayersList)

#		Refresh Combo
	
		self.refreshExportListCombo()
	
	
	def buttonExport_rightClicked(self):
		if self.osmBackgroundPath != None :
			THEL.viewMapOnBrowser(self.mainFrame, 'Image du dernier Fond Osm Exporté', self.osmBackgroundPath)
	

	def buttonLoadExport_clicked(self):
	
#		Vérifications
	
		savingPath = QGP.configPathExportOsm.replace('%PROJECT%', self.codeProject)
		if not os.path.isdir(savingPath) : self.mainFrame.setStatusWarning('Le répertoire des Fonds Osm n\'existe pas (encore) !') ; return
		fileName = self.exportListCombo.currentText()
		if not os.path.isfile(savingPath + fileName) : self.mainFrame.setStatusWarning('Le fichier ' +  fileName + ' n\'existe pas !') ; return

		self.mainFrame.setStatusWorking('Rechargement du Raster Osm ...')
		
#		Création du Groupe si nécessaire

		index, error = TLAY.findGroupIndex(QGP.configActiveMapOsmGroupName)	
		groupRaster = TLAY.createGroup(QGP.configActiveRasterOsmGroupName, index-1 if index != None else 999)
		
#		Recharger le Raster

		crsRaster = QgsCoordinateReferenceSystem()
		crsRaster.createFromString('EPSG:3812')
		layer, errorText = TLAY.loadRaster(savingPath, fileName, QGP.configActiveRasterOsmGroupName, fileName, crsRaster, 100)
		if layer == None: self.mainFrame.setStatusWarning(errorText) ; return

		self.showRasterGroup()
		self.refreshExportOsmCombo()
		self.mainFrame.setStatusDone(fileName + ' - Rechargé dans groupe : ' + QGP.configActiveRasterOsmGroupName)


# ========================================================================================
# ========================================================================================
#
# Création des différents cadres Menu
# 
# ========================================================================================
# ========================================================================================


# ========================================================================================
# Cadre : Download Osm
# ========================================================================================

	def menuBoxOsmDownload(self):
	
		groupBoxOsmDownload = QtWidgets.QGroupBox('OSM - Téléchargement et Création des Couches', self.mainMenu)
		groupBoxOsmDownload.setStyleSheet(DSTY.styleBox)
		
#	Bouton Download

		self.buttonDownload = TBUT.createActionButton(groupBoxOsmDownload, 1, 1, 'Télécharger', 'Normal')
		self.buttonDownload.clicked.connect(self.buttonDownload_clicked)

#	Nom du dernier fichier	

		self.downloadListCombo = TBUT.createComboButton(groupBoxOsmDownload, 2, 1, 'Double')
		
#	Bouton Créer
	
		self.buttonCreateLayers = TBUT.createActionButton(groupBoxOsmDownload, 4, 1, 'Créer Couches', 'Normal')
		self.buttonCreateLayers.clicked.connect(self.buttonCreateLayers_clicked)

# 	Terminé

		groupBoxOsmDownload.repaint()

		return groupBoxOsmDownload


# ========================================================================================
# Cadre : Affichage et Styles
# ========================================================================================

	def menuBoxOsmDisplayLayers(self):
	
		groupBoxOsmDisplay = QtWidgets.QGroupBox('OSM - Affichage et Styles', self.mainMenu)
		groupBoxOsmDisplay.setStyleSheet(DSTY.styleBox)
		
#	Echelles

		TBUT.createLabelBlackButton(groupBoxOsmDisplay, 1, 1, 'Echelle (K)', 'Normal', 'Normal')
		
		button5000 = TBUT.createRadioBoxButton(groupBoxOsmDisplay, 5, 1, '5', 'ShortHalf')
		button10000 = TBUT.createRadioBoxButton(groupBoxOsmDisplay, 6, 1, '10', 'ShortHalf')
		button20000 = TBUT.createRadioBoxButton(groupBoxOsmDisplay, 7, 1, '20', 'ShortHalf')
		button50000 = TBUT.createRadioBoxButton(groupBoxOsmDisplay, 8, 1, '50', 'ShortHalf')
	
		button5000.clicked.connect(self.buttonScaleAny_clicked(self.iface, self, 5000))
		button10000.clicked.connect(self.buttonScaleAny_clicked(self.iface, self, 10000))
		button20000.clicked.connect(self.buttonScaleAny_clicked(self.iface, self, 20000))
		button50000.clicked.connect(self.buttonScaleAny_clicked(self.iface, self, 50000))
		
#	Courbes de niveau		
		
		self.buttonAddCDNLayers = TBUT.createActionButton(groupBoxOsmDisplay, 4, 1, 'C. de Niveau', 'Normal')
		self.buttonAddCDNLayers.clicked.connect(self.buttonAddCDNLayers_clicked)
		
#	Style

		TBUT.createLabelBlackButton(groupBoxOsmDisplay, 1, 2, 'Styles', 'Normal', 'Normal')
		
		self.styleListCombo = TBUT.createComboButton(groupBoxOsmDisplay, 2, 2, 'Normal')		
		self.styleListCombo.setEditable(True)

		self.buttonReloadStyles = TBUT.createActionButton(groupBoxOsmDisplay, 3, 2, 'Appliquer', 'Normal')
		self.buttonReloadStyles.clicked.connect(self.buttonReloadStyles_clicked)
			
		self.buttonRecordStyles = TBUT.createActionButton(groupBoxOsmDisplay, 4, 2, 'Enregistrer', 'Normal')
		DSTY.setStyleMainButtonsInactive(self.buttonRecordStyles)
		self.buttonRecordStyles.setContextMenuPolicy(Qt.CustomContextMenu)
		self.buttonRecordStyles.customContextMenuRequested.connect(self.buttonRecordStyles_rightClicked)
		self.buttonRecordStyles.clicked.connect(self.buttonRecordStyles_clicked)

#	Couches

		TBUT.createLabelBlackButton(groupBoxOsmDisplay, 1, 3, 'Couches', 'Normal', 'Normal')
		
		self.buttonReorderLayers = TBUT.createActionButton(groupBoxOsmDisplay, 2, 3, 'Trier', 'Normal')
		self.buttonReorderLayers.clicked.connect(self.buttonReorderLayers_clicked)
		
		self.buttonSetLayersVisible = TBUT.createActionButton(groupBoxOsmDisplay, 3, 3, 'Visibles', 'Normal')
		self.buttonSetLayersVisible.clicked.connect(self.buttonSetLayersVisible_clicked)
		
		self.buttonSetLayersHidden = TBUT.createActionButton(groupBoxOsmDisplay, 4, 3, 'Cachés', 'Normal')
		self.buttonSetLayersHidden.clicked.connect(self.buttonSetLayersHidden_clicked)

# 	Terminé

		groupBoxOsmDisplay.repaint()

		return groupBoxOsmDisplay
		
		
# ========================================================================================
# Cadre : Couches
# ========================================================================================

	def menuBoxOsmLayers(self):
	
		groupBoxOsmLayers = QtWidgets.QGroupBox('OSM - Couches', self.mainMenu)
		groupBoxOsmLayers.setStyleSheet(DSTY.styleBox)
		
#	Canevas 

		TBUT.createLabelBlackButton(groupBoxOsmLayers, 1, 1, 'Canevas', 'Normal', 'Normal')
		
		self.canevasOsmPointsInfo = TBUT.createLabelGreenButton(groupBoxOsmLayers, 2, 1, '. . .', 'Normal', 'Normal')
		self.canevasOsmLinesInfo = TBUT.createLabelGreenButton(groupBoxOsmLayers, 3, 1, '. . .', 'Normal', 'Normal')
		self.canevasOsmAreasInfo = TBUT.createLabelGreenButton(groupBoxOsmLayers, 4, 1, '. . .', 'Normal', 'Normal')
		
#	Couches
		
		TBUT.createLabelBlackButton(groupBoxOsmLayers, 1, 2, 'Couches', 'Normal', 'Normal')

		self.buttonSaveLayers = TBUT.createActionButton(groupBoxOsmLayers, 2, 2, 'Enregistrer', 'Normal')
		self.buttonSaveLayers.clicked.connect(self.buttonSaveLayers_clicked)
		
		self.buttonClearLayers = TBUT.createActionButton(groupBoxOsmLayers, 4, 2, 'Supprimer', 'Normal')
		self.buttonClearLayers.clicked.connect(self.buttonClearLayers_clicked)
		
		self.savedFolderListCombo = TBUT.createComboButton(groupBoxOsmLayers, 2, 3, 'Double')		
	
		self.buttonLoadLayers = TBUT.createActionButton(groupBoxOsmLayers, 4, 3, 'Charger', 'Normal')
		self.buttonLoadLayers.clicked.connect(self.buttonLoadLayers_clicked)
	
#	Aide

		buttonHelpFiche = TBUT.createHelpButton(groupBoxOsmLayers, 1, 3, 'Aide Osm', 'Normal')
		buttonHelpFiche.clicked.connect(lambda x : webbrowser.open_new_tab(QGP.configMenuHelpBasePath + 'QCarto - Carte Active - Osm.html'))
	
# 	Terminé

		groupBoxOsmLayers.repaint()

		return groupBoxOsmLayers
		
		
# ========================================================================================
# Cadre : Export
# ========================================================================================

	def menuBoxOsmExport(self):
	
		groupBoxOsmExport = QtWidgets.QGroupBox('OSM - Export', self.mainMenu)
		groupBoxOsmExport.setStyleSheet(DSTY.styleBox)
		
#	Bouton Export

		self.buttonExport = TBUT.createActionButton(groupBoxOsmExport, 1, 1, 'Exporter', 'Normal')
		self.buttonExport.clicked.connect(self.buttonExport_clicked)
		self.buttonExport.setContextMenuPolicy(Qt.CustomContextMenu)
		self.buttonExport.customContextMenuRequested.connect(self.buttonExport_rightClicked)


#	Nom du dernier fichier	

		self.exportListCombo = TBUT.createComboButton(groupBoxOsmExport, 2, 1, 'Double')
		
#	Bouton Recharger
	
		self.buttonLoadExport = TBUT.createActionButton(groupBoxOsmExport, 4, 1, 'Recharger', 'Normal')
		self.buttonLoadExport.clicked.connect(self.buttonLoadExport_clicked)
	
# 	Terminé

		groupBoxOsmExport.repaint()

		return groupBoxOsmExport	
		
		
		
# ========================================================================================
# --- THE END ---
# ========================================================================================
	