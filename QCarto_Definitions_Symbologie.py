# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Définition des symbologies
# ========================================================================================

from PyQt5.QtCore import *
from PyQt5.QtGui import *

from qgis.core import *
from qgis.gui import *

import importlib

import QCarto_Tools_Coding as TCOD

import QCarto_Parameters_Global
importlib.reload(QCarto_Parameters_Global)
QGP = QCarto_Parameters_Global.globalParameters()


# ========================================================================================
#	Code des couleurs et des traits pour symbol
#		0 - Transparent
#		1 - Bordeau
#		4 - Mauve			
#	  104 - Mauve Fond clair RF
#		5 - Noir
#		6 - Bleu
#	 +  0 - Tirets
#    + 10 - Points
#    + 20 - Tirets Courts
#	 + 30 - Tirets-Points
#    + 40 - Croix
#	 + 50 - Lignes épaisseur tirets
# 	 + 60 - Lignes épaisseur tirets courts
#	   99 - Impossible - erreur
# ========================================================================================


# ========================================================================================
#	Symbologie
#		Chaque symbologie est une liste de deux dictionnaires
#			Dictionnaire 1 :	Sur itinéraire principal
#			Dictionnaire 2 : 	Sur autres GR.P.
#		Le dictionnaire définit les symboles pour chaque type de tronçons : Principal, Variante, Allongement, Raccourci, ...
#			Symbole 1 :	Quand le tronçon est balisé
#			Symbole 2:	Quand le tronçon n'est pas balisé			
# ========================================================================================

GR_Standard  = [ {'P': [ 1,  5],  'V': [31, 35],  'A': [99, 99], 'J': [99, 99], 'L': [31, 35], 'R': [31, 35], 'B': [31, 35] } ,  \
				 {'P': [11,  0],  'V': [11,  0],  'A': [11,  0], 'J': [11,  0], 'L': [11,  0], 'R': [11,  0], 'B': [11,  0] } ]

RB_Standard  = [ {'P': [ 5,  5],  'V': [24, 24],  'A': [24, 24], 'J': [24, 24], 'L': [99 ,99], 'R': [26, 26], 'B': [99, 99] } ,  \
				 {'P': [11,  0],  'V': [11,  0],  'A': [11,  0], 'J': [11,  0], 'L': [11,  0], 'R': [11,  0], 'B': [99, 99] } ]
				 
RF_Standard  = [ {'P': [ 5,  5],  'V': [104, 104],  'A': [104, 104], 'J': [104, 104], 'L': [99 ,99], 'R': [26, 26], 'B': [99, 99] } ,  \
				 {'P': [11,  0],  'V': [11,  0],    'A': [11,  0],   'J': [11,  0],   'L': [11,  0], 'R': [11,  0], 'B': [99, 99] } ]
				 
RB_Schéma  =   [ {'P': [55,  5],  'V': [64, 24],  'A': [64, 24], 'J': [64, 24], 'L': [99 ,99], 'R': [66, 26], 'B': [99, 99] } ,  \
				 {'P': [11,  0],  'V': [11,  0],  'A': [11,  0], 'J': [11,  0], 'L': [11,  0], 'R': [11,  0], 'B': [99, 99] } ]

IR_Spécial  =  [ {'P': [ 5,  5],  'V': [ 5,  5],  'A': [24, 24], 'J': [ 5,  5], 'L': [99 ,99], 'R': [99, 99], 'B': [99, 99] } ,  \
				 {'P': [11,  0],  'V': [11,  0],  'A': [11,  0], 'J': [11,  0], 'L': [11,  0], 'R': [11,  0], 'B': [99, 99] } ]
				 
RB_Ancien =    [ {'P': [ 1,  5],  'V': [31, 35],  'A': [31, 35], 'J': [31, 35], 'L': [99, 99], 'R': [ 1,  6], 'B': [99, 99] } ,  \
				 {'P': [11,  0],  'V': [11,  0],  'A': [11,  0], 'J': [11,  0], 'L': [11,  0], 'R': [11,  0], 'B': [11,  0] } ]

