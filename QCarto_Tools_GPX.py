# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Utilitaires pour la Gestion des Fichiers GPX
# ========================================================================================

from qgis.core import *
from qgis.gui import *

from xml.dom.minidom import parse, parseString	

import QCarto_Tools_Altitudes as TA
import QCarto_Tools_Coding as TCOD
import QCarto_Tools_Dates as TDAT
import QCarto_Tools_Files as TFIL
import QCarto_Tools_SCR as TSCR

import QCarto_Definitions_TopoGuides as DTOP	

import QCarto_Parameters_Global
QGP = QCarto_Parameters_Global.globalParameters()


# ========================================================================================
# Définir le nom standard d'un fichier GPX
#  >>> trackCode		: str		Code du Parcours
#  >>> trackName 		: str	   	Nom du Parcours
#  >>> nomGPX			: bool		Use standard GPX short name
#  <<< trackNameGPX	 	: str		Nom du Tracé pour fichier GPX (retrocompatibilty only)
# ========================================================================================

def defineTrackNameGPX(trackCode, trackName, nomGPX) :
		
	if trackName in (None, '') : return 'Parcours-sans-nom-dans-la-table'
	if not nomGPX : return trackName	
	
	valid, type, label, zone, number, itineraryCode, trackBaseCode, trackCode, modificationList, invalidationList, repeatCount, bifurcationNumber, direction = TCOD.elementsFromGrCode(trackCode)
	trackNameGPX = trackName	

	if type in QGP.typeSetTableGR :
		if type == 'GRT':
			trackNameGPX = trackNameGPX.replace('GRT-','',1)
		if label == 'BVW':
			trackNameGPX = trackNameGPX.replace('BVW','GTPBVW', 1)
		else:	
			if label != 'TDA' : trackNameGPX = trackNameGPX.replace(' 5 ',  ' 005 ')
			trackNameGPX = trackNameGPX.replace(' 12 ', ' 012 ')
			trackNameGPX = trackNameGPX.replace(' 14 ', ' 014 ')
			trackNameGPX = trackNameGPX.replace(' 15 ', ' 015 ')
			trackNameGPX = trackNameGPX.replace(' 16 ', ' 016 ')
			trackNameGPX = trackNameGPX.replace(' 17 ', ' 017 ')
			trackNameGPX = trackNameGPX.replace(' 56 ', ' 056 ')
			trackNameGPX = trackNameGPX.replace(' 57 ', ' 057 ')
			trackNameGPX = trackNameGPX.replace('GRP ','GRP')
			trackNameGPX = trackNameGPX.replace('GR ','GR')
		trackNameGPX = trackNameGPX.replace(' - ','_',1)
		trackNameGPX = trackNameGPX.replace(' - ','-')
		trackNameGPX = trackNameGPX.replace(' de ','-')
		trackNameGPX = trackNameGPX.replace(' ','-')
		trackNameGPX = trackNameGPX.replace('Principal','principal')
		trackNameGPX = TFIL.cleanFileName(trackNameGPX)
		return trackNameGPX
		
	if type in QGP.typeSetTableRB :
		for num in list('123456789'):
			s1 = ' ' + num + ' '
			s2 = ' 0' + num + ' '
			p = trackNameGPX.find(s1)
			if (p != -1) and (p <= 7): trackNameGPX = trackNameGPX.replace(s1, s2, 1)
		trackNameGPX = trackNameGPX.replace('  ',' ')
		trackNameGPX = trackNameGPX.replace('  ',' ')
		trackNameGPX = trackNameGPX.replace('  ',' ')
		trackNameGPX = trackNameGPX.replace(trackNameGPX.split(' - ')[0],trackNameGPX.split(' - ')[0].replace(' ','-'),1)
		trackNameGPX = trackNameGPX.replace(' - ','_')
		trackNameGPX = trackNameGPX.replace(' ','-')
		trackNameGPX = trackNameGPX.replace('Via','via')
		trackNameGPX = trackNameGPX.replace('Raccourci','raccourci')
		trackNameGPX = trackNameGPX.replace('raccourcis','raccourci')
		trackNameGPX = trackNameGPX.replace('raccourci','racc')
		trackNameGPX = trackNameGPX.replace('Variante','variante')
		trackNameGPX = trackNameGPX.replace('variantes','variante')
		trackNameGPX = trackNameGPX.replace('variante','var')
		trackNameGPX = trackNameGPX.replace('Allongement','allongement')
		trackNameGPX = trackNameGPX.replace('allongements','allongement')
		trackNameGPX = trackNameGPX.replace('allongement','all')
		trackNameGPX = TFIL.cleanFileName(trackNameGPX)
		if 'T' in modificationList: trackNameGPX += '_Temporaire'
		if 'F' in modificationList: trackNameGPX += '_Futur'
		return trackNameGPX
		
	else:
		return None
		
		
