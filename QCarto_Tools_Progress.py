# ========================================================================================
# by Michel Dawirs - SGR Asbl
# (c) SGR asbl 
# ----------------------------------------------------------------------------------------
# Utilitaires pour la Gestion barres de progression
# ========================================================================================

from qgis.PyQt import QtWidgets

import QCarto_Definitions_Styles as DSTY


def createProgressBar(mainButton, maxValue, size):

	progressBar = QtWidgets.QProgressBar(mainButton)
	DSTY.setStyleProgressBar(progressBar, size)
	progressBar.setRange(0, maxValue)
	progressBar.setValue(0)
	progressBar.deleteLater()
	progressBar.show()

	return progressBar


# ========================================================================================
# --- THE END ---
# ========================================================================================
