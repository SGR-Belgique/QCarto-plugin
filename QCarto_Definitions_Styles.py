# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Styles des Boutons et autres dans les Menus
# ========================================================================================


from PyQt5.QtCore import *
from PyQt5.QtGui import *
from qgis.core import *
from qgis.gui import *

import importlib

import QCarto_Definitions_Colors as DCOL
importlib.reload(DCOL)


# ========================================================================================
# Définition de la taille des boutons et des Fontes
# ========================================================================================

# Dimensions du grid	

gridElementWidth = 150
gridElementHeight = 30
gridElementMargin = 10

gridElementWidthCompact = 110
gridElementHeightCompact = 30
gridElementMarginCompact = 10

gridElementWidthCompact3_2 = 100
gridElementHeightCompact3_2 = 30
gridElementMarginCompact3_2 = 10

gridElementWidthShort = 120
gridElementHeightShort = 25
gridElementMarginShort = 5

# Dimensions des boutons

buttonWidthNormal = 120
buttonHeightNormal = 25

buttonWidthCompact = 80
buttonHeightCompact = 25

buttonWidthCompact3_2 = 70
buttonHeightCompact3_2 = 25

buttonWidthShort = 100
buttonHeightShort = 20

buttonMarginNormal = 8
buttonMarginShort = 5

buttonWidthShortHalf = 40
buttonWidthShortDouble = 220
buttonWidthShortTriple = 340
buttonWidthShortQuadruple = 460
buttonWidthShortPenta  = 580

buttonWidthDouble = buttonWidthNormal + gridElementWidth
buttonWidthDouble3 = buttonWidthNormal + 2 * gridElementWidth
buttonWidthDouble4 = buttonWidthNormal + 3 * gridElementWidth


# Fontes

buttonFontSizeNormal = 14
buttonFontSizeShort = 12
buttonFontSizeTimeShort = 12
buttonFontSizeActive = 14
buttonFontSizeLabel = 13
buttonFontSizeLabelBoxNormal = 13
buttonFontSizeLabelBoxSmall = 11
buttonFontSizeLabelBoxVerySmall = 9

buttonFontSizeCheckBoxNormal = 13
buttonFontSizeCheckBoxSmall = 11

buttonFontSizeRadiokBoxNormal = 13
buttonFontSizeRadioBoxSmall = 11

tableItemFontSize = 12
tableItemFontSizeSmall = 11


# ========================================================================================
# Html Hex Convert
# ========================================================================================

def colorToHtmlHex(color):
	return '#' + ('000000' + hex(color).replace('0x',''))[-6:]


# ========================================================================================
# Définition du style pour tous les cadres internes 
# ========================================================================================

styleBox = "QGroupBox {"
styleBox += "margin-top: 0.5em;"
styleBox += "border: 2px solid black;"
styleBox += "border-radius: 5px;"
styleBox += "font: bold 16px calibri"
styleBox += "} " 
styleBox += "QGroupBox:title {"
styleBox += "top: -13px; left: 10px"
styleBox += "} "

styleHiddenBox = "QGroupBox {"
styleHiddenBox += "border: 0px solid black;"
styleHiddenBox += "font: bold 16px calibri"
styleHiddenBox += "} " 


# ========================================================================================
# Style des boutons principaux
# ========================================================================================

styleMain = "QPushButton {"
styleMain += "background-color: " + colorToHtmlHex(DCOL.bgButtonNormal.rgb()) + ";"
styleMain += "color: white;"
styleMain += "border: 1px solid black;"
styleMain += "border-radius: 5px;"
styleMain += "font: bold calibri"
styleMain += "} " 

styleMainWarning = "QPushButton {"
styleMainWarning += "background-color: " + colorToHtmlHex(DCOL.bgButtonWarning.rgb()) + ";"
styleMainWarning += "color: white;"
styleMainWarning += "border: 1px solid black;"
styleMainWarning += "border-radius: 5px;"
styleMainWarning += "font: bold calibri"
styleMainWarning += "} " 

styleMainActive = "QPushButton {"
styleMainActive += "background-color: " + colorToHtmlHex(DCOL.bgButtonActive.rgb()) + ";"
styleMainActive += "color: black;"
styleMainActive += "border: 1px solid black;"
styleMainActive += "border-radius: 5px;"
styleMainActive += "font: bold calibri"
styleMainActive += "} " 

styleMainInactive = "QPushButton {"
styleMainInactive += "background-color: " + colorToHtmlHex(DCOL.bgButtonInactive.rgb()) + ";"
styleMainInactive += "color: white;"
styleMainInactive += "border: 1px solid black;"
styleMainInactive += "border-radius: 5px;"
styleMainInactive += "font: bold calibri"
styleMainInactive += "} " 

styleMainStrong = "QPushButton {"
styleMainStrong += "background-color: " + colorToHtmlHex(DCOL.bgButtonNormalStrong.rgb()) + ";"
styleMainStrong += "color: white;"
styleMainStrong += "border: 1px solid black;"
styleMainStrong += "border-radius: 5px;"
styleMainStrong += "font: bold calibri"
styleMainStrong += "} " 

styleMainInfo = "QPushButton {"
styleMainInfo += "background-color: " + colorToHtmlHex(DCOL.bgButtonInfo.rgb()) + ";"
styleMainInfo += "color: black;"
styleMainInfo += "border: 1px solid black;"
styleMainInfo += "border-radius: 5px;"
styleMainInfo += "font: bold calibri"
styleMainInfo += "} " 

