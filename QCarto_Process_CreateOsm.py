# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Generation automatique une série de couches Qgis à partir d'un fichier .osm 
# ========================================================================================


modShowPoint = 100
modShowLine = 100
modShowArea = 10
modShowFeature = 100
modShowRoute = 1
modShowTrace = 1


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qgis.core import *
from qgis.gui import *
from qgis.PyQt import QtWidgets

from xml.dom.minidom import parse, parseString	

import os
import time
import importlib
import traceback

import QCarto_Tools_Dates as TDAT
import QCarto_Tools_Files as TFIL
import QCarto_Tools_Layers as TLAY
importlib.reload(TLAY)
import QCarto_Tools_Geometries as TGEO
importlib.reload(TGEO)
import QCarto_Tools_Buttons as TBUT
import QCarto_Tools_Coding as TCOD
import QCarto_Tools_Progress as TPRO

import QCarto_Definitions_Colors as DCOL
import QCarto_Definitions_Styles as DSTY

import QCarto_Parameters_Global
importlib.reload(QCarto_Parameters_Global)
QGP = QCarto_Parameters_Global.globalParameters()	

modShowPoint = 100


# ========================================================================================
# Creation du shape d'une Relation OSM
# >>> iface
# >>> mainFrame
# >>> codeProject		: str				Code du projet (répertoire)
# >>> codeTrack			: str				Code du tracé
# >>> osmRelation		: str				Numéro de relation Osm
# <<< fileOsm			: bool				Relation Osm - None si erreur
# ========================================================================================

def createRelation(iface, mainFrame, codeProject, codeTrack, osmRelation):

# 	Welcome !

	mainFrame.setStatusWorking(codeTrack + ' - OSM relation ' + osmRelation + ' : Création d\'un shape du Parcours ...') 
	startTime = time.time()

#	Retrouver le fichier OSM

	path = QGP.configPathOsmFiles
	path = path.replace('%PROJECT%', codeProject)
	if not os.path.isdir(path) :
		mainFrame.setStatusWarning(codeTrack + ' - OSM relation ' + osmRelation +  ': Le répertoire Osm Files n\'existe pas !')
		return

	osmFile = None
	for fileName in sorted(os.listdir(path)):
		if codeTrack + ' - ' + osmRelation not in fileName: continue
		if fileName[-4:] != '.osm': continue
		osmFile = fileName								# Continue to find last file ...
	if osmFile == None:
		mainFrame.setStatusWarning(codeTrack + ' - OSM relation ' + osmRelation + ' : Le fichier .osm n\'existe pas !')
		return

	mainFrame.setStatusWorking(codeTrack + ' - OSM relation ' + osmRelation + ' : Fichier Osm = ' + osmFile)
			
# 	Retrouver / Créer les Groupe Qgis

	groupOsm, error = TLAY.findGroup(QGP.configOsmTrackGroupName)
	if groupOsm == None:
		groupIndexDB, error = TLAY.findGroupIndex(QGP.configDBCartoGroupName)
		TLAY.createGroup(QGP.configOsmTrackGroupName, groupIndexDB + 1 if groupIndexDB != None else 0)
		groupOsm, error = TLAY.findGroup(QGP.configOsmTrackGroupName)

#	Retrouver le sous-groupe de l'itinéraire

	osmSubGroupName = TCOD.itineraryFromTrackCode(codeTrack)
	subGroupOsm, error = TLAY.findGroup(osmSubGroupName)
	if subGroupOsm == None:
		subGroupOsm = groupOsm.addGroup(osmSubGroupName)
		subGroupOsm.setItemVisibilityChecked(True)	

#	Charger / Créer la couche du Parcours

	layerNameOsm = codeTrack + ' - ' + osmRelation
	layerOsm, error = TLAY.findLayerInGroup(osmSubGroupName, layerNameOsm)

	if layerOsm == None: 
		projectPath = QGP.configPathOsmTrack.replace('%PROJECT%', codeProject)
		TFIL.ensure_dir(projectPath)
		if not os.path.exists(projectPath + layerNameOsm + '.shp'):
			status, count = TFIL.copy_files(QGP.configPathOsmShape, projectPath, QGP.configFileOsmShape, layerNameOsm)
			if not status : 
				mainFrame.setStatusWarning(codeTrack + ' - OSM relation ' + osmRelation + ' : Le shape de référence Parcours-OSM n\'existe pas !')
				return
		layerOsm, errorText = TLAY.loadLayer(projectPath, layerNameOsm, osmSubGroupName, layerNameOsm, None, None, False)
		if layerOsm == None:
			mainFrame.setStatusWarning(codeTrack + ' - OSM relation ' + osmRelation + ' : ' + errorText)
			return

# 	Parser le fichier Osm et statistiques

	mainFrame.setStatusWorking(codeTrack + ' - OSM relation ' + osmRelation + ' : Parsing du Fichier OSM ...')
	osmXML = parse(path + osmFile)
	mainFrame.setStatusWorking(codeTrack + ' - OSM relation ' + osmRelation + ' : Parsing terminé !')
	TDAT.sleep(250)
	
# 	Création d'un Dictionnaire des Points

	mainFrame.setStatusWorking(codeTrack + ' - OSM relation ' + osmRelation + ' : Génération du Dictionnaire des Points ...')

	crs3812 = QgsCoordinateReferenceSystem("EPSG:3812")
	crs4326 = QgsCoordinateReferenceSystem("EPSG:4326")
	
	coordinateTransform = QgsCoordinateTransform()
	coordinateTransform.setSourceCrs(crs4326)
	coordinateTransform.setDestinationCrs(crs3812)

	dicoNoeuds = {}
	nodeCount = 0

	for node in osmXML.getElementsByTagName('node'):
		id = node.getAttribute("id")
		lat = node.getAttribute("lat")
		lon = node.getAttribute("lon")
		pXY =  QgsPointXY(float(lon),float(lat))
		pXY = coordinateTransform.transform(pXY)
		dicoNoeuds[id] = pXY
		nodeCount += 1
		QgsApplication.processEvents()
	
	mainFrame.setStatusWorking(codeTrack + ' - OSM relation ' + osmRelation + ' : Dictionnaire des Points : ' + str(nodeCount) + ' points !')
	TDAT.sleep(250)	
	
# 	Création d'un Dictionnaire des Lignes

	mainFrame.setStatusWorking(codeTrack + ' - OSM relation ' + osmRelation + ' : Génération du Dictionnaire des Lignes ...')

	dicoLignes = {}
	wayCount = 0

	for way in osmXML.getElementsByTagName('way'):
		id = way.getAttribute("id")
		listeSommets = []
		for point in way.getElementsByTagName("nd"):
			ref = point.getAttribute("ref")
			listeSommets.append(dicoNoeuds[ref])
		if (len(listeSommets) <= 1): continue
		if (listeSommets[0] == listeSommets[-1]): continue
		dicoLignes[id] = listeSommets
		wayCount += 1
		QgsApplication.processEvents()

	mainFrame.setStatusWorking(codeTrack + ' - OSM relation ' + osmRelation + ' : Dictionnaire des Lignes : ' + str(wayCount) + ' lignes !')
	TDAT.sleep(250)	

