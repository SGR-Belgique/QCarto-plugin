# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Gestion des Menus : Dock Side Menu for IGN Layer Edit
# ========================================================================================

from PyQt5.QtCore import *
from PyQt5.QtGui import *

from qgis.core import *
from qgis.gui import *
from qgis.PyQt import QtWidgets

import math
import webbrowser
import importlib
import hashlib

import QCarto_Tools_Buttons as TBUT
import QCarto_Tools_Canevas as TCAN
import QCarto_Tools_Coding as TCOD
import QCarto_Tools_Dates as TDAT
import QCarto_Tools_Files as TFIL
import QCarto_Tools_Layers as TLAY
import QCarto_Tools_Progress as TPRO

import QCarto_Definitions_Colors as DCOL
import QCarto_Definitions_Styles as DSTY

import QCarto_Menu_Identification as PIDE
importlib.reload(PIDE)

import QCarto_Parameters_Global
importlib.reload(QCarto_Parameters_Global)
QGP = QCarto_Parameters_Global.globalParameters()


C_Texte_Sections_SelectAll = 'Tous tracés'
C_Texte_Sections_SelectGR  = 'GR.P seuls'
		

# ========================================================================================
# Créer si nécessaire le cadre de la Page : Edit IGN V4
# >>> iface     :	
# >>> mainMenu  :	widget						Main Menu Widget - To be shown again on exit		
# >>> mainFrame : 	class mainMenuFrame			Top-level Frame (Tableau de Bord)
# <<< dockFrame : 	dock Frame					Dock Frame for 50K edition
# ========================================================================================

def editTronconsIGN50V4(iface, mainMenu, mainFrame, dockFrame):

	if dockFrame == None:
		dockFrame = menuDockEdit(iface, mainMenu, mainFrame, QGP.tableNameSectionsGREd4)

	return dockFrame


# ========================================================================================
# Class : menuDockEdit
# >>> iface    				 :	
# >>> mainMenu 				 : widget						Main Menu Widget - To be shown again on exit		
# >>> mainFrame				 : class mainMenuFrame			Top-level Frame (Tableau de Bord)
# >>> tableName				 : str							Nom de la table des Tronçons à editer
# <<< dockFrame 		  	 : class menuDockEdit			Dock Frame for 50K edition
# ========================================================================================

class menuDockEdit:

	def __init__(self, iface, mainMenu, mainFrame, tableName):

		mainFrame.setStatusWorking('Initialisation de la fenêtre d\'édition (quelques secondes) ...')

# 	Initialisation des Variables 

		self.iface = iface
		self.mainFrame = mainFrame
		self.mainMenu = mainMenu
		self.tableEditName = tableName
			
#	Accès aux Tables de la DB Carto

		self.layerTracksGR, 	self.layerTracksGRerror 	= self.mainFrame.layerTracksGR, 	self.mainFrame.layerTracksGRerror 	
		self.layerTracksRB, 	self.layerTracksRBerror 	= self.mainFrame.layerTracksRB, 	self.mainFrame.layerTracksRBerror 	
		self.layerSectionsGR, 	self.layerSectionsGRerror 	= self.mainFrame.layerSectionsGR, 	self.mainFrame.layerSectionsGRerror 	
		self.layerPointsGR, 	self.layerPointsGRError 	= self.mainFrame.layerPointsGR, 	self.mainFrame.layerPointsGRError 	
		self.layer50K, 			self.layer50Kerror 			= TLAY.openLayer(self.tableEditName)

#	Dictionnaires Principaux 
		
		self.dicoTracksGRFeatures = self.mainFrame.dicoTracksGRFeatures
		self.dicoTracksRBFeatures = self.mainFrame.dicoTracksRBFeatures
		self.dicoSectionsGRFeatures = self.mainFrame.dicoSectionsGRFeatures

# 	Création du Dock Widget Principal			
			
		self.dockEditWidget = QtWidgets.QDockWidget(self.iface.mainWindow())
		self.dockEditWidget.setFeatures(QtWidgets.QDockWidget.NoDockWidgetFeatures)
		
		self.iface.addDockWidget(Qt.RightDockWidgetArea, self.dockEditWidget)
		self.dockEditWidget.repaint()
		self.dockEditWidget.show()

# 	Création de tous les cadres internes au Widget

		self.createBoxes(self.iface, self.mainFrame)

		self.setButtonCurrentCreateInactive()		
		self.setButtonCurrentDeleteInactive()
		self.setButtonCurrentValidateInactive()

# 	Initialisation des Variables de Contexte

		self.currentId = None														# CurrentId is TEXT or None
		self.currentRow = None														# CurrentRow is INT or None
		self.lastSelect = None														# 'Canevas' or 'ActiveMap'
		self.autoSelect = True														# Always True - Former Button has been removed
		
# 	Initialisation et Connexion des couches Tronçons-GR et Tronçons-GR-Ed4

		self.root = QgsProject.instance().layerTreeRoot()

		self.connectSectionsGR()
		self.connect50K()

		self.setSelectMuteSectionsGR = False										# Used to remove selection without interrupting again		
		self.tableIndirectSelect = False											# Used to tell that table must be scolled ...

		self.layer50KUpdateStatus()

# 	Créations des dictionnaires

		self.dicoActiveSectionsGRFeatures = {}										# Must be initialized because Layer50K Select interrupt may occur before first select
		self.features50KDico = {}													# Must be initialized because Layer50K Select interrupt may occur before first select

		self.setStatusOk('Prêt')													# Must be before connect50K to see error in connect if any


# ========================================================================================
# Création des Widgets internes et Boutons
# ========================================================================================
		
	def createBoxes(self, iface, mainFrame):

#	Cadre des Contrôles

		self.groupBoxControls, self.buttonSelectActiveMap, self.buttonCancel, self.buttonSave, self.buttonExit = menuDockControls(iface, self.mainFrame, self, self.dockEditWidget)
		self.groupBoxControls.repaint()
		DSTY.setBoxGeometryShort(self.groupBoxControls, 1, 1, 4, 2)

# 	Cadre Affichage

		self.groupBoxDisplay, self.buttonReseauCW, self.buttonReseau50K, self.buttonAutoZoom, self.buttonIdentification = menuDockDisplay(iface, self.mainFrame, self, self.dockEditWidget)
		self.groupBoxDisplay.repaint()
		DSTY.setBoxGeometryShort(self.groupBoxDisplay, 1, 4, 4, 2)

# 	Cadre du Tracé Courant

		self.groupBoxCurrent, self.trackCurrentId, self.trackCurrentCodes,  self.buttonCurrentCreate, self.buttonCurrentValidate, self.buttonCurrentDelete, self.selectTracksCombo = \
				menuDockCurrent(iface, self.mainFrame, self, self.dockEditWidget)
		self.groupBoxCurrent.repaint()
		DSTY.setBoxGeometryShort(self.groupBoxCurrent, 1, 7, 4, 2)

#	Cadre de la Table

		self.groupBoxTableFrame = menuDockTableFrame(iface, self.mainFrame, self, self.dockEditWidget)
		self.groupBoxTableFrame.repaint()
		DSTY.setBoxGeometryShort(self.groupBoxTableFrame, 1, 10, 4, 22)

#	Table elle-même

		self.tableWidget = menuBoxTable(iface, self.mainFrame, self, self.dockEditWidget)
		self.tableWidget.repaint()
		DSTY.setBoxGeometryShort(self.tableWidget, 1, 10, 4, 22, True)

#	Cadre du Statut

		self.groupBoxStatus, self.labelStatus = menuDockStatus(iface, self.mainFrame, self, self.dockEditWidget)
		self.groupBoxStatus.repaint()
		DSTY.setBoxGeometryShort(self.groupBoxStatus, 1, 33, 4, 1)

		self.boxesList = [self.groupBoxControls, self.groupBoxDisplay, self.groupBoxCurrent, self.groupBoxTableFrame, self.tableWidget, self.groupBoxStatus]


