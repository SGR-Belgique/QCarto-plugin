# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Basic Function to manipulate Encoding values
# ========================================================================================

import importlib

import QCarto_Layers_Tracks as LTRK
importlib.reload(LTRK)

import QCarto_Parameters_Global
importlib.reload(QCarto_Parameters_Global)
QGP = QCarto_Parameters_Global.globalParameters()


# ========================================================================================
# Extract Parcours Type Code from Track Code
# >>> trackCode 		str				Track code 
# <<< type				str				'GR' 'GRP' 'GRT' 'RI' 'RB' 'RF' 'RL' 'IR'
# ========================================================================================

def itineraryTypeFromTrackCode(trackCode):
	try:
		codeParts = trackCode.split('-')
		type = codeParts[0]
		return type
	except:
		return ''


# ========================================================================================
# Extract Itinerary Code from Track Code
# >>> trackCode 		str				Track code 
# <<< itineraryCode		str				Itinerary Code - empty string '' if trackCode is invalid
# ========================================================================================

def itineraryFromTrackCode(trackCode):
	try:
		codeParts = trackCode.split('-')
		type = codeParts[0]
		if type in QGP.typeSetModeGR : 
			return '-'.join(codeParts[0:2])
		elif type in QGP.typeSetModeRB : 
			return '-'.join(codeParts[0:3])
		elif type in QGP.typeSetModeIR : 
			return '-'.join(codeParts[0:2])
		else:
			return ''
	except:
		return ''
		

# ========================================================================================
# Extract Itinerary Folder Code from Track Code - Different fot RB and GR
# >>> trackCode 				str				Track code 
# <<< itineraryFolderCode		str				Itinerary Code - empty string '' if trackCode is invalid
# ========================================================================================

def itineraryFolderFromTrackCode(trackCode):
	try:
		codeParts = trackCode.split('-')
		type = codeParts[0]
		if type in QGP.typeSetModeGR :
			return '-'.join(codeParts[0:2])
		elif type in QGP.typeSetModeRB :
			return '-'.join(codeParts[0:2])
		elif type in QGP.typeSetModeIR :
			return '-'.join(codeParts[0:2])
		elif type in QGP.typeSetModeNone :
			return '-'.join(codeParts[0:2])
		else:
			return ''
	except:
		return ''
		

# ========================================================================================
# Extract Project Code from Track Code
# >>> trackCode 		str				Track code 
# <<< projectCode		str				Like Itinerary for GR.P.T // without number for RB.F
# ========================================================================================

def projectFromTrackCode(trackCode):
	try:
		codeParts = trackCode.split('-')
		return '-'.join(codeParts[0:2])
	except:
		return ''

		
# ========================================================================================
# Extract Label GR from Track Code
# >>> trackCode 		str				Track code 
# <<< label				str				Number of GR label
# ========================================================================================

def labelGRFromTrackCode(trackCode):
	try:
		codeParts = trackCode.split('-')
		return codeParts[1]
	except:
		return ''


# ========================================================================================
# Extract Zone from Track Code
# >>> trackCode 		str				Track code 
# <<< zone				str				Zone for RB RL RF 
# ========================================================================================

def zoneFromTrackCode(trackCode):
	try:
		codeParts = trackCode.split('-')
		return codeParts[1] if codeParts[0] in QGP.typeSetModeRB else ''
	except:
		return ''

		
# ========================================================================================
# Extract RB Number from Track Code
# >>> trackCode 		str				Track code 
# <<< number			str				Number for RB RL RF 
# ========================================================================================

def numberFromTrackCode(trackCode):
	try:
		codeParts = trackCode.split('-')
		return codeParts[2] if codeParts[0] in QGP.typeSetModeRB else ''
	except:
		return ''


# ========================================================================================
# Extract Track Base Code from Track Code (For RB RF IR)
# >>> trackCode 		str				Track code 
# <<< trackBaseCode		str				Track Base Code - (without tags -R -A -V -J -L) - except cases $
# ========================================================================================

