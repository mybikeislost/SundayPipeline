'''
*
*  SundayRenderToolsPy.py
*  Version 0.5
*  Sunday Studio Pipeline (Maya) 
*
*  Maintained by Christian Esbo Agergaard - www.3dg.dk
*  Copyright Sunday Animation Studio ApS and Christian Esbo Agergaard 2011 | sundaystudio.com
*
'''
import maya.cmds as cmds
import maya.mel as mel
import os
import platform
import SundayDialogPy
reload(SundayDialogPy)
SundayImage = mel.eval('getenv SundayImage;')

def SundayRenderToolsImportRenderLayer():
    file = SundayDialogPy.SundayDialogFileOpen('/', 1, 'Render Layer File (*.rl)')
    if file == None:
        return None
    f = open(file[0], 'r')
    iL = eval(f.read())
    for curIL in iL:
        cmds.createRenderLayer(name = curIL, empty = True)
        addObj = iL[curIL]['objects']
        
        try:
            cmds.editRenderLayerMembers(curIL, addObj, noRecurse = True)
        except:
            file == None
            print 'Objects not found in scene'

        addAdj = iL[curIL]['adjustments']
        cmds.editRenderLayerGlobals(currentRenderLayer = curIL)
        for curAdj in addAdj:
            if curAdj.split('.')[1] != 'instObjGroups[0]':
                cmds.editRenderLayerAdjustment(curIL, curAdj)
                
                try:
                    cmds.setAttr(curAdj, addAdj[curAdj])
                except:
                	pass
                print 'Missing : ' + curAdj

                continue
            print 'Shader Overwrite : ' + curAdj
        
        addSet = iL[curIL]['settings']
        for curSet in addSet:
            if curSet == 'renderable':
                cmds.setAttr(curIL + '.renderable', addSet[curSet])
                continue
        
    


def SundayRenderToolsExportRenderLayer():
    exportLayers = { }
    RL = mel.eval('getSelectedRenderItems("RenderLayerTab", "", 0);')
    for curRL in RL:
        if curRL != 'defaultRenderLayer':
            rl = { }
            rl['objects'] = cmds.editRenderLayerMembers(curRL, query = True)
            adj = cmds.editRenderLayerAdjustment(curRL, query = True, layer = True)
            adjustments = { }
            if adj != None:
                for curAdj in adj:
                    adjustments[curAdj] = cmds.getAttr(curAdj)
                
            
            rl['adjustments'] = adjustments
            settings = { }
            settings['renderable'] = cmds.getAttr(curRL + '.renderable')
            rl['settings'] = settings
            exportLayers[curRL] = rl
            continue
        print 'Default layer can not be exported'
    
    file = SundayDialogPy.SundayDialogFileOpen('/', 0, 'Nothing!!')
    if file == None:
        return None
    f = open(file[0] + '.rl', 'w')
    f.write(str(exportLayers))
    f.close()


def SundayRenderToolsHideFGOnSelected():
    sel = cmds.ls(selection = True)
    if len(sel) != 0:
        shapes = cmds.listRelatives(sel, shapes = True)
        for shape in shapes:
            cmds.addAttr(shape, longName = 'miFinalGatherHide', attributeType = 'bool')
            cmds.setAttr(shape + '.miFinalGatherHide', 1)
        
    else:
        SundayDialogPy.SundayDialogConfirm('Error                              ', 'No objects selected', 'OK')


def SundayRenderToolsFixRenderLayerConnections():
    mel.eval('fixRenderLayerOutAdjustmentErrors;')


