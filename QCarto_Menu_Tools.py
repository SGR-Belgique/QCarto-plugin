# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Gestion des Menus : Page Outils
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
importlib.reload(LTRK)
import QCarto_Definitions_Styles as DSTY

import QCarto_Tools_CSV as TCSV
import QCarto_Tools_Coding as TCOD
import QCarto_Tools_Dates as TDAT
import QCarto_Tools_Layers as TLAY
import QCarto_Tools_Buttons as TBUT
import QCarto_Tools_Geometries as TGEO
import QCarto_Tools_Progress as TPRO

import QCarto_Menu_CreateGPX as PGPX
importlib.reload(PGPX)

import QCarto_Process_DownloadOsm as SOSMD
importlib.reload(SOSMD)
import QCarto_Process_CreateOsm as SOSMC
importlib.reload(SOSMC)

import QCarto_Parameters_Global
QGP = QCarto_Parameters_Global.globalParameters()

C_DicoPage_Frame = 5


# ========================================================================================
# Class : menuToolsFrame
# >>> iface
# >>> mainMenu 						: Widget of Main Menu
# >>> mainFrame 					: Main Menu Object
# ========================================================================================

class menuToolsFrame:

	def __init__(self, iface, mainMenu, mainFrame):

# 	Paramètres fournis

		self.iface = iface
		self.mainMenu = mainMenu
		self.mainFrame = mainFrame

#	Nom de la page

		self.pageName = 'Outils'

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
		self.listTracksRICodes  = LTRK.getOrderedListItineraryRB({'RI'}, self.mainFrame.dicoTracksRBFeatures)
		self.listTracksIRCodes  = LTRK.getOrderedListItineraryRB({'IR'}, self.mainFrame.dicoTracksRBFeatures)

#	Variables Locales 

		self.deltaHausdorffDico = {}
		self.srcCode = None
		self.dstCode = None		
		self.srcCodeType = None
		self.dstCodeType = None		
		self.selectedSrcTable = None
		self.selectedDstTable = None

		self.targetTrackSrcFeaturesList = []
		self.targetTrackDstFeaturesList = []
		self.targetSectionSrcFeaturesList = []
		self.targetSectionDstFeaturesList = []
		self.targetRepereSrcFeaturesList = []
		self.targetRepereDstFeaturesList = []
		
		self.trackManagementConfirmPending = False

# 	Création des sous-menus

		self.boxesList = []
		self.createMenuBoxes()

		self.mainFrame.setStatusDone('Page des ' + self.pageName + ' créée !')
		

	def createMenuBoxes(self):

		self.groupBoxSelect = self.menuBoxSelectSections()
		DSTY.setBoxGeometry(self.groupBoxSelect, 1, 4, 8, 1)
		self.boxesList.append(self.groupBoxSelect)

		self.groupBoxConvertGPX = self.menuBoxConvertGPX()
		DSTY.setBoxGeometry(self.groupBoxConvertGPX, 1, 6, 5, 2)
		self.boxesList.append(self.groupBoxConvertGPX)

		self.groupBoxExportPOI = self.menuBoxExportPOI()
		DSTY.setBoxGeometry(self.groupBoxExportPOI, 1, 9, 5, 2)
		self.boxesList.append(self.groupBoxExportPOI)

		self.groupBoxTrackManagement = self.menuBoxTrackManagement()
		DSTY.setBoxGeometry(self.groupBoxTrackManagement, 1, 12, 5, 8)
		self.boxesList.append(self.groupBoxTrackManagement)

		self.groupBoxTrackManagementMode = self.menuBoxTrackManagementMode()
		DSTY.setBoxGeometry(self.groupBoxTrackManagementMode, 1, 12, 4, 1)
		self.boxesList.append(self.groupBoxTrackManagementMode)

		self.groupBoxRelationOsm = self.menuBoxRelationOsm()
		DSTY.setBoxGeometry(self.groupBoxRelationOsm, 1, 21, 5, 4)
		self.boxesList.append(self.groupBoxRelationOsm)

		self.groupBoxCreateGPX = self.menuBoxCreateGPX()
		DSTY.setBoxGeometry(self.groupBoxCreateGPX, 6, 6, 3, 1)
		self.boxesList.append(self.groupBoxCreateGPX)

		self.groupBoxAttachPoints = self.menuBoxAttachPoints()
		DSTY.setBoxGeometry(self.groupBoxAttachPoints, 6, 8, 3, 6)
		self.boxesList.append(self.groupBoxAttachPoints)

		self.groupBoxCutSections = self.menuBoxCutSections()
		DSTY.setBoxGeometry(self.groupBoxCutSections, 6, 15, 3, 6)
		self.boxesList.append(self.groupBoxCutSections)

		self.groupBoxHighlightModifications = self.menuBoxHighlightModifications()
		DSTY.setBoxGeometry(self.groupBoxHighlightModifications, 6, 22, 3, 3)
		self.boxesList.append(self.groupBoxHighlightModifications)


# ========================================================================================
# Actions : A la demande de la fenêtre principale
# ========================================================================================

#	Show - Ouverture de cette fenêtre

	def show(self):
		for box in self.boxesList: box.show(), box.repaint()
		self.refreshComboGPXInfo()
		self.refreshInfoGPX()
		self.refreshComboPOIInfo()
		self.refreshInfoPOI()
		self.refreshInfoOSM()
		self.refreshInfoAttachPoints()
		self.refreshInfoCutSections()
		
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
# Actions Select / Zoom Tronçons GR
#
# ========================================================================================
# ========================================================================================

	def buttonSelectSectionsGR_clicked(self):
		idList = self.getCleanIdList()
		print(str(idList))
		self.layerSectionsGR.selectByIds(idList)
			
	def buttonZoomSectionsGR_clicked(self):
		idList = self.getCleanIdList()
		self.layerSectionsGR.selectByIds(idList)
		self.iface.mapCanvas().zoomToSelected(self.layerSectionsGR)
	
	def getCleanIdList(self):
		idList = self.selectIdInputButton.text()
		idList = idList.replace('et',' ')
		idList = idList.replace('ou',' ')
		idList = idList.replace('+',' ')
		idList = idList.replace('-',' ')
		idList = idList.replace(',',' ')
		idList = idList.replace(';',' ')
		idList = idList.replace('[','')
		idList = idList.replace(']','')
		idList = idList.replace('{','')
		idList = idList.replace('}','')

		return [int(id) for id in idList.split() if id.isdigit()]


# ========================================================================================
# ========================================================================================
#
# Actions Conversions GPX > Shape 3812
#
# ========================================================================================
# ========================================================================================

	def refreshComboGPXInfo(self):
		crs4326 = QgsCoordinateReferenceSystem()
		crs4326.createFromString("EPSG:4326")
		self.layerGPXCombo.clear()
		self.layerGPXCombo.addItem('')
		root = QgsProject.instance().layerTreeRoot()
		for L in root.findLayers():
			try:
				if(L.layer().geometryType() != 1): continue
				if(L.layer().crs() != crs4326): continue
				self.layerGPXCombo.addItem(L.name())
			except:
				continue			


	def refreshInfoGPX(self):
		layerName = self.layerGPXCombo.currentText()
		try:
			layerGPX = QgsProject.instance().mapLayersByName(layerName)[0]
			tracksCount = layerGPX.featureCount()
			textCount = DSTY.textFormatBlackNormal.replace('%TEXT%',str(tracksCount) + ' Tracé.s')
			self.buttonTracksGPXCount.setText(textCount)
			DSTY.setStyleOkLabel(self.buttonTracksGPXCount, 'Normal')
			segmentsCount = [len(f.geometry().asMultiPolyline()) for f in layerGPX.getFeatures()]
			textCount = DSTY.textFormatBlackNormal.replace('%TEXT%','-'.join([str(_) for _ in segmentsCount]) + ' Tronçon.s')
			self.buttonSectionsGPXCount.setText(textCount)
			DSTY.setStyleOkLabel(self.buttonSectionsGPXCount, 'Double')
		except:
			textCount = DSTY.textFormatBlackNormal.replace('%TEXT%','X X X')
			self.buttonTracksGPXCount.setText(textCount)
			DSTY.setStyleWarningLabel(self.buttonTracksGPXCount, 'Normal')
			self.buttonSectionsGPXCount.setText(textCount)
			DSTY.setStyleWarningLabel(self.buttonSectionsGPXCount, 'Double')


	def buttonTracksGPX2Shape_clicked(self): 
		
#		Ouvrir le shape GPX

		layerNameGPX = self.layerGPXCombo.currentText()
		try:
			layerGPX = QgsProject.instance().mapLayersByName(layerNameGPX)[0]
		except:
			self.mainMenuFrame.setStatusWarning('La couche GPX : ' + str(layerNameGPX) + ' ne peut pas être ouverte ?')
			return
		
#		Ajouter le shape 3812 si pas déjà présent

		layerName3812 = QGP.configGPXShapeLines
		layers3812 = QgsProject.instance().mapLayersByName(layerName3812)
		if layers3812 == []:
			layer3812, errorText = TLAY.loadLayer(QGP.configPathGPXShapes, layerName3812, QGP.configDBCartoGroupName, layerName3812, None, None, False)	
			if errorText != None:
				self.mainMenuFrame.setStatusWarning('Impossible d\'ajouter la couche : ' + layerName3812 + ' - ' + errorText)
				return
		else:
			layer3812 = layers3812[0]

# 	Ajouter les entités depuis le GPX

		layer3812.startEditing()
		layer3812.selectAll()
		layer3812.deleteSelectedFeatures()	
		newCount = 0; trkNum = 1
		
		for trk in layerGPX.getFeatures():
			trkLines = trk.geometry().asMultiPolyline()
			trkName = trk['name'] if trk['name'] != None else '--- Tracé sans nom ---'
			trksegNum = 1
			for trkseg in trkLines:
				line3812 = TGEO.convertLineCrs(trkseg, layerGPX.crs(), layer3812.crs())
				newGeometry = QgsGeometry.fromMultiPolylineXY([line3812])
				newGeometry.simplify(3)
				newFeature = QgsFeature()
				newFeature.setGeometry(newGeometry)
				newFeature.setFields(layer3812.fields())
				newFeature.setAttribute('name', trkName)
				newFeature.setAttribute('trk', trkNum)
				newFeature.setAttribute('trkseg', trksegNum)
				newFeature.setAttribute('points', len(trkseg))
				newFeature.setAttribute('length', newGeometry.length())
				layer3812.addFeature(newFeature)
				self.mainFrame.setStatusWorking(layerName3812 + ' : entité ' + trkName + ' ' + str(trkNum) + '-' + str(trksegNum) + ' ajoutée !')
				newCount += 1; trksegNum += 1
			trkNum += 1
		layer3812.commitChanges()
		self.mainFrame.setStatusDone(layerName3812 + ' : ' + str(newCount) + ' entité.s ajoutée.s !')


# ========================================================================================
# ========================================================================================
#
# Actions Conversions GPX > POI
#
# ========================================================================================
# ========================================================================================

	def refreshComboPOIInfo(self):
		crs4326 = QgsCoordinateReferenceSystem()
		crs4326.createFromString("EPSG:4326")
		self.layerPOICombo.clear()
		self.layerPOICombo.addItem('')
		root = QgsProject.instance().layerTreeRoot()
		for L in root.findLayers():
			try:
				if(L.layer().geometryType() != 0): continue
				if(L.layer().crs() != crs4326): continue
				self.layerPOICombo.addItem(L.name())
			except:
				continue			


	def refreshInfoPOI(self):
		layerName = self.layerPOICombo.currentText()
		try:
			layerPOI = QgsProject.instance().mapLayersByName(layerName)[0]
			pointsCount = layerPOI.featureCount()
			pointsSelectedCount = layerPOI.selectedFeatureCount()
			textCount = DSTY.textFormatBlackNormal.replace('%TEXT%',str(pointsCount) + ' (' + str(pointsSelectedCount) + ') POIs')
			self.buttonPOICount.setText(textCount)
			DSTY.setStyleOkLabel(self.buttonPOICount, 'Normal')
		except:
			textCount = DSTY.textFormatBlackNormal.replace('%TEXT%','X X X')
			self.buttonPOICount.setText(textCount)
			DSTY.setStyleWarningLabel(self.buttonPOICount, 'Normal')


	def buttonPOI2CSV_clicked(self): 
		
		if self.layerPOICombo.currentText().strip() == '':
			self.mainFrame.setStatusWarning('Vous devez choisir un fichier GPX !')
			return
		
		self.mainFrame.setStatusWorking('Export des POIs en CSV ...')
		
#		Ouvrir le shape GPX

		layerNamePOI = self.layerPOICombo.currentText()
		try:
			layerPOI = QgsProject.instance().mapLayersByName(layerNamePOI)[0]
		except:
			self.mainMenuFrame.setStatusWarning('La couche GPX des POI : ' + str(layerNamePOI) + ' ne peut pas être ouverte ?')
			return
		
