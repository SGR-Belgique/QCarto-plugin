# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Gestion du Menu Principal
# ========================================================================================

# ========================================================================================
# Quelques Notes pour les versions futures ...
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
from qgis.gui import QgsMapToolEmitPoint
from qgis.PyQt import QtWidgets

import os
import time
import importlib
import webbrowser
import traceback 

import QCarto_Definitions_Styles as DSTY

import QCarto_Tools_QParam as TQCP
importlib.reload(TQCP)
import QCarto_Tools_Dates as TDAT
import QCarto_Tools_Layers as TLAY
import QCarto_Tools_Buttons as TBUT

import QCarto_Menu_Parcours as PPAR
importlib.reload(PPAR)
import QCarto_Menu_Maps as PPRO
importlib.reload(PPRO)
import QCarto_Menu_ActiveMap as PMAP
importlib.reload(PMAP)
import QCarto_Menu_Deliveries as PDEL
importlib.reload(PDEL)
import QCarto_Menu_Verifications as PVER
importlib.reload(PVER)
import QCarto_Menu_Publications as PPUB
importlib.reload(PPUB)
import QCarto_Menu_Tools as PTOO
importlib.reload(PTOO)
import QCarto_Menu_Initialisations as PINI
importlib.reload(PINI)
import QCarto_Menu_Routage as PROU
importlib.reload(PROU)
import QCarto_Tools_Input as TINP
importlib.reload(TINP)
import QCarto_Menu_Identification as PIDE
importlib.reload(PIDE)
import QCarto_Menu_Maintenance as PMAI
importlib.reload(PMAI)

import QCarto_Bar_ActionButtons as BQAB
importlib.reload(BQAB)


import QCarto_Parameters_Global
importlib.reload(QCarto_Parameters_Global)
QGP = QCarto_Parameters_Global.globalParameters()


C_DicoPage_X = 0; C_DicoPage_Y = 1; C_DicoPage_Button = 2; C_DicoPage_Class = 3; C_DicoPage_Init = 4; C_DicoPage_Frame = 5


# ========================================================================================
# Class : mainMenuFrame :
#  - définit le cadre principal et le titre
#  - définit le cadre de logo
#  - définit le cadre de l'utilisateur
#  - définit le cadre de statut
#  - définit le cadre de contrôle : fermer et rafraichir
#  - définit le cadre docks
#  - définit le cadre des différentes pages 
# ========================================================================================

class menuMainFrame:

	def __init__(self, iface, parent):

# 	Paramètres fournis

		self.iface = iface
		self.parent = parent

#	Accès aux Tables de la DB Carto
	
		self.layerQCartoParam, 		self.layerQCartoParamError 	= TLAY.openLayer(QGP.tableNameQParam)
		self.layerTracksGR, 		self.layerTracksGRerror 	= TLAY.openLayer(QGP.tableNameTracksGR)
		self.layerTracksRB, 		self.layerTracksRBerror 	= TLAY.openLayer(QGP.tableNameTracksRB)
		self.layerTracksGRHist, 	self.layerTracksGRHisterror	= TLAY.openLayer(QGP.tableNameTracksGRHist)
		self.layerTracksRBHist, 	self.layerTracksRBHisterror	= TLAY.openLayer(QGP.tableNameTracksRBHist)
		self.layerSectionsGR, 		self.layerSectionsGRerror 	= TLAY.openLayer(QGP.tableNameSectionsGR)
		self.layerPointsGR, 		self.layerPointsGRError 	= TLAY.openLayer(QGP.tableNamePointsGR)
		self.layerSityTrail, 		self.layerSityTrailError 	= TLAY.openLayer(QGP.tableNameSityTrail)
		self.layerPOIs, 			self.layerPOIsError			= TLAY.openLayer(QGP.poisTablePOIsName)			
		self.layerCommunes, 		self.layerCommunesError		= TLAY.openLayer(QGP.configCommuneShapeName)		
		
#	Couches Carte Active - Partagées Descriptifs et Carte Active	

		self.layerActiveMapPoints 		= None
		self.layerActiveMapPoisRF 		= None
		self.layerActiveMapSections 	= None
		self.layerActiveMapLabels		= None
		self.layerActiveMapLabelsSimple	= None

