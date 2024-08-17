# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Script pour télécharger automatiquement un fichier .osm à partir d'un numéro de relation
# ========================================================================================

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qgis.core import *
from qgis.gui import *

import time
import importlib


import QCarto_Tools_Dates as TDAT
import QCarto_Tools_Files as TFIL
import QCarto_Tools_Geometries as TGEO


import QCarto_Parameters_Global
QGP = QCarto_Parameters_Global.globalParameters()	


# ========================================================================================
# Download d'une Relation OSM
# >>> mainFrame
# >>> codeProject		: str				Code du projet (répertoire)
# >>> codeTrack			: str				Code du tracé
# >>> osmRelation		: str				Numéro de relation Osm
# <<< fileOsm			: bool				Relation Osm - None si erreur
# ========================================================================================

def downloadRelation(mainFrame, codeProject, codeTrack, osmRelation):

# 	Welcome !

	mainFrame.setStatusWorking(codeTrack + ' - OSM relation ' + osmRelation + ' : Création de la requète Osm ...') 
	startTime = time.time()
	
# Définir le Nom du Fichier Osm

	timeStamp = TDAT.getTimeStamp()
	path = QGP.configPathOsmFiles
	path = path.replace('%PROJECT%', codeProject)
	TFIL.ensure_dir(path)
	fileOsm = codeTrack + ' - ' + osmRelation + " ("+ timeStamp + ").osm"

# Crée et exécute la Requète Osm
	
	osmRequest = OSMRequest(osmRelation, path + fileOsm, mainFrame)

	if (not osmRequest.run()): return None
	
# Bye bye ...

	endTime = time.time()
	workingTime = int(endTime - startTime)
	mainFrame.setStatusDone(codeTrack + ' - OSM relation ' + osmRelation + ' : Fichier ' + fileOsm + ' - OK ( en ' + str(workingTime) + ' s)')

	return fileOsm


# ========================================================================================
# Download d'un rectangle Carte
# >>> mainFrame
# >>> codeProject		: str				Code du projet (répertoire)
# >>> mapFeature		: str				Feature Map de la couche des emprises
# <<< fileOsm			: bool				Relation Osm - None si erreur
# ========================================================================================

def downloadMapArea(mainFrame, codeProject, mapFeature):

# 	Welcome !

	mainFrame.setStatusWorking(codeProject + ' Création de la requète Osm ...') 
	startTime = time.time()
	
#	Retrouver Itinéraire et Nom Carte	
	
	mapItinerary = mapFeature[QGP.tableFramesFieldItineraryCode]
	mapName = mapFeature[QGP.tableFramesFieldName]
	mapGeometry = mapFeature.geometry()
		
# Définir le Nom du Fichier Osm

	timeStamp = TDAT.getTimeStamp()
	path = QGP.configPathOsmFiles
	path = path.replace('%PROJECT%', codeProject)
	TFIL.ensure_dir(path)
	fileOsm = mapItinerary + ' - ' + mapName + " ("+ timeStamp + ").osm"
	fileOsm = TFIL.cleanFileName(fileOsm)

# Elargir le Rectangle Actif

	rectangleOsm = mapGeometry.boundingBox()
	extraMeters = QGP.configFrameOsmExtraSize
	rectangleOsm = TGEO.enlargeRectangle(rectangleOsm, extraMeters)

# Convertir le Rectangle en WGS 84
	
	crsMap = QgsCoordinateReferenceSystem("EPSG:3812")
	crsOsm = QgsCoordinateReferenceSystem("EPSG:4326")
	
	ccordinateTransform = QgsCoordinateTransform()
	ccordinateTransform.setSourceCrs(crsMap)
	ccordinateTransform.setDestinationCrs(crsOsm)
	rectangleOsmWGS84 = ccordinateTransform.transform(rectangleOsm)

# Crée et exécute la Requète Osm

	osmRequest = OSMRequest(None, path + fileOsm, mainFrame)
	osmRequest.setParameters(rectangleOsmWGS84.xMinimum(), rectangleOsmWGS84.yMinimum(), rectangleOsmWGS84.xMaximum(),rectangleOsmWGS84.yMaximum())
	
	if (not osmRequest.run()): return False
	
# Bye bye ...

	endTime = time.time()
	workingTime = int(endTime - startTime)
	mainFrame.setStatusDone('Fichier ' + fileOsm + ' - OK ( en ' + str(workingTime) + ' s)')

	return fileOsm


# ========================================================================================
# From OSMDownloader
# ========================================================================================

