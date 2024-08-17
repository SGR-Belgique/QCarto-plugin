# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ========================================================================================

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qgis.core import *
from qgis.gui import *

import sys
import time
import math
import importlib
	
import QCarto_Tools_Coding as TCOD
import QCarto_Tools_Dates as TDAT
import QCarto_Tools_Layers as TLAY
import QCarto_Tools_Files as TFIL
import QCarto_Tools_Progress as TPRO

import QCarto_Definitions_TopoGuides as DTOP	
import QCarto_Definitions_Styles as DSTY

	
import QCarto_Parameters_Global
QGP = QCarto_Parameters_Global.globalParameters()	


# ========================================================================================
# Process : Export Carte
# ========================================================================================

# ========================================================================================
# Export Carte
#  >>> iface
#  >>> mainFrame 			: class mainMenuFrame			Main Object
#  >>> activeMapFrame 		: class menuActiveMapFrame		ActiveMap Object
#  >>> mapMode				: str							PDF // Topo // Schéma
#  >>> mapBackground		: str							Voir : QGP.configDicoExportBackground
#  >>> mapFilePrefix		: str							Prefix for the Map file name
#  >>> requestedScale		: int 							Pour 'Couches Osm' : échelle pour export
#  >>> requestedMargin		: int							Marges en mm
#  >>> requestedOpacity 	: int							Opacité pour export [0..100]
#  >>> requestedLuminosity 	: int 							Luminosité pour export - Valeur [-255..255]
#  >>> requestedContrast 	: int 							Contraste pour export - Valeur [-100..100]
#  >>> addReseauGr			: bool							Flag pour ajout automatique du réseau GR
#  >>> addGlobalMap			: bool							Flag pour ajout automatique de la carte globale
#  >>> layersList 			: [QgsVectorLayers]				Liste des couches Qgis à exporter. Cas des 'Couches Osm' et 'Fond Osm'
#  <<< status				: bool							True iff OK
# ========================================================================================

def process_Export(iface, mainFrame, activeMapFrame, mapMode, mapBackground, mapFilePrefix, requestedScale, requestedMargin, requestedOpacity, requestedLuminosity, requestedContrast, addReseauGR, addGlobalMap, layersList = None):

	global imagePath
	global imageSaved
	global render
	global exportDpi
	
# 	Welcome !

	startTime = time.time()
	mainFrame.setStatusWorking('Export de la carte : démarrage du processus ...')
	if mainFrame.debugModeQCartoLevel > 0: print ('--- ')
	if mainFrame.debugModeQCartoLevel > 0: print ('--- Export')
	if mainFrame.debugModeQCartoLevel > 0: print ('--- Export - Fond Topo      = ' + mapBackground)
	if mainFrame.debugModeQCartoLevel > 0: print ('--- Export - Réseau GR      = ' + str(addReseauGR))
	if mainFrame.debugModeQCartoLevel > 0: print ('--- Export - Décorations    = ' + str(activeMapFrame.activeMapExportDecorationOption.isChecked()))
	if mainFrame.debugModeQCartoLevel > 0: print ('--- Export - Grilles        = ' + str(activeMapFrame.activeMapExportGridOption.isChecked()))
	if mainFrame.debugModeQCartoLevel > 0: print ('--- Export - Marges         = ' + str(requestedMargin))
	if mainFrame.debugModeQCartoLevel > 0: print ('--- Export - Echelle        = ' + str(requestedScale))
	if mainFrame.debugModeQCartoLevel > 0: print ('--- Export - Carte Globale  = ' + str(addGlobalMap))
	if mainFrame.debugModeQCartoLevel > 0: print ('--- Export - Tuiles         = ' + str(activeMapFrame.activeMapTileCounts))

	root = QgsProject.instance().layerTreeRoot()

# 	Retrouver l'échelle pour export

	echelleExport = activeMapFrame.activeMapFeature[QGP.tableFramesFieldEchelle] if mapBackground != QGP.configExportTextOsmLayers else requestedScale
	if mainFrame.debugModeQCartoLevel > 0: print ('--- Export - Echelle        = ' + str(echelleExport))

#	Retrouver la taille de la carte pour export

	mapGeometry =  mainFrame.layerMaps.getFeature(activeMapFrame.activeMapFeature.id()).geometry()					# Need to access real geometry - maybe temporarily changed
	tailleXCarte = mapGeometry.boundingBox().width()
	tailleYCarte = mapGeometry.boundingBox().height()
	if mainFrame.debugModeQCartoLevel > 0: print ('--- Export - Largeur m      = ' + str(tailleXCarte))
	if mainFrame.debugModeQCartoLevel > 0: print ('--- Export - Hauteur m      = ' + str(tailleYCarte))

#	Intégrer la zone extra pour Osm

	if mapBackground == QGP.configExportTextOsmLayers:
		tailleXCarte += 2 * QGP.configFrameOsmExtraSize
		tailleYCarte += 2 * QGP.configFrameOsmExtraSize

#	Rectangle d'export global

	mapMargin = round(requestedMargin * echelleExport / 1000) if mapBackground != QGP.configExportTextOsmLayers else QGP.configFrameOsmExtraSize
	rectExport = QgsRectangle()
	rectExport.setXMinimum(mapGeometry.boundingBox().xMinimum() - mapMargin)
	rectExport.setXMaximum(mapGeometry.boundingBox().xMaximum() + mapMargin)
	rectExport.setYMinimum(mapGeometry.boundingBox().yMinimum() - mapMargin)
	rectExport.setYMaximum(mapGeometry.boundingBox().yMaximum() + mapMargin)

# 	Compteurs de Couches

	couchesInexistantes = 0
	couchesNonVisibles = 0
	couchesHorsCadre = 0
	couchesVisibles = 0
	
#	Liste des Couches à exporter
	
	listeCoucheExport = []	
	
	
