# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Gestion des Menus : Page Maintenance
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
import os
import shutil

import QCarto_Layers_Tracks as LTRK

import QCarto_Tools_Buttons as TBUT
import QCarto_Tools_Coding as TCOD
import QCarto_Tools_Dates as TDAT
import QCarto_Tools_Files as TFIL
import QCarto_Tools_Layers as TLAY
import QCarto_Tools_Progress as TPRO

import QCarto_Definitions_Colors as DCOL
import QCarto_Definitions_Styles as DSTY

import QCarto_Process_BackupDB as SBAK
importlib.reload(SBAK)

import QCarto_Menu_EditTopo50 as P50K
importlib.reload(P50K)

import QCarto_QCarto_Migration as QMIG
importlib.reload(QMIG)

import QCarto_Parameters_Global
importlib.reload(QCarto_Parameters_Global)
QGP = QCarto_Parameters_Global.globalParameters()


# ========================================================================================
# Class : menuMaintenanceFrame
# >>> iface
# >>> mainMenu 						: Widget of Main Menu
# >>> mainFrame 					: Main Menu Object
# ========================================================================================

class menuMaintenanceFrame:

	def __init__(self, iface, mainMenu, mainFrame):

# 	Paramètres fournis

		self.iface = iface
		self.mainMenu = mainMenu
		self.mainFrame = mainFrame

#	Nom de la page

		self.pageName = 'Maintenance'

#	Accès aux Tables de la DB Carto

		self.layerTracksGR, 	self.layerTracksGRerror 	= self.mainFrame.layerTracksGR, 	self.mainFrame.layerTracksGRerror 	
		self.layerTracksRB, 	self.layerTracksRBerror 	= self.mainFrame.layerTracksRB, 	self.mainFrame.layerTracksRBerror 	
		self.layerSectionsGR, 	self.layerSectionsGRerror 	= self.mainFrame.layerSectionsGR, 	self.mainFrame.layerSectionsGRerror 	
		self.layerPointsGR, 	self.layerPointsGRError 	= self.mainFrame.layerPointsGR, 	self.mainFrame.layerPointsGRError 	
		self.layerCommunes, 	self.layerCommunesError		= self.mainFrame.layerCommunes, 	self.mainFrame.layerCommunesError		

#	Dictionnaires Principaux 
		
		self.dicoTracksGRFeatures = self.mainFrame.dicoTracksGRFeatures
		self.dicoTracksRBFeatures = self.mainFrame.dicoTracksRBFeatures
		self.dicoSectionsGRFeatures = self.mainFrame.dicoSectionsGRFeatures

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

		self.groupBoxBackupDB = self.menuBoxBackupDB()
		DSTY.setBoxGeometry(self.groupBoxBackupDB, 1, 4, 4, 3)
		self.boxesList.append(self.groupBoxBackupDB)

		self.groupBoxBackupDBReload = self.menuBoxBackupDBReload()
		DSTY.setBoxGeometry(self.groupBoxBackupDBReload, 5, 4, 4, 3)
		self.boxesList.append(self.groupBoxBackupDBReload)

		self.groupBoxBackupProject = self.menuBoxBackupProject()
		DSTY.setBoxGeometry(self.groupBoxBackupProject, 1, 8, 4, 3)
		self.boxesList.append(self.groupBoxBackupProject)

		self.groupBoxBackupProjectReload = self.menuBoxBackupProjectReload()
		DSTY.setBoxGeometry(self.groupBoxBackupProjectReload, 5, 8, 4, 3)
		self.boxesList.append(self.groupBoxBackupProjectReload)

#		self.groupBoxMigrateDB = self.menuBoxMigrateDB()										# No longer used - just for remember
#		DSTY.setBoxGeometry(self.groupBoxMigrateDB, 1, 12, 4, 3)
#		self.boxesList.append(self.groupBoxMigrateDB)

		self.groupBoxMigrateMap = self.menuBoxMigrateMap()
		DSTY.setBoxGeometry(self.groupBoxMigrateMap, 1, 12, 4, 2)
		self.boxesList.append(self.groupBoxMigrateMap)

		self.groupBoxEditTopo50 = self.menuBoxEditTopo50()
		DSTY.setBoxGeometry(self.groupBoxEditTopo50, 5, 12, 4, 1)
		self.boxesList.append(self.groupBoxEditTopo50)


# ========================================================================================
# Actions : A la demande de la fenêtre principale
# ========================================================================================

#	Show - Ouverture de cette fenêtre

	def show(self):
		for box in self.boxesList: box.show(), box.repaint()
		self.refreshBackupProjectCombo()
		self.initializeProjectReload()

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
# Actions : Backup DB
# ========================================================================================

	def backupDateRefresh(self):
	
		savingPath = QGP.configBackupPath
		if os.path.isdir(savingPath): 
			backupDirList = os.listdir(savingPath)
			if 'desktop.ini' in backupDirList : backupDirList.remove('desktop.ini')
			backupDirList.sort()
			path, file = os.path.split(backupDirList[-1])
			backupDate = TDAT.formatTimeStampForDisplay(file[0:19])
		else:
			savingPath = None
			backupDate = 'Répertoire pas trouvé'
	
		self.buttonBackupDate.setText(DSTY.textFormatBlackSmall.replace("%TEXT%",backupDate))
		if savingPath == None:
			DSTY.setStyleErrorLabel(self.buttonBackupDate)

	def buttonBackup_clicked(self):
		SBAK.process_BackupDB(self.mainFrame)
		self.backupDateRefresh()

	def buttonArchive_clicked(self):
		archiveName = TFIL.cleanFileName(self.buttonArchiveName.text())
		if (len(archiveName) <= 3):
			self.mainFrame.setStatusWarning('Le nom de l\'archive est invalide : ' + archiveName + ' !')
			return
		SBAK.process_BackupDB(self.mainFrame, archiveName)
		self.backupDateRefresh()