#	Création de la Liste des Lignes pour la Relation OSM 

	mainFrame.setStatusWorking(codeTrack + ' - OSM relation ' + osmRelation + ' : Génération de la Géométrie de la Relation ...')
	
	wayDico = {}
	for relation in osmXML.getElementsByTagName('relation'):
		id = relation.getAttribute("id")
		if id != osmRelation : continue
		wayDico = { member.getAttribute('ref') : dicoLignes[member.getAttribute('ref')] for member in relation.getElementsByTagName('member') if member.getAttribute('type') == 'way' and member.getAttribute('ref') in dicoLignes }
		QgsApplication.processEvents()
	
	mainFrame.setStatusWorking(codeTrack + ' - OSM relation ' + osmRelation + ' : Chemins dans la relation : ' + str(len(wayDico)) + ' chemins !')
	TDAT.sleep(250)	
	
# 	Définir la couche OSM

	mainFrame.setStatusWorking(codeTrack + ' - OSM relation ' + osmRelation + ' : Création de la couche ' + layerNameOsm)

	layerOsm.startEditing()
	layerOsm.selectAll()
	layerOsm.deleteSelectedFeatures()
	
	for wayId in wayDico:
		featureNew = QgsFeature()
		featureNew.setFields(layerOsm.fields())
		featureNew['osm_id'] = wayId
		featureNew.setGeometry(QgsGeometry.fromMultiPolylineXY([wayDico[wayId]]))
		layerOsm.addFeature(featureNew)
	
	layerOsm.commitChanges()	
	
	mainFrame.setStatusWorking(codeTrack + ' - OSM relation ' + osmRelation + ' : Couche créée = ' + layerNameOsm)
	TDAT.sleep(250)	

#	Calcul de la distance de Hausdorff

	try:
		geometryGR = mainFrame.dicoTracksGRFeatures[codeTrack].geometry()
		geometryOSM = QgsGeometry.fromMultiPolylineXY([wayDico[way] for way in wayDico])
		hausdorffDistance = geometryGR.hausdorffDistance(geometryOSM)
	except:
		hausdorffDistance = None

# 	Bye bye ...
	
	endTime = time.time()
	workingTime = int(endTime - startTime)
	mainFrame.setStatusDone(codeTrack + ' - OSM relation ' + osmRelation + ' : Couche ' + layerNameOsm + ' créée (' + str(workingTime) + ' s)')

	return hausdorffDistance

		
# ========================================================================================
# Creation des couches shape pour une emprise carte
# >>> iface
# >>> mainFrame
# >>> pathOsm			: str				Path du fichier Osm
# >>> fileOsm			: str				Fichier Osm
# ========================================================================================

class createMapShapesTask:

	def __init__(self, iface, mainFrame, pathOsm, fileOsm, mapGeometry):
		self.iface = iface
		self.mainFrame = mainFrame
		self.pathOsm = pathOsm
		self.fileOsm = fileOsm
		self.mapGeometry = mapGeometry
		self.mapRectangle = mapGeometry.boundingBox()

		self.dockWindow = controlOSMGenerationWindow(self.iface, self)
		self.mainFrame.setStatusWorking('Création de la classe createMapShapesTask ...')

	def start(self):
		self.startTime = time.time()
		self.taskOsm = QgsTask.fromFunction('Création des Couches Osm', self.createMapShapesTask, on_finished=self.createMapShapesTaskCompleted)
		QgsApplication.taskManager().addTask(self.taskOsm)
		self.taskOsm.progressChanged.connect(self.progress)
		self.taskOsm.taskTerminated.connect(self.terminated)
		self.mainFrame.setStatusInfo('La création des couches Osm est longue et se déroule dans une tache de fond ...')
		return self.taskOsm

	def terminated(self):
		self.dockWindow.setStatusError('Une erreur s\'est produite !')
		QgsApplication.processEvents()

	def stopRequested(self):
		self.dockWindow.setStatusError('STOP demandé !')
		try:
			self.taskOsm.cancel()
		except:
			pass
		time.sleep(2)
		try:			
			self.dockWindow.deleteLater() 
			self.dockWindow.close()
			del self.dockWindow
		except:
			pass


	def createMapShapesTaskCompleted(self, exception):
		if exception == None :
			self.dockWindow.deleteLater() 
			self.dockWindow.close()
			del self.dockWindow
		else :
			print('class createMapShapesTask : Error')
			print('Exception: {}'.format(exception))
			traceback.print_exc() 
			

	def createMapShapesTask(self, task):
		self.osmParseFile(task)
		time.sleep(1)
		self.osmCreatePointDictionary(task)
		time.sleep(1)
		self.osmCreatePointLayers(task)
		time.sleep(1)
		self.osmCreateLineDictionary(task)
		time.sleep(1)
		self.osmCreateLineLayers(task)
		time.sleep(1)
		self.osmCreateAreaLayers(task)
		time.sleep(1)
		self.osmCreateRandoDictionary(task)
		time.sleep(1)
		self.osmCreateRandoLayers(task)
		time.sleep(5)
		
		
		

		task.setProgress(100)
	
	def addLayersToCanevas(self, dicoLayers):
		styleDico = { coucheInfo[QGP.configLayerIndexName] : coucheInfo[QGP.configLayerIndexStyle] for coucheInfo in QGP.configOsmLayers }
		groupName = QGP.configActiveMapOsmGroupName
	
		for layerName in dicoLayers:
			layer = dicoLayers[layerName]
			crs = layer.crs()															# Set CRS																
			crs.createFromId(3812)  			
			layer.setCrs(crs)		
			layer.commitChanges()														# Commit changes already done
			layer.loadNamedStyle(QGP.configOsmStylesStandard + styleDico[layerName])	# Apply standard style
			QgsProject.instance().addMapLayer(layer, False)												
			TLAY.findGroup(groupName)[0].addLayer(layer)
	
		TLAY.foldLayersGroup(groupName)
	
	
	