#	Couches Projet Actif - Partagées Descriptifs et Carte Active	

		self.layerTEC = None
		self.layerSNCB = None
		
#	Couche des emprises	
		
		self.layerMaps = None		
		
#	Dictionnaires Principaux 
		
		self.dicoTracksGRFeatures = {f[QGP.tableTracksFieldCode] : f for f in self.layerTracksGR.getFeatures()} if self.layerTracksGR != None else {}
		self.dicoTracksRBFeatures = {f[QGP.tableTracksFieldCode] : f for f in self.layerTracksRB.getFeatures()} if self.layerTracksRB != None else {}
		self.dicoSectionsGRFeatures = { feature[QGP.tableSectionsFieldId] : feature for feature in self.layerSectionsGR.getFeatures() if not feature.geometry().isNull() } if self.layerSectionsGR != None else {}
		self.dicoSectionsGRFeaturesEndPoints = { id : [self.dicoSectionsGRFeatures[id].geometry().asMultiPolyline()[0][0], self.dicoSectionsGRFeatures[id].geometry().asMultiPolyline()[0][-1]] \
														for id in self.dicoSectionsGRFeatures }
		self.dicoPointsGRFeatures = { f[QGP.tablePointsFieldId] : f for f in self.layerPointsGR.getFeatures()} if self.layerPointsGR != None else {}												

#	Dock Menu pour Edition Tronçons Topo50

		self.dockMenuEditTopo50Ed4 = None

#	Dock Menu pour Création GPX

		self.dockMenuCreateGPX = None
		
# 	Fenêtre d'identification Réseau GR

		self.identificationWindow = None	
		self.pointTool = None		

#	Désactiver le highlight des modifications sur Tronçons-GR

		QgsExpressionContextUtils.setProjectVariable(QgsProject.instance(), QGP.tableSectionsGRHighlightVariable,'Non')  

#	Variables globales de la classe

		self.onError = False
		self.currentPageName = None
		self.currentPageInfo = False
		self.canvas = self.iface.mapCanvas()
		self.selectedMapFeature = None
		self.expertModeQCarto = False
		self.debugModeQCartoLevel = 0
		self.userFullName = QgsApplication.userFullName()
		
#	Définitions des Pages - Page Name : bouton-x  bouton-y  class  initStatus  pageFrame
#	C_DicoPage_X = 0; C_DicoPage_Y = 1; C_DicoPage_Button = 2; C_DicoPage_Class = 3; C_DicoPage_Init = 4; C_DicoPage_Frame = 5
			
		self.dicoDefinitionPages = {
			'Parcours' 			: [1, 1, None, PPAR.menuTracksFrame, 		False, 	None ] ,
			'Routage' 			: [1, 2, None, PROU.menuRoutageFrame, 		False, 	None ] ,
			'Cartes'	 		: [2, 1, None, PPRO.menuMapsFrame, 			False, 	None ] ,
			'Carte Active' 		: [2, 2, None, PMAP.menuActiveMapFrame, 	False, 	None ] ,
			'Livraisons' 		: [3, 1, None, PDEL.menuDeliveriesFrame, 	False, 	None ] ,
			'Publications' 		: [3, 2, None, PPUB.menuPublicationsFrame, 	False, 	None ] ,
			'Vérifications' 	: [4, 1, None, PVER.menuControlsFrame, 		False, 	None ] ,
			'Outils' 			: [4, 2, None, PTOO.menuToolsFrame, 		False, 	None ] ,
			'Initialisations' 	: [5, 1, None, PINI.menuInitFrame, 			False, 	None ] ,
			'Maintenance' 		: [5, 2, None, PMAI.menuMaintenanceFrame, 	False, 	None ] 
		}	
		
#	Création des différents Menu Principaux

		self.boxesList = []
		self.createMenuBoxes()
		self.createIdentificationTool()

#	Connection pour détection des modifications

		self.connectDBTables()

#	Définition des paramètres externes

		status = TQCP.initializeQCartoParameter(self)
		if not status :
			self.setStatusWarning('Vous devez ajouter la table des paramètres QCarto via la page Initialisation !')
			return


#	Terminé !

		self.mainMenu.activateWindow()
		self.setStatusDone('Initialisation terminée')


	def createMenuBoxes(self):