styleMainTransparent = "QPushButton {"
styleMainTransparent += "background: none;" 
styleMainTransparent += "color: white;"
styleMainTransparent += "border: none;"
styleMainTransparent += "font: bold calibri"
styleMainTransparent += "} " 


# ========================================================================================
# Style des boutons combo
# ========================================================================================

styleComboNormal = "QComboBox {"
styleComboNormal += "border: 1px solid black;"
styleComboNormal += "background-color: " + colorToHtmlHex(DCOL.bgComboNormal.rgb()) + ";"
styleComboNormal += "font: calibri;"
styleComboNormal += "padding-left: 10px"
styleComboNormal += "} "

styleComboWarning = "QComboBox {"
styleComboWarning += "border: 1px solid black;"
styleComboWarning += "background-color: " + colorToHtmlHex(DCOL.bgComboWarning.rgb()) + ";"
styleComboWarning += "font: calibri;"
styleComboWarning += "padding-left: 10px"
styleComboWarning += "} "

styleComboInfo = "QComboBox {"
styleComboInfo += "border: 1px solid black;"
styleComboInfo += "background-color: " + colorToHtmlHex(DCOL.bgComboInfo.rgb()) + ";"
styleComboInfo += "font: calibri;"
styleComboInfo += "padding-left: 10px"
styleComboInfo += "} "

styleComboInfoInit = "QComboBox {"
styleComboInfoInit += "border: 1px solid black;"
styleComboInfoInit += "background-color: " + colorToHtmlHex(DCOL.bgComboInfoInit.rgb()) + ";"
styleComboInfoInit += "font: calibri;"
styleComboInfoInit += "padding-left: 10px"
styleComboInfoInit += "} "


# ========================================================================================
# Style des check boxes
# ========================================================================================

styleCheckBoxNormal = "QCheckBox {"
styleCheckBoxNormal += "border: 1px solid black;"
styleCheckBoxNormal += "background-color: " + colorToHtmlHex(DCOL.bgCheckBoxNormal.rgb()) + ";"
styleCheckBoxNormal += "font: calibri;"
styleCheckBoxNormal += "padding-left: 10px"
styleCheckBoxNormal += "} "


# ========================================================================================
# Style des Radio Buttons
# ========================================================================================

styleRadioBoxNormal = "QRadioButton {"
styleRadioBoxNormal += "border: 1px solid black;"
styleRadioBoxNormal += "background-color: " + colorToHtmlHex(DCOL.bgRadioBoxNormal.rgb()) + ";"
styleRadioBoxNormal += "font: calibri;"
styleRadioBoxNormal += "padding-left: 10px"
styleRadioBoxNormal += "} "


# ========================================================================================
# Définition du style des textes
# ========================================================================================

textFormatBlackNormal = "<p><b><font color='" + colorToHtmlHex(DCOL.txtNormal.rgb()) + "'><center>%TEXT%</center></b></p>"
textFormatBlackNormalLeft = "<p style='text-align:left'><b><font color='" + colorToHtmlHex(DCOL.txtNormal.rgb()) + "'>%TEXT%</b></p>"
textFormatBlackSmall = "<p><<font color='" + colorToHtmlHex(DCOL.txtNormal.rgb()) + "'><center>%TEXT%</center></p>"
textFormatBlackCombo = "<p><b><font color='" + colorToHtmlHex(DCOL.txtNormal.rgb()) + "'><center>%TEXT%</center></b></p>"
textFormatBlackLabel = "<p style='text-align:right'><font color='" + colorToHtmlHex(DCOL.txtNormal.rgb()) + "'>%TEXT%</p>"
textFormatBlackLabelCenter = "<p style='text-align:center'><font color='" + colorToHtmlHex(DCOL.txtNormal.rgb()) + "'>%TEXT%</p>"
textFormatBlackLabelLeft = "<p style='text-align:left'><font color='" + colorToHtmlHex(DCOL.txtNormal.rgb()) + "'>%TEXT%</p>"
textFormatBlackLabelLeftBold = "<p style='text-align:left'><b><font color='" + colorToHtmlHex(DCOL.txtNormal.rgb()) + "'>%TEXT%</b></p>"
textFormatGreenNormal = "<p><b><font color='" + colorToHtmlHex(DCOL.txtGreen.rgb()) + "'><center>%TEXT%</center></b></p>"
textFormatGreenSmall = "<p><<font color='" + colorToHtmlHex(DCOL.txtGreen.rgb()) + "'><center>%TEXT%</center></p>"
textFormatRedNormal = "<p><b><font color='" + colorToHtmlHex(DCOL.txtRed.rgb()) + "'><center>%TEXT%</center></b></p>"
textFormatRedNormalLeft = "<p style='text-align:left'><b><font color='" + colorToHtmlHex(DCOL.txtRed.rgb()) + "'>%TEXT%</b></p>"
textFormatRedSmall = "<p><<font color='" + colorToHtmlHex(DCOL.txtRed.rgb()) + "'><center>%TEXT%</center></p>"
textFormatOrangeNormal = "<p><b><font color='" + colorToHtmlHex(DCOL.txtOrange.rgb()) + "'><center>%TEXT%</center></b></p>"

textFormatBlackRight = "<p style=\"text-align:right;\"><b><font color='" + colorToHtmlHex(DCOL.txtNormal.rgb()) + "'>%TEXT%</b></p>"


