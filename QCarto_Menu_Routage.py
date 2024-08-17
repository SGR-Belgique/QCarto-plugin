# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Gestion des Menus : Page Routage
# ========================================================================================


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qgis.core import *
from qgis.gui import *
from qgis.PyQt import QtWidgets

import webbrowser
import importlib
import time
import os

import QCarto_Layers_Tracks as LTRK
importlib.reload(LTRK)

import QCarto_Tools_QParam as TQCP
importlib.reload(TQCP)
import QCarto_Tools_Altitudes as TALT
importlib.reload(TALT)
import QCarto_Tools_Bornage as TBOR
importlib.reload(TBOR)
import QCarto_Tools_Coding as TCOD
importlib.reload(TCOD)
import QCarto_Tools_Dates as TDAT
importlib.reload(TDAT)
import QCarto_Tools_Buttons as TBUT
importlib.reload(TBUT)
import QCarto_Tools_Files as TFIL
importlib.reload(TFIL)
import QCarto_Tools_Layers as TLAY
importlib.reload(TLAY)
import QCarto_Tools_IGN as TIGN
importlib.reload(TIGN)
import QCarto_Tools_CSV as TCSV
importlib.reload(TCSV)
import QCarto_Tools_GPX as TGPX
importlib.reload(TGPX)
import QCarto_Tools_PlanRB as TPRB
importlib.reload(TPRB)
import QCarto_Tools_Help as THEL
importlib.reload(THEL)
import QCarto_Tools_Input as TINP
importlib.reload(TINP)
import QCarto_Tools_Ozi as TOZI
importlib.reload(TOZI)
import QCarto_Tools_Progress as TPRO
import QCarto_Tools_SCR as TSCR
importlib.reload(TSCR)
import QCarto_Tools_SiteGR as TSGR
importlib.reload(TSGR)

import QCarto_Definitions_Colors as DCOL
importlib.reload(DCOL)
import QCarto_Definitions_Styles as DSTY
importlib.reload(DSTY)
import QCarto_Definitions_TopoGuides as DTOP	
importlib.reload(DTOP)
import QCarto_Definitions_Symbologie as DSYM
importlib.reload(DSYM)

import QCarto_Parameters_Global
importlib.reload(QCarto_Parameters_Global)
QGP = QCarto_Parameters_Global.globalParameters()


# ========================================================================================
# Constantes locales à cette page
# ========================================================================================

C_ComboGRRBList_GR = 'GR.P seul'
C_ComboGRRBList_GRRB  = 'GR.P + RB.F'
C_ComboGRRBList = [C_ComboGRRBList_GR, C_ComboGRRBList_GRRB]

C_ComboRBFactor = ['├─┤ RB = 1 x GR', '├─┤ RB = 3 x GR', '├─┤ RB = 5 x GR', '├─┤ RB = 10 x GR', '├─┤ RB = 100 x GR']


# ========================================================================================
# Class : menuRoutageFrame
# >>> iface
# >>> mainMenu 				: Widget of Main Menu
# >>> mainFrame 			: Main Menu Object
# ========================================================================================

class menuRoutageFrame:

	def __init__(self, iface, mainMenu, mainFrame):

# 	Paramètres fournis

		self.iface = iface
		self.mainMenu = mainMenu
		self.mainFrame = mainFrame

#	Accès aux Tables de la DB Carto

		self.layerTracksGR, 		self.layerTracksGRerror 		= self.mainFrame.layerTracksGR, 		self.mainFrame.layerTracksGRerror 	
		self.layerTracksRB, 		self.layerTracksRBerror 		= self.mainFrame.layerTracksRB, 		self.mainFrame.layerTracksRBerror 	
		self.layerTracksGRHist, 	self.layerTracksGRHisterror		= self.mainFrame.layerTracksGRHist, 	self.mainFrame.layerTracksGRHisterror 	
		self.layerTracksRBHist, 	self.layerTracksRBHisterror		= self.mainFrame.layerTracksRBHist, 	self.mainFrame.layerTracksRBHisterror 	
		self.layerSectionsGR, 		self.layerSectionsGRerror 		= self.mainFrame.layerSectionsGR, 		self.mainFrame.layerSectionsGRerror 	
		self.layerPointsGR, 		self.layerPointsGRError 		= self.mainFrame.layerPointsGR, 		self.mainFrame.layerPointsGRError 	
		self.layerCommunes, 		self.layerCommunesError			= self.mainFrame.layerCommunes, 		self.mainFrame.layerCommunesError		

