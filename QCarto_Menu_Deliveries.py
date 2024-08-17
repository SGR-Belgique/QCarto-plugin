# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Gestion des Menus : Page Livraisons
# ========================================================================================


# ========================================================================================
# Dictionnaires
#	self.dicoProductsList 			dict			product	: baseName : dico product
#		dicoProduct					dict				see below for dico entries
#	self.dicoProductTable			dict			row : dicoProduct
# ========================================================================================

C_dicoProduct_localPathX				= 'Local Path'
C_dicoProduct_localFileX				= 'Local File'
C_dicoProduct_localDateX				= 'Local Date'

C_dicoProduct_cartoPathY				= 'Carto Path'
C_dicoProduct_cartoFileY				= 'Carto File'
C_dicoProduct_cartoDateY				= 'Carto Date'

C_dicoProduct_infoCartoName				= 'Info Carto Name'
C_dicoProduct_infoTopoName				= 'Info Topo Name'
C_dicoProduct_infoCartoDate				= 'Info Carto Date'
C_dicoProduct_infoTopoDate				= 'Info Topo Date'

C_dicoProduct_topoPathZ					= 'Topo Path'
C_dicoProduct_topoFolderOpen			= 'Topo Folder Open'
C_dicoProduct_topoFileExist				= 'Topo File Exist'

C_TextTousItineraries	= 'Tous itinéraires'


# ========================================================================================
# Fichiers de Date de livraison KnoopPuntNet
# ========================================================================================

C_deltaPathFileDelivery 		= 'Dates Calcul Delta/'
C_extensionFileOsmDelta		 	= 'QOsmDelta'

C_kpnPathFileDelivery 			= 'Dates Livraisons Kpn/'
C_extensionFileDeliveryKpnDate 	= 'QOsmKpn'


# ========================================================================================
# Imports
# ========================================================================================

from PyQt5.QtCore import *
from PyQt5.QtGui import *

from qgis.core import *
from qgis.gui import *
from qgis.PyQt import QtWidgets

import os
import webbrowser
import subprocess
import importlib

import QCarto_Layers_Tracks as LTRK

import QCarto_Tools_Buttons as TBUT
import QCarto_Tools_Coding as TCOD
import QCarto_Tools_CSV as TCSV
importlib.reload(TCSV)
import QCarto_Tools_Dates as TDAT
importlib.reload(TDAT)
import QCarto_Tools_Files as TFIL
import QCarto_Tools_ImageFile as TIMG
importlib.reload(TIMG)
import QCarto_Tools_Input as TINP
importlib.reload(TINP)
import QCarto_Tools_Help as THEL
importlib.reload(THEL)
import QCarto_Tools_GPX as TGPX
importlib.reload(TGPX)
import QCarto_Tools_Geometries as TGEO
import QCarto_Tools_Log as TLOG
importlib.reload(TLOG)
import QCarto_Tools_Progress as TPRO
import QCarto_Tools_Rubberband as TRUB
import QCarto_Tools_SCR as TSCR

import QCarto_Definitions_Colors as DCOL
import QCarto_Definitions_Styles as DSTY
importlib.reload(DSTY)
import QCarto_Definitions_TopoGuides as DTOP	
importlib.reload(DTOP)

import QCarto_Process_DownloadOsm as SOSMD
importlib.reload(SOSMD)
import QCarto_Process_CreateOsm as SOSMC
importlib.reload(SOSMC)

import QCarto_Parameters_Global
importlib.reload(QCarto_Parameters_Global)
QGP = QCarto_Parameters_Global.globalParameters()


# ========================================================================================
# Constantes des colonnes de la table Osm
# ========================================================================================

CO_colTrackCode =  [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQViewOSM].index(QGP.tableProductsFieldTrackCode)  
CO_colTrackName =  [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQViewOSM].index(QGP.tableProductsFieldTrackName)  
CO_colOsmid =	   [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQViewOSM].index(QGP.tableProductsFieldTrackOsmid)	
CO_colStampDB =    [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQViewOSM].index(QGP.tableProductsFieldTrackDateDB)
CO_colStampCarto = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQViewOSM].index(QGP.tableProductsFieldTrackDateY)
CO_colStampOsm  =  [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQViewOSM].index(QGP.tableProductsFieldTrackDateOsm)
CO_colStampKpn  =  [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQViewOSM].index(QGP.tableProductsFieldTrackDateKpn)
CO_colStampRel  =  [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQViewOSM].index(QGP.tableProductsFieldTrackDateOsmRel)
CO_colDeltaCarto = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQViewOSM].index(QGP.tableProductsFieldTrackDeltaY)
CO_colDeltaOsm  =  [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQViewOSM].index(QGP.tableProductsFieldTrackDeltaOsm)
CO_colDeltaRel  =  [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQViewOSM].index(QGP.tableProductsFieldTrackDeltaOsmRel)
CO_colCheckOsm  =  [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQViewOSM].index(QGP.tableProductsFieldCopyOsm)


# ========================================================================================
# Class : menuDeliveriesFrame
# >>> iface
# >>> mainMenu 						: Widget of Main Menu
# >>> mainFrame 					: Main Menu Object
# ========================================================================================

class menuDeliveriesFrame:

	def __init__(self, iface, mainMenu, mainFrame):

# 	Paramètres fournis

		self.iface = iface
		self.mainMenu = mainMenu
		self.mainFrame = mainFrame

#	Nom de la page

		self.pageName = 'Livraisons'

#	Accès aux Tables de la DB Carto

		self.layerTracksGR, 	self.layerTracksGRerror 	= self.mainFrame.layerTracksGR, 	self.mainFrame.layerTracksGRerror 	
		self.layerTracksRB, 	self.layerTracksRBerror 	= self.mainFrame.layerTracksRB, 	self.mainFrame.layerTracksRBerror 	
		self.layerSectionsGR, 	self.layerSectionsGRerror 	= self.mainFrame.layerSectionsGR, 	self.mainFrame.layerSectionsGRerror 	
		self.layerPointsGR, 	self.layerPointsGRError 	= self.mainFrame.layerPointsGR, 	self.mainFrame.layerPointsGRError 	
		self.layerCommunes, 	self.layerCommunesError		= self.mainFrame.layerCommunes, 	self.mainFrame.layerCommunesError		

#	Dictionnaires Principaux 

		self.dicoTracksName2CodeGR = { self.mainFrame.dicoTracksGRFeatures[code][QGP.tableTracksFieldName] : code for code in self.mainFrame.dicoTracksGRFeatures }

#	Variables globales de la classe

		self.viewMode = None
		self.typeSelected = None
		self.projectList = []
		self.deliveryTopoActive = True
		self.deliveryCartoActive = True
		self.rubberBandGPX = TRUB.rubberBandGPX(self.iface)
		self.rubberBandLastFileName = None

# 	Création des sous-menus

		self.boxesList = []
		self.createMenuBoxes()
		self.changeProductTableHeaders('Topo')

		self.mainFrame.setStatusDone('Page des ' + self.pageName + ' créée !')
		
	def createMenuBoxes(self):

		self.groupBoxSelection = self.menuBoxSelection()
		DSTY.setBoxGeometry(self.groupBoxSelection, 1, 4, 8, 2)
		self.boxesList.append(self.groupBoxSelection)
		
		self.groupBoxProductsFrame = self.menuBoxTableProductsFrame()
		DSTY.setBoxGeometry(self.groupBoxProductsFrame, 1, 7, 8, 17)
		self.boxesList.append(self.groupBoxProductsFrame)		
		
		self.groupBoxProductsTable = self.menuBoxTableProductsView()
		DSTY.setBoxGeometry(self.groupBoxProductsTable, 1, 7, 8, 17, True)
		self.boxesList.append(self.groupBoxProductsTable)		
	
		self.groupBoxProductsOsmTable = self.menuBoxTableProductsOsmView()
		DSTY.setBoxGeometry(self.groupBoxProductsOsmTable, 1, 7, 8, 17, True)
		self.boxesList.append(self.groupBoxProductsOsmTable)	

		self.groupBoxDeliveryCarto = self.menuBoxTableDeliveryCarto()
		DSTY.setBoxGeometry(self.groupBoxDeliveryCarto, 1, 25, 4, 2)
		self.boxesList.append(self.groupBoxDeliveryCarto)			

		self.groupBoxDeliveryTopo = self.menuBoxTableDeliveryTopo()
		DSTY.setBoxGeometry(self.groupBoxDeliveryTopo, 5, 25, 4, 2)
		self.boxesList.append(self.groupBoxDeliveryTopo)			

		self.groupBoxRelationOsm = self.menuBoxRelationOsm()
		DSTY.setBoxGeometry(self.groupBoxRelationOsm, 1, 25, 4, 2)
		self.boxesList.append(self.groupBoxRelationOsm)



# ========================================================================================
# Actions : A la demande de la fenêtre principale
# ========================================================================================

#	Show - Ouverture de cette fenêtre

	def show(self):
		for box in self.boxesList: box.show(), box.repaint()
		self.changeProductTableHeaders()
		self.refreshItineraryLists()

#	Hide - Ouverture d'une autre fenêtre

	def hide(self):
		for box in self.boxesList: box.hide()
		self.rubberBandGPX.clearRubberBand()

#	Close - Fermeture définitive

	def close(self):
		self.hide()
		for box in self.boxesList: del box
		self.rubberBandGPX.clearRubberBand()
		self.rubberBandGPX.deleteRubberBand()

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


# ========================================================================================
# Actions : Choix du Type d'itinéraire
# ========================================================================================
	
	def buttonRadioGR_clicked(self):
		self.itineraryCombo.clear()
		self.itineraryCombo.addItem(C_TextTousItineraries)
		for code in self.listTracksGRCodes:
			self.itineraryCombo.addItem(code)
		self.typeSelected = 'GR'	
	
	def buttonRadioGRP_clicked(self):
		self.itineraryCombo.clear()
		self.itineraryCombo.addItem(C_TextTousItineraries)
		for code in self.listTracksGRPCodes:
			self.itineraryCombo.addItem(code)
		self.typeSelected = 'GRP'	
	
	def buttonRadioGRT_clicked(self):
		self.itineraryCombo.clear()
		self.itineraryCombo.addItem(C_TextTousItineraries)
		for code in self.listTracksGRTCodes:
			self.itineraryCombo.addItem(code)
		self.typeSelected = 'GRT'	

	def buttonRadioRI_clicked(self):
		self.itineraryCombo.clear()
		self.itineraryCombo.addItem(C_TextTousItineraries)
		for code in self.listTracksRICodes:
			self.itineraryCombo.addItem(code)
		self.typeSelected = 'RI'	

	def buttonRadioRL_clicked(self):
		self.itineraryCombo.clear()
		self.itineraryCombo.addItem(C_TextTousItineraries)
		for code in self.listTracksRLCodes:
			self.itineraryCombo.addItem(code)
		self.typeSelected = 'RL'	

	def buttonRadioRB_clicked(self):
		self.itineraryCombo.clear()
		self.itineraryCombo.addItem(C_TextTousItineraries)
		for code in self.listTracksRBCodes:
			self.itineraryCombo.addItem(code)
		self.typeSelected = 'RB'	

	def buttonRadioRF_clicked(self):
		self.itineraryCombo.clear()
		self.itineraryCombo.addItem(C_TextTousItineraries)
		for code in self.listTracksRFCodes:
			self.itineraryCombo.addItem(code)
		self.typeSelected = 'RF'	

	def buttonRadioIR_clicked(self):
		self.itineraryCombo.clear()
		self.itineraryCombo.addItem(C_TextTousItineraries)
		for code in self.listTracksIRCodes:
			self.itineraryCombo.addItem(code)
		self.typeSelected = 'IR'	

	
# ========================================================================================
# ========================================================================================
#
# Actions pour : Tous produits sauf GPX Osm
# 
# ========================================================================================
# ========================================================================================

	def productItem_changed(self, item):
		self.showDeliveryCartoCounts()
		self.showDeliveryTopoCounts()
	

# ========================================================================================
#	Déterminer la liste des projets en fonction du choix du type d'itinéraire
# ========================================================================================

	def retrieveProjetsList(self):
		if self.typeSelected == None:
			self.projectList = []
		if self.typeSelected == 'GR':
			self.projectList = self.listTracksGRCodes if self.itineraryCombo.currentText() == C_TextTousItineraries else [self.itineraryCombo.currentText()]
		if self.typeSelected == 'GRP':
			self.projectList = self.listTracksGRPCodes if self.itineraryCombo.currentText() == C_TextTousItineraries else [self.itineraryCombo.currentText()]
		if self.typeSelected == 'GRT':
			self.projectList = self.listTracksGRTCodes if self.itineraryCombo.currentText() == C_TextTousItineraries else [self.itineraryCombo.currentText()]
		if self.typeSelected == 'RI':
			self.projectList = self.listTracksRICodes if self.itineraryCombo.currentText() == C_TextTousItineraries else [self.itineraryCombo.currentText()]
		if self.typeSelected == 'RL':
			self.projectList = self.listTracksRLCodes if self.itineraryCombo.currentText() == C_TextTousItineraries else [self.itineraryCombo.currentText()]
		if self.typeSelected == 'RB':
			self.projectList = self.listTracksRBCodes if self.itineraryCombo.currentText() == C_TextTousItineraries else [self.itineraryCombo.currentText()]
		if self.typeSelected == 'RF':
			self.projectList = self.listTracksRFCodes if self.itineraryCombo.currentText() == C_TextTousItineraries else [self.itineraryCombo.currentText()]
		if self.typeSelected == 'IR':
			self.projectList = self.listTracksIRCodes if self.itineraryCombo.currentText() == C_TextTousItineraries else [self.itineraryCombo.currentText()]


