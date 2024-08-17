# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Utilitaires pour la saisie de données
# ========================================================================================


# ========================================================================================
# Imports
# ========================================================================================

from PyQt5.QtCore import *
from PyQt5.QtGui import *

from qgis.core import *
from qgis.gui import *
from qgis.PyQt import QtWidgets

import importlib

import QCarto_Tools_Buttons as TBUT
importlib.reload(TBUT)


# ========================================================================================
# Class : inputFromCombo :
# ========================================================================================

class inputFromCombo:

	def __init__(self, iface, parent, title, label, comboList, resultFunction):

# 	Paramètres fournis

		self.iface = iface
		self.parent = parent
		self.title = title
		self.comboList = comboList
		self.resultFunction = resultFunction

#	Créer la fenêtre

		self.inputWindow = QtWidgets.QWidget()
		self.inputWindow.setGeometry(200,500,760,65)
		self.inputWindow.setWindowTitle(self.title)
		self.inputWindow.setWindowModality(Qt.ApplicationModal)
		self.inputWindow.repaint()
		self.inputWindow.show()
	
# Label 	
	
		self.label = TBUT.createLabelBlackButton(self.inputWindow, 1, 1, label, 'Normal', 'Normal')
		self.label.show()
	
#	Créer le Combo

		self.inputCombo = TBUT.createComboButton(self.inputWindow, 2, 1, 'Double')
		for _ in self.comboList : self.inputCombo.addItem(_)
		self.inputCombo.repaint()
		self.inputCombo.show()
		
#	Créer les boutons de commande

		self.buttonCancel = TBUT.createActionButton(self.inputWindow, 4, 1, 'Annuler', 'Normal')
		self.buttonCancel.clicked.connect(self.cancelRequested)
		self.buttonCancel.show()
		
		self.buttonConfirm = TBUT.createActionButton(self.inputWindow, 5, 1, 'Confirmer', 'Normal')
		self.buttonConfirm.clicked.connect(self.confirmRequested)
		self.buttonConfirm.show()
		
#		buttonShow.clicked.connect(self.createTracksView)	

	def cancelRequested(self):
		self.resultFunction(False, '')
	
	def confirmRequested(self):
		self.resultFunction(True, self.inputCombo.currentText())
		
		
# ========================================================================================
# Class : inputFromText 
# ========================================================================================

class inputFromText:

	def __init__(self, iface, parent, title, labelList, textList, resultFunction):

# 	Paramètres fournis

		self.iface = iface
		self.parent = parent
		self.title = title
		self.labelList = labelList
		self.textList = textList
		self.resultFunction = resultFunction

#	Créer la fenêtre

		self.inputWindow = QtWidgets.QWidget()
		self.inputWindow.setGeometry(200,500,610,30 * len(textList) + 30 + 55)
		self.inputWindow.setWindowTitle(self.title)
		self.inputWindow.setWindowModality(Qt.ApplicationModal)
		self.inputWindow.repaint()
		self.inputWindow.show()
	
#	Créer les lignes label + texte

		self.labelButtonList = []
		self.textButtonList = []

		for row in range(len(textList)):
			labelButton = TBUT.createLabelBlackButton(self.inputWindow, 1, 1 + row, labelList[row], 'Normal', 'Normal')
			textButton = TBUT.createInputButton(self.inputWindow, 2, 1 + row, 'Double3')
			textButton.setText(textList[row])
			labelButton.show()
			textButton.show()
			self.labelButtonList += [labelButton]
			self.textButtonList += [textButton]
			
#	Créer les boutons de commande

		self.buttonCancel = TBUT.createActionButton(self.inputWindow, 3, 2 + len(textList), 'Annuler', 'Normal')
		self.buttonCancel.clicked.connect(self.cancelRequested)
		self.buttonCancel.show()
		
		self.buttonConfirm = TBUT.createActionButton(self.inputWindow, 4, 2 + len(textList), 'Confirmer', 'Normal')
		self.buttonConfirm.clicked.connect(self.confirmRequested)
		self.buttonConfirm.show()
		
#		buttonShow.clicked.connect(self.createTracksView)	

	def cancelRequested(self):
		self.inputWindow.hide()
		self.resultFunction(False, [])
	
	def confirmRequested(self):
		self.inputWindow.hide()
		self.resultFunction(True, [_.text() for _ in self.textButtonList])


# ========================================================================================
# --- THE END ---
# ========================================================================================
			