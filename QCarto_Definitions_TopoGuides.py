# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Définition pour la Gestion des TopoGuides
# ========================================================================================

from PyQt5.QtCore import *
from PyQt5.QtGui import *

import importlib

import QCarto_Tools_Coding as TCOD

import QCarto_Parameters_Global
importlib.reload(QCarto_Parameters_Global)

QGP = QCarto_Parameters_Global.globalParameters()


# ========================================================================================
# Préfixes pour Livraison
# ========================================================================================

prefixSchema 		= '21'							# Schémas PNG
prefixProfils		= '22'							# Profils
prefixMapsPDF 		= '23'							# Cartes PNG for PDF
prefixPlanValues	= '24'							# Schémas - Distances CSV	
prefixMapsModif		= '25'							# Cartes PNG for PDF of Modification
prefixMapsTopo 		= '26'							# Cartes PNG for Topo
prefixGPX			= '27'							# Fichiers GPX RB

prefixGPXSityTrail  = '57'							# Fichiers GPX RB pour SityTrail

prefixHtml			= 'H7'							# Fichiers Html - Internal Pôle Carto
prefixSchemaBlanc	= 'B1'							# Fichiers schéma blancs - Internal Pôle Carto


dicoGRPathFromPrefix = { prefixProfils :	'22 - Profils/',
						 prefixMapsPDF : 	'23 - Cartes PDF/',
						 prefixMapsTopo : 	'26 - Cartes Topo/',
						 prefixPlanValues : '24 - Distances/'		}


# ========================================================================================
# Fichiers de Date de livraison
# ========================================================================================

subPathFileDelivery 			= 'Dates Livraisons/'
extensionFileDeliveryTopoDate 	= 'QTopo'
extensionFileDeliveryCartoDate 	= 'QCarto'

# ========================================================================================
# Définition des Tomes Topo Guides
# ========================================================================================

def getRangeByRBTome(itinerary, tomeNumber):

	type = TCOD.itineraryTypeFromTrackCode(itinerary)
	zone = TCOD.zoneFromTrackCode(itinerary)
	
	if type == 'RI':
		if tomeNumber == 1 : return  1, 9999
		if tomeNumber == 2 : return  0, -1
		if tomeNumber == 3 : return  0, -1
	if type == 'RL':
		if tomeNumber == 1 : return  1, 20
		if tomeNumber == 2 : return 21, 40
		if tomeNumber == 3 : return 41, 60
	if type == 'RB':
		if tomeNumber == 1 : 
			if zone == 'PN' : return  1, 6
			if zone != 'PN' : return  1, 16
		if tomeNumber == 2 : 
			if zone == 'PN' : return  7, 12
			if zone != 'PN' : return 17, 32
		if tomeNumber == 3 : 
			if zone == 'PN' : return  8, 18
			if zone != 'PN' : return 33, 48
	if type == 'RF' :
		if tomeNumber == 1 : return  1, 15
		if tomeNumber == 2 : return 16, 30

def getRBTome(itineraryCode):
	
	type = TCOD.itineraryTypeFromTrackCode(itineraryCode)
	zone = TCOD.zoneFromTrackCode(itineraryCode)

	number = TCOD.numberFromTrackCode(itineraryCode)
	numberValue = int('0' + ''.join([c for c in number if c.isdigit()]))

	if type == 'RI':
		return 1
	if type == 'RL':
		if numberValue <= 20: return 1
		if numberValue <= 40: return 2
		if numberValue <= 60: return 3
	if type == 'RB':
		if zone == 'PN':
			if numberValue <=  6: return 1
			if numberValue <= 12: return 2
			if numberValue <= 18: return 3
		if zone != 'PN':
			if numberValue <= 16: return 1
			if numberValue <= 32: return 2
			if numberValue <= 48: return 3
	if type == 'RF':
		if numberValue <= 15: return 1
		if numberValue <= 30: return 2

	return 9999			

def getGGZone(number):
	try :
		return ( ['XX', 'BW', 'BW', 'BW', 'BW', 'HA', 'HA', 'HA',	'HA', 'LG', 'LG', 'LG', 'LG', 'LU',	'LU', 'LU',	'LU', 'NA', 'NA', 'NA', 'NA', 	\
			        'BW', 'BW', 'BW', 'BW', 'HA', 'HA', 'HA',	'HA', 'LG', 'LG', 'LG', 'LG', 'LU',	'LU', 'LU',	'LU', 'NA', 'NA', 'NA', 'NA'] [int(number)] )
	except :				
		return 'XX'


