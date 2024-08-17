# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ========================================================================================

from qgis.core import *
from qgis.gui import *
from PyQt5.QtWidgets import QApplication

import QCarto_Tools_Dates as TDAT
import QCarto_Tools_Progress as TPRO

import QCarto_Parameters_Global
QGP = QCarto_Parameters_Global.globalParameters()


def migrateGrCode(grCodeOld):
	if grCodeOld == None: return None
	if grCodeOld[-1] == '²': return grCodeOld[0:-1]
	codeFields = grCodeOld.split('-')
	if len(codeFields) < 3: return '?---?'
	type = codeFields[0]
	
	if type in ('GR', 'GRP', 'GRT'):
		codeFields.pop(2)											# Remove edition

	elif type in ('RB', 'RF'):
		codeFields.pop(2)											# Remove edition
		codeFields[1] = codeFields[1][0:2]							# Remove Tome
		if len(codeFields) >= 3 : codeFields[2] = codeFields[2][1:]	# Remove 'B'
		if codeFields[1] == 'LG': codeFields[1] = 'Lg'				# Fix Liège
		if codeFields[1] == 'LU': codeFields[1] = 'Lu'				# Fix Luxembours
		if codeFields[1] == 'NA': codeFields[1] = 'Na'				# Fix Namur

	elif type == 'RL':
		codeFields.pop(1)											# Remove GG1/2
		codeFields.pop(1)											# Remove edition
		codeFields.append(codeFields[1][2:])						# Split NA23
		codeFields[1] = codeFields[1][0:2]							# Split NA23
		if codeFields[1] == 'LG': codeFields[1] = 'Lg'				# Fix Liège
		if codeFields[1] == 'LU': codeFields[1] = 'Lu'				# Fix Luxembours
		if codeFields[1] == 'NA': codeFields[1] = 'Na'				# Fix Namur
	
	elif type == 'IR':
		codeFields.pop(1)											# Remove MAG
		codeFields.pop(1)											# Remove edition
		codeFields[1] = codeFields[1][1:]							# Remove 'B'
		
	return '-'.join(codeFields)

def migrateGrList(grListOld):
	if grListOld == None: return None
	grCodeList = grListOld.split()
	return ' '.join([migrateGrCode(code) for code in grCodeList])

# ========================================================================================

def migrateTracesGR(mainFrame, button, selectedOny, unlocked):

	if not unlocked :
		mainFrame.setStatusWarning('Activation nécessaire : soyez prudents et patients !!!')
	return

	mainFrame.setStatusWorking('Migration : démarrage ...')
	
	layerNameOld = 'Tracés GR'
	layerOld = QgsProject.instance().mapLayersByName(layerNameOld)[0]
	featureListOld = [feature for feature in (layerOld.getSelectedFeatures() if selectedOny else layerOld.getFeatures())]
	
	layerNameNew = 'Parcours-GR'
	layerNew = QgsProject.instance().mapLayersByName(layerNameNew)[0]
	
	progressBar = TPRO.createProgressBar(button, layerOld.featureCount(), 'Normal')
	
	layerNew.startEditing()
	if selectedOny: 
		codeList = [migrateGrList(feature['code']) for feature in featureListOld]
		expression = '"code" IN ' + str(codeList).replace('[','(').replace(']',')')
		layerNew.selectByExpression(expression)
	else:
		layerNew.selectAll()	
	layerNew.deleteSelectedFeatures()

	for featureOld in featureListOld:
		if featureOld['etat'] == 'Libre' : progressBar.setValue(progressBar.value() + 1); continue
		featureNew = QgsFeature()
		featureNew.setFields(layerNew.fields())
		featureNew['code'] = migrateGrList(featureOld['code'])
		featureNew['nom'] = featureOld['nom']
		featureNew['etat'] = featureOld['etat']
		featureNew['osmid'] = featureOld['osmid']
		featureNew['date'] = featureOld['date']
		featureNew['distance'] = featureOld['dist']
		featureNew['d+'] = featureOld['d+']
		featureNew['d-'] = featureOld['d-']
		featureNew['altmin'] = featureOld['altmin']
		featureNew['altmax'] = featureOld['altmax']
		featureNew.setGeometry(featureOld.geometry())
		layerNew.addFeature(featureNew)
		mainFrame.setStatusWorking('Migration ' + str(featureOld.id()) + ' = ' + featureNew['code'] + ' (' + featureOld['code'] + ')')
		TDAT.sleep(50)
		progressBar.setValue(progressBar.value() + 1)
		QgsApplication.processEvents()
		
	mainFrame.setStatusWorking('Migration : enregistrement de la couche ...')
	layerNew.commitChanges()	
		
	del progressBar		
	mainFrame.setStatusDone('Migration Tracés-GR > Parcours-GR - OK')
		
		
