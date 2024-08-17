# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ========================================================================================

from qgis.core import *
from qgis.gui import *

import importlib

import QCarto_Layers_Tracks as LTRK
importlib.reload(LTRK)

import QCarto_Tools_Coding as TCOD
importlib.reload(TCOD)
import QCarto_Tools_Dates as TDAT
import QCarto_Tools_Files as TFIL
import QCarto_Tools_SCR as TSCR
import QCarto_Tools_Layers as TLAY
import QCarto_Tools_Progress as TPRO

import QCarto_Parameters_Global
QGP = QCarto_Parameters_Global.globalParameters()


# ========================================================================================
# Créer le fichier .csv Statistiques
# >>> path						: str			directory path
# >>> file						: str			file name including .csv
# >>> mainFrame					:
# >>> button					:				For Progress bar
# ========================================================================================

def exportCsvStats(path, file, mainFrame, button) :

# Utilitaries

	def getSectionsSet(listCodes, ignoreErrors = False) :
		setSectionsGR = set()
		for code in listCodes :
			QgsApplication.processEvents()
			dicoTrackSections = LTRK.generateDicoTracksSections(TCOD.itineraryTypeFromTrackCode(code), { code : None }, mainFrame.dicoSectionsGRFeatures)
			sectionOrderedIdList, sectionLostIdList, errorCode, gapList, modificationSet, sectionModifiedIdList = \
				LTRK.computeTracksOrderedSections(code, dicoTrackSections, mainFrame.dicoSectionsGRFeatures, mainFrame.dicoSectionsGRFeaturesEndPoints)				
			if errorCode != 0 and not ignoreErrors: return False, set()
			setSectionsGR.update(set([abs(id) for id in sectionOrderedIdList]))
		return True, setSectionsGR

	def outputZoneDistances(distanceTotale, setSections) :
		if layerProvinces == None : return
		distanceOutBe = distanceTotale
		distancesZone = {}
		for zone in sorted(dicosSectionsGRDistancesZone) :
			distancesZone[zone] = round(sum(dicosSectionsGRDistancesZone[zone][id] for id in setSections) / 1000) 
		for zone in sorted(distancesZone, reverse = True, key = lambda x : distancesZone[x] ) :
			if distancesZone[zone] == 0 : continue
			line = '      Distance' + separator + separator + zone.title() + separator + '{0:d} km'.format(distancesZone[zone])
			fileOut.write(line + '\n')	
			distanceOutBe -= distancesZone[zone]
		if distanceOutBe <= 0 : return
		line = '      Distance' + separator + separator + 'Hors Belgique' + separator + '{0:d} km'.format(distanceOutBe)
		fileOut.write(line + '\n')	
		QgsApplication.processEvents()

		
# Open Provinces Layer

	layerProvinces, error = TLAY.openLayer(QGP.configProvincesShapeName)
	if layerProvinces == None : mainFrame.setStatusError(error); return
	
# 	Create Progress Bar

	progressBar = TPRO.createProgressBar(button, (10 + 20 + 11 * 40) + (200 + 50) + 3 * (20 + 40 + 40 + 100 + 40 + 40) + 3 * (160 + 7 * 20), 'Normal')

# Open CSV File

	TFIL.ensure_dir(path)
	csvFilePath = path + file
	fileOut = open(csvFilePath, 'w', encoding='utf-8', errors='ignore')
	separator = QGP.configCSVSeparator
	
# Write Header

	line = 'Information' + separator + 'X' + separator + 'Zone' + separator + 'Distance' + separator + 'Liste'
	fileOut.write(line + '\n')	
	fileOut.write(separator + separator + separator + separator + '\n')	
	progressBar.setValue(progressBar.value() + 10)

# Dictionnaire des distances globales

	mainFrame.setStatusWorking('Création du dictionnaires des distances par tronçon ...')
	dicoSectionsGRDistances = { id : mainFrame.dicoSectionsGRFeatures[id].geometry().length() for id in mainFrame.dicoSectionsGRFeatures }
	progressBar.setValue(progressBar.value() + 20)