# ========================================================================================
# Gérer et exporter les GPX pour SityTrail
# >>> trackFrame	: class menuTracksFrame
# >>> codeExported	: str							Code du parcours à exporter
# >>> timeStampGPX  : str							Time stamp already () enclosed
# <<< status		: bool
# ========================================================================================
	
def exportGpxSityTrail(trackFrame, codeExported, timeStampGPX) :

#	Retrouver les informations dans la table SityTrail-RB

	itineraryRB = TCOD.itineraryFromTrackCode(codeExported)								# SityTrailm Table has one entry per RB Itinerary
	if itineraryRB not in trackFrame.dicoSityTrail : return False

	codeSityTrail = trackFrame.dicoSityTrail[codeExported][QGP.tableSityFieldCodeSity]	
	titreRB = trackFrame.dicoSityTrail[itineraryRB][QGP.tableSityFieldTitre] 			
	villagesRB = trackFrame.dicoSityTrail[itineraryRB][QGP.tableSityFieldVillages]
	introRB = trackFrame.dicoSityTrail[itineraryRB][QGP.tableSityFieldIntro]		

	if codeSityTrail == None : codeSityTrail = 'XXX'
	if titreRB == None : titreRB = 'Titre non défini'
	if villagesRB == None : villagesRB = 'Villages non définis'
	if introRB == None : introRB = 'Intro non définie'

	descriptionRB = titreRB + '. ' + villagesRB + '. ' + introRB

#	Retrouver les POIs

	pointSetSityTrail = { poi[0] for poi in trackFrame.dicoTracksComputeResults[codeExported][QGP.tableTracksIFieldPOIsAll] }

#	Déterminer le path d'export

	projectCode = TCOD.projectFromTrackCode(codeExported)
	pathGPXSityTrail = QGP.configPathExportGPXSityTrail.replace('%PROJECT%', projectCode)
		
#	Déterminer le nom du fichier GPX		

	trackName = trackFrame.dicoTracksViewFeatures[codeExported][QGP.tableTracksFieldName]
	fileGPXSityTrail = DTOP.prefixGPXSityTrail + ' - ' + codeSityTrail + ' - ' + trackName + timeStampGPX + '.gpx'

#	Supprimer les anciens GPX en option				
			
	if trackFrame.optionDeleteOldGPX.isChecked(): TFIL.remove_files(pathGPXSityTrail, trackName, len(fileGPXSityTrail))
	
#	Export le GPX

	trackXYZ = trackFrame.dicoTracksComputeResults[codeExported][QGP.tableTracksIFieldTrackXYZ]
	exportGpxTrack(pathGPXSityTrail, fileGPXSityTrail, codeExported, trackName, descriptionRB, trackXYZ, set(), pointSetSityTrail)

	return True		
		
		
# ========================================================================================
# Créer le fichier Trace .gpx - Simple tracé
# >>> path				: str										Directory path where to write GPX file
# >>> file				: str										File name including .gpx
# >>> code				: str										Track code - for Basecamp color setting 
# >>> name 				: str										Track name
# >>> desc				: str										Track descrption - intro for SityTrail
# >>> track 			: [QgsPoints]								Track geometry as a QgsPoints list
# >>> pointsSet			: set of point features
# >>> poisSet			: set of poi features
# >>> comment (CMT)		: str										Comment for field <cmt> - Default = 'Copyright SGR asbl'
# ========================================================================================