# ========================================================================================
# Actions : Backup Reload
# ========================================================================================

	def buttonBackupReload_clicked(self):
		self.backupReload(self.selectBackupCombo.currentText(), QGP.configBackupPath)

	def buttonArchiveReload_clicked(self):
		self.backupReload(self.selectArchiveCombo.currentText(), QGP.configArchivePath)

	def backupReload(self, backupDir, backupPath):

		TLAY.createGroup(backupDir, 0)

		for tableName in QGP.tablesBackupReloadList :
			print (QGP.configDBCartoStylesPath)
			layer, errorText = TLAY.loadLayer(backupPath + backupDir + '/', tableName, backupDir, backupDir[0:19] + ' - ' + tableName, QGP.configDBCartoStylesPath, tableName + '.qml', True)
			if layer == None:
				self.mainFrame.setStatusError('Erreur : ' + errorText)
				return

		self.mainFrame.setStatusDone('Groupe ' + backupDir + ' : ' + ' Les tables du backup sont rechargées')


# ========================================================================================
# Actions : Backup Project
# ========================================================================================

	def refreshBackupProjectCombo(self):
		self.selectBackupProjectCombo.addItem('')
		for fileName in os.listdir(QGP.configPathProject) :
			if not os.path.isdir(QGP.configPathProject + fileName) : continue
			self.selectBackupProjectCombo.addItem(fileName)

	def selectBackupProjectCombo_changed(self, textCombo):
		self.backupProjectFolder = textCombo + ' - ' + QgsApplication.userFullName() + ' (' + TDAT.getTimeStamp() + ')'
		self.buttonBackupProjectInfo.setText(DSTY.textFormatBlackNormalLeft.replace('%TEXT%',' ' + self.backupProjectFolder))
		DSTY.setStyleOkLabel(self.buttonBackupProjectInfo, 'Double3')			
	
	def buttonBackupProject_clicked(self):
		if self.selectBackupProjectCombo.currentText() == '':
			self.mainFrame.setStatusWarning('Choisissez un projet à copier au préalable !')
			return
		if not os.path.isdir(QGP.pathBackupCartoProjects):
			self.mainFrame.setStatusWarning('Le répertoire ' + QGP.pathBackupCartoProjects + ' n\'existe pas !')
			return
		self.mainFrame.setStatusWorking('Backup du projet : ' + self.selectBackupProjectCombo.currentText() + ' en cours ...')
		try:
			shutil.copytree(QGP.configPathProject + self.selectBackupProjectCombo.currentText(),  QGP.pathBackupCartoProjects + self.backupProjectFolder)
		except:
			self.mainFrame.setStatusError('Backup du projet : ' + self.selectBackupProjectCombo.currentText() + ' - shutil.copytree : une erreur s\'est produite ?')
			return		
		self.mainFrame.setStatusDone('Backup du projet : ' + self.selectBackupProjectCombo.currentText() + ' - OK')