# Dictionnaires des distances par zone

	dicosSectionsGRDistancesZone = {}
	for featureZone in layerProvinces.getFeatures() :
		mainFrame.setStatusWorking('Création du dictionnaires des distances - zone ' + featureZone['ADPRNAFR'] + ' ...')
		dicosSectionsGRDistancesZone[featureZone['ADPRNAFR']] = { id : featureZone.geometry().intersection(mainFrame.dicoSectionsGRFeatures[id].geometry()).length() for id in mainFrame.dicoSectionsGRFeatures }
		progressBar.setValue(progressBar.value() + 40)

# Statistiques : Réseau complet

	mainFrame.setStatusWorking('Statistiques : Réseau GR GRP GRT complet ...')

	line = 'Réseau GR Balisé'
	fileOut.write(line + '\n')	

	listCodesGR = [ code for code in mainFrame.dicoTracksGRFeatures if mainFrame.dicoTracksGRFeatures[code][QGP.tableTracksFieldStatus] == QGP.trackStatusPublished and not TCOD.isCodeModifiedGR(code) ]

	line = '    Nombre de Parcours' + separator + '{0:d}'.format(len(listCodesGR))
	fileOut.write(line + '\n')	

	sectionsOK, setSectionsGR = getSectionsSet(listCodesGR)
	distanceGR = round(sum(dicoSectionsGRDistances[id] for id in setSectionsGR) / 1000) if sectionsOK else -1

	line = '      Distance' + separator + separator + 'Total' + separator + '{0:d} km'.format(distanceGR)
	fileOut.write(line + '\n')	
	progressBar.setValue(progressBar.value() + 200)

	mainFrame.setStatusWorking('Statistiques : Réseau GR GRP GRT complet par Zone ...')
	outputZoneDistances(distanceGR, setSectionsGR)

	line = 'Note 1' + separator + separator + separator + separator + 'Les distances par province sont déterminées sur base des limites administratives'
	fileOut.write(line + '\n')	
	fileOut.write(separator + separator + separator + separator + '\n')	
	fileOut.write(separator + separator + separator + separator + '\n')	
	progressBar.setValue(progressBar.value() + 50)
	
# Statistiques : Sentiers GR puis GRP puis GRT

	setSectionsIdAlreadyCounted = set()									# Ensemble des sections déjà comptées
	setSingleGeometryLiaisons = set()									# Ensemble des géométries des laisons déjà comptées

	for itineraryType in ['GR', 'GRP', 'GRT'] :

		mainFrame.setStatusWorking('Statistiques : Sentiers ' +  itineraryType + ' ...')

		line = 'Sentiers ' + itineraryType
		fileOut.write(line + '\n')	

		line = '  Itinéraires Publiés'
		fileOut.write(line + '\n')	

# 		Liste des Itinéraires 			

		setLabelsGR = { TCOD.labelGRFromTrackCode(code) for code in mainFrame.dicoTracksGRFeatures if TCOD.itineraryTypeFromTrackCode(code) == itineraryType and 
																										mainFrame.dicoTracksGRFeatures[code][QGP.tableTracksFieldStatus] == QGP.trackStatusPublished }
		listCodesGR = [itineraryType + '-' + label for label in setLabelsGR]
		listCodesGR = sorted(list(listCodesGR), key = lambda x : TCOD.getTrackCodeGRSortingValue(x))

		line = '    Liste des Itinéraires' + separator + separator + separator + separator + ', '.join([TCOD.labelGRFromTrackCode(code) for code in listCodesGR])
		fileOut.write(line + '\n')	

		line = '    Nombre d\'Itinéraires' + separator + '{0:d}'.format(len(listCodesGR))
		fileOut.write(line + '\n')	
		progressBar.setValue(progressBar.value() + 20)

