# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Start QCarto - Connected to Plugin Q Button
# ========================================================================================

from qgis.core import *
from qgis.gui import *
from PyQt5.QtWidgets import QApplication

import sys
import time
import importlib

import QCarto_Tools_Dates as TDAT

import QCarto_Menu_Main
importlib.reload(QCarto_Menu_Main)

# ========================================================================================
# Called from Q Button is clicked 
#  - Create main menu
#  - Wait until it closes
# ========================================================================================

def startQCarto(iface):

	iface.messageBar().pushMessage('QCarto - Hello !', 0, 1)

	if QCarto_Menu_Main in sys.modules:
		importlib.reload(sys.modules[QCarto_Menu_Main])

	while True :
		QCartoRun = QCarto(iface)
		status = QCartoRun.run()
		del QCartoRun
		if not status : break
	
	iface.messageBar().pushMessage('QCarto bye ...', 0, 2)
		

# ========================================================================================
# Class : QCarto
#  - Crée le Tabeau de Bord - menuMainFrame
#  - Attend la requète de fermeture
# ========================================================================================

class QCarto:

	def __init__(self, iface):
		self.iface = iface
		self.QCartoRunning = True
		self.QCartoRestart = False
		self.menu = QCarto_Menu_Main.menuMainFrame(self.iface, self)

	def run(self):
		while self.QCartoRunning:
			QgsApplication.processEvents()
			time.sleep(0.01)
		del self.menu
		return self.QCartoRestart

	def requestRestart(self):
		self.requestReimport()
		self.QCartoRestart = True
		self.QCartoRunning = False

	def requestClose(self):
		self.QCartoRunning = False
		
	def requestReimport(self):
		if QCarto_Menu_Main in sys.modules:
			importlib.reload(sys.modules[QCarto_Menu_Main])
		
		
# ========================================================================================
# --- THE END ---
# ========================================================================================