# =============================================================================
# Trouver la couche : Grille
# =============================================================================

	listeCoucheExportGrid = []
	if mapBackground != QGP.configExportTextOsmLayers and activeMapFrame.activeMapExportGridOption.isChecked():

# 	Trouver la Couche des Grilles adéquate

		pointCentre3812 = rectExport.center()
		transform = QgsCoordinateTransform(QgsCoordinateReferenceSystem("EPSG:3812"), QgsCoordinateReferenceSystem("EPSG:4326"), QgsProject.instance())
		pointCentre4326 = transform.transform(pointCentre3812)
		UTM_Zone = math.trunc((pointCentre4326.x() + 180) / 6) + 1		
		if mainFrame.debugModeQCartoLevel > 0: print ('--- Export Grille - Centre 3812 = ' + str(pointCentre3812))
		if mainFrame.debugModeQCartoLevel > 0: print ('--- Export Grille - Centre 4326 = ' + str(pointCentre4326))
		if mainFrame.debugModeQCartoLevel > 0: print ('--- Export Grille - Zone UTM    = ' + str(UTM_Zone))
	
		nomCoucheGridExport = ''
		for gridShape in QGP.configGridShapesList: 
			if (str(UTM_Zone) in gridShape): nomCoucheGridExport = gridShape
		if mainFrame.debugModeQCartoLevel > 0: print ('--- Export Grille - Nom Couche  = ' + nomCoucheGridExport)
	
# 	Ajouter des couches à l'export - Grilles

		if (nomCoucheGridExport != ''):
			coucheGrid, error = TLAY.findLayerInGroup(QGP.configGridGroupName, nomCoucheGridExport)
			if coucheGrid == None: 
				mainFrame.setStatusError(error, False)
				return None
			listeCoucheExportGrid = [coucheGrid]
			if mainFrame.debugModeQCartoLevel > 0: print ('--- Export Grille - Nom Couche  = ' + nomCoucheGridExport + ' [Ajoutée])')
			couchesVisibles = couchesVisibles + 1
		else:
			couchesInexistantes = couchesInexistantes + 1


# =============================================================================
# Trouver les couches : 'Osm-Background'
# =============================================================================

	if mapBackground == QGP.configExportTextOsmLayers:
		listeCoucheExport = layersList


# =============================================================================
# Trouver les couches : Fond Blanc
# =============================================================================

	if mapBackground == QGP.configExportTextWhite:
		listeCoucheExport = []


# =============================================================================
# Trouver les couches : Fond Osm
# =============================================================================

	if mapBackground in [QGP.configExportTextOsm]:
		listeCoucheExport = layersList
		for layer in layersList : layer.renderer().setOpacity(requestedOpacity / 100)
		

# =============================================================================
# Trouver les couches : IGN Topo-50 V3 V4
# =============================================================================

	if mapBackground in [QGP.configExportTextTopo50Ed3, QGP.configExportTextTopo50Ed4]:
		listeCoucheExport = []

# 	Retrouver le groupe Topo-50

		if (mapBackground == QGP.configExportTextTopo50Ed3): groupIgn50Name = QGP.configIGN50Ed3GroupName
		if (mapBackground == QGP.configExportTextTopo50Ed4): groupIgn50Name = QGP.configIGN50Ed4GroupName
		groupIgn50, error = TLAY.findGroup(groupIgn50Name)
		if (groupIgn50 == None):
			mainFrame.setStatusError(error, False)
			return None

# 	Trouver les Cartes Topo-50 concernées

		listCouchesTopo50Export = []
		
		for child in groupIgn50.children():
			nomCoucheDansGroupe = child.name()
			coucheIgn50, error = TLAY.openLayer(nomCoucheDansGroupe)
			if coucheIgn50 == None: 
				mainFrame.setStatusError(error, False)
				return None
			validCouche = coucheIgn50.extent().intersects(rectExport)
			if (not validCouche):
				couchesHorsCadre += 1
				continue
			listCouchesTopo50Export.append(coucheIgn50)
			if mainFrame.debugModeQCartoLevel > 0: print ('--- Export Ign-50 - Nom Couche  = ' + nomCoucheDansGroupe + ' [Ajoutée])')

# 	Ajouter des couches à l'export - Topo-50

		for coucheIgn50 in listCouchesTopo50Export:
			coucheIgn50.renderer().setOpacity(requestedOpacity / 100)
			coucheIgn50.brightnessFilter().setBrightness(requestedLuminosity)
			coucheIgn50.brightnessFilter().setContrast(requestedContrast)
			listeCoucheExport.insert(0,coucheIgn50)
			if mainFrame.debugModeQCartoLevel > 0: print ('--- Export - Carte Topo-50 simple : ' + coucheIgn50.name() + ' ' + str(requestedOpacity) + '//' + str(requestedLuminosity) + '//' + str(requestedContrast) + '% [Ajoutée])')
			couchesVisibles = couchesVisibles + 1


# =============================================================================
# Trouver les couches :  Topo-50 Lux
# =============================================================================

#	if mapBackground in [globalParam.configExportTextTopo50Lux]:
#		listeCoucheExport = []
#
#		SGRCarto_Messages.msgShow(2,msgLevel,'----- Cartes Topo 50 Lux !')

# ----------------------------------------------------------
# Pour l'export sur Topo-Lux, Changer le CRS du projet courant et réorienter le cadre
# ----------------------------------------------------------

#		rectExport = SGRCarto_Geometries.adjustRectangle2Crs(rectExport, 'EPSG:3812', 'EPSG:2169')
#		SGRCarto_Messages.msgShow(2,msgLevel,'----- Cartes Topo 50 Lux : Crs changé')

# ----------------------------------------------------------
# Retrouver le groupe Topo-50 Lux
# ----------------------------------------------------------