# 	Ajouter les entités depuis le GPX

		poiFeatures = [poi for poi in (layerPOI.getSelectedFeatures() if self.selectionOnlyPOI.isChecked() else layerPOI.getFeatures()) ]
		TCSV.exportPoiPoints(QGP.configPathExportPOI, layerNamePOI + ' (' + TDAT.getTimeStamp() + ').csv', poiFeatures)

		self.mainFrame.setStatusDone('POIs exportés : ' + layerNamePOI + ' - OK')


# ========================================================================================
# ========================================================================================
#
# Actions Création GPX
#
# ========================================================================================
# ========================================================================================

	def buttonCreateGPX_clicked(self):
		self.mainFrame.dockMenuCreateGPX = PGPX.createGPXbySections(self.iface, self.mainMenu, self.mainFrame, self.mainFrame.dockMenuCreateGPX)
		self.mainFrame.dockMenuCreateGPX.show()
		self.mainMenu.hide()	


# ========================================================================================
# ========================================================================================
#
# Actions Relation OSM
#
# ========================================================================================
# ========================================================================================

	def refreshInfoOSM(self):

		self.trackCodeForOsm = self.mainFrame.dicoDefinitionPages['Parcours'][C_DicoPage_Frame].trackCodeOsm if self.mainFrame.dicoDefinitionPages['Parcours'][C_DicoPage_Frame] != None else None

		text = DSTY.textFormatBlackNormal.replace('%TEXT%',(self.trackCodeForOsm if self.trackCodeForOsm != None else '. . .'))
		self.buttonTrackOsmCode.setText(text)
		DSTY.setStyleOkLabel(self.buttonTrackOsmCode, 'Normal') if self.trackCodeForOsm != None else DSTY.setStyleWarningLabel(self.buttonTrackOsmCode, 'Normal')

		self.trackOsmidForOsm = self.mainFrame.dicoTracksGRFeatures[self.trackCodeForOsm][QGP.tableTracksFieldOsmid] if (self.trackCodeForOsm != None and self.trackCodeForOsm in self.mainFrame.dicoTracksGRFeatures) else None

		text = DSTY.textFormatBlackNormal.replace('%TEXT%',(self.trackOsmidForOsm if self.trackOsmidForOsm != None else '. . .'))
		self.buttonTrackOsmId.setText(text)
		DSTY.setStyleOkLabel(self.buttonTrackOsmId, 'Normal') if self.trackOsmidForOsm != None else DSTY.setStyleWarningLabel(self.buttonTrackOsmId, 'Normal')

		self.trackNameForOsm = self.mainFrame.dicoTracksGRFeatures[self.trackCodeForOsm][QGP.tableTracksFieldName] if (self.trackCodeForOsm != None and self.trackCodeForOsm in self.mainFrame.dicoTracksGRFeatures) else None

		text = DSTY.textFormatBlackNormal.replace('%TEXT%',(self.trackNameForOsm if self.trackNameForOsm != None else '. . .'))
		self.buttonTrackOsmName.setText(text)
		DSTY.setStyleOkLabel(self.buttonTrackOsmName, 'Double3') if self.trackNameForOsm != None else DSTY.setStyleWarningLabel(self.buttonTrackOsmName, 'Double3')

		text = DSTY.textFormatBlackNormal.replace('%TEXT%', '{:.1f} mètres'.format(self.deltaHausdorffDico[self.trackCodeForOsm]).replace('.',',') if self.trackCodeForOsm in self.deltaHausdorffDico else '. . .')
		self.buttonTrackOsmDelta.setText(text)
		DSTY.setStyleOkLabel(self.buttonTrackOsmDelta, 'Double') if self.trackCodeForOsm in self.deltaHausdorffDico else DSTY.setStyleWarningLabel(self.buttonTrackOsmDelta, 'Double')


	def buttonOsmDownload_clicked(self):
	
		if self.trackCodeForOsm == None:
			self.mainFrame.setStatusWarning('Sélectionnez au préalable un parcours GR via la page Parcours !')
			return
		
		if self.trackOsmidForOsm == None:
			self.mainFrame.setStatusWarning('Le numéro de relation Osm n\'est pas défini dans la table Parcours-GR !')
			return

		SOSMD.downloadRelation(self.mainFrame, TCOD.projectFromTrackCode(self.trackCodeForOsm), self.trackCodeForOsm, self.trackOsmidForOsm)


	def buttonOsmCreate_clicked(self):

		if self.trackCodeForOsm == None:
			self.mainFrame.setStatusWarning('Sélectionnez au préalable un parcours GR via la page Parcours !')
			return
		
		if self.trackOsmidForOsm == None:
			self.mainFrame.setStatusWarning('Le numéro de relation Osm n\'est pas défini dans la table Parcours-GR !')
			return

		delta = SOSMC.createRelation(self.iface, self.mainFrame, TCOD.projectFromTrackCode(self.trackCodeForOsm), self.trackCodeForOsm, self.trackOsmidForOsm)

		if delta != None:
			self.deltaHausdorffDico[self.trackCodeForOsm] = delta
			text = DSTY.textFormatBlackNormal.replace('%TEXT%', '{:.1f} mètres'.format(delta).replace('.',','))
			self.buttonTrackOsmDelta.setText(text)
			DSTY.setStyleOkLabel(self.buttonTrackOsmDelta, 'Double')


# ========================================================================================
# ========================================================================================
#
# Actions : Track Management
#
# ========================================================================================
# ========================================================================================


# ========================================================================================
#	Source / Destination Changed
# ========================================================================================

	def trackManagementSrc_changed(self):

		self.srcCode = self.trackManagementSrcInput.text()
		self.srcCodeType = TCOD.itineraryTypeFromTrackCode(self.srcCode)
		
		if self.srcCodeType in QGP.typeSetTableGR:
			self.selectedSrcTable = 'GR'
		elif self.srcCodeType in QGP.typeSetTableRB:
			self.selectedSrcTable = 'RB'
		else:
			self.selectedSrcTable = None

		if self.srcCode in self.mainFrame.dicoTracksGRFeatures:
			self.trackManagementSrcName.setText(DSTY.textFormatBlackNormal.replace('%TEXT%', str(self.mainFrame.dicoTracksGRFeatures[self.srcCode][QGP.tableTracksFieldName])))
			DSTY.setStyleOkLabel(self.trackManagementSrcName, 'Double3')
		elif self.srcCode in self.mainFrame.dicoTracksRBFeatures:	
			self.trackManagementSrcName.setText(DSTY.textFormatBlackNormal.replace('%TEXT%', str(self.mainFrame.dicoTracksRBFeatures[self.srcCode][QGP.tableTracksFieldName])))
			DSTY.setStyleOkLabel(self.trackManagementSrcName, 'Double3')
		else:
			self.trackManagementSrcName.setText(DSTY.textFormatBlackNormal.replace('%TEXT%', 'Ce code de parcours n\'existe pas (encore)'))
			DSTY.setStyleWarningLabel(self.trackManagementSrcName, 'Double3')
		
		self.trackManagementAny_changed()
		
	def trackManagementDst_changed(self):

		self.dstCode = self.trackManagementDstInput.text()
		self.dstCodeType = TCOD.itineraryTypeFromTrackCode(self.dstCode)
		
		if self.dstCodeType in QGP.typeSetTableGR:
			self.selectedDstTable = 'GR'
		elif self.dstCodeType in QGP.typeSetTableRB:
			self.selectedDstTable = 'RB'
		else:
			self.selectedDstTable = None

		if self.dstCode in self.mainFrame.dicoTracksGRFeatures:
			self.trackManagementDstName.setText(DSTY.textFormatBlackNormal.replace('%TEXT%', str(self.mainFrame.dicoTracksGRFeatures[self.dstCode][QGP.tableTracksFieldName])))
			DSTY.setStyleOkLabel(self.trackManagementDstName, 'Double3')
		elif self.dstCode in self.mainFrame.dicoTracksRBFeatures:	
			self.trackManagementDstName.setText(DSTY.textFormatBlackNormal.replace('%TEXT%', str(self.mainFrame.dicoTracksRBFeatures[self.dstCode][QGP.tableTracksFieldName])))
			DSTY.setStyleOkLabel(self.trackManagementDstName, 'Double3')
		else:
			self.trackManagementDstName.setText(DSTY.textFormatBlackNormal.replace('%TEXT%', 'Ce code de parcours n\'existe pas (encore)'))
			DSTY.setStyleWarningLabel(self.trackManagementDstName, 'Double3')
			
		self.trackManagementAny_changed()


# ========================================================================================
#	Show Target Counters
# ========================================================================================

	def trackManagementAny_changed(self):
	
		if self.srcCode == None : return									# Not yet initialized

#	Find Mode Parcours / Itinerary

		self.selectedMode = 'Parcours' if self.buttonTrackManagementModeTrack.isChecked() else 'Itinerary'
		
#	Détermination des Features Track Source concernées

		self.targetTrackSrcFeaturesList = []

		if self.selectedSrcTable == 'GR' :
			if self.selectedMode == 'Itinerary' :
				self.targetTrackSrcFeaturesList = [self.mainFrame.dicoTracksGRFeatures[code] for code in self.mainFrame.dicoTracksGRFeatures if self.srcCode == TCOD.itineraryFromTrackCode(code)]
			if self.selectedMode == 'Parcours' :
				self.targetTrackSrcFeaturesList = [self.mainFrame.dicoTracksGRFeatures[code] for code in self.mainFrame.dicoTracksGRFeatures if self.srcCode == code]
		if self.selectedSrcTable == 'RB' :
			if self.selectedMode == 'Itinerary' :
				self.targetTrackSrcFeaturesList = [self.mainFrame.dicoTracksRBFeatures[code] for code in self.mainFrame.dicoTracksRBFeatures if self.srcCode == TCOD.itineraryFromTrackCode(code)]
			if self.selectedMode == 'Parcours' :
				self.targetTrackSrcFeaturesList = [self.mainFrame.dicoTracksRBFeatures[code] for code in self.mainFrame.dicoTracksRBFeatures if self.srcCode == code]

		if self.targetSelectionOnlyButton.checkState() == Qt.Checked and self.targetTrackSrcFeaturesList != [] :
			layerTrack = self.layerTracksGR if self.selectedSrcTable == 'GR' else self.layerTracksRB			
			selectedCodes = [trackFeature[QGP.tableTracksFieldCode] for trackFeature in layerTrack.getSelectedFeatures()]
			self.targetTrackSrcFeaturesList = [trackFeature for trackFeature in self.targetTrackSrcFeaturesList if trackFeature[QGP.tableTracksFieldCode] in selectedCodes]

		text = DSTY.textFormatBlackNormal.replace('%TEXT%','{:d} parcours'.format(len(self.targetTrackSrcFeaturesList)))
		self.trackManagementSrcNbrTracks.setText(text)
		DSTY.setStyleOkLabel(self.trackManagementSrcNbrTracks, 'Normal')

		self.targetTracksActiveButton.setCheckState(Qt.Unchecked)	
	
#	Détermination des Features Track Destination concernées

		self.targetTrackDstFeaturesList = []

		if self.selectedDstTable == 'GR' :
			if self.selectedMode == 'Itinerary' :
				self.targetTrackDstFeaturesList = [self.mainFrame.dicoTracksGRFeatures[code] for code in self.mainFrame.dicoTracksGRFeatures if self.dstCode == TCOD.itineraryFromTrackCode(code)]
			if self.selectedMode == 'Parcours' :
				self.targetTrackDstFeaturesList = [self.mainFrame.dicoTracksGRFeatures[code] for code in self.mainFrame.dicoTracksGRFeatures if self.dstCode == code]
		if self.selectedDstTable == 'RB' :
			if self.selectedMode == 'Itinerary' :
				self.targetTrackDstFeaturesList = [self.mainFrame.dicoTracksRBFeatures[code] for code in self.mainFrame.dicoTracksRBFeatures if self.dstCode == TCOD.itineraryFromTrackCode(code)]
			if self.selectedMode == 'Parcours' :
				self.targetTrackDstFeaturesList = [self.mainFrame.dicoTracksRBFeatures[code] for code in self.mainFrame.dicoTracksRBFeatures if self.dstCode == code]

		text = DSTY.textFormatBlackNormal.replace('%TEXT%','{:d} parcours'.format(len(self.targetTrackDstFeaturesList)))
		self.trackManagementDstNbrTracks.setText(text)
		DSTY.setStyleOkLabel(self.trackManagementDstNbrTracks, 'Normal') if len(self.targetTrackDstFeaturesList) == 0 else DSTY.setStyleWarningLabel(self.trackManagementDstNbrTracks, 'Normal')

#	Warning if Tables are incompatibles

		if (self.selectedSrcTable == 'GR' and self.selectedDstTable == 'RB') or (self.selectedSrcTable == 'RB' and self.selectedDstTable == 'GR') :
			self.mainFrame.setStatusWarning('Il n\'est pas possible de copier / renommer à partir de 2 tables différentes')
		else:
			self.mainFrame.setStatusDone('Prêt')

