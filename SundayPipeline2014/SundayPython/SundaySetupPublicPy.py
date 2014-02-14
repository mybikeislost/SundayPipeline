import maya.cmds as cmds
import maya.mel as mel
import os
import sys
import string
import compiler
import platform
import time
import SundayUIToolsPy
import SundayInstallPipelinePublicPy
reload(SundayInstallPipelinePublicPy)
import SundayDialogPy
reload(SundayDialogPy)
import SundayHotkeyPy
reload(SundayHotkeyPy)
SundayImage = mel.eval('getenv SundayImage;')

def SundaySetupCreateMenuCall(mode):
    if cmds.popupMenu('CreateMenuMMLeft', query = True, exists = True):
        cmds.deleteUI('CreateMenuMMLeft')
    
    if cmds.popupMenu('CreateMenuMMMiddle', query = True, exists = True):
        cmds.deleteUI('CreateMenuMMMiddle')
    
    if mode == 0:
        return None
    cmds.popupMenu('CreateMenuMMLeft', button = 1, parent = 'viewPanes', markingMenu = True, allowOptionBoxes = True)
    cmds.menuItem(label = 'SUNDAY QUICK CREATE - LEFT', radialPosition = 'N', enable = False)
    cmds.menuItem(label = 'pSphere', command = 'import maya.mel as mel\nmel.eval("CreatePolygonSphere;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("CreatePolygonSphereOptions;")')
    cmds.menuItem(label = 'pCube', command = 'import maya.mel as mel\nmel.eval("CreatePolygonCube;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("CreatePolygonCubeOptions;")')
    cmds.menuItem(label = 'pCylinder', command = 'import maya.mel as mel\nmel.eval("CreatePolygonCylinder;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("CreatePolygonCylinderOptions;")')
    cmds.menuItem(label = 'pCone', command = 'import maya.mel as mel\nmel.eval("CreatePolygonCone;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("CreatePolygonConeOptions;")')
    cmds.menuItem(label = 'pPlane', command = 'import maya.mel as mel\nmel.eval("CreatePolygonPlane;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("CreatePolygonPlaneOptions;")')
    cmds.menuItem(label = 'pTorus', command = 'import maya.mel as mel\nmel.eval("CreatePolygonTorus;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("CreatePolygonTorusOptions;")')
    cmds.menuItem(label = 'pPyramid', command = 'import maya.mel as mel\nmel.eval("CreatePolygonPyramid;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("CreatePolygonPyramidOptions;")')
    cmds.menuItem(label = 'pPipe', command = 'import maya.mel as mel\nmel.eval("CreatePolygonPipe;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("CreatePolygonPipeOptions;")')
    cmds.menuItem(divider = True)
    cmds.menuItem(label = 'nSphere', command = 'import maya.mel as mel\nmel.eval("CreateNURBSSphere;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("CreateNURBSSphereOptions;")')
    cmds.menuItem(label = 'nCube', command = 'import maya.mel as mel\nmel.eval("CreateNURBSCube;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("CreateNURBSCubeOptions;")')
    cmds.menuItem(label = 'nCylinder', command = 'import maya.mel as mel\nmel.eval("CreateNURBSCylinder;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("CreateNURBSCylinderOptions;")')
    cmds.menuItem(label = 'nCone', command = 'import maya.mel as mel\nmel.eval("CreateNURBSCone;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("CreateNURBSConeOptions;")')
    cmds.menuItem(label = 'nPlane', command = 'import maya.mel as mel\nmel.eval("CreateNURBSPlane;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("CreateNURBSPlaneOptions;")')
    cmds.menuItem(label = 'nTorus', command = 'import maya.mel as mel\nmel.eval("CreateNURBSTorus;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("CreateNURBSTorusOptions;")')
    cmds.menuItem(divider = True)
    cmds.menuItem(label = 'nCircle', command = 'import maya.mel as mel\nmel.eval("CreateNURBSCircle;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("CreateNURBSCircleOptions;")')
    cmds.menuItem(label = 'CV Curve Tool', command = 'import maya.mel as mel\nmel.eval("CVCurveTool;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("CVCurveToolOptions;")')
    cmds.menuItem(label = 'Locator', command = 'import maya.mel as mel\nmel.eval("CreateLocator;")')
    cmds.menuItem(label = 'Text', command = 'import maya.mel as mel\nmel.eval("CreateTextOptions;")')
    cmds.menuItem(divider = True)
    cmds.menuItem(label = 'Ambient Light', command = 'import maya.mel as mel\nmel.eval("CreateAmbientLight;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("CreateAmbientLightOptions;")')
    cmds.menuItem(label = 'Directional Light   ', command = 'import maya.mel as mel\nmel.eval("CreateDirectionalLight;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("CreateDirectionalLightOptions;")')
    cmds.menuItem(label = 'Point Light', command = 'import maya.mel as mel\nmel.eval("CreatePointLight;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("CreatePointLightOptions;")')
    cmds.menuItem(label = 'Spot Light', command = 'import maya.mel as mel\nmel.eval("CreateSpotLight;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("CreateSpotLightOptions;")')
    cmds.menuItem(label = 'Area Light', command = 'import maya.mel as mel\nmel.eval("CreateAreaLight;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("CreateAreaLightOptions;")')
    cmds.menuItem(label = 'Volume Light', command = 'import maya.mel as mel\nmel.eval("CreateVolumeLight;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("CreateVolumeLightOptions;")')
    cmds.menuItem(divider = True)
    cmds.menuItem(label = 'Camera', command = 'import maya.mel as mel\nmel.eval("CreateCameraOnly;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("CreateCameraOnlyOptions")')
    cmds.menuItem(divider = True)
    cmds.menuItem(label = 'Joint', command = 'import maya.mel as mel\nmel.eval("JointTool;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("JointToolOptions;")')
    cmds.setParent('..')
    cmds.popupMenu('CreateMenuMMMiddle', button = 2, parent = 'viewPanes', markingMenu = True, allowOptionBoxes = True)
    cmds.menuItem(label = 'SUNDAY QUICK CREATE - MIDDLE', radialPosition = 'N', enable = False)
    cmds.menuItem(label = 'Blend Shape', command = 'import maya.mel as mel\nmel.eval("CreateBlendShape;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("CreateBlendShapeOptions;")')
    cmds.menuItem(label = 'Lattice', command = 'import maya.mel as mel\nmel.eval("CreateLattice;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("CreateLatticeOptions;")')
    cmds.menuItem(label = 'Cluster', command = 'import maya.mel as mel\nmel.eval("CreateCluster;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("CreateClusterOptions;")')
    cmds.menuItem(label = 'Soft Modification   ', command = 'import maya.mel as mel\nmel.eval("SoftModTool;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("SoftModToolOptions;")')
    cmds.menuItem(label = 'Sculp Deformer', command = 'import maya.mel as mel\nmel.eval("CreateSculptDeformer;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("CreateSculptDeformerOptions;")')
    cmds.menuItem(divider = True)
    cmds.menuItem(label = 'Bend Deformer', command = 'import maya.mel as mel\nmel.eval("Bend;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("BendOptions;")')
    cmds.menuItem(label = 'Flare Deformer', command = 'import maya.mel as mel\nmel.eval("Flare;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("FlareOptions;")')
    cmds.menuItem(label = 'Sine Deformer', command = 'import maya.mel as mel\nmel.eval("Sine;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("SineOptions;")')
    cmds.menuItem(label = 'Squash Deformer', command = 'import maya.mel as mel\nmel.eval("Squash;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("SquashOptions;")')
    cmds.menuItem(label = 'Twist Deformer', command = 'import maya.mel as mel\nmel.eval("Twist;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("TwistOptions;")')
    cmds.menuItem(label = 'Wave Deformer', command = 'import maya.mel as mel\nmel.eval("Wave;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("WaveOptions;")')
    cmds.menuItem(divider = True)
    cmds.menuItem(label = 'Emitter', command = 'import maya.mel as mel\nmel.eval("CreateEmitter;")')
    cmds.menuItem(optionBox = True, command = 'import maya.mel as mel\nmel.eval("CreateEmitterOptions;")')
    cmds.setParent('..')


