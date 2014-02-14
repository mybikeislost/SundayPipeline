'''
*
*  SundayUIToolPy.py
*  Version 0.5
*  Sunday Studio Pipeline (Maya) 
*
*  Maintained by Christian Esbo Agergaard - www.3dg.dk
*  Copyright Sunday Animation Studio ApS and Christian Esbo Agergaard 2011 | sundaystudio.com
*
'''
import maya.cmds as cmds
import maya.mel as mel
import SundayDialogPy
reload(SundayDialogPy)
SundayImage = mel.eval('getenv SundayImage;')

try:
    pass
except NameError:
    SundayShaderlinerJobScriptJob = []


def SundayUIToolsDockedShaderlinerSwatchToggle():
    if cmds.optionVar(query = 'SundayShaderlinerSwatch'):
        cmds.optionVar(intValue = ('SundayShaderlinerSwatch', 0))
        cmds.iconTextButton('SundayShaderlinerIcon', edit = True, image = SundayImage + 'SundaySolidSphereColor.png')
    else:
        cmds.optionVar(intValue = ('SundayShaderlinerSwatch', 1))
        cmds.iconTextButton('SundayShaderlinerIcon', edit = True, image = SundayImage + 'SundaySolidSphere.png')
    SundayUIToolsDockedShaderlinerUpdate()


def SundayUIToolsDockedShaderlinerRename(curShader):
    newName = SundayDialogPy.SundayDialogPromptVariable('Shader Rename', 'Rename                                                     ', curShader)
    if newName != None:
        cmds.rename(curShader, newName)
        SundayUIToolsDockedShaderlinerUpdate()
    


def SundayUIToolsDockedShaderlinerInputOutputInHypershade(curShader):
    cmds.select(curShader)
    cmds.hyperShade(shaderNetwork = curShader)
    mel.eval('HypershadeWindow;')


def SundayUIToolsDockedShaderlinerUpdate():
    selected = cmds.ls(selection = True)
    if cmds.scrollLayout('sundayShaderlinerInTheDockScroll', query = True, exists = True):
        cmds.deleteUI('sundayShaderlinerInTheDockScroll')
    
    cmds.setParent(cmds.menuBarLayout('sundayShaderlinerInTheDockMenuBarLayout', query = True, fullPathName = True))
    sSParent = cmds.scrollLayout('sundayShaderlinerInTheDockScroll', childResizable = True)
    cmds.scriptJob(event = [
        'deleteAll',
        SundayUIToolsDockedShaderlinerKillJobs], parent = sSParent)
    cmds.hyperShade('', shaderNetworksSelectMaterialNodes = True)
    selShader = cmds.ls(selection = True)
    shaders = cmds.ls(materials = True)
    shaders.sort()
    isSwatch = cmds.optionVar(query = 'SundayShaderlinerSwatch')
    for curShader in shaders:
        isRef = cmds.referenceQuery(curShader, isNodeReferenced = True)
        if len(selShader) > 0:
            if selShader[0] == curShader:
                cmds.rowLayout(numberOfColumns = 3, height = 44, columnWidth3 = (40, 75, 108), adjustableColumn = 2, backgroundColor = [
                    4.60052e+18,
                    4.60052e+18,
                    4.60052e+18])
            else:
                cmds.rowLayout(numberOfColumns = 3, height = 44, columnWidth3 = (40, 75, 108), adjustableColumn = 2)
        else:
            cmds.rowLayout(numberOfColumns = 3, height = 44, columnWidth3 = (40, 75, 108), adjustableColumn = 2)
        cmds.popupMenu(button = 3, markingMenu = True)
        cmds.menuItem(enable = False, label = 'Input-Output Connection in Hypershade', command = 'import SundayUIToolsPy\nreload(SundayUIToolsPy)\nSundayUIToolsPy.SundayUIToolsDockedShaderlinerInputOutputInHypershade("' + curShader + '")')
        if isSwatch:
            cmds.swatchDisplayPort(sn = curShader, pressCommand = 'cmds.select("' + curShader + '")', widthHeight = [
                40,
                40], renderSize = 40)
        else:
            cmds.iconTextButton(image1 = SundayImage + 'SundaySolidSphere.png', command = 'cmds.select("' + curShader + '")', backgroundColor = [
                4.59637e+18,
                4.59637e+18,
                4.59637e+18], height = 40, width = 40)
        cmds.columnLayout()
        cmds.text(label = curShader)
        cmds.separator(height = 4)
        if isRef:
            cmds.text(label = 'Ref : ' + cmds.nodeType(curShader), font = 'tinyBoldLabelFont')
        else:
            cmds.text(label = cmds.nodeType(curShader), font = 'tinyBoldLabelFont')
        cmds.setParent('..')
        cmds.rowLayout(numberOfColumns = 2, adjustableColumn = 2)
        cmds.columnLayout()
        cmds.button(label = 'Apply', command = 'cmds.hyperShade(assign="' + curShader + '")', height = 19, width = 50)
        if curShader == 'lambert1' or curShader == 'particleCloud1':
            cmds.button(enable = False, label = 'Clone', command = 'cmds.select("' + curShader + '")\ncmds.duplicate( upstreamNodes=True )\nimport SundayUIToolsPy\nreload(SundayUIToolsPy)\nSundayUIToolsPy.SundayUIToolsDockedShaderlinerUpdate()', height = 19, width = 50)
        else:
            cmds.button(label = 'Clone', command = 'cmds.select("' + curShader + '")\ncmds.duplicate( upstreamNodes=True )\nimport SundayUIToolsPy\nreload(SundayUIToolsPy)\nSundayUIToolsPy.SundayUIToolsDockedShaderlinerUpdate()', height = 19, width = 50)
        cmds.setParent('..')
        if curShader == 'lambert1' and curShader == 'particleCloud1' or isRef:
            cmds.columnLayout(enable = False)
        else:
            cmds.columnLayout()
        cmds.button(label = 'Delete', command = 'cmds.select("' + curShader + '")\ncmds.delete()\nimport SundayUIToolsPy\nreload(SundayUIToolsPy)\nSundayUIToolsPy.SundayUIToolsDockedShaderlinerUpdate()', height = 19, width = 50)
        cmds.button(label = 'Rename', command = 'import SundayUIToolsPy\nreload(SundayUIToolsPy)\nSundayUIToolsPy.SundayUIToolsDockedShaderlinerRename("' + curShader + '")', height = 19, width = 50)
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.setParent('..')
        cmds.separator(style = 'in')
        SundayShaderlinerJobScriptJob.append(cmds.scriptJob(nodeNameChanged = [
            curShader,
            SundayUIToolsDockedShaderlinerKillJobs], runOnce = True, parent = sSParent))
        SundayShaderlinerJobScriptJob.append(cmds.scriptJob(nodeDeleted = [
            curShader,
            SundayUIToolsDockedShaderlinerKillJobs], runOnce = True, parent = sSParent))
    
    cmds.setParent('..')
    
    try:
        cmds.select(selected)
    except:
        pass



