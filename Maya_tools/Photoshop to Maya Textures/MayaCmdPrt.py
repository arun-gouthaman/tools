import maya.cmds as cmds

if cmds.commandPort(':54321', q=True) !=1:

    cmds.commandPort(n=':54321', sourceType = 'python')