# 	Cadre Principal et Titre

		self.mainMenu = QtWidgets.QWidget()
		
		self.mainMenu.setWindowFlag(Qt.WindowCloseButtonHint, False)											# Disable Close Button - Closing that way prevent Qgis to close correctly
		self.mainMenu.setGeometry(50,140,1210,875)
		self.mainMenu.setWindowTitle('QCarto - Tableau de Bord - Version ' + QGP.version + ' - ' + QgsProject.instance().baseName())
		self.mainMenu.setWindowIcon(QIcon(QGP.configQCartoIcon))

		self.mainMenu.repaint()
		self.mainMenu.show()
		self.iface.mainWindow().statusBar().showMessage('Cadre Tableau de Bord créé')

# 	Cadre Contrôles

		self.groupBoxControl = self.menuBoxControl()
		DSTY.setBoxGeometry(self.groupBoxControl, 7, 28, 2, 1)
		self.boxesList.append(self.groupBoxControl)
		self.iface.mainWindow().statusBar().showMessage('Cadre Contrôles créé')

# 	Cadre Statut

		self.groupBoxStatus = self.menuBoxStatus()
		DSTY.setBoxGeometry(self.groupBoxStatus, 1, 28, 6, 1)
		self.boxesList.append(self.groupBoxStatus)
		self.iface.mainWindow().statusBar().showMessage('Cadre Statut créé')
		self.setStatusWorking('Initialisation ...')

# 	Cadre Logo
	
		self.groupBoxLogo = self.menuBoxLogo()
		DSTY.setBoxGeometry(self.groupBoxLogo, 8, 1, 1, 2)
		self.boxesList.append(self.groupBoxLogo)
		self.iface.mainWindow().statusBar().showMessage('Cadre Logo créé')
	
# 	Cadre Utilisateur

		self.groupBoxUser = self.menuBoxUser()
		DSTY.setBoxGeometry(self.groupBoxUser, 1, 1, 1, 2)
		self.boxesList.append(self.groupBoxUser)
		self.iface.mainWindow().statusBar().showMessage('Cadre Utilisateur créé')	

# 	Cadre Aides

		self.groupBoxHelp = self.menuBoxHelp()
		DSTY.setBoxGeometry(self.groupBoxHelp, 7, 1, 1, 2)
		self.boxesList.append(self.groupBoxHelp)
		self.iface.mainWindow().statusBar().showMessage('Cadre Aides créé')

#	Cadre Pages

		self.setStatusWorking('Création des différentes pages ...')
		self.groupBoxPages = self.menuBoxPages()
		DSTY.setBoxGeometry(self.groupBoxPages, 2, 1, 5, 2)
		self.boxesList.append(self.groupBoxPages)
		self.iface.mainWindow().statusBar().showMessage('Cadre Pages créé')
	

# ========================================================================================
# Connections de la DB pour détection des modifications
# ========================================================================================

	def connectDBTables(self):
		if self.layerTracksGR != None:
			self.layerTracksGR.afterCommitChanges.connect(self.showReloadActive)
		if self.layerTracksRB != None:
			self.layerTracksRB.afterCommitChanges.connect(self.showReloadActive)
		if self.layerSectionsGR != None:
			self.layerSectionsGR.afterCommitChanges.connect(self.showReloadActive)
		if self.layerPointsGR != None:
			self.layerPointsGR.afterCommitChanges.connect(self.showReloadActive)

	def disconnectDBTables(self):
		try:
			self.layerTracksGR.afterCommitChanges.disconnect(self.showReloadActive)
		except:
			pass
		try:
			self.layerTracksRB.afterCommitChanges.disconnect(self.showReloadActive)
		except:
			pass
		try:
			self.layerSectionsGR.afterCommitChanges.disconnect(self.showReloadActive)
		except:
			pass
		try:
			self.layerPointsGR.afterCommitChanges.disconnect(self.showReloadActive)
		except:
			pass

	def showReloadActive(self):	
		DSTY.setStyleNormalStrongButton(self.buttonReload)
	

# ========================================================================================
# Fonctions principales on-click
# ========================================================================================

