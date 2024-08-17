# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Utilitaires pour la Créer des Bornes (WP) kilométriques
# ========================================================================================

from qgis.core import *
from qgis.gui import *


# ========================================================================================
# Détermination de la liste des bornes (par exemple kilométriques) à partir du tracé
# 	- Il est possible de continuer le bornage d'un tracé précédent
#	- Les bornes sont créées à l'endroit exact par interpolation entre 2 points du tracé
#
#  >>> lineXY			: [QgsPoint] ou [QgsPointXY]	Ligne (liste de points) du tracé à borner
#  >>> markerLength		: int							Distance inter bornes, en mètres	[default = 1000]
#  >>> lastMarkerNumber : int							Numéro de la dernière borne sur le tracé (éventuel précédent)  [default = 0 pour commencer avec ce tracé et donc la borne 1]
#  >>> lastTrackLength  : float							Distance en mètres en fin de tracé précédent - [default = 0 pour commencer avec ce tracé]
#
#  <<< markerList		: [int, QgsPointXY]				Liste : Numéro de la borne et Position géographique
#  <<< lastMarkerNumber : int							Nouveau numéro de la dernière borne sur le tracé
# ========================================================================================

def generateMarkerList(lineXY, markerLength = 1000, lastMarkerNumber = 0, lastTrackLength = 0):

	markerList = []

	lastPoint = lineXY[0]
	nextMarkerNumber = lastMarkerNumber + 1
	nextMarkerLength = markerLength * nextMarkerNumber
	
	for pointNum in range(1, len(lineXY)):
		nextPoint = lineXY[pointNum]
		interDistance = nextPoint.distance(lastPoint)
		if interDistance == 0: continue
		nextTrackLength = lastTrackLength + interDistance
		if nextTrackLength >= nextMarkerLength:
			pointPositionFactor = (nextMarkerLength - lastTrackLength) / interDistance
			markerX = lastPoint.x() + (nextPoint.x() - lastPoint.x()) * pointPositionFactor
			markerY = lastPoint.y() + (nextPoint.y() - lastPoint.y()) * pointPositionFactor
			marker = [nextMarkerNumber, QgsPointXY(markerX, markerY)]
			markerList.append(marker)
			lastMarkerNumber = nextMarkerNumber
			nextMarkerNumber += 1
			nextMarkerLength += markerLength
		lastPoint = nextPoint
		lastTrackLength	= nextTrackLength
	
	return markerList, lastMarkerNumber


# ========================================================================================
# --- THE END ---
# ========================================================================================