def trackBaseCodeFromTrackCode(trackCode):

	if trackCode[-1] == '$': return trackCode[0:-1]

	codeParts = trackCode.split('-')
	trackBaseCodeParts = codeParts.copy()

	firstPart = 3 if itineraryTypeFromTrackCode(trackCode) != 'IR' else 2
	for part in codeParts[firstPart:]:
		if part[0] in ('R', 'V', 'L', 'A', 'J'):
			trackBaseCodeParts.remove(part)

	return '-'.join(trackBaseCodeParts)		
		
		
# ========================================================================================
# Remove all R V L A J B suffixes from track code - used for matching of point - track
# >>> trackCode 		str				Track code 
# <<< trackCode			str				Track Base Code : without tags -R -A -V -J -L -B without * $
# ========================================================================================
				
def removeRVLAJBFromTrackCode(trackCode):

	if trackCode[-1] in ('$', '*') : trackCode = trackCode[0:-1]

	codeParts = trackCode.split('-')
	trackBaseCodeParts = codeParts.copy()

	firstPart = len(itineraryFromTrackCode(trackCode))
	for part in codeParts[firstPart:]:
		if part[0] in ('R', 'V', 'L', 'A', 'J', 'B'):
			trackBaseCodeParts.remove(part)

	return '-'.join(trackBaseCodeParts)		
	
	
# ========================================================================================
# Remove all -MT -MF -# from track code - used for matching of poi - track
# >>> trackCode 		str				Track code 
# <<< trackCode			str				Track Base Code : without tags -M -#
# ========================================================================================		
		
def removeModificationsFromTrackCode(trackCode):

	codeParts = trackCode.split('-')
	trackBaseCodeParts = codeParts.copy()

	firstPart = len(itineraryFromTrackCode(trackCode).split('-'))
	for part in codeParts[firstPart:] :
		if part[0] in ('M', '#'):
			trackBaseCodeParts.remove(part)

	return '-'.join(trackBaseCodeParts)		

		
# ========================================================================================
# Extract Priority List from Track Code (For RB RF IR)
# >>> trackCode 		str				Track code 
# <<< priorityList 		str				List of  -R -A -V -J -L codes
# ========================================================================================

def trackPriorityListFromFromTrackCode(trackCode):

	firstPart = 3 if itineraryTypeFromTrackCode(trackCode) != 'IR' else 2

	return trackCode.split('-')[firstPart:]		
		

# ========================================================================================
# Purify Track Code - Remove special * characters
# >>> trackCode 		str				Track code 
# <<< trackCode			str				Track code 
# ========================================================================================

def purifyTrackCode(trackCode):
	return trackCode.replace('*','').replace('$','')
		

# ========================================================================================
# Extract list of codes from appropriate feature xx_list depending on type
# >>> feature 			QgsFeature			Feature 'Tronçons-GR'		
# >>> type				str					Itinerary Type : 'GR' 'GRP' 'GRT' 'RB' 'RF' 'RL' 'IR'
# <<< codeList			[gr_code]			List of 
# ========================================================================================		

def grCodeListFromSectionFeature(feature, type):

	if type == 'GR-P-T':
		return grCodeListFromSectionFeature(feature, 'GR') + grCodeListFromSectionFeature(feature, 'GRT')
	if type == 'RB-F-L-IR':
		return grCodeListFromSectionFeature(feature, 'RB') + grCodeListFromSectionFeature(feature, 'RF') + grCodeListFromSectionFeature(feature, 'RL') + \
					grCodeListFromSectionFeature(feature, 'RI') + grCodeListFromSectionFeature(feature, 'IR') 

	if type == 'GR':
		field = feature[QGP.tableSectionsFieldGRList]
	elif type == 'GRP':
		field = feature[QGP.tableSectionsFieldGRList]
	elif type == 'GRT':
		field = feature[QGP.tableSectionsFieldGRTList]
	elif type == 'RI':
		field = feature[QGP.tableSectionsFieldRIList]
	elif type == 'RL':
		field = feature[QGP.tableSectionsFieldRLList]
	elif type == 'RB':
		field = feature[QGP.tableSectionsFieldRBList]
	elif type == 'RF':
		field = feature[QGP.tableSectionsFieldRFList]
	elif type == 'IR':
		field = feature[QGP.tableSectionsFieldIRList]
	else:	
		field = None
	
	if field == None: field = ''
		
	return field.split()