#		groupIgn50LuxName = globalParam.configIGN50LuxGroupName
#		groupIgn50Lux = SGRCarto_Layers.findLayerGroup(msgLevel, groupIgn50LuxName, False)
#		if (groupIgn50Lux == None):
#			SGRCarto_Messages.msgShow(1,msgLevel,'??? Groupe des Cartes Topo-50 Lux : ' + groupIgn50LuxName + ' introuvable')
#			mainFrame.setStatusError('SGRCarto_Script_Export - Groupe des Cartes Topo-50 Lux introuvable')
#			return None

# ----------------------------------------------------------
# Trouver les Cartes Topo-50 concernées
# ----------------------------------------------------------

#		listCouchesTopo50Export = []
#		
#		for child in groupIgn50Lux.children():
#			nomCoucheDansGroupe = child.name()
#			SGRCarto_Messages.msgShow(4,msgLevel,'--------- Couche du Groupe : ' + groupIgn50LuxName + ' --- ' + nomCoucheDansGroupe)
#			listeCouches = QgsProject.instance().mapLayersByName(nomCoucheDansGroupe)
#			if (len(listeCouches) == 0): 
#				SGRCarto_Messages.msgShow(2,msgLevel,'-???- Couche inexistante : ' + nomCoucheDansGroupe + ' [! Ignorée !]')
#				couchesInexistantes += 1
#				continue
#			if (len(listeCouches) > 1):
#				SGRCarto_Messages.msgShow(2,msgLevel,'-???- Couche en double : ' + nomCoucheDansGroupe + ' [! Doubles Ignorés !]')
#				couchesDoubles += 1
#				continue
#			coucheQgis = listeCouches[0]	
#			rectCouche = coucheQgis.extent()
#			SGRCarto_Messages.msgShow(4,msgLevel,'--------- Etendue Couche = ' + str(rectCouche))
#			validCouche = rectCouche.intersects(rectExport)
#			if (not validCouche):
#				SGRCarto_Messages.msgShow(4,msgLevel,'--------- Couche hors Cadre : ' + nomCoucheDansGroupe)
#				couchesHorsCadre += 1
#				continue
#			listCouchesTopo50Export.append(nomCoucheDansGroupe)
#			SGRCarto_Messages.msgShow(2,msgLevel,'----- Couche Topo-50 Lux pour Export : ' + nomCoucheDansGroupe)
#		SGRCarto_Messages.msgShow(2,msgLevel,'----- Liste des couches Topo-50 Lux pour Export : ' + str(listCouchesTopo50Export))

# ----------------------------------------------------------
# Ajouter des couches à l'export - Topo-50
# ----------------------------------------------------------

#		for map in listCouchesTopo50Export:
#			listeCouches = QgsProject.instance().mapLayersByName(map)
#			coucheQgis = listeCouches[0]
#			coucheQgis.renderer().setOpacity(requestedOpacity / 100)
#			coucheQgis.brightnessFilter().setBrightness(requestedLuminosity)
#			coucheQgis.brightnessFilter().setContrast(requestedContrast)
#			listeCoucheExport.insert(0,coucheQgis)
#			SGRCarto_Messages.msgShow(2,msgLevel,'----- Carte Topo-50 simple : ' + map + ' ' + str(requestedOpacity) + '/' + str(requestedLuminosity) + '/' + str(requestedContrast) + '% [Ajoutée])')
#			couchesVisibles = couchesVisibles + 1
#
#		mainFrame.setStatusWorking('SGRCarto_Script_Export - ' + str(couchesVisibles) + ' couche.s visible.s - ' + str(couchesNonVisibles) + ' couche.s non visible.s')


# =============================================================================
# Trouver les couches : IGN Topo-400
# =============================================================================

#	if mapBackground in [globalParam.configExportTextTopo400]:
#		listeCoucheExport = []

# ----------------------------------------------------------
# Retrouver le groupe Topo-400
# ----------------------------------------------------------

#		groupIgn400Name = globalParam.configIGN400GroupName
#		groupIgn400 = SGRCarto_Layers.findLayerGroup(msgLevel, groupIgn400Name, False)
#		if (groupIgn400 == None):
#			SGRCarto_Messages.msgShow(1,msgLevel,'??? Groupe des Cartes Topo-400 : ' + groupIgn400 + ' introuvable')
#			mainFrame.setStatusError('SGRCarto_Script_Export - Groupe des Cartes Topo-400 : ' + groupIgn400 + ' introuvable')
#			return None

# ----------------------------------------------------------
# Trouver les Cartes Topo-400 concernées - En pratique 1 seule
# ----------------------------------------------------------

#		listCouchesTopo400Export = []
#		
#		for child in groupIgn400.children():
#			nomCoucheDansGroupe = child.name()
#			SGRCarto_Messages.msgShow(4,msgLevel,'--------- Couche du Groupe : ' + groupIgn400Name + ' --- ' + nomCoucheDansGroupe)
#			listeCouches = QgsProject.instance().mapLayersByName(nomCoucheDansGroupe)
#			if (len(listeCouches) == 0): 
#				SGRCarto_Messages.msgShow(2,msgLevel,'-???- Couche inexistante : ' + nomCoucheDansGroupe + ' [! Ignorée !]')
#				couchesInexistantes += 1
#				continue
#			if (len(listeCouches) > 1):
#				SGRCarto_Messages.msgShow(2,msgLevel,'-???- Couche en double : ' + nomCoucheDansGroupe + ' [! Doubles Ignorés !]')
#				couchesDoubles += 1
#				continue
#			coucheQgis = listeCouches[0]	
#			rectCouche = coucheQgis.extent()
#			transform = QgsCoordinateTransform(coucheQgis.crs(), QgsCoordinateReferenceSystem("EPSG:3812"), QgsProject.instance())
#			rectCouche = transform.transform(rectCouche)
#			SGRCarto_Messages.msgShow(4,msgLevel,'--------- Etendue Couche = ' + str(rectCouche))
#			validCouche = rectCouche.intersects(rectExport)
#			if (not validCouche):
#				SGRCarto_Messages.msgShow(4,msgLevel,'--------- Couche hors Cadre : ' + nomCoucheDansGroupe)
#				couchesHorsCadre += 1
#				continue
#			listCouchesTopo400Export.append(nomCoucheDansGroupe)
#			SGRCarto_Messages.msgShow(2,msgLevel,'----- Couche Topo-400 pour Export : ' + nomCoucheDansGroupe)
#		SGRCarto_Messages.msgShow(2,msgLevel,'----- Liste des couches Topo-400 pour Export : ' + str(listCouchesTopo400Export))

