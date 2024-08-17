# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ========================================================================================

from qgis.core import *
from qgis.gui import *

import importlib

import QCarto_Tools_Coding as TCOD
import QCarto_Tools_Files as TFIL
import QCarto_Tools_SCR as TSCR
importlib.reload(TSCR)

import QCarto_Parameters_Global
QGP = QCarto_Parameters_Global.globalParameters()


# ========================================================================================
# Créer le fichier .csv de la Table des Parcours
# >>> path			: str			directory path
# >>> file			: str			file name including .csv
# >>> dicoTrackGR	: dict 			dictionnazire des Parcours GR - Ignoré si None
# >>> dicoTrackRB	: dict			dictionnazire des Parcours RB - Ignoré si None
# ========================================================================================

def exportCsvTracksDico(path, file, dicoTrackGR, dicoTrackRB):

# Supprimer les anciens fichiers

	TFIL.remove_files(path, QGP.fileDeliveryTracksTableCsv, len(file))

# Open CSV File

	TFIL.ensure_dir(path)
	csvFilePath = path + file
	fileOut = open(csvFilePath, 'w', encoding='utf-8', errors='ignore')
	
	separator = QGP.configCSVSeparator
	
# Write Header

	line = 'Code' + separator + 'Nom' + separator + 'Etat' + separator + 'Distance' + separator + 'D+' + separator + 'D-' + separator + 'Altitude Min' + separator + 'Altitude Max'
	fileOut.write(line + '\n')	


# Export CSV tracks

	if dicoTrackGR != None:
		for code in sorted(dicoTrackGR, key = lambda x : TCOD.getTrackCodeGRSortingValue(x)) :
			line = TCOD.purifyTrackCode(code) + separator + str(dicoTrackGR[code][QGP.tableTracksFieldName]) + separator + str(dicoTrackGR[code][QGP.tableTracksFieldStatus]) + separator + \
						('{:.0f}'.format(dicoTrackGR[code][QGP.tableTracksFieldDistance]) 		if dicoTrackGR[code][QGP.tableTracksFieldDistance] != None 		else 'Non calculé') + separator + \
						('{:.0f}'.format(dicoTrackGR[code][QGP.tableTracksFieldDenivelePos]) 	if dicoTrackGR[code][QGP.tableTracksFieldDenivelePos] != None 	else 'Non calculé') + separator + \
						('{:.0f}'.format(dicoTrackGR[code][QGP.tableTracksFieldDeniveleNeg]) 	if dicoTrackGR[code][QGP.tableTracksFieldDeniveleNeg] != None 	else 'Non calculé') + separator + \
						('{:.0f}'.format(dicoTrackGR[code][QGP.tableTracksFieldAltmin]) 		if dicoTrackGR[code][QGP.tableTracksFieldAltmin] != None 		else 'Non calculé') + separator + \
						('{:.0f}'.format(dicoTrackGR[code][QGP.tableTracksFieldAltmax]) 		if dicoTrackGR[code][QGP.tableTracksFieldAltmax] != None 		else 'Non calculé') 
			fileOut.write(line + '\n')	

	if dicoTrackRB != None:
		for code in sorted(dicoTrackRB, key = lambda x : TCOD.getTrackCodeRBSortingValue(x)) :
			line = TCOD.purifyTrackCode(code) + separator + str(dicoTrackRB[code][QGP.tableTracksFieldName]) + separator + str(dicoTrackRB[code][QGP.tableTracksFieldStatus]) + separator + \
						('{:.0f}'.format(dicoTrackRB[code][QGP.tableTracksFieldDistance]) 		if dicoTrackRB[code][QGP.tableTracksFieldDistance] != None 		else 'Non calculé') + separator + \
						('{:.0f}'.format(dicoTrackRB[code][QGP.tableTracksFieldDenivelePos]) 	if dicoTrackRB[code][QGP.tableTracksFieldDenivelePos] != None 	else 'Non calculé') + separator + \
						('{:.0f}'.format(dicoTrackRB[code][QGP.tableTracksFieldDeniveleNeg]) 	if dicoTrackRB[code][QGP.tableTracksFieldDeniveleNeg] != None 	else 'Non calculé') + separator + \
						('{:.0f}'.format(dicoTrackRB[code][QGP.tableTracksFieldAltmin]) 		if dicoTrackRB[code][QGP.tableTracksFieldAltmin] != None 		else 'Non calculé') + separator + \
						('{:.0f}'.format(dicoTrackRB[code][QGP.tableTracksFieldAltmax]) 		if dicoTrackRB[code][QGP.tableTracksFieldAltmax] != None 		else 'Non calculé') 
			fileOut.write(line + '\n')	

 # Fermer le fichier

	fileOut.close()
 
