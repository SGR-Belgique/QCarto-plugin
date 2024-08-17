# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Gestion des Menus : Construction par Tronçon d'un GPX
# ========================================================================================

from PyQt5.QtCore import *
from PyQt5.QtGui import *

from qgis.core import *
from qgis.gui import *
from qgis.PyQt import QtWidgets

import importlib
import os
import webbrowser

import QCarto_Tools_Altitudes as TALT
import QCarto_Tools_Buttons as TBUT
import QCarto_Tools_Canevas as TCAN
import QCarto_Tools_Coding as TCOD
import QCarto_Tools_Dates as TDAT
import QCarto_Tools_Files as TFIL
import QCarto_Tools_GPX as TGPX
import QCarto_Tools_Layers as TLAY
import QCarto_Tools_Rubberband as TRUB
importlib.reload(TRUB)

import QCarto_Definitions_Colors as DCOL
import QCarto_Definitions_Styles as DSTY

import QCarto_Parameters_Global
importlib.reload(QCarto_Parameters_Global)
QGP = QCarto_Parameters_Global.globalParameters()


# ========================================================================================
# Créer si nécessaire le cadre de la Page : Create GPX
# >>> iface     :	
# >>> mainMenu  :	widget						Main Menu Widget - To be shown again on exit		
# >>> mainFrame : 	class mainMenuFrame			Top-level Frame (Tableau de Bord)
# <<< dockFrame : 	dock Frame					Dock Frame for GPX Creation
# ========================================================================================

def createGPXbySections(iface, mainMenu, mainFrame, dockFrame):

	if dockFrame == None:
		dockFrame = menuGPXCreation(iface, mainMenu, mainFrame)

	return dockFrame


# ========================================================================================
# Class : menuGPXCreation
# >>> iface    				 :	
# >>> mainMenu 				 : widget						Main Menu Widget - To be shown again on exit		
# >>> mainFrame				 : class mainMenuFrame			Top-level Frame (Tableau de Bord)
# <<< dockFrame 		  	 : class menuDockEdit			Dock Frame for 50K edition
# ========================================================================================

class menuGPXCreation:

	def __init__(self, iface, mainMenu, mainFrame):

		mainFrame.setStatusWorking('Initialisation de la fenêtre de création GPX (quelques secondes) ...')

# 	Initialisation des Variables 

		self.iface = iface
		self.mainFrame = mainFrame
		self.mainMenu = mainMenu
			
#	Accès aux Tables de la DB Carto

		self.layerSectionsGR, 	self.layerSectionsGRerror 	= self.mainFrame.layerSectionsGR, 	self.mainFrame.layerSectionsGRerror 	
		self.layerPointsGR, 	self.layerPointsGRError 	= self.mainFrame.layerPointsGR, 	self.mainFrame.layerPointsGRError 	

#	Dictionnaires Principaux 
		
		self.dicoSectionsGRFeatures = self.mainFrame.dicoSectionsGRFeatures

# 	Création du Dock Widget Principal			
			
		self.dockCreateGPXWidget = QtWidgets.QDockWidget(self.iface.mainWindow())
		self.dockCreateGPXWidget.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
		
		self.iface.addDockWidget(Qt.TopDockWidgetArea, self.dockCreateGPXWidget)
		self.dockCreateGPXWidget.repaint()
		self.dockCreateGPXWidget.show()

# 	Création de tous les cadres internes au Widget

		self.boxesList = []
		self.createBoxes()

# 	Initialisation des Variables de Contexte

		self.rubberBandGPX = TRUB.rubberBandGPX(self.iface)
		self.rubberBandGPX.setRubberBandColor(DCOL.bgRubberBandGPXCreation)
		self.trackIdList = []
		self.trackLine = []
		self.trackLenghtList = []
		self.refreshTrackInfo()
		
