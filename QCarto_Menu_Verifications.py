# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Gestion des Menus : Page Vérifications
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

import QCarto_Tools_Buttons as TBUT
import QCarto_Tools_Coding as TCOD

import QCarto_Definitions_Colors as DCOL
import QCarto_Definitions_Styles as DSTY

import QCarto_Controls_TracksGR as VTGR
importlib.reload(VTGR)
import QCarto_Controls_TracksRB as VTRB
importlib.reload(VTRB)
import QCarto_Controls_PointsGR as VPGR
importlib.reload(VPGR)
import QCarto_Controls_SectionsGR as VSGR
importlib.reload(VSGR)

import QCarto_Parameters_Global
QGP = QCarto_Parameters_Global.globalParameters()


# ========================================================================================
# Class : menuControlsFrame
# >>> iface
# >>> mainMenu 						: Widget of Main Menu
# >>> mainFrame 					: Main Menu Object
# ========================================================================================

class menuControlsFrame:

	def __init__(self, iface, mainMenu, mainFrame):

# 	Paramètres fournis

		self.iface = iface
		self.mainMenu = mainMenu
		self.mainFrame = mainFrame

#	Nom de la page

		self.pageName = 'Vérifications'

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

		self.groupBoxControlsTracksGR = self.menuBoxControlsTracksGR()
		DSTY.setBoxGeometry(self.groupBoxControlsTracksGR, 1, 4, 8, 6)
		self.boxesList.append(self.groupBoxControlsTracksGR)

		self.groupBoxControlsTracksRB = self.menuBoxControlsTracksRB()
		DSTY.setBoxGeometry(self.groupBoxControlsTracksRB, 1, 11, 8, 6)
		self.boxesList.append(self.groupBoxControlsTracksRB)

		self.groupBoxControlsSectionsGR = self.menuBoxControlsSectionsGR()
		DSTY.setBoxGeometry(self.groupBoxControlsSectionsGR, 1, 18, 8, 4)
		self.boxesList.append(self.groupBoxControlsSectionsGR)

		self.groupBoxControlsPointsGR = self.menuBoxControlsPointsGR()
		DSTY.setBoxGeometry(self.groupBoxControlsPointsGR, 1, 23, 8, 4)
		self.boxesList.append(self.groupBoxControlsPointsGR)


# ========================================================================================
# Actions : A la demande de la fenêtre principale
# ========================================================================================

#	Show - Ouverture de cette fenêtre

	def show(self):
		for box in self.boxesList: box.show(), box.repaint()

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
# Actions : Controles effectifs
# ========================================================================================

	def controlTrackGRSelected(self):
		self.mainFrame.setStatusWorking('Analyse des erreurs dans la table : Parcours-GR pour les parcours sélectionnés ...')
		VTGR.analyseTracksGR(self.mainFrame, self, self.dicoBoutonsErreursTracksGR, False)
		self.mainFrame.setStatusDone('Analyse des erreurs dans la table : Parcours-GR - Terminé')

	def controlTrackGRAll(self):
		self.mainFrame.setStatusWorking('Analyse des erreurs dans la table : Parcours-GR pour tous les parcours ...')
		VTGR.analyseTracksGR(self.mainFrame, self, self.dicoBoutonsErreursTracksGR, True)
		self.mainFrame.setStatusDone('Analyse des erreurs dans la table : Parcours-GR - Terminé')

	def controlTrackRBSelected(self):
		self.mainFrame.setStatusWorking('Analyse des erreurs dans la table : Parcours-RB pour les parcours sélectionnés ...')
		VTRB.analyseTracksRB(self.mainFrame, self, self.dicoBoutonsErreursTracksRB, False)
		self.mainFrame.setStatusDone('Analyse des erreurs dans la table : Parcours-RB - Terminé')

	def controlTrackRBAll(self):
		self.mainFrame.setStatusWorking('Analyse des erreurs dans la table : Parcours-RB pour tous les parcours ...')
		VTRB.analyseTracksRB(self.mainFrame, self, self.dicoBoutonsErreursTracksRB, True)
		self.mainFrame.setStatusDone('Analyse des erreurs dans la table : Parcours-RB - Terminé')

	def controlSectionsGRSelected(self):
		self.mainFrame.setStatusWorking('Analyse des erreurs dans la table : Tronçons-GR pour les tronçons sélectionnés ...')
		VSGR.analyseSectionsGR(self.mainFrame, self, self.dicoBoutonsErreursSectionsGR, False)
		self.mainFrame.setStatusDone('Analyse des erreurs dans la table : Parcours-GR - Terminé')

	def controlSectionsGRAll(self):
		self.mainFrame.setStatusWorking('Analyse des erreurs dans la table : Tronçons-GR pour tous les tronçons ...')
		VSGR.analyseSectionsGR(self.mainFrame, self, self.dicoBoutonsErreursSectionsGR, True)
		self.mainFrame.setStatusDone('Analyse des erreurs dans la table : Parcours-GR - Terminé')

	def controlPointsGRSelected(self):
		self.mainFrame.setStatusWorking('Analyse des erreurs dans la table : Repères-GR pour les repères sélectionnés ...')
		VPGR.analysePointsGR(self.mainFrame, self, self.dicoBoutonsErreursPointsGR, False)
		self.mainFrame.setStatusDone('Analyse des erreurs dans la table : Parcours-GR - Terminé')

	def controlPointsGRAll(self):
		self.mainFrame.setStatusWorking('Analyse des erreurs dans la table : Repères-GR pour tous les repères ...')
		VPGR.analysePointsGR(self.mainFrame, self, self.dicoBoutonsErreursPointsGR, True)
		self.mainFrame.setStatusDone('Analyse des erreurs dans la table : Parcours-GR - Terminé')