RB_Test  =	   [ {'P': [ 5,  5],  'V': [24, 24],  'A': [24, 24], 'J': [24, 24], 'L': [99, 99], 'R': [26, 26], 'B': [99, 99] } ,  \
				 {'P': [11,  0],  'V': [11,  0],  'A': [11,  0], 'J': [11,  0], 'L': [11,  0], 'R': [11,  0], 'B': [11,  0] } ]

RB_Test_A  =   [ {'P': [ 1,  5],  'V': [21, 25],  'A': [21, 25], 'J': [21, 25], 'L': [99 ,99], 'R': [21, 26], 'B': [99, 99] } ,  \
				 {'P': [11,  0],  'V': [11,  0],  'A': [11,  0], 'J': [11,  0], 'L': [11,  0], 'R': [11,  0], 'B': [99, 99] } ]

RB_Test_B  =   [ {'P': [ 1,  5],  'V': [21, 24],  'A': [21, 24], 'J': [21, 24], 'L': [99 ,99], 'R': [21, 26], 'B': [99, 99] } ,  \
				 {'P': [11,  0],  'V': [11,  0],  'A': [11,  0], 'J': [11,  0], 'L': [11,  0], 'R': [11,  0], 'B': [99, 99] } ]

RB_Test_C  =   [ {'P': [ 5,  5],  'V': [24, 24],  'A': [24, 24], 'J': [24, 24], 'L': [99 ,99], 'R': [26, 26], 'B': [99, 99] } ,  \
				 {'P': [11,  0],  'V': [11,  0],  'A': [11,  0], 'J': [11,  0], 'L': [11,  0], 'R': [11,  0], 'B': [99, 99] } ]

RB_Test_D  =   [ {'P': [55,  5],  'V': [64, 24],  'A': [64, 24], 'J': [64, 24], 'L': [99 ,99], 'R': [66, 26], 'B': [99, 99] } ,  \
				 {'P': [11,  0],  'V': [11,  0],  'A': [11,  0], 'J': [11,  0], 'L': [11,  0], 'R': [11,  0], 'B': [99, 99] } ]

RB_Test_3  =   [ {'P': [ 1,  5],  'V': [24, 24],  'A': [24, 24], 'J': [24, 24], 'L': [99 ,99], 'R': [26, 26], 'B': [99, 99] } ,  \
				 {'P': [11,  0],  'V': [11,  0],  'A': [11,  0], 'J': [11,  0], 'L': [11,  0], 'R': [11,  0], 'B': [11,  0] } ]

dicoSymbology = { 'GR-Standard' : GR_Standard, 
				  'RB-Standard' : RB_Standard,
				  'RF-Standard' : RF_Standard,
				  'RB-Schéma'   : RB_Schéma,
				  'IR-Spécial'	: IR_Spécial }
#				  'RB-Test' 	: RB_Test,
#				  'RB-Test-A' 	: RB_Test_A, 
#				  'RB-Test-B' 	: RB_Test_B, 
#				  'RB-Test-C' 	: RB_Test_C, 
#				  'RB-Test-D' 	: RB_Test_D, 
#				  'RB-Test-3' 	: RB_Test_3,
#				  'RB-Ancien'	: RB_Ancien}

def getSectionSymbol(dicoName, itineraryFlag, type, marked):
	if itineraryFlag : 
		if marked : return dicoSymbology[dicoName][0][type][0]
		else:		return dicoSymbology[dicoName][0][type][1]
	else:
		if marked : return dicoSymbology[dicoName][1][type][0]
		else:		return dicoSymbology[dicoName][1][type][1]