# ========================================================================================
# Fonctions hide / show / close / refresh
# ========================================================================================
	
	def hide(self):
		self.disconnectAll()																										# Déconnecter
		self.buttonReseauCW.setCheckState(Qt.Unchecked)																				# Afficher Tronçons-GR
		self.buttonReseauCW.setCheckState(Qt.Checked)																				# Afficher Tronçons-GR (Twice to be sure state is changed)
		self.buttonReseau50K.setCheckState(Qt.Checked)																				# Cacher Reseau 50K
		self.buttonReseau50K.setCheckState(Qt.Unchecked)																			# Cacher Reseau 50K (Twice to be sure state is changed)
		for box in self.boxesList:	box.hide()																						# Cacher tous les boxes ...
		self.dockEditWidget.setFixedWidth(10)																						# Rétrécir ...
		self.dockEditWidget.hide()																									# ... et cacher le dock widget
		QgsExpressionContextUtils.setProjectVariable(QgsProject.instance(), QGP.tablesSectionsGREd4VariableHighlight,'None')		# Annuler la variable de style
		self.mainFrame.setStatusDone("Bye - Edition du Réseau sur IGN 50 terminée")					

	def show(self):
		self.connectSectionsGR()																									# Reconnecter ...
		self.connect50K()																											# ...
		self.buttonReseauCW.setCheckState(Qt.Unchecked)																				# Afficher Tronçons-GR
		self.buttonReseauCW.setCheckState(Qt.Checked)																				# Afficher Tronçons-GR (Twice to be sure state is changed)
		self.buttonReseau50K.setCheckState(Qt.Checked)																				# Cacher Tronçons 50K
		self.buttonReseau50K.setCheckState(Qt.Unchecked)																			# Cacher Tronçons 50K (Twice to be sure state is changed)
		self.dockEditWidget.show()																									# Montrer ...
		self.dockEditWidget.setFixedWidth(500)																						# ... et élargir le dock widget
		for box in self.boxesList: box.show(), box.repaint()																		# Montrer tous les boxes ...
		self.activeMapFeature = self.mainFrame.selectedMapFeature																	# Retrouver la carte active ...
		self.buttonSelectActiveMap.setText(self.activeMapFeature[QGP.tableFramesFieldName] if self.activeMapFeature != None else '- - -')
			
	def close(self):
		self.disconnectAll()																										# Deconnecter
		self.hide()																													# Cacher et supprimer tous les widgets
		for box in self.boxesList: del box																							# ...
		self.iface.removeDockWidget(self.dockEditWidget)																			# ...
		del self.dockEditWidget																										# ...
		QgsExpressionContextUtils.setProjectVariable(QgsProject.instance(), QGP.tablesSectionsGREd4VariableHighlight,'None')		# Annuler la variable de style
		

# ========================================================================================
# Fonctions for setting the Status field : Error (red) // Warning (yellow) // Working (lime green) // Done (green) // Ok (grey)
# ========================================================================================

	def setStatusError(self, text):
		textFormat = DSTY.textFormatStatusErrorSmall
		self.labelStatus.setText(textFormat.replace('%TEXT%',text))
		self.labelStatus.setStyleSheet(DSTY.styleStatusError)
		QgsApplication.processEvents()

	def setStatusWarning(self, text):
		textFormat = DSTY.textFormatStatusWarningSmall
		self.labelStatus.setText(textFormat.replace('%TEXT%',text))
		self.labelStatus.setStyleSheet(DSTY.styleStatusWarning)
		QgsApplication.processEvents()

	def setStatusWorking(self, text):
		textFormat = DSTY.textFormatStatusWorkingSmall
		self.labelStatus.setText(textFormat.replace('%TEXT%',text))
		self.labelStatus.setStyleSheet(DSTY.styleStatusWorking)
		QgsApplication.processEvents()

	def setStatusDone(self, text):
		textFormat = DSTY.textFormatStatusWorkingSmall
		self.labelStatus.setText(textFormat.replace('%TEXT%',text))
		self.labelStatus.setStyleSheet(DSTY.styleStatusDone)
		QgsApplication.processEvents()

	def setStatusOk(self, text):
		textFormat = DSTY.textFormatStatusOkSmall
		self.labelStatus.setText(textFormat.replace('%TEXT%',text))
		self.labelStatus.setStyleSheet(DSTY.styleStatusOk)
		QgsApplication.processEvents()


# ========================================================================================
# Gestion des Boutons Actifs / Inactifs
# ========================================================================================

	def setButtonCurrentCreateActive(self):
		self.buttonCurrentCreateActive = True
		DSTY.setStyleNormalButton(self.buttonCurrentCreate)

	def setButtonCurrentCreateInactive(self):
		self.buttonCurrentCreateActive = False
		DSTY.setStyleMainButtonsInactive(self.buttonCurrentCreate)
	
	def setButtonCurrentValidateActive(self):
		self.buttonCurrentValidateActive = True
		DSTY.setStyleNormalButton(self.buttonCurrentValidate)

	def setButtonCurrentValidateInactive(self):
		self.buttonCurrentValidateActive = False
		DSTY.setStyleMainButtonsInactive(self.buttonCurrentValidate)
	
	def setButtonCurrentDeleteActive(self):
		self.buttonCurrentDeleteActive = True
		DSTY.setStyleNormalButton(self.buttonCurrentDelete)

	def setButtonCurrentDeleteInactive(self):
		self.buttonCurrentDeleteActive = False
		DSTY.setStyleMainButtonsInactive(self.buttonCurrentDelete)
	
	def setButtonsSaveCancelActive(self):
		DSTY.setStyleNormalButton(self.buttonCancel)
		DSTY.setStyleNormalButton(self.buttonSave)

	def setButtonsSaveCancelInactive(self):
		DSTY.setStyleMainButtonsInactive(self.buttonCancel)
		DSTY.setStyleMainButtonsInactive(self.buttonSave)


# ========================================================================================
# Connexions aux Couches Tronçons-GR et Tronçons-GR Ed4
# ========================================================================================
	
	def disconnectAll(self):
		try:
			self.layerSectionsGR.selectionChanged.disconnect()
			self.layer50K.selectionChanged.disconnect()
			self.layer50K.layerModified.disconnect()
		except:
			pass

	def connectSectionsGR(self):
		try:
			self.layerSectionsGR.selectionChanged.connect(self.layerSectionsGRSelectionChanged)
		except:
			pass

	def connect50K(self):
		if self.layer50K == None:
			self.setStatusError(self.layer50Kerror)
			return
		self.layer50K.selectionChanged.connect(self.layer50KSelectionChanged)
		self.layer50K.layerModified.connect(self.layer50KModified)


# ========================================================================================
# Actions des Couches Tronçons-GR et 50K
# ========================================================================================

	def layerSectionsGRSelectionChanged(self):
		if self.setSelectMuteSectionsGR: return
		idSection = [f[QGP.tableSectionsFieldId] for f in self.layerSectionsGR.getSelectedFeatures()]
		if len(idSection) == 0:																					# Aucune entité sélectionnée ...
			self.layer50KUpdateStatus()
			return
			
		if len(idSection) > 1:																					# Si plus d'une entité sélectionnée ...
			self.setStatusWarning('Sélectionnez une seule entité !')
			return 
		if idSection[0] not in self.dicoActiveSectionsGRFeatures:												# Si l'entité sélectionnée n'est pas dans la table ...
			self.setStatusWarning('Sélectionnez une entité qui se trouve dans la table !')
			return 
			
		self.setSelectMuteSectionsGR = True																		# Pour que l'appel ci-dessous n'ait pas d'effet ici
		self.layerSectionsGR.removeSelection()	
		self.setSelectMuteSectionsGR = False

		self.buttonReseauCW.setCheckState(Qt.Checked)															# Afficher Tronçons-GR
		self.iface.mapCanvas().redrawAllLayers()

		self.tableIndirectSelect = True
		self.setTableSelectedId(idSection[0])
		self.layer50KUpdateStatus()

	def layer50KSelectionChanged(self):
		id50K = [f[QGP.tableSectionsFieldId] for f in self.layer50K.getSelectedFeatures()]
		if len(id50K) == 0:																						# Rien à faire si la sélection est vide ...
			self.layer50KUpdateStatus()
			return
		if len(id50K) > 1:																						# Si plus d'une entité sélectionnée ...
			self.setStatusWarning('Sélectionnez une seule entité !')
			return
		if id50K[0] not in self.dicoActiveSectionsGRFeatures:													# Si l'entité sélectionnée n'est pas dans la table ...
			self.setStatusWarning('Sélectionnez une entité qui se trouve dans la table !')
			return
	
		self.buttonReseau50K.setCheckState(Qt.Checked)															# Afficher Tronçons 50K
		self.iface.mapCanvas().redrawAllLayers()

		self.tableIndirectSelect = True
		self.setTableSelectedId(id50K[0])
		self.layer50KUpdateStatus()
		tracesTableRefreshStyle(self.layer50K, self.tableWidget, self.dicoActiveSectionsGRFeatures, self.features50KDico)

	def layer50KModified(self):
		self.layer50KUpdateStatus()
		
	def layer50KUpdateStatus(self):
		if self.layer50K == None:
			self.setStatusError('Réseau 50K Non disponible !')
			return
		if self.layer50K.isModified():
			self.setButtonsSaveCancelActive()
			self.setStatusWarning('Réseau 50K Modifié !')
		else:
			self.setButtonsSaveCancelInactive()
			self.setStatusOk('Prêt')


