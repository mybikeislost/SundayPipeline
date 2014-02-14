'''
*
*  SundayHotkeyPy.py
*  Version 0.1
*  Sunday Studio Pipeline (Maya) 
*
*  Maintained by Christian Esbo Agergaard - www.3dg.dk
*  Copyright Sunday Animation Studio ApS and Christian Esbo Agergaard 2011 | sundaystudio.com
*
'''
import maya.cmds as cmds
import maya.mel as mel
import shutil
import subprocess
import os
import sys
import fnmatch
import platform
from xml.dom import minidom
import SundayDialogPy
reload(SundayDialogPy)

def SundayGeometryCacheShowHelp():
    cmds.showHelp('http://www.3dg.dk/2011/12/07/sunday-pipeline-maya-geometry-cache/', absolute = True)


def SundayGeometryCacheRevealInFinder():
    currentAssetPath = cmds.workspace(q = True, rootDirectory = True) + os.sep + 'data' + os.sep
    if platform.system() == 'Windows':
        subprocess.Popen([
            'explorer',
            currentAssetPath])
    elif platform.system() == 'Linux':
        subprocess.call([
            'xdg-open',
            currentAssetPath])
    else:
        subprocess.call([
            'open',
            '-R',
            currentAssetPath])


def SundayGeometryCacheDelete(cacheDir):
    deleteResult = SundayDialogPy.SundayDialogPromptYesNo('Delete Asset:', cacheDir, 'OK', 'Cancel')
    if deleteResult == 'OK':
        shutil.rmtree(cacheDir)
        SundayGeometryCacheImportUI()
    


def SundayGeometryCacheDeleteOnSelectedObjects():
    selected = cmds.ls(selection = True)
    cmds.select(hierarchy = True)
    mel.eval('source doImportCacheArgList;')
    
    try:
        mel.eval('setCacheEnable 0 0 {};')
        mel.eval('deleteGeometryCache;')
    except:
        pass

    cmds.text('sundayGeoCacheNodeLabel', edit = True, label = len(cmds.ls(type = 'cacheFile', long = True)))


def SundayGeometryCacheImportFile(cacheDir):
    selected = cmds.ls(selection = True)
    cmds.select(hierarchy = True)
    selObj = cmds.ls(selection = True, type = 'transform', long = True)
    files = os.listdir(cacheDir)
    mel.eval('source doImportCacheArgList;')
    
    try:
        mel.eval('setCacheEnable 0 0 {};')
        mel.eval('deleteGeometryCache;')
        print 'Deleting existing cache... Nothing is done if no cache exists.'
    except:
        pass

    for file in files:
        if os.path.splitext(file)[1] == '.xml':
            cacheFile = cacheDir + os.sep + file
            print 'Importing Cache File: ' + cacheFile
            reflist = minidom.parse(cacheFile).getElementsByTagName('channel0')
            fileObj = reflist[0].attributes['ChannelName'].value
            fileShape = fileObj.split(':')[len(fileObj.split(':')) - 1]
            for curObj in selObj:
                
                try:
                    if fileShape == cmds.getAttr(curObj + '.Geometry_Cache_Shape'):
                        cmds.select(curObj)
                        mel.eval('importCacheFile "' + cacheFile + '" "Best Guess";')
                except:
                	pass
                continue

            
    
    
    try:
        cmds.select(selected)
    except:
        pass

    cmds.text('sundayGeoCacheNodeLabel', edit = True, label = len(cmds.ls(type = 'cacheFile', long = True)))


def SundayGeometryCacheImportUI():
    global sundayGeometryCacheImportUI
    print 'SundayGeometryCacheImport'
    exportDir = cmds.workspace(q = True, rootDirectory = True) + 'data'
    cacheDir = os.listdir(exportDir)
    SundayMayaGuiPath = mel.eval('getenv SundayGui;')
    
    try:
        if cmds.window(sundayGeometryCacheImportUI, exists = True):
            cmds.deleteUI(sundayGeometryCacheImportUI)
        
        sundayGeometryCacheImportUI = cmds.loadUI(uiFile = SundayMayaGuiPath + 'SundayGeometryCacheImport.ui')
    except:
        sundayGeometryCacheImportUI = cmds.loadUI(uiFile = SundayMayaGuiPath + 'SundayGeometryCacheImport.ui')

    cmds.text('SundayGeometryCachePath', edit = True, label = exportDir)
    cmds.setParent(sundayGeometryCacheImportUI)
    cmds.setParent(cmds.button('SundayGeometryImportDummyButtonToGrabParent', query = True, fullPathName = True, parent = True))
    scrollLayout = cmds.scrollLayout(childResizable = True)
    for curCacheDir in cacheDir:
        if curCacheDir.split('.')[0] != '':
            cmds.rowLayout(numberOfColumns = 2, adjustableColumn = 1)
            cmds.button(height = 26, label = curCacheDir, command = 'import SundayGeometryCachePy\nreload(SundayGeometryCachePy)\nSundayGeometryCachePy.SundayGeometryCacheImportFile("' + exportDir + os.sep + curCacheDir + '")')
            cmds.button(height = 26, label = 'Delete', command = 'import SundayGeometryCachePy\nreload(SundayGeometryCachePy)\nSundayGeometryCachePy.SundayGeometryCacheDelete("' + exportDir + os.sep + curCacheDir + '")')
            cmds.setParent('..')
            continue
    
    cmds.setParent(sundayGeometryCacheImportUI)
    cmds.setParent(cmds.button('SundayGeometryImportDummyButtonToGrabParent', query = True, fullPathName = True, parent = True))
    cmds.text('sundayGeoCacheNodeLabel', edit = True, label = len(cmds.ls(type = 'cacheFile', long = True)))
    cmds.showWindow(sundayGeometryCacheImportUI)
    if platform.system() == 'Windows':
        cmds.window(sundayGeometryCacheImportUI, edit = True, topLeftCorner = [
            100,
            100])
    