#	Variables principales

		self.canvas = self.iface.mapCanvas()

		self.routingPointsCount = 0												# Nombre de points de routage définis
		self.routingPointCurrent = 0											# Point Current
		
		self.definingCanevasPoint = False										# En cours de sélection du point sur le canevas
		self.routingCanevasPoint = None											# Dernier point défini sur le canevas

		self.routingPointsDico = {}												# Dictionnaire des Points de routage	


#	Analyser les Tables DB		
		
		self.analyseTablesTracks(False)		
		
#	Créer les sous-menus 

		self.boxesList = []
		self.createMenuBoxes()
		self.refreshAllBoxes()
		

		
		self.mainFrame.setStatusDone('Page Routage créée !')

		
	def createMenuBoxes(self):

		self.groupBoxRoutingPoints = self.menuBoxRoutingPoints()
		DSTY.setBoxGeometry(self.groupBoxRoutingPoints, 1, 4, 4, 5)
		self.boxesList.append(self.groupBoxRoutingPoints)

		self.groupBoxRoutingWays = self.menuBoxRoutingWays()
		DSTY.setBoxGeometry(self.groupBoxRoutingWays, 5, 4, 2, 5)
		self.boxesList.append(self.groupBoxRoutingWays)

		self.groupBoxOptions = self.menuBoxOptions()
		DSTY.setBoxGeometry(self.groupBoxOptions, 7, 4, 1, 5)
		self.boxesList.append(self.groupBoxOptions)
		
		self.groupBoxActions = self.menuBoxActions()
		DSTY.setBoxGeometry(self.groupBoxActions, 8, 4, 1, 5)
		self.boxesList.append(self.groupBoxActions)
		
		self.groupBoxTracksFrame = self.menuBoxTableTracksFrame()
		DSTY.setBoxGeometry(self.groupBoxTracksFrame, 1, 10, 8, 17)
		self.boxesList.append(self.groupBoxTracksFrame)

		self.groupBoxTrackRoutingTable = self.menuBoxTableTracksView()
		DSTY.setBoxGeometry(self.groupBoxTrackRoutingTable, 1, 10, 8, 17, True)
		self.boxesList.append(self.groupBoxTrackRoutingTable)


# ========================================================================================
# Actions : A la demande de la fenêtre principale
# ========================================================================================

#	Show - Ouverture de cette fenêtre

	def show(self):
		for box in self.boxesList:
			box.show()
			box.repaint()

#	Hide - Ouverture d'une autre fenêtre

	def hide(self):
		for box in self.boxesList:
			box.hide()

#	Close - Fermeture définitive

	def close(self):
		self.hide()
		for box in self.boxesList:
			del box

#	Help on this page

	def help(self):
		webbrowser.open_new_tab(QGP.configMenuHelpBasePath + 'QCarto - Page - Routage.html')
	
	
	
# ========================================================================================
# ========================================================================================
#
# Définitions des Listes et Dictionnaires Globaux
# 
# ========================================================================================
# ========================================================================================

#	Table : Parcours-GR et Parcours)RB

	def analyseTablesTracks(self, reloadDico = False) :
		self.mainFrame.setStatusWorking('Analyse des Tables Parcours GR / RB ...')
		self.analyseTableTracksGR(reloadDico)
		self.analyseTableTracksRB(reloadDico)
		self.mainFrame.setStatusDone('Analyse des Tables Parcours GR / RB - OK')