# 		Distance des parcours principaux

		line = '    Parcours Principaux' 
		fileOut.write(line + '\n')	

		listCodesGR = [code for code in mainFrame.dicoTracksGRFeatures if TCOD.itineraryTypeFromTrackCode(code) == itineraryType and 
																			mainFrame.dicoTracksGRFeatures[code][QGP.tableTracksFieldStatus] == QGP.trackStatusPublished  and
																			TCOD.isCodePrincipalGR(code) and 
																			not TCOD.isCodeModifiedGR(code) ]

		sectionsOK, setSectionsGR = getSectionsSet(listCodesGR)
		setSectionsGR = setSectionsGR.difference(setSectionsIdAlreadyCounted)
		setSectionsIdAlreadyCounted = setSectionsIdAlreadyCounted.union(setSectionsGR)
		distanceGR = round(sum(dicoSectionsGRDistances[id] for id in setSectionsGR) / 1000) if sectionsOK else -1

		line = '      Distance' + separator + separator + 'Total' + separator + '{0:d} km'.format(distanceGR) 
		fileOut.write(line + '\n')	
		progressBar.setValue(progressBar.value() + 20)

		outputZoneDistances(distanceGR, setSectionsGR)
		fileOut.write(separator + separator + separator + separator + '\n')	
		progressBar.setValue(progressBar.value() + 20)
	
# 		Distance des variantes

		line = '    Variantes' 
		fileOut.write(line + '\n')	

		listCodesGR = [code for code in mainFrame.dicoTracksGRFeatures if TCOD.itineraryTypeFromTrackCode(code) == itineraryType and 
																			mainFrame.dicoTracksGRFeatures[code][QGP.tableTracksFieldStatus] == QGP.trackStatusPublished  and
																			TCOD.isCodeVarianteGR(code) and 
																			not TCOD.isCodeModifiedGR(code) ]

		line = '    Nombre de Variantes' + separator + '{0:d}'.format(len(listCodesGR))
		fileOut.write(line + '\n')	

		sectionsOK, setSectionsGR = getSectionsSet(listCodesGR)
		setSectionsGR = setSectionsGR.difference(setSectionsIdAlreadyCounted)
		setSectionsIdAlreadyCounted = setSectionsIdAlreadyCounted.union(setSectionsGR)
		distanceGR = round(sum(dicoSectionsGRDistances[id] for id in setSectionsGR) / 1000) if sectionsOK else -1

		line = '      Distance' + separator + separator + 'Total' + separator + '{0:d} km'.format(distanceGR)
		fileOut.write(line + '\n')	
		progressBar.setValue(progressBar.value() + 20)

		outputZoneDistances(distanceGR, setSectionsGR)
		fileOut.write(separator + separator + separator + separator + '\n')	
		progressBar.setValue(progressBar.value() + 20)
	
# 		Distance des liaisons

		line = '    Liaisons' 
		fileOut.write(line + '\n')	

		listCodesGR = [code for code in mainFrame.dicoTracksGRFeatures if TCOD.itineraryTypeFromTrackCode(code) == itineraryType and 
																			mainFrame.dicoTracksGRFeatures[code][QGP.tableTracksFieldStatus] == QGP.trackStatusPublished  and
																			TCOD.isCodeLiaisonGR(code) and 
																			not TCOD.isCodeModifiedGR(code) ]

		listSingleCodesGR = []

		mainFrame.setStatusWorking('Analyse des liaisons identiques ...')
		for code in listCodesGR :
			trackGeometry = mainFrame.dicoTracksGRFeatures[code].geometry()
			for geometry in setSingleGeometryLiaisons :
				QgsApplication.processEvents()
				if round(geometry.hausdorffDistance(trackGeometry)) < 100 : 
					mainFrame.setStatusWorking('Analyse des liaisons identiques : ' + code + ' existe déjà !', 250)
					break
			setSingleGeometryLiaisons.add(trackGeometry)
			listSingleCodesGR.append(code)
		progressBar.setValue(progressBar.value() + 100)

		line = '    Nombre de Liaisons' + separator + '{0:d}'.format(len(listSingleCodesGR))
		fileOut.write(line + '\n')	

		sectionsOK, setSectionsGR = getSectionsSet(listSingleCodesGR)
		setSectionsGR = setSectionsGR.difference(setSectionsIdAlreadyCounted)
		setSectionsIdAlreadyCounted = setSectionsIdAlreadyCounted.union(setSectionsGR)
		distanceGR = round(sum(dicoSectionsGRDistances[id] for id in setSectionsGR) / 1000) if sectionsOK else -1

		line = '      Distance' + separator + separator + 'Total' + separator + '{0:d} km'.format(distanceGR) 
		fileOut.write(line + '\n')	
		progressBar.setValue(progressBar.value() + 20)

		outputZoneDistances(distanceGR, setSectionsGR)
		fileOut.write(separator + separator + separator + separator + '\n')	
		progressBar.setValue(progressBar.value() + 20)