# ----------------------------------------------------------
# Ajouter des couches à l'export - Topo-400
# ----------------------------------------------------------

#		for map in listCouchesTopo400Export:
#			listeCouches = QgsProject.instance().mapLayersByName(map)
#			coucheQgis = listeCouches[0]
#			coucheQgis.renderer().setOpacity(requestedOpacity / 100)
#			coucheQgis.brightnessFilter().setBrightness(requestedLuminosity)
#			coucheQgis.brightnessFilter().setContrast(requestedContrast)
#			listeCoucheExport.insert(0,coucheQgis)
#			SGRCarto_Messages.msgShow(2,msgLevel,'----- Carte Topo-400 simple : ' + map + ' ' + str(requestedOpacity) + '/' + str(requestedLuminosity) + '/' + str(requestedContrast) + '% [Ajoutée])')
#			couchesVisibles = couchesVisibles + 1
#
#		mainFrame.setStatusWorking('SGRCarto_Script_Export - ' + str(couchesVisibles) + ' couche.s visible.s - ' + str(couchesNonVisibles) + ' couche.s non visible.s')


# =============================================================================
# Trouver les couches : IGN Topo-250
# =============================================================================

#	if mapBackground in [globalParam.configExportTextTopo250]:
#		listeCoucheExport = []

# ----------------------------------------------------------
# Retrouver le groupe Topo-250
# ----------------------------------------------------------

#	groupIgn250Name = globalParam.configIGN250GroupName
#		groupIgn250 = SGRCarto_Layers.findLayerGroup(msgLevel, groupIgn250Name, False)
#		if (groupIgn250 == None):
#			SGRCarto_Messages.msgShow(1,msgLevel,'??? Groupe des Cartes Topo-250 : ' + groupIgn250 + ' introuvable')
#			mainFrame.setStatusError('SGRCarto_Script_Export - Groupe des Cartes Topo-250 : ' + groupIgn250 + ' introuvable')
#			return None

# ----------------------------------------------------------
# Trouver les Cartes Topo-250 concernées - En pratique 1 seule
# ----------------------------------------------------------

#		listCouchesTopo250Export = []
#		
#		for child in groupIgn250.children():
#			nomCoucheDansGroupe = child.name()
#			SGRCarto_Messages.msgShow(4,msgLevel,'--------- Couche du Groupe : ' + groupIgn250Name + ' --- ' + nomCoucheDansGroupe)
#			listeCouches = QgsProject.instance().mapLayersByName(nomCoucheDansGroupe)
#			if (len(listeCouches) == 0): 
#				SGRCarto_Messages.msgShow(2,msgLevel,'-???- Couche inexistante : ' + nomCoucheDansGroupe + ' [! Ignorée !]')
#				couchesInexistantes += 1
#				continue
#			if (len(listeCouches) > 1):
#				SGRCarto_Messages.msgShow(2,msgLevel,'-???- Couche en double : ' + nomCoucheDansGroupe + ' [! Doubles Ignorés !]')
#				couchesDoubles += 1
#				continue
#			coucheQgis = listeCouches[0]	
#			rectCouche = coucheQgis.extent()
#			SGRCarto_Messages.msgShow(4,msgLevel,'--------- Etendue Couche = ' + str(rectCouche))
#			validCouche = rectCouche.intersects(rectExport)
#			if (not validCouche):
#				SGRCarto_Messages.msgShow(4,msgLevel,'--------- Couche hors Cadre : ' + nomCoucheDansGroupe)
#				couchesHorsCadre += 1
#				continue
#			listCouchesTopo250Export.append(nomCoucheDansGroupe)
#			SGRCarto_Messages.msgShow(2,msgLevel,'----- Couche Topo-250 pour Export : ' + nomCoucheDansGroupe)
#		SGRCarto_Messages.msgShow(2,msgLevel,'----- Liste des couches Topo-250 pour Export : ' + str(listCouchesTopo250Export))

# ----------------------------------------------------------
# Ajouter des couches à l'export - Topo-250
# ----------------------------------------------------------

#		for map in listCouchesTopo250Export:
#			listeCouches = QgsProject.instance().mapLayersByName(map)
#			coucheQgis = listeCouches[0]
#			coucheQgis.renderer().setOpacity(requestedOpacity / 100)
#			coucheQgis.brightnessFilter().setBrightness(requestedLuminosity)
#			coucheQgis.brightnessFilter().setContrast(requestedContrast)
#			listeCoucheExport.insert(0,coucheQgis)
#			SGRCarto_Messages.msgShow(2,msgLevel,'----- Carte Topo-250 simple : ' + map + ' ' + str(requestedOpacity) + '/' + str(requestedLuminosity) + '/' + str(requestedContrast) + '% [Ajoutée])')
#			couchesVisibles = couchesVisibles + 1
#
#		mainFrame.setStatusWorking('SGRCarto_Script_Export - ' + str(couchesVisibles) + ' couche.s visible.s - ' + str(couchesNonVisibles) + ' couche.s non visible.s')


# =============================================================================
# Trouver les couches : IGN Topo-10
# =============================================================================

#	if mapBackground in [globalParam.configExportTextTopo10]:
#		listeCoucheExport = []

# ----------------------------------------------------------
# Retrouver le groupe Topo-10
# ----------------------------------------------------------

