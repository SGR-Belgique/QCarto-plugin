# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Utilitaires pour la Gestion des Carte IGN
# ========================================================================================

import math

import QCarto_Parameters_Global
QGP = QCarto_Parameters_Global.globalParameters()


# ========================================================================================
# Convertir un point 3812 en Carte Topo 50
# ========================================================================================

def convertPoint3812toTopo25(pointFeature):
	
	try:
		x = pointFeature.geometry().asPoint().x()
		y = pointFeature.geometry().asPoint().y()
		line = math.floor((QGP.configIgnTopo25TableNord - y) / QGP.configIgnTopo25TableHeight)
		col = math.floor((x - QGP.configIgnTopo25TableOuest) / QGP.configIgnTopo25TableWidth)
		mapNumber = QGP.configIgnTopo25Table[line][col]
		mapName = QGP.configIgnTopo25NameDico[mapNumber]
	except:
		mapNumber = None
		mapName = None
		
	return mapNumber, mapName


# ========================================================================================
# --- THE END --- 
# ========================================================================================
