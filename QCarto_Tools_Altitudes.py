# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Utilitaires pour la Gestion des Altitudes
# ========================================================================================

from qgis.core import *
from qgis.gui import *

import os

import QCarto_Tools_Layers as TL

import QCarto_Parameters_Global
QGP = QCarto_Parameters_Global.globalParameters()


# ========================================================================================
# Détermination de l'altitude d'un Point Lambert 2008 via le MNT Wallonie et sinon trouvé, via MNT Copernicus
#  >>> pointXY  : QgsPointXY						Point source pour lequel l'altitude doit être déterminée
#  <<< altitude : float								Altitude en mètres
#				: None 								Si le MNT n'est pas sur le Canevas Qgis
#				: -9999 							Si le point n'est pas dans le MNT
# ========================================================================================

def getPointXYAltitude(pointXY):

	crs3812 = QgsCoordinateReferenceSystem()
	crs3812.createFromString("EPSG:3812")

	pointAltitudeA = getPointXYAltitudeFromMNT(pointXY, crs3812, QGP.configMntShapesList[0])
	if (pointAltitudeA != None): 
		if (pointAltitudeA != QGP.configAltitudeNotFound):
			return pointAltitudeA

	pointAltitudeB = getPointXYAltitudeFromMNT(pointXY, crs3812, QGP.configMntShapesList[1])
	return pointAltitudeB


# ========================================================================================
# Détermination de l'altitude d'un Point via un MNT particulier
#  >>> pointXY  : QgsPointXY						Point source pour lequel l'altitude doit être déterminée
#  >>> pointCrs : QgsCoordinateReferenceSystem 		Crs des coordonnées du Point source
#  >>> mntName  : str 								Nom de la Couche MNT sur le Canevas Qgis dans le groupe 'Carto - Altitudes'
#  <<< altitude : float								Altitude en mètres
#				: None 								Si le MNT n'est pas sur le Canevas Qgis
#				: -9999 							Si le point n'est pas dans le MNT
# ========================================================================================

def getPointXYAltitudeFromMNT(pointXY, pointCrs, mntName):

	groupName = QGP.configMntGroupName
	mntShape, error = TL.findLayerInGroup(groupName, mntName)
	if error != None: return None

	crsTransform = QgsCoordinateTransform()
	crsTransform.setSourceCrs(pointCrs)
	crsTransform.setDestinationCrs(QgsCoordinateReferenceSystem(QGP.configMntShapesCrs[mntName]))

	altitude = mntShape.dataProvider().sample(crsTransform.transform(pointXY), 1)

	if (altitude[1]): return(altitude[0])
	else : return QGP.configAltitudeNotFound


# ========================================================================================
# Ajout des Altitudes sur une Ligne de Points via un MNT particulier
#  >>> lineXY 	: [QgsPointXY]						Ligne (liste de points) pour laquelle l'altitude doit être déterminée
#  >>> lineCrs  : QgsCoordinateReferenceSystem 		Crs des coordonnées des points de la ligne lineXY
#  >>> mntName  : str 								Nom de la Couche MNT sur le Canevas Qgis dans le groupe 'Carto - Altitudes'
#  <<< status   : None 								Si le MNT n'est pas sur le Canevas Qgis
#                 int								Nombre de points pour lesquels l'altitude reste indéterminée. Zero si tous points OK
#  <<< lineXYZ  : [QgsPoint]						Ligne (liste de points) avec altitude (-9999 pour les altitudes indéterminées)
#				  None 								Si le MNT n'est pas sur le Canevas Qgis
# ========================================================================================

def setLineXYAltitudesFromMNT(lineXY, lineCrs, mntName):

	groupName = QGP.configMntGroupName
	mntShape, error = TL.findLayerInGroup(groupName, mntName)
	if error != None: return None, []

	crsTransform = QgsCoordinateTransform()
	crsTransform.setSourceCrs(lineCrs)
	crsTransform.setDestinationCrs(QgsCoordinateReferenceSystem(QGP.configMntShapesCrs[mntName]))

	nbrPointsOK = 0
	nbrPointsBAD = 0

	lineXYZ = []
	for pointXY in lineXY:
		point = QgsPoint(pointXY)
		altitude = mntShape.dataProvider().sample(crsTransform.transform(pointXY), 1)
		if (altitude[1]): 
			point.addZValue(altitude[0])
			nbrPointsOK += 1
		else: 
			point.addZValue(QGP.configAltitudeNotFound)
			nbrPointsBAD += 1
		point.addMValue()
		lineXYZ.append(point)
	
	return nbrPointsBAD, lineXYZ