#	Table : Parcours-GR

	def analyseTableTracksGR(self, reloadDico = False) :
		if self.layerTracksGR == None:
			self.mainFrame.setStatusError(self.layerTracksGRerror, False)
			return

		if reloadDico : self.mainFrame.dicoTracksGRFeatures = {f[QGP.tableTracksFieldCode] : f for f in self.layerTracksGR.getFeatures()}

		self.listItineraryGR = LTRK.getOrderedListItineraryGR({'GR'}, self.mainFrame.dicoTracksGRFeatures)
		self.listItineraryGRP = LTRK.getOrderedListItineraryGR({'GRP'}, self.mainFrame.dicoTracksGRFeatures)
		self.listItineraryGRT = LTRK.getOrderedListItineraryGR({'GRT'}, self.mainFrame.dicoTracksGRFeatures)

#	Table : Parcours-RB

	def analyseTableTracksRB(self, reloadDico = False) :
		if self.layerTracksRB == None:
			self.mainFrame.setStatusError(self.layerTracksRBerror, False)
			return

		if reloadDico : self.mainFrame.dicoTracksRBFeatures = {f[QGP.tableTracksFieldCode] : f for f in self.layerTracksRB.getFeatures()}

		self.listItineraryRI = LTRK.getOrderedListItineraryRB({'RI'}, self.mainFrame.dicoTracksRBFeatures, itineraryFolderMode = False)
		self.listItineraryRL = LTRK.getOrderedListItineraryRB({'RL'}, self.mainFrame.dicoTracksRBFeatures, itineraryFolderMode = False)
		self.listItineraryRB = LTRK.getOrderedListItineraryRB({'RB'}, self.mainFrame.dicoTracksRBFeatures, itineraryFolderMode = False)
		self.listItineraryRF = LTRK.getOrderedListItineraryRB({'RF'}, self.mainFrame.dicoTracksRBFeatures, itineraryFolderMode = False)
		self.listItineraryIR = LTRK.getOrderedListItineraryRB({'IR'}, self.mainFrame.dicoTracksRBFeatures, itineraryFolderMode = False)
	
	
	
	
	
	
	
# ========================================================================================
# ========================================================================================
#
# Rafraichir les différents Cadres
# 
# ========================================================================================
# ========================================================================================

	def refreshAllBoxes(self) :
		self.refreshRoutingPointsBox()
		
	def refreshRoutingPointsBox(self) :
	
		pointsCount = DSTY.textFormatBlackNormal.replace('%TEXT%',str(self.routingPointsCount) + ' point.s')
		self.routingPointsCountInfo.setText(pointsCount)
		DSTY.setStyleOkLabel(self.routingPointsCountInfo, 'Normal')

		self.routingCurrentPointCombo.clear()
		for i in range(self.routingPointsCount + 1) :
			self.routingCurrentPointCombo.addItem('Point ' + str(i))
		self.routingCurrentPointCombo.setCurrentIndex(self.routingPointCurrent)
			
		self.refreshRoutingPointsBoxItinerary()	
		self.refreshRoutingPointsBoxMark()
	
	def refreshRoutingPointsBoxItinerary(self) :
		self.routingPointSelectTrackCombo.currentIndexChanged.disconnect()
		self.routingPointSelectTrackCombo.clear()
		self.routingPointSelectTrackCombo.addItem(' ')
		for itinerary in self.listItineraryGR + self.listItineraryGRP + self.listItineraryGRT :
			if (itinerary in self.mainFrame.dicoTracksGRFeatures) and (self.mainFrame.dicoTracksGRFeatures[itinerary][QGP.tableTracksFieldStatus] != QGP.trackStatusPublished) : continue
			if (itinerary + '-P1' in self.mainFrame.dicoTracksGRFeatures) and (self.mainFrame.dicoTracksGRFeatures[itinerary + '-P1'][QGP.tableTracksFieldStatus] != QGP.trackStatusPublished) : continue
			self.routingPointSelectTrackCombo.addItem(itinerary)
		if self.optionComboModeGRRB.currentText() == C_ComboGRRBList_GRRB :
			for itinerary in self.listItineraryRB + self.listItineraryRF :
				self.routingPointSelectTrackCombo.addItem(itinerary)
		self.routingPointSelectTrackCombo.currentIndexChanged.connect(self.refreshRoutingPointsBoxMark)
		
	def refreshRoutingPointsBoxMark(self) :	
		self.routingPointSelectMarkCombo.currentIndexChanged.disconnect()
		markFeatureList = [ self.mainFrame.dicoPointsGRFeatures[id] for id in self.mainFrame.dicoPointsGRFeatures if TCOD.itineraryFromTrackCode(self.mainFrame.dicoPointsGRFeatures[id][QGP.tablePointsFieldGRCode]) == self.routingPointSelectTrackCombo.currentText() ]
		markFeatureList = sorted(markFeatureList, key = lambda x : int(x[QGP.tablePointsFieldRepere]) if x[QGP.tablePointsFieldRepere].isnumeric() else 9999)
		self.routingPointSelectMarkCombo.clear()
		self.routingPointSelectMarkCombo.addItem(' ')
		for feature in markFeatureList :	
			self.routingPointSelectMarkCombo.addItem(str(feature[QGP.tablePointsFieldGRCode]) + ' - ' + str(feature[QGP.tablePointsFieldRepere]) + ' - ' + str(feature[QGP.tablePointsFieldNom]))
		self.routingPointSelectMarkCombo.currentIndexChanged.connect(self.routingPointSelectMarkCombo_changed)

		
