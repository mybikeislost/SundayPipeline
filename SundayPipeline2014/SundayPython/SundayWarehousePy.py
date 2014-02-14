'''
*
*  SundayWarehousePy.py
*  Version 0.5
*  Sunday Studio Pipeline (Maya) 
*
*  Maintained by Christian Esbo Agergaard - www.3dg.dk
*  Copyright Sunday Animation Studio ApS and Christian Esbo Agergaard 2011 | sundaystudio.com
*
'''
import maya.cmds as cmds
import maya.mel as mel
import subprocess
import time
from time import gmtime, strftime
import os
import shutil
import sys
import re
import imp
import fnmatch
import platform
import SundayDialogPy
reload(SundayDialogPy)
SundayImage = mel.eval('getenv SundayImage;')

def SundayWarehouseFlushOptionMenu(flushOptionMenu):
    
    try:
        menuItems = cmds.optionMenu(flushOptionMenu, query = True, itemListLong = True)
        for curItem in menuItems:
            cmds.deleteUI(curItem, menuItem = True)
    except:
        pass



def SundayWarehouseRevealInFinder():
    if platform.system() == 'Windows':
        subprocess.Popen([
            'explorer',
            cmds.optionVar(query = 'SundayWarehousePath').replace('/', '\\')])
    elif platform.system() == 'Linux':
        subprocess.call([
            'xdg-open',
            cmds.optionVar(query = 'SundayWarehousePath')])
    else:
        subprocess.call([
            'open',
            '-R',
            cmds.optionVar(query = 'SundayWarehousePath')])


def SundayWarehouseBrowserOpenInColladaViewer(file):
    colladaViewer = cmds.optionVar(query = 'SundayColladaViewerPath').replace('#', file + '.dae')
    text = cmds.optionVar(query = 'SundayColladaViewerPath').replace('#', file + '.dae')
    result = 0
    if platform.system() == 'Windows':
        result = subprocess.call(colladaViewer.replace('/', '\\'), shell = True)
    else:
        result = subprocess.call(colladaViewer, shell = True)
    if result != 0:
        SundayDialogPy.SundayDialogConfirm('Error                                        ', 'Opening Collada failed.\nCheck viewer executable path.', 'OK')
    


def SundayWarehouseBrowserViewIcon(file):
    file = file + '.png'
    cmds.launchImageEditor(viewImageFile = file)