# 		Distance des boucles

		line = '    Boucles' 
		fileOut.write(line + '\n')	

		listCodesGR = [code for code in mainFrame.dicoTracksGRFeatures if TCOD.itineraryTypeFromTrackCode(code) == itineraryType and 
																			mainFrame.dicoTracksGRFeatures[code][QGP.tableTracksFieldStatus] == QGP.trackStatusPublished  and
																			TCOD.isCodeBoucleGR(code) and 
																			not TCOD.isCodeModifiedGR(code) ]

		line = '    Nombre de Boucles' + separator + '{0:d}'.format(len(listCodesGR))
		fileOut.write(line + '\n')	

		sectionsOK, setSectionsGR = getSectionsSet(listCodesGR)
		setSectionsGR = setSectionsGR.difference(setSectionsIdAlreadyCounted)
		setSectionsIdAlreadyCounted = setSectionsIdAlreadyCounted.union(setSectionsGR)
		distanceGR = round(sum(dicoSectionsGRDistances[id] for id in setSectionsGR) / 1000) if sectionsOK else -1

		line = '      Distance' + separator + separator + 'Total' + separator + '{0:d} km'.format(distanceGR) 
		fileOut.write(line + '\n')	
		progressBar.setValue(progressBar.value() + 20)

		outputZoneDistances(distanceGR, setSectionsGR)
		fileOut.write(separator + separator + separator + separator + '\n')	
		progressBar.setValue(progressBar.value() + 20)
		
	line = 'Note 1' + separator + separator + separator + separator + 'Les tronçons communs ne sont comptés qu\'une seule fois !'
	fileOut.write(line + '\n')	
	line = 'Note 2' + separator + separator + separator + separator + 'Les liaisons communes à plusieurs GR.P ne sont reprises qu\'une seule fois'
	fileOut.write(line + '\n')	
	fileOut.write(separator + separator + separator + separator + '\n')	
	fileOut.write(separator + separator + separator + separator + '\n')	

# Statistiques : RB puis RF puis RL


	for itineraryType in ['RB', 'RF', 'RL'] :

		mainFrame.setStatusWorking('Statistiques : Randos ' +  itineraryType + ' ...')

		setSectionsGRMarked = setSectionsIdAlreadyCounted

		line = 'Randos ' + itineraryType
		fileOut.write(line + '\n')	

		line = '  Itinéraires Publiés'
		fileOut.write(line + '\n')	

# 		Liste des Itinéraires 			

		setItineraryRando = { TCOD.itineraryFromTrackCode(code) for code in mainFrame.dicoTracksRBFeatures if TCOD.itineraryTypeFromTrackCode(code) == itineraryType and 
																												mainFrame.dicoTracksRBFeatures[code][QGP.tableTracksFieldStatus] == QGP.trackStatusPublished and 
																												mainFrame.dicoTracksRBFeatures[code][QGP.tableTracksFieldIndirect] in (None, '', '  ') }

		line = '    Nombre d\'Itinéraires' + separator + '{0:d}'.format(len(setItineraryRando)) + separator + 'Total'
		fileOut.write(line + '\n')	
		progressBar.setValue(progressBar.value() + 20)

		for zoneCode in QGP.dicoZonesNamesRB :
			countZone = sum(1 for code in setItineraryRando if TCOD.zoneFromTrackCode(code) == zoneCode)
			if countZone > 0 :
				line = separator + '{0:d}'.format(countZone) + separator + QGP.dicoZonesNamesRB[zoneCode]
				fileOut.write(line + '\n')	
		fileOut.write(separator + separator + separator + separator + '\n')	
		progressBar.setValue(progressBar.value() + 20)