# ========================================================================================
# ========================================================================================
#
# Gestion du Cadre : Points de routage
# 
# ========================================================================================
# ========================================================================================

	def routingPointSelectMarkCombo_changed(self) :
		self.routingPointLbrt78X.setText(DSTY.textFormatBlackNormal.replace('%TEXT%','. . .'))
		DSTY.setStyleWarningLabel(self.routingPointLbrt78X, 'Normal')		
		self.routingPointLbrt78Y.setText(DSTY.textFormatBlackNormal.replace('%TEXT%','. . .'))
		DSTY.setStyleWarningLabel(self.routingPointLbrt78Y, 'Normal')	
		self.routingCanevasPoint = None		
		self.routingPointDefinitionSGRRadio.setChecked(True)

	def routingDefineOnCanevasButton_clicked(self) :
		self.definingCanevasPoint = True	
		self.mainFrame.setStatusWorking('Cliquez précisément sur la carte pour positionner le Point !')
		self.canvas.setMapTool(self.routingNewPointTool)	
		
	def newCanevasPointDefined(self, pointClicked):
		if not self.definingCanevasPoint: return
		self.routingCanevasPoint = pointClicked
		self.mainFrame.setStatusDone('Position du Point (Lambert 78) = ' + str(int(self.routingCanevasPoint.x())) + ' - ' + str(int(self.routingCanevasPoint.y())))
		self.routingPointLbrt78X.setText(DSTY.textFormatBlackNormal.replace('%TEXT%','X = ' + str(int(self.routingCanevasPoint.x()))))
		DSTY.setStyleOkLabel(self.routingPointLbrt78X, 'Normal')		
		self.routingPointLbrt78Y.setText(DSTY.textFormatBlackNormal.replace('%TEXT%','Y = ' + str(int(self.routingCanevasPoint.y()))))
		DSTY.setStyleOkLabel(self.routingPointLbrt78Y, 'Normal')		
		self.routingPointDefinitionFreeRadio.setChecked(True)
		
		action = self.iface.actionPan()
		action.trigger()		
		self.mainMenu.activateWindow()
		
		
	def routingValidatePointButton_clicked(self) :
		if not self.isPointBoxValid() : return

		self.definePointDico(self.routingPointCurrent)
		self.routingPointsCount = len(self.routingPointsDico)
		self.routingPointCurrent += 1
		
		self.routingTrackTableRefresh()
		self.refreshRoutingPointsBox()
		
			
	def routingDeletePointButton_clicked(self) :
				
		if self.routingPointCurrent not in self.routingPointsDico :
			self.mainFrame.setStatusWarning('Le point ' + str(self.routingPointCurrent) + ' n\' a pas été validé !')
			return
		
		for pointNum in range(self.routingPointCurrent, self.routingPointsCount - 1) : self.routingPointsDico[pointNum] = self.routingPointsDico[pointNum + 1]
		self.routingPointsDico.pop(self.routingPointsCount - 1)
		self.routingPointsCount = len(self.routingPointsDico)
		self.routingPointCurrent = 0
		
		self.routingTrackTableRefresh()	
		self.routingPointCurrent = 0
		self.refreshRoutingPointsBox()
			

	def routingInsertPointButton_clicked(self) :
		if not self.isPointBoxValid() : return
	
		for pointNum in range(self.routingPointsCount, self.routingPointCurrent, - 1) : self.routingPointsDico[pointNum + 1] = self.routingPointsDico[pointNum]
		self.definePointDico(self.routingPointCurrent)
		self.routingPointsCount = len(self.routingPointsDico)
		self.routingPointCurrent += 1
		
		self.routingTrackTableRefresh()
		self.refreshRoutingPointsBox()
	
	
	def isPointBoxValid(self) :
		if self.routingPointDefinitionFreeRadio.isChecked() :
			if self.routingCanevasPoint == None	:
				self.mainFrame.setStatusWarning('Définir un point sur le canevas au préalable !')
				return False
		if self.routingPointDefinitionSGRRadio.isChecked() :
			if self.routingPointSelectTrackCombo.currentText().strip() == '' or self.routingPointSelectMarkCombo.currentText().strip() == '' :
				self.mainFrame.setStatusWarning('Définir un point repère au préalable !')
				return False
		return True		
		
	
	def definePointDico(self, pointNum) :	

		self.routingPointsDico[pointNum] = {}
		self.routingPointsDico[pointNum][QGP.routingTableFieldPointNum] = pointNum
		self.routingPointsDico[pointNum]['Mode'] = 'Canevas' if self.routingPointDefinitionFreeRadio.isChecked() else 'Repère'
		self.routingPointsDico[pointNum][QGP.routingTableFieldPointX] = int(self.routingCanevasPoint.x()) if self.routingPointDefinitionFreeRadio.isChecked() else -1
		self.routingPointsDico[pointNum][QGP.routingTableFieldPointY] = int(self.routingCanevasPoint.y()) if self.routingPointDefinitionFreeRadio.isChecked() else -1
		self.routingPointsDico[pointNum][QGP.routingTableFieldPointItinerary] = self.routingPointSelectTrackCombo.currentText() if self.routingPointDefinitionSGRRadio.isChecked() else '- - -'
		self.routingPointsDico[pointNum][QGP.routingTableFieldPointMark] = self.routingPointSelectMarkCombo.currentText() if self.routingPointDefinitionSGRRadio.isChecked() else '- - -'
	
	
	
	
	
			
			
		
