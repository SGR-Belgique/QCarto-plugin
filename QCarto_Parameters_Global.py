# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Partage des Paramètres Globaux entre les différents Scripts
# ========================================================================================

from PyQt5.QtCore import *
from PyQt5.QtGui import *


class globalParameters():
	def __init__(self):

		self.version = "Version 7.17 (a)"


# ========================================================================================
# Icone
# ========================================================================================

		self.configQCartoIcon = 'X:/QCarto/Documentation/Images/SGR Carto - Menu - Icone HTML.png'


# ========================================================================================
# Drives
# ========================================================================================

		self.configLocalPath = 'X:/QCarto/'													# Path de Base Personnel pour l'installation locale - Par défaut : 'X:/QCarto/'
		self.configLocalProjectPath = 'X:/QCarto Projets/'									# Path de Base Personnel pour les projets cartographiques
		self.pathDriveCarto = 'Y:/'															# Path de base pour le Drive de l'équipe carto 
		self.configMyDrivePath = 'Z:/'														# Path de base pour mon drive personnel


# ========================================================================================
# ========================================================================================
#
# Base de Donnée Carto - grsentiers - SGR-Carto2023
#
# ========================================================================================
# ========================================================================================

#	Toutes Tables

		self.tableAllFieldNomCarto			= 'nomCarto'
		self.tableAllFieldDateModif			= 'dateModif'

#	Table des Paramères

		self.tableNameQParam		= 'QCarto-Parametres'
		self.tableQParamFieldId		= 'id'
		self.tableQParamFieldGroup  = 'groupe'
		self.tableQParamFieldName   = 'nom'
		self.tableQParamFieldCode   = 'code'
		self.tableQParamFieldValue  = 'valeur'

#	Tables Parcours-GR Parcours-RB

		self.tableNameTracksGR 		= 'Parcours-GR'
		self.tableNameTracksRB 		= 'Parcours-RB'
		self.tableNameTracksGRHist 	= 'Historique-GR'
		self.tableNameTracksRBHist 	= 'Historique-RB'
		self.tableTracksFieldId 			= 'id'
		self.tableTracksFieldCode 			= 'code'
		self.tableTracksFieldName 			= 'nom'
		self.tableTracksFieldStatus 		= 'etat'
		self.tableTracksFieldMarked			= 'balisage'
		self.tableTracksFieldDate	 		= 'date'
		self.tableTracksFieldDistance 		= 'distance'
		self.tableTracksFieldVO		 		= 'vo'
		self.tableTracksFieldDenivelePos	= 'd+'
		self.tableTracksFieldDeniveleNeg	= 'd-'
		self.tableTracksFieldAltmin			= 'altmin'
		self.tableTracksFieldAltmax			= 'altmax'
		self.tableTracksFieldTroncons		= 'troncons'
		self.tableTracksFieldReperes		= 'reperes'
		self.tableTracksFieldOsmid			= 'osmid'
		self.tableTracksFieldIndirect		= 'indirect'
		self.tableTracksFieldDelta			= 'delta'					# Historique only

		
		self.tableTracksQFieldDelta 				= 'delta'
		self.tableTracksQFieldModif 				= 'mod'
		self.tableTracksIFieldErrorCode				= 'errorCode'
		self.tableTracksIFieldCalcul				= 'calcul'
		self.tableTracksIFieldGaps					= 'trous'
		self.tableTracksIFieldSectionsLost 			= 'sectionsLost'
		self.tableTracksIFieldGapsList				= 'gapsList'
		self.tableTracksIFieldGeometry				= 'geometry'
		self.tableTracksIFieldSectionsStartPoint 	= 'sectionStart'			# Numéro du point début pour chaque section du tracé
		self.tableTracksIFieldTrackXYZ				= 'trackXYZ'
		self.tableTracksIFieldTrackXYZS				= 'trackXYZLiss'			# Version Lissée
		self.tableTracksIFieldReperesPos			= 'reperesPosition'
		self.tableTracksIFieldReperesSectionList	= 'reperesSectionList'		# Liste des Sections après le repère jusqu'au suivant
		self.tableTracksIFieldSectionsModif 		= 'sectionsModified'
		self.tableTracksIFieldRecorded	    		= 'recorded'
		self.tableTracksIFieldMarkers				= 'markers'					# Bornes kilométriques
		self.tableTracksIFieldPOIs					= 'pois'
		self.tableTracksIFieldPOIsAll				= 'pois all'
		
		self.tableTracksIFieldDistanceEquivalenteDirecte = 'distEdir'
		self.tableTracksIFieldDistanceEquivalenteInverse = 'distEinv'
		self.tableTracksIFieldEchelleMaxPortrait = 'max █'
		self.tableTracksIFieldEchelleMaxPaysage = 'max ▄▄'
		
		

		self.typeSetTableGR 		= {'GR', 'GRP', 'GRT'}								# Related to table content
		self.typeSetTableRB 		= {'RL', 'RI', 'RB', 'RF', 'IR'}					# Related to table content
		self.typeSetAll				= {'GR', 'GRP', 'GRT', 'RL', 'RI', 'RB', 'RF', 'IR'}	

		self.typeSetComputeGRMode 	= {'GR', 'GRP', 'GRT'}								# Related to Track computation
		self.typeSetComputeRBMode 	= {'RB', 'RF', 'RL', 'RI', 'IR'}					# Related to Track computation

		self.typeSetModeGR  		= {'GR', 'GRP', 'GRT'}								# Related to itinerary extract					
		self.typeSetModeRB 			= {'RB', 'RF', 'RL', 'RI'}							# Related to itinerary extract					
		self.typeSetModeIR 			= {'IR'}											# Related to itinerary extract					
		self.typeSetModeNone		= ('ZZ')											# Only for Map not related to specific itinerary

		self.typeSetSityTrail 		= {'RB', 'RL', 'IR'}								# Related to GPX export for SityTrail

		self.validSuffixDirection	= {'1', 'X', 'Y'}
		self.validSuffixModif		= {'#', 'M'}
		self.validSuffixGR			= {'P', 'V', 'L', 'R', 'B'}
		self.validSuffixRB			= {'A', 'V', 'R', 'J'}

		self.tableTracksProjectVariableHighlight = 'QTrackHighlight'
		self.tableTracksProjectVariableHistory =   'QTrackHistory'

		self.trackStatusProposal = 		'Proposition'
		self.trackStatusProject = 		'Projet'
		self.trackStatusValidated = 	'Validé'
		self.trackStatusPublished = 	'Publié'
		self.trackStatusDeleted = 		'Supprimé'
		self.trackStatusExternal = 		'Externe'

		self.trackStatusForVerificationList = [self.trackStatusProject, self.trackStatusValidated, self.trackStatusPublished]
		self.trackStatusForQBalisage 		= [self.trackStatusValidated, self.trackStatusPublished]
		self.trackStatusForInput 			= [self.trackStatusProposal, self.trackStatusProject, self.trackStatusValidated, self.trackStatusPublished, self.trackStatusDeleted, self.trackStatusExternal]

		self.trackMarkedStandard = 		'Balisage Standard'
		self.trackMarkedNotMarked = 	'Non Balisé'
		self.trackMarkedFuture = 		'Balisage Futur'

		self.trackNotMarkedForQBalisage		= [self.trackMarkedNotMarked, self.trackMarkedFuture]
		self.trackMarkedForInput 			= [self.trackMarkedStandard, self.trackMarkedNotMarked, self.trackMarkedFuture]

#	Table Tronçons-GR 

		self.tableNameSectionsGR 	= 'Tronçons-GR'
		self.tableSectionsFieldId  			= 'id'
		self.tableSectionsFieldGRList		= 'gr_list'
		self.tableSectionsFieldGRTList		= 'grt_list'
		self.tableSectionsFieldRIList		= 'ri_list'
		self.tableSectionsFieldRLList		= 'rl_list'
		self.tableSectionsFieldRBList		= 'rb_list'
		self.tableSectionsFieldRFList		= 'rf_list'
		self.tableSectionsFieldIRList		= 'ir_list'
		
		self.tableSectionsFieldAllXList = [self.tableSectionsFieldGRList, self.tableSectionsFieldGRTList, \
										   self.tableSectionsFieldRIList, self.tableSectionsFieldRLList, self.tableSectionsFieldRBList, self.tableSectionsFieldRFList, self.tableSectionsFieldIRList]
		
#	Table Repères-GR

		self.tableNamePointsGR 		= 'Repères-GR'
		self.tablePointsFieldId 			= 'id'
		self.tablePointsFieldGRCode 		= 'gr_code'
		self.tablePointsFieldRepere 		= 'repere'
		self.tablePointsFieldNom			= 'nom'

		self.tablePointsGRCodeB2B	= 'B2B'

#	Table Tronçons-GR sur Topo50 Edition 4

		self.tableNameSectionsGREd4	= 'Tronçons-GR-Ed4'		
		
#	Table des Informations supplémentaires pour SityTrail

		self.tableNameSityTrail = 'SityTrail-RB'
		
		self.tableSityFieldCode			= 'code'
		self.tableSityFieldCodeSity		= 'codeST'
		self.tableSityFieldTitre		= 'titre'
		self.tableSityFieldVillages		= 'villages'
		self.tableSityFieldIntro		= 'intro'

# 	Répertoire de Backup et Archivage Qgis Cloud		
		
		self.configBackupPath = self.pathDriveCarto + 'Backup DB Qgis/Backups Qgis Cloud/'	
		self.configArchivePath = self.pathDriveCarto + 'Backup DB Qgis/Archives Qgis Cloud/'	

		self.configDBCartoStylesPath = self.configLocalPath + 'Qgis_Styles/Couches DB/'

#	Dictionnaire des Tables. Nom de la Table : [[ligne dans menu, colonne dans menu], clé primaire, géométrie] 

		self.tableNameDico	= 	{	self.tableNameQParam :				[[1,1], 'id', 	None]	,
									self.tableNameTracksGR :			[[2,1], 'code', 'MultiLineString']	,
									self.tableNameTracksRB :			[[2,3], 'code', 'MultiLineString']	,
									self.tableNameTracksGRHist :		[[3,1], 'id', 	'MultiLineString']	,
									self.tableNameTracksRBHist :		[[3,3], 'id',	'MultiLineString']	,
									self.tableNameSectionsGR :			[[4,1], 'id',	'MultiLineString']	,
									self.tableNameSectionsGREd4 :		[[4,3], 'id',	'MultiLineString']	,
									self.tableNamePointsGR :			[[5,1], 'id',	'Point'] ,		
									self.tableNameSityTrail :			[[6,1], 'id',	None] 		
								}
										
#	URI pour installation

		self.DBCartoPassword = '4c35abd6'

		self.configReseauGRInstallUriGeom = 	"dbname='fbhdtv_qcncfy' host=db.qgiscloud.com port=5432 user='fbhdtv_qcncfy' password='" + self.DBCartoPassword + "' key='%KEY%' estimatedmetadata=true " + \
												"type=%GEOM% checkPrimaryKeyUnicity='1' table='public'.'%LAYER%' (geom) sql="
		self.configReseauGRInstallUriNoGeom = 	"dbname='fbhdtv_qcncfy' host=db.qgiscloud.com port=5432 user='fbhdtv_qcncfy' password='" + self.DBCartoPassword + "' key='%KEY%' estimatedmetadata=true " + \
												"checkPrimaryKeyUnicity='1' table='public'.'%LAYER%' sql="

#	Distance de simplification dans la migration

		self.DBCartoSimplifyDistance = 1

#	Highlight des Tronçons modifiés récemment

		self.tableSectionsGRHighlightVariable	= 'QSectionsHighlight'								# Variable pour highlight des Tronçons modifiés 'Oui' / 'Non'
		self.tableSectionsGRHighlightVariableDe	= 'QSectionsHighlightJoursDe'							
		self.tableSectionsGRHighlightVariableA	= 'QSectionsHighlightJoursA'								



		self.tableSectionsGRHighlightModes = { 'Aujourd\'hui' : 1,
											   '3 jours'	  : 3,
											   'Une semaine'  : 7,
											   'Un mois'	  : 31,
											   '3 mois'		  : 91,
											   '1 an'		  : 365,
											   'Entre Dates'  : None		}


# ========================================================================================
# ========================================================================================
#
# Base de Donnée Carto - grsentiers - POIs
#
# ========================================================================================
# ========================================================================================

		self.userTablePOIsName = 'POIs_Utilisateurs'
		self.keysTablePOIsName = 'POIs_Cles'
		self.poisTablePOIsName = 'POIs_Table'

		self.poisTableFieldId			= 'id'
		self.poisTableFieldIdPOI		= 'id_poi'
		self.poisTableFieldTitre		= 'titre'
		self.poisTableFieldTexte		= 'texte'
		self.poisTableFieldStatus		= 'statut'
		self.poisTableFieldFlux			= 'flux'
		self.poisTableFieldType			= 'type'
		self.poisTableFieldZone			= 'zone'
		self.poisTableFieldTracks		= 'parcours'

		self.tablePOIsNameDico	= 		{	self.userTablePOIsName : 				[0, 'id',	None			]	,
											self.keysTablePOIsName :				[1, 'id', 	None			]	,
											self.poisTablePOIsName :				[2, 'id', 	'Point'			] 
										}	

#	URI pour installation

		self.DBPOIsPassword = 'b6cfc442'

		self.configDBPOIsGRInstallUriGeom = 	"dbname='zvqfll_shphan' host=db.qgiscloud.com port=5432 user='zvqfll_shphan' password='" + self.DBPOIsPassword + "' key='%KEY%' estimatedmetadata=true " + \
												"type=%GEOM% checkPrimaryKeyUnicity='1' table='public'.'%LAYER%' (geom) sql="
		self.configDBPOIsInstallUriNoGeom = 	"dbname='zvqfll_shphan' host=db.qgiscloud.com port=5432 user='zvqfll_shphan' password='" + self.DBPOIsPassword + "' key='%KEY%' estimatedmetadata=true " + \
												"checkPrimaryKeyUnicity='1' table='public'.'%LAYER%' sql="


# ========================================================================================
# ========================================================================================
#
# Base de Donnée Carto - grsentiers - Baliseurs
#
# ========================================================================================
# ========================================================================================

		self.zonesTableBaliseursName = 			'Parcours-Zones'
		self.baliseursTableBaliseursName = 		'Baliseurs-Liste'
		self.sectionsTableBaliseursName = 		'Baliseurs-Tronçons'
		self.historicTableBaliseursName = 		'Historique-Baliseurs'

		self.tableBaliseursNameDico	= 		{	self.zonesTableBaliseursName : 					[0, 'id',	None			]	,
												self.baliseursTableBaliseursName :				[1, 'id', 	None			]	,
												self.sectionsTableBaliseursName :				[2, 'id', 	None			] 	,
												self.historicTableBaliseursName :				[3, 'id', 	None			] 
											}

