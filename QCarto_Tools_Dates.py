# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Utilitaires pour la Gestion des dates
# ========================================================================================

from qgis.core import *
from qgis.gui import *

import time
	

# ========================================================================================
# Générer un id unique basé sur le temps
# <<< id 		int-8
# ==========================

def getTimeBasedId():
	return int(time.time() * 1000)	


# ========================================================================================
# Générer un cachet horodateur sur base des date et heure courantes
# <<< timeStamp : str				Format AAAA-MM-JJ HH-MM-SS ("-" et pas de ":" car utilisé dans noms de fichiers)
# ========================================================================================

def getTimeStamp():

	currentTime = time.time()
	year = time.localtime(currentTime)[0]
	mon = time.localtime(currentTime)[1]
	day = time.localtime(currentTime)[2]
	hour = time.localtime(currentTime)[3]
	min = time.localtime(currentTime)[4]
	sec = time.localtime(currentTime)[5]

	timeStamp = "{:04d}".format(year) + '-' + "{:02d}".format(mon) + '-' + "{:02d}".format(day) + ' ' + "{:02d}".format(hour) + '-' + "{:02d}".format(min) + '-' + "{:02d}".format(sec)

	return(timeStamp)


# ========================================================================================
# Vérifier si un timeStamp est d'aujourd'hui
# >>> timeStamp : str				Format AAAA-MM-JJ HH-MM-SS 
# <<< 			: bool				True if today (any time)
# ========================================================================================

def isTimeStampToday(timeStamp):
	if len(timeStamp) < 10: return False
	currentTime = time.time()
	year = time.localtime(currentTime)[0]
	mon = time.localtime(currentTime)[1]
	day = time.localtime(currentTime)[2]
	return (timeStamp[0:4] == "{:04d}".format(year) and timeStamp[5:7] == "{:02d}".format(mon) and timeStamp[8:10] == "{:02d}".format(day))


# ========================================================================================
# Calculer le nombre de jours depuis une date jusque maintenant
# >>> timeStamp : str				Format AAAA-MM-JJ HH-MM-SS 
# <<< 			: int				Nombre de jours passés - False si erreur
# ========================================================================================

def daysTillToday(timeStamp):
	if len(timeStamp) < 10: return False
	oldTime = time.mktime(time.strptime(timeStamp[0:10], '%Y-%m-%d'))
	return int((time.time() - oldTime) / 86400)


# ========================================================================================
# Générer un cachet horodateur sur base de la date courante. Version pour le nom des Fichiers GPX
# <<< dateStamp : str				Format AAAA-MM-JJ
# ========================================================================================

def getGPXDateStamp():

	currentTime = time.time()
	year = time.localtime(currentTime)[0]
	mon = time.localtime(currentTime)[1]
	day = time.localtime(currentTime)[2]

	dateStamp = "{:04d}".format(year) + '-' + "{:02d}".format(mon) + '-' + "{:02d}".format(day)

	return(dateStamp)


# ========================================================================================
# Générer date et heure au format <gpx> tag <time> 
# <<< timeStamp : str				Format : AAAA-MM-JJTHH:MM:SSZ
# ========================================================================================

def getGPXTimeTag():

	timeStamp = time.strftime('%Y-%m-%dT%H:%M:%SZ')

	return(timeStamp)


# ========================================================================================
# Extraire le timeStamp qui se trouve entre () dans un texte. 
#  	- pour les fichiers .gpx, le timestamp ne comprend pas l'heure est se compose des 1 caratères avant .gpx
#	- utilisé pour l'extraire des noms de fichier
#   - la fonction ne vérifie pas que le texte entre () soit un timeStamp
#
# >>> text      : str		Text contenant un TimeStamp entre ()			
# <<< timeStamp : str		TimeStamp extrait, normalement au format AAAA-MM-JJ HH-MM-SS
#							'XXXX-XX-XX XX-XX-XX' si les () ne sont pas trouvées
# ========================================================================================

def extractTimeStamp(text):
	try:
		timeStart = text.find('(') + 1
		timeClose = text.find(')')
		if text[-4:] == '.gpx' and timeStart == 0:
			return text[-14:-4] + ' 00-00-00'
		else:
			return text[timeStart:timeClose]
	except:
		return 'XXXX-XX-XX XX-XX-XX'


# ========================================================================================
# Modifie le TimeStamp pour afficher l'heure en HH:MM plutôt que HH-MM-SS (format file name)
# >>> timeStamp : str		TimeStamp 
# <<< timeStamp : str		TimeStamp reformatté. Les textes invalides restent inchangés
# ========================================================================================

def formatTimeStampForDisplay(timeStamp):
	displayTimeStamp = timeStamp
	if (len(timeStamp) != 19): return displayTimeStamp
	if (timeStamp[13] != '-'): return displayTimeStamp
	
	displayTimeStamp = displayTimeStamp[0:13] + ':' + displayTimeStamp[14:16]

	return displayTimeStamp


# ========================================================================================
# Converti une date fichier ou autre en time stamp
# >>> fileTime 	: int			Date et heure fichier  
# <<< timeStamp : str			TimeStamp YYYY-MM-JJ HH-MM-SS
# ========================================================================================

def convertTime2TimeStamp(fileTime):
	year = time.localtime(fileTime)[0]
	mon = time.localtime(fileTime)[1]
	day = time.localtime(fileTime)[2]
	hour = time.localtime(fileTime)[3]
	min = time.localtime(fileTime)[4]
	sec = time.localtime(fileTime)[5]
	timeStamp = "{:04d}".format(year) + '-' + "{:02d}".format(mon) + '-' + "{:02d}".format(day) + ' ' + "{:02d}".format(hour) + '-' + "{:02d}".format(min) + '-' + "{:02d}".format(sec)

	return timeStamp


# ========================================================================================
# Suspendre l'exécution. Les évènements qui interviennent sont gérés
# >>> milliseconds : Integer		Temps de suspension de l'exécution en milliseconds
# ========================================================================================

def sleep(milliseconds):
	for i in range(int(milliseconds/100)):
		QgsApplication.processEvents()
		time.sleep(0.1)


# ========================================================================================
# --- THE END ---
# ========================================================================================