# ========================================================================================
# Créer le fichier Trace .csv
# >>> path			: directory path
# >>> file			: file name including .csv
# >>> track 		: [QgsPoints]
# >>> pointsList	: [ [wp features, Track Point Number] ]							
# ========================================================================================

def exportCsvTrack(path, file, track, pointsList):

# Create Dico Track Point Number > WP	

	dicoPoints = {info[1] : info[0] for info in pointsList}

# Open CSV File

	TFIL.ensure_dir(path)
	csvFilePath = path + file
	fileOut = open(csvFilePath, 'w', encoding='utf-8', errors='ignore')
	
	separator = QGP.configCSVSeparator

# Write Header

	line = 'PointNum' + separator + 'LB08X' + separator + 'LB08Y' + separator + 'Altitude' + separator + 'WPNum' + separator + 'WPText'
	fileOut.write(line + '\n')	

# Write Track Points

	pointNum = 0
	for point in track:
		if pointNum in dicoPoints:
			wpNum  = dicoPoints[pointNum][QGP.tablePointsFieldRepere] if dicoPoints[pointNum][QGP.tablePointsFieldRepere] != None else '-?-'
			wpText = dicoPoints[pointNum][QGP.tablePointsFieldNom] if dicoPoints[pointNum][QGP.tablePointsFieldNom] != None else 'Repère-sans-nom'
			cleanCSVLine(wpNum)
			cleanCSVLine(wpText)
		else:
			wpNum = ''
			wpText = ''
		pointNum += 1
		line = str(pointNum) + separator + str(round(point.x(),3)) + separator + str(round(point.y(),3)) + separator + str(round(point.z(),0)) + separator + str(wpNum) + separator + str(wpText)
		fileOut.write(line + '\n')	

# Fermer le fichier

	fileOut.close()


# ========================================================================================
# Créer le fichier Trace Infos .csv 
# >>> mainMenuFrame 	: class mainMenuFrame				Object Main menu frame for display status
# >>> parentFrame	 	: class menuPageTracesTools			Object Trace Tool
# >>> path				: directory path
# >>> file			 	: file name including .csv
# >>> codeExported		: str								Code du tracé à exporter 
# <<< trackCommuneSet	: set()								Ensemble des communes traversés
# ========================================================================================

def exportCsvTrackInfos(mainMenuFrame, parentFrame, path, file, codeExported ):

#	Dictionnaire des Communes :														parentFrame.dicoCommunes
#	Dictionnaire des Tracés GR : trackId > feature Parcours GR						mainMenuFrame.dicoTracksGRFeatures
#	Dictionnaire des Tracés RB : trackId > feature Parcours GR						mainMenuFrame.dicoTracksRBFeatures
#	Dictionnaire des Segments  : idSection > feature Section						mainMenuFrame.dicoSectionsGRFeatures
# 	Dictionnaire des Points extrémités des Segments : idSection > [PointA, PointZ]	mainMenuFrame.dicoSectionsGRFeaturesEndPoints
#	Dictionnaire des Tracés > Tronçons : code > set(idSection)						parentFrame.dicoTrackSections
#	Dictionnaire des résultats de calcul 											parentFrame.dicoTracksComputeResults

	trackItinerary = TCOD.itineraryFromTrackCode(codeExported)
	trackGeometry = parentFrame.dicoTracksComputeResults[codeExported][QGP.tableTracksIFieldGeometry]
	trackCommuneSet = set()

#	Retrouver les infos importantes du calcul du tracé 

	sectionOrderedIdList = parentFrame.dicoTracksComputeResults[codeExported][QGP.tableTracksFieldTroncons]
	pointsAttachedList = parentFrame.dicoTracksComputeResults[codeExported][QGP.tableTracksIFieldReperesPos]