#	URI pour installation

		self.DBBaliseursPassword = '91d241a4'

		self.configDBBaliseursGRInstallUriGeom = 	"dbname='bopcbg_fkvyyb' host=db.qgiscloud.com port=5432 user='bopcbg_fkvyyb' password='" + self.DBBaliseursPassword + "' key='%KEY%' estimatedmetadata=true " + \
													"type=%GEOM% checkPrimaryKeyUnicity='1' table='public'.'%LAYER%' (geom) sql="
		self.configDBBaliseursInstallUriNoGeom = 	"dbname='bopcbg_fkvyyb' host=db.qgiscloud.com port=5432 user='bopcbg_fkvyyb' password='" + self.DBBaliseursPassword + "' key='%KEY%' estimatedmetadata=true " + \
													"checkPrimaryKeyUnicity='1' table='public'.'%LAYER%' sql="



# ========================================================================================
# ========================================================================================
#
# Base de Donnée Carto - grsentiers - Backup
#
# ========================================================================================
# ========================================================================================

		self.tablesBackupList =		[ 	self.tableNameTracksGR,
										self.tableNameTracksRB,
										self.tableNameSectionsGR,
										self.tableNamePointsGR,
										self.tableNameSectionsGREd4,
										self.tableNameTracksGRHist,
										self.tableNameTracksRBHist,
										self.tableNameQParam,
										self.tableNameSityTrail,
										self.zonesTableBaliseursName,
										self.baliseursTableBaliseursName,
										self.sectionsTableBaliseursName,
										self.historicTableBaliseursName,
										self.userTablePOIsName,
										self.poisTablePOIsName,
										self.keysTablePOIsName			] 
										
		self.tablesBackupReloadList =	[  	self.tableNameTracksGR,
											self.tableNameTracksRB,
											self.tableNameSectionsGR,
											self.tableNamePointsGR		] 


# ========================================================================================
# ========================================================================================
#
# Base de Donnée Carto - grsentiers - Carte Publique
#
# ========================================================================================
# ========================================================================================

#	Nom des Tables

		self.tableNamePublicTracksGR =			'Sentiers-GR-Public'
		self.tableNamePublicTracksGRP =			'Sentiers-GR-de-Pays-Public'
		self.tableNamePublicTracksGRT =			'Sentiers-GR-à-Thème-Public'
		self.tableNamePublicPointsGR = 			'Repères-GR-Public'
		self.tableNamePublicPointsGRP = 		'Repères-GR-de-Pays-Public'
		self.tableNamePublicSectionsClosed = 	'Tronçons-GR-Impraticables-Public'
		self.tableNamePublicStartRB = 			'Randos-Boucle-GR-Public'
		self.tableNamePublicStartRL = 			'Randos-GareAGare-GR-Public'
		self.tableNamePublicStartRI = 			'Randos-Itinérantes-GR-Public'
		self.tableNamePublicStartIR = 			'Idées-Rando-GR-Public'
		self.tableNamePublicZoneRB = 			'Randos-Boucle-Zones-GR-Public'
		self.tableNamePublicUrlsGRSite = 		'URLs-SiteGR-Public'
		self.tableNamePublicUrlsRBSite = 		'URLs-SiteRB-Public'
		
		
#	Champs toutes tables

		self.tablePublicFieldId =			'id'
		self.tablePublicFieldCode =			'code'
		self.tablePublicFieldLabel =		'etiquette'
		self.tablePublicFieldName =			'nom'
		self.tablePublicFieldDistance =		'distance'
		self.tablePublicFieldDPlus =		'd+'
		self.tablePublicFieldDMinus =		'd-'
		self.tablePublicFieldAltMin =		'altmin'
		self.tablePublicFieldAltMax =		'altmax'
		
#	Champs url : GR GRP GRT		
		
		self.tablePublicFieldUrlTopo =		'url-topo'
		self.tablePublicFieldUrlPhoto =		'url-photo'
		
#	Champs repères		
		
		self.tablePublicPointFieldId =			'id'
		self.tablePublicPointFieldCode =		'gr_code'
		self.tablePublicPointFieldRepere =		'repere'
		self.tablePublicPointFieldNom =			'nom'
		
#	Dictionnaire des Tables

#		Numéro de la table (unused) // index // geométrie // type of publication

		self.tablePublicNameDico	= 	{	self.tableNamePublicUrlsGRSite : 		[0, 'code',	 None,				'Url']	,
											self.tableNamePublicUrlsRBSite : 		[1, 'code',	 None,				'Url']	,
											self.tableNamePublicTracksGR :			[2, 'code', 'MultiLineString', 	'Track']	,
											self.tableNamePublicTracksGRP :			[3, 'code', 'MultiLineString', 	'Track']	,
											self.tableNamePublicTracksGRT :			[3, 'code', 'MultiLineString', 	'Track']	,
											self.tableNamePublicPointsGR :			[5, 'id', 	'Point', 			'Point']	,
											self.tableNamePublicPointsGRP :			[6, 'id', 	'Point',			'Point']	,
											self.tableNamePublicSectionsClosed :	[7, 'id', 	'MultiLineString', 	'Section']  ,
											self.tableNamePublicStartRB :			[8, 'code', 'Point',			('RB')]		,
											self.tableNamePublicStartRL :			[9, 'code', 'Point',			('RL')]		,
											self.tableNamePublicStartRI :			[10, 'code', 'Point',			('RI')]		,
											self.tableNamePublicStartIR :			[11, 'code', 'Point',			('IR')]		,
											self.tableNamePublicZoneRB : 			[12, 'code', 'Multipolygon',	('RB','IR')]	
										}

#	Zones des RB

		self.tablePublicRadiusRB = 3800			#	Rayon de cercle zone RB
		self.tablePublicRadiusIR = 3500			#	Rayon de cercle zone IR

#	Log des Publications

		self.pathPublicationsPublicMapLogfile = self.pathDriveCarto + 'Publications Carto/Log/Publications - Carte Publique - Log.csv'


# ========================================================================================
# ========================================================================================
#
# QCarto : Répertoires / Groupes
#
# ========================================================================================
# ========================================================================================

# ========================================================================================
# QCarto Projets - Répertoires
# ========================================================================================

		self.configPathProject = self.configLocalProjectPath															# Répertoire des projets effectifs
		self.configPathMapShapes = self.configLocalProjectPath + '%PROJECT%/Shapes Cartes/'							# Répertoire des shapes cartes du projet
		self.configPathExportCSV = self.configLocalProjectPath + '%PROJECT%/Points Repères CSV pour Excel/'
		self.configPathExportCSVInfos = self.configLocalProjectPath + '%PROJECT%/Traces CSV Infos pour Excel/'		# Répertoire des CSV Infos

# ========================================================================================
# Répertoire Aides
# ========================================================================================

		self.configMenuHelpBasePath = self.configLocalPath + 'Documentation/'
		self.configMenuLogoPath = self.configMenuHelpBasePath + 'Images/SGR Carto - Menu - Logo.png'
	
# ========================================================================================
# Répertoire des Styles
# ========================================================================================

		self.configPathStyles = self.configLocalPath + 'Qgis_Styles/'
		self.configFrameStyle = 'Cadres Cartes/'


# ========================================================================================
# QCarto - Noms des Groupes sur le Canevas Qgis
# ========================================================================================

		self.configDBCartoGroupName			= 'DB Carto'
		self.configDBPOIsGroupName			= 'DB POIs'
		self.configDBBaliseursGroupName		= 'DB Baliseurs'
		self.configMigrateGroupName			= 'Migration'

		self.configFrameGroupName 			= 'Descriptifs Cartes'
		self.configActiveMapGroupName 		= 'Carte Active'
		self.configActiveMapOsmGroupName	= 'Carte Active - Couches Osm'
		self.configActiveRasterOsmGroupName	= 'Carte Active - Fonds Osm'
		self.configActiveProjectGroupName 	= 'Projet Actif'
		self.configOtherProjectGroupName 	= 'Projet Autres'

		self.configGridGroupName 			= 'Carto - Grilles'
		self.configMntGroupName 			= 'Carto - Altitudes'
		self.configBorderGroupName 			= 'Carto - Frontières'
		self.configCdnGroupName 			= 'Carto - Courbes'
		self.configIGN50Ed3GroupName 		= 'Carto - Topo 50 Ed3'
		self.configIGN50Ed4GroupName 		= 'Carto - Topo 50 Ed4'
		self.configIGN400GroupName 			= 'Carto - Topo 400'
		self.configIGN250GroupName 			= 'Carto - Topo 250'	
		self.configIGNCWGroupName 			= 'Carto - CartoWeb'
		
		self.configPublicMapGroupName		= 'DB - Carte Publique'

		self.configOsmTrackGroupName		= 'Parcours Osm'


# ========================================================================================
# ========================================================================================
#
# QCarto - Parcours
#
# ========================================================================================
# ========================================================================================

#	Gestion des Altitudes		
		
		self.configAltitudeNotFound = -9999		
		self.configAltitudeSmoothRange = 8
		self.configAltitudeSmoothDistance = 50

#	Repères

		self.configMatchWPDistance = 5

#	Calcul

		self.C_ComputeTrackBifurcationDefault = 99
		self.configMatchDistanceShort = 10

		
#	Parcours Temporaires et Futur

		self.C_TrackTemporaryNameSuffix 	= ' - Modifié temporairement'
		self.C_TrackFutureNameSuffix 		= ' - Version future'


# ========================================================================================
# QCarto - Affichage Table des Parcours
# ========================================================================================

#	Nom du champ (0) // Largeur en pixel (1) // Type de valeur (2) // Source (3) //  Clics (4) G=1 D=2

		self.C_tracksTableQView_ColName 	= 0
		self.C_tracksTableQView_ColSize 	= 1
		self.C_tracksTableQView_ColType 	= 2
		self.C_tracksTableQView_ColSource 	= 3
		self.C_tracksTableQView_ColClics 	= 4					# Bitwise : 1=leftclic 2=rightclic
		self.C_tracksTableQView_ColEdit 	= 5					# Bitwise : 1=changepossible
		

		self.tracksTableQView = 	[[self.tableTracksFieldCode,						110,		'Text',		'Table',   	2, 	1	],			
									 [self.tableTracksFieldName,						240,		'Text',		'Table',	0, 	1	],			
									 [self.tableTracksFieldStatus,	 					 50,		'Text',		'Table',	0, 	1	],			
									 [self.tableTracksFieldDate,	 					115,		'Text',		'Calcul',	3, 	0	],			
									 [self.tableTracksFieldDistance,					 50,		'Int',		'Calcul',	3, 	0	],			
									 [self.tableTracksFieldVO,							 50,		'Int',		'Calcul',	0, 	0	],			
									 [self.tableTracksFieldDenivelePos,					 35,		'Int',		'Calcul',	0, 	0	],			
									 [self.tableTracksFieldDeniveleNeg,					 35,		'Int',		'Calcul',	0, 	0	],			
									 [self.tableTracksFieldAltmin,						 40,		'Int',		'Calcul',	0, 	0	],			
									 [self.tableTracksFieldAltmax,						 40,		'Int',		'Calcul',	0, 	0	],			
									 [self.tableTracksFieldTroncons,					 50,		'List',		'Calcul',	3, 	0	],			
									 [self.tableTracksFieldReperes,						 50,		'List',		'Calcul',	3, 	0	],			
									 [self.tableTracksIFieldPOIs, 						 50,		'List',		'Résultat',	1, 	0	],			
									 [self.tableTracksIFieldCalcul,						 80,		'Text',		'Résultat',	3, 	0	],			
									 [self.tableTracksIFieldGaps,						 40,		'List',		'Résultat',	3, 	0	],			
									 [self.tableTracksQFieldDelta,						 40,		'Int',		'Résultat',	1, 	0	],			
									 [self.tableTracksQFieldModif,						 25,		'List',		'Résultat',	3, 	0	], 
									 [self.tableTracksFieldMarked,						120,		'Text',		'Table',	0, 	1	], 
									 [self.tableTracksIFieldDistanceEquivalenteDirecte,	 50,		'Int',		'Résultat',	0, 	0	],
									 [self.tableTracksIFieldDistanceEquivalenteInverse,	 50,		'Int',		'Résultat',	0, 	0	],
									 [self.tableTracksIFieldEchelleMaxPortrait,			 50,		'TextR',	'Résultat',	0, 	0	],
									 [self.tableTracksIFieldEchelleMaxPaysage,			 50,		'TextR',	'Résultat',	0, 	0	],
									 [self.tableTracksIFieldPOIsAll, 					 50,		'List',		'Résultat',	1, 	0	]]			
		
		
#	Taille carte pour calcul des echelles en mètres (taille minimum cas PDF et Topo avec marge 5mm)

		self.C_trackScaleMapSize = [0.125, 0.190]
		self.C_trackScaleMapList = [10, 15, 20, 25, 30, 35, 40, 50, 60, 80, 100, 200, 250, 400, 600, 800, 1000, 2000]
		
#	Table pour l'affichage des repères

		self.C_pointsTableQView_ColRepère = 5
		self.C_pointsTableQView_ColName   = 6
		
		self.pointsTableQView = 	[['id',					 60,		'Int'	],			
									 ['───//───',			 80,		'Text'	],
									 ['Distance',			 80,		'Int'	],			
									 ['Delta',			 	 80,		'Int'	],			
									 ['Schéma',			 	 80,		'TextR'	],			
									 ['Repères',			 50,		'Text'	],			
									 ['Nom du repère',		350,		'Text'	],			
									 ['Alt',				 60,		'Int'	],			
									 ['UTM',				180,		'Text'  ]]

#	Table pour l'affichage des POIs

		self.C_poisTableQViewFieldId =			'id'
		self.C_poisTableQViewFieldIdPoi =		'Id-Poi'
		self.C_poisTableQViewFieldTitre =		'Titre'
		self.C_poisTableQViewFieldZone =		'Zone'
		self.C_poisTableQViewFieldFlux =		'Flux'
		self.C_poisTableQViewFieldDelta =		'Delta'
		

		self.C_C_poisTableQViewFieldFluxValidated = 'Validée'

		self.poisTableQView = 		[[self.C_poisTableQViewFieldId,			150,	'Int'	],
									 [self.C_poisTableQViewFieldIdPoi,		60,		'Int'	],
									 [self.C_poisTableQViewFieldTitre,		300,	'Text'	],
									 [self.C_poisTableQViewFieldZone,		100,	'Text'	],
									 [self.C_poisTableQViewFieldFlux,	 	100,	'Text'	],
									 [self.C_poisTableQViewFieldDelta,		100,	'Int'	]]
	
		self.C_poisComboTextAuto =		'GPX POIs Auto'
		self.C_poisComboTextClose = 	'GPX POIs Proches'
		self.C_poisComboTextNone = 		'GPX sans POIs'
		self.C_poisComboTextNoPOIs =	'Pas accès POIs' 

		self.poisComboList = 		[self.C_poisComboTextAuto, self.C_poisComboTextClose, self.C_poisComboTextNone]
		
		self.C_poisDeltaMax 	= 200
		self.C_poisDeltaClose 	= 100
		
		
