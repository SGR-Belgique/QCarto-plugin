# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Gestion des Menus : Page Carte Active
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
import ast
import math

import QCarto_Layers_Tracks as LTRK
import QCarto_Layers_ActiveMap as LMAP
importlib.reload(LMAP)

import QCarto_Tools_QParam as TQCP
importlib.reload(TQCP)
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

import QCarto_Process_Export as SEXP
importlib.reload(SEXP)

import QCarto_Menu_EditTopo50 as P50K
importlib.reload(P50K)
import QCarto_Menu_ActiveMap_SubMenu_Osm as MOSM
importlib.reload(MOSM)


import QCarto_Parameters_Global
QGP = QCarto_Parameters_Global.globalParameters()


# ========================================================================================
# Class : menuActiveMapFrame
# >>> iface
# >>> mainMenu 						: Widget of Main Menu
# >>> mainFrame 					: Main Menu Object
# ========================================================================================

class menuActiveMapFrame:

	def __init__(self, iface, mainMenu, mainFrame):

# 	Paramètres fournis

		self.iface = iface
		self.mainMenu = mainMenu
		self.mainFrame = mainFrame

#	Nom de la page

		self.pageName = 'Carte Active'

#	Accès aux Tables de la DB Carto

		self.layerTracksGR, 	self.layerTracksGRerror 	= self.mainFrame.layerTracksGR, 	self.mainFrame.layerTracksGRerror 	
		self.layerTracksRB, 	self.layerTracksRBerror 	= self.mainFrame.layerTracksRB, 	self.mainFrame.layerTracksRBerror 	
		self.layerSectionsGR, 	self.layerSectionsGRerror 	= self.mainFrame.layerSectionsGR, 	self.mainFrame.layerSectionsGRerror 	
		self.layerPointsGR, 	self.layerPointsGRError 	= self.mainFrame.layerPointsGR, 	self.mainFrame.layerPointsGRError 	
		self.layerPOIs, 		self.layerPOIsError 		= self.mainFrame.layerPOIs, 		self.mainFrame.layerPOIsError 	
		self.layerCommunes, 	self.layerCommunesError		= self.mainFrame.layerCommunes, 	self.mainFrame.layerCommunesError		
		self.layer50KEd4, 		self.layer50Kerror 			= TLAY.openLayer(QGP.tableNameSectionsGREd4)
		
#	Couches des Décorations

		self.layerMapNumber, 		self.layerMapNumberError		= TLAY.openLayer(QGP.configShapeMapDecorationNumber)
		self.layerMapCopyright, 	self.layerMapCopyrightError		= TLAY.openLayer(QGP.configShapeMapDecorationCopyright)
		self.layerMapWhiteFrame, 	self.layerMapWhiteFrameError	= TLAY.openLayer(QGP.configShapeMapDecorationWhiteFrame)

#	Listes des Itinéraires

		self.listTracksGRCodes  = LTRK.getOrderedListItineraryGR({'GR'},  self.mainFrame.dicoTracksGRFeatures)
		self.listTracksGRPCodes = LTRK.getOrderedListItineraryGR({'GRP'}, self.mainFrame.dicoTracksGRFeatures)
		self.listTracksGRTCodes = LTRK.getOrderedListItineraryGR({'GRT'}, self.mainFrame.dicoTracksGRFeatures)
		self.listTracksRLCodes  = LTRK.getOrderedListItineraryRB({'RL'}, self.mainFrame.dicoTracksRBFeatures)
		self.listTracksRBCodes  = LTRK.getOrderedListItineraryRB({'RB'}, self.mainFrame.dicoTracksRBFeatures)
		self.listTracksRFCodes  = LTRK.getOrderedListItineraryRB({'RF'}, self.mainFrame.dicoTracksRBFeatures)
		self.listTracksIRCodes  = LTRK.getOrderedListItineraryRB({'IR'}, self.mainFrame.dicoTracksRBFeatures)

#	Variables globales de la classe

		self.activeMapFeature = None
		self.quitOnLayerMapsChange = True		
		self.modificationsCheckBoxConnected = True
		self.imagePath = None
		
		self.configZoomMapScale = int(TQCP.retrieveQCartoParameter(self.mainFrame, 'USER', self.mainFrame.userFullName, 'ZoomCarte', 50000))
		
# 	Création des sous-menus

		self.boxesList = []
		self.createMenuBoxes()

		self.mainFrame.setStatusDone('Page des ' + self.pageName + ' créée !')
		
	def createMenuBoxes(self):

		self.groupBoxMapInfo = self.menuBoxMapInfo()
		DSTY.setBoxGeometry(self.groupBoxMapInfo, 1, 4, 8, 3)
		self.boxesList.append(self.groupBoxMapInfo)

		self.groupBoxCarteDecorations = self.menuBoxCarteDecorations()
		DSTY.setBoxGeometry(self.groupBoxCarteDecorations, 1, 8, 4, 2)
		self.boxesList.append(self.groupBoxCarteDecorations)

		self.groupBoxCarteDecorationsCopyright = self.menuBoxCarteDecorationsCopyright()
		DSTY.setBoxGeometry(self.groupBoxCarteDecorationsCopyright, 1, 8, 4, 1)
		self.boxesList.append(self.groupBoxCarteDecorationsCopyright)

		self.groupBoxCarteDecorationsName = self.menuBoxCarteDecorationsName()
		DSTY.setBoxGeometry(self.groupBoxCarteDecorationsName, 1, 9, 4, 1)
		self.boxesList.append(self.groupBoxCarteDecorationsName)

		self.groupBoxCarteModifications = self.menuBoxCarteModifications()
		DSTY.setBoxGeometry(self.groupBoxCarteModifications, 1, 11, 4, 2)
		self.boxesList.append(self.groupBoxCarteModifications)

		self.groupBoxCartePoints = self.menuBoxCartePoints()
		DSTY.setBoxGeometry(self.groupBoxCartePoints, 1, 14, 4, 3)
		self.boxesList.append(self.groupBoxCartePoints)

		self.groupBoxCarteLabels = self.menuBoxCarteLabels()
		DSTY.setBoxGeometry(self.groupBoxCarteLabels, 1, 18, 4, 1)
		self.boxesList.append(self.groupBoxCarteLabels)

		self.groupBoxCarteBackground = self.menuBoxCarteBackground()
		DSTY.setBoxGeometry(self.groupBoxCarteBackground, 1, 20, 4, 2)
		self.boxesList.append(self.groupBoxCarteBackground)

		self.groupBoxCarteSections = self.menuBoxCarteSections()
		DSTY.setBoxGeometry(self.groupBoxCarteSections, 1, 23, 4, 4)
		self.boxesList.append(self.groupBoxCarteSections)

		self.groupBoxCarteExport = self.menuBoxCarteExport()
		DSTY.setBoxGeometry(self.groupBoxCarteExport, 5, 20, 4, 7)
		self.boxesList.append(self.groupBoxCarteExport)

		self.groupBoxOsm = MOSM.subMenuActiveMapFrameOsm(self.iface, self.mainMenu, self.mainFrame, self, 5, 8)
		self.boxesList.append(self.groupBoxOsm)



# ========================================================================================
# Actions : A la demande de la fenêtre principale
# ========================================================================================

#	Show - Ouverture de cette fenêtre

	def show(self):
		for box in self.boxesList: box.show(), box.repaint()
		self.initializeActiveMap()
		self.connectMapsLayer()
		self.connectActiveMapLayers()
		
#	Hide - Ouverture d'une autre fenêtre

	def hide(self):
		for box in self.boxesList: box.hide()
		self.disconnectMapsLayer()
		self.disconnectActiveMapLayers()

#	Close - Fermeture définitive

	def close(self):
		self.hide()
		for box in self.boxesList: del box

#	Help on this page

	def help(self):
		webbrowser.open_new_tab(QGP.configMenuHelpBasePath + 'QCarto - Page - ' + self.pageName + '.html')
	

# ========================================================================================
# Connections au shape des emprises
# ========================================================================================
	
	def connectMapsLayer(self):
		if self.mainFrame.layerMaps == None: return
		self.mainFrame.layerMaps.featureAdded.connect(self.mapsShapeChangedExternally)
		self.mainFrame.layerMaps.featureDeleted.connect(self.mapsShapeChangedExternally)
		self.mainFrame.layerMaps.geometryChanged.connect(self.mapsShapeChangedExternally)
		self.mainFrame.layerMaps.attributeValueChanged.connect(self.mapsShapeChangedExternally)
		
	def disconnectMapsLayer(self):
		if self.mainFrame.layerMaps == None: return
		try:	
			self.mainFrame.layerMaps.featureAdded.disconnect(self.mapsShapeChangedExternally)
			self.mainFrame.layerMaps.featureDeleted.disconnect(self.mapsShapeChangedExternally)
			self.mainFrame.layerMaps.geometryChanged.disconnect(self.mapsShapeChangedExternally)
			self.mainFrame.layerMaps.attributeValueChanged.disconnect(self.mapsShapeChangedExternally)
		except:
			pass
	
	def mapsShapeChangedExternally(self):
		if self.mainFrame.layerMaps == None: return
		if not self.quitOnLayerMapsChange: return
		self.mainFrame.setStatusWarning('Le shape des emprises a été modifié - cette page n\'est plus valable !')
		TDAT.sleep(1000)
		self.mainFrame.selectedMapFeature = None
		self.mainFrame.requestPage('Cartes')


# ========================================================================================
# Connections au shapes de la carte active
# ========================================================================================

	def connectActiveMapLayers(self):
		if self.mainFrame.layerActiveMapPoints == None: return
		self.mainFrame.layerActiveMapPoints.featureAdded.connect(self.initializeActiveMapExportPoints)
		self.mainFrame.layerActiveMapPoints.featureDeleted.connect(self.initializeActiveMapExportPoints)
		self.mainFrame.layerActiveMapLabels.featureAdded.connect(self.initializeActiveMapExportLabels)
		self.mainFrame.layerActiveMapLabels.featureDeleted.connect(self.initializeActiveMapExportLabels)
		self.mainFrame.layerActiveMapLabelsSimple.featureAdded.connect(self.initializeActiveMapExportLabels)
		self.mainFrame.layerActiveMapLabelsSimple.featureDeleted.connect(self.initializeActiveMapExportLabels)

	def disconnectActiveMapLayers(self):
		if self.mainFrame.layerActiveMapPoints == None: return
		try:
			self.mainFrame.layerActiveMapPoints.featureAdded.disconnect(self.initializeActiveMapExportPoints)
			self.mainFrame.layerActiveMapPoints.featureDeleted.disconnect(self.initializeActiveMapExportPoints)
			self.mainFrame.layerActiveMapLabels.featureAdded.disconnect(self.initializeActiveMapExportLabels)
			self.mainFrame.layerActiveMapLabels.featureDeleted.disconnect(self.initializeActiveMapExportLabels)
			self.mainFrame.layerActiveMapLabelsSimple.featureAdded.disconnect(self.initializeActiveMapExportLabels)
			self.mainFrame.layerActiveMapLabelsSimple.featureDeleted.disconnect(self.initializeActiveMapExportLabels)
		except:
			pass


# ========================================================================================
# Actions : Paramères Cartes
# ========================================================================================

	def buttonActiveMapZoom_clicked(self):
		self.iface.mapCanvas().setExtent(self.mainFrame.selectedMapFeature.geometry().boundingBox())
		self.iface.mapCanvas().zoomScale(min(self.configZoomMapScale, self.activeMapScale))