#		groupIgn10Name = globalParam.configIGN10GroupName
#		groupIgn10 = SGRCarto_Layers.findLayerGroup(msgLevel, groupIgn10Name, False)
#
#		if (groupIgn10 == None):
#			SGRCarto_Messages.msgAbort('Groupe des Cartes Topo-10 introuvable')
#			mainFrame.setStatusError('SGRCarto_Script_Export - Groupe des Cartes Topo-10 introuvable')
#			return None

# ----------------------------------------------------------
# Trouver les Cartes Topo-10 concernées ! Not in 3812
# ----------------------------------------------------------

#		listCouchesTopo10Export = []
#
#		for child in groupIgn10.children():
#			nomCoucheDansGroupe = child.name()
#			SGRCarto_Messages.msgShow(4,msgLevel,'--------- Couche du Groupe : ' + groupIgn10Name + ' --- ' + nomCoucheDansGroupe)
#			listeCouches = QgsProject.instance().mapLayersByName(nomCoucheDansGroupe)
#			if (len(listeCouches) == 0): 
#				SGRCarto_Messages.msgShow(2,msgLevel,'-???- Couche inexistante : ' + nomCoucheDansGroupe + ' [! Ignorée !]')
#				couchesInexistantes += 1
#				continue
#			if (len(listeCouches) > 1):
#				SGRCarto_Messages.msgShow(2,msgLevel,'-???- Couche en double : ' + nomCoucheDansGroupe + ' [! Doubles Ignorés !]')
#				couchesDoubles += 1
#				continue
#			coucheQgis = listeCouches[0]	
#			rectCouche = coucheQgis.extent()
#			transform = QgsCoordinateTransform(coucheQgis.crs(), QgsCoordinateReferenceSystem("EPSG:3812"), QgsProject.instance())
#			rectCouche = transform.transform(rectCouche)
#			SGRCarto_Messages.msgShow(4,msgLevel,'--------- Etendue Couche = ' + str(rectCouche))
#			validCouche = rectCouche.intersects(rectExport)
#			if (not validCouche):
#				SGRCarto_Messages.msgShow(4,msgLevel,'--------- Couche hors Cadre : ' + nomCoucheDansGroupe)
#				couchesHorsCadre += 1
#				continue
#			listCouchesTopo10Export.append(nomCoucheDansGroupe)
#			SGRCarto_Messages.msgShow(2,msgLevel,'----- Couche Topo-10 pour Export : ' + nomCoucheDansGroupe)
#		SGRCarto_Messages.msgShow(2,msgLevel,'----- Liste des couches Topo-10 pour Export : ' + str(listCouchesTopo10Export))

# ----------------------------------------------------------
# Ajouter des couches à l'export - Topo-10
# ----------------------------------------------------------

#		for map in listCouchesTopo10Export:
#			listeCouches = QgsProject.instance().mapLayersByName(map)
#			coucheQgis = listeCouches[0]
#			coucheQgis.renderer().setOpacity(requestedOpacity / 100)
#			coucheQgis.brightnessFilter().setBrightness(requestedLuminosity)
#			coucheQgis.brightnessFilter().setContrast(requestedContrast)
#			listeCoucheExport.insert(0,coucheQgis)
#			SGRCarto_Messages.msgShow(2,msgLevel,'----- Carte Topo-10 simple : ' + map + ' ' + str(requestedOpacity) + '/' + str(requestedLuminosity) + '/' + str(requestedContrast) + '% [Ajoutée])')
#			couchesVisibles = couchesVisibles + 1
#
#		mainFrame.setStatusWorking('SGRCarto_Script_Export - ' + str(couchesVisibles) + ' couche.s visible.s - ' + str(couchesNonVisibles) + ' couche.s non visible.s')


# =============================================================================
# Trouver les couches : Canevas
# =============================================================================

	if mapBackground in [QGP.configExportTextCanevas]:
		listeCoucheExport = []
		for coucheQgis in iface.mapCanvas().layers():
			rectCouche = coucheQgis.extent()
			transform = QgsCoordinateTransform(coucheQgis.crs(), QgsCoordinateReferenceSystem("EPSG:3812"), QgsProject.instance())
			rectCouche = transform.transform(rectCouche)
			validCouche = rectCouche.intersects(rectExport)
			if (not validCouche):
				couchesHorsCadre += 1
			listeCoucheExport.insert(0,coucheQgis)
			couchesVisibles = couchesVisibles + 1

		listeCoucheExport.reverse()


# =============================================================================
# Trouver les couches : Décoration : Projets et Cadres 
# =============================================================================

	listeCoucheExportDecorations = []
	if mapBackground != QGP.configExportTextOsmLayers and activeMapFrame.activeMapExportDecorationOption.isChecked():

		coucheDecoration, error = TLAY.findLayerInGroup(QGP.configFrameGroupName, QGP.configShapeMapDecorationNumber)
		if coucheDecoration == None: 
			mainFrame.setStatusError(error, False)
			return None
		listeCoucheExportDecorations.append(coucheDecoration)
		if mainFrame.debugModeQCartoLevel > 0: print ('--- Export Décoration - Nom Couche  = ' + coucheDecoration.name() + ' [Ajoutée])')
		couchesVisibles = couchesVisibles + 1
	
		coucheDecoration, error = TLAY.findLayerInGroup(QGP.configFrameGroupName, QGP.configShapeMapDecorationCopyright)
		if coucheDecoration == None: 
			mainFrame.setStatusError(error, False)
			return None
		listeCoucheExportDecorations.append(coucheDecoration)
		if mainFrame.debugModeQCartoLevel > 0: print ('--- Export Décoration - Nom Couche  = ' + coucheDecoration.name() + ' [Ajoutée])')
		couchesVisibles = couchesVisibles + 1

		coucheDecoration, error = TLAY.findLayerInGroup(QGP.configFrameGroupName, QGP.configShapeMapDecorationWhiteFrame)
		if coucheDecoration != None and root.findLayer(coucheDecoration).isVisible():
			listeCoucheExportDecorations.append(coucheDecoration)
			if mainFrame.debugModeQCartoLevel > 0: print ('--- Export Décoration - Nom Couche  = ' + coucheDecoration.name() + ' [Ajoutée])')
			couchesVisibles = couchesVisibles + 1


