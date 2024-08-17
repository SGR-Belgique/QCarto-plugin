# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Utilitaires pour la Gestion des Aiudes spéciales
# ========================================================================================

import time
import webbrowser
import subprocess
import importlib
import os
from PIL import Image

import QCarto_Tools_Dates as TDAT

try:
	import QCarto_Parameters_Global
	importlib.reload(QCarto_Parameters_Global)
	QGP = QCarto_Parameters_Global.globalParameters()
except:
	QGP = None

try:
	import SGRBalisage_GlobalParameters 
	importlib.reload(SGRBalisage_GlobalParameters)
	QBP = SGRBalisage_GlobalParameters.globalParameters()
except:
	QBP = QGP

try:
	import QPhotos_GlobalParameters 
	importlib.reload(QPhotos_GlobalParameters)
	QPP = QPhotos_GlobalParameters.globalParameters()
except:
	QPP = QGP


# ========================================================================================
# Afficher une carte dans le navigateur
#  >>> mainFrame
#  >>> pageTitle	: txt				Texte pour le titre de la page
#  >>> mapPath 		: txt				Path complet de la carte à afficher
# ========================================================================================

def viewMapOnBrowser(mainFrame, pageTitle, mapPath):
	try:
		image = Image.open(mapPath)
		widthView = image.width if image.width <= 1500 else (1500 if image.width > image.height else int(1500 * (image.width / image.height)))
	except:
		widthView = 1500
	
	fileOut = open(QGP.configMenuHelpBasePath + QGP.exportSeeMapHtmlFile, 'w')
	for line in QGP.exportSeeMapHtmlContent:
		line = line.replace('%TITLE%', pageTitle)
		line = line.replace('%MAPPATH%', mapPath)
		line = line.replace('%WIDTH%', str(widthView))
		line = line.replace('%TIMESTAMP%', TDAT.extractTimeStamp(mapPath))
		fileOut.write(line + '\n')
	fileOut.close()	

	webbrowser.open_new_tab(QGP.configMenuHelpBasePath + QGP.exportSeeMapHtmlFile)
	mainFrame.setStatusDone('Le navigateur montre la Carte !')


# ========================================================================================
# Afficher une photo dans le navigateur
#  >>> mainFrame
#  >>> pageTitle	: txt				Texte pour le titre de la page
#  >>> mapPath 		: txt				Path complet de la carte à afficher
# ========================================================================================

def viewPhotoOnBrowser(mainFrame, pageTitle, mapPath):
	try:
		image = Image.open(mapPath)
		widthView = image.width if image.width <= 1500 else (1500 if image.width > image.height else int(1500 * (image.width / image.height)))
	except:
		widthView = 1500
	
	fileOut = open(QPP.configMenuHelpBasePath + QPP.exportSeePhotoHtmlFile, 'w')
	for line in QPP.exportSeePhotoHtmlContent:
		line = line.replace('%TITLE%', pageTitle)
		line = line.replace('%MAPPATH%', mapPath)
		line = line.replace('%WIDTH%', str(widthView))
		line = line.replace('%TIMESTAMP%', TDAT.extractTimeStamp(mapPath))
		fileOut.write(line + '\n')
	fileOut.close()	

	webbrowser.open_new_tab(QPP.configMenuHelpBasePath + QPP.exportSeePhotoHtmlFile)
	mainFrame.setStatusDone('Le navigateur montre la Photo !')
	

# ========================================================================================
# Afficher un fichier Html dans le navigateur
#  >>> mainFrame
#  >>> pageTitle	: txt				Texte pour le titre de la page
#  >>> htmlPath 	: txt				Path complet du fichier html
# ========================================================================================

def viewHtmlOnBrowser(mainFrame, pageTitle, htmlPath):
	fileOut = open(QGP.configMenuHelpBasePath + QGP.exportSeeHtmlHtmlFile, 'w')
	for line in QGP.exportSeeHtmlHtmlContent:
		if '%HTMLLINES%' in line:
			fileIn = open(htmlPath, 'r')
			for lineHtml in fileIn: fileOut.write(lineHtml + '\n')
			fileIn.close()
			continue			
		line = line.replace('%TITLE%', pageTitle)
		line = line.replace('%HTMLPATH%', htmlPath)
		line = line.replace('%TIMESTAMP%', TDAT.extractTimeStamp(htmlPath))
		fileOut.write(line + '\n')
	fileOut.close()	

	webbrowser.open_new_tab(QGP.configMenuHelpBasePath + QGP.exportSeeHtmlHtmlFile)
	mainFrame.setStatusDone('Le navigateur montre le fichier Html !')


# ========================================================================================
# Afficher un fichier CSV dans le navigateur
#  >>> mainFrame
#  >>> pageTitle	: txt				Texte pour le titre de la page
#  >>> csvPath 		: txt				Path complet du fichier à afficher
# ========================================================================================

def viewCsvOnBrowser(mainFrame, pageTitle, csvPath):

	separator = QGP.configCSVSeparator
	if os.path.isfile(QGP.configMenuHelpBasePath + QGP.exportSeeCsvHtmlFile) :
		fileOut = open(QGP.configMenuHelpBasePath + QGP.exportSeeCsvHtmlFile, 'w')
	elif os.path.isfile(QBP.configMenuHelpBasePath + QBP.exportSeeCsvHtmlFile) :
		fileOut = open(QBP.configMenuHelpBasePath + QBP.exportSeeCsvHtmlFile, 'w')
	else:
		mainFrame.setStatusWarning('Fichier introuvable !')
		return

	for line in QGP.exportSeeCsvHtmlContent:
		if line == '@TableRow@' :
			fileIn = open(csvPath, 'r')			
			for csvLine in fileIn:
				csvTableRow = '<tr><td>' + '</td><td>'.join(csvLine.split(separator)) + '</td></tr>'
				fileOut.write(csvTableRow + '\n')
			fileIn.close()	
		else:
			line = line.replace('%TITLE%', pageTitle)
			line = line.replace('%CSVPATH%', csvPath)
			line = line.replace('%TIMESTAMP%', TDAT.extractTimeStamp(csvPath))
			fileOut.write(line + '\n')
	fileOut.close()	

	webbrowser.open_new_tab(QGP.configMenuHelpBasePath + QGP.exportSeeCsvHtmlFile)
	mainFrame.setStatusDone('Le navigateur montre le contenu du fichier !')


# ========================================================================================
# Ouvrir l'explorateur windows sur un répertoire
#  >>> mainFrame
#  >>> folderPath	: txt				Path complet du répertoire (les / sont changés ici)
# ========================================================================================

def viewFolderExplorer(mainFrame, folderPath):

	try:
		folderPath = folderPath.replace('/','\\')
		subprocess.Popen('explorer ' + folderPath)
	except:
		mainFrame.setStatusWarning('Une erreur s\'est produite lors de la demande d\'ouverture de l\'explorer !')
		return

	mainFrame.setStatusInfo('Voir dans l\'explorer : ' + folderPath)


# ========================================================================================
# --- THE END ---
# ========================================================================================