# ========================================================================================
# Actions : Décorations
# ========================================================================================

	def decorationPositionChanged(self, type, position):
	
		self.quitOnLayerMapsChange = False											# Avoid automatical quit when changing layer Map	

		self.mainFrame.layerMaps.startEditing()
		if type == 'Nom' : self.mainFrame.layerMaps.changeAttributeValue(self.activeMapFeature.id(), self.activeMapFeature.fieldNameIndex(QGP.tableFramesFieldNumber), position)
		if type == 'Copyright' : self.mainFrame.layerMaps.changeAttributeValue(self.activeMapFeature.id(), self.activeMapFeature.fieldNameIndex(QGP.tableFramesFieldCopyright), position)
		self.mainFrame.layerMaps.commitChanges()
	
		if type == 'Nom' : 
			if not self.changeDecorationNumberPosition(position): return
		if type == 'Copyright' : 
			if not self.changeDecorationCopyrightPosition(position): return
	
		self.quitOnLayerMapsChange = True
		self.mainFrame.setStatusDone('Position du ' + type + ' de la carte : ' + position)


	def changeDecorationCopyrightPosition(self, position, definitively = True):
		if self.layerMapCopyright == None :
			self.mainFrame.setStatusError('La couche des copyright de carte n\'est pas sur le canevas ?', False)
			return False
		if self.activeMapScale == None:
			self.mainFrame.setStatusWarning('L\'échelle de la carte n\'est pas définie !')
			return False
		if position == None: return False

		mapNumberX, mapNumberY = self.getDecorationPosition('Copyright', position)

		self.layerMapCopyright.startEditing()
		
		copyrightType = QGP.exportActiveMapCopyrightDico[self.activeMapFeature[QGP.tableFramesFieldBackground]] if self.activeMapFeature[QGP.tableFramesFieldBackground] in QGP.exportActiveMapCopyrightDico else '-?-'
		if definitively: self.layerMapCopyright.changeAttributeValue(0, self.layerMapCopyright.fields().indexOf(QGP.tableDecorationFieldType), copyrightType)
		if definitively: self.layerMapCopyright.changeAttributeValue(0, self.layerMapCopyright.fields().indexOf(QGP.tableDecorationFieldScale), self.activeMapScale)
		self.layerMapCopyright.changeGeometry(0, QgsGeometry.fromPointXY(QgsPointXY(mapNumberX, mapNumberY)))
		if definitively: self.layerMapCopyright.commitChanges()

		return True


	def changeDecorationNumberPosition(self, position, definitively = True):
		if self.layerMapNumber == None :
			self.mainFrame.setStatusError('La couche des numéros de carte n\'est pas sur le canevas ?', False)
			return False
		if self.activeMapScale == None:
			self.mainFrame.setStatusWarning('L\'échelle de la carte n\'est pas définie !')
			return False
		if position == None: return False
		
		mapNumberX, mapNumberY = self.getDecorationPosition('Nom', position)

		self.layerMapNumber.startEditing()
		if definitively: self.layerMapNumber.changeAttributeValue(0, self.layerMapNumber.fields().indexOf(QGP.tableDecorationFieldType), 'Topo-brun' if position != 'Sans' else 'Sans')
		if definitively: self.layerMapNumber.changeAttributeValue(0, self.layerMapNumber.fields().indexOf(QGP.tableDecorationFieldScale), self.activeMapScale)
		if definitively: self.layerMapNumber.changeAttributeValue(0, self.layerMapNumber.fields().indexOf(QGP.tableDecorationFieldText), self.activeMapName)
		self.layerMapNumber.changeGeometry(0, QgsGeometry.fromPointXY(QgsPointXY(mapNumberX, mapNumberY)))
		if definitively: self.layerMapNumber.commitChanges()

		return True
		

	def getDecorationPosition(self, type, position):
		mapRectangle = self.mainFrame.layerMaps.getFeature(self.activeMapFeature.id()).geometry().boundingBox()					# Must query layer ! Emprise is temporarily changed !
		mapLeft = mapRectangle.xMinimum()
		mapRight = mapRectangle.xMaximum()
		mapTop = mapRectangle.yMaximum()
		mapBottom = mapRectangle.yMinimum()

		if type == 'Nom':
			margin = QGP.mapDecorationNameMargin
			width = QGP.mapDecorationNameWidth if len(self.activeMapName) <= 10 else len(self.activeMapName) * QGP.mapDecorationNameWidthExtra
			height = QGP.mapDecorationNameHeight
		if type == 'Copyright':
			margin = QGP.mapDecorationCopyrightMargin
			width = QGP.mapDecorationCopyrightWidth
			height = QGP.mapDecorationCopyrightHeight
			
		if position == 'Gauche':
			mapNumberX = mapLeft + self.activeMapScale * (margin + width / 2) / 1000
		elif position == 'Centre':
			mapNumberX = (mapLeft + mapRight) / 2
		elif position == 'Droite':
			mapNumberX = mapRight - self.activeMapScale * (margin + width / 2) / 1000
		else:
			mapNumberX = 0
		if type == 'Nom':
			mapNumberY = mapBottom + self.activeMapScale * (margin + height / 2) / 1000
		if type == 'Copyright':
			mapNumberY = mapTop - self.activeMapScale * (margin + height / 2) / 1000
		
		if self.mainFrame.debugModeQCartoLevel > 1 : print ('getDecorationPosition - map Lef-Rig-Top-Bot : ' + str(mapLeft) + ' - ' + str(mapRight) + ' - ' + str(mapTop) + ' - ' + str(mapBottom))
		if self.mainFrame.debugModeQCartoLevel > 1 : print ('getDecorationPosition - mapNumber X Y : ' + str(mapNumberX) + ' - ' + str(mapNumberY))
		
		return mapNumberX, mapNumberY
	
		
# ========================================================================================
# Actions : Points Repères
# ========================================================================================

	def buttonPointsLoad_clicked(self):
	
		self.mainFrame.setStatusWorking('Définition des Repères Effectifs à partir des Repères Carte ...')
		self.mainFrame.layerActiveMapPoints.startEditing()
		self.mainFrame.layerActiveMapPoints.selectAll()
		self.mainFrame.layerActiveMapPoints.deleteSelectedFeatures()
		
		for pointGlobalFeature in self.activeMapPointsGlobalFeaturesList:
			self.addPointExportFeature(pointGlobalFeature)

		self.mainFrame.layerActiveMapPoints.commitChanges()
		DSYM.setRepereStyleVariables(self.mainFrame.layerActiveMapPoints, self.activeMapScale)
		self.initializeActiveMapExportPoints()
		self.mainFrame.setStatusDone('Définition des Repères Effectifs à partir des Repères Carte - OK')
		if self.activeMapItineraryType == 'RF':	self.poisLoad()
	
	def poisLoad(self):
	
		self.mainFrame.setStatusWorking('Définition des Pois Effectifs à partir de la DB Pois ...')
		self.mainFrame.layerActiveMapPoisRF.startEditing()
		self.mainFrame.layerActiveMapPoisRF.selectAll()
		self.mainFrame.layerActiveMapPoisRF.deleteSelectedFeatures()
		
		for poiGlobalFeature in self.activeMapPoisGlobalFeaturesList:
			self.addPoiExportFeature(poiGlobalFeature)

		self.mainFrame.layerActiveMapPoisRF.commitChanges()
		DSYM.setPoisRFStyleVariables(self.mainFrame.layerActiveMapPoisRF, self.activeMapScale)
		self.initializeActiveMapExportPois()
		self.mainFrame.setStatusDone('Définition des Repères et Pois RF Effectifs à partir des Repères et Pois Carte - OK')
	
	def buttonPointsReload_clicked(self):

		self.mainFrame.setStatusWorking('Rechargement des Repères Effectifs à partir des Repères Carte ...')
		self.initializeActiveMapGlobalPoints()
		self.mainFrame.layerActiveMapPoints.startEditing()
		
		for pointGlobalFeature in self.activeMapPointsGlobalFeaturesList:
			pointAlreadyExist = False
			for pointExportFeature in self.mainFrame.layerActiveMapPoints.getFeatures():
				if (pointExportFeature[QGP.tableMapPointsFieldId] == pointGlobalFeature[QGP.tableMapPointsFieldId]):	
					self.mainFrame.layerActiveMapPoints.changeAttributeValue(pointExportFeature.id(), pointExportFeature.fieldNameIndex(QGP.tableMapPointsFieldRepere), pointGlobalFeature[QGP.tablePointsFieldRepere])
					self.mainFrame.layerActiveMapPoints.changeAttributeValue(pointExportFeature.id(), pointExportFeature.fieldNameIndex(QGP.tableMapPointsFieldIdXRepere), pointGlobalFeature.geometry().asPoint().x())
					self.mainFrame.layerActiveMapPoints.changeAttributeValue(pointExportFeature.id(), pointExportFeature.fieldNameIndex(QGP.tableMapPointsFieldIdYRepere), pointGlobalFeature.geometry().asPoint().y())
					self.mainFrame.layerActiveMapPoints.changeAttributeValue(pointExportFeature.id(), pointExportFeature.fieldNameIndex(QGP.tableMapPointsFieldTexte), pointGlobalFeature[QGP.tablePointsFieldNom])
					self.mainFrame.layerActiveMapPoints.changeAttributeValue(pointExportFeature.id(), pointExportFeature.fieldNameIndex(QGP.tableMapPointsFieldCouleur), DSYM.getPointColor(pointGlobalFeature[QGP.tablePublicPointFieldCode]))
					pointAlreadyExist = True
					break
			if not pointAlreadyExist:
				self.addPointExportFeature(pointGlobalFeature)			

		self.mainFrame.layerActiveMapPoints.commitChanges()
		DSYM.setRepereStyleVariables(self.mainFrame.layerActiveMapPoints, self.activeMapScale)
		self.initializeActiveMapExportPoints()
		self.mainFrame.setStatusDone('Rechargement des Repères Effectifs à partir des Repères Carte - OK')
		if self.activeMapItineraryType == 'RF':	self.poisReload()
	
	def poisReload(self):	

		self.mainFrame.setStatusWorking('Rechargement des Pois Effectifs à partir de la DB Pois ...')
		self.mainFrame.layerActiveMapPoisRF.startEditing()
		
		for poiGlobalFeature in self.activeMapPoisGlobalFeaturesList :
			poiAlreadyExist = False
			for poiExportFeature in self.mainFrame.layerActiveMapPoisRF.getFeatures() :
				if (poiExportFeature[QGP.tableMapPoiRFFieldId] == poiGlobalFeature[QGP.poisTableFieldIdPOI]):	
					self.mainFrame.layerActiveMapPoisRF.changeAttributeValue(poiExportFeature.id(), poiExportFeature.fieldNameIndex(QGP.tableMapPoiRFFieldPoint), str(poiGlobalFeature[QGP.poisTableFieldTracks]).split('-')[-1])
					poiAlreadyExist = True
					break
			if not poiAlreadyExist:
				self.addPoiExportFeature(poiGlobalFeature)			

		self.mainFrame.layerActiveMapPoisRF.commitChanges()
		DSYM.setPoisRFStyleVariables(self.mainFrame.layerActiveMapPoisRF, self.activeMapScale)
		self.initializeActiveMapExportPois()
		self.mainFrame.setStatusDone('Rechargement des Repères et Pois RF Effectifs à partir des Repères et Pois Carte - OK')
	
	def addPointExportFeature(self, pointGlobalFeature):
		pointExportFeature = QgsFeature()
		pointExportFeature.setFields(self.mainFrame.layerActiveMapPoints.fields())
		pointExportFeature.setAttribute(QGP.tableMapPointsFieldId, pointGlobalFeature[QGP.tablePointsFieldId])
		pointExportFeature.setAttribute(QGP.tableMapPointsFieldRepere, pointGlobalFeature[QGP.tablePointsFieldRepere])
		pointExportFeature.setAttribute(QGP.tableMapPointsFieldIdXRepere, pointGlobalFeature.geometry().asPoint().x())
		pointExportFeature.setAttribute(QGP.tableMapPointsFieldIdYRepere, pointGlobalFeature.geometry().asPoint().y())
		pointExportFeature.setAttribute(QGP.tableMapPointsFieldTexte, pointGlobalFeature[QGP.tablePointsFieldNom])
		pointExportFeature.setAttribute(QGP.tableMapPointsFieldCouleur, DSYM.getPointColor(pointGlobalFeature[QGP.tablePublicPointFieldCode]))

		pointGlobalPoint = pointGlobalFeature.geometry().asPoint()
		pointExportGeometry = QgsGeometry().fromPointXY(QgsPointXY(pointGlobalPoint.x() + QGP.tableMapPointsDistanceBouleX, pointGlobalPoint.y() + QGP.tableMapPointsDistanceBouleY))

		pointExportFeature.setGeometry(pointExportGeometry)
		self.mainFrame.layerActiveMapPoints.addFeature(pointExportFeature)

	def addPoiExportFeature(self, poiGlobalFeature):
		poiExportFeature = QgsFeature()
		poiExportFeature.setFields(self.mainFrame.layerActiveMapPoisRF.fields())
		poiExportFeature.setAttribute(QGP.tableMapPoiRFFieldId, poiGlobalFeature[QGP.poisTableFieldIdPOI])
		poiExportFeature.setAttribute(QGP.tableMapPoiRFFieldPoint, str(poiGlobalFeature[QGP.poisTableFieldTracks]).split('-')[-1])

		poiExactPoint = poiGlobalFeature.geometry().asPoint()
		poiMapPoint = QgsPointXY(poiExactPoint.x() + QGP.tableMapPoisDistanceBouleX, poiExactPoint.y() + QGP.tableMapPoisDistanceBouleY)
		poiExportGeometry = QgsGeometry.fromMultiPolylineXY([[poiExactPoint,poiMapPoint]])
		poiExportFeature.setGeometry(poiExportGeometry)
		self.mainFrame.layerActiveMapPoisRF.addFeature(poiExportFeature)
		
	