# ========================================================================================
# ========================================================================================
#
# Gestion du Cadre : Table du Parcours
# 
# ========================================================================================
# ========================================================================================	
		
	def createItem(self, value, format, italic = False):

		itemFont = QFont()
		itemFont.setPixelSize(DSTY.tableItemFontSize)
		itemFont.setItalic(italic)
		
		if value in (None, '') :
			itemText = ''
		elif format == 'List' :  
			itemText = str(len(value))
		elif format == 'Int' :
			itemText = '{:,d}'.format(int(value)).replace(',','.')
		elif format in ('Text', 'TextR') :
			itemText = value	
		else:
			itemText = '?#!%$'

		item = QtWidgets.QTableWidgetItem(itemText)
		item.setFont(itemFont)
		item.setFlags(item.flags() & ~Qt.ItemIsEditable)
		if format in ('Int', 'List', 'TextR') : item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)

		return item
		
		
	def routingTrackTableRefresh(self):
		self.groupBoxTrackRoutingTable.setSortingEnabled(False)									# This is needed ! Otherwise lines are sorted when filled and this results in garbage !
		self.groupBoxTrackRoutingTable.clearContents()
		self.groupBoxTrackRoutingTable.setRowCount(self.routingPointsCount)

		tableFields = QGP.routingTableQView
		for row in range(self.groupBoxTrackRoutingTable.rowCount()): 
			for col in range(len(tableFields)) :
				colName = tableFields[col][QGP.C_routingTableQView_ColName]
				value = self.routingPointsDico[row][colName] if colName in self.routingPointsDico[row] else ''
				item = self.createItem(value, tableFields[col][QGP.C_routingTableQView_ColType])
				self.groupBoxTrackRoutingTable.setItem(row, col, item)
	
		
		
		