# ========================================================================================
# Actions Principales du Cadre de Contrôle : Fermer // Enregistrer // Annuler // Maj Attributs
# ========================================================================================

	def buttonExit_clicked(self):
		self.hide()												# ... and self ... widget remains available
		self.mainMenu.show()

	def buttonSave_clicked(self):								
		if self.layer50K.isModified():
			self.layer50K.commitChanges()
		self.layer50KUpdateStatus()
		if self.lastSelect == 'Global' : 
			self.buttonSelectGlobal_process()
		if self.lastSelect == 'Global-All' : 
			self.buttonSelectGlobal_process(allMode = True)
		if self.lastSelect == 'Canevas' : 
			self.buttonSelectCanevas_process(False)
		if self.lastSelect == 'ActiveMap' : 
			self.buttonSelectActiveMap_process(False)

	def buttonCancel_clicked(self):
		if self.layer50K.isModified():
			self.layer50K.rollBack()
		self.layer50KUpdateStatus()
		if self.lastSelect == 'Canevas' : 
			self.buttonSelectCanevas_process(False)
		if self.lastSelect == 'ActiveMap' : 
			self.buttonSelectActiveMap_process(False)
	
	def buttonMajAttributes_clicked(self):
		self.buttonMajAttributesProcess()
		

# ========================================================================================
# Actions Sélection du Cadre de Contrôle : Global // Canevas // Carte
# ========================================================================================

	def buttonSelectGlobal_clicked(self):
		self.lastSelect = 'Global'
		self.buttonSelectGlobal_process()
		
	def buttonSelectGlobal_rightClicked(self):
		self.lastSelect = 'Global-All'
		self.buttonSelectGlobal_process(allMode = True)
	
	def buttonSelectCanevas_clicked(self):
		self.lastSelect = 'Canevas'
		self.buttonSelectCanevas_process(True)
		
	def buttonSelectActiveMap_clicked(self):
		self.lastSelect = 'ActiveMap'
		self.buttonSelectActiveMap_process(True)
		
# ========================================================================================
# Processing : Table sur Base Canevas
# ========================================================================================
	
	def buttonSelectCanevas_process(self, fullRefresh):

		if (self.layerSectionsGR == None) or (self.layer50K == None): 
			self.setStatusError("La couche Tronçons-GR et/ou Tronçons-GR-Ed4 n'est pas disponible ?")
			return

		type = 'GR' if self.selectTracksCombo.currentText() == C_Texte_Sections_SelectGR else 'ALL'
			
#	Create Sections Dico on Full Refresh (when really clicked)	

		if fullRefresh:											
			self.dicoActiveSectionsGRFeatures = { feature[QGP.tableSectionsFieldId] : feature for feature in self.layerSectionsGR.getFeatures(self.iface.mapCanvas().extent()) if type == 'ALL' or TCOD.getCodeListGRFromSectionFeature(feature) != [] }

#	Refresh 50K Dico in All Cases

		self.features50KDico = { feature[QGP.tableSectionsFieldId] : feature for feature in self.layer50K.getFeatures(self.iface.mapCanvas().extent()) }

#	And Refresh table
	
		tracesTableRefresh(self.tableWidget, self.dicoActiveSectionsGRFeatures, self.features50KDico, False)
		tracesTableRefreshStyle(self.layer50K, self.tableWidget, self.dicoActiveSectionsGRFeatures, self.features50KDico)

		self.setStatusDone('Recherche Canevas terminée !')


# ========================================================================================
# Processing : Table sur Base Carte Active
# ========================================================================================

	def buttonSelectActiveMap_process(self, fullRefresh):
			
		if (self.layerSectionsGR == None) or (self.layer50K == None): 
			self.setStatusError("La couche Tronçons-GR et/ou Tronçons-GR-Ed4 n'est pas disponible ?")
			return

		try:
			activeMapExtent = self.activeMapFeature.geometry().boundingBox()
		except:
			self.setStatusWarning('La Carte Active n\'est pas définie ?')
			return

		type = 'GR' if self.selectTracksCombo.currentText() == C_Texte_Sections_SelectGR else 'ALL'

#	Create Sections Dico on Full Refresh (when really clicked)	

		if fullRefresh:											
			self.dicoActiveSectionsGRFeatures = { feature[QGP.tableSectionsFieldId] : feature for feature in self.layerSectionsGR.getFeatures(activeMapExtent) if type == 'ALL' or TCOD.getCodeListGRFromSectionFeature(feature) != [] }

#	Refresh 50K Dico in All Cases

		self.features50KDico = { feature[QGP.tableSectionsFieldId] : feature for feature in self.layer50K.getFeatures(activeMapExtent) }
	
#	And Refresh table

		tracesTableRefresh(self.tableWidget, self.dicoActiveSectionsGRFeatures, self.features50KDico, False)
		tracesTableRefreshStyle(self.layer50K, self.tableWidget, self.dicoActiveSectionsGRFeatures, self.features50KDico)

		self.setStatusDone('Recherche Carte Active terminée !')

# ========================================================================================
# Processing : Table sur Base Globale
# ========================================================================================

	def buttonSelectGlobal_process(self, allMode = None):

		if (self.layerSectionsGR == None) or (self.layer50K == None): 
			self.setStatusError("La couche Tronçons-GR et/ou Tronçons-GR-Ed4 n'est pas disponible ?")
			return

# Nombre de lignes à remplir

		countMax = sum(1 for _ in self.layerSectionsGR.getFeatures()) if allMode else QGP.configSections50KGlobalMax 
		progressBar = TPRO.createProgressBar(self.buttonSelectGlobal, 10 + 10 + countMax, 'Short')
		
# Refresh an empty table while searching entities

		self.dicoActiveSectionsGRFeatures = {}
		self.features50KDico = {}
		tracesTableRefresh(self.tableWidget, self.dicoActiveSectionsGRFeatures, self.features50KDico, False)
		tracesTableRefreshStyle(self.layer50K, self.tableWidget, self.dicoActiveSectionsGRFeatures, self.features50KDico)
		self.setStatusWorking('Recherche des ' + str(countMax) + ' entités à définir / corriger ...')

# Compute dico of all Tronçons-GR entities and sort list of id's - Need to get all id's before sorting

		self.dicoActiveSectionsGRFeatures = { feature[QGP.tableSectionsFieldId] : feature for feature in self.layerSectionsGR.getFeatures() }
		progressBar.setValue(progressBar.value() + 10)

# Compute dico of all Réseau 50K entities

		self.features50KDico = { feature[QGP.tableSectionsFieldId] : feature for feature in self.layer50K.getFeatures() }
		progressBar.setValue(progressBar.value() + 10)
		
# Search for the N first entities where Réseau 50K is undefined or not correct

		idList = sorted(self.dicoActiveSectionsGRFeatures)

		count = 0
		for idSection in idList:
			QgsApplication.processEvents()
			if count >= countMax: 
				self.dicoActiveSectionsGRFeatures.pop(idSection)
				continue																											# Eliminate extra entities
			self.setStatusWorking('Recherche des entités à définir / corriger : ' + str(count) + ' / ' + str(countMax))
			feature = self.dicoActiveSectionsGRFeatures[idSection]
			if allMode :
				count += 1
				progressBar.setValue(progressBar.value() + 1)
				continue																											# Global all mode - keep it in list anyway
			if idSection not in self.features50KDico:
				count += 1
				progressBar.setValue(progressBar.value() + 1)
				continue																											# Section 50K not defined - keep it in list
			feature50K = self.features50KDico[idSection]	
			if getFeatureModificationLevel(feature50K, feature) > 0:
				count += 1
				progressBar.setValue(progressBar.value() + 1)
				continue																											# Section-GR Geometry changed - keep it in list
			self.dicoActiveSectionsGRFeatures.pop(idSection)																		# Section 50K up to date 
		
#	And Refresh table

		tracesTableRefresh(self.tableWidget, self.dicoActiveSectionsGRFeatures, self.features50KDico, False)
		tracesTableRefreshStyle(self.layer50K, self.tableWidget, self.dicoActiveSectionsGRFeatures, self.features50KDico)

		self.setStatusDone('Recherche Globale terminée !')
		del progressBar


# ========================================================================================
# Processing : Mise à jour attributs
# ========================================================================================

	def buttonMajAttributesProcess(self):
	
