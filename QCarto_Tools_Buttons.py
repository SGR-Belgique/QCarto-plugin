# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Styles des Boutons et autres dans le Menu
# ========================================================================================


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qgis.core import *
from qgis.gui import *
from qgis.PyQt import QtWidgets

import importlib

import QCarto_Definitions_Styles as DSTY
importlib.reload(DSTY)


# ========================================================================================
# Petits Boutons Carrés
# >>> groupBox : parent Widget
# >>> x        : horizontal position, from 1
# >>> y        : vertical position, from 1
# >>> pos      : horizontal place : 1, 2 or 3
# >>> size     : "Normal" "Short" 
# ========================================================================================

class squareLabelButton:

	def __init__(self, groupBox, x, y, pos, size):
		self.labelButton = QtWidgets.QLabel(groupBox)
		DSTY.moveButton(self.labelButton, x, y, size)
		self.labelButton.move(self.labelButton.x() + 3 + (self.labelButton.width() / 5) * (pos - 1) * 2, self.labelButton.y() + 3)
		self.labelButton.resize((self.labelButton.size().width() / 5) - 6, DSTY.buttonHeightNormal - 6 if size == 'Normal' else DSTY.buttonHeightShort - 6)

	def setColor(self, color):
		style = "QLabel {"
		style += "border: 1px solid black;"
		style += "background-color: " + DSTY.colorToHtmlHex(color.rgb()) + ";"
		style += "font: bold calibri;"
		style += "color: green;"
		style += "} "
		self.labelButton.setStyleSheet(style)


# ========================================================================================
# Bouton Action : 
# >>> groupBox : parent Widget
# >>> x        : horizontal position, from 1
# >>> y        : vertical position, from 1
# >>> text     : button text
# >>> size     : "Normal" "Short" "TimeShort" 
# ========================================================================================

def createActionButton(groupBox, x, y, text, size = "Normal"):

	actionButton = QtWidgets.QPushButton(groupBox)
	DSTY.setStyleMainButtons(actionButton, size)
	DSTY.moveButton(actionButton, x, y, size)
	actionButton.setText(text)

	return actionButton

def createActionButtonTransparent(groupBox, x, y, text, size = "Normal"):

	actionButton = QtWidgets.QPushButton(groupBox)
	DSTY.setStyleMainButtons(actionButton, size)
	DSTY.setStyleMainButtonsTransparent(actionButton)
	DSTY.moveButton(actionButton, x, y, size)
	actionButton.setText('')

	return actionButton
	

# ========================================================================================
# Bouton Help : 
# >>> groupBox : parent Widget
# >>> x        : horizontal position, from 1
# >>> y        : vertical position, from 1
# >>> text     : button text
# >>> size     : "Normal" "Short" "TimeShort" 
# ========================================================================================

def createHelpButton(groupBox, x, y, text, size = "Normal"):

	helpButton = QtWidgets.QPushButton(groupBox)
	DSTY.setStyleHelpButtons(helpButton, size)
	DSTY.moveButton(helpButton, x, y, size)
	helpButton.setText(text)

	return helpButton


# ========================================================================================
# Bouton Label : Black Text 
# >>> groupBox : parent Widget
# >>> x        : horizontal position, from 1
# >>> y        : vertical position, from 1
# >>> text     : button text
# >>> size     : "Normal" "Short" "TimeShort" 
# >>> position : "Right"  //  "Center"
# ========================================================================================

def createLabelBlackButton(groupBox, x, y, text, size = "Normal", position = "Right"):

	labelButton = QtWidgets.QLabel(groupBox)
	DSTY.setStyleBlackLabel(labelButton, size)
	DSTY.moveButton(labelButton, x, y, size)
	if position == "Center":
		textLabel = DSTY.textFormatBlackLabelCenter.replace("%TEXT%",text)
	elif position == "Left":
		textLabel = DSTY.textFormatBlackLabelLeft.replace("%TEXT%",text)
	else:
		textLabel = DSTY.textFormatBlackLabel.replace("%TEXT%",text)
	labelButton.setText(textLabel)

	return labelButton
	