# ========================================================================================
# Actions : Backup Project Reload
# ========================================================================================

	def initializeProjectReload(self):
		if not os.path.isdir(QGP.pathBackupCartoProjects):		
			self.mainFrame.setStatusWarning('Le répertoire ' + QGP.pathBackupCartoProjects + ' n\'existe pas !')
			return
		
		self.dicoProjectsBackup = {}
		self.setProjectsBackupItinerary = set()
		self.setProjectsBackupCartos = set()
		for fileName in  sorted(os.listdir(QGP.pathBackupCartoProjects), reverse=True):
			if not os.path.isdir(QGP.pathBackupCartoProjects + fileName) : continue
			itinerary = fileName.split(' - ')[0]
			cartoName = fileName.split(' - ')[-1].split(' (')[0]
			self.dicoProjectsBackup[fileName] = [itinerary, cartoName]
			self.setProjectsBackupItinerary.add(itinerary)
			self.setProjectsBackupCartos.add(cartoName)
			
		self.projectReloadItineraryCombo.clear()
		self.projectReloadItineraryCombo.addItem('Tous')
		for itinerary in list(self.setProjectsBackupItinerary): self.projectReloadItineraryCombo.addItem(itinerary)

		self.projectReloadCartoCombo.clear()
		self.projectReloadCartoCombo.addItem('Tous')
		for cartoName in list(self.setProjectsBackupCartos): self.projectReloadCartoCombo.addItem(cartoName)
		
		self.projectReloadCombo.clear()
		for fileName in self.dicoProjectsBackup: self.projectReloadCombo.addItem(fileName)
	

	def projectReloadFilterCombo_changed(self):
		self.projectReloadCombo.clear()
		for fileName in self.dicoProjectsBackup: 
			if self.projectReloadItineraryCombo.currentText() == 'Tous' or self.projectReloadItineraryCombo.currentText() == self.dicoProjectsBackup[fileName][0]:
				if self.projectReloadCartoCombo.currentText() == 'Tous' or self.projectReloadCartoCombo.currentText() == self.dicoProjectsBackup[fileName][1]:
					self.projectReloadCombo.addItem(fileName)

	
	def buttonReloadProject_clicked(self):
		fileName = self.projectReloadCombo.currentText()
		if fileName == '':
			self.mainFrame.setStatusWarning('Vous devez choisir un projet à recharger !')
			return
			
		self.mainFrame.setStatusWorking('Rechargement du projet : ' + fileName + ' ...')
		projectItinerary = self.dicoProjectsBackup[fileName][0]
		if os.path.exists(QGP.configPathProject + projectItinerary):
			try:
				os.rename(QGP.configPathProject + projectItinerary, QGP.configPathProject + projectItinerary + ' - Sauvegarde automatique (' + TDAT.getTimeStamp() + ')')
			except:
				self.mainFrame.setStatusError('Rename de votre projet existant impossible - la page carte est probablement ouverte sur ce projet !')
				return

		try:
			shutil.copytree(QGP.pathBackupCartoProjects + fileName, QGP.configPathProject + projectItinerary)
		except:
			self.mainFrame.setStatusError('Rechargement du projet impossible - la page carte est probablement ouverte sur ce projet !')
			return
		
			
		self.mainFrame.setStatusDone('Projet rechargé : ' + projectItinerary + ' - OK')


# ========================================================================================
# Actions : Edition de la couche Tronçons-GR-Ed4
# ========================================================================================

	def buttonEditTopo50Ed4_clicked(self):
		importlib.reload(P50K)
		self.mainFrame.dockMenuEditTopo50Ed4 = P50K.editTronconsIGN50V4(self.iface, self.mainMenu, self.mainFrame, self.mainFrame.dockMenuEditTopo50Ed4)
		self.mainFrame.dockMenuEditTopo50Ed4.show()
		self.mainMenu.hide()	
	

	def buttonTopo50Ed4Clean_clicked(self):
		if not self.mainFrame.expertModeQCarto :
			self.mainFrame.setStatusWarning('Cette commande est uniquement utilisable en mode expert Ø')
			return
		
		self.layer50K,	self.layer50Kerror = TLAY.openLayer(QGP.tableNameSectionsGREd4)
		if self.layer50K == None :
			self.mainFrame.setStatusWarning(self.layer50Kerror)
			return
		self.layer50K.startEditing()
			
		self.mainFrame.setStatusWorking('Suppression des entités trop distantes des entités correspondantes dans Tronçons-GR ...')	

		dico50KFeatures = { int(feature[QGP.tableSectionsFieldId]) : feature for feature in self.layer50K.getFeatures() }
		countFeaturesTotal = len(dico50KFeatures)
		countFeaturesLost = countFeaturesFar = 0
		progressBar = TPRO.createProgressBar(self.cleanButtonEd4, countFeaturesTotal, 'Normal')

		idSectionLostList = []
		idSectionFarList = []


		for idSection in dico50KFeatures :
			QgsApplication.processEvents()
			progressBar.setValue(progressBar.value() + 1)		
			feature50K = dico50KFeatures[idSection]
	
			if idSection not in self.mainFrame.dicoSectionsGRFeatures:
				countFeaturesLost += 1
				idSectionLostList.append(feature50K.id())
				self.layer50K.changeAttributeValue(feature50K.id(), feature50K.fieldNameIndex(QGP.tableSections50KFieldValidation), 'Inexistant')
				continue

			featureCW = self.mainFrame.dicoSectionsGRFeatures[idSection]		
			if featureCW.geometry().hausdorffDistance(feature50K.geometry()) > QGP.config50KDeltaMaxDelete : 
				countFeaturesFar += 1
				idSectionFarList.append(feature50K.id())
				self.layer50K.changeAttributeValue(feature50K.id(), feature50K.fieldNameIndex(QGP.tableSections50KFieldValidation), 'Distant')
				continue
			
		self.layer50K.selectByIds(idSectionLostList + idSectionFarList)
		self.mainFrame.setStatusDone('Tronçons-GR-Ed4 - Sélection des entités à supprimer : ' + str(countFeaturesLost) + ' Tronçons inexistants' + ' - ' + str(countFeaturesFar) + ' Tronçons distants ! TBC !!!')
		del progressBar


# ========================================================================================
# ========================================================================================
#
# Migration QCarto 6 > 7
# 
# ========================================================================================
# ========================================================================================

# ========================================================================================
# Migration Cartes
# ========================================================================================

	def migrateMaps(self):
	
		if not self.migrateMapsLockButton.isChecked():
			self.mainFrame.setStatusWarning('La Migration n\'est pas activée - Soyez très prudents avec cette opération !!!')	
			return