#	Demande de rechargement 

	def requestReload(self):
		self.setStatusWorking('Rechargement des tables de la DB Carto ...')
		self.layerPointsGR.reload()
		
		self.dicoTracksGRFeatures = {f[QGP.tableTracksFieldCode] : f for f in self.layerTracksGR.getFeatures()}
		self.dicoTracksRBFeatures = {f[QGP.tableTracksFieldCode] : f for f in self.layerTracksRB.getFeatures()}
		self.dicoSectionsGRFeatures = { feature[QGP.tableSectionsFieldId] : feature for feature in self.layerSectionsGR.getFeatures() if not feature.geometry().isNull() }
		self.dicoSectionsGRFeaturesEndPoints = { id : [self.dicoSectionsGRFeatures[id].geometry().asMultiPolyline()[0][0], self.dicoSectionsGRFeatures[id].geometry().asMultiPolyline()[0][-1]] \
														for id in self.dicoSectionsGRFeatures }
		self.dicoPointsGRFeatures = { f[QGP.tablePointsFieldId] : f for f in self.layerPointsGR.getFeatures()} if self.layerPointsGR != None else {}																										
		
		TQCP.initializeQCartoParameter(self)		
				
		DSTY.setStyleMainButtonsInactive(self.buttonReload)
		if self.dicoDefinitionPages['Parcours'][C_DicoPage_Frame] != None : 
			if self.debugModeQCartoLevel >= 1 : print ('Call Parcours')
			self.dicoDefinitionPages['Parcours'][C_DicoPage_Frame].mainReloadDone()
		self.setStatusDone('Rechargement des tables de la DB Carto - OK')

#	Demande de fermeture

	def closeRestartCommon(self):
		if self.currentPageName != None:
			self.dicoDefinitionPages[self.currentPageName][C_DicoPage_Frame].hide()	
		self.disconnectDBTables()
		self.updateSectionMissingLabels()
		if self.dockMenuEditTopo50Ed4 != None : self.dockMenuEditTopo50Ed4.close()
		if self.dockMenuCreateGPX != None : self.dockMenuCreateGPX.close()
		if self.identificationWindow != None : self.identificationWindow.close()
		if self.pointTool != None : del self.pointTool
		self.ActionButtons.removeButtons()
		self.mainMenu.hide()
		self.mainMenu.deleteLater()

	def requestClose(self):
		self.closeRestartCommon()
		self.parent.requestClose()
	
#	Demande de redémarrage
	
	def requestRestart(self):
		self.setStatusWarning('Redémarrage de QCarto dans 1 seconde ...')
		TDAT.sleep(1000)
		self.closeRestartCommon()
		self.parent.requestRestart()
	
#	Demande de chargement d'une page 

	def requestPage(self, newPageName):
	
		if newPageName == self.currentPageName : 
			if self.currentPageInfo : 
				self.currentPageInfo = False
			else:	
				return

		if newPageName == 'Carte Active':
			if self.selectedMapFeature == None:
				self.setStatusWarning('Page ' + newPageName + ' : pas de carte active !')
				return		
	
		if self.currentPageName in self.dicoDefinitionPages:
			DSTY.setStyleMainButtons(self.dicoDefinitionPages[self.currentPageName][C_DicoPage_Button])
			self.dicoDefinitionPages[self.currentPageName][C_DicoPage_Frame].hide()
			self.currentPageName = None

		infosPage = self.dicoDefinitionPages[newPageName]

		if not infosPage[C_DicoPage_Init] :
			self.setStatusWorking('Initialisation de la page : ' + newPageName + ' ...')
			if self.expertModeQCarto :		
				infosPage[C_DicoPage_Frame] = infosPage[C_DicoPage_Class](self.iface, self.mainMenu, self)
				infosPage[C_DicoPage_Init] = True
			else:		
				try:
					infosPage[C_DicoPage_Frame] = infosPage[C_DicoPage_Class](self.iface, self.mainMenu, self)
					infosPage[C_DicoPage_Init] = True
				except:
					self.setStatusWarning('Initialisation de la page : ' + newPageName + ' impossible !', 2000)
					traceback.print_exc() 
					return

		infosPage[C_DicoPage_Frame].show()
		DSTY.setStyleActiveButton(infosPage[C_DicoPage_Button])
		self.currentPageName = newPageName
		self.buttonHelpPage.setText('Aide ' + newPageName)
		self.buttonHelpPage.clicked.disconnect()
		self.buttonHelpPage.clicked.connect(infosPage[C_DicoPage_Frame].help)

		self.setStatusDone('Page ' + newPageName + ' - Prêt')

