'''
*
*  SundayPlusSavePy.py
*  Version 0.6
*  Sunday Studio Pipeline (Maya) 
*
*  Maintained by Christian Esbo Agergaard - www.3dg.dk
*  Copyright Sunday Animation Studio ApS and Christian Esbo Agergaard 2011 | sundaystudio.com
*
'''
import maya.cmds as cmds
import maya.mel as mel
import os
import shutil
import platform
import SundayDialogPy
reload(SundayDialogPy)

def SundayPlusSaveWrongFileConvention():
    plusSaveHelpDialog = SundayDialogPy.SundayDialogPromptYesNo('Error                                                     ', 'Scene is not the right file convention: Name_###_Author.mb', 'OK', 'HELP')
    if plusSaveHelpDialog == 'HELP':
        cmds.showHelp('http://www.3dg.dk/2011/12/07/sunday-pipeline-plus-save/', absolute = True)
    


def SundayPlusSaveDoSave(name, curVersion, author, nC, hC):
    path = os.path.dirname(cmds.file(query = True, sceneName = True)) + os.sep
    ext = os.path.splitext(cmds.file(query = True, sceneName = True, shortName = True))[1]
    historyFile = cmds.file(query = True, sceneName = True)
    historyFileName = cmds.file(query = True, sceneName = True, shortName = True).split('_')[0]
    newName = name + '_' + '%03d' % int(curVersion) + '_' + author + nC + ext
    if os.path.exists(path + newName):
        SundayDialogPy.SundayDialogConfirm('Error                                                             ', 'File already exists. Did not not plus save file.', 'OK')
        return None
    newFile = cmds.file(rename = path + newName)
    cmds.file(save = True)
    if os.path.isdir(path + '_History') != True:
        os.mkdir(path + '_History')
    
    
    try:
        if cmds.checkBox('plusSaveOptionMoveOldFile', query = True, value = True) == False:
            shutil.move(historyFile, path + '_History' + os.sep + historyFileName + '_' + '%03d' % (int(curVersion) - 1) + '_' + author + hC + ext)
    except:
        os.path.exists(path + newName)
        shutil.move(historyFile, path + '_History' + os.sep + historyFileName + '_' + '%03d' % (int(curVersion) - 1) + '_' + author + hC + ext)

    if ext == '.mb':
        mel.eval('addRecentFile "' + newFile + '" "mayaBinary";')
    else:
        mel.eval('addRecentFile "' + newFile + '" "mayaAscii";')


def SundayPlusSave():
    if len(os.path.splitext(cmds.file(query = True, sceneName = True, shortName = True))[0].split('_')) > 2:
        
        try:
            curNameSplit = os.path.splitext(cmds.file(query = True, sceneName = True, shortName = True))[0].split('_')
            curName = curNameSplit[0]
            curVersion = curNameSplit[1]
            curAuthor = curNameSplit[2]
            curCaption = ''
            for i in range(3, len(curNameSplit)):
                curCaption = curCaption + '_' + curNameSplit[i]
            
            SundayPlusSaveDoSave(curName, int(curVersion) + 1, curAuthor, curCaption, curCaption)
        except:
            pass
        SundayPlusSaveWrongFileConvention()

    else:
        SundayPlusSaveWrongFileConvention()


def SundayPlusSaveOptions():
    name = cmds.textField('plusSaveNewSceneLineEdit', query = True, text = True)
    author = cmds.textField('plusSaveAuthorLineEdit', query = True, text = True)
    version = cmds.textField('plusSaveFileVersionLineEdit', query = True, text = True)
    nC = cmds.textField('plusSaveNewCaptionLineEdit', query = True, text = True)
    hC = cmds.textField('plusSaveHistoryCaptionLineEdit', query = True, text = True)
    if nC != '':
        nC = '_' + nC
    
    if hC != '':
        hC = '_' + hC
    
    SundayPlusSaveDoSave(name, version, author, nC, hC)
    SundayPlusSaveOptionsUIClose()


def SundayPlusSaveUnlockVersion():
    cmds.textField('plusSaveFileVersionLineEdit', edit = True, enable = True)
    cmds.button('plusSaveUnlockVersion', edit = True, enable = False)


def SundayPlusSaveChangeNewCaption():
    newCaption = cmds.optionMenu('plusSaveNewCaptionComboBox', query = True, value = True)
    cmds.textField('plusSaveNewCaptionLineEdit', edit = True, text = newCaption)


def SundayPlusSaveChangeHistoryCaption():
    historyCaption = cmds.optionMenu('plusSaveHistoryCaptionComboBox', query = True, value = True)
    cmds.textField('plusSaveHistoryCaptionLineEdit', edit = True, text = historyCaption)


def SundayPlusSaveOptionsUIClose():
    cmds.deleteUI(plusSaveDialogUI)


def SundayPlusSaveOptionsUI():
    global plusSaveDialogUI
    if len(os.path.splitext(cmds.file(query = True, sceneName = True, shortName = True))[0].split('_')) > 2:
        SundayMayaGuiPath = mel.eval('getenv SundayGui;')
        
        try:
            if cmds.window(plusSaveDialogUI, exists = True):
                cmds.deleteUI(plusSaveDialogUI)
            
            plusSaveDialogUI = cmds.loadUI(uiFile = SundayMayaGuiPath + 'SundayPlusSaveOption.ui')
        except:
            plusSaveDialogUI = cmds.loadUI(uiFile = SundayMayaGuiPath + 'SundayPlusSaveOption.ui')

        cmds.textField('plusSaveAuthorLineEdit', edit = True, text = cmds.optionVar(query = 'SundayUserName'))
        cmds.textField('plusSaveNewSceneLineEdit', edit = True, text = os.path.splitext(cmds.file(query = True, sceneName = True, shortName = True))[0].split('_')[0])
        cmds.textField('plusSaveFileVersionLineEdit', edit = True, text = int(os.path.splitext(cmds.file(query = True, sceneName = True, shortName = True))[0].split('_')[1]) + 1)
        curNameSplit = os.path.splitext(cmds.file(query = True, sceneName = True, shortName = True))[0].split('_')
        curCaption = ''
        for i in range(3, len(curNameSplit)):
            curCaption = curCaption + '_' + curNameSplit[i]
        
        cmds.textField('plusSaveNewCaptionLineEdit', edit = True, text = curCaption[1:])
        cmds.textField('plusSaveHistoryCaptionLineEdit', edit = True, text = curCaption[1:])
        cmds.optionMenu('plusSaveNewCaptionComboBox', edit = True, changeCommand = 'SundayPlusSavePy.SundayPlusSaveChangeNewCaption()')
        cmds.optionMenu('plusSaveHistoryCaptionComboBox', edit = True, changeCommand = 'SundayPlusSavePy.SundayPlusSaveChangeHistoryCaption()')
        cmds.showWindow(plusSaveDialogUI)
        if platform.system() == 'Windows':
            cmds.window(plusSaveDialogUI, edit = True, topLeftCorner = [
                100,
                100])
        
    else:
        SundayPlusSaveWrongFileConvention()

