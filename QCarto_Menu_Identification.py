# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Gestion des Menus : Identification des Tronçons du Réseau GR
# ========================================================================================

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qgis.core import *
from qgis.gui import *
from qgis.PyQt import QtWidgets

import time
import math
import webbrowser
import importlib

import QCarto_Definitions_Colors as DCOL
import QCarto_Definitions_Styles as DSTY

import QCarto_Tools_Buttons as TBUT
import QCarto_Tools_Layers as TLAY
import QCarto_Tools_Coding as TCOD
import QCarto_Tools_Input as TINP
importlib.reload(TINP)


try:
	import SGRBalisage_WindowHistoricSegment
	importlib.reload(SGRBalisage_WindowHistoricSegment)
except:
	pass
	
import QCarto_Parameters_Global
importlib.reload(QCarto_Parameters_Global)
QGP = QCarto_Parameters_Global.globalParameters()


# ========================================================================================
# Class : identificationView
# >>> self
# >>> iface
# ========================================================================================

class identificationView:

	def __init__(self, iface, mainFrame, enableEdition = False):

		self.iface = iface
		self.mainFrame = mainFrame
		self.enableEdition = enableEdition
		self.sectionId = None
		self.pointsIdList = []
	
# Retrouver la couche des Baliseurs si présente
	
		layerName = QGP.configBaliseursTracksLayerName
		self.layerTracksBaliseurs, error = TLAY.findLayerInGroup(QGP.configBaliseursGroup, layerName)
		
# Création de la fenêtre
		
		self.groupView = QtWidgets.QDockWidget(self.iface.mainWindow())
		self.groupView.setFeatures(QtWidgets.QDockWidget.DockWidgetFloatable | QtWidgets.QDockWidget.DockWidgetClosable)
		self.iface.addDockWidget(Qt.TopDockWidgetArea, self.groupView)

		self.groupView.setWindowFlag(Qt.WindowStaysOnTopHint, True)
		self.groupView.setWindowIcon(QIcon(QGP.configActionIcon_GrI))

		self.groupView.hide()																				
		self.groupView.repaint()
		
# Dictionnaire des Tracés GR + RB - déterminé une fois pour toute à partir des dictionnaires main frame
	
		self.dicoTracksGRRBFeatures = { TCOD.purifyTrackCode(trackCode) : self.mainFrame.dicoTracksRBFeatures[trackCode] for trackCode in self.mainFrame.dicoTracksRBFeatures }
		self.dicoTracksGRRBFeatures.update(self.mainFrame.dicoTracksGRFeatures)

# Dictionnaire des Tracés indirects

		self.dicoTracksGRRBIndirectCodes = { code : self.dicoTracksGRRBFeatures[code][QGP.tableTracksFieldIndirect] for code in self.dicoTracksGRRBFeatures if self.dicoTracksGRRBFeatures[code][QGP.tableTracksFieldIndirect] != None }

		print (str(self.dicoTracksGRRBIndirectCodes))

# Création des Cadres	
	
		self.createBoxes()
	
# Redirection de fermeture	
	
		self.groupView.closeEvent = self.dockWidgetClosing


# ----------------------------------------------------------
# Reset pan action tool on exit
# ----------------------------------------------------------

	def dockWidgetClosing(self, event):
		action = self.iface.actionPan()
		action.trigger()
		event.accept()
	
	
# ----------------------------------------------------------
# Création des Cadres sous-menus
# ----------------------------------------------------------

	def createBoxes(self):

		self.groupBoxTrack, self.sectionCurrentId, self.trackCurrentDist, self.sectionCartoName, self.sectionDateModif, self.sectionBaliseur, self.sectionBaliseurDuo  = \
				identificationViewTrackFrame(self.iface, self, self.groupView)
		self.groupBoxTrack.repaint()
		DSTY.setBoxGeometryShort(self.groupBoxTrack, 1, 1, 12, 1)

		self.groupBoxListFrame = identificationViewGrListFrame(self.iface, self, self.groupView)
		self.groupBoxListFrame.repaint()
		DSTY.setBoxGeometryShort(self.groupBoxListFrame, 1, 3, 7, 7)

		self.tableWidget = identificationViewGrListTable(self.iface, self, self.groupView)
		self.tableWidget.repaint()
		DSTY.setBoxGeometryShort(self.tableWidget, 1, 3, 7, 7, True)

		self.groupBoxListFramePoints = identificationViewPointListFrame(self.iface, self, self.groupView)
		self.groupBoxListFramePoints.repaint()
		DSTY.setBoxGeometryShort(self.groupBoxListFramePoints, 8, 3, 5, 7)

		self.tableWidgetPoints = identificationViewPointListTable(self.iface, self, self.groupView)
		self.tableWidgetPoints.repaint()
		DSTY.setBoxGeometryShort(self.tableWidgetPoints, 8, 3, 5, 7, True)

		self.boxesList = [self.groupBoxTrack, self.groupBoxListFrame, self.tableWidget, self.groupBoxListFramePoints, self.tableWidgetPoints]
	
	