# =============================================================================
# Trouver les couches : Projet Actif et Projet Autres
# =============================================================================

	listeCoucheExportActiveProject = []
	if addReseauGR:

# 	Retrouver le groupe : Projet Actif 

		groupActiveProject, error = TLAY.findGroup(QGP.configActiveProjectGroupName)
		if (groupActiveProject == None):
			mainFrame.setStatusError(error, False)
			return None

# 	Ajouter des couches à l'export - Projet Actif

		for child in groupActiveProject.children():
			nomCoucheProject = child.name()
			coucheActiveProject, error = TLAY.findLayerInGroup(QGP.configActiveProjectGroupName, nomCoucheProject)
			if coucheActiveProject == None: 
				mainFrame.setStatusError(error, False)
				return None
			node = root.findLayer(coucheActiveProject)
			if node.isVisible():
				listeCoucheExportActiveProject.append(coucheActiveProject)
				if mainFrame.debugModeQCartoLevel > 0: print ('--- Export Projet Actif - Nom Couche  = ' + nomCoucheProject + ' [Ajoutée])')
				couchesVisibles = couchesVisibles + 1
			else:
				couchesNonVisibles = couchesNonVisibles + 1

# 	Retrouver le groupe : Projet Autres (optionnel)

		groupOtherProject, error = TLAY.findGroup(QGP.configOtherProjectGroupName)
		if (groupOtherProject != None) :

# 	Ajouter des couches à l'export - Projet Autres

			for child in groupOtherProject.children():
				nomCoucheProject = child.name()
				coucheOthersProject, error = TLAY.findLayerInGroup(QGP.configOtherProjectGroupName, nomCoucheProject)
				if coucheOthersProject == None: 
					mainFrame.setStatusError(error, False)
					return None
				node = root.findLayer(coucheOthersProject)
				if node.isVisible():
					listeCoucheExportActiveProject.append(coucheOthersProject)
					if mainFrame.debugModeQCartoLevel > 0: print ('--- Export Projet Autres - Nom Couche  = ' + nomCoucheProject + ' [Ajoutée])')
					couchesVisibles = couchesVisibles + 1
				else:
					couchesNonVisibles = couchesNonVisibles + 1


# =============================================================================
# Trouver les couches : Carte Active
# =============================================================================

	listeCoucheExportActiveMap = []
	if addReseauGR:

# 	Retrouver le groupe : Projet Actif 

		groupActiveMap, error = TLAY.findGroup(QGP.configActiveMapGroupName)
		if (groupActiveMap == None):
			mainFrame.setStatusError(error, False)
			return None

# 	Ajouter des couches à l'export - Carte Active

		for child in groupActiveMap.children():
			nomCoucheActiveMap = child.name()
			coucheActiveMap, error = TLAY.findLayerInGroup(QGP.configActiveMapGroupName, nomCoucheActiveMap)
			if coucheActiveMap == None: 
				mainFrame.setStatusError(error, False)
				return None
			node = root.findLayer(coucheActiveMap)
			if node.isVisible():
				listeCoucheExportActiveMap.append(coucheActiveMap)
				if mainFrame.debugModeQCartoLevel > 0: print ('--- Export Carte Active - Nom Couche  = ' + nomCoucheActiveMap + ' [Ajoutée])')
				couchesVisibles = couchesVisibles + 1
			else:
				couchesNonVisibles = couchesNonVisibles + 1


# =============================================================================
# =============================================================================
#
# Boucler sur les différentes tuiles
#
# =============================================================================
# =============================================================================

	tileXCount = activeMapFrame.activeMapTileCounts[0]
	tileYCount = activeMapFrame.activeMapTileCounts[1]

	globalWidth = mapGeometry.boundingBox().width()
	globalHeight = mapGeometry.boundingBox().height()
	globalStamp = TDAT.getTimeStamp()

	dicoTileFileNames = {}

# 	Create Progress Bar

	progressBar = TPRO.createProgressBar(activeMapFrame.activeMapExportTileCurrentInfo, tileXCount * tileYCount, 'Normal')

	for tileX in range(tileXCount) :
		dicoTileFileNames[tileX] = {}
		for tileY in range(tileYCount) :

			if mainFrame.debugModeQCartoLevel > 0: print ('--- Export - Tile = ' + str(tileX) + ' - ' + str(tileY))

#		Taille du papier en mm

			papierXCarte = tailleXCarte * 1000 / (echelleExport * activeMapFrame.activeMapTileCounts[0])
			papierYCarte = tailleYCarte * 1000 / (echelleExport * activeMapFrame.activeMapTileCounts[1])
			papierXCarte = papierXCarte + 2 * requestedMargin
			papierYCarte = papierYCarte + 2 * requestedMargin
			if mainFrame.debugModeQCartoLevel > 0: print ('--- Export - Largeur mm     = ' + str(papierXCarte))
			if mainFrame.debugModeQCartoLevel > 0: print ('--- Export - Hauteur mm     = ' + str(papierYCarte))
	
# 		Intégrer les Marges (la zone extra si configExportTextOsmBackground) à la Géométrie d'export

			mapMargin = round(requestedMargin * echelleExport / 1000) if mapBackground != QGP.configExportTextOsmLayers else QGP.configFrameOsmExtraSize
			rectExportTile = QgsRectangle()
			rectExportTile.setXMinimum(mapGeometry.boundingBox().xMinimum() + tileX * globalWidth / tileXCount - mapMargin)
			rectExportTile.setXMaximum(mapGeometry.boundingBox().xMinimum() + (tileX + 1) * globalWidth / tileXCount + mapMargin)
			rectExportTile.setYMaximum(mapGeometry.boundingBox().yMaximum() - tileY * globalHeight / tileYCount + mapMargin)
			rectExportTile.setYMinimum(mapGeometry.boundingBox().yMaximum() - (tileY + 1) * globalHeight / tileYCount - mapMargin)
			if mainFrame.debugModeQCartoLevel > 0: print ('--- Export - Rectangle      = ' + str(rectExportTile))