# ========================================================================================
# Définition des styles pour Status
# ========================================================================================

textFormatStatusError = "<p style='font-size:14px'><b><font color='" + colorToHtmlHex(DCOL.txtNormal.rgb()) + "'><center>%TEXT%</center></b></p>"
textFormatStatusWarning = "<p style='font-size:14px'><b><font color='" + colorToHtmlHex(DCOL.txtNormal.rgb()) + "'><center>%TEXT%</center></b></p>"
textFormatStatusWorking = "<p style='font-size:14px'><b><font color='" + colorToHtmlHex(DCOL.txtNormal.rgb()) + "'><center>%TEXT%</center></b></p>"
textFormatStatusInfo = "<p style='font-size:14px'><b><font color='" + colorToHtmlHex(DCOL.txtNormal.rgb()) + "'><center>%TEXT%</center></b></p>"
textFormatStatusOk = "<p style='font-size:14px'><b><font color='" + colorToHtmlHex(DCOL.txtNormal.rgb()) + "'><center>%TEXT%</center></b></p>"

textFormatStatusErrorSmall = "<p style='font-size:11px'><b><font color='" + colorToHtmlHex(DCOL.txtNormal.rgb()) + "'><center>%TEXT%</center></b></p>"
textFormatStatusWarningSmall = "<p style='font-size:11px'><b><font color='" + colorToHtmlHex(DCOL.txtNormal.rgb()) + "'><center>%TEXT%</center></b></p>"
textFormatStatusWorkingSmall = "<p style='font-size:11px'><b><font color='" + colorToHtmlHex(DCOL.txtNormal.rgb()) + "'><center>%TEXT%</center></b></p>"
textFormatStatusOkSmall = "<p style='font-size:11px'><b><font color='" + colorToHtmlHex(DCOL.txtNormal.rgb()) + "'><center>%TEXT%</center></b></p>"

styleStatusError = "QLabel {border: 1px solid black; background-color: " + colorToHtmlHex(DCOL.bgStatusError.rgb()) + ";}"
styleStatusWarning = "QLabel {border: 1px solid black; background-color: " + colorToHtmlHex(DCOL.bgStatusWarning.rgb()) + ";}"
styleStatusWorking = "QLabel {border: 1px solid black; background-color: " + colorToHtmlHex(DCOL.bgStatusWorking.rgb()) + ";}"
styleStatusDone = "QLabel {border: 1px solid black; background-color: " + colorToHtmlHex(DCOL.bgStatusDone.rgb()) + ";}"
styleStatusInfo = "QLabel {border: 1px solid black; background-color: " + colorToHtmlHex(DCOL.bgStatusInfo.rgb()) + ";}"
styleStatusOk = "QLabel {border: 1px solid black; background-color: " + colorToHtmlHex(DCOL.bgStatusOk.rgb()) + ";}"


# ========================================================================================
# Définir la géométrie d'un cadre en fontion de sa position dans le menu principal
# Voir Tableur : Tableau de Bord.xlsx
# >>> box 	: widget box
# >>> x   	: left position of box, from 1 to 8
# >>> y   	: top position of box, from 1 to 28
# >>> w   	: width of box
# >>> h   	: height of box
# >>> t		: table inside Flag (false by default) - used for embedded table
# ========================================================================================

def setBoxGeometry(box, x, y, w, h, t = False):
	xPos = gridElementMargin + gridElementWidth * (x-1)
	yPos = gridElementMargin + gridElementHeight * (y-1)
	width = gridElementWidth * w - gridElementMargin
	height = gridElementHeight * (h + 1) - gridElementMargin
	if not t:
		box.setGeometry(xPos,yPos,width, height)
	else:
		box.setGeometry(xPos+buttonMarginNormal,yPos + 25,width - 2 * buttonMarginNormal, height-35)
	
def setBoxGeometryShort(box, x, y, w, h, t = False):
	xPos = gridElementMarginShort + gridElementWidthShort * (x-1)
	yPos = gridElementMarginShort + gridElementHeightShort * (y-1)
	width = gridElementWidthShort * w - gridElementMarginShort
	height = gridElementHeightShort * (h + 1) - gridElementMarginShort
	if not t:
		box.setGeometry(xPos,yPos,width, height)
	else:
		box.setGeometry(xPos+buttonMarginNormal,yPos + 25,width - 2 * buttonMarginNormal, height-35)
	
def setWindowGeometry(window, x, y, w, h):
	xPos = x
	yPos = y
	width = gridElementWidth * w + gridElementMargin
	height = gridElementHeight * h + gridElementMargin
	window.setGeometry(xPos, yPos, width, height + 30)
	

# ========================================================================================
# Positionner le bouton dans son cadre.
# >>> button	: widget button
# >>> x   		: left position of button, from 1
# >>> y   		: top position of button, from 1
# ========================================================================================
		