# 	Create Progress Bar

		progressBar = TPRO.createProgressBar(self.buttonMajAttributes, len(self.dicoActiveSectionsGRFeatures), 'Short')
		for idSection in self.dicoActiveSectionsGRFeatures:
			progressBar.setValue(progressBar.value() + 1)
			QgsApplication.processEvents()
			if idSection not in self.features50KDico: continue						
			if areFeatureAttributesIdentical(self.features50KDico[idSection], self.dicoActiveSectionsGRFeatures[idSection]): continue
			self.layer50K.startEditing()
			self.featureMajAttribtutes(idSection)

		tracesTableRefresh(self.tableWidget, self.dicoActiveSectionsGRFeatures, self.features50KDico, False)
		tracesTableRefreshStyle(self.layer50K, self.tableWidget, self.dicoActiveSectionsGRFeatures, self.features50KDico)

		self.setStatusDone('Attributs des entités de la table mis-à-jour !')
		del progressBar

	def featureMajAttribtutes(self, idSection):
		for fieldName in QGP.configSections50KFieldsCopyList: 
			index = self.features50KDico[idSection].fieldNameIndex(fieldName)
			self.features50KDico[idSection].setAttribute(index, self.dicoActiveSectionsGRFeatures[idSection].attribute(fieldName))
			self.layer50K.changeAttributeValue(self.features50KDico[idSection].id(),index,self.dicoActiveSectionsGRFeatures[idSection].attribute(fieldName))


# ========================================================================================
# Actions du Cadre Affichage
# ========================================================================================

# Affichage de la Carte CW / 50K

	def buttonCartoCW_clicked(self):
		TCAN.groupShowOnCanevas(QGP.configIGNCWGroupName, True)
		TCAN.groupShowOnCanevas(QGP.configIGN50Ed4GroupName, False)

	def buttonCarto50K_clicked(self):
		TCAN.groupShowOnCanevas(QGP.configIGNCWGroupName, False)
		TCAN.groupShowOnCanevas(QGP.configIGN50Ed4GroupName, True)

# Sélection sur Réseau CW / 50K

	def buttonSelectOnCW_clicked(self):
		self.buttonReseauCW.setCheckState(Qt.Checked)
		self.iface.layerTreeView().setCurrentLayer(self.layerSectionsGR)
		action = self.iface.actionSelect()
		action.trigger()
		
	def buttonSelectOn50K_clicked(self):
		self.buttonReseau50K.setCheckState(Qt.Checked)
		self.iface.layerTreeView().setCurrentLayer(self.layer50K)
		action = self.iface.actionSelect()
		action.trigger()

# Affichage du Réseau CW / 50K

	def buttonReseauCWChanged(self, state):
		if self.layerSectionsGR == None: return
		TCAN.layerShowOnCanevas(self.layerSectionsGR, state == Qt.Checked)

	def buttonReseau50KChanged(self, state):
		if self.layer50K == None: return
		TCAN.layerShowOnCanevas(self.layer50K, state == Qt.Checked)


# ========================================================================================
# Actions du Cadre Tronçon Actif
# ========================================================================================

# Action to display Current Id Info (when selection changes)

	def displayCurrentTrackInfo(self):

		if self.currentId == None:
			text = DSTY.textFormatBlackSmall.replace('%TEXT%',' X ')
			self.trackCurrentId.setText(text)
			DSTY.setStyleWarningLabel(self.trackCurrentId, "Short")
			self.trackCurrentCodes.setText(text)
			DSTY.setStyleWarningLabel(self.trackCurrentCodes, "ShortTriple")
			return

		text = DSTY.textFormatBlackSmall.replace('%TEXT%',self.currentId)
		self.trackCurrentId.setText(text)
		DSTY.setStyleOkLabel(self.trackCurrentId, "Short")
		gr_list = TCOD.getCodeListALLFromSectionFeature(self.dicoActiveSectionsGRFeatures[int(self.currentId)])
		text = 'Tous champs xx_list sont vides' if gr_list == [] else ' // '.join(gr_list)
		self.trackCurrentCodes.setText(text)
		DSTY.setStyleOkLabel(self.trackCurrentCodes, "ShortTriple")

# Action to zoom to current tronçon

	def buttonCurrentZoom_clicked(self):
		if self.currentId == None: return
		idSection = int(self.currentId)
		if idSection not in self.dicoActiveSectionsGRFeatures:	return	
		self.iface.mapCanvas().zoomToFeatureExtent(self.dicoActiveSectionsGRFeatures[idSection].geometry().boundingBox())
		if self.iface.mapCanvas().scale() < QGP.configSections50KMaxScale: self.iface.mapCanvas().zoomScale(QGP.configSections50KMaxScale)

# Création / Edition du tronçon courant
	
	def buttonCurrentCreate_clicked(self):
		if not self.buttonCurrentCreateActive: return	
		if self.currentId == None: return
		createdId = self.currentId																							# Save for below use - Refresh in Create kiils it 
		idSection = int(createdId)
		if idSection not in self.features50KDico:
			if not self.createCurrentProcess(idSection): return
		else:
			self.layer50K.startEditing()
		self.buttonReseauCW.setCheckState(Qt.Unchecked)
		self.buttonReseau50K.setCheckState(Qt.Checked)
		self.iface.layerTreeView().setCurrentLayer(self.layer50K)
		self.layer50K.selectByExpression('"' + QGP.tableSectionsFieldId + '"' + ' = ' + createdId)
		action = self.iface.actionVertexToolActiveLayer()
		action.trigger()	
	
	def createCurrentProcess(self, sectionId):
		if sectionId not in self.dicoActiveSectionsGRFeatures:									
			self.setStatusError('? ID inconnu au DICO Tronçons-GR - erreur interne ?')
			return False
		if sectionId in self.features50KDico:			
			self.setStatusError('ID déjà connu au DICO Tronçons-50K - erreur interne ?')
			return False
		
		idSection = self.dicoActiveSectionsGRFeatures[sectionId].id()															# Must retrieve original feature !
		geomSection = self.layerSectionsGR.getFeature(idSection).geometry()

		newFeature50K = QgsFeature()
		newFeature50K.setFields(self.layer50K.fields())
		newFeature50K.setAttribute(QGP.tableSectionsFieldId,sectionId)
		newFeature50K.setGeometry(geomSection)
		self.layer50K.startEditing()
		self.layer50K.addFeature(newFeature50K)
		self.features50KDico[sectionId] = newFeature50K
		self.featureMajAttribtutes(sectionId)

		tracesTableRefresh(self.tableWidget, self.dicoActiveSectionsGRFeatures, self.features50KDico, False)
		tracesTableRefreshStyle(self.layer50K, self.tableWidget, self.dicoActiveSectionsGRFeatures, self.features50KDico)
		tracesTableScrollToCurrentRow(self.tableWidget, self.currentRow)

		return True
	
# Validation du tronçon courant

	def buttonCurrentValidate_clicked(self):
		if not self.buttonCurrentValidateActive: return	
		if self.currentId == None: return
		createdId = self.currentId																								# Save for below use - Refresh in Create kiils it 
		self.updateCurrentValidation()
		self.buttonReseauCW.setCheckState(Qt.Checked)
		self.iface.layerTreeView().setCurrentLayer(self.layerSectionsGR)
		self.setTableSelectedId(int(createdId))
	
	def updateCurrentValidation(self):
		idSection = int(self.currentId)
		if idSection not in self.dicoActiveSectionsGRFeatures:									
			self.setStatusError('? ID inconnu au DICO Tronçons-GR - erreur interne ?')
			return False

		hashGeom, pts, dist, pAX, pAY, pZX, pZY = getFeatureValidationData(self.layerSectionsGR.getFeature(self.dicoActiveSectionsGRFeatures[idSection].id()))
		stamp = TDAT.getTimeStamp()	
	
		id50K = self.features50KDico[idSection].id()
		self.layer50K.startEditing()
		self.layer50K.changeAttributeValue(id50K,self.features50KDico[idSection].fieldNameIndex(QGP.tableSections50KFieldHash),hashGeom)
		self.layer50K.changeAttributeValue(id50K,self.features50KDico[idSection].fieldNameIndex(QGP.tableSections50KFieldPoints),pts)
		self.layer50K.changeAttributeValue(id50K,self.features50KDico[idSection].fieldNameIndex(QGP.tableSections50KFieldist),dist)
		self.layer50K.changeAttributeValue(id50K,self.features50KDico[idSection].fieldNameIndex(QGP.tableSections50KFieldPAX),pAX)
		self.layer50K.changeAttributeValue(id50K,self.features50KDico[idSection].fieldNameIndex(QGP.tableSections50KFieldPAY),pAY)
		self.layer50K.changeAttributeValue(id50K,self.features50KDico[idSection].fieldNameIndex(QGP.tableSections50KFieldPZX),pZX)
		self.layer50K.changeAttributeValue(id50K,self.features50KDico[idSection].fieldNameIndex(QGP.tableSections50KFieldPZY),pZY)
		self.layer50K.changeAttributeValue(id50K,self.features50KDico[idSection].fieldNameIndex(QGP.tableSections50KFieldDate),stamp)
		self.layer50K.changeAttributeValue(id50K,self.features50KDico[idSection].fieldNameIndex(QGP.tableSections50KFieldValidation),QgsApplication.userFullName())

		self.features50KDico[idSection].setAttribute(QGP.tableSections50KFieldDate,stamp)
		self.features50KDico[idSection].setAttribute(QGP.tableSections50KFieldValidation,QgsApplication.userFullName())
		self.features50KDico[idSection].setAttribute(QGP.tableSections50KFieldHash,hashGeom)
		self.features50KDico[idSection].setGeometry(self.layer50K.getFeature(id50K).geometry())

		self.layer50K.removeSelection()	

		tracesTableRefresh(self.tableWidget, self.dicoActiveSectionsGRFeatures, self.features50KDico, False)
		tracesTableRefreshStyle(self.layer50K, self.tableWidget, self.dicoActiveSectionsGRFeatures, self.features50KDico)
		tracesTableScrollToCurrentRow(self.tableWidget, self.currentRow)
	