# ========================================================================================
# Extract list of all codes GR GRP GRT RL RB RF IR from requested feature
# >>> feature 			QgsFeature			Feature 'Tronçons-GR'		
# <<< codeList			[gr_code]			List of 
# ========================================================================================		

def getCodeListALLFromSectionFeature(feature):
	fieldGR  = feature[QGP.tableSectionsFieldGRList]  if feature[QGP.tableSectionsFieldGRList]  != None else ''
	fieldGRT = feature[QGP.tableSectionsFieldGRTList] if feature[QGP.tableSectionsFieldGRTList] != None else ''
	fieldRI  = feature[QGP.tableSectionsFieldRIList]  if feature[QGP.tableSectionsFieldRIList]  != None else ''
	fieldRL  = feature[QGP.tableSectionsFieldRLList]  if feature[QGP.tableSectionsFieldRLList]  != None else ''
	fieldRB  = feature[QGP.tableSectionsFieldRBList]  if feature[QGP.tableSectionsFieldRBList]  != None else ''
	fieldRF  = feature[QGP.tableSectionsFieldRFList]  if feature[QGP.tableSectionsFieldRFList]  != None else ''
	fieldIR  = feature[QGP.tableSectionsFieldIRList]  if feature[QGP.tableSectionsFieldIRList]  != None else ''
	
	field = fieldGR + ' ' + fieldGRT + ' ' + fieldRI + ' ' + fieldRL + ' ' + fieldRB + ' ' + fieldRF + ' ' + fieldIR
		
	return field.split()


# ========================================================================================
# Extract list of codes GR GRP GRT from requested feature
# >>> feature 			QgsFeature			Feature 'Tronçons-GR'		
# <<< codeList			[gr_code]			List of 
# ========================================================================================		

def getCodeListGRFromSectionFeature(feature):
	fieldGR = feature[QGP.tableSectionsFieldGRList] if feature[QGP.tableSectionsFieldGRList] != None else ''
	fieldGRT = feature[QGP.tableSectionsFieldGRTList] if feature[QGP.tableSectionsFieldGRTList] != None else ''
	
	field = fieldGR + ' ' + fieldGRT
		
	return field.split()

# ========================================================================================
# Extract list of codes RL RB RF from requested feature
# >>> feature 			QgsFeature			Feature 'Tronçons-GR'		
# <<< codeList			[gr_code]			List of 
# ========================================================================================		

def getCodeListRBFromSectionFeature(feature):
	fieldRI = feature[QGP.tableSectionsFieldRIList] if feature[QGP.tableSectionsFieldRIList] != None else ''
	fieldRL = feature[QGP.tableSectionsFieldRLList] if feature[QGP.tableSectionsFieldRLList] != None else ''
	fieldRB = feature[QGP.tableSectionsFieldRBList] if feature[QGP.tableSectionsFieldRBList] != None else ''
	fieldRF = feature[QGP.tableSectionsFieldRFList] if feature[QGP.tableSectionsFieldRFList] != None else ''
	
	field = fieldRI + ' ' + fieldRL + ' ' + fieldRB + ' ' + fieldRF
		
	return field.split()


# ========================================================================================
# Extract dico of all codes from requested feature
# >>> feature 			QgsFeature				Feature 'Tronçons-GR'		
# <<< codeDico			{ GR : gr_list ...}
# ========================================================================================		
		
def getCodeDicoFromSectionFeature(feature):
	fieldGR  = feature[QGP.tableSectionsFieldGRList]  if feature[QGP.tableSectionsFieldGRList]  != None else ''
	fieldGRT = feature[QGP.tableSectionsFieldGRTList] if feature[QGP.tableSectionsFieldGRTList] != None else ''
	fieldRI  = feature[QGP.tableSectionsFieldRIList]  if feature[QGP.tableSectionsFieldRIList]  != None else ''
	fieldRL  = feature[QGP.tableSectionsFieldRLList]  if feature[QGP.tableSectionsFieldRLList]  != None else ''
	fieldRB  = feature[QGP.tableSectionsFieldRBList]  if feature[QGP.tableSectionsFieldRBList]  != None else ''
	fieldRF  = feature[QGP.tableSectionsFieldRFList]  if feature[QGP.tableSectionsFieldRFList]  != None else ''
	fieldIR  = feature[QGP.tableSectionsFieldIRList]  if feature[QGP.tableSectionsFieldIRList]  != None else ''
	
	return {'gr_list' : fieldGR.split(), 'grt_list' : fieldGRT.split(), 'ri_list' : fieldRI.split(), 'rl_list' : fieldRL.split(), 'rb_list' : fieldRB.split(), 'rf_list' : fieldRF.split(), 'ir_list' : fieldIR.split() }
		