def SundayWarehouseCreate():
    sel = cmds.ls(selection = True)
    if cmds.ls(selection = True):
        assetPath = cmds.optionVar(query = 'SundayWarehousePath') + '/' + cmds.optionMenu('whCategoryCreateComboBox', query = True, value = True) + '/' + cmds.optionMenu('whTypeCreateComboBox', query = True, value = True) + '/' + cmds.textField('whNameLineEdit', query = True, text = True)
        if os.path.isdir(assetPath) != True:
            os.mkdir(assetPath)
            file = assetPath + '/' + cmds.textField('whNameLineEdit', query = True, text = True)
            shaderGroups = []
            for curSel in sel:
                print cmds.listConnections(curSel)
                seNode = cmds.listConnections(curSel, type = 'shadingEngine', destination = True, source = False, plugs = False)
                
                try:
                    print seNode
                    if cmds.nodeType(seNode[0]) == 'shadingEngine':
                        cmds.select(seNode, add = True, noExpand = True)
                        shaderGroups.append(seNode[0])
                except:
                	pass
                continue

            
            if cmds.radioButton('whCreateMayaBinary', query = True, select = True):
                cmds.file(file, op = 'v=0', typ = 'mayaBinary', es = True)
            else:
                cmds.file(file, op = 'v=0', typ = 'mayaAscii', es = True)
            if cmds.checkBox('whCreateExportColladaCheckBox', query = True, value = True):
                mel.eval('loadPlugin -quiet "fbxmaya";')
                mel.eval('FBXExportColladaFrameRate 25.0;')
                mayaVersion = mel.eval('$mayaVersion = `getApplicationVersionAsFloat`;')
                if mayaVersion != 4.65656e+18:
                    mel.eval('FBXExportTriangulate -v true;')
                
                mel.eval('FBXExportCameras -v true;')
                mel.eval('FBXExportLights -v true;')
                mel.eval('FBXExport -file "' + file + '.dae" -s;')
                inFileName = file + '.dae'
                outFileName = file + '.temp'
                infile = open(inFileName)
                outfile = open(outFileName, 'w')
                reFile = re.compile('(.*)<init_from>.*/(.*)</init_from>')
                for line in infile:
                    m = re.match(reFile, line)
                    if m:
                        outfile.write(m.group(1) + '<init_from>sourceimages/' + m.group(2) + '</init_from>\n')
                        continue
                    outfile.write(line)
                
                infile.close()
                outfile.close()
                shutil.move(outFileName, inFileName)
                cmds.select(sel)
            
            shutil.copyfile(cmds.iconTextButton('iconImage', query = True, image1 = True), file + '.png')
            notes = { }
            notes['Author'] = cmds.textField('whAuthorLineEdit', query = True, text = True)
            notes['Notes'] = str(cmds.scrollField('whInfoTextCreate', query = True, text = True))
            notes['Version'] = mel.eval('getApplicationVersionAsFloat;')
            notes['Render'] = cmds.getAttr('defaultRenderGlobals.ren')
            f = open(file + '.info', 'w')
            f.write(str(notes))
            f.close()
            if cmds.checkBox('whPostImportScriptCheckBox', query = True, value = True):
                f = open(file + '.py', 'w')
                f.write(str(cmds.scrollField('whPythonTextEdit', query = True, text = True)))
                f.close()
            
            if cmds.checkBox('whCreateIncludeTexturesCheckBox', query = True, value = True):
                cmds.hyperShade('', shaderNetworksSelectMaterialNodes = True)
                if len(shaderGroups) != 0:
                    cmds.select(shaderGroups, add = True, noExpand = True)
                
                selShader = cmds.ls(selection = True)
                for curSelShader in selShader:
                    notes = cmds.hyperShade(listUpstreamNodes = curSelShader)
                    for note in notes:
                        if cmds.nodeType(note) == 'file' or cmds.nodeType(note) == 'psdFileTex':
                            cmds.select(note)
                            texFile = cmds.getAttr(note + '.fileTextureName')
                            texturePath = assetPath + '/' + 'sourceimages'
                            stripTexFile = os.path.basename(texFile).split('_')
                            if len(stripTexFile) >= 2:
                                stripTexFilePath = os.path.dirname(texFile)
                                filterTexFile = ''
                                for i in range(len(stripTexFile) - 1):
                                    filterTexFile = filterTexFile + stripTexFile[i] + '_'
                                
                                for matchFile in os.listdir(stripTexFilePath):
                                    if fnmatch.fnmatch(matchFile, filterTexFile + '*'):
                                        print 'Copy : ' + matchFile
                                        
                                        try:
                                            if os.path.isdir(texturePath) != True:
                                                os.mkdir(texturePath)
                                            
                                            shutil.copyfile(os.path.dirname(cmds.getAttr(note + '.fileTextureName')) + '/' + matchFile, texturePath + '/' + matchFile)
                                        except:
                							pass
                                        print 'ERROR. File not found ' + texturePath + '/' + matchFile

                                        continue
                                
                            else:
                                
                                try:
                                    if os.path.isdir(texturePath) != True:
                                        os.mkdir(texturePath)
                                    
                                    shutil.copyfile(cmds.getAttr(note + '.fileTextureName'), texturePath + '/' + os.path.basename(texFile))
                                except:
                					pass
                                print 'ERROR. File not found ' + texturePath + '/' + matchFile

                        len(stripTexFile) >= 2
                    
                
            
            if cmds.checkBox('whCreateExportColladaCheckBox', query = True, value = True) and cmds.checkBox('whCreateViewColladaCheckBox', query = True, value = True):
                SundayWarehouseBrowserOpenInColladaViewer(file)
            
            cmds.optionVar(intValue = ('SundayWarehouseIncludeTexture', cmds.checkBox('whCreateIncludeTexturesCheckBox', query = True, value = True)))
            cmds.optionVar(intValue = ('SundayWarehouseExportCollada', cmds.checkBox('whCreateExportColladaCheckBox', query = True, value = True)))
            cmds.optionVar(intValue = ('SundayWarehouseViewCollada', cmds.checkBox('whCreateViewColladaCheckBox', query = True, value = True)))
            cmds.select(sel)
        else:
            SundayDialogPy.SundayDialogConfirm('Error                                        ', 'Warehouse asset already exists: ' + cmds.textField('whNameLineEdit', query = True, text = True), 'OK')
    else:
        SundayDialogPy.SundayDialogConfirm('Error                                                                ', 'Nothing Selected. Warehouse asset not created.', 'OK')


def SundayWarehouseViewPortCreateIcon():
    iconFile = cmds.internalVar(userTmpDir = True) + 'SundayWarehouseIcon_' + time.strftime('%a-%d-%b-%Y_%H-%M-%S', gmtime()) + '.png'
    iconSize = [
        512,
        512]
    curRenderImage = cmds.getAttr('defaultRenderGlobals.imageFormat')
    cmds.setAttr('defaultRenderGlobals.imageFormat', 32)
    cmds.playblast(forceOverwrite = True, framePadding = 0, viewer = False, showOrnaments = False, frame = cmds.currentTime(query = True), widthHeight = iconSize, percent = 100, format = 'iff', compression = 'png', filename = iconFile)
    cmds.setAttr('defaultRenderGlobals.imageFormat', curRenderImage)
    icon = iconFile + '.0.png'
    cmds.iconTextButton('iconImage', edit = True, image = icon)
    cmds.button('whCreateIcon', edit = True, label = 'Re-Create Icon')