#	Créer la liste des passages kilométriques. Chaque info est une sous-liste.
#	Format des élements de la sous-liste : [distance, idSection, repère, nompoint]

	distanceTotal = 0
	infoTrackList = [[distanceTotal, 0, None, sectionOrderedIdList[0], None, None, [], [], None, None, set() ]]
	for idSection in sectionOrderedIdList:
		distanceTotal += mainMenuFrame.dicoSectionsGRFeatures[abs(idSection)].geometry().length()
		grList = TCOD.getCodeListGRFromSectionFeature(mainMenuFrame.dicoSectionsGRFeatures[abs(idSection)])
		rbList = TCOD.getCodeListRBFromSectionFeature(mainMenuFrame.dicoSectionsGRFeatures[abs(idSection)])
		infoTrackList.append([distanceTotal, 0, None, idSection, None, None, grList, rbList, None, None, set(), False ])

	C_infoDistanceSection = 0 ; C_infoDistanceIntermediaire = 1; C_infoPointNumIntermediaire = 2; C_infoIdSection = 3
	C_infoRepere = 4 ; C_infoNomPoint = 5; C_infoGRList = 6; C_infoRBList = 7
	C_infoCommuneRepere = 8; C_infoCommunesSegment = 9
	C_flagsGRRB = 10
	C_flagModificationFuture = 11

#	Nettoyer la liste des autres Parcours GR / GRP / GRT

	for info in infoTrackList[1:]:
		grList = info[C_infoGRList].copy()
		info[C_infoGRList] = []
		for grCode in grList:
			valid, type, u3, u4, u5, sectionItinerary, sectionTrackBaseCode, sectionTrackCode, sectionModifList, sectionInvalidationList, repeatCount, bifurcationNumber, direction = TCOD.elementsFromGrCode(grCode)
			if trackItinerary == sectionItinerary : 
				if 'F' in sectionModifList : info[C_flagModificationFuture] = True
				continue
			info[C_infoGRList].append(sectionTrackCode)
			info[C_flagsGRRB].add(type)
		info[C_infoGRList] = sorted(info[C_infoGRList], key = TCOD.getTrackCodeGRSortingValue)
	mainMenuFrame.setStatusWorking('Parcours : ' + codeExported + ' Liste des autres parcours GR / GRP / GRT triée')

#	Nettoyer la liste des autres Tracés RB / RF / RL

	for info in infoTrackList[1:]:
		rbList = info[C_infoRBList].copy()
		info[C_infoRBList] = []
		for grCode in rbList:
			valid, type, u3, u4, u5, sectionItinerary, sectionTrackBaseCode, sectionTrackCode, sectionModifList, sectionInvalidationList, repeatCount, bifurcationNumber, direction = TCOD.elementsFromGrCode(grCode)
			if trackItinerary == sectionItinerary : 
				if 'F' in sectionModifList : info[C_flagModificationFuture] = True
				continue
			info[C_infoRBList].append(sectionTrackCode)
			info[C_flagsGRRB].add(type)
		info[C_infoRBList] = sorted(info[C_infoRBList], key = TCOD.getTrackCodeRBSortingValue)
		info[C_flagsGRRB] = '-'.join(info[C_flagsGRRB]) + '-'
	mainMenuFrame.setStatusWorking('Parcours : ' + codeExported + ' Liste des autres parcours RB / RF / RL triée')

#	Gérer les points repères

	trackPointsList = [info[0] for info in pointsAttachedList]
	remainingPointsGRList = trackPointsList.copy()															# Contain only points never found	

	mainMenuFrame.setStatusWorking('Parcours : ' + codeExported + ' - Nombre points à accrocher : ' + str(len(trackPointsList)))

#	Trouver le point repère au début du premier segment

	for pointFeature in trackPointsList:
		point = pointFeature.geometry().asPoint()
		idSection = infoTrackList[0][C_infoIdSection]														# First segment id
		lineSection = mainMenuFrame.dicoSectionsGRFeatures[abs(idSection)].geometry().asMultiPolyline()[0]					# First line 
		linePointA = lineSection[0] if idSection > 0 else lineSection[-1]									# First point of first segment
		if point.distance(linePointA) <= QGP.configMatchDistanceShort:
			infoTrackList[0][C_infoRepere] = pointFeature[QGP.tablePointsFieldRepere]
			infoTrackList[0][C_infoNomPoint] = pointFeature[QGP.tablePointsFieldNom]
			remainingPointsGRList.remove(pointFeature)								
			break
	