def moveButton(button, x, y, mode = "Normal"):

	if mode in ('Normal', 'TimeShort', 'Double', 'Double3', 'Double4'):
		button.move(round(gridElementMargin + gridElementWidth * (x-1)), round(gridElementMargin + buttonMarginNormal + gridElementHeight * (y-1)))
	if mode in ('Short', 'ShortDouble', "ShortTriple", "ShortQuadruple", "ShortPenta"):
		button.move(round(gridElementMarginShort + gridElementWidthShort * (x-1)), round(gridElementMargin + buttonMarginNormal + gridElementHeightShort * (y-1)))
	if mode == "ShortHalf":
		button.move(round(gridElementMargin + int((gridElementWidth/3)) * (x-1)), round(gridElementMargin + buttonMarginNormal + gridElementHeight * (y-1)))
	if mode == 'Compact':
		button.move(round(gridElementMarginCompact + gridElementWidth + gridElementWidthCompact * (x-2)), round(gridElementMarginCompact + buttonMarginNormal + gridElementHeightCompact * (y-1)))
	if mode == 'Compact3_2':
		button.move(round(gridElementMarginCompact3_2 + gridElementWidthCompact3_2 * (x-1)), round(gridElementMarginCompact3_2 + buttonMarginNormal + gridElementHeightCompact3_2 * (y-1)))


# ========================================================================================
# Tailler et positionner le grand Label Status
# >>> buttonLabel	: widget button
# >>> w				: int							Taille - en nombre d'éléments - du label
# >>> mode 			: str							Defaut = 'Normal'
# >>> x 			: int							Position X du label. Defaut = 1
# ========================================================================================

def setStatusLabel(buttonLabel, w, mode = 'Normal', x = 1):

	moveButton(buttonLabel, x, 1, mode)
	if mode in ('Normal'):
		buttonLabel.resize(buttonWidthNormal + (w-1) * gridElementWidth, buttonHeightNormal)
	if mode in ('Short', 'ShortDouble', "ShortTriple"):
		buttonLabel.resize(buttonWidthShort + (w-1) * gridElementWidthShort, buttonHeightShort)
	buttonLabel.setStyleSheet("QLabel {border: 1px solid black;}")


# ========================================================================================
# Appliquer le style des boutons principaux
# ========================================================================================

def setStyleMainButtons(button, mode = "Normal"):

	font = QFont()
	if mode == "Normal":
		font.setPixelSize(buttonFontSizeNormal)
	if mode == "Short":
		font.setPixelSize(buttonFontSizeShort)

	button.setStyleSheet(styleMain)
	button.setFont(font)
	if mode == "Normal":
		button.resize(buttonWidthNormal,buttonHeightNormal)
	if mode == "Short":
		button.resize(buttonWidthShort,buttonHeightShort)
	if mode == "Double":
		button.resize(buttonWidthDouble,buttonHeightNormal)
	if mode == "ShortHalf":
		button.resize(buttonWidthShortHalf,buttonHeightShort)
	if mode == "ShortTriple":
		button.resize(buttonWidthShortTriple,buttonHeightShort)

def setStyleNormalButton(button):
	button.setStyleSheet(styleMain)
	
def setStyleWarningButton(button):
	button.setStyleSheet(styleMainWarning)
	
def setStyleActiveButton(button):
	button.setStyleSheet(styleMainActive)
	
def setStyleNormalStrongButton(button):
	button.setStyleSheet(styleMainStrong)
	
def setStyleInfoButton(button):
	button.setStyleSheet(styleMainInfo)
	
def setStyleMainButtonsInactive(button):
	button.setStyleSheet(styleMainInactive)

def setStyleMainButtonsTransparent(button):
	button.setStyleSheet(styleMainTransparent)


# ========================================================================================
# Appliquer le style d'une barre de progres
# ========================================================================================
	
def setStyleProgressBar(button, mode = "Normal"):

	style = "QProgressBar {"
	style += "color: white;"
	style += "background: #C0C0C0;"
	style += "text-align: center;"
	style += "QProgressBar::chunk { background-color: green }"

	font = QFont()
	font.setPixelSize(buttonFontSizeNormal)

	button.setStyleSheet(style)
	button.setFont(font)
	if mode == "Normal":
		button.resize(buttonWidthNormal,buttonHeightNormal)
	if mode == "Short":
		button.resize(buttonWidthShort,buttonHeightShort)
	if mode == "Double":
		button.resize(buttonWidthDouble,buttonHeightNormal)
	if mode == "ShortHalf":
		button.resize(buttonWidthShortHalf,buttonHeightShort)
	if mode == "ShortTriple":
		button.resize(buttonWidthShortTriple,buttonHeightShort)


# ========================================================================================
# Appliquer le style des boutons projets
# ========================================================================================
	
def setStyleProjectButtons(button):

	style = "QPushButton {"
	style += "background-color: " + colorToHtmlHex(DCOL.bgButtonProjectNormal.rgb()) + ";"
	style += "color: black;"
	style += "border: 1px solid black;"
	style += "border-radius: 5px;"
	style += "font: calibri"
	style += "} " 

	font = QFont()
	font.setPixelSize(buttonFontSizeNormal)

	button.setStyleSheet(style)
	button.setFont(font)
	button.resize(buttonWidthNormal,buttonHeightNormal)

def setStyleProjectActiveButton(button):

	style = "QPushButton {"
	style += "background-color: " + colorToHtmlHex(DCOL.bgButtonActive.rgb()) + ";"
	style += "color: black;"
	style += "border: 1px solid black;"
	style += "border-radius: 5px;"
	style += "font: bold calibri"
	style += "} " 

	font = QFont()
	font.setPixelSize(buttonFontSizeActive)

	button.setStyleSheet(style)
	button.setFont(font)
	button.resize(buttonWidthNormal,buttonHeightNormal)
	

# ========================================================================================
# Appliquer le style des boutons cartes
# ========================================================================================
	