# ========================================================================================
# ========================================================================================
#
# Gestion de l'avancement 
#
# ========================================================================================
# ========================================================================================
	
	def progress(self, value):
		workingTime = int(time.time() - self.startTime)
		self.dockWindow.setOsmTime(workingTime)
	
		if value == 10 :															# Values in range 10 - 19 : Parsing		
			self.dockWindow.setStatusWorking('Parsing Fichier OSM ...')
		if value == 19 :
			self.dockWindow.setNodeCount(self.nodeCount)
			self.dockWindow.setWayCount(self.wayCount)
			self.dockWindow.setRelationCount(self.relationCount)
			self.dockWindow.setStatusDone('Parsing terminé !')

		if value == 20 : 															# Values in range 20 - 29 : Points 		
			self.dockWindow.setStatusWorking('Dictionnaire des Points ...')
		if value == 21 : 															
			self.dockWindow.setStatusDone('Dico : ' + str(self.nodeTagCount) + ' points avec Tag')
		if value == 22 : 															
			self.dockWindow.setStatusWorking('Points : initialisation ...')
			self.dockWindow.setPointsNodeCount(self.nodeTagCount)
		if value == 23 : 															
			self.dockWindow.setStatusWorking('Points : création des couches ...')
		if value == 24 : 
			self.dockWindow.setStatusWorking('Points : ajout des attributs ...')
		if value == 25 : 
			self.dockWindow.setStatusWorking('Points : création des entités ...')
		if value == 26 : 
			self.dockWindow.setStatusWorking('Points créés :  ' + str(self.runningCount) + ' ...')
		if value == 27 : 
			self.dockWindow.setStatusWorking('Points créés :  ' + str(self.runningCount))
			self.dockWindow.setPointsPointCount(self.runningCount)
			self.dockWindow.setPointsLayerCount(len(self.dicoPointLayers))
		if value == 28 : 
			self.dockWindow.setStatusWorking('Points :  ajout des entités ...')
		if value == 29 : 
			self.dockWindow.setStatusWorking('Points :  ajout des couches sur le Canevas ...')
			self.addLayersToCanevas(self.dicoPointLayers)
		if value == 29.5 : 
			self.dockWindow.setStatusDone('Points : couches ajoutées au Canevas')

		if value == 30 : 															# Values in range 30 - 39 : Lignes 		
			self.dockWindow.setStatusWorking('Dictionnaire des Lignes ...')
		if value == 31 : 															
			self.dockWindow.setStatusDone('Dicos Lignes : ' +  str(self.wayCount) + ' / Aires  : ' + str(self.areaCount))
		if value == 32 : 															
			self.dockWindow.setStatusWorking('Lignes : initialisation ...')
			self.dockWindow.setLinesWayCount(self.wayCount)
		if value == 33 : 															
			self.dockWindow.setStatusWorking('Lignes : création des couches ...')
		if value == 34 : 
			self.dockWindow.setStatusWorking('Lignes : ajout des attributs ...')
		if value == 35 : 
			self.dockWindow.setStatusWorking('Lignes : création des entités ...')
		if value == 36 : 
			self.dockWindow.setStatusWorking('Lignes créées :  ' + str(self.runningCount) + ' ...')
		if value == 36.5 : 
			self.dockWindow.setStatusWorking('Lignes : assemblage des lignes ...')
		if value == 37 : 
			self.dockWindow.setStatusWorking('Lignes créées :  ' + str(self.runningCount))
			self.dockWindow.setLinesLineCount(self.runningCount)
			self.dockWindow.setLinesLayerCount(len(self.dicoLineLayers))
		if value == 38 : 
			self.dockWindow.setStatusWorking('Lignes :  ajout des entités ...')
		if value == 39 : 
			self.dockWindow.setStatusWorking('Lignes :  ajout des couches sur le Canevas ...')
			self.addLayersToCanevas(self.dicoLineLayers)
		if value == 39.5 : 
			self.dockWindow.setStatusDone('Lignes : couches ajoutées au Canevas')
	
		if value == 42 : 															# Values in range 40 - 49 : Aires
			self.dockWindow.setStatusWorking('Aires : initialisation ...')
			self.dockWindow.setAreasWayCount(self.wayCount)
		if value == 43 : 															
			self.dockWindow.setStatusWorking('Aires : création des couches ...')
		if value == 44 : 
			self.dockWindow.setStatusWorking('Aires : ajout des attributs ...')
		if value == 45 : 
			self.dockWindow.setStatusWorking('Aires : création des entités ...')
		if value == 46 : 
			self.dockWindow.setStatusWorking('Aires créées :  ' + str(self.runningCount) + ' ...')
		if value == 47 : 
			self.dockWindow.setStatusWorking('Aires créées :  ' + str(self.runningCount))
			self.dockWindow.setAreasAreaCount(self.runningCount)
			self.dockWindow.setAreasLayerCount(len(self.dicoAreaLayers))
		if value == 48 : 
			self.dockWindow.setStatusWorking('Aires :  ajout des entités ...')
	
		if value == 50 : 															# Values in range 50 - 59 : Aires Complexes 		
			self.dockWindow.setStatusWorking('Dictionnaire des Aires Complexes ...')
		if value == 50.5 :
			self.dockWindow.setStatusWorking('Aires créées :  ' + str(self.runningCount) + ' ...')
		if value == 51 : 															
			self.dockWindow.setStatusDone('Dicos Aires : ' +  str(self.wayCount) + ' / Aires  : ' + str(self.areaCount))
			self.dockWindow.setComplexGeoCount(self.runningCount)
		if value == 55 : 
			self.dockWindow.setStatusWorking('Aires Complexes : création des entités ...')
		if value == 56 : 
			self.dockWindow.setStatusWorking('Aires Complexes créées :  ' + str(self.runningCount) + ' ...')
		if value == 57 : 
			self.dockWindow.setStatusWorking('Aires Complexes créées :  ' + str(self.runningCount))
			self.dockWindow.setComplexAreaCount(self.runningCount)
			self.dockWindow.setComplexLayerCount(len(self.dicoAreaLayers))
		if value == 58 : 
			self.dockWindow.setStatusWorking('Aires :  ajout des entités ...')
		if value == 59 : 
			self.dockWindow.setStatusWorking('Aires :  ajout des couches sur le Canevas ...')
			self.addLayersToCanevas(self.dicoAreaLayers)
		if value == 59.5 : 
			self.dockWindow.setStatusDone('Aires : couches ajoutées au Canevas')

		if value == 60 : 															# Values in range 60 - 69 : Routes 		
			self.dockWindow.setStatusWorking('Dictionnaire des Routes ...')
		if value == 61 : 															
			self.dockWindow.setStatusDone('Dico : ' + str(self.routeCount) + ' routes')
		if value == 62 : 															
			self.dockWindow.setStatusWorking('Routes : initialisation ...')
			self.dockWindow.setAreasWayCount(self.routeCount)
		if value == 63 : 															
			self.dockWindow.setStatusWorking('Routes : création des couches ...')
		if value == 64 : 
			self.dockWindow.setStatusWorking('Routes : ajout des attributs ...')
		if value == 65 : 
			self.dockWindow.setStatusWorking('Routes : création des entités ...')
		if value == 66 : 
			self.dockWindow.setStatusWorking('Routes créées :  ' + str(self.runningCount) + ' ...')
		if value == 67 : 
			self.dockWindow.setStatusWorking('Routes créées :  ' + str(self.runningCount))
			self.dockWindow.setRandosRouteCount(self.routeCount)
			self.dockWindow.setRandosLayerCount(len(self.dicoRouteLayers))
		if value == 68 : 
			self.dockWindow.setStatusWorking('Routes :  ajout des entités ...')
		if value == 69 : 
			self.dockWindow.setStatusWorking('Routes :  ajout des couches sur le Canevas ...')
			self.addLayersToCanevas(self.dicoRouteLayers)
		if value == 69.5 : 
			self.dockWindow.setStatusDone('Routes : couches ajoutées au Canevas')





		if value == 99 : 															# Values 90 - 99  : erreurs
			self.dockWindow.setStatusError('STOP demandé !')

		if value == 100 :															# Value 100 is terminated
			self.dockWindow.setStatusDone('Tout est terminé !')
			self.mainFrame.setStatusInfo('La création des couches Osm est terminée !')
	
		QgsApplication.processEvents()
	
	

# ========================================================================================
# ========================================================================================
#
# Fonctions de la taches en background
#
# ========================================================================================
# ========================================================================================

	
# ========================================================================================
# Parsing du fichier Osm et statistiques
# ========================================================================================
		
	def osmParseFile(self, task):
		task.setProgress(10)

		self.osmXML = parse(self.pathOsm + self.fileOsm)

		self.nodeCount = sum([1 for _ in self.osmXML.getElementsByTagName('node')])
		self.wayCount = sum([1 for _ in self.osmXML.getElementsByTagName('way')])
		self.relationCount = sum([1 for _ in self.osmXML.getElementsByTagName('relation')])

		task.setProgress(19)
			
		
# =============================================================================
# Création d'un Dictionnaire des Points
# All points are kept at this stage since points out of map may be needed for lines or areas
# =============================================================================

	def osmCreatePointDictionary(self, task) :
		task.setProgress(20)

		crs3812 = QgsCoordinateReferenceSystem("EPSG:3812")
		crs4326 = QgsCoordinateReferenceSystem("EPSG:4326")
	
		coordinateTransform = QgsCoordinateTransform()
		coordinateTransform.setSourceCrs(crs4326)
		coordinateTransform.setDestinationCrs(crs3812)

		self.dicoNoeuds = {}
		self.nodeTagCount = 0

		for node in self.osmXML.getElementsByTagName('node'):
			id = node.getAttribute("id")
			lat = node.getAttribute("lat")
			lon = node.getAttribute("lon")
			pXY =  QgsPointXY(float(lon),float(lat))
			pXY = coordinateTransform.transform(pXY)
			self.dicoNoeuds[id] = pXY
			if (node.hasChildNodes()):	self.nodeTagCount += 1
			QgsApplication.processEvents()

		task.setProgress(21)
		
		