#	Accrocher les points repères à la fin de chaque segment

	for pointFeature in trackPointsList:
		point = pointFeature.geometry().asPoint()
		for info in infoTrackList[1:]:																		# Try to attach to end of segments
			if info[C_infoRepere] != None: continue															# Already a point attached
			idSection = info[C_infoIdSection]
			lineSection = mainMenuFrame.dicoSectionsGRFeatures[abs(idSection)].geometry().asMultiPolyline()[0].copy()
			linePointZ = lineSection[-1] if idSection > 0 else lineSection[0]
			if point.distance(linePointZ) <= QGP.configMatchDistanceShort:
				info[C_infoRepere] = pointFeature[QGP.tablePointsFieldRepere]
				info[C_infoNomPoint] = pointFeature[QGP.tablePointsFieldNom]
				if pointFeature in remainingPointsGRList: remainingPointsGRList.remove(pointFeature)								
					
		mainMenuFrame.setStatusWorking('Parcours : ' + codeExported + ' - Nombre points à accrocher au milieu : ' + str(len(remainingPointsGRList)))
					
#	Accrocher les points restants au milieu des segments et couper les segments correspondants

	for pointFeature in remainingPointsGRList:
		point = pointFeature.geometry().asPoint()
		for info in infoTrackList[1:] :																		# Try to attach to middle of segment
			idSection = info[C_infoIdSection]
			lineSection = mainMenuFrame.dicoSectionsGRFeatures[abs(idSection)].geometry().asMultiPolyline()[0].copy()
			if idSection < 0: lineSection.reverse()
			pointLineBest, indexLineBest, iP, iN, distance2Line = QgsGeometry.fromPolylineXY(lineSection).closestVertex(point)    
			if distance2Line <= QGP.configMatchDistanceShort**2:
				newInfo = info.copy()
				newInfo[C_infoDistanceIntermediaire] = (-QgsGeometry.fromPolylineXY(lineSection[indexLineBest:]).length())
				newInfo[C_infoPointNumIntermediaire] = indexLineBest
				newInfo[C_infoRepere] = pointFeature[QGP.tablePointsFieldRepere]
				newInfo[C_infoNomPoint] = pointFeature[QGP.tablePointsFieldNom]
				infoTrackList.append(newInfo)
				infoTrackList = sorted(infoTrackList, key = lambda x: x[0] + x[1])
				break

		mainMenuFrame.setStatusWorking('Parcours : ' + codeExported + ' - Nombre points impossible à accrocher au milieu : ' + str(len(remainingPointsGRList)))

#		Créer un sous-dictionnaire des communes traversées par le tracé
		
	dicoTrackCommunes = {commune : parentFrame.dicoCommunes[commune] for commune in parentFrame.dicoCommunes if parentFrame.dicoCommunes[commune].geometry().intersects(trackGeometry)}
	mainMenuFrame.setStatusWorking('Parcours : ' + codeExported + ' Dictionnaire des communes : ' + str(len(dicoTrackCommunes)) + ' communes')

#	Déterminer la commune du premier point repère (en début de ligne 0)

	if infoTrackList[0][C_infoRepere] != None:												
		idSection = infoTrackList[0][C_infoIdSection]												
		lineSection = mainMenuFrame.dicoSectionsGRFeatures[abs(idSection)].geometry().asMultiPolyline()[0]
		linePointA = lineSection[0] if idSection > 0 else lineSection[-1]
		for commune in dicoTrackCommunes:
			if dicoTrackCommunes[commune].geometry().contains(linePointA):
				infoTrackList[0][C_infoCommuneRepere] = commune.title()
				trackCommuneSet.add(commune.title())
				break