# ========================================================================================
# Extract gr_code from Point feature
# >>> feature 			QgsFeature			Feature 'Repères-GR'		
# <<< gr_code			str					gr_code field - empty string '' if gr_code is NULL
# ========================================================================================		
		
def grCodeFromPointFeature(feature):
	gr_code = feature[QGP.tablePointsFieldGRCode]
	return gr_code.strip() if gr_code != None else ''


# ========================================================================================
# Décomposer un code gr_code
#  >>> gr_code				: str			Code gr_code élémentaire
#  <<< valid				: bool			Code is valid
#  <<< type					: str			Itinerary Type : 'GR' 'GRP' 'GRT' 'RB' 'RF' 'RL' 'IR'
#  <<< label				: str			Label (GR GRP GRT)
#  <<< zone					: str			Zone (RB, RF, RL)
#  <<< number				: str 			Number (RB, RF, RL, IR)
#  <<< itineraryCode		: str			Itineary Code
#  <<< trackBaseCode		: str			Track base code (without tags -M -#) (without tags -X -Y -1) (without tags -R -A -V -J -L) 
#  <<< trackCode 			: str 			Track full code (without tags -M -#) (without tags -X -Y -1)
#  <<< modificationList 	: [str]			List of modifications tags (-MTag)
#  <<< invalidationList		: [str]			List of invalid tags (-#Tag)
#  <<< repeatCount  		: int			Number of repetitions (-Xnn)
#  <<< bifurcationNumber	: int			Number of bifurcation (-Ynn)
#  <<< direction			: str			Direction code (-1d)	
# ========================================================================================
		
def elementsFromGrCode(gr_code):

	valid = True
	modificationList = []
	invalidationList = []
	repeatCount = 1
	bifurcationNumber = QGP.C_ComputeTrackBifurcationDefault
	direction = None

	try:
		codeParts = gr_code.split('-')

		trackCodeParts = codeParts.copy()
		trackBaseCodeParts = codeParts.copy()

		type = codeParts[0]
		label = codeParts[1] if type in QGP.typeSetModeGR else ''
		zone = codeParts[1] if type in QGP.typeSetModeRB else ''
		number = codeParts[2] if type in QGP.typeSetModeRB else ''
		number = codeParts[1] if type in QGP.typeSetModeIR else number

		itineraryCode = itineraryFromTrackCode(gr_code)
		
		if type in ('GR', 'GRP', 'GRT', 'IR'):	firstPart = 2 
		if type in ('RI', 'RB', 'RF', 'RL'):	firstPart = 3

		for part in codeParts[firstPart:]:
			if part[0] == 'M':
				if part[1:] != '' : modificationList.append(part[1:])
				trackCodeParts.remove(part)
				trackBaseCodeParts.remove(part)
			if part[0] == '#':
				if part[1:] != '' : invalidationList.append(part[1:])
				trackCodeParts.remove(part)
				trackBaseCodeParts.remove(part)
			if part[0] == 'X':
				repeatCount = int(part[1:]) if part[1:].isdigit() else 1
				trackCodeParts.remove(part)
				trackBaseCodeParts.remove(part)
			if part[0] == 'Y':
				bifurcationNumber = int(part[1:]) if part[1:].isdigit() else 99
				trackCodeParts.remove(part)
				trackBaseCodeParts.remove(part)
			if part[0] == '1':
				direction = part[1:]
				trackCodeParts.remove(part)
				trackBaseCodeParts.remove(part)
			if part[0] in ('R', 'V', 'L', 'A', 'J'):
				trackBaseCodeParts.remove(part)

	except:
		return False, '', '', '', '', '', '', '', modificationList, invalidationList, repeatCount, bifurcationNumber, direction

	trackBaseCode = '-'.join(trackBaseCodeParts)		
	trackCode = '-'.join(trackCodeParts)

	return valid, type, label, zone, number, itineraryCode, trackBaseCode, trackCode, modificationList, invalidationList, repeatCount, bifurcationNumber, direction
	