# 	Créations des dictionnaires

		self.setStatusOk('Prêt')													


	def createBoxes(self):

		self.groupBoxName = self.menuGPXCreationName()
		DSTY.setBoxGeometry(self.groupBoxName, 1, 1, 8, 1)
		self.boxesList.append(self.groupBoxName)

		self.groupBoxSection = self.menuGPXCreationSection()
		DSTY.setBoxGeometry(self.groupBoxSection, 1, 3, 8, 1)
		self.boxesList.append(self.groupBoxSection)

		self.groupBoxTrack = self.menuGPXCreationTrack()
		DSTY.setBoxGeometry(self.groupBoxTrack, 1, 5, 8, 1)
		self.boxesList.append(self.groupBoxTrack)

		self.groupBoxStatus = self.menuGPXCreationStatus()
		DSTY.setBoxGeometry(self.groupBoxStatus, 1, 7, 6, 1)
		self.boxesList.append(self.groupBoxStatus)

		self.groupBoxControls = self.menuGPXCreationControls()
		DSTY.setBoxGeometry(self.groupBoxControls, 7, 7, 2, 1)
		self.boxesList.append(self.groupBoxControls)


# ========================================================================================
# Actions Principales
# ========================================================================================

	def requestClose_clicked(self):
		self.hide()
		self.mainMenu.show()

	def show(self):
		self.dockCreateGPXWidget.show()
		self.dockCreateGPXWidget.setMinimumHeight(200)
		for box in self.boxesList: box.show(), box.repaint()
		self.connectSectionsGR()	
		self.activateSectionsGR()
		self.rubberBandGPX.refreshRubberBand(self.trackLine, [])
		
	def hide(self):
		for box in self.boxesList: box.hide(), box.repaint()
		self.disconnectSectionsGR()	
		self.rubberBandGPX.clearRubberBand()
		self.dockCreateGPXWidget.hide()

	def close(self):
		self.hide()		
		for box in self.boxesList: del box		
		self.rubberBandGPX.clearRubberBand()
		self.rubberBandGPX.deleteRubberBand()
		self.iface.removeDockWidget(self.dockCreateGPXWidget)																	
		del self.dockCreateGPXWidget																								
																										
		
		