#	Détermination des Features Section Source concernées

		self.targetSectionSrcFeaturesList = []

		for idSection in self.mainFrame.dicoSectionsGRFeatures :
			gr_list = TCOD.getCodeListALLFromSectionFeature(self.mainFrame.dicoSectionsGRFeatures[idSection])
			for gr_code in gr_list:
				valid, type, label, zone, number, itineraryCode, trackBaseCode, trackCode, modificationList, invalidationList, repeatCount, bifurcationNumber, direction = TCOD.elementsFromGrCode(gr_code)		
				if (self.selectedMode == 'Itinerary' and itineraryCode == self.srcCode) or (self.selectedMode == 'Parcours' and trackCode == self.srcCode) :
					self.targetSectionSrcFeaturesList.append(self.mainFrame.dicoSectionsGRFeatures[idSection])
					break
					
		if self.targetSelectionOnlyButton.checkState() == Qt.Checked : 
			layerSection = self.layerSectionsGR
			selectedId = [sectionFeature.id() for sectionFeature in layerSection.getSelectedFeatures()]
			self.targetSectionSrcFeaturesList = [sectionFeature for sectionFeature in self.targetSectionSrcFeaturesList if sectionFeature.id() in selectedId]					
					
		text = DSTY.textFormatBlackNormal.replace('%TEXT%','{:d} tronçons'.format(len(self.targetSectionSrcFeaturesList)))
		self.trackManagementSrcNbrSections.setText(text)
		DSTY.setStyleOkLabel(self.trackManagementSrcNbrSections, 'Normal')

		self.targetSectionsActiveButton.setCheckState(Qt.Unchecked)	

#	Détermination des Features Section Destination concernées

		self.targetSectionDstFeaturesList = []

		for idSection in self.mainFrame.dicoSectionsGRFeatures :
			gr_list = TCOD.grCodeListFromSectionFeature(self.mainFrame.dicoSectionsGRFeatures[idSection], self.dstCodeType)
			for gr_code in gr_list:
				valid, type, label, zone, number, itineraryCode, trackBaseCode, trackCode, modificationList, invalidationList, repeatCount, bifurcationNumber, direction = TCOD.elementsFromGrCode(gr_code)		
				if (self.selectedMode == 'Itinerary' and itineraryCode == self.dstCode) or (self.selectedMode == 'Parcours' and trackCode == self.dstCode) :
					self.targetSectionDstFeaturesList.append(self.mainFrame.dicoSectionsGRFeatures[idSection])
					break
						
		text = DSTY.textFormatBlackNormal.replace('%TEXT%','{:d} tronçons'.format(len(self.targetSectionDstFeaturesList)))
		self.trackManagementDstNbrSections.setText(text)
		DSTY.setStyleOkLabel(self.trackManagementDstNbrSections, 'Normal') if len(self.targetSectionDstFeaturesList) == 0 else DSTY.setStyleWarningLabel(self.trackManagementDstNbrSections, 'Normal')

#	Détermination des Features Repere Source concernées

		self.targetRepereSrcFeaturesList = []

		for idRepere in self.mainFrame.dicoPointsGRFeatures :
			grCode = TCOD.grCodeFromPointFeature(self.mainFrame.dicoPointsGRFeatures[idRepere])
			if (self.selectedMode == 'Itinerary' and TCOD.itineraryFromTrackCode(grCode) == self.srcCode) or (self.selectedMode == 'Parcours' and grCode == self.srcCode) :
				self.targetRepereSrcFeaturesList.append(self.mainFrame.dicoPointsGRFeatures[idRepere])
					
		if self.targetSelectionOnlyButton.checkState() == Qt.Checked : 
			layerPoints = self.layerPointsGR
			selectedId = [repereFeature.id() for repereFeature in layerPoints.getSelectedFeatures()]
			self.targetRepereSrcFeaturesList = [repereFeature for repereFeature in self.targetRepereSrcFeaturesList if repereFeature.id() in selectedId]					
					
		text = DSTY.textFormatBlackNormal.replace('%TEXT%','{:d} repères'.format(len(self.targetRepereSrcFeaturesList)))
		self.trackManagementSrcNbrReperes.setText(text)
		DSTY.setStyleOkLabel(self.trackManagementSrcNbrReperes, 'Normal')

		self.targetReperesActiveButton.setCheckState(Qt.Unchecked)	

#	Détermination des Features Repere Destination concernées

		self.targetRepereDstFeaturesList = []

		for idRepere in self.mainFrame.dicoPointsGRFeatures :
			grCode = TCOD.grCodeFromPointFeature(self.mainFrame.dicoPointsGRFeatures[idRepere])
			if (self.selectedMode == 'Itinerary' and TCOD.itineraryFromTrackCode(grCode) == self.dstCode) or (self.selectedMode == 'Parcours' and grCode == self.dstCode) :
				self.targetRepereDstFeaturesList.append(self.mainFrame.dicoPointsGRFeatures[idRepere])

		text = DSTY.textFormatBlackNormal.replace('%TEXT%','{:d} repères'.format(len(self.targetRepereDstFeaturesList)))
		self.trackManagementDstNbrReperes.setText(text)
		DSTY.setStyleOkLabel(self.trackManagementDstNbrReperes, 'Normal') if len(self.targetRepereDstFeaturesList) == 0 else DSTY.setStyleWarningLabel(self.trackManagementDstNbrReperes, 'Normal')


# ========================================================================================
#	Warnings
# ========================================================================================

	def trackManagementWarning_clear(self):
		self.targetOperationWarning.clear()
		self.targetTracksWarning.clear()
		self.targetSectionsWarning.clear()
		self.targetReperesWarning.clear()

	def trackManagementWarning_operation(self, operation):
		self.targetOperationWarning.clear()
		self.targetOperationWarning.setText(DSTY.textFormatRedNormal.replace('%TEXT%', operation + ' : '))

	def trackManagementWarning_count(self, target, count):
		if target == 'Tracks' : self.targetTracksWarning.setText(DSTY.textFormatRedNormal.replace('%TEXT%', str(count) + ' parcours'))
		if target == 'Sections' : self.targetSectionsWarning.setText(DSTY.textFormatRedNormal.replace('%TEXT%', str(count) + ' tronçons'))
		if target == 'Repères' : self.targetReperesWarning.setText(DSTY.textFormatRedNormal.replace('%TEXT%', str(count) + ' repères'))


# ========================================================================================
#	Vérifications préalables
# ========================================================================================

	def trackManagement_verifications(self, action):
		if self.trackManagementConfirmPending :
			self.mainFrame.setStatusWarning('Vous avez déjà une opération en cours : Annulez ou Confirmez !')
			return 0
			
		totalCount = len(self.targetTrackSrcFeaturesList) if self.targetTracksActiveButton.checkState() == Qt.Checked else 0 
		totalCount += len(self.targetSectionSrcFeaturesList) if self.targetSectionsActiveButton.checkState() == Qt.Checked else 0 
		totalCount += len(self.targetRepereSrcFeaturesList) if self.targetReperesActiveButton.checkState() == Qt.Checked else 0 
		if totalCount == 0 :
			self.mainFrame.setStatusWarning('Il n\'y a aucune opération à effectuer !')
			return 0

		for layer in (self.layerTracksGR, self.layerTracksRB, self.layerSectionsGR, self.layerPointsGR) :
			if layer.isModified() :
				self.mainFrame.setStatusWarning('La table ' + layer.name() + ' est déjà en cours de modification !')
				return 0
		
		if action in ('Supprimer') :
			return totalCount
	
		if action in ('Copier', 'Renommer') :
			if self.dstCode == '' :		
				self.mainFrame.setStatusWarning('Le code de destination est vide !') ; return 0
			if self.dstCode == self.srcCode :
				self.mainFrame.setStatusWarning('Le code de destination est identique au code source !') ; return 0
			valid, type, label, zone, number, itineraryCode, trackBaseCode, trackCode, modificationList, invalidationList, repeatCount, bifurcationNumber, direction = TCOD.elementsFromGrCode(self.dstCode)		
			if not valid :
				self.mainFrame.setStatusWarning('Le code de destination n\'est pas valide') ; return 0
			if not self.trackManagement_areTypesCompatibles() : 
				self.mainFrame.setStatusWarning('Il est impossible de Copier / Renommer entre les Tables Parcours-GR / Parcours-RB') ; return 0
			return totalCount

	def trackManagement_areTypesCompatibles(self) :
		if self.targetTracksActiveButton.checkState() == Qt.Unchecked : return True
		srcType = TCOD.itineraryTypeFromTrackCode(self.srcCode)
		dstType = TCOD.itineraryTypeFromTrackCode(self.dstCode)
		if srcType in QGP.typeSetTableGR and dstType in QGP.typeSetTableRB  : return False
		if srcType in QGP.typeSetTableRB and dstType in QGP.typeSetTableGR  : return False
		return True


# ========================================================================================
#	Action : Rename
# ========================================================================================
	
	def trackManagementRename_clicked(self):
		totalCount = self.trackManagement_verifications('Renommer')
		if totalCount == 0 : return

		progressBar = TPRO.createProgressBar(self.trackManagementButtonRename, totalCount, 'Normal')
		self.trackManagementWarning_clear()
		self.trackManagementWarning_operation('Renommer')

		if self.targetTracksActiveButton.checkState() == Qt.Checked and len(self.targetTrackSrcFeaturesList) > 0 :
			self.mainFrame.setStatusWorking('Renommage des entités dans la table des Parcours ...')
			layerTrack = self.layerTracksGR if self.selectedSrcTable == 'GR' else self.layerTracksRB
			layerTrack.startEditing()
			for trackFeature in self.targetTrackSrcFeaturesList:
				layerTrack.changeAttributeValue(trackFeature.id(), trackFeature.fieldNameIndex(QGP.tableTracksFieldCode), trackFeature[QGP.tableTracksFieldCode].replace(self.srcCode, self.dstCode))
				layerTrack.changeAttributeValue(trackFeature.id(), trackFeature.fieldNameIndex(QGP.tableTracksFieldName), trackFeature[QGP.tableTracksFieldName].replace(self.srcCode, self.dstCode))
				progressBar.setValue(progressBar.value() + 1)
				QgsApplication.processEvents()
			self.trackManagementWarning_count('Tracks', len(self.targetTrackSrcFeaturesList))

		if self.targetSectionsActiveButton.checkState() == Qt.Checked and len(self.targetSectionSrcFeaturesList) > 0 :
			self.mainFrame.setStatusWorking('Renommage dans les codes x_list de la table des Tronçons ...')
			layerSection = self.layerSectionsGR
			layerSection.startEditing()		
			for sectionFeature in self.targetSectionSrcFeaturesList:
				dicoCodeList = TCOD.getCodeDicoFromSectionFeature(sectionFeature)
				newDico = dicoCodeList.copy()
				for xxList in dicoCodeList :
					for code in dicoCodeList[xxList] :
						valid, type, label, zone, number, itineraryCode, trackBaseCode, trackCode, modificationList, invalidationList, repeatCount, bifurcationNumber, direction = TCOD.elementsFromGrCode(code)
						if not valid : continue
						if self.selectedMode == 'Itinerary' and itineraryCode != self.srcCode : continue  													# Not in target : do not change in newDico
						if self.selectedMode == 'Parcours' and trackCode != self.srcCode : continue															# Not in target : do not change in newDico
						if self.selectedMode == 'Itinerary' and itineraryCode == self.srcCode : newCode = code.replace(self.srcCode, self.dstCode)			# Change Itinerary
						if self.selectedMode == 'Parcours' and trackCode == self.srcCode : newCode = code.replace(self.srcCode, self.dstCode)				# Change Itinerary
						newType = TCOD.itineraryTypeFromTrackCode(newCode)
						newList = newType.lower() + '_list' if newType != 'GRP' else 'gr_list'
						newDico[xxList].remove(code)											
						newDico[newList].append(newCode)											
				for xxList in newDico :
					layerSection.changeAttributeValue(sectionFeature.id(), sectionFeature.fieldNameIndex(xxList), '  '.join(newDico[xxList]))
				progressBar.setValue(progressBar.value() + 1)
				QgsApplication.processEvents()
			self.trackManagementWarning_count('Sections', len(self.targetSectionSrcFeaturesList))

		if self.targetReperesActiveButton.checkState() == Qt.Checked and len(self.targetRepereSrcFeaturesList) > 0 :
			self.mainFrame.setStatusWorking('Renommage des entités dans la table des Repères ...')
			layerPoints = self.layerPointsGR
			layerPoints.startEditing()
			for repereFeature in self.targetRepereSrcFeaturesList:
				layerPoints.changeAttributeValue(repereFeature.id(), repereFeature.fieldNameIndex(QGP.tablePointsFieldGRCode), repereFeature[QGP.tablePointsFieldGRCode].replace(self.srcCode, self.dstCode))
				progressBar.setValue(progressBar.value() + 1)
				QgsApplication.processEvents()
			self.trackManagementWarning_count('Repères', len(self.targetRepereSrcFeaturesList))

		self.trackManagementConfirmPending = True
		del progressBar		

		self.mainFrame.setStatusWarning('Tables des Parcours / Tronçons / Repères : Confirmez ou annulez les modifications !')