def SundayRenderToolsCreateContribution(passType, passName, channelNum, filtered):
    sel = cmds.textScrollList('MRContributionPassComboBoxList', query = True, selectItem = True)[0]
    print '----------------------------------------------------'
    print 'Create Pass with Contribution for Selected Object(s)'
    print 'Selected  : ' + sel
    print 'Type      : ' + passType
    print 'Pass Name : ' + passName
    print 'Channel   : ' + str(channelNum)
    print 'Filtered  : ' + str(filtered)
    objects = cmds.ls(selection = True)
    if len(objects) == 0:
        SundayDialogPy.SundayDialogConfirm('Error                             ', 'No objects selected', 'OK')
        return None
    if passName != None:
        passName = passName + '_' + passType
        currentRenderLayer = cmds.editRenderLayerGlobals(query = True, currentRenderLayer = True)
        renderNode = cmds.createNode('renderPass', name = passName)
        passCont = renderNode + '_Cont'
        if passType == 'CAMZ_Remapped':
            cmds.setRenderPassType(renderNode, type = 'CAMZ')
            cmds.setAttr(renderNode + '.remap', 1)
        else:
            cmds.setRenderPassType(renderNode, type = passType)
        cmds.setAttr(renderNode + '.numChannels', channelNum)
        cmds.setAttr(renderNode + '.filtering', filtered)
        cmds.connectAttr(currentRenderLayer + '.renderPass', renderNode + '.owner', nextAvailable = True)
        map = cmds.createNode('passContributionMap', name = passCont)
        cmds.connectAttr(currentRenderLayer + '.passContributionMap', passCont + '.owner', nextAvailable = True)
        cmds.connectAttr(renderNode + '.message', passCont + '.renderPass', nextAvailable = True)
        for curObject in objects:
            cmds.connectAttr(curObject + '.message', passCont + '.dagObjects', nextAvailable = True)
        
        if cmds.checkBox('MRContributionPassSelectPass', query = True, value = True):
            cmds.select(renderNode)
        else:
            cmds.select(objects)
    


def SundayRenderToolsCreateContributionCreate():
    sel = cmds.textScrollList('MRContributionPassComboBoxList', query = True, selectItem = True)[0]
    passName = cmds.textField('MRContributionPassName', query = True, text = True)
    filtered = cmds.checkBox('MRContributionPassFiltering', query = True, value = True)
    channelNum = cmds.optionMenu('MRContributionPassChannels', query = True, value = True)
    if channelNum == '1 (A)':
        channelNum = '1'
    elif channelNum == '3 (RGB)':
        channelNum = '3'
    else:
        channelNum = '4'
    passType = ''
    if sel == '2D Motion Vector':
        passType = 'MV2E'
    elif sel == '3D Motion Vector':
        passType = 'MV3'
    elif sel == 'Ambient':
        passType = 'AMB'
    elif sel == 'Ambient Irradiance':
        passType = 'AMBIRR'
    elif sel == 'Ambient Material Color':
        passType = 'AMBRAW'
    elif sel == 'Ambient Occlusion':
        passType = 'AO'
    elif sel == 'Beauty':
        passType = 'BEAUTY'
    elif sel == 'BEAUTY':
        passType = 'MV3'
    elif sel == 'Camera Depth':
        passType = 'CAMZ'
    elif sel == 'Camera Depth Remapped':
        passType = 'CAMZ_Remapped'
    elif sel == 'Coverage':
        passType = 'COV'
    elif sel == 'Custom Color':
        passType = 'CSTCOL'
    elif sel == 'Custom Depth':
        passType = 'CSTZ'
    elif sel == 'Custom Label':
        passType = 'CSTLBL'
    elif sel == 'Custom Vector':
        passType = 'CSTVCT'
    elif sel == 'Diffuse':
        passType = 'DIFF'
    elif sel == 'Diffuse Material Color':
        passType = 'DIFRAW'
    elif sel == 'Diffuse Without Shadows':
        passType = 'DIFFNS'
    elif sel == 'Direct Irradiance':
        passType = 'DIRIRR'
    elif sel == 'Direct Irradiance Without Shadows':
        passType = 'DIRRNS'
    elif sel == 'Glow Source':
        passType = 'GLORAW'
    elif sel == 'Incandescence':
        passType = 'INC'
    elif sel == 'Incidence (Light / Normal)':
        passType = 'INCILN'
    elif sel == 'Material Incidence (Camera / Normal)':
        passType = 'INCMCN'
    elif sel == 'Object Incidence (Camera / Normal)':
        passType = 'INCICN'
    elif sel == 'Indirect':
        passType = 'INDIRR'
    elif sel == 'Light Volume':
        passType = 'VOLLIT'
    elif sel == 'Matte':
        passType = 'MATTE'
    elif sel == 'Normalized 2D Motion Vector':
        passType = 'MV2N'
    elif sel == 'Material Normal':
        passType = 'NORMAM'
    elif sel == 'Object Normal':
        passType = 'NORMAL'
    elif sel == 'Object Volume':
        passType = 'VOLOBJ'
    elif sel == 'Opacity':
        passType = 'OPACTY'
    elif sel == 'Raw Shadow':
        passType = 'SHDRAW'
    elif sel == 'Reflection':
        passType = 'REFL'
    elif sel == 'Reflection Material Color':
        passType = 'REFLRA'
    elif sel == 'Refraction':
        passType = 'REFR'
    elif sel == 'Refraction Material Color':
        passType = 'REFRRA'
    elif sel == 'Scatter':
        passType = 'SCAT'
    elif sel == 'Scene Volume':
        passType = 'VOLSCN'
    elif sel == 'Shadow':
        passType = 'SHD'
    elif sel == 'Specular':
        passType = 'SPEC'
    elif sel == 'Specular Without Shadows':
        passType = 'SPECNS'
    elif sel == 'Translucence':
        passType = 'TRNSLU'
    elif sel == 'Translucence Without Shadows':
        passType = 'TRNSNS'
    
    SundayRenderToolsCreateContribution(passType, passName, int(channelNum), int(filtered))