# Validation de tous les tronçons non réellement modifiés lors de la migration
# Usage Unique !!!!

	def buttonAllValidate_clicked(self):
		return																# Disabled after unique usage - kept for any future use
		countStart = 3501; countEnd = 3560
		self.setStatusWorking('Validation des tronçons migrés simplfiés ...')
		features50KList = [feature for feature in self.layer50K.getFeatures()]
		features50KList = sorted(features50KList, key=lambda f: int(f[QGP.tableSectionsFieldId]))
		self.setStatusWorking('Validation des tronçons migrés simplfiés - ' + str(countEnd - countStart + 1)  + ' tronçons ...')
		self.layerOld,	self.layerOldEerror = TLAY.openLayer('Old-ReseauGR-Complet_A-Jour')
		self.layer50K.startEditing()
		progressBar = TPRO.createProgressBar(self.buttonAllValidate, countEnd - countStart + 1 , 'Short')
		loopCount = validatedCount = 0

		for feature50K in features50KList :
			loopCount += 1
			if loopCount < countStart : continue
			if loopCount > countEnd : break
			progressBar.setValue(progressBar.value() + 1)
			QgsApplication.processEvents()

			idSection = int(feature50K[QGP.tableSections50KFieldId])
			print('buttonAllValidate_clicked - id = ' + str(idSection))
			if feature50K[QGP.tableSections50KFieldValidation] == None : continue
			featureOld = [f for f in self.layerOld.getFeatures('"' + QGP.tableSectionsFieldId + '"' + ' = ' + str(idSection))]
			if len(featureOld) != 1 : continue
			featureOld = featureOld[0]
			if not featureOld.isValid() : continue
			featureNew = [f for f in self.layerSectionsGR.getFeatures('"' + QGP.tableSectionsFieldId + '"' + ' = ' + str(idSection))]
			if len(featureNew) != 1 : continue
			featureNew = featureNew[0]
			if not featureNew.isValid() : continue
			if featureNew.geometry().hausdorffDistance(featureOld.geometry()) > 1 : continue

			hashGeom, pts, dist, pAX, pAY, pZX, pZY = getFeatureValidationData(featureNew)
	
			self.layer50K.changeAttributeValue(feature50K.id(),feature50K.fieldNameIndex(QGP.tableSections50KFieldHash),hashGeom)
			self.layer50K.changeAttributeValue(feature50K.id(),feature50K.fieldNameIndex(QGP.tableSections50KFieldPoints),pts)
			self.layer50K.changeAttributeValue(feature50K.id(),feature50K.fieldNameIndex(QGP.tableSections50KFieldist),dist)
			self.layer50K.changeAttributeValue(feature50K.id(),feature50K.fieldNameIndex(QGP.tableSections50KFieldPAX),pAX)
			self.layer50K.changeAttributeValue(feature50K.id(),feature50K.fieldNameIndex(QGP.tableSections50KFieldPAY),pAY)
			self.layer50K.changeAttributeValue(feature50K.id(),feature50K.fieldNameIndex(QGP.tableSections50KFieldPZX),pZX)
			self.layer50K.changeAttributeValue(feature50K.id(),feature50K.fieldNameIndex(QGP.tableSections50KFieldPZY),pZY)

			validatedCount += 1
			print('buttonAllValidate_clicked - id = ' + str(idSection) + ' - validated')


		self.setStatusDone('Validation des tronçons migrés simplfiés - TBC ' + str(validatedCount) + ' validations' )
		del progressBar
	
	
# Suppression du tronçon courant
				
	def buttonCurrentDelete_clicked(self):
		if not self.buttonCurrentDeleteActive: return	
		if self.currentId == None: return
		deletedId = self.currentId																							
		idSection = int(deletedId)
		if idSection not in self.features50KDico:
			self.setStatusError('ID  inconnu au DICO 50K - erreur interne ?')
			return 
		self.layer50K.startEditing()
		self.layer50K.deleteFeature(self.features50KDico[idSection].id())
		self.features50KDico.pop(idSection)

		tracesTableRefresh(self.tableWidget, self.dicoActiveSectionsGRFeatures, self.features50KDico, False)
		tracesTableRefreshStyle(self.layer50K, self.tableWidget, self.dicoActiveSectionsGRFeatures, self.features50KDico)
		tracesTableScrollToCurrentRow(self.tableWidget, self.currentRow)

		self.setTableSelectedId(int(deletedId))


# ========================================================================================
# Connexions à la Table
# ========================================================================================

# ----------------------------------------------------------
# Sélectionner un item de la table quand sélection sur couche
# ----------------------------------------------------------

	def setTableSelectedId(self, idSection):

		listIdTable = sorted([x for x in self.dicoActiveSectionsGRFeatures])
		tableIndex = listIdTable.index(idSection)

		self.tableWidget.clearSelection()
		self.tableWidget.setRangeSelected(QtWidgets.QTableWidgetSelectionRange(tableIndex, 0, tableIndex, 0), True)
		
		self.setStatusWorking('Tronçon ' + str(idSection) + ' sélectionné - Ligne ' + str(tableIndex + 1))

# ----------------------------------------------------------
# Changement de sélection dans la table (direct ou indirect)
# ----------------------------------------------------------

	def tableWidget_selectionChanged(self):

	# Clear info for case selection is not valid

		QgsExpressionContextUtils.setProjectVariable(QgsProject.instance(),QGP.tablesSectionsGREd4VariableHighlight, 'None')
		self.currentId = None
		idList = tracesTableSelectedIdList(self.tableWidget)
		if len(idList) == 0: return																			# Be sure not loop when recursively called

	# Clear selection if more than one - will recursively call and stop for len == 0

		if len(idList) > 1:
			self.tableWidget.clearSelection()

	# Valid selection - only one ID

		else:
			self.currentId = idList[0]

			if self.buttonIdentification.isChecked() :
				if self.mainFrame.identificationWindow == None:
					self.setStatusWorking('Initialisation de la fenêtre d\'dentification ...')
					self.mainFrame.identificationWindow = PIDE.identificationView(self.iface, self.mainFrame)
					self.setStatusDone('Initialisation de la fenêtre d\'dentification - OK')
				self.mainFrame.identificationWindow.show()
				self.mainFrame.identificationWindow.update(self.dicoActiveSectionsGRFeatures[int(self.currentId)])

			QgsExpressionContextUtils.setProjectVariable(QgsProject.instance(),QGP.tablesSectionsGREd4VariableHighlight, self.currentId)

			listIdTable = sorted([x for x in self.dicoActiveSectionsGRFeatures])
			self.currentRow = listIdTable.index(int(self.currentId))

	# Update track info display

		self.displayCurrentTrackInfo()
		
	# Activate / Deactivate Buttons

		if self.currentId == None:
			self.setButtonCurrentCreateInactive()	
			self.setButtonCurrentValidateInactive()	
			self.setButtonCurrentDeleteInactive()	
		else:
			if int(self.currentId) in self.features50KDico:
				self.setButtonCurrentCreateActive()	
				self.setButtonCurrentValidateActive()
				self.setButtonCurrentDeleteActive()
			else:
				self.setButtonCurrentCreateActive()	
				self.setButtonCurrentValidateInactive()	
				self.setButtonCurrentDeleteInactive()	

	# Auto Zoom 

		if self.buttonAutoZoom.checkState() == Qt.Checked:
			self.buttonCurrentZoom_clicked()

	# Scroll 

		if self.tableIndirectSelect:
			if self.currentId != None:
				listIdTable = sorted([x for x in self.dicoActiveSectionsGRFeatures])
				tableIndex = listIdTable.index(int(self.currentId))
				self.tableWidget.scrollToTop()
				self.tableWidget.scrollToItem(self.tableWidget.item(min(tableIndex + 6, len(listIdTable) - 1), 0))			
			self.tableIndirectSelect = False


