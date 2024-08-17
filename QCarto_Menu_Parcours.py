# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Gestion des Menus : Page Tracés
# ========================================================================================


# ========================================================================================
# Global Variables
#	self.mainFrame.dicoSectionsGRFeatures				dict			id : Section Feature		For all sections
# 	self.mainFrame.dicoSectionsGRFeaturesEndPoints	dict			id : [PointA, PointZ]
#	self.mainFrame.dicoTracksGRFeatures 	 			dict			code : Track Feature		For all tracks GR GRP GRT
#	self.mainFrame.dicoTracksRBFeatures  				dict			code : Track Feature		For all tracks RB RF RL IR
# 	self.dicoTracksViewFeatures				dict 			code : Track-Feature		For all tracks displayed in table
#	self.setPointsViewFeatures				set				Point-Feature				For all tracks displayed in table
#   self.dicoTrackSections 					dict			code : set(idSection)		For all tracks displayed in table
#	self.listTracksSelectedCodes			list			[code]						For all tracks selected in table
#	self.dicoTracksComputeResults			dict			code : dict results			For all tracks computed
#	self.dicoCommunes						dict			nom : Commune Feature
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


C_Repere_CuttingInfo_OK 		= 'OK'
C_Repere_CuttingInfo_Detached 	= 'Détaché'
C_Repere_CuttingInfo_NotCut		= 'Non coupé'


# ========================================================================================
# Class : menuTracksFrame
# >>> iface
# >>> mainMenu 				: Widget of Main Menu
# >>> mainFrame 			: Main Menu Object
# ========================================================================================

class menuTracksFrame:

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

#	Accès aux Tables de la DB POIs et SityTrail

		self.layerPOIs, 			self.layerPOIsError				= self.mainFrame.layerPOIs, 			self.mainFrame.layerPOIsError 		
		self.layerSityTrail, 		self.layerSityTrailError 		= self.mainFrame.layerSityTrail, 		self.mainFrame.layerSityTrailError 		

#	Création du Dictionnaire SityTrail

		self.dicoSityTrail = { feature[QGP.tableSityFieldCode] : feature for feature in self.layerSityTrail.getFeatures() } if self.layerSityTrail != None else {}

#	Variables principales

		self.typeSelected = None

		self.listTracksSelectedCodes = []													# Liste des codes sélectionnés dans la table
		self.listTracksViewCodes = []														# Liste ordonnée des codes affichés dans la table 
		self.setPointsViewFeatures = set()													# Ensemble des codes des repères affichés
		self.dicoTracksComputeResults = {}													# Dictionnaire des résultats de calcul
		self.dicoCommunes = None															# Dictionnaire des communes, déterminé si necessaire

		self.trackCodeOsm = None															# Code Parcours pour Génération Osm (Via Page Tools)
		self.trackRecordForced = False														# Forcer l'enregistrement des parcours même si non modifiés

		self.distancesItineraryPathCSV = None													
		self.distancesTrackPathCSV = None

#	Créer les sous-menus 

		self.boxesList = []
		self.createMenuBoxes()

		self.readFromDBTables()

		QgsExpressionContextUtils.setProjectVariable(QgsProject.instance(),QGP.tableTracksProjectVariableHighlight,'')
		QgsExpressionContextUtils.setProjectVariable(QgsProject.instance(),QGP.tableTracksProjectVariableHistory,'')

		if self.layerPOIs == None :
			self.mainFrame.setStatusWarning('Page des Parcours créée - Sans accès aux POIs !', 2000)
		elif self.layerSityTrail == None :
			self.mainFrame.setStatusWarning('Page des Parcours créée - Sans accès aux infos SityTrail !', 2000)
		else :
			self.mainFrame.setStatusDone('Page des Parcours créée !')

		
	def createMenuBoxes(self):

		self.groupBoxItinerary = self.menuBoxItinerary()
		DSTY.setBoxGeometry(self.groupBoxItinerary, 1, 4, 6, 2)
		self.boxesList.append(self.groupBoxItinerary)

		self.groupBoxLandmarks = self.menuBoxLandmarks()
		DSTY.setBoxGeometry(self.groupBoxLandmarks, 1, 7, 2, 2)
		self.boxesList.append(self.groupBoxLandmarks)

		self.groupBoxTracks = self.menuBoxTracks()
		DSTY.setBoxGeometry(self.groupBoxTracks, 3, 7, 1, 2)
		self.boxesList.append(self.groupBoxTracks)

		self.groupBoxSections = self.menuBoxSections()
		DSTY.setBoxGeometry(self.groupBoxSections, 4, 7, 1, 2)
		self.boxesList.append(self.groupBoxSections)

		self.groupBoxModifications = self.menuBoxModifications()
		DSTY.setBoxGeometry(self.groupBoxModifications, 5, 7, 2, 2)
		self.boxesList.append(self.groupBoxModifications)

		self.groupBoxOptions = self.menuBoxOptions()
		DSTY.setBoxGeometry(self.groupBoxOptions, 7, 4, 1, 5)
		self.boxesList.append(self.groupBoxOptions)
		
		self.groupBoxActions = self.menuBoxActions()
		DSTY.setBoxGeometry(self.groupBoxActions, 8, 4, 1, 5)
		self.boxesList.append(self.groupBoxActions)
		
		self.groupBoxTracksFrame = self.menuBoxTableTracksFrame()
		DSTY.setBoxGeometry(self.groupBoxTracksFrame, 1, 10, 8, 17)
		self.boxesList.append(self.groupBoxTracksFrame)

		self.groupBoxTracksTable = self.menuBoxTableTracksView()
		DSTY.setBoxGeometry(self.groupBoxTracksTable, 1, 10, 8, 17, True)
		self.boxesList.append(self.groupBoxTracksTable)

		self.groupBoxPointsTable = self.menuBoxTablePointsView()
		DSTY.setBoxGeometry(self.groupBoxPointsTable, 1, 10, 8, 17, True)
		self.boxesList.append(self.groupBoxPointsTable)
		self.groupBoxPointsTable.hide()

		self.groupBoxSectionsTable = self.menuBoxTableSectionsView()
		DSTY.setBoxGeometry(self.groupBoxSectionsTable, 1, 10, 8, 17, True)
		self.boxesList.append(self.groupBoxSectionsTable)
		self.groupBoxSectionsTable.hide()

		self.groupBoxPOIsTable = self.menuBoxTablePOIsView()
		DSTY.setBoxGeometry(self.groupBoxPOIsTable, 1, 10, 8, 17, True)
		self.boxesList.append(self.groupBoxPOIsTable)
		self.groupBoxPOIsTable.hide()

		self.groupBoxHistoricTable = self.menuBoxTableHistoricView()
		DSTY.setBoxGeometry(self.groupBoxHistoricTable, 1, 10, 8, 17, True)
		self.boxesList.append(self.groupBoxHistoricTable)
		self.groupBoxHistoricTable.hide()

		self.groupBoxCommonTracksTable = self.menuBoxTableCommonTracksView()
		DSTY.setBoxGeometry(self.groupBoxCommonTracksTable, 1, 10, 8, 17, True)
		self.boxesList.append(self.groupBoxCommonTracksTable)
		self.groupBoxCommonTracksTable.hide()

		self.groupBoxHtmlTracksTable = self.menuBoxTableHtmlTracksView()
		DSTY.setBoxGeometry(self.groupBoxHtmlTracksTable, 1, 10, 8, 17, True)
		self.boxesList.append(self.groupBoxHtmlTracksTable)
		self.groupBoxHtmlTracksTable.hide()


	def readFromDBTables(self):

		self.mainFrame.setStatusWorking('Lecture et analyse des Tables de la DB Carto ...')

#		Liste des Parcours

		self.listTracksGRCodes =  ['? Parcours-GR ?']
		self.listTracksGRPCodes = ['? Parcours-GR ?']
		self.listTracksGRTCodes = ['? Parcours-GR ?']
		self.listTracksRICodes =  ['? Parcours-RB ?']
		self.listTracksRLCodes =  ['? Parcours-RB ?']
		self.listTracksRBCodes =  ['? Parcours-RB ?']
		self.listTracksRFCodes =  ['? Parcours-RB ?']
		self.listTracksIRCodes =  ['? Parcours-RB ?']

		self.analyseTableTracksGR()
		self.analyseTableTracksRB()
		self.analyseTableSectionsGR()

# 		Dictionnaire des Tracés GR + RB - déterminé une fois pour toute à partir des dictionnaires main frame - Utilisé pour retrouver les noms de parcours
	
		self.dicoTracksGRRBFeatures = { TCOD.purifyTrackCode(trackCode) : self.mainFrame.dicoTracksRBFeatures[trackCode] for trackCode in self.mainFrame.dicoTracksRBFeatures }
		self.dicoTracksGRRBFeatures.update(self.mainFrame.dicoTracksGRFeatures)

		self.mainFrame.setStatusDone('Lecture et analyse des Tables de la DB Carto - OK')


# ========================================================================================
# Actions : A la demande de la fenêtre principale
# ========================================================================================

#	Show - Ouverture de cette fenêtre

	def show(self):
		for box in self.boxesList:
			box.show()
			box.repaint()
		self.groupBoxPointsTable.hide()		
		self.groupBoxSectionsTable.hide()	
		self.groupBoxPOIsTable.hide()	
		self.groupBoxHistoricTable.hide()
		self.groupBoxCommonTracksTable.hide()
		self.groupBoxHtmlTracksTable.hide()
		self.connectDBTables()	
		self.toggleGPXHtml('GPX')

#	Hide - Ouverture d'une autre fenêtre

	def hide(self):
		for box in self.boxesList:
			box.hide()
		self.disconnectDBTables()	

#	Close - Fermeture définitive

	def close(self):
		self.hide()
		for box in self.boxesList:
			del box

#	Help on this page

	def help(self):
		webbrowser.open_new_tab(QGP.configMenuHelpBasePath + 'QCarto - Page - Parcours.html')
	

#	DB Reloaded

	def mainReloadDone(self):
		self.readFromDBTables()
		DSTY.setStyleMainButtonsInactive(self.buttonRefreshTracks)
		DSTY.setStyleMainButtonsInactive(self.buttonRefreshSections)
	

# ========================================================================================
# Connections de la DB pour détection des modifications
# ========================================================================================

	def connectDBTables(self):
		if self.layerTracksGR != None:
			self.layerTracksGR.featureAdded.connect(self.showLayerTracksGRRBChanged)
			self.layerTracksGR.featureDeleted.connect(self.showLayerTracksGRRBChanged)
			self.layerTracksGR.geometryChanged.connect(self.showLayerTracksGRRBChanged)
			self.layerTracksGR.attributeValueChanged.connect(self.showLayerTracksGRRBChanged)

		if self.layerTracksRB != None:
			self.layerTracksRB.featureAdded.connect(self.showLayerTracksGRRBChanged)
			self.layerTracksRB.featureDeleted.connect(self.showLayerTracksGRRBChanged)
			self.layerTracksRB.geometryChanged.connect(self.showLayerTracksGRRBChanged)
			self.layerTracksRB.attributeValueChanged.connect(self.showLayerTracksGRRBChanged)

		if self.layerSectionsGR != None:
			self.layerSectionsGR.featureAdded.connect(self.showLayerSectionsGRChanged)
			self.layerSectionsGR.featureDeleted.connect(self.showLayerSectionsGRChanged)
			self.layerSectionsGR.geometryChanged.connect(self.showLayerSectionsGRChanged)
			self.layerSectionsGR.attributeValueChanged.connect(self.showLayerSectionsGRChanged)

		if self.layerPointsGR != None:
			self.layerPointsGR.featureAdded.connect(self.showLayerPointsGRChanged)
			self.layerPointsGR.featureDeleted.connect(self.showLayerPointsGRChanged)
			self.layerPointsGR.geometryChanged.connect(self.showLayerPointsGRChanged)
			self.layerPointsGR.attributeValueChanged.connect(self.showLayerPointsGRChanged)
			self.layerPointsGR.afterCommitChanges.connect(self.createPointsView)

	def disconnectDBTables(self):
		if self.layerTracksGR != None:
			try:
				self.layerTracksGR.featureAdded.disconnect(self.showLayerTracksGRRBChanged)
				self.layerTracksGR.featureDeleted.disconnect(self.showLayerTracksGRRBChanged)
				self.layerTracksGR.geometryChanged.disconnect(self.showLayerTracksGRRBChanged)
				self.layerTracksGR.attributeValueChanged.disconnect(self.showLayerTracksGRRBChanged)
			except:
				pass

		if self.layerTracksRB != None:
			try:
				self.layerTracksRB.featureAdded.disconnect(self.showLayerTracksGRRBChanged)
				self.layerTracksRB.featureDeleted.disconnect(self.showLayerTracksGRRBChanged)
				self.layerTracksRB.geometryChanged.disconnect(self.showLayerTracksGRRBChanged)
				self.layerTracksRB.attributeValueChanged.disconnect(self.showLayerTracksGRRBChanged)
			except:
				pass


		if self.layerSectionsGR != None:
			try:
				self.layerSectionsGR.featureAdded.disconnect(self.showLayerSectionsGRChanged)
				self.layerSectionsGR.featureDeleted.disconnect(self.showLayerSectionsGRChanged)
				self.layerSectionsGR.geometryChanged.disconnect(self.showLayerSectionsGRChanged)
				self.layerSectionsGR.attributeValueChanged.disconnect(self.showLayerSectionsGRChanged)
			except:
				pass

		if self.layerPointsGR != None:
			try:
				self.layerPointsGR.featureAdded.disconnect(self.showLayerPointsGRChanged)
				self.layerPointsGR.featureDeleted.disconnect(self.showLayerPointsGRChanged)
				self.layerPointsGR.geometryChanged.disconnect(self.showLayerPointsGRChanged)
				self.layerPointsGR.attributeValueChanged.disconnect(self.showLayerPointsGRChanged)
				self.layerPointsGR.afterCommitChanges.disconnect(self.createPointsView)
			except:
				pass

	def showLayerTracksGRRBChanged(self):	
		DSTY.setStyleNormalStrongButton(self.buttonRefreshTracks)
	
	def showLayerSectionsGRChanged(self):	
		DSTY.setStyleNormalStrongButton(self.buttonRefreshSections)
	
	def showLayerPointsGRChanged(self):	
		DSTY.setStyleNormalStrongButton(self.buttonRefreshPoints)
		
	
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

	
# ========================================================================================
# Actions : Afficher ! 		Définition de la liste affichée des parcours
#			Sélectionner	Sélectionner les Parcours dans la table "Parocurs-GR" ou "Parocurs-RB"
# ========================================================================================	
	
	def createTracksView(self, typeExternalRequest= None, dicoTracksViewFeaturesExternalRequest = None):

#		Be sure we are in Normal view (not Html)

		self.toggleGPXHtml('GPX')

#		Compute Dictionnary of Tracks features from selection request
		
		if dicoTracksViewFeaturesExternalRequest == None:

			itinerarySelected = self.itineraryCombo.currentText()
			if (itinerarySelected.strip() == ''):
				self.mainFrame.setStatusWarning('Pas d\'itinéraire sélectionné')
				return
			
			type = TCOD.itineraryTypeFromTrackCode(itinerarySelected)
			num = int(self.itineraryNumeroCombo.currentText().split()[1]) if self.itineraryNumeroCombo.currentText() != '' else -1
		
			if type in QGP.typeSetTableGR :
				self.dicoTracksViewFeatures = {code : self.mainFrame.dicoTracksGRFeatures[code] for code in self.mainFrame.dicoTracksGRFeatures if '-'.join(code.split('-')[0:2]) == itinerarySelected}
				selection = self.itinerarySelectCombo.currentText()
				if selection == 'Tome 1':
					self.dicoTracksViewFeatures = {code : self.dicoTracksViewFeatures[code] for code in self.dicoTracksViewFeatures if 1 in DTOP.getGRTomeList(code) }
				if selection == 'Tome 2':
					self.dicoTracksViewFeatures = {code : self.dicoTracksViewFeatures[code] for code in self.dicoTracksViewFeatures if 2 in DTOP.getGRTomeList(code) }
				if selection == 'Tome 3':
					self.dicoTracksViewFeatures = {code : self.dicoTracksViewFeatures[code] for code in self.dicoTracksViewFeatures if 3 in DTOP.getGRTomeList(code) }

			if type in QGP.typeSetModeRB:
				self.dicoTracksViewFeatures = {code : self.mainFrame.dicoTracksRBFeatures[code] for code in self.mainFrame.dicoTracksRBFeatures if '-'.join(code.split('-')[0:2]) == itinerarySelected}
				selection = self.itinerarySelectCombo.currentText()
				if selection == 'Tome 1':
					min, max = DTOP.getRangeByRBTome(itinerarySelected, 1)
				elif selection == 'Tome 2':
					min, max = DTOP.getRangeByRBTome(itinerarySelected, 2)
				elif selection == 'Tome 3':
					min, max = DTOP.getRangeByRBTome(itinerarySelected, 3)
				elif num != -1:
					min = max = num
				elif selection == 'Unité' and num != -1:
					min = max = num
				else:
					min = 0; max = 9999
				self.dicoTracksViewFeatures = {code : self.dicoTracksViewFeatures[code] for code in self.dicoTracksViewFeatures if int(code.split('-')[2][0:2]) >= min and int(code.split('-')[2][0:2]) <= max}
	
			if type in ('IR'):
				self.dicoTracksViewFeatures = {code : self.mainFrame.dicoTracksRBFeatures[code] for code in self.mainFrame.dicoTracksRBFeatures if '-'.join(code.split('-')[0:2]) == itinerarySelected}

		else:
			self.typeSelected = typeExternalRequest
			self.dicoTracksViewFeatures = dicoTracksViewFeaturesExternalRequest

#		Enrichir dicoTracksViewIndirectFeatures avec les parcours indirects

		self.dicoTracksIndirectCodes = {}
		for code in self.dicoTracksViewFeatures:
			self.dicoTracksIndirectCodes[code] = self.dicoTracksViewFeatures[code][QGP.tableTracksFieldIndirect] if self.dicoTracksViewFeatures[code][QGP.tableTracksFieldIndirect] != None else code

		self.dicoTracksViewIndirectFeatures = self.dicoTracksViewFeatures.copy()
		for code in self.dicoTracksIndirectCodes:
			if self.dicoTracksIndirectCodes[code] == code: continue
			type = TCOD.itineraryTypeFromTrackCode(code)
			if type in QGP.typeSetTableGR :
				self.dicoTracksViewIndirectFeatures[self.dicoTracksIndirectCodes[code]] = self.mainFrame.dicoTracksGRFeatures[self.dicoTracksIndirectCodes[code]]
			if type in QGP.typeSetTableRB :
				self.dicoTracksViewIndirectFeatures[self.dicoTracksIndirectCodes[code]] = self.mainFrame.dicoTracksRBFeatures[self.dicoTracksIndirectCodes[code]]

#		Compute Set of Points features corresponding to Tracks viewed

		self.initializeTracksTable()																							# Display Track Table
		self.dicoTracksComputeResults = {}																						# Effacer le dictionnaire des calculs
		QgsExpressionContextUtils.setProjectVariable(QgsProject.instance(),QGP.tableTracksProjectVariableHighlight,'')			# Supprimer le parcours surligné
		self.mainFrame.requestPage('Parcours')																					# In case we are in info mode

#		Compute Set of Points features corresponding to Tracks viewed

		self.createPointsView()
				
	def selectTracksViewed(self):
		if self.layerTracksGR == None:
			self.mainFrame.setStatusError(self.layerTracksGRerror, False)
			return
		if self.layerTracksRB == None:
			self.mainFrame.setStatusError(self.layerTracksRBerror, False)
			return
		if len(self.listTracksSelectedCodes) == 0:
			self.mainFrame.setStatusWarning('Vous devez sélectionner au moins un tracé dans la table !')
			return
		
		self.mainFrame.setStatusWorking('Sélection des Parcours dans la table "Parcours-GR" ou "Parcours-RB" ...')
		self.layerTracksGR.removeSelection()
		self.layerTracksRB.removeSelection()
		self.layerTracksGR.selectByIds( [ self.dicoTracksViewFeatures[code].id() for code in self.listTracksSelectedCodes if TCOD.itineraryTypeFromTrackCode(self.dicoTracksViewFeatures[code][QGP.tableTracksFieldCode]) in QGP.typeSetTableGR ] )
		self.layerTracksRB.selectByIds( [ self.dicoTracksViewFeatures[code].id() for code in self.listTracksSelectedCodes if TCOD.itineraryTypeFromTrackCode(self.dicoTracksViewFeatures[code][QGP.tableTracksFieldCode]) in QGP.typeSetTableRB ] )
		self.mainFrame.setStatusDone('Sélection des Parcours - OK')
	
	def zoomTracksSelected(self):
		if self.typeSelected in QGP.typeSetTableGR :
			if self.layerTracksGR == None:
				self.mainFrame.setStatusError(self.layerTracksGRerror, False)
				return
			self.iface.mapCanvas().zoomToSelected(self.layerTracksGR)		

		if self.typeSelected in QGP.typeSetTableRB :
			if self.layerTracksRB == None:
				self.mainFrame.setStatusError(self.layerTracksRBerror, False)
				return
			self.iface.mapCanvas().zoomToSelected(self.layerTracksRB)		

		self.mainFrame.setStatusDone('Zoom sur les Parcours sélectionnés - OK')