# ========================================================================================
# Update : update track info // show (display window) // hide (hide window) // close (terminate)
# ========================================================================================

	def update(self, closestFeatureSection, closeFeaturesPoint = []):
		self.closestFeatureSection = closestFeatureSection									# Remember here for double-clic edit
		if closestFeatureSection != None:
			self.sectionId = closestFeatureSection[QGP.tableSectionsFieldId]
			self.showTrackInfo(closestFeatureSection)
			self.showCodesInfo(closestFeatureSection)
		else:
			self.sectionId = None
			self.clearTrackInfo()
			self.clearCodesInfo()
			
		if len(closeFeaturesPoint) > 0:
			self.showPointsInfo(closeFeaturesPoint)
			self.pointsIdList = [feature.id() for feature in closeFeaturesPoint]
		else:
			self.clearPointsInfo()
			self.pointsIdList = []
			
	def show(self):
		self.groupView.show()	
		self.groupView.showNormal()
		
	def hide(self):
		self.groupView.hide()	

	def close(self):
		for box in self.boxesList: 	del box
		self.groupView.hide()	
		self.groupView.deleteLater()


# ========================================================================================
# Show Track / Track Code Information
# ========================================================================================

	def getItemText(self, type, trackCode):
		if type in QGP.typeSetTableGR:
			if TCOD.isCodePrincipalGR(trackCode) : 
				itemText = '■■■■■■■■■■■■■■■'
			elif TCOD.isCodeVarianteGR(trackCode) : 
				itemText = '■■■ ■■■ ■■■ ■■■' 
			elif TCOD.isCodeLiaisonGR(trackCode) : 
				itemText = '■ ■ ■ ■ ■ ■ ■ ■' 
			elif TCOD.isCodeBoucleGR(trackCode) : 
				itemText = '■ ■ ■ ■ ■ ■ ■ ■'
			else:
				itemText = '■    ■    ■'
		if type in QGP.typeSetTableRB:
			if type == 'RI':
				itemText = '■■■ ■ ■■■ ■ ■■■' 
			else:
				itemText = '■ ■ ■ ■ ■ ■ ■ ■'
		return itemText

	def getItemColor(self, type):
		if type == 'GR':
			color = DCOL.fgTrackGR
		elif type == 'GRP':
			color = DCOL.fgTrackGRP
		elif type == 'GRT':
			color = DCOL.fgTrackGRT
		elif type == 'RI':
			color = DCOL.fgTrackRI
		elif type == 'RB':
			color = DCOL.fgTrackRB
		elif type == 'RF':
			color = DCOL.fgTrackRF
		elif type == 'RL':
			color = DCOL.fgTrackRL
		else:
			color = DCOL.fgTrackOther
		return color

	def showTrackInfo(self, featureSection):
		text = DSTY.textFormatBlackSmall.replace('%TEXT%',str(self.sectionId))
		self.sectionCurrentId.setText(text)

		dist = featureSection.geometry().length()
		text = DSTY.textFormatBlackSmall.replace('%TEXT%','{:,.2f}'.format(dist/1000) + ' km')
		self.trackCurrentDist.setText(text)

		cartoName = featureSection[QGP.tableAllFieldNomCarto] if featureSection[QGP.tableAllFieldNomCarto] != None else '---'
		text = DSTY.textFormatBlackSmall.replace('%TEXT%',str(cartoName))
		self.sectionCartoName.setText(text)

		dateModif = featureSection[QGP.tableAllFieldDateModif] if featureSection[QGP.tableAllFieldDateModif] != None else '--- Carto et Date non disponibles ---'
		text = DSTY.textFormatBlackSmall.replace('%TEXT%',str(dateModif))
		self.sectionDateModif.setText(text)

		text1 = '--- Info Baliseur non disponible ---'
		text2 = '--- Info Baliseur duo non disponible ---'
		if self.layerTracksBaliseurs != None:
			text1 = '--- Pas de baliseur ---'
			text2 = '--- Pas de baliseur duo ---'
			try:	
				baliseurTrackFeature = [f for f in self.layerTracksBaliseurs.getFeatures() if int(f[QGP.configBaliseursTracksFieldIdRcaj]) == self.sectionId][0]
				baliseurId = baliseurTrackFeature[QGP.configBaliseursTracksFieldIdBaliseur]
				baliseurNom = baliseurTrackFeature[QGP.configBaliseursTracksFieldNomBaliseur]
				baliseurDuoId = baliseurTrackFeature[QGP.configBaliseursTracksFieldIdBaliseurDuo]
				baliseurDuoNom = baliseurTrackFeature[QGP.configBaliseursTracksFieldNomBaliseurDuo]
				if baliseurId != None:
					text1 = DSTY.textFormatBlackSmall.replace('%TEXT%', 'Bal : ' + str(baliseurNom) + ' [' + str(baliseurId) + ']')
				if baliseurDuoId != None:
					text2 = DSTY.textFormatBlackSmall.replace('%TEXT%', 'Duo : ' + str(baliseurDuoNom) + ' [' + str(baliseurDuoId) + ']')
			except:
				pass
		self.sectionBaliseur.setText(text1)
		self.sectionBaliseurDuo.setText(text2)

	def clearTrackInfo(self):
		text = DSTY.textFormatBlackSmall.replace('%TEXT%','. . .')
		self.sectionCurrentId.setText(text)
		self.trackCurrentDist.setText(text)
		self.sectionBaliseur.setText(text)
		self.sectionBaliseurDuo.setText(text)
	
	def showCodesInfo(self, featureSection):
		codeList = TCOD.getCodeListALLFromSectionFeature(featureSection)
		for indirectCode in self.dicoTracksGRRBIndirectCodes:
			if self.dicoTracksGRRBIndirectCodes[indirectCode] in codeList:
				codeList.append(indirectCode)

		self.tableWidget.setRowCount(len(codeList))
		itemFont = QFont()
		itemFont.setPixelSize(DSTY.tableItemFontSize)
		itemFontSmall = QFont()
		itemFontSmall.setPixelSize(DSTY.tableItemFontSizeSmall)


		for row in range(len(codeList)):
		