def SundayWarehouseRenderViewCreateIcon():
    iconFile = cmds.internalVar(userTmpDir = True) + 'SundayWarehouseIcon_' + time.strftime('%a-%d-%b-%Y_%H-%M-%S', gmtime()) + '.png'
    curRenderImage = cmds.getAttr('defaultRenderGlobals.imageFormat')
    cmds.setAttr('defaultRenderGlobals.imageFormat', 32)
    
    try:
        saveIcon = mel.eval('renderWindowSaveImageCallback "renderView" "' + iconFile + '" "image";')
    except:
        pass

    if os.path.exists(iconFile):
        cmds.setAttr('defaultRenderGlobals.imageFormat', curRenderImage)
        cmds.iconTextButton('iconImage', edit = True, image = iconFile, width = 30)
    else:
        SundayDialogPy.SundayDialogConfirm('Error                                                                                                        ', 'No RenderView Image found. Maybe nothing is rendered yet?', 'OK')
    print 'RenderView Icon created'


def SundayWarehouseChooseIcon():
    fileIcon = SundayDialogPy.SundayDialogFileOpen('/', 1, 'PNG (*.png)')
    if fileIcon != None:
        cmds.iconTextButton('iconImage', edit = True, image = fileIcon[0])
    


def SundayWarehouseCreateTypeUpdate():
    SundayWarehouseFlushOptionMenu('whTypeCreateComboBox')
    typeList = os.listdir(cmds.optionVar(query = 'SundayWarehousePath') + '/' + cmds.optionMenu('whCategoryCreateComboBox', query = True, value = True))
    if len(typeList) != 0:
        cmds.optionMenu('whTypeCreateComboBox', edit = True, enable = True)
        cmds.button('whCreateFromSelected', edit = True, enable = True)
        cmds.setParent('whTypeCreateComboBox', menu = True)
        for curType in typeList:
            if curType != '.DS_Store':
                cmds.menuItem(label = curType)
                continue
        
    else:
        cmds.optionMenu('whTypeCreateComboBox', edit = True, enable = False)
        cmds.button('whCreateFromSelected', edit = True, enable = False)


def SundayWarehouseCreateUpdate():
    SundayWarehouseFlushOptionMenu('whCategoryCreateComboBox')
    
    try:
        cateList = os.listdir(cmds.optionVar(query = 'SundayWarehousePath'))
    except:
        SundayDialogPy.SundayDialogConfirm('ERROR                                                                  ', 'Sunday Warehouse path was not found.\nCheck the Sunday Settings.', 'OK')
        return None

    cmds.optionMenu('whCategoryCreateComboBox', edit = True, changeCommand = 'SundayWarehousePy.SundayWarehouseCreateTypeUpdate()')
    if len(cateList) != 0:
        cmds.optionMenu('whCategoryCreateComboBox', edit = True, enable = True)
        cmds.button('whCreateFromSelected', edit = True, enable = True)
        cmds.setParent('whCategoryCreateComboBox', menu = True)
        for curCate in cateList:
            if curCate != '.DS_Store':
                cmds.menuItem(label = curCate)
                continue
        
        SundayWarehouseCreateTypeUpdate()
    else:
        cmds.optionMenu('whCategoryCreateComboBox', edit = True, enable = False)
        cmds.optionMenu('whTypeCreateComboBox', edit = True, enable = False)
        cmds.button('whCreateFromSelected', edit = True, enable = False)


def SundayWarehouseCreateNewCategory():
    newCate = SundayDialogPy.SundayDialogPromptVariable('', 'New Category Name                       ', '')
    if newCate != None:
        os.mkdir(cmds.optionVar(query = 'SundayWarehousePath') + '/' + newCate)
        SundayWarehouseCreateUpdate()
    


def SundayWarehouseCreateNewType():
    newType = SundayDialogPy.SundayDialogPromptVariable('', 'New Type Name                           ', '')
    if newType != None:
        print os.mkdir(cmds.optionVar(query = 'SundayWarehousePath') + '/' + cmds.optionMenu('whCategoryCreateComboBox', query = True, value = True) + '/' + newType)
        SundayWarehouseCreateTypeUpdate()
    


def SundayWarehouseViewColladaCheckBoxToggle():
    if cmds.checkBox('whCreateExportColladaCheckBox', query = True, value = True):
        cmds.checkBox('whCreateViewColladaCheckBox', edit = True, enable = True)
    else:
        cmds.checkBox('whCreateViewColladaCheckBox', edit = True, enable = False)


def SundayWarehousePostImportPythonScriptToggle():
    if cmds.checkBox('whPostImportScriptCheckBox', query = True, value = True):
        cmds.button('whPythonRun', edit = True, visible = True)
        cmds.button('whPythonHelp', edit = True, visible = True)
        cmds.window(warehouseCreateUI, edit = True, height = 600)
    else:
        cmds.button('whPythonRun', edit = True, visible = False)
        cmds.button('whPythonHelp', edit = True, visible = False)
        cmds.window(warehouseCreateUI, edit = True, height = 514)


def SundayWarehousePostImportPythonScriptRun():
    exec str(cmds.scrollField('whPythonTextEdit', query = True, text = True))


