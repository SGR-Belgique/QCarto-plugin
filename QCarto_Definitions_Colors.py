# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Couleurs des Menus et Tables
# ========================================================================================

from PyQt5.QtCore import *
from PyQt5.QtGui import *


# ========================================================================================
# Définition des Couleurs
# ========================================================================================

black = 						QColor('#000000')
lightGray = 					QColor('#C0C0C0')
veryLightGray1 = 				QColor('#E4E4E4')
veryLightGray2 = 				QColor('#F0F0F0')
darkGray = 						QColor('#A0A0A0')
white = 						QColor('#FFFFFF')

pureRed = 						QColor('#FF0000')
pureRedGR = 					QColor('#E2001A')
paleRed = 						QColor('#FFB6C1')
veryDarkRed = 					QColor('#720000')

brown = 						QColor('#A53E2A')

pureBlue = 						QColor('#0000FF')
vividBlue = 					QColor('#3399FF')
lightGrayishBlue =			 	QColor('#E0F2FE')
darkBlue = 						QColor('#0000A4')
verySoftBlue = 					QColor('#afddfc')

pureLimeGreen =					QColor('#00FF00')
darkLimeGreen =					QColor('#008000')
veryDarkLimeGreen =				QColor('#006000')
veryLightCyan_limeGreen = 		QColor('#99FFCC')
veryPaleCyan = 					QColor('#E0FFFF')
veryPaleCyan_limeGreen = 		QColor('#E0FFF0')

pureOrange = 					QColor('#FFA500')
pureOrangePlus = 				QColor('#FF6500')
verySoftOrange = 				QColor('#fcceaf')

pureYellow = 					QColor('#FFFF00')
veryPaleYellow = 				QColor('#FFFACD')

strongViolet = 					QColor('#9932CC')
softViolet = 					QColor('#9370DB')

pureMagenta = 					QColor('#FF00FF')
strongMagenta = 				QColor('#B300B3')
grayishMagenta = 				QColor('#D8BFD8')
veryDarkMagenta = 				QColor('#670067')
softMagenta = 					QColor('#E74EE7')


# ========================================================================================
# Définition des Couleurs utilisées par Thème
# ========================================================================================

# Text

txtNormal = black
txtGreen = veryDarkLimeGreen
txtRed = pureRed
txtOrange = pureOrange

# Foreground

fgTableNormal = black
fgTableError = pureRed
fgTableZone = darkLimeGreen


fgTrackGR = pureRed
fgTrackGRP = pureYellow
fgTrackGRT = darkLimeGreen
fgTrackRI = brown
fgTrackRB = pureOrange
fgTrackRF = pureLimeGreen
fgTrackRL = pureBlue
fgTrackOther = lightGray

fgTableCopy = strongViolet
fgTableNoCopy = darkGray


# Background

bgNormal = veryLightGray2
bgButtonNormal = softViolet
bgButtonNormalStrong = strongViolet
bgButtonWarning = veryDarkRed
bgButtonActive = pureLimeGreen
bgButtonInactive = lightGray
bgButtonProjectNormal = veryLightGray1
bgButtonHelp = grayishMagenta
bgButtonInfo = lightGrayishBlue

bgComboNormal = lightGrayishBlue
bgComboWarning = veryPaleYellow
bgComboInfo = veryLightCyan_limeGreen
bgComboInfoInit = veryLightGray1

bgCheckBoxNormal = lightGrayishBlue
bgRadioBoxNormal = lightGrayishBlue

bgLabelNormal = veryLightGray1
bgLabelOk = veryLightCyan_limeGreen
bgLabelWarning = veryPaleYellow
bgLabelError = paleRed
bgLabelFixed = lightGrayishBlue

bgLineEdit = lightGrayishBlue

bgTableOk = veryLightCyan_limeGreen
bgTableToday = veryLightCyan_limeGreen
bgTableTodayStrong = pureLimeGreen
bgTableChanged = veryPaleCyan
bgTableOtherCarto = verySoftBlue
bgTableError = paleRed
bgTableErrorViolet = softMagenta
bgTableWarning = veryPaleYellow
bgTableWarningSevere = pureOrange
bgTableWarningOtherCarto = verySoftOrange
bgTableSelected = vividBlue
bgTableCorner = pureRedGR
bgTableGrid = lightGray
bgTableHeader = lightGray
bgTable = veryLightGray2

fgTable50KNormal = black
fgTable50KNotDefined = darkGray
bgTable50KNormal = veryLightGray2
bgTable50KSelected = pureMagenta

bgTable50KModified = pureOrange

bgTable50KUnchanged = darkLimeGreen
bgTable50KLevel1 = veryLightCyan_limeGreen
bgTable50KLevel2 = pureYellow
bgTable50KLevel3 = pureOrange
bgTable50KInvalid = pureRed
	
bgStatusError = pureRed
bgStatusWarning = pureYellow
bgStatusWorking = pureLimeGreen
bgStatusDone = veryLightCyan_limeGreen
bgStatusInfo = lightGrayishBlue
bgStatusOk = veryLightGray1
		
# Rubberband

bgRubberBandGPXTrack = pureLimeGreen
bgRubberBandGPXTrack.setAlphaF(0.5)
bgRubberBandGPXPointsA = pureOrange
bgRubberBandGPXPointsA.setAlphaF(0.8)
bgRubberBandGPXPointsB = darkLimeGreen
bgRubberBandGPXPointsB.setAlphaF(0.8)

bgRubberBandGPXCreation = softViolet


# ========================================================================================
# The End
# ========================================================================================