#	Table pour l'affichage de l'historique

		self.historicTableQView = 	[[self.tableTracksFieldId,					120,		'Int'	],			
									 [self.tableTracksFieldDate,				120,		'Text'	],			
									 [self.tableAllFieldNomCarto,				120,		'Text'	],			
									 [self.tableTracksFieldDistance,			 80,		'Int'	],			
									 [self.tableTracksFieldDelta,				 80,		'Int'	],			
									 [self.tableTracksFieldDenivelePos,			 80,		'Int'	],			
									 [self.tableTracksFieldDeniveleNeg,			 80,		'Int'	]]

#	Table pour l'affichage des Parcours communs

		self.commonTracksTableQView =  [[self.tableTracksFieldCode,			110,		'Text'	], 		
 									    [self.tableTracksFieldName,			240,		'Text'  ],		
										['Tronçons',						700,		'Text'	]]

#	Table pour l'affichage du détails des tronçons

		self.sectionsTableQView = 	[['id',					 50,		'Int'	],			\
									 ['Distance',			 60,		'Int'	],			\
									 ['Delta',			 	 60,		'Int'	],			\
									 ['GR',					 120,		'Text'	],			\
									 ['GRP',				 120,		'Text'	],			\
									 ['GRT',				 120,		'Text'	],			\
									 ['RI',				 	 100,		'Text'	],			\
									 ['RB',				 	 120,		'Text'	],			\
									 ['RF',				 	 120,		'Text'	],			\
									 ['RL',				 	 120,		'Text'	],			\
									 ['IR',				 	 100,		'Text'	]]

#	Table pour l'affichage des détails HTML

		self.htmlTracksTableQView = 	[[self.tableTracksFieldCode,						110		],
										[self.tableTracksFieldName,							350		],
										[self.tableTracksFieldStatus,	 					 50		],
										['NomGPX',						   		 	 	    300		],
										['Date Locale',										 80		],
										['Date Site',										 80		],
										['Date URL',										 80		]]

		self.C_htmlTracksTableQView_ColCode			= 0
		self.C_htmlTracksTableQView_ColName			= 1
		self.C_htmlTracksTableQView_ColNameGPX		= 3
		self.C_htmlTracksTableQView_ColDateLocal 	= 4
		self.C_htmlTracksTableQView_ColDateSite		= 5
		self.C_htmlTracksTableQView_ColDateUrl		= 6
		
#	Codes html

#		self.configSiteGPXHtmlHeaderLines 	= 	[ '<p>Traces GPX téléchargeables du <strong><span style="color: #d0121a;">%GR%</span></strong></p>' ]
#		self.configSiteGPXHtmlTrackLines 	=	[ '<p><span style="color: #2c9ffd;"><strong><a href="%URL%"><span style="color: #2c9ffd;">%NAME%</span></a></strong></span></p>' ]

		self.configSiteGPXHtmlUrl			=	  'https://grsentiers.be/GPX/'
		self.configSiteMAJHtmlUrl			=	  'https://grsentiers.be/MAJ/'

		self.configSiteGPXHtmlHeaderLines 	=	[ '<div class="container">' ,
												  '<div class="mega-col col-md-6">' ,
												  '<div class="row" style="margin-bottom: 25px;">' ,
												  '<div class="card-body">' ,
												  '<h3 class="card-title" style="text-align: center;">GPX</h3>' ,
												  '<div class="row card-text">' ,
												  '<p style="box-sizing: border-box; margin: 12px 0px; padding: 0px; border: 0px; font-style: inherit; font-variant: inherit; font-stretch: inherit; ' ,
												  '   line-height: inherit; font-family: inherit; font-optical-sizing: inherit; font-kerning: inherit; font-feature-settings: inherit; ' ,
												  '   font-variation-settings: inherit; font-size: 14px; vertical-align: top; background: transparent; outline: none; color: #847f7b; text-align: center;">' ,
												  '   Traces GPX du <span style="color: #d0121a;"><strong>%GR%</strong></span> téléchargeables</p>' ,
												  '<table style="margin: 0px auto; padding: 0px; border: 0px; font-style: inherit; font-variant: inherit; font-stretch: inherit; line-height: ' , 
												  '   inherit; font-family: inherit; font-optical-sizing: inherit; font-kerning: inherit; font-feature-settings: inherit; font-variation-settings: inherit; ' ,
												  '   font-size: 14px; vertical-align: top; border-collapse: collapse; border-spacing: 0px; background: transparent; outline: none; max-width: 100%;">' ,
												  '<tbody style="box-sizing: border-box; margin: 0px; padding: 0px; border: 0px; font-style: inherit; font-variant: inherit; font-stretch: inherit; ' ,
												  '   line-height: inherit; font-family: inherit; font-optical-sizing: inherit; font-kerning: inherit; font-feature-settings: inherit; font-variation-settings: inherit; ' ,
												  '   vertical-align: top; background: transparent; outline: none;">' ,
												  '<tr style="box-sizing: border-box; margin: 0px; padding: 0px; border: 0px; font-style: inherit; font-variant: inherit; font-stretch: inherit; line-height: inherit; ' ,
												  '   font-family: inherit; font-optical-sizing: inherit; font-kerning: inherit; font-feature-settings: inherit; font-variation-settings: inherit; vertical-align: top; background: transparent; outline: none;">' ,
												  '<td width="59%" style="box-sizing: border-box; margin: 0px; padding: 9px 10px; border: 0px; font-style: inherit; font-variant: inherit; font-stretch: inherit; ' ,
												  '  line-height: inherit; font-family: inherit; font-optical-sizing: inherit; font-kerning: inherit; font-feature-settings: inherit; font-variation-settings: inherit; ' ,
												  '  font-size: 14px; vertical-align: top; background: transparent; outline: none;"><strong>Nom du parcours</strong></td>' ,
												  '<td width="21%" style="box-sizing: border-box; margin: 0px; padding: 9px 10px; border: 0px; font-style: inherit; font-variant: inherit; font-stretch: inherit; ' , 
												  '  line-height: inherit; font-family: inherit; font-optical-sizing: inherit; font-kerning: inherit; font-feature-settings: inherit; font-variation-settings: inherit; ' ,
												  '  font-size: 14px; vertical-align: top; text-align: center; background: transparent; outline: none;"><strong>modifié le</strong></td>' ,
												  '<td width="18%" style="box-sizing: border-box; margin: 0px; padding: 9px 10px; border: 0px; font-style: inherit; font-variant: inherit; font-stretch: inherit; ' ,
												  '  line-height: inherit; font-family: inherit; font-optical-sizing: inherit; font-kerning: inherit; font-feature-settings: inherit; font-variation-settings: inherit; ' ,
												  '  font-size: 14px; vertical-align: top; text-align: right; background: transparent; outline: none;"><strong>longueur</strong></td>' ,
												  '<td width="2%" style="box-sizing: border-box; margin: 0px; padding: 9px 10px; border: 0px; font-style: inherit; font-variant: inherit; font-stretch: inherit; ' ,
												  '  line-height: inherit; font-family: inherit; font-optical-sizing: inherit; font-kerning: inherit; font-feature-settings: inherit; font-variation-settings: inherit; ' ,
												  '  font-size: 14px; vertical-align: top; background: transparent; outline: none;"><strong></strong></td>' ,
												  '</tr>' ]												  

		self.configSiteGPXHtmlTrackLines	=	[ '<tr style="box-sizing: border-box; margin: 0px; padding: 0px; border: 0px; font-style: inherit; font-variant: inherit; font-stretch: inherit; line-height: inherit; font-family: inherit; font-optical-sizing: inherit; font-kerning: inherit; font-feature-settings: inherit; font-variation-settings: inherit; vertical-align: top; background: transparent; outline: none;">' ,
												  '  <td style="box-sizing: border-box; margin: 0px; padding: 9px 10px; border: 0px; font-style: inherit; font-variant: inherit; font-stretch: inherit; line-height: inherit; font-family: inherit; font-optical-sizing: inherit; font-kerning: inherit; font-feature-settings: inherit; font-variation-settings: inherit; font-size: 14px; vertical-align: top; background: transparent; outline: none;"><span style="color: #2c9ffd;"><strong><a href=%URL% style="box-sizing: border-box; margin: 0px; padding: 0px; border: 0px; font-style: inherit; font-variant: inherit; font-weight: normal; font-stretch: inherit; line-height: inherit; font-family: inherit; font-optical-sizing: inherit; font-kerning: inherit; font-feature-settings: inherit; font-variation-settings: inherit; vertical-align: baseline; background: transparent; outline: none; color: #1f191b; text-decoration-line: none;"><span style="color: #2c9ffd;">%NAME%</span></a></strong></span></td>' ,
												  '  <td style="box-sizing: border-box; margin: 0px; padding: 9px 10px; border: 0px; font-style: inherit; font-variant: inherit; font-stretch: inherit; line-height: inherit; font-family: inherit; font-optical-sizing: inherit; font-kerning: inherit; font-feature-settings: inherit; font-variation-settings: inherit; font-size: 14px; vertical-align: top; text-align: center; background: transparent; outline: none;">%DATE%</td>' ,
												  '  <td style="box-sizing: border-box; margin: 0px; padding: 9px 10px; border: 0px; font-style: inherit; font-variant: inherit; font-stretch: inherit; line-height: inherit; font-family: inherit; font-optical-sizing: inherit; font-kerning: inherit; font-feature-settings: inherit; font-variation-settings: inherit; font-size: 14px; vertical-align: top; text-align: right; background: transparent; outline: none;">%DIST%</td>' ,
												  '  <td style="box-sizing: border-box; margin: 0px; padding: 9px 10px; border: 0px; font-style: inherit; font-variant: inherit; font-stretch: inherit; line-height: inherit; font-family: inherit; font-optical-sizing: inherit; font-kerning: inherit; font-feature-settings: inherit; font-variation-settings: inherit; font-size: 14px; vertical-align: top; background: transparent; outline: none;"></td>' ,
												  '</tr>' ]

		self.configSiteGPXHtmlFooterLines	= 	[ '</tbody>' ,
												  '</table>' ,
												  '</div>' ,
												  '</div>' ,
												  '</div>' ,
												  '</div>'  ]

		self.configSiteMAJHtmlLines 		= 	[ '<div class="mega-col col-md-1"></div>' ,
												  '<div class="mega-col col-md-5">' ,
												  '<div class="row" style="margin-bottom: 25px;">' ,
												  '<div><center>' ,
												  '<h3>Mises à jour</h3>' ,
												  '<p><span style="color: #d0121a;">Modifications globales de la<span style="color: #8f28fe;"> dernière édition</span> du %GR%.</span></p>' ,
												  '<ul style="list-style-type: circle; list-style: inside;">' ,
												  '<li style="box-sizing: border-box; border: 0px; font-variant-numeric: inherit; font-variant-east-asian: inherit; font-variant-alternates: inherit; font-stretch: inherit; line-height: inherit; font-family: PTSansRegular, Georgia, Palatino, "Times New Roman", sans-serif; font-optical-sizing: inherit; font-kerning: inherit; font-feature-settings: inherit; font-variation-settings: inherit; font-size: 14px; vertical-align: top; outline: none; color: #847f7b;"><span style="color: #4a4a4a;">Mise à jour le %DATEL%.</span><span style="color: #4a4a4a;"> </span></li>' ,
												  '<li style="box-sizing: border-box; border: 0px; font-variant-numeric: inherit; font-variant-east-asian: inherit; font-variant-alternates: inherit; font-stretch: inherit; line-height: inherit; font-family: PTSansRegular, Georgia, Palatino, "Times New Roman", sans-serif; font-optical-sizing: inherit; font-kerning: inherit; font-feature-settings: inherit; font-variation-settings: inherit; font-size: 14px; vertical-align: top; outline: none; color: #847f7b;"><span style="color: #4a4a4a;">Pour visualiser et imprimer ces modifications cliquez </span><span style="text-decoration-line: underline;"><strong><a href=%URL% target="_blank" style="box-sizing: border-box; margin: 0px; padding: 0px; border: 0px; font-style: inherit; font-variant: inherit; font-weight: normal; font-stretch: inherit; line-height: inherit; font-family: inherit; font-optical-sizing: inherit; font-kerning: inherit; font-feature-settings: inherit; font-variation-settings: inherit; vertical-align: baseline; background: transparent; outline: none; color: #2c9ffd; text-decoration-line: none;" rel="noopener">ICI</a></strong></span></li>' ,
												  '</ul>' ,
												  '</center></div>' ,
												  '</div>' ,
												  '</div>' ,
												  '</div>' ,
												  '<div class="row" style="margin-bottom: 25px;">' ,
												  '<div class="mega-col col-md-3"></div>' ,
												  '<div class="mega-col col-md-6"><center>' ,
												  '%NOTE%' ,
												  '<center></div>' ,
												  '<div class="mega-col col-md-3"></div>' ,
												  '</div>'  ]


# 	Répertoire pour l'Export des GPX

		self.configPathExportGPX = self.configLocalProjectPath + '%PROJECT%/Traces GPX/'
		self.configPathExportGPXSityTrail = self.configLocalProjectPath + '%PROJECT%/Traces GPX - SityTrail/'
		self.configPathExportGPXMarkers = self.configLocalProjectPath + '%PROJECT%/Traces GPX - Bornes/'
		self.configPathExportOZI = self.configLocalProjectPath + '%PROJECT%/Traces Oziexplorer/'
		
		
# ========================================================================================
# ========================================================================================
#
# QCarto - Définition et Affichage Table des Emprises Cartes
# 
# ========================================================================================
# ========================================================================================
									 
#	Tables Emprises

		self.configPathFrame = self.configLocalPath + 'Qgis_Shapes/Descriptifs/'								# Répertoire du shape de référence
		self.configShapeFrameName = 'Emprises'																			# Nom du fichier shape de référence

		self.tableFramesFieldItineraryCode		= 'Itineraire'
		self.tableFramesFieldName				= 'Nom'
		self.tableFramesFieldFormat				= 'Format'
		self.tableFramesFieldEchelle			= 'Echelle'
		self.tableFramesFieldFolder				= 'Folder'
		self.tableFramesFieldNumber				= 'Numéro'
		self.tableFramesFieldCopyright			= 'Copyright'
		self.tableFramesFieldBackground			= 'Fond Topo'
		self.tableFramesFieldModifications		= 'Modifs'

		self.tableFramesQFieldNote				= 'Remarque'