# =============================================================================
# Création des couches de type Point
# =============================================================================
		
	def osmCreatePointLayers(self, task) :

#	Informations sur les couches

		task.setProgress(22)
		layerInfoList = [coucheInfo for coucheInfo in QGP.configOsmLayers if coucheInfo[QGP.configLayerIndexType] == 'Points']
		dicoLayersTags = { coucheInfo[QGP.configLayerIndexName] : coucheInfo[QGP.configLayerIndexTags:] for coucheInfo in layerInfoList }
		time.sleep(0.5)

#	Création des couches	

		task.setProgress(23)
		self.dicoPointLayers = { coucheInfo[QGP.configLayerIndexName] : QgsVectorLayer('Point', coucheInfo[QGP.configLayerIndexName], 'memory') for coucheInfo in layerInfoList }
		time.sleep(0.5)
		
#	Ajout des attributs	

		task.setProgress(24)
		for layerName in self.dicoPointLayers:
			layer = self.dicoPointLayers[layerName]
			provider = layer.dataProvider()
			layer.startEditing()
			for fieldName in QGP.configOsmIdentificationTagList + QGP.configOsmNameTagList + dicoLayersTags[layerName] :
				provider.addAttributes([QgsField(self.shortenAttributeName(fieldName), QVariant.String)])
			layer.updateFields()
#			print(	layerName + ' : ' + str([ str(_) for _ in layer.fields()]))
		time.sleep(0.5)
		
#	Création des Entités Points		
		
		task.setProgress(25)

		self.dicoNewFeaturesLists = { layerName : [] for layerName in self.dicoPointLayers }
		self.runningCount = 0

		for node in self.osmXML.getElementsByTagName('node'):
			if not node.hasChildNodes(): continue											# Node has no attribute - useless in shape
			id = node.getAttribute('id')
			if not self.mapGeometry.contains(self.dicoNoeuds[id]): continue					# Not inside map - useless in later
			self.runningCount += 1
			for layerName in self.dicoPointLayers :
				tagMatch = False
				newFeature = QgsFeature()
				newFeature.setFields(self.dicoPointLayers[layerName].fields())
				for tag in node.getElementsByTagName('tag'):
					attribute = tag.getAttribute('k')
					value = tag.getAttribute('v')
					if (attribute in dicoLayersTags[layerName]):
						tagMatch = True
						newFeature.setAttribute(self.shortenAttributeName(attribute), value)
					if (attribute in QGP.configOsmNameTagList):
						newFeature.setAttribute(self.shortenAttributeName(attribute), value)
				if (tagMatch): 
					newFeature.setAttribute('osm_id', id)
					newFeature.setAttribute('osm_type', 'node')
					geometry = QgsGeometry.fromPointXY(self.dicoNoeuds[id])
					newFeature.setGeometry(geometry)
					self.dicoNewFeaturesLists[layerName].append(newFeature)
			if ((self.runningCount % modShowPoint) == 0): task.setProgress(26)

		task.setProgress(27)
		time.sleep(0.5)
		
#	Ajouter les entités aux couches	

		task.setProgress(28)
		for layerName in self.dicoPointLayers :
			layer = self.dicoPointLayers[layerName]
			layer.addFeatures(self.dicoNewFeaturesLists[layerName], QgsFeatureSink.FastInsert)
		time.sleep(0.5)
		
#	Ajout des couches sur le canevas - Cannot be done in task itself

		task.setProgress(29)
		time.sleep(5)
		task.setProgress(29.5)
		time.sleep(0.5)

			
# =============================================================================
# Création d'un Dictionnaire des Lignes
# =============================================================================

	def osmCreateLineDictionary(self, task) :
		task.setProgress(30)

		self.dicoLignes = {}
		self.dicoAires = {}

		self.areaCount = 0
		self.wayCount = 0

		for way in self.osmXML.getElementsByTagName('way'):
			id = way.getAttribute('id')
			listeSommets = []
			for point in way.getElementsByTagName('nd'):
				ref = point.getAttribute('ref')
				listeSommets.append(self.dicoNoeuds[ref])
			if (len(listeSommets) <= 1): continue
			if (listeSommets[0] == listeSommets[-1]):
				self.dicoAires[id] = listeSommets
				self.areaCount += 1
			self.dicoLignes[id] = listeSommets
			self.wayCount += 1
	
		task.setProgress(31)			
	
			
# =============================================================================
# Création des couches de type Ligne
# =============================================================================
		
	def osmCreateLineLayers(self, task) :			
			
#	Informations sur les couches

		task.setProgress(32)
		layerInfoList = [coucheInfo for coucheInfo in QGP.configOsmLayers if coucheInfo[QGP.configLayerIndexType] == 'Lignes']
		dicoLayersTags = { coucheInfo[QGP.configLayerIndexName] : coucheInfo[QGP.configLayerIndexTags:] for coucheInfo in layerInfoList }
		time.sleep(0.5)

#	Création des couches	

		task.setProgress(33)
		self.dicoLineLayers = { coucheInfo[QGP.configLayerIndexName] : QgsVectorLayer('MultiLineString', coucheInfo[QGP.configLayerIndexName], 'memory') for coucheInfo in layerInfoList }
		time.sleep(0.5)
		
#	Ajout des attributs	

		task.setProgress(34)
		for layerName in self.dicoLineLayers:
			layer = self.dicoLineLayers[layerName]
			provider = layer.dataProvider()
			layer.startEditing()
			for fieldName in QGP.configOsmIdentificationTagList + QGP.configOsmNameTagList + dicoLayersTags[layerName] :
				provider.addAttributes([QgsField(self.shortenAttributeName(fieldName), QVariant.String)])
			layer.updateFields()
#			print(	layerName + ' : ' + str([ str(_) for _ in layer.fields()]))
		time.sleep(0.5)
		
#	Création des Entités Lignes		
		
		task.setProgress(35)	

		self.dicoNewFeaturesLists = { layerName : [] for layerName in self.dicoLineLayers }
		self.runningCount = 0

		for way in self.osmXML.getElementsByTagName('way'):
			id = way.getAttribute('id')
			geometry = QgsGeometry.fromPolylineXY(self.dicoLignes[id])
			if not geometry.boundingBoxIntersects(self.mapRectangle): continue			# Not inside map - useless in shape
			self.runningCount += 1
			for layerName in self.dicoLineLayers :
				tagMatch = False
				newFeature = QgsFeature()
				newFeature.setFields(self.dicoLineLayers[layerName].fields())
				for tag in way.getElementsByTagName('tag'):
					attribute = tag.getAttribute('k')
					value = tag.getAttribute('v')
					if attribute in dicoLayersTags[layerName]:
						tagMatch = True
						newFeature.setAttribute(self.shortenAttributeName(attribute), value)
					if attribute in QGP.configOsmNameTagList:
						newFeature.setAttribute(self.shortenAttributeName(attribute), value)
				if (tagMatch): 
					newFeature.setAttribute('osm_id', id)
					newFeature.setAttribute('osm_type', 'way')
					newFeature.setGeometry(geometry)
					self.dicoNewFeaturesLists[layerName].append(newFeature)
			if ((self.runningCount % modShowLine) == 0): task.setProgress(36)