def exportGpxTrack(path, file, code, name, desc, track, pointsSet, poisSet, comment = 'Copyright SGR asbl'):

# Calculer l'emprise en WGS 84
#					yMax
#	   p1 +-----------------------+ p2
#         |                       |
#    xMin |                       | xMax
#         |                       |
#	   p4 +-----------------------+ p3
#					yMin
	
	emprise3812 = QgsGeometry.fromPolyline(track).boundingBox()
	p1Lat, p1Lon, p2Lat, p2Lon, p3Lat, p3Lon, p4Lat, p4Lon = TSCR.convertRect3812toWgs84(emprise3812.xMinimum(), emprise3812.yMinimum(), emprise3812.xMaximum(), emprise3812.yMaximum())
	
# Open GPX File

	TFIL.ensure_dir(path)
	gpxFilePath = path + file
	fileOut = open(gpxFilePath, 'w', encoding='utf-8', errors='ignore')
	
# Write Header

	for line in QGP.configGPXHeaderLines: 
		fileOut.write(line + '\n')	

# Write Metadata

	timeStamp = TDAT.getTimeStamp()
	date = timeStamp[0:10]
	time = timeStamp[11:19].replace('-',':')

	for line in QGP.configGPXMetadataLines: 
		line = line.replace('%DATE%', date)
		line = line.replace('%TIME%', time)
		line = line.replace('%MINLAT%', str(min(p3Lat, p4Lat)))
		line = line.replace('%MINLONG%', str(min(p1Lon, p4Lon)))
		line = line.replace('%MAXLAT%', str(max(p1Lat, p2Lat)))
		line = line.replace('%MAXLONG%', str(max(p2Lon, p3Lon)))
		fileOut.write(line + '\n')	

# Write Waypoints

	writeWaypoints(pointsSet, fileOut)

# Write POIs

	writePOIs(poisSet, fileOut)

# Write Track Open

	name = cleanXMLText(str(name))
	desc = cleanXMLText(str(desc))

	for line in QGP.configGPXTrkOpenLines: 
		line = line.replace('%NAME%', name + ' - ' + date)
		line = line.replace('%DESC%', desc)
		line = line.replace('%CMT%', comment)
		if TCOD.isCodeLiaisonGR(code) : line = line.replace('%COLOR%', QGP.configGPXCouleurGRLiaisons)
		if TCOD.isCodeVarianteGR(code) : line = line.replace('%COLOR%', QGP.configGPXCouleurGRVariantes)
		line = line.replace('%COLOR%', QGP.configGPXCouleurGR)
		fileOut.write(line + '\n')	

# Write Segment Open 

	for line in QGP.configGPXSegOpenLines: 
		fileOut.write(line + '\n')	

# Write Track Points

	for point in track:
		alt = point.z()
		lat, lon = TSCR.convertPoint3812toWgs84(point.x(), point.y())
		for line in QGP.configTrkptLines: 
			line = line.replace('%LAT%', str(lat))
			line = line.replace('%LON%', str(lon))
			line = line.replace('%ALT%', str(alt))
			line = line.replace('%TIME%', TDAT.getGPXTimeTag())
			fileOut.write(line + '\n')	

# Write Segment Close

	for line in QGP.configGPXSegCloseLines: 
		fileOut.write(line + '\n')	

# Write Track Close

	for line in QGP.configGPXTrkCloseLines: 
		fileOut.write(line + '\n')	

# Fermer le fichier

	fileOut.close()
	
	
# ========================================================================================
# Write Waypoints in GPX
# >>> waypointsSet		: set of Point Features
# >>> fileOut
# ========================================================================================
	