#	Nom du champ (0) // Largeur en pixel (1) // Type de valeur (2) // Source (3) //  Clics (4) G=1 D=2

		self.C_framesTableQView_ColName 	= 0
		self.C_framesTableQView_ColSize 	= 1

		self.mapsTableQView =	 	[[self.tableFramesFieldItineraryCode,			 80		],			\
									 [self.tableFramesFieldName,					200		],			\
									 [self.tableFramesFieldFormat,	 				100		],			\
									 [self.tableFramesFieldEchelle,	 				 60		],			\
									 [self.tableFramesFieldFolder,	 				420		],			\
									 [self.tableFramesQFieldNote,					280		]]

# 	Cadrage des Cartes

		self.C_dicoPaperFormats_ColMargin = 2
		self.C_dicoPaperFormats_ColTopoFormat = 3

		self.dicoPaperFormats = { 
			'PDF-Paysage' : 				[ 200,	138,	0, 	'Topo-Paysage'	], 
			'PDF-Portrait' :				[ 138,	200,	0, 	'Topo-Portrait'	],  
			'IR-Paysage' : 					[ 240,	168,	7, 	None			], 
			'IR-Portrait' :					[ 168,	240, 	7,	None			],  
			'Topo-Paysage' : 				[ 210, 	135,	5, 	None			],	
			'Topo-Portrait' : 				[ 135,	210,	5, 	None			],
			'Topo-Globale-Paysage' :		[ 243,	210,	3,	None			],
			'Topo-Globale-Portrait' :		[ 210,	243,	3,	None			],
			'Topo-Réseau-Paysage' :			[ 205,	130,	0,	None			],
			'A4-Paysage' : 					[ 297,  210,    0,  None			],
			'A3-Paysage' : 					[ 420,  297,    0,  None			],
			'A2-Paysage' : 					[ 594,  420,    0,  None			],
			'A1-Paysage' : 					[ 841,  594,    0,  None			],
			'Libre-Petite' : 				[ 100,  100,    0,  None			],
			'Libre-Moyenne' : 				[ 250,  250,    0,  None			],
			'Libre-Grande' : 				[ 1000, 1000,   0,  None			]
			}

		self.configMapScales = [50000, 40000, 35000, 25000, 20000, 15000, 10000, 100000, 250000, 300000, 400000, 500000, 600000, 800000, 1000000, 1250000, 5000, 7500, 75000]

		self.configCreateMapMaxScale = 100000	 							# Condition pour créer une carte

#	Table pour l'affichage des cartes exportées

		self.tableMapsExportedFieldFile		= 'Fichier'

		self.mapsExportedTableQView = 	[['Préfixe',			 50,		'Text'	],			\
										 ['Itinéraire',		 	100,		'Text'	],			\
										 ['Nom',				150,		'Text'	],			\
										 ['Mode',				 80,		'Text'	],			\
										 ['Fichier',			750,		'Text'	]]
		
		
#	Tailles maximum pour les cartes géantes

		self.mapsExportMaxSize = [841, 594]
		
		
# ========================================================================================
# ========================================================================================
#
# QCarto - Définition et Affichage du Menu d'édition 50 K
#
# ========================================================================================
# ========================================================================================
		
# 	Noms des Attributs
		
		self.tableSections50KFieldId = 'id'
		self.tableSections50KFieldDate = 'date'
		self.tableSections50KFieldHash = 'hash'
		self.tableSections50KFieldPoints = 'pts'
		self.tableSections50KFieldist = 'dist_mm'
		self.tableSections50KFieldPAX = 'pa_x'
		self.tableSections50KFieldPAY = 'pa_y'
		self.tableSections50KFieldPZX = 'pz_x'
		self.tableSections50KFieldPZY = 'pz_y'
		self.tableSections50KFieldValidation = 'validation'
		
# 	Paramètres pour la fenêtre d'édition IGN 50

		self.configDiff50KMaxLevel1  = [ 1000,  0,  1]									# Differences max for level 1 on dist, pts, c_x et c_y)
		self.configDiff50KMaxLevel2  = [10000,  2,  5]									# Differences max for level 2 on dist, pts, c_x et c_y)
		self.configDiff50KMaxLevel3  = [50000, 10, 25]									# Differences max for level 3 on dist, pts, c_x et c_y)

		self.C_Table_Edit50K_Index_Id = 0
		self.C_Table_Edit50K_Index_Date = 1
		self.C_Table_Edit50K_Index_Carto = 2
		self.C_Table_Edit50K_Index_GeometryColor = 3
		self.C_Table_Edit50K_Index_GeometryInfo = 4
		self.C_Table_Edit50K_Index_AttributesColor = 5
		self.C_Table_Edit50K_Index_AttributesInfo = 6
		self.C_Table_Edit50K_Index_AttributesDelta = 7
				
		self.configTableEdit50KFields = [['Id',						40	],
										 ['Date',					100	],
										 ['Carto',					55  ],
										 ['',						15	],
										 ['Géo CW',					70	],
										 ['',						15	],
										 ['Attributs',				70	],
										 ['Δ m',					40	]]
		
		self.configSections50KFieldsCopyList = [self.tableSectionsFieldGRList, self.tableSectionsFieldGRTList, self.tableSectionsFieldRLList, self.tableSectionsFieldRBList, self.tableSectionsFieldRFList, self.tableSectionsFieldIRList]
		
		self.configSections50KGlobalMax = 100																# Count of feature displayed in global mode

		self.config50KDeltaMaxNormal = 50																	# Delta Hausdorff max sinon afficher jaune
		self.config50KDeltaMaxWarning = 100																	# Delta Hausdorff max sinon afficher rouge
		self.config50KDeltaMaxDelete = 400																	# Delta Hausdorff max au nettoyage
		
		self.configSections50KMaxScale = 2000																# Max scale for auto zoom
	
		self.tablesSectionsGREd4VariableHighlight 	= 'QSectionsIdEd4'										# Variable pour highlight Tronçons lors édition Topo-50
		
		
# ========================================================================================
# ========================================================================================
#
# Action Buttons
#
# ========================================================================================
# ========================================================================================

		self.configQCartoBarName = 'QCartoBar'
		self.configPluginBarName = 'mPluginToolBar'

		self.configActionIcon_QW = self.configLocalPath + 'Qgis_Icons/Action-QW.png'
		self.configActionIcon_25K = self.configLocalPath + 'Qgis_Icons/Action-25K.png'
		self.configActionIcon_50K = self.configLocalPath + 'Qgis_Icons/Action-50K.png'
		self.configActionIcon_100K = self.configLocalPath + 'Qgis_Icons/Action-100K.png'
		self.configActionIcon_MapL = self.configLocalPath + 'Qgis_Icons/Action-MapL.png'
		self.configActionIcon_MapP = self.configLocalPath + 'Qgis_Icons/Action-MapP.png'
		self.configActionIcon_Map = self.configLocalPath + 'Qgis_Icons/Action-Map.png'
		self.configActionIcon_MapV = self.configLocalPath + 'Qgis_Icons/Action-MapVirgin.png'
		self.configActionIcon_GrT = self.configLocalPath + 'Qgis_Icons/Action-GRToggle.png'
		self.configActionIcon_EtiA = self.configLocalPath + 'Qgis_Icons/Action-EtiA.png'
		self.configActionIcon_GrI = self.configLocalPath + 'Qgis_Icons/Action-GRInfos.png'
		self.configActionIcon_GrE = self.configLocalPath + 'Qgis_Icons/Action-GREdit.png'

		self.configActionName_QW 	= 'QActionQW'
		self.configActionName_25K 	= 'QAction25K'
		self.configActionName_50K 	= 'QAction50K'
		self.configActionName_100K 	= 'QAction100K'
		self.configActionName_MapL 	= 'QActionMapL'
		self.configActionName_MapP 	= 'QActionMapP'
		self.configActionName_Map 	= 'QActionMap'
		self.configActionName_MapV 	= 'QActionMapV'
		self.configActionName_GrT	= 'QActionGrT'
		self.configActionName_EtiA	= 'QActionEtiA'
		self.configActionName_GrI 	= 'QActionGrI'
		self.configActionName_GrE 	= 'QActionGrE'

		self.configActionDistance_GrI = 20
		self.configActionDistance_PrI = 160

		self.configActionDistance_GrE = 20

		self.configActionButtonsList = ['QW', '25K', '50K', '100K', 'Map', 'MapV', 'GrT', 'EtiA', 'GrI', 'GrE']
		
		
# ========================================================================================
# ========================================================================================
#
# Menus d'identification 
#
# ========================================================================================
# ========================================================================================

		self.configTableIdViewFields = 		[['Code',						120	],
											['D',							 30 ],
											['Type',						125 ],
											['Nom',							300	],
											['Etat',						100	],
											['Dist',						 70 ],
											['Seg',							 40	]]						# Attention : ordre des champs hardcodé dans SGRCarto_MenuViewIdentification
	
		self.configTablePointViewFields = 	[['Id',							 40	],
											['Code',						100 ],
											['Type',						120 ],
											['Repère',						 40 ],
											['Nom',							250	]]						# Attention : ordre des champs hardcodé dans SGRCarto_MenuViewPointIdentification

		
# ========================================================================================
# ========================================================================================
#
# QCarto - Carte Active 
#
# ========================================================================================
# ========================================================================================

		self.configPathActiveMap = self.configLocalPath + 'Qgis_Shapes/Carte Active/'

#	Variables pour définir la carte active 

		self.tableMapsActiveMapVariableHighlight 	= 'QMapActive'						# Nom de la carte active
		self.tableMapsActiveMapVariableScale 		= 'QMapScale'						# Echelle de la carte active (texte)
		self.tableMapsActiveMapVariableType			= 'QMapType'						# Type de carte : "PDF" // "Topo" pour copyright
		self.tableMapsActiveMapVariableEditMode 	= 'QMapEditMode'					# Mode édition : "Edition" // "Export"
		self.tableActiveMapNumberVariableName		= 'QMapName'						# Nom Carte pour style Numéro Carte



# ========================================================================================
# QCarto - Carte Active - Position des Décorations - en mm
# ========================================================================================

		self.configShapeMapDecorationNumber = 'Numéro'	
		self.configShapeMapDecorationCopyright = 'Copyright'	
		self.configShapeMapDecorationWhiteFrame = 'Cadre Blanc'	

		self.mapDecorationNameMargin = 5
		self.mapDecorationNameWidth = 12									 			# Largeur de base pour 10 caratères max
		self.mapDecorationNameWidthExtra = 1.2											# Largeur par caractère à partir de 10
		self.mapDecorationNameHeight = 4
		
		self.mapDecorationCopyrightMargin = 5
		self.mapDecorationCopyrightWidth = 40
		self.mapDecorationCopyrightHeight = 15
			
		self.tableDecorationFieldType = 'type'
		self.tableDecorationFieldScale = 'echelle'
		self.tableDecorationFieldText = 'texte'
	
	
# ========================================================================================
# QCarto - Carte Active - Repères
# ========================================================================================

		self.configShapeMapReperes = 'Points Repères'	

		self.tableMapPointsFieldId = 'id'
		self.tableMapPointsFieldRepere = 'Repère'
		self.tableMapPointsFieldIdXRepere = 'X_Repère'
		self.tableMapPointsFieldIdYRepere = 'Y_Repère'
		self.tableMapPointsFieldTexte = 'Texte'
		self.tableMapPointsFieldCouleur = 'Couleur'
		
		self.tableMapPointsDistanceBouleX = 500																# Where boule is created originally
		self.tableMapPointsDistanceBouleY = 250																# Where boule is created originally


# ========================================================================================
# QCarto - Carte Active - Points Intérêt RF
# ========================================================================================

		self.configShapeMapPoiRF = 'Points Intéret RF'	

		self.tableMapPoiRFFieldId = 'id'
		self.tableMapPoiRFFieldPoint = 'Point'
		
		self.tableMapPoisDistanceBouleX = 300																# Where Poi is created originally
		self.tableMapPoisDistanceBouleY = 150																# Where Poi is created originally


# ========================================================================================
# QCarto - Carte Active - Etiquettes
# ========================================================================================

		self.configShapeMapLabels = 'Etiquettes Parcours'	
		
		self.tableMapLabelsFieldLabel = 'Label'
		self.tableMapLabelsFieldCouleur = 'Couleur'
		

		self.configShapeMapLabelsSimple = 'Etiquettes Simples'

		self.tableMapLabelsSimpleFieldType 		= 'Type'
		self.tableMapLabelsSimpleFieldText 		= 'Texte'
		self.tableMapLabelsSimpleFieldTextDuo 	= 'Texte Duo'


# ========================================================================================
# QCarto - Carte Active - Tronçons
# ========================================================================================

		self.configShapeMapSections = 'Tronçons'	
		
		self.tableMapSectionsFieldType 		= 'Type'
		self.tableMapSectionsFieldState 	= 'Etat'
		self.tableMapSectionsFieldSymbol	= 'Symbole'
		self.tableMapSectionsFieldSections	= 'Sections'
		
		self.sectionsGetFeaturesExtraSize = 	800					

		self.activeMapLinesMergeDistanceMax = 20
		self.activeMapLinesDensificationDistance = 5														# Geometry densification before shortening en mètres
		self.activeMapLinesShortenDistance = 1																# Geometry shorten distance at both extremities en mm


# ========================================================================================
# QCarto - Carte Active - Fond Carte pour export
# ========================================================================================

		self.exportBackgroundNone 		= 'Fond Blanc'
		self.exportBackgroundOsm		= 'Fond Osm'
		self.exportBackgroundIGN50Ed3 	= 'IGN-50 Ed3'
		self.exportBackgroundIGN50Ed4 	= 'IGN-50 Ed4'
		self.exportBackgroundCanevas 	= 'Canevas'
		

#		self.exportActiveMapComboList = [self.exportBackgroundNone, self.exportBackgroundOsm, self.exportBackgroundIGN50Ed3, self.exportBackgroundIGN50Ed4] 
		self.exportActiveMapCopyrightDico = { self.exportBackgroundNone 		: 'None',
											  self.exportBackgroundOsm 			: 'OSM' ,
											  self.exportBackgroundIGN50Ed3		: 'IGN' ,
											  self.exportBackgroundIGN50Ed4		: 'IGN' ,
											  self.exportBackgroundCanevas		: 'IGN'
											}


# ========================================================================================
# ========================================================================================
#
# QCarto - Projet Actif
#
# ========================================================================================
# ========================================================================================

		self.configPathProjectFramesGeneric = self.configLocalProjectPath + '%PROJECT%/Emprises Cartes/'
		self.configPathProjectShapesGeneric = self.configLocalProjectPath + '%PROJECT%/Shapes Projet/'

		self.configPathActiveProject = self.configLocalPath + 'Qgis_Shapes/Projet Actif/'

		self.configShapeProjectNameTEC = 'Arrêts TEC'	
		self.configShapeProjectNameSNCB = 'Gares SNCB'