# ========================================================================================

def migrateTracesRB(mainFrame, button, selectedOny, unlocked):

	if not unlocked :
		mainFrame.setStatusWarning('Activation nécessaire : soyez prudents et patients !!!')
	return

	mainFrame.setStatusWorking('Migration : démarrage ...')
	
	layerNameOld = 'Tracés RB'
	layerOld = QgsProject.instance().mapLayersByName(layerNameOld)[0]
	featureListOld = [feature for feature in (layerOld.getSelectedFeatures() if selectedOny else layerOld.getFeatures())]
	
	layerNameNew = 'Parcours-RB'
	layerNew = QgsProject.instance().mapLayersByName(layerNameNew)[0]
	
	progressBar = TPRO.createProgressBar(button, layerOld.featureCount(), 'Normal')
		
	layerNew.startEditing()
	if selectedOny: 
		codeList = [migrateGrList(feature['code']) for feature in featureListOld]
		expression = '"code" IN ' + str(codeList).replace('[','(').replace(']',')')
		layerNew.selectByExpression(expression)
	else:
		layerNew.selectAll()
	layerNew.deleteSelectedFeatures()

	for featureOld in featureListOld:
		if featureOld['etat'] == 'Libre' : progressBar.setValue(progressBar.value() + 1); continue
		if featureOld['etat'] == 'Obsolete' : progressBar.setValue(progressBar.value() + 1); continue
		featureNew = QgsFeature()
		featureNew.setFields(layerNew.fields())
		featureNew['code'] = migrateGrList(featureOld['code'])
		featureNew['nom'] = featureOld['nom']
		featureNew['etat'] = featureOld['etat']
		featureNew['date'] = featureOld['date']
		featureNew['distance'] = featureOld['dist']
		featureNew['d+'] = featureOld['d+']
		featureNew['d-'] = featureOld['d-']
		featureNew['altmin'] = featureOld['altmin']
		featureNew['altmax'] = featureOld['altmax']
		featureNew.setGeometry(featureOld.geometry())
		layerNew.addFeature(featureNew)
		mainFrame.setStatusWorking('Migration ' + str(featureOld.id()) + ' = ' + featureNew['code'] + ' (' + featureOld['code'] + ')')
		TDAT.sleep(50)
		progressBar.setValue(progressBar.value() + 1)	
		QgsApplication.processEvents()

	mainFrame.setStatusWorking('Migration : enregistrement de la couche ...')
	layerNew.commitChanges()	
		
	del progressBar		
	mainFrame.setStatusDone('Migration Tracés-RB > Parcours-RB - OK')


# ========================================================================================

def migrateReperesGR(mainFrame, button, selectedOny, unlocked):

	if not unlocked :
		mainFrame.setStatusWarning('Activation nécessaire : soyez prudents et patients !!!')
	return

	mainFrame.setStatusWorking('Migration : démarrage ...')

	layerNameOld = 'Points GR'
	layerOld = QgsProject.instance().mapLayersByName(layerNameOld)[0]
	featureListOld = [feature for feature in (layerOld.getSelectedFeatures() if selectedOny else layerOld.getFeatures())]
	
	layerNameNew = 'Repères-GR'
	layerNew = QgsProject.instance().mapLayersByName(layerNameNew)[0]
	
	progressBar = TPRO.createProgressBar(button, len(featureListOld), 'Normal')	
	
	layerNew.startEditing()
	if selectedOny: 
		layerNew.selectByIds([feature.id() for feature in featureListOld])
	else:
		layerNew.selectAll()
	layerNew.deleteSelectedFeatures()
	layerNew.commitChanges()	
	layerNew.startEditing()

	for featureOld in featureListOld:

		gr_code_old = featureOld['gr_code']
		if gr_code_old == None: gr_code_old = ''

		gr_code_new = migrateGrList(gr_code_old).split()
		gr_code_new = ' '.join([code for code in gr_code_new])
		QgsApplication.processEvents()

		featureNew = QgsFeature()
		featureNew.setFields(layerNew.fields())
		featureNew['id'] = featureOld['id']
		featureNew['gr_code'] = gr_code_new
		featureNew['repere'] = featureOld['repere']
		featureNew['nom'] = featureOld['Nom']
		featureNew.setGeometry(featureOld.geometry())
		layerNew.addFeature(featureNew)
		
		mainFrame.setStatusWorking('Migration ' + str(featureOld.id()) + ' = ' + featureNew['gr_code'] + ' (' + str(featureOld['gr_code']) + ')')