# ========================================================================================
#	Action : Copy
# ========================================================================================

	def trackManagementCopy_clicked(self):
		totalCount = self.trackManagement_verifications('Copier')
		if totalCount == 0 : return

		progressBar = TPRO.createProgressBar(self.trackManagementButtonCopy, totalCount, 'Normal')
		self.trackManagementWarning_clear()
		self.trackManagementWarning_operation('Copier')

		if self.targetTracksActiveButton.checkState() == Qt.Checked and len(self.targetTrackSrcFeaturesList) > 0 :
			self.mainFrame.setStatusWorking('Copie des entités dans la table des Parcours ...')
			layerTrack = self.layerTracksGR if self.selectedSrcTable == 'GR' else self.layerTracksRB
			layerTrack.startEditing()
			for trackFeature in self.targetTrackSrcFeaturesList:
				newFeature = QgsFeature()
				newFeature.setFields(layerTrack.fields())
				newFeature[QGP.tableTracksFieldCode] = trackFeature[QGP.tableTracksFieldCode].replace(self.srcCode, self.dstCode)
				newFeature[QGP.tableTracksFieldName] = 'Nom et état du parcours à définir !'
				newFeature[QGP.tableTracksFieldStatus] = ''
				layerTrack.addFeature(newFeature)
				progressBar.setValue(progressBar.value() + 1)
				QgsApplication.processEvents()
			self.trackManagementWarning_count('Tracks', len(self.targetTrackSrcFeaturesList))

		if self.targetSectionsActiveButton.checkState() == Qt.Checked and len(self.targetSectionSrcFeaturesList) > 0 :
			self.mainFrame.setStatusWorking('Copie dans les codes x_list de la table des Tronçons ...')
			layerSection = self.layerSectionsGR
			layerSection.startEditing()		
			for sectionFeature in self.targetSectionSrcFeaturesList:
				dicoCodeList = TCOD.getCodeDicoFromSectionFeature(sectionFeature)
				newDico = dicoCodeList.copy()
				for xxList in dicoCodeList :
					for code in dicoCodeList[xxList] :
						valid, type, label, zone, number, itineraryCode, trackBaseCode, trackCode, modificationList, invalidationList, repeatCount, bifurcationNumber, direction = TCOD.elementsFromGrCode(code)
						if not valid : continue
						if self.selectedMode == 'Itinerary' and itineraryCode != self.srcCode : continue  													# Not in target : do not change in newDico
						if self.selectedMode == 'Parcours' and trackCode != self.srcCode : continue															# Not in target : do not change in newDico
						if self.selectedMode == 'Itinerary' and itineraryCode == self.srcCode : newCode = code.replace(self.srcCode, self.dstCode)			# Change Itinerary
						if self.selectedMode == 'Parcours' and trackCode == self.srcCode : newCode = code.replace(self.srcCode, self.dstCode)				# Change Itinerary
						newType = TCOD.itineraryTypeFromTrackCode(newCode)
						newList = newType.lower() + '_list' if newType != 'GRP' else 'gr_list'
						newDico[newList].append(newCode)											
				for xxList in newDico :
					layerSection.changeAttributeValue(sectionFeature.id(), sectionFeature.fieldNameIndex(xxList), '  '.join(newDico[xxList]))
				progressBar.setValue(progressBar.value() + 1)
				QgsApplication.processEvents()
			self.trackManagementWarning_count('Sections', len(self.targetSectionSrcFeaturesList))

		if self.targetReperesActiveButton.checkState() == Qt.Checked and len(self.targetRepereSrcFeaturesList) > 0 :
			self.mainFrame.setStatusWorking('Copie des entités dans la table des Repères ...')
			layerPoints = self.layerPointsGR
			layerPoints.startEditing()
			for repereFeature in self.targetRepereSrcFeaturesList:
				newFeature = QgsFeature(repereFeature)
				newFeature[QGP.tablePointsFieldId] = layerPoints.maximumValue(repereFeature.fieldNameIndex(QGP.tablePointsFieldId)) + 1
				newFeature[QGP.tablePointsFieldGRCode] = repereFeature[QGP.tablePointsFieldGRCode].replace(self.srcCode, self.dstCode)
				layerPoints.addFeature(newFeature)
				progressBar.setValue(progressBar.value() + 1)
				QgsApplication.processEvents()
			self.trackManagementWarning_count('Repères', len(self.targetRepereSrcFeaturesList))

		self.trackManagementConfirmPending = True
		del progressBar		

		self.mainFrame.setStatusWarning('Tables des Parcours / Tronçons / Repères : Confirmez ou annulez les modifications !')


# ========================================================================================
#	Action : Delete
# ========================================================================================
	
	def trackManagementDelete_clicked(self):
		totalCount = self.trackManagement_verifications('Supprimer')
		if totalCount == 0 : return

		progressBar = TPRO.createProgressBar(self.trackManagementButtonDelete, totalCount, 'Normal')
		self.trackManagementWarning_clear()
		self.trackManagementWarning_operation('Suppression')

		if self.targetTracksActiveButton.checkState() == Qt.Checked and len(self.targetTrackSrcFeaturesList) > 0 :
			self.mainFrame.setStatusWorking('Suppressions des entités dans la table des Parcours ...')
			layerTrack = self.layerTracksGR if self.selectedSrcTable == 'GR' else self.layerTracksRB
			layerTrack.startEditing()
			for trackFeature in self.targetTrackSrcFeaturesList:
				layerTrack.deleteFeature(trackFeature.id())
				progressBar.setValue(progressBar.value() + 1)
				QgsApplication.processEvents()
			self.trackManagementWarning_count('Tracks', len(self.targetTrackSrcFeaturesList))

		if self.targetSectionsActiveButton.checkState() == Qt.Checked and len(self.targetSectionSrcFeaturesList) > 0 :
			self.mainFrame.setStatusWorking('Suppressions dans les codes x_list de la table des Tronçons ...')
			layerSection = self.layerSectionsGR
			layerSection.startEditing()		
			for sectionFeature in self.targetSectionSrcFeaturesList:
				dicoCodeList = TCOD.getCodeDicoFromSectionFeature(sectionFeature)
				for xxList in dicoCodeList :
					newList = []
					for code in dicoCodeList[xxList] :
						valid, type, label, zone, number, itineraryCode, trackBaseCode, trackCode, modificationList, invalidationList, repeatCount, bifurcationNumber, direction = TCOD.elementsFromGrCode(code)
						if self.selectedMode == 'Itinerary' and itineraryCode == self.srcCode : continue  		# Removed since not added to newList
						if self.selectedMode == 'Parcours' and self.srcCode == trackCode : continue				# Removed since not added to newList
						newList.append(code)
					layerSection.changeAttributeValue(sectionFeature.id(), sectionFeature.fieldNameIndex(xxList), '  '.join(newList))
					progressBar.setValue(progressBar.value() + 1)
					QgsApplication.processEvents()
			self.trackManagementWarning_count('Sections', len(self.targetSectionSrcFeaturesList))

		if self.targetReperesActiveButton.checkState() == Qt.Checked and len(self.targetRepereSrcFeaturesList) > 0 :
			self.mainFrame.setStatusWorking('Suppressions des entités dans la table des Repères ...')
			layerPoints = self.layerPointsGR
			layerPoints.startEditing()
			for repereFeature in self.targetRepereSrcFeaturesList:
				layerPoints.deleteFeature(repereFeature.id())
				progressBar.setValue(progressBar.value() + 1)
				QgsApplication.processEvents()
			self.trackManagementWarning_count('Repères', len(self.targetRepereSrcFeaturesList))

		self.trackManagementConfirmPending = True
		del progressBar		

		self.mainFrame.setStatusWarning('Tables des Parcours / Tronçons / Repères : Confirmez ou annulez les modifications !')


# ========================================================================================
#	Actions : Annuler / Confirmer
# ========================================================================================
	
	def trackManagementCancel_clicked(self):
		self.mainFrame.setStatusWorking('Annulation ...')
		self.layerTracksGR.rollBack()
		self.layerTracksRB.rollBack()	
		self.layerSectionsGR.rollBack()		
		self.layerPointsGR.rollBack()		
		self.trackManagementWarning_clear()
		self.trackManagementConfirmPending = False
		self.mainFrame.setStatusDone('Tables des Parcours / Tronçons / Repères : Modifications annulées !')

	def trackManagementConfirm_clicked(self):
		if self.targetTracksActiveButton.checkState() == Qt.Checked : 
			self.mainFrame.setStatusWorking('Table de Parcours : enregistrement ...')
			self.layerTracksGR.commitChanges()
			self.layerTracksRB.commitChanges()	
			self.mainFrame.setStatusWorking('Table de Parcours : Modifications enregistrées !')
			TDAT.sleep(500)
		if self.targetSectionsActiveButton.checkState() == Qt.Checked : 
			self.mainFrame.setStatusWorking('Table de Tronçons : enregistrement ...')
			self.layerSectionsGR.commitChanges()
			self.mainFrame.setStatusWorking('Table des Tronçons : Modifications enregistrées !')
			TDAT.sleep(500)
		if self.targetReperesActiveButton.checkState() == Qt.Checked : 
			self.mainFrame.setStatusWorking('Table de Repères : enregistrement ...')
			self.layerPointsGR.commitChanges()
			self.mainFrame.setStatusWorking('Table des Repères : Modifications enregistrées !')
			TDAT.sleep(500)

		self.trackManagementWarning_clear()
		self.trackManagementConfirmPending = False
		self.mainFrame.requestReload()
		self.mainFrame.setStatusDone('Modifications enregistrées et tables rechargées')


# ========================================================================================
#	Actions : Sélections
# ========================================================================================

	def trackManagementSelectSrcTracks_rightClicked(self):
		layerTrack = self.layerTracksGR if self.selectedSrcTable == 'GR' else self.layerTracksRB
		layerTrack.removeSelection()
		layerTrack.selectByIds( [ trackFeature.id() for trackFeature in self.targetTrackSrcFeaturesList  ] )
		self.mainFrame.setStatusDone('Table ' + layerTrack.name() + ' : ' + str(len(self.targetTrackSrcFeaturesList)) + ' parcours sélectionnés')

	def trackManagementSelectDstTracks_rightClicked(self):
		layerTrack = self.layerTracksGR if self.selectedSrcTable == 'GR' else self.layerTracksRB
		layerTrack.removeSelection()
		layerTrack.selectByIds( [ trackFeature.id() for trackFeature in self.targetTrackDstFeaturesList  ] )
		self.mainFrame.setStatusDone('Table ' + layerTrack.name() + ' : ' + str(len(self.targetTrackDstFeaturesList)) + ' parcours sélectionnés')

	def trackManagementSelectSrcSections_rightClicked(self):
		layerSection = self.layerSectionsGR
		layerSection.removeSelection()
		layerSection.selectByIds( [ sectionFeature.id() for sectionFeature in self.targetSectionSrcFeaturesList  ] )
		self.mainFrame.setStatusDone('Table ' + layerSection.name() + ' : ' + str(len(self.targetSectionSrcFeaturesList)) + ' tronçons sélectionnés')

	def trackManagementSelectDstSections_rightClicked(self):
		layerSection = self.layerSectionsGR
		layerSection.removeSelection()
		layerSection.selectByIds( [ sectionFeature.id() for sectionFeature in self.targetSectionDstFeaturesList  ] )
		self.mainFrame.setStatusDone('Table ' + layerSection.name() + ' : ' + str(len(self.targetSectionDstFeaturesList)) + ' tronçons sélectionnés')

	def trackManagementSelectSrcReperes_rightClicked(self):
		layerPoint = self.layerPointsGR
		layerPoint.removeSelection()
		layerPoint.selectByIds( [ repereFeature.id() for repereFeature in self.targetRepereSrcFeaturesList  ] )
		self.mainFrame.setStatusDone('Table ' + layerPoint.name() + ' : ' + str(len(self.targetRepereSrcFeaturesList)) + ' repères sélectionnés')

	def trackManagementSelectDstReperes_rightClicked(self):
		layerPoint = self.layerPointsGR
		layerPoint.removeSelection()
		layerPoint.selectByIds( [ repereFeature.id() for repereFeature in self.targetRepereDstFeaturesList  ] )
		self.mainFrame.setStatusDone('Table ' + layerPoint.name() + ' : ' + str(len(self.targetRepereDstFeaturesList)) + ' repères sélectionnés')