# ========================================================================================
# ========================================================================================
#
# QCarto - Export Carte Active 
#
# ========================================================================================
# ========================================================================================

# ========================================================================================
# Export des Cartes     (Must be defined before : Réseau GR - Définition des Couches à Générer)
# ========================================================================================
		
		self.configExportTextAuto 			= 'Automatique'
		self.configExportTextTopo50Ed3 		= 'IGN-50 Ed3'
		self.configExportTextTopo50Ed4 		= 'IGN-50 Ed4'
		self.configExportTextTopo400 		= 'IGN-400'
		self.configExportTextTopo250 		= 'IGN-250'
		self.configExportTextOsm 			= 'Fond Osm'
		self.configExportTextWhite 			= 'Fond Blanc'
		self.configExportTextCanevas 		= 'Canevas'
		self.configExportTextOsmLayers		= 'Couches Osm'
		
		self.configDicoExportBackground =  \
			{ self.configExportTextAuto : 			[	381,	85	],
			  self.configExportTextTopo50Ed4 :  	[ 	381,	85	],
			  self.configExportTextTopo50Ed3 :		[ 	381,	85	],
			  self.configExportTextTopo400 : 		[	381,	85  ],
			  self.configExportTextTopo250 : 		[	381,	85	],
			  self.configExportTextOsm : 			[	600,	70	],
			  self.configExportTextWhite :			[	400,   100	],
			  self.configExportTextCanevas : 		[	600,   100	] }
			
# Densités d'export
		self.configExportDpiList = [200, 254, 381, 400, 600, 800, 1000, 1200]
		self.configExportDpiOsm = 600													# Utilisé lors de l'export du fond Osm
		
# Opacités d'export
		self.configExportOpacityList = [100, 95, 90, 85, 80, 75, 70, 60, 50, 25]

# Autres Paramètres d'export
		self.configExportBgdColor = QColor(244, 244, 244)
		self.configExportWaitMax = 120

# Répertoire pour l'Export des Images Cartes et Schémas 
		self.configPathExportImages = self.configLocalProjectPath + '%PROJECT%/Cartes Images/'
		self.configFileExportImages = '%PREFIX% - %ITI% - %MAP% - %MODE% - %BACK% (%TIME%)%TILE%.png'
		self.configPathExportPlans  = self.configLocalProjectPath + '%PROJECT%/Schémas/'
		self.configPathExportPlansImages  = self.configLocalProjectPath + '%PROJECT%/Schémas - Images Cartes/'
		self.configFileExportPlans  = '%PREFIX% - %ITI% - %MAP% - %MODE% (%TIME%).png'
		self.configPathExportPlansValues  = self.configLocalProjectPath + '%PROJECT%/Schémas - Distances/'
		self.configFileExportPlansValues  = '%PREFIX% - %ITI% - %NAME% (%TIME%).csv'
		self.configFileExportGRItineraryValues  = '%PREFIX% - %ITI% - Itinéraire (%TIME%).csv'
		self.configFileExportGRTrackValues  = '%PREFIX% - %TRACK% - Parcours (%TIME%).csv'
		self.configPathExportProfils  = self.configLocalProjectPath + '%PROJECT%/Profils Altimétriques/'		


# ========================================================================================
# ========================================================================================
#
# QCarto - Livraisons
#
# ========================================================================================
# ========================================================================================

		self.pathMyDrive	= self.configMyDrivePath	
		self.pathDriveTopo  = self.configMyDrivePath

		self.pathDeliveriesCarto = self.pathDriveCarto + 'Publications Carto/'
		self.pathDeliveriesCartoMaps = self.pathDeliveriesCarto + '%PROJECT%/Cartes/'
		self.pathDeliveriesCartoPlans = self.pathDeliveriesCarto + '%PROJECT%/Schémas/'
		self.pathDeliveriesCartoDistances = self.pathDeliveriesCarto + '%PROJECT%/Schémas - Distances/'
		self.pathDeliveriesCartoProfils = self.pathDeliveriesCarto + '%PROJECT%/Profils Altimétriques/'
		self.pathDeliveriesCartoGPX = self.pathDeliveriesCarto + '%PROJECT%/Traces GPX/'
		self.pathDeliveriesCartoGPXSityTrail = self.pathDeliveriesCarto + '%PROJECT%/Traces GPX - SityTrail/'

		self.pathDeliveriesCartoLogfile = self.pathDriveCarto + 'Publications Carto/Log/Livraisons - Log Carto global.csv'
		self.pathDeliveriesTopoLogfile = self.pathDriveCarto + 'Publications Carto/Log/Livraisons - Log Topo global.csv'

		self.pathDeliveriesCoordinationOSM = self.pathDriveCarto + 'Coordination SGR-OSM/Traces GPX/'
		self.pathDeliveriesCoordinationOSMCSV = self.pathDriveCarto + 'Coordination SGR-OSM/Rapports CSV/'
		self.pathDeliveriesCoordinationOSMLogfile = self.pathDriveCarto + 'Coordination SGR-OSM/Log/Livraisons - Log global.txt'
		
		self.pathDeliveriesTopoMapsRB = self.pathMyDrive + '.shortcut-targets-by-id/13JYEuKtccv3Xzv-3w4fTZxv_D7Lb0fqx/PRODUCTION RB à l\'unité/%TOPO%/%RB%/'
		self.pathDeliveriesTopoMapsIR = self.pathMyDrive + '.shortcut-targets-by-id/13JYEuKtccv3Xzv-3w4fTZxv_D7Lb0fqx/PRODUCTION RB à l\'unité/IR - Idées Rando/%IR%/'
		self.pathDeliveriesTopoMapsRI = self.pathMyDrive + '.shortcut-targets-by-id/13JYEuKtccv3Xzv-3w4fTZxv_D7Lb0fqx/PRODUCTION RB à l\'unité/RI - Randos en Itinérance/%RI%/'
		self.pathDeliveriesTopoMapsGR = self.pathMyDrive + '.shortcut-targets-by-id/1ZDCJoy0WdHIeD1bEMRjcO0p2a-qDeENB/PRODUCTION GR GRP GRT/%TOPO%/'
		self.pathDeliveriesSiteGR 	  = self.pathMyDrive + '.shortcut-targets-by-id/1rX4tx2e_J_sCIY0E2MBCQws1mBL756eC/GR GRP GRT (Boîte aux lettres Publications)/'
		self.pathDeliveriesSiteRB 	  = self.pathMyDrive + '.shortcut-targets-by-id/1t3Re7CgY72XNVikcqe1kOdZA5-2T8ilW/RB RF RL IR (Boîte aux lettres Publications)/'
		self.pathDeliveriesSityTrail  = self.pathMyDrive + '.shortcut-targets-by-id/1JzyJH3J9T6i4gnFw6JqYSaM8ilNpHxGz/SityTrail (Boîte aux lettres Publications)/'

		self.tableProductsFieldItineraryCode		= 'Itinéraire'
		self.tableProductsFieldFileName				= 'Fichier'
		self.tableProductsFieldDateLocal			= 'Date Génération (X:)'
		self.tableProductsFieldCopyCarto			= 'Copie X: > Y:' 
		self.tableProductsFieldDateCarto			= 'Date Partage SGR (Y:)'
		self.tableProductsFieldCopyTopo				= 'Copie Y: > Z:' 
		self.tableProductsFieldDateTopo				= 'Date Topo SGR (Z:)'
		self.tableProductsFieldOpenTopo				= 'Répertoire'

		self.tableProductsFieldTrackCode			= 'Code'
		self.tableProductsFieldTrackName			= 'Nom'
		self.tableProductsFieldTrackOsmid			= 'OsmId'
		self.tableProductsFieldTrackDateDB			= 'Date DB'
		self.tableProductsFieldTrackDateY			= 'Date Y'
		self.tableProductsFieldTrackDeltaY			= 'Delta Y'
		self.tableProductsFieldCopyOsm				= 'Y: > Coord' 
		self.tableProductsFieldTrackDateOsm			= 'Date Coord'
		self.tableProductsFieldTrackDeltaOsm		= 'Delta Coord'
		self.tableProductsFieldTrackDateKpn			= 'Date KPN'
		self.tableProductsFieldTrackDateOsmRel		= 'Date Osm'
		self.tableProductsFieldTrackDeltaOsmRel		= 'Delta Osm'
		
#	Nom du champ (0) // Largeur en pixel (1) 

		self.C_productsTableQView_ColName 	= 0
		self.C_productsTableQView_ColSize 	= 1
		self.C_productsTableQView_Type	 	= 2
		self.C_productsTableQView_Position 	= 3

		self.productsTableQView =	 	[[self.tableProductsFieldItineraryCode,				100, 	'Text', 		'Left' 		],			
										[self.tableProductsFieldFileName,					300, 	'Text',			'Left'		],			
										[self.tableProductsFieldDateLocal,	 				140, 	'Text',			'Center'	],			
										[self.tableProductsFieldCopyCarto,	 				100, 	'Checkbox',		'Center'	],	
										[self.tableProductsFieldDateCarto,	 				140, 	'Text',			'Center'	],
										[self.tableProductsFieldCopyTopo,	 				100, 	'Checkbox',		'Center'	],		
										[self.tableProductsFieldDateTopo,	 				140, 	'Text',			'Center'	],
										[self.tableProductsFieldOpenTopo,	 				100, 	'Text',			'Center'	]]

		self.productsTableQViewOSM =	[[self.tableProductsFieldTrackCode,					 90, 	'Text', 		'Left' 		],	
										 [self.tableProductsFieldTrackName, 				280, 	'Text',			'Left'		],
										 [self.tableProductsFieldTrackOsmid, 				 60, 	'Text',			'Center'	],
										 [self.tableProductsFieldTrackDateDB, 				120, 	'Text',			'Center'	],
										 [self.tableProductsFieldTrackDateY, 				125, 	'Text',			'Center'	],
										 [self.tableProductsFieldTrackDeltaY, 				 60, 	'Dist',			'Right'		],
										 [self.tableProductsFieldCopyOsm,	 				 90, 	'Checkbox',		'Center'	],		
										 [self.tableProductsFieldTrackDateOsm, 				120, 	'Text',			'Center'	],
										 [self.tableProductsFieldTrackDeltaOsm, 			 60, 	'Dist',			'Right'		],
										 [self.tableProductsFieldTrackDateKpn, 				120, 	'Text',			'Center'	],
										 [self.tableProductsFieldTrackDateOsmRel, 			120, 	'Text',			'Center'	],
										 [self.tableProductsFieldTrackDeltaOsmRel,			 60,	'Dist',			'Right'		]]
										 
		self.productsTableQViewGPX =	[self.tableProductsFieldItineraryCode,
										 self.tableProductsFieldFileName,
										 self.tableProductsFieldDateLocal,
										 self.tableProductsFieldCopyCarto,
										 self.tableProductsFieldDateCarto,
										 self.tableProductsFieldCopyTopo,
										 'Date Livraison Site',
										 self.tableProductsFieldOpenTopo]

#	For GPX retro-compatibility

		self.pathCompatibilityGPXForGR = 'Y:/Publications Carto/GPX SGR à jour/GR/'
		self.pathCompatibilityGPXForRB = 'Y:/Publications Carto/GPX SGR à jour/%TYPE%/%ITI%/'
		
#	Livraisons GPS - Utilisateurs autorisés

		self.authorizedUserListDeliveryOsm = ['Michel Dawirs']
		
		
# ========================================================================================
# ========================================================================================
#
# QCarto - Publications
#
# ========================================================================================
# ========================================================================================

#	Disctionnaire des Zones

		self.dicoZonesNamesRB = 	{ 	'Br' : 'Bruxelles' ,
										'BB' : 'Bruxelles et Brabant' ,
										'Bw' : 'Brabant Wallon' ,
										'Ha' : 'Hainaut' ,
										'Lg' : 'Liège' ,
										'Lu' : 'Luxembourg' ,
										'Na' : 'Namur' ,
										'PN' : 'Parcs Naturels'
									}	

#	Table des Parcours

		self.pathDeliveryTracksTableCsv = self.pathDeliveriesCarto + 'Table des Parcours/'
		self.fileDeliveryTracksTableCsv = 'Table des Parcours'

#	Statistiques

		self.pathDeliveryStatsCsv = self.pathDeliveriesCarto + 'SGR - Statistiques Réseau/'
		self.fileDeliveryStatsCsv = 'Statistiques Réseau'


# ========================================================================================
# ========================================================================================
#
# QCarto - Routage
#
# ========================================================================================
# ========================================================================================


# ========================================================================================
# QCarto - Affichage Table du Parcours
# ========================================================================================

#	Nom du champ (0) // Largeur en pixel (1) // Type de valeur (2) // Source (3) //  Clics (4) G=1 D=2

		self.C_routingTableQView_ColName 	= 0
		self.C_routingTableQView_ColSize 	= 1
		self.C_routingTableQView_ColType 	= 2
		self.C_routingTableQView_ColSource 	= 3
		self.C_routingTableQView_ColClics 	= 4					# Bitwise : 1=leftclic 2=rightclic
		self.C_routingTableQView_ColEdit 	= 5					# Bitwise : 1=changepossible
		
		self.routingTableFieldPointNum 				= 'Point'
		self.routingTableFieldPointX 				= 'X'
		self.routingTableFieldPointY 				= 'Y'
		self.routingTableFieldPointItinerary 		= 'GR / RB'
		self.routingTableFieldPointMark		 		= 'Repère'



		self.routingTableQView = 	[[self.routingTableFieldPointNum,						 50,		'Int',		'Table',   	0, 	0	],			
									 [self.routingTableFieldPointX,							 50,		'Int',		'Table',	0, 	0	],			
									 [self.routingTableFieldPointY,							 50,		'Int',		'Table',	0, 	0	],			
									 [self.routingTableFieldPointItinerary,					 80,		'Text',		'Table',	0, 	0	],			
									 [self.routingTableFieldPointMark,						200,		'Text',		'Table',	0, 	0	]]		