# ========================================================================================
# Connection à la Couche des Tronçons
# ========================================================================================

	def activateSectionsGR(self):
		self.iface.layerTreeView().setCurrentLayer(self.layerSectionsGR)
		action = self.iface.actionSelect()
		action.trigger()

	def connectSectionsGR(self):
		if self.layerSectionsGR != None : self.layerSectionsGR.selectionChanged.connect(self.sectionsGRSelectionChanged)	
	
	def disconnectSectionsGR(self):
		try:
			self.layerSectionsGR.selectionChanged.disconnect(self.sectionsGRSelectionChanged)	
		except:
			pass

	def sectionsGRSelectionChanged(self):

		featureList = [feature for feature in self.layerSectionsGR.getSelectedFeatures() ]

		if len(featureList) != 1:
			text = DSTY.textFormatBlackSmall.replace('%TEXT%',' X X X ')
			self.sectionInfoLength.setText(text)
			DSTY.setStyleWarningLabel(self.sectionInfoLength, 'Normal')
			self.sectionInfoDelta.setText(text)
			DSTY.setStyleWarningLabel(self.sectionInfoDelta, 'Normal')

		if len(featureList) == 0:
			text = DSTY.textFormatBlackSmall.replace('%TEXT%',' X X X ')
			self.sectionInfoId.setText(text)
			DSTY.setStyleWarningLabel(self.sectionInfoId, 'Normal')

		if len(featureList) > 1:
			text = DSTY.textFormatBlackSmall.replace('%TEXT%', str(len(featureList)) + ' x')
			self.sectionInfoId.setText(text)
			DSTY.setStyleWarningLabel(self.sectionInfoId, 'Normal')

		if len(featureList) == 1:
			text = DSTY.textFormatBlackSmall.replace('%TEXT%', str(featureList[0].id()))
			self.sectionInfoId.setText(text)
			DSTY.setStyleOkLabel(self.sectionInfoId, 'Normal')
			text = DSTY.textFormatBlackSmall.replace('%TEXT%', '{0:d} m'.format(int(featureList[0].geometry().length())))
			self.sectionInfoLength.setText(text)
			DSTY.setStyleOkLabel(self.sectionInfoLength, 'Normal')
			delta, orientation = self.computeDistanceTrack2Section(featureList[0])
			text = DSTY.textFormatBlackSmall.replace('%TEXT%', '{0:d} m'.format(int(delta)))
			self.sectionInfoDelta.setText(text)
			DSTY.setStyleOkLabel(self.sectionInfoDelta, 'Normal')


	def computeDistanceTrack2Section(self, sectionFeature):

		if len(self.trackIdList) == 0: 
			return 0, None

		if len(self.trackIdList) == 1:
			distance_ZA = self.trackLine[-1].distance(sectionFeature.geometry().asMultiPolyline()[0][0])
			distance_ZZ = self.trackLine[-1].distance(sectionFeature.geometry().asMultiPolyline()[0][-1])
			distance_AA = self.trackLine[0].distance(sectionFeature.geometry().asMultiPolyline()[0][0])
			distance_AZ = self.trackLine[0].distance(sectionFeature.geometry().asMultiPolyline()[0][-1])
			if distance_ZA == min(distance_ZA, distance_ZZ, distance_AA, distance_AZ) : return distance_ZA, 'ZA'
			if distance_ZZ == min(distance_ZA, distance_ZZ, distance_AA, distance_AZ) : return distance_ZZ, 'ZZ'
			if distance_AA == min(distance_ZA, distance_ZZ, distance_AA, distance_AZ) : return distance_AA, 'AA'
			if distance_AZ == min(distance_ZA, distance_ZZ, distance_AA, distance_AZ) : return distance_AZ, 'AZ'

		if len(self.trackIdList) > 1:
			distance_ZA = self.trackLine[-1].distance(sectionFeature.geometry().asMultiPolyline()[0][0])
			distance_ZZ = self.trackLine[-1].distance(sectionFeature.geometry().asMultiPolyline()[0][-1])
			if distance_ZA == min(distance_ZA, distance_ZZ) : return distance_ZA, 'ZA'
			if distance_ZZ == min(distance_ZA, distance_ZZ) : return distance_ZZ, 'ZZ'


# ========================================================================================
# Affichage des infos du tracé en construction
# ========================================================================================

	def refreshTrackInfo(self):

		if len(self.trackIdList) == 0:
			text = DSTY.textFormatBlackSmall.replace('%TEXT%','0 x')
			self.trackInfoIds.setText(text)
			text = DSTY.textFormatBlackSmall.replace('%TEXT%','0 m')
			self.trackInfoLength.setText(text)
			self.trackInfoDPlus.setText(text)
			self.trackInfoDMinus.setText(text)
			
		if len(self.trackIdList) > 0:
			text = DSTY.textFormatBlackSmall.replace('%TEXT%','{0:d} x'.format(len(self.trackIdList)))
			self.trackInfoIds.setText(text)
			text = DSTY.textFormatBlackSmall.replace('%TEXT%','{0:d} m'.format(int(QgsGeometry.fromMultiPolylineXY([self.trackLine]).length())))
			self.trackInfoLength.setText(text)
			trackLineXYZ, missingAltitude1, missingAltitude2 = TALT.addTrackAltitudes(self.trackLine)
			dPlus, dMinus, missing = TALT.computeTrackAscending(trackLineXYZ)		
			text = DSTY.textFormatBlackSmall.replace('%TEXT%','{0:d} m+'.format(int(dPlus)))
			self.trackInfoDPlus.setText(text)
			text = DSTY.textFormatBlackSmall.replace('%TEXT%','{0:d} m-'.format(int(dMinus)))
			self.trackInfoDMinus.setText(text)
			
		DSTY.setStyleOkLabel(self.trackInfoIds, 'Normal')	
		DSTY.setStyleOkLabel(self.trackInfoLength, 'Normal')	
		DSTY.setStyleOkLabel(self.trackInfoDPlus, 'Normal')	
		DSTY.setStyleOkLabel(self.trackInfoDMinus, 'Normal')	

		self.rubberBandGPX.refreshRubberBand(self.trackLine, [])