def SundayGeometryCacheExport():
    selected = cmds.ls(selection = True)
    exportDir = cmds.workspace(q = True, rootDirectory = True) + os.sep + 'data' + os.sep + cmds.textField('geometryExportNameLineEdit', query = True, text = True)
    startFrame = cmds.textField('geometryExportStartFrameEdit', query = True, text = True)
    endFrame = cmds.textField('geometryExportEndFrameEdit', query = True, text = True)
    cmds.select(hierarchy = True)
    cmds.select(visible = True)
    cmds.select(cmds.ls(selection = True, type = 'mesh'))
    mel.eval('doCreateGeometryCache 6 {"3", "' + str(startFrame) + '" , "' + str(endFrame) + '", "OneFile", "1", "' + str(exportDir) + '", "1", "","0", "export", "0", "1", "1", "0", "0", "mcc", "1"};')
    cmds.select(selected)
    SundayGeometryCacheExportUIClose()


def SundayGeometryCacheExportSetCacheName(name):
    cmds.textField('geometryExportNameLineEdit', edit = True, text = name)


def SundayGeometryCacheExportUI():
    global sundayGeometryCacheExportUI
    SundayMayaGuiPath = mel.eval('getenv SundayGui;')
    
    try:
        if cmds.window(sundayGeometryCacheExportUI, exists = True):
            cmds.deleteUI(sundayGeometryCacheExportUI)
        
        sundayGeometryCacheExportUI = cmds.loadUI(uiFile = SundayMayaGuiPath + 'SundayGeometryCacheExport.ui')
    except:
        sundayGeometryCacheExportUI = cmds.loadUI(uiFile = SundayMayaGuiPath + 'SundayGeometryCacheExport.ui')

    cmds.setParent(sundayGeometryCacheExportUI)
    
    try:
        selected = cmds.ls(selection = True)[0].split('|')
        cmds.textField('geometryExportNameLineEdit', edit = True, text = selected[len(selected) - 1].replace(':', '-'))
    except:
        cmds.textField('geometryExportNameLineEdit', edit = True, text = 'CacheData')

    cmds.textField('geometryExportStartFrameEdit', edit = True, text = cmds.playbackOptions(query = True, min = True))
    cmds.textField('geometryExportEndFrameEdit', edit = True, text = cmds.playbackOptions(query = True, max = True))
    cmds.setParent(sundayGeometryCacheExportUI)
    cmds.setParent(cmds.button('SundayGeometryExportDummyButtonToGrabParent', query = True, fullPathName = True, parent = True))
    scrollLayout = cmds.scrollLayout(childResizable = True)
    exportDir = cmds.workspace(q = True, rootDirectory = True) + 'data'
    cacheDir = os.listdir(exportDir)
    for curCacheDir in cacheDir:
        if curCacheDir.split('.')[0] != '':
            cmds.rowLayout(numberOfColumns = 2, adjustableColumn = 1)
            cmds.button(height = 26, label = curCacheDir, command = 'import SundayGeometryCachePy\nreload(SundayGeometryCachePy)\nSundayGeometryCachePy.SundayGeometryCacheExportSetCacheName("' + curCacheDir + '")')
            cmds.setParent('..')
            continue
    
    cmds.setParent(sundayGeometryCacheExportUI)
    cmds.setParent(cmds.button('SundayGeometryExportDummyButtonToGrabParent', query = True, fullPathName = True, parent = True))
    cmds.showWindow(sundayGeometryCacheExportUI)
    if platform.system() == 'Windows':
        cmds.window(sundayGeometryCacheExportUI, edit = True, topLeftCorner = [
            100,
            100])
    


def SundayGeometryCacheExportUIClose():
    cmds.deleteUI(sundayGeometryCacheExportUI)


def SundayGeometryCacheExportPrePare():
    print 'SundayGeometryCachePrePare'
    selected = cmds.ls(selection = True)
    cmds.select(hierarchy = True)
    cmds.select(cmds.ls(selection = True, type = 'mesh'))
    selObjects = cmds.ls(selection = True)
    objList = []
    for curSel in selObjects:
        object = curSel.split('|')
        objList.append(object[len(object) - 1])
    
    dList = []
    for curObj in objList:
        if objList.count(curObj) > 1:
            dList.append(curObj)
            continue
    
    if len(list(set(dList))) > 0:
        return dList
    print 'scene ok'
    return ''