# ========================================================================================
# Actions : Modifications
# ========================================================================================

	def modificationCheckChanged(self):
		if not self.modificationsCheckBoxConnected : return

		self.modificationsLists = [[],[]]
		if self.includeModifsTemporaryMainOption.isChecked() : self.modificationsLists[0].append('T')
		if self.includeModifsFuturesMainOption.isChecked() : self.modificationsLists[0].append('F')
		if self.includeModifsTemporaryOtherOption.isChecked() : self.modificationsLists[1].append('T')
		if self.includeModifsFuturesOtherOption.isChecked() : self.modificationsLists[1].append('F')

		self.quitOnLayerMapsChange = False													# Avoid automatical quit when changing layer Map	
		self.mainFrame.layerMaps.startEditing()
		self.mainFrame.layerMaps.changeAttributeValue(self.activeMapFeature.id(), self.activeMapFeature.fieldNameIndex(QGP.tableFramesFieldModifications), str(self.modificationsLists))
		self.mainFrame.layerMaps.commitChanges()
		self.quitOnLayerMapsChange = True													# Avoid automatical quit when changing layer Map	

		self.initializeActiveMapGlobalPoints()												# Need to be refresh since depends on modifications selected
		self.activeMapFeature = self.mainFrame.layerMaps.getFeature(self.activeMapFeature.id())
		self.mainFrame.setStatusDone('Prise en compte des modifications pour la génération carte : ' + str(self.modificationsLists))


	def buttonHelpModifications_clicked(self):
		webbrowser.open_new_tab(QGP.configMenuHelpBasePath + 'QCarto - Carte Active - Définitions - Repères.html')


# ========================================================================================
# Actions : Fond Topo
# ========================================================================================

	def backgroundComboChanged(self):
		self.quitOnLayerMapsChange = False													# Avoid automatical quit when changing layer Map	
		self.mainFrame.layerMaps.startEditing()
		self.mainFrame.layerMaps.changeAttributeValue(self.activeMapFeature.id(), self.activeMapFeature.fieldNameIndex(QGP.tableFramesFieldBackground), self.activeMapBackgroundCombo.currentText())
		self.mainFrame.layerMaps.commitChanges()
		self.quitOnLayerMapsChange = True													# Avoid automatical quit when changing layer Map	

		self.activeMapFeature = self.mainFrame.layerMaps.getFeature(self.activeMapFeature.id())
		self.initializeActiveMapExportBackground()
		
		self.activeMapExportBackgroundCombo.setCurrentText(self.activeMapBackgroundCombo.currentText())
		self.activeMapExportBackgroundInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%',self.activeMapBackgroundCombo.currentText()))
		DSTY.setStyleOkLabel(self.activeMapExportBackgroundInfo, 'Normal')	

		self.mainFrame.setStatusDone('Fond topographique pour la génération carte : ' + self.activeMapBackgroundCombo.currentText())


# ========================================================================================
# Actions : Sections
# ========================================================================================

	def buttonSectionsLoad_clicked(self):

		self.mainFrame.setStatusWorking('Analyse des tronçons ...')

#		Déterminer les sections sur le parcours principal et celles sur les autres GR	

		self.initializeActiveMapGlobalSections()
		self.itinerarySectionFeaturesList, self.otherSectionFeaturesList = LMAP.getActiveMapEffectiveSectionsFeatures(self.activeMapItinerary, self.activeMapSectionsGlobalFeaturesList, self.modificationsLists)

		sectionsText = '  {:0d} + {:0d} tronçons'.format(len(self.itinerarySectionFeaturesList), len(self.otherSectionFeaturesList))
		self.activeMapSectionsUsedInfo.setText(DSTY.textFormatBlackNormalLeft.replace('%TEXT%',sectionsText))
		DSTY.setStyleOkLabel(self.activeMapSectionsUsedInfo, 'Normal')	

#		Déterminer l'état du balisage - Dictionnaire : sectionId : Marked-Flag

		dicoSectionsMarked = { feature.id() : DSYM.isSectionFeatureMarked(self.mainFrame, feature) for feature in self.activeMapSectionsGlobalFeaturesList }
		if self.mainFrame.debugModeQCartoLevel > 0 : print ('Marked : ' + str([str(feature.id()) + ' : ' + str(dicoSectionsMarked[feature.id()]) for feature in self.activeMapSectionsGlobalFeaturesList]))

#		Déterminer les types de parcours 

		dicoItinerarySectionsType = { feature.id() : LMAP.getSectionFeatureType(feature, self.activeMapItinerary) for feature in self.itinerarySectionFeaturesList }
		dicoOtherSectionsType = { feature.id() : LMAP.getSectionFeatureType(feature, None) for feature in self.otherSectionFeaturesList }
		if self.mainFrame.debugModeQCartoLevel > 0 : print ('Itinerary Types : ' + str([str(feature.id()) + ' : ' + str(dicoItinerarySectionsType[feature.id()]) for feature in self.itinerarySectionFeaturesList]))
		if self.mainFrame.debugModeQCartoLevel > 0 : print ('Others GR Types : ' + str([str(feature.id()) + ' : ' + str(dicoOtherSectionsType[feature.id()]) for feature in self.otherSectionFeaturesList]))

#		Déterminer la symbologie

		if self.activeMapSymbologyCombo.currentText() == 'Automatique' :
			if self.activeMapItineraryType in QGP.typeSetModeGR :
				dicoName = 'GR-Standard'
			elif self.activeMapItineraryType == 'RF' :
				dicoName = 'RF-Standard'
			else :
				dicoName = 'RB-Standard'
		else :
			dicoName = self.activeMapSymbologyCombo.currentText()
		
		dicoItinerarySectionsSymbol = { feature.id() : DSYM.getSectionSymbol(dicoName, True, dicoItinerarySectionsType[feature.id()], dicoSectionsMarked[feature.id()]) for feature in self.itinerarySectionFeaturesList }
		dicoOtherSectionsSymbol = { feature.id() : DSYM.getSectionSymbol(dicoName, False, dicoOtherSectionsType[feature.id()], dicoSectionsMarked[feature.id()]) for feature in self.otherSectionFeaturesList }
		if self.mainFrame.debugModeQCartoLevel > 0 : print ('Itinerary Symbols : ' + str([str(feature.id()) + ' : ' + str(dicoItinerarySectionsSymbol[feature.id()]) for feature in self.itinerarySectionFeaturesList]))
		if self.mainFrame.debugModeQCartoLevel > 0 : print ('Others GR Symbols : ' + str([str(feature.id()) + ' : ' + str(dicoOtherSectionsSymbol[feature.id()]) for feature in self.otherSectionFeaturesList]))

		DSYM.setSectionStyleVariables(self.mainFrame.layerActiveMapSections, self.activeMapScale)

#		Définir la couche

		self.mainFrame.setStatusWorking('Chargement des Tronçons avec leur symbologie ...')
		
		self.mainFrame.layerActiveMapSections.startEditing()
		self.mainFrame.layerActiveMapSections.selectAll()
		self.mainFrame.layerActiveMapSections.deleteSelectedFeatures()

		for sectionFeature in self.itinerarySectionFeaturesList:
			sectionExportFeature = QgsFeature()
			sectionExportFeature.setFields(self.mainFrame.layerActiveMapSections.fields())
			sectionExportFeature.setAttribute(QGP.tableMapSectionsFieldType, dicoItinerarySectionsType[sectionFeature.id()])
			sectionExportFeature.setAttribute(QGP.tableMapSectionsFieldState, 'TBC ...')
			sectionExportFeature.setAttribute(QGP.tableMapSectionsFieldSymbol, dicoItinerarySectionsSymbol[sectionFeature.id()])
			sectionExportFeature.setAttribute(QGP.tableMapSectionsFieldSections, str(sectionFeature.id()))
			sectionExportFeature.setGeometry(sectionFeature.geometry())
			self.mainFrame.layerActiveMapSections.addFeature(sectionExportFeature)

		for sectionFeature in self.otherSectionFeaturesList:
			sectionExportFeature = QgsFeature()
			sectionExportFeature.setFields(self.mainFrame.layerActiveMapSections.fields())
			sectionExportFeature.setAttribute(QGP.tableMapSectionsFieldType, dicoOtherSectionsType[sectionFeature.id()])
			sectionExportFeature.setAttribute(QGP.tableMapSectionsFieldState, 'TBC ...')
			sectionExportFeature.setAttribute(QGP.tableMapSectionsFieldSymbol, dicoOtherSectionsSymbol[sectionFeature.id()])
			sectionExportFeature.setAttribute(QGP.tableMapSectionsFieldSections, str(sectionFeature.id()))
			sectionExportFeature.setGeometry(sectionFeature.geometry())
			self.mainFrame.layerActiveMapSections.addFeature(sectionExportFeature)

		self.mainFrame.layerActiveMapSections.commitChanges()
		
#		Remplacer les Tronçons disponibles sur IGN Edition 4	

		self.mainFrame.setStatusWorking('Remplacement de la géométrie des Tronçons sur IGN Edition 4 ...')
		if self.activeMapBackground == QGP.exportBackgroundIGN50Ed4 : 
			countSubstitue = LMAP.substituteActiveMapSections(self.mainFrame.layerActiveMapSections, self.layer50KEd4)
		else :
			countSubstitue = 0
		
		sectionsText = '  {:0d} tronçons'.format(countSubstitue)
		self.activeMapSectionsSustituedInfo.setText(DSTY.textFormatBlackNormalLeft.replace('%TEXT%',sectionsText))
		DSTY.setStyleOkLabel(self.activeMapSectionsSustituedInfo, 'Normal')			
		
