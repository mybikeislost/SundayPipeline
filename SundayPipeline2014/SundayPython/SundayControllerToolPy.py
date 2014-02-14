'''
*
*  SundayControllerToolPy.py
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

def SundayControllerToolApply(locatorType):
    joints = cmds.ls(selection = True)
    if len(joints) != 0:
        ctrls = []
        locatorUp = '0 0 0'
        if cmds.radioButton('ControllerDirectionXUpRadioButton', query = True, select = True):
            locatorUp = '90 0 0'
        
        if cmds.radioButton('ControllerDirectionYUpRadioButton', query = True, select = True):
            locatorUp = '0 90 0'
        
        if cmds.radioButton('ControllerDirectionZUpRadioButton', query = True, select = True):
            locatorUp = '0 0 90'
        
        for curJoint in joints:
            joint_grp = curJoint + '_GRP'
            joint_ctrl = curJoint + '_CTRL'
            ctrls.append(joint_ctrl)
            cmds.group(empty = True, name = joint_grp)
            if cmds.checkBox('CreateSDKGroupCheckBox', query = True, value = True):
                joint_sdk = curJoint + '_SDK'
                cmds.group(empty = True, name = joint_sdk)
                cmds.parent(joint_sdk, joint_grp)
                mel.eval(SundayLocatorToolPy.SundayLocatorToolGetLocator(joint_ctrl, locatorType, locatorUp))
                cmds.parent(joint_ctrl, joint_sdk)
            else:
                mel.eval(SundayLocatorToolPy.SundayLocatorToolGetLocator(joint_ctrl, locatorType, locatorUp))
                cmds.parent(joint_ctrl, joint_grp)
            print cmds.iconTextRadioCollection('ltColorCollection', query = True, select = True)
            cmds.setAttr(joint_ctrl + '.overrideEnabled', 1)
            cmds.setAttr(joint_ctrl + '.overrideColor', int(cmds.iconTextRadioCollection('ltColorCollection', query = True, select = True).split('_')[1]))
            cmds.select(curJoint, joint_grp)
            cmds.pointConstraint(name = joint_grp + '_tempJOINTPointConstraint')
            cmds.orientConstraint(name = joint_grp + '_tempJOINTOrientConstraint')
            cmds.delete(joint_grp + '_tempJOINTPointConstraint*')
            cmds.delete(joint_grp + '_tempJOINTOrientConstraint*')
            if cmds.checkBox('CreateConstraintCheckBox', query = True, value = True):
                cmds.parentConstraint(joint_ctrl, curJoint)
            
            if cmds.checkBox('CreateParentConstraintCheckBox', query = True, value = True):
                cmds.select(curJoint)
                cmds.pickWalk(direction = 'up')
                if cmds.ls(selection = True)[0] != curJoint:
                    cmds.select(joint_grp, add = True)
                    cmds.ParentConstraint()
                
            cmds.ls(selection = True)[0] != curJoint
        
        cmds.select(ctrls)
    else:
        SundayDialogPy.SundayDialogConfirm('Error                                        ', 'No joints selected', 'OK')


def SundayControllerToolUI():
    global sundayControllerToolUI
    SundayMayaGuiPath = mel.eval('getenv SundayGui;')
    
    try:
        if cmds.window(sundayControllerToolUI, exists = True):
            cmds.deleteUI(sundayControllerToolUI)
        
        sundayControllerToolUI = cmds.loadUI(uiFile = SundayMayaGuiPath + 'SundayControllerTool.ui')
    except:
        sundayControllerToolUI = cmds.loadUI(uiFile = SundayMayaGuiPath + 'SundayControllerTool.ui')

    cmds.setParent(sundayControllerToolUI)
    cmds.setParent(cmds.button('SundayControllerToolChooseColorDummyButtonToGrabParent', query = True, fullPathName = True, parent = True))
    cmds.iconTextRadioCollection('ltColorCollection')
    cmds.rowColumnLayout(numberOfColumns = 8)
    cmds.text(label = 'Color : ')
    cmds.iconTextRadioButton('DarkBlue_5', image1 = SundayImage + 'SundayColorDarkBlue.png', height = 20, width = 20, select = True)
    cmds.iconTextRadioButton('DarkRed_4', image1 = SundayImage + 'SundayColorDarkRed.png', height = 20, width = 20)
    cmds.iconTextRadioButton('Purple_9', image1 = SundayImage + 'SundayColorPurple.png', height = 20, width = 20)
    cmds.iconTextRadioButton('Red_13', image1 = SundayImage + 'SundayColorRed.png', height = 20, width = 20)
    cmds.iconTextRadioButton('Green_14', image1 = SundayImage + 'SundayColorGreen.png', height = 20, width = 20)
    cmds.iconTextRadioButton('LightBlue_18', image1 = SundayImage + 'SundayColorLightBlue.png', height = 20, width = 20)
    cmds.iconTextRadioButton('Yellow_17', image1 = SundayImage + 'SundayColorYellow.png', height = 20, width = 20)
    cmds.setParent(sundayControllerToolUI)
    cmds.setParent(cmds.button('SundayControllerToolDummyButtonToGrabParent', query = True, fullPathName = True, parent = True))
    cmds.scrollLayout(childResizable = True)
    cmds.rowColumnLayout(numberOfColumns = 8)
    SundayLocatorToolPy.SundayLocatorToolMakeLocatorButtonsInWidget('SundayControllerToolPy\nreload(SundayControllerToolPy)\nSundayControllerToolPy.SundayControllerToolApply')
    cmds.showWindow(sundayControllerToolUI)
    if platform.system() == 'Windows':
        cmds.window(sundayControllerToolUI, edit = True, topLeftCorner = [
            100,
            100])
    


def SundayControllerToolUIClose():
    cmds.deleteUI(sundayControllerToolUI)