# ========================================================================================
#	Déterminer le dictionnaire des products, c'est-à-dire des fichiers, créés localement, sur X:/QCarto Projets
#		- self.dicoProductsList 
#		- seuls les fichiers produits avec la bonne extension et le bon préfixe sont repris
#		- losrque plusieurs versions existent, cas ou seul la date et heures sont différentes, seul le fichier le plus récent est repris
# ========================================================================================

	def generateDicoProductsLocalList(self, productFolderPath, fileTypeList, prefixList):
		rootFolder = QGP.configPathProject
		if not os.path.isdir(rootFolder): return																		# Should not happen unless X: is not defined
		for product in os.listdir(rootFolder):
			if product not in self.projectList: continue
			if product not in self.dicoProductsList : self.dicoProductsList[product] = {}
			productPath = productFolderPath.replace('%PROJECT%', product)												
			if not os.path.isdir(productPath): continue																	# Never worked on this product				
			if self.mainFrame.debugModeQCartoLevel >= 1 : print('generateDicoProductsLocalList - Product = ' + product + ' = ' + productPath)
			lastBaseName = lastTimeStamp = None
			for fileName in os.listdir(productPath):
				baseName, timeStamp, extension = TFIL.splitFileName(fileName)
				if not any(baseName[0:len(prefix)] == prefix for prefix in prefixList): continue						# Look only for files with selected prefixes
				if extension not in fileTypeList: continue																		# Look only for files with right extension
				if '-Draft' in baseName and not self.draftCheckBox.checkState() == Qt.Checked : continue				# Look only for non draft is requested
				if baseName == lastBaseName and timeStamp <= lastTimeStamp: continue									# Keep only most recent version
				lastBaseName = baseName; lastTimeStamp = timeStamp
				if self.mainFrame.debugModeQCartoLevel >= 1 : print('generateDicoProductsLocalList - fileName = ' + fileName)
				if baseName not in self.dicoProductsList[product]: self.dicoProductsList[product][baseName] = {}
				self.dicoProductsList[product][baseName][C_dicoProduct_localPathX] = productPath
				self.dicoProductsList[product][baseName][C_dicoProduct_localFileX] = fileName
				self.dicoProductsList[product][baseName][C_dicoProduct_localDateX] = timeStamp
		
	
# ========================================================================================
#	Déterminer le dictionnaire des products, c'est-à-dire des fichiers, qui existent sur le drive des Carto, sur Y:/Publications SGR
#		- self.dicoProductsList 
#		- seuls les fichiers produits avec la bonne extension et le bon préfixe sont repris
# ========================================================================================

	def generateDicoProductsCartoList(self, productFolderPath, fileTypeList, prefixList):
		allProductsPath = QGP.pathDeliveriesCarto
		if not os.path.isdir(allProductsPath): return																	# Should not happen unless Y: is not defined
		if self.mainFrame.debugModeQCartoLevel >= 1 : print('generateDicoProductsCartoList - allProductsPath = ' + allProductsPath)
		for product in os.listdir(allProductsPath):
			if product not in self.projectList: continue
			if product not in self.dicoProductsList : self.dicoProductsList[product] = {}
			productPath = productFolderPath.replace('%PROJECT%', product)												
			if not os.path.isdir(productPath): continue																	# Nobody ever worked on this product				
			if self.mainFrame.debugModeQCartoLevel >= 1 : print('generateDicoProductsCartoList - Product = ' + product + ' = ' + productPath)
			for fileName in os.listdir(productPath):
				baseName, timeStampCarto, extension = TFIL.splitFileName(fileName)
				if not any(baseName[0:len(prefix)] == prefix for prefix in prefixList): continue						# Look only for files with selected prefixes
				if extension not in fileTypeList: continue																		# Look only for files with right extension
				if '-Draft' in baseName and not self.draftCheckBox.checkState() == Qt.Checked : continue				# Look only for non draft is requested
				if self.mainFrame.debugModeQCartoLevel >= 1 : print('generateDicoProductsCartoList - fileName = ' + fileName)
				if baseName not in self.dicoProductsList[product]: self.dicoProductsList[product][baseName] = {}
				self.dicoProductsList[product][baseName][C_dicoProduct_cartoPathY] = productPath
				self.dicoProductsList[product][baseName][C_dicoProduct_cartoFileY] = fileName
				self.dicoProductsList[product][baseName][C_dicoProduct_cartoDateY] = timeStampCarto
				self.dicoProductsList[product][baseName][C_dicoProduct_infoCartoName], self.dicoProductsList[product][baseName][C_dicoProduct_infoCartoDate] = self.getDeliveryInfo('Carto', product, fileName, productPath)
				self.dicoProductsList[product][baseName][C_dicoProduct_infoTopoName], self.dicoProductsList[product][baseName][C_dicoProduct_infoTopoDate] = self.getDeliveryInfo('Topo', product, fileName, productPath)
				if self.mainFrame.debugModeQCartoLevel >= 1 : print('dicoProductsCartoList - fileName = ' + fileName + ' = ' + str(self.dicoProductsList[product][baseName]))


# ========================================================================================
#	Déterminer le dictionnaire des products, c'est-à-dire des fichiers :
#		- self.dicoProductsList 
#		- seuls les fichiers produits avec la bonne extension et le bon préfixe sont repris
#  >>> targetPath : str				Dossier cible (GPX OSM) - par défaut la cible est prise sur le Drive Topo
# ========================================================================================F

	def generateDicoProductsTopoList(self, targetPath = None):
		for product in self.dicoProductsList:
			for baseName in self.dicoProductsList[product]:
				prefix, trackCode, name	 = TFIL.splitFileBaseName(baseName)				
				deliveryPath = DTOP.getDriveTopoPath(trackCode, prefix) if targetPath == None else targetPath
				if self.mainFrame.debugModeQCartoLevel >= 1 : print('generateDicoProductsTopoList - deliveryPath = ' + deliveryPath)
				fileName = self.dicoProductsList[product][baseName][C_dicoProduct_cartoFileY] if C_dicoProduct_cartoFileY in self.dicoProductsList[product][baseName] else None
				self.dicoProductsList[product][baseName][C_dicoProduct_topoPathZ] = deliveryPath
				self.dicoProductsList[product][baseName][C_dicoProduct_topoFolderOpen] = os.path.isdir(deliveryPath)
				self.dicoProductsList[product][baseName][C_dicoProduct_topoFileExist] = os.path.isfile(deliveryPath + self.dicoProductsList[product][baseName][C_dicoProduct_cartoFileY]) if fileName != None else False


# ========================================================================================
#	Obtenir les infos du fichier de livraison
#	 >>> mode 				: str				'Carto' ou 'Topo'    
#	 >>> product			: str				Code produit   
#	 >>> fileName			: str				File Name
#	 >>> filePath			: str				Path complet du fichier (avec son extension de base)
#	 <<< cartographe		: str				Nom du cartographe // None if file does not exist // False si fichier incorrect
#	 <<< date livraison		: str				Date de livraison // Filepath if file does not exist // Filepath si fichier incorrect
# ========================================================================================

	def getDeliveryInfo(self, mode, product, fileName, filePath):
		if mode == 'Carto' : filePath += DTOP.subPathFileDelivery + TFIL.changeFileExtension(fileName, DTOP.extensionFileDeliveryCartoDate)
		if mode == 'Topo' : filePath += DTOP.subPathFileDelivery + TFIL.changeFileExtension(fileName, DTOP.extensionFileDeliveryTopoDate)
		if not os.path.isfile(filePath) : return None, filePath
		
		try:
			fileIn = open(filePath, 'r')
			info = fileIn.readline().replace('\n','')
			fileIn.close()
			return info.split(' - ')[1], info.split(' - ')[0]
		except:
			return False, filePath

			
# ========================================================================================
#	Initialiser la table des produits
# ========================================================================================
	
	def initializeProductsTable(self):

		def createItem(value, position):
			itemFont = QFont()
			itemFont.setPixelSize(DSTY.tableItemFontSize)
			itemText = value if value not in (None, '') else ''
			item = QtWidgets.QTableWidgetItem(itemText)
			if position == 'Left': item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
			if position == 'Center': item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
			item.setFont(itemFont)
			item.setFlags(item.flags() & ~Qt.ItemIsEditable)
			return item
			
		def sortFileNames(baseName):													# Pour avoir les cartes GR.P.T dans bon ordre !
			fileNameParts = baseName.split(' - ')
			try:
				if TCOD.itineraryTypeFromTrackCode(fileNameParts[1]) not in QGP.typeSetModeGR : return baseName	
				mapNameParts = fileNameParts[2].split(' ')
				mapNum = int(mapNameParts[1])
				mapNameParts[1] = ('0000' + str(mapNum))[-4:]
				fileNameParts[2] = ' '.join(mapNameParts)
				if 'Draft' in fileNameParts[0] : fileNameParts[0] = 'ZZZZ' + fileNameParts[0]
				return ' - '.join(fileNameParts)
			except:
				return baseName	

		self.groupBoxProductsTable.itemChanged.disconnect()
		self.groupBoxProductsTable.setSortingEnabled(False)									
		self.groupBoxProductsTable.clearContents()
		self.groupBoxProductsTable.setRowCount(sum(len(self.dicoProductsList[product]) for product in self.dicoProductsList))

		self.dicoProductTable = {}
		tableFields = QGP.productsTableQView
		row = 0
		for product in sorted(self.dicoProductsList):
			for baseName in sorted(self.dicoProductsList[product], key=lambda x: sortFileNames(x), reverse=False):
				itinerary = product
				timeStampLocal = self.dicoProductsList[product][baseName][C_dicoProduct_localDateX] if C_dicoProduct_localDateX in self.dicoProductsList[product][baseName] else ''
				timeStampCarto = self.dicoProductsList[product][baseName][C_dicoProduct_cartoDateY] if C_dicoProduct_cartoDateY in self.dicoProductsList[product][baseName] else ''
				timeStampTopo = timeStampCarto if (C_dicoProduct_infoTopoName in self.dicoProductsList[product][baseName] and self.dicoProductsList[product][baseName][C_dicoProduct_infoTopoName] not in (None, False)) else ''
				folderInfo = 'Ouvert' if C_dicoProduct_topoFolderOpen in self.dicoProductsList[product][baseName] and self.dicoProductsList[product][baseName][C_dicoProduct_topoFolderOpen] else 'Non trouvé'
				if self.mainFrame.debugModeQCartoLevel >= 1 : print('initializeProductsTable = ' + baseName + ' = ' + timeStampCarto + ' = ' + timeStampTopo)
				for col in range(len(tableFields)):
					value = [itinerary, baseName, timeStampLocal, 'Copier !', timeStampCarto, 'Copier !', timeStampTopo, folderInfo][col]
					item = createItem(value, tableFields[col][QGP.C_productsTableQView_Position])
					self.groupBoxProductsTable.setItem(row, col, item)
					if tableFields[col][QGP.C_productsTableQView_Type] == 'Checkbox' : 	
						self.groupBoxProductsTable.item(row, col).setCheckState(Qt.Checked)
				self.dicoProductTable[row] = self.dicoProductsList[product][baseName]
				row += 1
		self.groupBoxProductsTable.itemChanged.connect(self.productItem_changed)


# ========================================================================================
#	Colorer la table des produits en fonctions des dates
#		date X :	- vert foncé 	: créé aujourd'hui
#					- vert 		 	: plus récent que sur Y: (ou inexistant sur Y:)
#					- jaune 		: moins récent sur sur Y:
#		date Y :	- vert 			: par moi, plus récent sur Y: (ou inexistant sur X:)
#					- bleu			: par autre, plus récent sur Y: (ou inexistant sur X:)
#					- jaune			: par moi, plus récent en local
#					- orange 		: par autre, plus récent en local
#		date Z :	- vert			: par moi, même date sur Y:
#					- bleu			: par autre, même date sur Y:
#					- jaune			: plus récent sur carto
#					- rouge 		: plus récent sur topo 
#					- barré			: ficher supprimé par maquetiste
# ========================================================================================

	def colorProductTable(self):
	
		colItinerary  = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldItineraryCode)
		colBaseName   = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldFileName)
		colStampLocal = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldDateLocal)
		colStampCarto = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldDateCarto)
		colStampTopo  = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldDateTopo)
		colCheckCarto = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldCopyCarto)
		colCheckTopo  = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldCopyTopo)
		colOpenTopo   = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldOpenTopo)
		self.deliveryCartoNewCount = 0
		self.deliveryTopoNewCount = 0
		self.groupBoxProductsTable.itemChanged.disconnect()
	
		for row in range(self.groupBoxProductsTable.rowCount()):		
		
			timeStampLocal = self.groupBoxProductsTable.item(row, colStampLocal).text()
			timeStampCarto = self.groupBoxProductsTable.item(row, colStampCarto).text()
			timeStampTopo  = self.groupBoxProductsTable.item(row, colStampTopo).text()

			product  = self.groupBoxProductsTable.item(row, colItinerary).text()
			baseName = self.groupBoxProductsTable.item(row, colBaseName).text()
			
			topoFolderOpen 	  = self.dicoProductsList[product][baseName][C_dicoProduct_topoFolderOpen]
			topoFileExist     = self.dicoProductsList[product][baseName][C_dicoProduct_topoFileExist]
			infoCartoName 	  = self.dicoProductsList[product][baseName][C_dicoProduct_infoCartoName] if C_dicoProduct_infoCartoName in self.dicoProductsList[product][baseName] else '--- no carto ---'
			infoTopoName  	  = self.dicoProductsList[product][baseName][C_dicoProduct_infoTopoName] if C_dicoProduct_infoTopoName in self.dicoProductsList[product][baseName] else '--- no carto ---'	
			
#		Couleurs pour le répertoire Topo

			self.groupBoxProductsTable.item(row, colOpenTopo).setBackground(DCOL.bgLabelOk if topoFolderOpen else DCOL.bgTableWarningSevere)

#		Couleurs pour la date X:	

			if TDAT.isTimeStampToday(timeStampLocal):
				self.groupBoxProductsTable.item(row, colStampLocal).setBackground(DCOL.bgTableTodayStrong)
			elif timeStampLocal != '' and (timeStampCarto == '' or timeStampLocal > timeStampCarto):
				self.groupBoxProductsTable.item(row, colStampLocal).setBackground(DCOL.bgTableOk)
			elif timeStampLocal != '':
				self.groupBoxProductsTable.item(row, colStampLocal).setBackground(DCOL.bgTableWarning)