def getGRTomeList(trackCode):
	type = TCOD.itineraryTypeFromTrackCode(trackCode)
	label = TCOD.labelGRFromTrackCode(trackCode)
	trackCode = TCOD.removeModificationsFromTrackCode(trackCode)

	if label == '129':
		if trackCode in ['GR-129', 'GR-129-L9'] : return [1, 2]
		elif trackCode in ['GR-129-V1', 'GR-129-V2', 'GR-129-L7', 'GR-129-L8', 'GR-129-L10', 'GR-129-L11', ] : return [1]
		elif trackCode in ['GR-129-V3', 'GR-129-L1', 'GR-129-L2',  'GR-129-L3', 'GR-129-L4', 'GR-129-L5', 'GR-129-L6', ] : return [2]
		else : return [1, 2]

	if label == 'BVW' :
		if trackCode in ['GRT-BVW-P01', 'GRT-BVW-P02', 'GRT-BVW-P03', 'GRT-BVW-P04','GRT-BVW-P05', 'GRT-BVW-P06', 'GRT-BVW-P07', 'GRT-BVW-P08', 'GRT-BVW-P09', \
						 'GRT-BVW-P10', 'GRT-BVW-P11', 'GRT-BVW-P12', 'GRT-BVW-P13'] : return [1]
		if trackCode in ['GRT-BVW-P14', 'GRT-BVW-P15', 'GRT-BVW-P16', 'GRT-BVW-P17','GRT-BVW-P18', 'GRT-BVW-P19', 'GRT-BVW-P20', 'GRT-BVW-P21', 'GRT-BVW-P22', \
						 'GRT-BVW-P23'] : return [2]
		if trackCode in ['GRT-BVW-P24', 'GRT-BVW-P25', 'GRT-BVW-P26', 'GRT-BVW-P27','GRT-BVW-P28', 'GRT-BVW-P29', 'GRT-BVW-P30', 'GRT-BVW-P31', 'GRT-BVW-P32', \
						 'GRT-BVW-P33'] : return [3]
		else : return [1, 2, 3]

	return [1, 2, 3]


# ========================================================================================
# Définition des répertoires sur le Drive Topo
# ========================================================================================

def getDriveTopoPath(itineraryCode, prefix = None):

	print(itineraryCode + ' - ' + str(prefix))

	type = TCOD.itineraryTypeFromTrackCode(itineraryCode)

	if type in QGP.typeSetModeGR :
		grLabel = TCOD.labelGRFromTrackCode(itineraryCode)
		if grLabel == 'BVW' : grLabel = 'GTPBVW'		
		topo = type.upper() + ' ' + grLabel.upper()

		path = QGP.pathDeliveriesTopoMapsGR
		path = path.replace('%TOPO%', topo)

		if prefix in dicoGRPathFromPrefix :
			path += dicoGRPathFromPrefix[prefix]
		else:
			path += '92 - Divers Carto'
			
		return path	
		
	if type == 'IR':	
		path = QGP.pathDeliveriesTopoMapsIR
		path = path.replace('%IR%', itineraryCode)
		return path		
		
	if type == 'RL':
		number 	= TCOD.numberFromTrackCode(itineraryCode)
		if number in ('T1', 'T2', 'T3') :
			tomeNumber = int(number[1]) 
		else:
			tomeNumber	= getRBTome(itineraryCode)
		zone = getGGZone(number)

		topo = 'GG Tome ' + str(tomeNumber)									# Exemple : GG Tome 1
		rb = 'GG-' + zone + '-' + number.upper()							# Exemple : GG-BW-04

		path = QGP.pathDeliveriesTopoMapsRB
		path = path.replace('%TOPO%', topo)
		path = path.replace('%RB%', ('05. GRAPHISTE/Topo Global' if number in ('T1', 'T2', 'T3') else rb))
		
		return path	

	if type == 'RI':
		path = QGP.pathDeliveriesTopoMapsRI
		path = path.replace('%RI%', itineraryCode.upper())
		return path	

	if type in QGP.typeSetModeRB :
		number = TCOD.numberFromTrackCode(itineraryCode)
		if number in ('T1', 'T2', 'T3') :
			tomeNumber = int(number[1]) 
		else:
			tomeNumber	= getRBTome(itineraryCode)
		zone = TCOD.zoneFromTrackCode(itineraryCode)

		zoneTopo = zone if zone != 'PN' else 'PNW'			
		topo = type.upper() + ' ' + zoneTopo.upper() + ' Tome ' + str(tomeNumber)
		rb = type.upper() + '-' + zone.upper() + '-' + number.upper()
	
		path = QGP.pathDeliveriesTopoMapsRB
		path = path.replace('%TOPO%', topo)
		path = path.replace('%RB%', ('05. GRAPHISTE/Topo Global' if number in ('T1', 'T2', 'T3') else rb))
		
		return path	
	
	return '? --- error --- ?'	


# ========================================================================================
# The End
# ========================================================================================