def setStyleMapButtons(button, mode = "Normal"):

	style = "QPushButton {"
	style += "background-color: " + colorToHtmlHex(DCOL.bgButtonProjectNormal.rgb()) + ";"
	style += "color: black;"
	style += "border: 1px solid black;"
	style += "border-radius: 5px;"
	style += "font: calibri"
	style += "} " 

	font = QFont()
	font.setPixelSize(buttonFontSizeNormal)

	button.setStyleSheet(style)
	button.setFont(font)
	
	if mode == "Normal":
		button.resize(buttonWidthNormal,buttonHeightNormal)
	if mode == "Short":
		button.resize(buttonWidthShort,buttonHeightShort)
	
def setStyleMapActiveButton(button, mode = "Normal"):

	style = "QPushButton {"
	style += "background-color: " + colorToHtmlHex(DCOL.bgButtonActive.rgb()) + ";"
	style += "color: black;"
	style += "border: 1px solid black;"
	style += "border-radius: 5px;"
	style += "font: bold calibri"
	style += "} " 

	font = QFont()
	font.setPixelSize(buttonFontSizeActive)

	button.setStyleSheet(style)
	button.setFont(font)

	if mode == "Normal":
		button.resize(buttonWidthNormal,buttonHeightNormal)
	if mode == "Short":
		button.resize(buttonWidthShort,buttonHeightShort)


# ========================================================================================
# Appliquer le style des Combo Box
# ========================================================================================

def setStyleComboBox(combo, mode = "Normal"):

	font = QFont()
	font.setPixelSize(11)

	combo.setStyleSheet(styleComboNormal)
	combo.setFont(font)
	if mode == "Normal":
		combo.resize(buttonWidthNormal,buttonHeightNormal)
	if mode == "Short":
		combo.resize(buttonWidthShort,buttonHeightShort)
	if mode == "ShortHalf":
		combo.resize(buttonWidthShortHalf,buttonHeightShort)
	if mode == "ShortDouble":
		combo.resize(buttonWidthShortDouble,buttonHeightShort)
	if mode == "ShortTriple":
		combo.resize(buttonWidthShortTriple,buttonHeightShort)
	if mode == "ShortQuadruple":
		combo.resize(buttonWidthShortQuadruple,buttonHeightShort)
	if mode == "Double":
		combo.resize(buttonWidthDouble,buttonHeightNormal)
	if mode == "Double3":
		combo.resize(buttonWidthDouble3,buttonHeightNormal)
	if mode == "Double4":
		combo.resize(buttonWidthDouble4,buttonHeightNormal)
	
def setComboBoxOk(combo):
	combo.setStyleSheet(styleComboNormal)

def setComboBoxWarning(combo):
	combo.setStyleSheet(styleComboWarning)

def setComboBoxInfo(combo):
	combo.setStyleSheet(styleComboInfo)

def setComboBoxInfoInit(combo):
	combo.setStyleSheet(styleComboInfoInit)


# ========================================================================================
# Appliquer le style des Check Box
# ========================================================================================

def setStyleCheckBox(checkBox, mode = "Normal"):

	font = QFont()
	if mode == "Normal":
		font.setPixelSize(buttonFontSizeCheckBoxNormal)
	if mode == "Short":
		font.setPixelSize(buttonFontSizeCheckBoxSmall)
	font.setBold(True)

	checkBox.setStyleSheet(styleCheckBoxNormal)
	checkBox.setFont(font)
	if mode == "Normal":
		checkBox.resize(buttonWidthNormal,buttonHeightNormal)
	if mode == "Short":
		checkBox.resize(buttonWidthShort,buttonHeightShort)
	if mode == "ShortHalf":
		checkBox.resize(buttonWidthShortHalf,buttonHeightShort)
	if mode == "ShortDouble":
		checkBox.resize(buttonWidthShortDouble,buttonHeightShort)
	if mode == "ShortTriple":
		checkBox.resize(buttonWidthShortTriple,buttonHeightShort)
	if mode == "Double":
		checkBox.resize(buttonWidthDouble,buttonHeightNormal)
	

# ========================================================================================
# Appliquer le style des Radio Buttons
# ========================================================================================

def setStyleRadioBox(radioBox, mode = "Normal"):

	font = QFont()
	if mode == "Normal":
		font.setPixelSize(buttonFontSizeRadiokBoxNormal)
	if mode == "Short":
		font.setPixelSize(buttonFontSizeRadioBoxSmall)
	font.setBold(True)

	radioBox.setStyleSheet(styleCheckBoxNormal)
	radioBox.setFont(font)
	if mode == "Normal":
		radioBox.resize(buttonWidthNormal,buttonHeightNormal)
	if mode == "Double":
		radioBox.resize(buttonWidthDouble,buttonHeightNormal)
	if mode == "Short":
		radioBox.resize(buttonWidthShort,buttonHeightShort)
	if mode == "ShortHalf":
		radioBox.resize(buttonWidthShortHalf,buttonHeightShort)
	if mode == "ShortDouble":
		radioBox.resize(buttonWidthShortDouble,buttonHeightShort)
	if mode == "ShortTriple":
		radioBox.resize(buttonWidthShortTriple,buttonHeightShort)
	if mode == "Compact":
		radioBox.resize(buttonWidthCompact,buttonHeightCompact)
	if mode == "Compact3_2":
		radioBox.resize(buttonWidthCompact3_2,buttonHeightCompact3_2)
	