#		Code			
			code = str(codeList[row])
			itemText = code
			item = QtWidgets.QTableWidgetItem(itemText)
			item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
			item.setFont(itemFontSmall)
			self.tableWidget.setItem(row, 0, item)

			valid, type, label, zone, number, itineraryCode, trackBaseCode, trackCode, modificationList, invalidationList, repeatCount, bifurcationNumber, direction = TCOD.elementsFromGrCode(code)		
			if not valid: continue

#		Début
			itemText = '■' if direction != None else ''
			item = QtWidgets.QTableWidgetItem(itemText)
			item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
			item.setFont(itemFontSmall)
			item.setFont(QFont('Consolas'))
			item.setFlags(item.flags() & ~Qt.ItemIsEditable)
			self.tableWidget.setItem(row, 1, item)

#		Type
			itemText = self.getItemText(type, trackCode)
			item = QtWidgets.QTableWidgetItem(itemText)
			item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
			item.setFont(itemFontSmall)
			item.setFont(QFont('Consolas'))
			color = self.getItemColor(type)
			item.setForeground(color)
			item.setFlags(item.flags() & ~Qt.ItemIsEditable)
			self.tableWidget.setItem(row, 2, item)

#		Nom
			itemText = str(self.dicoTracksGRRBFeatures[trackCode][QGP.tableTracksFieldName]) if trackCode in self.dicoTracksGRRBFeatures else "?! Ce code n'est pas défini ?!"
			item = QtWidgets.QTableWidgetItem(itemText)
			item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
			item.setFont(itemFontSmall)
			item.setFlags(item.flags() & ~Qt.ItemIsEditable)
			self.tableWidget.setItem(row, 3, item)
			if trackCode not in self.dicoTracksGRRBFeatures:	continue

#		Etat
			state = self.dicoTracksGRRBFeatures[trackCode][QGP.tableTracksFieldStatus]
			itemText = str(state)
			item = QtWidgets.QTableWidgetItem(itemText)
			item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
			item.setFont(itemFontSmall)
			item.setFlags(item.flags() & ~Qt.ItemIsEditable)
			self.tableWidget.setItem(row, 4, item)

