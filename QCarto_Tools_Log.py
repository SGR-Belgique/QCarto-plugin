# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Utilitaires divers pour Log info
# ========================================================================================

from qgis.core import *
from qgis.gui import *

import os
import shutil

import QCarto_Tools_Dates as TDAT
import QCarto_Tools_Files as TFIL

import QCarto_Parameters_Global
QGP = QCarto_Parameters_Global.globalParameters()


# ========================================================================================
# Log text info file log - le timestamp et le nom du carto sont automatiques
#  >>> logType  : str			'DeliveryOsm'  
#  >>> infos    : [str]			Liste des infos à logger 
#  <<< status	: bool			True if done, False if error
# ========================================================================================

def appendInfoInLogfile(logType, infos):

	if logType == 'DeliveryOsm' : 
		filePath = QGP.pathDeliveriesCoordinationOSMLogfile
	elif logType == 'DeliveryCarto' :
		filePath = QGP.pathDeliveriesCartoLogfile
	elif logType == 'DeliveryTopo' :
		filePath = QGP.pathDeliveriesTopoLogfile
	elif logType == 'PublicMap' :
		filePath = QGP.pathPublicationsPublicMapLogfile
	else :
		return False

	TFIL.ensure_dir(filePath)
	fileOut = open(filePath, 'a', encoding='utf-8', errors='ignore')
	newline   = QGP.configCSVNewLine
	separator = QGP.configCSVSeparator
	
	try:
		fileOut.write(TDAT.getTimeStamp() + separator + QgsApplication.userFullName() + separator + separator.join(infos) + newline)
		fileOut.close()
	except:
		fileOut.close()
		return False

	return True

		
# ========================================================================================
# --- THE END ---
# ========================================================================================