#		Couleurs pour la date Y:	

			if infoCartoName == self.mainFrame.userFullName:
				if timeStampCarto != '' and timeStampCarto >= timeStampLocal:
					self.groupBoxProductsTable.item(row, colStampCarto).setBackground(DCOL.bgTableOk)
				elif timeStampCarto != '':
					self.groupBoxProductsTable.item(row, colStampCarto).setBackground(DCOL.bgTableWarning)	
					self.deliveryCartoNewCount += 1
			else:
				if timeStampCarto != '' and timeStampCarto >= timeStampLocal:
					self.groupBoxProductsTable.item(row, colStampCarto).setBackground(DCOL.bgTableOtherCarto)
				elif timeStampCarto != '':
					self.groupBoxProductsTable.item(row, colStampCarto).setBackground(DCOL.bgTableWarningOtherCarto)					
					self.deliveryCartoNewCount += 1
			self.groupBoxProductsTable.item(row, colCheckCarto).setCheckState(Qt.Unchecked)												# All unchecked is safer
	
#		Couleurs pour la date Z:	

			if timeStampTopo != '' and timeStampTopo > timeStampCarto:
				self.groupBoxProductsTable.item(row, colStampTopo).setBackground(DCOL.bgTableError)
			elif timeStampTopo != '' and timeStampTopo < timeStampCarto:
				self.groupBoxProductsTable.item(row, colStampTopo).setBackground(DCOL.bgTableWarning)
				self.deliveryTopoNewCount += 1
			elif timeStampTopo != '' and timeStampTopo == timeStampCarto:
				if infoTopoName == self.mainFrame.userFullName:
					self.groupBoxProductsTable.item(row, colStampTopo).setBackground(DCOL.bgTableOk)
				else:
					self.groupBoxProductsTable.item(row, colStampTopo).setBackground(DCOL.bgTableOtherCarto)
			if not topoFileExist:
				itemFont = self.groupBoxProductsTable.item(row, colStampTopo).font()
				itemFont.setStrikeOut(True)
				self.groupBoxProductsTable.item(row, colStampTopo).setFont(itemFont)				
			self.groupBoxProductsTable.item(row, colCheckTopo).setCheckState(Qt.Unchecked)												# All unchecked is safer
		
		self.groupBoxProductsTable.itemChanged.connect(self.productItem_changed)

		return
		

# ========================================================================================
#	Changer les entêtes de colonne en fonction du type de produit
# ========================================================================================
	
	def changeProductTableHeaders(self, mode = None) :
		if mode == None : mode = self.lastTableMode
		self.lastTableMode = mode

		if mode == 'Topo':
			self.viewMode = 'Topo'
			self.groupBoxDeliveryCarto.show()
			self.groupBoxRelationOsm.hide()
			self.groupBoxProductsTable.show()
			self.groupBoxProductsOsmTable.hide()
			for col in range(len(QGP.productsTableQView)):
				self.groupBoxProductsTable.setHorizontalHeaderItem(col, QtWidgets.QTableWidgetItem(QGP.productsTableQView[col][QGP.C_productsTableQView_ColName]))		
			self.groupBoxDeliveryTopo.setTitle('Livraisons vers Drive du Pôle Topo')				

		if mode == 'OSM':
			self.viewMode = 'OSM'
			self.groupBoxDeliveryCarto.hide()
			self.groupBoxRelationOsm.show()
			self.groupBoxProductsTable.hide()
			self.groupBoxProductsOsmTable.show()
			self.groupBoxDeliveryTopo.setTitle('Livraisons vers Coordination OSM')		
			
		if mode == 'GPX':
			self.viewMode = 'GPX'
			self.groupBoxDeliveryCarto.show()
			self.groupBoxRelationOsm.hide()
			self.groupBoxProductsTable.show()
			self.groupBoxProductsOsmTable.hide()
			for col in range(len(QGP.productsTableQViewGPX)):
				self.groupBoxProductsTable.setHorizontalHeaderItem(col, QtWidgets.QTableWidgetItem(QGP.productsTableQViewGPX[col]))
			self.groupBoxDeliveryTopo.setTitle('Livraisons vers Drive du Pôle Topo')				
	
	
# ========================================================================================
#	Déterminer le décompte des produits sélectionnés pour livraison vers Carto
#	Refuser la livraison de produits antérieurs - Sauf Forcage
# ========================================================================================

	def showDeliveryCartoCounts(self):		
		colCheckCarto = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldCopyCarto)
		colStampLocal = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldDateLocal)
		colStampCarto = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldDateCarto)
		self.groupBoxProductsTable.itemChanged.disconnect()

		self.deliveryCartoCopyCount = 0
		for row in range(self.groupBoxProductsTable.rowCount()):
			timeStampLocal = self.groupBoxProductsTable.item(row, colStampLocal).text()
			timeStampCarto = self.groupBoxProductsTable.item(row, colStampCarto).text()
		
			if self.deliveryCartoForceButton.checkState() == Qt.Unchecked:
				if timeStampLocal == '' or timeStampLocal <= timeStampCarto: self.groupBoxProductsTable.item(row, colCheckCarto).setCheckState(Qt.Unchecked)
			if self.groupBoxProductsTable.item(row, colCheckCarto).checkState() == Qt.Checked:
				self.groupBoxProductsTable.item(row, colCheckCarto).setForeground(DCOL.fgTableCopy)
				self.deliveryCartoCopyCount += 1
			else:
				self.groupBoxProductsTable.item(row, colCheckCarto).setForeground(DCOL.fgTableNoCopy)
			self.groupBoxProductsTable.item(row, colCheckCarto).setSelected(False)

		self.deliveryCartoNewCountInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%',str(self.deliveryCartoNewCount) + ' fichiers'))
		DSTY.setStyleOkLabel(self.deliveryCartoNewCountInfo, 'Normal')	
		self.deliveryCartoCopyCountInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%',str(self.deliveryCartoCopyCount) + ' fichiers'))
		DSTY.setStyleOkLabel(self.deliveryCartoCopyCountInfo, 'Normal')	
		
		self.groupBoxProductsTable.itemChanged.connect(self.productItem_changed)


# ========================================================================================
#	Déterminer le décompte des produits sélectionnés pour livraison vers Topo 
#	Refuser la livraison de produits antérieurs
# ========================================================================================

	def showDeliveryTopoCounts(self):		
	
		colCheckTopo  = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldCopyTopo)
		colStampCarto = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldDateCarto)
		colStampTopo  = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldDateTopo)
		self.groupBoxProductsTable.itemChanged.disconnect()

		self.deliveryTopoCopyCount = 0
		for row in range(self.groupBoxProductsTable.rowCount()):
			timeStampCarto = self.groupBoxProductsTable.item(row, colStampCarto).text()
			timeStampTopo = self.groupBoxProductsTable.item(row, colStampTopo).text()

			if self.deliveryTopoForceButton.checkState() == Qt.Unchecked:
				if timeStampCarto == '' or timeStampCarto <= timeStampTopo: self.groupBoxProductsTable.item(row, colCheckTopo).setCheckState(Qt.Unchecked)
			if self.groupBoxProductsTable.item(row, colCheckTopo).checkState() == Qt.Checked:
				self.groupBoxProductsTable.item(row, colCheckTopo).setForeground(DCOL.fgTableCopy)
				self.deliveryTopoCopyCount += 1
			else:
				self.groupBoxProductsTable.item(row, colCheckTopo).setForeground(DCOL.fgTableNoCopy)
			self.groupBoxProductsTable.item(row, colCheckTopo).setSelected(False)

		self.deliveryTopoNewCountInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%',str(self.deliveryTopoNewCount) + ' fichiers'))
		DSTY.setStyleOkLabel(self.deliveryTopoNewCountInfo, 'Normal')	
		self.deliveryTopoCopyCountInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%',str(self.deliveryTopoCopyCount) + ' fichiers'))
		DSTY.setStyleOkLabel(self.deliveryTopoCopyCountInfo, 'Normal')	
		
		self.groupBoxProductsTable.itemChanged.connect(self.productItem_changed)