# ========================================================================================
# Test divers for GR GRP GRT
#  >>> gr_code				: str			Code gr_code élémentaire
# ========================================================================================

def isCodePrincipalGR(gr_code):
	try:
		codeparts = gr_code.split('-')
		return len(codeparts) == 2 or codeparts[2][0] == 'P'
	except:
		return False

def isCodeVarianteGR(gr_code):
	try:
		return gr_code.split('-')[2][0] == 'V'
	except:
		return False

def isCodeLiaisonGR(gr_code):
	try:
		return gr_code.split('-')[2][0] == 'L'
	except:
		return False

def isCodeShortcutGR(gr_code):
	try:
		return gr_code.split('-')[2][0] == 'R'
	except:
		return False

def isCodeBoucleGR(gr_code):
	try:
		return gr_code.split('-')[2][0] == 'B'
	except:
		return False
		
def isCodeModifiedGR(gr_code):		
	try:
		codeparts = gr_code.split('-')
		return any(part[0] == 'M' for part in codeparts[2:])
	except:
		return False
		

# ========================================================================================
# Test divers for RB RF RL IR
#  >>> gr_code				: str			Code gr_code élémentaire
# ========================================================================================

def isCodeBaseRB(gr_code):
	firstPart = 3 if itineraryTypeFromTrackCode(gr_code) != 'IR' else 2
	try:
		codeparts = gr_code.split('-')
		return len(codeparts) == firstPart
	except:
		return False
		
def isCodeVariantRB(gr_code):
	firstPart = 3 if itineraryTypeFromTrackCode(gr_code) != 'IR' else 2
	try:
		codeparts = gr_code.split('-')
		return any(suffix[0] == 'V' for suffix in codeparts[firstPart:])
	except:
		return False		

def isCodeElongationRB(gr_code):
	firstPart = 3 if itineraryTypeFromTrackCode(gr_code) != 'IR' else 2
	try:
		codeparts = gr_code.split('-')
		return any(suffix[0] == 'A' for suffix in codeparts[firstPart:])
	except:
		return False	
		
def isCodeShorcutRB(gr_code):
	firstPart = 3 if itineraryTypeFromTrackCode(gr_code) != 'IR' else 2
	try:
		codeparts = gr_code.split('-')
		return any(suffix[0] == 'R' for suffix in codeparts[firstPart:])
	except:
		return False	
		
def isCodeDayRB(gr_code):
	firstPart = 3 if itineraryTypeFromTrackCode(gr_code) != 'IR' else 2
	try:
		codeparts = gr_code.split('-')
		return any(suffix[0] == 'J' for suffix in codeparts[firstPart:])
	except:
		return False	
		
		
# ========================================================================================
# ========================================================================================
#
#  Fonctions de Gestion de Modifications -M -#
# 
# ========================================================================================		
# ========================================================================================

		
# ========================================================================================
# Déterminer la compatibilité des codes de modification entre section et Code du tracé calculé
# Egalement valable pour la compatibilié entre repère et tracé
# 		Section / Tracé  	None				-M [xyz]			  -# [xyz]
# 		---------------+-------------------------------------------------------------
#    	  None	       |    True     			True				  True
#    	 -M [abc]      |    False 				Any xyz in [abc]	  not Any xyz in abc
#    	 -# [abc]      |    True	 			not Any xyz in abc    Any xyz in abc
# ========================================================================================	

def modificationCodesCompatibility(sectionModifTags, sectionInvalidTags, trackModifTags, trackInvalidTags):
	if '0' in sectionInvalidTags: return False
	if 'A' in sectionInvalidTags: return False
	if sectionModifTags == [] and sectionInvalidTags == []:														# Ligne 1 du tableau
		return True
	elif sectionModifTags != []:																				# Ligne 2 du tableau
		if trackModifTags == [] and trackInvalidTags == []:
			return False
		elif trackModifTags != []:
			return any(tag in sectionModifTags for tag in trackModifTags)
		else:
			return not any(tag in sectionModifTags for tag in trackInvalidTags)
	else:																										# Ligne 3 du tableau
		if trackModifTags == [] and trackInvalidTags == []:
			return True
		elif trackModifTags != []:
			return not any(tag in sectionInvalidTags for tag in trackModifTags)
		else:
			return any(tag in sectionInvalidTags for tag in trackInvalidTags)


