# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ========================================================================================

from qgis.core import *
from qgis.gui import *

import time
import sys
import os
import importlib
	
import QCarto_Tools_Dates as TDAT
import QCarto_Tools_Files as TFIL
import QCarto_Tools_Layers as TLAY
	
import QCarto_Parameters_Global
QGP = QCarto_Parameters_Global.globalParameters()	


# ========================================================================================
# Process : Backup de la DB Carto
# ========================================================================================

def process_BackupDB(mainFrame, archiveName = None):

	mainFrame.setStatusWorking('Backup de la DB Carto ...')
	startTime = time.time()
	
#	Définir le path de backup et vérifier

	savingPath = QGP.configBackupPath if archiveName == None else QGP.configArchivePath
	if not os.path.isdir(savingPath):
		mainFrame.setStatusError(' Le répertoire de backup : ' + savingPath + ' n\'existe pas ?')
		return False	

	savingPath += TDAT.getTimeStamp()
	savingPath += ' (Backup Complet)' + '/' if archiveName == None else ' (' + archiveName + ')' + '/'
	TFIL.ensure_dir(savingPath)

#	Procéder au backup des couches 

	errorCount = 0
	backupCount = 0

	for layerName in QGP.tablesBackupList:

		mainFrame.setStatusWorking('Backup de la couche : ' + layerName + ' ...')

		layer, errorText = TLAY.openLayer(layerName)
		if layer == None:
			mainFrame.setStatusWarning(errorText)
			TDAT.sleep(2000)
			errorCount += 2
			continue

#		Backup en mode SHP

		anyError = QgsVectorFileWriter.writeAsVectorFormat(layer, savingPath + layerName + '.shp', 'UTF-8', layer.crs(), 'ESRI Shapefile')
		if (anyError[0] != 0):
			mainFrame.setStatusWarning('Backup de la couche : ' + layerName + ' : Backup .shp impossible - ' + str(anyError))
			TDAT.sleep(2000)
			errorCount += 1
		else:
			mainFrame.setStatusWorking('Backup de la couche : ' + layerName + ' : Backup .shp terminé !')
			backupCount += 1
		QgsApplication.processEvents()
		
#		Backup en mode CSV

		anyError = QgsVectorFileWriter.writeAsVectorFormat(layer, savingPath + layerName + '.csv', 'UTF-8', layer.crs(), 'CSV')
		if (anyError[0] != 0):
			mainFrame.setStatusWarning('Backup de la couche : ' + layerName + ' : Backup .csv impossible - ' + str(anyError))
			TDAT.sleep(2000)
			errorCount += 1
		else:
			mainFrame.setStatusWorking('Backup de la couche : ' + layerName + ' : Backup .csv terminé !')
			backupCount += 1
		QgsApplication.processEvents()

#	Terminé

	if errorCount == 0 :
		mainFrame.setStatusDone('Backup de la DB Carto : ' + str(backupCount) + ' couches - OK')
	else:
		mainFrame.setStatusWarning('Backup de la DB Carto : ' + str(errorCount) + ' couches incorrectes !')
			
	endTime = time.time()
	workingTime = int(endTime - startTime)

	return True

		
# ========================================================================================
# --- THE END ---
# ========================================================================================
		