def writeWaypoints(waypointsSet, fileOut):

	for point in waypointsSet:
		if not point.hasGeometry(): continue
		geometry = point.geometry().asPoint()
		lat, lon = TSCR.convertPoint3812toWgs84(geometry.x(), geometry.y())
		alt = TA.getPointXYAltitude(geometry)

		code = point[QGP.tablePointsFieldGRCode] if point[QGP.tablePointsFieldGRCode] != None else '???-??'
		repere = point[QGP.tablePointsFieldRepere] if point[QGP.tablePointsFieldRepere] != None else '??'
		nom = point[QGP.tablePointsFieldNom] if point[QGP.tablePointsFieldNom] != None else 'Pas de nom défini'
	
		name = code + '-' + repere
		desc = name + ' - ' + cleanXMLText(str(nom))

		for line in QGP.configGPXWaypointLines: 
			if '%ALT%' in line:
				if alt in (None, QGP.configAltitudeNotFound): continue
			line = line.replace('%LAT%', str(lat))
			line = line.replace('%LON%', str(lon))
			line = line.replace('%ALT%', str(round(alt,1)))
			line = line.replace('%NAME%', str(name))
			line = line.replace('%DESC%', str(desc))
			fileOut.write(line + '\n')		

	
# ========================================================================================
# Write POIs in GPX
# >>> poisSet		: set of POIs Features
# >>> fileOut
# ========================================================================================
	
def writePOIs(poisSet, fileOut):

	for poi in poisSet:
		if not poi.hasGeometry(): continue
		geometry = poi.geometry().asPoint()
		lat, lon = TSCR.convertPoint3812toWgs84(geometry.x(), geometry.y())
		alt = TA.getPointXYAltitude(geometry)

		titre = cleanXMLText(str(poi[QGP.poisTableFieldTitre]))
		texte = cleanXMLText(str(poi[QGP.poisTableFieldTexte]))	

		for line in QGP.configGPXPoiLines: 
			if '%ALT%' in line:
				if alt in (None, QGP.configAltitudeNotFound): continue
			line = line.replace('%LAT%', str(lat))
			line = line.replace('%LON%', str(lon))
			line = line.replace('%ALT%', str(round(alt,1)))
			line = line.replace('%TITLE%', str(titre))
			line = line.replace('%TEXT%', str(texte))
			fileOut.write(line + '\n')		
	
	
# ========================================================================================
# Créer le fichier Markers .gpx
# >>> path			 : str								Directory path
# >>> file			 : str								File name including .gpx
# >>> markerList     : [ [markerNum, markerPoint] ]		List of Markers
# >>> markerFormat	 : str								Text for format of marker wp name  - exemple '{:2d km}' 
# ========================================================================================

def exportGpxMarkers(path, file, markerList, markerFormat):

# Calculer l'emprise en WGS 84
#					yMax
#	   p1 +-----------------------+ p2
#         |                       |
#    xMin |                       | xMax
#         |                       |
#	   p4 +-----------------------+ p3
#					yMin
	
	xMin = yMin = -9999
	xMax = yMax = 9999
	
	for marker in markerList:
		x = marker[1].x()
		y = marker[1].y()
		if x < xMin: xMin = x 
		if x > xMax: xMax = x 
		if y < yMin: yMin = y 
		if y > yMax: yMax = y
	p1Lat, p1Lon, p2Lat, p2Lon, p3Lat, p3Lon, p4Lat, p4Lon = TSCR.convertRect3812toWgs84(xMin, yMin, xMax, yMax)
	
# Open GPX File

	TFIL.ensure_dir(path)
	gpxFilePath = path + file
	fileOut = open(gpxFilePath, 'w', encoding='utf-8', errors='ignore')
	
# Write Header

	for line in QGP.configGPXHeaderLines: 
		fileOut.write(line + '\n')	