#		TDAT.sleep(500)
		progressBar.setValue(progressBar.value() + 1)	
		QgsApplication.processEvents()
		
	mainFrame.setStatusWorking('Migration : enregistrement de la couche ...')
	layerNew.commitChanges()	

	if selectedOny: 
		layerNew.selectByIds([feature.id() for feature in featureListOld])
		
	del progressBar		
	mainFrame.setStatusDone('Migration Points GR > Repères-GR - OK')


# ========================================================================================

def migrateReseauGR(mainFrame, button, selectedOny, unlocked):

	if not unlocked :
		mainFrame.setStatusWarning('Activation nécessaire : soyez prudents et patients !!!')
	return

	mainFrame.setStatusWorking('Migration : démarrage ...')
	
	layerNameOld = 'Réseau GR'
	layerOld = QgsProject.instance().mapLayersByName(layerNameOld)[0]
	featureListOld = [feature for feature in (layerOld.getSelectedFeatures() if selectedOny else layerOld.getFeatures())]

	layerNameNew = 'Tronçons-GR'
	layerNew = QgsProject.instance().mapLayersByName(layerNameNew)[0]
	
	progressBar = TPRO.createProgressBar(button, len(featureListOld), 'Normal')		
	
	layerNew.startEditing()
	if selectedOny: 
		layerNew.selectByIds([feature.id() for feature in featureListOld])
	else:
		layerNew.selectAll()
	layerNew.deleteSelectedFeatures()	
	
	for featureOld in featureListOld:
		gr_list = featureOld['gr_list']
		grt_list = featureOld['grt_list']
		rb_list = featureOld['rb_list']
		rf_list = featureOld['rf_list']

		if gr_list == None: gr_list = ''
		if grt_list == None: grt_list = ''
		if rb_list == None: rb_list = ''
		if rf_list == None: rf_list = ''

		all_list_old = gr_list + ' ' + grt_list + ' ' + rb_list + ' ' + rf_list
		all_list_old = all_list_old.replace('$', '')
		all_list_old = all_list_old.replace('*', '')
		all_list_new = migrateGrList(all_list_old).split()
	
		gr_list = ' '.join([code for code in all_list_new if code.split('-')[0] in ('GR', 'GRP')])
		grt_list = ' '.join([code for code in all_list_new if code.split('-')[0] == 'GRT'])
		rl_list = ' '.join([code for code in all_list_new if code.split('-')[0] == 'RL'])
		rb_list = ' '.join([code for code in all_list_new if code.split('-')[0] == 'RB'])
		rf_list = ' '.join([code for code in all_list_new if code.split('-')[0] == 'RF'])
		ir_list = ' '.join([code for code in all_list_new if code.split('-')[0] == 'IR'])

		featureNew = QgsFeature()
		featureNew.setFields(layerNew.fields())
		featureNew['id'] = featureOld['id']
		featureNew['gr_list'] = gr_list
		featureNew['grt_list'] = grt_list
		featureNew['rl_list'] = rl_list
		featureNew['rb_list'] = rb_list
		featureNew['rf_list'] = rf_list
		featureNew['ir_list'] = ir_list
		newGeometry = featureOld.geometry().simplify(QGP.DBCartoSimplifyDistance)
		featureNew.setGeometry(newGeometry)
		layerNew.addFeature(featureNew)
		
		mainFrame.setStatusWorking('Migration : ' + str(featureOld['id']) + ' = ' + gr_list + ' // ' + grt_list + ' // ' + rl_list + ' // ' + rb_list + ' // ' + rf_list + ' // ' + ir_list + ' (' + all_list_old + ')')
		TDAT.sleep(10)
		progressBar.setValue(progressBar.value() + 1)	
		QgsApplication.processEvents()
		
	mainFrame.setStatusWorking('Migration : enregistrement de la couche ...')
	layerNew.commitChanges()	
	
	del progressBar		
	mainFrame.setStatusDone('Migration Réseau GR > Tronçons-GR - OK')
	
		
# ========================================================================================

