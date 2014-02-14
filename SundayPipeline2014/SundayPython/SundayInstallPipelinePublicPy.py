'''
*
*  SundayInstallPipelinePublicPy.py
*  Version 0.6
*  Sunday Studio Pipeline (Maya) 
*
*  Maintained by Christian Esbo Agergaard - www.3dg.dk
*  Copyright Sunday Animation Studio ApS and Christian Esbo Agergaard 2011 | sundaystudio.com
*
'''
import maya.cmds as cmds
import maya.mel as mel
import os
import time
import urllib2
import zipfile
import shutil
import tempfile
import imp

def SundayInstallPipelineVersion():
    pipelineVersion = 4.60358e+18
    return pipelineVersion


def SundayInstallPipelineCheckForUpdate(mode):
    import SundaySetupPublicPy as SundaySetupPublicPy
    reload(SundaySetupPublicPy)
    import SundayDialogPy as SundayDialogPy
    reload(SundayDialogPy)
    fetchFile = tempfile.gettempdir() + os.sep + 'SundayInstallPipelinePublicPy.py'
    
    try:
        open(fetchFile, 'wb').write(urllib2.urlopen('http://3dg.dk/sundaypipeline/mayapublic/SundayInstallPipelinePublicPy.temp').read())
    except:
        if mode == 'active':
            SundayDialogPy.SundayDialogConfirm('Error Fetching Pipeline From Online Repository                ', 'Check Net Connection or Firewall Settings', 'OK')
        else:
            print 'Error Fetching Pipeline From Online Repository - Check Net Connection or Firewall Settings'
        return None

    onlineVersion = imp.load_source('module.name', fetchFile).SundayInstallPipelineVersion()
    if onlineVersion > SundayInstallPipelineVersion():
        updateResult = SundayDialogPy.SundayDialogPromptYesNoCancel('New Sunday Pipeline Version: ' + str(onlineVersion) + '      ', 'Update now?', ' CHANGE LOG ', 'YES', 'NO')
        if updateResult == 'YES':
            
            try:
                SundaySetupPublicPy.SundaySetupSettingssUIClose()
            except:
                pass

            imp.load_source('module.name', fetchFile).SundayInstallPipeline()
        
        if updateResult == ' CHANGE LOG ':
            cmds.showHelp('http://www.3dg.dk/2011/08/12/sunday-pipeline-maya-public/#changelog', absolute = True)
        
    elif mode == 'active':
        SundayDialogPy.SundayDialogConfirm('Sunday Pipeline Is Up To Date       ', 'Current Version: ' + str(SundayInstallPipelineVersion()), 'OK')
    else:
        print 'Sunday Pipeline Is Up To Date. Current Version: ' + str(SundayInstallPipelineVersion())


