# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Utilitaires pour la Gestion du Site GR
# ========================================================================================

from qgis.core import *
from qgis.gui import *

import time
import ftplib
	
import QCarto_Parameters_Global
QGP = QCarto_Parameters_Global.globalParameters()


# ========================================================================================
# Lire le répertoire GPX / MAJ sur le Site SGR
#  >>> mode : str						'GPX' // ' MAJ'
# ========================================================================================

def readSiteSGRDirectory(mode):
	
	try:
		siteSGR = ftplib.FTP()
		siteSGR.connect(QGP.configSiteSGRFtpConnect)
		siteSGR.login(QGP.configSiteSGRFtpUser, QGP.configSiteSGRFtpPassword)
		siteSGR.encoding = 'utf-8'
		siteSGR.cwd(QGP.configSiteSGRGPXFolder if mode == 'GPX' else QGP.configSiteSGRMAJFolder)
	except:
		return None

	try:
		fileList = []
		siteSGR.retrlines('MLSD', fileList.append)
		fileList = sorted(fileList)
	except:
		return None

	siteSGR.close()		

	fileList = [file.split()[1] for file in fileList if file[-4:] == ('.gpx' if mode == 'GPX' else '.pdf') ]
	
	return fileList
	

# ========================================================================================
# --- THE END ---
# ========================================================================================