def SundayRenderToolsCreateContributionChange():
    sel = cmds.textScrollList('MRContributionPassComboBoxList', query = True, selectItem = True)[0]
    cmds.checkBox('MRContributionPassFiltering', edit = True, value = True)
    if sel == 'Ambient Occlusion':
        cmds.optionMenu('MRContributionPassChannels', edit = True, value = '1 (A)')
    elif sel == 'Beauty Without Reflections and Refractions':
        cmds.optionMenu('MRContributionPassChannels', edit = True, value = '4 (RGBA)')
    elif sel == 'Beauty':
        cmds.optionMenu('MRContributionPassChannels', edit = True, value = '4 (RGBA)')
    elif sel == 'Camera Depth Remapped':
        cmds.optionMenu('MRContributionPassChannels', edit = True, value = '1 (A)')
        cmds.checkBox('MRContributionPassFiltering', edit = True, value = False)
    elif sel == 'Camera Depth':
        cmds.optionMenu('MRContributionPassChannels', edit = True, value = '1 (A)')
        cmds.checkBox('MRContributionPassFiltering', edit = True, value = False)
    elif sel == 'Coverage':
        cmds.optionMenu('MRContributionPassChannels', edit = True, value = '1 (A)')
    elif sel == 'Custom Color':
        cmds.optionMenu('MRContributionPassChannels', edit = True, value = '4 (RGBA)')
    elif sel == 'Custom Depth':
        cmds.optionMenu('MRContributionPassChannels', edit = True, value = '1 (A)')
        cmds.checkBox('MRContributionPassFiltering', edit = True, value = False)
    elif sel == 'Custom Color':
        cmds.optionMenu('MRContributionPassChannels', edit = True, value = '4 (RGBA)')
    elif sel == 'Custom Label':
        cmds.optionMenu('MRContributionPassChannels', edit = True, value = '1 (A)')
    elif sel == 'Glow Source':
        cmds.optionMenu('MRContributionPassChannels', edit = True, value = '4 (RGBA)')
    elif sel == 'Object Incidence (Camera / Normal)':
        cmds.optionMenu('MRContributionPassChannels', edit = True, value = '1 (A)')
    elif sel == 'Material Incidence (Camera / Normal)':
        cmds.optionMenu('MRContributionPassChannels', edit = True, value = '1 (A)')
    elif sel == 'Incidence (Light / Normal)':
        cmds.optionMenu('MRContributionPassChannels', edit = True, value = '1 (A)')
    elif sel == 'Matte':
        cmds.optionMenu('MRContributionPassChannels', edit = True, value = '1 (A)')
    elif sel == 'Light Volume':
        cmds.optionMenu('MRContributionPassChannels', edit = True, value = '4 (RGBA)')
    elif sel == 'Object Volume':
        cmds.optionMenu('MRContributionPassChannels', edit = True, value = '4 (RGBA)')
    elif sel == 'Scene Volume':
        cmds.optionMenu('MRContributionPassChannels', edit = True, value = '4 (RGBA)')
    else:
        cmds.optionMenu('MRContributionPassChannels', edit = True, value = '3 (RGB)')