def migrateLabelsTronconsGR(mainFrame, button, selectedOny, unlocked):

	if not unlocked :
		mainFrame.setStatusWarning('Activation nécessaire : soyez prudents et patients !!!')
	return

	mainFrame.setStatusWorking('Migration étiquettes : démarrage ...')
	
	layerNameNew = 'Tronçons-GR'
	layerNew = QgsProject.instance().mapLayersByName(layerNameNew)[0]
	
	featureList = [feature for feature in (layerNew.getSelectedFeatures() if selectedOny else layerNew.getFeatures())]
	
	progressBar = TPRO.createProgressBar(button, len(featureList), 'Normal')		
	
	layerNew.startEditing()			
	for feature in featureList:
		layerNew.changeAttributeValue(feature.id(), feature.fieldNameIndex('ir_list'), feature['ir_list'] + ' ')
		mainFrame.setStatusWorking('Migration étiquettes : ' + str(feature['id']))
		progressBar.setValue(progressBar.value() + 1)	
		QgsApplication.processEvents()
		
	mainFrame.setStatusWorking('Migration : enregistrement de la couche ...')
	layerNew.commitChanges()	
		
	del progressBar		
	mainFrame.setStatusDone('Migration étiquettes - OK')
		
		
# ========================================================================================

def migrateReseauGREd4(mainFrame, button, selectedOny, unlocked):

	if not unlocked :
		mainFrame.setStatusWarning('Activation nécessaire : soyez prudents et patients !!!')
	return

	mainFrame.setStatusWorking('Migration : démarrage ...')
	
	layerNameOld = 'Réseau 50K Ed4'
	layerOld = QgsProject.instance().mapLayersByName(layerNameOld)[0]
	featureListOld = [feature for feature in (layerOld.getSelectedFeatures() if selectedOny else layerOld.getFeatures())]

	layerNameNew = 'Tronçons-GR-Ed4'
	layerNew = QgsProject.instance().mapLayersByName(layerNameNew)[0]
	
	progressBar = TPRO.createProgressBar(button, len(featureListOld), 'Normal')		
	
	layerNew.startEditing()
	if selectedOny: 
		layerNew.selectByIds([feature.id() for feature in featureListOld])
	else:
		layerNew.selectAll()
	layerNew.deleteSelectedFeatures()	
	
	for featureOld in featureListOld:
		gr_list = featureOld['gr_list']
		grt_list = featureOld['grt_list']
		rb_list = featureOld['rb_list']
		rf_list = featureOld['rf_list']

		if gr_list == None: gr_list = ''
		if grt_list == None: grt_list = ''
		if rb_list == None: rb_list = ''
		if rf_list == None: rf_list = ''

		all_list_old = gr_list + ' ' + grt_list + ' ' + rb_list + ' ' + rf_list
		all_list_old = all_list_old.replace('$', '')
		all_list_old = all_list_old.replace('*', '')
		all_list_new = migrateGrList(all_list_old).split()
	
		gr_list = ' '.join([code for code in all_list_new if code.split('-')[0] in ('GR', 'GRP')])
		grt_list = ' '.join([code for code in all_list_new if code.split('-')[0] == 'GRT'])
		rl_list = ' '.join([code for code in all_list_new if code.split('-')[0] == 'RL'])
		rb_list = ' '.join([code for code in all_list_new if code.split('-')[0] == 'RB'])
		rf_list = ' '.join([code for code in all_list_new if code.split('-')[0] == 'RF'])
		ir_list = ' '.join([code for code in all_list_new if code.split('-')[0] == 'IR'])

		featureNew = QgsFeature()
		featureNew.setFields(layerNew.fields())
		featureNew['id'] = featureOld['id']
		featureNew['gr_list'] = gr_list
		featureNew['grt_list'] = grt_list
		featureNew['rl_list'] = rl_list
		featureNew['rb_list'] = rb_list
		featureNew['rf_list'] = rf_list
		featureNew['ir_list'] = ir_list
		for field in ('hash', 'pts', 'dist_mm', 'date', 'pa_x', 'pa_y', 'pz_x', 'pz_y', 'validation') :
			featureNew[field] = featureOld[field]
		newGeometry = featureOld.geometry().simplify(QGP.DBCartoSimplifyDistance)
		featureNew.setGeometry(newGeometry)
		layerNew.addFeature(featureNew)
		
		mainFrame.setStatusWorking('Migration : ' + str(featureOld['id']) + ' = ' + gr_list + ' // ' + grt_list + ' // ' + rl_list + ' // ' + rb_list + ' // ' + rf_list + ' // ' + ir_list + ' (' + all_list_old + ')')
		TDAT.sleep(10)
		progressBar.setValue(progressBar.value() + 1)	
		QgsApplication.processEvents()
		
	mainFrame.setStatusWorking('Migration : enregistrement de la couche ...')
	layerNew.commitChanges()	
	
	del progressBar		
	mainFrame.setStatusDone('Migration Réseau GR > Tronçons-GR-Ed4 - OK')
	
		
# ========================================================================================
# --- THE END ---
# ========================================================================================