#	Créer le groupe Migration

		groupMigrationName = QGP.configMigrateGroupName
		TLAY.cleanLayerGroup(groupMigrationName)

		if TLAY.findGroup(groupMigrationName)[0] == None:
			TLAY.createGroup(groupMigrationName, 0)
		TLAY.findGroup(groupMigrationName)[0].setExpanded(True)

#	Charger le shape Cadres des anciennes cartes

		srcPath = QGP.configPathProject + self.migrateMapProjectSrcCombo.currentText() + '/Cadres Cartes/'
		if not os.path.isdir(srcPath):
			self.mainFrame.setStatusWarning('Le répertoire source Cadres Cartes n\'existe pas !')
			return
		if not os.path.isfile(srcPath + 'Cadres Cartes.shp'):
			self.mainFrame.setStatusWarning('Le shape source Cadres Cartes n\'existe pas !')
			return
			
		layerCadres, error = TLAY.loadLayer(srcPath, 'Cadres Cartes', groupMigrationName, 'Cadres Anciennes Cartes', None, None, False)
		if layerCadres == None:
			self.mainFrame.setStatusWarning(error)
			return

#	Charger le shape emprise des nouvelles cartes

		self.migrateMapProjectSrcInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%',str(len([f for f in layerCadres.getFeatures()])) + ' carte.s'))
		DSTY.setStyleOkLabel(self.migrateMapProjectSrcInfo)		

		dstPath = QGP.configPathProjectFramesGeneric.replace('%PROJECT%', self.migrateMapProjectDstCombo.currentText())
		if not os.path.isdir(dstPath):
			self.mainFrame.setStatusWarning('Le répertoire destination Emprises Cartes n\'existe pas !')
			return
		if not os.path.isfile(dstPath + QGP.configShapeFrameName + '.shp'):
			self.mainFrame.setStatusWarning('Le shape destination Emprises n\'existe pas !')
			return			

		layerEmprises, error = TLAY.loadLayer(dstPath, QGP.configShapeFrameName, groupMigrationName, 'Emprises Nouvelles Cartes', None, None, False)
		if layerEmprises == None:
			self.mainFrame.setStatusWarning(error)
			return
		
		self.migrateMapProjectDstInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%',str(len([f for f in layerEmprises.getFeatures()])) + ' carte.s'))
		DSTY.setStyleOkLabel(self.migrateMapProjectDstInfo)		

		existingMapNames = [feature[QGP.tableFramesFieldName] for feature in layerEmprises.getFeatures()]


#	Paramètres pour toutes cartes

		newItinerary = self.migrateMapProjectDstCombo.currentText()
		newType = TCOD.itineraryTypeFromTrackCode(newItinerary)

#	Copier les emprises cartes

		layerEmprises.startEditing()

		for oldMapFeature in layerCadres.getFeatures():
			self.mainFrame.setStatusWorking('Migration : ' + oldMapFeature['Nom Carte'] + ' ...')
		
			oldName = oldMapFeature['Nom Carte']
			try:
				newItineraryCode = newItinerary if newType in QGP.typeSetModeGR else oldName.split(' - ')[0][1:]
				newName = oldName if newType in QGP.typeSetModeGR else oldName.split(' - ')[1]
			except:
				newItineraryCode = newItinerary
				newName = oldName
			
			oldBackground = oldMapFeature['Fond Topo']
			if oldBackground == 'Fond Topo-50 Ed4':
				newBackground = 'IGN-50 Ed4'
			elif oldBackground == 'Fond Topo-50 Ed3':
				newBackground = 'IGN-50 Ed3'
			else:
				newBackground = 'Fond Blanc'
		
			oldFolder = oldMapFeature['GR Fold']
		
			newFolder = QGP.configPathMapShapes.replace('%PROJECT%', newItinerary ) + '/' + newItineraryCode + ' - ' + newName + '/'
		
			if newName not in existingMapNames:
				newMapFeature = QgsFeature()
				newMapFeature.setFields(layerEmprises.fields())
				newMapFeature.setAttribute(QGP.tableFramesFieldItineraryCode, newItineraryCode)
				newMapFeature.setAttribute(QGP.tableFramesFieldName, newName)
				newMapFeature.setAttribute(QGP.tableFramesFieldFormat, oldMapFeature['Format'])
				newMapFeature.setAttribute(QGP.tableFramesFieldEchelle, oldMapFeature['Echelle'])
				newMapFeature.setAttribute(QGP.tableFramesFieldFolder, newFolder)
				newMapFeature.setAttribute(QGP.tableFramesFieldNumber, oldMapFeature['Pos Num'])
				newMapFeature.setAttribute(QGP.tableFramesFieldCopyright, oldMapFeature['Pos Copy'])
				newMapFeature.setAttribute(QGP.tableFramesFieldBackground, newBackground)
				newMapFeature.setAttribute(QGP.tableFramesFieldModifications, '[[],[]]')			
				newMapFeature.setGeometry(oldMapFeature.geometry())
				
				layerEmprises.addFeature(newMapFeature)
	
				self.migrateMapProjectDstInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%',str(len([f for f in layerEmprises.getFeatures()])) + ' carte.s'))
				DSTY.setStyleOkLabel(self.migrateMapProjectDstInfo)		
	
				self.mainFrame.setStatusWorking('Migration : ' + oldMapFeature['Nom Carte'] + ' - Emprise OK')
				TDAT.sleep(250)
			