# ========================================================================================
# ========================================================================================
#
# Création des différents cadres Menu
# 
# ========================================================================================
# ========================================================================================


# ========================================================================================
# Cadre : Vérifications Parcours-GR
# ========================================================================================

	def menuBoxControlsTracksGR(self):
	
		def createButton(errorCode, x, y, type, leftClic, rightClic):
			self.dicoBoutonsErreursTracksGR[errorCode] = self.errorInfo(self, self.mainFrame, groupBoxControlsTracksGR, x, y, errorCode, type, leftClic, rightClic, self.layerTracksGR)

		groupBoxControlsTracksGR = QtWidgets.QGroupBox('Vérifications de la table : Parcours-GR', self.mainMenu)
		groupBoxControlsTracksGR.setStyleSheet(DSTY.styleBox)
		
# 	Ajout des boutons pour toutes les vérifications

		self.dicoBoutonsErreursTracksGR = {}
	
		createButton('Typ-I', 1, 1, 'Error', True, False)
		createButton('Suf-I', 2, 1, 'Error', True, False)
		createButton('Geo-0', 3, 1, 'Error', True, False)

		createButton('C-OK', 	1, 2, 'Info', 	False, 	False)
		createButton('C-Vide', 	2, 2, 'Error', 	True, 	True)
		createButton('C-D-0', 	3, 2, 'Error', 	True, 	True)
		createButton('C-D-N', 	4, 2, 'Error', 	True, 	True)
		createButton('C-Inc', 	5, 2, 'Error', 	True, 	True)
		createButton('C-Y', 	6, 2, 'Error', 	True, 	True)
		createButton('C-Trou', 	7, 2, 'Error', 	True, 	True)

		createButton('D-1', 	1, 3, 'Error', True, True)
		createButton('D-10', 	2, 3, 'Error', True, True)
		createButton('D-100', 	3, 3, 'Error', True, True)
		createButton('D-1000', 	4, 3, 'Error', True, True)

		createButton('E-0', 	1, 4, 'Info', True, True)
		createButton('E-I', 	2, 4, 'Info', True, True)
		createButton('E-P', 	3, 4, 'Info', True, True)
		createButton('E-PJ', 	4, 4, 'Info', True, True)
		createButton('E-VA', 	5, 4, 'Info', True, True)
		createButton('E-PU', 	6, 4, 'Info', True, True)
		createButton('E-SU', 	7, 4, 'Info', True, True)
		createButton('E-EX', 	8, 4, 'Info', True, True)

		createButton('T-P',   1, 5, 'Info', True, False)
		createButton('T-V',   2, 5, 'Info', True, False)
		createButton('T-L',   3, 5, 'Info', True, False)
		createButton('T-R',   4, 5, 'Info', True, False)
		createButton('T-B',   5, 5, 'Info', True, False)

		createButton('T-MT',   6, 5, 'Info', True, False)
		createButton('T-MF',   7, 5, 'Info', True, False)

		createButton('T-ENT', 1, 6, 'Info', False, False)
		createButton('T-GR',  2, 6, 'Info', False, False)
		createButton('T-GRP', 3, 6, 'Info', False, False)
		createButton('T-GRT', 4, 6, 'Info', False, False)
		createButton('T-KM',  5, 6, 'Info', False, False)

