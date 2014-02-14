'''
*
*  SundayDialogPy.py
*  Version 0.2
*  Sunday Studio Pipeline (Maya) 
*
*  Maintained by Christian Esbo Agergaard - www.3dg.dk
*  Copyright Sunday Animation Studio ApS and Christian Esbo Agergaard 2011 | sundaystudio.com
*
'''
import maya.cmds as cmds
import maya.mel as mel

def SundayDialogFileOpen(startingDirectory, fileMode, fileFilter):
    file = cmds.fileDialog2(startingDirectory = startingDirectory, fileMode = fileMode, fileFilter = fileFilter)
    return file


def SundayDialogPromptYesNo(title, message, yes, no):
    result = cmds.confirmDialog(title = title, message = message, button = [
        yes,
        no], defaultButton = yes, cancelButton = no, dismissString = no)
    return result


def SundayDialogPromptYesNoCancel(title, message, yes, no, cancel):
    result = cmds.confirmDialog(title = title, message = message, button = [
        yes,
        no,
        cancel], defaultButton = yes, cancelButton = cancel, dismissString = cancel)
    return result


def SundayDialogConfirm(title, message, confirm):
    cmds.confirmDialog(title = title, message = message, button = confirm)


def SundayDialogPromptVariable(title, message, text):
    result = cmds.promptDialog(title = title, message = message, text = text, button = [
        'OK',
        'Cancel'], defaultButton = 'OK', cancelButton = 'Cancel', dismissString = 'Cancel')
    if result == 'OK':
        text = cmds.promptDialog(query = True, text = True)
        if text == '':
            SundayDialogConfirm('Error                ', 'Needs a name!', 'OK')
        else:
            return text
    text == ''


def SundayDialogPromptVariableAndStayOpen(title, message, text, ok, close):
    result = cmds.promptDialog(title = title, message = message, text = text, button = [
        ok,
        close], defaultButton = ok, cancelButton = close, dismissString = close)
    if result != close:
        return cmds.promptDialog(query = True, text = True)
    return 0

