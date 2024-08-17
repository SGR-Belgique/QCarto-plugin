# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Utilitaire pour la Gestion des Boutons d'action Utilisateur
# ========================================================================================

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qgis.core import *
from qgis.gui import *
from qgis.PyQt import QtWidgets

import QCarto_Tools_Canevas as TCAN

import QCarto_Parameters_Global
QGP = QCarto_Parameters_Global.globalParameters()


# ========================================================================================
# Créer la Barre QCarto
# ========================================================================================

def createQCartoBar(iface):

# 	Retrieve Pluggin Bar

	pluginBarS = [ _ for _ in iface.mainWindow().findChildren(QtWidgets.QToolBar) if _.objectName() == QGP.configPluginBarName]
	pluginBar = pluginBarS[0] if pluginBarS != [] else None

#	Create QCarto Tool Bar

	qCartoBar = iface.addToolBar(QGP.configQCartoBarName)
	qCartoBar.setObjectName(QGP.configQCartoBarName)
	if pluginBar != None:
		iface.mainWindow().insertToolBar(pluginBar, qCartoBar)
		iface.mainWindow().insertToolBar(qCartoBar, pluginBar)
	qCartoBar.deleteLater()	

	return qCartoBar


# ========================================================================================
# Class : QActionButtons
#  - Ajoute des boutons suivant les utilisateurs
# ========================================================================================