def SundayUIToolsDockedShaderlinerKillJobs():
    for curJS in SundayShaderlinerJobScriptJob:
        
        try:
            cmds.scriptJob(kill = curJS, force = True)
        except:
            pass
        continue

    
    del SundayShaderlinerJobScriptJob[:]
    SundayUIToolsDockedShaderlinerUpdate()


def SundayUIToolsDockedShaderliner():
    if cmds.dockControl('sundayShaderlinerInTheDock', query = True, exists = True):
        cmds.deleteUI('sundayShaderlinerInTheDock')
    
    shaderlinerlinerLayout = cmds.paneLayout('sundayShaderlinerInTheDockPane', parent = mel.eval('$temp1=$gMainWindow'))
    cmds.dockControl('sundayShaderlinerInTheDock', width = 275, area = 'left', label = 'Shaderliner', content = shaderlinerlinerLayout, allowedArea = [
        'right',
        'left'])
    cmds.setParent(cmds.paneLayout('sundayShaderlinerInTheDockPane', query = True, fullPathName = True))
    cmds.menuBarLayout('sundayShaderlinerInTheDockMenuBarLayout')
    cmds.flowLayout(columnSpacing = 5)
    cmds.separator(style = 'none', width = 1)
    cmds.iconTextButton(image = SundayImage + 'SundayRefresh.png', width = 28, height = 28, command = 'import SundayUIToolsPy\nreload(SundayUIToolsPy)\nSundayUIToolsPy.SundayUIToolsDockedShaderlinerUpdate()')
    if cmds.optionVar(query = 'SundayShaderlinerSwatch'):
        cmds.iconTextButton('SundayShaderlinerIcon', image = SundayImage + 'SundaySolidSphere.png', width = 30, height = 30, command = 'import SundayUIToolsPy\nreload(SundayUIToolsPy)\nSundayUIToolsPy.SundayUIToolsDockedShaderlinerSwatchToggle()')
    else:
        cmds.iconTextButton('SundayShaderlinerIcon', image = SundayImage + 'SundaySolidSphereColor.png', width = 30, height = 30, command = 'import SundayUIToolsPy\nreload(SundayUIToolsPy)\nSundayUIToolsPy.SundayUIToolsDockedShaderlinerSwatchToggle()')
    cmds.setParent('..')
    SundayUIToolsDockedShaderlinerUpdate()