def SundayInstallPipeline():
    print ''
    print ''
    print '-----------------------------------------------------------------------------------------'
    print 'INFO: Installing Sunday Pipeline (Maya) Public aka SPMP - Version: ' + str(SundayInstallPipelineVersion())
    print 'NOTE: Ignore the Runtime Warning if this is the initial install. Auto-Update should not throw any warnings.'
    print '-----------------------------------------------------------------------------------------'
    print 'Progress:'
    if cmds.pluginInfo('SundayPluginPublic.py', query = True, loaded = True):
        print 'INFO: Unloading existing SPMP Plugin'
        cmds.unloadPlugin('SundayPluginPublic.py')
        print '-----------------------------------------------------------------------------------------'
    
    print 'INFO: Removing plugin from old pipeline structure (Deprecated in >0.8)'
    
    try:
        OLDpluginFilePath = ''
        if os.name == 'nt':
            print 'INFO: Platform is Windows'
            OLDpluginFilePath = mel.eval('getenv MAYA_PLUG_IN_PATH').split(';')[0]
        else:
            print 'INFO: Platform is OSX/Linux'
            OLDpluginFilePath = mel.eval('getenv MAYA_PLUG_IN_PATH').split(':')[0]
        if os.path.exists(OLDpluginFilePath + '/' + 'SundayPluginPublic.py'):
            os.remove(OLDpluginFilePath + '/' + 'SundayPluginPublic.py')
        
        print 'INFO: Removing old/current SPMP Plugin if it exists'
        if os.path.exists(OLDpluginFilePath + os.sep + 'SundayPluginPublic.py'):
            print 'INFO: SPMP plugin found, removing it'
            os.remove(OLDpluginFilePath + os.sep + 'SundayPluginPublic.py')
        
        if not os.listdir(OLDpluginFilePath):
            os.rmdir(OLDpluginFilePath)
    except:
        pass

    print 'INFO: Create pipeline file structure - SundayPipeline directory'
    mayaAppDir = mel.eval('getenv MAYA_APP_DIR')
    pluginFilePath = mayaAppDir + '/' + 'plug-ins'
    print 'INFO: Plugin Path : ' + pluginFilePath
    sundayInstallPath = mayaAppDir + '/' + 'SundayPipeline'
    print 'INFO: Pipeline Path : ' + sundayInstallPath
    print 'INFO: Removing old/current SPMP Plugin if it exists'
    if os.path.exists(pluginFilePath + '/' + 'SundayPluginPublic.py'):
        print 'INFO: SPMP plugin found, removing it'
        os.remove(pluginFilePath + '/' + 'SundayPluginPublic.py')
    else:
        
        try:
            print 'INFO: Plugin direcotry not found, creating it : ' + pluginFilePath
            os.mkdir(pluginFilePath)
        except:
            print 'INFO: Plugin directory already exists : ' + pluginFilePath

    print 'INFO: Maya plugin path is set to : ' + pluginFilePath
    print 'INFO: Removing old/current SPMP Plugin if it exists'
    if os.path.exists(pluginFilePath + '/' + 'SundayPluginPublic.py'):
        print 'INFO: SPMP plugin found, removing it'
        os.remove(pluginFilePath + '/' + 'SundayPluginPublic.py')
    else:
        
        try:
            print 'INFO: Plugin direcotry not found, creating it : ' + pluginFilePath
            os.mkdir(pluginFilePath)
        except:
            print 'INFO: Plugin directory already exists : ' + pluginFilePath

    if os.path.isdir(sundayInstallPath) != True:
        print 'INFO: Pipeline directory not found, creating it'
        os.mkdir(sundayInstallPath)
    else:
        print 'INFO: Pipeline directory found, cleaning it'
        shutil.rmtree(sundayInstallPath)
        os.mkdir(sundayInstallPath)
    print 'INFO: Downloading plugin zip file'
    
    try:
        pluginFile = os.path.join(pluginFilePath, 'plugin.zip')
        open(pluginFile, 'wb').write(urllib2.urlopen('http://3dg.dk/sundaypipeline/mayapublic/plugin.zip').read())
        print 'INFO: Extracting plugin to : ' + pluginFilePath
        zipfile.ZipFile(pluginFile).extractall(pluginFilePath)
    except:
        print 'ERROR: Plugin download or extract failed'

    print 'INFO: Downloading pipeline zip file'
    
    try:
        pipelineFile = os.path.join(sundayInstallPath, 'pipeline.zip')
        open(pipelineFile, 'wb').write(urllib2.urlopen('http://3dg.dk/sundaypipeline/mayapublic/pipeline.zip').read())
        print 'INFO: Extracting pipeline to : ' + sundayInstallPath
        zipfile.ZipFile(pipelineFile).extractall(sundayInstallPath)
    except:
        print 'ERROR: Pipeline download or extract failed'

    print 'INFO: Removing plugin and resources zip files'
    
    try:
        os.remove(pluginFile)
        os.remove(pipelineFile)
    except:
        print 'ERROR: Removing plugin and resources zip files failed. Check file permissions or try to delete manually'

    print 'INFO: Removing __MACOSX hidden files if exists'
    if os.path.exists(pluginFilePath + '/' + '__MACOSX'):
        shutil.rmtree(pluginFilePath + '/' + '__MACOSX')
        shutil.rmtree(sundayInstallPath + '/' + '__MACOSX')
    
    print 'INFO: Sunday Pipeline (Maya) Public Installed'
    print '-----------------------------------------------------------------------------------------'
    print 'INFO: Load SPMP plugin '
    
    try:
        cmds.loadPlugin('SundayPluginPublic.py')
        cmds.pluginInfo('SundayPluginPublic.py', edit = True, autoload = True)
        print 'INFO: Sunday menu should now be visible :)'
    except:
        print 'ERROR: Loading SPMP plugin failed. Try loading manually or reinstall'

    print '-----------------------------------------------------------------------------------------'
    print ''
    print ''