# ========================================================================================
# Construction du Tracé
# ========================================================================================

	def razTrack_clicked(self):
		self.trackIdList = []
		self.trackLine = []
		self.trackLenghtList = []

		self.refreshTrackInfo()
		self.layerSectionsGR.removeSelection()

		self.setStatusDone('Le tracé en construction a été effacé !')


	def removeTrack_clicked(self):
		if len(self.trackIdList) == 0:
			self.setStatusWarning('Le tracé est vide !')
			return
		self.trackIdList.pop()
		self.trackLine = self.trackLine[0:self.trackLenghtList.pop()]
		
		self.refreshTrackInfo()
		self.layerSectionsGR.removeSelection()		
		
		self.setStatusDone('La dernière section du tracé a été supprimée !')		


	def addSection_clicked(self):

		featureList = [feature for feature in self.layerSectionsGR.getSelectedFeatures() ]

		if len(featureList) == 0:
			self.setStatusWarning('Pas de tronçon sélectionné !')
			return
		if len(featureList) > 1:
			self.setStatusWarning('Plusieurs tronçons sélectionnés en même temps !')
			return

		delta, orientation = self.computeDistanceTrack2Section(featureList[0])
		if delta >= QGP.activeMapLinesMergeDistanceMax:
			self.setStatusWarning('Le tronçon sélectionné est trop distant du tracé en construction !')
			return

		sectionLine = featureList[0].geometry().asMultiPolyline()[0]
		sectionId = featureList[0].id()

		if orientation in ('AZ', 'AA'):										# Track has 1 section but reversed
			self.trackIdList[0] = - self.trackIdList[0]
			self.trackLine.reverse()
		
		if 	orientation in ('AZ', 'ZZ'):									# Section must be reversed
			sectionLine.reverse()
			sectionId = - sectionId
			
		self.trackLenghtList.append(len(self.trackLine))
		self.trackIdList.append(sectionId)	
		self.trackLine += sectionLine if delta > 0 else sectionLine[1:]

		self.refreshTrackInfo()
		self.layerSectionsGR.removeSelection()

		self.setStatusDone('Le tronçon sélectionné a été ajouté au tracé !')


# ========================================================================================
# Export du GPX
# ========================================================================================

	def exportTrackGPX_clicked(self):
	
#	Contrôles préalables 

		projectCode = self.projectGPXCombo.currentText()
		if projectCode == '':
			self.setStatusWarning('Le projet n\'est pas défini !')
			return

		fileName = self.nameGPX.text()
		if fileName == '':
			self.setStatusWarning('Le nom du fichier n\'est pas défini !')
			return

		if self.trackIdList == []:
			self.setStatusWarning('Le tracé est vide !')
			return		
		
		
#	Definir le path et le nom du fichier 		

		self.setStatusWorking('Export du Tracé GPX ...')
	
		timeStamp = ' (' + TDAT.getTimeStamp() + ')'
		pathGPX = QGP.configPathExportGPX.replace('%PROJECT%', projectCode)
		fileGpx = fileName + timeStamp + '.gpx'

#	Export GPX

		trackXYZ, missingAltitude1, missingAltitude2 = TALT.addTrackAltitudes(self.trackLine)
		TGPX.exportGpxTrack(pathGPX, fileGpx, 'No-Code', fileName, 'GPX créé par Tronçon', trackXYZ, set(), set())

		self.setStatusDone('Fichier GPX : ' + pathGPX + fileGpx + ' - OK')
		