# ========================================================================================
# Actions Help
# ========================================================================================

	def buttonHelpControls_clicked(self):
		webbrowser.open_new_tab(QGP.configMenuHelpBasePath + 'QCarto - Dock - Edition 50K.html')


# ========================================================================================
# Créer le cadre : Contrôles
# >>> iface
# >>> mainFrame 	: class mainMenuFrame				Top-level Frame (Tableau de Bord)
# >>> parentFrame   : class menuDockEdit				Parent Frame
# >>> parentWidget  : widget							Where to install local Widgets
# ========================================================================================

def menuDockControls(iface, mainFrame, parentFrame, parentWidget):

# ----------------------------------------------------------
# Créer Groupe : Contrôles
# ----------------------------------------------------------
		
	groupBox = QtWidgets.QGroupBox(parentFrame.tableEditName + ' - Contrôles', parentWidget)
	groupBox.setStyleSheet(DSTY.styleBox)

# ----------------------------------------------------------
# Ajouter Bouton : Select Global // Canevas // Carte Active
# ----------------------------------------------------------

	parentFrame.buttonSelectGlobal = TBUT.createActionButton(groupBox, 1, 1, 'Global', 'Short')
	parentFrame.buttonSelectGlobal.clicked.connect(parentFrame.buttonSelectGlobal_clicked)
	parentFrame.buttonSelectGlobal.setContextMenuPolicy(Qt.CustomContextMenu)
	parentFrame.buttonSelectGlobal.customContextMenuRequested.connect(parentFrame.buttonSelectGlobal_rightClicked)

	buttonSelectCanevas = TBUT.createActionButton(groupBox, 2, 1, 'Canevas', 'Short')
	buttonSelectCanevas.clicked.connect(parentFrame.buttonSelectCanevas_clicked)

	buttonSelectActiveMap = TBUT.createActionButton(groupBox, 3, 1, 'Carte Active', 'Short')
	buttonSelectActiveMap.clicked.connect(parentFrame.buttonSelectActiveMap_clicked)

# ----------------------------------------------------------
# Ajouter Boutons : MAJ Attributs // Annuler // Enregistrer // Fermer
# ----------------------------------------------------------

	parentFrame.buttonMajAttributes = TBUT.createActionButton(groupBox, 1, 2, 'MAJ Attributs', 'Short')
	parentFrame.buttonMajAttributes.clicked.connect(parentFrame.buttonMajAttributes_clicked)

	buttonSave = TBUT.createActionButton(groupBox, 2, 2, 'Enregistrer', 'Short')
	buttonSave.clicked.connect(parentFrame.buttonSave_clicked)

	buttonCancel = TBUT.createActionButton(groupBox, 3, 2, 'Annuler', 'Short')
	buttonCancel.clicked.connect(parentFrame.buttonCancel_clicked)

	buttonExit = TBUT.createActionButton(groupBox, 4, 2, 'Fermer', 'Short')
	buttonExit.clicked.connect(parentFrame.buttonExit_clicked)

# ----------------------------------------------------------
# Ajouter Bouton : Help
# ----------------------------------------------------------

	buttonHelpControls = TBUT.createHelpButton(groupBox, 4, 1, 'Aide', 'Short')
	buttonHelpControls.clicked.connect(parentFrame.buttonHelpControls_clicked)
	
	return groupBox, buttonSelectActiveMap, buttonCancel, buttonSave, buttonExit


# ========================================================================================
# Créer le cadre : Display
# >>> iface
# >>> mainFrame 	: class mainMenuFrame				Top-level Frame (Tableau de Bord)
# >>> parentFrame   : class menuDockEdit				Parent Frame
# >>> parentWidget  : widget							Where to install local Widgets
# ========================================================================================

def menuDockDisplay(iface, mainFrame, parentFrame, parentWidget):

# ----------------------------------------------------------
# Créer Groupe : Affichage
# ----------------------------------------------------------
		
	groupBox = QtWidgets.QGroupBox("Affichage", parentWidget)
	groupBox.setStyleSheet(DSTY.styleBox)

# ----------------------------------------------------------
# Ajouter Boutons : Carto CW / Carto 50K
# ----------------------------------------------------------

	buttonCartoCW = TBUT.createActionButton(groupBox, 1, 1, 'Carte CW', 'Short')
	buttonCartoCW.clicked.connect(parentFrame.buttonCartoCW_clicked)

	buttonCarto50K = TBUT.createActionButton(groupBox, 1, 2, 'Carte 50K', 'Short')
	buttonCarto50K.clicked.connect(parentFrame.buttonCarto50K_clicked)

# ----------------------------------------------------------
# Ajouter Boutons : Select Réseau CW / 50K
# ----------------------------------------------------------

	buttonSelectOnCW = TBUT.createActionButton(groupBox, 2, 1, 'Sel Réseau CW', 'Short')
	buttonSelectOnCW.clicked.connect(parentFrame.buttonSelectOnCW_clicked)

	buttonSelectOn50K = TBUT.createActionButton(groupBox, 2, 2, 'Sel Réseau 50K', 'Short')
	buttonSelectOn50K.clicked.connect(parentFrame.buttonSelectOn50K_clicked)

# ----------------------------------------------------------
# Ajouter Check Boxes : Réseau CW / Réseau 50K
# ----------------------------------------------------------

	buttonReseauCW = TBUT.createCheckBoxButton(groupBox, 3, 1, 'Réseau CW', 'Short')
	buttonReseauCW.setCheckState(Qt.Checked)
	buttonReseauCW.stateChanged.connect(parentFrame.buttonReseauCWChanged)
	
	buttonReseau50K = TBUT.createCheckBoxButton(groupBox, 3, 2, 'Réseau 50K', 'Short')
	buttonReseau50K.setCheckState(Qt.Unchecked)
	buttonReseau50K.stateChanged.connect(parentFrame.buttonReseau50KChanged)

# ----------------------------------------------------------
# Ajouter Check Boxes : AutoZoom / Identification
# ----------------------------------------------------------

	buttonAutoZoom  = TBUT.createCheckBoxButton(groupBox, 4, 1, 'Auto Zoom', 'Short')
	buttonAutoZoom.setCheckState(Qt.Checked)

	buttonIdentification  = TBUT.createCheckBoxButton(groupBox, 4, 2, 'Identification', 'Short')
	buttonIdentification.setCheckState(Qt.Unchecked)

	return groupBox, buttonReseauCW, buttonReseau50K, buttonAutoZoom, buttonIdentification


# ========================================================================================
# Créer le cadre : Current
# >>> iface
# >>> mainFrame 	: class mainMenuFrame				Top-level Frame (Tableau de Bord)
# >>> parentFrame   : class menuDockEdit				Parent Frame
# >>> parentWidget  : widget							Where to install local Widgets
# ========================================================================================

def menuDockCurrent(iface, mainFrame, parentFrame, parentWidget):

# ----------------------------------------------------------
# Créer Groupe : Current
# ----------------------------------------------------------
		
	groupBox = QtWidgets.QGroupBox("Tronçon Actif", parentWidget)
	groupBox.setStyleSheet(DSTY.styleBox)

# ----------------------------------------------------------
# Ajouter Info pour : Current Id + Gr_Codes
# ----------------------------------------------------------

	trackCurrentId = TBUT.createLabelGreenButton(groupBox, 1, 1, '. . .', 'Short', 'Normal')
	DSTY.setStyleWarningLabel(trackCurrentId, "Short")

	trackCurrentIdHiddenButton = TBUT.createActionButtonTransparent(groupBox, 1, 1, '', 'Short')
	trackCurrentIdHiddenButton.clicked.connect(parentFrame.buttonCurrentZoom_clicked)

	trackCurrentCodes = TBUT.createLabelGreenButton(groupBox, 2, 1, '. . .', 'ShortTriple', 'Normal')
	DSTY.setStyleWarningLabel(trackCurrentCodes, "ShortTriple")

# ----------------------------------------------------------
# Ajouter Combo : selection tracés
# ----------------------------------------------------------

	selectTracksCombo = TBUT.createComboButton(groupBox, 4, 2, 'Short')
	selectTracksCombo.addItem(C_Texte_Sections_SelectAll)
	selectTracksCombo.addItem(C_Texte_Sections_SelectGR)
	
# ----------------------------------------------------------
# Ajouter Boutons : Créer / Valider / Supprimer
# ----------------------------------------------------------

	buttonCurrentCreate = TBUT.createActionButton(groupBox, 1, 2, 'Créer / Editer', 'Short')
	buttonCurrentCreate.clicked.connect(parentFrame.buttonCurrentCreate_clicked)

	buttonCurrentValidate = TBUT.createActionButton(groupBox, 2, 2, 'Valider', 'Short')
	buttonCurrentValidate.clicked.connect(parentFrame.buttonCurrentValidate_clicked)

	buttonCurrentDelete = TBUT.createActionButton(groupBox, 3, 2, 'Supprimer', 'Short')
	buttonCurrentDelete.clicked.connect(parentFrame.buttonCurrentDelete_clicked)

	return groupBox, trackCurrentId, trackCurrentCodes, buttonCurrentCreate, buttonCurrentValidate, buttonCurrentDelete, selectTracksCombo
	