# ========================================================================================
# Check compatibility between track code and gr code of repère
# >>> trackCode 		str				Track code 
# >>> grCode			str				Repère gr_code
# <<< 					bool			True if compatible
# ========================================================================================		
		
def areTrackAndPointCodesCompatibles(trackCode, grCode):
	trackValid, trackType, u_Label, u_Zone, u_Number, trackItineraryCode, trackTrackBaseCode, trackTrackCode, \
					trackModifList, trackInvalidationList, u_RepeatCount, u_BifurcationNumber, u_Direction = elementsFromGrCode(trackCode)
	pointValid, pointType, u_Label, u_Zone, u_Number, pointItineraryCode, pointTrackBaseCode, pointTrackCode, \
					pointModifList, pointInvalidationList, u_RepeatCount, u_BifurcationNumber, u_Direction = elementsFromGrCode(grCode)

	if not trackValid or not pointValid : return False
	if not modificationCodesCompatibility(pointModifList, pointInvalidationList, trackModifList, trackInvalidationList): return False

	if pointTrackBaseCode == trackTrackBaseCode: return True
	if pointType in QGP.typeSetModeGR and trackType in QGP.typeSetModeGR and pointTrackBaseCode == trackItineraryCode: return True
	return False
		
		
# ========================================================================================
# ========================================================================================
#
#  Fonctions de Tri
# 
# ========================================================================================		
# ========================================================================================
		
		
# ========================================================================================
# Fonction de tri pour une liste de codes Tracés GR / GRP / GRT
#  >>> trackCode 			: str				codeTrack du tracé
#  <<< 						: int				valeur de tri
# ========================================================================================

def getTrackCodeGRSortingValue(trackCode):

#	12222333

	try:
		codeParts = trackCode.split('-')

		tri_1 = 9
		if codeParts[0] == 'GR':	tri_1 = 1
		if codeParts[0] == 'GRP':	tri_1 = 2
		if codeParts[0] == 'GRT':	tri_1 = 3
		
		tri_2 = int('0' + ''.join(c for c in codeParts[1] if c.isdigit()))
		if tri_2 == 0:
			tri_2 = 9999
			if codeParts[1] == 'SAT':	tri_2 = 9001
			if codeParts[1] == 'SMA':	tri_2 = 9002
			if codeParts[1] == 'BVW':	tri_2 = 9003

		if len(codeParts) > 2:
			tri_3 = int('0' + ''.join(c for c in codeParts[2] if c.isdigit()))
			if codeParts[2][0] == 'P': tri_3 += 500
			if codeParts[2][0] == 'V': tri_3 += 600
			if codeParts[2][0] == 'L': tri_3 += 700
			if codeParts[2][0] == 'B': tri_3 += 800
		else:
			tri_3 = 0
	except: 
		return 9999999999
			
	return tri_1 * 10**7 + tri_2 * 10**3 + tri_3	
			
	
# ========================================================================================
# Fonction de tri pour une liste de codes Tracés RB / RF / RL
#  >>> trackCode 			: str				codeTrack du tracé
#  <<< 						: int				valeur de tri
# ========================================================================================

def getTrackCodeRBSortingValue(trackCode):