# Write Metadata

	timeStamp = TDAT.getTimeStamp()
	date = timeStamp[0:10]
	time = timeStamp[11:19].replace('-',':')

	for line in QGP.configGPXMetadataLines: 
		line = line.replace('%DATE%', date)
		line = line.replace('%TIME%', time)
		line = line.replace('%MINLAT%', str(min(p3Lat, p4Lat)))
		line = line.replace('%MINLONG%', str(min(p1Lon, p4Lon)))
		line = line.replace('%MAXLAT%', str(max(p1Lat, p2Lat)))
		line = line.replace('%MAXLONG%', str(max(p2Lon, p3Lon)))
		fileOut.write(line + '\n')	

# Write Waypoints

	writeMarkers(markerList, markerFormat, fileOut)

# Write Gpx Close

	for line in QGP.configGPXCloseLines: 
		fileOut.write(line + '\n')	

# Fermer le fichier

	fileOut.close()

	
# ========================================================================================
# Write Markers in an open GPX file.
# >>> markerList	 : [ [markerNum, markerPoint] ]			List of Markers
# >>> markerFormat	 : str									Text for format of marker wp name  - exemple '{:2d km}' 
# >>> fileOut		 : file object							Current GPX File
# ========================================================================================
	
def writeMarkers(markerList, markerFormat, fileOut):

	for marker in markerList:
		x = marker[1].x()
		y = marker[1].y()
		lat, lon = TSCR.convertPoint3812toWgs84(x, y)
		name = markerFormat.format(marker[0])
		desc = name
		name = cleanXMLText(str(name))
		desc = cleanXMLText(str(desc))
		for line in QGP.configGPXWaypointLines: 
			if '%ALT%' in line: continue
			line = line.replace('%LAT%', str(lat))
			line = line.replace('%LON%', str(lon))
			line = line.replace('%NAME%', name)
			line = line.replace('%DESC%', desc)
			line = line.replace('%SYM%', QGP.configGPXWPCouleurKM)
			fileOut.write(line + '\n')		


# ========================================================================================
# Importer un ficher GPX et convertir le Tracé
# >>> pathFile			: str										Path complet du fichier GPX
# <<< trackLine			: [QGSPoints]								None if error
# <<< wayPointsA		: [QGSPoints]								When <desc> is 50 char max, normally a WP. None if error
# <<< wayPointsB		: [QGSPoints]								When <desc> is more than 50 char, normally a POI. None if error
# <<< errorText			: str
# ========================================================================================

def importGpxTrack(pathFile):
	
	trackLine = []
	wayPointsA = []
	wayPointsB = []
	
	try:
		gpxXML = parse(pathFile)
	except:
		return None, None, 'Le fichier GPX est mal formatté'

	for trackPoint in gpxXML.getElementsByTagName('trkpt'):
		lat = float(trackPoint.getAttribute('lat'))
		lon = float(trackPoint.getAttribute('lon'))
		px, py = TSCR.convertPointWgs84to3812(lon, lat)
		trackLine += [QgsPointXY(px, py)]
	
	for wp in gpxXML.getElementsByTagName('wpt'):
		lat = float(wp.getAttribute('lat'))
		lon = float(wp.getAttribute('lon'))
		px, py = TSCR.convertPointWgs84to3812(lon, lat)
		try:
			tag = wp.getElementsByTagName('desc')[0]
			desc = ' '.join(t.nodeValue for t in tag.childNodes if t.nodeType == t.TEXT_NODE)
		except:
			desc = ''
		if len(desc) <=50 : wayPointsA += [QgsPointXY(px, py)]
		if len(desc) > 50 : wayPointsB += [QgsPointXY(px, py)]

#	print ('wayPointsA = ' + str(len(wayPointsA)))
#	print ('wayPointsB = ' + str(len(wayPointsB)))

	return trackLine, wayPointsA, wayPointsB, None

	
# ========================================================================================
# Clean string for XML - Manage special characters & < >
# >>> text		: str						Original Text
# <<< text		: str						Text with & replaced by &amp; // < replaced by &lt; // > replaced by &gt;
# ========================================================================================

def cleanXMLText(text):

	text = text.replace('&', '&amp;')
	text = text.replace('<', '&lt;')
	text = text.replace('>', '&gt;')
	
	return text


# ========================================================================================
# --- THE END ---
# ========================================================================================
