# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Utilitaires pour la Gestion d'un Rubberband
# ========================================================================================

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qgis.core import *
from qgis.gui import *
from qgis.PyQt import QtWidgets

import importlib

import QCarto_Definitions_Colors as DCOL
importlib.reload(DCOL)

class rubberBandGPX:

	def __init__(self, iface):
		self.iface = iface
		if Qgis.QGIS_VERSION_INT <  33000 : self.canvasLine = QgsRubberBand(self.iface.mapCanvas(), False) 										 # False = not a polygon
		if Qgis.QGIS_VERSION_INT >= 33000 : self.canvasLine = QgsRubberBand(self.iface.mapCanvas(), geometryType = Qgis.GeometryType.Line)
		self.canvasLine.setColor(DCOL.bgRubberBandGPXTrack)
		self.canvasLine.setWidth(12)
		self.canvasLine.reset()
		if Qgis.QGIS_VERSION_INT <  33000 : self.canvasPointsA = QgsRubberBand(self.iface.mapCanvas(), 0) 								
		if Qgis.QGIS_VERSION_INT >= 33000 : self.canvasPointsA = QgsRubberBand(self.iface.mapCanvas(), geometryType = Qgis.GeometryType.Point)
		self.canvasPointsA.setColor(DCOL.bgRubberBandGPXPointsA)
		self.canvasPointsA.setIconSize(18)
		self.canvasPointsA.reset()
		if Qgis.QGIS_VERSION_INT <  33000 : self.canvasPointsB = QgsRubberBand(self.iface.mapCanvas(), 0) 								
		if Qgis.QGIS_VERSION_INT >= 33000 : self.canvasPointsB = QgsRubberBand(self.iface.mapCanvas(), geometryType = Qgis.GeometryType.Point)
		self.canvasPointsB.setColor(DCOL.bgRubberBandGPXPointsB)
		self.canvasPointsB.setIconSize(12)
		self.canvasPointsB.reset()


	def deleteRubberBand(self):
		self.canvasLine.reset()
		self.canvasPointsA.reset()
		self.canvasPointsB.reset()
		del self.canvasLine
		del self.canvasPointsA
		del self.canvasPointsB

	def clearRubberBand(self):
		self.canvasLine.reset()
		self.canvasPointsA.reset()
		self.canvasPointsB.reset()
		
	def refreshRubberBand(self, trackLine, wayPointsA = [], wayPointsB = []):
		self.canvasLine.reset() if trackLine == [] else self.canvasLine.setToGeometry(QgsGeometry.fromMultiPolylineXY([trackLine]), None)
		self.canvasPointsA.reset() if wayPointsA == [] else self.canvasPointsA.setToGeometry(QgsGeometry.fromMultiPointXY(wayPointsA))
		self.canvasPointsB.reset() if wayPointsB == [] else self.canvasPointsB.setToGeometry(QgsGeometry.fromMultiPointXY(wayPointsB))

	def setRubberBandColor(self, color):
		colorRubber = QColor(color)
		colorRubber.setAlpha(127)
		self.canvasLine.setColor(colorRubber)
		

# ========================================================================================
# --- THE END ---
# ========================================================================================