# ========================================================================================
# Actions : Gérer les demandes d'ajout / suppression des parcours modifiés
# ========================================================================================		
	
	def modificationControlAll(self):
		if len(self.listTracksSelectedCodes) != 1:
			self.mainFrame.setStatusWarning('Vous devez sélectionner un et un seul parcours dans la table !')
			return False
		codeSelected = self.listTracksSelectedCodes[0]
		if codeSelected not in self.dicoTracksComputeResults:
			self.mainFrame.setStatusWarning('Vous devez d\'abord calculer le parcours !')
			return False
		return True	
	
	def modificationControlAdd(self, letter):
		codeSelected = self.listTracksSelectedCodes[0]
		if letter not in self.dicoTracksComputeResults[codeSelected][QGP.tableTracksQFieldModif]: 
			self.mainFrame.setStatusWarning('Ce parcours n\'a aucun tronçon encodé -#' + letter + ' ou -M' + letter + ' !')
			return False
		trackValid, trackType, u3, u4, u5, u6, trackBaseCode, trackCode, trackModifTags, trackInvalidTags, u11, u12, u13 = TCOD.elementsFromGrCode(codeSelected)			
		if letter in trackModifTags:
			self.mainFrame.setStatusWarning('Ce parcours est déjà un parcours -M' + letter + ' !')
			return False
		trackNewCode = trackCode + '-M' + letter
		if trackNewCode in self.dicoTracksViewFeatures:
			self.mainFrame.setStatusWarning('Le parcours ' + codeSelected + '-M' + letter + ' existe déjà !')
			return False
		return True	
	
	def modificationControlRemove(self, letter):
		codeSelected = self.listTracksSelectedCodes[0]
		if letter in self.dicoTracksComputeResults[codeSelected][QGP.tableTracksQFieldModif]: 
			self.mainFrame.setStatusWarning('Ce parcours a encore au moins un tronçon encodé -#' + letter + ' ou -M' + letter + ' !')
			return False
		trackValid, trackType, u3, u4, u5, u6, trackBaseCode, trackCode, trackModifTags, trackInvalidTags, u11, u12, u13 = TCOD.elementsFromGrCode(codeSelected)			
		if letter not in trackModifTags:
			self.mainFrame.setStatusWarning('Ce parcours est n\'est pas un parcours -M' + letter + ' !')
			return False
		return True	

	def modificationAddTrackTemporary(self):
		if not self.modificationControlAll(): return
		if not self.modificationControlAdd('T'): return
		
		codeSelected = self.listTracksSelectedCodes[0]
		trackValid, trackType, u3, u4, u5, u6, trackBaseCode, trackCode, trackModifTags, trackInvalidTags, u11, u12, u13 = TCOD.elementsFromGrCode(codeSelected)			
		trackNewCode = trackCode + '-MT'
		layerTrack = self.layerTracksGR if trackType in QGP.typeSetTableGR else self.layerTracksRB

		self.mainFrame.setStatusWorking('Ajout du Parcours ' + trackNewCode + ' dans la table ' + layerTrack.name())
		done = LTRK.addTrackFeatureToTable(layerTrack, self.dicoTracksViewFeatures[codeSelected], trackNewCode, QGP.C_TrackTemporaryNameSuffix)
		if not done:
			self.mainFrame.setStatusError('Parcours ' + trackNewCode + ' : erreur lors de l\'ajout dans la table ' + layerTrack.name(), False)
			return

		self.mainFrame.setStatusWorking('Rechargement de la table ' + layerTrack.name())
		self.analyseTableTracksGR()	if trackType in QGP.typeSetTableGR else self.analyseTableTracksRB()
		self.createTracksView()
		self.mainFrame.setStatusDone('Parcours ' + trackNewCode + ' ajouté dans la table ' + layerTrack.name())

	def modificationAddTrackFuture(self):
		if not self.modificationControlAll(): return
		if not self.modificationControlAdd('F'): return

		codeSelected = self.listTracksSelectedCodes[0]
		trackValid, trackType, u3, u4, u5, u6, trackBaseCode, trackCode, trackModifTags, trackInvalidTags, u11, u12, u13 = TCOD.elementsFromGrCode(codeSelected)			
		trackNewCode = trackCode + '-MF'
		layerTrack = self.layerTracksGR if trackType in QGP.typeSetTableGR else self.layerTracksRB

		self.mainFrame.setStatusWorking('Ajout du Parcours ' + trackNewCode + ' dans la table ' + layerTrack.name())
		done = LTRK.addTrackFeatureToTable(layerTrack, self.dicoTracksViewFeatures[codeSelected], trackNewCode, QGP.C_TrackFutureNameSuffix)
		if not done:
			self.mainFrame.setStatusError('Parcours ' + trackNewCode + ' : erreur lors de l\'ajout dans la table ' + layerTrack.name(), False)
			return

		self.mainFrame.setStatusWorking('Rechargement de la table ' + layerTrack.name())
		self.analyseTableTracksGR()	if trackType in QGP.typeSetTableGR else self.analyseTableTracksRB()
		self.createTracksView()
		self.mainFrame.setStatusDone('Parcours ' + trackNewCode + ' ajouté dans la table ' + layerTrack.name())
			
	def modificationRemoveTrackTemporary(self):	
		if not self.modificationControlAll(): return
		if not self.modificationControlRemove('T'): return

		codeSelected = self.listTracksSelectedCodes[0]
		trackValid, trackType, u3, u4, u5, u6, trackBaseCode, trackCode, trackModifTags, trackInvalidTags, u11, u12, u13 = TCOD.elementsFromGrCode(codeSelected)			
		trackOldCode = trackCode + '-MT'
		layerTrack = self.layerTracksGR if trackType in QGP.typeSetTableGR else self.layerTracksRB

		self.mainFrame.setStatusWorking('Suppression du Parcours ' + trackOldCode + ' dans la table ' + layerTrack.name())
		done = LTRK.removeTrackFeatureToTable(layerTrack, self.dicoTracksViewFeatures[codeSelected])
		if not done:
			self.mainFrame.setStatusError('Parcours ' + trackOldCode + ' : erreur lors de la suppression dans la table ' + layerTrack.name(), False)
			return

		self.mainFrame.setStatusWorking('Rechargement de la table ' + layerTrack.name())
		self.analyseTableTracksGR()	if trackType in QGP.typeSetTableGR else self.analyseTableTracksRB()
		self.createTracksView()
		self.mainFrame.setStatusDone('Parcours ' + trackOldCode + ' supprimé dans la table ' + layerTrack.name())
	
	def modificationRemoveTrackFuture(self):	
		if not self.modificationControlAll(): return
		if not self.modificationControlRemove('F'): return

		codeSelected = self.listTracksSelectedCodes[0]
		trackValid, trackType, u3, u4, u5, u6, trackBaseCode, trackCode, trackModifTags, trackInvalidTags, u11, u12, u13 = TCOD.elementsFromGrCode(codeSelected)			
		trackOldCode = trackCode + '-MF'
		layerTrack = self.layerTracksGR if trackType in QGP.typeSetTableGR else self.layerTracksRB

		self.mainFrame.setStatusWorking('Suppression du Parcours ' + trackOldCode + ' dans la table ' + layerTrack.name())
		done = LTRK.removeTrackFeatureToTable(layerTrack, self.dicoTracksViewFeatures[codeSelected])
		if not done:
			self.mainFrame.setStatusError('Parcours ' + trackOldCode + ' : erreur lors de la suppression dans la table ' + layerTrack.name(), False)
			return

		self.mainFrame.setStatusWorking('Rechargement de la table ' + layerTrack.name())
		self.analyseTableTracksGR()	if trackType in QGP.typeSetTableGR else self.analyseTableTracksRB()
		self.createTracksView()
		self.mainFrame.setStatusDone('Parcours ' + trackOldCode + ' supprimé dans la table ' + layerTrack.name())
		
	
# ========================================================================================
# Actions : Recharger 		Retrouver et afficher le décompte des Tronçons GR
#			Sélectionner	Sélectionner les Points dans la table "Repères-GR"
# ========================================================================================	
	
	def reloadSections(self):
		self.mainFrame.setStatusWorking('Rechargement global des Tronçons GR ...')
		self.analyseTableSectionsGR()
		self.mainFrame.setStatusDone('Rechargement global des Tronçons GR - OK')


# ========================================================================================
# Actions : Recharger 		Retrouver et afficher le décompte des Points repères
#			Sélectionner	Sélectionner les Points dans la table "Repères-GR"
# ========================================================================================	
	
	def createPointsView(self):
		self.mainFrame.setStatusWorking('Recherche des Points repères pour les Parcours affichés ...')
		self.extractItineraryLandmarks()
		self.initializePointsInfo()		
		DSTY.setStyleMainButtonsInactive(self.buttonRefreshPoints)
		self.mainFrame.setStatusDone('Recherche des Points repères pour les Parcours affichés - OK')

	def selectPointsViewed(self):
		if self.layerPointsGR == None:
			self.mainFrame.setStatusError(self.layerPointsGRError, False)
			return

		self.mainFrame.setStatusWorking('Sélection des Points repères pour les Parcours affichés dans la table "Repères-GR" ...')
		self.layerPointsGR.removeSelection()
		self.layerPointsGR.selectByIds([ feature.id() for feature in self.setPointsViewFeatures ])
		self.mainFrame.setStatusDone('Sélection des Points repères pour les Parcours affichés - OK')
	
	def zoomPointsSelected(self):
		if self.layerPointsGR == None:
			self.mainFrame.setStatusError(self.layerPointsGRError, False)
			return

		self.iface.mapCanvas().zoomToSelected(self.layerPointsGR)		
		self.mainFrame.setStatusDone('Zoom sur les Points repères sélectionnés - OK')

	
# ========================================================================================
# ========================================================================================
#
# Opérations sur les Tables
#
# ========================================================================================
# ========================================================================================
	
# ========================================================================================
# Opérations sur la Table des Parcours
# ========================================================================================	

#	Définition d'un item de la table

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

#	Sélection de tous les Parcours - Right-click on Afficher !

	def selectAllTracks(self):
		self.toggleGPXHtml('GPX') 																												#		Be sure we are in Normal view (not Html)
		range = QtWidgets.QTableWidgetSelectionRange(0, 0, self.groupBoxTracksTable.rowCount()-1, 0)
		self.groupBoxTracksTable.setRangeSelected(range, True)

#	Liste des Codes sélectionnés - Selection changed

	def getSelectedTracksCodes(self):
		self.listTracksSelectedCodes = list({self.groupBoxTracksTable.item(item.row(),0).text() for item in self.groupBoxTracksTable.selectedItems()})
		self.trackCodeOsm = self.listTracksSelectedCodes[0] if len(self.listTracksSelectedCodes) == 1 else None									# For page Tools

#	Click on Table Item

	def trackTable_itemClicked(self, item):
		code = self.groupBoxTracksTable.item(item.row(),0).text()
		label = QGP.tracksTableQView[item.column()][0]
		self.showTrackTableElementInfo(code, item.column(), label)

#	Right-Click on Table Item

	def trackTable_itemRightClicked(self, point):
		if point == None: return
		item = self.groupBoxTracksTable.itemAt(point)
		if item == None: return
		code = self.groupBoxTracksTable.item(item.row(),0).text()
		label = QGP.tracksTableQView[item.column()][0]
		self.selectTrackTableElementInfo(code, item.column(), label)

#	Double-Click on Table Item

	def trackTable_itemDoubleClicked(self, item):
		code = self.groupBoxTracksTable.item(item.row(),0).text()
		label = QGP.tracksTableQView[item.column()][0]
		self.changeTrackTableElement(code, label, item)

#	Initialisation de la table des parcours pour les parcours à afficher

	def initializeTracksTable(self):
		
		self.listTracksViewCodes = [code for code in self.dicoTracksViewFeatures]
		self.listTracksViewCodes = sorted(self.listTracksViewCodes, key=TCOD.getTrackTableALLSortingValue)
		
		self.groupBoxTracksTable.setSortingEnabled(False)									# This is needed ! Otherwise lines are sorted when filled and this results in garbage !
		self.groupBoxTracksTable.clearContents()
		self.groupBoxTracksTable.setRowCount(len(self.listTracksViewCodes))

		tableFields = QGP.tracksTableQView
		for row in range(self.groupBoxTracksTable.rowCount()): 
			code = self.listTracksViewCodes[row]
			feature = self.dicoTracksViewFeatures[code]
			for col in range(len(tableFields)):
				value = feature[tableFields[col][0]] if tableFields[col][3] != 'Résultat' else ''
				if tableFields[col][2] == 'List' and value not in (None, ''): value = value.replace('[','').replace(']','').split(',')			# Replace Text (from Table) by real List
				item = self.createItem(value, tableFields[col][2], feature[QGP.tableTracksFieldIndirect] != None)
				self.groupBoxTracksTable.setItem(row, col, item)
			
#		self.groupBoxTracksTable.setSortingEnabled(True)									# Removed since it sorts automatically on code ...

	
#	Effacement des données avant calcul	

	def clearTracksTableBeforeCompute(self):
	
		self.groupBoxTracksTable.setSortingEnabled(False)									# This is needed ! Otherwise lines are sorted when filled and this results in garbage !

		tableFields = QGP.tracksTableQView
		for row in range(self.groupBoxTracksTable.rowCount()): 
			code = self.groupBoxTracksTable.item(row, 0).text()
			if code not in self.listTracksSelectedCodes: continue
			for col in range(len(tableFields)):
				if tableFields[col][3] in ('Calcul', 'Résultat') :
					self.groupBoxTracksTable.item(row, col).setText('')
			
#		self.groupBoxTracksTable.setSortingEnabled(True)
	
#	Affichage des résultats d'un calcul

	def showTracksTableComputeResults(self, codeComputed):

		def changeColor(row, col, code, field, value):
			if field in (QGP.tableTracksFieldDate, QGP.tableTracksIFieldCalcul):
				color = DCOL.bgTableOk if self.dicoTracksComputeResults[code][QGP.tableTracksIFieldErrorCode] == 0 else DCOL.bgTableError
			elif field == QGP.tableTracksIFieldGaps:
				color = DCOL.bgTableOk if value == [] else DCOL.bgTableWarning
			elif field == QGP.tableTracksQFieldModif:
				color = DCOL.bgTable if value == [] else DCOL.bgTableWarning
			elif field == QGP.tableTracksFieldVO:
				color = DCOL.bgTable if (self.typeSelected not in ('GRP', 'RB', 'RF', 'RI') or (self.typeSelected == 'GRP' and not TCOD.isCodePrincipalGR(code))) else (DCOL.bgTableOk if value == 0 else DCOL.bgTableError)
			elif field in (QGP.tableTracksIFieldPOIs, QGP.tableTracksIFieldPOIsAll) :
				color = DCOL.bgTable if self.layerPOIs != None else DCOL.bgTableError
			else:
				return
			self.groupBoxTracksTable.item(row, col).setBackground(color)

		self.groupBoxTracksTable.setSortingEnabled(False)									# This is needed ! Otherwise lines are sorted when filled and this results in garbage !
	
		tableFields = QGP.tracksTableQView

		for row in range(self.groupBoxTracksTable.rowCount()): 
			code = self.groupBoxTracksTable.item(row, 0).text()
			if code != codeComputed: continue
			for col in range(len(tableFields)):
				field = tableFields[col][0]
				if field in self.dicoTracksComputeResults[code]:
					value = self.dicoTracksComputeResults[code][field]
					item = self.createItem(value, tableFields[col][2])
					self.groupBoxTracksTable.setItem(row, col, item)
					changeColor(row, col, code, field, value)

#		self.groupBoxTracksTable.setSortingEnabled(True)
	
# ========================================================================================
#	Affichage des informations quand une case est cliquée
# ========================================================================================

	def showTrackTableElementInfo(self, code, column, label):

		infoField = QGP.tracksTableQView[column]		

		if infoField[QGP.C_tracksTableQView_ColClics] not in (1,3): 												# Pas d'action définie pour clic gauche
			self.mainFrame.setStatusOk('Prêt')
			return																									

		if label == QGP.tableTracksFieldDate:
			self.mainFrame.setStatusWorking('Parcours ' + code + ' : Préparation de l\'historique ...')
			QgsApplication.processEvents()
			self.initializeHistoricTable(code)
			self.groupBoxTracksTable.hide()
			self.groupBoxHistoricTable.show()
			self.mainFrame.setStatusInfo('Parcours ' + code + ' : Historique - Voir Table')
			self.mainFrame.requestPageInfo('Parcours')
			return

		if label == QGP.tableTracksFieldReperes:
			if code in self.dicoTracksComputeResults:				
				self.mainFrame.setStatusInfo('Parcours ' + code + ' : Repères - Voir Table')
				self.initializePointsTable(code)
				self.groupBoxTracksTable.hide()
				self.groupBoxPointsTable.show()
				self.mainFrame.requestPageInfo('Parcours')
			else :
				if self.typeSelected in QGP.typeSetTableGR : trackFeature = self.mainFrame.dicoTracksGRFeatures[code]
				if self.typeSelected in QGP.typeSetTableRB : trackFeature = self.mainFrame.dicoTracksRBFeatures[code]			
				self.mainFrame.setStatusInfo('Parcours ' + code + ' - Repères enregistrés : ' + str(trackFeature[QGP.tableTracksFieldReperes]))
			return

#		Pour tous les suivants, le parcours doit avoir été calculé !

		if code not in self.dicoTracksComputeResults:																# Parcours non encore calculé
			self.mainFrame.setStatusWarning('Parcours ' + code + ' : ce parcours n\'a pas été calculé !')		
			return

		if label == QGP.tableTracksFieldDistance:
			self.mainFrame.setStatusInfo('Parcours ' + code + ' : Parcours Communs - Voir Table')
			self.initializeCommonTracksTable(code)
			self.groupBoxTracksTable.hide()
			self.groupBoxCommonTracksTable.show()
			self.mainFrame.requestPageInfo('Parcours')
			return		

		if label == QGP.tableTracksIFieldCalcul:
			errorCode = self.dicoTracksComputeResults[code][QGP.tableTracksIFieldErrorCode]
			if errorCode == 0:
				self.mainFrame.setStatusInfo('Parcours ' + code + ' : ce parcours a été calculé correctement !')
			elif errorCode == 1:
				self.mainFrame.setStatusWarning('Parcours ' + code + ' : aucun tronçon n\'a été trouvé pour ce parcours ?')
			elif errorCode == 2:
				self.mainFrame.setStatusWarning('Parcours ' + code + ' : aucun tronçon initial (suffixe -1x) n\'a été trouvé pour ce parcours ?')
			elif errorCode in (3, 13):
				self.mainFrame.setStatusWarning('Parcours ' + code + ' : plusieurs tronçons initiaux (suffixe -1x) : ' + str(self.dicoTracksComputeResults[code][QGP.tableTracksIFieldSectionsLost]))
			elif errorCode in (4, 14):
				self.mainFrame.setStatusWarning('Parcours ' + code + ' : plusieurs tronçons non accrochés : ' + str(self.dicoTracksComputeResults[code][QGP.tableTracksIFieldSectionsLost]))
			elif errorCode in (5, 15):
				self.mainFrame.setStatusWarning('Parcours ' + code + ' : bifurcation indéterminée : ' + str(self.dicoTracksComputeResults[code][QGP.tableTracksFieldTroncons][-1]) + ' > ' + str(self.dicoTracksComputeResults[code][QGP.tableTracksIFieldSectionsLost]))
			else:
				self.mainFrame.setStatusError('Parcours ' + code + ' : Code erreur inconnu ?')

		if label == QGP.tableTracksIFieldGaps:
			gapList = self.dicoTracksComputeResults[code][QGP.tableTracksIFieldGaps]
			if len(gapList) == 0:
				self.mainFrame.setStatusInfo('Parcours ' + code + ' : tous les tronçons sont parfaitement attachés !')
			else:
				self.mainFrame.setStatusWarning('Parcours ' + code + ' : ' + str(len(gapList)) + ' trou.s : ' + ' // '.join([str(gap[0]) + '-' + str(gap[1]) + '=' + str(round(gap[3],1)) + ' m' for gap in gapList]))

		if label == QGP.tableTracksFieldTroncons:
			self.mainFrame.setStatusInfo('Parcours ' + code + ' : Détail des tronçons - Voir Table')
			self.initializeSectionsTable(code)
			self.groupBoxTracksTable.hide()
			self.groupBoxSectionsTable.show()
			self.mainFrame.requestPageInfo('Parcours')
			return				
		
		if label in (QGP.tableTracksIFieldPOIs, QGP.tableTracksIFieldPOIsAll) :
			self.mainFrame.setStatusInfo('Parcours ' + code + ' : Détail des POIs associés - Voir Table')
			self.initializePOIsTable(code, label)
			self.groupBoxTracksTable.hide()
			self.groupBoxPOIsTable.show()
			self.mainFrame.requestPageInfo('Parcours')
			return				

		if label == QGP.tableTracksQFieldDelta:
			if self.dicoTracksComputeResults[code][QGP.tableTracksQFieldDelta] != None:
				if self.typeSelected in QGP.typeSetTableGR : trackFeature = self.mainFrame.dicoTracksGRFeatures[code]
				if self.typeSelected in QGP.typeSetTableRB : trackFeature = self.mainFrame.dicoTracksRBFeatures[code]
				self.mainFrame.setStatusInfo('Parcours ' + code + ' : Différence Hausdorff = ' + '{:,d}'.format(self.dicoTracksComputeResults[code][QGP.tableTracksQFieldDelta]).replace(',','.') + \
														' mètres (Comparé à : ' + str(trackFeature[QGP.tableAllFieldNomCarto]) + ' - ' + str(trackFeature[QGP.tableAllFieldDateModif]) + ')')
			else:
				self.mainFrame.setStatusInfo('Parcours ' + code + ' : Pas de distance Hausdorff calculée')

		if label == QGP.tableTracksQFieldModif:
			if self.dicoTracksComputeResults[code][QGP.tableTracksQFieldModif] != []:
				self.mainFrame.setStatusInfo('Parcours ' + code + ' : Liste des modifications détectées : ' + ' , '.join(self.dicoTracksComputeResults[code][QGP.tableTracksQFieldModif]))
			else:
				self.mainFrame.setStatusInfo('Parcours ' + code + ' : Pas de modifications détectées')


