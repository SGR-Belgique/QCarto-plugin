# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Utilitaires pour l'export des Tracés au Format OziExplorer .plt
# ========================================================================================

from qgis.core import *
from qgis.gui import *

import math

import QCarto_Tools_Coding as TCOD
import QCarto_Tools_Files as TFIL
import QCarto_Tools_SCR as TSCR

import QCarto_Parameters_Global
QGP = QCarto_Parameters_Global.globalParameters()


# ========================================================================================
# Créer le fichier Trace .plt
# ========================================================================================

def exportOziTrack(path, file, code, name, track):

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
	
# Open PLT File

	TFIL.ensure_dir(path)
	pltFilePath = path + file
	fileOut = open(pltFilePath, 'w', encoding='utf-8', errors='ignore')
	
# Write Header

	for line in QGP.configOziTrackFileHeaderLines: 
		line = line.replace('%NAME%', name)
		if TCOD.isCodeLiaisonGR(code): line = line.replace('%COLOR%', str(QGP.configPLTCouleurGRVariantes))
		if TCOD.isCodeLiaisonGR(code):  line = line.replace('%COLOR%', str(QGP.configPLTcouleurGRLiaisons))
		line = line.replace('%COLOR%', str(QGP.configPLTCouleurGR))
		fileOut.write(line + '\n')	

# Write Track Points

	pt1 = True
	for point in track:
		alt = point.z()
		lat, lon = TSCR.convertPoint3812toWgs84(point.x(), point.y())
		for line in QGP.configOziTrackPointFileLines: 
			if pt1 : 
				line = line.replace('%SEG%', '1')
				pt1 = False
			else:
				line = line.replace('%SEG%', '0')
			line = line.replace('%LAT%', str(lat))
			line = line.replace('%LON%', str(lon))
			if alt == QGP.configAltitudeNotFound:
				line = line.replace('%ALT%', '-777')
			else:
				line = line.replace('%ALT%', str(math.floor(alt / 0.3048)))
			fileOut.write(line + '\n')	

#	Fermer le fichier

	fileOut.close()
	
		
# ========================================================================================
# --- THE END ---
# ========================================================================================