# ========================================================================================
# ========================================================================================
#
# Actions : Attacher Repères
#
# ========================================================================================
# ========================================================================================

	def refreshInfoAttachPoints(self):
		text = DSTY.textFormatBlackNormal.replace('%TEXT%','{:d} repères'.format(self.layerPointsGR.selectedFeatureCount()))
		self.attachPointsSelectedCount.setText(text)
		DSTY.setStyleOkLabel(self.attachPointsSelectedCount, 'Normal')	
		
		text = DSTY.textFormatBlackNormal.replace('%TEXT%','. . .')
		for label in (self.attachPointsAlreadyAttachedCount, self.attachPointsNoSectionCount, self.attachPointsMultipleSectionCount, self.attachPointsTooFarSectionCount, self.attachPointsUnchangedCount, self.attachPointsAttachedCount) :
			label.setText(text)
			DSTY.setStyleWarningLabel(label, 'Normal')
	

	def buttonAttachPoints_clicked(self):
	
		self.mainFrame.setStatusWorking('Déplacement des repères sélectionnés sur un Tronçon compatible ...')
		self.refreshInfoAttachPoints()
		progressBar = TPRO.createProgressBar(self.buttonAttachPoints, self.layerPointsGR.selectedFeatureCount(), 'Normal')		
		self.attachPointsListAlreadyAttached = [] ; self.attachPointsListAttached = [] ; self.attachPointsListUnchanged = [] ; self.attachPointsListNoSection = [] ; self.attachPointsListMultipleSection = [] ; self.attachPointsListTooFarSection = []
		self.layerPointsGR.startEditing()

		for pointFeature in self.layerPointsGR.getSelectedFeatures() :
			progressBar.setValue(progressBar.value() + 1)
			QgsApplication.processEvents()
			point = pointFeature.geometry().asPoint()
			pointItinerary = TCOD.itineraryFromTrackCode(TCOD.grCodeFromPointFeature(pointFeature))
			closeArea = QgsRectangle(point.x() - QGP.C_ToolsMaxDistanceForAttachPoint, point.y() - QGP.C_ToolsMaxDistanceForAttachPoint, point.x() + QGP.C_ToolsMaxDistanceForAttachPoint, point.y() + QGP.C_ToolsMaxDistanceForAttachPoint)
			closeSections = [ section for section in self.layerSectionsGR.getFeatures(closeArea) ]
			closeSections = [ section for section in closeSections if pointItinerary in [TCOD.elementsFromGrCode(code)[5] for code in TCOD.getCodeListALLFromSectionFeature(section)] ]
			if len(closeSections) == 0 : self.attachPointsListUnchanged.append(pointFeature); self.attachPointsListNoSection.append(pointFeature); continue
			if len(closeSections) > 1 :
				for section in closeSections :																					# Search if at least one vertex is very close to point ...
					sectionPoint, indexPoint, iP, iN, distance2Section2 = section.geometry().closestVertex(point) 	
					if distance2Section2 <= QGP.C_ToolsCloseDistanceForAttachPoint ** 2 : closeSections = [section] ; break
			if len(closeSections) > 1  : self.attachPointsListUnchanged.append(pointFeature); self.attachPointsListMultipleSection.append(pointFeature); continue
			sectionPoint, indexPoint, iP, iN, distance2Section2 = closeSections[0].geometry().closestVertex(point) 
			if distance2Section2 == 0 : self.attachPointsListUnchanged.append(pointFeature); self.attachPointsListAlreadyAttached.append(pointFeature); continue
			if distance2Section2 > QGP.C_ToolsMaxDistanceForAttachPoint ** 2 : self.attachPointsListUnchanged.append(pointFeature); self.attachPointsListTooFarSection.append(pointFeature); continue
			self.layerPointsGR.changeGeometry(pointFeature.id(), QgsGeometry.fromPointXY(sectionPoint))
			self.attachPointsListAttached.append(pointFeature)

		self.layerPointsGR.commitChanges()
		del progressBar
		
		text = DSTY.textFormatBlackNormal.replace('%TEXT%','{:d} repères'.format(len(self.attachPointsListAlreadyAttached)))
		self.attachPointsAlreadyAttachedCount.setText(text)
		DSTY.setStyleOkLabel(self.attachPointsAlreadyAttachedCount, 'Normal')
	
		text = DSTY.textFormatBlackNormal.replace('%TEXT%','{:d} repères'.format(len(self.attachPointsListNoSection)))
		self.attachPointsNoSectionCount.setText(text)
		DSTY.setStyleWarningLabel(self.attachPointsNoSectionCount, 'Normal') if len(self.attachPointsListNoSection) > 0 else DSTY.setStyleOkLabel(self.attachPointsNoSectionCount, 'Normal')	
		
		text = DSTY.textFormatBlackNormal.replace('%TEXT%','{:d} repères'.format(len(self.attachPointsListMultipleSection)))
		self.attachPointsMultipleSectionCount.setText(text)
		DSTY.setStyleWarningLabel(self.attachPointsMultipleSectionCount, 'Normal') if len(self.attachPointsListMultipleSection) > 0 else DSTY.setStyleOkLabel(self.attachPointsMultipleSectionCount, 'Normal')	
		
		text = DSTY.textFormatBlackNormal.replace('%TEXT%','{:d} repères'.format(len(self.attachPointsListTooFarSection)))
		self.attachPointsTooFarSectionCount.setText(text)
		DSTY.setStyleWarningLabel(self.attachPointsTooFarSectionCount, 'Normal') if len(self.attachPointsListTooFarSection) > 0 else DSTY.setStyleOkLabel(self.attachPointsTooFarSectionCount, 'Normal')	
	
		text = DSTY.textFormatBlackNormal.replace('%TEXT%','{:d} repères'.format(len(self.attachPointsListUnchanged)))
		self.attachPointsUnchangedCount.setText(text)
		DSTY.setStyleOkLabel(self.attachPointsUnchangedCount, 'Normal')

		text = DSTY.textFormatBlackNormal.replace('%TEXT%','{:d} repères'.format(len(self.attachPointsListAttached)))
		self.attachPointsAttachedCount.setText(text)
		DSTY.setStyleOkLabel(self.attachPointsAttachedCount, 'Normal') 

		self.mainFrame.setStatusDone('Déplacement des repères sélectionnés sur un Tronçon compatible - OK')


	def buttonAttachPointsAlreadyAttached_clicked(self):
		self.layerPointsGR.selectByIds( [ pointFeature.id() for pointFeature in self.attachPointsListAlreadyAttached ] )
		self.mainFrame.setStatusInfo('Table Repères-GR : repères correspondants sélectionnés !')

	def buttonAttachPointsNoSection_clicked(self):
		self.layerPointsGR.selectByIds( [ pointFeature.id() for pointFeature in self.attachPointsListNoSection ] )
		self.mainFrame.setStatusInfo('Table Repères-GR : repères correspondants sélectionnés !')
	
	def buttonAttachPointsMultipleSection_clicked(self):
		self.layerPointsGR.selectByIds( [ pointFeature.id() for pointFeature in self.attachPointsListMultipleSection ] )
		self.mainFrame.setStatusInfo('Table Repères-GR : repères correspondants sélectionnés !')

	def buttonAttachPointsToFarSection_clicked(self):
		self.layerPointsGR.selectByIds( [ pointFeature.id() for pointFeature in self.attachPointsListTooFarSection ] )
		self.mainFrame.setStatusInfo('Table Repères-GR : repères correspondants sélectionnés !')
	
	def buttonAttachPointsUnchanged_clicked(self):
		self.layerPointsGR.selectByIds( [ pointFeature.id() for pointFeature in self.attachPointsListUnchanged ] )
		self.mainFrame.setStatusInfo('Table Repères-GR : repères correspondants sélectionnés !')
	
	def buttonAttachPointsAttached_clicked(self):
		self.layerPointsGR.selectByIds( [ pointFeature.id() for pointFeature in self.attachPointsListAttached ] )
		self.mainFrame.setStatusInfo('Table Repères-GR : repères correspondants sélectionnés !')
	

# ========================================================================================
# ========================================================================================
#
# Actions : Couper Sections
#
# ========================================================================================
# ========================================================================================

	def refreshInfoCutSections(self):
		text = DSTY.textFormatBlackNormal.replace('%TEXT%','{:d} repères'.format(self.layerPointsGR.selectedFeatureCount()))
		self.cutSectionsPointsSelectedCount.setText(text)
		DSTY.setStyleOkLabel(self.cutSectionsPointsSelectedCount, 'Normal')	
	
		text = DSTY.textFormatBlackNormal.replace('%TEXT%','. . .')
		for label in (self.cutSectionsAlreadyCutCount, self.cutSectionsDetachedCount, self.cutSectionsTooShortCount, self.cutSectionsCode1orYCount, self.cutSectionsMultipleCount, self.cutSectionsUnchangedCount, self.cutSectionsCutCount) :
			label.setText(text)
			DSTY.setStyleWarningLabel(label, 'Normal')
		
	
	def buttonCutSections_clicked(self):
	
		if self.layerSectionsGR.isModified():
			self.mainFrame.setStatusWarning('La couche Tronçons-GR est déjà en cours de modification !')
			return
	
		self.mainFrame.setStatusWorking('Découpage des Tronçons au niveau des repères sélectionnés ...')
		self.refreshInfoCutSections()
		progressBar = TPRO.createProgressBar(self.buttonCutSections, self.layerPointsGR.selectedFeatureCount(), 'Normal')		
		self.cutSectionsListAlreadyCut = [] ; self.cutSectionsListDetached = [] ; self.cutSectionsListTooShort = [] ;  self.cutSectionsListCode1orY = [] ;  self.cutSectionsListMultiple = [] ;  self.cutSectionsListCut = [] ;  self.cutSectionsListUnchanged = [] 
		self.layerSectionsGR.startEditing()

		for pointFeature in self.layerPointsGR.getSelectedFeatures() :
			progressBar.setValue(progressBar.value() + 1)
			QgsApplication.processEvents()
			pointXY = pointFeature.geometry().asPoint()
			pointItinerary = TCOD.itineraryFromTrackCode(TCOD.grCodeFromPointFeature(pointFeature))

			closeArea = QgsRectangle(pointXY.x() - QGP.C_ToolsMaxDistanceForAttachPoint, pointXY.y() - QGP.C_ToolsMaxDistanceForAttachPoint, pointXY.x() + QGP.C_ToolsMaxDistanceForAttachPoint, pointXY.y() + QGP.C_ToolsMaxDistanceForAttachPoint)
			closeSections = [ section for section in self.layerSectionsGR.getFeatures(closeArea) ]
			if self.mainFrame.debugModeQCartoLevel == 3 : print('Repère = ' + str(pointFeature[QGP.tablePointsFieldRepere]) + ' - Close 1° = ' + str(len(closeSections)))
			closeSections = [ section for section in closeSections if pointItinerary in [TCOD.elementsFromGrCode(code)[5] for code in TCOD.getCodeListALLFromSectionFeature(section)] ]
			if self.mainFrame.debugModeQCartoLevel == 3 : print('Repère = ' + str(pointFeature[QGP.tablePointsFieldRepere]) + ' - Close 2° = ' + str(len(closeSections)))
			if len(closeSections) == 0 : self.cutSectionsListUnchanged.append(pointFeature); self.cutSectionsListDetached.append(pointFeature); continue

			if any(pointXY in [section.geometry().asMultiPolyline()[0][0], section.geometry().asMultiPolyline()[0][-1]] for section in closeSections) : \
				self.cutSectionsListUnchanged.append(pointFeature); self.cutSectionsListAlreadyCut.append(pointFeature); continue			

			closeSections = [ section for section in closeSections if section.geometry().closestVertex(pointXY)[4] == 0]
			if self.mainFrame.debugModeQCartoLevel == 3 : print('Repère = ' + str(pointFeature[QGP.tablePointsFieldRepere]) + ' - Close 3° = ' + str(len(closeSections)))
			if len(closeSections) == 0 : self.cutSectionsListUnchanged.append(pointFeature); self.cutSectionsListDetached.append(pointFeature); continue
			if len(closeSections) > 1 : self.cutSectionsListUnchanged.append(pointFeature); self.cutSectionsListMultiple.append(pointFeature); continue

			targetSection = closeSections[0]; targetSectionValid = True
			for gr_code in TCOD.getCodeListALLFromSectionFeature(targetSection) :
				valid, type, label, zone, number, itineraryCode, trackBaseCode, trackCode, modificationList, invalidationList, repeatCount, bifurcationNumber, direction = TCOD.elementsFromGrCode(gr_code)		
				if direction != None : self.cutSectionsListUnchanged.append(pointFeature); self.cutSectionsListCode1orY.append(pointFeature); targetSectionValid = False; break
				if bifurcationNumber != QGP.C_ComputeTrackBifurcationDefault : self.cutSectionsListUnchanged.append(pointFeature); self.cutSectionsListCode1orY.append(pointFeature); targetSectionValid = False; break
			if not targetSectionValid : continue
			
			sectionPoint, indexPoint, iPrevious, iNext, distance2Section2 = targetSection.geometry().closestVertex(pointXY) 	
			lineA = targetSection.geometry().asMultiPolyline()[0][0:indexPoint+1]
			lineB = targetSection.geometry().asMultiPolyline()[0][indexPoint:]
			if QgsGeometry.fromPolylineXY(lineA).length() < QGP.C_ToolsMinimumSectionLength or QgsGeometry.fromPolylineXY(lineB).length() < QGP.C_ToolsMinimumSectionLength : 
				self.cutSectionsListUnchanged.append(pointFeature); self.cutSectionsListTooShort.append(pointFeature); continue
			self.layerSectionsGR.changeGeometry(targetSection.id(), QgsGeometry.fromMultiPolylineXY([lineA]))
			newSection = QgsFeature(targetSection)
			newSection.setAttribute(QGP.tableSectionsFieldId, self.layerSectionsGR.maximumValue(newSection.fieldNameIndex(QGP.tableSectionsFieldId)) + 1)
			newSection.setGeometry(QgsGeometry.fromMultiPolylineXY([lineB]))
			self.layerSectionsGR.addFeature(newSection)
			self.cutSectionsListCut.append(pointFeature)

		if self.layerSectionsGR.isModified() : self.layerSectionsGR.commitChanges()

