# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Définition des Règles pour la Publication
# ========================================================================================

from qgis.core import *
from qgis.gui import *

import QCarto_Tools_Coding as TCOD

import QCarto_Parameters_Global
QGP = QCarto_Parameters_Global.globalParameters()


# ========================================================================================
# Déterminer si un Parcours de la Table Parcours-GR doit apparaitre sur la carte publique
#  >>> code					: str					Code du Parcours dans la table Parcours-GR
#  <<< dicoTracks 			: dict 					Code : Track Feature		For all tracks GR GRP GRT
# ========================================================================================

def isTrackGROnPublicMap(code, dicoTracks):
	
#	Seuls les Parcours Publiés sont publiés !

	if dicoTracks[code][QGP.tableTracksFieldStatus] != 'Publié' : return False

#	Les Parcours sans géométrie ne peuvent pas être publiés

	if dicoTracks[code].geometry().isNull() : return False
	if dicoTracks[code].geometry().isEmpty() : return False
	
#	Analyse du code

	valid, type, label, zone, number, itineraryCode, trackBaseCode, trackCode, modificationList, invalidationList, repeatCount, bifurcationNumber, direction = TCOD.elementsFromGrCode(code)		

	if not valid : return False

#	Les Parcours modifiés sont publiés, les autres modifications non

	if 'F' in modificationList : return False
	if 'T' in modificationList : return True

#	Les Parcours pour lesquels une modification temporaire existe ne sont pas publiés

	if modificationList == []:
		if (code + '-MT') in dicoTracks : return False
		
#	Tous les autres parcours sont publiés

	return True


# ========================================================================================
# Déterminer si un Parcours de la Table Parcours-RB doit apparaitre sur la carte publique
#  >>> code					: str					Code du Parcours dans la table Parcours-RB
#  >>> dicoTracks 			: dict 					Code : Track Feature		For all tracks RB RF RL
# ========================================================================================

def isTrackRBOnPublicMap(code, dicoTracks):
	
#	Seuls les Parcours Publiés sont publiés !

	if dicoTracks[code][QGP.tableTracksFieldStatus] != 'Publié' : return False

#	Les Parcours sans géométrie ne peuvent pas être publiés

	if dicoTracks[code].geometry().isNull() : return False
	if dicoTracks[code].geometry().isEmpty() : return False
	
#	Analyse du code

	valid, type, label, zone, number, itineraryCode, trackBaseCode, trackCode, modificationList, invalidationList, repeatCount, bifurcationNumber, direction = TCOD.elementsFromGrCode(code)		

	if not valid : return False

#	Les allongements et raccourcis ne sont pas publiés

	if trackCode != trackBaseCode: return False

#	Les Parcours modifiés ne sont pas publiés, les autres modifications non plus

	if 'F' in modificationList : return False
	if 'T' in modificationList : return False

#	Tous les autres parcours sont publés

	return True


# ========================================================================================
# The End
# ========================================================================================