#									 [self.tableTracksFieldStatus,	 					 50,		'Text',		'Table',	0, 	1	],			
#									 [self.tableTracksFieldDate,	 					115,		'Text',		'Calcul',	3, 	0	],			
#									 [self.tableTracksFieldDistance,					 50,		'Int',		'Calcul',	3, 	0	],			
#									 [self.tableTracksFieldVO,							 50,		'Int',		'Calcul',	0, 	0	],			
#									 [self.tableTracksFieldDenivelePos,					 35,		'Int',		'Calcul',	0, 	0	],			
#									 [self.tableTracksFieldDeniveleNeg,					 35,		'Int',		'Calcul',	0, 	0	],			
#									 [self.tableTracksFieldAltmin,						 40,		'Int',		'Calcul',	0, 	0	],			
#									 [self.tableTracksFieldAltmax,						 40,		'Int',		'Calcul',	0, 	0	],			
#									 [self.tableTracksFieldTroncons,					 50,		'List',		'Calcul',	3, 	0	],			
#									 [self.tableTracksFieldReperes,						 50,		'List',		'Calcul',	3, 	0	],			
#									 [self.tableTracksIFieldPOIs, 						 50,		'List',		'Résultat',	1, 	0	],			
#									 [self.tableTracksIFieldCalcul,						 80,		'Text',		'Résultat',	3, 	0	],			
#									 [self.tableTracksIFieldGaps,						 40,		'List',		'Résultat',	3, 	0	],			
#									 [self.tableTracksQFieldDelta,						 40,		'Int',		'Résultat',	1, 	0	],			
#									 [self.tableTracksQFieldModif,						 25,		'List',		'Résultat',	3, 	0	], 
#									 [self.tableTracksFieldMarked,						120,		'Text',		'Table',	0, 	1	], 
#									 [self.tableTracksIFieldDistanceEquivalenteDirecte,	 50,		'Int',		'Résultat',	0, 	0	],
#									 [self.tableTracksIFieldDistanceEquivalenteInverse,	 50,		'Int',		'Résultat',	0, 	0	],
#									 [self.tableTracksIFieldEchelleMaxPortrait,			 50,		'TextR',	'Résultat',	0, 	0	],
#									 [self.tableTracksIFieldEchelleMaxPaysage,			 50,		'TextR',	'Résultat',	0, 	0	],
#									 [self.tableTracksIFieldPOIsAll, 					 50,		'List',		'Résultat',	1, 	0	]]			
		



# ========================================================================================
# ========================================================================================
#
# QCarto - Maintenance
#
# ========================================================================================
# ========================================================================================

#	Répertoire Backup Projet sur Drive

		self.pathBackupCartoProjects = self.pathDriveCarto + 'Backup Projets QCarto/'


# ========================================================================================
# ========================================================================================
#
# QCarto - Outils
#
# ========================================================================================
# ========================================================================================

# 	Répertoire et Nom de la Couche de référence pour la conversion des GPX en Shape		
		self.configPathGPXShapes = self.configLocalPath + 'Qgis_Shapes/Couches Gpx/'
		self.configGPXShapeLines = 'Shape 3812 (GPX)'

#	Réperoire pour export Point
		self.configPathExportPOI = self.configLocalProjectPath + 'Export POI/'

#	Distance maximum pour attacher points 

		self.C_ToolsMaxDistanceForAttachPoint = 5					# A plus de 5 mètres, on attache pas automatiquement
		self.C_ToolsCloseDistanceForAttachPoint = 1					# A 1 mètre, on attache même si plusieurs sections
		
#	Longeur minimale pour découpe automatique segment

		self.C_ToolsMinimumSectionLength = 50						# Aucune section coupée plus courte que 50 m


# ========================================================================================
# ========================================================================================
#
# QCarto - Divers
#
# ========================================================================================
# ========================================================================================

# 	CSV Format
		
		self.configCSVSeparator = ';'
		self.configCSVSeparatorReplacement = '.'

		self.configCSVNewLine = '\n'
		self.configCSVNewLineReplacement = ' '
		

# ========================================================================================
# ========================================================================================
#
# QCarto - HTML
#
# ========================================================================================
# ========================================================================================

# Fichier HTML pour voir la Carte

		self.exportSeeMapHtmlFile = 'QCarto - Carte Active - Voir Carte.html'

		self.exportSeeMapHtmlContent = [
										'<!DOCTYPE html>', 
										'<html>' ,
										'<head>' ,
										'<meta http-equiv="Content-type" content="text/html; charset=utf-8" />' ,
										'<title>SGR Carto - Documentation</title>' ,
										'<link rel="stylesheet" href="SGR Carto - Menus - Styles.css">' ,
										'<link rel="icon" type="Images/png" href="Images/SGR Carto - Menu - Icone HTML.png" />' ,
										'</head>' ,
										'<body>' ,
										'<h1 style = "vertical-align:middle"> &nbsp %TITLE% &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp <img src = "Images/SGR Carto - Logo.png" width = "150" style = "vertical-align:bottom" ></h1>' ,
										'<h2> Image de la Carte : %MAPPATH%"</h2>' ,
										'<img src = "FILE:\\\\\\%MAPPATH%" width = "%WIDTH%">' ,
										'<br><br>' ,
										'<p><i>[Date export fichier : %TIMESTAMP%]' ,
										'</body>', 
										'</html>'
									]

# Fichier HTML pour voir le code Html (GPX)

		self.exportSeeHtmlHtmlFile = 'QCarto - Fichier HTML - Voir contenu.html'
		
		self.exportSeeHtmlHtmlContent = [
										'<!DOCTYPE html>', 
										'<html>' ,
										'<head>' ,
										'<meta http-equiv="Content-type" content="text/html; charset=utf-8" />' ,
										'<title>SGR Carto - Livraisons</title>' ,
										'<link rel="stylesheet" href="SGR Carto - Menus - Styles.css">' ,
										'<link rel="icon" type="Images/png" href="Images/SGR Carto - Menu - Icone HTML.png" />' ,
										'</head>' ,
										'<body>' ,
										'<h1 style = "vertical-align:middle"> &nbsp %TITLE% &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp <img src = "Images/SGR Carto - Logo.png" width = "150" style = "vertical-align:bottom" ></h1>' ,
										'<h2> Vue du fichier Html : %HTMLPATH%"</h2>' ,
										'<article style="padding: 30px; background-color: #f6f8ff; border-style: dotted">' ,
										'%HTMLLINES%' ,
										'</article>' ,
										'<br><br>' ,
										'<p><i>[Date export fichier : %TIMESTAMP%]' ,
										'</body>', 
										'</html>'
									]
		
# Ficher HTML pour voir un CSV

		self.exportSeeCsvHtmlFile = 'QCarto - Fichier CSV - Voir contenu.html'

		self.exportSeeCsvHtmlContent = [
										'<!DOCTYPE html>', 
										'<html>' ,
										'<head>' ,
										'<meta http-equiv="Content-type" content="text/html; charset=utf-8" />' ,
										'<title>SGR Carto - Documentation</title>' ,
										'<link rel="stylesheet" href="SGR Carto - Menus - Styles.css">' ,
										'<link rel="icon" type="Images/png" href="Images/SGR Carto - Menu - Icone HTML.png" />' ,
										'</head>' ,
										'<body>' ,
										'<h1 style = "vertical-align:middle"> &nbsp %TITLE% &nbsp &nbsp &nbsp &nbsp &nbsp &nbsp <img src = "Images/SGR Carto - Logo.png" width = "150" style = "vertical-align:bottom" ></h1>' ,
										'<h2> Contenu du fichier : %CSVPATH%</h2>' ,
										'<table>' ,
										'@TableRow@' ,
										'</table>' ,
										'<br><br>' ,
										'<p><i>[Date export fichier : %TIMESTAMP%]' ,
										'</body>', 
										'</html>'
									]


# ========================================================================================
# ========================================================================================
#
# GPX Format
#
# ========================================================================================
# ========================================================================================
		
		self.configGPXHeaderLines = 	['<?xml version="1.0" encoding="UTF-8" standalone="yes"?>',															\
										'<gpx',																												\
										' xmlns="http://www.topografix.com/GPX/1/1"',																		\
										' creator="SGR asbl - Carto Team - QCarto - ' + self.version + '"',													\
										' version="1.1"',																									\
										' xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"',															\
										' xsi:schemaLocation="http://www.topografix.com/GPX/1/1 http://www.topografix.com/GPX/1/1/gpx.xsd">' ]

		self.configGPXMetadataLines = 	['<metadata>',																										\
										 ' <copyright>Propriété de l\'asbl SGR protégée par le droit d\'auteur</copyright>',								\
										 ' <time>%DATE%T%TIME%Z</time>',																					\
										 ' <bounds minlat="%MINLAT%" minlon="%MINLONG%" maxlat="%MAXLAT%" maxlon="%MAXLONG%"/>',							\
										 '</metadata>'		]					

		self.configGPXTrkOpenLines = 	['<trk>',																						\
										 ' <name>%NAME%</name>',																		\
										 ' <desc>%DESC%</desc>',																		\
#										 ' <cmt>%CMT%</cmt>',																			\		# Causes Bug in Basecamp
										 ' <extensions>',																				\
										 '  <gpxx:TrackExtension xmlns:gpxx="http://www.garmin.com/xmlschemas/GpxExtensions/v3">', 		\
										 '  <gpxx:DisplayColor>%COLOR%</gpxx:DisplayColor>',											\
										 '  </gpxx:TrackExtension>',																	\
										 ' </extensions>'			]

		self.configGPXTrkCloseLines = 	['</trk>',						\
										 '</gpx>'					]				

		self.configGPXTrkCloseTrkLines = 	['</trk>' ]
		self.configGPXTrkCloseGpxLines = 	['</gpx>' ]

		self.configGPXSegOpenLines = 	['<trkseg>'		]
		self.configGPXSegCloseLines = 	['</trkseg>'	]
		
		self.configTrkptLines = 		['<trkpt lat="%LAT%" lon="%LON%">',				\
										 '	<ele>%ALT%</ele>',							\
										 '	<time>%TIME%</time>',						\
										 '</trkpt>'					]				


		self.configGPXCouleurGR = 					'Red'
		self.configGPXCouleurGRVariantes = 			'Blue'
		self.configGPXCouleurGRLiaisons = 			'Magenta'
		self.configGPXCouleurGRBoucles = 			'Green'

		self.configMultiGPXCouleurBase = 			'Magenta'
		self.configMultiGPXCouleurRac = 			'Blue'
		self.configMultiGPXCouleurVar = 			'Green'
		self.configMultiGPXCouleurRetour = 			'Black'

		self.configGPXWPCouleurPOI = 				'Navaid, Green'
		self.configGPXWPCouleurRBDA = 				'Trail Head'
		self.configGPXWPCouleurRB = 				'Navaid, Red'
		self.configGPXWPCouleurGR = 				'Navaid, White/Red'
		self.configGPXWPCouleurKM = 				'Triangle, Blue'
		self.configGPXWPCouleurUndefined = 			'Navaid, Black'

		self.configGPXWaypointLines = 	['<wpt lat="%LAT%" lon="%LON%">',					\
										 '  <ele>%ALT%</ele>',								\
										 '  <name>%NAME%</name>',							\
										 '  <desc>%DESC%</desc>',							\
										 '  <sym>Navaid, White/Red</sym>',					\
										 '</wpt>'						]

		self.configGPXPoiLines = 		['<wpt lat="%LAT%" lon="%LON%">',					\
										 '  <ele>%ALT%</ele>',								\
										 '  <name>%TITLE%</name>',							\
										 '  <desc>%TEXT%</desc>',							\
										 '  <sym>Navaid, Green</sym>',						\
										 '</wpt>'						]

		self.configGPXCloseLines = 		['</gpx>'			]				


# ========================================================================================
# ========================================================================================
#
# Accès au Site SGR
#
# ========================================================================================
# ========================================================================================

		self.configSiteSGRFtpConnect = 'ftp.cluster028.hosting.ovh.net'
		self.configSiteSGRFtpUser = 'grsente'
		self.configSiteSGRFtpPassword = 'ENeC8JZXpqXz'
		self.configSiteSGRGPXFolder = 'www/GPX'
		self.configSiteSGRMAJFolder = 'www/MAJ'


# ========================================================================================
# ========================================================================================
#
# Rasters et MNT
#
# ========================================================================================
# ========================================================================================

#  Répertoire et Noms des Couches de Référence pour les Cartes IGN Topo 400

		self.configPathIgn400Shapes = self.configLocalPath + 'Qgis_Rasters/BEL IGN Topo 400/'
		self.configIgn400ShapesList = [	'400d_381.tif' ]

#  Répertoire et Noms des Couches de Référence pour les Cartes IGN Topo 250

		self.configPathIgn250Shapes = self.configLocalPath + 'Qgis_Rasters/BEL IGN Topo 250/'
		self.configIgn250ShapesList = [	'Map_381dpi.tif' ]

#  Répertoire et Noms des Couches de Référence pour les Cartes IGN Topo 50
		self.configPathIgn50Ed3Shapes = self.configLocalPath + 'Qgis_Rasters/BEL IGN Topo 50 - Ed3/'
		self.configPathIgn50Ed4Shapes = self.configLocalPath + 'Qgis_Rasters/BEL IGN Topo 50 - Ed4/'
		self.configIgn50ShapesList = ['23map.tif', '27_28_36map.tif', '29map.tif', \
									  '30map.tif', '31map.tif', '32map.tif', '33map.tif', '34map.tif', '35_43map.tif', '37map.tif', '38map.tif', '39map.tif', \
									  '40map.tif', '41map.tif', '42map.tif', '44map.tif', '45map.tif', '46map.tif', '47map.tif', '48map.tif', '49map.tif', \
									  '50_50Amap.tif', '51map.tif', '52map.tif', '53map.tif', '54map.tif', '55map.tif', '56_56Amap.tif', '57map.tif', '58map.tif', '59map.tif', \
									  '60map.tif', '61map.tif', '62map.tif', '63_66map.tif', '64map.tif', '65map.tif', '67_70map.tif', '68_69map.tif', '71_72map.tif' ]
		self.configIgn50InstallOpacity = 85


# ========================================================================================
# MNT pour le Calcul des Altitudes
# ========================================================================================

#  Répertoire et Noms des Couches de Référence pour les MNT 
		self.configPathMntShapes = self.configLocalPath + 'Qgis_Rasters/BEL Altitudes/'
		self.configMntShapesList = ['WAL_MNT_Round_2013_2014.tif', 'MNT Europe Copernicus - Belgium Xtra.tif']
		self.configMntShapesCrs =  {'WAL_MNT_Round_2013_2014.tif' : 'EPSG:31370', 'MNT Europe Copernicus - Belgium Xtra.tif' : 'EPSG:3035' }   
		
										# Last added because using dataProvider Crs no longer works since 3.34


# ========================================================================================
# Couches des Frontières et limites
# ========================================================================================

		self.configPathBorderShapes = self.configLocalPath + 'Qgis_Shapes/BEL Frontières/'
		self.configCommuneShapeName = 'BEL - Communes 3812'
		self.configProvincesShapeName = 'BEL - Provinces 3812'
		self.configBelgiumShapeName = 'BEL - Belgique Frontière'
		self.configBorderShapesList = [self.configBelgiumShapeName, self.configProvincesShapeName, self.configCommuneShapeName ]	

		self.configCommuneFieldName = 'ADMUNAFR'
		self.configPathCommunesCSV = 'Communes Traversées/'
		self.configPathInfosTrackCSV = 'Infos Tracés/'