# ========================================================================================
#	Afficher / Cacher les colonnes de Livraison Topo
# ========================================================================================

	def showTopoDelivery(self, showTopoFlag):
		self.deliveryTopoActive = showTopoFlag
		for header in (QGP.tableProductsFieldCopyTopo, QGP.tableProductsFieldDateTopo, QGP.tableProductsFieldOpenTopo):
			self.groupBoxProductsTable.setColumnHidden( [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(header), not showTopoFlag)
		self.groupBoxDeliveryTopo.show() if showTopoFlag else self.groupBoxDeliveryTopo.hide()
		

# ========================================================================================
#	Afficher en vert Fluo le bouton produit sélectionné
# ========================================================================================

	def highlightProductButton(self, button):
	
		for _ in (self.buttonShowMaps, self.buttonShowSchemas, self.buttonShowDistances, self.buttonShowProfiles, self.buttonShowGPX, self.buttonShowOSM):
			DSTY.setStyleMainButtons(_)
			
		DSTY.setStyleActiveButton(button)


# ========================================================================================
# ========================================================================================
#
# Actions pour : Cartes
# 
# ========================================================================================
# ========================================================================================
	
	def clearCartoAndTopoCheck(self):
		self.deliveryCartoLockButton.setCheckState(Qt.Unchecked)	
		self.deliveryTopoLockButton.setCheckState(Qt.Unchecked)	
		self.deliveryCartoForceButton.setCheckState(Qt.Unchecked)				
		self.deliveryTopoForceButton.setCheckState(Qt.Unchecked)				

	
	def createMapsView(self):
		self.mainFrame.setStatusWorking('Définition de la Table pour les Cartes ...')
		self.groupBoxProductsTable.clearContents()

		self.deliveryCartoPath = QGP.pathDeliveriesCartoMaps
		self.deliveryPrefixList = [DTOP.prefixMapsPDF, DTOP.prefixMapsModif, DTOP.prefixMapsTopo]
		self.deliveryFileTypeList = ['png']
		self.clearCartoAndTopoCheck()
		
		self.showTopoDelivery(True)		
		self.changeProductTableHeaders('Topo')				
		
		self.retrieveProjetsList()
		self.dicoProductsList = {}
		self.generateDicoProductsLocalList(QGP.configPathExportImages, self.deliveryFileTypeList, self.deliveryPrefixList)
		self.generateDicoProductsCartoList(self.deliveryCartoPath, self.deliveryFileTypeList, self.deliveryPrefixList)
		self.generateDicoProductsTopoList()
		self.initializeProductsTable()
		self.colorProductTable()
		self.showDeliveryCartoCounts()
		self.showDeliveryTopoCounts()
		
		self.highlightProductButton(self.buttonShowMaps)
		self.mainFrame.setStatusDone('Table des livraisons Cartes - OK')
	

# ========================================================================================
# ========================================================================================
#
# Actions pour : Schémas
# 
# ========================================================================================
# ========================================================================================	
	
	def createSchemaView(self):
		self.mainFrame.setStatusWorking('Définition de la Table pour les Schémas ...')
		self.groupBoxProductsTable.clearContents()

		self.deliveryCartoPath = QGP.pathDeliveriesCartoPlans
		self.deliveryPrefixList = [DTOP.prefixSchema]
		self.deliveryFileTypeList = ['png']
		self.clearCartoAndTopoCheck()
				
		self.showTopoDelivery(True)				
		self.changeProductTableHeaders('Topo')				
	
		self.retrieveProjetsList()
		self.dicoProductsList = {}
		self.generateDicoProductsLocalList(QGP.configPathExportPlans, self.deliveryFileTypeList, self.deliveryPrefixList)
		self.generateDicoProductsCartoList(self.deliveryCartoPath, self.deliveryFileTypeList, self.deliveryPrefixList)
		self.generateDicoProductsTopoList()
		self.initializeProductsTable()
		self.colorProductTable()
		self.showDeliveryCartoCounts()
		self.showDeliveryTopoCounts()
	
		self.highlightProductButton(self.buttonShowSchemas)
		self.mainFrame.setStatusDone('Table des livraisons Schémas - OK')

	
# ========================================================================================
# ========================================================================================
#
# Actions pour : Distances (CSV)
# 
# ========================================================================================
# ========================================================================================	
	
	def createDistancesView(self):
		self.mainFrame.setStatusWorking('Définition de la Table pour les Distances ...')
		self.groupBoxProductsTable.clearContents()

		self.deliveryCartoPath = QGP.pathDeliveriesCartoDistances
		self.deliveryPrefixList = [DTOP.prefixPlanValues]
		self.deliveryFileTypeList = ['csv']
		self.clearCartoAndTopoCheck()
				
		self.showTopoDelivery(True)
		self.changeProductTableHeaders('Topo')				
				
		self.retrieveProjetsList()
		self.dicoProductsList = {}
		self.generateDicoProductsLocalList(QGP.configPathExportPlansValues, self.deliveryFileTypeList, self.deliveryPrefixList)
		self.generateDicoProductsCartoList(self.deliveryCartoPath, self.deliveryFileTypeList, self.deliveryPrefixList)
		self.generateDicoProductsTopoList()
		self.initializeProductsTable()
		self.colorProductTable()
		self.showDeliveryCartoCounts()
		self.showDeliveryTopoCounts()
		
		self.highlightProductButton(self.buttonShowDistances)
		self.mainFrame.setStatusDone('Table des livraisons Distances - OK')
	
	
# ========================================================================================
# ========================================================================================
#
# Actions pour : Profils Altimétriques
# 
# ========================================================================================
# ========================================================================================	
	
	def createProfilesView(self):
		self.mainFrame.setStatusWorking('Définition de la Table pour les Profils ...')
		self.groupBoxProductsTable.clearContents()

		self.deliveryCartoPath = QGP.pathDeliveriesCartoProfils
		self.deliveryPrefixList = [DTOP.prefixProfils]
		self.deliveryFileTypeList = ['png']
		self.clearCartoAndTopoCheck()
		
		self.showTopoDelivery(True)
		self.changeProductTableHeaders('Topo')				

		self.retrieveProjetsList()
		self.dicoProductsList = {}
		self.generateDicoProductsLocalList(QGP.configPathExportProfils, self.deliveryFileTypeList, self.deliveryPrefixList)
		self.generateDicoProductsCartoList(self.deliveryCartoPath, self.deliveryFileTypeList, self.deliveryPrefixList)
		self.generateDicoProductsTopoList()
		self.initializeProductsTable()
		self.colorProductTable()
		self.showDeliveryCartoCounts()
		self.showDeliveryTopoCounts()
		
		self.highlightProductButton(self.buttonShowProfiles)
		self.mainFrame.setStatusDone('Table des livraisons Profils - OK')


# ========================================================================================
# ========================================================================================
#
# Actions pour : Fichiers GPX
# 
# ========================================================================================
# ========================================================================================	
	
	def createGPXView(self):
		self.mainFrame.setStatusWorking('Définition de la Table pour les GPX ...')
		self.groupBoxProductsTable.clearContents()

		self.deliveryCartoPath = QGP.pathDeliveriesCartoGPX
		self.deliveryPrefixList = [DTOP.prefixGPX, DTOP.prefixHtml]
		self.deliveryFileTypeList = ['gpx', 'html']
		self.clearCartoAndTopoCheck()
				
		self.showTopoDelivery(True)
		self.changeProductTableHeaders('GPX' if self.typeSelected in QGP.typeSetModeGR else 'Topo')				
				
		self.retrieveProjetsList()
		self.dicoProductsList = {}
		self.generateDicoProductsLocalList(QGP.configPathExportGPX, self.deliveryFileTypeList, self.deliveryPrefixList)
		self.generateDicoProductsCartoList(self.deliveryCartoPath, self.deliveryFileTypeList, self.deliveryPrefixList)
		self.generateDicoProductsTopoList(QGP.pathDeliveriesSiteGR if self.typeSelected in QGP.typeSetModeGR else None)	
		self.initializeProductsTable()
		self.colorProductTable()
		self.showDeliveryCartoCounts()
		self.showDeliveryTopoCounts()
		
		self.highlightProductButton(self.buttonShowGPX)
		self.mainFrame.setStatusDone('Table des livraisons GPX - OK')


# ========================================================================================
# ========================================================================================
#
# Actions pour : Fichiers GPX for SityTrail
# 
# ========================================================================================
# ========================================================================================	
	
	def createGPXSityTrailView(self):
		self.mainFrame.setStatusWorking('Définition de la Table pour les GPX ...')
		self.groupBoxProductsTable.clearContents()

		self.deliveryCartoPath = QGP.pathDeliveriesCartoGPXSityTrail
		self.deliveryPrefixList = [DTOP.prefixGPXSityTrail]
		self.deliveryFileTypeList = ['gpx']
		self.clearCartoAndTopoCheck()
				
		self.showTopoDelivery(True)
		self.changeProductTableHeaders('Topo')
				
		self.retrieveProjetsList()
		self.dicoProductsList = {}
		self.generateDicoProductsLocalList(QGP.configPathExportGPXSityTrail, self.deliveryFileTypeList, self.deliveryPrefixList)
		self.generateDicoProductsCartoList(self.deliveryCartoPath, self.deliveryFileTypeList, self.deliveryPrefixList)
		self.generateDicoProductsTopoList(QGP.pathDeliveriesSityTrail)
		self.initializeProductsTable()
		self.colorProductTable()
		self.showDeliveryCartoCounts()
		self.showDeliveryTopoCounts()
		
		self.highlightProductButton(self.buttonShowGPXSityTrail)
		self.mainFrame.setStatusDone('Table des livraisons GPX SityTrail - OK')


# ========================================================================================
# ========================================================================================
#
# Actions pour : Fichiers GPX OSM
# 
# ========================================================================================
# ========================================================================================	
	
	def createOSMView(self):
		self.mainFrame.setStatusWorking('Définition de la Table pour tous les Parcours Osm ...')

		self.changeProductTableHeaders('OSM')			
		self.clearCartoAndTopoCheck()
		self.retrieveProjetsList()
		self.dicoProductsOsm = {}
		self.initializeProductsOsmTable()					# First call to clear Table
		self.generateDicoProductsOsm()
		self.initializeProductsOsmTable()
		self.colorProductsOsmTable()
		self.showDeliveryOsmCounts()
		
		self.highlightProductButton(self.buttonShowOSM)
		self.mainFrame.setStatusDone('Table des livraisons Osm - OK')


# ========================================================================================
# Génération du dictionnaire complet
# ========================================================================================

	def generateDicoProductsOsm(self):
	
#	Extraire les Track Features concernées 

		trackCodeOsmList = [ trackCode for trackCode in self.mainFrame.dicoTracksGRFeatures if TCOD.itineraryFromTrackCode(trackCode) in self.projectList ]

#	Create Progress Bar

		progressBar = TPRO.createProgressBar(self.buttonShowOSM, len(trackCodeOsmList), 'Normal')

# 	Check Y Folder	
	
		allProductsPath = QGP.pathDeliveriesCarto
		if not os.path.isdir(allProductsPath): return																	# Should not happen unless Y: is not defined
		prefixGPX = DTOP.prefixGPX + ' - '
	
#	Loop all Track GR GRP GRT

		for trackCode in trackCodeOsmList :

			progressBar.setValue(progressBar.value() + 1)
			QgsApplication.processEvents()
		
#		Reject Track Modified / Futures / Not Marked

			valid, type, label, zone, number, itineraryCode, trackBaseCode, trackCode, modificationList, invalidationList, repeatCount, bifurcationNumber, direction = TCOD.elementsFromGrCode(trackCode)		
			if not valid : continue
			if 'T' in modificationList : continue
			if 'F' in modificationList : continue
			if self.mainFrame.dicoTracksGRFeatures[trackCode][QGP.tableTracksFieldMarked] != 	QGP.trackMarkedStandard : continue
		
#		Get Info from Track DB Feature


			self.dicoProductsOsm[trackCode] = {}
			self.dicoProductsOsm[trackCode]['Nom'] = self.mainFrame.dicoTracksGRFeatures[trackCode][QGP.tableTracksFieldName]
			self.dicoProductsOsm[trackCode]['Osmid'] = self.mainFrame.dicoTracksGRFeatures[trackCode][QGP.tableTracksFieldOsmid]
			self.dicoProductsOsm[trackCode]['Date DB'] = self.mainFrame.dicoTracksGRFeatures[trackCode][QGP.tableAllFieldDateModif].replace('T',' ').replace(':','-')

#		Get Info from Y: Publications Carto

			self.dicoProductsOsm[trackCode]['Path Y'] = ''
			self.dicoProductsOsm[trackCode]['Date Y'] = ''
			self.dicoProductsOsm[trackCode]['Delta Y'] = -1
			self.dicoProductsOsm[trackCode]['File Y'] = ''
			
			productPathY = self.dicoProductsOsm[trackCode]['Path Y'] = QGP.pathDeliveriesCartoGPX.replace('%PROJECT%', itineraryCode)	
			if os.path.isdir(productPathY): 
				for fileName in sorted(os.listdir(productPathY)):
					baseName, timeStampCarto, extension = TFIL.splitFileName(fileName)
					if extension != 'gpx' : continue
					if baseName[0:len(prefixGPX)] != prefixGPX : continue
					if baseName != prefixGPX + self.dicoProductsOsm[trackCode]['Nom'] : continue
					self.dicoProductsOsm[trackCode]['File Y'] = fileName
					self.dicoProductsOsm[trackCode]['Date Y'] = timeStampCarto
					trackLineGPX, wayPoints, wayPois, errorText = TGPX.importGpxTrack(productPathY + fileName)
					if trackLineGPX != None :
						self.dicoProductsOsm[trackCode]['Delta Y'] = round(self.mainFrame.dicoTracksGRFeatures[trackCode].geometry().hausdorffDistance(QgsGeometry().fromPolylineXY(trackLineGPX)))
#					break

#		Get Info from Y: Coordination Osm

			self.dicoProductsOsm[trackCode]['Path Osm'] = ''
			self.dicoProductsOsm[trackCode]['Date Osm'] = ''
			self.dicoProductsOsm[trackCode]['Delta Osm'] = -1
			self.dicoProductsOsm[trackCode]['File Osm'] = ''
		
			productPathOsm = self.dicoProductsOsm[trackCode]['Path Osm'] = QGP.pathDeliveriesCoordinationOSM
			if os.path.isdir(productPathOsm): 	
				for fileName in sorted(os.listdir(productPathOsm)):
					baseName, timeStampCarto, extension = TFIL.splitFileName(fileName)
					if extension != 'gpx' : continue
					if baseName[0:len(prefixGPX)] != prefixGPX : continue
					if baseName != prefixGPX + self.dicoProductsOsm[trackCode]['Nom'] : continue
					self.dicoProductsOsm[trackCode]['File Osm'] = fileName
					self.dicoProductsOsm[trackCode]['Date Osm'] = timeStampCarto
					trackLineGPX, wayPoints, wayPois, errorText = TGPX.importGpxTrack(productPathOsm + fileName)
					if trackLineGPX != None :
						self.dicoProductsOsm[trackCode]['Delta Osm'] = round(self.mainFrame.dicoTracksGRFeatures[trackCode].geometry().hausdorffDistance(QgsGeometry().fromPolylineXY(trackLineGPX)))
#					break

#		Retrieve Knooppuntnet delivery date
		
			self.dicoProductsOsm[trackCode]['Date Kpn'] = ''

			if self.dicoProductsOsm[trackCode]['File Osm'] != '' :
				filePath = QGP.pathDeliveriesCoordinationOSM + C_kpnPathFileDelivery + TFIL.changeFileExtension(self.dicoProductsOsm[trackCode]['File Osm'], C_extensionFileDeliveryKpnDate)
				try:
					fileIn = open(filePath, 'r')
					info = fileIn.readline().replace('\n','')
					fileIn.close()
					self.dicoProductsOsm[trackCode]['Date Kpn'] = info.split(' - ')[0]
				except:	
					pass
		
#		Retrieve Delta and Computation date
		
			self.dicoProductsOsm[trackCode]['Delta Osm Relation'] = -1
			self.dicoProductsOsm[trackCode]['Date Osm Relation'] = ''

			filePath = QGP.pathDeliveriesCoordinationOSM + C_deltaPathFileDelivery + self.dicoProductsOsm[trackCode]['Nom'] + '.' + C_extensionFileOsmDelta
			try:
				fileIn = open(filePath, 'r')
				info = fileIn.readline().replace('\n','')
				fileIn.close()
				self.dicoProductsOsm[trackCode]['Delta Osm Relation'] = int(info.split(' - ')[2])
				self.dicoProductsOsm[trackCode]['Date Osm Relation'] = info.split(' - ')[0]
			except:	
				pass

#	Terminé

		del progressBar


# ========================================================================================
#	Initialiser la table - sauf couleurs
# ========================================================================================
		
	def initializeProductsOsmTable(self):		

		def createItem(value, type, position):
			itemFont = QFont()
			itemFont.setPixelSize(DSTY.tableItemFontSize)
			if type == 'Text' : itemText = value if value not in (None, '') else ''
			if type == 'Dist' : itemText = '{:0d} m'.format(value) if value != -1 else ''
			if type == 'Checkbox' : itemText = value
			item = QtWidgets.QTableWidgetItem(itemText)
			if position == 'Left': item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
			if position == 'Center': item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
			if position == 'Right': item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
			item.setFont(itemFont)
			item.setFlags(item.flags() & ~Qt.ItemIsEditable)
			return item
			
		self.groupBoxProductsOsmTable.itemChanged.disconnect()		
		self.groupBoxProductsOsmTable.setSortingEnabled(False)									
		self.groupBoxProductsOsmTable.clearContents()
		self.groupBoxProductsOsmTable.setRowCount(len(self.dicoProductsOsm))
			
		tableFields = QGP.productsTableQViewOSM			
		for row, trackCode in zip(range(len(self.dicoProductsOsm)), sorted(self.dicoProductsOsm, reverse = False)) :
			for col in range(len(tableFields)):
				value = ([trackCode] + [ self.dicoProductsOsm[trackCode][_x_] for _x_ in ['Nom', 'Osmid', 'Date DB', 'Date Y', 'Delta Y']] + \
							['Copier !'] + [ self.dicoProductsOsm[trackCode][_x_] for _x_ in ['Date Osm', 'Delta Osm', 'Date Kpn', 'Date Osm Relation', 'Delta Osm Relation' ]] ) [col]
				item = createItem(value, tableFields[col][QGP.C_productsTableQView_Type], tableFields[col][QGP.C_productsTableQView_Position])
				self.groupBoxProductsOsmTable.setItem(row, col, item)
				if tableFields[col][QGP.C_productsTableQView_Type] == 'Checkbox' : 	
					self.groupBoxProductsOsmTable.item(row, col).setCheckState(Qt.Unchecked)
			row += 1

		self.groupBoxProductsOsmTable.setSortingEnabled(True)		
		self.groupBoxProductsOsmTable.sortByColumn(0, Qt.AscendingOrder)
		self.groupBoxProductsOsmTable.itemChanged.connect(self.productOsmItem_changed)


# ========================================================================================
#	Colorer la table des produits en fonctions des dates
#
#		OsmId :		- vert 			: défini
#					- jaune			: non défini
#
#		Date DB :	- vert fluo		: aujourd'hui
#					- vert 			: plus récent DB que Y
#					- jaune			: moins récent DB que Y
#
#		Date Y :	- vert fluo		: aujourd'hui
#					- vert 			: plus récent Y que Osm
#					- jaune			: moins récent Y que Osm
#
#		Date Osm :	- vert fluo		: aujourd'hui
#					- vert 			: plus récent Osm que Kpn
#					- jaune			: moins récent Osm que Kpn
#
#		Date Kpn :  - vert fluo		: aujourd'hui
#					- rouge			: vide	
#					- vert 			: delta <= 10
#					- jaune : 		: delta <= 100
#					- orange :		: delta <= 1000 m 
#					- rouge :		: delta > 1000 m 
#
#		Delta		- vert :		: <= 10 
#					- jaune : 		: <= 100 m ou vide
#					- orange :		: <= 1000 m 
#					- rouge :		: > 1000 m 
#
# ========================================================================================

	def colorProductsOsmTable(self):
	
		self.deliveryTopoNewCount = 0
	
		for row in range(self.groupBoxProductsOsmTable.rowCount()):		
		
			trackCode = self.groupBoxProductsOsmTable.item(row, CO_colTrackCode).text()
			osmid = self.dicoProductsOsm[trackCode]['Osmid']
			timeStampDB = self.dicoProductsOsm[trackCode]['Date DB']
			timeStampCarto = self.dicoProductsOsm[trackCode]['Date Y']
			timeStampOsm  = self.dicoProductsOsm[trackCode]['Date Osm']
			timeStampOsmRel = self.dicoProductsOsm[trackCode]['Date Osm Relation']
			timeStampKpn  = self.dicoProductsOsm[trackCode]['Date Kpn']
			deltaCarto = self.dicoProductsOsm[trackCode]['Delta Y']
			deltaOsm = self.dicoProductsOsm[trackCode]['Delta Osm']
			deltaOsmRel = self.dicoProductsOsm[trackCode]['Delta Osm Relation']

#		Couleurs Osmid

			if osmid not in (None, '') :
				self.groupBoxProductsOsmTable.item(row, CO_colOsmid).setBackground(DCOL.bgTableOk)
			else:
				pass

#		Couleurs Delta

			for delta, col in zip([deltaCarto, deltaOsm, deltaOsmRel], [CO_colDeltaCarto, CO_colDeltaOsm, CO_colDeltaRel]) :
				if delta == -1:
					pass
				elif int(delta) > 1000:
					self.groupBoxProductsOsmTable.item(row, col).setBackground(DCOL.bgTableError)
				elif int(delta) > 100:
					self.groupBoxProductsOsmTable.item(row, col).setBackground(DCOL.bgTableWarningSevere)
				elif int(delta) > 10:
					self.groupBoxProductsOsmTable.item(row, col).setBackground(DCOL.bgTableWarning)	
				else:
					self.groupBoxProductsOsmTable.item(row, col).setBackground(DCOL.bgTableOk)	

#		Couleurs pour la date DB

			if TDAT.isTimeStampToday(timeStampDB) : 
				self.groupBoxProductsOsmTable.item(row, CO_colStampDB).setBackground(DCOL.bgTableTodayStrong)
			elif timeStampDB != '' and (timeStampCarto == '' or timeStampDB > timeStampCarto):
				self.groupBoxProductsOsmTable.item(row, CO_colStampDB).setBackground(DCOL.bgTableOk)
			elif timeStampDB != '':
				self.groupBoxProductsOsmTable.item(row, CO_colStampDB).setBackground(DCOL.bgTableWarning)

#		Couleurs pour la date Y

			if timeStampCarto != '' and (timeStampOsm == '' or timeStampCarto > timeStampOsm):
				self.deliveryTopoNewCount += 1
				if TDAT.isTimeStampToday(timeStampCarto) : 
					self.groupBoxProductsOsmTable.item(row, CO_colStampCarto).setBackground(DCOL.bgTableTodayStrong)
				else :
					self.groupBoxProductsOsmTable.item(row, CO_colStampCarto).setBackground(DCOL.bgTableOk)
			elif timeStampCarto != '':
				self.groupBoxProductsOsmTable.item(row, CO_colStampCarto).setBackground(DCOL.bgTableWarning)

#		Couleurs pour la date Osm

			if TDAT.isTimeStampToday(timeStampOsm) : 
				self.groupBoxProductsOsmTable.item(row, CO_colStampOsm).setBackground(DCOL.bgTableTodayStrong)
			elif timeStampOsm != '' and (timeStampKpn == '' or timeStampOsm > timeStampKpn):
				self.groupBoxProductsOsmTable.item(row, CO_colStampOsm).setBackground(DCOL.bgTableOk)
			elif timeStampOsm != '':
				self.groupBoxProductsOsmTable.item(row, CO_colStampOsm).setBackground(DCOL.bgTableWarning)

#		Couleurs pour la date Osm Relation

			if timeStampOsmRel == '':
				pass
			elif TDAT.isTimeStampToday(timeStampOsmRel) : 
				self.groupBoxProductsOsmTable.item(row, CO_colStampRel).setBackground(DCOL.bgTableTodayStrong)
			elif TDAT.daysTillToday(timeStampOsmRel) == False:
				self.groupBoxProductsOsmTable.item(row, CO_colStampRel).setBackground(DCOL.bgTableError)
			elif TDAT.daysTillToday(timeStampOsmRel) <= 10:
				self.groupBoxProductsOsmTable.item(row, CO_colStampRel).setBackground(DCOL.bgTableOk)
			elif TDAT.daysTillToday(timeStampOsmRel) <= 30:
				self.groupBoxProductsOsmTable.item(row, CO_colStampRel).setBackground(DCOL.bgTableWarning)
			elif TDAT.daysTillToday(timeStampOsmRel) <= 91:
				self.groupBoxProductsOsmTable.item(row, CO_colStampRel).setBackground(DCOL.bgTableWarningSevere)
			else:
				self.groupBoxProductsOsmTable.item(row, CO_colStampRel).setBackground(DCOL.bgTableError)

#		Couleurs pour la date Kpn

			if timeStampKpn == '':
				self.groupBoxProductsOsmTable.item(row, CO_colStampKpn).setBackground(DCOL.bgTableError)
			elif int(deltaOsm) > 1000:
				self.groupBoxProductsOsmTable.item(row, CO_colStampKpn).setBackground(DCOL.bgTableError)
			elif int(deltaOsm) > 100:
				self.groupBoxProductsOsmTable.item(row, CO_colStampKpn).setBackground(DCOL.bgTableWarningSevere)
			elif int(deltaOsm) > 10:
				self.groupBoxProductsOsmTable.item(row, CO_colStampKpn).setBackground(DCOL.bgTableWarning)	
			elif TDAT.isTimeStampToday(timeStampKpn) : 
				self.groupBoxProductsOsmTable.item(row, CO_colStampKpn).setBackground(DCOL.bgTableTodayStrong)
			else:
				self.groupBoxProductsOsmTable.item(row, CO_colStampKpn).setBackground(DCOL.bgTableOk)	


# ========================================================================================
#	Auto Select if Header clicked
# ========================================================================================

	def tableOsmHeader_clicked(self, index):

		for row in range(self.groupBoxProductsOsmTable.rowCount()):
			timeStampCarto = self.groupBoxProductsOsmTable.item(row, CO_colStampCarto).text()
			timeStampOsm = self.groupBoxProductsOsmTable.item(row, CO_colStampOsm).text()
			self.groupBoxProductsOsmTable.item(row, CO_colCheckOsm).setCheckState(Qt.Checked if (TDAT.isTimeStampToday(timeStampCarto) and not TDAT.isTimeStampToday(timeStampOsm)) else Qt.Unchecked)
		self.groupBoxProductsOsmTable.clearSelection()
	
	
# ========================================================================================
#	Update delivery count if Osm table changed
# ========================================================================================
	
	def productOsmItem_changed(self, item):
		self.showDeliveryOsmCounts()
	
	def showDeliveryOsmCounts(self):		
		self.groupBoxProductsOsmTable.itemChanged.disconnect()

		self.deliveryOsmCopyCount = 0
		for row in range(self.groupBoxProductsOsmTable.rowCount()):
			timeStampCarto = self.groupBoxProductsOsmTable.item(row, CO_colStampCarto).text()
			timeStampOsm = self.groupBoxProductsOsmTable.item(row, CO_colStampOsm).text()
		
			if self.deliveryTopoForceButton.checkState() == Qt.Unchecked:
				if timeStampCarto == '' or timeStampCarto <= timeStampOsm: self.groupBoxProductsOsmTable.item(row, CO_colCheckOsm).setCheckState(Qt.Unchecked)
			if self.groupBoxProductsOsmTable.item(row, CO_colCheckOsm).checkState() == Qt.Checked:
				self.groupBoxProductsOsmTable.item(row, CO_colCheckOsm).setForeground(DCOL.fgTableCopy)
				self.deliveryOsmCopyCount += 1
			else:
				self.groupBoxProductsOsmTable.item(row, CO_colCheckOsm).setForeground(DCOL.fgTableNoCopy)
			self.groupBoxProductsOsmTable.item(row, CO_colCheckOsm).setSelected(False)

		self.deliveryTopoNewCountInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%',str(self.deliveryTopoNewCount) + ' fichiers'))
		DSTY.setStyleOkLabel(self.deliveryTopoNewCountInfo, 'Normal')	
		self.deliveryTopoCopyCountInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%',str(self.deliveryOsmCopyCount) + ' fichiers'))
		DSTY.setStyleOkLabel(self.deliveryTopoCopyCountInfo, 'Normal')	
		
		self.groupBoxProductsOsmTable.itemChanged.connect(self.productOsmItem_changed)

	
# ========================================================================================
#	Update Relation Osm Box when selection changed
# ========================================================================================
	
	def productOsmItem_selectionChanged(self):
		self.trackCodeForOsm = None
		self.trackOsmidForOsm = None
		listSelectedItemRows = list({item.row() for item in self.groupBoxProductsOsmTable.selectedItems()})
		selectedRow = listSelectedItemRows[0] if len(listSelectedItemRows) == 1 else None

		if selectedRow != None :
			trackCode = self.groupBoxProductsOsmTable.item(selectedRow, CO_colTrackCode).text()
			self.buttonTrackOsmCode.setText(DSTY.textFormatBlackNormal.replace('%TEXT%', trackCode))
			DSTY.setStyleOkLabel(self.buttonTrackOsmCode, 'Normal')

			osmid = self.groupBoxProductsOsmTable.item(selectedRow, CO_colOsmid).text()
			self.buttonTrackOsmId.setText(DSTY.textFormatBlackNormal.replace('%TEXT%', osmid))
			DSTY.setStyleOkLabel(self.buttonTrackOsmId, 'Normal')

			trackName = self.groupBoxProductsOsmTable.item(selectedRow, CO_colTrackName).text()
			self.buttonTrackOsmName.setText(DSTY.textFormatBlackNormal.replace('%TEXT%', trackName))
			DSTY.setStyleOkLabel(self.buttonTrackOsmName, 'Double')

			dateDelta = self.dicoProductsOsm[trackCode]['Date Osm Relation']
			self.buttonTrackOsmDateDelta.setText(DSTY.textFormatBlackNormal.replace('%TEXT%', dateDelta[0:10]))
			DSTY.setStyleOkLabel(self.buttonTrackOsmDateDelta, 'Normal')

			delta = self.dicoProductsOsm[trackCode]['Delta Osm Relation']
			self.buttonTrackOsmDelta.setText(DSTY.textFormatBlackNormal.replace('%TEXT%', '{:.1f} mètres'.format(float(delta)) if delta != '' else ''))
			DSTY.setStyleOkLabel(self.buttonTrackOsmDelta, 'Normal')
			self.trackCodeForOsm = trackCode
			self.trackOsmidForOsm = osmid if osmid not in ('', None) else None

		else:
			self.buttonTrackOsmCode.setText(DSTY.textFormatBlackNormal.replace('%TEXT%', '. . .'))
			DSTY.setStyleWarningLabel(self.buttonTrackOsmCode, 'Normal')
			self.buttonTrackOsmId.setText(DSTY.textFormatBlackNormal.replace('%TEXT%', '. . .'))
			DSTY.setStyleWarningLabel(self.buttonTrackOsmId, 'Normal')
			self.buttonTrackOsmName.setText(DSTY.textFormatBlackNormal.replace('%TEXT%', '. . .'))
			DSTY.setStyleWarningLabel(self.buttonTrackOsmName, 'Double')
			self.buttonTrackOsmDateDelta.setText(DSTY.textFormatBlackNormal.replace('%TEXT%', '. . .'))
			DSTY.setStyleWarningLabel(self.buttonTrackOsmDateDelta, 'Normal')
			self.buttonTrackOsmDelta.setText(DSTY.textFormatBlackNormal.replace('%TEXT%', '. . .'))
			DSTY.setStyleWarningLabel(self.buttonTrackOsmDelta, 'Normal')
	
	def buttonOsmDownload_clicked(self):
		if self.trackCodeForOsm == None: self.mainFrame.setStatusWarning('Sélectionnez au préalable un parcours GR dans la table !') ; return
		if self.trackOsmidForOsm == None: self.mainFrame.setStatusWarning('Le numéro de relation Osm n\'est pas défini dans la table Parcours-GR !') ; return
		SOSMD.downloadRelation(self.mainFrame, TCOD.projectFromTrackCode(self.trackCodeForOsm), self.trackCodeForOsm, self.trackOsmidForOsm)

	def buttonOsmCreate_clicked(self):
		if self.trackCodeForOsm == None: self.mainFrame.setStatusWarning('Sélectionnez au préalable un parcours GR dans la table !') ; return
		if self.trackOsmidForOsm == None: self.mainFrame.setStatusWarning('Le numéro de relation Osm n\'est pas défini dans la table Parcours-GR !') ; return
		delta = SOSMC.createRelation(self.iface, self.mainFrame, TCOD.projectFromTrackCode(self.trackCodeForOsm), self.trackCodeForOsm, self.trackOsmidForOsm)

		if delta != None:
			timeStamp = TDAT.getTimeStamp()	
			self.dicoProductsOsm[self.trackCodeForOsm]['Delta Osm Relation'] = str(round(delta))
			self.dicoProductsOsm[self.trackCodeForOsm]['Date Osm Relation'] = timeStamp
			self.recordDeltaOsm(timeStamp, delta)
			text = DSTY.textFormatBlackNormal.replace('%TEXT%', timeStamp[0:10])
			self.buttonTrackOsmDateDelta.setText(text)
			DSTY.setStyleOkLabel(self.buttonTrackOsmDateDelta, 'Normal', strong = True)
			text = DSTY.textFormatBlackNormal.replace('%TEXT%', '{:.1f} mètres'.format(delta).replace('.',','))
			self.buttonTrackOsmDelta.setText(text)
			DSTY.setStyleOkLabel(self.buttonTrackOsmDelta, 'Normal', strong = True)
			
	def recordDeltaOsm(self, timeStamp, delta):
			deltaRecordPath = QGP.pathDeliveriesCoordinationOSM + C_deltaPathFileDelivery
			if TFIL.ensure_dir(deltaRecordPath) :
				fileInfoName = self.dicoProductsOsm[self.trackCodeForOsm]['Nom'] + '.' + C_extensionFileOsmDelta
				fileOut = open(deltaRecordPath + fileInfoName, 'w', encoding='utf-8', errors='ignore')
				fileOut.write(timeStamp + ' - ' + QgsApplication.userFullName() + ' - ' + str(int(delta))+ QGP.configCSVNewLine)
				fileOut.close()
				self.mainFrame.setStatusDone('Delta Osm-GR enregistré : ' + str(delta) + ' mètres')
			else:
				self.mainFrame.setStatusWarning('Impossible de créer le répertoire : ' + deltaRecordPath, 2000)	
	
		
# ========================================================================================
#	Changes Date Knooppuntnet when double-clic // Zoom to track when double clic on code
# ========================================================================================
	
	def productOsmItem_itemDoubleClicked(self, item):	
		if QgsApplication.userFullName() not in QGP.authorizedUserListDeliveryOsm :
			self.mainFrame.setStatusWarning('Utilisateur non autorisé : ' + QgsApplication.userFullName())
			return
		trackCode = self.groupBoxProductsOsmTable.item(item.row(), CO_colTrackCode).text()
		label = QGP.productsTableQViewOSM[item.column()][QGP.C_productsTableQView_ColName]
		self.changeProductOsmTableElement(trackCode, label, item)	
	
	def changeProductOsmTableElement(self, trackCode, label, item):
		self.activeItemForChange = item		
		self.activeCodeForChange = trackCode

		if label == QGP.tableProductsFieldTrackDateKpn:
			if self.dicoProductsOsm[trackCode]['Date Osm'] == '':
				self.mainFrame.setStatusWarning('Le fichier GPX n\'a pas été livré !')
				self.activeItemForChange = None
			else:	
				self.dateInputWindow = TINP.inputFromText(self.iface, self, 'Parcours = ' + trackCode + ' : Modifier la date knooppuntnet', ['Date Knooppuntnet'], [TDAT.getTimeStamp()], self.changeKnooppuntnetDate)	

		elif label == QGP.tableProductsFieldTrackCode:
			self.layerTracksGR.removeSelection()
			self.layerTracksGR.selectByIds( [ self.mainFrame.dicoTracksGRFeatures[trackCode].id() ] )
			self.iface.mapCanvas().zoomToSelected(self.layerTracksGR)		
			self.layerTracksGR.removeSelection()
			self.mainFrame.setStatusInfo('Zoom sur le Parcours : ' + trackCode)

		else:
			self.mainFrame.setStatusOk('Double-clic non défini sur cette colonne')
			self.activeItemForChange = None

	def changeKnooppuntnetDate(self, status, newDateList):
		if status :
			self.dicoProductsOsm[self.activeCodeForChange]['Date Kpn'] = newDateList[0]
			self.activeItemForChange.setText(newDateList[0])
			self.colorProductsOsmTable()
			dateKpnRecordPath = QGP.pathDeliveriesCoordinationOSM + C_kpnPathFileDelivery
			if TFIL.ensure_dir(dateKpnRecordPath) :
				fileInfoName = TFIL.changeFileExtension(self.dicoProductsOsm[self.activeCodeForChange]['File Osm'], C_extensionFileDeliveryKpnDate)
				fileOut = open(dateKpnRecordPath + fileInfoName, 'w', encoding='utf-8', errors='ignore')
				fileOut.write(newDateList[0] + ' - ' + QgsApplication.userFullName() + QGP.configCSVNewLine)
				fileOut.close()
				self.mainFrame.setStatusDone('Date Knooppuntnet modifiée : ' + str(newDateList[0]))
				TLOG.appendInfoInLogfile('DeliveryOsm', [self.activeCodeForChange, 'Livraison Knooppuntnet'])
			else:
				self.mainFrame.setStatusWarning('Impossible de créer le répertoire : ' + dateKpnRecordPath, 2000)
		else:
			self.mainFrame.setStatusOk('Date Knooppuntnet - Annulation') ; return

		self.activeItemForChange = None		
		self.activeCodeForChange = None
		del self.dateInputWindow


# ========================================================================================
#	Info si Osm item right clicked
# ========================================================================================
	
	def productOsmItem_rightClicked(self, point):
		if point == None: return
		item = self.groupBoxProductsOsmTable.itemAt(point)
		if item == None: return
		trackCode = self.groupBoxProductsOsmTable.item(item.row(), CO_colTrackCode).text()
		
		if item.column() == CO_colStampCarto :
			if not os.path.isdir(self.dicoProductsOsm[trackCode]['Path Y']) : 
				self.mainFrame.setStatusInfo(trackCode + ' : le répertoire sur Y: n\'existe pas !')
				return
			THEL.viewFolderExplorer(self.mainFrame, self.dicoProductsOsm[trackCode]['Path Y'])			

		elif item.column() == CO_colStampOsm :
			if not os.path.isdir(self.dicoProductsOsm[trackCode]['Path Osm']) : 
				self.mainFrame.setStatusInfo(trackCode + ' : le répertoire ' + QGP.pathDeliveriesCoordinationOSM + ' n\'existe pas ???')
				return
			THEL.viewFolderExplorer(self.mainFrame, self.dicoProductsOsm[trackCode]['Path Osm'])			

		elif item.column() == CO_colTrackCode :
			QgsExpressionContextUtils.setProjectVariable(QgsProject.instance(),QGP.tableTracksProjectVariableHighlight, trackCode)		
			self.iface.mapCanvas().refreshAllLayers()
			QgsApplication.processEvents()
			self.mainFrame.setStatusInfo('Parcours ' + trackCode + ' : le parcours tel qu\'enregistré est surligné ... ')
			return

		else:
			self.mainFrame.setStatusOk('Clic-droit non défini sur cette colonne')

	
# ========================================================================================
#	Copies Y > Osm
# ========================================================================================

	def deliveryOsm_clicked(self):

		if QgsApplication.userFullName() not in QGP.authorizedUserListDeliveryOsm :
			self.mainFrame.setStatusWarning('Utilisateur non autorisé : ' + QgsApplication.userFullName())
			return

		if not self.deliveryTopoLockButton.isChecked():
			self.mainFrame.setStatusWarning('La Livraison n\'est pas activée !')
			return
		self.mainFrame.setStatusWorking('Copie des fichiers pour livraison ...')

		countCopy = 0

		for row in range(self.groupBoxProductsOsmTable.rowCount()):
			if not self.groupBoxProductsOsmTable.item(row, CO_colCheckOsm).checkState() == Qt.Checked: continue			# Not requested for copy
			trackCode = self.groupBoxProductsOsmTable.item(row, CO_colTrackCode).text()
			trackName = self.groupBoxProductsOsmTable.item(row, CO_colTrackName).text()
			pathY = self.dicoProductsOsm[trackCode]['Path Y']
			fileY = self.dicoProductsOsm[trackCode]['File Y']
			pathOsm = self.dicoProductsOsm[trackCode]['Path Osm']

			status, count = TFIL.copy_files(pathY, pathOsm, fileY)														# Copier le fichier
			if not status or count != 1: self.mainFrame.setStatusError('Impossible de copier le ficher : ' + fileY, False) ; return
	
			self.dicoProductsOsm[trackCode]['Date Osm'] = self.dicoProductsOsm[trackCode]['Date Y']
			self.dicoProductsOsm[trackCode]['Delta Osm'] = self.dicoProductsOsm[trackCode]['Delta Y']
			
			TLOG.appendInfoInLogfile('DeliveryOsm', [trackCode, trackName, 'Livraison Y > Osm'])
			
			countCopy += 1
	
		self.initializeProductsOsmTable()
		self.colorProductsOsmTable()
		self.showDeliveryOsmCounts()

		self.deliveryTopoLockButton.setCheckState(Qt.Unchecked)	
		self.deliveryTopoForceButton.setCheckState(Qt.Unchecked)					
	
		if countCopy > 0:	
			self.mainFrame.setStatusDone('Copie vers le Drive Osm : '  + str(countCopy) + ' fichiers - OK')
		else:
			self.mainFrame.setStatusWarning('Aucun fichier n\'a été copié !')


# ========================================================================================
#	Génération CSV si right clic
# ========================================================================================

	def createOSMView_rightClicked(self):
	
#	Vérifications préliminaires

		if self.viewMode != 'OSM' : return
		if self.groupBoxProductsOsmTable.rowCount() == 0: return
		self.mainFrame.setStatusWorking('Table des livraisons Osm : génération du rapport CSV ...')
	
#	Nom du fichier Rapport

		filePath = QGP.pathDeliveriesCoordinationOSMCSV	
		fileName = (self.typeSelected if self.itineraryCombo.currentText() == C_TextTousItineraries else self.itineraryCombo.currentText()) + ' - Synchronisation Knooppuntnet (' + TDAT.getTimeStamp() + ').csv'

#	Extraire les données

		headers = [QGP.tableProductsFieldTrackCode, QGP.tableProductsFieldTrackName, QGP.tableProductsFieldTrackOsmid, \
						QGP.tableProductsFieldTrackDateDB, QGP.tableProductsFieldTrackDateOsm, QGP.tableProductsFieldTrackDeltaOsm, QGP.tableProductsFieldTrackDateKpn ]
						
		data = [ [self.groupBoxProductsOsmTable.item(row,col).text() for col in [CO_colTrackCode, CO_colTrackName, CO_colOsmid, CO_colStampDB, CO_colStampOsm, CO_colDeltaOsm, CO_colStampKpn] ] \
						for row in range(self.groupBoxProductsOsmTable.rowCount()) ]
		
#	Créer le fichier Rapport

		TCSV.exportOsmDeliveryData(filePath, fileName, headers, data)

#	Montrer le rapport

		textInfo = 'Rapport sur ' + QGP.pathDeliveriesCoordinationOSMCSV 
		THEL.viewCsvOnBrowser(self.mainFrame, textInfo, filePath + fileName)

#	Terminé

		self.mainFrame.setStatusDone('Table des livraisons Osm : génération du rapport CSV - OK')


# ========================================================================================
# ========================================================================================
#
# Actions de livraison
# 
# ========================================================================================
# ========================================================================================

# ========================================================================================
#	Livraison - Copie des fichiers - depuis la version locale vers le drive carto
# ========================================================================================
	
	def deliveryCarto_clicked(self):
		if not self.deliveryCartoLockButton.isChecked():
			self.mainFrame.setStatusWarning('La Livraison n\'est pas activée !')
			return
		self.mainFrame.setStatusWorking('Copie des fichiers pour livraison ...')
		
		colCheckCarto = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldCopyCarto)
		colItinerary = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldItineraryCode)
		colBaseName = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldFileName)
		countCopy = 0

		for row in range(self.groupBoxProductsTable.rowCount()):
			if not self.groupBoxProductsTable.item(row, colCheckCarto).checkState() == Qt.Checked: continue				# Not requested for copy
			product = self.groupBoxProductsTable.item(row, colItinerary).text()
			baseName = self.groupBoxProductsTable.item(row, colBaseName).text()		
			if C_dicoProduct_localFileX not in self.dicoProductsList[product][baseName]: continue						# No local file - should normally not happen - check cleared before
			fileName = self.dicoProductsList[product][baseName][C_dicoProduct_localFileX]
			filePath = self.dicoProductsList[product][baseName][C_dicoProduct_localPathX]
			dstPath = self.deliveryCartoPath.replace('%PROJECT%', product)												# Détermination du path destination Y:
			if not TFIL.ensure_dir(dstPath)	:																			# Créer le répertoire si nécessaire
				self.mainFrame.setStatusError('Impossible de créer le répertoire : ' + dstPath, False)
				return
			TFIL.remove_files(dstPath, baseName, len(fileName))																									# Supprimer les fichiers avec un nom identique (plus vieux fichiers)
			TFIL.remove_files(dstPath + DTOP.subPathFileDelivery, baseName, len(TFIL.changeFileExtension(fileName, DTOP.extensionFileDeliveryCartoDate)))		# Supprimer les fichiers avec un nom identique - idem .QCarto
			status, count = TFIL.copy_files(filePath, dstPath, fileName)																						# Copier le fichier
			if status and count == 1:
				self.recordDeliveryInfoFile(dstPath, fileName, DTOP.extensionFileDeliveryCartoDate )															# Noter sur le drive carto la livraison
				TLOG.appendInfoInLogfile('DeliveryCarto', [fileName, dstPath, 'OK - Livraison X > Y '])
				countCopy += 1
			else:
				self.mainFrame.setStatusError('Impossible de copier le ficher : ' + fileName, False)
				TLOG.appendInfoInLogfile('DeliveryCarto', [fileName, dstPath, '? ERREUR ? - Livraison X > Y'])
				return

		# Rafraichir la table en relisant le répertoire de destination
				
		self.generateDicoProductsCartoList(self.deliveryCartoPath, self.deliveryFileTypeList, self.deliveryPrefixList)
		self.initializeProductsTable()
		self.colorProductTable()
		self.showDeliveryCartoCounts()
		self.deliveryCartoLockButton.setCheckState(Qt.Unchecked)	
		self.deliveryCartoForceButton.setCheckState(Qt.Unchecked)					

		if countCopy > 0:
			self.mainFrame.setStatusDone('Copie vers le Drive Carto : ' + str(countCopy) + ' fichiers - OK')
		else:
			self.mainFrame.setStatusWarning('Aucun fichier n\'a été copié !')
		
	
