# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Utilitaires pour la Gestion des Fichiers Images !!
# ========================================================================================

import importlib
from PIL import Image, ExifTags



# ========================================================================================
# Déterminer l'orientation d'une photo d'après Exif 
#  >>> photoPath 		: txt			Path complet de la photo
#  <<< orientation		:  3 : tournée à 180°
#						:  6 : tournée 90° sens anti-horlogique
#						:  8 : tournée 90° sens horlogique
# ========================================================================================

def getPhotoFileExifOrientation(photoPath) :

	try :
		photo = Image.open(photoPath)

		for orientation in ExifTags.TAGS.keys() :
			if ExifTags.TAGS[orientation]=='Orientation' : break

		exif = photo._getexif()
		
		return exif[orientation]

	except :
		return None


# ========================================================================================
# Déterminer l'orientation d'un fichier image
#  >>> imagePath 		: txt			Path complet de la carte (ou n'importe quelle image)
#  <<< orientation		: txt			'L' or 'P' - None if error
# ========================================================================================

def getImageFileOrientation(imagePath):
	try:
		image = Image.open(imagePath)
		return 'W' if image.width >= image.height else 'P'
	except:
		return None


# ========================================================================================
# Déterminer les dimensions d'un fichier image
#  >>> imagePath 		: txt			Path complet de la carte (ou n'importe quelle image)
#  <<< width 			: int			En pixels
#  <<< height			: int			En pixels
# ========================================================================================

def getImageFileDimensions(imagePath):
	try:
		image = Image.open(imagePath)
		return image.width, image.height
	except:
		return -1, -1


# ========================================================================================
# Effectuer une rotation du fichier image
#  >>> imagePath 		: txt			Path complet de la carte à afficher
#  <<< status			: bool			Operation status - True iff OK
# ========================================================================================

def rotate90ImageFile(imagePath):
	try:
		image = Image.open(imagePath)
		image = image.transpose(Image.ROTATE_90)
		image.save(imagePath)
		return True
	except:
		return False


# ========================================================================================
# Retrouver la géolocalisation d'une photo
#  >>> photoPath 		: txt			Path complet de la photo
#  <<< status 			: bool			Retrieve geolocalisation sucessfull or not
#  <<< position			: dico			Dictionnaire of Position : Longitude, Latitude, Altitude in WGS 84
# ========================================================================================

def getPhotoLocalisation(photoPath):

	try : 
		import piexif
		from GPSPhoto import gpsphoto
	except :
		return False, None
		
	try:
		position = gpsphoto.getGPSData(photoPath)
	except:
		return False, None
		
	return True, position


# ========================================================================================
# --- THE END ---
# ========================================================================================