# ========================================================================================
# Créer le cadre : Cadre Table
# >>> iface
# >>> mainFrame 	: class mainMenuFrame				Top-level Frame (Tableau de Bord)
# >>> parentFrame   : class menuDockEdit				Parent Frame
# >>> parentWidget  : widget							Where to install local Widgets
# ========================================================================================

def menuDockTableFrame(iface, mainFrame, parentFrame, parentWidget):

# ----------------------------------------------------------
# Créer Groupe : Contrôles
# ----------------------------------------------------------
		
	groupBox = QtWidgets.QGroupBox("Table des Tronçons", parentWidget)
	groupBox.setStyleSheet(DSTY.styleBox)

	return groupBox


# ========================================================================================
# Créer la table elle-même
# >>> iface
# >>> mainFrame 	: class mainMenuFrame				Top-level Frame (Tableau de Bord)
# >>> parentFrame   : class menuDockEdit				Parent Frame
# >>> parentWidget  : widget							Where to install local Widgets
# ========================================================================================

def menuBoxTable(iface, mainFrame, parentFrame, parentWidget):

# ----------------------------------------------------------
# Créer la Table 
# ----------------------------------------------------------
		
	rowsCount = 0
	columnsCount = len(QGP.configTableEdit50KFields)
		
	tableWidget = QtWidgets.QTableWidget(rowsCount,columnsCount,parentWidget)
	tableWidget.repaint()
	
	DSTY.setStyleTableTraces(tableWidget)
	
# ----------------------------------------------------------
# Entêtes de colonnes
# ----------------------------------------------------------
	
	tableFields = QGP.configTableEdit50KFields
	tableWidget.horizontalHeader().setMinimumSectionSize(2)
	
	for col in range(len(tableFields)):
		tableWidget.setHorizontalHeaderItem(col, QtWidgets.QTableWidgetItem(tableFields[col][0]))
		tableWidget.setColumnWidth(col, tableFields[col][1])

	tracesTableRefresh(tableWidget, None, None, True)

# ----------------------------------------------------------
# Catch Signal of Selection Change
# ----------------------------------------------------------

	tableWidget.itemSelectionChanged.connect(parentFrame.tableWidget_selectionChanged)

	return tableWidget


# ========================================================================================
# Calculer la liste des Id sélectionnés et des lignes sélectionnées
# >>> table 		: table widget
# <<< idList		:
# ========================================================================================

def tracesTableSelectedIdList(tableWidget):

	idList = []

	for row in range(tableWidget.rowCount()):
		codeItem = tableWidget.item(row, 0)
		if codeItem.isSelected():
			idList.append(codeItem.text())

	return idList


# ========================================================================================
# Remplir / Rafraichir la Table
# >>> table 			: table widget
# >>> dicoActiveSectionsGRFeatures  : {ID: featureRACJ}			Dictionnaire des Features du Réseau GR
# >>> features50KDico   : {ID: featureRACJ}			Dictionnaire des Features du Réseau GR 50K
# >>> initFlag			: bool						True : initialize table
#													False : refresh table (default)
# ========================================================================================

def tracesTableRefresh(tableWidget, dicoActiveSectionsGRFeatures, features50KDico, initFlag = False):
	
	if initFlag:
		tableWidget.setRowCount(0)
		return

	tableWidget.setSortingEnabled(False)							# This is needed ! Otherwise lines are sorted when filled and this results in garbage !
	tableWidget.clearContents()
	tableWidget.setRowCount(len(dicoActiveSectionsGRFeatures))

	listId = sorted([x for x in dicoActiveSectionsGRFeatures])
	listId50K = [x for x in features50KDico]

	itemFont = QFont()
	itemFont.setPixelSize(DSTY.tableItemFontSize)
	itemFontSmall = QFont()
	itemFontSmall.setPixelSize(DSTY.tableItemFontSizeSmall)

	today = TDAT.getTimeStamp()[0:10]

	row = 0
	for id in listId:
	
		tableWidget.setRowHeight(row, 20)
	
		# Colonne ID
	
		itemText = str(id)
		item = QtWidgets.QTableWidgetItem(itemText)
		item.setTextAlignment(Qt.AlignCenter | Qt.AlignVCenter)
		item.setFont(itemFont)
		tableWidget.setItem(row, QGP.C_Table_Edit50K_Index_Id, item)
		
		# Colonne Date (Format YYYY-MM-DD HH-MM)
		
		itemText = str(features50KDico[id].attribute(QGP.tableSections50KFieldDate))[0:16] if id in features50KDico else 'Non défini'
		item = QtWidgets.QTableWidgetItem(itemText)
		item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
		item.setFont(itemFontSmall)
		if itemText[0:10] == today : item.setBackground(DCOL.bgTableToday)
		tableWidget.setItem(row, QGP.C_Table_Edit50K_Index_Date, item)

		# Colonne Carto
		
		if id in features50KDico:

			itemText = str(features50KDico[id].attribute(QGP.tableSections50KFieldValidation))				# Str to handle NULL case
			itemText = itemText.split()[0]
			item = QtWidgets.QTableWidgetItem(itemText)
			item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
			item.setFont(itemFontSmall)
			tableWidget.setItem(row, QGP.C_Table_Edit50K_Index_Carto, item)
		
		# Colonne Géométrie
		
			level = getFeatureModificationLevel(features50KDico[id], dicoActiveSectionsGRFeatures[id])
			if (level == 0): itemHashText = 'Identique'
			if (level == 1): itemHashText = 'Similaire'
			if (level == 2): itemHashText = 'Modifiée ~'
			if (level == 3): itemHashText = 'Modifiée'
			if (level >= 4): itemHashText = 'Modifiée >'
			item = QtWidgets.QTableWidgetItem(itemHashText)
			item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
			item.setFont(itemFontSmall)
			tableWidget.setItem(row, QGP.C_Table_Edit50K_Index_GeometryInfo, item)
		
		# Colonne Géométrie Couleur
		
			item = QtWidgets.QTableWidgetItem('')
			if (level == 0): item.setBackground(DCOL.bgTable50KUnchanged)
			if (level == 1): item.setBackground(DCOL.bgTable50KLevel1)
			if (level == 2): item.setBackground(DCOL.bgTable50KLevel2)
			if (level == 3): item.setBackground(DCOL.bgTable50KLevel3)
			if (level >= 4): item.setBackground(DCOL.bgTable50KInvalid)
			tableWidget.setItem(row, QGP.C_Table_Edit50K_Index_GeometryColor, item)

		# Colonne Attributs

			attributesIdentical = areFeatureAttributesIdentical(features50KDico[id], dicoActiveSectionsGRFeatures[id])
			itemText = 'Identiques' if attributesIdentical else 'Modifiés'
			item = QtWidgets.QTableWidgetItem(itemText)
			item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
			item.setFont(itemFontSmall)
			tableWidget.setItem(row, QGP.C_Table_Edit50K_Index_AttributesInfo, item)

		# Colonne Attributs Couleur
		
			item = QtWidgets.QTableWidgetItem('')
			item.setBackground(DCOL.bgTable50KUnchanged) if attributesIdentical else item.setBackground(DCOL.bgTable50KInvalid)
			tableWidget.setItem(row, QGP.C_Table_Edit50K_Index_AttributesColor, item)

		# Colonne Delta Hausdorff

			if id in features50KDico:
				geometryCW = dicoActiveSectionsGRFeatures[id].geometry()
				geometry50K = features50KDico[id].geometry()
				distanceHausdorff = geometryCW.hausdorffDistance(geometry50K)
				itemText = str(int(round(distanceHausdorff,0)))
				level = 0
				if distanceHausdorff > 0: level = 1
				if distanceHausdorff > QGP.config50KDeltaMaxNormal: level = 2
				if distanceHausdorff > QGP.config50KDeltaMaxWarning: level = 3
			else:
				itemText = ''
				level = -1

			item = QtWidgets.QTableWidgetItem(itemText)
			item.setTextAlignment(Qt.AlignRight | Qt.AlignVCenter)
			item.setFont(itemFontSmall)
			
			if level == 3:  item.setBackground(DCOL.bgTable50KInvalid)
			if level == 2:  item.setBackground(DCOL.bgTable50KLevel2)
			if level == 1:  item.setBackground(DCOL.bgTable50KLevel1)
			if level == 0:  item.setBackground(DCOL.bgTable50KUnchanged)
			
			tableWidget.setItem(row, QGP.C_Table_Edit50K_Index_AttributesDelta, item)
			
		row += 1