# ========================================================================================
# ========================================================================================
#
# Gestion des Modifications des Options
# 
# ========================================================================================
# ========================================================================================

	def optionComboModeGRRB_changed(self) :
		self.refreshRoutingPointsBoxItinerary()
		self.refreshRoutingPointsBoxMark()


# ========================================================================================
# ========================================================================================
#
# Création des différents cadres Menu
# 
# ========================================================================================
# ========================================================================================

# ========================================================================================
# Cadre : Points de Routage
# ========================================================================================

	def menuBoxRoutingPoints(self):
	
		groupBoxRoutingPoints = QtWidgets.QGroupBox('Points de Routage', self.mainMenu)
		groupBoxRoutingPoints.setStyleSheet(DSTY.styleBox)
		
#	Nombre de Points et Sélection

		TBUT.createLabelBlackButton(groupBoxRoutingPoints, 1, 1, 'Point à éditer', 'Normal', 'Normal')
		self.routingCurrentPointCombo = TBUT.createComboButton(groupBoxRoutingPoints, 2, 1, 'Normal')

		TBUT.createLabelBlackButton(groupBoxRoutingPoints, 3, 1, 'Nombre de Points', 'Normal', 'Normal')
		self.routingPointsCountInfo = TBUT.createLabelGreenButton(groupBoxRoutingPoints, 4, 1, '. . .', 'Normal', 'Normal')
		DSTY.setStyleWarningLabel(self.routingPointsCountInfo, "Normal")
		

#	Mode de définition

		self.routingPointDefinitionSGRRadio  = TBUT.createRadioBoxButton(groupBoxRoutingPoints, 1, 2, 'Repères GR'  , 'Normal')
		self.routingPointDefinitionSGRRadio.setChecked(True)
		self.routingPointDefinitionFreeRadio  = TBUT.createRadioBoxButton(groupBoxRoutingPoints, 1, 3, 'Canevas'  , 'Normal')

#	Combos sélection Point

		self.routingPointSelectTrackCombo = TBUT.createComboButton(groupBoxRoutingPoints, 2, 2, 'Normal')
		self.routingPointSelectTrackCombo.currentIndexChanged.connect(self.refreshRoutingPointsBoxMark)
		self.routingPointSelectMarkCombo = TBUT.createComboButton(groupBoxRoutingPoints, 3, 2, 'Double')
		self.routingPointSelectMarkCombo.currentIndexChanged.connect(self.routingPointSelectMarkCombo_changed)
			
#	Définition sur Canevas 

		self.routingDefineOnCanevasButton = TBUT.createActionButton(groupBoxRoutingPoints, 2, 3, 'Définir', 'Normal')
		self.routingDefineOnCanevasButton.clicked.connect(self.routingDefineOnCanevasButton_clicked)	

		self.routingNewPointTool = QgsMapToolEmitPoint(self.canvas)
		self.routingNewPointTool.canvasClicked.connect(self.newCanevasPointDefined)

		self.routingPointLbrt78X = TBUT.createLabelGreenButton(groupBoxRoutingPoints, 3, 3, '. . .', 'Normal', 'Normal')
		self.routingPointLbrt78Y = TBUT.createLabelGreenButton(groupBoxRoutingPoints, 4, 3, '. . .', 'Normal', 'Normal')
			
