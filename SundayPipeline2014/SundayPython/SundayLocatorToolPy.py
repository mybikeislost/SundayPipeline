'''
*
*  SundayLocatorToolPy.py
*  Version 0.3
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
import SundayLocatorToolPy
reload(SundayLocatorToolPy)
import SundayDialogPy
reload(SundayDialogPy)
SundayImage = mel.eval('getenv SundayImage;')

def SundayLocatorToolGetLocator(locatorName, locatorType, locatorUp):
    if locatorType == 'null':
        locatorReturn = '\t\t\t\t\t\t$locator = `createNode transform -name "' + locatorName + '"`;\n\t\t\t\t\t\tselect $locator;\n\t\t\t\t\t\t'
    elif locatorType == 'circle':
        locatorReturn = '\t\t\t\t\t\t$locator = `createNode transform -name "' + locatorName + '"`;\n\t\t\t\t\t\t\tsetAttr ".ra" -type "double3" ' + locatorUp + ';\n\t\t\t\t\t\tcreateNode nurbsCurve -parent $locator;\n\t\t\t\t\t\t\tsetAttr -k off ".v";\n\t\t\t\t\t\t\tsetAttr ".cc" -type "nurbsCurve" \n\t\t\t\t\t\t\t3 8 2 no 3\n\t\t\t\t\t\t\t13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\n\t\t\t\t\t\t\t11\n\t\t\t\t\t\t\t0.78361162489122504 4.7982373409884682e-17 -0.78361162489122382\n\t\t\t\t\t\t\t-1.2643170607829326e-16 6.7857323231109134e-17 -1.1081941875543879\n\t\t\t\t\t\t\t-0.78361162489122427 4.7982373409884713e-17 -0.78361162489122427\n\t\t\t\t\t\t\t-1.1081941875543879 1.9663354616187859e-32 -3.2112695072372299e-16\n\t\t\t\t\t\t\t-0.78361162489122449 -4.7982373409884694e-17 0.78361162489122405\n\t\t\t\t\t\t\t-3.3392053635905195e-16 -6.7857323231109146e-17 1.1081941875543881\n\t\t\t\t\t\t\t0.78361162489122382 -4.7982373409884719e-17 0.78361162489122438\n\t\t\t\t\t\t\t1.1081941875543879 -3.6446300679047921e-32 5.9521325992805852e-16\n\t\t\t\t\t\t\t0.78361162489122504 4.7982373409884682e-17 -0.78361162489122382\n\t\t\t\t\t\t\t-1.2643170607829326e-16 6.7857323231109134e-17 -1.1081941875543879\n\t\t\t\t\t\t\t-0.78361162489122427 4.7982373409884713e-17 -0.78361162489122427\n\t\t\t\t\t\t\t;\n\t\t\t\t\t\tselect $locator;\n\t\t\t\t\t\t'
    elif locatorType == 'square':
        locatorReturn = '\t\t\t\t\t\t$locator = `createNode transform -name "' + locatorName + '"`;\n\t\t\t\t\t\t\tsetAttr ".ra" -type "double3" ' + locatorUp + ';\n\t\t\t\t\t\tcreateNode nurbsCurve -parent $locator;\n\t\t\t\t\t\t\tsetAttr -k off ".v";\n\t\t\t\t\t\t\tsetAttr ".cc" -type "nurbsCurve" \n\t\t\t\t\t\t\t1 4 0 no 3\n\t\t\t\t\t\t\t5 0 1 2 3 4\n\t\t\t\t\t\t\t5\n\t\t\t\t\t\t\t1 0 1\n\t\t\t\t\t\t\t-1 0 1\n\t\t\t\t\t\t\t-1 0 -1\n\t\t\t\t\t\t\t1 0 -1\n\t\t\t\t\t\t\t1 0 1\n\t\t\t\t\t\t\t;\n\t\t\t\t\t\tselect $locator;\n\t\t\t\t\t\t'
    elif locatorType == 'rectangle':
        locatorReturn = '\t\t\t\t\t\t$locator = `createNode transform -name "' + locatorName + '"`;\n\t\t\t\t\t\t\tsetAttr ".ra" -type "double3" ' + locatorUp + ';\n\t\t\t\t\t\tcreateNode nurbsCurve -parent $locator;\n\t\t\t\t\t\t\tsetAttr -k off ".v";\n\t\t\t\t\t\t\tsetAttr ".cc" -type "nurbsCurve" \n\t\t\t\t\t\t\t1 3 0 no 3\n\t\t\t\t\t\t\t4 0 1 2 3\n\t\t\t\t\t\t\t4\n\t\t\t\t\t\t\t0 0 1\n\t\t\t\t\t\t\t-1 0 -1\n\t\t\t\t\t\t\t1 0 -1\n\t\t\t\t\t\t\t0 0 1\n\t\t\t\t\t\t\t;\n\t\t\t\t\t\tselect $locator;\n\t\t\t\t\t\t'
    elif locatorType == '3dcross':
        locatorReturn = '\t\t\t\t\t\t$locator = `createNode transform -name "' + locatorName + '"`;\n\t\t\t\t\t\tcreateNode nurbsCurve -parent $locator;\n\t\t\t\t\t\t\tsetAttr -k off ".v";\n\t\t\t\t\t\t\tsetAttr ".cc" -type "nurbsCurve" \n\t\t\t\t\t\t\t\t1 2 0 no 3\n\t\t\t\t\t\t\t\t3 0 1 2\n\t\t\t\t\t\t\t\t3\n\t\t\t\t\t\t\t\t0 0 1\n\t\t\t\t\t\t\t\t0 0 0\n\t\t\t\t\t\t\t\t0 0 -1\n\t\t\t\t\t\t\t\t;\n\t\t\t\t\t\tcreateNode nurbsCurve -parent $locator;\n\t\t\t\t\t\t\tsetAttr -k off ".v";\n\t\t\t\t\t\t\tsetAttr ".cc" -type "nurbsCurve" \n\t\t\t\t\t\t\t\t1 2 0 no 3\n\t\t\t\t\t\t\t\t3 0 1 2\n\t\t\t\t\t\t\t\t3\n\t\t\t\t\t\t\t\t1 0 0\n\t\t\t\t\t\t\t\t0 0 0\n\t\t\t\t\t\t\t\t-1 0 0\n\t\t\t\t\t\t\t\t;\n\t\t\t\t\t\tcreateNode nurbsCurve -parent $locator;\n\t\t\t\t\t\t\tsetAttr -k off ".v";\n\t\t\t\t\t\t\tsetAttr ".cc" -type "nurbsCurve" \n\t\t\t\t\t\t\t\t1 2 0 no 3\n\t\t\t\t\t\t\t\t3 0 1 2\n\t\t\t\t\t\t\t\t3\n\t\t\t\t\t\t\t\t0 -1 0\n\t\t\t\t\t\t\t\t0 0 0\n\t\t\t\t\t\t\t\t0 1 0\n\t\t\t\t\t\t\t\t;\n\t\t\t\t\t\tselect $locator;\n\t\t\t\t\t\t'
    elif locatorType == 'cube':
        locatorReturn = '\t\t\t\t\t\t$locator = `createNode transform -name "' + locatorName + '"`;\n\t\t\t\t\t\tcreateNode nurbsCurve -parent $locator;\n\t\t\t\t\t\t\tsetAttr -k off ".v";\n\t\t\t\t\t\t\tsetAttr ".cc" -type "nurbsCurve" \n\t\t\t\t\t\t\t\t1 4 0 no 3\n\t\t\t\t\t\t\t\t5 0 1 2 3 4\n\t\t\t\t\t\t\t\t5\n\t\t\t\t\t\t\t\t1.0000000000000002 -1 -0.99999999999999978\n\t\t\t\t\t\t\t\t0.99999999999999978 -1 1.0000000000000002\n\t\t\t\t\t\t\t\t-1.0000000000000002 -1 0.99999999999999978\n\t\t\t\t\t\t\t\t-0.99999999999999978 -1 -1.0000000000000002\n\t\t\t\t\t\t\t\t1.0000000000000002 -1 -0.99999999999999978\n\t\t\t\t\t\t\t;\n\t\t\t\t\t\tcreateNode nurbsCurve -parent $locator;\n\t\t\t\t\t\t\tsetAttr -k off ".v";\n\t\t\t\t\t\t\tsetAttr ".cc" -type "nurbsCurve" \n\t\t\t\t\t\t\t\t1 4 0 no 3\n\t\t\t\t\t\t\t\t5 0 1 2 3 4\n\t\t\t\t\t\t\t\t5\n\t\t\t\t\t\t\t\t1.0000000000000002 1 -0.99999999999999978\n\t\t\t\t\t\t\t\t0.99999999999999978 1 1.0000000000000002\n\t\t\t\t\t\t\t\t-1.0000000000000002 1 0.99999999999999978\n\t\t\t\t\t\t\t\t-0.99999999999999978 1 -1.0000000000000002\n\t\t\t\t\t\t\t\t1.0000000000000002 1 -0.99999999999999978\n\t\t\t\t\t\t\t;\n\t\t\t\t\t\tcreateNode nurbsCurve -parent $locator;\n\t\t\t\t\t\t\tsetAttr -k off ".v";\n\t\t\t\t\t\t\tsetAttr ".cc" -type "nurbsCurve" \n\t\t\t\t\t\t\t\t1 4 0 no 3\n\t\t\t\t\t\t\t\t5 0 1 2 3 4\n\t\t\t\t\t\t\t\t5\n\t\t\t\t\t\t\t\t1.0000000000000002 0.99999999999999978 1.0000000000000007\n\t\t\t\t\t\t\t\t0.99999999999999978 -1.0000000000000002 1.0000000000000011\n\t\t\t\t\t\t\t\t-1.0000000000000002 -0.99999999999999978 1.0000000000000011\n\t\t\t\t\t\t\t\t-0.99999999999999978 1.0000000000000002 1.0000000000000007\n\t\t\t\t\t\t\t\t1.0000000000000002 0.99999999999999978 1.0000000000000007\n\t\t\t\t\t\t\t;\n\t\t\t\t\t\tcreateNode nurbsCurve -parent $locator;\n\t\t\t\t\t\t\tsetAttr -k off ".v";\n\t\t\t\t\t\t\tsetAttr ".cc" -type "nurbsCurve" \n\t\t\t\t\t\t\t\t1 4 0 no 3\n\t\t\t\t\t\t\t\t5 0 1 2 3 4\n\t\t\t\t\t\t\t\t5\n\t\t\t\t\t\t\t\t1.0000000000000002 0.99999999999999978 -1.0000000000000011\n\t\t\t\t\t\t\t\t0.99999999999999978 -1.0000000000000002 -1.0000000000000007\n\t\t\t\t\t\t\t\t-1.0000000000000002 -0.99999999999999978 -1.0000000000000007\n\t\t\t\t\t\t\t\t-0.99999999999999978 1.0000000000000002 -1.0000000000000011\n\t\t\t\t\t\t\t\t1.0000000000000002 0.99999999999999978 -1.0000000000000011\n\t\t\t\t\t\t\t;\n\t\t\t\t\t\tselect $locator;\n\t\t\t\t\t\t'
    elif locatorType == 'sphere':
        locatorReturn = '\t\t\t\t\t\t$locator = `createNode transform -name "' + locatorName + '"`;\n\t\t\t\t\t\tcreateNode nurbsCurve -parent $locator;\n\t\t\t\t\t\t\tsetAttr -k off ".v";\n\t\t\t\t\t\t\tsetAttr ".cc" -type "nurbsCurve" \n\t\t3 8 2 no 3\n\t\t13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\n\t\t11\n\t\t0 0.78361162489122504 -0.78361162489122393\n\t\t0 -1.2643170607829324e-16 -1.1081941875543881\n\t\t0 -0.78361162489122427 -0.78361162489122438\n\t\t0 -1.1081941875543879 -4.3214925318623865e-16\n\t\t0 -0.78361162489122449 0.78361162489122393\n\t\t0 -3.3392053635905195e-16 1.1081941875543881\n\t\t0 0.78361162489122382 0.78361162489122427\n\t\t0 1.1081941875543879 4.8419095746554286e-16\n\t\t0 0.78361162489122504 -0.78361162489122393\n\t\t0 -1.2643170607829324e-16 -1.1081941875543881\n\t\t0 -0.78361162489122427 -0.78361162489122438\n\t\t;\n\t\t\t\t\t\tcreateNode nurbsCurve -parent $locator;\n\t\t\t\t\t\t\tsetAttr -k off ".v";\n\t\t\t\t\t\t\tsetAttr ".cc" -type "nurbsCurve" \n\t\t3 8 2 no 3\n\t\t13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\n\t\t11\n\t\t0.78361162489122549 4.7982373409884701e-17 -0.78361162489122393\n\t\t0 6.7857323231109159e-17 -1.1081941875543881\n\t\t-0.78361162489122549 4.7982373409884731e-17 -0.78361162489122438\n\t\t-1.108194187554389 1.9663354616187867e-32 -4.3214925318623865e-16\n\t\t-0.78361162489122549 -4.7982373409884713e-17 0.78361162489122393\n\t\t0 -6.7857323231109171e-17 1.1081941875543881\n\t\t0.78361162489122371 -4.7982373409884738e-17 0.78361162489122427\n\t\t1.108194187554389 -3.6446300679047938e-32 4.8419095746554286e-16\n\t\t0.78361162489122549 4.7982373409884701e-17 -0.78361162489122393\n\t\t0 6.7857323231109159e-17 -1.1081941875543881\n\t\t-0.78361162489122549 4.7982373409884731e-17 -0.78361162489122438\n\t\t;\n\t\t\t\t\t\tcreateNode nurbsCurve -parent $locator;\n\t\t\t\t\t\t\tsetAttr -k off ".v";\n\t\t\t\t\t\t\tsetAttr ".cc" -type "nurbsCurve" \n\t\t3 8 2 no 3\n\t\t13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\n\t\t11\n\t\t-0.78361162489122549 0.78361162489122538 -4.110333963798983e-16\n\t\t-1.108194187554389 3.6570537503316709e-16 -5.3530206034286682e-16\n\t\t-0.78361162489122727 -0.78361162489122393 -4.1103339637989845e-16\n\t\t-1.7763568394002505e-15 -1.1081941875543879 -1.1102230246251578e-16\n\t\t0.78361162489122194 -0.78361162489122482 1.8898879145486709e-16\n\t\t1.1081941875543873 -8.2605761747051237e-16 3.1325745541783561e-16\n\t\t0.78361162489122371 0.78361162489122349 1.8898879145486719e-16\n\t\t0 1.1081941875543879 -1.1102230246251543e-16\n\t\t-0.78361162489122549 0.78361162489122538 -4.110333963798983e-16\n\t\t-1.108194187554389 3.6570537503316709e-16 -5.3530206034286682e-16\n\t\t-0.78361162489122727 -0.78361162489122393 -4.1103339637989845e-16\n\t\t;\n\t\t\t\t\t\tselect $locator;\n\t\t\t\t\t\t'
    elif locatorType == 'star':
        locatorReturn = '\t\t\t\t\t\t$locator = `createNode transform -name "' + locatorName + '"`;\n\t\t\t\t\t\tcreateNode nurbsCurve -parent $locator;\n\t\t\t\t\t\t\tsetAttr -k off ".v";\n\t\t\t\t\t\t\tsetAttr ".cc" -type "nurbsCurve" \n\t\t3 8 2 no 3\n\t\t13 -2 -1 0 1 2 3 4 5 6 7 8 9 10\n\t\t11\n\t\t-0.13101108041334086 8.0221150140516729e-18 -0.13101108041334059\n\t\t-1.2905414429197926 7.9022872361936499e-17 -1.3932241725035234e-16\n\t\t-0.13101108041334086 8.0221150140516806e-18 0.13101108041333998\n\t\t0 2.2898851414317867e-32 1.2905414429197923\n\t\t0.13101108041334086 -8.0221150140516776e-18 0.13101108041334003\n\t\t1.2905414429197926 -7.9022872361936523e-17 6.7542308794376924e-16\n\t\t0.13101108041334086 -8.0221150140516822e-18 -0.13101108041334025\n\t\t1.7763568394002505e-15 -4.2443338898236819e-32 -1.2905414429197923\n\t\t-0.13101108041334086 8.0221150140516729e-18 -0.13101108041334059\n\t\t-1.2905414429197926 7.9022872361936499e-17 -1.3932241725035234e-16\n\t\t-0.13101108041334086 8.0221150140516806e-18 0.13101108041333998\n\t\t;\n\t\t\t\t\t\tselect $locator;\n\t\t\t\t\t\t'
    
    return locatorReturn


def SundayLocatorToolMakeLocatorButtonsInWidget(buttonCommand):
    cmds.iconTextButton(image1 = SundayImage + 'SundayTextNull.png', label = '', height = 50, width = 50, command = buttonCommand + '("null")')
    cmds.iconTextButton(image1 = SundayImage + 'SundayCircle.png', label = '', height = 50, width = 50, command = buttonCommand + '("circle")')
    cmds.iconTextButton(image1 = SundayImage + 'SundaySquare.png', label = '', height = 50, width = 50, command = buttonCommand + '("square")')
    cmds.iconTextButton(image1 = SundayImage + 'SundayRectangle.png', label = '', height = 50, width = 50, command = buttonCommand + '("rectangle")')
    cmds.iconTextButton(image1 = SundayImage + 'SundayCross.png', label = '', height = 50, width = 50, command = buttonCommand + '("3dcross")')
    cmds.iconTextButton(image1 = SundayImage + 'SundayCube.png', label = '', height = 50, width = 50, command = buttonCommand + '("cube")')
    cmds.iconTextButton(image1 = SundayImage + 'SundaySphereLocator.png', label = '', height = 50, width = 50, command = buttonCommand + '("sphere")')
    cmds.iconTextButton(image1 = SundayImage + 'SundayStarLocator.png', label = '', height = 50, width = 50, command = buttonCommand + '("star")')


def SundayLocatorToolMoveSelectedToLocator(locators, objects):
    
    try:
        selection = cmds.ls(selection = True)
        for i in range(0, len(objects)):
            objParent = cmds.listRelatives(objects[i], parent = True, fullPath = True)
            if objParent == None:
                pass
            1
            cmds.parent(locators[i], objParent)
            cmds.parent(objects[i], locators[i])
        
        if len(selection) != 0:
            cmds.select(selection)
        else:
            cmds.select(clear = True)
    except:
        pass



def SundayLocatorToolCreate(locatorType):
    objects = cmds.ls(selection = True)
    locators = []
    locatorUp = '0 0 0'
    if cmds.radioButton('LocatorDirectionXUpRadioButton', query = True, select = True):
        locatorUp = '0 0 90'
    
    if cmds.radioButton('LocatorDirectionYUpRadioButton', query = True, select = True):
        locatorUp = '0 90 0'
    
    if cmds.radioButton('LocatorDirectionZUpRadioButton', query = True, select = True):
        locatorUp = '90 0 0'
    
    if cmds.checkBox('SundayLocatorToolMakeControllerForSelectedCheckBox', query = True, value = True):
        if len(objects) != 0:
            for curObj in objects:
                mel.eval(SundayLocatorToolPy.SundayLocatorToolGetLocator(curObj + '_CTRL', locatorType, locatorUp))
                curLocator = cmds.ls(selection = True)[0]
                locators.append(curLocator)
                cmds.setAttr(curLocator + '.overrideEnabled', 1)
                cmds.setAttr(curLocator + '.overrideColor', int(cmds.iconTextRadioCollection('SundayLocatorToolColorCollection', query = True, select = True).split('_')[1]))
                cmds.select(curObj, curLocator)
                cmds.pointConstraint(name = curLocator + '_tempJOINTPointConstraint')
                cmds.orientConstraint(name = curLocator + '_tempJOINTOrientConstraint')
                cmds.delete(curLocator + '_tempJOINTPointConstraint*')
                cmds.delete(curLocator + '_tempJOINTOrientConstraint*')
            
        else:
            SundayDialogPy.SundayDialogConfirm('Error                                        ', 'No objects selected', 'OK')
            return None
        (len(objects) != 0).select(locators)
        cmds.headsUpMessage('Transform the locator(s) as you like and deselect to make it an controller')
        cmds.scriptJob(event = [
            'SelectionChanged',
            'SundayLocatorToolPy\nreload(SundayLocatorToolPy)\nSundayLocatorToolPy.SundayLocatorToolMoveSelectedToLocator(' + str(locators) + ', ' + str(objects) + ')'], runOnce = True)
    elif len(objects) != 0:
        for curObj in objects:
            mel.eval(SundayLocatorToolPy.SundayLocatorToolGetLocator(curObj + '_CTRL', locatorType, locatorUp))
            curLocator = cmds.ls(selection = True)[0]
            cmds.setAttr(curLocator + '.overrideEnabled', 1)
            cmds.setAttr(curLocator + '.overrideColor', int(cmds.iconTextRadioCollection('SundayLocatorToolColorCollection', query = True, select = True).split('_')[1]))
            locators.append(curLocator)
            cmds.select(curObj, curLocator)
            cmds.pointConstraint(name = curLocator + '_tempJOINTPointConstraint')
            cmds.orientConstraint(name = curLocator + '_tempJOINTOrientConstraint')
            cmds.delete(curLocator + '_tempJOINTPointConstraint*')
            cmds.delete(curLocator + '_tempJOINTOrientConstraint*')
            cmds.select(locators)
        
    else:
        mel.eval(SundayLocatorToolPy.SundayLocatorToolGetLocator('SundayLocator', locatorType, locatorUp))
        curLocator = cmds.ls(selection = True)[0]
        cmds.setAttr(curLocator + '.overrideEnabled', 1)
        cmds.setAttr(curLocator + '.overrideColor', int(cmds.iconTextRadioCollection('SundayLocatorToolColorCollection', query = True, select = True).split('_')[1]))


def SundayLocatorToolUI():
    global sundayLocatorToolUI
    SundayMayaGuiPath = mel.eval('getenv SundayGui;')
    
    try:
        if cmds.window(sundayLocatorToolUI, exists = True):
            cmds.deleteUI(sundayLocatorToolUI)
        
        sundayLocatorToolUI = cmds.loadUI(uiFile = SundayMayaGuiPath + 'SundayLocatorTool.ui')
    except:
        sundayLocatorToolUI = cmds.loadUI(uiFile = SundayMayaGuiPath + 'SundayLocatorTool.ui')

    cmds.setParent(sundayLocatorToolUI)
    cmds.setParent(cmds.button('SundayLocatorToolChooseColorDummyButtonToGrabParent', query = True, fullPathName = True, parent = True))
    cmds.iconTextRadioCollection('SundayLocatorToolColorCollection')
    cmds.rowColumnLayout(numberOfColumns = 8)
    cmds.text(label = 'Color : ')
    cmds.iconTextRadioButton('DarkBlue_5', image1 = SundayImage + 'SundayColorDarkBlue.png', height = 20, width = 20, select = True)
    cmds.iconTextRadioButton('DarkRed_4', image1 = SundayImage + 'SundayColorDarkRed.png', height = 20, width = 20)
    cmds.iconTextRadioButton('Purple_9', image1 = SundayImage + 'SundayColorPurple.png', height = 20, width = 20)
    cmds.iconTextRadioButton('Red_13', image1 = SundayImage + 'SundayColorRed.png', height = 20, width = 20)
    cmds.iconTextRadioButton('Green_14', image1 = SundayImage + 'SundayColorGreen.png', height = 20, width = 20)
    cmds.iconTextRadioButton('LightBlue_18', image1 = SundayImage + 'SundayColorLightBlue.png', height = 20, width = 20)
    cmds.iconTextRadioButton('Yellow_17', image1 = SundayImage + 'SundayColorYellow.png', height = 20, width = 20)
    cmds.setParent(sundayLocatorToolUI)
    cmds.setParent(cmds.button('SundayLocatorToolDummyButtonToGrabParent', query = True, fullPathName = True, parent = True))
    cmds.scrollLayout(childResizable = True)
    cmds.rowColumnLayout(numberOfColumns = 8)
    SundayLocatorToolMakeLocatorButtonsInWidget('SundayLocatorToolPy\nreload(SundayLocatorToolPy)\nSundayLocatorToolPy.SundayLocatorToolCreate')
    cmds.showWindow(sundayLocatorToolUI)
    if platform.system() == 'Windows':
        cmds.window(sundayLocatorToolUI, edit = True, topLeftCorner = [
            100,
            100])
    


def SundayLocatorToolUIClose():
    cmds.deleteUI(sundayLocatorToolUI)

