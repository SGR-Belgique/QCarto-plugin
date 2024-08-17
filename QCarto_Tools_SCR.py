# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Utilitaires pour la Gestion des SCR
# ========================================================================================

from qgis.core import *
from qgis.gui import *

# ========================================================================================
# Convertir un rectangle 3812 en 4 points WGS84
#
#					yMax
#	   p1 +-----------------------+ p2
#         |                       |
#    xMin |                       | xMax
#         |                       |
#	   p4 +-----------------------+ p3
#					yMin
#
# ========================================================================================

def convertRect3812toWgs84(xMin, yMin, xMax, yMax):
	
	crs3812 = QgsCoordinateReferenceSystem("EPSG:3812")
	crs4326 = QgsCoordinateReferenceSystem("EPSG:4326")
	
	coordinateTransform = QgsCoordinateTransform()
	coordinateTransform.setSourceCrs(crs3812)
	coordinateTransform.setDestinationCrs(crs4326)

	p1 = coordinateTransform.transform(xMin, yMax)
	p1Lat = p1.y()
	p1Lon = p1.x()

	p2 = coordinateTransform.transform(xMax, yMax)
	p2Lat = p2.y()
	p2Lon = p2.x()

	p3 = coordinateTransform.transform(xMax, yMin)
	p3Lat = p3.y()
	p3Lon = p3.x()

	p4 = coordinateTransform.transform(xMin, yMin)
	p4Lat = p4.y()
	p4Lon = p4.x()

	return p1Lat, p1Lon, p2Lat, p2Lon, p3Lat, p3Lon, p4Lat, p4Lon


# ========================================================================================
# Convertir un point 3812 en point WGS84
# ========================================================================================

def convertPoint3812toWgs84(x, y):
	
	crs3812 = QgsCoordinateReferenceSystem("EPSG:3812")
	crs4326 = QgsCoordinateReferenceSystem("EPSG:4326")
	
	coordinateTransform = QgsCoordinateTransform()
	coordinateTransform.setSourceCrs(crs3812)
	coordinateTransform.setDestinationCrs(crs4326)

	p = coordinateTransform.transform(x, y)
	pLat = p.y()
	pLon = p.x()

	return pLat, pLon


# ========================================================================================
# Convertir un point WGS84 en point 3812
# ========================================================================================

def convertPointWgs84to3812(pLon, pLat):
	
	crs3812 = QgsCoordinateReferenceSystem("EPSG:3812")
	crs4326 = QgsCoordinateReferenceSystem("EPSG:4326")
	
	coordinateTransform = QgsCoordinateTransform()
	coordinateTransform.setSourceCrs(crs4326)
	coordinateTransform.setDestinationCrs(crs3812)

	p = coordinateTransform.transform(pLon, pLat)

	return p.x(), p.y()


# ========================================================================================
# Convertir un point Wgs 84 en point UTM 31/32
# ========================================================================================

def convertPointWgs84toUtm(lat, lon):
	
	crs4326 = QgsCoordinateReferenceSystem("EPSG:4326")

	if (lon < 6):
		zone = 31
		crsUtm = QgsCoordinateReferenceSystem("EPSG:32631")
	else:
		zone = 32
		crsUtm = QgsCoordinateReferenceSystem("EPSG:32632")
	
	coordinateTransform = QgsCoordinateTransform()
	coordinateTransform.setSourceCrs(crs4326)
	coordinateTransform.setDestinationCrs(crsUtm)

	p = coordinateTransform.transform(lon, lat)
	pX = p.x()
	pY = p.y()

	return zone, pX, pY


# ========================================================================================
# Convertir un point 3812 en UTM Text
# ========================================================================================

def convertPoint3812toUtmText(point):
	pLat, pLon = convertPoint3812toWgs84(point.x(), point.y())
	zone, pX, pY = convertPointWgs84toUtm(pLat, pLon)
	return 'UTM {:.0f} U {:.0f} {:.0f}'.format(zone, pX, pY) 


# ========================================================================================
# Convertir une ligne de Points d'un CRS vers un autre
# >>> lineXY  : [QgsPointXY]						Ligne de points à convertir
# >>> crsIn   : QgsCoordinateReferenceSystem		CRS de lineXY
# >>> crsOut  : QgsCoordinateReferenceSystem		CRS vers lequel lineXY doit ête convertie
# <<< lineOut : [QgsPointXY]						Ligne de points convertie en crsOut
# ========================================================================================

def convertLineCrs(lineXY, crsIn, crsOut):

	coordinateTransform = QgsCoordinateTransform()
	coordinateTransform.setSourceCrs(crsIn)
	coordinateTransform.setDestinationCrs(crsOut)
	
	lineOut = [coordinateTransform.transform(P) for P in lineXY]
	
	return lineOut


# ========================================================================================
# Convertir une latitude / longitude en degres minutes secondes
# >>> latOrLong : float			Latitude / Longitude 
# <<< degres 	: int			Degrés
# <<< minutes	: int 			Minutes
# <<< secondes	: float			Secondes et décimales
# ========================================================================================

def latOrLong2DMS(latOrLong):
	degres = int(latOrLong)
	minutes = int((latOrLong - degres) * 60)
	secondes = (((latOrLong - degres) * 60) - minutes) * 60
	return degres, minutes, secondes


# ========================================================================================
# --- THE END ---
# ========================================================================================