#		Déterminer la commune des autres repères

	for info in infoTrackList[1:]:									
		if info[C_infoRepere] == None: continue					
		idSection = info[C_infoIdSection]
		lineSection = mainMenuFrame.dicoSectionsGRFeatures[abs(idSection)].geometry().asMultiPolyline()[0]
		linePointZ = lineSection[-1] if idSection > 0 else lineSection[0]
		for commune in dicoTrackCommunes:
			if dicoTrackCommunes[commune].geometry().contains(linePointZ):
				info[C_infoCommuneRepere] = commune.title()
				trackCommuneSet.add(commune.title())
				break

		mainMenuFrame.setStatusWorking('Parcours : ' + codeExported + ' Communes des repères déterminées')

#	Déterminer les communes travesées par les segments

	idSectionPrevious = None; pointNumPrevious = None
	for info in infoTrackList[1:] :									
		idSection = info[C_infoIdSection]
		lineSection = mainMenuFrame.dicoSectionsGRFeatures[abs(idSection)].geometry().asMultiPolyline()[0]
		if idSection < 0: lineSection.reverse()
		pointNumIntermediaire = info[C_infoPointNumIntermediaire]
		if 	idSection == idSectionPrevious:
			if pointNumIntermediaire != None:
				line = lineSection[pointNumPrevious:pointNumIntermediaire+1]
			else:
				line = lineSection[pointNumPrevious:]
		else:
			if pointNumIntermediaire != None:
				line = lineSection[0:pointNumIntermediaire+1]
			else:
				line = lineSection
		lineGeometry = QgsGeometry.fromPolylineXY(line)		
		communeList = []
		for commune in dicoTrackCommunes:
			if dicoTrackCommunes[commune].geometry().intersects(lineGeometry):
				communeList.append(commune.title())
				trackCommuneSet.add(commune.title())
		info[C_infoCommunesSegment] = communeList
		idSectionPrevious = idSection; pointNumPrevious = pointNumIntermediaire
				
		mainMenuFrame.setStatusWorking('Communes des segments déterminées')

#	Regrouper les lignes aux mêmes tracés, mêmes communes

	for info in infoTrackList:
		info[C_infoIdSection] = [info[C_infoIdSection]]

	doneMerge = False
	while not doneMerge:
		doneMerge = True			
		for lineNum in range(1, len(infoTrackList) - 1):
			if infoTrackList[lineNum][C_infoRepere] != None: continue
			if infoTrackList[lineNum][C_infoGRList] != infoTrackList[lineNum + 1][C_infoGRList]: continue
			if infoTrackList[lineNum][C_infoRBList] != infoTrackList[lineNum + 1][C_infoRBList]: continue
			if infoTrackList[lineNum][C_infoCommunesSegment] != infoTrackList[lineNum + 1][C_infoCommunesSegment]: continue
			if infoTrackList[lineNum][C_flagModificationFuture] != infoTrackList[lineNum + 1][C_flagModificationFuture]: continue
			infoTrackList[lineNum + 1][C_infoIdSection] = infoTrackList[lineNum][C_infoIdSection] + infoTrackList[lineNum + 1][C_infoIdSection]
			infoTrackList.pop(lineNum)	
			doneMerge = False
			break

#	Créer le fichier CSV
#	Distance Repère Nom Commune 
#	                             segmentId FlagsTracés TracéID Nom [Communes]


	dicoTrackFeatures = mainMenuFrame.dicoTracksGRFeatures.copy()
	dicoTrackFeatures.update(mainMenuFrame.dicoTracksRBFeatures)

