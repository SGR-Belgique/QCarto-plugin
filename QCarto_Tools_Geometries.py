# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Utilitaires pour la Gestion des Geometries
# ========================================================================================

from qgis.core import *
from qgis.gui import *


import QCarto_Parameters_Global
QGP = QCarto_Parameters_Global.globalParameters()


# ========================================================================================
# Elargir un Rectangle de quelques mètres dans toutes les directions Nord Sud Est Ouest à centre inchangé
# >>> rectangle 		: QgsRectangle				Rectangle à élargir
# >>> extraMeters 		: int						Distance en mètres de l'élargissement
# <<< enlargedRectangle : QgsRectangle				Rectangle élargi
# ========================================================================================

def enlargeRectangle(rectangle, extraMeters):	

	enlargedRectangle = QgsRectangle(rectangle)
	enlargedRectangle.setXMinimum(rectangle.xMinimum() - extraMeters)
	enlargedRectangle.setXMaximum(rectangle.xMaximum() + extraMeters)
	enlargedRectangle.setYMinimum(rectangle.yMinimum() - extraMeters)
	enlargedRectangle.setYMaximum(rectangle.yMaximum() + extraMeters)

	return(enlargedRectangle)


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
# Regrouper les Lignes en Polygones
# >>> debugLevel : int 
# >>> waysList 	: multiPolyline			Liste de lignes (chaque ligne est une liste de points)
# <<< return   	: multiPlyGon			Liste de polygones fermés 
# ========================================================================================

def mergeLinesIntoPolygons(debugLevel, waysList):

	openWaysList = []
	polygonsList = []

	for way in waysList:
		if (way[0] == way[-1]):
			polygonsList.append(way)
			if debugLevel >= 2 : print('--- mergeLinesIntoPolygons : Closed Way found')
		else:
			openWaysList.append(way)

	while (len(openWaysList) > 0):
		if debugLevel >= 3 : print('------ Way 0 : ' + str(openWaysList[0][0]) + ' >>> ' + str(openWaysList[0][-1]) + ' [' + str(len(openWaysList[0])) + ']')
		merged = False
		startPoint = openWaysList[0][0]
		for numWay in range(1, len(openWaysList)):
			if (startPoint == openWaysList[numWay][0]):
				if debugLevel >= 3 : print('------ Way ' + str(numWay) + ' : ' + str(openWaysList[numWay][0]) + ' >>> ' + str(openWaysList[numWay][-1]) + ' [' + str(len(openWaysList[numWay])) + ']')
				newWay = openWaysList[numWay][:0:-1] + openWaysList[0]
				if debugLevel >= 3 : print('------ newWay : ' + str(newWay[0]) + ' >>> ' + str(newWay[-1]) + ' [' + str(len(newWay)) + ']')
				if (newWay[0] == newWay[-1]):
					polygonsList.append(newWay)
					del openWaysList[numWay]
					del openWaysList[0]
					if debugLevel >= 2 : print('------ mergeLinesIntoPolygons : Closed Way by start-start created')
				else:
					openWaysList[0] = newWay
					if debugLevel >= 2 : print('------ mergeLinesIntoPolygons : Merged Way by start-start created')
					del openWaysList[numWay]
				merged = True
				break
			if (startPoint == openWaysList[numWay][-1]):
				if debugLevel >= 3 : print('------ Way ' + str(numWay) + ' : ' + str(openWaysList[numWay][0]) + ' >>> ' + str(openWaysList[numWay][-1]) + ' [' + str(len(openWaysList[numWay])) + ']')
				newWay = openWaysList[numWay] + openWaysList[0][1:]
				if debugLevel >= 3 : print('------ newWay : ' + str(newWay[0]) + ' >>> ' + str(newWay[-1]) + ' [' + str(len(newWay)) + ']')
				if (newWay[0] == newWay[-1]):
					polygonsList.append(newWay)
					del openWaysList[numWay]
					del openWaysList[0]
					if debugLevel >= 2 : print('------ mergeLinesIntoPolygons : Closed Way by start-end created')
				else:
					openWaysList[0] = newWay
					if debugLevel >= 2 : print('------ mergeLinesIntoPolygons : Merged Way by start-end created')
					del openWaysList[numWay]
				merged = True
				break
		if (not merged):
			del openWaysList[0]
			if debugLevel >= 2 : print('-?---- Way 0 : Unmergeable and deleted ')

	if debugLevel >= 2 : print('--- mergeLinesIntoPolygons : Created ' + str(len(polygonsList)) + ' polygons')
	if debugLevel >= 2 : print('--- mergeLinesIntoPolygons : out')

	return(polygonsList)
	

# ========================================================================================
# --- THE END ---
# ========================================================================================