def SundayRenderToolsCreateContributionUI():
    global mrContributionUI
    SundayMayaGuiPath = mel.eval('getenv SundayGui;')
    
    try:
        if cmds.window(mrContributionUI, exists = True):
            cmds.deleteUI(mrContributionUI)
        
        mrContributionUI = cmds.loadUI(uiFile = SundayMayaGuiPath + 'SundayMRContribution.ui')
    except:
        mrContributionUI = cmds.loadUI(uiFile = SundayMayaGuiPath + 'SundayMRContribution.ui')

    cmds.textScrollList('MRContributionPassComboBoxList', edit = True, selectCommand = 'SundayRenderToolsPy.SundayRenderToolsCreateContributionChange()', doubleClickCommand = 'SundayRenderToolsPy.SundayRenderToolsCreateContributionCreate()', allowMultiSelection = False, append = [
        '2D Motion Vector',
        '3D Motion Vector',
        'Ambient',
        'Ambient Irradiance',
        'Ambient Material Color',
        'Ambient Occlusion',
        'Beauty',
        'Camera Depth',
        'Camera Depth Remapped',
        'Coverage',
        'Custom Color',
        'Custom Depth',
        'Custom Label',
        'Custom Vector',
        'Diffuse',
        'Diffuse Material Color',
        'Diffuse Without Shadows',
        'Direct Irradiance',
        'Direct Irradiance Without Shadows',
        'Glow Source',
        'Incandescence',
        'Incidence (Light / Normal)',
        'Indirect',
        'Light Volume',
        'Material Incidence (Camera / Normal)',
        'Material Normal',
        'Matte',
        'Normalized 2D Motion Vector',
        'Object Incidence (Camera / Normal)',
        'Object Normal',
        'Object Volume',
        'Opacity',
        'Raw Shadow',
        'Reflection',
        'Reflection Material Color',
        'Refraction',
        'Refraction Material Color',
        'Scatter',
        'Scene Volume',
        'Shadow',
        'Specular',
        'Specular Without Shadows',
        'Translucence',
        'Translucence Without Shadows'])
    cmds.showWindow(mrContributionUI)
    if platform.system() == 'Windows':
        cmds.window(mrContributionUI, edit = True, topLeftCorner = [
            100,
            100])
    


def SundayRenderSetTexturePathToProjectSet(note, textureMissing):
    texFile = cmds.getAttr(note + '.fileTextureName')
    if texFile == '':
        print 'Empty/None file name in : ' + note
        return None
    stripFile = os.path.basename(texFile)
    if os.path.isfile(cmds.workspace(query = True, fullName = True) + os.sep + 'sourceimages' + os.sep + stripFile):
        cmds.setAttr(note + '.fileTextureName', 'sourceimages' + os.sep + stripFile, type = 'string')
    else:
        textureMissing.append(stripFile)
    return textureMissing


def SundayRenderSetTexturePathToProject(object):
    sel = cmds.ls(selection = True)
    shaderGroups = []
    for curSel in sel:
        seNode = cmds.listConnections(curSel, type = 'shadingEngine', destination = True, source = False, plugs = False)
        if cmds.nodeType(seNode) == 'shadingEngine':
            cmds.select(seNode, add = True, noExpand = True)
            shaderGroups.append(seNode[0])
            continue
    
    textureMissing = []
    if object == 'selected':
        if len(sel) == 0:
            SundayDialogPy.SundayDialogConfirm('ERROR                       ', 'Nothing selected.', 'OK')
        else:
            cmds.hyperShade('', shaderNetworksSelectMaterialNodes = True)
            if len(shaderGroups) != 0:
                cmds.select(shaderGroups, add = True, noExpand = True)
            
            selShader = cmds.ls(selection = True)
            for curSelShader in selShader:
                notes = cmds.hyperShade(listUpstreamNodes = curSelShader)
                for note in notes:
                    if cmds.nodeType(note) == 'file' or cmds.nodeType(note) == 'psdFileTex':
                        cmds.select(note)
                        textureMissing = SundayRenderSetTexturePathToProjectSet(note, textureMissing)
                        continue
                
            
    elif object == 'global':
        notes = cmds.ls(type = 'file')
        for note in notes:
            cmds.select(note)
            textureMissing = SundayRenderSetTexturePathToProjectSet(note, textureMissing)
        
    
    if len(textureMissing) > 0:
        SundayDialogPy.SundayDialogConfirm('Textures not set to source images (missing)', str(textureMissing), 'OK')
    
    
    try:
        cmds.select(sel)
    except:
        cmds.select(clear = True)