def SundaySetupCreateMenu(mode):
    hotKey = str(cmds.optionVar(query = 'SundayQuickCreateHotKey'))
    if mode == 'marking_create':
        SundayHotkeyPy.SundayHotkeyWrapper('python', 'CreateMenuMM', hotKey, 'import SundaySetupPublicPy\\nreload(SundaySetupPublicPy)\\nSundaySetupPublicPy.SundaySetupCreateMenuCall(1)', 'import SundaySetupPublicPy\\nreload(SundaySetupPublicPy)\\nSundaySetupPublicPy.SundaySetupCreateMenuCall(0)', False, False, False)
    
    if mode == 'marking_remove':
        SundayHotkeyPy.SundayHotkeyWrapper('mel', 'CreateMenuMM', hotKey, '', '', False, False, False)
    


def SundaySetupMenu():
    gMainWindow = mel.eval('$temp1=$gMainWindow')
    if cmds.menu('sundayMenu', query = True, exists = True):
        cmds.deleteUI('sundayMenu', menu = True)
    
    sundayMenu = cmds.menu('sundayMenu', parent = gMainWindow, tearOff = True, label = 'Sunday')
    cmds.menuItem(parent = 'sundayMenu', label = 'Settings', command = 'import SundaySetupPublicPy\nreload(SundaySetupPublicPy)\nSundaySetupPublicPy.SundaySetupSettingsUI()')
    cmds.menuItem(parent = 'sundayMenu', label = ' SCENE ', divider = True)
    cmds.menuItem(parent = 'sundayMenu', label = 'Plus Save', command = 'import SundayPlusSavePy\nreload(SundayPlusSavePy)\nSundayPlusSavePy.SundayPlusSave()')
    cmds.menuItem(parent = 'sundayMenu', optionBox = True, command = 'import SundayPlusSavePy\nreload(SundayPlusSavePy)\nSundayPlusSavePy.SundayPlusSaveOptionsUI()')
    cmds.menuItem(parent = 'sundayMenu', label = 'Project', subMenu = True)
    cmds.menuItem(label = 'Set Project And Open Scene', command = 'import SundayProjectPy\nreload(SundayProjectPy)\nSundayProjectPy.SundayProjectOpenAndSetProject()')
    cmds.menuItem(label = 'Set Project From Scene', command = 'import SundayProjectPy\nreload(SundayProjectPy)\nSundayProjectPy.SundayProjectSetProjectFromScene()')
    cmds.menuItem(label = 'Reveal Project', command = 'import SundayProjectPy\nreload(SundayProjectPy)\nSundayProjectPy.SundayProjectRevealProject()')
    cmds.setParent('..')
    cmds.menuItem(parent = 'sundayMenu', label = ' ASSET ', divider = True)
    cmds.menuItem(parent = 'sundayMenu', label = 'Asset Export', command = 'import SundayAssetExportPy\nreload(SundayAssetExportPy)\nSundayAssetExportPy.SundayAssetExportOptionsUI()')
    cmds.menuItem(parent = 'sundayMenu', label = 'Warehouse Browser', command = 'import SundayWarehousePy\nreload(SundayWarehousePy)\nSundayWarehousePy.SundayWarehouseBrowserUI()')
    cmds.menuItem(parent = 'sundayMenu', optionBox = True, command = 'import SundayWarehousePy\nreload(SundayWarehousePy)\nSundayWarehousePy.SundayWarehouseBrowserDockedUI()')
    cmds.menuItem(parent = 'sundayMenu', label = 'Warehouse Create', command = 'import SundayWarehousePy\nreload(SundayWarehousePy)\nSundayWarehousePy.SundayWarehouseCreateUI()')
    cmds.menuItem(parent = 'sundayMenu', label = ' ANIMATION ', divider = True)
    cmds.menuItem(parent = 'sundayMenu', label = 'Locator Tool', command = 'import SundayLocatorToolPy\nreload(SundayLocatorToolPy)\nSundayLocatorToolPy.SundayLocatorToolUI()')
    cmds.menuItem(parent = 'sundayMenu', label = 'Controller Tool', command = 'import SundayControllerToolPy\nreload(SundayControllerToolPy)\nSundayControllerToolPy.SundayControllerToolUI()')
    cmds.menuItem(parent = 'sundayMenu', label = 'Between Tool', command = 'import SundayBetweenToolPy\nreload(SundayBetweenToolPy)\nSundayBetweenToolPy.SundayBetweenToolUI()')
    cmds.menuItem(parent = 'sundayMenu', label = ' GEOMETRY CACHE ', divider = True)
    cmds.menuItem(parent = 'sundayMenu', label = 'GeoCache Export', command = 'import SundayGeometryCachePy\nreload(SundayGeometryCachePy)\nSundayGeometryCachePy.SundayGeometryCacheExportUI()')
    cmds.menuItem(parent = 'sundayMenu', label = 'GeoCache Import', command = 'import SundayGeometryCachePy\nreload(SundayGeometryCachePy)\nSundayGeometryCachePy.SundayGeometryCacheImportUI()')
    cmds.menuItem(parent = 'sundayMenu', label = ' RENDERING ', divider = True)
    cmds.menuItem(parent = 'sundayMenu', label = 'Mental Ray', subMenu = True)
    cmds.menuItem(label = 'Contribution Pass Tool', command = 'import SundayRenderToolsPy\nreload(SundayRenderToolsPy)\nSundayRenderToolsPy.SundayRenderToolsCreateContributionUI()')
    cmds.setParent('..')
    cmds.menuItem(parent = 'sundayMenu', label = ' IMPORT/EXPORT ', divider = True)
    cmds.menuItem(parent = 'sundayMenu', label = 'Maya To After Effects', command = 'import SundayMayaToAEPy\nreload(SundayMayaToAEPy)\nSundayMayaToAEPy.SundayMayaToAEOptionsUI()')
    cmds.menuItem(parent = 'sundayMenu', label = ' HELP ', divider = True)
    cmds.menuItem(parent = 'sundayMenu', label = 'Sunday Pipeline Help', command = 'import maya\nmaya.cmds.showHelp( "http://www.3dg.dk/2011/08/12/sunday-pipeline-maya-public/", absolute=True  )')