# 	Assembler les lignes contigues si les attributs sont identiques
	
		task.setProgress(36.5)

		for layerName in self.dicoLineLayers :
			featureList = self.dicoNewFeaturesLists[layerName] 
			for mergingNumA in range(len(featureList) - 1) :						# Number of feature merging so far // -1 because single last cannot be merged
				if mergingNumA >= len(featureList) - 1 : break							# Must be retested since lenght changes when poping below
				featureA = featureList[mergingNumA]										# Feature A will be tested with other features for merging
				attributesA = featureA.attributes()
				lineA = featureA.geometry().asPolyline()
				for mergingNumB in range(len(featureList)-1,mergingNumA,-1):			# For all remaining features - reverse order because features will be removed
					featureB = featureList[mergingNumB]										# Feature B candidate for merging
					attributesB = featureB.attributes()
					if attributesA[1:] != attributesB[1:]: continue							# Reject if attributes are not identical - attribute 0 is OsmId is excluded
					lineB = featureB.geometry().asPolyline()
					if lineA[-1] == lineB[0]:																# A > B
						lineA = lineA + lineB[1:] ; merging = True
					elif lineA[-1] == lineB[-1]:															# A > B reversed
						lineB.reverse() ; lineA = lineA + lineB[1:] ; merging = True
					elif lineA[0] == lineB[-1]:																# B > A
						lineA = lineB + lineA[1:] ; merging = True
					elif lineA[0] == lineB[0]:																# B reversed > A
						lineB.reverse() ; lineA = lineB + lineA[1:] ; merging = True
					else:
						merging = False
					if merging:
						featureA.setGeometry(QgsGeometry.fromPolylineXY(lineA))
						featureList.pop(mergingNumB)
				task.setProgress(36.5)

		task.setProgress(37)
		time.sleep(0.5)

#	Ajouter les entités aux couches	

		task.setProgress(38)
		for layerName in self.dicoLineLayers :
			layer = self.dicoLineLayers[layerName]
			layer.addFeatures(self.dicoNewFeaturesLists[layerName], QgsFeatureSink.FastInsert)
		time.sleep(0.5)
		
#	Ajout des couches sur le canevas - Cannot be done in task itself

		task.setProgress(39)
		time.sleep(5)
		task.setProgress(39.5)
		time.sleep(0.5)


# =============================================================================
# Création des couches de type Aire
# =============================================================================
		
	def osmCreateAreaLayers(self, task) :			
			
#	Informations sur les couches

		task.setProgress(42)
		layerInfoList = [coucheInfo for coucheInfo in QGP.configOsmLayers if coucheInfo[QGP.configLayerIndexType] == 'Aires']
		dicoLayersTags = { coucheInfo[QGP.configLayerIndexName] : coucheInfo[QGP.configLayerIndexTags:] for coucheInfo in layerInfoList }
		time.sleep(0.5)

#	Création des couches	

		task.setProgress(43)
		self.dicoAreaLayers = { coucheInfo[QGP.configLayerIndexName] : QgsVectorLayer('MultiPolygon', coucheInfo[QGP.configLayerIndexName], 'memory') for coucheInfo in layerInfoList }
		time.sleep(0.5)
		
#	Ajout des attributs	

		task.setProgress(44)
		for layerName in self.dicoAreaLayers:
			layer = self.dicoAreaLayers[layerName]
			provider = layer.dataProvider()
			layer.startEditing()
			for fieldName in QGP.configOsmIdentificationTagList + QGP.configOsmNameTagList + dicoLayersTags[layerName] :
				provider.addAttributes([QgsField(self.shortenAttributeName(fieldName), QVariant.String)])
			layer.updateFields()
		time.sleep(0.5)
		
#	Création des Entités Aires		
		
		task.setProgress(45)	

		self.dicoNewFeaturesLists = { layerName : [] for layerName in self.dicoAreaLayers }
		self.runningCount = 0		

		for way in self.osmXML.getElementsByTagName('way'):
			id = way.getAttribute('id')
			if (id not in self.dicoAires): continue
			geometry =  QgsGeometry.fromPolygonXY([self.dicoAires[id]])
			if not geometry.boundingBoxIntersects(self.mapRectangle): continue			# Not inside map - useless in shape
			self.runningCount += 1
			for layerName in self.dicoAreaLayers :
				tagMatch = False
				newFeature = QgsFeature()
				newFeature.setFields(self.dicoAreaLayers[layerName].fields())
				for tag in way.getElementsByTagName('tag'):
					attribute = tag.getAttribute('k')
					value = tag.getAttribute('v')
					for special in QGP.configOsmAreaPrefixToRemove:
						if attribute[0:len(special)] == special : attribute = attribute[len(special):] ; break
					if attribute in dicoLayersTags[layerName]:
						tagMatch = True
						newFeature.setAttribute(self.shortenAttributeName(attribute), value)
					if attribute in QGP.configOsmNameTagList:
						newFeature.setAttribute(self.shortenAttributeName(attribute), value)
				if (tagMatch): 
					newFeature.setAttribute('osm_id', id)
					newFeature.setAttribute('osm_type', 'area')
					newFeature.setGeometry(geometry)
					self.dicoNewFeaturesLists[layerName].append(newFeature)
			if ((self.runningCount % modShowArea) == 0): task.setProgress(46)

		task.setProgress(47)
		time.sleep(0.5)

#	Ajouter les entités aux couches	

		task.setProgress(48)
		for layerName in self.dicoAreaLayers :
			layer = self.dicoAreaLayers[layerName]
			layer.addFeatures(self.dicoNewFeaturesLists[layerName], QgsFeatureSink.FastInsert)
		time.sleep(0.5)
		
# 	Création d'un Dictionnaire de toutes les géométries complexes

		task.setProgress(50)

		dicoGeometries = {}
		self.runningCount = 0		

		for relation in self.osmXML.getElementsByTagName('relation'):
			id = relation.getAttribute('id')
			outerWaysList = []
			innerWaysList = []
			for member in relation.getElementsByTagName('member'):
				type = member.getAttribute('type')
				ref = member.getAttribute('ref')
				role = member.getAttribute('role')
				if (type != 'way'): continue
				if (role == 'outer'): outerWaysList.append(self.dicoLignes[ref])
				if (role == 'inner'): innerWaysList.append(self.dicoLignes[ref])
			if (outerWaysList == []): continue
			outerPolygonList = TGEO.mergeLinesIntoPolygons(self.mainFrame.debugModeQCartoLevel, outerWaysList)
			innerPolygonList = TGEO.mergeLinesIntoPolygons(self.mainFrame.debugModeQCartoLevel, innerWaysList)
			if (outerPolygonList == []): continue
			geometry = QgsGeometry.fromMultiPolygonXY([[x] for x in outerPolygonList])
			for inner in innerPolygonList:
				status = geometry.addRing(inner)
			dicoGeometries[id] = geometry
			self.runningCount += 1
			if ((self.runningCount % modShowArea) == 0): task.setProgress(50.5)

		task.setProgress(51)