#		Distance
			dist = self.dicoTracksGRRBFeatures[trackCode][QGP.tableTracksFieldDistance]
			if dist == None: continue
			itemText = '{:,.1f}'.format(dist/1000).replace(',','.') + ' km  '
			item = QtWidgets.QTableWidgetItem(itemText)
			item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
			item.setFont(itemFontSmall)
			item.setFlags(item.flags() & ~Qt.ItemIsEditable)
			self.tableWidget.setItem(row, 5, item)

#		Segments
			seg = self.dicoTracksGRRBFeatures[trackCode][QGP.tableTracksFieldTroncons]
			if seg == None: continue
			itemText = str(len(seg)) + ' '
			item = QtWidgets.QTableWidgetItem(itemText)
			item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
			item.setFont(itemFontSmall)
			item.setFlags(item.flags() & ~Qt.ItemIsEditable)
			self.tableWidget.setItem(row, 6, item)


	def clearCodesInfo(self):
		self.tableWidget.setRowCount(0)


# ========================================================================================
# Show Point Information
# ========================================================================================

	def showPointsInfo(self, featurePointsList):
	
		self.tableWidgetPoints.setRowCount(len(featurePointsList))
		itemFontSmall = QFont()
		itemFontSmall.setPixelSize(DSTY.tableItemFontSizeSmall)
	
		for row in range(len(featurePointsList)):
	
# 		Id	
			id = str(featurePointsList[row][QGP.tablePointsFieldId])
			itemText = id
			item = QtWidgets.QTableWidgetItem(itemText)
			item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
			item.setFont(itemFontSmall)
			item.setFlags(item.flags() & ~Qt.ItemIsEditable)
			self.tableWidgetPoints.setItem(row, 0, item)

# 		Code
			code = str(featurePointsList[row][QGP.tablePointsFieldGRCode])
			itemText = code
			item = QtWidgets.QTableWidgetItem(itemText)
			item.setTextAlignment(Qt.AlignLeft| Qt.AlignVCenter)
			item.setFont(itemFontSmall)
			item.setFlags(item.flags() & ~Qt.ItemIsEditable)
			self.tableWidgetPoints.setItem(row, 1, item)

			valid, type, label, zone, number, itineraryCode, trackBaseCode, trackCode, modificationList, invalidationList, repeatCount, bifurcationNumber, direction = TCOD.elementsFromGrCode(code)		
			if not valid: continue

#		Type
			itemText = self.getItemText(type, trackCode)
			item = QtWidgets.QTableWidgetItem(itemText)
			item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
			item.setFont(QFont('Consolas'))
			color = self.getItemColor(type)
			item.setForeground(color)
			item.setFlags(item.flags() & ~Qt.ItemIsEditable)
			self.tableWidgetPoints.setItem(row, 2, item)

# 		Repère
			repere = str(featurePointsList[row][QGP.tablePointsFieldRepere])
			itemText = repere
			item = QtWidgets.QTableWidgetItem(itemText)
			item.setTextAlignment(Qt.AlignCenter| Qt.AlignVCenter)
			item.setFont(itemFontSmall)
			item.setFlags(item.flags() & ~Qt.ItemIsEditable)
			self.tableWidgetPoints.setItem(row, 3, item)

# 		Nom
			nom = str(featurePointsList[row][QGP.tablePointsFieldNom])
			itemText = nom
			item = QtWidgets.QTableWidgetItem(itemText)
			item.setTextAlignment(Qt.AlignLeft| Qt.AlignVCenter)
			item.setFont(itemFontSmall)
			item.setFlags(item.flags() & ~Qt.ItemIsEditable)
			self.tableWidgetPoints.setItem(row, 4, item)

	def clearPointsInfo(self):
		self.tableWidgetPoints.setRowCount(0)


# ========================================================================================
# Actions Sélection when right clic on Section Id
# ========================================================================================

	def buttonSectionCurrentId_rightClicked(self):
		if self.sectionId == None: return
		if self.mainFrame.layerSectionsGR == None: return
		self.mainFrame.layerSectionsGR.selectByIds([self.sectionId])
		self.mainFrame.layerPointsGR.selectByIds(self.pointsIdList)


