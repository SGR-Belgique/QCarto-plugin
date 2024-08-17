# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Utilitaires pour la Gestion Paramètres Externes QCarto
# ========================================================================================

from qgis.core import *
from qgis.gui import *

import importlib

import QCarto_Parameters_Global
importlib.reload(QCarto_Parameters_Global)
QGP = QCarto_Parameters_Global.globalParameters()

	
# ========================================================================================
# Initialiser les dictionnaires de paramètres
# ========================================================================================

def initializeQCartoParameter(mainFrame) :

	if mainFrame.layerQCartoParam == None : return False

	mainFrame.dicoQCartoParam = {}

	for feature in mainFrame.layerQCartoParam.getFeatures() :
		group = feature[QGP.tableQParamFieldGroup]
		name = feature[QGP.tableQParamFieldName]
		code = feature[QGP.tableQParamFieldCode]
		value = feature[QGP.tableQParamFieldValue]
		if group not in mainFrame.dicoQCartoParam : mainFrame.dicoQCartoParam[group] = {}
		if name not in mainFrame.dicoQCartoParam[group] : mainFrame.dicoQCartoParam[group][name] = {}
		mainFrame.dicoQCartoParam[group][name][code] = value

	return True


# ========================================================================================
# Retrouver la valeur d'un paramètre
# ========================================================================================

def retrieveQCartoParameter(mainFrame, group, name, code, default = None) :

	try : 
		return mainFrame.dicoQCartoParam[group][name][code]
	except:
		return default


# ========================================================================================
# --- THE END ---
# ========================================================================================