#	Boutons Analyse

		self.buttonControlSelectionTracksGR = TBUT.createActionButton(groupBoxControlsTracksGR, 7, 6, 'Vérif. Sélection', 'Normal')
		self.buttonControlSelectionTracksGR.clicked.connect(self.controlTrackGRSelected)	

		self.buttonControlAllTracksGR = TBUT.createActionButton(groupBoxControlsTracksGR, 8, 6, 'Vérif. Globale', 'Normal')
		self.buttonControlAllTracksGR.clicked.connect(self.controlTrackGRAll)	

#	Boutons Aide

		buttonHelpDBCarto = TBUT.createHelpButton(groupBoxControlsTracksGR, 7, 1, 'DB Carto', 'Normal')
		buttonHelpDBCarto.clicked.connect(self.buttonHelpLDBCarto_clicked)

		buttonHelpLegend = TBUT.createHelpButton(groupBoxControlsTracksGR, 8, 1, 'Légende', 'Normal')
		buttonHelpLegend.clicked.connect(self.buttonHelpLegendTrackGR_clicked)

# 	Terminé

		groupBoxControlsTracksGR.repaint()

		return groupBoxControlsTracksGR
		

	def buttonHelpLDBCarto_clicked(self):
		webbrowser.open_new_tab(QGP.configMenuHelpBasePath + 'QCarto - DB Carto - Vue Globale.html')

	def buttonHelpLegendTrackGR_clicked(self):
		webbrowser.open_new_tab(QGP.configMenuHelpBasePath + 'QCarto - DB Vérifications - Parcours GR.html')


# ========================================================================================
# Cadre : Vérifications Parcours-RB
# ========================================================================================

	def menuBoxControlsTracksRB(self):
	
		def createButton(errorCode, x, y, type, leftClic, rightClic):
			self.dicoBoutonsErreursTracksRB[errorCode] = self.errorInfo(self, self.mainFrame, groupBoxControlsTracksRB, x, y, errorCode, type, leftClic, rightClic, self.layerTracksRB)

		groupBoxControlsTracksRB = QtWidgets.QGroupBox('Vérifications de la table : Parcours-RB', self.mainMenu)
		groupBoxControlsTracksRB.setStyleSheet(DSTY.styleBox)

# 	Ajout des boutons pour toutes les vérifications

		self.dicoBoutonsErreursTracksRB = {}
	
		createButton('Typ-I', 1, 1, 'Error', True, False)
		createButton('Suf-I', 2, 1, 'Error', True, False)
		createButton('Geo-0', 3, 1, 'Error', True, False)

		createButton('C-OK', 	1, 2, 'Info', 	False, 	False)
		createButton('C-Vide', 	2, 2, 'Error', 	True, 	True)
		createButton('C-D-0', 	3, 2, 'Error', 	True, 	True)
		createButton('C-D-N', 	4, 2, 'Error', 	True, 	True)
		createButton('C-Inc', 	5, 2, 'Error', 	True, 	True)
		createButton('C-Y', 	6, 2, 'Error', 	True, 	True)
		createButton('CV-D-M', 	7, 2, 'Error', 	True, 	True)
		createButton('CV-Inc', 	8, 2, 'Error', 	True, 	True)
		createButton('CV-Y', 	9, 2, 'Error', 	True, 	True)
		createButton('C-Trou', 10, 2, 'Error', 	True, 	True)

		createButton('D-1', 	1, 3, 'Error', True, True)
		createButton('D-10', 	2, 3, 'Error', True, True)
		createButton('D-100', 	3, 3, 'Error', True, True)
		createButton('D-1000', 	4, 3, 'Error', True, True)

		createButton('E-0', 	1, 4, 'Info', True, True)
		createButton('E-I', 	2, 4, 'Info', True, True)
		createButton('E-P', 	3, 4, 'Info', True, True)
		createButton('E-PJ', 	4, 4, 'Info', True, True)
		createButton('E-VA', 	5, 4, 'Info', True, True)
		createButton('E-PU', 	6, 4, 'Info', True, True)
		createButton('E-SU', 	7, 4, 'Info', True, True)
		createButton('E-EX', 	8, 4, 'Info', True, True)

		createButton('T-P',   1, 5, 'Info', True, False)
		createButton('T-V',   2, 5, 'Info', True, False)
		createButton('T-A',   3, 5, 'Info', True, False)
		createButton('T-R',   4, 5, 'Info', True, False)
		createButton('T-J',   5, 5, 'Info', True, False)

		createButton('T-MT',   6, 5, 'Info', True, False)
		createButton('T-MF',   7, 5, 'Info', True, False)

		createButton('T-ENT', 1, 6, 'Info', False, False)
		createButton('T-RI',  2, 6, 'Info', False, False)
		createButton('T-RB',  3, 6, 'Info', False, False)
		createButton('T-RL',  4, 6, 'Info', False, False)
		createButton('T-RF',  5, 6, 'Info', False, False)
		createButton('T-IR',  6, 6, 'Info', False, False)
		createButton('T-KM',  7, 6, 'Info', False, False)