# ========================================================================================
# Appliquer le style des QInputDialog 
# ========================================================================================

def setStyleLineEdit(inputBox, mode = "Normal"):

	style = "QLineEdit {"
	style += "border: 1px solid black;"
	style += "background-color: " + colorToHtmlHex(DCOL.bgLineEdit.rgb()) + ";"
	style += "font: calibri;"
	style += "padding-left: 10px"
	style += "} "

	font = QFont()
	font.setPixelSize(11)

	inputBox.setStyleSheet(style)
	inputBox.setFont(font)
	if mode == "Normal":
		inputBox.resize(buttonWidthNormal,buttonHeightNormal)
	if mode == "Short":
		inputBox.resize(buttonWidthShort,buttonHeightShort)
	if mode == "ShortHalf":
		inputBox.resize(buttonWidthShortHalf,buttonHeightShort)
	if mode == "ShortDouble":
		inputBox.resize(buttonWidthShortDouble,buttonHeightShort)
	if mode == "ShortTriple":
		inputBox.resize(buttonWidthShortTriple,buttonHeightShort)
	if mode == "ShortPenta":
		inputBox.resize(buttonWidthShortPenta,buttonHeightShort)
	if mode == "Double":
		inputBox.resize(buttonWidthDouble,buttonHeightNormal)
	if mode == "Double3":
		inputBox.resize(buttonWidthDouble3,buttonHeightNormal)
	if mode == "Double4":
		inputBox.resize(buttonWidthDouble4,buttonHeightNormal)


# ========================================================================================
# Appliquer le style des QDateTimeEdit 
# ========================================================================================

def setStyleLDatedit(inputDateBox, mode = 'Normal'):

	style = "QDateTimeEdit {"
	style += "border: 1px solid black;"
	style += "background-color: " + colorToHtmlHex(DCOL.bgLineEdit.rgb()) + ";"
	style += "font: calibri;"
	style += "padding-left: 10px"
	style += "} "

	font = QFont()
	font.setPixelSize(11)

	inputDateBox.setStyleSheet(style)
	inputDateBox.setFont(font)
	if mode == 'Normal':
		inputDateBox.resize(buttonWidthNormal,buttonHeightNormal)
	if mode == 'Double':
		inputDateBox.resize(buttonWidthDouble,buttonHeightNormal)
	if mode == 'Double3':
		inputDateBox.resize(buttonWidthDouble3,buttonHeightNormal)
	if mode == 'Double4':
		inputDateBox.resize(buttonWidthDouble4,buttonHeightNormal)


# ========================================================================================
# Appliquer le style des boutons d'aide
# ========================================================================================

def setStyleHelpButtons(button, mode = "Normal"):

	style = "QPushButton {"
	style += "background-color: " + colorToHtmlHex(DCOL.bgButtonHelp.rgb()) + ";"
	style += "color: black;"
	style += "border: 1px solid black;"
	style += "border-radius: 5px;"
	style += "font: calibri"
	style += "} " 

	font = QFont()
	if mode == "Normal":
		font.setPixelSize(buttonFontSizeNormal)
	if mode == "Short":
		font.setPixelSize(buttonFontSizeShort)

	button.setStyleSheet(style)
	button.setFont(font)
	if mode == "Normal":
		button.resize(buttonWidthNormal,buttonHeightNormal)
	if mode == "Short":
		button.resize(buttonWidthShort,buttonHeightShort)
	if mode == "ShortHalf":
		button.resize(buttonWidthShortHalf,buttonHeightShort)
	if mode == "ShortDouble":
		button.resize(buttonWidthShortDouble,buttonHeightShort)
	if mode == "ShortTriple":
		button.resize(buttonWidthShortTriple,buttonHeightShort)

	
# ========================================================================================
# Définition du Style des Labels en Noir sans Cadre
# ========================================================================================
	
def setStyleBlackLabel(label, mode = "Normal"):

	style = "QLabel {"
	style += "border: none;"
	style += "font: calibri;"
	style += "color: black;"
	style += "} "

	font = QFont()
	font.setPixelSize(buttonFontSizeLabel)

	label.setStyleSheet(style)
	label.setFont(font)
	label.setTextFormat(1)
	if mode == "Normal":
		label.resize(buttonWidthNormal,buttonHeightNormal)
	if mode == "Short":
		label.resize(buttonWidthShort,buttonHeightShort)
	if mode == "ShortDouble":
		label.resize(buttonWidthShortDouble,buttonHeightShort)
	if mode == "ShortTriple":
		label.resize(buttonWidthShortTriple,buttonHeightShort)
	if mode == "Double":
		label.resize(buttonWidthDouble,buttonHeightNormal)
	if mode == "Double3":
		label.resize(buttonWidthDouble3,buttonHeightNormal)
	if mode == "Double4":
		label.resize(buttonWidthDouble4,buttonHeightNormal)
	if mode == "ShortHalf":
		label.resize(buttonWidthShortHalf,buttonHeightShort)

	
# ========================================================================================
# Définition du Style des Labels en Vert
# ========================================================================================
	