#		Combiner la géométrie des tronçons à symbologie identique		
		
		self.mainFrame.setStatusWorking('Combinaison des Tronçons contigüs avec symbologie identique ...')
		LMAP.mergeActiveMapSections(self.mainFrame.layerActiveMapSections)
		
#		Raccourcir la géométrie des tronçons aux extrémités
		
		self.mainFrame.setStatusWorking('Raccourcissement des extrémités des tronçons ... ')
		LMAP.shortenActiveMapSections(self.mainFrame.layerActiveMapSections, QGP.activeMapLinesShortenDistance * self.activeMapScale / 1000)
		
#		Réorienter la géométrie des tronçons 
		
		self.mainFrame.setStatusWorking('Réorientation des tronçons ... ')
		LMAP.turnActiveMapSections(self.mainFrame.layerActiveMapSections)
		
		self.mainFrame.setStatusDone('Chargement des Tronçons avec leur symbologie - OK')


# ========================================================================================
# Actions : Edition de la couche Tronçons-GR-Ed4
# ========================================================================================

	def buttonEditIGN50V4_clicked(self):
		importlib.reload(P50K)
		self.mainFrame.dockMenuEditTopo50Ed4 = P50K.editTronconsIGN50V4(self.iface, self.mainMenu, self.mainFrame, self.mainFrame.dockMenuEditTopo50Ed4)
		self.mainFrame.dockMenuEditTopo50Ed4.show()
		self.mainMenu.hide()	
	

# ========================================================================================
# Actions : Styles
# ========================================================================================

#	Style Etiquettes

	def buttonLabelsMAJStyle_clicked(self):
		errorText, status = self.mainFrame.layerActiveMapLabels.loadNamedStyle(QGP.configPathActiveMap + QGP.configShapeMapLabels + '.qml')
		if not status:
			self.mainFrame.setStatusError(errorText, False)
			return

		self.mainFrame.setStatusWorking('Rechargement du Style par défaut des étiquettes ...')
		status, count = TFIL.copy_files(QGP.configPathActiveMap, self.activeMapFolder, QGP.configShapeMapLabels + '.qml')
		if not status:
			self.mainFrame.setStatusError('Fichier : ' + QGP.configPathActiveMap + QGP.configShapeMapLabels + '.qml' + ' : + Copie impossible ?', False)

		errorText, status = self.mainFrame.layerActiveMapLabelsSimple.loadNamedStyle(QGP.configPathActiveMap + QGP.configShapeMapLabelsSimple + '.qml')
		if not status:
			self.mainFrame.setStatusError(errorText, False)
			return

		self.mainFrame.setStatusWorking('Rechargement du Style par défaut des étiquettes simples ...')
		status, count = TFIL.copy_files(QGP.configPathActiveMap, self.activeMapFolder, QGP.configShapeMapLabelsSimple + '.qml')
		if not status:
			self.mainFrame.setStatusError('Fichier : ' + QGP.configPathActiveMap + QGP.configShapeMapLabelsSimple + '.qml' + ' : + Copie impossible ?', False)

		self.checkLabelsMAJStyle()
		self.iface.mapCanvas().refreshAllLayers()
		self.mainFrame.setStatusDone('Style des étiquettes et étiquettes simples pour cette carte réinitialisé - OK')


	def checkLabelsMAJStyle(self):
		pathStyleFileCurrent = self.activeMapFolder + QGP.configShapeMapLabels + '.qml'
		pathStyleFileReference = QGP.configPathActiveMap + QGP.configShapeMapLabels + '.qml'
		pathStyleFileCurrentSimple = self.activeMapFolder + QGP.configShapeMapLabelsSimple + '.qml'
		pathStyleFileReferenceSimple = QGP.configPathActiveMap + QGP.configShapeMapLabelsSimple + '.qml'
		fileA = open(pathStyleFileCurrent, 'r')
		fileB = open(pathStyleFileReference, 'r')
		fileC = open(pathStyleFileCurrent, 'r')
		fileD = open(pathStyleFileReference, 'r')
		if fileA.read() != fileB.read() or fileC.read() != fileD.read() :
			DSTY.setStyleNormalStrongButton(self.buttonStyleLabelsReload)
		else :
			DSTY.setStyleMainButtonsInactive(self.buttonStyleLabelsReload)


#	Style Points

	def buttonPointsMAJStyle_clicked(self):
		errorText, status = self.mainFrame.layerActiveMapPoints.loadNamedStyle(QGP.configPathActiveMap + QGP.configShapeMapReperes + '.qml')
		if not status:
			self.mainFrame.setStatusError(errorText, False)
			return

		self.mainFrame.setStatusWorking('Rechargement du Style par défaut des r ...')
		status, count = TFIL.copy_files(QGP.configPathActiveMap, self.activeMapFolder, QGP.configShapeMapReperes + '.qml')
		if not status:
			self.mainFrame.setStatusError('Fichier : ' + QGP.configPathActiveMap + QGP.configShapeMapReperes + '.qml' + ' : + Copie impossible ?', False)

		self.checkPointsMAJStyle()
		self.iface.mapCanvas().refreshAllLayers()
		self.mainFrame.setStatusDone('Style des repères pour cette carte réinitialisé - OK')

	def checkPointsMAJStyle(self):
		pathStyleFileCurrent = self.activeMapFolder + QGP.configShapeMapReperes + '.qml'
		pathStyleFileReference = QGP.configPathActiveMap + QGP.configShapeMapReperes + '.qml'
		fileA = open(pathStyleFileCurrent, 'r')
		fileB = open(pathStyleFileReference, 'r')
		if fileA.read() != fileB.read() :
			DSTY.setStyleNormalStrongButton(self.buttonStylePointsReload)
		else :
			DSTY.setStyleMainButtonsInactive(self.buttonStylePointsReload)


#	Style Tronçons

	def buttonSectionsMAJStyle_clicked(self):
		errorText, status = self.mainFrame.layerActiveMapSections.loadNamedStyle(QGP.configPathActiveMap + QGP.configShapeMapSections + '.qml')
		if not status:
			self.mainFrame.setStatusError(errorText, False)
			return

		self.mainFrame.setStatusWorking('Rechargement du Style par défaut des tronçons ...')
		status, count = TFIL.copy_files(QGP.configPathActiveMap, self.activeMapFolder, QGP.configShapeMapSections + '.qml')
		if not status:
			self.mainFrame.setStatusError('Fichier : ' + QGP.configPathActiveMap + QGP.configShapeMapSections + '.qml' + ' : + Copie impossible ?', False)

		DSYM.setSectionStyleVariables(self.mainFrame.layerActiveMapSections, self.activeMapScale)
		self.checkSectionsMAJStyle()
		self.iface.mapCanvas().refreshAllLayers()
		self.mainFrame.setStatusDone('Style des tronçons pour cette carte réinitialisé - OK')

	def checkSectionsMAJStyle(self):
		pathStyleFileCurrent = self.activeMapFolder + QGP.configShapeMapSections + '.qml'
		pathStyleFileReference = QGP.configPathActiveMap + QGP.configShapeMapSections + '.qml'
		fileA = open(pathStyleFileCurrent, 'r')
		fileB = open(pathStyleFileReference, 'r')
		if fileA.read() != fileB.read() :
			DSTY.setStyleNormalStrongButton(self.buttonStyleSectionsReload)
		else :
			DSTY.setStyleMainButtonsInactive(self.buttonStyleSectionsReload)


# ========================================================================================
# Actions : Export
# ========================================================================================

	def activeMapExportBackgroundInfoChanged(self):
		self.setExportDpiOpacityDefaultValues()

	def setExportDpiOpacityDefaultValues(self):
		self.activeMapExportDpiCombo.setCurrentText(str(QGP.configDicoExportBackground[self.activeMapExportBackgroundCombo.currentText()][0]))
		self.activeMapExportOpacityCombo.setCurrentText(str(QGP.configDicoExportBackground[self.activeMapExportBackgroundCombo.currentText()][1]))

	def buttonExportSchema_clicked(self):
		if TLAY.isLayerInGroupEditable(QGP.configActiveMapGroupName):				
			self.mainFrame.setStatusWarning('Un fichier - dont les modifications seraient perdues - est en mode édition dans le groupe : ' + QGP.configActiveMapGroupName + ' !')
			return		
		self.resetPointMapSchemaTemporarily()
		self.activeMapImagePath = SEXP.process_Export(self.iface, self.mainFrame, self, 'Schéma', 
										'Fond Blanc', DTOP.prefixSchemaBlanc + ('-Draft' if self.activeMapExportDraftOption.isChecked() else ''),
										None, 0, 
										int(self.activeMapExportOpacityCombo.currentText()), 
										0, 0, 
										True, False, None)
		self.mainFrame.layerActiveMapPoints.rollBack()

	def buttonExportTopo_clicked(self):
		QgsExpressionContextUtils.setLayerVariable(self.layerMapCopyright, QGP.tableMapsActiveMapVariableType, 'Topo')
		formatChanged, marginExport = self.reframeMapTopoTemporarily()
		if formatChanged :
			self.changeGridLabelPositionsTemporarily()
			self.changeDecorationCopyrightPosition(self.activeMapFeature[QGP.tableFramesFieldCopyright] , False)
			self.changeDecorationNumberPosition(self.activeMapFeature[QGP.tableFramesFieldNumber], False)
		
		self.activeMapImagePath =  SEXP.process_Export(self.iface, self.mainFrame, self, 'Topo',
										self.activeMapExportBackgroundCombo.currentText(),	DTOP.prefixMapsTopo + ('-Draft' if self.activeMapExportDraftOption.isChecked() else ''),
										None, marginExport, 
										int(self.activeMapExportOpacityCombo.currentText()), 
										0, 0, 
										True, False, self.retrieveOsmRasterLayer())
		
		if formatChanged :
			self.mainFrame.layerMaps.rollBack()
			self.resetGridLabelPositions()
			self.layerMapCopyright.rollBack()
			self.layerMapNumber.rollBack()

		QgsExpressionContextUtils.setLayerVariable(self.layerMapCopyright, QGP.tableMapsActiveMapVariableType, 'PDF')

	def buttonExportPDF_clicked(self):
		QgsExpressionContextUtils.setLayerVariable(self.layerMapCopyright, QGP.tableMapsActiveMapVariableType, 'PDF')

		self.activeMapImagePath = SEXP.process_Export(self.iface, self.mainFrame, self, 'PDF',
										self.activeMapExportBackgroundCombo.currentText(),  DTOP.prefixMapsPDF + ('-Draft' if self.activeMapExportDraftOption.isChecked() else ''),
										None, self.activeMapMargin, 
										int(self.activeMapExportOpacityCombo.currentText()), 
										0, 0, 
										True, False, self.retrieveOsmRasterLayer())
	
	def retrieveOsmRasterLayer(self):
		if not self.activeMapExportBackgroundCombo.currentText() == QGP.configExportTextOsm : return []
		rasterOsmLayerName = self.exportOsmCombo.currentText()
		rasterOsmLayer, errorText = TLAY.findLayerInGroup(QGP.configActiveRasterOsmGroupName, rasterOsmLayerName)
		return [rasterOsmLayer]

	def reframeMapTopoTemporarily(self):
		
#		Vérifier s'il faut changer le format

		topoFormat = QGP.dicoPaperFormats[self.activeMapFormat][QGP.C_dicoPaperFormats_ColTopoFormat]
		if topoFormat == None: return False, QGP.dicoPaperFormats[self.activeMapFormat][QGP.C_dicoPaperFormats_ColMargin]
		