# ========================================================================================
# Actions Edition when double clic on Section Id
# ========================================================================================

	def buttonSectionCurrentId_doubleClicked(self):
		if self.sectionId == None: return
		if self.mainFrame.layerSectionsGR == None: return
		if self.closestFeatureSection == None : return
		self.closestFeatureSectionXCodes = [(self.closestFeatureSection[_] if self.closestFeatureSection[_] != None else ' ') for _ in QGP.tableSectionsFieldAllXList]
		self.xListInputWindow = TINP.inputFromText(self.iface, self, 'Tronçon = ' + str(self.sectionId) + ' : Modifier les codes x_list', QGP.tableSectionsFieldAllXList, self.closestFeatureSectionXCodes, self.editSectionXListCodesResult)	

	def editSectionXListCodesResult(self, status, newCodesList):
		del self.xListInputWindow
		if not status : return
		if newCodesList == self.closestFeatureSectionXCodes: return
		try:
			layerSectionAlreadyEditable = self.mainFrame.layerSectionsGR.isEditable()
			self.mainFrame.layerSectionsGR.startEditing()
			for field, value in zip(QGP.tableSectionsFieldAllXList, newCodesList) :
				self.mainFrame.layerSectionsGR.changeAttributeValue(self.closestFeatureSection.id(), self.closestFeatureSection.fieldNameIndex(field), value)
			if not layerSectionAlreadyEditable : self.mainFrame.layerSectionsGR.commitChanges()
		except:
			self.mainFrame.setStatusError('Tronçon ' + str(self.closestFeatureSection.id()) + ' : erreur imprévue lors de la mise à jour du tronçon !', False)
			self.mainFrame.mainMenu.activateWindow()
			self.mainFrame.mainMenu.show()
		for field, value in zip(QGP.tableSectionsFieldAllXList, newCodesList) : self.closestFeatureSection[field] = value
		self.showTrackInfo(self.closestFeatureSection)
		self.showCodesInfo(self.closestFeatureSection)
			

# ========================================================================================
# Actions Right Click on Table - Experimental
# ========================================================================================

	def tableWidget_rightClicked(self, point):
		item = self.tableWidget.itemAt(point)

# ========================================================================================
# Actions Historique Baliseurs
# ========================================================================================

	def buttonBaliseurHistorique_clicked(self):
		if self.sectionId == None: return
		importlib.reload(SGRBalisage_WindowHistoricSegment)
		self.historyWindow = SGRBalisage_WindowHistoricSegment.baliseurHistoryWindow(self.iface, self)
		self.historyWindow.refresh()
		self.historyWindow.show()
		

# ========================================================================================
# Créer le cadre : Track Info
# >>> iface
# >>> parentFrame   : class identificationView
# >>> parentWidget  : widget						Parent where to install local Widgets
# ========================================================================================

def identificationViewTrackFrame(iface, parentFrame, parentWidget):

# ----------------------------------------------------------
# Créer Groupe : Identification Infos
# ----------------------------------------------------------
		
	groupBox = QtWidgets.QGroupBox('Identification - Tronçon GR / RB', parentWidget)
	groupBox.setStyleSheet(DSTY.styleBox)

	sectionCurrentId = TBUT.createLabelGreenButton(groupBox, 1, 1, '. . .', 'Short', 'Normal')
	DSTY.setStyleOkLabel(sectionCurrentId, "Short")

	if parentFrame.enableEdition :
		sectionIdHidden = TBUT.createActionButtonTransparent(groupBox, 1, 1, '', 'Normal')
		sectionIdHidden.setContextMenuPolicy(Qt.CustomContextMenu)
		sectionIdHidden.customContextMenuRequested.connect(parentFrame.buttonSectionCurrentId_rightClicked)
		sectionIdHidden.clicked.connect(parentFrame.buttonSectionCurrentId_doubleClicked)

	trackCurrentDist = TBUT.createLabelGreenButton(groupBox, 2, 1, '. . .', 'Short', 'Normal')
	DSTY.setStyleOkLabel(trackCurrentDist, "Short")

	sectionCartoName = TBUT.createLabelGreenButton(groupBox, 3, 1, '. . .', 'Short', 'Normal')
	DSTY.setStyleOkLabel(sectionCartoName, "Short")

	sectionDateModif = TBUT.createLabelGreenButton(groupBox, 4, 1, '. . .', 'ShortDouble', 'Normal')
	DSTY.setStyleOkLabel(sectionDateModif, "ShortDouble")

	sectionBaliseur = TBUT.createLabelGreenButton(groupBox, 6, 1, '. . .', 'ShortDouble', 'Normal')
	DSTY.setStyleOkLabel(sectionBaliseur, "ShortDouble")

	sectionBaliseurDuo = TBUT.createLabelGreenButton(groupBox, 8, 1, '. . .', 'ShortDouble', 'Normal')
	DSTY.setStyleOkLabel(sectionBaliseurDuo, "ShortDouble")

	if parentFrame.layerTracksBaliseurs != None:
		buttonBaliseurHistorique = TBUT.createActionButton(groupBox, 10, 1, 'Historique', 'Short')
		buttonBaliseurHistorique.clicked.connect(parentFrame.buttonBaliseurHistorique_clicked)

	buttonHelp = TBUT.createHelpButton(groupBox, 12, 1, 'Aide', 'Short')
	buttonHelp.clicked.connect(buttonHelp_clicked)

	groupBox.show()																				
	groupBox.repaint()
	
	return groupBox, sectionCurrentId, trackCurrentDist, sectionCartoName, sectionDateModif, sectionBaliseur, sectionBaliseurDuo