#	Demande de mode Info d'une page 

	def requestPageInfo(self, pageName):
		infosPage = self.dicoDefinitionPages[pageName]
		DSTY.setStyleInfoButton(infosPage[C_DicoPage_Button])
		self.currentPageInfo = True

#	Demande de chargement de parcours spécifiques

	def requestPageParcoursView(self, type, featureList):
		self.requestPage('Parcours')
		self.dicoDefinitionPages['Parcours'][C_DicoPage_Frame].createTracksView(type, featureList)

#	Remplir les étiquette manquantes suite aux découpes - Qgis ne gère pas l'étiquette automatiquement

	def updateSectionMissingLabels(self):
		try:																		# Avoid error if Qgis closed before QCarto
			if self.layerSectionsGR.isEditable(): return
		except:
			return
		try:
			if self.debugModeQCartoLevel >= 1 : print ('--- Missing Labels - Start ...')
			self.layerSectionsGR.selectByExpression('"id" > 11500 and "etiquette" = ' + "''")
			if self.layerSectionsGR.selectedFeatureCount() > 0:
				self.layerSectionsGR.startEditing()
				for f in self.layerSectionsGR.getSelectedFeatures():
					self.layerSectionsGR.changeAttributeValue(f.id(), f.fieldNameIndex('etiquette'), '')
				self.layerSectionsGR.commitChanges()
				self.layerSectionsGR.removeSelection()
			if self.debugModeQCartoLevel >= 1 : print ('--- Missing Labels - Done')
		except:
			self.layerSectionsGR.rollBack()


# ==========================================================
# Routines pour l'affichage des types de statut
# ==========================================================

	def setStatusError(self, text, permanent = True):
		if permanent : self.onError = True
		self.labelStatus.setText(DSTY.textFormatStatusError.replace('%TEXT%',text))
		self.labelStatus.setStyleSheet(DSTY.styleStatusError)

	def setStatusWarning(self, text, sleepTime = 0):
		if self.onError : return
		self.labelStatus.setText(DSTY.textFormatStatusWarning.replace('%TEXT%',text))
		self.labelStatus.setStyleSheet(DSTY.styleStatusWarning)
		if sleepTime > 0: TDAT.sleep(sleepTime)

	def setStatusWorking(self, text, sleepTime = 0):
		if self.onError : return
		self.labelStatus.setText(DSTY.textFormatStatusWorking.replace('%TEXT%',text))
		self.labelStatus.setStyleSheet(DSTY.styleStatusWorking)
		if sleepTime > 0: TDAT.sleep(sleepTime)
		self.groupBoxStatus.repaint()

	def setStatusDone(self, text):
		if self.onError : return
		self.labelStatus.setText(DSTY.textFormatStatusWorking.replace('%TEXT%',text))
		self.labelStatus.setStyleSheet(DSTY.styleStatusDone)

	def setStatusInfo(self, text):
		if self.onError : return
		self.labelStatus.setText(DSTY.textFormatStatusInfo.replace('%TEXT%',text))
		self.labelStatus.setStyleSheet(DSTY.styleStatusInfo)

	def setStatusOk(self, text, clearPermanent = False):
		if clearPermanent : self.onError = False
		if self.onError : return
		self.labelStatus.setText(DSTY.textFormatStatusOk.replace('%TEXT%',text))
		self.labelStatus.setStyleSheet(DSTY.styleStatusOk)


# ========================================================================================
# ========================================================================================
#
# Boutons actions pour Montrer QCarto
# 
# ========================================================================================
# ========================================================================================

	def actionButtonQWToggled(self):
		self.mainMenu.activateWindow()


# ========================================================================================
# ========================================================================================
#
# Boutons actions et Fenêtre d'identification
# 
# ========================================================================================
# ========================================================================================

	def createIdentificationTool(self):

		self.setStatusWorking('Initialisation de la barre d\'outils QCarto ...')