#	Boutons Analyse

		self.buttonControlSelectionTracksRB = TBUT.createActionButton(groupBoxControlsTracksRB, 7, 6, 'Vérif. Sélection', 'Normal')
		self.buttonControlSelectionTracksRB.clicked.connect(self.controlTrackRBSelected)	

		self.buttonControlAllTracksRB = TBUT.createActionButton(groupBoxControlsTracksRB, 8, 6, 'Vérif. Globale', 'Normal')
		self.buttonControlAllTracksRB.clicked.connect(self.controlTrackRBAll)	

#	Bouton Aide

		buttonHelpLegend = TBUT.createHelpButton(groupBoxControlsTracksRB, 8, 1, 'Légende', 'Normal')
		buttonHelpLegend.clicked.connect(self.buttonHelpLegendTrackRB_clicked)

# 	Terminé

		groupBoxControlsTracksRB.repaint()

		return groupBoxControlsTracksRB


	def buttonHelpLegendTrackRB_clicked(self):
		webbrowser.open_new_tab(QGP.configMenuHelpBasePath + 'QCarto - DB Vérifications - Parcours RB.html')


# ========================================================================================
# Cadre : Vérifications Tronçons-GR
# ========================================================================================

	def menuBoxControlsSectionsGR(self):
	
		def createButton(errorCode, x, y, type, leftClic, rightClic):
			self.dicoBoutonsErreursSectionsGR[errorCode] = self.errorInfo(self, self.mainFrame, groupBoxControlsSectionsGR, x, y, errorCode, type, leftClic, rightClic, self.layerSectionsGR)

		groupBoxControlsSectionsGR = QtWidgets.QGroupBox('Vérifications de la table : Tronçons-GR', self.mainMenu)
		groupBoxControlsSectionsGR.setStyleSheet(DSTY.styleBox)

		
# 	Ajout des boutons pour toutes les vérifications

		self.dicoBoutonsErreursSectionsGR = {}

		createButton('Cod-0', 1, 1, 'Error', True, False)
		createButton('Cod-I', 2, 1, 'Error', True, False)
		createButton('Typ-I', 3, 1, 'Error', True, False)
		createButton('Suf-I', 4, 1, 'Error', True, False)
		createButton('Par-I', 5, 1, 'Error', True, False)

		createButton('Geo-0', 1, 2, 'Error', True, True)
		createButton('Geo-M', 2, 2, 'Error', True, True)
		createButton('T-KM',  3, 2, 'Info', False, False)

		createButton('T-MT',  1, 3, 'Info', True, False)
		createButton('T-#T',  2, 3, 'Info', True, False)
		createButton('T-MF',  3, 3, 'Info', True, False)
		createButton('T-#F',  4, 3, 'Info', True, False)
		createButton('T-#0',  5, 3, 'Info', True, False)
		createButton('T-#A',  6, 3, 'Info', True, False)

		createButton('T-ENT', 1, 4, 'Info', False, False)
		createButton('T-GR',  2, 4, 'Info', False, False)
		createButton('T-GRP', 3, 4, 'Info', False, False)
		createButton('T-GRT', 4, 4, 'Info', False, False)
		createButton('T-RI',  5, 4, 'Info', False, False)
		createButton('T-RL',  6, 4, 'Info', False, False)
		createButton('T-RB',  7, 4, 'Info', False, False)
		createButton('T-RF',  8, 4, 'Info', False, False)
		createButton('T-IR',  9, 4, 'Info', False, False)