# 	Création de Toutes les Entités Aires Complexes

		task.setProgress(55)	

		self.dicoNewFeaturesLists = { layerName : [] for layerName in self.dicoAreaLayers }
		self.runningCount = 0		
	
		for relation in self.osmXML.getElementsByTagName('relation'):
			id = relation.getAttribute('id')
			if (id not in dicoGeometries): continue
			if not dicoGeometries[id].boundingBoxIntersects(self.mapRectangle): continue			# Not inside map - useless in shape
			self.runningCount += 1
			for layerName in self.dicoAreaLayers :
				tagMatch = False
				newFeature = QgsFeature()
				newFeature.setFields(self.dicoAreaLayers[layerName].fields())
				for tag in relation.getElementsByTagName('tag'):
					attribute = tag.getAttribute('k')
					value = tag.getAttribute('v')
					for special in QGP.configOsmAreaPrefixToRemove:
						if attribute[0:len(special)] == special : attribute = attribute[len(special):] ; break
					if attribute in dicoLayersTags[layerName]:
						tagMatch = True
						newFeature.setAttribute(self.shortenAttributeName(attribute), value)
					if (attribute in QGP.configOsmNameTagList):
						newFeature.setAttribute(self.shortenAttributeName(attribute), value)
				if tagMatch: 
					newFeature.setAttribute('osm_id', id)
					newFeature.setAttribute('osm_type', 'multi')
					newFeature.setGeometry(dicoGeometries[id])
					self.dicoNewFeaturesLists[layerName].append(newFeature)
			if ((self.runningCount % modShowArea) == 0): task.setProgress(56)

		task.setProgress(57)
		time.sleep(0.5)

#	Ajouter les entités aux couches	

		task.setProgress(58)
		for layerName in self.dicoAreaLayers :
			layer = self.dicoAreaLayers[layerName]
			layer.addFeatures(self.dicoNewFeaturesLists[layerName], QgsFeatureSink.FastInsert)
		time.sleep(0.5)	
	
#	Ajout des couches sur le canevas - Cannot be done in task itself

		task.setProgress(59)
		time.sleep(5)
		task.setProgress(59.5)
		time.sleep(0.5)
			

# =============================================================================
# Création d'un Dictionnaire des Randos
# =============================================================================

	def osmCreateRandoDictionary(self, task) :
		task.setProgress(60)

		self.dicoRoutes = {}
		self.routeCount = 0		
	
		for relation in self.osmXML.getElementsByTagName('relation'):
			if not any([((tag.getAttribute('k') == 'type') and (tag.getAttribute('v') == 'route')) for tag in relation.getElementsByTagName('tag')]): continue
			wayList = [self.dicoLignes[member.getAttribute('ref')] for member in relation.getElementsByTagName('member') if member.getAttribute('type') == 'way' and member.getAttribute('ref') in self.dicoLignes]
			if len(wayList) == 0: continue
			geometry = QgsGeometry.fromMultiPolylineXY(wayList)
			id = relation.getAttribute("id")
			self.dicoRoutes[id] = geometry
			self.routeCount += 1

		task.setProgress(61)


# =============================================================================
# Création des Couches de type Routes - Rando
# =============================================================================
	
	def osmCreateRandoLayers(self, task):
	
#	Informations sur les couches

		task.setProgress(62)
		layerInfoList = [coucheInfo for coucheInfo in QGP.configOsmLayers if coucheInfo[QGP.configLayerIndexType] == 'Routes']
		dicoLayersTags = { coucheInfo[QGP.configLayerIndexName] : coucheInfo[QGP.configLayerIndexTags:] for coucheInfo in layerInfoList }
		time.sleep(0.5)

#	Création des couches	

		task.setProgress(63)
		self.dicoRouteLayers = { coucheInfo[QGP.configLayerIndexName] : QgsVectorLayer('MultiLineString', coucheInfo[QGP.configLayerIndexName], 'memory') for coucheInfo in layerInfoList }
		time.sleep(0.5)
		
#	Ajout des attributs	

		task.setProgress(64)
		for layerName in self.dicoRouteLayers:
			layer = self.dicoRouteLayers[layerName]
			provider = layer.dataProvider()
			layer.startEditing()
			for fieldName in QGP.configOsmIdentificationTagList + QGP.configOsmNameTagList + dicoLayersTags[layerName] :
				provider.addAttributes([QgsField(self.shortenAttributeName(fieldName), QVariant.String)])
			layer.updateFields()
		time.sleep(0.5)

#	Création des Entités Aires		
	
		task.setProgress(65)	

		self.dicoNewFeaturesLists = { layerName : [] for layerName in self.dicoRouteLayers }
		self.runningCount = 0		

		for relation in self.osmXML.getElementsByTagName('relation'):
			id = relation.getAttribute('id')
			if (id not in self.dicoRoutes): continue
			if not any([((tag.getAttribute('k') == 'route') and (tag.getAttribute('v') == 'hiking')) for tag in relation.getElementsByTagName('tag')]): continue
			self.runningCount += 1
			for layerName in self.dicoRouteLayers :
				tagMatch = False
				newFeature = QgsFeature()
				newFeature.setFields(self.dicoRouteLayers[layerName].fields())
				for tag in relation.getElementsByTagName('tag'):
					attribute = tag.getAttribute('k')
					value = tag.getAttribute('v')
					if attribute in dicoLayersTags[layerName]:
						tagMatch = True
						newFeature.setAttribute(self.shortenAttributeName(attribute), value)
					if attribute in QGP.configOsmNameTagList:
						newFeature.setAttribute(self.shortenAttributeName(attribute), value)
				if (tagMatch): 
					newFeature.setAttribute('osm_id', id)
					newFeature.setAttribute('osm_type', 'route')
					newFeature.setGeometry(self.dicoRoutes[id])
					self.dicoNewFeaturesLists[layerName].append(newFeature)
				if ((self.runningCount % modShowRoute) == 0): task.setProgress(66)
	
		task.setProgress(67)
		time.sleep(0.5)

#	Ajouter les entités aux couches	

		task.setProgress(68)
		for layerName in self.dicoRouteLayers :
			layer = self.dicoRouteLayers[layerName]
			layer.addFeatures(self.dicoNewFeaturesLists[layerName], QgsFeatureSink.FastInsert)
		time.sleep(0.5)

#	Ajout des couches sur le canevas - Cannot be done in task itself

		task.setProgress(69)
		time.sleep(5)
		task.setProgress(69.5)
		time.sleep(0.5)
			







	
# ========================================================================================
# Raccourci un nom d'attribut - Les noms des attributs shape file sont limités à 10 caractères
# Remplace les : par _ dans les noms d'attributs
#  >>> attributeName :  str				Nom de l'attribut à raccourcir si trop long
#  <<< attributeName :  str				Shortened name if attributeName longer than 10 characters
# ========================================================================================

	def shortenAttributeName(self, attributeName):
		if (attributeName == 'trail_visibility'): return ('Ztrail_vis')
		if (attributeName == 'information'): return ('Zinfo')
		if (attributeName == 'generator:source'): return ('Zgen_src')
		if (attributeName == 'tower:type'): return ('Ztower_typ')
		if (attributeName == 'addr:housenumber'): return ('Zaddr_num')
		if (attributeName == 'admin_level'): return ('Zadmin_lev')
		if (attributeName == 'intermittent'): return ('Zinter')
		if (attributeName == 'osmc:symbol'): return ('Zosmc')

		attributeName = attributeName.replace(':','_')

		if (len(attributeName) <= 10): return (attributeName)
		return ('Z' + attributeName[0:9])
	
		
		
		
		
		
# ========================================================================================
# ========================================================================================
#
# Fenêtre de Contrôle
#
# ========================================================================================
# ========================================================================================

class controlOSMGenerationWindow:

	def __init__(self, iface, parent):

# 	Initialisation des Variables 

		self.iface = iface
		self.parent = parent