# ========================================================================================
# Set Status : Error / Working / Ok
# ========================================================================================

	def setStatusError(self, text):
		textFormat = DSTY.textFormatStatusError
		self.labelStatus.setText(textFormat.replace('%TEXT%',text))
		self.labelStatus.setStyleSheet(DSTY.styleStatusError)
		QgsApplication.processEvents()

	def setStatusWarning(self, text):
		textFormat = DSTY.textFormatStatusWarning
		self.labelStatus.setText(textFormat.replace('%TEXT%',text))
		self.labelStatus.setStyleSheet(DSTY.styleStatusWarning)
		QgsApplication.processEvents()

	def setStatusWorking(self, text):
		textFormat = DSTY.textFormatStatusWorking
		self.labelStatus.setText(textFormat.replace('%TEXT%',text))
		self.labelStatus.setStyleSheet(DSTY.styleStatusWorking)
		QgsApplication.processEvents()

	def setStatusDone(self, text):
		textFormat = DSTY.textFormatStatusWorking
		self.labelStatus.setText(textFormat.replace('%TEXT%',text))
		self.labelStatus.setStyleSheet(DSTY.styleStatusDone)
		QgsApplication.processEvents()

	def setStatusOk(self, text):
		textFormat = DSTY.textFormatStatusOk
		self.labelStatus.setText(textFormat.replace('%TEXT%',text))
		self.labelStatus.setStyleSheet(DSTY.styleStatusOk)
		QgsApplication.processEvents()


# ========================================================================================
# ========================================================================================
#
# Création des différents cadres Menu
# 
# ========================================================================================
# ========================================================================================


# ========================================================================================
# Créer le cadre : Nom du tracé
# ========================================================================================

	def menuGPXCreationName(self):

		groupBoxName = QtWidgets.QGroupBox('Nom du tracé', self.dockCreateGPXWidget)
		groupBoxName.setStyleSheet(DSTY.styleBox)

#	Projet et Nom

		TBUT.createLabelBlackButton(groupBoxName, 1, 1, 'Projet / Nom', 'Normal', 'Normal')
		
		self.projectGPXCombo = TBUT.createComboButton(groupBoxName, 2, 1, 'Double')		
		self.projectGPXCombo.setPlaceholderText('Choisir un répertoire projet ...')
		for fileName in os.listdir(QGP.configPathProject) :
			if not os.path.isdir(QGP.configPathProject + fileName) : continue
			self.projectGPXCombo.addItem(fileName)		
		
		self.nameGPX = TBUT.createInputButton(groupBoxName, 4, 1, 'Double4')
	
#	Bouton Aide

		buttonHelp = TBUT.createHelpButton(groupBoxName, 8, 1, 'Aide', 'Normal')
		buttonHelp.clicked.connect(self.buttonHelp_clicked)
	
# 	Terminé

		groupBoxName.repaint()

		return groupBoxName


	def buttonHelp_clicked(self):
		webbrowser.open_new_tab(QGP.configMenuHelpBasePath + 'QCarto - Dock - Création GPX.html')
			

# ========================================================================================
# Créer le cadre : Info Section
# ========================================================================================

	def menuGPXCreationSection(self):

		groupBoxSection = QtWidgets.QGroupBox('Tronçon Sélectionné', self.dockCreateGPXWidget)
		groupBoxSection.setStyleSheet(DSTY.styleBox)

#	Info Tronçon

		TBUT.createLabelBlackButton(groupBoxSection, 1, 1, 'ID / Long / Delta', 'Normal', 'Normal')

		self.sectionInfoId = TBUT.createLabelGreenButton(groupBoxSection, 2, 1, '. . .', 'Normal', 'Normal')
		DSTY.setStyleWarningLabel(self.sectionInfoId, "Normal")

		self.sectionInfoLength = TBUT.createLabelGreenButton(groupBoxSection, 3, 1, '. . .', 'Normal', 'Normal')
		DSTY.setStyleWarningLabel(self.sectionInfoLength, "Normal")

		self.sectionInfoDelta = TBUT.createLabelGreenButton(groupBoxSection, 4, 1, '. . .', 'Normal', 'Normal')
		DSTY.setStyleWarningLabel(self.sectionInfoDelta, "Normal")
	