# ========================================================================================
# Couches des Courbes de Niveau
# ========================================================================================

		self.configPathCdnShapes = self.configLocalPath + 'Qgis_Shapes/BEL Courbes/'
		self.configCdnShapesList = ['BEL - Xtra - 5m', 'BEL - Nord - 5m', 'BEL - Centre - 5m', 'BEL - Sud - 5m']						# Xtra doit être en premier (findBestCdnShape)


# ========================================================================================
# Couches des Grilles
# ========================================================================================

		self.configPathGridShapes = self.configLocalPath + 'Qgis_Shapes/BEL Grilles/'
		self.configGridShapesList = ['Grille UTM-31 on 3812', 'Grille UTM-32 on 3812']

		self.gridLabelWhiteFrameDistance = 3																							# Distance du cadre en mm (dans cadre blanc IR)
		self.gridLabelRBDistance = -5																									# Sur la carte RB, en mm
		
		self.gridVariableLineTop 		= 'QLabelLineTop'
		self.gridVariableLineBottom 	= 'QLabelLineBottom'
		self.gridVariableLineLeft		= 'QLabelLineLeft'
		self.gridVariableLineRight	 	= 'QLabelLineRight'


# ========================================================================================
# IGN Topo 25 - Identification et Nom
# ========================================================================================

		self.configIgnTopo25Table = 			\
			(('','','','','','','','','','1/7-8','2/5-6','2/7-8','3/5-6','','','','','','',''),																				\
			 ('','','','','','','','','','7/3-4','8/1-2','8/3-4','9/1-2','','','','','','',''),																				\
			 ('','','','4/7-8','5/5-6','5/7-8','6/5-6','6/7-8','7/5-6','7/7-8','8/5-6','8/7-8','9/5-6','9/7-8','10/5-6','','','','',''),									\
			 ('','','12/1-2','12/3-4','13/1-2','13/3-4','14/1-2','14/3-4','15/1-2','15/3-4','16/1-2','16/3-4','17/1-2','17/3-4','18/1-2','18/3-4','','','',''),				\
			 ('','11/7-8','12/5-6','12/7-8','13/5-6','13/7-8','14/5-6','14/7-8','15/5-6','15/7-8','16/5-6','16/7-8','17/5-6','17/7-8','18/5-6','18/7-8','','','',''),		\
			 ('','19/3-4','20/1-2','20/3-4','21/1-2','21/3-4','22/1-2','22/3-4','23/1-2','23/3-4','24/1-2','24/3-4','25/1-2','25/3-4','26/1-2','26/3-4','','','',''),		\
			 ('','19/7-8','20/5-6','20/7-8','21/5-6','21/7-8','22/5-6','22/7-8','23/5-6','23/7-8','24/5-6','24/7-8','25/5-6','25/7-8','26/5-6','26/7-8','','','',''),		\
			 ('','27/3-4','28/1-2','28/3-4','29/1-2','29/3-4','30/1-2','30/3-4','31/1-2','31/3-4','32/1-2','32/3-4','33/1-2','33/3-4','34/1-2','34/3-4','','','',''),		\
			 ('','','28/5-6','28/7-8','29/5-6','29/7-8','30/5-6','30/7-8','31/5-6','31/7-8','32/5-6','32/7-8','33/5-6','33/7-8','34/5-6','34/7-8','35/5-6','','',''),		\
			 ('','','36/1-2','36/3-4','37/1-2','37/3-4','38/1-2','38/3-4','39/1-2','39/3-4','40/1-2','40/3-4','41/1-2','41/3-4','42/1-2','42/3-4','43/1-2','43/3-4','',''),	\
			 ('','','','','37/5-6','37/7-8','38/5-6','38/7-8','39/5-6','39/7-8','40/5-6','40/7-8','41/5-6','41/7-8','42/5-6','42/7-8','43/5-6','43/7-8','',''),				\
			 ('','','','','44/1-2','44/3-4','45/1-2','45/3-4','46/1-2','46/3-4','47/1-2','47/3-4','48/1-2','48/3-4','49/1-2','49/3-4','50/1-2','50/3-4','50/3-4',''),		\
			 ('','','','','','','45/5-6','45/7-8','46/5-6','46/7-8','47/5-6','47/7-8','48/5-6','48/7-8','49/5-6','49/7-8','50/5-6','50/7-8','50A/5-6',''),					\
			 ('','','','','','','51/1-2','51/3-4','52/1-2','52/3-4','53/1-2','53/3-4','54/1-2','54/3-4','55/1-2','55/3-4','56/1-2','56/3-4','56A/1-2',''),					\
			 ('','','','','','','','','52/5-6','52/7-8','53/5-6','53/7-8','54/5-6','54/7-8','55/5-6','55/7-8','56/5-6','56/7-8','',''),										\
			 ('','','','','','','','','57/1-2','57/3-4','58/1-2','58/3-4','59/1-2','59/3-4','60/1-2','60/3-4','61/1-2','61/3-4','',''),										\
			 ('','','','','','','','','57/5-6','57/7-8','58/5-6','58/7-8','59/5-6','59/7-8','60/5-6','60/7-8','61/5-6','','',''),											\
			 ('','','','','','','','','62/1-2','62/3-4','63/1-2','63/3-4','64/1-2','64/3-4','65/1-2','65/3-4','','','',''),													\
			 ('','','','','','','','','','','','63/7-8','64/5-6','64/7-8','65/5-6','65/7-8','','','',''),																	\
			 ('','','','','','','','','','','','66/3-4','67/1-2','67/3-4','68/1-2','68/3-4','','','',''),																	\
			 ('','','','','','','','','','','','','67/5-6','67/7-8','68/5-6','68/7-8','69/5-6','','',''),																	\
			 ('','','','','','','','','','','','','','70/3-4','71/1-2','71/3-4','72/1-2','','',''),																			\
			 ('','','','','','','','','','','','','','','71/5-6','71/7-8','','','',''))

		self.configIgnTopo25TableNord = 748000
		self.configIgnTopo25TableOuest = 502000
		self.configIgnTopo25TableWidth = 16000
		self.configIgnTopo25TableHeight = 10000
		
		self.configIgnTopo25NameDico = {					\
			'01/7-8': 'Essen', '02/6-7': 'Meerle', '03/5-6': 'Maarle', '04/7-8': 'Blankenberge', '05/5-6': 'Knokke-Heist', '05/8-06/5': 'Watervliet', '07/3-4': 'Kalmthout',	\
			'07/5-6': 'Kieldrecht', '07/7-8': 'Brasschaat', '08/1-2': 'Hoogstraten', '08/3-4': 'Baarle-Hertog', '08/5-6': 'Brecht', '08/7-8': 'Turnhout', '09/1-2': 'Ravels',	\
			'09/5-6': 'Arendonk', '09/7-8': 'Achthoek', '10/5-6': 'Achel-Station', '11/7-8': 'Koksijde', '12/1-2': 'Oostende', '12/3-4': 'Oudenburg', '12/5-6': 'Nieuwpoort',	\
			'12/7-8': 'Gistel', '13/1-2': 'Brugge', '13/3-4': 'Eeklo', '13/5-6': 'Oostkamp', '13/7-8': 'Zomergem', '14/1-2': 'Assenede', '14/3-4': 'Stekene',	\
			'14/5-6': 'Evergem', '14/7-8': 'Lokeren', '15/1-2': 'Beveren', '15/3-4': 'Antwerpen', '15/5-6': 'Sint-Niklaas', '15/7-8': 'Kontich', '16/1-2': 'Zandhoven',	\
			'16/3-4': 'Kasterlee', '16/5-6': 'Lier', '16/7-8': 'Geel', '17/1-2': 'Mol', '17/3-4': 'Lommel', '17/5-6': 'Balen', '17/7-8': 'Hechtel-Eksel',	\
			'18/1-2': 'Hamont-Achel', '18/3-4': 'Groot-Beersel', '18/5-6': 'Bree', '18/7-8': 'Maaseik', '19/3-4': 'Veurne', '19/7-8': 'Roesbrugge-Haringe', '20/1-2': 'Diksmuide',	\
			'20/3-4': 'Torhout', '20/5-6': 'Lo-Reninge', '20/7-8': 'Roeselare', '21/1-2': 'Tielt', '21/3-4': 'Aalter', '21/5-6': 'Izegem', '21/7-8': 'Deinze',	\
			'22/1-2': 'Gent', '22/3-4': 'Zele', '22/5-6': 'Merelbeke', '22/7-8': 'Aalst', '23/1-2': 'Dendermonde', '23/3-4': 'Mechelen', '23/5-6': 'Merchtem',	\
			'23/7-8': 'Vilvoorde', '24/1-2': 'Heist-op-den-Berg', '24/3-4': 'Herselt', '24/5-6': 'Haacht', '24/7-8': 'Aarschot', '25/1-2': 'Tessenderlo', '25/3-4': 'Heusden-Zolder',	\
			'25/5-6': 'Diest', '25/7-8': 'Hasselt', '26/1-2': 'Opglabbeek', '26/3-4': 'Dilsen-Stokkem', '26/5-6': 'Genk', '26/7-8': 'Maasmechelen', '27/3-4': 'Watou',	\
			'28/1-2': 'Ieper', '28/3-4': 'Zonnebeke', '28/5-6': 'Heuvelland', '28/7-8': 'Menen', '29/1-2': 'Kortrijk', '29/3-4': 'Oudenaarde', '29/5-6': 'Mouscron',	\
			'29/7-8': 'Ronse', '30/1-2': 'Zottegem', '30/3-4': 'Ninove', '30/5-6': 'Brakel', '30/7-8': 'Geraardsbergen', '31/1-2': 'Dilbeek', '31/3-4': 'Brussel-Bruxelles',	\
			'31/5-6': 'Halle', '31/7-8': 'Ukkel-Uccle', '32/1-2': 'Leuven', '32/3-4': 'Lubbeek', '32/5-6': 'Huldenberg', '32/7-8': 'Tienen', '33/1-2': 'Zoutleeuw',	\
			'33/3-4': 'Alken', '33/5-6': 'Sint-Truiden', '33/7-8': 'Borgloon', '34/1-2': 'Bilzen', '34/5-6': 'Tongeren', '34/7-8': 'Voeren', '35/5-6': 'Plombières',	\
			'36/1-2': 'Le Bizet', '37/1-2': 'Estaimpuis', '37/3-4': 'Frasnes-lez-Anvaing', '37/5-6': 'Tournai', '37/7-8': 'Leuze-en-Hainaut', '38/1-2': 'Lessines', '38/3-4': 'Enghien',	\
			'38/5-6': 'Ath', '38/7-8': 'Soignies', '39/1-2': 'Tubize', '39/3-4': 'Waterloo', '39/5-6': 'Braine-le-Comte', '39/7-8': 'Nivelles', '40/1-2': 'Wavre',	\
			'40/3-4': 'Jodoigne', '40/5-6': 'Gembloux', '40/7-8': 'Éghezée', '41/1-2': 'Hannut', '41/3-4': 'Waremme', '41/5-6': 'Braives', '41/7-8': 'Saint-Georges-sur-Meuse',	\
			'42/1-2': 'Liège', '42/3-4': 'Herve', '42/5-6': 'Seraing', '42/7-8': 'Verviers', '43/1-2': 'Eupen', '43/3-4': 'Petergensfeld', '43/5-6': 'Limbourg',	\
			'43/7-8': 'Reinartzhof', '44/1-2': 'Rongy', '44/3-4': 'Péruwelz', '45/1-2': 'Belœil', '45/3-4': 'Jurbise', '45/5-6': 'Boussu', '45/7-8': 'Mons',	\
			'46/1-2': 'La Louvière', '46/3-4': 'Pont-à-Celles', '46/5-6': 'Binche', '46/7-8': 'Charleroi', '47/1-2': 'Fleurus', '47/3-4': 'Namur', '47/5-6': 'Fosses-la-Ville',	\
			'47/7-8': 'Profondeville', '48/1-2': 'Andenne', '48/3-4': 'Huy', '48/5-6': 'Gesves', '48/7-8': 'Clavier', '49/1-2': 'Esneux', '49/3-4': 'Spa',	\
			'49/5-6': 'Hamoir', '49/7-8': 'Stoumont', '50/1-2': 'Sart', '50/3-4': 'Elsenborn', '50/5-6': 'Malmedy', '50/7-8': 'Bütgenbach', '50a/5-6': 'Losheimergraben',	\
			'51/1-2': 'Honnelles', '51/3-4': 'Grand-Reng', '52/1-2': 'Thuin', '52/3-4': 'Ham-sur-Heure-Nalinnes', '52/5-6': 'Beaumont', '52/7-8': 'Walcourt', '53/1-2': 'Mettet',	\
			'53/3-4': 'Yvoir', '53/5-6': 'Philippeville', '53/7-8': 'Dinant', '54/1-2': 'Ciney', '54/3-4': 'Somme-Leuze', '54/5-6': 'Leignon', '54/7-8': 'Marche-en-Famenne',	\
			'55/1-2': 'Durbuy', '55/3-4': 'Lierneux', '55/5-6': 'Rendeux', '55/7-8': 'Odeigne', '56/1-2': 'Vielsalm', '56/3-4': 'Sankt Vith', '56/5-6': 'Gouvy',	\
			'56/7-8': 'Reuland', '56a/1-2': 'Manderfeld', '57/1-2': 'Sivry-Rance', '57/3-4': 'Cerfontaine', '57/5-6': 'Momignies', '57/7-8': 'Couvin', '58/1-2': 'Doische',	\
			'58/3-4': 'Beauraing', '58/5-6': 'Viroinval', '58/7-8': 'Winenne', '59/1-2': 'Houyet', '59/3-4': 'Rochefort', '59/5-6': 'Wellin', '59/7-8': 'Saint-Hubert',	\
			'60/1-2': 'La Roche-en-Ardenne', '60/3-4': 'Houffalize', '60/5-6': 'Sainte-Ode', '60/7-8': 'Bertogne', '61/1-2': 'Limerlé', '61/3-4': 'Ouren', '62/1-2': 'Macquenoise',	\
			'62/3-4': 'Cul-des-Sarts', '63/1-2': 'Moulin Manteau', '63/3-4': 'Gedinne', '63/7-8': 'Vresse-sur-Semois', '64/1-2': 'Bièvre', '64/3-4': 'Libin', '64/5-6': 'Paliseul',	\
			'64/7-8': 'Bertrix', '65/1-2': 'Sibret', '65/3-4': 'Bastogne', '65/5-6': 'Neufchâteau', '65/7-8': 'Martelange', '66/3-4': 'Sugny', '67/1-2': 'Bouillon',	\
			'67/3-4': 'Herbeumont', '67/5-6': 'Muno', '67/7-8': 'Florenville', '68/1-2': 'Léglise', '68/3-4': 'Attert', '68/5-6': 'Étalle', '68/7-8': 'Arlon',	\
			'69/5-6': 'Autelbas', '70/3-4': 'Villers-devant-Orval', '71/1-2': 'Virton', '71/3-4': 'Aubange', '71/5-6': 'Rouvroy', '71/7-8': 'Signeulx', '72/1-2': 'Kwintenhof',	\
		}


