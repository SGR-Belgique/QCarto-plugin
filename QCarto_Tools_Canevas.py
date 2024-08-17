# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Utilitaires pour la Gestion du Canevas Qgis
# ========================================================================================

from qgis.core import *
from qgis.gui import *

import QCarto_Parameters_Global
QGP = QCarto_Parameters_Global.globalParameters()


# ========================================================================================
# Montrer // Cacher un panneau sur le Canevas - En cas d'erreur, rien ne se passe
#  >>> iface
#  >>> panelName		 : str			Nom du Panneau
#  >>> showFlag 		 : bool			True = Montrer // False = Cacher
#  <<< showFlagBefore	 : bool			True = Panneau visible avant // False = Panneau non visible avant
# ========================================================================================

def setCanevasPanelVisibility(iface, panelName, showFlag):
	try:
		panelList = [x for x in iface.mainWindow().findChildren(QDockWidget) if x.windowTitle() == panelName]
		visible = panelList[0].isVisible()
		panelList[0].setVisible(showFlag)
		return visible
	except:
		return False


# ========================================================================================
# Montrer / Cacher un Groupe sur le Canevas
# >>> name  : str							Group Name on Canevas
# >>> flag  : bool							True = Montrer // False = Cacher
# ========================================================================================

def groupShowOnCanevas(name, flag):
	root = QgsProject.instance().layerTreeRoot()
	groupNode = root.findGroup(name)
	if groupNode != None : groupNode.setItemVisibilityChecked(flag)

def groupShowToggleOnCanevas(name):
	root = QgsProject.instance().layerTreeRoot()
	groupNode = root.findGroup(name)
	if groupNode != None : groupNode.setItemVisibilityChecked(not groupNode.itemVisibilityChecked())


# ========================================================================================
# Montrer / Cacher une Couche sur le Canevas
# >>> layer : QgsVectorLayer				Layer on Canevas
# >>> flag  : bool							True = Montrer // False = Cacher
# ========================================================================================

def layerShowOnCanevas(layer, flag):
	root = QgsProject.instance().layerTreeRoot()
	layerNode = root.findLayer(layer.id())
	layerNode.setItemVisibilityChecked(flag)

		
# ========================================================================================
# --- THE END ---
# ========================================================================================