# 	Création du Dock Widget Principal			
			
		self.controlWindowWidget = QtWidgets.QDockWidget(self.iface.mainWindow())
		self.controlWindowWidget.setFeatures(QtWidgets.QDockWidget.DockWidgetClosable)
		
		self.iface.addDockWidget(Qt.RightDockWidgetArea, self.controlWindowWidget)
		self.controlWindowWidget.repaint()
		self.controlWindowWidget.show()
#		self.controlWindowWidget.setFixedWidth(200)			

# Cadre OSM File

		self.groupBoxOSM = QtWidgets.QGroupBox('Fichier Osm', self.controlWindowWidget)
		self.groupBoxOSM.setStyleSheet(DSTY.styleBox)
		DSTY.setBoxGeometryShort(self.groupBoxOSM, 1, 1, 2, 3)
		
		TBUT.createLabelBlackButton(self.groupBoxOSM, 1, 1, 'Noeuds', 'Short')
		TBUT.createLabelBlackButton(self.groupBoxOSM, 1, 2, 'Chemins', 'Short')
		TBUT.createLabelBlackButton(self.groupBoxOSM, 1, 3, 'Relations', 'Short')
		
		self.nodeCountButton = TBUT.createLabelGreenButton(self.groupBoxOSM, 2, 1, '. . .', 'Short', 'Normal')
		self.wayCountButton = TBUT.createLabelGreenButton(self.groupBoxOSM, 2, 2, '. . .', 'Short', 'Normal')
		self.relationCountButton = TBUT.createLabelGreenButton(self.groupBoxOSM, 2, 3, '. . .', 'Short', 'Normal')
			
		self.groupBoxOSM.show()
		self.groupBoxOSM.repaint()

# Cadre des Couches Points

		self.groupBoxPoints = QtWidgets.QGroupBox('Couches de Points', self.controlWindowWidget)
		self.groupBoxPoints.setStyleSheet(DSTY.styleBox)
		DSTY.setBoxGeometryShort(self.groupBoxPoints, 1, 5, 2, 3)

		TBUT.createLabelBlackButton(self.groupBoxPoints, 1, 1, 'Noeuds', 'Short')
		TBUT.createLabelBlackButton(self.groupBoxPoints, 1, 2, 'Points', 'Short')
		TBUT.createLabelBlackButton(self.groupBoxPoints, 1, 3, 'Couches', 'Short')

		self.pointsdNodeCountButton = TBUT.createLabelGreenButton(self.groupBoxPoints, 2, 1, '. . .', 'Short', 'Normal')
		self.pointsdPointCountButton = TBUT.createLabelGreenButton(self.groupBoxPoints, 2, 2, '. . .', 'Short', 'Normal')
		self.pointsdLayerCountButton = TBUT.createLabelGreenButton(self.groupBoxPoints, 2, 3, '. . .', 'Short', 'Normal')

		self.groupBoxPoints.show()
		self.groupBoxPoints.repaint()

# Cadre des Couches Lignes

		self.groupBoxLines = QtWidgets.QGroupBox('Couches de Lignes', self.controlWindowWidget)
		self.groupBoxLines.setStyleSheet(DSTY.styleBox)
		DSTY.setBoxGeometryShort(self.groupBoxLines, 1, 9, 2, 3)

		TBUT.createLabelBlackButton(self.groupBoxLines, 1, 1, 'Chemins Ouverts', 'Short')
		TBUT.createLabelBlackButton(self.groupBoxLines, 1, 2, 'Lignes', 'Short')
		TBUT.createLabelBlackButton(self.groupBoxLines, 1, 3, 'Couches', 'Short')

		self.linesWayCountButton = TBUT.createLabelGreenButton(self.groupBoxLines, 2, 1, '. . .', 'Short', 'Normal')
		self.linesdLineCountButton = TBUT.createLabelGreenButton(self.groupBoxLines, 2, 2, '. . .', 'Short', 'Normal')
		self.linesdLayerCountButton = TBUT.createLabelGreenButton(self.groupBoxLines, 2, 3, '. . .', 'Short', 'Normal')

		self.groupBoxLines.show()
		self.groupBoxLines.repaint()

# Cadre des Couches Aires

		self.groupBoxAreas = QtWidgets.QGroupBox('Couches des Aires', self.controlWindowWidget)
		self.groupBoxAreas.setStyleSheet(DSTY.styleBox)
		DSTY.setBoxGeometryShort(self.groupBoxAreas, 1, 13, 2, 3)

		TBUT.createLabelBlackButton(self.groupBoxAreas, 1, 1, 'Chemins Fermés', 'Short')
		TBUT.createLabelBlackButton(self.groupBoxAreas, 1, 2, 'Aires', 'Short')
		TBUT.createLabelBlackButton(self.groupBoxAreas, 1, 3, 'Couches', 'Short')

		self.areasWayCountButton = TBUT.createLabelGreenButton(self.groupBoxAreas, 2, 1, '. . .', 'Short', 'Normal')
		self.areasAreaCountButton = TBUT.createLabelGreenButton(self.groupBoxAreas, 2, 2, '. . .', 'Short', 'Normal')
		self.areasdLayerCountButton = TBUT.createLabelGreenButton(self.groupBoxAreas, 2, 3, '. . .', 'Short', 'Normal')

		self.groupBoxAreas.show()
		self.groupBoxAreas.repaint()

# Cadre des Couches Aires Complexes

		self.groupBoxAreasComplex = QtWidgets.QGroupBox('Couches des Aires Complexes', self.controlWindowWidget)
		self.groupBoxAreasComplex.setStyleSheet(DSTY.styleBox)
		DSTY.setBoxGeometryShort(self.groupBoxAreasComplex, 1, 17, 2, 3)

		TBUT.createLabelBlackButton(self.groupBoxAreasComplex, 1, 1, 'Aires Complexes', 'Short')
		TBUT.createLabelBlackButton(self.groupBoxAreasComplex, 1, 2, 'Aires', 'Short')
		TBUT.createLabelBlackButton(self.groupBoxAreasComplex, 1, 3, 'Couches', 'Short')

		self.complexGeoCountButton = TBUT.createLabelGreenButton(self.groupBoxAreasComplex, 2, 1, '. . .', 'Short', 'Normal')
		self.complexAreaCountButton = TBUT.createLabelGreenButton(self.groupBoxAreasComplex, 2, 2, '. . .', 'Short', 'Normal')
		self.complexLayerCountButton = TBUT.createLabelGreenButton(self.groupBoxAreasComplex, 2, 3, '. . .', 'Short', 'Normal')

		self.groupBoxAreasComplex.show()
		self.groupBoxAreasComplex.repaint()

# Cadre des Couches Routes

		self.groupBoxRoutes = QtWidgets.QGroupBox('Couches des Routes', self.controlWindowWidget)
		self.groupBoxRoutes.setStyleSheet(DSTY.styleBox)
		DSTY.setBoxGeometryShort(self.groupBoxRoutes, 1, 21, 2, 3)

		TBUT.createLabelBlackButton(self.groupBoxRoutes, 1, 1, 'Relations Route', 'Short')
		TBUT.createLabelBlackButton(self.groupBoxRoutes, 1, 2, 'Routes Rando', 'Short')
		TBUT.createLabelBlackButton(self.groupBoxRoutes, 1, 3, 'Couches', 'Short')

		self.randosRelationCountButton = TBUT.createLabelGreenButton(self.groupBoxRoutes, 2, 1, '. . .', 'Short', 'Normal')
		self.randosRouteCountButton = TBUT.createLabelGreenButton(self.groupBoxRoutes, 2, 2, '. . .', 'Short', 'Normal')
		self.randosLayerCountButton = TBUT.createLabelGreenButton(self.groupBoxRoutes, 2, 3, '. . .', 'Short', 'Normal')

		self.groupBoxRoutes.show()
		self.groupBoxRoutes.repaint()