# =============================================================================
# Finaliser l'export tile
# =============================================================================

#		Afficher numéro de tuile 

#			activeMapFrame.activeMapExportTileCurrentInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%', '. . . ' + str(tileX) + '-' + str(tileY) + ' . . .'))

# 		Retrouver les paramètres d'export

			if mapMode == 'Schéma' : 
				exportDpi = 300
				exportPath = QGP.configPathExportPlansImages.replace('%PROJECT%', TCOD.itineraryFolderFromTrackCode(activeMapFrame.activeMapItinerary)) if mapBackground != QGP.configExportTextOsmLayers else QGP.configPathExportOsm
				exportFile = QGP.configFileExportPlans
				TFIL.ensure_dir(exportPath)
				deliveryPath = QGP.configPathExportPlans.replace('%PROJECT%', TCOD.itineraryFolderFromTrackCode(activeMapFrame.activeMapItinerary)) if mapBackground != QGP.configExportTextOsmLayers else QGP.configPathExportOsm
				TFIL.ensure_dir(deliveryPath)
			else:	
				exportDpi = int(activeMapFrame.activeMapExportDpiCombo.currentText()) if mapBackground != QGP.configExportTextOsmLayers else QGP.configExportDpiOsm
				exportPath = (QGP.configPathExportImages if mapBackground != QGP.configExportTextOsmLayers else QGP.configPathExportOsm).replace('%PROJECT%', TCOD.itineraryFolderFromTrackCode(activeMapFrame.activeMapItinerary)) 
				exportFile = QGP.configFileExportImages  if mapBackground != QGP.configExportTextOsmLayers else QGP.configNameExportOsm
				TFIL.ensure_dir(exportPath)

			exportFile = exportFile if mapBackground != QGP.configExportTextOsmLayers else QGP.configNameExportOsm
			exportFile = exportFile.replace("%PREFIX%", mapFilePrefix)
			exportFile = exportFile.replace("%ITI%", activeMapFrame.activeMapItinerary)
			exportFile = exportFile.replace("%MAP%", activeMapFrame.activeMapName)
			exportFile = exportFile.replace("%MODE%", mapMode)
			exportFile = exportFile.replace("%BACK%", mapBackground)	
			exportFile = exportFile.replace("%SCALE%", str(echelleExport))	
			exportFile = exportFile.replace("%TIME%", globalStamp)
			exportFile = exportFile.replace("%TILE%", (' - Tile ' + '{:02d}'.format(tileX) + '-' + '{:02d}'.format(tileY)) if tileXCount * tileYCount > 1 else '')
			dicoTileFileNames[tileX][tileY] = exportFile

			imagePath = exportPath + exportFile	

			exportBgdColor = QGP.configExportBgdColor
			exportWaitMax =	QGP.configExportWaitMax

			if mainFrame.debugModeQCartoLevel > 0: print ('')
			if mainFrame.debugModeQCartoLevel > 0: print ('--- Export Path         = ' + exportPath)
			if mainFrame.debugModeQCartoLevel > 0: print ('--- Export File         = ' + exportFile)
			if mainFrame.debugModeQCartoLevel > 0: print ('--- Export DPI          = ' + str(exportDpi))
			if mainFrame.debugModeQCartoLevel > 0: print ('--- Export Background   = ' + str(exportBgdColor))
			if mainFrame.debugModeQCartoLevel > 0: print ('--- Export Wait Max     = ' + str(exportWaitMax))

# 		Afficher la Liste des Couches et les décomptes
	
			if mapBackground not in [QGP.configExportTextCanevas, QGP.configExportTextOsmLayers]:
				listeCoucheExport = listeCoucheExportDecorations + listeCoucheExportActiveMap + listeCoucheExportActiveProject + listeCoucheExportGrid + listeCoucheExport

			if mainFrame.debugModeQCartoLevel > 0: print ('')
			if mainFrame.debugModeQCartoLevel > 0: print ('--- Export Couches = ' + str(len(listeCoucheExport)))
			for couche in listeCoucheExport:
				if mainFrame.debugModeQCartoLevel > 0: print ('--- Export Couche = ' + str(couche))

			if mainFrame.debugModeQCartoLevel > 0: print (' ')
			if mainFrame.debugModeQCartoLevel > 0: print ('--- Couche.s visible.s à exporter = ' + str(couchesVisibles))
			if mainFrame.debugModeQCartoLevel > 0: print ('--- Couche.s visible.s à exporter = ' + str(couchesNonVisibles))
			if mainFrame.debugModeQCartoLevel > 0: print ('--- Couche.s non visible.s = ' + str(couchesNonVisibles))
			if mainFrame.debugModeQCartoLevel > 0: print ('--- Couche.s hors cadre    = ' + str(couchesHorsCadre))
			if mainFrame.debugModeQCartoLevel > 0: print ('--- Couche.s inexistante.s = ' + str(couchesInexistantes))

# 	Calculer parametres export

			pixelsX = math.ceil(papierXCarte / 25.4 * exportDpi)
			pixelsY = math.ceil(papierYCarte / 25.4 * exportDpi)
			if mainFrame.debugModeQCartoLevel > 0: print (' ')
			if mainFrame.debugModeQCartoLevel > 0: print ('--- Export - Pixels X = ' + str(pixelsX))
			if mainFrame.debugModeQCartoLevel > 0: print ('--- Export - Pixels Y = ' + str(pixelsY))