#	Sélection des informations quand une case est cliquée-droit
	
	def selectTrackTableElementInfo(self, code, column, label):

		infoField = QGP.tracksTableQView[column]		

		if infoField[QGP.C_tracksTableQView_ColClics] not in (2,3): 																	# Pas d'action définie pour clic droit
			self.mainFrame.setStatusOk('Prêt')
			return																									

		if label == QGP.tableTracksFieldCode:
			QgsExpressionContextUtils.setProjectVariable(QgsProject.instance(),QGP.tableTracksProjectVariableHighlight,code)			# Définir le parcours surligné
			self.iface.mapCanvas().refreshAllLayers()
			QgsApplication.processEvents()
			self.mainFrame.setStatusInfo('Parcours ' + code + ' : le parcours tel qu\'enregistré est surligné ... ')
			return

		if label == QGP.tableTracksFieldDate:
			QgsExpressionContextUtils.setProjectVariable(QgsProject.instance(),QGP.tableTracksProjectVariableHistory,code)				# Définir le parcours historique surligné
			self.iface.mapCanvas().refreshAllLayers()
			QgsApplication.processEvents()
			self.mainFrame.setStatusInfo('Parcours ' + code + ' : les parcours enregistrés dans l\'historique sont affichés ... ')
			return

		if code not in self.dicoTracksComputeResults:																					# Parcours non encore calculé
			self.mainFrame.setStatusWarning('Parcours ' + code + ' : ce parcours n\'a pas été calculé !')		
			return

		if label == QGP.tableTracksFieldStatus:
			dicoCommonTracksSectionsList = self.generateCommonTracksDico(code)		
			selectTrackListGR = [trackCode for trackCode in dicoCommonTracksSectionsList if TCOD.itineraryTypeFromTrackCode(trackCode) in QGP.typeSetTableGR]
			selectTrackListRB = [trackCode for trackCode in dicoCommonTracksSectionsList if TCOD.itineraryTypeFromTrackCode(trackCode) in QGP.typeSetTableRB]
			self.layerTracksGR.removeSelection()
			self.layerTracksGR.selectByExpression('"' + QGP.tableTracksFieldCode + '"' + ' IN ' + str(selectTrackListGR).replace('[','(').replace(']',')'))
			self.layerTracksRB.removeSelection()
			self.layerTracksRB.selectByExpression('"' + QGP.tableTracksFieldCode + '"' + ' IN ' + str(selectTrackListRB).replace('[','(').replace(']',')'))
			self.mainFrame.setStatusInfo('Parcours ' + code + ' : sélection des tous les parcours communs ...')

		if label == QGP.tableTracksIFieldCalcul:
			errorCode = self.dicoTracksComputeResults[code][QGP.tableTracksIFieldErrorCode]
			if errorCode == 0:
				selectList = [abs(sectionId) for sectionId in self.dicoTracksComputeResults[code][QGP.tableTracksFieldTroncons]]
				self.mainFrame.setStatusInfo('Parcours ' + code + ' : sélection de tous les tronçons du parcours ... ')
			elif errorCode == 1:
				selectList = []
				self.mainFrame.setStatusWarning('Parcours ' + code + ' : aucun tronçon ne peut être sélectionné pour ce parcours ?')
			elif errorCode == 2:
				selectList = [abs(sectionId) for sectionId in self.dicoTracksComputeResults[code][QGP.tableTracksIFieldSectionsLost]]
				self.mainFrame.setStatusInfo('Parcours ' + code + ' : sélection de tous les tronçons du parcours ... ')
			elif errorCode in (3, 13):
				selectList = [abs(sectionId) for sectionId in self.dicoTracksComputeResults[code][QGP.tableTracksIFieldSectionsLost]]
				self.mainFrame.setStatusInfo('Parcours ' + code + ' : sélection de tous les tronçons avec suffixe -1x ...')
			elif errorCode in (4, 14):
				selectList = [abs(sectionId) for sectionId in self.dicoTracksComputeResults[code][QGP.tableTracksIFieldSectionsLost]]
				self.mainFrame.setStatusInfo('Parcours ' + code + ' : sélection des tronçons non accrochés ... ')
			elif errorCode in (5, 15):
				selectList = [abs(self.dicoTracksComputeResults[code][QGP.tableTracksFieldTroncons][-1])]
				self.mainFrame.setStatusInfo('Parcours ' + code + ' : sélection du tronçon avant la bifurcation indéterminée ... ')
			else:
				selectList = []
				self.mainFrame.setStatusError('Parcours ' + code + ' : Code erreur inconnu ?')
			self.layerSectionsGR.removeSelection()
			self.layerSectionsGR.selectByIds(selectList)
			self.iface.mapCanvas().zoomToSelected(self.layerSectionsGR)		

		if label == QGP.tableTracksIFieldGaps:
			gapList = self.dicoTracksComputeResults[code][QGP.tableTracksIFieldGaps]
			if len(gapList) == 0:
				self.mainFrame.setStatusInfo('Parcours ' + code + ' : sélection nulle - tous les tronçons sont parfaitement attachés !')
				return
			else:
				self.mainFrame.setStatusInfo('Parcours ' + code + ' : sélection des tronçons au premier trou ... ')
				self.layerSectionsGR.selectByIds([abs(gapList[0][0]), abs(gapList[0][1])])
				self.iface.mapCanvas().setCenter(gapList[0][2])
				self.iface.mapCanvas().zoomScale(max(1,int(16 * gapList[0][3])))

		if label == QGP.tableTracksFieldTroncons:
			self.mainFrame.setStatusInfo('Parcours ' + code + ' : sélection des tronçons du parcours dans la table Tronçons-GR ...')		
			self.layerSectionsGR.selectByIds([abs(id) for id in self.dicoTracksComputeResults[code][QGP.tableTracksFieldTroncons]])
			self.iface.mapCanvas().zoomToSelected(self.layerSectionsGR)		

		if label == QGP.tableTracksFieldReperes:
			self.mainFrame.setStatusInfo('Parcours ' + code + ' : sélection des repères associés au parcours dans la table Repères-GR ...')		
			self.layerPointsGR.selectByIds([info[0].id() for info in self.dicoTracksComputeResults[code][QGP.tableTracksIFieldReperesPos]])
			self.iface.mapCanvas().zoomToSelected(self.layerPointsGR)		

		if label == QGP.tableTracksQFieldModif:
			self.mainFrame.setStatusInfo('Parcours ' + code + ' : sélection des tronçons modifiés = ' + str(self.dicoTracksComputeResults[code][QGP.tableTracksIFieldSectionsModif]))
			self.layerSectionsGR.selectByIds(self.dicoTracksComputeResults[code][QGP.tableTracksIFieldSectionsModif]) 
			self.iface.mapCanvas().zoomToSelected(self.layerSectionsGR)		


# ========================================================================================
#	Modification directe de la table de la DB quand une case est double-cliquée
# ========================================================================================

	def changeTrackTableElement(self, code, label, item):
	
		infoField = QGP.tracksTableQView[item.column()]		

		if infoField[QGP.C_tracksTableQView_ColEdit] != 1: 																# Pas d'action définie pour double clic 
			self.mainFrame.setStatusOk('Prêt')
			self.activeItemForChange = None
			return	
		self.activeItemForChange = item		
		self.activeCodeForChange = code

		if label == QGP.tableTracksFieldCode:
			self.trackCodeInputWindow = TINP.inputFromText(self.iface, self, 'Parcours : Définir le Code', ['Code'], [code], self.changeTrackCode)		

		if label == QGP.tableTracksFieldStatus:
			self.trackStateInputWindow = TINP.inputFromCombo(self.iface, self, 'Parcours : Définir Etat', 'Etat', QGP.trackStatusForInput, self.changeTrackState)		

		if label == QGP.tableTracksFieldName:
			self.trackNameInputWindow = TINP.inputFromText(self.iface, self, 'Parcours : Modifier le Nom', ['Nom du Parcours'], [self.activeItemForChange.text()], self.changeTrackName)		

		if label == QGP.tableTracksFieldMarked:
			self.trackMarkedInputWindow = TINP.inputFromCombo(self.iface, self, 'Parcours : Définir Balisage', 'Balisage', QGP.trackMarkedForInput, self.changeTrackMarked)		

	def changeTrackCode(self, status, newName):
		if self.activeItemForChange == None	:
			self.mainFrame.setStatusError('changeTrackCode - erreur interne @#{?!$')
			del self.trackCodeInputWindow
			return
			
		if status:
			self.changeTrackAttribute('Code du Parcours', QGP.tableTracksFieldCode, newName[0])
		else:
			self.mainFrame.setStatusInfo(self.activeCodeForChange + ' : annulation de la demande')
		
		self.activeItemForChange = None		
		self.activeCodeForChange = None
		del self.trackCodeInputWindow

	def changeTrackState(self, status, newState):
		if self.activeItemForChange == None	:
			self.mainFrame.setStatusError('changeTrackState - erreur interne @#{?!$')
			del self.trackStateInputWindow
			return
			
		if status:
			self.changeTrackAttribute('Etat du Parcours', QGP.tableTracksFieldStatus, newState)
		else:
			self.mainFrame.setStatusInfo(self.activeCodeForChange + ' : annulation de la demande')
		
		self.activeItemForChange = None		
		self.activeCodeForChange = None
		del self.trackStateInputWindow

	def changeTrackName(self, status, newName):
		if self.activeItemForChange == None	:
			self.mainFrame.setStatusError('changeTrackName - erreur interne @#{?!$')
			del self.trackNameInputWindow
			return
			
		if status:
			self.changeTrackAttribute('Nom du Parcours', QGP.tableTracksFieldName, newName[0])
		else:
			self.mainFrame.setStatusInfo(self.activeCodeForChange + ' : annulation de la demande')
		
		self.activeItemForChange = None		
		self.activeCodeForChange = None
		del self.trackNameInputWindow

	def changeTrackMarked(self, status, newValue):
		if self.activeItemForChange == None	:
			self.mainFrame.setStatusError('changeTrackMarked - erreur interne @#{?!$')
			del self.trackMarkedInputWindow
			return
			
		if status:
			self.changeTrackAttribute('Balisage', QGP.tableTracksFieldMarked, newValue)
		else:
			self.mainFrame.setStatusInfo(self.activeCodeForChange + ' : annulation de la demande')
		
		self.activeItemForChange = None		
		self.activeCodeForChange = None
		del self.trackMarkedInputWindow

	def changeTrackAttribute(self, attributeName, attributeField, newValue) : 
		self.mainFrame.setStatusWorking(self.activeCodeForChange + ' : mise à jour attribut ' + attributeName + ' : ' + self.activeItemForChange.text() + ' >>> ' + newValue)
		if self.typeSelected in QGP.typeSetTableGR : self.mainFrame.dicoTracksGRFeatures[self.activeCodeForChange][attributeField] = newValue					# Change in Dico GR Tracks
		if self.typeSelected in QGP.typeSetTableRB : self.mainFrame.dicoTracksRBFeatures[self.activeCodeForChange][attributeField] = newValue					# Change in Dico RB Tracks
		self.activeItemForChange.setText(newValue)																									# Change QCarto Table
		try:
			trackFeature = (self.mainFrame.dicoTracksGRFeatures if self.typeSelected in QGP.typeSetTableGR else self.mainFrame.dicoTracksRBFeatures) [self.activeCodeForChange]
			layerTrack = self.layerTracksGR if self.typeSelected in QGP.typeSetTableGR else self.layerTracksRB
			layerTrackAlreadyEditable = layerTrack.isEditable()
			layerTrack.startEditing()
			layerTrack.changeAttributeValue(trackFeature.id(), trackFeature.fieldNameIndex(attributeField), newValue)
			if not layerTrackAlreadyEditable : layerTrack.commitChanges()
			self.mainFrame.setStatusDone(self.activeCodeForChange + ' : attribut ' +  attributeName + ' mis à jour = ' + newValue)
		except:
			self.mainFrame.setStatusError(self.activeCodeForChange + ' : erreur imprévue lors de la mise à jour attribut ' +  attributeName)


# ========================================================================================
# Opérations sur la Table des Points Repères
# ========================================================================================	
	
	def initializePointsTable(self, code):

#	Copy points attached list and possibly add one if missing at start / end

		trackLineXYZ = self.dicoTracksComputeResults[code][QGP.tableTracksIFieldTrackXYZ]
		pointsAttachedList = self.dicoTracksComputeResults[code][QGP.tableTracksIFieldReperesPos].copy()
		if pointsAttachedList == [] or pointsAttachedList[0][1] != 0: pointsAttachedList = [[None, 0]] + pointsAttachedList
		if pointsAttachedList[-1][1] != len(trackLineXYZ) - 1 : pointsAttachedList = pointsAttachedList + [[None, len(trackLineXYZ) - 1]]

#	Init table rows

		self.groupBoxPointsTable.setSortingEnabled(False)		
		self.groupBoxPointsTable.clearContents()
		self.groupBoxPointsTable.setRowCount(len(pointsAttachedList))

		self.repereCuttingOkList = []; self.repereCuttingDetachedList = []; self.repereCuttingNotCutList = []

		tableFields = QGP.pointsTableQView
		previousDistance = 0
		
		for row in range(self.groupBoxPointsTable.rowCount()): 
		
#		Extract repere info		
			
			if pointsAttachedList[row][0] == None:																	# Case of start / end point initially missing 
				distance = 0 if row == 0 else QgsGeometry.fromPolyline(trackLineXYZ).length()
				reperePoint = None
				repereAltitude = TALT.getPointXYAltitude(QgsPointXY(trackLineXYZ[0])) if row == 0 else TALT.getPointXYAltitude(QgsPointXY(trackLineXYZ[-1]))
				repereUTM = '─────'
				repereId = -1
				repereTrackDistance = 0
				repereTrackCut = True
			else :																									# Normal case 
				distance = QgsGeometry.fromPolyline(trackLineXYZ[0:pointsAttachedList[row][1]+1]).length()
				reperePoint = pointsAttachedList[row][0].geometry().asPoint()
				repereAltitude = TALT.getPointXYAltitude(reperePoint)
				repereUTM = TSCR.convertPoint3812toUtmText(reperePoint)
				repereId = pointsAttachedList[row][0].id()
				repereTrackDistance = reperePoint.distance(QgsPointXY(trackLineXYZ[pointsAttachedList[row][1]]))
				repereTrackCut = (repereTrackDistance == 0) and \
								(any(reperePoint in self.mainFrame.dicoSectionsGRFeaturesEndPoints[abs(idSection)] for idSection in self.dicoTracksComputeResults[code][QGP.tableTracksFieldTroncons]))

#		Define List of Repères Cut / Detached / Not Cut

			if repereTrackCut:
				repereInfo = C_Repere_CuttingInfo_OK; self.repereCuttingOkList.append(repereId)
			elif repereTrackDistance > 0:
				repereInfo = C_Repere_CuttingInfo_Detached; self.repereCuttingDetachedList.append(repereId)
			else:
				repereInfo = C_Repere_CuttingInfo_NotCut; self.repereCuttingNotCutList.append(repereId)

#		Define infos for table

			if row == 0:	
				previousDistance = 0
				repereDe = pointsAttachedList[row][0][QGP.tablePointsFieldRepere] if pointsAttachedList[row][0] != None else '──'
				values = [repereId, repereInfo, distance, 0, '', repereDe, pointsAttachedList[row][0][QGP.tablePointsFieldNom] if pointsAttachedList[row][0] != None else '─── Début du Parcours ───', repereAltitude, repereUTM]
				repereSequenceOK = (repereDe == '1') or (repereDe == 'D') or (repereDe == 'D/A')
			else:
				delta = distance - previousDistance
				repereA = pointsAttachedList[row][0][QGP.tablePointsFieldRepere] if pointsAttachedList[row][0] != None else '──'
				index =  repereDe + ' >>> ' + repereA
				if code in self.dicoRBPlanDistances :
					if index in self.dicoRBPlanDistances[code]:
						schema = '{:.1f}'.format(self.dicoRBPlanDistances[code][index]).replace('.',',')
					else:
						schema = '- - -'
				else:
					schema = 'N/A'
				values = [repereId, repereInfo, distance, delta, schema, repereA, pointsAttachedList[row][0][QGP.tablePointsFieldNom] if pointsAttachedList[row][0] != None else '─── Fin du Parcours ───', repereAltitude, repereUTM]

#		Prepare for Next Row	

				previousDistance = distance	
				repereDePrevious = repereDe
				repereDe = repereA
				repereSequenceOK = (int('0' + ''.join([c for c in repereDe if c.isdigit()])) == 1 + int('0' + ''.join([c for c in repereDePrevious if c.isdigit()])))
				if row == self.groupBoxPointsTable.rowCount()-1 :
					if (repereDe == '1') or (repereDe == 'A') or (repereDe == 'D/A') : repereSequenceOK = True
			
			for col in range(len(tableFields)):
				value = values[col]	
				item = self.createItem(value, tableFields[col][2])
				if col == 1 and repereInfo != 'OK': item.setBackground(DCOL.bgTableWarning)
				if col == 5 and not repereSequenceOK: item.setBackground(DCOL.bgTableWarning)
				if col == 5 and repereId == -1 : item.setBackground(DCOL.bgTableError)
				self.groupBoxPointsTable.setItem(row, col, item)

#	Click on Table Item

	def trackPointTable_itemClicked(self, item):
		if item.column() == 1:
			if item.text() == C_Repere_CuttingInfo_OK : 		idList = self.repereCuttingOkList
			if item.text() == C_Repere_CuttingInfo_Detached : 	idList = self.repereCuttingDetachedList
			if item.text() == C_Repere_CuttingInfo_NotCut : 	idList = self.repereCuttingNotCutList
		else:
			idList = [int(self.groupBoxPointsTable.item(item.row(),0).text().replace('.',''))]
		self.layerPointsGR.selectByIds(idList)
		self.mainFrame.setStatusInfo('Repères ' + str(idList) + ' : sélectionnés dans la table Repères-GR ...')		

	def trackPointTable_itemRightClicked(self, point):
		if point == None: return															# If clic out of table
		item = self.groupBoxPointsTable.itemAt(point)
		if item == None : return															# If clic out of items
		id = int(self.groupBoxPointsTable.item(item.row(),0).text().replace('.',''))
		if id == -1 : return																# If fake repere added 
		self.layerPointsGR.selectByIds([id])
		self.iface.mapCanvas().zoomToSelected(self.layerPointsGR)		
		self.iface.mapCanvas().zoomScale(1000)
		self.mainFrame.setStatusInfo('Repère ' + str(id) + ' : zoom du canevas sur ce repère ...')
	
#	Double click pour édition

	def trackPointTable_itemDoubleClicked(self, item):
		id = int(self.groupBoxPointsTable.item(item.row(),0).text().replace('.',''))
		if id == -1 : return																# If fake repere added 
		label = QGP.pointsTableQView[item.column()][0]
		self.changePointTableElement(id, label, item)
		
	def changePointTableElement(self, id, label, item):
		infoField = QGP.pointsTableQView[item.column()]		
		if item.column() not in (QGP.C_pointsTableQView_ColRepère, QGP.C_pointsTableQView_ColName) : 
			self.mainFrame.setStatusOk('Prêt')
			return		
		self.activeItemForChange = item		
		self.activeIdForChange = id
		self.pointInputWindow = TINP.inputFromText(self.iface, self, 'Repère : ' + str(id) + ' Modifier le repère', [QGP.tablePointsFieldRepere, QGP.tablePointsFieldNom], \
										[ str(self.mainFrame.dicoPointsGRFeatures[id][_]) for _ in (QGP.tablePointsFieldRepere, QGP.tablePointsFieldNom) ], 	\
										self.editPointAttributesResult)	
	
	def editPointAttributesResult(self, status, newAttributesList):
		if self.activeItemForChange == None	:
			self.mainFrame.setStatusError('editPointAttributesResult - erreur interne @#{?!$')
			del self.pointInputWindow
			return
			
		if status:
			self.mainFrame.setStatusWorking('Repère ' + str(self.activeIdForChange) + ' : mise à jour des attributs : ' + str(newAttributesList))
			self.groupBoxPointsTable.item(self.activeItemForChange.row(),QGP.C_pointsTableQView_ColRepère).setText(newAttributesList[0])		
			self.groupBoxPointsTable.item(self.activeItemForChange.row(),QGP.C_pointsTableQView_ColName).setText(newAttributesList[1])		
			try:
				pointFeature = self.mainFrame.dicoPointsGRFeatures[self.activeIdForChange]
				layerPointAlreadyEditable = self.layerPointsGR.isEditable()
				self.layerPointsGR.startEditing()
				self.layerPointsGR.changeAttributeValue(pointFeature.id(), pointFeature.fieldNameIndex(QGP.tablePointsFieldRepere), newAttributesList[0])	
				self.layerPointsGR.changeAttributeValue(pointFeature.id(), pointFeature.fieldNameIndex(QGP.tablePointsFieldNom), newAttributesList[1])	
				if not layerPointAlreadyEditable : self.layerPointsGR.commitChanges()
				self.mainFrame.setStatusDone('Repère ' + str(self.activeIdForChange) + ' : attributs mis à jour = ' + str(newAttributesList))
			except:
				self.mainFrame.setStatusError('Repère ' + str(self.activeIdForChange) + ' : erreur imprévue lors de la mise à jour des attributs')
		else:
			self.mainFrame.setStatusInfo('Repère ' + str(self.activeIdForChange) + ' : annulation de la demande')
		
		self.activeItemForChange = None		
		self.activeIdForChange = None
		del self.pointInputWindow
		

# ========================================================================================
# Opérations sur la Table des POIs
# ========================================================================================	
	
	def initializePOIsTable(self, code, label):

		poisList = self.dicoTracksComputeResults[code][label]

		self.groupBoxPOIsTable.setSortingEnabled(False)		
		self.groupBoxPOIsTable.clearContents()
		self.groupBoxPOIsTable.setRowCount(len(poisList))

		tableFields = QGP.poisTableQView
		for row in range(self.groupBoxPOIsTable.rowCount()): 
			values = [ poisList[row][0][QGP.poisTableFieldId], poisList[row][0][QGP.poisTableFieldIdPOI], \
					    poisList[row][0][QGP.poisTableFieldTitre], poisList[row][0][QGP.poisTableFieldZone], poisList[row][0][QGP.poisTableFieldFlux], \
						int(poisList[row][1]) ]
			for col in range(len(tableFields)):
				value = values[col]	
				item = self.createItem(value, tableFields[col][2])
				self.groupBoxPOIsTable.setItem(row, col, item)

		self.poisTablePositionDico = { poi[0][QGP.poisTableFieldId] : poi[0].geometry().asPoint() for poi in poisList  }
		self.groupBoxPOIsTable.setSortingEnabled(True)		


#	Click on Table Item

	def poisTable_itemRightClicked(self, point):
		if point == None: return
		item = self.groupBoxPOIsTable.itemAt(point)
		id = int(self.groupBoxPOIsTable.item(item.row(),0).text().replace('.',''))
		position = self.poisTablePositionDico[id]
		self.iface.mapCanvas().setCenter(position)
		self.iface.mapCanvas().zoomScale(1000)
		self.mainFrame.setStatusInfo('POI ' + str(id) + ' : zoom du canevas sur ce POI ...')
	
	