# ========================================================================================
#	Livraison - Copie des fichiers - depuis le drive carto vers le drive topo
# ========================================================================================

	def deliveryTopo_clicked(self):
		if self.viewMode == 'OSM' : self.deliveryOsm_clicked() ; return
	
		if not self.deliveryTopoLockButton.isChecked():
			self.mainFrame.setStatusWarning('La Livraison n\'est pas activée !')
			return
		self.mainFrame.setStatusWorking('Copie des fichiers pour livraison ...')
				
		colCheckTopo  = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldCopyTopo)
		colItinerary = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldItineraryCode)
		colBaseName = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldFileName)
		countCopy = 0

		for row in range(self.groupBoxProductsTable.rowCount()):
			if not self.groupBoxProductsTable.item(row, colCheckTopo).checkState() == Qt.Checked: continue				# Not requested for copy
			product = self.groupBoxProductsTable.item(row, colItinerary).text()
			baseName = self.groupBoxProductsTable.item(row, colBaseName).text()		
			if C_dicoProduct_cartoFileY not in self.dicoProductsList[product][baseName]: continue						# No carto file - should normally not happen - check cleared before
			if not self.dicoProductsList[product][baseName][C_dicoProduct_topoFolderOpen]: continue						# Topo folder does not exist
			fileName = self.dicoProductsList[product][baseName][C_dicoProduct_cartoFileY]
			filePath = self.dicoProductsList[product][baseName][C_dicoProduct_cartoPathY]
			dstPath  = self.dicoProductsList[product][baseName][C_dicoProduct_topoPathZ]							
			if '-Draft' in fileName : continue																			# Le fichiers draft ne sont livrés
			
			newBaseName = baseName																						# By default
			newFileName = fileName

			if self.typeSelected in QGP.typeSetModeGR and dstPath == QGP.pathDeliveriesSiteGR:							# Case of GR.P.T GPX : compact file name for retrocompatibilty
				prefixAndBaseName, timeStamp, u3 = TFIL.splitFileName(fileName)	
				prefix, u2, u3 = TFIL.splitFileBaseName(prefixAndBaseName)
				if self.mainFrame.debugModeQCartoLevel >= 2: print ('deliveryTopo_clicked - prefix : >>>' + prefix + '<<<')
				if prefix == DTOP.prefixGPX :
					trackName = ' - '.join(prefixAndBaseName.split(' - ')[1:])														# Must remove prefix												
					trackCode = self.dicoTracksName2CodeGR[trackName] if trackName in self.dicoTracksName2CodeGR else 'GR-???'		# Retrieve original track code
					nameGPX = TGPX.defineTrackNameGPX(trackCode, trackName, True)													# Retrieve retrocompatibility name
					newBaseName = nameGPX
					newFileName = nameGPX + '_' + timeStamp[0:10] + '.gpx'
					if self.mainFrame.debugModeQCartoLevel >= 2 : print ('deliveryTopo_clicked : ' + fileName + ' >>> ' + newFileName)
				elif prefix == DTOP.prefixHtml :
					newBaseName = ' - '.join(baseName.split(' - ')[1:])
					newFileName = ' - '.join(fileName.split(' - ')[1:])
			
			TFIL.remove_files(dstPath, newBaseName, len(newFileName))																							# Supprimer les fichiers avec un nom identique (plus vieux fichiers)					
			TFIL.remove_files(filePath + DTOP.subPathFileDelivery, baseName, len(TFIL.changeFileExtension(fileName, DTOP.extensionFileDeliveryTopoDate)))		# Supprimer les fichiers avec un nom identique - idem .QTopo
			status, count = TFIL.copy_files(filePath, dstPath, fileName, newFileName)																			# Copier le fichier
			if status and count == 1:
				self.recordDeliveryInfoFile(filePath, fileName, DTOP.extensionFileDeliveryTopoDate )															# Noter sur le drive carto la livraison
				TLOG.appendInfoInLogfile('DeliveryTopo', [fileName, dstPath, newFileName, 'OK - Livraison Y > Z'])
				countCopy += 1
			else:	
				self.mainFrame.setStatusError('Impossible de copier le ficher : ' + newFileName, False)
				TLOG.appendInfoInLogfile('DeliveryTopo', [fileName, dstPath, newFileName, '? ERREUR ? - Livraison Y > Z'])
				
