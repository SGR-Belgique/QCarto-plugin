# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Utilitaires pour la Gestion des Couches du Réseau SGR
# ========================================================================================


from qgis.core import *
from qgis.gui import *

import os


# ========================================================================================
# Ouvrir une couche existante d'un nom donné
#  >>> layerName	: str				Nom de la couche sur le Canevas
#  <<< return	 	: layer				QgsVectorLayer iff error returned is None
#					: None or str		Error string or None if OK
# ========================================================================================

def openLayer(layerName):
	layers = QgsProject.instance().mapLayersByName(layerName)
	if len(layers) == 0:
		return None, '??? La couche : ' + layerName + " n'est pas présente sur le Canevas"
	if len(layers) > 1:
		return None, '??? La couche : ' + layerName + " est multiple sur le Canevas"
	return layers[0], None


# ========================================================================================
# Trouver un groupe sur le canevas Qgis
#  >>> groupName : Nom du groupe de Couches Qgis
#  <<< return	 : group, error
# ========================================================================================

def findGroup(groupName):

	root = QgsProject.instance().layerTreeRoot()
	group = root.findGroup(groupName)
	if (not(group)): return None, "Le Groupe " + groupName + " n'est pas présent sur le Canevas"

	return group, None


# ========================================================================================
# Trouver l'index d'un groupe sur le canevas Qgis
#  >>> groupName : Nom du groupe de Couches Qgis
#  <<< return	 : index, error
# ========================================================================================

def findGroupIndex(groupName):

	root = QgsProject.instance().layerTreeRoot()
	groupNameList = [group.name() for group in root.findGroups()]
	if (groupName not in groupNameList): return None, "Le Groupe " + groupName + " n'est pas présent sur le Canevas"

	return groupNameList.index(groupName), None


# ========================================================================================
# Creer un groupe sur le canevas Qgis s'il n'existe pas déjà
#  >>> groupName : Nom du groupe de Couches Qgis
#  >>> groupIndex : [999] Insérer groupe à l'index groupIndex
#  <<< return : QgsLayerTreeGroup
# ========================================================================================

def createGroup(groupName, groupIndex = 999):

	root = QgsProject.instance().layerTreeRoot()
	group = root.findGroup(groupName)

	if not(group) :
		group = root.insertGroup(groupIndex, groupName)
		group.setItemVisibilityChecked(True)
	return(group)


# ========================================================================================
# Trouver un groupe sur le canevas Qgis et une couche dans ce groupe
#  >>> groupName : Nom du groupe de Couches Qgis
#  >>> layerName : Nom de la Couche Qgis
#  <<< return	 : layer, error
# ========================================================================================

def findLayerInGroup(groupName, layerName):

	root = QgsProject.instance().layerTreeRoot()
	group = root.findGroup(groupName)
	if (not(group)): 
		return None, "Le Groupe " + groupName + " n'est pas présent sur le Canevas"

	for layerNode in group.findLayers():
		if layerNode.name() == layerName: return layerNode.layer(), None
		
	return None,  "La Couche " + layerName + " n'est pas présente dans le groupe " + groupName


# ========================================================================================
# Déterminer si une au moins des couches d'un group sur le Canevas Qgis est en mode édition
#  >>> groupName : str			Nom du groupe sur le Canevas Qgis 
#  <<<  		   bool			True si au moins une couche est en mode édition
#								False si toutes les couches sont fermées pour l'édition ou si le groupe n'existe pas 
# ========================================================================================

def isLayerInGroupEditable(groupName):

	root = QgsProject.instance().layerTreeRoot()
	group = root.findGroup(groupName)
	if group == None: return False
	for child in group.children():
		if child.layer().isEditable(): return True
	return False	
	
	
# ========================================================================================
# Déterminer si une au moins des couches d'un group sur le Canevas Qgis est en mode édition et modifiée
#  >>> groupName : str			Nom du groupe sur le Canevas Qgis 
#  <<<  		   bool			True si au moins une couche est en mode édition
#								False si toutes les couches sont fermées pour l'édition ou si le groupe n'existe pas 
# ========================================================================================

def isLayerInGroupModified(groupName):

	root = QgsProject.instance().layerTreeRoot()
	group = root.findGroup(groupName)
	if group == None: return False
	for child in group.children():
		if child.layer().isModified(): return True
	return False	


# ========================================================================================
# Supprimer une des Couches d'un Groupe Qgis
#  >>> groupName : str			Nom du groupe sur le Canevas Qgis 
# ========================================================================================

def removeLayerFromGroup(groupName, layerName):

	root = QgsProject.instance().layerTreeRoot()
	group = root.findGroup(groupName)

	for node in group.children():
		if node.name() == layerName: group.removeLayer(node.layer())
		