#	Bouton Ajouter Section

		buttonAddSection = TBUT.createActionButton(groupBoxSection, 6, 1, 'Ajouter', 'Normal')
		buttonAddSection.clicked.connect(self.addSection_clicked)				
		
# 	Terminé

		groupBoxSection.repaint()

		return groupBoxSection


# ========================================================================================
# Créer le cadre : Info Tracé
# ========================================================================================

	def menuGPXCreationTrack(self):

		groupBoxTrack = QtWidgets.QGroupBox('Parcours en Construction', self.dockCreateGPXWidget)
		groupBoxTrack.setStyleSheet(DSTY.styleBox)

#	Info Tronçon

		TBUT.createLabelBlackButton(groupBoxTrack, 1, 1, 'ID # / Long / D+ / D-', 'Normal', 'Normal')

		self.trackInfoIds = TBUT.createLabelGreenButton(groupBoxTrack, 2, 1, '. . .', 'Normal', 'Normal')
		DSTY.setStyleWarningLabel(self.trackInfoIds, "Normal")

		self.trackInfoLength = TBUT.createLabelGreenButton(groupBoxTrack, 3, 1, '. . .', 'Normal', 'Normal')
		DSTY.setStyleWarningLabel(self.trackInfoLength, "Normal")

		self.trackInfoDPlus = TBUT.createLabelGreenButton(groupBoxTrack, 4, 1, '. . .', 'Normal', 'Normal')
		DSTY.setStyleWarningLabel(self.trackInfoDPlus, "Normal")
	
		self.trackInfoDMinus = TBUT.createLabelGreenButton(groupBoxTrack, 5, 1, '. . .', 'Normal', 'Normal')
		DSTY.setStyleWarningLabel(self.trackInfoDMinus, "Normal")
	
#	Boutons

		buttonRazTrack = TBUT.createActionButton(groupBoxTrack, 6, 1, 'RAZ', 'Normal')
		buttonRazTrack.clicked.connect(self.razTrack_clicked)				

		buttonRemoveTrack = TBUT.createActionButton(groupBoxTrack, 7, 1, '<<<', 'Normal')
		buttonRemoveTrack.clicked.connect(self.removeTrack_clicked)				
	
		buttonExportTrackGPX = TBUT.createActionButton(groupBoxTrack, 8, 1, 'Export GPX', 'Normal')
		buttonExportTrackGPX.clicked.connect(self.exportTrackGPX_clicked)				
			
# 	Terminé

		groupBoxTrack.repaint()

		return groupBoxTrack


# ========================================================================================
# Créer le cadre : Status
# ========================================================================================

	def menuGPXCreationStatus(self):

		groupBoxStatus = QtWidgets.QGroupBox('Status', self.dockCreateGPXWidget)
		groupBoxStatus.setStyleSheet(DSTY.styleBox)

#	Status label

		self.labelStatus = QtWidgets.QLabel(groupBoxStatus)
		DSTY.setStatusLabel(self.labelStatus, 6, 'Normal')

# 	Terminé

		groupBoxStatus.repaint()

		return groupBoxStatus


# ========================================================================================
# Créer le cadre : Contrôles
# ========================================================================================

	def menuGPXCreationControls(self):

		groupBoxControls = QtWidgets.QGroupBox('Contrôles', self.dockCreateGPXWidget)
		groupBoxControls.setStyleSheet(DSTY.styleBox)

#	Bouton Exit

		buttonExit = TBUT.createActionButton(groupBoxControls, 2, 1, 'Fermer', 'Normal')
		buttonExit.clicked.connect(self.requestClose_clicked)				

# 	Terminé

		groupBoxControls.repaint()

		return groupBoxControls


# ========================================================================================
# --- THE END ---
# ========================================================================================