#			Tourner la carte en mode portrait				
				
			prefixAndBaseName, u2, u3 = TFIL.splitFileName(fileName)	
			prefix, u2, u3 = TFIL.splitFileBaseName(prefixAndBaseName)
			if prefix == DTOP.prefixMapsPDF:
				print('AAA = ' + dstPath + newFileName)
				orientation = TIMG.getImageFileOrientation(dstPath + newFileName)
				print('BBB = ' + dstPath + newFileName + ' - ' + str(orientation))
				if orientation == 'W' and not TIMG.rotate90ImageFile(dstPath + newFileName):
					self.mainFrame.setStatusWarning(newFileName + ' : la rotation du fichier a échoué !', 1500)
				
		# Rafraichir la table en relisant le répertoire de destination
				
		self.generateDicoProductsCartoList(self.deliveryCartoPath, self.deliveryFileTypeList, self.deliveryPrefixList)
		self.initializeProductsTable()
		self.colorProductTable()
		self.showDeliveryTopoCounts()
		self.deliveryTopoLockButton.setCheckState(Qt.Unchecked)	
		self.deliveryTopoForceButton.setCheckState(Qt.Unchecked)					
	
		if countCopy > 0:	
			self.mainFrame.setStatusDone('Copie vers le Drive Topo : '  + str(countCopy) + ' fichiers - OK')
		else:
			self.mainFrame.setStatusWarning('Aucun fichier n\'a été copié !')