#		Create QCarto Tool Bar

		self.qCartoBar = BQAB.createQCartoBar(self.iface)
		self.iface.mainWindow().statusBar().showMessage('QCarto Toolbar créée !')

#		Add requested action buttons

		self.ActionButtons = BQAB.QActionButtons(self.iface, self, self.qCartoBar, QGP.configActionButtonsList)		
		self.iface.mainWindow().statusBar().showMessage('Boutons Actions Crées')		

# 		Fenêtre d'identification Réseau GR

		self.identificationWindow = None																		


	def actionButtonIdentificationToggled(self, checked):															# Connexion faite par QActionButtons
	
		if self.identificationWindow == None:				
			self.setStatusWorking('Initialisation de la fenêtre d\'dentification ...')
			self.identificationWindow = PIDE.identificationView(self.iface, self, True)
			self.identificationWindow.hide()
			self.setStatusDone('Initialisation de la fenêtre d\'dentification - OK')
		
		self.pointTool = QgsMapToolEmitPoint(self.canvas)
		self.pointTool.canvasClicked.connect(self.showIdentification)
		self.canvas.setMapTool(self.pointTool)


	def showIdentification(self, pointClicked):
		if self.layerSectionsGR == None: return

		pointRange = QGP.configActionDistance_GrI
		targetRectangle = QgsRectangle(pointClicked.x() - pointRange, pointClicked.y() - pointRange, pointClicked.x() + pointRange, pointClicked.y() + pointRange)
		closeFeaturesSections = [f for f in self.layerSectionsGR.getFeatures(targetRectangle) if f.geometry().intersects(targetRectangle)]
		distanceFeaturesSections = [f.geometry().distance(QgsGeometry.fromPointXY(pointClicked)) for f in closeFeaturesSections]
		closestFeatureSection = None if closeFeaturesSections == [] else closeFeaturesSections[distanceFeaturesSections.index(min(distanceFeaturesSections))]

		pointRange = QGP.configActionDistance_PrI
		targetRectangle = QgsRectangle(pointClicked.x() - pointRange, pointClicked.y() - pointRange, pointClicked.x() + pointRange, pointClicked.y() + pointRange)
		closeFeaturesPoint = [f for f in self.layerPointsGR.getFeatures(targetRectangle) if f.geometry().intersects(targetRectangle)]

		self.identificationWindow.show()
		self.identificationWindow.update(closestFeatureSection, closeFeaturesPoint)
		self.setStatusDone('Voir fenêtre d\'identification')


# ========================================================================================
# ========================================================================================
#
# Fenêtre d'édition gr_list.s
# 
# ========================================================================================
# ========================================================================================

	def actionButtonEditToggled(self, checked):	
		self.pointEditTool = QgsMapToolEmitPoint(self.canvas)
		self.pointEditTool.canvasClicked.connect(self.editSectionXListCodes)
		self.canvas.setMapTool(self.pointEditTool)
		self.setStatusInfo('Outil d\'édition des codes xx_list du tronçon activé !')
	
	def editSectionXListCodes(self, pointClicked):
		if self.layerSectionsGR == None: return

		pointRange = QGP.configActionDistance_GrE
		targetRectangle = QgsRectangle(pointClicked.x() - pointRange, pointClicked.y() - pointRange, pointClicked.x() + pointRange, pointClicked.y() + pointRange)
		closeFeaturesSections = [f for f in self.layerSectionsGR.getFeatures(targetRectangle) if f.geometry().intersects(targetRectangle)]
		if closeFeaturesSections == []: return
		distanceFeaturesSections = [f.geometry().distance(QgsGeometry.fromPointXY(pointClicked)) for f in closeFeaturesSections]
		self.activeFeatureSectionForEdit = closeFeaturesSections[distanceFeaturesSections.index(min(distanceFeaturesSections))]
		self.activeFeatureSectionXCodes = [(self.activeFeatureSectionForEdit[_] if self.activeFeatureSectionForEdit[_] != None else ' ') for _ in QGP.tableSectionsFieldAllXList]
		self.xListInputWindow = TINP.inputFromText(self.iface, self, 'Tronçon : Modifier les codes x_list', QGP.tableSectionsFieldAllXList, self.activeFeatureSectionXCodes, self.editSectionXListCodesResult)	

	def editSectionXListCodesResult(self, status, newCodesList):
		del self.xListInputWindow
		self.mainMenu.activateWindow()
		self.mainMenu.show()
		if not status : self.setStatusInfo('Annulation de l\'édition !'); return
		if newCodesList == self.activeFeatureSectionXCodes: self.setStatusInfo('Edition : Champs non modifiés !'); return
		self.setStatusWorking('Tronçon ' + str(self.activeFeatureSectionForEdit.id()) + ' >>> ' + str(newCodesList) + ' ...')
		try:
			layerSectionAlreadyEditable = self.layerSectionsGR.isEditable()
			self.layerSectionsGR.startEditing()
			for field, value in zip(QGP.tableSectionsFieldAllXList, newCodesList) :
				self.layerSectionsGR.changeAttributeValue(self.activeFeatureSectionForEdit.id(), self.activeFeatureSectionForEdit.fieldNameIndex(field), value)
			if not layerSectionAlreadyEditable : self.layerSectionsGR.commitChanges()
			self.setStatusDone('Tronçon ' + str(self.activeFeatureSectionForEdit.id()) + ' = ' + str(newCodesList))
		except:
			self.setStatusError('Tronçon ' + str(self.activeFeatureSectionForEdit.id()) + ' : erreur imprévue lors de la mise à jour du tronçon !', False)