#		self.layerSectionsGR.commitChanges()
		del progressBar
	
		text = DSTY.textFormatBlackNormal.replace('%TEXT%','{:d} repères'.format(len(self.cutSectionsListAlreadyCut)))
		self.cutSectionsAlreadyCutCount.setText(text)
		DSTY.setStyleOkLabel(self.cutSectionsAlreadyCutCount, 'Normal')
	
		text = DSTY.textFormatBlackNormal.replace('%TEXT%','{:d} repères'.format(len(self.cutSectionsListDetached)))
		self.cutSectionsDetachedCount.setText(text)
		DSTY.setStyleWarningLabel(self.cutSectionsDetachedCount, 'Normal') if len(self.cutSectionsListDetached) > 0 else DSTY.setStyleOkLabel(self.cutSectionsDetachedCount, 'Normal')	
		
		text = DSTY.textFormatBlackNormal.replace('%TEXT%','{:d} repères'.format(len(self.cutSectionsListTooShort)))
		self.cutSectionsTooShortCount.setText(text)
		DSTY.setStyleWarningLabel(self.cutSectionsTooShortCount, 'Normal') if len(self.cutSectionsListTooShort) > 0 else DSTY.setStyleOkLabel(self.cutSectionsTooShortCount, 'Normal')	
		
		text = DSTY.textFormatBlackNormal.replace('%TEXT%','{:d} repères'.format(len(self.cutSectionsListCode1orY)))
		self.cutSectionsCode1orYCount.setText(text)
		DSTY.setStyleWarningLabel(self.cutSectionsCode1orYCount, 'Normal') if len(self.cutSectionsListCode1orY) > 0 else DSTY.setStyleOkLabel(self.cutSectionsCode1orYCount, 'Normal')	
	
		text = DSTY.textFormatBlackNormal.replace('%TEXT%','{:d} repères'.format(len(self.cutSectionsListMultiple)))
		self.cutSectionsMultipleCount.setText(text)
		DSTY.setStyleWarningLabel(self.cutSectionsMultipleCount, 'Normal') if len(self.cutSectionsListMultiple) > 0 else DSTY.setStyleOkLabel(self.cutSectionsMultipleCount, 'Normal')	

		text = DSTY.textFormatBlackNormal.replace('%TEXT%','{:d} repères'.format(len(self.cutSectionsListUnchanged)))
		self.cutSectionsUnchangedCount.setText(text)
		DSTY.setStyleOkLabel(self.cutSectionsUnchangedCount, 'Normal')

		text = DSTY.textFormatBlackNormal.replace('%TEXT%','{:d} repères'.format(len(self.cutSectionsListCut)))
		self.cutSectionsCutCount.setText(text)
		DSTY.setStyleOkLabel(self.cutSectionsCutCount, 'Normal') 

		self.mainFrame.setStatusDone('Découpage des Tronçons au niveau des repères sélectionnés - OK')


	def buttoncutSectionsAlreadyCut_clicked(self):
		self.layerPointsGR.selectByIds( [ pointFeature.id() for pointFeature in self.cutSectionsListAlreadyCut ] )
		self.mainFrame.setStatusInfo('Table Repères-GR : repères correspondants sélectionnés !')	
	
	def buttoncutSectionsDetached_clicked(self):
		self.layerPointsGR.selectByIds( [ pointFeature.id() for pointFeature in self.cutSectionsListDetached ] )
		self.mainFrame.setStatusInfo('Table Repères-GR : repères correspondants sélectionnés !')	
	
	def buttoncutSectionsTooShort_clicked(self):
		self.layerPointsGR.selectByIds( [ pointFeature.id() for pointFeature in self.cutSectionsListTooShort ] )
		self.mainFrame.setStatusInfo('Table Repères-GR : repères correspondants sélectionnés !')	
	
	def buttoncutSectionsCode1orY_clicked(self):
		self.layerPointsGR.selectByIds( [ pointFeature.id() for pointFeature in self.cutSectionsListCode1orY ] )
		self.mainFrame.setStatusInfo('Table Repères-GR : repères correspondants sélectionnés !')	

	def buttoncutSectionsMultiple_clicked(self):
		self.layerPointsGR.selectByIds( [ pointFeature.id() for pointFeature in self.cutSectionsListMultiple ] )
		self.mainFrame.setStatusInfo('Table Repères-GR : repères correspondants sélectionnés !')	
	
	def buttoncutSectionsCut_clicked(self):
		self.layerPointsGR.selectByIds( [ pointFeature.id() for pointFeature in self.cutSectionsListCut ] )
		self.mainFrame.setStatusInfo('Table Repères-GR : repères correspondants sélectionnés !')	

	def buttoncutSectionsUnchanged_clicked(self):
		self.layerPointsGR.selectByIds( [ pointFeature.id() for pointFeature in self.cutSectionsListUnchanged ] )
		self.mainFrame.setStatusInfo('Table Repères-GR : repères correspondants sélectionnés !')	


# ========================================================================================
# ========================================================================================
#
# Highlight Tronçons-GR : activation
#
# ========================================================================================
# ========================================================================================

	def sectionHighlightActivate(self):
		QgsExpressionContextUtils.setProjectVariable(QgsProject.instance(), QGP.tableSectionsGRHighlightVariable, 'Oui' if self.sectionHighlightActiveButton.checkState() == Qt.Checked else 'Non')
		self.iface.mapCanvas().refreshAllLayers()

	def sectionHighlightChangeMode(self):
		if QGP.tableSectionsGRHighlightModes[self.sectionHighlightModeCombo.currentText()] == None:
			self.sectionHighlightChangeDates()
		else:
			countDays = QGP.tableSectionsGRHighlightModes[self.sectionHighlightModeCombo.currentText()]
			QgsExpressionContextUtils.setProjectVariable(QgsProject.instance(), QGP.tableSectionsGRHighlightVariableDe, str(countDays-1))
			QgsExpressionContextUtils.setProjectVariable(QgsProject.instance(), QGP.tableSectionsGRHighlightVariableA, '0')
			if self.sectionHighlightActiveButton.checkState() == Qt.Checked : self.iface.mapCanvas().refreshAllLayers()

	def sectionHighlightChangeDates(self):
		if QGP.tableSectionsGRHighlightModes[self.sectionHighlightModeCombo.currentText()] == None:
			dateFrom = self.sectionHighlightDateEditFrom.date()
			dateTo = self.sectionHighlightDateEditTo.date()
			countDays = dateFrom.daysTo(QDate.currentDate())
			QgsExpressionContextUtils.setProjectVariable(QgsProject.instance(), QGP.tableSectionsGRHighlightVariableDe, str(dateFrom.daysTo(QDate.currentDate())-1))
			QgsExpressionContextUtils.setProjectVariable(QgsProject.instance(), QGP.tableSectionsGRHighlightVariableA, str(dateTo.daysTo(QDate.currentDate())))
			if self.sectionHighlightActiveButton.checkState() == Qt.Checked : self.iface.mapCanvas().refreshAllLayers()

	def buttonSectionHighlightSelect_clicked(self):
		if QGP.tableSectionsGRHighlightModes[self.sectionHighlightModeCombo.currentText()] == None:
			dateFrom = self.sectionHighlightDateEditFrom.date()
			dateTo = self.sectionHighlightDateEditTo.date()
		else:
			countDays = QGP.tableSectionsGRHighlightModes[self.sectionHighlightModeCombo.currentText()]
			dateFrom = QDate.currentDate().addDays(-(countDays-1))
			dateTo = QDate.currentDate()
		self.layerSectionsGR.removeSelection()
		expression = 'substr("dateModif",1,10) >= ' + "'" + dateFrom.toString('yyyy-MM-dd') + "'" + ' and ' + 'substr("dateModif",1,10) <= ' + "'" + dateTo.toString('yyyy-MM-dd') + "'"
		print (expression)
		self.layerSectionsGR.selectByExpression(expression)
		self.mainFrame.setStatusInfo('Sélection : ' + expression)


# ========================================================================================
# ========================================================================================
#
# Création des différents cadres Menu
# 
# ========================================================================================
# ========================================================================================

# ========================================================================================
# Cadre : Sélection Tronçons
# ========================================================================================

	def menuBoxSelectSections(self):

		groupBoxSelect = QtWidgets.QGroupBox('Select ID.s', self.mainMenu)
		groupBoxSelect.setStyleSheet(DSTY.styleBox)

# 	Ajouter Label Bouton et Input

		TBUT.createLabelBlackButton(groupBoxSelect, 1, 1, 'Liste ID.s', 'Normal', 'Normal')
		self.selectIdInputButton = TBUT.createInputButton(groupBoxSelect, 2, 1, 'Double4')

# ----------------------------------------------------------
# Ajouter Boutons : Select / Zoom
# ----------------------------------------------------------

		buttonSelectSections = TBUT.createActionButton(groupBoxSelect, 7, 1, 'Select', 'Normal')
		buttonSelectSections.clicked.connect(self.buttonSelectSectionsGR_clicked)

		buttonZoomSections = TBUT.createActionButton(groupBoxSelect, 8, 1, 'Zoom', 'Normal')
		buttonZoomSections.clicked.connect(self.buttonZoomSectionsGR_clicked)

# 	Terminé

		groupBoxSelect.repaint()

		return groupBoxSelect
		
				
# ========================================================================================
# Cadre : Conversion GPX
# ========================================================================================

	def menuBoxConvertGPX(self):

		groupBoxConvertGPX = QtWidgets.QGroupBox('Convertir GPX en Shape 3812', self.mainMenu)
		groupBoxConvertGPX.setStyleSheet(DSTY.styleBox)

# 	Label et Combo pour choix GPX

		TBUT.createLabelBlackButton(groupBoxConvertGPX, 1, 1, 'Choix du GPX', 'Normal')

		self.layerGPXCombo = TBUT.createComboButton(groupBoxConvertGPX, 2, 1, 'Double3')
		self.layerGPXCombo.currentTextChanged.connect(self.refreshInfoGPX)

# 	Label et Info sur les entités du GPX

		TBUT.createLabelBlackButton(groupBoxConvertGPX, 1, 2, 'Infos GPX', 'Normal')

		self.buttonTracksGPXCount = TBUT.createLabelGreenButton(groupBoxConvertGPX, 2, 2, '. . .', 'Normal')
		DSTY.setStyleWarningLabel(self.buttonTracksGPXCount, "Normal")

		self.buttonSectionsGPXCount = TBUT.createLabelGreenButton(groupBoxConvertGPX, 3, 2, '. . .', 'Double')
		DSTY.setStyleWarningLabel(self.buttonSectionsGPXCount, "Double")

# 	Bouton : Convertir GPX en Shape

		buttonTracksGPX2Shape = TBUT.createActionButton(groupBoxConvertGPX, 5, 2, 'GPX > Shape', 'Normal')
		buttonTracksGPX2Shape.clicked.connect(self.buttonTracksGPX2Shape_clicked)

# 	Bouton : Aide

		buttonHelpConvertGPX = TBUT.createHelpButton(groupBoxConvertGPX, 5, 1, 'Aide', 'Normal')
		buttonHelpConvertGPX.clicked.connect(self.buttonHelpConvertGPX_clicked)

# 	Terminé

		groupBoxConvertGPX.repaint()

		return groupBoxConvertGPX


	def buttonHelpConvertGPX_clicked(self):
		webbrowser.open_new_tab(QGP.configMenuHelpBasePath + 'QCarto - Outils - Conversion GPX.html')
		
		
# ========================================================================================
# Cadre : Conversion POI > CSV
# ========================================================================================

	def menuBoxExportPOI(self):

		groupBoxExportPOI = QtWidgets.QGroupBox('POI : Convertir GPX en CSV', self.mainMenu)
		groupBoxExportPOI.setStyleSheet(DSTY.styleBox)

# 	Label et Combo pour choix GPX

		TBUT.createLabelBlackButton(groupBoxExportPOI, 1, 1, 'Choix du GPX', 'Normal')

		self.layerPOICombo = TBUT.createComboButton(groupBoxExportPOI, 2, 1, 'Double3')
		self.layerPOICombo.currentTextChanged.connect(self.refreshInfoPOI)