# ========================================================================================
#	Livraison - Création du fichier date de livraison sur le drive Carto
# ========================================================================================

	def recordDeliveryInfoFile(self, srcPath, fileName, extension):
		recordPath = srcPath + DTOP.subPathFileDelivery
		if TFIL.ensure_dir(recordPath) :
			fileInfoName = TFIL.changeFileExtension(fileName, extension)
			fileOut = open(recordPath + fileInfoName, 'w', encoding='utf-8', errors='ignore')
			fileOut.write(TDAT.getTimeStamp() + ' - ' + QgsApplication.userFullName() + QGP.configCSVNewLine)
			fileOut.close()
		else:
			self.mainFrame.setStatusWarning('Impossible de créer le répertoire : ' + recordPath, 2000)
			
	
# ========================================================================================
#	Info si item clicked
# ========================================================================================
	
	def productItem_clicked	(self, item):
		code = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView][item.column()]
		colItinerary = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldItineraryCode)
		colBaseName = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldFileName)
		colStampLocal = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldDateLocal)
		colStampCarto = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldDateCarto)
		colStampTopo  = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldDateTopo)
		product = self.groupBoxProductsTable.item(item.row(), colItinerary).text()
		baseName = self.groupBoxProductsTable.item(item.row(), colBaseName).text()

		if code in (QGP.tableProductsFieldFileName) :																	
			if C_dicoProduct_localFileX not in self.dicoProductsList[product][baseName]:
				self.mainFrame.setStatusInfo(baseName + ' : ce fichier n\'existe pas en local sur ' + QGP.configPathProject)
				return
			fileName = self.dicoProductsList[product][baseName][C_dicoProduct_localFileX]
			filePath = self.dicoProductsList[product][baseName][C_dicoProduct_localPathX]
			textInfo = 'Fichier source local sur ' + QGP.configPathProject 
			if 	'png' in self.deliveryFileTypeList : THEL.viewMapOnBrowser(self.mainFrame, textInfo, filePath + fileName)
			if 	'csv' in self.deliveryFileTypeList : THEL.viewCsvOnBrowser(self.mainFrame, textInfo, filePath + fileName)
			if  'html' in self.deliveryFileTypeList and fileName[-5:] == '.html' : THEL.viewHtmlOnBrowser(self.mainFrame, textInfo, filePath + fileName)
			if 	'gpx' in self.deliveryFileTypeList and fileName[-4:] == '.gpx' : self.showGPXRubberBand(filePath, fileName)

		if code in (QGP.tableProductsFieldDateCarto) :
			stampCarto = self.groupBoxProductsTable.item(item.row(), colStampCarto).text()
			if stampCarto == '' : self.mainFrame.setStatusInfo('Ce fichier n\'a pas été livré sur Y: !'); return
			if self.dicoProductsList[product][baseName][C_dicoProduct_infoCartoName] == None: self.mainFrame.setStatusWarning('Le fichier livraison n\'existe pas (il devrait) !'); return	
			if self.dicoProductsList[product][baseName][C_dicoProduct_infoCartoName] == False: self.mainFrame.setStatusWarning('Le fichier livraison est corrompu !'); return	
			self.mainFrame.setStatusInfo('Livraison sur le drive Carto par : ' + self.dicoProductsList[product][baseName][C_dicoProduct_infoCartoName] + ' - ' + self.dicoProductsList[product][baseName][C_dicoProduct_infoCartoDate])

		if code in (QGP.tableProductsFieldDateTopo) :
			stampTopo = self.groupBoxProductsTable.item(item.row(), colStampTopo).text()
			if stampTopo == '' : self.mainFrame.setStatusInfo('Ce fichier n\'a pas été livré sur Z: !'); return
			if self.dicoProductsList[product][baseName][C_dicoProduct_infoTopoName] == None: self.mainFrame.setStatusWarning('Le fichier livraison n\'existe pas (il devrait) !'); return	
			if self.dicoProductsList[product][baseName][C_dicoProduct_infoTopoName] == False: self.mainFrame.setStatusWarning('Le fichier livraison est corrompu !'); return	
			self.mainFrame.setStatusInfo('Livraison sur le drive Topo par : ' + self.dicoProductsList[product][baseName][C_dicoProduct_infoTopoName] + ' - ' + self.dicoProductsList[product][baseName][C_dicoProduct_infoTopoDate])

		if code in (QGP.tableProductsFieldOpenTopo) :
			deliveryPath  = self.dicoProductsList[product][baseName][C_dicoProduct_topoPathZ]
			self.mainFrame.setStatusInfo(deliveryPath)

		if code in (QGP.tableProductsFieldItineraryCode, QGP.tableProductsFieldDateLocal) :
			self.mainFrame.setStatusOk('Prêt')


	def showGPXRubberBand(self, filePath, fileName):
		self.rubberBandGPX.clearRubberBand()
		if self.rubberBandLastFileName == fileName: self.rubberBandLastFileName = None; return
		trackLine, wayPoints, wayPois, errorText = TGPX.importGpxTrack(filePath + fileName)
		if errorText != None: self.mainFrame.setStatusWarning(fileName + ' : ' + errorText); return			
		self.rubberBandGPX.refreshRubberBand(trackLine, wayPoints, wayPois)
		self.rubberBandLastFileName = fileName
		self.iface.mapCanvas().setExtent(TGEO.enlargeRectangle(QgsGeometry.fromPolylineXY(trackLine).boundingBox(),1000))
		self.mainFrame.setStatusInfo(fileName + ' : Le tracé réel du GPX est surligné en vert')	


# ========================================================================================
#	Info si item right clicked
# ========================================================================================
	
	def productItem_rightClicked(self, point):
		if point == None: return
		item = self.groupBoxProductsTable.itemAt(point)
		if item == None: return
		
		code = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView][item.column()]
		colItinerary = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldItineraryCode)
		colBaseName = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldFileName)
		colStampLocal = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldDateLocal)
		colStampCarto = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldDateCarto)
		colStampTopo  = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldDateTopo)

		product = self.groupBoxProductsTable.item(item.row(), colItinerary).text()
		baseName = self.groupBoxProductsTable.item(item.row(), colBaseName).text()
		
		if code in (QGP.tableProductsFieldFileName) :
			if C_dicoProduct_cartoFileY not in self.dicoProductsList[product][baseName]:
				self.mainFrame.setStatusInfo(baseName + ' : ce fichier n\'a pas été partagé sur ' + QGP.pathDeliveriesCarto)
				return
			fileName = self.dicoProductsList[product][baseName][C_dicoProduct_cartoFileY]
			filePath = self.dicoProductsList[product][baseName][C_dicoProduct_cartoPathY]
			textInfo = 'Fichier partagé carto sur ' + QGP.pathDeliveriesCarto 
			if 	'png' in self.deliveryFileTypeList : THEL.viewMapOnBrowser(self.mainFrame, textInfo, filePath + fileName)
			if 	'csv' in self.deliveryFileTypeList : THEL.viewCsvOnBrowser(self.mainFrame, textInfo, filePath + fileName)
			if  'html' in self.deliveryFileTypeList and fileName[-5:] == '.html' : THEL.viewHtmlOnBrowser(self.mainFrame, textInfo, filePath + fileName)
			if 	'gpx' in self.deliveryFileTypeList and fileName[-4:] == '.gpx' : self.showGPXRubberBand(filePath, fileName)

		if code in (QGP.tableProductsFieldDateLocal) :
			if C_dicoProduct_localPathX not in self.dicoProductsList[product][baseName]:
				self.mainFrame.setStatusInfo(baseName + ' : ce fichier n\'existe pas en local sur ' + QGP.configPathProject)
				return
			THEL.viewFolderExplorer(self.mainFrame, self.dicoProductsList[product][baseName][C_dicoProduct_localPathX])			

		if code in (QGP.tableProductsFieldDateCarto) :
			if C_dicoProduct_cartoPathY not in self.dicoProductsList[product][baseName]:
				self.mainFrame.setStatusInfo(baseName + ' : ce fichier n\'a pas été partagé sur ' + QGP.pathDeliveriesCarto)
				return
			THEL.viewFolderExplorer(self.mainFrame, self.dicoProductsList[product][baseName][C_dicoProduct_cartoPathY])			
				
		if code in (QGP.tableProductsFieldDateTopo) :
			if C_dicoProduct_topoPathZ not in self.dicoProductsList[product][baseName]:
				self.mainFrame.setStatusInfo(baseName + ' : ce fichier n\'a pas été livré sur ' + QGP.pathDriveTopo)
				return
			THEL.viewFolderExplorer(self.mainFrame, self.dicoProductsList[product][baseName][C_dicoProduct_topoPathZ])			

		if code in (QGP.tableProductsFieldItineraryCode) :
			self.mainFrame.setStatusOk('Prêt')


# ========================================================================================
#	Auto Select if Header clicked
# ========================================================================================

	def tableHeader_clicked(self, index):
		colStampLocal = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldDateLocal)
		colStampCarto = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldDateCarto)
		colStampTopo  = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldDateTopo)
		colCheckCarto = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldCopyCarto)
		colCheckTopo  = [ _[QGP.C_productsTableQView_ColName] for _ in QGP.productsTableQView].index(QGP.tableProductsFieldCopyTopo)

		if index == colCheckCarto:
			for row in range(self.groupBoxProductsTable.rowCount()):
				timeStampLocal = self.groupBoxProductsTable.item(row, colStampLocal).text()
				timeStampCarto = self.groupBoxProductsTable.item(row, colStampCarto).text()
				self.groupBoxProductsTable.item(row, colCheckCarto).setCheckState(Qt.Checked if (TDAT.isTimeStampToday(timeStampLocal) and not TDAT.isTimeStampToday(timeStampCarto)) else Qt.Unchecked)
			self.groupBoxProductsTable.clearSelection()
	
		if index == colCheckTopo:
			for row in range(self.groupBoxProductsTable.rowCount()):
				timeStampCarto = self.groupBoxProductsTable.item(row, colStampCarto).text()
				timeStampTopo = self.groupBoxProductsTable.item(row, colStampTopo).text()
				self.groupBoxProductsTable.item(row, colCheckTopo).setCheckState(Qt.Checked if (TDAT.isTimeStampToday(timeStampCarto) and not TDAT.isTimeStampToday(timeStampTopo)) else Qt.Unchecked)
			self.groupBoxProductsTable.clearSelection()
		
	