#	Boutons Analyse

		self.buttonControlSelectionSectionsGR = TBUT.createActionButton(groupBoxControlsSectionsGR, 7, 4, 'Vérif. Sélection', 'Normal')
		self.buttonControlSelectionSectionsGR.clicked.connect(self.controlSectionsGRSelected)	

		self.buttonControlAllSectionsGR = TBUT.createActionButton(groupBoxControlsSectionsGR, 8, 4, 'Vérif. Globale', 'Normal')
		self.buttonControlAllSectionsGR.clicked.connect(self.controlSectionsGRAll)	

#	Bouton Aide

		buttonHelpLegend = TBUT.createHelpButton(groupBoxControlsSectionsGR, 8, 1, 'Légende', 'Normal')
		buttonHelpLegend.clicked.connect(self.buttonHelpLegendSectionsGR_clicked)

# 	Terminé

		groupBoxControlsSectionsGR.repaint()

		return groupBoxControlsSectionsGR


	def buttonHelpLegendSectionsGR_clicked(self):
		webbrowser.open_new_tab(QGP.configMenuHelpBasePath + 'QCarto - DB Vérifications - Sections GR.html')


# ========================================================================================
# Cadre : Vérifications Repères-GR
# ========================================================================================

	def menuBoxControlsPointsGR(self):
	
		def createButton(errorCode, x, y, type, leftClic, rightClic):
			self.dicoBoutonsErreursPointsGR[errorCode] = self.errorInfo(self, self.mainFrame, groupBoxControlsPointsGR, x, y, errorCode, type, leftClic, rightClic, self.layerPointsGR)

		groupBoxControlsPointsGR = QtWidgets.QGroupBox('Vérifications de la table : Repères-GR', self.mainMenu)
		groupBoxControlsPointsGR.setStyleSheet(DSTY.styleBox)

# 	Ajout des boutons pour toutes les vérifications

		self.dicoBoutonsErreursPointsGR = {}
	
		createButton('Cod-0', 1, 1, 'Error', True, False)
		createButton('Cod-I', 2, 1, 'Error', True, False)
		createButton('Typ-I', 3, 1, 'Error', True, False)
		createButton('Suf-I', 4, 1, 'Error', True, False)
		createButton('Par-I', 5, 1, 'Error', True, False)
		createButton('Rep-0', 6, 1, 'Error', True, False)
		createButton('Nom-0', 7, 1, 'Error', True, False)
		
		createButton('Geo-0', 1, 2, 'Error', True, False)
		createButton('Att-0', 2, 2, 'Error', True, False)
		createButton('Att-D', 3, 2, 'Error', True, False)
		createButton('Att-S', 4, 2, 'Error', True, False)

		createButton('T-ENT', 1, 4, 'Info', False, False)
		createButton('T-GR',  2, 4, 'Info', True, False)
		createButton('T-GRP', 3, 4, 'Info', True, False)
		createButton('T-GRT', 4, 4, 'Info', True, False)
		createButton('T-RI',  5, 4, 'Info', True, False)
		createButton('T-RL',  6, 4, 'Info', True, False)
		createButton('T-RB',  7, 4, 'Info', True, False)
		createButton('T-RF',  8, 4, 'Info', True, False)
		createButton('T-IR',  9, 4, 'Info', True, False)
		createButton('T-B2B', 9, 3, 'Info', True, False)
		
#	Check box d'activation pour les vérifications lentes de géométrie

		self.checkGeometryPointsGR = TBUT.createCheckBoxButton(groupBoxControlsPointsGR, 4, 2, '! Lent !', 'Normal')
		self.checkGeometryPointsGR.setCheckState(Qt.Unchecked)	

#	Boutons Analyse

		self.buttonControlSelectionPointsGR = TBUT.createActionButton(groupBoxControlsPointsGR, 7, 4, 'Vérif. Sélection', 'Normal')
		self.buttonControlSelectionPointsGR.clicked.connect(self.controlPointsGRSelected)	

		self.buttonControlAllPointsGR = TBUT.createActionButton(groupBoxControlsPointsGR, 8, 4, 'Vérif. Globale', 'Normal')
		self.buttonControlAllPointsGR.clicked.connect(self.controlPointsGRAll)	