def setStyleGreenLabel(label, mode = "Normal"):

	style = "QLabel {"
	style += "border: 1px solid black;"
	style += "background-color: " + colorToHtmlHex(DCOL.bgLabelNormal.rgb()) + ";"
	style += "font: bold calibri;"
	style += "color: green;"
	style += "} "

	font = QFont()
	if mode == "Normal":
		font.setPixelSize(buttonFontSizeLabelBoxNormal)
	if mode == "Short":
		font.setPixelSize(buttonFontSizeLabelBoxNormal)
	if mode == "TimeShort":
		font.setPixelSize(buttonFontSizeTimeShort)

	label.setStyleSheet(style)
	label.setFont(font)
	label.setTextFormat(1)
	if mode in ('Normal', 'TimeShort'):
		label.resize(buttonWidthNormal,buttonHeightNormal)
	if mode == "Double":
		label.resize(buttonWidthDouble,buttonHeightNormal)
	if mode == "Double3":
		label.resize(buttonWidthDouble3,buttonHeightNormal)
	if mode == "Double4":
		label.resize(buttonWidthDouble4,buttonHeightNormal)
	if mode == "Short":
		label.resize(buttonWidthShort,buttonHeightShort)
	if mode == "ShortHalf":
		label.resize(buttonWidthShortHalf,buttonHeightShort)
	if mode == "ShortDouble":
		label.resize(buttonWidthShortDouble,buttonHeightShort)
	if mode == "ShortTriple":
		label.resize(buttonWidthShortTriple,buttonHeightShort)
			
def setStyleGreenLabelSmall(label, mode = "Normal"):

	setStyleGreenLabel(label, mode)
	font = QFont()
	font.setPixelSize(buttonFontSizeLabelBoxSmall)
	label.setFont(font)

def setStyleGreenLabelVerySmall(label, mode = "Normal"):

	setStyleGreenLabel(label, mode)
	font = QFont()
	font.setPixelSize(buttonFontSizeLabelBoxVerySmall)
	label.setFont(font)


# ========================================================================================
# Définition du Style des Labels d'Erreur (fond Rouge) et Warning (fond jaune)
# ========================================================================================
	
def setStyleErrorLabel(label, mode = "Normal"):

	style = "QLabel {"
	style += "border: 1px solid black;"
	style += "background-color: " + colorToHtmlHex(DCOL.bgLabelError.rgb()) + ";"
	style += "font: bold calibri;"
	style += "color: black;"
	style += "} "

	font = QFont()
	if mode == "Normal":
		font.setPixelSize(buttonFontSizeLabelBoxNormal)
	if mode == "Short":
		font.setPixelSize(buttonFontSizeLabelBoxNormal)
	if mode == "TimeShort":
		font.setPixelSize(buttonFontSizeTimeShort)

	label.setStyleSheet(style)
	label.setFont(font)
	label.setTextFormat(1)
	if mode in ('Normal', 'TimeShort'):
		label.resize(buttonWidthNormal,buttonHeightNormal)
	if mode == "Short":
		label.resize(buttonWidthShort,buttonHeightShort)
	if mode == "ShortDouble":
		label.resize(buttonWidthShortDouble,buttonHeightShort)
	if mode == "ShortTriple":
		label.resize(buttonWidthShortTriple,buttonHeightShort)
	
def setStyleErrorLabelSmall(label, mode = "Normal"):

	setStyleErrorLabel(label, mode)
	font = QFont()
	font.setPixelSize(buttonFontSizeLabelBoxSmall)
	label.setFont(font)
	
def setStyleErrorLabelVerySmall(label, mode = "Normal"):

	setStyleErrorLabel(label, mode)
	font = QFont()
	font.setPixelSize(buttonFontSizeLabelBoxVerySmall)
	label.setFont(font)
	
def setStyleErrorLabelMean(label, mode = "Normal"):

	setStyleErrorLabel(label, mode)
	font = QFont()
	font.setPixelSize(12)
	label.setFont(font)
		
def setStyleWarningLabel(label, mode = "Normal"):

	style = "QLabel {"
	style += "border: 1px solid black;"
	style += "background-color: " + colorToHtmlHex(DCOL.bgLabelWarning.rgb()) + ";"
	style += "font: bold calibri;"
	style += "color: black;"
	style += "} "

	font = QFont()
	if mode == "Normal":
		font.setPixelSize(buttonFontSizeLabelBoxNormal)
	if mode == "Short":
		font.setPixelSize(buttonFontSizeLabelBoxNormal)
	if mode == "ShortDouble":
		font.setPixelSize(buttonFontSizeLabelBoxNormal)
	if mode == "TimeShort":
		font.setPixelSize(buttonFontSizeTimeShort)

	label.setStyleSheet(style)
	label.setFont(font)
	label.setTextFormat(1)
	if mode in ('Normal', 'TimeShort'):
		label.resize(buttonWidthNormal,buttonHeightNormal)
	if mode == "Short":
		label.resize(buttonWidthShort,buttonHeightShort)
	if mode == "ShortDouble":
		label.resize(buttonWidthShortDouble,buttonHeightShort)
	if mode == "ShortTriple":
		label.resize(buttonWidthShortTriple,buttonHeightShort)
	
def setStyleWarningLabelSmall(label, mode = "Normal"):

	setStyleWarningLabel(label, mode)
	font = QFont()
	font.setPixelSize(buttonFontSizeLabelBoxSmall)
	label.setFont(font)

def setStyleWarningLabelMean(label, mode = "Normal"):

	setStyleWarningLabel(label, mode)
	font = QFont()
	font.setPixelSize(12)
	label.setFont(font)
		
	
# ========================================================================================
# Définition du Style des Labels Sans Erreur (fond Vert)
# ========================================================================================
	