# 	Label et Info sur les entités du GPX

		TBUT.createLabelBlackButton(groupBoxExportPOI, 1, 2, 'Points', 'Normal')

		self.buttonPOICount = TBUT.createLabelGreenButton(groupBoxExportPOI, 2, 2, '. . .', 'Double')
		DSTY.setStyleWarningLabel(self.buttonPOICount, "Double")

#	Check pour sélection only

		self.selectionOnlyPOI = TBUT.createCheckBoxButton(groupBoxExportPOI, 4, 2, 'Sélection', 'Normal')
		self.selectionOnlyPOI.setCheckState(Qt.Unchecked)	

# 	Bouton : Convertir GPX en CSV

		buttonPOI2CSV = TBUT.createActionButton(groupBoxExportPOI, 5, 2, 'GPX > CSV', 'Normal')
		buttonPOI2CSV.clicked.connect(self.buttonPOI2CSV_clicked)

# 	Bouton : Aide

		buttonHelpConvertPOI = TBUT.createHelpButton(groupBoxExportPOI, 5, 1, 'Aide', 'Normal')
#		buttonHelpConvertGPX.clicked.connect(buttonHelpConvertGPX_clicked)

# 	Terminé

		groupBoxExportPOI.repaint()

		return groupBoxExportPOI		
		

# ========================================================================================
# Cadre : Gestion des Parcours
# ========================================================================================

	def menuBoxTrackManagement(self):

		groupBoxTrackManagement = QtWidgets.QGroupBox('Parcours et Itinéraires : Copie / Renommage / Suppression', self.mainMenu)
		groupBoxTrackManagement.setStyleSheet(DSTY.styleBox)

#	Source

		TBUT.createLabelBlackButton(groupBoxTrackManagement, 1, 2, 'Source', 'Normal')
		
		self.trackManagementSrcInput = TBUT.createInputButton(groupBoxTrackManagement, 2, 2, 'Normal')	
		self.trackManagementSrcInput.returnPressed.connect(self.trackManagementSrc_changed)
		self.trackManagementSrcName = TBUT.createLabelGreenButton(groupBoxTrackManagement, 3, 2, '. . .', 'Double3')

		self.completerSrc = QtWidgets.QCompleter(sorted([code for code in (self.mainFrame.dicoTracksGRFeatures | self.mainFrame.dicoTracksRBFeatures)]))
		self.completerSrc.setCaseSensitivity(Qt.CaseInsensitive)
		self.completerSrc.setWidget(self.trackManagementSrcInput)
		self.trackManagementSrcInput.setCompleter(self.completerSrc)

#	Destination

		TBUT.createLabelBlackButton(groupBoxTrackManagement, 1, 3, 'Destination', 'Normal')
		
		self.trackManagementDstInput = TBUT.createInputButton(groupBoxTrackManagement, 2, 3, 'Normal')	
		self.trackManagementDstInput.returnPressed.connect(self.trackManagementDst_changed)
		self.trackManagementDstName = TBUT.createLabelGreenButton(groupBoxTrackManagement, 3, 3, '. . .', 'Double3')

		self.completerDst = QtWidgets.QCompleter(sorted([code for code in (self.mainFrame.dicoTracksGRFeatures | self.mainFrame.dicoTracksRBFeatures)]))
		self.completerDst.setCaseSensitivity(Qt.CaseInsensitive)
		self.completerDst.setWidget(self.trackManagementDstInput)
		self.trackManagementDstInput.setCompleter(self.completerDst)

#	Parcours Source et Destination

		TBUT.createLabelBlackButton(groupBoxTrackManagement, 1, 4, 'Parcours Source', 'Normal')

		self.targetTracksActiveButton = TBUT.createCheckBoxButton(groupBoxTrackManagement, 2, 4, 'Activer', 'Normal')
		self.targetTracksActiveButton.setCheckState(Qt.Unchecked)	

		self.trackManagementSrcNbrTracks = TBUT.createLabelGreenButton(groupBoxTrackManagement, 3, 4, '. . .', 'Normal')
		self.trackManagementSrcNbrTracks.setContextMenuPolicy(Qt.CustomContextMenu)
		self.trackManagementSrcNbrTracks.customContextMenuRequested.connect(self.trackManagementSelectSrcTracks_rightClicked)

		TBUT.createLabelBlackButton(groupBoxTrackManagement, 4, 4, 'Parcours Destination', 'Normal')

		self.trackManagementDstNbrTracks = TBUT.createLabelGreenButton(groupBoxTrackManagement, 5, 4, '. . .', 'Normal')
		self.trackManagementDstNbrTracks.setContextMenuPolicy(Qt.CustomContextMenu)
		self.trackManagementDstNbrTracks.customContextMenuRequested.connect(self.trackManagementSelectDstTracks_rightClicked)

#	Tronçons Source et Destination

		TBUT.createLabelBlackButton(groupBoxTrackManagement, 1, 5, 'Tronçons Source', 'Normal')
			
		self.targetSectionsActiveButton = TBUT.createCheckBoxButton(groupBoxTrackManagement, 2, 5, 'Activer', 'Normal')
		self.targetSectionsActiveButton.setCheckState(Qt.Unchecked)				
			
		self.trackManagementSrcNbrSections = TBUT.createLabelGreenButton(groupBoxTrackManagement, 3, 5, '. . .', 'Normal')
		self.trackManagementSrcNbrSections.setContextMenuPolicy(Qt.CustomContextMenu)
		self.trackManagementSrcNbrSections.customContextMenuRequested.connect(self.trackManagementSelectSrcSections_rightClicked)

		TBUT.createLabelBlackButton(groupBoxTrackManagement, 4, 5, 'Tronçons Destination', 'Normal')

		self.trackManagementDstNbrSections = TBUT.createLabelGreenButton(groupBoxTrackManagement, 5, 5, '. . .', 'Normal')
		self.trackManagementDstNbrSections.setContextMenuPolicy(Qt.CustomContextMenu)
		self.trackManagementDstNbrSections.customContextMenuRequested.connect(self.trackManagementSelectDstSections_rightClicked)

#	Repères Source et Destination

		TBUT.createLabelBlackButton(groupBoxTrackManagement, 1, 6, 'Repères Source', 'Normal')
			
		self.targetReperesActiveButton = TBUT.createCheckBoxButton(groupBoxTrackManagement, 2, 6, 'Activer', 'Normal')
		self.targetReperesActiveButton.setCheckState(Qt.Unchecked)				
			
		self.trackManagementSrcNbrReperes = TBUT.createLabelGreenButton(groupBoxTrackManagement, 3, 6, '. . .', 'Normal')
		self.trackManagementSrcNbrReperes.setContextMenuPolicy(Qt.CustomContextMenu)
		self.trackManagementSrcNbrReperes.customContextMenuRequested.connect(self.trackManagementSelectSrcReperes_rightClicked)

		TBUT.createLabelBlackButton(groupBoxTrackManagement, 4, 6, 'Repères Destination', 'Normal')

		self.trackManagementDstNbrReperes = TBUT.createLabelGreenButton(groupBoxTrackManagement, 5, 6, '. . .', 'Normal')
		self.trackManagementDstNbrReperes.setContextMenuPolicy(Qt.CustomContextMenu)
		self.trackManagementDstNbrReperes.customContextMenuRequested.connect(self.trackManagementSelectDstReperes_rightClicked)

#	Avertissement

		self.targetOperationWarning = TBUT.createLabelBlackButton(groupBoxTrackManagement, 1, 8, '', 'Normal')
		self.targetTracksWarning = TBUT.createLabelBlackButton(groupBoxTrackManagement, 2, 8, '', 'Normal')
		self.targetSectionsWarning = TBUT.createLabelBlackButton(groupBoxTrackManagement, 3, 8, '', 'Normal')
		self.targetReperesWarning = TBUT.createLabelBlackButton(groupBoxTrackManagement, 4, 8, '', 'Normal')

#	Actions

		self.trackManagementButtonRename = TBUT.createActionButton(groupBoxTrackManagement, 2, 7, 'Renommer', 'Normal')
		self.trackManagementButtonRename.clicked.connect(self.trackManagementRename_clicked)

		self.trackManagementButtonCopy = TBUT.createActionButton(groupBoxTrackManagement, 3, 7, 'Copier', 'Normal')
		self.trackManagementButtonCopy.clicked.connect(self.trackManagementCopy_clicked)

		self.trackManagementButtonDelete = TBUT.createActionButton(groupBoxTrackManagement, 4, 7, 'Supprimer', 'Normal')
		self.trackManagementButtonDelete.clicked.connect(self.trackManagementDelete_clicked)

		self.trackManagementButtonCancel = TBUT.createActionButton(groupBoxTrackManagement, 5, 7, 'Annuler', 'Normal')
		self.trackManagementButtonCancel.clicked.connect(self.trackManagementCancel_clicked)

		self.trackManagementButtonConfirm = TBUT.createActionButton(groupBoxTrackManagement, 5, 8, 'Confirmer', 'Normal')
		self.trackManagementButtonConfirm.clicked.connect(self.trackManagementConfirm_clicked)
		DSTY.setStyleWarningButton(self.trackManagementButtonConfirm)

# 	Bouton : Aide

		buttonHelpTrackManagement = TBUT.createHelpButton(groupBoxTrackManagement, 5, 1, 'Aide', 'Normal')
		buttonHelpTrackManagement.clicked.connect(self.buttonHelpTrackManagement_clicked)
		
# 	Terminé

		groupBoxTrackManagement.repaint()

		return groupBoxTrackManagement		


	def buttonHelpTrackManagement_clicked(self):
		webbrowser.open_new_tab(QGP.configMenuHelpBasePath + 'QCarto - Outils - Gestion Parcours.html')

# ========================================================================================

	def menuBoxTrackManagementMode(self):
	
		groupBoxTrackManagementMode = QtWidgets.QGroupBox('', self.mainMenu)
		groupBoxTrackManagementMode.setStyleSheet(DSTY.styleHiddenBox)

# 	Radio Boutons

		TBUT.createLabelBlackButton(groupBoxTrackManagementMode, 1, 1, 'Etendue', 'Normal')

		self.buttonTrackManagementModeTrack = TBUT.createRadioBoxButton(groupBoxTrackManagementMode, 2, 1, 'Parcours', 'Normal')
		self.buttonTrackManagementModeTrack.setChecked(True)
		self.buttonTrackManagementModeIti = TBUT.createRadioBoxButton(groupBoxTrackManagementMode, 3, 1, 'Itinéraire', 'Normal')

		self.buttonTrackManagementModeTrack.clicked.connect(self.trackManagementAny_changed)
		self.buttonTrackManagementModeIti.clicked.connect(self.trackManagementAny_changed)

#	Selection only

		self.targetSelectionOnlyButton = TBUT.createCheckBoxButton(groupBoxTrackManagementMode, 4, 1, 'Sélection', 'Normal')
		self.targetSelectionOnlyButton.setCheckState(Qt.Unchecked)	
		self.targetSelectionOnlyButton.stateChanged.connect(self.trackManagementAny_changed)

# 	Terminé

		groupBoxTrackManagementMode.repaint()

		return groupBoxTrackManagementMode


# ========================================================================================
# Cadre : Relation OSM
# ========================================================================================

	def menuBoxRelationOsm(self):

		groupBoxRelationOsm = QtWidgets.QGroupBox('Parcours : Relation Osm', self.mainMenu)
		groupBoxRelationOsm.setStyleSheet(DSTY.styleBox)

#	Parcours

		TBUT.createLabelBlackButton(groupBoxRelationOsm, 1, 1, 'Parcours', 'Normal')

		self.buttonTrackOsmCode = TBUT.createLabelGreenButton(groupBoxRelationOsm, 2, 1, '. . .', 'Normal')
		DSTY.setStyleWarningLabel(self.buttonTrackOsmCode, "Normal")

		self.buttonTrackOsmId = TBUT.createLabelGreenButton(groupBoxRelationOsm, 3, 1, '. . .', 'Normal')
		DSTY.setStyleWarningLabel(self.buttonTrackOsmId, "Normal")

		TBUT.createLabelBlackButton(groupBoxRelationOsm, 1, 2, 'Nom', 'Normal')

		self.buttonTrackOsmName = TBUT.createLabelGreenButton(groupBoxRelationOsm, 2, 2, '. . .', 'Double3')
		DSTY.setStyleWarningLabel(self.buttonTrackOsmName, "Double3")

#	Hausdorff

		TBUT.createLabelBlackButton(groupBoxRelationOsm, 1, 3, 'Delta GR-OSM', 'Normal')

		self.buttonTrackOsmDelta = TBUT.createLabelGreenButton(groupBoxRelationOsm, 2, 3, '. . .', 'Double')
		DSTY.setStyleWarningLabel(self.buttonTrackOsmDelta, "Double")