#	Copier les Tronçons (vides)

			srcPath = QGP.configPathActiveMap
			dstPath = newFolder
			TFIL.ensure_dir(dstPath)
			status, count = TFIL.copy_files(srcPath, dstPath, QGP.configShapeMapSections)
			if status:
				self.mainFrame.setStatusWorking('Fichiers : ' + dstPath + QGP.configShapeMapSections + ' : ' + str(count) + ' fichiers créés !')
				TDAT.sleep(250)
			else:			
				self.mainFrame.setStatusError('Impossible de copier le shape des Tronçons !', False)
				TDAT.sleep(1000)			

#	Copier les Etiquettes 

			srcPath = QGP.configPathProject + self.migrateMapProjectSrcCombo.currentText() + '/Cartes Shapes/' + oldFolder + '/'
			dstPath = newFolder
			TFIL.ensure_dir(dstPath)
				
			status, count = TFIL.copy_files(srcPath, dstPath, 'Noms Tracés', QGP.configShapeMapLabels)
			if status:
				self.mainFrame.setStatusWorking('Fichiers : ' + dstPath + QGP.configShapeMapLabels + ' : ' + str(count) + ' fichiers créés !')
				TDAT.sleep(250)
			else:			
				self.mainFrame.setStatusError('Impossible de copier le shape des étiquettes !', False)
				TDAT.sleep(1000)

			status, count = TFIL.copy_files(QGP.configPathActiveMap, dstPath, QGP.configShapeMapLabels + '.qml')
			
#	Copier les Repères 

			srcPath = QGP.configPathProject + self.migrateMapProjectSrcCombo.currentText() + '/Cartes Shapes/' + oldFolder + '/'
			dstPath = newFolder
			TFIL.ensure_dir(dstPath)
				
			status, count = TFIL.copy_files(srcPath, dstPath, 'Points Repères GR', QGP.configShapeMapReperes)
			if status:
				self.mainFrame.setStatusWorking('Fichiers : ' + dstPath + QGP.configShapeMapReperes + ' : ' + str(count) + ' fichiers créés !')
				TDAT.sleep(250)
			else:			
				self.mainFrame.setStatusError('Impossible de copier le shape des repères !', False)
				TDAT.sleep(1000)

			status, count = TFIL.copy_files(QGP.configPathActiveMap, dstPath, QGP.configShapeMapReperes + '.qml')

		layerEmprises.commitChanges()	

#	Copie les Shapes des TEC et Gares

		srcPath = QGP.configPathProject + self.migrateMapProjectSrcCombo.currentText() + '/Cartes Shapes/Toutes Cartes/'
		dstPath = QGP.configPathProjectShapesGeneric.replace('%PROJECT%', newItinerary )

		status, count = TFIL.copy_files(srcPath, dstPath, QGP.configShapeProjectNameTEC)
		if status:
			self.mainFrame.setStatusWorking('Fichiers : ' + dstPath + QGP.configShapeProjectNameTEC + ' : ' + str(count) + ' fichiers créés !')
			TDAT.sleep(250)
		else:			
			self.mainFrame.setStatusError('Impossible de copier le shape des TEC !', False)
			TDAT.sleep(1000)

		status, count = TFIL.copy_files(QGP.configPathActiveProject, dstPath, QGP.configShapeProjectNameTEC + '.qml')

		status, count = TFIL.copy_files(srcPath, dstPath, QGP.configShapeProjectNameSNCB)
		if status:
			self.mainFrame.setStatusWorking('Fichiers : ' + dstPath + QGP.configShapeProjectNameSNCB + ' : ' + str(count) + ' fichiers créés !')
			TDAT.sleep(250)
		else:			
			self.mainFrame.setStatusError('Impossible de copier le shape des Gares SNCB !', False)
			TDAT.sleep(1000)

		status, count = TFIL.copy_files(QGP.configPathActiveProject, dstPath, QGP.configShapeProjectNameSNCB + '.qml')

		self.mainFrame.setStatusDone('Migration terminée - Avec un peu de chance ;-) OK')


# ========================================================================================
# ========================================================================================
#
# Création des différents cadres Menu
# 
# ========================================================================================
# ========================================================================================


# ========================================================================================
# Cadre : Backup
# ========================================================================================

	def menuBoxBackupDB(self):

		groupBoxBackupDB = QtWidgets.QGroupBox('Backup DB Carto', self.mainMenu)
		groupBoxBackupDB.setStyleSheet(DSTY.styleBox)

#	Label et Info pour : Dernier Backup
		
		TBUT.createLabelBlackButton(groupBoxBackupDB, 1, 1, 'Dernier Backup', 'Normal')

		self.buttonBackupDate = TBUT.createLabelGreenButton(groupBoxBackupDB, 2, 1, '...', 'Normal', 'Small')
		self.backupDateRefresh()
		
# 	Label et Info pour : Répertoire
		
		TBUT.createLabelBlackButton(groupBoxBackupDB, 1, 2, 'Répertoire', 'Normal')

		buttonBackupFolder = TBUT.createLabelGreenButton(groupBoxBackupDB, 2, 2, QGP.configBackupPath, 'Double', 'VerySmall')
		if not os.path.isdir(QGP.configBackupPath): 	DSTY.setStyleErrorLabelVerySmall(buttonBackupFolder, "Double")
				