def setStyleOkLabel(label, mode = 'Normal', strong = False):

	style = "QLabel {"
	style += "border: 1px solid black;"
	if not strong :	style += "background-color: " + colorToHtmlHex(DCOL.bgLabelOk.rgb()) + ";"
	if strong :		style += "background-color: " + colorToHtmlHex(DCOL.bgTableTodayStrong.rgb()) + ";"
	style += "font: bold calibri;"
	style += "color: black;"
	style += "} "

	font = QFont()
	if mode == "Normal":
		font.setPixelSize(buttonFontSizeLabelBoxNormal)
	if mode == "Short":
		font.setPixelSize(buttonFontSizeLabelBoxNormal)
	if mode == "TimeShort":
		font.setPixelSize(buttonFontSizeTimeShort)
		
	label.setStyleSheet(style)
	label.setFont(font)
	label.setTextFormat(1)
	if mode in ('Normal', 'TimeShort'):
		label.resize(buttonWidthNormal,buttonHeightNormal)
	if mode == "Short":
		label.resize(buttonWidthShort,buttonHeightShort)
	if mode == "ShortDouble":
		label.resize(buttonWidthShortDouble,buttonHeightShort)
	if mode == "ShortTriple":
		label.resize(buttonWidthShortTriple,buttonHeightShort)
	
def setStyleOkLabelSmall(label, mode = "Normal"):

	setStyleOkLabel(label, mode)
	font = QFont()
	font.setPixelSize(buttonFontSizeLabelBoxSmall)
	label.setFont(font)

def setStyleOkLabelMean(label, mode = "Normal"):

	setStyleOkLabel(label, mode)
	font = QFont()
	font.setPixelSize(12)
	label.setFont(font)
	

# ========================================================================================
# Définition du Style des Labels après Corrections
# ========================================================================================
	
def setStyleFixedLabel(label, mode = "Normal"):

	style = "QLabel {"
	style += "border: 1px solid black;"
	style += "background-color: " + colorToHtmlHex(DCOL.bgLabelFixed.rgb()) + ";"
	style += "font: bold calibri;"
	style += "color: black;"
	style += "} "

	font = QFont()
	if mode == "Normal":
		font.setPixelSize(buttonFontSizeLabelBoxNormalNormal)
	if mode == "Short":
		font.setPixelSize(buttonFontSizeLabelBoxNormalNormal)
	if mode == "TimeShort":
		font.setPixelSize(buttonFontSizeTimeShort)

	label.setStyleSheet(style)
	label.setFont(font)
	label.setTextFormat(1)
	if mode in ('Normal', 'TimeShort'):
		label.resize(buttonWidthNormal,buttonHeightNormal)
	if mode == "Short":
		label.resize(buttonWidthShort,buttonHeightShort)
	
def setStyleFixedLabelSmall(label, mode = "Normal"):

	setStyleFixedLabel(label, mode)
	font = QFont()
	font.setPixelSize(buttonFontSizeLabelBoxSmall)
	label.setFont(font)

def setStyleFixedLabelMean(label, mode = "Normal"):

	setStyleFixedLabel(label, mode)
	font = QFont()
	font.setPixelSize(12)
	label.setFont(font)
	
	
# ========================================================================================
# Définition du Style des Scroll Area
# ========================================================================================
	
def setStyleScrollArea(label, x, y, mode = "Normal"):

	moveButton(label, x, y, mode)

	if mode == "Normal":
		label.resize(buttonWidthNormal,buttonHeightNormal)
	if mode == "Short":
		label.resize(buttonWidthShort,buttonHeightShort)
	if mode == "ShortDouble":
		label.resize(buttonWidthShortDouble,buttonHeightShort)
	if mode == "ShortTriple":
		label.resize(buttonWidthShortTriple,buttonHeightShort)
	if mode == "ShortPenta":
		label.resize(buttonWidthShortPenta,buttonHeightShort)
	if mode == "Double":
		label.resize(buttonWidthDouble,buttonHeightNormal)
	if mode == "Double3":
		label.resize(buttonWidthDouble3,buttonHeightNormal)
	if mode == "Double4":
		label.resize(buttonWidthDouble4,buttonHeightNormal)
	if mode == "ShortHalf":
		label.resize(buttonWidthShortHalf,buttonHeightShort)

		
# ========================================================================================
# Définition du Style de la Table des Tracés GR
# ========================================================================================
	
def setStyleTableTraces(table):
	
	style = ""
	style += "QTableCornerButton::section { background-color: " + colorToHtmlHex(DCOL.bgTableCorner.rgb()) + "; }"	
	style += "QHeaderView::section { color:black; background-color:" + colorToHtmlHex(DCOL.bgTableHeader.rgb()) + "; }"	
	style += "QTableWidget {background-color: " + colorToHtmlHex(DCOL.bgTable.rgb()) + "; gridline-color: " + colorToHtmlHex(DCOL.bgTableGrid.rgb()) + "; font: calibri; font-size: 10pt;}"
	style += "QTableView::item:selected { color:white; background: " + colorToHtmlHex(DCOL.bgTableSelected.rgb()) + "; font-weight:900; }"
	table.setStyleSheet(style)

	font = QFont()
	font.setPixelSize(10)
	table.setFont(font)

	vh = table.verticalHeader()
	vh.setDefaultSectionSize(25)

	
# ========================================================================================
# The End
# ========================================================================================