# ========================================================================================
# Opérations sur la Table des détails Sections 
# ========================================================================================	
	
	def initializeSectionsTable(self, code):

		sectionsList = self.dicoTracksComputeResults[code][QGP.tableTracksFieldTroncons]

		self.groupBoxSectionsTable.setSortingEnabled(False)		
		self.groupBoxSectionsTable.clearContents()
		self.groupBoxSectionsTable.setRowCount(len(sectionsList))

		tableFields = QGP.sectionsTableQView
		totalDistance = 0
		for row in range(self.groupBoxSectionsTable.rowCount()): 
			sectionId = abs(sectionsList[row])
			delta = self.mainFrame.dicoSectionsGRFeatures[sectionId].geometry().length()
			totalDistance += delta
			grList = []; grpList = []; grtList = []
			riList = []; rbList = []; rfList = []; rlList = []; irList = []; 
			codeList = TCOD.getCodeListALLFromSectionFeature(self.mainFrame.dicoSectionsGRFeatures[sectionId])
			for gr_code in codeList: 
				valid, type, label, zone, number, itineraryCode, trackBaseCode, trackCode, modificationList, invalidationList, repeatCount, bifurcationNumber, direction = TCOD.elementsFromGrCode(gr_code)		
				if not valid : continue
				if trackCode == code: continue
				if type == 'GR' : grList.append(trackBaseCode[3:])
				if type == 'GRP': grpList.append(trackBaseCode[4:])
				if type == 'GRT' : grtList.append(trackBaseCode[4:])
				if type == 'RI' : riList.append(trackBaseCode[3:])
				if type == 'RB' : rbList.append(trackBaseCode[3:])
				if type == 'RF' : rfList.append(trackBaseCode[3:])
				if type == 'RL' : rlList.append(trackBaseCode[3:])
				if type == 'IR' : irList.append(trackBaseCode[3:])
			values = [sectionId, totalDistance, delta, ' '.join(grList), ' '.join(grpList), ' '.join(grtList), ' '.join(riList), ' '.join(rbList), ' '.join(rfList), ' '.join(rlList), ' '.join(irList)]
			for col in range(len(tableFields)):
				value = values[col]	
				item = self.createItem(value, tableFields[col][2])
				self.groupBoxSectionsTable.setItem(row, col, item)

#	Click on Table Item

	def trackSectionTable_itemClicked(self, item):
		id = int(self.groupBoxSectionsTable.item(item.row(),0).text().replace('.',''))
		self.layerSectionsGR.selectByIds([id])
		self.mainFrame.setStatusInfo('Tronçon ' + str(id) + ' : sélectionné dans la table Tronçons-GR ...')		

	def trackSectionTable_itemRightClicked(self, point):
		if point == None: return
		item = self.groupBoxSectionsTable.itemAt(point)
		id = int(self.groupBoxSectionsTable.item(item.row(),0).text().replace('.',''))
		self.layerSectionsGR.selectByIds([id])
		self.iface.mapCanvas().zoomToSelected(self.layerSectionsGR)		
		self.iface.mapCanvas().zoomScale(5000)
		self.mainFrame.setStatusInfo('Tronçon ' + str(id) + ' : zoom du canevas sur ce tronçon ...')
	

# ========================================================================================
# Opérations sur la Table Historique
# ========================================================================================	
	
	def initializeHistoricTable(self, code):

		if self.typeSelected in QGP.typeSetTableGR : historicFeatureList = [feature for feature in self.mainFrame.layerTracksGRHist.getFeatures() if feature[QGP.tableTracksFieldCode] == code]
		if self.typeSelected in QGP.typeSetTableRB : historicFeatureList = [feature for feature in self.mainFrame.layerTracksRBHist.getFeatures() if feature[QGP.tableTracksFieldCode] == code]

		historicFeatureList = sorted(historicFeatureList, key = lambda f: f[QGP.tableTracksFieldId], reverse=True)

		self.groupBoxHistoricTable.setSortingEnabled(False)		
		self.groupBoxHistoricTable.clearContents()
		self.groupBoxHistoricTable.setRowCount(len(historicFeatureList))

		tableFields = QGP.historicTableQView
		for row in range(self.groupBoxHistoricTable.rowCount()): 
			for col in range(len(tableFields)):			
				value = historicFeatureList[row][tableFields[col][0]]
				item = self.createItem(value, tableFields[col][2])
				self.groupBoxHistoricTable.setItem(row, col, item)


# ========================================================================================
# Opérations sur la Table des Repères
# ========================================================================================	

	def initializePointsInfo(self):
		textPointsCount = DSTY.textFormatBlackNormal.replace('%TEXT%',str(len(self.setPointsViewFeatures)) + ' repère.s')
		self.pointCountInfo.setText(textPointsCount)
		DSTY.setStyleOkLabel(self.pointCountInfo, 'Normal')


# ========================================================================================
# Opérations sur la Table des Parcours Communs
# ========================================================================================	

	def initializeCommonTracksTable(self, trackCodeSelected):
	
		dicoCommonTracksSectionsList = self.generateCommonTracksDico(trackCodeSelected)

		self.groupBoxCommonTracksTable.setSortingEnabled(False)		
		self.groupBoxCommonTracksTable.clearContents()
		self.groupBoxCommonTracksTable.setRowCount(len(dicoCommonTracksSectionsList))				
				
		tableFields = QGP.commonTracksTableQView; row = 0
		for trackCode in sorted(dicoCommonTracksSectionsList):
			trackName = self.dicoTracksGRRBFeatures[trackCode][QGP.tableTracksFieldName] if trackCode in self.dicoTracksGRRBFeatures else 'Code Parcours non défini'
			for col in range(len(tableFields)):			
				value = [trackCode, trackName, str(dicoCommonTracksSectionsList[trackCode])][col]
				item = self.createItem(value, tableFields[col][2])
				self.groupBoxCommonTracksTable.setItem(row, col, item)
			row += 1

	def generateCommonTracksDico(self, trackCodeSelected):
		dicoCommonTracksSectionsList = {}
		for sectionId in self.dicoTracksComputeResults[trackCodeSelected][QGP.tableTracksFieldTroncons] :
			all_list = TCOD.getCodeListALLFromSectionFeature(self.mainFrame.dicoSectionsGRFeatures[abs(sectionId)])
			for gr_code in all_list:
				valid, type, label, zone, number, itineraryCode, trackBaseCode, trackCode, modificationList, invalidationList, repeatCount, bifurcationNumber, direction = TCOD.elementsFromGrCode(gr_code)		
				if not valid : continue
				if trackCode == trackCodeSelected: continue
				if trackCode not in dicoCommonTracksSectionsList: dicoCommonTracksSectionsList[trackCode] = []
				dicoCommonTracksSectionsList[trackCode].append(abs(sectionId))
		return dicoCommonTracksSectionsList


# ========================================================================================
# ========================================================================================
#
# Définitions des Listes et Dictionnaires Globaux
# 
# ========================================================================================
# ========================================================================================

#	Table : Parcours-GR et Parcours)RB

	def analyseTablesTracks(self):
		self.mainFrame.setStatusWorking('Rechargement des Tables Parcours GR / RB ...')
		self.analyseTableTracksGR()
		self.analyseTableTracksRB()
		self.mainFrame.setStatusDone('Rechargement des Tables Parcours GR / RB - OK')

#	Table : Parcours-GR

	def analyseTableTracksGR(self, reloadDico = True) :
		if self.layerTracksGR == None:
			self.mainFrame.setStatusError(self.layerTracksGRerror, False)
			return

		if reloadDico : self.mainFrame.dicoTracksGRFeatures = {f[QGP.tableTracksFieldCode] : f for f in self.layerTracksGR.getFeatures()}

		self.listTracksGRCodes = LTRK.getOrderedListItineraryGR({'GR'}, self.mainFrame.dicoTracksGRFeatures)
		self.listTracksGRPCodes = LTRK.getOrderedListItineraryGR({'GRP'}, self.mainFrame.dicoTracksGRFeatures)
		self.listTracksGRTCodes = LTRK.getOrderedListItineraryGR({'GRT'}, self.mainFrame.dicoTracksGRFeatures)
		DSTY.setStyleMainButtonsInactive(self.buttonRefreshTracks)


#	Table : Parcours-RB

	def analyseTableTracksRB(self, reloadDico = True) :
		if self.layerTracksRB == None:
			self.mainFrame.setStatusError(self.layerTracksRBerror, False)
			return

		if reloadDico : self.mainFrame.dicoTracksRBFeatures = {f[QGP.tableTracksFieldCode] : f for f in self.layerTracksRB.getFeatures()}

		self.listTracksRICodes = LTRK.getOrderedListItineraryRB({'RI'}, self.mainFrame.dicoTracksRBFeatures)
		self.listTracksRLCodes = LTRK.getOrderedListItineraryRB({'RL'}, self.mainFrame.dicoTracksRBFeatures)
		self.listTracksRBCodes = LTRK.getOrderedListItineraryRB({'RB'}, self.mainFrame.dicoTracksRBFeatures)
		self.listTracksRFCodes = LTRK.getOrderedListItineraryRB({'RF'}, self.mainFrame.dicoTracksRBFeatures)
		self.listTracksIRCodes = LTRK.getOrderedListItineraryRB({'IR'}, self.mainFrame.dicoTracksRBFeatures)
		DSTY.setStyleMainButtonsInactive(self.buttonRefreshTracks)


#	Table : Tronçons-GR

	def analyseTableSectionsGR(self, reloadDico = True) :
		if self.layerSectionsGR == None:
			self.mainFrame.setStatusError(self.layerSectionsGRerror, False)
			return

		if reloadDico : 
			self.mainFrame.dicoSectionsGRFeatures = { feature[QGP.tableSectionsFieldId] : feature for feature in self.layerSectionsGR.getFeatures() if not feature.geometry().isNull() }
			self.mainFrame.dicoSectionsGRFeaturesEndPoints = { id : [self.mainFrame.dicoSectionsGRFeatures[id].geometry().asMultiPolyline()[0][0], self.mainFrame.dicoSectionsGRFeatures[id].geometry().asMultiPolyline()[0][-1]] \
														for id in self.mainFrame.dicoSectionsGRFeatures }

		textSectionsCount = DSTY.textFormatBlackNormal.replace('%TEXT%',str(len(self.mainFrame.dicoSectionsGRFeatures )) + ' tronçon.s')
		self.sectionCountInfo.setText(textSectionsCount)
		DSTY.setStyleOkLabel(self.sectionCountInfo, 'Normal')
		DSTY.setStyleMainButtonsInactive(self.buttonRefreshSections)


#	Table : Repères-GR

	def extractItineraryLandmarks(self):
		if self.layerPointsGR == None:
			self.mainFrame.setStatusError(self.layerPointsGRError, False)
			return
		
		setItineraryViewCodes = { TCOD.itineraryFromTrackCode(self.dicoTracksIndirectCodes[code]) for code in self.listTracksViewCodes }
		self.setPointsViewFeatures = { feature for feature in self.layerPointsGR.getFeatures() if TCOD.itineraryFromTrackCode(TCOD.grCodeFromPointFeature(feature)) in setItineraryViewCodes }


# ========================================================================================
# ========================================================================================
#
# Actions Principales
# 
# ========================================================================================
# ========================================================================================

# ========================================================================================
# Calcul des Parcours
# ========================================================================================

	def computeTracks(self):

		def getErrorTextFromCode(errorCode):
			if errorCode == 0  : return 'OK'
			if errorCode == 1  : return 'Vide ?'
			if errorCode == 2  : return 'Début où ?'
			if errorCode == 3  : return 'DébutS ?'
			if errorCode == 4  : return 'Incomplet ?'
			if errorCode == 5  : return 'Y par où ?'
			if errorCode == 13 : return 'V:DébutS ?'
			if errorCode == 14 : return 'V:Incomplet ?'
			if errorCode == 15 : return 'V:Y par où ?'
			if errorCode == 16 : return 'V:#?! Boucle'
			return '? Erreur Interne'

#	Check if at least 1 tracks is selected		
		
		if len(self.listTracksSelectedCodes) == 0:
			self.mainFrame.setStatusWarning('Vous devez sélectionner au moins un parcours dans la table !')
			return
		
# 	Create Progress Bar

		progressBar = TPRO.createProgressBar(self.buttonCompute, len(self.listTracksSelectedCodes), 'Normal')
	
#	Dictionnaire des distances pour les parcours	
	
		self.dicoGRTrackDistances = {}		
		
#	Dictionnaire des Parcours GR 			: Déjà créé = self.mainFrame.dicoTracksGRFeatures
#	Dictionnaire des Parcours RB 			: Déjà créé = self.mainFrame.dicoTracksRBFeatures
#	Dictionnaire des Tronçons GR 			: Déjà créé = self.mainFrame.dicoSectionsGRFeatures
#   Dictionnaire des Extrémités Tronçons GR : Déjà créé = self.mainFrame.dicoSectionsGRFeaturesEndPoints
		
		self.dicoTrackSections = LTRK.generateDicoTracksSections(self.typeSelected, self.dicoTracksViewIndirectFeatures, self.mainFrame.dicoSectionsGRFeatures)

#	Effacer les infos qui sont calculées

		self.clearTracksTableBeforeCompute()

#	Déterminer un même time stamp pour tous les parcours calculés

		trackComputeTime = TDAT.getTimeStamp()		

#	Calculer le parcours pour tous les codes sélectionnés

		for codeComputed in self.listTracksSelectedCodes:
			
			self.dicoTracksComputeResults[codeComputed] = {}										# Clear results for this code
		
#			Assemblage des tronçons du parcours

			self.mainFrame.setStatusWorking('Parcours ' + codeComputed + ' : détermination de l\'ordre des tronçons ...')
			sectionOrderedIdList, sectionLostIdList, errorCode, gapList, modificationSet, sectionModifiedIdList = \
													LTRK.computeTracksOrderedSections(self.dicoTracksIndirectCodes[codeComputed], self.dicoTrackSections, self.mainFrame.dicoSectionsGRFeatures, self.mainFrame.dicoSectionsGRFeaturesEndPoints)				
			self.dicoTracksComputeResults[codeComputed][QGP.tableTracksIFieldCalcul] = getErrorTextFromCode(errorCode)
			self.dicoTracksComputeResults[codeComputed][QGP.tableTracksFieldTroncons] = sectionOrderedIdList
			self.dicoTracksComputeResults[codeComputed][QGP.tableTracksIFieldGaps] = gapList
			self.dicoTracksComputeResults[codeComputed][QGP.tableTracksIFieldSectionsLost] = sectionLostIdList
			self.dicoTracksComputeResults[codeComputed][QGP.tableTracksIFieldErrorCode] = errorCode
			self.dicoTracksComputeResults[codeComputed][QGP.tableTracksQFieldModif] = list(modificationSet)
			self.dicoTracksComputeResults[codeComputed][QGP.tableTracksIFieldSectionsModif] = sectionModifiedIdList
			self.dicoTracksComputeResults[codeComputed][QGP.tableTracksIFieldRecorded] = False

#			Calcul de la géométrie, distance, vo - Calcul du Numéro de Point à chaque Section

			self.mainFrame.setStatusWorking('Parcours ' + codeComputed + ' : détermination de la géométrie du parcours ...')
			trackLine = []
			sectionsStartPointList = [0]																# Par définition de la première section
			for sectionNumber in range(len(sectionOrderedIdList)):
				idSection = sectionOrderedIdList[sectionNumber]
				sectionLine = self.mainFrame.dicoSectionsGRFeatures[abs(idSection)].geometry().asMultiPolyline()[0]
				if idSection < 0: sectionLine.reverse()
				trackLine = sectionLine if sectionNumber == 0 else trackLine + sectionLine[1:]
				sectionsStartPointList.append(len(trackLine) - 1)
			trackGeometry = QgsGeometry().fromMultiPolylineXY([trackLine])
			trackDistance = round(trackGeometry.length())
			trackVO = round(trackLine[0].distance(trackLine[-1])) if trackLine != [] else -1
			self.dicoTracksComputeResults[codeComputed][QGP.tableTracksIFieldGeometry] = trackGeometry
			self.dicoTracksComputeResults[codeComputed][QGP.tableTracksFieldDistance] = trackDistance
			self.dicoTracksComputeResults[codeComputed][QGP.tableTracksFieldVO] = trackVO
			self.dicoTracksComputeResults[codeComputed][QGP.tableTracksIFieldSectionsStartPoint] = sectionsStartPointList
			if self.mainFrame.debugModeQCartoLevel >= 3 : print ('SectionsStartPointList = ' + str(sectionsStartPointList))
			if self.mainFrame.debugModeQCartoLevel >= 3 : print ('SectionOrderedIdList = ' + str(sectionOrderedIdList))

# 			Ajouter les altitudes

			self.mainFrame.setStatusWorking('Parcours ' + codeComputed + ' : détermination des altitudes ...')
			trackLineXYZ, missingAltitude1, missingAltitude2 = TALT.addTrackAltitudes(trackLine)
			if missingAltitude1 == None:
				self.mainFrame.setStatusError('Le MNT Wallonie n\'est pas présent sur le canevas !', False)
				return
			if missingAltitude2 == None:
				self.mainFrame.setStatusError('Le MNT Copernicus n\'est pas présent sur le canevas !', False)
				return
			self.dicoTracksComputeResults[codeComputed][QGP.tableTracksIFieldTrackXYZ] = trackLineXYZ
			if self.mainFrame.debugModeQCartoLevel >= 3 : print('Altitudes manquantes = ' + str(missingAltitude1) + ' // ' + str(missingAltitude1))
			
#			Lisser les Altitudes

			dPlus, dMinus, missing = TALT.computeTrackAscending(trackLineXYZ)
			if self.mainFrame.debugModeQCartoLevel >= 3 : print('Denivelés avant lissage : ' + str(round(dPlus)) + ' / ' + str(round(dMinus)))


			trackLineXYZS = trackLineXYZ.copy()
			self.mainFrame.setStatusWorking('Parcours ' + codeComputed + ' : lissage des altitudes ...')
			TALT.smoothTrackAltitudes(trackLineXYZS)
			self.dicoTracksComputeResults[codeComputed][QGP.tableTracksIFieldTrackXYZS] = trackLineXYZS

# 			Calculer les Dénivelés

			self.mainFrame.setStatusWorking('Parcours ' + codeComputed + ' : détermination des dénivelés ...')
			dPlus, dMinus, missing = TALT.computeTrackAscending(trackLineXYZS)
			self.dicoTracksComputeResults[codeComputed][QGP.tableTracksFieldDenivelePos] = round(dPlus)
			self.dicoTracksComputeResults[codeComputed][QGP.tableTracksFieldDeniveleNeg] = round(dMinus)
			if self.mainFrame.debugModeQCartoLevel >= 3 : print('Denivelés après lissage : ' + str(round(dPlus)) + ' / ' + str(round(dMinus)))

# 			Calculer les Altitudes Min et Max	

			self.mainFrame.setStatusWorking('Parcours ' + codeComputed + ' : détermination des altitudes min et max ...')
			altmax, altmin, missing = TALT.computeTrackAltitudesMinMax(trackLineXYZ)
			self.dicoTracksComputeResults[codeComputed][QGP.tableTracksFieldAltmin] = round(altmin)
			self.dicoTracksComputeResults[codeComputed][QGP.tableTracksFieldAltmax] = round(altmax)
			
#			Calculer la distance équivalente	

			self.mainFrame.setStatusWorking('Parcours ' + codeComputed + ' : détermination de la distance équivalente ...')
			distanceEquivalente, distanceEquivalenteInverse, missing = TALT.computeTrackEquivalentDistance(trackLineXYZ)
			if self.mainFrame.debugModeQCartoLevel >= 1 : print (codeComputed + ' - distances UFO = ' + str(distanceEquivalente) + ' - ' + str(distanceEquivalenteInverse))
			self.dicoTracksComputeResults[codeComputed][QGP.tableTracksIFieldDistanceEquivalenteDirecte] = round(distanceEquivalente)	
			self.dicoTracksComputeResults[codeComputed][QGP.tableTracksIFieldDistanceEquivalenteInverse] = round(distanceEquivalenteInverse)	
						
# 			Calculer la distance de Hausdorff par rapport à l'ancien parcours			
			
			hausdorffDistance = None
			if self.optionComputeDelta.isChecked():			
				self.mainFrame.setStatusWorking('Parcours ' + codeComputed + ' : détermination de la distance de Hausdorff par rapport à l\'ancien parcours ...')
				try:
					if self.typeSelected in QGP.typeSetTableGR : oldGeometry = self.mainFrame.dicoTracksGRFeatures[codeComputed].geometry()
					if self.typeSelected in QGP.typeSetTableRB : oldGeometry = self.mainFrame.dicoTracksRBFeatures[codeComputed].geometry()
					oldGeometry = QgsGeometry().fromPolylineXY(oldGeometry.asMultiPolyline()[0])
					hausdorffDistance = round(oldGeometry.hausdorffDistance(QgsGeometry().fromPolylineXY(trackLine)))
				except:
					pass
			self.dicoTracksComputeResults[codeComputed][QGP.tableTracksQFieldDelta] = hausdorffDistance
			
#			Calculer les échelles emprise

			if trackLine != [] :
				trackBox = QgsGeometry().fromPolylineXY(trackLine).boundingBox()
				trackTotalWidth = trackBox.width()
				trackTotalHeight = trackBox.height()
				scalePortrait = int(1 + max(trackTotalWidth / QGP.C_trackScaleMapSize[0], trackTotalHeight/QGP.C_trackScaleMapSize[1]) / 1000)
				scalePaysage = int(1 + max(trackTotalWidth / QGP.C_trackScaleMapSize[1], trackTotalHeight/QGP.C_trackScaleMapSize[0]) / 1000)
				scalePortrait = min( _x_ for _x_ in QGP.C_trackScaleMapList if _x_ >= scalePortrait)
				scalePaysage = min( _x_ for _x_ in QGP.C_trackScaleMapList if _x_ >= scalePaysage)
				self.dicoTracksComputeResults[codeComputed][QGP.tableTracksIFieldEchelleMaxPortrait] = str(scalePortrait) + ' K'
				self.dicoTracksComputeResults[codeComputed][QGP.tableTracksIFieldEchelleMaxPaysage] = str(scalePaysage) + ' K'
			else:
				self.dicoTracksComputeResults[codeComputed][QGP.tableTracksIFieldEchelleMaxPortrait] = '───'
				self.dicoTracksComputeResults[codeComputed][QGP.tableTracksIFieldEchelleMaxPaysage] = '───'
			
#			Calculer le bornage 			
			
			if TQCP.retrieveQCartoParameter(self.mainFrame, 'USER', self.mainFrame.userFullName, 'Bornage', 'Non') == 'Oui' and trackLine != []:
				self.dicoTracksComputeResults[codeComputed][QGP.tableTracksIFieldMarkers], lastMarkerNumber = TBOR.generateMarkerList(trackLine)
			