def SundayWarehouseCreateUI():
    global warehouseCreateUI
    if cmds.optionVar(query = 'SundayWarehousePath') == 'WarehousePathNotSet':
        SundayDialogPy.SundayDialogConfirm('Error                                        ', 'Warehouse path not set.\nOpen settings and set the path.', 'OK')
        return None
    SundayMayaGuiPath = mel.eval('getenv SundayGui;')
    
    try:
        if cmds.window(warehouseCreateUI, exists = True):
            cmds.deleteUI(warehouseCreateUI)
        
        warehouseCreateUI = cmds.loadUI(uiFile = SundayMayaGuiPath + 'SundayWarehouseCreate.ui')
    except:
        cmds.optionVar(query = 'SundayWarehousePath') == 'WarehousePathNotSet'
        warehouseCreateUI = cmds.loadUI(uiFile = SundayMayaGuiPath + 'SundayWarehouseCreate.ui')

    cmds.setParent(warehouseCreateUI)
    cmds.setParent(cmds.button('warehouseIconDummyButtonToGrabParent', query = True, fullPathName = True, parent = True))
    cmds.iconTextButton('iconImage', image = SundayImage + 'SundayLogoBlack_128x128.png', width = 128, height = 128)
    cmds.setParent(warehouseCreateUI)
    cmds.textField('whAuthorLineEdit', edit = True, text = cmds.optionVar(query = 'SundayUserName'))
    cmds.checkBox('whCreateExportColladaCheckBox', edit = True, changeCommand = 'SundayWarehousePy.SundayWarehouseViewColladaCheckBoxToggle()')
    cmds.checkBox('whPostImportScriptCheckBox', edit = True, changeCommand = 'SundayWarehousePy.SundayWarehousePostImportPythonScriptToggle()')
    
    try:
        cmds.checkBox('whCreateIncludeTexturesCheckBox', edit = True, value = cmds.optionVar(query = 'SundayWarehouseIncludeTexture'))
        cmds.checkBox('whCreateExportColladaCheckBox', edit = True, value = cmds.optionVar(query = 'SundayWarehouseExportCollada'))
        cmds.checkBox('whCreateViewColladaCheckBox', edit = True, value = cmds.optionVar(query = 'SundayWarehouseViewCollada'))
    except:
        cmds.optionVar(query = 'SundayWarehousePath') == 'WarehousePathNotSet'

    SundayWarehouseViewColladaCheckBoxToggle()
    SundayWarehousePostImportPythonScriptToggle()
    cmds.showWindow(warehouseCreateUI)
    if platform.system() == 'Windows':
        cmds.window(warehouseCreateUI, edit = True, topLeftCorner = [
            100,
            100])
    
    SundayWarehouseCreateUpdate()


def SundayWarehouseBrowserOpenFile(file):
    curScene = cmds.file(query = True, sceneName = True)
    if curScene != '':
        result = SundayDialogPy.SundayDialogPromptYesNoCancel('Save Changes                                                                                                                                                                ', 'Save to ' + curScene, 'Save', "Don't Save", 'Cancel')
    else:
        result = 'open'
    if result != 'Cancel':
        if result == 'Save':
            cmds.file(save = True)
        
        cmds.file(file, open = True, force = True)
        ext = os.path.splitext(cmds.file(query = True, sceneName = True, shortName = True))[1]
        if ext == '.mb':
            mel.eval('addRecentFile "' + file + '" "mayaBinary";')
        else:
            mel.eval('addRecentFile "' + file + '" "mayaAscii";')
    


def SundayWarehouseBrowserRevealAsset(file):
    if platform.system() == 'Windows':
        subprocess.Popen([
            'explorer',
            os.path.dirname(file).replace('/', '\\')])
    elif platform.system() == 'Linux':
        subprocess.call([
            'xdg-open',
            os.path.dirname(file)])
    else:
        subprocess.call([
            'open',
            '-R',
            os.path.dirname(file)])


def SundayWarehouseBrowserDeleteAsset():
    
    try:
        deleteFile = cmds.iconTextRadioButton(cmds.iconTextRadioCollection('whAssetCollection', query = True, select = True), query = True, label = True)
    except:
        SundayDialogPy.SundayDialogConfirm('Rename Error                                ', 'No Asset Selected!', 'OK')
        return None

    deleteResult = SundayDialogPy.SundayDialogPromptYesNo('Delete Asset:', os.path.splitext(os.path.basename(cmds.iconTextRadioButton(cmds.iconTextRadioCollection('whAssetCollection', query = True, select = True), query = True, label = True)))[0], 'OK', 'Cancel')
    if deleteResult == 'OK':
        shutil.rmtree(os.path.dirname(deleteFile))
        SundayWarehouseBrowserUpdateAssets()
    