#		Retrouver les paramètres du format Topo temporaire

		topoMapWidth = QGP.dicoPaperFormats[topoFormat][0] * self.activeMapScale / 1000
		topoMapHeight = QGP.dicoPaperFormats[topoFormat][1] * self.activeMapScale / 1000
		
#		Créer les 4 points du nouveau rectangle en gardant le même centre

		centerPoint = self.activeMapBox.center()
		PNO = QgsPointXY(centerPoint.x() - topoMapWidth / 2, centerPoint.y() + topoMapHeight / 2)
		PNE = QgsPointXY(centerPoint.x() + topoMapWidth / 2, centerPoint.y() + topoMapHeight / 2)
		PSE = QgsPointXY(centerPoint.x() + topoMapWidth / 2, centerPoint.y() - topoMapHeight / 2)
		PSO = QgsPointXY(centerPoint.x() - topoMapWidth / 2, centerPoint.y() - topoMapHeight / 2)

		self.temporaryActiveMapBox = QgsRectangle(PNO, PSE)					# Used to position grid labels

#		Modifier temporairement la géométrie de l'entité

		self.quitOnLayerMapsChange = False

		self.mainFrame.layerMaps.startEditing()
		self.mainFrame.layerMaps.changeGeometry(self.activeMapFeature.id(), QgsGeometry.fromMultiPolygonXY([[[PNO, PNE, PSE, PSO, PNO]]]))

		return True, QGP.dicoPaperFormats[topoFormat][QGP.C_dicoPaperFormats_ColMargin]


	def changeGridLabelPositionsTemporarily(self):
		for gridName in QGP.configGridShapesList:
			gridLayer, errorText = TLAY.openLayer(gridName)
			if gridLayer != None:
				QgsExpressionContextUtils.setLayerVariable(gridLayer, QGP.gridVariableLineTop, str(int(self.temporaryActiveMapBox.yMaximum() + self.gridLabeldistance)))
				QgsExpressionContextUtils.setLayerVariable(gridLayer, QGP.gridVariableLineBottom, str(int(self.temporaryActiveMapBox.yMinimum() - self.gridLabeldistance)))
				QgsExpressionContextUtils.setLayerVariable(gridLayer, QGP.gridVariableLineLeft, str(int(self.temporaryActiveMapBox.xMinimum() - self.gridLabeldistance)))
				QgsExpressionContextUtils.setLayerVariable(gridLayer, QGP.gridVariableLineRight, str(int(self.temporaryActiveMapBox.xMaximum() + self.gridLabeldistance)))
	
	def resetGridLabelPositions(self):
		for gridName in QGP.configGridShapesList:
			gridLayer, errorText = TLAY.openLayer(gridName)
			if gridLayer != None:
				QgsExpressionContextUtils.setLayerVariable(gridLayer, QGP.gridVariableLineTop, str(int(self.activeMapBox.yMaximum() + self.gridLabeldistance)))
				QgsExpressionContextUtils.setLayerVariable(gridLayer, QGP.gridVariableLineBottom, str(int(self.activeMapBox.yMinimum() - self.gridLabeldistance)))
				QgsExpressionContextUtils.setLayerVariable(gridLayer, QGP.gridVariableLineLeft, str(int(self.activeMapBox.xMinimum() - self.gridLabeldistance)))
				QgsExpressionContextUtils.setLayerVariable(gridLayer, QGP.gridVariableLineRight, str(int(self.activeMapBox.xMaximum() + self.gridLabeldistance)))
	
	
	def resetPointMapSchemaTemporarily(self):
	
		self.mainFrame.layerActiveMapPoints.startEditing()
		for feature in self.mainFrame.layerActiveMapPoints.getFeatures():
			pointXY = QgsPointXY(feature[QGP.tableMapPointsFieldIdXRepere], feature[QGP.tableMapPointsFieldIdYRepere])
			self.mainFrame.layerActiveMapPoints.changeGeometry(feature.id(), QgsGeometry.fromPointXY(pointXY))


	def buttonHelpViewMap_clicked(self):
		if self.activeMapImagePath != None:
			THEL.viewMapOnBrowser(self.mainFrame, 'Image de la dernière Carte Exportée', self.activeMapImagePath)
		

# ========================================================================================
# ========================================================================================
#
# Initialisation d'une nouvelle carte active
# 
# ========================================================================================
# ========================================================================================

	def initializeActiveMap(self):
	
#		Définir les variables pour le style des Repères, des Etiquettes	
	
		if self.activeMapFeature == self.mainFrame.selectedMapFeature : 
			scale = self.activeMapFeature[QGP.tableFramesFieldEchelle]
			DSYM.setRepereStyleVariables(self.mainFrame.layerActiveMapPoints, scale)
			DSYM.setLabelsSimpleStyleVariables(self.mainFrame.layerActiveMapLabelsSimple, scale)	
			DSYM.setSectionStyleVariables(self.mainFrame.layerActiveMapSections, scale)
			if TCOD.itineraryTypeFromTrackCode(self.activeMapItinerary) == 'RF':					
				DSYM.setPoisRFStyleVariables(self.mainFrame.layerActiveMapPoisRF, scale)
			return
		
		self.mainFrame.setStatusWorking('Carte Active - Préparation  .')
	
#		Informations de la Carte
	
		self.activeMapFeature = QgsFeature(self.mainFrame.selectedMapFeature)
		self.activeMapItinerary = self.activeMapFeature[QGP.tableFramesFieldItineraryCode]
		self.activeMapItineraryType = TCOD.itineraryTypeFromTrackCode(self.activeMapItinerary)
		self.activeMapFormat = self.activeMapFeature[QGP.tableFramesFieldFormat]
		self.activeMapMargin = QGP.dicoPaperFormats[self.activeMapFormat][2] if self.activeMapFormat != None else 0
		self.activeMapScale = self.activeMapFeature[QGP.tableFramesFieldEchelle]
		self.activeMapName = self.activeMapFeature[QGP.tableFramesFieldName]
		self.activeMapFolder = self.activeMapFeature[QGP.tableFramesFieldFolder]
		self.activeMapBackground = self.activeMapFeature[QGP.tableFramesFieldBackground]
		self.activeMapBox = self.activeMapFeature.geometry().boundingBox()
		self.activeMapBoxEnlarged = TGEO.enlargeRectangle(self.activeMapBox, QGP.sectionsGetFeaturesExtraSize)
		self.activeMapTileCounts = [math.ceil(self.activeMapBox.width() * 1000 / (self.activeMapScale * QGP.mapsExportMaxSize[0])), math.ceil(self.activeMapBox.height() * 1000 / (self.activeMapScale * QGP.mapsExportMaxSize[1]))]
		self.activeMapImagePath = None

#		Définir la variable de Carte active pour le cadre blanc éventuel

		if self.layerMapWhiteFrame != None : QgsExpressionContextUtils.setLayerVariable(self.layerMapWhiteFrame, QGP.tableMapsActiveMapVariableHighlight, self.activeMapName)

#		Définir la variable pour la largeur de l'étiquette du numéro carte

		QgsExpressionContextUtils.setLayerVariable(self.layerMapNumber, QGP.tableActiveMapNumberVariableName, self.activeMapName)

#		Définir le type de Copyright - PDF par défaut

		QgsExpressionContextUtils.setLayerVariable(self.layerMapCopyright, QGP.tableMapsActiveMapVariableType, 'PDF')
		
#		Définir les variables de position des Labels pour les Grilles - si présentes

		if self.activeMapItineraryType == 'IR' and self.activeMapFormat[0:3] == 'IR-' :
			self.gridLabeldistance = QGP.gridLabelWhiteFrameDistance * self.activeMapScale / 1000
		elif self.activeMapItineraryType in ('RB', 'IR') :
			self.gridLabeldistance = QGP.gridLabelRBDistance * self.activeMapScale / 1000
		else :
			self.gridLabeldistance = 9999

		for gridName in QGP.configGridShapesList:
			gridLayer, errorText = TLAY.openLayer(gridName)
			if gridLayer != None:
				QgsExpressionContextUtils.setLayerVariable(gridLayer, QGP.gridVariableLineTop, str(int(self.activeMapBox.yMaximum() + self.gridLabeldistance)))
				QgsExpressionContextUtils.setLayerVariable(gridLayer, QGP.gridVariableLineBottom, str(int(self.activeMapBox.yMinimum() - self.gridLabeldistance)))
				QgsExpressionContextUtils.setLayerVariable(gridLayer, QGP.gridVariableLineLeft, str(int(self.activeMapBox.xMinimum() - self.gridLabeldistance)))
				QgsExpressionContextUtils.setLayerVariable(gridLayer, QGP.gridVariableLineRight, str(int(self.activeMapBox.xMaximum() + self.gridLabeldistance)))
	
#		Définir les variables pour le style des Repères, des Etiquettes	
	
		DSYM.setRepereStyleVariables(self.mainFrame.layerActiveMapPoints, self.activeMapScale)
		DSYM.setLabelsSimpleStyleVariables(self.mainFrame.layerActiveMapLabelsSimple, self.activeMapScale)	
		DSYM.setSectionStyleVariables(self.mainFrame.layerActiveMapSections, self.activeMapScale)
		if TCOD.itineraryTypeFromTrackCode(self.activeMapItinerary) == 'RF':					
			DSYM.setPoisRFStyleVariables(self.mainFrame.layerActiveMapPoisRF, self.activeMapScale)
		
# 		Initialisation des cadres		
		
		self.initializeActiveMapInformations(); 		self.mainFrame.setStatusWorking('Carte Active - Préparation  . .')
		self.initializeActiveMapDecorations(); 			self.mainFrame.setStatusWorking('Carte Active - Préparation  . . .')
		self.initializeActiveMapExportModifications(); 	self.mainFrame.setStatusWorking('Carte Active - Préparation  . . . .')
		self.initializeActiveMapGlobalPoints(); 		self.mainFrame.setStatusWorking('Carte Active - Préparation  . . . . .')
		self.initializeActiveMapExportPoints(); 		self.mainFrame.setStatusWorking('Carte Active - Préparation  . . . . . .')
		self.initializeActiveMapExportLabels(); 		self.mainFrame.setStatusWorking('Carte Active - Préparation  . . . . . . .')
		self.initializeActiveMapExportBackground();		self.mainFrame.setStatusWorking('Carte Active - Préparation  . . . . . . . .')
		self.initializeActiveMapGlobalSections();		self.mainFrame.setStatusWorking('Carte Active - Préparation  . . . . . . . . .')
		self.initializeActiveMapExport();				self.mainFrame.setStatusWorking('Carte Active - Préparation  . . . . . . . . . .')