def SundaySetupMenuRemove():
    if cmds.menu('sundayMenu', query = True, exists = True):
        cmds.deleteUI('sundayMenu', menu = True)
    


def SundaySetupCheckIntegrity():
    firstStart = False
    if cmds.optionVar(query = 'SundayUserName', exists = True) == 0:
        cmds.optionVar(stringValue = ('SundayUserName', 'NoUserSet'))
        firstStart = True
    
    if cmds.optionVar(query = 'SundayWarehousePath', exists = True) == 0:
        cmds.optionVar(stringValue = ('SundayWarehousePath', 'WarehousePathNotSet'))
        firstStart = True
    
    if cmds.optionVar(query = 'SundayColladaViewerPath', exists = True) == 0:
        cmds.optionVar(stringValue = ('SundayColladaViewerPath', 'SundayColladaViewerPath'))
        firstStart = True
    
    if firstStart == True:
        SundayDialogPy.SundayDialogConfirm('Sunday Pipeline Information                                          ', "This is the first time you run Sunday Pipeline or it's been updated.\n\nPlease check your settings to see if everything is ok!\n\nYou will see this box every time bigger changes has been made to the pipeline.", 'OK')
    


def SundaySetupSettingsDisableHotboxHotkey():
    if cmds.optionVar(query = 'SundayDisableHotbox'):
        SundayHotkeyPy.SundayHotkeyWrapper('mel', 'panePop', 'Space', 'panePop;', '', False, False, False)
    else:
        SundayHotkeyPy.SundayHotkeyWrapper('mel', 'hotBox', 'Space', 'hotBox;', 'hotBox -release', False, False, False)