# ========================================================================================
# ========================================================================================
#
# Création des différents cadres Menu
# 
# ========================================================================================
# ========================================================================================

# ========================================================================================
# Créer le cadre : Contrôle
# ========================================================================================

	def menuBoxControl(self):

		groupBox = QtWidgets.QGroupBox("Contrôles",self.mainMenu)
		groupBox.setStyleSheet(DSTY.styleBox)

#	Boutons Recharger et Fermer

		self.buttonReload = TBUT.createActionButton(groupBox, 1, 1, 'Recharger', 'Normal')
		self.buttonReload.clicked.connect(self.requestReload)		
		DSTY.setStyleMainButtonsInactive(self.buttonReload)

		buttonClose = TBUT.createActionButton(groupBox, 2, 1, 'Terminer', 'Normal')
		buttonClose.clicked.connect(self.requestClose)		
		buttonClose.setContextMenuPolicy(Qt.CustomContextMenu)
		buttonClose.customContextMenuRequested.connect(self.requestRestart)

# 	Terminé	
	
		groupBox.repaint()
		groupBox.show()

		return groupBox

	
# ========================================================================================
# Créer le cadre : Statut
# ========================================================================================

	def menuBoxStatus(self):

		groupBox = QtWidgets.QGroupBox("Statut", self.mainMenu)
		groupBox.setStyleSheet(DSTY.styleBox)

#	Label Erreur - Avec Scroll Area pour Info longues dans la Page Tracé

		self.labelStatus = QtWidgets.QLabel(groupBox)
		self.labelStatus.setWordWrap(True)
		self.labelStatus.setTextInteractionFlags(Qt.TextSelectableByKeyboard | Qt.TextSelectableByMouse)
		DSTY.setStatusLabel(self.labelStatus, 6)

		self.scrollArea = QtWidgets.QScrollArea(groupBox)
		self.scrollArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
		self.scrollArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
		self.scrollArea.setWidgetResizable(True)
		self.scrollArea.setWidget(self.labelStatus)
		DSTY.setStatusLabel(self.scrollArea, 6)

# 	Terminé	
	
		groupBox.repaint()
		groupBox.show()

		return groupBox


# ========================================================================================
# Créer le cadre : Logo
# ========================================================================================

	def menuBoxLogo(self):

		groupBox = QtWidgets.QGroupBox(QGP.version, self.mainMenu)
		groupBox.setStyleSheet(DSTY.styleBox)
	
#	Logo 	
	
		logo = QtWidgets.QLabel(groupBox)
		logo.move(10,20)
		pixmap = QPixmap(QGP.configMenuLogoPath)
		logo.setPixmap(pixmap)
	
# 	Terminé	
	
		groupBox.repaint()
		groupBox.show()

		return groupBox