# 		Vérification des Styles

		self.checkPointsMAJStyle()
		self.checkSectionsMAJStyle()
		self.checkLabelsMAJStyle()

		self.mainFrame.setStatusDone('Carte Active - OK')
		
	def initializeActiveMapInformations(self):		

		self.activeMapItineraryInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%',str(self.activeMapFeature[QGP.tableFramesFieldItineraryCode])))
		DSTY.setStyleOkLabel(self.activeMapItineraryInfo, 'Normal')
		
		self.activeMapNameInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%',str(self.activeMapFeature[QGP.tableFramesFieldName])))
		DSTY.setStyleOkLabel(self.activeMapNameInfo, 'Double')

		self.activeMapFormatInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%',str(self.activeMapFormat)))
		DSTY.setStyleOkLabel(self.activeMapFormatInfo, 'Normal')

		self.activeMapScaleInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%',str(self.activeMapFeature[QGP.tableFramesFieldEchelle])))
		DSTY.setStyleOkLabel(self.activeMapScaleInfo, 'Normal')

		if self.activeMapScale != None:
			self.activeMapPaperWidthInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%','{:,d} mm'.format(round(self.activeMapBox.width() * 1000 / self.activeMapScale)).replace(',','.')))
			DSTY.setStyleOkLabel(self.activeMapPaperWidthInfo, 'Normal')
			self.activeMapPaperHeightInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%','{:,d} mm'.format(round(self.activeMapBox.height() * 1000 / self.activeMapScale)).replace(',','.')))
			DSTY.setStyleOkLabel(self.activeMapPaperHeightInfo, 'Normal')
			if self.activeMapFormat in QGP.dicoPaperFormats:
				if round(self.activeMapBox.width() * 1000 / self.activeMapScale) != QGP.dicoPaperFormats[self.activeMapFormat][0] :
					DSTY.setStyleErrorLabel(self.activeMapPaperWidthInfo, 'Normal')
				if round(self.activeMapBox.height() * 1000 / self.activeMapScale) != QGP.dicoPaperFormats[self.activeMapFormat][1] :
					DSTY.setStyleErrorLabel(self.activeMapPaperHeightInfo, 'Normal')

		self.activeMapPaperMarginInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%','{:,d} mm'.format(self.activeMapMargin)))
		DSTY.setStyleOkLabel(self.activeMapPaperMarginInfo, 'Normal')

		self.activeMapRealWidthInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%','{:,d} m'.format(round(self.activeMapBox.width())).replace(',','.')))
		DSTY.setStyleOkLabel(self.activeMapRealWidthInfo, 'Normal')

		self.activeMapRealHeightInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%','{:,d} m'.format(round(self.activeMapBox.height())).replace(',','.')))
		DSTY.setStyleOkLabel(self.activeMapRealHeightInfo, 'Normal')

		self.activeMapFolderInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%',str(self.activeMapFeature[QGP.tableFramesFieldFolder])))
		DSTY.setStyleOkLabel(self.activeMapFolderInfo, 'Double3')

	def initializeActiveMapDecorations(self):
		self.changeDecorationCopyrightPosition(self.activeMapFeature[QGP.tableFramesFieldCopyright])
		self.changeDecorationNumberPosition(self.activeMapFeature[QGP.tableFramesFieldNumber])

	def initializeActiveMapGlobalPoints(self):
	
		mapItineraryWithModifications = self.activeMapItinerary + ('-MT' if 'T' in self.modificationsLists[0] else '') + ('-MF' if 'F' in self.modificationsLists[0] else '')
		self.activeMapPointsGlobalFeaturesList = [feature for feature in self.layerPointsGR.getFeatures(self.activeMapBox) if TCOD.areTrackAndPointCodesCompatibles(mapItineraryWithModifications, feature[QGP.tablePointsFieldGRCode]) ]
		repereList = [str(feature[QGP.tablePointsFieldRepere]) for feature in self.activeMapPointsGlobalFeaturesList]
		repereList = sorted(repereList, key = lambda x: int('0' + ''.join(c for c in x if c.isdigit())))
		repereText = '  {:0d} repères : '.format(len(repereList)) + ' '.join( _ for _ in repereList)
		self.activeMapPointsGlobalInfo.setText(DSTY.textFormatBlackNormalLeft.replace('%TEXT%',repereText))
		DSTY.setStyleOkLabel(self.activeMapPointsGlobalInfo, 'Double')

		if self.activeMapItineraryType == 'RF' :
			if self.layerPOIs != None :		 
				self.activeMapPoisGlobalFeaturesList = [feature for feature in self.layerPOIs.getFeatures(self.activeMapBox) \
															if feature[QGP.poisTableFieldType] == 'RF' and \
																TCOD.areTrackAndPointCodesCompatibles(mapItineraryWithModifications, '-'.join(str(feature[QGP.poisTableFieldTracks]).split('-')[0:-1])) ]
				poisList = [str(feature[QGP.poisTableFieldTracks]).split('-')[-1] for feature in self.activeMapPoisGlobalFeaturesList]
				poisList = sorted(poisList)
				poisText = '  {:0d} pois : '.format(len(poisList)) + ' '.join( _ for _ in poisList)
				self.activeMapPoisGlobalInfo.setText(DSTY.textFormatBlackNormalLeft.replace('%TEXT%',poisText))
				DSTY.setStyleOkLabel(self.activeMapPoisGlobalInfo, 'Normal')
			else:
				DSTY.setStyleErrorLabel(self.activeMapPoisGlobalInfo, 'Normal')

	def initializeActiveMapExportPoints(self):

		activeMapPointsExportFeaturesList = [feature for feature in self.mainFrame.layerActiveMapPoints.getFeatures()]
		repereList = [str(feature[QGP.tableMapPointsFieldRepere]) for feature in activeMapPointsExportFeaturesList]
		repereList = sorted(repereList, key = lambda x: int('0' + ''.join(c for c in x if c.isdigit())))
		repereText = '  {:0d} repères : '.format(len(repereList)) + ' '.join( _ for _ in repereList)
		self.activeMapPointsExportInfo.setText(DSTY.textFormatBlackNormalLeft.replace('%TEXT%',repereText))
		DSTY.setStyleOkLabel(self.activeMapPointsExportInfo, 'Double')

	def initializeActiveMapExportPois(self):

		activeMapPoisExportFeaturesList = [feature for feature in self.mainFrame.layerActiveMapPoisRF.getFeatures()]
		poiList = [str(feature[QGP.tableMapPoiRFFieldPoint]) for feature in activeMapPoisExportFeaturesList]
		poiList = sorted(poiList)
		poiText = '  {:0d} pois : '.format(len(poiList)) + ' '.join( _ for _ in poiList)
		self.activeMapPoisExportInfo.setText(DSTY.textFormatBlackNormalLeft.replace('%TEXT%',poiText))
		DSTY.setStyleOkLabel(self.activeMapPoisExportInfo, 'Normal') if self.layerPOIs != None else DSTY.setStyleErrorLabel(self.activeMapPoisExportInfo, 'Normal')

	def initializeActiveMapExportLabels(self):
		activeMapLabelsExportFeaturesList = [feature for feature in self.mainFrame.layerActiveMapLabels.getFeatures()]
		activeMapLabelsSimpleExportFeaturesList = [feature for feature in self.mainFrame.layerActiveMapLabelsSimple.getFeatures()]
		labelsText = ' {:0d}+{:0d} etiquettes'.format(len(activeMapLabelsExportFeaturesList),len(activeMapLabelsSimpleExportFeaturesList))
		self.activeMapLabelsExportInfo.setText(DSTY.textFormatBlackNormalLeft.replace('%TEXT%',labelsText))
		DSTY.setStyleOkLabel(self.activeMapLabelsExportInfo, 'Normal')

	def initializeActiveMapExportModifications(self):
		self.modificationsLists = ast.literal_eval(self.activeMapFeature[QGP.tableFramesFieldModifications]) if self.activeMapFeature[QGP.tableFramesFieldModifications] != None else [[],[]]
		self.modificationsCheckBoxConnected = False
		self.includeModifsTemporaryMainOption.setChecked(True if 'T' in self.modificationsLists[0] else False)
		self.includeModifsFuturesMainOption.setChecked(True if 'F' in self.modificationsLists[0] else False)
		self.includeModifsTemporaryOtherOption.setChecked(True if 'T' in self.modificationsLists[1] else False)
		self.includeModifsFuturesOtherOption.setChecked(True if 'F' in self.modificationsLists[1] else False)
		self.modificationsCheckBoxConnected = True
		
	def initializeActiveMapExportBackground(self):
		self.activeMapBackground = self.activeMapFeature[QGP.tableFramesFieldBackground]
		if self.activeMapFeature[QGP.tableFramesFieldBackground] != None:
			self.activeMapBackgroundCombo.setCurrentText(self.activeMapBackground)
			self.activeMapBackgroundInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%', self.activeMapFeature[QGP.tableFramesFieldBackground]))
			DSTY.setStyleOkLabel(self.activeMapBackgroundInfo, 'Normal')
		else:
			self.activeMapBackgroundInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%', 'Non défini'))
			DSTY.setStyleWarningLabel(self.activeMapBackgroundInfo, 'Normal')

	def initializeActiveMapGlobalSections(self):
	
		self.activeMapSectionsGlobalFeaturesList = [feature for feature in self.layerSectionsGR.getFeatures(self.activeMapBoxEnlarged)]
		sectionsText = '  {:0d} tronçons'.format(len(self.activeMapSectionsGlobalFeaturesList))
		self.activeMapSectionsGlobalInfo.setText(DSTY.textFormatBlackNormalLeft.replace('%TEXT%',sectionsText))
		DSTY.setStyleOkLabel(self.activeMapSectionsGlobalInfo, 'Normal')	

		self.activeMapSectionsUsedInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%','. . .'))
		DSTY.setStyleOkLabel(self.activeMapSectionsUsedInfo)
		self.activeMapSectionsSustituedInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%','. . .'))
		DSTY.setStyleOkLabel(self.activeMapSectionsSustituedInfo)

		sectionsText = '  {:0d} tronçons'.format(sum(1 for _ in self.mainFrame.layerActiveMapSections.getFeatures()))
		self.activeMapSectionsMergedInfo.setText(DSTY.textFormatBlackNormalLeft.replace('%TEXT%',sectionsText))
		DSTY.setStyleOkLabel(self.activeMapSectionsMergedInfo, 'Normal')	

	def initializeActiveMapExport(self):
		self.activeMapExportBackgroundCombo.setCurrentText(self.activeMapBackgroundCombo.currentText())
		self.activeMapExportBackgroundInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%',self.activeMapBackgroundCombo.currentText()))
		DSTY.setStyleOkLabel(self.activeMapExportBackgroundInfo, 'Normal')	

		self.activeMapExportDecorationOption.setCheckState(Qt.Checked)
		self.activeMapExportGridOption.setCheckState(Qt.Checked if DSYM.isGridOnMap(self.activeMapItineraryType) else Qt.Unchecked)

		self.activeMapExportCountInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%', str(self.activeMapTileCounts[0]) + ' x ' + str(self.activeMapTileCounts[1])))
		DSTY.setStyleOkLabel(self.activeMapExportCountInfo, 'Normal')	

		self.activeMapExportTileSizeInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%', \
			str(round((self.activeMapBox.width() * 1000) / (self.activeMapScale * self.activeMapTileCounts[0]))) + ' mm x ' + \
			str(round((self.activeMapBox.height() * 1000) / (self.activeMapScale * self.activeMapTileCounts[1]))) + ' mm'))
		DSTY.setStyleOkLabel(self.activeMapExportTileSizeInfo, 'Normal')	


# ========================================================================================
# ========================================================================================
#
# Création des différents cadres Menu
# 
# ========================================================================================
# ========================================================================================


# ========================================================================================
# Cadre : Informations Carte
# ========================================================================================

	def menuBoxMapInfo(self):
	
		groupBoxMapInfo = QtWidgets.QGroupBox('Paramètres de la Carte', self.mainMenu)
		groupBoxMapInfo.setStyleSheet(DSTY.styleBox)
		
#	Itinéraire et nom de la carte	

		TBUT.createLabelBlackButton(groupBoxMapInfo, 1, 1, 'Itinéraire / Nom', 'Normal', 'Normal')
		self.activeMapItineraryInfo = TBUT.createLabelGreenButton(groupBoxMapInfo, 2, 1, '. . .', 'Normal', 'Normal')
		DSTY.setStyleWarningLabel(self.activeMapItineraryInfo, "Normal")
		self.activeMapNameInfo = TBUT.createLabelGreenButton(groupBoxMapInfo, 3, 1, '. . .', 'Double', 'Normal')
		DSTY.setStyleWarningLabel(self.activeMapNameInfo, "Double")