# Cadre Contrôles : Timing + Stop Button

		self.groupBoxControl = QtWidgets.QGroupBox('Contrôles', self.controlWindowWidget)
		self.groupBoxControl.setStyleSheet(DSTY.styleBox)

		self.timeLabel = TBUT.createLabelGreenButton(self.groupBoxControl, 1, 1, '. . .', 'Short')
		self.stopButton = TBUT.createActionButton(self.groupBoxControl, 2, 1, 'STOP', 'Short')	
		DSTY.setStyleWarningButton(self.stopButton)
		self.stopButton.clicked.connect(self.stopRequest)
		
		DSTY.setBoxGeometryShort(self.groupBoxControl, 1, 25, 2, 1)
		self.groupBoxControl.show()
		self.groupBoxControl.repaint()

# Cadre Status

		self.groupBoxStatus = QtWidgets.QGroupBox('Statut', self.controlWindowWidget)
		self.groupBoxStatus.setStyleSheet(DSTY.styleBox)
		DSTY.setBoxGeometryShort(self.groupBoxStatus, 1, 27, 2, 1)

		self.labelStatus = QtWidgets.QLabel(self.groupBoxStatus)
		DSTY.setStatusLabel(self.labelStatus, 2, 'Short')

		self.groupBoxStatus.show()
		self.groupBoxStatus.repaint()




# ----------------------------------------------------------
# Cadre Couches OSM
# ----------------------------------------------------------
#
#		self.groupBoxOSMLayers = QtWidgets.QGroupBox('Couches OSM : ', self.controlWindowWidget)
#		self.groupBoxOSMLayers.setStyleSheet(DSTY.styleBox)
#		DSTY.setBoxGeometryShort(self.groupBoxOSMLayers, 1, 3, 6, 6)
#		




# ========================================================================================
# Action : Button STOP pressed
# ========================================================================================

	def stopRequest(self):
		self.parent.stopRequested()
 	

# ========================================================================================
# Set OSM Info functions
# ========================================================================================

	def setOsmTime(self, count):
		self.timeLabel.setText(DSTY.textFormatBlackSmall.replace('%TEXT%','{:d} sec'.format(count)))

	def setNodeCount(self, count):
		self.nodeCountButton.setText(DSTY.textFormatBlackSmall.replace('%TEXT%','{:d}'.format(count)))

	def setWayCount(self, count):
		self.wayCountButton.setText(DSTY.textFormatBlackSmall.replace('%TEXT%','{:d}'.format(count)))

	def setRelationCount(self, count):
		self.relationCountButton.setText(DSTY.textFormatBlackSmall.replace('%TEXT%','{:d}'.format(count)))

	def setPointsNodeCount(self, count):
		self.pointsdNodeCountButton.setText(DSTY.textFormatBlackSmall.replace('%TEXT%','{:d}'.format(count)))

	def setPointsPointCount(self, count):
		self.pointsdPointCountButton.setText(DSTY.textFormatBlackSmall.replace('%TEXT%','{:d}'.format(count)))

	def setPointsLayerCount(self, count):
		self.pointsdLayerCountButton.setText(DSTY.textFormatBlackSmall.replace('%TEXT%','{:d}'.format(count)))

	def setLinesWayCount(self, count):
		self.linesWayCountButton.setText(DSTY.textFormatBlackSmall.replace('%TEXT%','{:d}'.format(count)))

	def setLinesLineCount(self, count):
		self.linesdLineCountButton.setText(DSTY.textFormatBlackSmall.replace('%TEXT%','{:d}'.format(count)))

	def setLinesLayerCount(self, count):
		self.linesdLayerCountButton.setText(DSTY.textFormatBlackSmall.replace('%TEXT%','{:d}'.format(count)))

	def setAreasWayCount(self, count):
		self.areasWayCountButton.setText(DSTY.textFormatBlackSmall.replace('%TEXT%','{:d}'.format(count)))

	def setAreasAreaCount(self, count):
		self.areasAreaCountButton.setText(DSTY.textFormatBlackSmall.replace('%TEXT%','{:d}'.format(count)))

	def setAreasLayerCount(self, count):
		self.areasdLayerCountButton.setText(DSTY.textFormatBlackSmall.replace('%TEXT%','{:d}'.format(count)))

	def setComplexGeoCount(self, count):
		self.complexGeoCountButton.setText(DSTY.textFormatBlackSmall.replace('%TEXT%','{:d}'.format(count)))

	def setComplexAreaCount(self, count):
		self.complexAreaCountButton.setText(DSTY.textFormatBlackSmall.replace('%TEXT%','{:d}'.format(count)))

	def setComplexLayerCount(self, count):
		self.complexLayerCountButton.setText(DSTY.textFormatBlackSmall.replace('%TEXT%','{:d}'.format(count)))
		
	def setRandosRelationCount(self, count):
		self.randosRelationCountButton.setText(DSTY.textFormatBlackSmall.replace('%TEXT%','{:d}'.format(count)))
	
	def setRandosRouteCount(self, count):
		self.randosRouteCountButton.setText(DSTY.textFormatBlackSmall.replace('%TEXT%','{:d}'.format(count)))
	
	def setRandosLayerCount(self, count):
		self.randosLayerCountButton.setText(DSTY.textFormatBlackSmall.replace('%TEXT%','{:d}'.format(count)))
		

#		SGRCarto_MenusButtons.createLabelBlackButton(self.groupBoxOSMLayers, 1, 6, 'Relations GR', 'Short')
#		SGRCarto_MenusButtons.createLabelBlackButton(self.groupBoxOSMLayers, 3, 6, 'Tracés GR', 'Short')
#		SGRCarto_MenusButtons.createLabelBlackButton(self.groupBoxOSMLayers, 5, 6, 'Couches', 'Short')
#
#		self.tracesRelationCountButton = SGRCarto_MenusButtons.createLabelGreenButton(self.groupBoxOSMLayers, 2, 6, '. . .', 'Short', 'Normal')
#		self.tracesRouteCountButton = SGRCarto_MenusButtons.createLabelGreenButton(self.groupBoxOSMLayers, 4, 6, '. . .', 'Short', 'Normal')
#		self.tracesLayerCountButton = SGRCarto_MenusButtons.createLabelGreenButton(self.groupBoxOSMLayers, 6, 6, '. . .', 'Short', 'Normal')
#
#		self.groupBoxOSMLayers.show()
#		self.groupBoxOSMLayers.repaint()
#








	def setOsmFilename(self, text):
		self.groupBoxOSM.setTitle('Fichier OSM : ' + text)
				












	def setTracesRelationCount(self, count):
		self.tracesRelationCountButton.setText(DSTY.textFormatBlackSmall.replace('%TEXT%','{:d}'.format(count)))
	
	def setTracesRouteCount(self, count):
		self.tracesRouteCountButton.setText(DSTY.textFormatBlackSmall.replace('%TEXT%','{:d}'.format(count)))
	
	def setTracesLayerCount(self, count):
		self.tracesLayerCountButton.setText(DSTY.textFormatBlackSmall.replace('%TEXT%','{:d}'.format(count)))

# ========================================================================================
# Set Status Functions
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
		
		
# ========================================================================================
# --- THE END ---
# ========================================================================================
		
		
		
		
# ========================================================================================
# --- THE END ---
# ========================================================================================