# ========================================================================================
# IGN Topo Rasters - Luxembourg
# ========================================================================================

#  Répertoire et Noms des Couches de Référence pour les Cartes IGN Topo 50
		self.configPathIgn50LuxShapes = self.configLocalPath + 'Qgis_Rasters/LUX IGN Topo 50/'
		self.configIgn50LuxShapesList = ['SCAN_BD-L-CARTO50_TOPO_NORD.TIF', 'SCAN_BD-L-CARTO50_TOPO_SUD.TIF']


# ========================================================================================
# Natagriwal - Zones Natura 2000
# ========================================================================================
		
		self.configPathNatagriwalShapes = self.configLocalPath + 'Qgis_Shapes/Natagriwal/'
		self.configNatagriwalShapeLignes = 'GR-N2000.shp'
		
		self.configNatagriwalShapeNameGR = 'GR-N2000'
		self.configNatagriwalShapeNameRB = 'RB-N2000'
		self.configNatagriwalFieldGRCode 	= 'gr_code'
		self.configNatagriwalFieldGRNom 	= 'gr_nom'
		self.configNatagriwalFieldGRDate 	= 'gr_date'
		self.configNatagriwalFieldGRDist	= 'gr_dist'
		self.configNatagriwalFieldNatCode   = 'nat_code'
		self.configNatagriwalFieldNatDist   = 'nat_dist'
		self.configNatagriwalFieldNatSeg    = 'nat_seg'
	
		self.configN2000FieldCodeSite 	= 'CODE_SITE'

		self.configPathIntersectionShapes = self.configLocalProjectPath + '%PROJECT%/Intersection Shapes/'

				
# ========================================================================================
# ========================================================================================
# 
# OpenStreetMap
# 
# ========================================================================================
# ========================================================================================

# Répertoire et fichiers de référence

		self.configPathOsmShape = self.configLocalPath + 'Qgis_Shapes/Couches Osm/'
		self.configFileOsmShape = 'Parcours-OSM'

# Répertoire des Fichiers .osm du Projet
		self.configPathOsmFiles = self.configLocalProjectPath + '%PROJECT%/Osm Files/'
		self.configPathOsmTrack = self.configLocalProjectPath + '%PROJECT%/Osm Parcours/'

# Répertoire des shapes cartes Osm du projet

		self.configPathMapShapesOsm = self.configLocalProjectPath + '%PROJECT%/Shapes Cartes Osm/'					

# Répertoire et Nom Générique pour l'Export des Fonds Osm
		self.configPathExportOsm = self.configLocalProjectPath + '%PROJECT%/Fonds Osm/'
		self.configNameExportOsm = '%ITI% - %MAP% - Fond Osm %SCALE% (%TIME%).png'

# Elargissaement du rectangle Carte lors de l'export

		self.configFrameOsmExtraSize = 500

# Table des Couches Osm
#	Note : it is supposed that there is only one layer 'Traces'
#   Note : text values in column 0 cannot be changed (or code must be changed too)

		self.configOsmLayers = \
			['Aires', 	'Terrains Fond', 			'Terrains Fond.qml',		'landuse',		'natural',		'leisure',		'amenity',		'surface', 							\
																				'tourism',		'wetland',		'aeroway',		'leaf_type',	'landcover'								], \
			['Courbes',	'Courbes Niveau',		 	'Courbes_5m.qml'																													], \
			['Aires',	'Terrains CDN', 			'Terrains CDN.qml',			'natural',		'leisure',		'amenity',		'man_made',		'power', 	'tourism', 'landuse'		], \
			['Lignes',	'Lignes Rivieres', 			'Rivieres.qml',				'waterway',		'location',		'tunnel',		'intermittent'											], \
			['Aires',	'Zones Eau', 				'Zones Eau.qml',			'landuse',		'natural',		'waterway'																], \
			['Aires',	'Zones Nature',				'Zones Nature.qml',			'natural',		'leisure',		'amenity',		'boundary'												], \
			['Lignes',	'Lignes Nature',			'Lignes Nature.qml',		'natural', 		'man_made'																				], \
			['Lignes',	'Lignes Limites', 			'Lignes Limites.qml',		'boundary',		'leisure',		'admin_level'															], \
			['Aires', 	'Constructions', 			'Constructions.qml',		'building',		'leisure',		'amenity',		'historic',		'power',		'addr:housenumber'		], \
			['Points', 	'Points Nature',			'Points Nature.qml',		'natural',		'ford'																					], \
			['Lignes',	'Lignes Routes', 			'Lignes Routes.qml',		'highway',		'railway',		'aeroway',		'aerialway',	'footway',		'man_made',   	'area',	   \
																				'bridge',		'tunnel',		'access', 		'sac_scale',	'trail_visibility', 	'tracktype'		], \
			['Lignes',	'Lignes Barrieres',			'Lignes Barrieres.qml',		'barrier', 		'historic',		'waterway',		'natural'												], \
			['Lignes',	'Lignes Elec', 				'Lignes Elec.qml',			'power'																									], \
			['Aires', 	'Points Zones',				'Points Zones.qml',			'building',		'power',		'amenity',		'natural',		'leisure',	 	'man_made', 			   \
																				'aeroway',   	'railway'																					], \
			['Points', 	'Points Elec', 				'Points Elec.qml',			'power',		'man_made', 	'pipeline',		'generator:source'	, 'tower:type'						], \
			['Points', 	'Points Routes', 			'Points Routes.qml',		'highway',		'railway',		'aeroway',		'amenity', 	'station'									], \
			['Points', 	'Points Interet',			'Points Interet.qml',		'amenity',		'natural',		'information',	'tourism', 		'man_made',	 'leisure',  'tower:type'	], \
			['Points', 	'Points Monuments',			'Points Monuments.qml',		'amenity',		'historic',		'man_made',		'natural'												], \
			['Points', 	'Points Barrieres',			'Points Barrieres.qml',		'barrier'																								], \
			['Points', 	'Points Commerces',			'Points Commerces.qml',		'amenity',		'shop',			'tourism'																], \
			['Aires', 	'Zones Localites',			'Zones Localites.qml',		'place' 																								], \
			['Points',	'Points Localites', 		'Points Localites.qml',		'place'																									], \
			['Routes', 	'Routes Rando',				'Routes Rando.qml',			'type', 		'route',		'network',		'operator',		'osmc:symbol'							], \
			['Traces', 	'Traces GR',				'Traces GR.qml',			'type', 		'route',		'network',		'operator',		'osmc:symbol'							]

# Special Tags

		self.configOsmAreaPrefixToRemove = ['disused:']

# Tags d'identification 
		self.configOsmIdentificationTagList = ['osm_id', 'osm_type']
		self.configOsmNameTagList = ['name', 'name:fr', 'ref', 'ele']

# Définition des indexes de la Table ci-dessous

		self.configLayerIndexType = 0
		self.configLayerIndexName = 1
		self.configLayerIndexStyle = 2
		self.configLayerIndexShape = 3
		self.configLayerIndexTags = 3


		self.configOsmStyles = self.configLocalPath + 'Qgis_Styles/Couches Osm/'
		self.configOsmStylesStandard = self.configOsmStyles + 'Standard/'


# ========================================================================================
# ========================================================================================
# 
# OziExplorer
# 
# ========================================================================================
# ========================================================================================
		
		self.configOziMapFileText = \
			[	"OziExplorer Map Data File Version 2.2",
				"%MAPNAME%",
				"%MAPFILE%",
				"1 ,Map Code,",
				"WGS 84,,0.0000,0.0000,",
				"Reserved 1",
				"Reserved 2",
				"Magnetic Variation,,,E",
				"Map Projection,Mercator,PolyCal,No,AutoCalOnly,No,BSBUseWPX,No",
				"Point01,xy,         0,          0,in, deg,  %P1LATDEG%, %P1LATMIN%,N, %P1LONDEG%, %P1LONMIN%,E, grid,   ,           ,           ,N",
				"Point02,xy,%PIXWIDTH%,          0,in, deg,  %P2LATDEG%, %P2LATMIN%,N, %P2LONDEG%, %P2LONMIN%,E, grid,   ,           ,           ,N",
				"Point03,xy,%PIXWIDTH%,%PIXHEIGHT%,in, deg,  %P3LATDEG%, %P3LATMIN%,N, %P3LONDEG%, %P3LONMIN%,E, grid,   ,           ,           ,N",
				"Point04,xy,         0,%PIXHEIGHT%,in, deg,  %P4LATDEG%, %P4LATMIN%,N, %P4LONDEG%, %P4LONMIN%,E, grid,   ,           ,           ,N",
				"Point05,xy,     ,     ,in, deg,    ,        ,N,    ,        ,E, grid,   ,           ,           ,N",
				"Point06,xy,     ,     ,in, deg,    ,        ,N,    ,        ,E, grid,   ,           ,           ,N",
				"Point07,xy,     ,     ,in, deg,    ,        ,N,    ,        ,E, grid,   ,           ,           ,N",
				"Point08,xy,     ,     ,in, deg,    ,        ,N,    ,        ,E, grid,   ,           ,           ,N",
				"Point09,xy,     ,     ,in, deg,    ,        ,N,    ,        ,E, grid,   ,           ,           ,N",
				"Point10,xy,     ,     ,in, deg,    ,        ,N,    ,        ,E, grid,   ,           ,           ,N",
				"Point11,xy,     ,     ,in, deg,    ,        ,N,    ,        ,E, grid,   ,           ,           ,N",
				"Point12,xy,     ,     ,in, deg,    ,        ,N,    ,        ,E, grid,   ,           ,           ,N",
				"Point13,xy,     ,     ,in, deg,    ,        ,N,    ,        ,E, grid,   ,           ,           ,N",
				"Point14,xy,     ,     ,in, deg,    ,        ,N,    ,        ,E, grid,   ,           ,           ,N",
				"Point15,xy,     ,     ,in, deg,    ,        ,N,    ,        ,E, grid,   ,           ,           ,N",
				"Point16,xy,     ,     ,in, deg,    ,        ,N,    ,        ,E, grid,   ,           ,           ,N",
				"Point17,xy,     ,     ,in, deg,    ,        ,N,    ,        ,E, grid,   ,           ,           ,N",
				"Point18,xy,     ,     ,in, deg,    ,        ,N,    ,        ,E, grid,   ,           ,           ,N",
				"Point19,xy,     ,     ,in, deg,    ,        ,N,    ,        ,E, grid,   ,           ,           ,N",
				"Point20,xy,     ,     ,in, deg,    ,        ,N,    ,        ,E, grid,   ,           ,           ,N",
				"Point21,xy,     ,     ,in, deg,    ,        ,N,    ,        ,E, grid,   ,           ,           ,N",
				"Point22,xy,     ,     ,in, deg,    ,        ,N,    ,        ,E, grid,   ,           ,           ,N",
				"Point23,xy,     ,     ,in, deg,    ,        ,N,    ,        ,E, grid,   ,           ,           ,N",
				"Point24,xy,     ,     ,in, deg,    ,        ,N,    ,        ,E, grid,   ,           ,           ,N",
				"Point25,xy,     ,     ,in, deg,    ,        ,N,    ,        ,E, grid,   ,           ,           ,N",
				"Point26,xy,     ,     ,in, deg,    ,        ,N,    ,        ,E, grid,   ,           ,           ,N",
				"Point27,xy,     ,     ,in, deg,    ,        ,N,    ,        ,E, grid,   ,           ,           ,N",
				"Point28,xy,     ,     ,in, deg,    ,        ,N,    ,        ,E, grid,   ,           ,           ,N",
				"Point29,xy,     ,     ,in, deg,    ,        ,N,    ,        ,E, grid,   ,           ,           ,N",
				"Point30,xy,     ,     ,in, deg,    ,        ,N,    ,        ,E, grid,   ,           ,           ,N",
				"Projection Setup,,,,,,,,,",
				"Map Feature = MF ; Map Comment = MC     These follow if they exist",
				"Track File = TF      These follow if they exist",
				"Moving Map Parameters = MM?    These follow if they exist",
				"MM0,Yes",
				"MMPNUM,4",
				"MMPXY,1,0,0",
				"MMPXY,2,%PIXWIDTH%,0",
				"MMPXY,3,%PIXWIDTH%,%PIXHEIGHT%",
				"MMPXY,4,0,%PIXHEIGHT%",
				"MMPLL,1,   %P1LAT%,  %P1LON%",
				"MMPLL,2,   %P2LAT%,  %P2LON%",
				"MMPLL,3,   %P3LAT%,  %P3LON%",
				"MMPLL,4,   %P4LAT%,  %P4LON%",
				"MM1B,0.800000",
				"MOP,Map Open Position,0,0",
				"IWH,Map Image Width/Height,%PIXWIDTH%,%PIXHEIGHT%",
				"MLP,Map Last Position,%P1LAT%,%P1LON%,100"	]
				
		self.configOziTrackFileHeaderLines = \
			['OziExplorer Track Point File Version 2.1',								\
			 'WGS 84',																	\
			 'Altitude is in Feet',														\
			 'Reserved 3',																\
			 '0,5,%COLOR%,%NAME%,0,0,2,8421376,-1,0',	\
			 '99999'			]

		self.configOziTrackPointFileLines = ['%LAT%, %LON%, %SEG%, %ALT%, 0.0000000,,']
				
		self.configPLTCouleurGR = 					255
		self.configPLTCouleurGRVariantes = 			16711680
		self.configPLTcouleurGRLiaisons = 			16711935
		self.configPLTCouleurGRBoucles = 			32768
			



# ========================================================================================
# ========================================================================================
#
# QBalisage
#
# ========================================================================================
# ========================================================================================

		self.configBaliseursGroup = 'DB Baliseurs'																	# For identification used in QBalisage
		self.configBaliseursTracksLayerName = 'Baliseurs-Tronçons'													# For identification used in QBalisage
		
		self.configBaliseursTracksFieldIdRcaj = 'id_section'
		self.configBaliseursTracksFieldIdBaliseur = 'id_bal'
		self.configBaliseursTracksFieldNomBaliseur = 'nom_bal'
		self.configBaliseursTracksFieldIdBaliseurDuo = 'id_duo'
		self.configBaliseursTracksFieldNomBaliseurDuo = 'nom_duo'


# ========================================================================================
# --- THE END ---
# ========================================================================================





















	
	





# ========================================================================================
# Répertoires et Noms des Couches de Référence
# ========================================================================================









		


# ========================================================================================
# --- THE END ---
# ========================================================================================