#			Rechercher les repères accrochés au parcours

			self.mainFrame.setStatusWorking('Parcours ' + codeComputed + ' : détermination des repères ...')
			pointsAttachedList = self.searchPointsNearTrack(self.dicoTracksIndirectCodes[codeComputed], trackLine)
			self.dicoTracksComputeResults[codeComputed][QGP.tableTracksFieldReperes] = [pointAttached[0][QGP.tablePointsFieldRepere] for pointAttached in pointsAttachedList]
			self.dicoTracksComputeResults[codeComputed][QGP.tableTracksIFieldReperesPos] = pointsAttachedList

#			Calculer la liste des Sections d'un repère à l'autre pour le plan

			if self.mainFrame.debugModeQCartoLevel >= 3 : print('PointsAttachedList = ' + str([point[1] for point in pointsAttachedList]))
			self.dicoTracksComputeResults[codeComputed][QGP.tableTracksIFieldReperesSectionList] = []				# List of sections from Point to Point - Warning : points may be on section middle !!
			for pointNum in range(len(pointsAttachedList)) :
				startSectionNum = max(n for n in range(len(sectionsStartPointList)) if pointsAttachedList[pointNum][1] >= sectionsStartPointList[n])			
				if pointNum == len(pointsAttachedList) - 1 :
					endSectionNum = 999999																														# Last point - sections to end
				elif pointsAttachedList[pointNum + 1][1] in sectionsStartPointList :
					endSectionNum = sectionsStartPointList.index(pointsAttachedList[pointNum + 1][1])															# Next point is just on section start 
				else :
					endSectionNum = 1 + max(n for n in range(len(sectionsStartPointList)) if pointsAttachedList[pointNum+1][1] >= sectionsStartPointList[n])	# Next point in section middle	
				sectionList = sectionOrderedIdList[startSectionNum:endSectionNum]
				self.dicoTracksComputeResults[codeComputed][QGP.tableTracksIFieldReperesSectionList].append(sectionList)
				if self.mainFrame.debugModeQCartoLevel >= 3 : 
					print(QGP.tableTracksIFieldReperesSectionList + ' = ' + str(self.dicoTracksComputeResults[codeComputed][QGP.tableTracksIFieldReperesSectionList][-1] ))
					
#			Rechercher les POIs accrochés au parcours - TBC
				
			self.mainFrame.setStatusWorking('Parcours ' + codeComputed + ' : détermination des POIS ...')				
			poisCloseList, poisAttachedList = self.searchPOIsNearTrack(self.dicoTracksIndirectCodes[codeComputed], trackLine)
			if self.mainFrame.debugModeQCartoLevel >= 1 : print ('poisCloseList = ' + str(poisCloseList))
			if self.mainFrame.debugModeQCartoLevel >= 1 : print ('poisAttachedList = ' + str(poisAttachedList))
			self.dicoTracksComputeResults[codeComputed][QGP.tableTracksIFieldPOIsAll] = poisCloseList
			self.dicoTracksComputeResults[codeComputed][QGP.tableTracksIFieldPOIs] = poisAttachedList
			
#			Ajouter l'horodateur
				
			self.dicoTracksComputeResults[codeComputed][QGP.tableTracksFieldDate] = trackComputeTime

#			Calculer le dictionnaire de distance pour ce Parcours

			self.createGRTrackDistancesDico(codeComputed)

#			Afficher les résultats pour ce parcours

			self.showTracksTableComputeResults(codeComputed)

#			Afficher l'avancement

			progressBar.setValue(progressBar.value() + 1)
			QgsApplication.processEvents()

#		Créer le dictionnaire des distances schéma RB RF RI IR

		self.mainFrame.setStatusWorking('Création du Dictionnaire des distances schéma ...')
		status = self.createRBPlanDistancesDico()
		if status == False:
			self.mainFrame.setStatusWarning('Une erreur anormale s\'est produite lors de la création du Dictionnaire des distances schéma !')
			TDAT.sleep(2000)

#		Créer le dictionnaire des distances de l'itinéraire

		self.createItineraryDistancesDico()

#		Terminé !

		self.mainFrame.setStatusDone(str(len(self.listTracksSelectedCodes)) + ' parcour.s : calculs terminés !')
		del progressBar


# ========================================================================================
# Déterminer les repères proches des parcours
# >>> codeComputed			: str			code du parcours en cours de calcul
# >>> trackLine				: [QgsPoints]
# <<< pointsAttached		: [[PointFeature, trackPointNumber]]
# ========================================================================================

	def searchPointsNearTrack(self, codeComputed, trackLine):

		pointsAttached = []
		if trackLine == [] : return pointsAttached

		for pointRepere in self.setPointsViewFeatures:

			gr_code = TCOD.grCodeFromPointFeature(pointRepere)
			if not TCOD.areTrackAndPointCodesCompatibles(codeComputed, gr_code): continue					# Check that all parts of gr_code (of repere) are in code computed (which may have additional parts (-R, -M, ...)
			if pointRepere.geometry().isNull() : continue
	
#			Vérifier si le repère est proche du premier point du parcours

			closeToTrack = False
			distancePointTrack = pointRepere.geometry().distance(QgsGeometry.fromPointXY(trackLine[0]))
			if distancePointTrack <= QGP.configMatchWPDistance :
				closeToTrack = True
				bestDistance = distancePointTrack
				pointNum = 0
				
#			Trouver où les points sont attachés

			for i in range(1, len(trackLine)) :
				distancePointTrack = pointRepere.geometry().distance(QgsGeometry.fromPointXY(trackLine[i]))
				if closeToTrack:
					if distancePointTrack > QGP.configMatchWPDistance:
						pointsAttached.append([QgsFeature(pointRepere), pointNum])
						closeToTrack = False
					if distancePointTrack < bestDistance:
						bestDistance = distancePointTrack
						pointNum = i
				if not closeToTrack:
					if distancePointTrack <= QGP.configMatchWPDistance:
						closeToTrack = True
						bestDistance = distancePointTrack
						pointNum = i
					
#			Traiter le dernier point

			if closeToTrack:
				pointsAttached.append([QgsFeature(pointRepere), pointNum])
				closeToTrack = False

		pointsAttached = sorted(pointsAttached, key = lambda x: x[1])

		return pointsAttached


# ========================================================================================
# Déterminer les POIs proches des parcours
# >>> codeComputed			: str			code du parcours en cours de calcul
# >>> trackLine				: [QgsPoints]
# <<< poisClose				: set([poisFeature, delta])				Pois close to track
# <<< poisAttached			: set([poisFeature, delta])				Pois attached based on rules
# ========================================================================================

	def searchPOIsNearTrack(self, codeComputed, trackLine):

		if self.optionComboPOIsInGPX.currentText() == QGP.C_poisComboTextNoPOIs : return [], []

		poisClose = [ [poisFeature, poisFeature.geometry().distance(QgsGeometry.fromPolylineXY(trackLine)) ] \
				for poisFeature in self.layerPOIs.getFeatures() if poisFeature.geometry().distance(QgsGeometry.fromPolylineXY(trackLine)) <= QGP.C_poisDeltaMax ]		# Find all in range 200m
		poisClose = [ poi for poi in poisClose if poi[1] <= QGP.C_poisDeltaClose]																						# POIs close only
	
		if self.optionComboPOIsInGPX.currentText() == QGP.C_poisComboTextNone :
			poisAttached = []
		elif self.optionComboPOIsInGPX.currentText() == QGP.C_poisComboTextClose : 
			poisAttached = poisClose								
		elif self.optionComboPOIsInGPX.currentText() == QGP.C_poisComboTextAuto :
			if TCOD.itineraryTypeFromTrackCode(codeComputed) in QGP.typeSetComputeGRMode : poisAttached = []
			if TCOD.itineraryTypeFromTrackCode(codeComputed) in QGP.typeSetComputeRBMode : 
				poisAttached = [ poi for poi in poisClose if poi[0][QGP.poisTableFieldFlux] == QGP.C_C_poisTableQViewFieldFluxValidated ]							# RB Auto if here : Flux must be Validée
				poisAttached = [ poi for poi in poisAttached if TCOD.removeModificationsFromTrackCode(codeComputed) in poi[0][QGP.poisTableFieldTracks].split() ]	# RB Auto if here : Track must have been selected
		else :
			pass
		
		return poisClose, poisAttached


# ========================================================================================
# Créer le dictionnaire des distances de l'itinéraire pour GR GRP GRT RI RB RL RF IR
#	- uniquement si le calcul porte sur l'ensemble des parcours d'un unique itinéraire
# ========================================================================================

	def createItineraryDistancesDico(self):
	
#		Déterminer l'itinéraire Concerné

		self.dicoItineraryDistances = {}	
	
		itinerarySet = set((TCOD.itineraryFromTrackCode(code)) for code in self.listTracksSelectedCodes)
		itineratyTypeSet = {TCOD.itineraryTypeFromTrackCode(_) for _ in itinerarySet}
		if len(itineratyTypeSet) != 1: return	
		itineraryType = itineratyTypeSet.pop()
		
		if itineraryType in QGP.typeSetTableGR:
			if len(itinerarySet) != 1: return																				# Works only for a single itinerary in case GR GRP GRT

		if len(self.listTracksSelectedCodes) != len(self.listTracksViewCodes) : return										# Works only if all selected

		for code in self.listTracksSelectedCodes:
			if self.dicoTracksComputeResults[code][QGP.tableTracksIFieldErrorCode] != 0: 	return							# Works only if correctly computed

#		Dictionnaire des distances réelles en mètres par segment		
		
		if itineraryType in QGP.typeSetTableGR:
			for code in self.listTracksSelectedCodes:
				self.dicoItineraryDistances[code] = [self.mainFrame.dicoTracksGRFeatures[code][QGP.tableTracksFieldName], self.dicoTracksComputeResults[code][QGP.tableTracksFieldDistance], \
											self.dicoTracksComputeResults[code][QGP.tableTracksFieldDenivelePos], self.dicoTracksComputeResults[code][QGP.tableTracksFieldDeniveleNeg]]
				if self.mainFrame.debugModeQCartoLevel >= 2 : print('Dico Itinéraire : ' + code + ' = ' + str(self.dicoItineraryDistances[code]))
		if itineraryType in QGP.typeSetTableRB:
			for code in self.listTracksSelectedCodes:
				self.dicoItineraryDistances[code] = [self.mainFrame.dicoTracksRBFeatures[code][QGP.tableTracksFieldName], self.dicoTracksComputeResults[code][QGP.tableTracksFieldDistance], \
											self.dicoTracksComputeResults[code][QGP.tableTracksFieldDenivelePos], self.dicoTracksComputeResults[code][QGP.tableTracksFieldDeniveleNeg]]
				if self.mainFrame.debugModeQCartoLevel >= 2 : print('Dico Itinéraire : ' + code + ' = ' + str(self.dicoItineraryDistances[code]))
			
			
			
# ========================================================================================
# Créer le dictionnaire des distances pour un parcours GR
#	- uniquement pour GR GRP GRT
# ========================================================================================

	def createGRTrackDistancesDico(self, code):
	
#		Preliminary Checks	
	
		self.dicoGRTrackDistances[code] = {}		
		if not self.typeSelected in QGP.typeSetTableGR : return																# Works only for GR

		if self.dicoTracksComputeResults[code][QGP.tableTracksIFieldErrorCode] != 0 : 	return 								# Works only if correctly computed
		if self.dicoTracksComputeResults[code][QGP.tableTracksIFieldReperesPos] == [] : return 								# Works only if points found

#		Dictionnaire des distances réelles en mètres par segment		
		
		self.dicoGRTrackDistances[code][code] = {}
		self.dicoGRTrackDistances[code]['Noms'] = {}		
		
		pointsAttachedList = self.dicoTracksComputeResults[code][QGP.tableTracksIFieldReperesPos]
		startingPoint = pointsAttachedList[0][0]
		trackLineXYZ = self.dicoTracksComputeResults[code][QGP.tableTracksIFieldTrackXYZ]
		for pointNum in range(1, len(pointsAttachedList)) :
			distance = QgsGeometry.fromPolyline(trackLineXYZ[pointsAttachedList[pointNum-1][1]:pointsAttachedList[pointNum][1]+1]).length()
			index =  str(pointsAttachedList[pointNum-1][0][QGP.tablePointsFieldRepere]) + ' >>> ' + str(pointsAttachedList[pointNum][0][QGP.tablePointsFieldRepere])
			self.dicoGRTrackDistances[code][code][index] = distance
			self.dicoGRTrackDistances[code]['Noms'][index] = [str(pointsAttachedList[pointNum-1][0][QGP.tablePointsFieldNom]), str(pointsAttachedList[pointNum][0][QGP.tablePointsFieldNom])]
		self.dicoGRTrackDistances[code][code]['Total'] = self.dicoTracksComputeResults[code][QGP.tableTracksFieldDistance]
				
#		Convertir les distances en hectomètres

		for index in self.dicoGRTrackDistances[code][code]:
			self.dicoGRTrackDistances[code][code][index] = self.dicoGRTrackDistances[code][code][index] / 100

#		Déterminer la Distance totale arrondie du parcours la Distance totale si segments tronqués
#		Note : la distance totale ne concerne que la somme des distances entre point : il peut manquer un point au début et / ou à la fin !!!!

		baseGRDistanceTotal = round(sum(self.dicoGRTrackDistances[code][code][index] for index in self.dicoGRTrackDistances[code][code] if index != 'Total'))
		baseGRDistanceTruncated = int(sum(int(self.dicoGRTrackDistances[code][code][index]) for index in self.dicoGRTrackDistances[code][code] if index != 'Total'))

#		Déterminer la plus haute partie fractionnaire pour un arrondi correspondant au total

		listFractionDistance = [self.dicoGRTrackDistances[code][code][index] % 1 for index in self.dicoGRTrackDistances[code][code] if index != 'Total']
		listFractionDistance.sort(reverse = True)
		countMissing = baseGRDistanceTotal - baseGRDistanceTruncated
		highestFraction = listFractionDistance[countMissing - 1] if countMissing != 0 else 999

#		Arrondir les segments 

		for index in self.dicoGRTrackDistances[code][code]:
			if index == 'Total' : continue
			if self.dicoGRTrackDistances[code][code][index] % 1 >= highestFraction:
				self.dicoGRTrackDistances[code][code][index] = int(self.dicoGRTrackDistances[code][code][index] + 1)
			else:
				self.dicoGRTrackDistances[code][code][index] = int(self.dicoGRTrackDistances[code][code][index])

#		Remettre toutes les valeurs en km

		for index in self.dicoGRTrackDistances[code][code]:
			self.dicoGRTrackDistances[code][code][index] = self.dicoGRTrackDistances[code][code][index] / 10

#		Ajouter les noms

		for index in self.dicoGRTrackDistances[code][code]:
			if index == 'Total' : continue
			self.dicoGRTrackDistances[code][code][index] = [self.dicoGRTrackDistances[code][code][index]] + self.dicoGRTrackDistances[code]['Noms'][index]
		del self.dicoGRTrackDistances[code]['Noms']

#		Autres valeurs pour le Parcours

		lat, lon = TSCR.convertPoint3812toWgs84(startingPoint.geometry().asPoint().x(), startingPoint.geometry().asPoint().y())
		latD, latM, latS = TSCR.latOrLong2DMS(lat)
		lonD, lonM, lonS = TSCR.latOrLong2DMS(lon)
		self.dicoGRTrackDistances[code][' Départ'] = {}																					# Warning index ' Départ' is with 255 space to be last when sorted
		self.dicoGRTrackDistances[code][' Départ']['Lat - Long'] = '{:d}° {:02d}\' {:04.1f}" N , {:d}° {:02d}\' {:04.1f}" E'.format(latD, latM, latS, lonD, lonM, lonS)
		self.dicoGRTrackDistances[code][' Départ']['Dénivelé Pos'] = self.dicoTracksComputeResults[code][QGP.tableTracksFieldDenivelePos]
		self.dicoGRTrackDistances[code][' Départ']['Dénivelé Nég'] = self.dicoTracksComputeResults[code][QGP.tableTracksFieldDeniveleNeg]
		self.dicoGRTrackDistances[code][' Départ']['Altitude Min'] = self.dicoTracksComputeResults[code][QGP.tableTracksFieldAltmin]
		self.dicoGRTrackDistances[code][' Départ']['Altitude Max'] = self.dicoTracksComputeResults[code][QGP.tableTracksFieldAltmax]

#		Cartes IGN

		listMapsIGN = []
		for point in self.dicoTracksComputeResults[code][QGP.tableTracksIFieldReperesPos] :
			mapNumber, mapName = TIGN.convertPoint3812toTopo25(point[0])				
			if mapNumber != None and [mapNumber, mapName] not in listMapsIGN : listMapsIGN.append([mapNumber, mapName])

		mapNum = 0			
		self.dicoGRTrackDistances[code][' IGN 1:25000'] = {}																						# Warning index ' IGN' is with 255 space to be last when sorted
		for map in listMapsIGN :
			mapNum += 1
			self.dicoGRTrackDistances[code][' IGN 1:25000']['Carte ' + str(mapNum)] = map[0] + ' \u00AB' + ' ' + map[1] + ' \u00BB'

		return 


# ========================================================================================
# Créer le dictionnaire des distances pour schéma et maquetistes
#	- uniquement pour RB RF
#	- uniquement si le calcul ne porte pas sur plusieurs RB
# ========================================================================================

	def createRBPlanDistancesDico(self):
	
		self.dicoRBPlanDistances, self.dicoRBPlanTracksList = TPRB.createRBPlan(self.mainFrame, self.listTracksSelectedCodes, self.dicoTracksComputeResults, self.mainFrame.dicoSectionsGRFeatures)
		for code in self.dicoRBPlanDistances :
			for info in self.dicoRBPlanDistances[code] :
				if self.mainFrame.debugModeQCartoLevel >= 3 : print('RB Dico Main / Index = ' + code + ' / ' + info + ' = ' + str(self.dicoRBPlanDistances[code][info]))
		for code in self.dicoRBPlanTracksList :
			for index in self.dicoRBPlanTracksList[code] :
				if self.mainFrame.debugModeQCartoLevel >= 3 : print('Common Tracks - Code / Index = ' + code + ' / ' + index + ' = ' + str(self.dicoRBPlanTracksList[code][index]))
				
		return True				
					

	def createRBPlanDistancesDico_oldVersion(self) :				# No longer used
	
#		Déterminer la RB concernée 	

		self.dicoRBPlanDistances = {}	
		self.dicoRBPlanTracksList = {}	
		if not self.typeSelected in QGP.typeSetTableRB : return None														# Works only for RB
	
		itineraryRBSet = set((TCOD.itineraryFromTrackCode(code)) for code in self.listTracksSelectedCodes)
		if len(itineraryRBSet) != 1: return	None																			# Works only for a single RB
		itineraryRB = itineraryRBSet.pop()
		
#		Déterminer l'itinéraire principal - attention aux cas des modifications futures ou temporaires

		if itineraryRB in self.listTracksSelectedCodes:
			itineraryRBMain = itineraryRB
		elif itineraryRB + '-MF' in self.listTracksSelectedCodes:
			itineraryRBMain = itineraryRB + '-MF'
		elif itineraryRB + '-MT' in self.listTracksSelectedCodes:
			itineraryRBMain = itineraryRB + '-MT'
		else:
			return None

		for code in self.listTracksSelectedCodes:
			if self.dicoTracksComputeResults[code][QGP.tableTracksIFieldErrorCode] != 0: 	return None						# Works only if correctly computed
			if self.dicoTracksComputeResults[code][QGP.tableTracksIFieldReperesPos] == [] : return None						# Works only if points found

#		Dictionnaire des distances réelles en mètres par segment	
		
		for code in self.listTracksSelectedCodes:
			self.dicoRBPlanDistances[code] = {}
			pointsAttachedList = self.dicoTracksComputeResults[code][QGP.tableTracksIFieldReperesPos]
			if code == itineraryRBMain: startingPoint = pointsAttachedList[0][0]
			trackLineXYZ = self.dicoTracksComputeResults[code][QGP.tableTracksIFieldTrackXYZ]
			for pointNum in range(1, len(pointsAttachedList)) :
				distance = QgsGeometry.fromPolyline(trackLineXYZ[pointsAttachedList[pointNum-1][1]:pointsAttachedList[pointNum][1]+1]).length()
				index =  str(pointsAttachedList[pointNum-1][0][QGP.tablePointsFieldRepere]) + ' >>> ' + str(pointsAttachedList[pointNum][0][QGP.tablePointsFieldRepere])
				self.dicoRBPlanDistances[code][index] = distance
				if self.mainFrame.debugModeQCartoLevel == 3 : print('Code = ' + code + ' // pointNum = ' + str(pointNum) + ' // pt de = ' + str(pointsAttachedList[pointNum-1][1]) \
																		+ ' // pt & = ' + str(pointsAttachedList[pointNum][1]) + ' // m = ' + str(distance) \
																		+ ' // tot = ' + str(QgsGeometry.fromPolyline(trackLineXYZ[0:pointsAttachedList[pointNum][1]]).length()))	
			if self.mainFrame.debugModeQCartoLevel == 3 : print('Tot = ' + str(QgsGeometry.fromPolyline(trackLineXYZ).length()) + ' // nbrpt = ' + str(len(trackLineXYZ)))
			self.dicoRBPlanDistances[code]['Total'] = round(self.dicoTracksComputeResults[code][QGP.tableTracksFieldDistance])
				
#		Dictionnaire des autres Tracés GR.P.T

		for code in self.listTracksSelectedCodes:
			self.dicoRBPlanTracksList[code] = {}
			pointsAttachedList = self.dicoTracksComputeResults[code][QGP.tableTracksIFieldReperesPos]
			for pointNum in range(1, len(pointsAttachedList)) :
				index =  str(pointsAttachedList[pointNum-1][0][QGP.tablePointsFieldRepere]) + ' >>> ' + str(pointsAttachedList[pointNum][0][QGP.tablePointsFieldRepere])
				sectionList = self.dicoTracksComputeResults[code][QGP.tableTracksIFieldReperesSectionList][pointNum-1]
				if sectionList == None : self.dicoRBPlanTracksList[code][index] = '--?--' ; continue
				pointTrackList = []
				lastSectionOnGRList = None
				for sectionId in sectionList:
					sectionOnGRList = []
					sectionFeature = self.mainFrame.dicoSectionsGRFeatures[abs(sectionId)]