#	Actions		

		TBUT.createLabelBlackButton(groupBoxRoutingPoints, 1, 5, 'Actions sur ce Point', 'Normal', 'Normal')

		self.routingValidatePointButton = TBUT.createActionButton(groupBoxRoutingPoints, 2, 5, 'Valider', 'Normal')
		self.routingValidatePointButton.clicked.connect(self.routingValidatePointButton_clicked)

		self.routingDeletePointButton = TBUT.createActionButton(groupBoxRoutingPoints, 3, 5, 'Supprimer', 'Normal')
		self.routingDeletePointButton.clicked.connect(self.routingDeletePointButton_clicked)
		
		self.routingInsertPointButton = TBUT.createActionButton(groupBoxRoutingPoints, 4, 5, 'Insérer', 'Normal')
		self.routingInsertPointButton.clicked.connect(self.routingInsertPointButton_clicked)
		
		
# 	Terminé

		groupBoxRoutingPoints.repaint()

		return groupBoxRoutingPoints


# ========================================================================================
# Cadre : Points Repères
# ========================================================================================

	def menuBoxRoutingWays(self):
	
		groupBoxRoutingWays = QtWidgets.QGroupBox('Routage', self.mainMenu)
		groupBoxRoutingWays.setStyleSheet(DSTY.styleBox)


# 	Terminé

		groupBoxRoutingWays.repaint()

		return groupBoxRoutingWays





# ========================================================================================
# Cadre : Options
# ========================================================================================

	def menuBoxOptions(self):

		groupBoxOptions = QtWidgets.QGroupBox('Options', self.mainMenu)
		groupBoxOptions.setStyleSheet(DSTY.styleBox)

#	Créer les cases options choisir

		self.optionComboModeGRRB = TBUT.createComboButton(groupBoxOptions, 1, 1, 'Normal')
		for text in C_ComboGRRBList : self.optionComboModeGRRB.addItem(text)
		self.optionComboModeGRRB.currentTextChanged.connect(self.optionComboModeGRRB_changed)

		self.optionComboRBFactor = TBUT.createComboButton(groupBoxOptions, 1, 2, 'Normal')
		for text in C_ComboRBFactor : self.optionComboRBFactor.addItem(text)



		groupBoxOptions.repaint()

		return groupBoxOptions


# ========================================================================================
# Cadre : Actions
# ========================================================================================

	def menuBoxActions(self):

		groupBoxActions = QtWidgets.QGroupBox('Actions', self.mainMenu)
		groupBoxActions.setStyleSheet(DSTY.styleBox)

#	Créer les boutons d'action		


		groupBoxActions.repaint()

		return groupBoxActions



# ========================================================================================
# Cadre : Cadre de la Table des Parcours
# ========================================================================================

	def menuBoxTableTracksFrame(self):
	
		groupBoxRoutingTrackFrame = QtWidgets.QGroupBox('Table du Parcours', self.mainMenu)
		groupBoxRoutingTrackFrame.setStyleSheet(DSTY.styleBox)

		groupBoxRoutingTrackFrame.repaint()

		return groupBoxRoutingTrackFrame


# ========================================================================================
# Cadre : Table des Parcours
# ========================================================================================

	def menuBoxTableTracksView(self):

		groupBoxRoutingTrackTable = QtWidgets.QTableWidget(0,len(QGP.routingTableQView), self.mainMenu)
		groupBoxRoutingTrackTable.setStyleSheet(DSTY.styleBox)

		DSTY.setStyleTableTraces(groupBoxRoutingTrackTable)

		tableFields = QGP.routingTableQView
		for col in range(len(tableFields)):
			groupBoxRoutingTrackTable.setHorizontalHeaderItem(col, QtWidgets.QTableWidgetItem(tableFields[col][0]))
			groupBoxRoutingTrackTable.setColumnWidth(col, tableFields[col][1])


		
		groupBoxRoutingTrackTable.repaint()

		return groupBoxRoutingTrackTable
	

# ========================================================================================
# --- THE END ---
# ========================================================================================
	