class QActionButtons:

	def __init__(self, iface, mainFrame, qCartoBar, buttonList):
	
		self.iface = iface	
		self.buttonList = buttonList
		self.mainFrame = mainFrame
		
		if 'QW' in buttonList:
			self.actionQW = QtWidgets.QAction(QIcon(QGP.configActionIcon_QW), 'Activer QCarto', self.iface.mainWindow())	
			self.actionQW.setObjectName(QGP.configActionName_QW)
			qCartoBar.addAction(self.actionQW)
			self.actionQW.triggered.connect(mainFrame.actionButtonQWToggled)

		if '25K' in buttonList:
			self.action25K = QtWidgets.QAction(QIcon(QGP.configActionIcon_25K), 'Echelle 1:25.000', self.iface.mainWindow())	
			self.action25K.setObjectName(QGP.configActionName_25K)
			qCartoBar.addAction(self.action25K)
			self.action25K.triggered.connect(self.runAction25K)

		if '50K' in buttonList:
			self.action50K = QtWidgets.QAction(QIcon(QGP.configActionIcon_50K), 'Echelle 1:50.000', self.iface.mainWindow())	
			self.action50K.setObjectName(QGP.configActionName_50K)
			qCartoBar.addAction(self.action50K)
			self.action50K.triggered.connect(self.runAction50K)
	
		if '100K' in buttonList:
			self.action100K = QtWidgets.QAction(QIcon(QGP.configActionIcon_100K), 'Echelle 1:100.000', self.iface.mainWindow())	
			self.action100K.setObjectName(QGP.configActionName_100K)
			qCartoBar.addAction(self.action100K)
			self.action100K.triggered.connect(self.runAction100K)
	
		if 'Map' in buttonList:
			self.actionMap = QtWidgets.QAction(QIcon(QGP.configActionIcon_Map), 'Vue Carte', self.iface.mainWindow())	
			self.actionMap.setObjectName(QGP.configActionName_Map)
			qCartoBar.addAction(self.actionMap)
			self.actionMap.triggered.connect(self.runActionMap)
		
		if 'MapV' in buttonList:
			self.actionMapV = QtWidgets.QAction(QIcon(QGP.configActionIcon_MapV), 'Vue Carte Vierge', self.iface.mainWindow())	
			self.actionMapV.setObjectName(QGP.configActionName_MapV)
			qCartoBar.addAction(self.actionMapV)
			self.actionMapV.triggered.connect(self.runActionMapV)
		
		if 'GrT' in buttonList:
			self.actionGrT = QtWidgets.QAction(QIcon(QGP.configActionIcon_GrT), 'Vue GR on/off', self.iface.mainWindow())	
			self.actionGrT.setObjectName(QGP.configActionName_GrT)
			qCartoBar.addAction(self.actionGrT)
			self.actionGrT.triggered.connect(self.runActionGrToggle)

		if 'EtiA' in buttonList:
			self.actionEtiA = QtWidgets.QAction(QIcon(QGP.configActionIcon_EtiA), 'Aligner Etiquettes', self.iface.mainWindow())	
			self.actionEtiA.setObjectName(QGP.configActionName_EtiA)
			qCartoBar.addAction(self.actionEtiA)
			self.actionEtiA.triggered.connect(self.runActionEtiA)
	
		if 'GrI' in buttonList:
			self.actionGrI = QtWidgets.QAction(QIcon(QGP.configActionIcon_GrI), 'Identification GR', self.iface.mainWindow())	
			self.actionGrI.setObjectName(QGP.configActionName_GrI)
			qCartoBar.addAction(self.actionGrI)
			self.actionGrI.triggered.connect(mainFrame.actionButtonIdentificationToggled)
			
		if 'GrE' in buttonList:
			self.actionGrE = QtWidgets.QAction(QIcon(QGP.configActionIcon_GrE), 'Edition x_list', self.iface.mainWindow())	
			self.actionGrE.setObjectName(QGP.configActionName_GrE)
			qCartoBar.addAction(self.actionGrE)
			self.actionGrE.triggered.connect(mainFrame.actionButtonEditToggled)
			
		if 'GrI-B' in buttonList:																									# Idem for QBalisage
			self.actionGrI = QtWidgets.QAction(QIcon('X:/QBalisage/Qgis_Icons/Action-GRInfos.png'), 'Identification GR', self.iface.mainWindow())	
			self.actionGrI.setObjectName(QGP.configActionName_GrI)
			qCartoBar.addAction(self.actionGrI)
			self.actionGrI.triggered.connect(mainFrame.actionButtonIdentificationToggled)			
			

	def removeButtons(self):
		if '25K' in self.buttonList: 	self.iface.removeToolBarIcon(self.action25K)
		if '50K' in self.buttonList:	self.iface.removeToolBarIcon(self.action50K)
		if '100K' in self.buttonList:	self.iface.removeToolBarIcon(self.action100K)
		if 'Map' in self.buttonList:	self.iface.removeToolBarIcon(self.actionMap)
		if 'MapV' in self.buttonList:	self.iface.removeToolBarIcon(self.actionMapV)
		if 'GrT' in self.buttonList:	self.iface.removeToolBarIcon(self.actionGrT)
		if 'GrI' in self.buttonList:	self.iface.removeToolBarIcon(self.actionGrI)
		if 'GrE' in self.buttonList:	self.iface.removeToolBarIcon(self.actionGrE)

	def runAction25K(self):
		self.iface.mapCanvas().zoomScale(25000)

	def runAction50K(self):
		self.iface.mapCanvas().zoomScale(50000)

	def runAction100K(self):
		self.iface.mapCanvas().zoomScale(100000)

	def runActionMap(self):
		try:
			TCAN.groupShowOnCanevas(QGP.configFrameGroupName, True)								# Montrer groupe Descriptifs
			TCAN.groupShowOnCanevas(QGP.configActiveProjectGroupName, True)						# Montrer groupe Projet Actif
			TCAN.groupShowOnCanevas(QGP.configOtherProjectGroupName, True)						# Montrer groupe Projet Autres
			TCAN.groupShowOnCanevas(QGP.configActiveMapGroupName, True)							# Montrer groupe Carte Active
			TCAN.groupShowOnCanevas(QGP.configIGN50Ed4GroupName, True)							# Montrer groupe Cartes IGN-50 Edition 4
			TCAN.groupShowOnCanevas(QGP.configDBCartoGroupName, False)							# Cacher groupe des Tables DB Carto
			TCAN.groupShowOnCanevas(QGP.configIGNCWGroupName, False)							# Cacher groupe CartoWeb
		except:
			pass

	def runActionMapV(self):
		try:
			TCAN.groupShowOnCanevas(QGP.configFrameGroupName, True)								# Montrer groupe Descriptifs
			TCAN.groupShowOnCanevas(QGP.configActiveProjectGroupName, True)						# Montrer groupe Projet Actif
			TCAN.groupShowOnCanevas(QGP.configOtherProjectGroupName, True)						# Montrer groupe Projet Autres
			TCAN.groupShowOnCanevas(QGP.configActiveMapGroupName, True)							# Montrer groupe Carte Active
			TCAN.groupShowOnCanevas(QGP.configIGN50Ed4GroupName, False)							# Cacher groupe Cartes IGN-50 Edition 4
			TCAN.groupShowOnCanevas(QGP.configDBCartoGroupName, False)							# Cacher groupe des Tables DB Carto
			TCAN.groupShowOnCanevas(QGP.configIGNCWGroupName, False)							# Cacher groupe CartoWeb
		except:
			pass

	def runActionGrToggle(self):
		try:
			TCAN.groupShowToggleOnCanevas(QGP.configDBCartoGroupName)
		except:
			pass

	def runActionEtiA(self):
		try:
			if self.mainFrame.debugModeQCartoLevel == 3 : print ('Alignement des Etiquettes')
			if self.mainFrame.layerActiveMapLabelsSimple == None : return
			selectedLabels = [labelFeature for labelFeature in self.mainFrame.layerActiveMapLabelsSimple.getSelectedFeatures()]
			if len(selectedLabels) < 2: return
			if len(selectedLabels) > 5: return
			for labelFeature in selectedLabels:
				if self.mainFrame.debugModeQCartoLevel == 3 : print('Etiquette position Y = ' + str(labelFeature.geometry().asPoint().y()))
			labelMeanYPos = sum(labelFeature.geometry().asPoint().y() for labelFeature in selectedLabels) / len(selectedLabels)
			if self.mainFrame.debugModeQCartoLevel == 3 : print('Etiquette position moyenne Y = ' + str(labelMeanYPos))
			alreadyEditable = self.mainFrame.layerActiveMapLabelsSimple.isEditable()
			self.mainFrame.layerActiveMapLabelsSimple.startEditing()
			for labelFeature in selectedLabels:
				self.mainFrame.layerActiveMapLabelsSimple.changeGeometry(labelFeature.id(), QgsGeometry.fromPointXY(QgsPointXY(labelFeature.geometry().asPoint().x(), labelMeanYPos)))
			if not alreadyEditable:
				self.mainFrame.layerActiveMapLabelsSimple.commitChanges()

		except:
			pass



# ========================================================================================
# --- THE END ---
# ========================================================================================