#	Format et Echelle	

		TBUT.createLabelBlackButton(groupBoxMapInfo, 1, 2, 'Format / Echelle', 'Normal', 'Normal')
		self.activeMapFormatInfo = TBUT.createLabelGreenButton(groupBoxMapInfo, 2, 2, '. . .', 'Normal', 'Normal')
		DSTY.setStyleWarningLabel(self.activeMapFormatInfo, "Normal")
		self.activeMapScaleInfo = TBUT.createLabelGreenButton(groupBoxMapInfo, 3, 2, '. . .', 'Normal', 'Normal')
		DSTY.setStyleWarningLabel(self.activeMapScaleInfo, "Normal")

#	Largeur / Hauteur Papier / Marge

		TBUT.createLabelBlackButton(groupBoxMapInfo, 1, 3, 'Largeur / Hauteur', 'Normal', 'Normal')
		self.activeMapPaperWidthInfo = TBUT.createLabelGreenButton(groupBoxMapInfo, 2, 3, '. . .', 'Normal', 'Normal')
		DSTY.setStyleWarningLabel(self.activeMapPaperWidthInfo, "Normal")
		self.activeMapPaperHeightInfo = TBUT.createLabelGreenButton(groupBoxMapInfo, 3, 3, '. . .', 'Normal', 'Normal')
		DSTY.setStyleWarningLabel(self.activeMapPaperHeightInfo, "Normal")
		self.activeMapPaperMarginInfo = TBUT.createLabelGreenButton(groupBoxMapInfo, 4, 3, '. . .', 'Normal', 'Normal')
		DSTY.setStyleWarningLabel(self.activeMapPaperMarginInfo, "Normal")

#	Largeur / Hauteur Terrain

		TBUT.createLabelBlackButton(groupBoxMapInfo, 5, 3, 'Longitude / Latitude', 'Normal', 'Normal')
		self.activeMapRealWidthInfo = TBUT.createLabelGreenButton(groupBoxMapInfo, 6, 3, '. . .', 'Normal', 'Normal')
		DSTY.setStyleWarningLabel(self.activeMapRealWidthInfo, "Normal")
		self.activeMapRealHeightInfo = TBUT.createLabelGreenButton(groupBoxMapInfo, 7, 3, '. . .', 'Normal', 'Normal')
		DSTY.setStyleWarningLabel(self.activeMapRealHeightInfo, "Normal")

#	Folder

		TBUT.createLabelBlackButton(groupBoxMapInfo, 5, 1, 'Répertoire Shapes', 'Normal', 'Normal')
		self.activeMapFolderInfo = TBUT.createLabelGreenButton(groupBoxMapInfo, 6, 1, '. . .', 'Double3', 'Normal')
		DSTY.setStyleWarningLabel(self.activeMapFolderInfo, "Double3")
				
#	Bouton Zoom

		buttonActiveMapZoom = TBUT.createActionButton(groupBoxMapInfo, 8, 3, 'Zoom', 'Normal')
		buttonActiveMapZoom.clicked.connect(self.buttonActiveMapZoom_clicked)

# 	Terminé

		groupBoxMapInfo.repaint()

		return groupBoxMapInfo


# ========================================================================================
# Cadre : Décorations - Copyright et Nom Carte
# ========================================================================================

	def menuBoxCarteDecorations(self):

		groupBoxDecorations = QtWidgets.QGroupBox('Décorations - Copyright et Nom Carte', self.mainMenu)
		groupBoxDecorations.setStyleSheet(DSTY.styleBox)

#	Labels pour 2 séries de boutons	

		TBUT.createLabelBlackButton(groupBoxDecorations, 1, 1, 'Copyright', 'Normal')
		TBUT.createLabelBlackButton(groupBoxDecorations, 1, 2, 'Nom Carte', 'Normal')
	

# 	Terminé

		groupBoxDecorations.repaint()

		return groupBoxDecorations


	def menuBoxCarteDecorationsCopyright(self):

		groupBoxCopyright = QtWidgets.QGroupBox('', self.mainMenu)
		groupBoxCopyright.setStyleSheet(DSTY.styleHiddenBox)

# 	Radio Boutons

		buttonMapCopyrightLeft = TBUT.createRadioBoxButton(groupBoxCopyright, 2, 1, 'A gauche', 'Compact')
		buttonMapCopyrightCenter = TBUT.createRadioBoxButton(groupBoxCopyright, 3, 1, 'Au centre', 'Compact')
		buttonMapCopyrightRight = TBUT.createRadioBoxButton(groupBoxCopyright, 4, 1, 'A droite', 'Compact')
		buttonMapCopyrightNone = TBUT.createRadioBoxButton(groupBoxCopyright, 5, 1, 'Sans', 'Compact')

		buttonMapCopyrightLeft.clicked.connect(buttonDecoration_clicked(self, 'Copyright', 'Gauche'))
		buttonMapCopyrightCenter.clicked.connect(buttonDecoration_clicked(self, 'Copyright', 'Centre'))
		buttonMapCopyrightRight.clicked.connect(buttonDecoration_clicked(self, 'Copyright', 'Droite'))
		buttonMapCopyrightNone.clicked.connect(buttonDecoration_clicked(self, 'Copyright', 'Sans'))

# 	Terminé

		groupBoxCopyright.repaint()

		return groupBoxCopyright


	def menuBoxCarteDecorationsName(self):

		groupBoxName = QtWidgets.QGroupBox('', self.mainMenu)
		groupBoxName.setStyleSheet(DSTY.styleHiddenBox)

# 	Radio Boutons

		buttonMapNameLeft = TBUT.createRadioBoxButton(groupBoxName, 2, 1, 'A gauche', 'Compact')
		buttonMapNameCenter = TBUT.createRadioBoxButton(groupBoxName, 3, 1, 'Au centre', 'Compact')
		buttonMapNameRight = TBUT.createRadioBoxButton(groupBoxName, 4, 1, 'A droite', 'Compact')
		buttonMapNameNone = TBUT.createRadioBoxButton(groupBoxName, 5, 1, 'Sans', 'Compact')

		buttonMapNameLeft.clicked.connect(buttonDecoration_clicked(self, 'Nom', 'Gauche'))
		buttonMapNameCenter.clicked.connect(buttonDecoration_clicked(self, 'Nom', 'Centre'))
		buttonMapNameRight.clicked.connect(buttonDecoration_clicked(self, 'Nom', 'Droite'))
		buttonMapNameNone.clicked.connect(buttonDecoration_clicked(self, 'Nom', 'Sans'))

# 	Terminé

		groupBoxName.repaint()

		return groupBoxName
		
		
# ========================================================================================
# Cadre : Points Repères
# ========================================================================================

	def menuBoxCartePoints(self):

		groupBoxPoints = QtWidgets.QGroupBox('Repères et Pois RF sur la Carte', self.mainMenu)
		groupBoxPoints.setStyleSheet(DSTY.styleBox)

#	Repères possibles sur la carte et repères effectifs		
		
		TBUT.createLabelBlackButton(groupBoxPoints, 1, 1, 'Repères Emprise', 'Normal')
		self.activeMapPointsGlobalInfo = TBUT.createLabelGreenButton(groupBoxPoints, 2, 1, '. . .', 'Double', 'Normal')
		
		TBUT.createLabelBlackButton(groupBoxPoints, 1, 2, 'Repères Export', 'Normal')
		self.activeMapPointsExportInfo = TBUT.createLabelGreenButton(groupBoxPoints, 2, 2, '. . .', 'Double', 'Normal')
		
#	Pois possibles sur la carte RF et Pois effectifs

		self.activeMapPoisGlobalInfo = TBUT.createLabelGreenButton(groupBoxPoints, 4, 1, '. . .', 'Normal', 'Normal')
		self.activeMapPoisExportInfo = TBUT.createLabelGreenButton(groupBoxPoints, 4, 2, '. . .', 'Normal', 'Normal')
		
#	Bouton Aide

		buttonHelpPoints = TBUT.createHelpButton(groupBoxPoints, 4, 3, 'Aide Repères', 'Normal')
		buttonHelpPoints.clicked.connect(self.buttonHelpPoints_clicked)

#	Boutons Actions

		self.buttonStylePointsReload = TBUT.createActionButton(groupBoxPoints, 1, 3, 'MAJ Style', 'Normal')
		self.buttonStylePointsReload.clicked.connect(self.buttonPointsMAJStyle_clicked)
			
		buttonPointsReload = TBUT.createActionButton(groupBoxPoints, 2, 3, 'MAJ Repères', 'Normal')
		buttonPointsReload.clicked.connect(self.buttonPointsReload_clicked)

		buttonPointsLoad = TBUT.createActionButton(groupBoxPoints, 3, 3, 'Charger Repères', 'Normal')
		buttonPointsLoad.clicked.connect(self.buttonPointsLoad_clicked)
		
# 	Terminé

		groupBoxPoints.repaint()

		return groupBoxPoints		
		
	def buttonHelpPoints_clicked(self):
		webbrowser.open_new_tab(QGP.configMenuHelpBasePath + 'QCarto - Carte Active - Définitions - Repères.html')
		
		
# ========================================================================================
# Cadre : Etiquettes
# ========================================================================================

	def menuBoxCarteLabels(self):

		groupBoxLabels = QtWidgets.QGroupBox('Etiquettes sur la Carte', self.mainMenu)
		groupBoxLabels.setStyleSheet(DSTY.styleBox)

#	Etiquettes effectives
		
		TBUT.createLabelBlackButton(groupBoxLabels, 1, 1, 'Etiquettes Carte', 'Normal')
		self.activeMapLabelsExportInfo = TBUT.createLabelGreenButton(groupBoxLabels, 2, 1, '. . .', 'Normal', 'Normal')
		
		self.buttonStyleLabelsReload = TBUT.createActionButton(groupBoxLabels, 3, 1, 'MAJ Style', 'Normal')
		self.buttonStyleLabelsReload.clicked.connect(self.buttonLabelsMAJStyle_clicked)
		
#	Bouton Aide

		buttonHelpLabels = TBUT.createHelpButton(groupBoxLabels, 4, 1, 'Aide Etiquettes', 'Normal')
		buttonHelpLabels.clicked.connect(self.buttonHelpLabels_clicked)

# 	Terminé

		groupBoxLabels.repaint()

		return groupBoxLabels			
	

	def buttonHelpLabels_clicked(self):
		webbrowser.open_new_tab(QGP.configMenuHelpBasePath + 'QCarto - Carte Active - Définitions - Etiquettes.html')
	
	
# ========================================================================================
# Cadre : Gestion des Modifications
# ========================================================================================

	def menuBoxCarteModifications(self):

		groupBoxModifications = QtWidgets.QGroupBox('Modifications à prendre en compte', self.mainMenu)
		groupBoxModifications.setStyleSheet(DSTY.styleBox)