#					if not DSYM.isSectionFeatureMarked(sectionFeature) : continue							# Bug - msut continue to take HGR into account
					codeList = TCOD.getCodeListGRFromSectionFeature(sectionFeature)
					for gr_code in codeList: 
						valid, type, label, zone, number, itineraryCode, trackBaseCode, trackCode, modificationList, invalidationList, repeatCount, bifurcationNumber, direction = TCOD.elementsFromGrCode(gr_code)		
						if not valid : continue
						if not DSYM.isSectionGrCodeMarked(self.mainFrame, gr_code) : continue
						trackCodeParts = trackCode.split('-')
						if len(trackCodeParts) == 2 or (len(trackCodeParts) == 3 and trackCodeParts[2][0] == 'P') :	
							sectionOnGRList.append(trackCodeParts[1])
						elif len(trackCodeParts) == 3 :
							sectionOnGRList.append(trackCodeParts[1] + '-' + trackCodeParts[2][0])
						else:
							sectionOnGRList.append('?')
					sectionOnGRList = sorted(list(set(sectionOnGRList)))			
					if sectionOnGRList != lastSectionOnGRList : pointTrackList.append(sectionOnGRList) ; lastSectionOnGRList = sectionOnGRList
				if self.mainFrame.debugModeQCartoLevel >= 3 : print('pointTrackList = ' + str(pointTrackList))
				textList = []
				for sectionList in pointTrackList :
					textList.append(' '.join(gr for gr in sectionList) if sectionList != [] else '══')
				if self.mainFrame.debugModeQCartoLevel >= 3 : print('TextList = ' + str(textList))
				self.dicoRBPlanTracksList[code][index] = (' ║ '.join(text for text in textList)) if any(text != '══' for text in textList) else '══'
				if self.mainFrame.debugModeQCartoLevel >= 3 : print('Index ' + index + ' = ' + str(self.dicoRBPlanTracksList[code][index]))
				
#		Convertir les distances en hectomètres

		if self.mainFrame.debugModeQCartoLevel == 3 : print('RB Base - Distances Réelles en hectomètres')	
		for code in self.dicoRBPlanDistances:
			for index in self.dicoRBPlanDistances[code]:
				self.dicoRBPlanDistances[code][index] = self.dicoRBPlanDistances[code][index] / 100
				if self.mainFrame.debugModeQCartoLevel == 3 : print(code + ' : ' + index + ' = ' + str(self.dicoRBPlanDistances[code][index]))

#		Déterminer la Distance totale arrondie de la RB de Base et la Distance totale si segments tronqués

		baseRBDistanceTotal = self.dicoRBPlanDistances[itineraryRBMain]['Total'] = round(self.dicoRBPlanDistances[itineraryRBMain]['Total'])
		if self.mainFrame.debugModeQCartoLevel == 3 : print ('RB Base - Distance Totale = ' + str(baseRBDistanceTotal))
	
		baseRBDistanceTruncated = sum(int(self.dicoRBPlanDistances[itineraryRBMain][index]) for index in self.dicoRBPlanDistances[itineraryRBMain] if index != 'Total')
		if self.mainFrame.debugModeQCartoLevel == 3 : print ('RB Base - Distance Tronquée = ' + str(baseRBDistanceTruncated))

#		Déterminer la plus haute partie fractionnaire pour un arrondi correspondant au total

		listFractionDistance = [self.dicoRBPlanDistances[itineraryRBMain][index] % 1 for index in self.dicoRBPlanDistances[itineraryRBMain] if index != 'Total']
		listFractionDistance.sort(reverse = True)
		countMissing = baseRBDistanceTotal - baseRBDistanceTruncated
		if countMissing > len(listFractionDistance) :
			print ('RB Base - countMissing = ' + str(countMissing) + ' >>> ' + str(len(listFractionDistance)) + ' ???')
			return False
			countMissing = len(listFractionDistance)
		highestFraction = listFractionDistance[countMissing - 1] if countMissing != 0 else 999
		if self.mainFrame.debugModeQCartoLevel == 3 : print ('RB Base - Liste Fractions = ' + str(listFractionDistance))
		if self.mainFrame.debugModeQCartoLevel == 3 : print ('RB Base - Highest Fraction = ' + str(highestFraction))

#		Arrondir les segments de la RB de Base

		if self.mainFrame.debugModeQCartoLevel == 3 : print('RB Base - Distances Finales en hectomètres')	
		for index in self.dicoRBPlanDistances[itineraryRBMain]:
			if index == 'Total' : continue
			if self.dicoRBPlanDistances[itineraryRBMain][index] % 1 >= highestFraction:
				self.dicoRBPlanDistances[itineraryRBMain][index] = int(self.dicoRBPlanDistances[itineraryRBMain][index] + 1)
			else:
				self.dicoRBPlanDistances[itineraryRBMain][index] = int(self.dicoRBPlanDistances[itineraryRBMain][index])
			if self.mainFrame.debugModeQCartoLevel == 3 : print(itineraryRBMain + ' : ' + index + ' = ' + str(self.dicoRBPlanDistances[itineraryRBMain][index]))

#		Traiter les variantes

		for code in self.dicoRBPlanDistances:
			if code == itineraryRBMain: continue
			
#			Déterminer la distance totale arrondie			
	
			variantRBDistanceTotal = self.dicoRBPlanDistances[code]['Total'] = round(self.dicoRBPlanDistances[code]['Total'])
			if self.mainFrame.debugModeQCartoLevel == 3 : print (code + ' : Distance Totale Variant = ' + str(variantRBDistanceTotal))
				
#			Déterminer la partie déjà fixée et la partie libre (segments spécifiques)
			
			variantFixedDistance = variantFreeDistance = 0
			indexFixed = []
			for index in self.dicoRBPlanDistances[code]:
				if index == 'Total' : continue
				if index in self.dicoRBPlanDistances[itineraryRBMain] and abs(self.dicoRBPlanDistances[itineraryRBMain][index] - self.dicoRBPlanDistances[code][index]) <= 1:		
					variantFixedDistance += self.dicoRBPlanDistances[itineraryRBMain][index]											# Valeur réelle déjà déterminée
					indexFixed.append(index)
				else:
					variantFreeDistance += int(self.dicoRBPlanDistances[code][index])												# Valeur tronquée

#			Calculer la distance manquante et éliminer les segments de la RB de base

			missingDistance = variantRBDistanceTotal - variantFixedDistance - variantFreeDistance
			for index in indexFixed:
				self.dicoRBPlanDistances[code].pop(index)
			if self.mainFrame.debugModeQCartoLevel == 3 : print (code + ' : Distance RB Variant Missing = ' + str(missingDistance))
			if self.mainFrame.debugModeQCartoLevel == 3 : print (code + ' : Distance RB Variant Free = ' + str(variantFreeDistance))
			if self.mainFrame.debugModeQCartoLevel == 3 : print (code + ' : Distance RB Variant Fixed = ' + str(variantFixedDistance))
			if self.mainFrame.debugModeQCartoLevel == 3 : print (code + ' : Index restants = ' + str(len(self.dicoRBPlanDistances[code]) - 1))						# -1 for Total

#			Déterminer et arrondir les segments nécessaires

			listFractionDistance = [self.dicoRBPlanDistances[code][index] % 1 for index in self.dicoRBPlanDistances[code] if index != 'Total']
			listFractionDistance.sort(reverse = True)
			if listFractionDistance == [] : 
				if self.mainFrame.debugModeQCartoLevel == 3 : print(code + ' : la liste des segments propres est vide !')
				continue
				
#			Cas principal ou il manque de la distance 				
				
			if 	missingDistance >= 0 :
				countMissing = missingDistance
				extraDelta = 0
				while countMissing > len(listFractionDistance) :																		# Sometime need moe then just ronding
					countMissing -= len(listFractionDistance)
					extraDelta += 1
				if self.mainFrame.debugModeQCartoLevel == 3 : print('Extra Delta = ' + str(extraDelta))
				if self.mainFrame.debugModeQCartoLevel == 3 : print('countMissing = ' + str(countMissing))
				if self.mainFrame.debugModeQCartoLevel == 3 : print('listFractionDistance = ' + str(listFractionDistance))
				highestFraction = listFractionDistance[countMissing - 1] if countMissing != 0 else 999
				if self.mainFrame.debugModeQCartoLevel == 3 : print (code + ' - Liste Fractions = ' + str(listFractionDistance))
				if self.mainFrame.debugModeQCartoLevel == 3 : print (code + ' - Highest Fraction = ' + str(highestFraction))
				for index in self.dicoRBPlanDistances[code]:
					if index == 'Total' : continue
					if self.dicoRBPlanDistances[code][index] % 1 >= highestFraction:
						self.dicoRBPlanDistances[code][index] = int(self.dicoRBPlanDistances[code][index] + 1) + extraDelta
					else:
						self.dicoRBPlanDistances[code][index] = int(self.dicoRBPlanDistances[code][index]) + extraDelta
					if self.mainFrame.debugModeQCartoLevel == 3 : print(code + ' : ' + index + ' = ' + str(self.dicoRBPlanDistances[code][index]))

#			Cas rare ou il faut supprimer de la distance

			if 	missingDistance < 0 :
				listFractionDistance.reverse()																						# Need to find smallest	
				countExtra = -missingDistance
				extraDelta = 0
				while countExtra > len(listFractionDistance) :																		# Sometime need moe then just ronding
					countExtra -= len(listFractionDistance)
					extraDelta += 1
				if self.mainFrame.debugModeQCartoLevel == 3 : print('Extra Delta = ' + str(extraDelta))
				if self.mainFrame.debugModeQCartoLevel == 3 : print('countExtra = ' + str(countExtra))
				if self.mainFrame.debugModeQCartoLevel == 3 : print('listFractionDistance = ' + str(listFractionDistance))
				smallestFraction = listFractionDistance[countExtra - 1] if countExtra != 0 else 999
				if self.mainFrame.debugModeQCartoLevel == 3 : print (code + ' - Liste Fractions = ' + str(listFractionDistance))
				if self.mainFrame.debugModeQCartoLevel == 3 : print (code + ' - Smallest Fraction = ' + str(smallestFraction))
				for index in self.dicoRBPlanDistances[code]:
					if index == 'Total' : continue
					if self.dicoRBPlanDistances[code][index] % 1 <= smallestFraction:
						self.dicoRBPlanDistances[code][index] = int(self.dicoRBPlanDistances[code][index] - 1) - extraDelta
					else:
						self.dicoRBPlanDistances[code][index] = int(self.dicoRBPlanDistances[code][index]) - extraDelta
					if self.mainFrame.debugModeQCartoLevel == 3 : print(code + ' : ' + index + ' = ' + str(self.dicoRBPlanDistances[code][index]))

#			Ajouter différence

			self.dicoRBPlanDistances[code]['Différence'] = abs(variantRBDistanceTotal - baseRBDistanceTotal)

#		Remettre toutes les valeurs en km

		for code in self.dicoRBPlanDistances:
			for index in self.dicoRBPlanDistances[code]:
				self.dicoRBPlanDistances[code][index] = self.dicoRBPlanDistances[code][index] / 10

#		Autres valeurs pour la RB Base

		lat, lon = TSCR.convertPoint3812toWgs84(startingPoint.geometry().asPoint().x(), startingPoint.geometry().asPoint().y())
		latD, latM, latS = TSCR.latOrLong2DMS(lat)
		lonD, lonM, lonS = TSCR.latOrLong2DMS(lon)
		self.dicoRBPlanDistances[' Départ'] = {}																					# Warning index ' Départ' is with 255 space to be last when sorted
		self.dicoRBPlanDistances[' Départ']['Lat - Long'] = '{:d}° {:02d}\' {:04.1f}" N , {:d}° {:02d}\' {:04.1f}" E'.format(latD, latM, latS, lonD, lonM, lonS)
		self.dicoRBPlanDistances[' Départ']['Dénivelé'] = self.dicoTracksComputeResults[itineraryRBMain][QGP.tableTracksFieldDenivelePos]
		self.dicoRBPlanDistances[' Départ']['Altitude Min'] = self.dicoTracksComputeResults[itineraryRBMain][QGP.tableTracksFieldAltmin]
		self.dicoRBPlanDistances[' Départ']['Altitude Max'] = self.dicoTracksComputeResults[itineraryRBMain][QGP.tableTracksFieldAltmax]

#		Cartes IGN

		listMapsIGN = []
		for code in self.listTracksSelectedCodes:
			for point in self.dicoTracksComputeResults[code][QGP.tableTracksIFieldReperesPos] :
				mapNumber, mapName = TIGN.convertPoint3812toTopo25(point[0])				
				if mapNumber != None and [mapNumber, mapName] not in listMapsIGN : listMapsIGN.append([mapNumber, mapName])

		mapNum = 0			
		self.dicoRBPlanDistances[' IGN 1:25000'] = {}																				# Warning index ' IGN' is with 255 space to be last when sorted
		for map in listMapsIGN :
			mapNum += 1
			self.dicoRBPlanDistances[' IGN 1:25000']['Carte ' + str(mapNum)] = map[0] + ' \u00AB' + ' ' + map[1] + ' \u00BB'

		return True


# ========================================================================================
# Enregistrement des Parcours
# ========================================================================================

	def recordTracksForced(self):
		self.trackRecordForced = not self.trackRecordForced 
		DSTY.setStyleNormalStrongButton(self.buttonRecord) if self.trackRecordForced else DSTY.setStyleNormalButton(self.buttonRecord)


	def recordTracks(self):

		if not self.controlTrackComputed() : return
		
		if not self.optionComputeDelta.isChecked():	
			self.mainFrame.setStatusWarning('L\'enregistrement n\'est possible que si la Calcul des Delta Haussdorf est coché !')
			return
		
#	Retrieve correct track layer and open it in edition

		if self.typeSelected in QGP.typeSetTableGR : layerTrack = self.layerTracksGR; layerHistoric = self.layerTracksGRHist
		if self.typeSelected in QGP.typeSetTableRB : layerTrack = self.layerTracksRB; layerHistoric = self.layerTracksRBHist
		
		layerTrack.startEditing()
		layerHistoric.startEditing()
		
# 	Create Progress Bar - 1 for time to commit

		progressBar = TPRO.createProgressBar(self.buttonRecord, 4 + 4 + 2 * len(self.listTracksSelectedCodes), 'Normal')
	
#	Enregistrer les parcours correctement calculés

		recordedCount = notRecordedCount = notChangedCount = 0

		for codeRecorded in self.listTracksSelectedCodes:

			self.mainFrame.setStatusWorking('Enregistrement du parcours : ' + codeRecorded + ' - ' + self.dicoTracksViewFeatures[codeRecorded][QGP.tableTracksFieldName])

#			Eviter les parcours incorectment calculés			

			if self.dicoTracksComputeResults[codeRecorded][QGP.tableTracksIFieldErrorCode] != 0: 
				notRecordedCount += 1
				progressBar.setValue(progressBar.value() + 1)
				continue

#			Eviter les parcours non changés - sauf si forcage

			if not self.trackRecordForced:
				if self.dicoTracksComputeResults[codeRecorded][QGP.tableTracksIFieldRecorded] or \
											(self.dicoTracksComputeResults[codeRecorded][QGP.tableTracksQFieldDelta] != None and self.dicoTracksComputeResults[codeRecorded][QGP.tableTracksQFieldDelta] < 1):
					notChangedCount += 1
					progressBar.setValue(progressBar.value() + 1)
					continue

#			Retrouver l'entité de base

			if self.typeSelected in QGP.typeSetTableGR : trackFeature = self.mainFrame.dicoTracksGRFeatures[codeRecorded]
			if self.typeSelected in QGP.typeSetTableRB : trackFeature = self.mainFrame.dicoTracksRBFeatures[codeRecorded]

#			Modifier les attributs calculés

			tableFields = QGP.tracksTableQView

			for col in range(len(tableFields)):
				if tableFields[col][3] != 'Calcul' : continue
				field = tableFields[col][0]
				type = tableFields[col][2]
				value = self.dicoTracksComputeResults[codeRecorded][field] if type != 'List' else str(self.dicoTracksComputeResults[codeRecorded][field])
				layerTrack.changeAttributeValue(trackFeature.id(), trackFeature.fieldNameIndex(field), value)
				trackFeature.setAttribute(trackFeature.fieldNameIndex(field), value)

#			Modifier la géométrie dans la couche DB et dans le dictionnaire 

			layerTrack.changeGeometry(trackFeature.id(), self.dicoTracksComputeResults[codeRecorded][QGP.tableTracksIFieldGeometry])
			trackFeature.setGeometry(self.dicoTracksComputeResults[codeRecorded][QGP.tableTracksIFieldGeometry])
			progressBar.setValue(progressBar.value() + 1)
				
#			Enregistrer l'Historique

			trackHistFeature = QgsFeature()
			trackHistFeature.setFields(layerHistoric.fields())
			for fieldName in layerTrack.fields().names():
				trackHistFeature.setAttribute(fieldName, trackFeature[fieldName])
			trackHistFeature[QGP.tableTracksFieldId] = int(time.time() * 1000)
			trackHistFeature[QGP.tableTracksFieldDelta] = self.dicoTracksComputeResults[codeRecorded][QGP.tableTracksQFieldDelta]
			trackHistFeature[QGP.tableAllFieldNomCarto] = QgsApplication.userFullName()															# Not automatical when create
			trackHistFeature[QGP.tableTracksFieldDate] = self.dicoTracksComputeResults[codeRecorded][QGP.tableTracksFieldDate]					# Be sure to take new date
						
			trackHistFeature.setGeometry(self.dicoTracksComputeResults[codeRecorded][QGP.tableTracksIFieldGeometry])
			layerHistoric.addFeature(trackHistFeature)

#			Afficher l'avancement

			self.dicoTracksComputeResults[codeRecorded][QGP.tableTracksIFieldRecorded] = True
			progressBar.setValue(progressBar.value() + 1)
			QgsApplication.processEvents()
			recordedCount += 1

		self.mainFrame.setStatusWorking('Fermeture de la couche des Parcours ...')
		layerTrack.commitChanges()
		progressBar.setValue(progressBar.value() + 4)
		layerHistoric.commitChanges()
		progressBar.setValue(progressBar.value() + 4)

#	Afficher le status final

		if notRecordedCount == 0 and notChangedCount == 0:
			self.mainFrame.setStatusDone(str(recordedCount) + ' parcours enregistrés !')
		else:
			self.mainFrame.setStatusDone(str(recordedCount) + ' parcours enregistrés - '  + str(notChangedCount) + ' parcours inchangés - ' + str(notRecordedCount) + ' parcours incorrects')
		del progressBar
	
		self.trackRecordForced = False
		DSTY.setStyleNormalButton(self.buttonRecord)

	
# ========================================================================================
# Export des Parcours - GPX PLT 
# ========================================================================================

	def exportTracksGPX(self):
	
		if not self.controlTrackComputed() : return
		
# 	Create Progress Bar 

		progressBar = TPRO.createProgressBar(self.buttonExportGPX, len(self.listTracksSelectedCodes), 'Normal')

# 	Même timestamp pour tous les exports --- V 7.9 : Toujours timestamp complet

		timeStamp = TDAT.getTimeStamp()
		timeStampGPX = ' (' + timeStamp + ')'
		timeStampOzi = ' (' + timeStamp + ')'

#	Même Préfix pour tous --- V 7.9

		prefixGPX = DTOP.prefixGPX + ' - '

#	Exporter les parcours correctement calculés

		exportedCount = notExportedCount = exportedCountSityTrail = notExportedCountSityTrail = 0

		for codeExported in self.listTracksSelectedCodes:

			self.mainFrame.setStatusWorking('Export GPX du parcours : ' + codeExported + ' - ' + self.dicoTracksViewFeatures[codeExported][QGP.tableTracksFieldName])

#			Eviter les parcours incorrectement calculés			

			if self.dicoTracksComputeResults[codeExported][QGP.tableTracksIFieldErrorCode] != 0: 
				notExportedCount += 1
				progressBar.setValue(progressBar.value() + 1)
				continue

#			Retrouver l'entité de base

			if self.typeSelected in QGP.typeSetTableGR : trackFeature = self.mainFrame.dicoTracksGRFeatures[codeExported]
			if self.typeSelected in QGP.typeSetTableRB : trackFeature = self.mainFrame.dicoTracksRBFeatures[codeExported]

#			Déterminer le path et le nom des fichiers
			
			projectCode = TCOD.projectFromTrackCode(codeExported)
			trackName = self.dicoTracksViewFeatures[codeExported][QGP.tableTracksFieldName]

			pathGPX = QGP.configPathExportGPX.replace('%PROJECT%', projectCode)
			fileGPX = fileBaseName = TGPX.defineTrackNameGPX(codeExported, trackName, False)
			fileGPX = prefixGPX + fileGPX
			fileGPX += timeStampGPX
			fileGPX += '.gpx'

#			Déterminer les repères à inclure dans le GPX - en éliminant les doublons

			pointSet = { pointAttached[0] for pointAttached in self.dicoTracksComputeResults[codeExported][QGP.tableTracksIFieldReperesPos]} if self.optionIncludeWPInGPX.isChecked() else set()
	
#			Déterminer les POI à inclure dans le GPX

			poisSet = { poi[0] for poi in self.dicoTracksComputeResults[codeExported][QGP.tableTracksIFieldPOIs] }

#			Supprimer old GPX files si option

			if self.optionDeleteOldGPX.isChecked():
				TFIL.remove_files(pathGPX, fileBaseName, len(fileGPX))

#			Export GPX

			trackXYZ = self.dicoTracksComputeResults[codeExported][QGP.tableTracksIFieldTrackXYZ]
			TGPX.exportGpxTrack(pathGPX, fileGPX, codeExported, trackName, trackName, trackXYZ, pointSet, poisSet)

#			Export GPX for SityTrail

			if TQCP.retrieveQCartoParameter(self.mainFrame, 'USER', self.mainFrame.userFullName, 'SityTrail', 'Non') == 'Oui' :
				if self.typeSelected in QGP.typeSetSityTrail : 
					status = TGPX.exportGpxSityTrail(self, codeExported, timeStampGPX)
					if status : exportedCountSityTrail += 1
					else : notExportedCountSityTrail += 1

#			Export GPX for Retrocompatibility (Xavier on GPX à jour)

			if self.optionCompatibilityGPX.checkState() == Qt.Checked :
				if self.typeSelected in QGP.typeSetTableGR : 
					pathGPXCompatibility = QGP.pathCompatibilityGPXForGR
				if self.typeSelected in QGP.typeSetTableRB : 
					pathGPXCompatibility = QGP.pathCompatibilityGPXForRB
					pathGPXCompatibility = pathGPXCompatibility.replace('%TYPE%', self.typeSelected)
					pathGPXCompatibility = pathGPXCompatibility.replace('%ITI%', projectCode)
				fileGPXCompatibility = fileBaseNameCompatibility = TGPX.defineTrackNameGPX(codeExported, trackName, True)
				fileGPXCompatibility += '_' + TDAT.getGPXDateStamp()
				fileGPXCompatibility += '.gpx'
			
				TFIL.remove_files(pathGPXCompatibility, fileBaseNameCompatibility, len(fileGPXCompatibility))
				TGPX.exportGpxTrack(pathGPXCompatibility, fileGPXCompatibility, codeExported, trackName, trackName, trackXYZ, pointSet, poisSet)
			