# ========================================================================================
# Ajout des Altitudes manquantes sur une Ligne de Points via MNT particulier
#
#  >>> lineXYZ 	: [QgsPoint]						Ligne (liste de points) pour laquelle les altitudes manquantes doivent être déterminées
#  >>> lineCrs  : QgsCoordinateReferenceSystem 		Crs des coordonnées des points de la ligne lineXYZ
#  >>> mntName  : str 								Nom de la Couche MNT sur le Canevas Qgis dans le groupe 'Carto - Altitudes'
#
#  <<< status   : None 								Si le MNT n'est pas sur le Canevas Qgis
#                 int								Nombre de points pour lesquels l'altitude reste indéterminée. Zero si tous points OK
#  <<< lineXYZ  : [QgsPoint]						Ligne (liste de points) avec altitude (-9999 pour les altitudes indéterminées)
#													La ligne reste inchangée si le MNT n'est pas présent
# ========================================================================================

def setLineXYMissingAltitudesFromMNT(lineXYZ, lineCrs, mntName):

	groupName = QGP.configMntGroupName
	mntShape, error = TL.findLayerInGroup(groupName, mntName)
	if error != None: return None, lineXYZ

	crsTransform = QgsCoordinateTransform()
	crsTransform.setSourceCrs(lineCrs)
	crsTransform.setDestinationCrs(QgsCoordinateReferenceSystem(QGP.configMntShapesCrs[mntName]))

	nbrPointsOK = 0
	nbrPointsBAD = 0

	newLineXYZ = []
	for point in lineXYZ:
		if point.z() == QGP.configAltitudeNotFound: 
			altitude = mntShape.dataProvider().sample(crsTransform.transform(QgsPointXY(point)), 1)
			if (altitude[1]): 
				point.setZ(altitude[0])
				nbrPointsOK += 1
			else: 
				nbrPointsBAD += 1
		newLineXYZ.append(point)
	
	return nbrPointsBAD, newLineXYZ


# ========================================================================================
# Ajouter les Altitudes 
#  >>> track				: [Points]
#  >>> mainFrame	  		: Main Menu Frame - for display
#  >>> showStatus	  		: Flag : show status in mainFrame
#  <<< trackYZ
#  <<< missing				: Points sans Altitude
#  <<< error				: Text for Field 'Erreurs' - None si pas erreur
#  <<< comment				: Text for Field 'Commentaires'
# ========================================================================================

def addTrackAltitudes(track):

	crs3812 = QgsCoordinateReferenceSystem()
	crs3812.createFromString("EPSG:3812")

	missingMNT1, trackXYZ1 = setLineXYAltitudesFromMNT(track, crs3812, QGP.configMntShapesList[0])
	missingMNT2, trackXYZ2 = setLineXYMissingAltitudesFromMNT(trackXYZ1, crs3812, QGP.configMntShapesList[1])

	print('Missing = ' + str(missingMNT1) + ' - ' + str(missingMNT2))
	
	return trackXYZ2, missingMNT1, missingMNT2
	

# ========================================================================================
# Lisser les Altitudes 
#  >>> trackXYZ				: [Points]
# ========================================================================================

def smoothTrackAltitudes(trackXYZ):

	if len(trackXYZ) < QGP.configAltitudeSmoothRange: return
	
	trackDistances = []; totalDistance = 0
	for pointNum in range(len(trackXYZ)):
		if pointNum > 0: totalDistance += trackXYZ[pointNum - 1].distance(trackXYZ[pointNum])			
		trackDistances.append(totalDistance)

	for pointNum in range(len(trackXYZ)) :
		if trackXYZ[pointNum].z() == QGP.configAltitudeNotFound: continue
		pFrom = max(0, pointNum - QGP.configAltitudeSmoothRange)
		pTo = min(len(trackXYZ), pointNum + QGP.configAltitudeSmoothRange + 1)
		coefTotal = 0; elevationSum = 0
		for pNum in range(pFrom, pTo):
			if trackXYZ[pNum].z() == QGP.configAltitudeNotFound: continue
			coef = 2 ** -(abs((trackDistances[pointNum] - trackDistances[pNum]) / QGP.configAltitudeSmoothDistance))
			coefTotal += coef
			elevationSum += trackXYZ[pNum].z() * coef
		trackXYZ[pointNum].setZ(elevationSum / coefTotal)