def SundayUIToolsDockedOutliner():
    outlinerLayout = cmds.paneLayout(parent = mel.eval('$temp1=$gMainWindow'))
    if cmds.dockControl('sundayOutlinerInTheDock', exists = True):
        cmds.deleteUI('sundayOutlinerInTheDock')
    
    outlinerDock = cmds.dockControl('sundayOutlinerInTheDock', width = 275, area = 'left', label = 'Outliner', content = outlinerLayout, allowedArea = [
        'right',
        'left'])
    mel.eval('OutlinerWindow;')
    cmds.control('outlinerPanel1Window', edit = True, parent = outlinerLayout)


def SundayUIToolsChannelBoxCloseAttributeValue():
    print 'Clone Value ....................................'
    channelBox = mel.eval('global string $gChannelBoxName; $temp=$gChannelBoxName;')
    attr = cmds.channelBox(channelBox, query = True, selectedMainAttributes = True)
    obj = cmds.channelBox(channelBox, query = True, mainObjectList = True)
    sO = obj[0]
    for curAttr in attr:
        sOA = sO + '.' + curAttr
        curValue = cmds.getAttr(obj[0] + '.' + curAttr)
        for i in range(len(obj) - 1):
            
            try:
                cmds.setAttr(obj[i + 1] + '.' + curAttr, curValue)
            except:
                pass
            continue

        
    


def SundayUIToolsChannelBoxCloseAttributeName():
    print 'Clone Name ...................................'
    channelBox = mel.eval('global string $gChannelBoxName; $temp=$gChannelBoxName;')
    attr = cmds.channelBox(channelBox, query = True, selectedMainAttributes = True)
    obj = cmds.channelBox(channelBox, query = True, mainObjectList = True)
    sO = obj[0]
    for curAttr in attr:
        sOA = sO + '.' + curAttr
        for i in range(len(obj) - 1):
            compoundParent = cmds.attributeQuery(curAttr, node = sO, listParent = True)
            if compoundParent != None:
                
                try:
                    cmds.addAttr(longName = cmds.attributeQuery(compoundParent[0], node = sO, longName = True), shortName = cmds.attributeQuery(compoundParent[0], node = sO, shortName = True), niceName = cmds.attributeQuery(compoundParent[0], node = sO, niceName = True), attributeType = 'compound', numberOfChildren = cmds.attributeQuery(compoundParent[0], node = sO, numberOfChildren = True)[0])
                    for curCA in cmds.attributeQuery(compoundParent[0], node = sO, listChildren = True):
                        cmds.addAttr(longName = cmds.attributeQuery(curCA, node = sO, longName = True), shortName = cmds.attributeQuery(curCA, node = sO, shortName = True), niceName = cmds.attributeQuery(curCA, node = sO, niceName = True), attributeType = cmds.getAttr(sOA, type = True), parent = cmds.attributeQuery(compoundParent[0], node = sO, longName = True))
                    
                    for curCA in cmds.attributeQuery(compoundParent[0], node = sO, listChildren = True):
                        cmds.setAttr(obj[i + 1] + '.' + curCA, keyable = cmds.getAttr(sOA, keyable = True), lock = cmds.getAttr(sOA, lock = True), channelBox = cmds.getAttr(sOA, channelBox = True), caching = cmds.getAttr(sOA, caching = True))
                except:
                    pass

                continue
            if cmds.getAttr(sOA, type = True) == 'enum':
                
                try:
                    cmds.addAttr(longName = cmds.attributeQuery(curAttr, node = sO, longName = True), shortName = cmds.attributeQuery(curAttr, node = sO, shortName = True), niceName = cmds.attributeQuery(curAttr, node = sO, niceName = True), attributeType = cmds.getAttr(sOA, type = True), enumName = cmds.attributeQuery(curAttr, node = sO, listEnum = True)[0])
                    cmds.setAttr(obj[i + 1] + '.' + curAttr, keyable = cmds.getAttr(sOA, keyable = True), lock = cmds.getAttr(sOA, lock = True), channelBox = cmds.getAttr(sOA, channelBox = True), caching = cmds.getAttr(sOA, caching = True))
                except:
                    pass

                continue
            if cmds.attributeQuery(curAttr, node = sO, rangeExists = True):
                
                try:
                    cmds.addAttr(longName = cmds.attributeQuery(curAttr, node = sO, longName = True), shortName = cmds.attributeQuery(curAttr, node = sO, shortName = True), niceName = cmds.attributeQuery(curAttr, node = sO, niceName = True), attributeType = cmds.getAttr(sOA, type = True), minValue = cmds.attributeQuery(curAttr, node = sO, minimum = True)[0], maxValue = cmds.attributeQuery(curAttr, node = sO, maximum = True)[0])
                    cmds.setAttr(obj[i + 1] + '.' + curAttr, keyable = cmds.getAttr(sOA, keyable = True), lock = cmds.getAttr(sOA, lock = True), channelBox = cmds.getAttr(sOA, channelBox = True), caching = cmds.getAttr(sOA, caching = True))
                except:
                    pass

                continue
            
            try:
                cmds.addAttr(longName = cmds.attributeQuery(curAttr, node = sO, longName = True), shortName = cmds.attributeQuery(curAttr, node = sO, shortName = True), niceName = cmds.attributeQuery(curAttr, node = sO, niceName = True), attributeType = cmds.getAttr(sOA, type = True))
                cmds.setAttr(obj[i + 1] + '.' + curAttr, keyable = cmds.getAttr(sOA, keyable = True), lock = cmds.getAttr(sOA, lock = True), channelBox = cmds.getAttr(sOA, channelBox = True), caching = cmds.getAttr(sOA, caching = True))
            except:
                pass
            continue

        
    
    print 'Attributes cloned'


