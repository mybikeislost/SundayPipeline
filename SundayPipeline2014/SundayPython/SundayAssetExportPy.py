'''
*
*  SUNAssetExport.py
*  Sunday Animation Studio "Asset Export" for AutoDesk Maya 
*  Version 2011.01b
*
*  Maintained by Christian Esbo Agergaard | cea@sundaystudio.com
*  Copyright Sunday Animation Studio ApS 2010 | sundaystudio.com
*
'''
import os
import shutil
import time
from time import gmtime, strftime
import subprocess
import platform
import maya.cmds as cmds
import maya.mel as mel
import SundayDialogPy
reload(SundayDialogPy)
import SundayGeometryCachePy
reload(SundayGeometryCachePy)

def SundayAssetExportOptionsRigAndGeoCheckBoxToggle():
    if cmds.radioButton('assetExportSelectedRadioButton', query = True, select = True):
        cmds.control('RigAndCacheGroupBox', edit = True, enable = True)
    else:
        cmds.control('RigAndCacheGroupBox', edit = True, enable = False)


def SundayAssetExportOptionsCurrentAssetDirectory():
    currentAssetPath = cmds.workspace(q = True, rootDirectory = True) + cmds.workspace(fileRuleEntry = 'templates') + os.sep
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


def SundayAssetExportOptions():
    currentAssetPath = cmds.workspace(q = True, rootDirectory = True) + cmds.workspace(fileRuleEntry = 'templates') + os.sep
    assetExportNameShort = cmds.textField('assetExportNameLineEdit', query = True, text = True) + '_Asset'
    assetExportName = currentAssetPath + assetExportNameShort
    if cmds.file(assetExportName + '.mb', query = True, ex = True) == True:
        if os.path.isdir(currentAssetPath + '_History') != True:
            os.mkdir(currentAssetPath + '_History')
        
        timeStamp = time.strftime('%a-%d-%b-%Y_%H-%M-%S', gmtime())
        shutil.move(assetExportName + '.mb', currentAssetPath + '_History' + os.sep + assetExportNameShort + '_' + timeStamp + '.mb')
    
    if cmds.radioButton('assetExportSelectedRadioButton', query = True, select = True):
        selectedAsset = cmds.ls(selection = True)
        if selectedAsset:
            conflict = SundayGeometryCachePy.SundayGeometryCacheExportPrePare()
            if len(conflict) > 0 and cmds.checkBox('assetExportRemoveHiddenObjects', query = True, enable = True):
                cmds.select(clear = True)
                sList = []
                for curObj in conflict:
                    for ccSel in cmds.ls(curObj, long = True):
                        cmds.select(ccSel, add = True)
                    
                
                SundayDialogPy.SundayDialogConfirm('Object Conflict.\nPlease correct/rename before exporting Geometry Cache Asset.\n\nAsset not exported.\n\nConflict objects are selected:', str(list(set(conflict))).replace("[u'", '').replace("', u'", ', ').replace("']", ''), 'OK')
                return None
            cmds.select(selectedAsset)
            cmds.file(assetExportName, op = 'v=0', typ = 'mayaBinary', es = True)
            if cmds.checkBox('assetExportRemoveHiddenObjects', query = True, enable = True):
                selected = cmds.ls(selection = True, long = True)
                tempGrp = cmds.group(name = selectedAsset[0] + '_GeoOnly', empty = True)
                cmds.select(selected)
                cmds.select(hierarchy = True)
                cmds.select(cmds.ls(selection = True, type = 'mesh'))
                cmds.pickWalk(direction = 'up')
                meshSel = cmds.ls(selection = True)
                for curSel in meshSel:
                    cmds.select(curSel)
                    cmds.select(hierarchy = True)
                    cmds.select(cmds.ls(selection = True, type = 'mesh'))
                    curShape = cmds.ls(selection = True)[0]
                    newSel = cmds.duplicate(curSel)
                    cmds.parent(newSel[0], tempGrp)
                    cmds.rename(newSel[0], curSel)
                    cmds.select(hierarchy = True)
                    cmds.select(cmds.ls(selection = True, type = 'mesh'))
                    cmds.rename(cmds.ls(selection = True)[0], curShape)
                
                cmds.select(tempGrp)
                cmds.select(hierarchy = True)
                newGrpSel = cmds.ls(selection = True)
                for curSel in newGrpSel:
                    
                    try:
                        cmds.setAttr(curSel + '.translateX', lock = False)
                        cmds.setAttr(curSel + '.translateY', lock = False)
                        cmds.setAttr(curSel + '.translateZ', lock = False)
                        cmds.setAttr(curSel + '.rotateX', lock = False)
                        cmds.setAttr(curSel + '.rotateY', lock = False)
                        cmds.setAttr(curSel + '.rotateZ', lock = False)
                        cmds.setAttr(curSel + '.scaleX', lock = False)
                        cmds.setAttr(curSel + '.scaleY', lock = False)
                        cmds.setAttr(curSel + '.scaleZ', lock = False)
                    except:
                		pass
                    continue

                
                visiGrp = cmds.group(name = 'HiddenObjects_GRP', empty = True, parent = tempGrp)
                cmds.setAttr(visiGrp + '.visibility', False)
                for curSel in newGrpSel:
                    
                    try:
                        if cmds.getAttr(curSel + '.visibility') == False:
                            cmds.setAttr(curSel + '.visibility', True)
                            cmds.parent(curSel, visiGrp)
                    except:
                		pass
                    continue

                
                if cmds.checkBox('assetExportRemoveHiddenObjects', query = True, value = True):
                    cmds.delete(visiGrp)
                
                cmds.select(tempGrp)
                cmds.select(hierarchy = True)
                cmds.delete(constraints = True)
                mel.eval('FreezeTransformations;')
                mel.eval('DeleteHistory;')
                for curSel in cmds.ls(selection = True, type = 'shape'):
                    cmds.select(cmds.listRelatives(curSel, parent = True, fullPath = True)[0])
                    
                    try:
                        cmds.addAttr(longName = 'SUNDAY_STUDIO', numberOfChildren = 1, attributeType = 'compound')
                    except:
                        pass

                    
                    try:
                        cmds.addAttr(longName = 'Geometry_Cache_Shape', dataType = 'string', parent = 'SUNDAY_STUDIO')
                    except:
                        pass

                    cmds.setAttr(cmds.ls(selection = True)[0] + '.Geometry_Cache_Shape', curSel.split('|')[len(curSel.split('|')) - 1], type = 'string')
                    cmds.setAttr(cmds.ls(selection = True)[0] + '.Geometry_Cache_Shape', lock = True)
                
                cmds.select(tempGrp)
                print '................'
                deleteObjects = []
                for curDel in selected:
                    deleteObjects.append(mel.eval('rootOf("' + curDel + '")'))
                
                
                try:
                    cmds.select(deleteObjects)
                    cmds.select(hierarchy = True)
                    cmds.lockNode(lock = False)
                    cmds.delete(deleteObjects)
                except:
                    SundayDialogPy.SundayDialogConfirm('Warning!                                                                                                                            ', 'Could not clean GeoOnly scene completely. The selected object could be locked and therefore not be removed for complete cleanup.\n\nCheck GeoOnly asset scene before using it.', 'OK')

                cmds.select(tempGrp)
                cmds.file(assetExportName + '_GeoOnly', op = 'v=0', typ = 'mayaBinary', es = True)
                cmds.undo()
                cmds.undo()
                cmds.delete(tempGrp)
                cmds.select(selectedAsset)
            
        else:
            SundayDialogPy.SundayDialogConfirm('Error                                        ', 'Nothing Selected', 'OK')
    else:
        cmds.file(assetExportName, op = 'v=0', typ = 'mayaBinary', ea = True)
    SundayAssetExportOptionsUIClose()


def SundayAssetExportOptionsUIClose():
    cmds.deleteUI(assetExportDialog)


def SundayAssetExportOptionsUI():
    global assetExportDialog
    SundayMayaGuiPath = mel.eval('getenv SundayGui;')
    assetExportDialog = cmds.loadUI(uiFile = SundayMayaGuiPath + 'SundayAssetExportOption.ui')
    sceneName = cmds.file(query = True, shn = True, sn = True)
    assetName = sceneName.split('_')
    cmds.textField('assetExportNameLineEdit', edit = True, text = assetName[0])
    cmds.radioButton('assetExportSelectedRadioButton', edit = True, changeCommand = 'SundayAssetExportPy.SundayAssetExportOptionsRigAndGeoCheckBoxToggle()')
    cmds.showWindow(assetExportDialog)