def SundayWarehouseBrowserRenameAsset():
    
    try:
        renameAssetPath = os.path.dirname(cmds.iconTextRadioButton(cmds.iconTextRadioCollection('whAssetCollection', query = True, select = True), query = True, label = True))
        renameAssetName = cmds.iconTextRadioButton(cmds.iconTextRadioCollection('whAssetCollection', query = True, select = True), query = True, annotation = True)
    except:
        SundayDialogPy.SundayDialogConfirm('Delete Error                                ', 'No Asset Selected!', 'OK')
        return None

    newName = SundayDialogPy.SundayDialogPromptVariable('Asset Rename', 'Rename                                                     ', renameAssetName)
    if newName == None:
        return None
    assetFiles = os.listdir(renameAssetPath)
    renameAsset = renameAssetPath + '/' + renameAssetName
    if os.path.exists(renameAsset + '.mb'):
        os.renames(renameAsset + '.mb', renameAssetPath + '/' + newName + '.mb')
    
    if os.path.exists(renameAsset + '.ma'):
        os.renames(renameAsset + '.ma', renameAssetPath + '/' + newName + '.ma')
    
    if os.path.exists(renameAsset + '.py'):
        os.renames(renameAsset + '.py', renameAssetPath + '/' + newName + '.py')
    
    if os.path.exists(renameAsset + '.info'):
        os.renames(renameAsset + '.info', renameAssetPath + '/' + newName + '.info')
    
    if os.path.exists(renameAsset + '.png'):
        os.renames(renameAsset + '.png', renameAssetPath + '/' + newName + '.png')
    
    if os.path.exists(renameAsset + '.dae'):
        os.renames(renameAsset + '.dae', renameAssetPath + '/' + newName + '.dae')
    
    assetTypePath = cmds.optionVar(query = 'SundayWarehousePath') + '/' + cmds.optionMenu('whCategoryComboBox', query = True, value = True) + '/' + cmds.optionMenu('whTypeComboBox', query = True, value = True)
    os.renames(renameAssetPath, assetTypePath + '/' + newName)
    SundayWarehouseBrowserUpdateAssets()


def SundayWarehouseBrowserImport(type):
    selected = cmds.ls(selection = True)
    if cmds.iconTextRadioCollection('whAssetCollection', query = True, select = True) == 'NONE':
        SundayDialogPy.SundayDialogConfirm('Error while ' + type + '                              ', 'No Asset Selected!', 'OK')
        return None
    assetPath = os.path.dirname(cmds.iconTextRadioButton(cmds.iconTextRadioCollection('whAssetCollection', query = True, select = True), query = True, label = True))
    if cmds.checkBox('whBrowseIncludeTexturesCheckBox', query = True, value = True):
        sourceImagesPath = cmds.workspace(q = True, rootDirectory = True) + cmds.workspace(fileRuleEntry = 'sourceImages') + '/'
        texPath = assetPath + '/' + 'sourceimages' + '/'
        if os.path.isdir(texPath):
            Tex = os.listdir(texPath)
            textureExists = []
            for curTex in Tex:
                assetTex = texPath + curTex
                if curTex != '.DS_Store':
                    if os.path.exists(sourceImagesPath + curTex):
                        print sourceImagesPath + curTex
                        textureExists.append(curTex)
                    
                os.path.exists(sourceImagesPath + curTex)
            
            if len(textureExists) > 0:
                overwrite = SundayDialogPy.SundayDialogPromptYesNo('Texture(s) already exists in Source Images. Overwrite All?', str(textureExists), 'YES', 'NO')
                if overwrite == 'YES':
                    for curTex in Tex:
                        if curTex != '.DS_Store':
                            assetTex = texPath + curTex
                            shutil.copyfile(assetTex, sourceImagesPath + curTex)
                            continue
                        cmds.iconTextRadioCollection('whAssetCollection', query = True, select = True) == 'NONE'
                    
                
            else:
                for curTex in Tex:
                    if curTex != '.DS_Store':
                        assetTex = texPath + curTex
                        shutil.copyfile(assetTex, sourceImagesPath + curTex)
                        continue
                    cmds.iconTextRadioCollection('whAssetCollection', query = True, select = True) == 'NONE'
                
        
    
    importFile = cmds.iconTextRadioButton(cmds.iconTextRadioCollection('whAssetCollection', query = True, select = True), query = True, label = True)
    fileType = 'mayaBinary'
    if os.path.splitext(importFile)[1] == '.ma':
        fileType = 'mayaAscii'
    
    newNodes = []
    iV = cmds.checkBox('whBrowseIgnoreVersion', query = True, value = True)
    if type == 'reference':
        newNodes = cmds.file(importFile, r = True, type = fileType, namespace = '', returnNewNodes = True, ignoreVersion = iV)
    elif cmds.checkBox('whBrowseUseNameSpace', query = True, value = True):
        newNodes = cmds.file(importFile, i = True, type = fileType, namespace = '', returnNewNodes = True, ignoreVersion = iV)
    else:
        newNodes = cmds.file(importFile, i = True, type = fileType, usingNamespaces = False, returnNewNodes = True, ignoreVersion = iV)
    if cmds.checkBox('whBrowseSetTexturePathCheckBox', query = True, value = True):
        import SundayRenderToolsPy as SundayRenderToolsPy
        reload(SundayRenderToolsPy)
        cmds.select(newNodes)
        SundayRenderToolsPy.SundayRenderSetTexturePathToProject('selected')
    
    if cmds.checkBox('whRunPostImportScript', query = True, value = True) & cmds.checkBox('whRunPostImportScript', query = True, enable = True):
        print 'Run Post Import Script'
        pythonFile = assetPath + '/' + os.path.basename(assetPath) + '.py'
        if os.path.exists(pythonFile):
            cmds.select(newNodes)
            imp.load_source('module.name', pythonFile)
            
            try:
                os.remove(pythonFile + 'c')
            except:
                pass

        
    
    
    try:
        cmds.select(selected)
    except:
        cmds.iconTextRadioCollection('whAssetCollection', query = True, select = True) == 'NONE'
        cmds.select(clear = True)