def SundayUIToolsChannelBox():
    channelBoxMenu = cmds.channelBox(mel.eval('$temp=$gChannelBoxName'), query = True, fullPathName = True) + '|popupMenu1'
    mel.eval('generateChannelMenu ' + channelBoxMenu + ' 1;')
    cmds.menuItem('SundayUiToolsChannelBoxScripts1', divider = True, parent = channelBoxMenu, enable = False)
    cmds.menuItem('SundayUiToolsChannelBoxScripts2', label = 'Sunday Studio ', parent = channelBoxMenu, enable = False)
    cmds.menuItem('SundayUiToolsChannelBoxCloneAttributeValue', label = 'Clone Attributes Value to Selected', parent = channelBoxMenu, command = 'import SundayUIToolsPy\nreload(SundayUIToolsPy)\nSundayUIToolsPy.SundayUIToolsChannelBoxCloseAttributeValue()')
    cmds.menuItem('SundayUiToolsChannelBoxCloneAttributeName', label = 'Clone Attributes Name to Selected', parent = channelBoxMenu, command = 'import SundayUIToolsPy\nreload(SundayUIToolsPy)\nSundayUIToolsPy.SundayUIToolsChannelBoxCloseAttributeName()')
    cmds.menuItem('SundayUiToolsChannelBoxMoveAttributeDown', label = 'Move Attribute to Bottom', parent = channelBoxMenu, command = 'import maya.mel\nmaya.mel.eval("channelBoxCommand -deleteAttributes; undo;")')


def SundayUIToolsChannelBoxUnload():
    cmds.deleteUI('SundayUiToolsChannelBoxScripts1')
    cmds.deleteUI('SundayUiToolsChannelBoxScripts2')
    cmds.deleteUI('SundayUiToolsChannelBoxCloneAttributeValue')
    cmds.deleteUI('SundayUiToolsChannelBoxCloneAttributeName')
    cmds.deleteUI('SundayUiToolsChannelBoxMoveAttributeDown')


def SundayUIToolsRenderLayers():
    renderLayerMenu = 'MayaWindow|MainChannelsLayersLayout|ChannelsLayersPaneLayout|LayerEditorForm|DisplayLayerUITabLayout|RenderLayerTab|menu8'
    mel.eval('layerEditorBuildRenderLayerMenu("MayaWindow|MainChannelsLayersLayout|ChannelsLayersPaneLayout|LayerEditorForm|DisplayLayerUITabLayout|RenderLayerTab|menu8", "RenderLayerTab");')
    cmds.menuItem('SundayUiToolsRenderLayers1', parent = renderLayerMenu, divider = True)
    cmds.menuItem('SundayUiToolsRenderLayers2', label = 'Sunday', parent = renderLayerMenu, enable = False)
    cmds.menuItem('SundayUiToolsRenderLayersImport', label = 'Import Render Layer (beta)', command = 'import SundayRenderToolsPy\nreload(SundayRenderToolsPy)\nSundayRenderToolsPy.SundayRenderToolsImportRenderLayer()', parent = renderLayerMenu)
    cmds.menuItem('SundayUiToolsRenderLayersExport', label = 'Export Render Layer (beta)', command = 'import SundayRenderToolsPy\nreload(SundayRenderToolsPy)\nSundayRenderToolsPy.SundayRenderToolsExportRenderLayer()', parent = renderLayerMenu)


def SundayUIToolsRenderLayersUnload():
    cmds.deleteUI('SundayUiToolsRenderLayers1')
    cmds.deleteUI('SundayUiToolsRenderLayers2')
    cmds.deleteUI('SundayUiToolsRenderLayersImport')
    cmds.deleteUI('SundayUiToolsRenderLayersExport')