# Open CSV File

	TFIL.ensure_dir(path)
	csvFilePath = path + file
	fileOut = open(csvFilePath, 'w', encoding='utf-8', errors='ignore')
	
	separator = QGP.configCSVSeparator
	newLine = QGP.configCSVNewLine

	fileOut.write('Distance' + separator + 'Repère' + separator + 'Nom repère' + separator + 'Commune' + separator + \
						'ID Segment' + separator + 'Flags Tracés' + separator + 'Code Tracé' + separator + 'Nom Tracé' + separator + 'Communes' + newLine)

	info = infoTrackList[0]
	distance = info[C_infoDistanceSection] + info[C_infoDistanceIntermediaire]
	distanceText = '{:,.2f}'.format(distance/1000)
	communeRepere = infoTrackList[0][C_infoCommuneRepere] if infoTrackList[0][C_infoCommuneRepere] != None else ""
	fileOut.write(distanceText + separator + str(info[C_infoRepere]) + separator + str(info[C_infoNomPoint]) + separator + communeRepere + newLine)
	
	for info in infoTrackList[1:]:
		distance = info[C_infoDistanceSection] + info[C_infoDistanceIntermediaire]
		distanceText = '{:,.2f}'.format(distance/1000)
		grrbList = info[C_infoGRList] + info[C_infoRBList]
		if grrbList == []:
			fileOut.write(distanceText + separator + separator + separator + separator + str(info[C_infoIdSection]) + (' *' if info[C_flagModificationFuture] else '') + separator + \
						  info[C_flagsGRRB] + separator + separator + separator + str(info[C_infoCommunesSegment]) + newLine)
		else:
			if grrbList[0] in dicoTrackFeatures:
				nomTracé = dicoTrackFeatures[grrbList[0]][QGP.tableTracksFieldName]
			else:
				nomTracé = ""
			fileOut.write(distanceText + separator + separator + separator + separator + str(info[C_infoIdSection])  + (' *' if info[C_flagModificationFuture] else '') + separator + \
			              info[C_flagsGRRB] + separator + grrbList[0] + separator + nomTracé + separator + str(info[C_infoCommunesSegment]) + newLine)
		for grrb in grrbList[1:]:
			if grrb in dicoTrackFeatures:
				nomTracé = dicoTrackFeatures[grrb][QGP.tableTracksFieldName]
			else:
				nomTracé = ""
			fileOut.write(separator + separator + separator + separator + separator + \
				          info[C_flagsGRRB] + separator + grrb + separator + nomTracé + newLine)
		if info[C_infoRepere] != None:
			communeRepere = info[C_infoCommuneRepere] if info[C_infoCommuneRepere] != None else ""
			fileOut.write(distanceText + separator + info[C_infoRepere] + separator + info[C_infoNomPoint] + separator + communeRepere + newLine)
				
	fileOut.close()

	mainMenuFrame.setStatusWorking('Parcours : ' + codeExported + ' Fichier CSV = ' + file)

	return trackCommuneSet


# ========================================================================================
# Créer le fichier des distances itinéraire GR
# >>> path			: directory path
# >>> file			: file name including .csv
# >>> dicoDistances	: Dictionnaire des distances GR
# ========================================================================================

def exportCsvGRItineraryDistances(path, file, dicoDistances):

# Open CSV File

	TFIL.ensure_dir(path)
	csvFilePath = path + file
	fileOut = open(csvFilePath, 'w', encoding='utf-8', errors='ignore')
	
	separator = QGP.configCSVSeparator
	newLine = QGP.configCSVNewLine

# Write Header 

	line = 'Code Parcours' + separator + 'Nom Parcours' + separator + 'Distance' + separator + 'Dénivelé Positif' + separator + 'Dénivelé Négatif'
	fileOut.write(line + newLine)	

# Write Info

	for code in sorted(dicoDistances):
		line = code + separator + dicoDistances[code][0] + separator + '{:.1f} km'.format(dicoDistances[code][1]/1000) + separator + '{:.0f} m'.format(dicoDistances[code][2]) + separator + '{:.0f} m'.format(dicoDistances[code][3])
		fileOut.write(line + newLine)	

# Fermer le fichier

	fileOut.close()


# ========================================================================================
# Créer le fichier des distances parcours GR
# >>> path			: directory path
# >>> file			: file name including .csv
# >>> dicoDistances	: Dictionnaire des distances GR
# ========================================================================================

def exportCsvGRTrackDistances(path, file, dicoDistances):

	exportCsvPlan(path, file, dicoDistances)


# ========================================================================================
# Créer le fichier du plan schema .csv
# >>> path			: directory path
# >>> file			: file name including .csv
# >>> dicoPlan		: Dictionnaire du plan
# ========================================================================================

def exportCsvPlan(path, file, dicoPlan, dicoTracks = None):

# Open CSV File

	TFIL.ensure_dir(path)
	csvFilePath = path + file
	fileOut = open(csvFilePath, 'w', encoding='utf-8', errors='ignore')
	
	separator = QGP.configCSVSeparator
	newLine = QGP.configCSVNewLine