# ========================================================================================
# Calculer les dénivelés
#  >>> track				: [Points]
#  <<< dPlus				: Dénivelé Positif
#  <<< dMinus				: Dénivelé Négatif 	(positive value returned)
#  <<< missing				: Points sans Altitude
# ========================================================================================
		
def computeTrackAscending(track):

	dPlus = dMinus = 0
	missing = 0
	lastElevation = QGP.configAltitudeNotFound

	for point in track:
		if point.z() == QGP.configAltitudeNotFound:
			missing += 1
			continue
		if lastElevation == QGP.configAltitudeNotFound:
			lastElevation = point.z()
			continue
		newElevation = point.z()
		if newElevation >= lastElevation:
			dPlus += (newElevation - lastElevation)
		else:
			dMinus += (lastElevation - newElevation)	
		lastElevation = newElevation
		
	return 	dPlus, dMinus, missing


# ========================================================================================
# Calculer les altitudes min et max
#  >>> track				: [Points]
#  <<< altMax				: Altitude Max
#  <<< altMin				: Altitude Min
#  <<< missing				: Points sans Altitude
# ========================================================================================
		
def computeTrackAltitudesMinMax(track):

	altMax = -9999
	altMin = 9999
	missing = 0

	for point in track:
		if point.z() == QGP.configAltitudeNotFound:
			missing += 1
			continue
		if point.z() < altMin: altMin = point.z()
		if point.z() > altMax: altMax = point.z()
		
	return 	altMax, altMin, missing
		
		
# ========================================================================================
# Calculer la distance équivalente UFO
#  >>> track				: [Points]
#  <<< distance				: Distence équivalente
#  <<< missing				: Points sans Altitude
# ========================================================================================		
		
def computeTrackEquivalentDistance(track):

	distanceUFO = 0; distanceUFOInverse = 0; distanceTotal = 0;
	missing = 0
	previousPoint = None
	
	for point in track:
		if previousPoint != None: 
			distance = point.distance(previousPoint)
			coefficient, coefficientInverse = computeUFORemiPoisvertCoefficients(previousPoint, point)
			if coefficient == None: missing +=1; coefficient = coefficientInverse = 1
			distanceTotal += distance
			distanceUFO += distance * coefficient
			distanceUFOInverse += distance * coefficientInverse
			if False :  print ('distanceTotal = ' + str(distanceTotal) + ' - distanceUFO = ' +  str(distanceUFO))
		previousPoint = point
	
	return 	distanceUFO, distanceUFOInverse, missing

		
# ========================================================================================		
# Coéfficients - Calcul Distance Equivalente - Rémi Poisvert			
#==========================================================
#	Coéfficient X	0,027700000	
#	Coéfficient X²	0,002200000	
#	Coéfficient X³	-0,000002000	
#	Coéfficient X4	-0,000000400				
#	Pente Max Valide pour Formule	40,0%	
#	Pente Min Valide pour Formule	-40,0%		
#==========================================================	
		
def computeUFORemiPoisvertCoefficients(pa, pb):
	if pa.z() == QGP.configAltitudeNotFound or pb.z() == QGP.configAltitudeNotFound: return None, None
	distance = pa.distance(pb)
	if distance == 0: return 0, 0
	
	penteVraie = 100 * (pb.z() - pa.z()) / distance
	penteCalcul = max(min(penteVraie, 40), -40)
	coefficient = 1 + 0.027700000 * penteCalcul + 0.002200000 * penteCalcul**2 - 0.000002000 * penteCalcul**3 - 0.000002000 * penteCalcul**4
	if penteVraie != 0 : coefficient = coefficient * penteVraie / penteCalcul 
	
	penteVraieInverse = -penteVraie
	penteCalculInverse = -penteCalcul
	coefficientInverse = 1 + 0.027700000 * penteCalculInverse + 0.002200000 * penteCalculInverse**2 - 0.000002000 * penteCalculInverse**3 - 0.000002000 * penteCalculInverse**4
	if penteVraieInverse != 0 : coefficientInverse = coefficientInverse * penteVraieInverse / penteCalculInverse 

	if False : print ('penteCalcul = ' + str(penteCalcul) + ' - coefficients = ' +  str(coefficient) + ' - ' + str(coefficientInverse))
	
	return coefficient, coefficientInverse
		
						
# ========================================================================================
# --- THE END ---
# ========================================================================================