# 	Boutons

		buttonOsmDownload = TBUT.createActionButton(groupBoxRelationOsm, 1, 4, 'Charger Osm', 'Normal')
		buttonOsmDownload.clicked.connect(self.buttonOsmDownload_clicked)

		buttonOsmCreate = TBUT.createActionButton(groupBoxRelationOsm, 2, 4, 'Créer Osm', 'Normal')
		buttonOsmCreate.clicked.connect(self.buttonOsmCreate_clicked)

# 	Terminé

		groupBoxRelationOsm.repaint()

		return groupBoxRelationOsm		


# ========================================================================================
# Cadre : Création GPX
# ========================================================================================

	def menuBoxCreateGPX(self):

		groupBoxCreateGPX = QtWidgets.QGroupBox('Création GPX par Tronçon', self.mainMenu)
		groupBoxCreateGPX.setStyleSheet(DSTY.styleBox)

# 	Bouton : Création GPX

		buttonCreateGPX = TBUT.createActionButton(groupBoxCreateGPX, 1, 1, 'Création GPX', 'Normal')
		buttonCreateGPX.clicked.connect(self.buttonCreateGPX_clicked)

# 	Aide

		buttonHelp = TBUT.createHelpButton(groupBoxCreateGPX, 3, 1, 'Aide', 'Normal')
		buttonHelp.clicked.connect(lambda x : webbrowser.open_new_tab(QGP.configMenuHelpBasePath + 'QCarto - Dock - Création GPX.html'))

# 	Terminé

		groupBoxCreateGPX.repaint()

		return groupBoxCreateGPX		
		

# ========================================================================================
# Cadre : Attacher Repères
# ========================================================================================

	def menuBoxAttachPoints(self):

		groupBoxAttachPoints = QtWidgets.QGroupBox('Attacher les Repères sélectionnés sur Tronçon', self.mainMenu)
		groupBoxAttachPoints.setStyleSheet(DSTY.styleBox)

# 	Info sur les Repères sélectionnés

		TBUT.createLabelBlackButton(groupBoxAttachPoints, 1, 1, 'Sélection', 'Normal')
		self.attachPointsSelectedCount = TBUT.createLabelGreenButton(groupBoxAttachPoints, 2, 1, '. . .', 'Normal')

#	Info sur les repères modifiés

		TBUT.createLabelBlackButton(groupBoxAttachPoints, 1, 2, 'Déjà attachés', 'Normal')

		self.attachPointsAlreadyAttachedCount = TBUT.createLabelGreenButton(groupBoxAttachPoints, 2, 2, '. . .', 'Normal')
		self.attachPointsAlreadyAttachedCountSelect = TBUT.createActionButtonTransparent(groupBoxAttachPoints, 2, 2, '', 'Normal')
		self.attachPointsAlreadyAttachedCountSelect.clicked.connect(self.buttonAttachPointsAlreadyAttached_clicked)
		
		TBUT.createLabelBlackButton(groupBoxAttachPoints, 1, 3, '0 / > 1 tronçons', 'Normal')

		self.attachPointsNoSectionCount = TBUT.createLabelGreenButton(groupBoxAttachPoints, 2, 3, '. . .', 'Normal')
		self.attachPointsNoSectionCountSelect = TBUT.createActionButtonTransparent(groupBoxAttachPoints, 2, 3, '', 'Normal')
		self.attachPointsNoSectionCountSelect.clicked.connect(self.buttonAttachPointsNoSection_clicked)
		
		self.attachPointsMultipleSectionCount = TBUT.createLabelGreenButton(groupBoxAttachPoints, 3, 3, '. . .', 'Normal')
		self.attachPointsMultipleSectionCountSelect = TBUT.createActionButtonTransparent(groupBoxAttachPoints, 3, 3, '', 'Normal')
		self.attachPointsMultipleSectionCountSelect.clicked.connect(self.buttonAttachPointsMultipleSection_clicked)

		TBUT.createLabelBlackButton(groupBoxAttachPoints, 1, 4, 'Trop distants', 'Normal')

		self.attachPointsTooFarSectionCount = TBUT.createLabelGreenButton(groupBoxAttachPoints, 2, 4, '. . .', 'Normal')
		self.attachPointsTooFarSectionCountSelect = TBUT.createActionButtonTransparent(groupBoxAttachPoints, 2, 4, '', 'Normal')
		self.attachPointsTooFarSectionCountSelect.clicked.connect(self.buttonAttachPointsToFarSection_clicked)

		TBUT.createLabelBlackButton(groupBoxAttachPoints, 1, 5, 'Attachés / inchangés', 'Normal')

		self.attachPointsAttachedCount = TBUT.createLabelGreenButton(groupBoxAttachPoints, 2, 5, '. . .', 'Normal')
		self.attachPointsAttachedCountSelect = TBUT.createActionButtonTransparent(groupBoxAttachPoints, 2, 5, '', 'Normal')
		self.attachPointsAttachedCountSelect.clicked.connect(self.buttonAttachPointsAttached_clicked)

		self.attachPointsUnchangedCount = TBUT.createLabelGreenButton(groupBoxAttachPoints, 3, 5, '. . .', 'Normal')
		self.attachPointsUnchangedCountSelect = TBUT.createActionButtonTransparent(groupBoxAttachPoints, 3, 5, '', 'Normal')
		self.attachPointsUnchangedCountSelect.clicked.connect(self.buttonAttachPointsUnchanged_clicked)

#	Action

		self.buttonAttachPoints = TBUT.createActionButton(groupBoxAttachPoints, 3, 6, 'Attacher', 'Normal')
		DSTY.setStyleWarningButton(self.buttonAttachPoints)
		self.buttonAttachPoints.clicked.connect(self.buttonAttachPoints_clicked)

# 	Aide

		buttonHelpAttachPoints = TBUT.createHelpButton(groupBoxAttachPoints, 3, 1, 'Aide', 'Normal')
		buttonHelpAttachPoints.clicked.connect(lambda x : webbrowser.open_new_tab(QGP.configMenuHelpBasePath + 'QCarto - Outils - Attachement Repères.html'))
		
# 	Terminé

		groupBoxAttachPoints.repaint()

		return groupBoxAttachPoints		
		
		
# ========================================================================================
# Cadre : Découper Sections
# ========================================================================================

	def menuBoxCutSections(self):

		groupBoxCutSections = QtWidgets.QGroupBox('Couper les tronçons au niveau des Repères sélectionnés', self.mainMenu)
		groupBoxCutSections.setStyleSheet(DSTY.styleBox)

# 	Info sur les Repères sélectionnés

		TBUT.createLabelBlackButton(groupBoxCutSections, 1, 1, 'Sélection', 'Normal')
		self.cutSectionsPointsSelectedCount = TBUT.createLabelGreenButton(groupBoxCutSections, 2, 1, '. . .', 'Normal')

#	Info sur les repères modifiés

		TBUT.createLabelBlackButton(groupBoxCutSections, 1, 2, 'Déjà coupés', 'Normal')

		self.cutSectionsAlreadyCutCount = TBUT.createLabelGreenButton(groupBoxCutSections, 2, 2, '. . .', 'Normal')
		self.cutSectionsAlreadyCutCountSelect = TBUT.createActionButtonTransparent(groupBoxCutSections, 2, 2, '', 'Normal')
		self.cutSectionsAlreadyCutCountSelect.clicked.connect(self.buttoncutSectionsAlreadyCut_clicked)
		
		TBUT.createLabelBlackButton(groupBoxCutSections, 1, 3, 'Distants / Courts', 'Normal')

		self.cutSectionsDetachedCount = TBUT.createLabelGreenButton(groupBoxCutSections, 2, 3, '. . .', 'Normal')
		self.cutSectionsDetachedCountSelect = TBUT.createActionButtonTransparent(groupBoxCutSections, 2, 3, '', 'Normal')
		self.cutSectionsDetachedCountSelect.clicked.connect(self.buttoncutSectionsDetached_clicked)
		
		self.cutSectionsTooShortCount = TBUT.createLabelGreenButton(groupBoxCutSections, 3, 3, '. . .', 'Normal')
		self.cutSectionsTooShortCountSelect = TBUT.createActionButtonTransparent(groupBoxCutSections, 3, 3, '', 'Normal')
		self.cutSectionsTooShortCountSelect.clicked.connect(self.buttoncutSectionsTooShort_clicked)

		TBUT.createLabelBlackButton(groupBoxCutSections, 1, 4, '-1 or -Y / Multiple', 'Normal')

		self.cutSectionsCode1orYCount = TBUT.createLabelGreenButton(groupBoxCutSections, 2, 4, '. . .', 'Normal')
		self.cutSectionsCode1orYCountSelect = TBUT.createActionButtonTransparent(groupBoxCutSections, 2, 4, '', 'Normal')
		self.cutSectionsCode1orYCountSelect.clicked.connect(self.buttoncutSectionsCode1orY_clicked)

		self.cutSectionsMultipleCount = TBUT.createLabelGreenButton(groupBoxCutSections, 3, 4, '. . .', 'Normal')
		self.cutSectionsMultipleCountSelect = TBUT.createActionButtonTransparent(groupBoxCutSections, 3, 4, '', 'Normal')
		self.cutSectionsMultipleCountSelect.clicked.connect(self.buttoncutSectionsMultiple_clicked)

		TBUT.createLabelBlackButton(groupBoxCutSections, 1, 5, 'Coupés / inchangés', 'Normal')

		self.cutSectionsCutCount = TBUT.createLabelGreenButton(groupBoxCutSections, 2, 5, '. . .', 'Normal')
		self.cutSectionsCutCountSelect = TBUT.createActionButtonTransparent(groupBoxCutSections, 2, 5, '', 'Normal')
		self.cutSectionsCutCountSelect.clicked.connect(self.buttoncutSectionsCut_clicked)

		self.cutSectionsUnchangedCount = TBUT.createLabelGreenButton(groupBoxCutSections, 3, 5, '. . .', 'Normal')
		self.cutSectionsUnchangedCountSelect = TBUT.createActionButtonTransparent(groupBoxCutSections, 3, 5, '', 'Normal')
		self.cutSectionsUnchangedCountSelect.clicked.connect(self.buttoncutSectionsUnchanged_clicked)

#	Action

		self.buttonCutSections = TBUT.createActionButton(groupBoxCutSections, 3, 6, 'Couper', 'Normal')
		DSTY.setStyleWarningButton(self.buttonCutSections)
		self.buttonCutSections.clicked.connect(self.buttonCutSections_clicked)

# 	Aide

		buttonHelpCutSections = TBUT.createHelpButton(groupBoxCutSections, 3, 1, 'Aide', 'Normal')
		buttonHelpCutSections.clicked.connect(lambda x : webbrowser.open_new_tab(QGP.configMenuHelpBasePath + 'QCarto - Outils - Découpe Tronçons.html'))
		
# 	Terminé

		groupBoxCutSections.repaint()

		return groupBoxCutSections		
		
				
# ========================================================================================
# Cadre : Highlight Tronçons
# ========================================================================================

	def menuBoxHighlightModifications(self):

		groupBoxHighlight = QtWidgets.QGroupBox('Montrer les Tronçons-GR modifiés', self.mainMenu)
		groupBoxHighlight.setStyleSheet(DSTY.styleBox)

#	Activation / mode

		TBUT.createLabelBlackButton(groupBoxHighlight, 1, 1, 'Activation / Mode', 'Normal')

		self.sectionHighlightActiveButton = TBUT.createCheckBoxButton(groupBoxHighlight, 2, 1, 'Activer', 'Normal')
		self.sectionHighlightActiveButton.setCheckState(Qt.Unchecked)	
		self.sectionHighlightActiveButton.stateChanged.connect(self.sectionHighlightActivate)

		self.sectionHighlightModeCombo = TBUT.createComboButton(groupBoxHighlight, 3, 1, 'Normal')
		for mode in QGP.tableSectionsGRHighlightModes :
			self.sectionHighlightModeCombo.addItem(mode)
		self.sectionHighlightModeCombo.currentTextChanged.connect(self.sectionHighlightChangeMode)
		self.sectionHighlightChangeMode()					

#	Dates

		TBUT.createLabelBlackButton(groupBoxHighlight, 1, 2, 'Depuis / jusque', 'Normal')
		self.sectionHighlightDateEditFrom = TBUT.createInputDateButton(groupBoxHighlight, 2, 2, 'Normal')
		self.sectionHighlightDateEditTo = TBUT.createInputDateButton(groupBoxHighlight, 3, 2, 'Normal')
		self.sectionHighlightDateEditFrom.dateChanged.connect(self.sectionHighlightChangeDates)
		self.sectionHighlightDateEditTo.dateChanged.connect(self.sectionHighlightChangeDates)
		self.sectionHighlightChangeDates()

#	Sélection

		self.buttonSectionHighlightSelect = TBUT.createActionButton(groupBoxHighlight, 3, 3, 'Sélectionner', 'Normal')
		self.buttonSectionHighlightSelect.clicked.connect(self.buttonSectionHighlightSelect_clicked)

# 	Terminé

		groupBoxHighlight.repaint()

		return groupBoxHighlight		
		


# ========================================================================================
# --- THE END ---
# ========================================================================================
	