# ========================================================================================
# Bouton Label : Green Style / Yellow if Warning / Red if Error
# >>> groupBox : parent Widget
# >>> x        : horizontal position, from 1
# >>> y        : vertical position, from 1
# >>> text     : button text
# >>> size     : "Normal" "Short" "TimeShort" 
# >>> font	   : "Normal" "Small"
# ========================================================================================

def createLabelGreenButton(groupBox, x, y, text, size = 'Normal', font = 'Normal'):

	labelButton = QtWidgets.QLabel(groupBox)
	if font == 'Normal' : DSTY.setStyleGreenLabel(labelButton, size)
	if font == 'Small' : DSTY.setStyleGreenLabelSmall(labelButton, size)
	if font == 'VerySmall' : DSTY.setStyleGreenLabelVerySmall(labelButton, size)
	DSTY.moveButton(labelButton, x, y, size)
	textLabel = DSTY.textFormatBlackSmall.replace("%TEXT%",text)
	labelButton.setText(textLabel)

	return labelButton


# ========================================================================================
# Bouton Combo Box
# >>> groupBox : parent Widget
# >>> x        : horizontal position, from 1
# >>> y        : vertical position, from 1
# >>> size     : "Normal" "Short" "TimeShort" 
# ========================================================================================

def createComboButton(groupBox, x, y, size = "Normal"):

	comboButton = QtWidgets.QComboBox(groupBox)
	DSTY.setStyleComboBox(comboButton, size)
	DSTY.moveButton(comboButton, x, y, size)

	return comboButton


# ========================================================================================
# Bouton Check Box
# >>> groupBox : parent Widget
# >>> x        : horizontal position, from 1
# >>> y        : vertical position, from 1
# >>> text     : button text
# >>> size     : "Normal" "Short" "TimeShort" 
# ========================================================================================

def createCheckBoxButton(groupBox, x, y, text, size = "Normal"):

	checkBoxButton = QtWidgets.QCheckBox(text, groupBox)

	DSTY.setStyleCheckBox(checkBoxButton, size)
	DSTY.moveButton(checkBoxButton, x, y, size)

	return checkBoxButton


# ========================================================================================
# Bouton Radio Box
# >>> groupBox : parent Widget
# >>> x        : horizontal position, from 1
# >>> y        : vertical position, from 1
# >>> text     : button text
# >>> size     : "Normal" "Short" "TimeShort" 
# ========================================================================================

def createRadioBoxButton(groupBox, x, y, text, size = "Normal"):

	radioBoxButton = QtWidgets.QRadioButton(text, groupBox)
	DSTY.setStyleRadioBox(radioBoxButton, size)
	DSTY.moveButton(radioBoxButton, x, y, size)

	return radioBoxButton


# ========================================================================================
# Bouton Input Box
# >>> groupBox : parent Widget
# >>> x        : horizontal position, from 1
# >>> y        : vertical position, from 1
# >>> size     : "Normal" "Short" "TimeShort" 
# ========================================================================================

def createInputButton(groupBox, x, y, size = "Normal"):

	inputButton = QtWidgets.QLineEdit(groupBox)
	DSTY.setStyleLineEdit(inputButton, size)
	DSTY.moveButton(inputButton, x, y, size)

	return inputButton


# ========================================================================================
# Bouton Input Date
# >>> groupBox : parent Widget
# >>> x        : horizontal position, from 1
# >>> y        : vertical position, from 1
# >>> size     : "Normal" "Short" "TimeShort" 
# ========================================================================================

def createInputDateButton(groupBox, x, y, size = 'Normal'):

	inputDateButton = QtWidgets.QDateTimeEdit(QDate.currentDate(), groupBox)
	inputDateButton.setDisplayFormat('yyyy.MM.dd')
	inputDateButton.setCalendarPopup(True)
	
	DSTY.setStyleLDatedit(inputDateButton, size)
	DSTY.moveButton(inputDateButton, x, y, size)

	return inputDateButton


# ========================================================================================
# The End
# ========================================================================================
