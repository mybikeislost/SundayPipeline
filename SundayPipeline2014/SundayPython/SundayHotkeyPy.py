'''
*
*  SundayHotkeyPy.py
*  Version 0.5
*  Sunday Studio Pipeline (Maya) 
*
*  Maintained by Christian Esbo Agergaard - www.3dg.dk
*  Copyright Sunday Animation Studio ApS and Christian Esbo Agergaard 2011 | sundaystudio.com
*
'''
import maya.cmds as cmds
import maya.mel as mel

def SundayHotkeyWrapper(sourceType, name, key, down, release, alt, ctrl, cmd):
    if sourceType == 'python':
        print 'Setkey : ' + key + ' - Script : ' + down
        cmds.nameCommand(name + '_down', annotation = 'annotation_' + name, command = 'python( "' + down + '" )')
        cmds.nameCommand(name + '_release', annotation = 'annotation_' + release, command = 'python( "' + release + '" )')
        cmds.hotkey(k = key, name = name + '_down', releaseName = name + '_release', alt = alt, ctl = ctrl, cmd = cmd)
    else:
        print 'Setkey : ' + key + ' - Script : ' + down
        cmds.nameCommand(name + '_down', annotation = 'annotation_' + name, command = down)
        cmds.nameCommand(name + '_release', annotation = 'annotation_' + release, command = release)
        cmds.hotkey(k = key, name = name + '_down', releaseName = name + '_release', alt = alt, ctl = ctrl, cmd = cmd)


def SundayHotkeyReset():
    cmds.optionVar(stringValue = ('SundayHotkeyLayout', 'Maya Default'))
    mel.eval('source hotkeySetup')