# ========================================================================================
# Créer le cadre : Utilisateur
# ========================================================================================

	def menuBoxUser(self):

		groupBox = QtWidgets.QGroupBox("Utilisateur", self.mainMenu)
		groupBox.setStyleSheet(DSTY.styleBox)

#	Labels User Name et Computer

		labelUser = TBUT.createLabelGreenButton(groupBox, 1, 1, self.userFullName)
		labelComputer = TBUT.createLabelGreenButton(groupBox, 1, 2, QgsApplication.systemEnvVars()['COMPUTERNAME'])

#	Bouton Caché Mode Expert

		expertModeButton = TBUT.createActionButtonTransparent(groupBox, 1, 1, '')
		expertModeButton.setContextMenuPolicy(Qt.CustomContextMenu)
		expertModeButton.customContextMenuRequested.connect(self.expertModeToggled)

#	Bouton Caché Debug

		debugModeButton = TBUT.createActionButtonTransparent(groupBox, 1, 2, '')
		debugModeButton.setContextMenuPolicy(Qt.CustomContextMenu)
		debugModeButton.customContextMenuRequested.connect(self.debugModeToggled)

# 	Terminé	
	
		groupBox.repaint()
		groupBox.show()

		return groupBox

	def expertModeToggled(self) :
		self.expertModeQCarto = not self.expertModeQCarto
		self.setStatusDone('Mode Expert QCarto : ' + ('Activé ! Soyez prudents avec ces commandes !' if self.expertModeQCarto else 'Désactivé'))

	def debugModeToggled(self) :
		self.debugModeQCartoLevel = (self.debugModeQCartoLevel + 1) % 4
		self.setStatusDone('Debug QCarto : ' + ('Niveau = ' + str(self.debugModeQCartoLevel) if self.debugModeQCartoLevel > 0 else 'Désactivé'))

# ========================================================================================
# Créer le cadre : Aides
# ========================================================================================

	def menuBoxHelp(self):

		groupBox = QtWidgets.QGroupBox("Aides", self.mainMenu)
		groupBox.setStyleSheet(DSTY.styleBox)

#	Boutons d'aides

		buttonHelpGeneral = TBUT.createHelpButton(groupBox, 1, 1, 'Aide Générale', 'Normal')
		buttonHelpGeneral.clicked.connect(self.buttonHelp_clicked)

		self.buttonHelpPage = TBUT.createHelpButton(groupBox, 1, 2, 'Aide Pages', 'Normal')
		self.buttonHelpPage.clicked.connect(self.buttonHelpPage_clicked)

# 	Terminé	
	
		groupBox.repaint()
		groupBox.show()

		return groupBox

	def buttonHelp_clicked(self):
		webbrowser.open_new_tab(QGP.configMenuHelpBasePath + 'QCarto - Aide - Générale.html')

	def buttonHelpPage_clicked(self):
		webbrowser.open_new_tab(QGP.configMenuHelpBasePath + 'QCarto - Aide - Pages.html')
	

# ========================================================================================
# Créer le cadre : Pages
# ========================================================================================

	def menuBoxPages(self):
	
		groupBox = QtWidgets.QGroupBox("Pages", self.mainMenu)
		groupBox.setStyleSheet(DSTY.styleBox)

#	Boutons pour chaque Page

		for pageName in self.dicoDefinitionPages:
			self.dicoDefinitionPages[pageName][C_DicoPage_Button] = TBUT.createActionButton(groupBox, self.dicoDefinitionPages[pageName][C_DicoPage_X], self.dicoDefinitionPages[pageName][C_DicoPage_Y], pageName, 'Normal')
			self.dicoDefinitionPages[pageName][C_DicoPage_Button].clicked.connect(buttonPage_clicked(self, pageName))

# 	Terminé	
	
		groupBox.repaint()
		groupBox.show()

		return groupBox


# ========================================================================================
# Class pour définir l'action quand un bouton projet est cliqué
# ========================================================================================

class buttonPage_clicked:
	def __init__(self, mainFrame, pageName):
		self.mainFrame = mainFrame
		self.pageName = pageName
	def __call__(self):
		self.mainFrame.requestPage(self.pageName)


# ========================================================================================
# --- THE END ---
# ========================================================================================

