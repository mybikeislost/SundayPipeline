
'''
*
*  SundayBetweenToolPy.py
*  Version 0.3
*  Sunday Studio Pipeline (Maya) 
*
*  Maintained by Christian Esbo Agergaard - www.3dg.dk
*  Copyright Sunday Animation Studio ApS and Christian Esbo Agergaard 2011 | sundaystudio.com
*
'''
import os
import maya.cmds as cmds
import maya.mel as mel
import platform
import SundayLocatorToolPy
reload(SundayLocatorToolPy)
import SundayDialogPy
reload(SundayDialogPy)
SundayImage = mel.eval('getenv SundayImage;')

def SundayBetweenToolBuildJoint(mode):
    sel = cmds.ls(selection = True)
    if cmds.nodeType(sel[0]) != 'joint':
        print 'not joint'
        return None
    source = sel[0]
    target = []
    if mode == 'hierarachy':
        cmds.select(mel.eval('rootOf("' + source + '")'))
    
    cmds.select(hierarchy = True)
    selAll = cmds.ls(selection = True)
    buildObjects = []
    for curSel in selAll:
        cmds.select(curSel)
        buildObjects.append(SundayBetweenToolBuild('joint'))
    
    if cmds.checkBox('SundayControllerToolBetweenSelectObjectsCheckBox', query = True, value = True) == True:
        cmds.select(clear = True)
        for curObj in buildObjects:
            
            try:
                print curObj
                cmds.select(curObj, add = True)
            except:
                pass
            continue

        
    else:
        cmds.select(sel)