# 	Export .pgw World File

			if mapBackground in (QGP.configExportTextOsmLayers, QGP.configExportTextCanevas) :
				meterByPixelX = (papierXCarte * echelleExport / 1000) / pixelsX
				meterByPixelY = (papierYCarte * echelleExport / 1000) / pixelsY
				x0 = rectExportTile.xMinimum() + meterByPixelX / 2
				y0 = rectExportTile.yMaximum() - meterByPixelY / 2

				exportWorldFile(exportPath, exportFile, x0, y0, meterByPixelX, meterByPixelY)

# 	Préparer le "render"

			crs = QgsCoordinateReferenceSystem()
			crs.createFromString('EPSG:3812')

#	if mapBackground in [globalParam.configExportTextTopo50Lux]:
#		crs.createFromString('EPSG:2169')
#	else:
#		crs.createFromString('EPSG:3812')

			settings = QgsMapSettings()
			settings.setLayers(listeCoucheExport)
			settings.setBackgroundColor(exportBgdColor)
			settings.setOutputSize(QSize(pixelsX, pixelsY))
			settings.setOutputDpi(exportDpi)
			settings.setExtent(rectExportTile)
			settings.setDestinationCrs(crs)
	
			if mainFrame.debugModeQCartoLevel > 0: print (' ')
			if mainFrame.debugModeQCartoLevel > 0: print ('--- Cadre Export = ' + str(settings.extent()))
			if mainFrame.debugModeQCartoLevel > 0: print ('--- Echelle Calculée = ' + str(settings.scale()))
			if mainFrame.debugModeQCartoLevel > 0: print ('--- Settings Valides = ' + str(settings.hasValidSettings()))

			QgsApplication.processEvents()

			render = QgsMapRendererParallelJob(settings)
			render.waitForFinished()
			render.finished.connect(exportFinished)


# =============================================================================
# Export Effectif
# =============================================================================

			if tileXCount * tileYCount == 1 :
				mainFrame.setStatusWorking('Export de la carte : démarrage export effectif ...')
			else :
				mainFrame.setStatusWorking('Export de la tuile ' + str(tileX) + '-' + str(tileY) + ' : démarrage export effectif ...')
		
			imageSaved = False
			waitCount = 0

			render.start()

			while (not imageSaved):
				QgsApplication.processEvents()
				TDAT.sleep(1000)
				waitCount = waitCount + 1
				mainFrame.setStatusWorking('Export en cours ... (' + str(waitCount) + ' sec)')
				if (waitCount > exportWaitMax): 
					mainFrame.setStatusWorking('Export toujours en cours en parallèle ... (exit)')
					break
	
			if (imageSaved):
				png = QImage()
				png.load(imagePath)
				png.setDotsPerMeterX(math.ceil(exportDpi / 25.4 * 1000))
				png.setDotsPerMeterY(math.ceil(exportDpi / 25.4 * 1000))
				png.save(imagePath, "png")
				
			progressBar.setValue(progressBar.value() + 1)

				
# =============================================================================
# Export IrfanView Batch
# =============================================================================

	if tileXCount > 1 or tileYCount > 1 :
		newline   = QGP.configCSVNewLine
		fileOut = open(exportPath + 'Z3 - Map Band Generation (' + globalStamp + ').bat', 'w', encoding='utf-8', errors='ignore')
		for band in dicoTileFileNames :
			fileOut.write('"C:\Program Files\IrfanView\i_view64.exe" /panorama=(2')
			for tile in dicoTileFileNames[band] :
				fileOut.write(',' + dicoTileFileNames[band][tile])
			fileOut.write(') /convert=' + mapFilePrefix + '- ' + activeMapFrame.activeMapItinerary + ' - ' + activeMapFrame.activeMapName + ' - ' + 'Map Band ' + str(band) + ' (' + globalStamp + ').png')
			fileOut.write(newline)
		fileOut.close()

			
# =============================================================================
# Done ...
# =============================================================================

	del progressBar
	activeMapFrame.activeMapExportTileCurrentInfo.setText(DSTY.textFormatBlackNormal.replace('%TEXT%', 'Terminé'))

	endTime = time.time()
	workingTime = int(endTime - startTime)

	if (couchesInexistantes > 0) :
		mainFrame.setStatusWarning('Export terminé : ' + str(couchesInexistantes) + ' couche.s inexistante.s - ')
	else:	
		mainFrame.setStatusDone('Carte = ' + imagePath)

	return imagePath

# ========================================================================================
	
def exportFinished():

	global imageSaved
	global imagePath
	global msgLevel

	img = render.renderedImage()
	img.save(imagePath, "png")
	imageSaved = True


# ========================================================================================
# Créer un fichier "world" .pgw
# ========================================================================================

def exportWorldFile(path, file, x0, y0, meterByPixelX, meterByPixelY):

	worldPath = path + file
	worldPath = worldPath.replace('.png','.pgw')
	
	fileOut = open(worldPath, 'w', encoding='utf8', errors='ignore')
	fileOut.write('{:.12f}'.format(meterByPixelX) + '\n')						# Ligne 1 : Direction X - Mètres / pixel  	Line 1: A: x-component of the pixel width (x-scale)
	fileOut.write('{:.12f}'.format(0) + '\n')									# Ligne 2 : 0 								Line 2: D: y-component of the pixel width (y-skew)
	fileOut.write('{:.12f}'.format(0) + '\n')									# Ligne 3 : 0								Line 3: B: x-component of the pixel height (x-skew)
	fileOut.write('{:.12f}'.format(-meterByPixelY) + '\n')						# Ligne 4 : Direction Y - Mètres / pixel 	Line 4: E: y-component of the pixel height (y-scale), typically negative
	fileOut.write('{:.12f}'.format(x0) + '\n')									# Ligne 5 : X0 (pixel NO)					Line 5: C: x-coordinate of the center of the original image's upper left pixel transformed to the map
	fileOut.write('{:.12f}'.format(y0) + '\n')									# Ligne 6 : Y0 (pixel NO)					Line 6: F: y-coordinate of the center of the original image's upper left pixel transformed to the map
	fileOut.close()


# ========================================================================================
# --- THE END ---
# ========================================================================================