# ========================================================================================
# Supprimer toutes les Couches d'un Groupe Qgis
#  >>> groupName : str			Nom du groupe sur le Canevas Qgis 
# ========================================================================================

def cleanLayerGroup(groupName):

	root = QgsProject.instance().layerTreeRoot()
	group = root.findGroup(groupName)

	if group == None: return

	group.removeAllChildren()
		

# ========================================================================================
# Replier complètement un Groupe Qgis
#  >>> groupName : str			Nom du groupe sur le Canevas Qgis 
# ========================================================================================

def foldLayersGroup(groupName):

	root = QgsProject.instance().layerTreeRoot()
	group = root.findGroup(groupName)

	if group == None: return

	for layerNode in group.findLayers():
		layerNode.setExpanded(True)
		layerNode.setExpanded(False)


# ========================================================================================
# Recharger une Couche depuis un fichier 
#  >>> path 		: str					Répertoire où trouver la couche
#  >>> file			: str					Nom du fichier couche (sans extension - .dbf est ajouté automatiquement)
#  >>> groupName	: str					Nom du groupe où déplacer la couche
#  >>> layerName	: str					Nom de la couche sur la Canevas
#  >>> stylePath    : str					Répertoire où trouver le style
#  >>> styleFile    : str					Nom du ficher style - None si pas de style à appliquer
#  >>> readonly		: bool					Flag - empêcher l'écriture sur la couche
#  <<< layer, errorText
# ========================================================================================

def loadLayer(path, file, groupName, layerName, stylePath, styleFile, readonly = False):

#	Check if path and file exist

	if not os.path.isdir(path):  return None, 'Le répertoire du fichier ' + file + ' est introuvable !'
	if not os.path.isfile(path + file + '.dbf'): return None, 'Le fichier ' + file + ' est introuvable !'

#	Check if group exists and layer does not yet exists

	root = QgsProject.instance().layerTreeRoot()
	group = root.findGroup(groupName)
	if group == None: return None, 'Le groupe ' + groupName + ' n\'est pas sur le canevas !'

	layer, error = findLayerInGroup(groupName, layerName) 
	if layer != None: return None, 'La couche ' + layerName + ' existe déjà !'
	
#	Create layer

	layer = QgsVectorLayer(path + file + '.dbf', layerName, 'ogr')
	layer.setName(layerName)
	layer.setReadOnly(readonly)
	if (layer == None): return None, 'Impossible de créer la couche : ' + layerName

#	Insert layer in requested group

	QgsProject.instance().addMapLayer(layer, False)
	group.addLayer(layer)

#	Load style if requested

	if styleFile != None:
		loadResult = False
		layer.loadNamedStyle(stylePath + styleFile, loadResult)

#	Replier la couche

	layerSetExpanded(layer, False)

	return layer, None


# ========================================================================================
# Recharger une Couche Raster depuis un fichier 
#  >>> path 		: str							Répertoire où trouver la couche
#  >>> file			: str							Nom du fichier couche (sans extension - .dbf est ajouté automatiquement)
#  >>> groupName	: str							Nom du groupe où déplacer la couche
#  >>> layerName	: str							Nom de la couche sur la Canevas
#  >>> crs			: QgsCoordinateReferenceSystem
#  >>> opacity		: int
#  <<< layer, errorText
# ========================================================================================

def loadRaster(path, file, groupName, layerName, crs, opacity):

#	Check if path and file exist

	if not os.path.isdir(path):  return None, 'Le répertoire du fichier ' + file + ' est introuvable !'
	if not os.path.isfile(path + file): return None, 'Le fichier ' + file + ' est introuvable !'

#	Check if group exists and layer does not yet exists

	root = QgsProject.instance().layerTreeRoot()
	group = root.findGroup(groupName)
	if group == None: return None, 'Le groupe ' + groupName + ' n\'est pas sur le canevas !'

	layer, error = findLayerInGroup(groupName, layerName) 
	if layer != None: return None, 'La couche ' + layerName + ' existe déjà !'
	
#	Create layer

	layer =  QgsRasterLayer(path + file, layerName, 'gdal')
	if (layer == None): return None, 'Impossible de créer la couche : ' + layerName

	layer.setName(layerName)
	layer.setCrs(crs)
	layer.renderer().setOpacity(opacity / 100)

#	Insert layer in requested group

	QgsProject.instance().addMapLayer(layer, False)
	group.addLayer(layer)

#	Replier la couche

	layerSetExpanded(layer, False)

	return layer, None


# ========================================================================================
# Replier / Déplier une Couche sur le Canevas
# ========================================================================================

def layerSetExpanded(layer, flag):

	root = QgsProject.instance().layerTreeRoot()
	layerNode = root.findLayer(layer.id())
	layerNode.setExpanded(flag)


# ========================================================================================
# --- THE END ---
# ========================================================================================