def SundaySetupSettingsQuickCreateHotkey():
    if cmds.optionVar(query = 'SundayQuickCreate'):
        SundaySetupCreateMenu('marking_create')
    else:
        SundaySetupCreateMenu('marking_remove')


def SundaySetupSettingsSave():
    cmds.optionVar(stringValue = ('SundayUserName', cmds.textField('sundayUserNameLineEdit', query = True, text = True)))
    cmds.optionVar(stringValue = ('SundayColladaViewerPath', cmds.textField('sundayColladaViewerPathLineEdit', query = True, text = True)))
    SundayWarehousePath = cmds.textField('sundayWarehousePathLineEdit', query = True, text = True)
    if SundayWarehousePath != cmds.optionVar(query = 'SundayWarehousePath'):
        if not os.path.exists(SundayWarehousePath):
            SundayDialogPy.SundayDialogConfirm('Path Error                                           ', 'Warehouse Path does not exists.', 'OK')
            return None
        cmds.optionVar(stringValue = ('SundayWarehousePath', SundayWarehousePath.replace('\\', '/')))
    
    cmds.optionVar(intValue = ('SundayDisableHotbox', cmds.checkBox('sundayDisableHotboxCheckBox', query = True, value = True)))
    cmds.optionVar(intValue = ('SundayQuickCreate', cmds.checkBox('sundayQuickCreateCheckBox', query = True, value = True)))
    if cmds.checkBox('sundayQuickCreateCheckBox', query = True, value = True):
        if cmds.textField('sundayQuickCreateHotKeyLineEdit', query = True, text = True) != cmds.optionVar(query = 'SundayQuickCreateHotKey'):
            SundaySetupCreateMenu('marking_remove')
        
        SundaySetupSettingsQuickCreateHotkey()
    else:
        SundaySetupCreateMenu('marking_remove')
    cmds.optionVar(stringValue = ('SundayQuickCreateHotKey', cmds.textField('sundayQuickCreateHotKeyLineEdit', query = True, text = True)))
    SundaySetupSettingsDisableHotboxHotkey()
    SundaySetupSettingssUIClose()