def SundayWarehouseBrowserUpdateInfo(file):
    asset = cmds.iconTextRadioButton(cmds.iconTextRadioCollection('whAssetCollection', query = True, select = True), query = True, annotation = True)
    f = open(file + '/' + asset + '.info', 'r')
    importNotes = eval(f.read())
    printNotes = 'Asset Name : ' + asset
    printNotes = printNotes + '\n'
    printNotes = printNotes + 'Author : ' + str(importNotes['Author']) + ' | Version : ' + str(importNotes['Version']) + ' | Render : ' + str(importNotes['Render'])
    printNotes = printNotes + '\n'
    printNotes = printNotes + 'Notes : ' + str(importNotes['Notes'])
    printNotes = printNotes + '\n'
    sourceImages = file + '/' + 'sourceimages' + '/'
    texList = ''
    if os.path.isdir(sourceImages):
        for curTex in os.listdir(sourceImages):
            if curTex != '.DS_Store':
                texList = texList + '-' + curTex + ' '
                continue
        
        printNotes = printNotes + 'Textures : ' + texList
    
    cmds.scrollField('whInfoTextBrowser', edit = True, text = printNotes)
    cmds.checkBox('whBrowseUseNameSpace', edit = True, label = 'Use Name Space (' + asset + ')')
    assetPath = os.path.dirname(cmds.iconTextRadioButton(cmds.iconTextRadioCollection('whAssetCollection', query = True, select = True), query = True, label = True))
    pythonFile = assetPath + '/' + os.path.basename(assetPath) + '.py'
    if os.path.exists(pythonFile):
        cmds.checkBox('whRunPostImportScript', edit = True, enable = True)
    else:
        cmds.checkBox('whRunPostImportScript', edit = True, enable = False)