def setSectionStyleVariables(layer, scale):

	scaleFactorDico = {50000 : 1, 40000 : 1, 35000 : 1.1, 25000 : 1.1, 20000 : 1.12, 15000 : 1.15, 10000 : 1.25 }
	if scale not in scaleFactorDico : return

	lignes50_E		= 40						# Largeur des lignes 50 en mètres à l'échelle au 1:50000	
	lignes60_E		= 35						# Largeur des lignes 60 en mètres à l'échelle au 1:50000	
	tiretLongs_E	= 40						# Largeur des tirets longs en mètres à l'échelle au 1:50000	
	tiretLongs_T	= [200,100]					# Espacement des tirets longs en mètres à l'échelle au 1:50000	
	tiretCourts_E	= 35						# Largeur des tirets longs en mètres à l'échelle au 1:50000	
	tiretCourts_T	= [100,50]					# Espacement des tirets longs en mètres à l'échelle au 1:50000	
	tiretMixtes_E	= 38						# Largeur des tirets mixtes en mètres à l'échelle au 1:50000	
	tiretMixtes_T	= [130,87,9, 87]			# Espacement des tirets mixtes en mètres à l'échelle au 1:50000	
	points_E		= 40						# Largeur des points en mètres à l'échelle au 1:50000	
	points_T		= [7,110]					# Espacement des points en mètres à l'échelle au 1:50000	
		
	QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLignes50_E', 		str(round(lignes50_E 		* scale / 50000 * scaleFactorDico[scale], 1)))
	QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLignes60_E', 		str(round(lignes60_E 		* scale / 50000 * scaleFactorDico[scale], 1)))
	QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleTiretsLong_E', 	str(round(tiretLongs_E 		* scale / 50000 * scaleFactorDico[scale], 1)))
	QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleTiretsLong_T', 	str(round(tiretLongs_T[0]	* scale / 50000 * scaleFactorDico[scale], 1)) + ';' + str(round(tiretLongs_T[1]	* scale / 50000 * scaleFactorDico[scale], 1)))
	QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleTiretsCourt_E', 	str(round(tiretCourts_E 	* scale / 50000 * scaleFactorDico[scale], 1)))
	QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleTiretsCourt_T', 	str(round(tiretCourts_T[0]	* scale / 50000 * scaleFactorDico[scale], 1)) + ';' + str(round(tiretCourts_T[1]	* scale / 50000 * scaleFactorDico[scale], 1)))
	QgsExpressionContextUtils.setLayerVariable( layer, 'QStylePoints_E', 		str(round(points_E 			* scale / 50000 * scaleFactorDico[scale], 1)))
	QgsExpressionContextUtils.setLayerVariable( layer, 'QStylePoints_T', 		str(round(points_T[0]		* scale / 50000 * scaleFactorDico[scale], 1)) + ';' + str(round(points_T[1]	* scale / 50000 * scaleFactorDico[scale], 1)))
	QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleTiretsMixte_E', 	str(round(tiretMixtes_E 	* scale / 50000 * scaleFactorDico[scale], 1)))
	QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleTiretsMixte_T', 	str(round(tiretMixtes_T[0]	* scale / 50000 * scaleFactorDico[scale], 1)) + ';' \
																			  + str(round(tiretMixtes_T[1]	* scale / 50000 * scaleFactorDico[scale], 1)) + ';' \
																			  + str(round(tiretMixtes_T[2]	* scale / 50000 * scaleFactorDico[scale], 1)) + ';' \
																			  + str(round(tiretMixtes_T[3]	* scale / 50000 * scaleFactorDico[scale], 1)))