# ========================================================================================
# Highlight features selected in layer 50 K
# >>> layer50K
# >>> table 			: table widget
# >>> dicoActiveSectionsGRFeatures  : canvas features Dico : Réseau GR
# >>> features50KDico   : canvas features Dico : Réseau GR on 50K
# >>> initFlag			: first call - clear rows - default = False
# ========================================================================================

def tracesTableRefreshStyle(layer50K, tableWidget, dicoActiveSectionsGRFeatures, features50KDico):

	listId = sorted([x for x in dicoActiveSectionsGRFeatures])
	listId50K = [x for x in features50KDico]
	listId50KSelected = [x.attribute(QGP.tableSections50KFieldId) for x in layer50K.getSelectedFeatures()]

	if len(listId) == 0: return

# Lowlight when Track in 50K is not defined
	
	row = 0
	for id in listId:
		if id in features50KDico:
			tableWidget.item(row, QGP.C_Table_Edit50K_Index_Id).setForeground(DCOL.fgTable50KNormal)
			tableWidget.item(row, QGP.C_Table_Edit50K_Index_Date).setForeground(DCOL.fgTable50KNormal)
			tableWidget.item(row, QGP.C_Table_Edit50K_Index_Carto).setForeground(DCOL.fgTable50KNormal)
		else:
			tableWidget.item(row, QGP.C_Table_Edit50K_Index_Id).setForeground(DCOL.fgTable50KNotDefined)
			tableWidget.item(row, QGP.C_Table_Edit50K_Index_Date).setForeground(DCOL.fgTable50KNotDefined)
		row += 1

# Highlight when Track in 50K is Selected

	row = 0
	for id in listId:
		if id in listId50KSelected:
			tableWidget.item(row, QGP.C_Table_Edit50K_Index_Date).setBackground(DCOL.bgTable50KSelected)
		else:
			tableWidget.item(row, QGP.C_Table_Edit50K_Index_Date).setBackground(DCOL.bgTable50KNormal)
		row += 1

			
# ========================================================================================
# Scroller pour afficher la ligne courante
# >>> table 			: table widget
# >>> showRow 			: Ligne à afficher
# ========================================================================================
			
def tracesTableScrollToCurrentRow(tableWidget, showRow):
	if showRow != None:		
		tableWidget.scrollToTop()
		tableWidget.scrollToItem(tableWidget.item(showRow + 6,0))					# 6 to be a bit above bottom
				
			
# ========================================================================================
# Créer le cadre : Statut
# >>> iface
# >>> mainFrame 	: class mainFrame			Top-level Frame (Tableau de Brod)
# >>> parentFrame   : class menuDockEdit			Parent Frame that calls this 
# >>> parentWidget  : widget						Parent widget where to install local Widgets
# ========================================================================================

def menuDockStatus(iface, mainFrame, parentFrame, parentWidget):

# ----------------------------------------------------------
# Créer Groupe : Statut
# ----------------------------------------------------------

	groupBox = QtWidgets.QGroupBox("Statut",parentWidget)
	groupBox.setStyleSheet(DSTY.styleBox)

# ----------------------------------------------------------
# Ajouter Label : Erreur
# ----------------------------------------------------------

	labelStatus = QtWidgets.QLabel(groupBox)
	DSTY.setStatusLabel(labelStatus, 4, 'Short')

#	parentFrame.buttonAllValidate = TBUT.createActionButton(groupBox, 1, 2, 'Valider', 'Short')
#	parentFrame.buttonAllValidate.clicked.connect(parentFrame.buttonAllValidate_clicked)


	return groupBox, labelStatus


# ========================================================================================
# Obtenir Hash et données Validation pour la géométrie d'une feature Tronçons-GR
# >>> feature : QgsFeature				Feature de la couche Réseau GR
# <<< hash		  : int						Hash on Geometry
# <<< pts		  : int						Count of Points in Geometry
# <<< dist		  : int						Distance in mm
# <<< pAX		  : int						Lambert 08 X of First Point (integer part rounded)
# <<< pAY		  : int						Lambert 08 Y of First Point (integer part rounded)
# <<< pZX		  : int						Lambert 08 X of Last Point (integer part rounded)
# <<< pZY		  : int						Lambert 08 Y of Last Point (integer part rounded)
# ========================================================================================

def getFeatureValidationData(feature):

	geom = feature.geometry()
	geomText = geom.asWkt(3)										# mm precision (3) is enough
	hash = hashlib.sha3_256()										# keccak - thanks to my ex-collegues
	hash.update(geomText.encode())
	hashGeom = int(hash.hexdigest()[0:10],16)						# keep 5 hex digit - 2^8^5 = 2^40 ~ 10^12 - collision probability is very low 
	pts = len(geom.asMultiPolyline()[0])
	dist = round(1000 * geom.length())
	pAX = round(geom.asMultiPolyline()[0][0].x())
	pAY = round(geom.asMultiPolyline()[0][0].y())
	pZX = round(geom.asMultiPolyline()[0][-1].x())
	pZY = round(geom.asMultiPolyline()[0][-1].y())

	return hashGeom, pts, dist, pAX, pAY, pZX, pZY


# ========================================================================================
# Calculer le niveau de modification de la géométrie depuis la validation
# >>> feature50K  : QgsFeature				Feature de la couche Tronçons 50K
# >>> featureCW  : QgsFeature				Feature de la couche Tronçons GR
# <<< level		  : int						0 = hash unchanged // 1 = very small deltas // 2 = small deltas // 3 = medium deltas // 4 = large deltas
# ========================================================================================

def getFeatureModificationLevel(feature50K, featureCW):

	maxLevel1 = QGP.configDiff50KMaxLevel1
	maxLevel2  = QGP.configDiff50KMaxLevel2
	maxLevel3  = QGP.configDiff50KMaxLevel3

	hash50K = feature50K.attribute(QGP.tableSections50KFieldHash)
	dist50K = feature50K.attribute(QGP.tableSections50KFieldist)
	pts50K = feature50K.attribute(QGP.tableSections50KFieldPoints)
	pAX50K = feature50K.attribute(QGP.tableSections50KFieldPAX)
	pAY50K = feature50K.attribute(QGP.tableSections50KFieldPAY)
	pZX50K = feature50K.attribute(QGP.tableSections50KFieldPZX)
	pZY50K = feature50K.attribute(QGP.tableSections50KFieldPZY)
	if hash50K == None : hash50K = 999999999
	if dist50K == None : dist50K = 999999999
	if pts50K == None : pts50K = 999999999
	if pAX50K == None : pAX50K = 999999999
	if pAY50K == None : pAY50K = 999999999
	if pZX50K == None : pZX50K = 999999999
	if pZY50K == None : pZY50K = 999999999

	hashGeom, pts, dist, pAX, pAY, pZX, pZY = getFeatureValidationData(featureCW)
	deltaHash = abs(hashGeom - hash50K)
	deltaDist = abs(dist - dist50K)
	deltaPts = abs(pts - pts50K)
	deltaPA = math.sqrt(math.pow((pAX50K - pAX), 2) + math.pow((pAY50K - pAY), 2))
	deltaPZ = math.sqrt(math.pow((pZX50K - pZX), 2) + math.pow((pZY50K - pZY), 2))

	if (deltaHash == 0): return 0
	if (deltaDist <= maxLevel1[0]) and (deltaPts <= maxLevel1[1]) and (deltaPA <= maxLevel1[2]) and (deltaPZ <= maxLevel1[2]): return 1
	if (deltaDist <= maxLevel2[0]) and (deltaPts <= maxLevel2[1]) and (deltaPA <= maxLevel2[2]) and (deltaPZ <= maxLevel2[2]): return 2
	if (deltaDist <= maxLevel3[0]) and (deltaPts <= maxLevel3[1]) and (deltaPA <= maxLevel3[2]) and (deltaPZ <= maxLevel3[2]): return 3
	return 4
	
	
# ========================================================================================
# Vérifier si les attributs des features Tronçons-GR et Tronçons-GR Ed4 sont identiques. Pour les atttributs dans la liste QGP.configSections50KFieldsCopyList
# >>> feature50K  : QgsFeature				Feature de la couche Réseau 50K
# >>> featureCW : QgsFeature				Feature de la couche Réseau GR
# <<< 			  : bool					True iff both features have same attributes
# ========================================================================================
	
def areFeatureAttributesIdentical(feature50K, featureCW):

	return (all(str(feature50K.attribute(a)).strip() == str(featureCW.attribute(a)).strip() for a in QGP.configSections50KFieldsCopyList))
	
	
# ========================================================================================
# --- THE END ---
# ========================================================================================