# Write Plan Info

	for code in dicoPlan:
		if code != ' Départ' : continue
		for index in dicoPlan[code]:
			if index == 'Lat - Long':
				line = code + separator + index + separator + '' + separator + '' + separator + dicoPlan[code][index] + separator + ''
				fileOut.write(line + newLine)	
			else:	
				line = code + separator + index + separator + '' + separator + str(dicoPlan[code][index]) + separator + '' + separator + ''
				fileOut.write(line + newLine)	
		fileOut.write(newLine)	

	for code in sorted(dicoPlan):
		if code == ' Départ' : continue
		total = 0
		for index in dicoPlan[code]:
			if ' ' in code:
				line = code + separator + index + separator + '' + separator + '' + separator + dicoPlan[code][index].replace('.',',') + separator + ''
				fileOut.write(line + newLine)	
				continue
			if '>>>' in index:
				if type(dicoPlan[code][index]) == type([]) :
					dist = dicoPlan[code][index][0]
					nomDe = dicoPlan[code][index][1]
					nomA = dicoPlan[code][index][2]
				else :
					dist = dicoPlan[code][index]
					nomDe = dicoTracks[code][index] if dicoTracks != None else '--?--'
					nomA = ' '
				total += dist
				line = code + separator + index.replace('>>>','à') + separator + '{:.1f}'.format(dist).replace('.',',') + separator + '{:.1f}'.format(total).replace('.',',') + separator + nomDe + separator + nomA
				fileOut.write(line + newLine)	
				continue
			if index in ('Total', 'Différence') :
				line = code + separator + index + separator + '{:.1f}'.format(dicoPlan[code][index]).replace('.',',') + separator + '' + separator + '' + separator + ''
				fileOut.write(line + newLine)	
				continue
			line = code + separator + index + separator + '{:.0f}'.format(dicoPlan[code][index]).replace('.',',') + separator + '' + separator + '' + separator + ''
			fileOut.write(line + newLine)	
		fileOut.write(newLine)	

# Fermer le fichier

	fileOut.close()


# ========================================================================================
# Créer le fichier des POI .csv
# >>> path			: directory path
# >>> file			: file name including .csv
# >>> poiFeatures	: [QgsFeatures]
# ========================================================================================

def exportPoiPoints(path, file, poiFeatures):

# Open CSV File

	TFIL.ensure_dir(path)
	csvFilePath = path + file
	fileOut = open(csvFilePath, 'w', encoding='utf-8', errors='ignore')
	
	separator = QGP.configCSVSeparator
	newline   = QGP.configCSVNewLine

# Write Header

	line = 'Lbrt08_X' + separator + 'Lbrt08_Y' + separator + 'Nom' + newline
	fileOut.write(line)

# Write POI

	for poi in poiFeatures:
		lbrt3812_X, lbrt3812_Y = TSCR.convertPointWgs84to3812(poi.geometry().asPoint().x(), poi.geometry().asPoint().y())
		line = str(int(lbrt3812_X)) + separator + str(int(lbrt3812_Y)) + separator + poi['name'] + newline
		fileOut.write(line)

# Fermer le fichier

	fileOut.close()


# ========================================================================================
# Créer le fichier des Livraisons OSM
# >>> path			: directory path
# >>> file			: file name including .csv
# >>> headers   	: [text]
# >>> data 			: [ [text] ]
# ========================================================================================

def exportOsmDeliveryData(path, file, headers, data):

# Open CSV File

	TFIL.ensure_dir(path)
	csvFilePath = path + file
	fileOut = open(csvFilePath, 'w', encoding='utf-8', errors='ignore')
	
	separator = QGP.configCSVSeparator
	newline   = QGP.configCSVNewLine

# Write Header

	line = separator.join(headers) + newline
	fileOut.write(line)

# Write Data

	for info in data:
		line = separator.join(info) + newline
		fileOut.write(line)

# Fermer le fichier

	fileOut.close()


# ========================================================================================
# Remplacer les caractères problématiques dans une line CSV
#  >>> line : str
# ========================================================================================
		
def cleanCSVLine(line):

	line.replace(QGP.configCSVSeparator, QGP.configCSVSeparatorReplacement)
	line.replace(QGP.configCSVNewLine, QGP.configCSVNewLineReplacement)


# ========================================================================================
# --- THE END ---
# ========================================================================================