def setLabelsSimpleStyleVariables(layer, scale):

	if scale == 50000:
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_Symbol', 			'60')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_Font', 			'100')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_StampX', 			'30')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_StampY', 			'10')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_StampE', 			'5')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_DuoXP', 			'100,0')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_DuoXN', 			'-100,0')

	if scale == 40000:
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_Symbol', 			'48')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_Font', 			'80')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_StampX', 			'24')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_StampY', 			'8')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_StampE', 			'4')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_DuoXP', 			'80,0')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_DuoXN', 			'-80,0')

	if scale == 35000:
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_Symbol', 			'45')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_Font', 			'75')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_StampX', 			'22.5')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_StampY', 			'7.5')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_StampE', 			'3.75')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_DuoXP', 			'75,0')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_DuoXN', 			'-75,0')

	if scale == 25000:
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_Symbol', 			'32')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_Font', 			'52')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_StampX', 			'16')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_StampY', 			'5.2')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_StampE', 			'2.6')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_DuoXP', 			'52,0')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_DuoXN', 			'-52,0')

	if scale == 20000:
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_Symbol', 			'25')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_Font', 			'42')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_StampX', 			'12.6')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_StampY', 			'4.2')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_StampE', 			'2.1')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_DuoXP', 			'42,0')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_DuoXN', 			'-42,0')

	if scale == 15000:
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_Symbol', 			'19')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_Font', 			'31.5')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_StampX', 			'9.5')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_StampY', 			'3.2')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_StampE', 			'1.6')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_DuoXP', 			'31.5,0')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_DuoXN', 			'-31.5,0')

	if scale == 10000:
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_Symbol', 			'13')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_Font', 			'21.6')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_StampX', 			'6.5')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_StampY', 			'2.2')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_StampE', 			'1.1')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_DuoXP', 			'21.6,0')
		QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLabels_DuoXN', 			'-21.6,0')


def setRepereStyleVariables(layer, scale):

	scaleFactorDico = {50000 : 1, 40000 : 1, 35000 : 1.05, 25000 : 1.05, 20000 : 1.05, 15000 : 1.08, 10000 : 1.1 }
	if scale not in scaleFactorDico : return

	texte_12_L		= 125						# Largeur du Texte (1 ou 2 char ) en mètres à l'échelle au 1:50000
	texte_3_L		= 100						# Largeur du Texte (3 char) en mètres à l'échelle au 1:50000
	cadre_DA_L	 	= 355						# Largeur du Cadre D/A en mètres à l'échelle au 1:50000
	cadre_D_L 		= 220						# Largeur du Cadre D en mètres à l'échelle au 1:50000
	cadre_A_L 		= 220						# Largeur du Cadre A en mètres à l'échelle au 1:50000
	lignes_L		= 13.25						# Largeur des Lignes et connecteurs en mètres à l'échelle au 1:50000
	boules_L		= 250						# Largeur des Boules en mètres à l'échelle au 1:50000
	boules_bord_L	= 17.5						# Largeur des Bords boules en mètres à l'échelle au 1:50000
	connecteur_DA_G = 50						# Attache des connecteurs D A D/A en mètres à l'échelle au 1:50000
	connecteurs_G   = boules_L / 2				# Attache des connecteurs au centre des boules normales à l'échelle au 1:50000
		
	QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleTexte12_L', 	str(round(texte_12_L 		* scale / 50000 * scaleFactorDico[scale], 1)))
	QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleTexte3_L', 	str(round(texte_3_L 		* scale / 50000 * scaleFactorDico[scale], 1)))
	QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleCadreDA_L', 	str(round(cadre_DA_L 		* scale / 50000 * scaleFactorDico[scale], 1)))
	QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleCadreD_L', 	str(round(cadre_D_L  		* scale / 50000 * scaleFactorDico[scale], 1)))
	QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleCadreA_L',	str(round(cadre_A_L  		* scale / 50000 * scaleFactorDico[scale], 1)))
	QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLignes_L',	str(round(lignes_L   		* scale / 50000 * scaleFactorDico[scale], 2)))
	QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleBoules_L',	str(round(boules_L   		* scale / 50000 * scaleFactorDico[scale], 1)))
	QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleBords_L',		str(round(boules_bord_L   	* scale / 50000 * scaleFactorDico[scale], 2)))
	QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleConnDA_G',	str(round(connecteur_DA_G   * scale / 50000 * scaleFactorDico[scale], 1)))
	QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleConn_G',		str(round(connecteurs_G   	* scale / 50000 * scaleFactorDico[scale], 1)))
	

