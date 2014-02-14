'''
*
*  SundayMayaToAEPy.py
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

def SundayMayaToAEOptionsUICustomPath():
    filePath = cmds.fileDialog2(startingDirectory = '/', fileFilter = 'Maya Ascii (*.ma)')
    
    try:
        exportPathEdit = cmds.textField('exportPathEdit', edit = True, text = filePath[0])
    except:
        pass



def SundayMayaToAEOptions():
    print '-----------'
    sel = cmds.ls(selection = True)
    cam = []
    for curSel in sel:
        if cmds.listRelatives(curSel, type = 'camera') != None:
            cam.append(curSel)
            continue
    
    if len(cam) == 0:
        SundayDialogPy.SundayDialogConfirm('ERROR\n\nNo Camera Selected.                                                ', 'One Or More Cameras Will Be Exported If Selected.', 'OK')
        return None
    exportPathEdit = cmds.textField('exportPathEdit', query = True, text = True)
    startFrameEdit = cmds.textField('startFrameEdit', query = True, text = True)
    endFrameEdit = cmds.textField('endFrameEdit', query = True, text = True)
    locatorScaleEdit = float(cmds.textField('locatorScaleEdit', query = True, text = True))
    keyCamAttribute = cmds.checkBox('MayaToAEKeyCamAttribute', query = True, value = True)
    delUnknownNodes = cmds.checkBox('MayaToAEDeleteUknownNodes', query = True, value = True)
    cmds.group(em = True, name = 'MayaToAEGroup')
    aeCam = []
    for curCam in cam:
        MayaToAECam = curCam + '_MayaToAE'
        cmds.select(curCam)
        cmds.duplicate(n = MayaToAECam, st = True, upstreamNodes = True)
        cmds.setAttr(MayaToAECam + '.translateX', lock = False)
        cmds.setAttr(MayaToAECam + '.translateY', lock = False)
        cmds.setAttr(MayaToAECam + '.translateZ', lock = False)
        cmds.setAttr(MayaToAECam + '.rotateX', lock = False)
        cmds.setAttr(MayaToAECam + '.rotateY', lock = False)
        cmds.setAttr(MayaToAECam + '.rotateZ', lock = False)
        cmds.setAttr(MayaToAECam + '.scaleX', lock = False)
        cmds.setAttr(MayaToAECam + '.scaleY', lock = False)
        cmds.setAttr(MayaToAECam + '.scaleZ', lock = False)
        cmds.setAttr(MayaToAECam + '.visibility', lock = False)
        mel.eval('channelBoxCommand -break;')
        mel.eval('CBdeleteConnection "' + MayaToAECam + '.translateX";')
        mel.eval('CBdeleteConnection "' + MayaToAECam + '.translateY";')
        mel.eval('CBdeleteConnection "' + MayaToAECam + '.translateZ";')
        mel.eval('CBdeleteConnection "' + MayaToAECam + '.rotateX";')
        mel.eval('CBdeleteConnection "' + MayaToAECam + '.rotateY";')
        mel.eval('CBdeleteConnection "' + MayaToAECam + '.rotateZ";')
        mel.eval('CBdeleteConnection "' + MayaToAECam + '.scaleX";')
        mel.eval('CBdeleteConnection "' + MayaToAECam + '.scaleY";')
        mel.eval('CBdeleteConnection "' + MayaToAECam + '.scaleZ";')
        cmds.parent(MayaToAECam, 'MayaToAEGroup')
        cmds.parentConstraint(curCam, MayaToAECam)
        aeCam.append(MayaToAECam)
    
    cmds.parent(aeCam, world = True)
    loc = []
    aeLocString = '_MayaToAE_NULL'
    if cmds.radioButton('MayaToAENullRadioButton', query = True, select = True):
        
        try:
            cmds.select('*NULL*')
            loc = cmds.ls(selection = True, type = 'transform')
        except:
            len(cam) == 0
            print 'No NULL locators found'

        aeLocString = '_MayaToAE'
    elif cmds.radioButton('MayaToAESelectedRadioButton', query = True, select = True):
        for curSel in sel:
            if cmds.listRelatives(curSel, type = 'locator') != None:
                loc.append(curSel)
                continue
            len(cam) == 0
        
    else:
        loc = cmds.ls(type = 'locator')
    aeLoc = []
    for curLoc in loc:
        MayaToAENull = curLoc + aeLocString
        cmds.select(curLoc)
        cmds.duplicate(name = MayaToAENull, st = True)
        cmds.setAttr(MayaToAENull + '.translateX', lock = False)
        cmds.setAttr(MayaToAENull + '.translateY', lock = False)
        cmds.setAttr(MayaToAENull + '.translateZ', lock = False)
        cmds.setAttr(MayaToAENull + '.rotateX', lock = False)
        cmds.setAttr(MayaToAENull + '.rotateY', lock = False)
        cmds.setAttr(MayaToAENull + '.rotateZ', lock = False)
        cmds.setAttr(MayaToAENull + '.scaleX', locatorScaleEdit, lock = False)
        cmds.setAttr(MayaToAENull + '.scaleY', locatorScaleEdit, lock = False)
        cmds.setAttr(MayaToAENull + '.scaleZ', locatorScaleEdit, lock = False)
        cmds.parent(MayaToAENull, 'MayaToAEGroup')
        cmds.parentConstraint(curLoc, MayaToAENull)
        aeLoc.append(MayaToAENull)
    
    if len(loc) > 0:
        cmds.parent(aeLoc, world = True)
    
    toBake = aeCam + aeLoc
    cmds.bakeResults(toBake, simulation = True, t = (startFrameEdit, endFrameEdit), sb = 1, dic = True, pok = True, sac = False, ral = False, bol = False, cp = False, shape = True)
    cmds.delete('*_MayaToAE_parentConstraint*')
    cmds.delete('MayaToAEGroup')
    cmds.select(toBake)
    cmds.delete(sc = True, uac = False, hi = '', cp = 0, s = 1)
    if keyCamAttribute == True:
        for curCam in aeCam:
            cmds.setKeyframe(curCam + '.focalLength')
        
    
    uNodeDeleteUnfo = False
    if delUnknownNodes == True:
        uNodes = cmds.ls(type = 'unknown')
        if len(uNodes) > 0:
            cmds.delete(uNodes)
            uNodeDeleteUnfo = True
        
    
    
    try:
        cmds.file(exportPathEdit, force = True, op = 'v=0', typ = 'mayaAscii', es = True)
    except:
        SundayDialogPy.SundayDialogConfirm('ERROR\n\nThere maybe unknown nodes in the scene.             ', 'Try the export with "Delete Unknown Nodes and Undo" checked.', 'OK')

    if uNodeDeleteUnfo:
        cmds.undo()
    
    cmds.delete()
    
    try:
        cmds.select(sel)
    except:
        pass



def SundayMayaToAEOptionsUIClose():
    cmds.deleteUI(mayaToAEDialog)


def SundayMayaToAEOptionsUI():
    global mayaToAEOptionsUI
    SundayMayaGuiPath = mel.eval('getenv SundayGui;')
    
    try:
        if cmds.window(mayaToAEOptionsUI, exists = True):
            cmds.deleteUI(mayaToAEOptionsUI)
        
        mayaToAEOptionsUI = cmds.loadUI(uiFile = SundayMayaGuiPath + 'SundayMayaToAEOption.ui')
    except:
        mayaToAEOptionsUI = cmds.loadUI(uiFile = SundayMayaGuiPath + 'SundayMayaToAEOption.ui')

    cmds.textField('startFrameEdit', edit = True, text = cmds.playbackOptions(query = True, min = True))
    cmds.textField('endFrameEdit', edit = True, text = cmds.playbackOptions(query = True, max = True))
    cmds.textField('exportPathEdit', edit = True, text = os.path.dirname(cmds.file(query = True, sceneName = True)) + '/' + 'MayaToAE.ma')
    locatorScaleEdit = cmds.textField('locatorScaleEdit', edit = True, text = '0.001')
    cmds.showWindow(mayaToAEOptionsUI)
    if platform.system() == 'Windows':
        cmds.window(mayaToAEOptionsUI, edit = True, topLeftCorner = [
            100,
            100])
    