class OSMRequest(QRunnable):

	import urllib.request, urllib.error, urllib.parse
	from qgis.PyQt.QtCore import QObject, QSettings, pyqtSlot, QRunnable
	import time
	import sys

	def __init__(self, osmRelation, filename, mainFrame):
		super(OSMRequest, self).__init__()

		self.osmRelation = osmRelation
		self.filename = filename
		self.mainFrame = mainFrame
		if self.osmRelation != None :
			self.xmlData = '<osm-script timeout=\"60\">'
			self.xmlData += '<union>'
			self.xmlData += '<query type="relation">'
			self.xmlData += '<id-query type="relation" ref="%osmRelation%"/>'
			self.xmlData += '</query>'
			self.xmlData += '<recurse type="relation-node" into="nodes"/>'
			self.xmlData += '<recurse type="relation-way"/>'
			self.xmlData += '<recurse type="way-node"/>'
			self.xmlData += '</union>'
			self.xmlData += '<print/>'
			self.xmlData += '</osm-script>'
		else:
			self.xmlData = '<osm-script timeout=\"60\">'
			self.xmlData += '<union into=\"_\">'
			self.xmlData += '<bbox-query e=\"maxlong\" n=\"maxlat\" s=\"minlat\" w=\"minlong\"/>'
			self.xmlData += '<recurse type=\"up\"/><recurse type=\"down\"/>'
			self.xmlData += '</union><print limit=\"\" mode=\"meta\" order=\"id\"/>'
			self.xmlData += '</osm-script>'
		self.stopped = False

	def setParameters(self, minLong, minLat, maxLong, maxLat):
		self.minLong = minLong
		self.minLat = minLat
		self.maxLong = maxLong
		self.maxLat = maxLat

	def makePostFile(self):
		if self.osmRelation != None :
			xmlData = self.xmlData.replace('%osmRelation%', self.osmRelation)
		else:
			xmlData = self.xmlData.replace('maxlong', str(self.maxLong))
			xmlData = xmlData.replace('maxlat', str(self.maxLat))
			xmlData = xmlData.replace('minlong', str(self.minLong))
			xmlData = xmlData.replace('minlat', str(self.minLat))
		xmlData = xmlData.encode('utf-8')
		return xmlData

	def makeRequest(self):
		import urllib.request, urllib.error, urllib.parse
		osmUrl = 'http://overpass-api.de/api/interpreter'
		postFile = self.makePostFile()
		req = urllib.request.Request(url=osmUrl, data=postFile, headers={'Content-Type': 'application/xml'})
		return req

	def run(self):
	
		import urllib.request, urllib.error, urllib.parse
		import importlib
	
		xml = self.makePostFile()
		req = self.makeRequest()
		
		if self.mainFrame.debugModeQCartoLevel >= 1 : print ('--- OsmDownloader - Request File : ' + self.filename)
		if self.mainFrame.debugModeQCartoLevel >= 1 : print ('--- OsmDownloader - Xml : ' + str(xml))
		if self.mainFrame.debugModeQCartoLevel >= 1 : print ('--- OsmDownloader - Request : ' + str(req))

		try:
			response = urllib.request.urlopen(req)
		except urllib.error.URLError as e:
			self.mainFrame.setStatusError('Urllib - Error occurred : ' + str(e.args) + ' --- Reason: ' + str(e.reason), False)
			return False
		except urllib.error.HTTPError as e:
			self.mainFrame.setStatusError('Urllib - Error occurred : ' + str(e.args) + ' --- Reason: ' + str(e.reason), False)
			return False

		local_file = open(self.filename, 'wb')

		total_size = 0; last_size = 0; block_size = 1024*8
		
		while not self.stopped:
			QgsApplication.processEvents()
			if (total_size >= (last_size + 1)):
				self.mainFrame.setStatusWorking('--- OsmDownloader - File Size = ' + '{:.2f}'.format(total_size) + ' MB ... ')
				last_size = total_size
			buffer = response.read(block_size)
			if not buffer: break

			try:
				local_file.write(buffer)
				size = len(buffer)/float(1024*1024)
				total_size += size
			except:
				local_file.close()
				self.mainFrame.setStatusError('File Write - Error occurred', False)
				return False

		local_file.close()
		self.mainFrame.setStatusWorking('--- OsmDownloader - File Size = ' + '{:.2f}'.format(total_size) + ' MB')
		TDAT.sleep(2000)

		return True
		
		
# ========================================================================================
# --- THE END ---
# ========================================================================================