def setPoisRFStyleVariables(layer, scale):

	scaleFactorDico = {50000 : 1, 40000 : 1, 35000 : 1.05, 25000 : 1.05, 20000 : 1.05, 15000 : 1.08, 10000 : 1.1 }
	if scale not in scaleFactorDico : return

	texte_L			= 150						# Largeur du Texte (1 char) en mètres à l'échelle au 1:50000
	lignes_L		= 13.25						# Largeur des Lignes et connecteurs en mètres à l'échelle au 1:50000
	boules_L		= 400						# Largeur des Boules en mètres à l'échelle au 1:50000
		
	QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleTexte_L', 	str(round(texte_L 			* scale / 50000 * scaleFactorDico[scale], 1)))
	QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleLignes_L',	str(round(lignes_L   		* scale / 50000 * scaleFactorDico[scale], 2)))
	QgsExpressionContextUtils.setLayerVariable( layer, 'QStyleBoules_L',	str(round(boules_L   		* scale / 50000 * scaleFactorDico[scale], 1)))
	

# ========================================================================================
#	Symbologie des Points repères
#    - toujours couleur standard sauf BVW parcours pairs
# ========================================================================================

def  getPointColor(gr_code):
    if TCOD.itineraryTypeFromTrackCode(gr_code) == 'GRT' and TCOD.labelGRFromTrackCode(gr_code) == 'BVW':
        try:
            trackNumber = int(''.join(c for c in gr_code.split('-')[2] if c.isdigit()))
            if trackNumber % 2 == 0 : return 'Mauve'
        except:
            pass
    return 'Standard'        
 

# ========================================================================================
#	Grille en fonction du type d'itinéraire
# ========================================================================================

def isGridOnMap(type):
	if type in ('RB', 'RF', 'RL', 'IR'): return True
	if type in ('GR', 'GRP', 'GRT'): return False


# ========================================================================================
# Déterminer si un tronçon est balisé ou non
#  >>> mainFrame									For access to main Dico
#  >>> sectionFeature	 	: QgsFeature			Tronçon à évaluer
#  <<< marked 				: Bool					Balisé ou non, par définition :
#														Les tronçons avec GR ou GRP sont balisés
#														Les tronçons avec GRT autres que BVW sont balisés
#								  						Tous les autres tronçons ne sont pas balisés
# ========================================================================================	
	
def isSectionFeatureMarked(mainFrame, sectionFeature):

	codeList = TCOD.getCodeListALLFromSectionFeature(sectionFeature)
	for gr_code in codeList:
		valid, type, label, zone, number, itineraryCode, trackBaseCode, trackCode, modificationList, invalidationList, repeatCount, bifurcationNumber, direction = TCOD.elementsFromGrCode(gr_code)
		if not valid: continue
		if isSectionGrCodeMarked(mainFrame, gr_code) : return True
	return False

def isSectionGrCodeMarked(mainFrame, gr_code) :
	valid, type, label, zone, number, itineraryCode, trackBaseCode, trackCode, modificationList, invalidationList, repeatCount, bifurcationNumber, direction = TCOD.elementsFromGrCode(gr_code)
	if not valid: return False

	if type in QGP.typeSetTableGR :
		if trackCode not in mainFrame.dicoTracksGRFeatures : return False	
		if mainFrame.dicoTracksGRFeatures[trackCode][QGP.tableTracksFieldStatus] not in QGP.trackStatusForQBalisage : return False	

	if type in ('GR', 'GRP'): 
		if label == 'TDA' : return False			
		if label != '412' and  TCOD.isCodeBoucleGR(gr_code) : return False	
		return True

	if type == 'GRT' :
		if label == 'BVW': return False
		return True

	return False


# ========================================================================================
# The End
# ========================================================================================