#	Modifications à prendre en compte
		
		TBUT.createLabelBlackButton(groupBoxModifications, 1, 1, 'Itinéraire', 'Normal')

		self.includeModifsTemporaryMainOption = TBUT.createCheckBoxButton(groupBoxModifications, 2, 1, 'Temporaires', 'Normal')
		self.includeModifsTemporaryMainOption.stateChanged.connect(self.modificationCheckChanged)

		self.includeModifsFuturesMainOption = TBUT.createCheckBoxButton(groupBoxModifications, 3, 1, 'Futures', 'Normal')
		self.includeModifsFuturesMainOption.stateChanged.connect(self.modificationCheckChanged)
	
		TBUT.createLabelBlackButton(groupBoxModifications, 1, 2, 'Autres GR', 'Normal')

		self.includeModifsTemporaryOtherOption = TBUT.createCheckBoxButton(groupBoxModifications, 2, 2, 'Temporaires', 'Normal')
		self.includeModifsTemporaryOtherOption.stateChanged.connect(self.modificationCheckChanged)

		self.includeModifsFuturesOtherOption = TBUT.createCheckBoxButton(groupBoxModifications, 3, 2, 'Futures', 'Normal')
		self.includeModifsFuturesOtherOption.stateChanged.connect(self.modificationCheckChanged)
	
#	Bouton Aide

		buttonHelpModifications = TBUT.createHelpButton(groupBoxModifications, 4, 1, 'Aide Modifications', 'Normal')
		buttonHelpModifications.clicked.connect(self.buttonHelpModifications_clicked)

# 	Terminé

		groupBoxModifications.repaint()

		return groupBoxModifications			
	
	
# ========================================================================================
# Cadre : Carte du fond
# ========================================================================================

	def menuBoxCarteBackground(self):

		groupBoxBackground = QtWidgets.QGroupBox('Fond de la Carte', self.mainMenu)
		groupBoxBackground.setStyleSheet(DSTY.styleBox)

#	Fond actuel et combo
		
		TBUT.createLabelBlackButton(groupBoxBackground, 1, 1, 'Fond Carte', 'Normal')

		self.activeMapBackgroundInfo = TBUT.createLabelGreenButton(groupBoxBackground, 2, 1, '. . .', 'Normal', 'Normal')
		self.activeMapBackgroundCombo = TBUT.createComboButton(groupBoxBackground, 3, 1, 'Normal')
		for background in QGP.exportActiveMapCopyrightDico:
			self.activeMapBackgroundCombo.addItem(background)
		self.activeMapBackgroundCombo.currentTextChanged.connect(self.backgroundComboChanged)
		
#	Bouton Aide

		buttonHelpMBackground = TBUT.createHelpButton(groupBoxBackground, 4, 1, 'Aide Fond', 'Normal')
#		buttonHelpMBackground.clicked.connect(self.buttonHelpBackground_clicked)

#	Boutons Actions pour édition des couches tronçons sur IGN

		TBUT.createLabelBlackButton(groupBoxBackground, 1, 2, 'Tronçons sur IGN', 'Normal')

#		buttonEditIGN50V3 = TBUT.createActionButton(groupBoxBackground, 2, 2, 'IGN-50 Ed3', 'Normal')
#		buttonEditIGN50V3.clicked.connect()

		buttonEditIGN50V4 = TBUT.createActionButton(groupBoxBackground, 3, 2, 'IGN-50 Ed4', 'Normal')
		buttonEditIGN50V4.clicked.connect(self.buttonEditIGN50V4_clicked)

# 	Terminé

		groupBoxBackground.repaint()

		return groupBoxBackground			
		
		
# ========================================================================================
# Cadre : Sections
# ========================================================================================

	def menuBoxCarteSections(self):

		groupBoxSections = QtWidgets.QGroupBox('Tronçons sur la Carte', self.mainMenu)
		groupBoxSections.setStyleSheet(DSTY.styleBox)

#	Sections tout compris sur la carte 
		
		TBUT.createLabelBlackButton(groupBoxSections, 1, 1, 'Tronçons Carte', 'Normal')
		self.activeMapSectionsGlobalInfo = TBUT.createLabelGreenButton(groupBoxSections, 2, 1, '. . .', 'Normal', 'Normal')
		
#	Sections effectives sur la carte 
		
		TBUT.createLabelBlackButton(groupBoxSections, 1, 2, 'Tronçons Utilisés', 'Normal')
		self.activeMapSectionsUsedInfo = TBUT.createLabelGreenButton(groupBoxSections, 2, 2, '. . .', 'Normal', 'Normal')

		TBUT.createLabelBlackButton(groupBoxSections, 3, 2, 'Tronçons substitués', 'Normal')
		self.activeMapSectionsSustituedInfo = TBUT.createLabelGreenButton(groupBoxSections, 4, 2, '. . .', 'Normal', 'Normal')
	
#	Sections combinées sur la carte 
		
		TBUT.createLabelBlackButton(groupBoxSections, 1, 3, 'Tronçons Assemblés', 'Normal')
		self.activeMapSectionsMergedInfo = TBUT.createLabelGreenButton(groupBoxSections, 2, 3, '. . .', 'Normal', 'Normal')
			
#	Symbologie		

		TBUT.createLabelBlackButton(groupBoxSections, 3, 3, 'Symbologie', 'Normal')
		self.activeMapSymbologyCombo = TBUT.createComboButton(groupBoxSections, 4, 3, 'Normal')
		self.activeMapSymbologyCombo.addItem('Automatique')
		for symbology in DSYM.dicoSymbology:
			self.activeMapSymbologyCombo.addItem(symbology)
			
		buttonHelpSymbology = TBUT.createHelpButton(groupBoxSections, 3, 1, 'Aide Symbologie', 'Normal')
		buttonHelpSymbology.clicked.connect(self.buttonHelpSymbology_clicked)			
			
			
#	Bouton Aide

		buttonHelpSections = TBUT.createHelpButton(groupBoxSections, 4, 1, 'Aide Sections', 'Normal')
#		buttonHelpSections.clicked.connect(self.buttonHelpSections_clicked)

#	Boutons Actions

		self.buttonStyleSectionsReload = TBUT.createActionButton(groupBoxSections, 1, 4, 'MAJ Style', 'Normal')
		self.buttonStyleSectionsReload.clicked.connect(self.buttonSectionsMAJStyle_clicked)
			
		buttonSectionsLoad = TBUT.createActionButton(groupBoxSections, 3, 4, 'Charger Tronçons', 'Normal')
		buttonSectionsLoad.clicked.connect(self.buttonSectionsLoad_clicked)
		
# 	Terminé

		groupBoxSections.repaint()

		return groupBoxSections				
		
				
	def buttonHelpSymbology_clicked(self):
		webbrowser.open_new_tab(QGP.configMenuHelpBasePath + 'QCarto - Symbologie - Cartes Topo.html')	
		
		
# ========================================================================================
# Cadre : Export
# ========================================================================================

	def menuBoxCarteExport(self):

		groupBoxExport = QtWidgets.QGroupBox('Export Image Carte', self.mainMenu)
		groupBoxExport.setStyleSheet(DSTY.styleBox)
		
#	Choix du Fond de Carte

		TBUT.createLabelBlackButton(groupBoxExport, 1, 1, 'Choix du Fond', 'Normal')
		self.activeMapExportBackgroundCombo = TBUT.createComboButton(groupBoxExport, 2, 1, 'Normal')
		for background in QGP.configDicoExportBackground:
			self.activeMapExportBackgroundCombo.addItem(background)
		self.activeMapExportBackgroundCombo.currentTextChanged.connect(self.activeMapExportBackgroundInfoChanged)
		self.activeMapExportBackgroundInfo = TBUT.createLabelGreenButton(groupBoxExport, 3, 1, '. . .', 'Normal', 'Normal')
		
#	Choix du Fond de Carte OSM

		TBUT.createLabelBlackButton(groupBoxExport, 1, 2, 'Fond OSM', 'Normal')
		self.exportOsmCombo = TBUT.createComboButton(groupBoxExport, 2, 2, 'Double')
			
#	DPI / Opacité		
		
		TBUT.createLabelBlackButton(groupBoxExport, 1, 3, 'DPI / Opacité', 'Normal')
		
		self.activeMapExportDpiCombo = TBUT.createComboButton(groupBoxExport, 2, 3, 'Normal')
		for dpi in QGP.configExportDpiList:
			self.activeMapExportDpiCombo.addItem(str(dpi))

		self.activeMapExportOpacityCombo = TBUT.createComboButton(groupBoxExport, 3, 3, 'Normal')
		for opacity in QGP.configExportOpacityList:
			self.activeMapExportOpacityCombo.addItem(str(opacity))
	
#	Décorations 
		
		TBUT.createLabelBlackButton(groupBoxExport, 1, 4, 'Copyright / Nom', 'Normal')
		
		self.activeMapExportDecorationOption = TBUT.createCheckBoxButton(groupBoxExport, 2, 4, 'Décorations', 'Normal')
		
#	Grille 
		
		TBUT.createLabelBlackButton(groupBoxExport, 1, 5, 'Grille UTM', 'Normal')

		self.activeMapExportGridOption = TBUT.createCheckBoxButton(groupBoxExport, 2, 5, 'Grille', 'Normal')
		
#	Mode draft

		TBUT.createLabelBlackButton(groupBoxExport, 1, 6, 'Mode draft', 'Normal')
		
		self.activeMapExportDraftOption = TBUT.createCheckBoxButton(groupBoxExport, 2, 6, 'Draft', 'Normal')
		self.activeMapExportDraftOption.setCheckState(Qt.Checked)
			
#	Nombre de pavés	et taille	
			
		TBUT.createLabelBlackButton(groupBoxExport, 3, 4, 'Tuiles', 'Normal')
		self.activeMapExportCountInfo = TBUT.createLabelGreenButton(groupBoxExport, 4, 4, '. . .', 'Normal', 'Normal')

		TBUT.createLabelBlackButton(groupBoxExport, 3, 5, 'Taille', 'Normal')
		self.activeMapExportTileSizeInfo = TBUT.createLabelGreenButton(groupBoxExport, 4, 5, '. . .', 'Normal', 'Normal')

		TBUT.createLabelBlackButton(groupBoxExport, 3, 6, 'Export en cours', 'Normal')
		self.activeMapExportTileCurrentInfo = TBUT.createLabelGreenButton(groupBoxExport, 4, 6, '. . .', 'Normal', 'Normal')

	
#	Boutons Actions		

		buttonExportPlan = TBUT.createActionButton(groupBoxExport, 2, 7, 'Export Schéma', 'Normal')
		buttonExportPlan.clicked.connect(self.buttonExportSchema_clicked)

		buttonExportTopo = TBUT.createActionButton(groupBoxExport, 3, 7, 'Export Topo', 'Normal')
		buttonExportTopo.clicked.connect(self.buttonExportTopo_clicked)

		buttonExportPDF = TBUT.createActionButton(groupBoxExport, 4, 7, 'Export PDF', 'Normal')
		buttonExportPDF.clicked.connect(self.buttonExportPDF_clicked)
		
#	Boutons Aide

		buttonHelpExport = TBUT.createHelpButton(groupBoxExport, 4, 1, 'Aide Export', 'Normal')
		buttonHelpExport.clicked.connect(self.buttonHelpExport_clicked)		
		
		buttonHelpSeeMap = TBUT.createHelpButton(groupBoxExport, 1, 7, 'Voir Carte', 'Normal')
		buttonHelpSeeMap.clicked.connect(self.buttonHelpViewMap_clicked)		
		
# 	Terminé

		groupBoxExport.repaint()

		return groupBoxExport				
			

	def buttonHelpExport_clicked(self):
		webbrowser.open_new_tab(QGP.configMenuHelpBasePath + 'QCarto - Carte Active - Export.html')			
				
				
# ========================================================================================
# Class pour définir l'action quand un bouton décoration est cliqué
# ========================================================================================

class buttonDecoration_clicked:
	def __init__(self, parentFrame, type, position):
		self.parentFrame = parentFrame
		self.type = type
		self.position = position
	def __call__(self):
		self.parentFrame.decorationPositionChanged(self.type, self.position)


# ========================================================================================
# --- THE END ---
# ========================================================================================
	