# ========================================================================================
# ========================================================================================
#
# Création des différents cadres Menu
# 
# ========================================================================================
# ========================================================================================

# ========================================================================================
# Cadre : Sélection
# ========================================================================================

	def menuBoxSelection(self):
	
		groupBoxSelection = QtWidgets.QGroupBox('Choix du produit à livrer', self.mainMenu)
		groupBoxSelection.setStyleSheet(DSTY.styleBox)
		
#	Créer un bouton Radio pour chaque type d'itinéraire

		TBUT.createLabelBlackButton(groupBoxSelection, 1, 1, 'Choix Itinéraire', 'Normal', 'Normal')

		buttonRadioGR  = TBUT.createRadioBoxButton(groupBoxSelection, 2.6, 1, 'GR'  , 'Compact3_2')
		buttonRadioGRP = TBUT.createRadioBoxButton(groupBoxSelection, 3.3, 1, 'GRP' , 'Compact3_2')
		buttonRadioGRT = TBUT.createRadioBoxButton(groupBoxSelection, 4.1, 1, 'GRT' , 'Compact3_2')
		buttonRadioRI  = TBUT.createRadioBoxButton(groupBoxSelection, 4.8, 1, 'RI'  , 'Compact3_2')
		buttonRadioRL  = TBUT.createRadioBoxButton(groupBoxSelection, 5.6, 1, 'RL'  , 'Compact3_2')
		buttonRadioRB  = TBUT.createRadioBoxButton(groupBoxSelection, 6.4, 1, 'RB'  , 'Compact3_2')
		buttonRadioRF  = TBUT.createRadioBoxButton(groupBoxSelection, 7.2, 1, 'RF'  , 'Compact3_2')
		buttonRadioIR  = TBUT.createRadioBoxButton(groupBoxSelection, 8.0, 1, 'IR'  , 'Compact3_2')

		buttonRadioGR.clicked.connect(self.buttonRadioGR_clicked)
		buttonRadioGRP.clicked.connect(self.buttonRadioGRP_clicked)
		buttonRadioGRT.clicked.connect(self.buttonRadioGRT_clicked)
		buttonRadioRI.clicked.connect(self.buttonRadioRI_clicked)
		buttonRadioRL.clicked.connect(self.buttonRadioRL_clicked)
		buttonRadioRB.clicked.connect(self.buttonRadioRB_clicked)
		buttonRadioRF.clicked.connect(self.buttonRadioRF_clicked)
		buttonRadioIR.clicked.connect(self.buttonRadioIR_clicked)
		
#	Créer un menu déroulant pour le choix de l'itinéraire et la sélection

		self.itineraryCombo = TBUT.createComboButton(groupBoxSelection, 7, 1, 'Normal')
	
#	Créer un checkbox pour include draft ou non

		self.draftCheckBox = TBUT.createCheckBoxButton(groupBoxSelection, 8, 1, 'Drafts', 'Normal')
		self.draftCheckBox.setCheckState(Qt.Unchecked)
	
#	Créer les boutons d'action	

		TBUT.createLabelBlackButton(groupBoxSelection, 1, 2, 'Voir les Produits', 'Normal', 'Normal')
	
		self.buttonShowMaps = TBUT.createActionButton(groupBoxSelection, 2, 2, 'Cartes', 'Normal')
		self.buttonShowMaps.clicked.connect(self.createMapsView)		
	
		self.buttonShowSchemas = TBUT.createActionButton(groupBoxSelection, 3, 2, 'Schémas', 'Normal')
		self.buttonShowSchemas.clicked.connect(self.createSchemaView)		

		self.buttonShowDistances = TBUT.createActionButton(groupBoxSelection, 4, 2, 'Distances', 'Normal')
		self.buttonShowDistances.clicked.connect(self.createDistancesView)		
	
		self.buttonShowProfiles = TBUT.createActionButton(groupBoxSelection, 5, 2, 'Profils', 'Normal')
		self.buttonShowProfiles.clicked.connect(self.createProfilesView)			
	
		self.buttonShowGPX = TBUT.createActionButton(groupBoxSelection, 6, 2, 'GPX', 'Normal')
		self.buttonShowGPX.clicked.connect(self.createGPXView)				

		self.buttonShowGPXSityTrail = TBUT.createActionButton(groupBoxSelection, 7, 2, 'GPX SityTrail', 'Normal')
		self.buttonShowGPXSityTrail.clicked.connect(self.createGPXSityTrailView)				
	
		self.buttonShowOSM = TBUT.createActionButton(groupBoxSelection, 8, 2, 'GPX OSM', 'Normal')
		self.buttonShowOSM.clicked.connect(self.createOSMView)					
		self.buttonShowOSM.setContextMenuPolicy(Qt.CustomContextMenu)
		self.buttonShowOSM.customContextMenuRequested.connect(self.createOSMView_rightClicked)		
	
# 	Terminé

		groupBoxSelection.repaint()

		return groupBoxSelection

	
# ========================================================================================
# Cadre : Cadre de la Table des Produits
# ========================================================================================

	def menuBoxTableProductsFrame(self):
	
		groupBoxProductsFrame = QtWidgets.QGroupBox('Table des Produits', self.mainMenu)
		groupBoxProductsFrame.setStyleSheet(DSTY.styleBox)

		groupBoxProductsFrame.repaint()

		return groupBoxProductsFrame
	
	
# ========================================================================================
# Cadre : Table des Produits
# ========================================================================================

	def menuBoxTableProductsView(self):

		groupBoxProductsView = QtWidgets.QTableWidget(0,len(QGP.productsTableQView), self.mainMenu)
		groupBoxProductsView.setStyleSheet(DSTY.styleBox)

		DSTY.setStyleTableTraces(groupBoxProductsView)

		tableFields = QGP.productsTableQView
		for col in range(len(tableFields)):
			groupBoxProductsView.setHorizontalHeaderItem(col, QtWidgets.QTableWidgetItem(tableFields[col][QGP.C_productsTableQView_ColName]))
			groupBoxProductsView.setColumnWidth(col, tableFields[col][QGP.C_productsTableQView_ColSize])

		groupBoxProductsView.itemChanged.connect(self.productItem_changed)
		groupBoxProductsView.itemClicked.connect(self.productItem_clicked)

		groupBoxProductsView.setContextMenuPolicy(Qt.CustomContextMenu)
		groupBoxProductsView.customContextMenuRequested.connect(self.productItem_rightClicked)		

		groupBoxProductsView.horizontalHeader().sectionClicked.connect(self.tableHeader_clicked)
		
		groupBoxProductsView.repaint()

		return groupBoxProductsView


# ========================================================================================
# Cadre : Table des Produits - Osm
# ========================================================================================

	def menuBoxTableProductsOsmView(self):

		groupBoxProductsOsmView = QtWidgets.QTableWidget(0,len(QGP.productsTableQViewOSM), self.mainMenu)
		groupBoxProductsOsmView.setStyleSheet(DSTY.styleBox)

		DSTY.setStyleTableTraces(groupBoxProductsOsmView)

		tableFields = QGP.productsTableQViewOSM
		for col in range(len(tableFields)):
			groupBoxProductsOsmView.setHorizontalHeaderItem(col, QtWidgets.QTableWidgetItem(tableFields[col][QGP.C_productsTableQView_ColName]))
			groupBoxProductsOsmView.setColumnWidth(col, tableFields[col][QGP.C_productsTableQView_ColSize])

		groupBoxProductsOsmView.itemSelectionChanged.connect(self.productOsmItem_selectionChanged)
		groupBoxProductsOsmView.itemChanged.connect(self.productOsmItem_changed)

		groupBoxProductsOsmView.setContextMenuPolicy(Qt.CustomContextMenu)
		groupBoxProductsOsmView.customContextMenuRequested.connect(self.productOsmItem_rightClicked)		

		groupBoxProductsOsmView.itemDoubleClicked.connect(self.productOsmItem_itemDoubleClicked)


		groupBoxProductsOsmView.horizontalHeader().sectionClicked.connect(self.tableOsmHeader_clicked)
		
		groupBoxProductsOsmView.repaint()

		return groupBoxProductsOsmView


# ========================================================================================
# Cadre : Livraisons Local > Carto
# ========================================================================================

	def menuBoxTableDeliveryCarto(self):

		groupBoxDeliveryCartoView = QtWidgets.QGroupBox('Livraisons vers Drive des Cartos', self.mainMenu)
		groupBoxDeliveryCartoView.setStyleSheet(DSTY.styleBox)

#	Nombre de produits nouveaux / cochés

		TBUT.createLabelBlackButton(groupBoxDeliveryCartoView, 1, 1, 'Nouveaux Produits', 'Normal', 'Normal')
		self.deliveryCartoNewCountInfo = TBUT.createLabelGreenButton(groupBoxDeliveryCartoView, 2, 1, '. . .', 'Normal', 'Normal')

		TBUT.createLabelBlackButton(groupBoxDeliveryCartoView, 1, 2, 'Produits à copier', 'Normal', 'Normal')
		self.deliveryCartoCopyCountInfo = TBUT.createLabelGreenButton(groupBoxDeliveryCartoView, 2, 2, '. . .', 'Normal', 'Normal')

#	Bouton pour Forcer sans Contrôle de Date

		self.deliveryCartoForceButton = TBUT.createCheckBoxButton(groupBoxDeliveryCartoView, 3, 2, 'Forcer', 'Normal')
		self.deliveryCartoForceButton.setCheckState(Qt.Unchecked)	

#	Bouton Activation

		self.deliveryCartoLockButton = TBUT.createCheckBoxButton(groupBoxDeliveryCartoView, 4, 1, 'Activer', 'Normal')
		self.deliveryCartoLockButton.setCheckState(Qt.Unchecked)	

#	Créer les boutons d'action	

		buttonDeliveryCarto = TBUT.createActionButton(groupBoxDeliveryCartoView, 4, 2, 'Livrer !', 'Normal')
		DSTY.setStyleWarningButton(buttonDeliveryCarto)
		buttonDeliveryCarto.clicked.connect(self.deliveryCarto_clicked)		

		groupBoxDeliveryCartoView.repaint()

		return groupBoxDeliveryCartoView


# ========================================================================================
# Cadre : Livraisons Carto > Topo
# ========================================================================================

	def menuBoxTableDeliveryTopo(self):

		groupBoxDeliveryTopoView = QtWidgets.QGroupBox('Livraisons vers Drive du Pôle Topo', self.mainMenu)
		groupBoxDeliveryTopoView.setStyleSheet(DSTY.styleBox)

#	Nombre de produits nouveaux / cochés

		TBUT.createLabelBlackButton(groupBoxDeliveryTopoView, 1, 1, 'Nouveaux Produits', 'Normal', 'Normal')
		self.deliveryTopoNewCountInfo = TBUT.createLabelGreenButton(groupBoxDeliveryTopoView, 2, 1, '. . .', 'Normal', 'Normal')

		TBUT.createLabelBlackButton(groupBoxDeliveryTopoView, 1, 2, 'Produits à copier', 'Normal', 'Normal')
		self.deliveryTopoCopyCountInfo = TBUT.createLabelGreenButton(groupBoxDeliveryTopoView, 2, 2, '. . .', 'Normal', 'Normal')

#	Bouton pour Forcer sans Contrôle de Date

		self.deliveryTopoForceButton = TBUT.createCheckBoxButton(groupBoxDeliveryTopoView, 3, 2, 'Forcer', 'Normal')
		self.deliveryTopoForceButton.setCheckState(Qt.Unchecked)	

#	Bouton Activation

		self.deliveryTopoLockButton = TBUT.createCheckBoxButton(groupBoxDeliveryTopoView, 4, 1, 'Activer', 'Normal')
		self.deliveryTopoLockButton.setCheckState(Qt.Unchecked)	

#	Créer les boutons d'action	

		buttonDeliveryTopo = TBUT.createActionButton(groupBoxDeliveryTopoView, 4, 2, 'Livrer !', 'Normal')
		DSTY.setStyleWarningButton(buttonDeliveryTopo)
		buttonDeliveryTopo.clicked.connect(self.deliveryTopo_clicked)		

		groupBoxDeliveryTopoView.repaint()

		return groupBoxDeliveryTopoView


# ========================================================================================
# Cadre : Relation OSM
# ========================================================================================

	def menuBoxRelationOsm(self):

		groupBoxRelationOsm = QtWidgets.QGroupBox('Parcours : Relation Osm', self.mainMenu)
		groupBoxRelationOsm.setStyleSheet(DSTY.styleBox)

#	Parcours

		self.buttonTrackOsmCode = TBUT.createLabelGreenButton(groupBoxRelationOsm, 1, 1, '. . .', 'Normal')
		DSTY.setStyleWarningLabel(self.buttonTrackOsmCode, 'Normal')

		self.buttonTrackOsmId = TBUT.createLabelGreenButton(groupBoxRelationOsm, 2, 1, '. . .', 'Normal')
		DSTY.setStyleWarningLabel(self.buttonTrackOsmId, 'Normal')

		self.buttonTrackOsmName = TBUT.createLabelGreenButton(groupBoxRelationOsm, 3, 1, '. . .', 'Double')
		DSTY.setStyleWarningLabel(self.buttonTrackOsmName, 'Double')

#	Hausdorff

		self.buttonTrackOsmDateDelta = TBUT.createLabelGreenButton(groupBoxRelationOsm, 1, 2, '. . .', 'Normal')
		DSTY.setStyleWarningLabel(self.buttonTrackOsmDateDelta, 'Normal')

		self.buttonTrackOsmDelta = TBUT.createLabelGreenButton(groupBoxRelationOsm, 2, 2, '. . .', 'Normal')
		DSTY.setStyleWarningLabel(self.buttonTrackOsmDelta, 'Normal')

# 	Boutons

		buttonOsmDownload = TBUT.createActionButton(groupBoxRelationOsm, 3, 2, 'Charger Osm', 'Normal')
		buttonOsmDownload.clicked.connect(self.buttonOsmDownload_clicked)

		buttonOsmCreate = TBUT.createActionButton(groupBoxRelationOsm, 4, 2, 'Créer Osm', 'Normal')
		buttonOsmCreate.clicked.connect(self.buttonOsmCreate_clicked)

# 	Terminé

		groupBoxRelationOsm.repaint()

		return groupBoxRelationOsm		


# ========================================================================================
# --- THE END ---
# ========================================================================================
	