# 	Bouton : Backup

		buttonBackup = TBUT.createActionButton(groupBoxBackupDB, 4, 2, 'Backup', 'Normal')
		buttonBackup.clicked.connect(self.buttonBackup_clicked)
	
#	Label et Saisie pour Nom Archive

		TBUT.createLabelBlackButton(groupBoxBackupDB, 1, 3, 'Nom Archive', 'Normal')
		self.buttonArchiveName = TBUT.createInputButton(groupBoxBackupDB, 2, 3, 'Double')

# 	Bouton : Archive

		buttonArchive = TBUT.createActionButton(groupBoxBackupDB, 4, 3, 'Archiver', 'Normal')
		buttonArchive.clicked.connect(self.buttonArchive_clicked)	
		
#	Bouton Aide

		buttonHelpBackup = TBUT.createHelpButton(groupBoxBackupDB, 4, 1, 'Aide Backup', 'Normal')
		buttonHelpBackup.clicked.connect(self.buttonHelpBackup_clicked)


# 	Terminé

		groupBoxBackupDB.repaint()

		return groupBoxBackupDB			
		
	
	def buttonHelpBackup_clicked(self):
		webbrowser.open_new_tab(QGP.configMenuHelpBasePath + 'QCarto - Maintenance - Backup.html')


# ========================================================================================
# Cadre : Recharger Backup / Archive
# ========================================================================================

	def menuBoxBackupDBReload(self):

		groupBoxBackupDBReload = QtWidgets.QGroupBox('Recharger Backup / Archive', self.mainMenu)
		groupBoxBackupDBReload.setStyleSheet(DSTY.styleBox)

# 	Label Bouton et Combo pour : Choix Backup 

		TBUT.createLabelBlackButton(groupBoxBackupDBReload, 1, 2, 'Choix du Backup', 'Normal')
	
		self.selectBackupCombo = TBUT.createComboButton(groupBoxBackupDBReload, 2, 2, 'Double')

		savingPath = QGP.configBackupPath
		if os.path.isdir(savingPath): 
			backupDirList = os.listdir(savingPath)
			if 'desktop.ini' in backupDirList : backupDirList.remove('desktop.ini')
			backupDirList.sort()
			backupDirList.reverse()
			for dirBackup in backupDirList: self.selectBackupCombo.addItem(dirBackup)

# 	Label Bouton et Combo pour : Choix Archive

		TBUT.createLabelBlackButton(groupBoxBackupDBReload, 1, 3, 'Choix de l\'archive', 'Normal')

		self.selectArchiveCombo = TBUT.createComboButton(groupBoxBackupDBReload, 2, 3, 'Double')

		savingPath = QGP.configArchivePath
		if os.path.isdir(savingPath): 
			backupDirList = os.listdir(savingPath)
			if 'desktop.ini' in backupDirList : backupDirList.remove('desktop.ini')
			backupDirList.sort()
			backupDirList.reverse()
			for dirBackup in backupDirList: self.selectArchiveCombo.addItem(dirBackup)

# 	Bouton : Backup / Archive Rechargement

		buttonBackupReload = TBUT.createActionButton(groupBoxBackupDBReload, 4, 2, 'Recharger', 'Normal')
		buttonBackupReload.clicked.connect(self.buttonBackupReload_clicked)

		buttonArchiveReload = TBUT.createActionButton(groupBoxBackupDBReload, 4, 3, 'Recharger', 'Normal')
		buttonArchiveReload.clicked.connect(self.buttonArchiveReload_clicked)

# 	Boutons aide

		buttonHelpBackupReload = TBUT.createHelpButton(groupBoxBackupDBReload, 4, 1, 'Aide Recharger', 'Normal')
		buttonHelpBackupReload.clicked.connect(self.buttonHelpBackupReload_clicked)
		
# 	Terminé

		groupBoxBackupDBReload.repaint()

		return groupBoxBackupDBReload			


	def buttonHelpBackupReload_clicked(self):
		webbrowser.open_new_tab(QGP.configMenuHelpBasePath + 'QCarto - Maintenance - Backup Rechargement.html')	
	
	
# ========================================================================================
# Cadre : Backup Projet
# ========================================================================================

	def menuBoxBackupProject(self):

		groupBoxBackupProjet = QtWidgets.QGroupBox('Backup Projet QCarto', self.mainMenu)
		groupBoxBackupProjet.setStyleSheet(DSTY.styleBox)

#	Label et Combo pour : Choix Projet
		
		TBUT.createLabelBlackButton(groupBoxBackupProjet, 1, 1, 'Choix du Projet', 'Normal')
		self.selectBackupProjectCombo = TBUT.createComboButton(groupBoxBackupProjet, 2, 1, 'Double')
		self.selectBackupProjectCombo.currentTextChanged.connect(self.selectBackupProjectCombo_changed)

#	Labet et Info du Nom du Backup

		TBUT.createLabelBlackButton(groupBoxBackupProjet, 1, 2, 'Répertoire à créer', 'Normal')
		self.buttonBackupProjectInfo = TBUT.createLabelGreenButton(groupBoxBackupProjet, 2, 2, '...', 'Double3', 'Small')
		