def SundaySetupSettingsUI():
    global sundaySettingsUI
    SundayMayaGuiPath = mel.eval('getenv SundayGui;')
    
    try:
        if cmds.window(sundaySettingsUI, exists = True):
            cmds.deleteUI(sundaySettingsUI)
        
        sundaySettingsUI = cmds.loadUI(uiFile = SundayMayaGuiPath + 'SundaySettingsPublic.ui')
    except:
        sundaySettingsUI = cmds.loadUI(uiFile = SundayMayaGuiPath + 'SundaySettingsPublic.ui')

    cmds.textField('sundayUserNameLineEdit', edit = True, text = cmds.optionVar(query = 'SundayUserName'))
    if platform.system() == 'Windows':
        cmds.textField('sundayWarehousePathLineEdit', edit = True, text = cmds.optionVar(query = 'SundayWarehousePath').replace('/', '\\'))
    else:
        cmds.textField('sundayWarehousePathLineEdit', edit = True, text = cmds.optionVar(query = 'SundayWarehousePath'))
    cmds.textField('sundayColladaViewerPathLineEdit', edit = True, text = cmds.optionVar(query = 'SundayColladaViewerPath'))
    cmds.text('SundaySettingsPipelineVersionLabel', edit = True, label = str(SundayInstallPipelinePublicPy.SundayInstallPipelineVersion()))
    cmds.checkBox('sundayDisableHotboxCheckBox', edit = True, value = cmds.optionVar(query = 'SundayDisableHotbox'))
    cmds.checkBox('sundayQuickCreateCheckBox', edit = True, value = cmds.optionVar(query = 'SundayQuickCreate'))
    cmds.textField('sundayQuickCreateHotKeyLineEdit', edit = True, text = cmds.optionVar(query = 'SundayQuickCreateHotKey'))
    cmds.showWindow(sundaySettingsUI)
    if platform.system() == 'Windows':
        cmds.window(sundaySettingsUI, edit = True, topLeftCorner = [
            100,
            100])
    


def SundaySetupWarehousePathButton():
    filePath = cmds.fileDialog2(startingDirectory = os.sep, fileMode = 3)
    
    try:
        if platform.system() == 'Windows':
            exportPathEdit = cmds.textField('sundayWarehousePathLineEdit', edit = True, text = filePath[0].replace('/', '\\'))
        else:
            exportPathEdit = cmds.textField('sundayWarehousePathLineEdit', edit = True, text = filePath[0])
    except:
        pass



def SundaySetupSettingssUIClose():
    cmds.deleteUI(sundaySettingsUI)


def SundaySetupRunEveryTime():
    SundaySetupSettingsDisableHotboxHotkey()
    SundaySetupSettingsQuickCreateHotkey()


def SundaySetupLoad():
    SundayInstallPipelinePublicPy.SundayInstallPipelineCheckForUpdate('silent')
    SundaySetupMenu()
    reload(SundayUIToolsPy)
    
    try:
        SundayUIToolsPy.SundayUIToolsChannelBox()
    except:
        print 'Could not add Sunday Tools to ChannelBox'

    SundaySetupRunEveryTime()
    SundaySetupCheckIntegrity()


def SundaySetupUnLoad():
    SundaySetupMenuRemove()
    reload(SundayUIToolsPy)
    SundayUIToolsPy.SundayUIToolsChannelBoxUnload()
    SundaySetupRunEveryTime()