def buttonHelp_clicked():
	webbrowser.open_new_tab(QGP.configMenuHelpBasePath + 'QCarto - Docks - Identification.html')
	


# ========================================================================================
# Créer le cadre : Gr List Frame
# >>> iface
# >>> parentFrame   : class identificationView
# >>> parentWidget  : widget						Parent where to install local Widgets
# ========================================================================================

def identificationViewGrListFrame(iface, parentFrame, parentWidget):

# ----------------------------------------------------------
# Créer Groupe : Identification Tronçon
# ----------------------------------------------------------
		
	groupBox = QtWidgets.QGroupBox('Identification - Parcours GR / RB', parentWidget)
	groupBox.setStyleSheet(DSTY.styleBox)

	groupBox.show()																				
	groupBox.repaint()
	
	return groupBox


# ========================================================================================
# Créer la table : Gr List
# >>> iface
# >>> parentFrame   : class identificationView
# >>> parentWidget  : widget						Parent where to install local Widgets
# ========================================================================================

def identificationViewGrListTable(iface, parentFrame, parentWidget):

# ----------------------------------------------------------
# Créer la Table 
# ----------------------------------------------------------
		
	rowsCount = 0
	columnsCount = len(QGP.configTableIdViewFields)
		
	tableWidget = QtWidgets.QTableWidget(rowsCount,columnsCount,parentWidget)
	tableWidget.repaint()
	
	DSTY.setStyleTableTraces(tableWidget)
	
	
	tableWidget.setContextMenuPolicy(Qt.CustomContextMenu)
	tableWidget.customContextMenuRequested.connect(parentFrame.tableWidget_rightClicked)
	
# ----------------------------------------------------------
# Entêtes de colonnes
# ----------------------------------------------------------
	
	tableFields = QGP.configTableIdViewFields
	
	for col in range(len(tableFields)):
		tableWidget.setHorizontalHeaderItem(col, QtWidgets.QTableWidgetItem(tableFields[col][0]))
		tableWidget.setColumnWidth(col, tableFields[col][1])

	return tableWidget


# ========================================================================================
# Créer le cadre :  List Frame Points
# >>> iface
# >>> parentFrame   : class identificationView
# >>> parentWidget  : widget						Parent where to install local Widgets
# ========================================================================================

def identificationViewPointListFrame(iface, parentFrame, parentWidget):

# ----------------------------------------------------------
# Créer Groupe : Identification Tronçon
# ----------------------------------------------------------
		
	groupBox = QtWidgets.QGroupBox('Identification - Repères GR / RB', parentWidget)
	groupBox.setStyleSheet(DSTY.styleBox)

	groupBox.show()																				
	groupBox.repaint()
	
	return groupBox


# ========================================================================================
# Créer la table : Gr List
# >>> iface
# >>> parentFrame   : class identificationView
# >>> parentWidget  : widget						Parent where to install local Widgets
# ========================================================================================

def identificationViewPointListTable(iface, parentFrame, parentWidget):

# ----------------------------------------------------------
# Créer la Table 
# ----------------------------------------------------------
		
	rowsCount = 0
	columnsCount = len(QGP.configTablePointViewFields)
		
	tableWidget = QtWidgets.QTableWidget(rowsCount,columnsCount,parentWidget)
	tableWidget.repaint()
	
	DSTY.setStyleTableTraces(tableWidget)
	
# ----------------------------------------------------------
# Entêtes de colonnes
# ----------------------------------------------------------
	
	tableFields = QGP.configTablePointViewFields
	
	for col in range(len(tableFields)):
		tableWidget.setHorizontalHeaderItem(col, QtWidgets.QTableWidgetItem(tableFields[col][0]))
		tableWidget.setColumnWidth(col, tableFields[col][1])

	return tableWidget


# ========================================================================================
# --- THE END ---
# ========================================================================================