#	12233344

	try:
		codeParts = trackCode.split('-')

		tri_1 = 9
		if codeParts[0] == 'RB':	tri_1 = 1
		if codeParts[0] == 'RF':	tri_1 = 2
		if codeParts[0] == 'RL':	tri_1 = 3
		if codeParts[0] == 'RI':	tri_1 = 4
	
		tri_2 = 0
		if codeParts[1] == 'BB' : tri_2 = 10
		if codeParts[1] == 'Br' : tri_2 = 20
		if codeParts[1] == 'BW' : tri_2 = 30
		if codeParts[1] == 'Ha' : tri_2 = 40
		if codeParts[1] == 'Lg' : tri_2 = 50
		if codeParts[1] == 'Lu' : tri_2 = 60
		if codeParts[1] == 'Na' : tri_2 = 70
		if codeParts[1] == 'PN' : tri_2 = 80
	
		tri_3 = int('0' + ''.join(c for c in codeParts[2] if c.isdigit()))
		if codeParts[1] == 'PN':
			tri_3 *= 3
			if codeParts[2][-1] == 'A' : tri_3 += 0
			if codeParts[2][-1] == 'B' : tri_3 += 1
			if codeParts[2][-1] == 'C' : tri_3 += 2

		if len(codeParts) > 3:
			tri_4 = int('0' + ''.join(c for c in codeParts[3] if c.isdigit()))
			if codeParts[3][0] == 'R': tri_4 += 10
			if codeParts[3][0] == 'V': tri_4 += 20
			if codeParts[3][0] == 'A': tri_4 += 30
		else:
			tri_4 = 0
		
	except: 
		return 9999999999
				
#	print('getTrackCodeRBSortingValue : ' + trackCode + ' = ' + str(tri_1 * 10**7 + tri_2 * 10**5 + tri_3 * 10**2 + tri_4))
	return tri_1 * 10**7 + tri_2 * 10**5 + tri_3 * 10**2 + tri_4 
			

# ========================================================================================
# Fonction de tri pour une liste de codes de Parcours GR
#	- les parcours principaux
#	- ensuite les variantes
#	- puis les liaisons
#	- puis les boucles
#  >>> trackCode 			: str				codeTrack du tracé
#  <<< 						: int				valeur de tri
# ========================================================================================

def getTrackTableGRSortingValue(trackCode):								
	parts = trackCode.split('-')
	if len(parts) < 2: return 999999
	if len(parts) == 2: return 0
	if len(parts) == 3 and parts[2] == 'MT': return 10
	if len(parts) == 3 and parts[2] == 'MF': return 20	

	num = int('0' + ''.join([c for c in parts[2][1:] if c.isdigit()]))
	if parts[2][0] == 'P': return 2000 + num
	if parts[2][0] == 'V': return 3000 + num
	if parts[2][0] == 'L': return 4000 + num
	return 5000 + num


# ========================================================================================
# Fonction de tri pour une liste de codes de Parcours RB
#	- les parcours de base
#	- les raccourcis
#	- ensuite les variantes et allongements 
#	- puis les jours
#  >>> trackCode 			: str				codeTrack du tracé
#  <<< 						: int				valeur de tri
# ========================================================================================

def getTrackTableRBSortingValue(trackCode):								
	parts = trackCode.split('-')
	if len(parts) < 3: return 999999
	numRB = 10000 * int('0' + ''.join([c for c in parts[2] if c.isdigit()]))
	if parts[2][-1] == 'A' : numRB += 1000
	if parts[2][-1] == 'B' : numRB += 2000
	if parts[2][-1] == 'C' : numRB += 3000
	if '_O' in parts[2]: numRB += 500
	if '_N' in parts[2]: numRB += 500
	if len(parts) == 3: return numRB

	numV = int('0' + ''.join([c for c in parts[3][1:] if c.isdigit()]))
	if parts[3][0] == 'R': return numRB + 100 + numV
	if parts[3][0] == 'V': return numRB + 200 + numV
	if parts[3][0] == 'A': return numRB + 300 + numV
	if parts[3][0] == 'J': return numRB + 400 + numV
	return 500 + numRB


# ========================================================================================
# Fonction de tri pour une liste de codes de Parcours GR / RB
#  >>> trackCode 			: str				codeTrack du tracé
#  <<< 						: int				valeur de tri
# ========================================================================================

def getTrackTableALLSortingValue(trackCode):		
	
	type = itineraryTypeFromTrackCode(trackCode)
	if type in QGP.typeSetTableGR : return getTrackTableGRSortingValue(trackCode)
	if type in QGP.typeSetTableRB : return getTrackTableRBSortingValue(trackCode)
	return 999999


# ========================================================================================
# --- THE END ---
# ========================================================================================