#			Export Ozi

			if TQCP.retrieveQCartoParameter(self.mainFrame, 'USER', self.mainFrame.userFullName, 'GénérationOzi', 'Non') == 'Oui' :
				pathOZI = QGP.configPathExportOZI.replace('%PROJECT%', projectCode)
				fileOzi = TFIL.cleanFileName(trackName)
				fileOzi += timeStampOzi 
				fileOzi += '.plt'
				trackNameOzi = trackName + ' (' + timeStamp[0:10] + ')'
				if self.optionDeleteOldGPX.isChecked(): TFIL.remove_files(pathOZI, TFIL.cleanFileName(trackName), len(fileOzi))
				TOZI.exportOziTrack(pathOZI, fileOzi, codeExported, trackNameOzi, trackXYZ)

#			Export GPX Bornage - Option

			if TQCP.retrieveQCartoParameter(self.mainFrame, 'USER', self.mainFrame.userFullName, 'Bornage', 'Non') == 'Oui' :
				pathGPX = QGP.configPathExportGPXMarkers.replace('%PROJECT%', projectCode)
				fileGPX = fileBaseName = TGPX.defineTrackNameGPX(codeExported, trackName, False)
				fileGPX += ' - Bornes' 
				fileGPX += timeStampGPX
				fileGPX += '.gpx'
				if self.optionDeleteOldGPX.isChecked():
					TFIL.remove_files(pathGPX, fileBaseName, len(fileGPX))
				TGPX.exportGpxMarkers(pathGPX, fileGPX, self.dicoTracksComputeResults[codeExported][QGP.tableTracksIFieldMarkers],  '{:d} km')

#			Afficher l'avancement

			progressBar.setValue(progressBar.value() + 1)
			QgsApplication.processEvents()
			exportedCount += 1

#	Afficher le status final

		if notExportedCount == 0 and notExportedCountSityTrail == 0:
			self.mainFrame.setStatusDone(str(exportedCount) + ' parcours exportés !' + ' - ' + str(exportedCountSityTrail) + ' parcours SityTrail !')
		elif notExportedCountSityTrail > 0 :
			self.mainFrame.setStatusWarning('Erreur export Gpx SityTrail : ' + str(notExportedCountSityTrail) + ' parcours incorrect.s')
		else:
			self.mainFrame.setStatusWarning(str(exportedCount) + ' parcours exportés - ' + str(notExportedCount) + ' parcours incorrects - ' + str(exportedCountSityTrail) + ' parcours SityTrail')
		del progressBar
	
	
# ========================================================================================
# Export des Parcours - Html
# ========================================================================================

	def initializeTracksHtmlTable(self):
		
		self.groupBoxHtmlTracksTable.setSortingEnabled(False)									
		self.groupBoxHtmlTracksTable.clearContents()
		self.groupBoxHtmlTracksTable.setRowCount(len(self.listTracksSelectedCodes) + 1)												# 1 extra for cahier MAJ
		if len(self.listTracksSelectedCodes) == 0: self.mainFrame.setStatusWarning('Aucun code n\'est sélectionné !'); return
		self.sortedListTracksCodesForHtml = sorted(self.listTracksSelectedCodes, key=TCOD.getTrackTableALLSortingValue)

#		Rechercher les Dates des GPX sur le Site SGR

		fileGPXSiteList = TSGR.readSiteSGRDirectory('GPX')
		if fileGPXSiteList == None: self.mainFrame.setStatusWarning('Lecture du répertoire GPX impossible sur le Site SGR !'); return
		fileGPXSiteDico = { file[:-15] : file[-14:-4] for file in fileGPXSiteList}
		if self.mainFrame.debugModeQCartoLevel >= 2 : 
			for entry in sorted(fileGPXSiteDico) :
				print('fileGPXSiteDico : ' + entry + ' = <<<' + fileGPXSiteDico[entry] + '>>>')

#		Rechercher les Dates des GPX en local

		projectCode = TCOD.projectFromTrackCode(self.sortedListTracksCodesForHtml[0])
		pathLocalGPX = QGP.configPathExportGPX.replace('%PROJECT%', projectCode)
		fileGPXLocalDico = {}
		if os.path.isdir(pathLocalGPX): 	
			lastBaseName = lastTimeStamp = None
			for fileName in os.listdir(pathLocalGPX):
				baseName, timeStamp, extension = TFIL.splitFileName(fileName)
				if extension != 'gpx': continue
				if baseName == lastBaseName and timeStamp <= lastTimeStamp: continue									# Keep only most recent version
				lastBaseName = baseName; lastTimeStamp = timeStamp
				fileGPXLocalDico[' - '.join(baseName.split(' - ')[1:])] = timeStamp[0:10]
		else:
			self.mainFrame.setStatusWarning('Répertoire GPX Local (encore) inexistant !')	

#		Rechercher les informations locales (Y) concernant le Cahier des MAJ

		cahierMAJLocalPath = TQCP.retrieveQCartoParameter(self.mainFrame, 'MAJ', 'Path', 'Local', 'XXX')
		cahierMAJName = TQCP.retrieveQCartoParameter(self.mainFrame, 'MAJ', 'NomCahier', TCOD.itineraryFromTrackCode(self.listTracksSelectedCodes[0]))

		if 'Tome' in self.itinerarySelectCombo.currentText() :									# For special cases of Parcours in several tomes
			try:
				tome = int(self.itinerarySelectCombo.currentText()[-1])
				cahierMAJName = cahierMAJName.split(' // ')[tome - 1]
			except:
				cahierMAJName = None

		if cahierMAJName != None :
			cahierMAJDateLocal =  'Non trouvé'
			if os.path.isdir(cahierMAJLocalPath): 	
				for fileName in os.listdir(cahierMAJLocalPath):
					if fileName[-4:] != '.pdf' : continue
					if fileName[0:len(cahierMAJName)] != cahierMAJName : continue
					cahierMAJDateLocal = fileName[-14:-4]
					break
		else:
			cahierMAJName = '--- Nom défini ---'
			cahierMAJDateLocal = ' '

#		Rechercher la Date du cahier MAJ sur le Site SGR

		fileMAJSiteList = TSGR.readSiteSGRDirectory('MAJ')
		if fileMAJSiteList == None: self.mainFrame.setStatusWarning('Lecture du répertoire MAJ impossible sur le Site SGR !'); return
		fileMAJSiteDico = { file[:-15] : file[-14:-4] for file in fileMAJSiteList}
		if self.mainFrame.debugModeQCartoLevel >= 2 : 
			for entry in sorted(fileMAJSiteDico) :
				print('fileMAJSiteDico : ' + entry + ' = <<<' + fileMAJSiteDico[entry] + '>>>')

#		Remplissage de la table

		tableFields = QGP.htmlTracksTableQView
		self.allTracksHaveUrlValidDate = True
		for row in range(self.groupBoxHtmlTracksTable.rowCount()): 
			if row == 0 :																								# Line 0 is for cahier MAJ
				trackCode = 'Cahier MAJ'
				trackName = cahierMAJName
				trackStatus = ' '
				nameGPX = ' '
				dateGPXSite = fileMAJSiteDico[cahierMAJName] if cahierMAJName in fileMAJSiteDico else 'Non trouvé'
				dateGPXLocal = cahierMAJDateLocal
				dateUrl = dateGPXLocal if TDAT.isTimeStampToday(dateGPXLocal) else (dateGPXSite if dateGPXSite != 'Non trouvé' else 'AAAA-MM-JJ')
			else :
				trackCode = self.sortedListTracksCodesForHtml[row - 1]
				trackName = self.dicoTracksViewFeatures[trackCode][QGP.tableTracksFieldName]
				trackStatus = self.dicoTracksViewFeatures[trackCode][QGP.tableTracksFieldStatus]
				nameGPX = TGPX.defineTrackNameGPX(trackCode, trackName, True)	
				dateGPXSite = fileGPXSiteDico[nameGPX] if nameGPX in fileGPXSiteDico else 'Non trouvé'
				dateGPXLocal = fileGPXLocalDico[trackName] if trackName in fileGPXLocalDico else 'Non trouvé'
				dateUrl = dateGPXLocal if TDAT.isTimeStampToday(dateGPXLocal) else (dateGPXSite if dateGPXSite != 'Non trouvé' else 'AAAA-MM-JJ')
				if dateUrl == 'AAAA-MM-JJ' : self.allTracksHaveUrlValidDate = False
			
			for col in range(len(tableFields)):
				values = [ trackCode, trackName, trackStatus, nameGPX, dateGPXLocal, dateGPXSite, dateUrl ]
				item = self.createItem(values[col], 'Text')
				self.groupBoxHtmlTracksTable.setItem(row, col, item)
			
#		Color table

		for row in range(self.groupBoxHtmlTracksTable.rowCount()): 
			if TDAT.isTimeStampToday(self.groupBoxHtmlTracksTable.item(row, QGP.C_htmlTracksTableQView_ColDateLocal).text()):
				self.groupBoxHtmlTracksTable.item(row, QGP.C_htmlTracksTableQView_ColDateLocal).setBackground(DCOL.bgTableTodayStrong)
				self.groupBoxHtmlTracksTable.item(row, QGP.C_htmlTracksTableQView_ColDateUrl).setBackground(DCOL.bgTableTodayStrong)
			elif self.groupBoxHtmlTracksTable.item(row, QGP.C_htmlTracksTableQView_ColDateSite).text() != 'Non trouvé':
				self.groupBoxHtmlTracksTable.item(row, QGP.C_htmlTracksTableQView_ColDateSite).setBackground(DCOL.bgTableOk)
				self.groupBoxHtmlTracksTable.item(row, QGP.C_htmlTracksTableQView_ColDateUrl).setBackground(DCOL.bgTableOk)
			else:
				self.groupBoxHtmlTracksTable.item(row, QGP.C_htmlTracksTableQView_ColCode).setBackground(DCOL.bgTableError)
				self.groupBoxHtmlTracksTable.item(row, QGP.C_htmlTracksTableQView_ColName).setBackground(DCOL.bgTableError)
				self.groupBoxHtmlTracksTable.item(row, QGP.C_htmlTracksTableQView_ColDateUrl).setBackground(DCOL.bgTableError)
	
	
	def exportTracksHtml(self):
	
#	Timestamp	
	
		timeStamp = TDAT.getTimeStamp()
		timeStampHtml = ' (' + timeStamp + ')'

#	Prefix

		prefixHtml = DTOP.prefixHtml + ' - '
	
#	Déterminer le projet

		if len(self.sortedListTracksCodesForHtml) == 0: self.mainFrame.setStatusWarning('La liste des parcours est vide !'); return
		projectCode = TCOD.projectFromTrackCode(self.sortedListTracksCodesForHtml[0])		
	
#	Déterminer le path et le nom du fichier

		pathHtml = QGP.configPathExportGPX.replace('%PROJECT%', projectCode)					# Same as for GPX files 
		TFIL.ensure_dir(pathHtml)		
		fileHtml = prefixHtml + projectCode + ' - ' + 'Code Html pour Site SGR' + timeStampHtml + '.html'

#	Ecrire le fichier

		fileOut = open(pathHtml + fileHtml, 'w', encoding='utf-8', errors='ignore')


		for line in QGP.configSiteGPXHtmlHeaderLines: 											# Header
			line = line.replace('%GR%', projectCode)
			fileOut.write(line + '\n')	

		for row in range(self.groupBoxHtmlTracksTable.rowCount()): 
			if row == 0 : continue																# Skip Cahier MAJ now
			trackCode = self.groupBoxHtmlTracksTable.item(row, QGP.C_htmlTracksTableQView_ColCode).text()
			trackName = self.groupBoxHtmlTracksTable.item(row, QGP.C_htmlTracksTableQView_ColName).text()
			nameGPX = self.groupBoxHtmlTracksTable.item(row, QGP.C_htmlTracksTableQView_ColNameGPX).text()	
			dateLocal = self.groupBoxHtmlTracksTable.item(row, QGP.C_htmlTracksTableQView_ColDateLocal).text()	
			dateUrl = self.groupBoxHtmlTracksTable.item(row, QGP.C_htmlTracksTableQView_ColDateUrl).text()	
			distance = self.dicoTracksGRRBFeatures[trackCode][QGP.tableTracksFieldDistance]
			for line in QGP.configSiteGPXHtmlTrackLines: 
				url = QGP.configSiteGPXHtmlUrl + nameGPX + '_' + self.groupBoxHtmlTracksTable.item(row, QGP.C_htmlTracksTableQView_ColDateUrl).text() + '.gpx'
				line = line.replace('%URL%', url)
				line = line.replace('%NAME%', trackName)
				line = line.replace('%DATE%', dateUrl)
				line = line.replace('%DIST%', '{:,.1f} km'.format(distance/1000).replace('.',',') if distance != None else ' ')
				fileOut.write(line + '\n')	
		
		for line in QGP.configSiteGPXHtmlFooterLines: 											# Footer
			fileOut.write(line + '\n')	
		
		cahierMAJName = self.groupBoxHtmlTracksTable.item(0, QGP.C_htmlTracksTableQView_ColName).text()
		cahierNoteSite = TQCP.retrieveQCartoParameter(self.mainFrame, 'MAJ', 'NoteSite', projectCode, ' ')
		cahierDate = self.groupBoxHtmlTracksTable.item(0, QGP.C_htmlTracksTableQView_ColDateUrl).text()
		cahierDateLongue = cahierDate[-2:] + ' ' + ['janvier', 'février', 'mars', 'avril', 'mai', 'juin', 'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre'][int(cahierDate[5:7])-1] + ' ' + cahierDate[0:4]

		for line in QGP.configSiteMAJHtmlLines: 												# Cahier MAJ
			url = QGP.configSiteMAJHtmlUrl + cahierMAJName + '_' + cahierDate + '.pdf'
			line = line.replace('%URL%', url)
			line = line.replace('%GR%', projectCode)
			line = line.replace('%DATEL%', cahierDateLongue)
			line = line.replace('%NOTE%', cahierNoteSite)
			fileOut.write(line + '\n')	
			
		fileOut.close()
	
#	Afficher le résultat

		if self.allTracksHaveUrlValidDate:
			self.mainFrame.setStatusDone('Le fichier ' + fileHtml + ' a été généré !')
		else:
			self.mainFrame.setStatusWarning('Le fichier ' + fileHtml + ' a été généré avec Url incomplètes !')
	
	
# ========================================================================================
# Export des Parcours - CSV
# ========================================================================================
	
	def exportTracksCSV(self):

		if not self.controlTrackComputed() : return
		
# 	Create Progress Bar 

		progressBar = TPRO.createProgressBar(self.buttonExportCSV, len(self.listTracksSelectedCodes), 'Normal')

# 	Même timestamp pour tous les exports

		timeStamp = TDAT.getTimeStamp()
		timeStampCSV = ' (' + timeStamp + ')'

#	Exporter les parcours correctement calculés

		exportedCount = notExportedCount = 0

		for codeExported in self.listTracksSelectedCodes:

			self.mainFrame.setStatusWorking('Export CSV du parcours : ' + codeExported + ' - ' + self.dicoTracksViewFeatures[codeExported][QGP.tableTracksFieldName])

#			Eviter les parcours incorrectement calculés			

			if self.dicoTracksComputeResults[codeExported][QGP.tableTracksIFieldErrorCode] != 0: 
				notExportedCount += 1
				progressBar.setValue(progressBar.value() + 1)
				continue

#			Retrouver l'entité de base

			if self.typeSelected in QGP.typeSetTableGR : trackFeature = self.mainFrame.dicoTracksGRFeatures[codeExported]
			if self.typeSelected in QGP.typeSetTableRB : trackFeature = self.mainFrame.dicoTracksRBFeatures[codeExported]

#			Déterminer le path et le nom des fichiers
			
			projectCode = TCOD.projectFromTrackCode(codeExported)
			trackName = self.dicoTracksViewFeatures[codeExported][QGP.tableTracksFieldName]

			pathCSV = QGP.configPathExportCSV.replace('%PROJECT%', projectCode)
			fileCSV = TFIL.cleanFileName(codeExported + ' = ' + trackName)
			fileCSV += timeStampCSV
			fileCSV += '.csv'

#			Déterminer les repères à inclure dans le csv

			pointList = self.dicoTracksComputeResults[codeExported][QGP.tableTracksIFieldReperesPos]

#			Export CSV pour Excel

			trackXYZ = self.dicoTracksComputeResults[codeExported][QGP.tableTracksIFieldTrackXYZ]
			TCSV.exportCsvTrack(pathCSV, fileCSV, trackXYZ, pointList)

#			Exporter le CSV distances parcours GR

			self.distancesTrackPathCSV = None

			if codeExported in self.dicoGRTrackDistances and self.dicoGRTrackDistances[codeExported] != {}:
				itineraryGR = TCOD.itineraryFromTrackCode(codeExported)
				projectCode = TCOD.projectFromTrackCode(itineraryGR)
				self.mainFrame.setStatusWorking(itineraryGR + ' - Export des valeurs du parcours GR.P.T ...')
				pathCSV = QGP.configPathExportPlansValues.replace('%PROJECT%', projectCode)
				fileCSV = QGP.configFileExportGRTrackValues
				fileCSV = fileCSV.replace('%PREFIX%', DTOP.prefixPlanValues)
				fileCSV = fileCSV.replace('%TRACK%', codeExported)
				fileCSV = fileCSV.replace('%TIME%', timeStamp)
				fileCSV = TFIL.cleanFileName(fileCSV)
				self.distancesTrackPathCSV = pathCSV + fileCSV																# Remember for right click
				TCSV.exportCsvGRTrackDistances(pathCSV, fileCSV, self.dicoGRTrackDistances[codeExported])

#			Afficher l'avancement

			progressBar.setValue(progressBar.value() + 1)
			QgsApplication.processEvents()
			exportedCount += 1

#	Exporter les Distances Itinéraire si Possible

		self.distancesItineraryPathCSV = None

		if self.dicoItineraryDistances != {}:
			itinerary = TCOD.itineraryFromTrackCode(sorted(self.dicoItineraryDistances)[0])
			projectCode = TCOD.projectFromTrackCode(itinerary)
			self.mainFrame.setStatusWorking(itinerary + ' - Export des valeurs de l\'itinéraire GR.P.T ...')
			pathCSV = QGP.configPathExportPlansValues.replace('%PROJECT%', projectCode)
			fileCSV = QGP.configFileExportGRItineraryValues
			fileCSV = fileCSV.replace('%PREFIX%', DTOP.prefixPlanValues)
			fileCSV = fileCSV.replace('%ITI%', projectCode)																	# Use project needed for RB because several RB at a time
			fileCSV = fileCSV.replace('%TIME%', timeStamp)
			fileCSV = TFIL.cleanFileName(fileCSV)
			self.distancesItineraryPathCSV = pathCSV + fileCSV																# Remember for right click
			TCSV.exportCsvGRItineraryDistances(pathCSV, fileCSV, self.dicoItineraryDistances)

#	Exporter le Plan si possible

		if self.dicoRBPlanDistances != {}:
			itineraryRB = TCOD.itineraryFromTrackCode(sorted(self.dicoRBPlanDistances)[0])
			projectCode = TCOD.projectFromTrackCode(itineraryRB)
			trackName = self.mainFrame.dicoTracksRBFeatures[itineraryRB][QGP.tableTracksFieldName]
			if trackName.split(' - ')[0] == itineraryRB : trackName = trackName[len(itineraryRB) + len(' - '):]				
			self.mainFrame.setStatusWorking(itineraryRB + ' - Export des valeurs pour maquetistes ...')
			pathCSV = QGP.configPathExportPlansValues.replace('%PROJECT%', projectCode)
			fileCSV = QGP.configFileExportPlansValues
			fileCSV = fileCSV.replace('%PREFIX%', DTOP.prefixPlanValues)
			fileCSV = fileCSV.replace('%ITI%', itineraryRB)
			fileCSV = fileCSV.replace('%NAME%', trackName)
			fileCSV = fileCSV.replace('%TIME%', timeStamp)
			fileCSV = TFIL.cleanFileName(fileCSV)
			self.distancesItineraryPathCSV = pathCSV + fileCSV																# Remember for right click
			TCSV.exportCsvPlan(pathCSV, fileCSV, self.dicoRBPlanDistances, self.dicoRBPlanTracksList)

#	Afficher le status final

		if notExportedCount == 0:
			self.mainFrame.setStatusDone(str(exportedCount) + ' parcour.s exporté.s !')
		else:
			self.mainFrame.setStatusWarning(str(exportedCount) + ' parcour.s exporté.s - ' + str(notExportedCount) + ' parcour.s incorrect.s')
			del progressBar


	def showDistanceCSV(self):
		if self.distancesItineraryPathCSV != None:																			# Try first Itinéraire / RB
			THEL.viewCsvOnBrowser(self.mainFrame, 'Fichier source local sur ' + QGP.configPathProject, self.distancesItineraryPathCSV)
			self.mainFrame.setStatusInfo('Votre navigateur montre le contenu du fichiers CSV des distances de l\'itinéraire')

		if self.distancesTrackPathCSV != None:
			THEL.viewCsvOnBrowser(self.mainFrame, 'Fichier source local sur ' + QGP.configPathProject, self.distancesTrackPathCSV)
			self.mainFrame.setStatusInfo('Votre navigateur montre le contenu du fichiers CSV des distances du parcours')
			return


# ========================================================================================
# Export des Parcours - Infos parcours
# ========================================================================================
	
	def exportTracksInfos(self):
	
		if not self.controlTrackComputed() : return

#	Dictionnaire des Communes si pas encore créé

		if self.dicoCommunes == None:
			if self.layerCommunes == None:
				self.mainFrame.setStatusError(self.layerCommunesError, False)
				return
			
		self.dicoCommunes = {f[QGP.configCommuneFieldName] : f for f in self.layerCommunes.getFeatures()}
		self.dicoTracksCommunes = {}
		self.mainFrame.setStatusWorking('Dictionnaire des Communes : ' + str(len(self.dicoCommunes)) + ' communes')