# 	Bouton : Backup

		buttonBackupProject = TBUT.createActionButton(groupBoxBackupProjet, 4, 3, 'Backup', 'Normal')
		buttonBackupProject.clicked.connect(self.buttonBackupProject_clicked)		
		
#	Bouton Help

		buttonHelpFiche = TBUT.createHelpButton(groupBoxBackupProjet, 4, 1, 'Fiche', 'Normal')
		buttonHelpFiche.clicked.connect(lambda x : webbrowser.open_new_tab(QGP.configMenuHelpBasePath + 'QCarto - Fiche - Partage Projets.html'))	

# 	Terminé

		groupBoxBackupProjet.repaint()

		return groupBoxBackupProjet			
			
	
# ========================================================================================
# Cadre : Backup Projet Reload
# ========================================================================================

	def menuBoxBackupProjectReload(self):

		groupBoxBackupProjetReload = QtWidgets.QGroupBox('Recharger Projet QCarto', self.mainMenu)
		groupBoxBackupProjetReload.setStyleSheet(DSTY.styleBox)

#	Label et Combos pour : Filtres
		
		TBUT.createLabelBlackButton(groupBoxBackupProjetReload, 1, 1, 'Itinéraire / Carto', 'Normal')
		self.projectReloadItineraryCombo = TBUT.createComboButton(groupBoxBackupProjetReload, 2, 1, 'Normal')
		self.projectReloadItineraryCombo.currentTextChanged.connect(self.projectReloadFilterCombo_changed)

		self.projectReloadCartoCombo = TBUT.createComboButton(groupBoxBackupProjetReload, 3, 1, 'Normal')
		self.projectReloadCartoCombo.currentTextChanged.connect(self.projectReloadFilterCombo_changed)

#	Label et Info du Nom du Backup

		TBUT.createLabelBlackButton(groupBoxBackupProjetReload, 1, 2, 'Projet à recharger', 'Normal')
		self.projectReloadCombo = TBUT.createComboButton(groupBoxBackupProjetReload, 2, 2, 'Double')
		
# 	Bouton : Recharger 

		buttonReloadProject = TBUT.createActionButton(groupBoxBackupProjetReload, 4, 3, 'Recharger', 'Normal')
		buttonReloadProject.clicked.connect(self.buttonReloadProject_clicked)		
		
#	Bouton Help

		buttonHelpFiche = TBUT.createHelpButton(groupBoxBackupProjetReload, 4, 1, 'Fiche', 'Normal')
		buttonHelpFiche.clicked.connect(lambda x : webbrowser.open_new_tab(QGP.configMenuHelpBasePath + 'QCarto - Fiche - Partage Projets.html'))	

# 	Terminé

		groupBoxBackupProjetReload.repaint()

		return groupBoxBackupProjetReload			
			

# ========================================================================================
# Cadre : Migration DB Carto V6 V7
# ========================================================================================

	def menuBoxMigrateDB(self):

		groupBoxMigrateDB = QtWidgets.QGroupBox('Migration DB Carto : QCarto 6 > 7', self.mainMenu)
		groupBoxMigrateDB.setStyleSheet(DSTY.styleBox)

		self.buttonMigrateTracksGR = TBUT.createActionButton(groupBoxMigrateDB, 1, 2, 'Tracés-GR', 'Normal')
		DSTY.setStyleWarningButton(self.buttonMigrateTracksGR)
		self.buttonMigrateTracksGR.clicked.connect(lambda x : QMIG.migrateTracesGR(self.mainFrame, self.buttonMigrateTracksGR, self.migrateSelectedOnlyButton.isChecked(), self.migrateDBLockButton.isChecked()))
		
		self.buttonMigrateTracksRB = TBUT.createActionButton(groupBoxMigrateDB, 1, 3, 'Tracés-RB', 'Normal')
		DSTY.setStyleWarningButton(self.buttonMigrateTracksRB)
		self.buttonMigrateTracksRB.clicked.connect(lambda x : QMIG.migrateTracesRB(self.mainFrame, self.buttonMigrateTracksRB, self.migrateSelectedOnlyButton.isChecked(), self.migrateDBLockButton.isChecked()))

		self.buttonMigratePointsGR = TBUT.createActionButton(groupBoxMigrateDB, 2, 3, 'Points-GR', 'Normal')
		DSTY.setStyleWarningButton(self.buttonMigratePointsGR)
		self.buttonMigratePointsGR.clicked.connect(lambda x : QMIG.migrateReperesGR(self.mainFrame, self.buttonMigratePointsGR, self.migrateSelectedOnlyButton.isChecked(), self.migrateDBLockButton.isChecked()))

		self.buttonMigrateReseauGR = TBUT.createActionButton(groupBoxMigrateDB, 3, 3, 'Réseau-GR', 'Normal')
		DSTY.setStyleWarningButton(self.buttonMigrateReseauGR)
		self.buttonMigrateReseauGR.clicked.connect(lambda x : QMIG.migrateReseauGR(self.mainFrame, self.buttonMigrateReseauGR, self.migrateSelectedOnlyButton.isChecked(), self.migrateDBLockButton.isChecked()))

		self.buttonMigrateReseauGREd4 = TBUT.createActionButton(groupBoxMigrateDB, 3, 2, 'Réseau-GR-Ed4', 'Normal')
		DSTY.setStyleWarningButton(self.buttonMigrateReseauGREd4)
		self.buttonMigrateReseauGREd4.clicked.connect(lambda x : QMIG.migrateReseauGREd4(self.mainFrame, self.buttonMigrateReseauGREd4, self.migrateSelectedOnlyButton.isChecked(), self.migrateDBLockButton.isChecked()))

		self.buttonMigrateLabelsTronconsGR = TBUT.createActionButton(groupBoxMigrateDB, 4, 3, 'Etiquettes-GR', 'Normal')
		DSTY.setStyleWarningButton(self.buttonMigrateLabelsTronconsGR)
		self.buttonMigrateLabelsTronconsGR.clicked.connect(lambda x : QMIG.migrateLabelsTronconsGR(self.mainFrame, self.buttonMigrateLabelsTronconsGR, self.migrateSelectedOnlyButton.isChecked(), self.migrateDBLockButton.isChecked()))

		self.migrateSelectedOnlyButton = TBUT.createCheckBoxButton(groupBoxMigrateDB, 3, 1, 'Sélection', 'Normal')
		self.migrateSelectedOnlyButton.setCheckState(Qt.Checked)	

		self.migrateDBLockButton = TBUT.createCheckBoxButton(groupBoxMigrateDB, 4, 1, 'Activer', 'Normal')
		self.migrateDBLockButton.setCheckState(Qt.Unchecked)	