def SundayWarehouseBrowserUpdateAssets():
    cmds.optionVar(stringValue = ('whIconViewComboBox', cmds.optionMenu('whIconViewComboBox', query = True, value = True)))
    cmds.setParent(warehouseBrowserUI)
    cmds.setParent(cmds.button('warehouseIconDummyButtonToGrabParent', query = True, fullPathName = True, parent = True))
    if cmds.scrollLayout('whScrollLayout', query = True, exists = True):
        cmds.deleteUI('whScrollLayout', layout = True)
    
    iconLayout = cmds.optionMenu('whIconViewComboBox', query = True, value = True)
    iconSize = iconLayout.split('x')
    if len(iconSize) > 1:
        cmds.scrollLayout('whScrollLayout', childResizable = True)
        if iconLayout == '64x64':
            cmds.rowColumnLayout(numberOfColumns = 8)
        
        if iconLayout == '96x96':
            cmds.rowColumnLayout(numberOfColumns = 5)
        
        if iconLayout == '128x128':
            cmds.rowColumnLayout(numberOfColumns = 4)
        
        if iconLayout == '192x192':
            cmds.rowColumnLayout(numberOfColumns = 2)
        
        if iconLayout == '256x256':
            cmds.rowColumnLayout(numberOfColumns = 2)
        
    else:
        cmds.scrollLayout('whScrollLayout', childResizable = True)
        cmds.rowColumnLayout(numberOfColumns = 1)
    assetPath = cmds.optionVar(query = 'SundayWarehousePath') + '/' + cmds.optionMenu('whCategoryComboBox', query = True, value = True) + '/' + cmds.optionMenu('whTypeComboBox', query = True, value = True)
    assetDir = os.listdir(assetPath)
    cmds.optionVar(stringValue = ('whIconCaption', cmds.iconTextCheckBox('whIconCaption', query = True, value = True)))
    if len(assetDir) != 0:
        cmds.iconTextRadioCollection('whAssetCollection')
        for curAsset in assetDir:
            curAssetPath = assetPath + '/' + curAsset + '/'
            if curAsset != '.DS_Store':
                assetFile = os.listdir(curAssetPath)
                for curFile in assetFile:
                    file = os.path.splitext(curFile)[0]
                    fileEx = os.path.splitext(curFile)[1]
                    if fileEx == '.mb' or fileEx == '.ma':
                        image = curAssetPath + file + '.png'
                        if len(iconSize) > 1:
                            if cmds.optionVar(query = 'whIconCaption') == 'True':
                                cmds.columnLayout(rowSpacing = 0, columnWidth = int(iconSize[0]))
                            
                            assetIcon = cmds.iconTextRadioButton(image1 = image, height = int(iconSize[0]), width = int(iconSize[0]), onCommand = 'SundayWarehousePy.SundayWarehouseBrowserUpdateInfo("' + curAssetPath + '")', label = curAssetPath + curFile, annotation = file)
                            cmds.popupMenu(button = 3, markingMenu = True)
                            cmds.menuItem(label = 'View Icon', command = 'SundayWarehousePy.SundayWarehouseBrowserViewIcon("' + curAssetPath + file + '")')
                            if os.path.exists(curAssetPath + file + '.dae'):
                                cmds.menuItem(label = 'View Collada', command = 'SundayWarehousePy.SundayWarehouseBrowserOpenInColladaViewer("' + curAssetPath + file + '")')
                            else:
                                cmds.menuItem(label = 'View Collada (No .DAE)', enable = False)
                            cmds.menuItem(label = 'Reveal Asset', command = 'SundayWarehousePy.SundayWarehouseBrowserRevealAsset("' + curAssetPath + file + '")')
                            cmds.menuItem(divider = True)
                            cmds.menuItem(label = 'Open Original', command = 'SundayWarehousePy.SundayWarehouseBrowserOpenFile("' + curAssetPath + file + fileEx + '")')
                            if cmds.optionVar(query = 'whIconCaption') == 'True':
                                cmds.text(label = file, width = int(iconSize[0]), align = 'left')
                                cmds.setParent('..')
                            
                        else:
                            cmds.rowColumnLayout(numberOfColumns = 3, columnWidth = [
                                (1, 64),
                                (2, 8),
                                (3, 435)])
                            assetIcon = cmds.iconTextRadioButton(image1 = image, height = 64, width = 64, onCommand = 'SundayWarehousePy.SundayWarehouseBrowserUpdateInfo("' + curAssetPath + '")', label = curAssetPath + curFile, annotation = file)
                            cmds.popupMenu(button = 3, markingMenu = True)
                            cmds.menuItem(label = 'View Icon', command = 'SundayWarehousePy.SundayWarehouseBrowserViewIcon("' + curAssetPath + file + '")')
                            if os.path.exists(curAssetPath + file + '.dae'):
                                cmds.menuItem(label = 'View Collada', command = 'SundayWarehousePy.SundayWarehouseBrowserOpenInColladaViewer("' + curAssetPath + file + '")')
                            else:
                                cmds.menuItem(label = 'View Collada (No .DAE)', enable = False)
                            cmds.menuItem(label = 'Reveal Asset', command = 'SundayWarehousePy.SundayWarehouseBrowserRevealAsset("' + curAssetPath + file + '")')
                            cmds.menuItem(divider = True)
                            cmds.menuItem(label = 'Open Original', command = 'SundayWarehousePy.SundayWarehouseBrowserOpenFile("' + curAssetPath + file + '")')
                            cmds.text(label = '')
                            cmds.text(label = file, align = 'left')
                            cmds.setParent('..')
                    len(iconSize) > 1
                
        
    
    cmds.optionVar(stringValue = ('whCategoryComboBox', cmds.optionMenu('whCategoryComboBox', query = True, value = True)))
    cmds.optionVar(stringValue = ('whTypeComboBox', cmds.optionMenu('whTypeComboBox', query = True, value = True)))


def SundayWarehouseBrowserUpdateType():
    SundayWarehouseFlushOptionMenu('whTypeComboBox')
    typeList = os.listdir(cmds.optionVar(query = 'SundayWarehousePath') + '/' + cmds.optionMenu('whCategoryComboBox', query = True, value = True))
    if len(typeList) != 0:
        cmds.optionMenu('whTypeComboBox', edit = True, enable = True)
        cmds.setParent('whTypeComboBox', menu = True)
        for curType in typeList:
            if curType != '.DS_Store':
                cmds.menuItem(label = curType)
                continue
        
        
        try:
            cmds.optionMenu('whTypeComboBox', edit = True, value = cmds.optionVar(query = 'whTypeComboBox'))
        except:
            pass

        SundayWarehouseBrowserUpdateAssets()
    else:
        cmds.optionMenu('whTypeComboBox', edit = True, enable = False)
        if cmds.scrollLayout('whScrollLayout', query = True, exists = True):
            cmds.deleteUI('whScrollLayout', layout = True)
        


def SundayWarehouseBrowserUpdate():
    SundayWarehouseFlushOptionMenu('whCategoryComboBox')
    cateList = os.listdir(cmds.optionVar(query = 'SundayWarehousePath'))
    if len(cateList) != 0:
        cmds.optionMenu('whCategoryComboBox', edit = True, enable = True)
        cmds.setParent('whCategoryComboBox', menu = True)
        for curCate in cateList:
            if curCate != '.DS_Store':
                cmds.menuItem(label = curCate)
                continue
        
        
        try:
            cmds.optionMenu('whCategoryComboBox', edit = True, value = cmds.optionVar(query = 'whCategoryComboBox'))
        except:
            pass

        SundayWarehouseBrowserUpdateType()
    else:
        cmds.optionMenu('whCategoryComboBox', edit = True, enable = False)
        cmds.optionMenu('whTypeComboBox', edit = True, enable = False)


