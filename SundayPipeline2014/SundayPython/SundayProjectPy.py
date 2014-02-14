'''
*
*  SundayProjectPy.py
*  Version 0.4
*  Sunday Studio Pipeline (Maya) 
*
*  Maintained by Christian Esbo Agergaard - www.3dg.dk
*  Copyright Sunday Animation Studio ApS and Christian Esbo Agergaard 2011 | sundaystudio.com
*
'''
import maya.cmds as cmds
import maya.mel as mel
import os
import subprocess
import platform
import SundayDialogPy
reload(SundayDialogPy)

def SundayProjectOpenAndSetProject():
    file = SundayDialogPy.SundayDialogFileOpen('/', 1, 'Maya Files (*.mb *.ma)')
    
    try:
        if len(file) != 0:
            curScene = cmds.file(query = True, sceneName = True)
            if curScene != '':
                result = SundayDialogPy.SundayDialogPromptYesNoCancel('Save Changes', 'Save to ' + curScene, 'Save', "Don't Save", 'Cancel')
            else:
                result = 'open'
            if result != 'Cancel':
                projectPath = file[0].split('/')
                newProject = ''
                for compPath in range(0, len(projectPath) - 2):
                    newProject = newProject + projectPath[compPath] + '/'
                
                mel.eval('setProject "' + newProject + '";')
                if result == 'Save':
                    cmds.file(save = True)
                
                cmds.file(file[0], force = True, options = 'v=0', open = True)
                if os.path.splitext(cmds.file(query = True, sceneName = True, shortName = True))[1] == '.mb':
                    mel.eval('addRecentFile "' + file[0] + '" "mayaBinary";')
                else:
                    mel.eval('addRecentFile "' + file[0] + '" "mayaAscii";')
            
    except:
        pass



def SundayProjectSetProjectFromScene():
    sceneFile = cmds.file(query = True, sceneName = True).split('/')
    newProject = ''
    for compPath in range(0, len(sceneFile) - 2):
        newProject = newProject + sceneFile[compPath] + '/'
    
    mel.eval('setProject "' + newProject + '";')
    SundayDialogPy.SundayDialogConfirm('Project Path Set To :                         ', newProject, 'OK')


def SundayProjectRevealProject():
    project = cmds.workspace(query = True, fullName = True)
    if platform.system() == 'Windows':
        subprocess.Popen([
            'explorer',
            project.replace('/', '\\')])
    elif platform.system() == 'Linux':
        subprocess.call([
            'xdg-open',
            project])
    else:
        subprocess.call([
            'open',
            '-R',
            project])
