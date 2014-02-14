'''
*
*  SundayPluginPublic.py
*  Version 0.5
*  Sunday Studio Pipeline (Maya) 
*
*  Maintained by Christian Esbo Agergaard - www.3dg.dk
*  Copyright Sunday Animation Studio ApS and Christian Esbo Agergaard 2011 | sundaystudio.com
*
'''

import sys
import os
import imp

import maya.cmds as cmds
import maya.mel as mel

### - Configuration.

# Fetched Pipeline
sundayInstallPath = mel.eval('getenv MAYA_APP_DIR') + '/' + 'SundayPipeline2014'

# Manual Install Pipeline
# Windows Example
#sundayInstallPath = 'c:/Documents and Settings/user/My Doucments/maya/pipeline'
# Mac/Linux Example
#sundayInstallPath = '~/Library/Preferences/Autodesk/pipeline'

###################################################################################################

guiFilePath = sundayInstallPath + '/' + 'SundayGui' + '/'
imageFilImage = sundayInstallPath + '/' + 'SundayImage' + '/'
pythonFilePath = sundayInstallPath + '/' + 'SundayPython' + '/'
melFilePath = sundayInstallPath + '/' + 'SundayMel' + '/'

sys.path.append(pythonFilePath)
import SundaySetupPublicPy
reload(SundaySetupPublicPy)

def initializePlugin(obj):
	mel.eval('putenv "SundayGui" "' + guiFilePath + '"')
	mel.eval('putenv "SundayImage" "' + imageFilImage + '"')
	mel.eval('putenv "SundayMel" "' + melFilePath + '"')

	reload(SundaySetupPublicPy)
	SundaySetupPublicPy.SundaySetupLoad()

	print "Sunday Plugin initilized."

def uninitializePlugin(obj):

	reload(SundaySetupPublicPy)
	SundaySetupPublicPy.SundaySetupUnLoad()

	print "Sunday Plugin uninitilized."