def SundayWarehouseBrowserDeleteCategory():
    deleteResult = SundayDialogPy.SundayDialogPromptYesNo('Delete Category:', cmds.optionMenu('whCategoryComboBox', query = True, value = True), 'OK', 'Cancel')
    if deleteResult == 'OK':
        deleteDir = cmds.optionVar(query = 'SundayWarehousePath') + '/' + cmds.optionMenu('whCategoryComboBox', query = True, value = True)
        shutil.rmtree(deleteDir)
        SundayWarehouseBrowserUpdate()
    


def SundayWarehouseBrowserDeleteType():
    deleteResult = SundayDialogPy.SundayDialogPromptYesNo('Delete Type:', cmds.optionMenu('whTypeComboBox', query = True, value = True), 'OK', 'Cancel')
    if deleteResult == 'OK':
        deleteDir = cmds.optionVar(query = 'SundayWarehousePath') + '/' + cmds.optionMenu('whCategoryComboBox', query = True, value = True) + '/' + cmds.optionMenu('whTypeComboBox', query = True, value = True)
        shutil.rmtree(deleteDir)
        SundayWarehouseBrowserUpdateType()
    


def SundayWarehouseBrowserDockedUI():
    if cmds.dockControl('sundayWarehouseBrowserDock', query = True, exists = True):
        cmds.deleteUI('sundayWarehouseBrowserDock')
    
    SundayWarehouseBrowserUI()
    mainWindow = cmds.paneLayout(parent = mel.eval('$temp1=$gMainWindow'))
    cmds.dockControl('sundayWarehouseBrowserDock', width = 275, area = 'right', label = 'Sunday | Warehouse Browser', content = mainWindow, allowedArea = [
        'right',
        'left'], backgroundColor = [
        4.6007e+18,
        4.6007e+18,
        4.6007e+18])
    cmds.control(warehouseBrowserUI, edit = True, parent = mainWindow)


def SundayWarehouseBrowserUI():
    global warehouseBrowserUI
    if cmds.optionVar(query = 'SundayWarehousePath') == 'WarehousePathNotSet':
        SundayDialogPy.SundayDialogConfirm('Error                                        ', 'Warehouse path not set.\nOpen settings and set the path.', 'OK')
        return None
    SundayMayaGuiPath = mel.eval('getenv SundayGui;')
    
    try:
        if cmds.window(warehouseBrowserUI, query = True, exists = True):
            cmds.deleteUI(warehouseBrowserUI)
        
        warehouseBrowserUI = cmds.loadUI(uiFile = SundayMayaGuiPath + 'SundayWarehouseBrowser.ui')
    except:
        cmds.optionVar(query = 'SundayWarehousePath') == 'WarehousePathNotSet'
        warehouseBrowserUI = cmds.loadUI(uiFile = SundayMayaGuiPath + 'SundayWarehouseBrowser.ui')

    if cmds.dockControl('sundayWarehouseBrowserDock', query = True, exists = True):
        cmds.deleteUI('sundayWarehouseBrowserDock')
    
    
    try:
        cmds.optionMenu('whIconViewComboBox', edit = True, value = cmds.optionVar(query = 'whIconViewComboBox'))
    except:
        cmds.optionVar(query = 'SundayWarehousePath') == 'WarehousePathNotSet'

    cmds.setParent(cmds.button('whIconCaptionDummy', query = True, fullPathName = True, parent = True))
    cmds.deleteUI('whIconCaptionDummy')
    cmds.iconTextCheckBox('whIconCaption', image1 = SundayImage + 'SundayImageCaption.png', changeCommand = 'SundayWarehousePy.SundayWarehouseBrowserUpdateAssets()')
    cmds.setParent(warehouseBrowserUI)
    if cmds.optionVar(query = 'whIconCaption') == 'True':
        cmds.iconTextCheckBox('whIconCaption', edit = True, value = True)
    
    cmds.showWindow(warehouseBrowserUI)
    if platform.system() == 'Windows':
        cmds.window(warehouseBrowserUI, edit = True, topLeftCorner = [
            100,
            100])
    
    cmds.optionMenu('whIconViewComboBox', edit = True, changeCommand = 'SundayWarehousePy.SundayWarehouseBrowserUpdateAssets()')
    cmds.optionMenu('whCategoryComboBox', edit = True, changeCommand = 'SundayWarehousePy.SundayWarehouseBrowserUpdateType()')
    cmds.optionMenu('whTypeComboBox', edit = True, changeCommand = 'SundayWarehousePy.SundayWarehouseBrowserUpdateAssets()')
    SundayWarehouseBrowserUpdate()
    
    try:
        cmds.deleteUI('sundayWarehouseBrowserDock')
    except:
        cmds.optionVar(query = 'SundayWarehousePath') == 'WarehousePathNotSet'