def SundayRenderToolsChangeTextureResolutionSet(level, note):
    texFile = cmds.getAttr(note + '.fileTextureName')
    if texFile == '':
        print 'Empty/None file name in : ' + note
        return None
    stripFile = os.path.basename(texFile).split('_')
    stripPath = os.path.dirname(texFile)
    newTexFile = ''
    for i in range(len(stripFile) - 1):
        newTexFile = newTexFile + stripFile[i] + '_'
    
    newTexFile = newTexFile + str(level) + os.path.splitext(texFile)[1]
    newTexFile = stripPath + os.sep + newTexFile
    if os.path.isfile(newTexFile):
        cmds.setAttr(note + '.fileTextureName', newTexFile, type = 'string')
    else:
        print 'Texture not found : ' + newTexFile


def SundayRenderToolsChangeTextureResolution(object, level):
    sel = cmds.ls(selection = True)
    if object == 'selected':
        if len(sel) == 0:
            SundayDialogPy.SundayDialogConfirm('ERROR                       ', 'Nothing selected.', 'OK')
        else:
            cmds.hyperShade('', shaderNetworksSelectMaterialNodes = True)
            selShader = cmds.ls(selection = True)
            for curSelShader in selShader:
                notes = cmds.hyperShade(listUpstreamNodes = curSelShader)
                for note in notes:
                    if cmds.nodeType(note) == 'file' or cmds.nodeType(note) == 'psdFileTex':
                        cmds.select(note)
                        SundayRenderToolsChangeTextureResolutionSet(level, note)
                        continue
                
            
    elif object == 'global':
        notes = cmds.ls(type = 'file')
        for note in notes:
            cmds.select(note)
            SundayRenderToolsChangeTextureResolutionSet(level, note)
        
    
    
    try:
        cmds.select(sel)
    except:
        pass



def SundayRenderToolsTextureConvert():
    file = 'file2'
    obj = 'PalmTreeA_HeadShape'
    fileSizeX = cmds.getAttr(file + '.outSizeX')
    fileSizeY = cmds.getAttr(file + '.outSizeY')
    newfileName = os.path.basename(cmds.getAttr('file2.fileTextureName'))
    curTexFile = cmds.convertSolidTx(file, obj, fileImageName = newfileName + '_High.png', fileFormat = 'png', alpha = True, rx = fileSizeX, ry = fileSizeY)
    curTexFile = cmds.convertSolidTx(file, obj, fileImageName = newfileName + '_Medium.png', fileFormat = 'png', alpha = True, rx = fileSizeX / 2, ry = fileSizeY / 2)
    curTexFile = cmds.convertSolidTx(file, obj, fileImageName = newfileName + '_Low.png', fileFormat = 'png', alpha = True, rx = fileSizeX / 4, ry = fileSizeY / 4)
    print curTexFile


def SundayRenderToolsSave():
    SundayRenderToolsUIClose()


def SundayRenderToolsUI():
    global sundayRenderToolsUI
    SundayMayaGuiPath = mel.eval('getenv SundayGui;')
    sundayRenderToolsUI = cmds.loadUI(uiFile = SundayMayaGuiPath + 'SundayRenderTools.ui')
    cmds.showWindow(sundayRenderToolsUI)


def SundayRenderToolsUIClose():
    cmds.deleteUI(sundayRenderToolsUI)

