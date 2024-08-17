# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Utilitaires divers pour Fichiers
# ========================================================================================

import os
import shutil

import QCarto_Tools_Dates as TDAT


# ========================================================================================
# Crée un répertoire s'il n'existe pas déjà
#  >>> file_path :  str			- path d'un fichier dans le répertoire à créer si nécéssaire
#  	 		 	    			- ou path du répertoire terminé par /	
#  <<< status	 : bool			- True if done, False if error
# ========================================================================================

def ensure_dir(file_path):
	try:														# Below generate error if drive does not exist 
		dir = os.path.dirname(file_path)
		if not os.path.exists(dir):
			os.makedirs(dir)
		return True	
	except:
		return False

# ========================================================================================
# Supprime un répertoire et tous les sous-répertoires / fichiers
#  >>> dir_path :  str			Path du répertoire à supprimer
# ========================================================================================

def remove_dir(dir_path):
	shutil.rmtree(dir_path, True, None)


# ========================================================================================
# Supprime les fichiers d'un répertoire qui commencent par un nom donné et qui ont une longueur de nom donnée
#  >>> dir_path  	: str			Path du répertoire
#  >>> file_name 	: str			Nom de base des fichiers à supprimer
#  >>> name_length 	: int			Longueur du nom des fichiers à supprimer - Certains noms commencent de la même façon (ex. raccourci) et ne doivent pas être supprimés)
# ========================================================================================

def remove_files(dir_path, file_name, name_length):
	try:
		fileList = os.listdir(dir_path)
		for file in fileList:
			if len(file) != name_length: continue					# Name lengths must be as requested
			if file_name not in file: continue						# Name must match
			os.remove(dir_path + '\\' + file)
	except:
		pass


# ========================================================================================
# Copier les fichiers d'un répertoire vers un autre
#  >>> src_path 	 	: str			Path du répertoire source
#  >>> dst_path 	 	: str			Path du répertoire destination
#  >>> file_name 		: str			Nom de base des fichiers à copier
#  >>> file_newname 	: str			Nouveau nom des fichiers - None pour conserver le même nom
#  <<< status 			: bool			Copy done or not
#  <<< count 			: int			Nombre de fichiers copiés
# ========================================================================================

def copy_files(src_path, dst_path, file_name, file_newname = None):
	count = 0
	for src_file in os.listdir(src_path): 
		if file_name not in src_file: continue
		dst_file = src_file if file_newname == None else src_file.replace(file_name, file_newname)
		try :
			shutil.copyfile(src_path + src_file, dst_path + dst_file)
			count += 1
		except:
			return False, count
	return  True, count


# ========================================================================================
# Epurer un nom de fichier en remplacant les charactères illégaux
#  >>> name		: str			Texte proposé comme nom de fichier
#  <<< fileName : str			Nom de fichier correct. Les caractères <>:"/\|? sont remplacés 
# ========================================================================================

def cleanFileName(name):

	fileName = name
	fileName = fileName.replace('<','(')
	fileName = fileName.replace('>',')')
	fileName = fileName.replace(':','.')
	fileName = fileName.replace('"','')
	fileName = fileName.replace('/','-')
	fileName = fileName.replace('\\','-')
	fileName = fileName.replace('|','-')
	fileName = fileName.replace('?','-')
	fileName = fileName.replace('*','+')

	return fileName

		
# ========================================================================================
# Split a QCarto standardized File Name
#  >>> fileName		: str		Full file name with extension
#  <<< baseName		: str		File name with time stamp and without extension
#  <<< timeStamp	: str		Normally 19 characters
#  <<< extension	: str		Excluding the .
# ========================================================================================
		
def splitFileName(fileName):
	baseName = fileName.split(' (')[0]
	timeStamp = TDAT.extractTimeStamp(fileName)
	extension = fileName.split('.')[-1]
	
	return baseName, timeStamp, extension

		
# ========================================================================================
# Split a QCarto standardized File Base Name
#  >>> fileBaseName		: str		File name with time stamp and without extension
#  <<< prefix			: str		File prefix
#  <<< trackCode		: str		Code du Parcours
#  <<< name				: str		Nom du Parcours
# ========================================================================================
		
def splitFileBaseName(baseName):
	parts = baseName.split(' - ')
	prefix = ''
	trackCode = ''
	name = 'Nom mal structuré'
	
	try:
		prefix = parts[0]
		trackCode = parts[1]
		name = ' - '.join(parts[2:])			# Fixed 7.8 as - can appear in name itself
	except:
		pass
		
	return prefix, trackCode, name
		
		
# ========================================================================================
# Change File extension
#  >>> fileName		: str		Full file name with extension
#  >>> newExtension : str		Nouvelle extension - '.' non compris
#  <<< fileNewName	: str		Full file name with new extension - '' si erreur
# ========================================================================================
		
def changeFileExtension(fileName, newExtension):
	extension = fileName.split('.')[-1]	
	nudeName = fileName.split('.')[0]	

	return nudeName + '.' + newExtension
				
		
# ========================================================================================
# --- THE END ---
# ========================================================================================


