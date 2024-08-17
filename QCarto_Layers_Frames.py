# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Utilitaires pour la Gestion des Emprises Cartes 
# ========================================================================================

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qgis.core import *
from qgis.gui import *

import QCarto_Tools_Layers as TLAY

import QCarto_Parameters_Global

QGP = QCarto_Parameters_Global.globalParameters()


# ========================================================================================
# Ajouter la Couche Qgis des Emprises au Canevas
#   >>> iface
# ========================================================================================

def addFrameShape(framePath):
	
# Retrouver le style des Emprises

	stylePath = QGP.configPathStyles + QGP.configFrameStyle
	styleFile = QGP.configShapeFrameName + '.qml'

# Nom de la couche et du groupe

	frameName = QGP.configShapeFrameName
	groupName = QGP.configFrameGroupName

# Ajouter la couche des Emprises

	layer, error = TLAY.loadLayer(framePath, frameName, groupName, frameName, stylePath, styleFile, False)

	return layer, error


# ========================================================================================
# --- THE END ---
# ========================================================================================