# 	Terminé

		groupBoxMigrateDB.repaint()

		return groupBoxMigrateDB			
	
	
# ========================================================================================
# Cadre : Migration Cartes V6 V7
# ========================================================================================

	def menuBoxMigrateMap(self):

		groupBoxMigrateMap = QtWidgets.QGroupBox('Migration Carte : QCarto 6 > 7', self.mainMenu)
		groupBoxMigrateMap.setStyleSheet(DSTY.styleBox)

#	Sélection du Projet Source

		TBUT.createLabelBlackButton(groupBoxMigrateMap, 1, 1, 'Projet Source', 'Normal', 'Normal')
		self.migrateMapProjectSrcCombo = TBUT.createComboButton(groupBoxMigrateMap, 2, 1, 'Normal')
		for folder in os.listdir(QGP.configPathProject) :
			if os.path.isdir(QGP.configPathProject + folder): self.migrateMapProjectSrcCombo.addItem(folder)
		self.migrateMapProjectSrcInfo = TBUT.createLabelGreenButton(groupBoxMigrateMap, 3, 1, '. . .', 'Normal', 'Normal')

#	Sélection du Projet Destination

		TBUT.createLabelBlackButton(groupBoxMigrateMap, 1, 2, 'Projet Destination', 'Normal', 'Normal')
		self.migrateMapProjectDstCombo = TBUT.createComboButton(groupBoxMigrateMap, 2, 2, 'Normal')
		for folder in os.listdir(QGP.configPathProject) :
			if os.path.isdir(QGP.configPathProject + folder): self.migrateMapProjectDstCombo.addItem(folder)
		self.migrateMapProjectDstInfo = TBUT.createLabelGreenButton(groupBoxMigrateMap, 3, 2, '. . .', 'Normal', 'Normal')

#	Bouton Migration

		self.migrateMapsLockButton = TBUT.createCheckBoxButton(groupBoxMigrateMap, 4, 1, 'Activer', 'Normal')
		self.migrateMapsLockButton.setCheckState(Qt.Unchecked)	


		self.buttonMigrateMaps = TBUT.createActionButton(groupBoxMigrateMap, 4, 2, 'Migration', 'Normal')
		DSTY.setStyleWarningButton(self.buttonMigrateMaps)
		self.buttonMigrateMaps.clicked.connect(self.migrateMaps)

# 	Terminé

		groupBoxMigrateMap.repaint()

		return groupBoxMigrateMap			
	
	
# ========================================================================================
# Cadre : Edition Tronçons-GR Topo50
# ========================================================================================
	
	def menuBoxEditTopo50(self):

		groupBoxEditTopo50 = QtWidgets.QGroupBox('Edition de la couche : Tronçons-GR-Ed4', self.mainMenu)
		groupBoxEditTopo50.setStyleSheet(DSTY.styleBox)

#	Bouton 

		editButtonEd4 = TBUT.createActionButton(groupBoxEditTopo50, 1, 1, 'Tronçons-Ed4', 'Normal')
		editButtonEd4.clicked.connect(self.buttonEditTopo50Ed4_clicked)

		self.cleanButtonEd4 = TBUT.createActionButton(groupBoxEditTopo50, 4, 1, 'Ø Nettoyage Ø', 'Normal')
		self.cleanButtonEd4.clicked.connect(self.buttonTopo50Ed4Clean_clicked)
		DSTY.setStyleWarningButton(self.cleanButtonEd4)

# 	Terminé

		groupBoxEditTopo50.repaint()

		return groupBoxEditTopo50			
	
	
# ========================================================================================
# --- THE END ---
# ========================================================================================
	