# 		Liste des Parcours 			

		setTrackRando = { TCOD.removeModificationsFromTrackCode(code) for code in mainFrame.dicoTracksRBFeatures if TCOD.itineraryTypeFromTrackCode(code) == itineraryType and 
																													mainFrame.dicoTracksRBFeatures[code][QGP.tableTracksFieldStatus] == QGP.trackStatusPublished and 
																													mainFrame.dicoTracksRBFeatures[code][QGP.tableTracksFieldIndirect] in (None, '', '  ') }

		print('setTrackRando = ' + str(setTrackRando))

		line = '    Nombre de Parcours' + separator + '{0:d}'.format(len(setTrackRando)) + separator + 'Total'
		fileOut.write(line + '\n')	
		progressBar.setValue(progressBar.value() + 160)

		for zoneCode in QGP.dicoZonesNamesRB :
			countZone = sum(1 for code in setTrackRando if TCOD.zoneFromTrackCode(code) == zoneCode)
			if countZone > 0 :
				line = separator + '{0:d}'.format(countZone) + separator + QGP.dicoZonesNamesRB[zoneCode]
				fileOut.write(line + '\n')	
		fileOut.write(separator + separator + separator + separator + '\n')	
		progressBar.setValue(progressBar.value() + 20)

# 		Distances Totales des Parcours 			

		sectionsOK, setSectionsRB = getSectionsSet(setTrackRando, True)
		distanceRB = round(sum(dicoSectionsGRDistances[id] for id in setSectionsRB) / 1000) 

		line = '      Distances Totales' + separator + separator + 'Total' + separator + '{0:d} km'.format(distanceRB)
		fileOut.write(line + '\n')	
		progressBar.setValue(progressBar.value() + 20)

		for zoneCode in QGP.dicoZonesNamesRB :
			setTrackZone = { code for code in setTrackRando if TCOD.zoneFromTrackCode(code) == zoneCode }
			sectionsOK, setSectionsRBZone = getSectionsSet(setTrackZone, True)
			distanceRB = round(sum(dicoSectionsGRDistances[id] for id in setSectionsRBZone) / 1000)
			if distanceRB > 0 :
				line = separator + separator + QGP.dicoZonesNamesRB[zoneCode] + separator + '{0:d} km'.format(distanceRB) 
				fileOut.write(line + '\n')	
		line = 'Note' + separator + separator + separator + separator + 'Distances complètes y compris les tronçons balisés'
		fileOut.write(line + '\n')	
		line = 'Note' + separator + separator + separator + separator + 'Distances zones : certains tronçons sont communs à plusieurs zones !'
		fileOut.write(line + '\n')	
				
		fileOut.write(separator + separator + separator + separator + '\n')	
		progressBar.setValue(progressBar.value() + 20)

# 		Distances Totales des Parcours - Non balisé		

		setSectionsRB = setSectionsRB.difference(setSectionsGRMarked)
		distanceRB = round(sum(dicoSectionsGRDistances[id] for id in setSectionsRB) / 1000) 

		line = '      Distances hors GR.P' + separator + separator + 'Total' + separator + '{0:d} km'.format(distanceRB) + separator + 'Tronçons non balisés'
		fileOut.write(line + '\n')	
		progressBar.setValue(progressBar.value() + 20)

		for zoneCode in QGP.dicoZonesNamesRB :
			setTrackZone = { code for code in setTrackRando if TCOD.zoneFromTrackCode(code) == zoneCode }
			sectionsOK, setSectionsRBZone = getSectionsSet(setTrackZone, True)
			setSectionsRBZone = setSectionsRBZone.difference(setSectionsGRMarked)
			distanceRB = round(sum(dicoSectionsGRDistances[id] for id in setSectionsRBZone) / 1000)
			if distanceRB > 0 :
				line = separator + separator + QGP.dicoZonesNamesRB[zoneCode] + separator + '{0:d} km'.format(distanceRB) 
				fileOut.write(line + '\n')	
		line = 'Note' + separator + separator + separator + separator + 'Distances des tronçons non balisés uniquement'
		fileOut.write(line + '\n')	

		fileOut.write(separator + separator + separator + separator + '\n')	
		progressBar.setValue(progressBar.value() + 20)

		fileOut.write(separator + separator + separator + separator + '\n')	

#	Date de génération

	line = 'Créé par : ' + mainFrame.userFullName + separator + separator + separator + separator + 'Généré le ' + TDAT.extractTimeStamp(file)
	fileOut.write(line + '\n')	
	fileOut.write(separator + separator + separator + separator + '\n')	

# Fermer le fichier et fermer la barre d'avancement

	fileOut.close()

	del progressBar


# ========================================================================================
# --- THE END ---
# ========================================================================================