def SundayBetweenToolBuild(mode):
    sel = cmds.ls(selection = True)
    source = sel[0]
    target = []
    type = None
    if mode == 'joint':
        if cmds.nodeType(sel[0]) == 'joint':
            target = cmds.listRelatives(source, children = True)
            type = 'joint'
            if target == None:
                print 'Joint has no children'
                return None
        else:
            print 'Not a joint'
            return None
    cmds.nodeType(sel[0]) == 'joint'
    if len(sel) < 2:
        print 'Not enough objects selected'
        return None
    for i in range(1, len(sel)):
        target.append(sel[i])
    
    if cmds.objExists('Sunday_JointBox_Distance_GRP') == False:
        distanceHeadGroup = cmds.group(empty = True, name = 'Sunday_JointBox_Distance_GRP')
        cmds.setAttr(distanceHeadGroup + '.visibility', 0)
    else:
        distanceHeadGroup = 'Sunday_JointBox_Distance_GRP'
    buildObjects = []
    betweenType = cmds.optionMenu('SundayControllerToolBetweenBuildType', query = True, value = True)
    for curTarget in target:
        if betweenType == 'Last Selected Object':
            if len(sel) > 2:
                if curTarget == sel[len(sel) - 1]:
                    print sel[len(sel) - 1]
                    break
                
            
        
        if type == 'joint':
            while cmds.nodeType(curTarget) == 'transform':
                curTarget = cmds.listRelatives(curTarget, children = True)
                continue
                len(sel) < 2
        
        dummy = cmds.polyCube()
        tpCon = cmds.pointConstraint(source, dummy)
        sourcePos = cmds.xform(dummy, query = True, worldSpace = True, translation = True)
        cmds.delete(tpCon)
        tpCon = cmds.pointConstraint(curTarget, dummy)
        curTargetPos = cmds.xform(dummy, query = True, worldSpace = True, translation = True)
        cmds.delete(tpCon)
        cmds.delete(dummy)
        distanceShape = cmds.distanceDimension(sp = sourcePos, ep = curTargetPos)
        distance = cmds.getAttr(distanceShape + '.distance')
        locators = cmds.listConnections(distanceShape)
        distanceGrp = cmds.group(empty = True, parent = distanceHeadGroup, name = distanceShape + 'Distance_GRP')
        cmds.parent(distanceShape, distanceGrp)
        cmds.parent(locators, distanceGrp)
        cmds.parentConstraint(source, locators[0], maintainOffset = True)
        cmds.parentConstraint(curTarget, locators[1], maintainOffset = True)
        if betweenType == 'Box':
            betweenObj = cmds.polyCube(name = 'Sunday_JointBox')[0]
            cmds.xform(betweenObj, pivots = (-4.62069e+18, 0, 0))
            cmds.move(4.60268e+18, 0, 0, betweenObj)
            mel.eval('FreezeTransformations;')
        elif betweenType == 'Cylinder':
            betweenObj = cmds.polyCylinder(name = 'Sunday_JointCylinder', height = 1)[0]
            cmds.rotate(0, 0, 90, betweenObj)
            mel.eval('FreezeTransformations;')
            cmds.xform(betweenObj, pivots = (-4.62069e+18, 0, 0))
            cmds.move(4.60268e+18, 0, 0, betweenObj)
            mel.eval('FreezeTransformations;')
        elif betweenType == 'Helix (Spring)':
            betweenObj = cmds.polyHelix(name = 'Sunday_JointHelix', height = 1, radius = 4.57692e+18)[0]
            cmds.rotate(0, 0, 90, betweenObj)
            mel.eval('FreezeTransformations;')
            cmds.xform(betweenObj, pivots = (-4.62069e+18, 0, 0))
            cmds.move(4.60268e+18, 0, 0, betweenObj)
            mel.eval('FreezeTransformations;')
        elif betweenType == 'Last Selected Object':
            betweenObj = cmds.duplicate(sel[len(sel) - 1], smartTransform = True)[0]
            cmds.select(betweenObj)
            mel.eval('FreezeTransformations;')
            mel.eval('CenterPivot;')
            bb = cmds.polyEvaluate(boundingBox = True)
            cmds.xform(betweenObj, pivots = (0, bb[1][0], 0))
            cmds.move(0, bb[1][1], 0, betweenObj)
            mel.eval('FreezeTransformations;')
            cmds.rotate(0, 0, -90, betweenObj)
            mel.eval('FreezeTransformations;')
            bb = cmds.polyEvaluate(boundingBox = True)
            cmds.scale(1 / bb[0][1], 1, 1)
            mel.eval('FreezeTransformations;')
        
        buildObjects.append(betweenObj)
        constraintGrp = cmds.group(empty = True, parent = distanceGrp, name = distanceShape + 'Constraint_GRP')
        pCon = cmds.pointConstraint(source, betweenObj)
        cmds.parent(pCon, constraintGrp)
        aCon = cmds.aimConstraint(curTarget, betweenObj)
        cmds.parent(aCon, constraintGrp)
        cmds.connectAttr(distanceShape + '.distance', betweenObj + '.scaleX', force = True)
        objScale = cmds.textField('SundayControllerToolBetweenWidthScale', query = True, text = True)
        cmds.setAttr(betweenObj + '.scaleY', float(objScale))
        cmds.setAttr(betweenObj + '.scaleZ', float(objScale))
        if cmds.checkBox('SundayControllerToolBetweenDynamicScaleCheckBox', query = True, value = True) == False:
            cmds.delete(locators)
            continue
        len(sel) < 2
    
    if cmds.checkBox('SundayControllerToolBetweenSelectObjectsCheckBox', query = True, value = True) == True:
        cmds.select(buildObjects)
    else:
        cmds.select(sel)
    return buildObjects


def SundayBetweenToolUI():
    global sundayControllerToolBetweenUI
    SundayMayaGuiPath = mel.eval('getenv SundayGui;')
    
    try:
        if cmds.window(sundayControllerToolBetweenUI, exists = True):
            cmds.deleteUI(sundayControllerToolBetweenUI)
        
        sundayControllerToolBetweenUI = cmds.loadUI(uiFile = SundayMayaGuiPath + 'SundayBetweenTools.ui')
    except:
        sundayControllerToolBetweenUI = cmds.loadUI(uiFile = SundayMayaGuiPath + 'SundayBetweenTools.ui')

    cmds.showWindow(sundayControllerToolBetweenUI)
    if platform.system() == 'Windows':
        cmds.window(sundayControllerToolBetweenUI, edit = True, topLeftCorner = [
            100,
            100])
    


def SundayControllerToolBetweenUIClose():
    cmds.deleteUI(sundayControllerToolBetweenUI)