#	Bouton Aide

		buttonHelpLegend = TBUT.createHelpButton(groupBoxControlsPointsGR, 8, 1, 'Légende', 'Normal')
		buttonHelpLegend.clicked.connect(self.buttonHelpLegendPointsGR_clicked)

# 	Terminé

		groupBoxControlsPointsGR.repaint()

		return groupBoxControlsPointsGR


	def buttonHelpLegendPointsGR_clicked(self):
		webbrowser.open_new_tab(QGP.configMenuHelpBasePath + 'QCarto - DB Vérifications - Repères GR.html')


# ========================================================================================
# ========================================================================================
#
# Gestion des boutons d'erreur
# 
# ========================================================================================
# ========================================================================================

# ========================================================================================
# Classe errorInfo pour les informations d'erreur
#  >>> controlFrame		:	menuControlsFrame
#  >>> mainFrame		:					
#  >>> parentWidget 	: 							Parent where to install local Widgets
#  >>> xPos 			: int 						Position x in parent Widget 
#  >>> yPos 			: int						Position y in parent Widget
#  >>> errorCode 		: str						Code d'erreur 
#  >>> type				: str						Type de bouton : 'Info' // 'Error'
#  >>> enableLeftClic 	: bool						Call generic fonction on left clic
#  >>> enableRightClic 	: bool						Call generic fonction on right clic
#  >>> layer			: 							
# ========================================================================================

	class errorInfo:

# 	Initialisation

		def __init__(self, controlFrame, mainFrame, parentWidget, xPos, yPos, errorCode, type, enableLeftClic, enableRightClic, layer):

			self.controlFrame = controlFrame
			self.mainFrame = mainFrame
			self.parentWidget = parentWidget
			self.errorCode = errorCode
			self.type = type
			self.enableLeftClic = enableLeftClic
			self.enableRightClic = enableRightClic
			self.layer = layer

			self.errorCount = 0
			self.value = 0
			self.featureList = []

			self.label = TBUT.createLabelBlackButton(self.parentWidget, 1 + 2 * (xPos-1), yPos, errorCode, 'ShortHalf')
			self.bouton = TBUT.createLabelGreenButton(self.parentWidget, 2 + 2 * (xPos-1), yPos, '. . .', 'ShortHalf', 'Normal')
			self.select = TBUT.createActionButtonTransparent(self.parentWidget, 2 + 2 * (xPos-1), yPos, '', 'ShortHalf')

			self.select.clicked.connect(self.select_leftClicked)
			self.select.setContextMenuPolicy(Qt.CustomContextMenu)
			self.select.customContextMenuRequested.connect(self.select_rightClicked)

		def reset(self):
			self.errorCount = 0
			self.value = 0
			self.featureList = []
			DSTY.setStyleWarningLabel(self.bouton, "ShortHalf")
			self.bouton.setText(DSTY.textFormatBlackNormal.replace('%TEXT%',str(self.errorCount)))
			self.bouton.repaint()

		def addError(self, feature = None):
			self.errorCount += 1
			DSTY.setStyleWarningLabel(self.bouton, "ShortHalf")
			self.bouton.setText(DSTY.textFormatBlackNormal.replace('%TEXT%',str(self.errorCount)))
			self.bouton.repaint()
			if feature != None: self.featureList.append(feature)

		def addValue(self, value):
			self.value += value
			DSTY.setStyleWarningLabel(self.bouton, "ShortHalf")
			self.bouton.setText(DSTY.textFormatBlackNormal.replace('%TEXT%',str(int(self.value))))
			self.bouton.repaint()

		def showFinal(self):
			if self.type == 'Info' or self.errorCount == 0:
				DSTY.setStyleOkLabel(self.bouton, "ShortHalf")
			else:	
				DSTY.setStyleErrorLabel(self.bouton, "ShortHalf")
			self.bouton.repaint()

		def getBouton(self):
			return self.bouton

		def select_leftClicked(self):
			if self.enableLeftClic:	
				self.controlFrame.errorInfo_leftClicked(self.errorCode, self.featureList, self.layer)
			else:
				self.mainFrame.setStatusInfo(self.errorCode + ' : pas d\'action définie !')

		def select_rightClicked(self):
			if self.enableRightClic:	
				self.controlFrame.errorInfo_rightClicked(self.errorCode, self.featureList, self.layer)
			else:
				self.mainFrame.setStatusInfo(self.errorCode + ' : pas d\'action définie !')