# 	Create Progress Bar 

		progressBar = TPRO.createProgressBar(self.buttonExportCSV, len(self.listTracksSelectedCodes), 'Normal')

# 	Même timestamp pour tous les exports

		timeStamp = TDAT.getTimeStamp()
		timeStampCSV = ' (' + timeStamp + ')'

#	Exporter les parcours correctement calculés

		exportedCount = notExportedCount = 0

		for codeExported in self.listTracksSelectedCodes:

			self.mainFrame.setStatusWorking('Export CSV Info du parcours : ' + codeExported + ' - ' + self.dicoTracksViewFeatures[codeExported][QGP.tableTracksFieldName])

#			Eviter les parcours incorrectement calculés			

			if self.dicoTracksComputeResults[codeExported][QGP.tableTracksIFieldErrorCode] != 0: 
				notExportedCount += 1
				progressBar.setValue(progressBar.value() + 1)
				continue

#			Retrouver l'entité de base

			if self.typeSelected in QGP.typeSetTableGR : trackFeature = self.mainFrame.dicoTracksGRFeatures[codeExported]
			if self.typeSelected in QGP.typeSetTableRB : trackFeature = self.mainFrame.dicoTracksRBFeatures[codeExported]

#			Déterminer le path et le nom des fichiers
			
			projectCode = TCOD.projectFromTrackCode(codeExported)
			trackName = self.dicoTracksViewFeatures[codeExported][QGP.tableTracksFieldName]

			pathCSV = QGP.configPathExportCSVInfos.replace('%PROJECT%', projectCode)
			fileCSV = TFIL.cleanFileName(trackName)
			fileCSV += timeStampCSV
			fileCSV += '.csv'

#			Export CSV Infos

			self.dicoTracksCommunes[codeExported] = TCSV.exportCsvTrackInfos(self.mainFrame, self, pathCSV, fileCSV, codeExported)

#			Afficher l'avancement

			progressBar.setValue(progressBar.value() + 1)
			QgsApplication.processEvents()
			exportedCount += 1

#	Exporter la liste globale des communes par parcours

		self.exportCommunesInfos(projectCode, timeStampCSV)

#	Afficher le status final

		if notExportedCount == 0:
			self.mainFrame.setStatusDone(str(exportedCount) + ' parcour.s exporté.s !')
		else:
			self.mainFrame.setStatusWarning(str(exportedCount) + ' parcour.s exporté.s - ' + str(notExportedCount) + ' parcour.s incorrect.s')
			del progressBar


	def exportCommunesInfos(self, projectCode, timeStamp):
		pathCSV = QGP.configPathExportCSVInfos.replace('%PROJECT%', projectCode)
		fileTXT = TFIL.cleanFileName(projectCode + ' - Communes traversés')
		fileTXT += timeStamp
		fileTXT += '.txt'	
		newLine = QGP.configCSVNewLine

		TFIL.ensure_dir(pathCSV)
		fileOut = open(pathCSV + fileTXT, 'w', encoding='utf-8', errors='ignore')

		for codeExported in self.dicoTracksCommunes:
			fileOut.write(codeExported + ' - ' + self.dicoTracksViewFeatures[codeExported][QGP.tableTracksFieldName] + ' = ' + ', '.join(c for c in sorted(self.dicoTracksCommunes[codeExported])) + newLine)
		
		fileOut.close()

	
# ========================================================================================

	def controlTrackComputed(self):

#	Check if at least 1 tracks is selected		
		
		if len(self.listTracksSelectedCodes) == 0:																
			self.mainFrame.setStatusWarning('Vous devez sélectionner au moins un parcours dans la table !')
			return False
		
#	Check that selected tracks have effectively been computed	
		
		if sum([1 for code in self.listTracksSelectedCodes if code not in self.dicoTracksComputeResults]) > 0:
			self.mainFrame.setStatusWarning('Vous n\'avez pas calculé tous les parcours sélectionnés dans la table !')
			return False
			
		return True
		
	
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

		buttonRadioGR.clicked.connect(self.buttonRadioGR_clicked)
		buttonRadioGRP.clicked.connect(self.buttonRadioGRP_clicked)
		buttonRadioGRT.clicked.connect(self.buttonRadioGRT_clicked)
		buttonRadioRI.clicked.connect(self.buttonRadioRI_clicked)
		buttonRadioRL.clicked.connect(self.buttonRadioRL_clicked)
		buttonRadioRB.clicked.connect(self.buttonRadioRB_clicked)
		buttonRadioRF.clicked.connect(self.buttonRadioRF_clicked)
		buttonRadioIR.clicked.connect(self.buttonRadioIR_clicked)
		
#	Créer un menu déroulant pour le choix de l'itinéraire et la sélection

		TBUT.createLabelBlackButton(groupBoxItinerary, 1, 2, 'Choix Itinéraire', 'Normal', 'Normal')
		self.itineraryCombo = TBUT.createComboButton(groupBoxItinerary, 2, 2, 'Normal')

		self.itinerarySelectCombo = TBUT.createComboButton(groupBoxItinerary, 3, 2, 'Normal')
		self.itinerarySelectCombo.addItem('Tous')
		self.itinerarySelectCombo.addItem('Unité')
		self.itinerarySelectCombo.addItem('Tome 1')									# Warning : word Tome is used below 
		self.itinerarySelectCombo.addItem('Tome 2')									# Warning : word Tome is used below 
		self.itinerarySelectCombo.addItem('Tome 3')									# Warning : word Tome is used below 

		self.itineraryNumeroCombo = TBUT.createComboButton(groupBoxItinerary, 4, 2, 'Normal')
		self.itineraryNumeroCombo.addItem('')
		for i in range(48): self.itineraryNumeroCombo.addItem('Rando {:02d}'.format(i+1))
		
#	Créer le bouton d'action		

		buttonShow = TBUT.createActionButton(groupBoxItinerary, 6, 2, 'Afficher !', 'Normal')
		buttonShow.clicked.connect(self.createTracksView)		
		
		buttonShow.setContextMenuPolicy(Qt.CustomContextMenu)
		buttonShow.customContextMenuRequested.connect(self.selectAllTracks)
			
# 	Terminé

		groupBoxItinerary.repaint()

		return groupBoxItinerary


# ========================================================================================
# Cadre : Points Repères
# ========================================================================================

	def menuBoxLandmarks(self):
	
		groupBoxLandmarks = QtWidgets.QGroupBox('Points Repères', self.mainMenu)
		groupBoxLandmarks.setStyleSheet(DSTY.styleBox)

		TBUT.createLabelBlackButton(groupBoxLandmarks, 1, 1, 'Repères trouvés', 'Normal', 'Normal')

#	Créer le décompte des Points

		self.pointCountInfo = TBUT.createLabelGreenButton(groupBoxLandmarks, 2, 1, '. . .', 'Normal', 'Normal')
		DSTY.setStyleWarningLabel(self.pointCountInfo, "Normal")

#	Créer les boutons d'actions

		buttonSelect = TBUT.createActionButton(groupBoxLandmarks, 1, 2, 'Sélectionner', 'Normal')
		buttonSelect.clicked.connect(self.selectPointsViewed)		

		buttonSelect.setContextMenuPolicy(Qt.CustomContextMenu)
		buttonSelect.customContextMenuRequested.connect(self.zoomPointsSelected)

		self.buttonRefreshPoints = TBUT.createActionButton(groupBoxLandmarks, 2, 2, 'Recharger', 'Normal')
		DSTY.setStyleMainButtonsInactive(self.buttonRefreshPoints)
		self.buttonRefreshPoints.clicked.connect(self.createPointsView)		

# 	Terminé

		groupBoxLandmarks.repaint()

		return groupBoxLandmarks


# ========================================================================================
# Cadre : Parcours GR / RB
# ========================================================================================

	def menuBoxTracks(self):
	
		groupBoxTracks = QtWidgets.QGroupBox('Parcours GR / RB', self.mainMenu)
		groupBoxTracks.setStyleSheet(DSTY.styleBox)
		
#	Créer les 2 boutons d'actions		

		buttonSelect = TBUT.createActionButton(groupBoxTracks, 1, 1, 'Sélectionner', 'Normal')
		buttonSelect.clicked.connect(self.selectTracksViewed)		

		buttonSelect.setContextMenuPolicy(Qt.CustomContextMenu)
		buttonSelect.customContextMenuRequested.connect(self.zoomTracksSelected)

		self.buttonRefreshTracks = TBUT.createActionButton(groupBoxTracks, 1, 2, 'Recharger', 'Normal')
		self.buttonRefreshTracks.clicked.connect(self.analyseTablesTracks)		
		
# 	Terminé

		groupBoxTracks.repaint()

		return groupBoxTracks


# ========================================================================================
# Cadre : Tronçons GR
# ========================================================================================

	def menuBoxSections(self):
	
		groupBoxSections = QtWidgets.QGroupBox('Tronçons GR', self.mainMenu)
		groupBoxSections.setStyleSheet(DSTY.styleBox)

#	Créer le décompte Global des Sections

		self.sectionCountInfo = TBUT.createLabelGreenButton(groupBoxSections, 1, 1, '. . .', 'Normal', 'Normal')
		DSTY.setStyleWarningLabel(self.pointCountInfo, "Normal")

#	Créer le bouton de rechargement global

		self.buttonRefreshSections = TBUT.createActionButton(groupBoxSections, 1, 2, 'Recharger', 'Normal')
		self.buttonRefreshSections.clicked.connect(self.reloadSections)		

# 	Terminé

		groupBoxSections.repaint()

		return groupBoxSections


# ========================================================================================
# Cadre : Modifications
# ========================================================================================

	def menuBoxModifications(self):

		groupBoxModifications = QtWidgets.QGroupBox('Gestion des Modifications', self.mainMenu)
		groupBoxModifications.setStyleSheet(DSTY.styleBox)

#	Créer les boutons d'action		

		self.buttonAddTrackTemporary = TBUT.createActionButton(groupBoxModifications, 1, 1, '+ Parcours -MT', 'Normal')
		self.buttonAddTrackTemporary.clicked.connect(self.modificationAddTrackTemporary)

		self.buttonRemoveTrackTemporary = TBUT.createActionButton(groupBoxModifications, 1, 2, 'x Parcours -MT', 'Normal')
		self.buttonRemoveTrackTemporary.clicked.connect(self.modificationRemoveTrackTemporary)

		self.buttonAddTrackFuture = TBUT.createActionButton(groupBoxModifications, 2, 1, '+ Parcours -MF', 'Normal')
		self.buttonAddTrackFuture.clicked.connect(self.modificationAddTrackFuture)

		self.buttonRemoveTrackFuture = TBUT.createActionButton(groupBoxModifications, 2, 2, 'x Parcours -MF', 'Normal')
		self.buttonRemoveTrackFuture.clicked.connect(self.modificationRemoveTrackFuture)

		groupBoxModifications.repaint()

		return groupBoxModifications


# ========================================================================================
# Cadre : Options
# ========================================================================================

	def menuBoxOptions(self):

		groupBoxOptions = QtWidgets.QGroupBox('Options', self.mainMenu)
		groupBoxOptions.setStyleSheet(DSTY.styleBox)

#	Créer les cases options à cocher

		self.optionComputeDelta = TBUT.createCheckBoxButton(groupBoxOptions, 1, 1, 'Calcul Delta', 'Normal')
		self.optionComputeDelta.setCheckState(Qt.Checked)

		self.optionCompatibilityGPX = TBUT.createCheckBoxButton(groupBoxOptions, 1, 2, 'GPX à jour', 'Normal')
		self.optionCompatibilityGPX.setCheckState(Qt.Unchecked)

		self.optionDeleteOldGPX = TBUT.createCheckBoxButton(groupBoxOptions, 1, 3, 'X anciens GPX', 'Normal')
		self.optionDeleteOldGPX.setCheckState(Qt.Checked)

		self.optionIncludeWPInGPX = TBUT.createCheckBoxButton(groupBoxOptions, 1, 4, 'Repères > GPX', 'Normal')
		self.optionIncludeWPInGPX.setCheckState(Qt.Checked)

		self.optionComboPOIsInGPX = TBUT.createComboButton(groupBoxOptions, 1, 5, 'Normal')
		for text in (QGP.poisComboList if self.layerPOIs != None else [QGP.C_poisComboTextNoPOIs]) : self.optionComboPOIsInGPX.addItem(text)

		groupBoxOptions.repaint()

		return groupBoxOptions


# ========================================================================================
# Cadre : Actions
# ========================================================================================

	def menuBoxActions(self):

		groupBoxActions = QtWidgets.QGroupBox('Actions', self.mainMenu)
		groupBoxActions.setStyleSheet(DSTY.styleBox)

#	Créer les boutons d'action		

		self.buttonCompute = TBUT.createActionButton(groupBoxActions, 1, 1, 'Calculer', 'Normal')
		self.buttonCompute.clicked.connect(self.computeTracks)

		self.buttonRecord = TBUT.createActionButton(groupBoxActions, 1, 2, 'Enregistrer', 'Normal')
		self.buttonRecord.clicked.connect(self.recordTracks)
		self.buttonRecord.setContextMenuPolicy(Qt.CustomContextMenu)
		self.buttonRecord.customContextMenuRequested.connect(self.recordTracksForced)		

		self.buttonExportGPX = TBUT.createActionButton(groupBoxActions, 1, 3, 'Exporter GPX', 'Normal')
		self.buttonExportGPX.clicked.connect(self.exportTracksGPX)
		self.buttonExportGPX.setContextMenuPolicy(Qt.CustomContextMenu)
		self.buttonExportGPX.customContextMenuRequested.connect(lambda _ : self.toggleGPXHtml('Html'))

		self.buttonExportHtml = TBUT.createActionButton(groupBoxActions, 1, 3, 'Exporter Html', 'Normal')
		self.buttonExportHtml.clicked.connect(self.exportTracksHtml)
		self.buttonExportHtml.setContextMenuPolicy(Qt.CustomContextMenu)
		self.buttonExportHtml.customContextMenuRequested.connect(lambda _ : self.toggleGPXHtml('GPX'))
		self.buttonExportHtml.hide()

		self.buttonExportCSV = TBUT.createActionButton(groupBoxActions, 1, 4, 'Exporter CSV', 'Normal')
		self.buttonExportCSV.clicked.connect(self.exportTracksCSV)
		self.buttonExportCSV.setContextMenuPolicy(Qt.CustomContextMenu)
		self.buttonExportCSV.customContextMenuRequested.connect(self.showDistanceCSV)

		self.buttonExportInfos = TBUT.createActionButton(groupBoxActions, 1, 5, 'Exporter Infos', 'Normal')
		self.buttonExportInfos.clicked.connect(self.exportTracksInfos)

		groupBoxActions.repaint()

		return groupBoxActions

	def toggleGPXHtml(self, mode):
		if mode == 'Html':
			if self.typeSelected not in QGP.typeSetTableGR :	return	
			self.buttonExportGPX.hide()
			self.buttonExportHtml.show()
			self.groupBoxTracksTable.hide()
			self.groupBoxHtmlTracksTable.show()
			self.initializeTracksHtmlTable()
			return
		if mode == 'GPX':
			self.buttonExportGPX.show()
			self.buttonExportHtml.hide()
			self.groupBoxTracksTable.show()
			self.groupBoxHtmlTracksTable.hide()
			return


# ========================================================================================
# Cadre : Cadre de la Table des Parcours
# ========================================================================================

	def menuBoxTableTracksFrame(self):
	
		groupBoxTracksFrame = QtWidgets.QGroupBox('Table des Parcours', self.mainMenu)
		groupBoxTracksFrame.setStyleSheet(DSTY.styleBox)

		groupBoxTracksFrame.repaint()

		return groupBoxTracksFrame


# ========================================================================================
# Cadre : Table des Parcours
# ========================================================================================

	def menuBoxTableTracksView(self):

		groupBoxTracksView = QtWidgets.QTableWidget(0,len(QGP.tracksTableQView), self.mainMenu)
		groupBoxTracksView.setStyleSheet(DSTY.styleBox)

		DSTY.setStyleTableTraces(groupBoxTracksView)

		tableFields = QGP.tracksTableQView
		for col in range(len(tableFields)):
			groupBoxTracksView.setHorizontalHeaderItem(col, QtWidgets.QTableWidgetItem(tableFields[col][0]))
			groupBoxTracksView.setColumnWidth(col, tableFields[col][1])

		groupBoxTracksView.itemSelectionChanged.connect(self.getSelectedTracksCodes)
		groupBoxTracksView.itemClicked.connect(self.trackTable_itemClicked)

		groupBoxTracksView.setContextMenuPolicy(Qt.CustomContextMenu)
		groupBoxTracksView.customContextMenuRequested.connect(self.trackTable_itemRightClicked)
		groupBoxTracksView.itemDoubleClicked.connect(self.trackTable_itemDoubleClicked)
		
		groupBoxTracksView.repaint()

		return groupBoxTracksView
	
	
# ========================================================================================
# Cadre : Table des Repères sur le Parcours
# ========================================================================================
	
	def menuBoxTablePointsView(self):

		groupBoxPointsView = QtWidgets.QTableWidget(0,len(QGP.pointsTableQView), self.mainMenu)
		groupBoxPointsView.setStyleSheet(DSTY.styleBox)

		DSTY.setStyleTableTraces(groupBoxPointsView)

		tableFields = QGP.pointsTableQView
		for col in range(len(tableFields)):
			groupBoxPointsView.setHorizontalHeaderItem(col, QtWidgets.QTableWidgetItem(tableFields[col][0]))
			groupBoxPointsView.setColumnWidth(col, tableFields[col][1])

		groupBoxPointsView.itemClicked.connect(self.trackPointTable_itemClicked)

		groupBoxPointsView.setContextMenuPolicy(Qt.CustomContextMenu)
		groupBoxPointsView.customContextMenuRequested.connect(self.trackPointTable_itemRightClicked)
		groupBoxPointsView.itemDoubleClicked.connect(self.trackPointTable_itemDoubleClicked)

		groupBoxPointsView.repaint()

		return groupBoxPointsView	
	
	
# ========================================================================================
# Cadre : Table des Sections sur le Parcours
# ========================================================================================
	
	def menuBoxTableSectionsView(self):

		groupBoxSectionsView = QtWidgets.QTableWidget(0,len(QGP.sectionsTableQView), self.mainMenu)
		groupBoxSectionsView.setStyleSheet(DSTY.styleBox)

		DSTY.setStyleTableTraces(groupBoxSectionsView)

		tableFields = QGP.sectionsTableQView
		for col in range(len(tableFields)):
			groupBoxSectionsView.setHorizontalHeaderItem(col, QtWidgets.QTableWidgetItem(tableFields[col][0]))
			groupBoxSectionsView.setColumnWidth(col, tableFields[col][1])

		groupBoxSectionsView.itemClicked.connect(self.trackSectionTable_itemClicked)

		groupBoxSectionsView.setContextMenuPolicy(Qt.CustomContextMenu)
		groupBoxSectionsView.customContextMenuRequested.connect(self.trackSectionTable_itemRightClicked)

		groupBoxSectionsView.repaint()

		return groupBoxSectionsView	
	
	
# ========================================================================================
# Cadre : Table des Pois sur le Parcours
# ========================================================================================
	
	def menuBoxTablePOIsView(self):

		groupBoxPOIsView = QtWidgets.QTableWidget(0,len(QGP.poisTableQView), self.mainMenu)
		groupBoxPOIsView.setStyleSheet(DSTY.styleBox)

		DSTY.setStyleTableTraces(groupBoxPOIsView)

		tableFields = QGP.poisTableQView
		for col in range(len(tableFields)):
			groupBoxPOIsView.setHorizontalHeaderItem(col, QtWidgets.QTableWidgetItem(tableFields[col][0]))
			groupBoxPOIsView.setColumnWidth(col, tableFields[col][1])

		groupBoxPOIsView.setContextMenuPolicy(Qt.CustomContextMenu)
		groupBoxPOIsView.customContextMenuRequested.connect(self.poisTable_itemRightClicked)

		groupBoxPOIsView.repaint()

		return groupBoxPOIsView	
	

# ========================================================================================
# Cadre : Table de l'historique du parcours
# ========================================================================================
	
	def menuBoxTableHistoricView(self):

		groupBoxHistoricView = QtWidgets.QTableWidget(0,len(QGP.historicTableQView), self.mainMenu)
		groupBoxHistoricView.setStyleSheet(DSTY.styleBox)

		DSTY.setStyleTableTraces(groupBoxHistoricView)

		tableFields = QGP.historicTableQView
		for col in range(len(tableFields)):
			groupBoxHistoricView.setHorizontalHeaderItem(col, QtWidgets.QTableWidgetItem(tableFields[col][0]))
			groupBoxHistoricView.setColumnWidth(col, tableFields[col][1])

		groupBoxHistoricView.repaint()

		return groupBoxHistoricView	
	
	
# ========================================================================================
# Cadre : Table des Parcours communs
# ========================================================================================
	
	def menuBoxTableCommonTracksView(self):

		groupBoxCommonTracksView = QtWidgets.QTableWidget(0,len(QGP.commonTracksTableQView), self.mainMenu)
		groupBoxCommonTracksView.setStyleSheet(DSTY.styleBox)

		DSTY.setStyleTableTraces(groupBoxCommonTracksView)

		tableFields = QGP.commonTracksTableQView
		for col in range(len(tableFields)):
			groupBoxCommonTracksView.setHorizontalHeaderItem(col, QtWidgets.QTableWidgetItem(tableFields[col][0]))
			groupBoxCommonTracksView.setColumnWidth(col, tableFields[col][1])

		groupBoxCommonTracksView.repaint()

		return groupBoxCommonTracksView	
	
	
# ========================================================================================
# Cadre : Table des Infos Html
# ========================================================================================
	
	def menuBoxTableHtmlTracksView(self):

		groupBoxHtmlTracksView = QtWidgets.QTableWidget(0,len(QGP.htmlTracksTableQView), self.mainMenu)
		groupBoxHtmlTracksView.setStyleSheet(DSTY.styleBox)

		DSTY.setStyleTableTraces(groupBoxHtmlTracksView)

		tableFields = QGP.htmlTracksTableQView
		for col in range(len(tableFields)):
			groupBoxHtmlTracksView.setHorizontalHeaderItem(col, QtWidgets.QTableWidgetItem(tableFields[col][0]))
			groupBoxHtmlTracksView.setColumnWidth(col, tableFields[col][1])

		groupBoxHtmlTracksView.repaint()

		return groupBoxHtmlTracksView	


# ========================================================================================
# --- THE END ---
# ========================================================================================
	