# ========================================================================================
# Actions : clic gauche ou droit sur boutons
# ========================================================================================

	def errorInfo_leftClicked(self, errorCode, featureList, layer):
		if len(featureList) == 0:
			self.mainFrame.setStatusInfo(errorCode + ' : aucune entité sélectionnée dans ' + layer.name())
		else:
			layer.selectByIds( [ feature.id() for feature in featureList] )
			self.mainFrame.setStatusInfo(errorCode + ' : ' + str(len(featureList)) + ' entités sélectionnées dans ' + layer.name())

	def errorInfo_rightClicked(self, errorCode, featureList, layer):
		if len(featureList) == 0:
			self.mainFrame.setStatusInfo(errorCode + ' : aucune entité sélectionnée dans ' + layer.name())
		else:
			if layer.name() == QGP.tableNameTracksGR :
				dicoTracksViewFeatures = {feature[QGP.tableTracksFieldCode] : 
				self.mainFrame.dicoTracksGRFeatures[feature[QGP.tableTracksFieldCode]] for feature in featureList}
				self.mainFrame.requestPageParcoursView('GR', dicoTracksViewFeatures)
				self.mainFrame.setStatusInfo(errorCode + ' : ' + str(len(featureList)) + ' entités affichées dans la Page Parcours')
			if layer.name() == QGP.tableNameTracksRB :
				dicoTracksViewFeatures = {feature[QGP.tableTracksFieldCode] : self.mainFrame.dicoTracksRBFeatures[feature[QGP.tableTracksFieldCode]] for feature in featureList}
				self.mainFrame.requestPageParcoursView('RB', dicoTracksViewFeatures)
				self.mainFrame.setStatusInfo(errorCode + ' : ' + str(len(featureList)) + ' entités affichées dans la Page Parcours')
			if layer.name() == QGP.tableNameSectionsGR :
				if any(not layer.getFeature(feature.id()).isValid() for feature in featureList) : 
					self.mainFrame.setStatusError('Tronçons-GR : au moins un des tronçons n\'existe plus', False) ; return
				if errorCode == 'Geo-0' :
					if any(feature.hasGeometry() for feature in featureList) : 	
						self.mainFrame.setStatusError('Tronçons-GR : au moins un des tronçons n\'a pas une géométrie nulle ?', False) ; return
					layer.startEditing()
					for feature in featureList :
						layer.deleteFeature(feature.id())
					layer.commitChanges()
					self.mainFrame.setStatusInfo(errorCode + ' : ' + str(len(featureList)) + ' entités supprimées de la table Tronçons-GR')
				if errorCode == 'Geo-M' :
					if any(len(feature.geometry().asMultiPolyline()) <= 1 for feature in featureList) : 	
						self.mainFrame.setStatusError('Tronçons-GR : au moins un des tronçons n\'a pas une géométrie multiple ?', False) ; return
					layer.startEditing()
					for feature in featureList :
						lineList = feature.geometry().asMultiPolyline()								# List of elementary lines from geometry
						lineList = [ l for l in lineList if len(l) > 1 ]							# Keep only significant elementary lines - do not know if can happen
						if len(lineList) == 0: layerGR.deleteFeature(feature.id()) ; continue		# No more signficant geometry
						for n in range(1,len(lineList)):											# For all elementary lines except first one
							newFeature = QgsFeature(feature)													# Copy all from original feature
							newFeature[QGP.tableSectionsFieldId] = layer.maximumValue(newFeature.fieldNameIndex(QGP.tableSectionsFieldId)) + n
							newFeature.setGeometry(QgsGeometry().fromMultiPolylineXY([lineList[n]]))			# Set up one elementary line
							layer.addFeature(newFeature)														# Add new feature
						layer.changeGeometry(feature.id(), QgsGeometry().fromMultiPolylineXY([lineList[0]]))	# Keep first (0) elementary line is left in original entity
					layer.commitChanges()
					self.mainFrame.setStatusInfo(errorCode + ' : ' + str(len(featureList)) + ' entités décomposées dans la table Tronçons-GR')
					



# ========================================================================================
# --- THE END ---
# ========================================================================================
	