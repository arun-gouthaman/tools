import pymel.all as pm
import CustomScripts


def CustomScripts_UI():

    WINDOW = 'CustomScripts'
    if pm.window(WINDOW, query=True, exists=True):
        pm.deleteUI(WINDOW)
    pm.window(WINDOW,
              title="Custom Scripts",
              iconName='CS',
              widthHeight=(200, 400))
    column_1 = pm.columnLayout(adjustableColumn=True)

    pm.separator(height=20, style='in', parent=column_1)
    pm.button(label='Immediate Parent in Hierarchy',
              command=lambda x: CustomScripts.immediateParent())

    pm.separator(height=20, style='in', parent=column_1)
    hide_jnt_col = pm.rowColumnLayout(parent=column_1,
                                      numberOfColumns=3,
                                      columnWidth=(1, 95))
    pm.button(label='Hide Joint',
              command=lambda x: CustomScripts.jntHide(),
              parent=hide_jnt_col)
    pm.separator(parent=hide_jnt_col, horizontal=False, width=10)
    pm.button(label='Show Joint',
              command=lambda x: CustomScripts.jntShow(),
              parent=hide_jnt_col,
              width=95)

    pm.separator(height=20, style='in', parent=column_1)
    lod_col = pm.rowColumnLayout(parent=column_1,
                                 numberOfColumns=3,
                                 columnWidth=(1, 95))
    pm.button(label='LOD off',
              command=lambda x: CustomScripts.lodOff(),
              parent=lod_col)
    pm.separator(parent=lod_col, horizontal=False, width=10)
    pm.button(label='LOD on',
              command=lambda x: CustomScripts.lodOn(),
              parent=lod_col,
              width=95)

    pm.separator(height=20, style='in', parent=column_1)
    pm.button(label='Parent( in selection order)',
              command=lambda x: CustomScripts.parentChain(),
              parent=column_1)

    # get object name
    pm.separator(height=20, style='in', parent=column_1)
    row_col_2 = pm.rowColumnLayout(numberOfColumns=2,
                                   columnWidth=(1, 150),
                                   parent=column_1,
                                   columnOffset=(2, 'left', 10))
    object_name = pm.TextField(parent=row_col_2)
    pm.button(
        label='<<',
        parent=row_col_2,
        command=lambda x: object_name.setText(str(pm.ls(selection=True)[0])))
    row_col_3 = pm.rowColumnLayout(numberOfColumns=2,
                                   columnWidth=(1, 100),
                                   parent=column_1,
                                   columnOffset=(2, 'left', 10))
    prntChk = pm.checkBox("parent", parent=row_col_3)
    sclChk = pm.checkBox("scale", parent=row_col_3)
    pm.separator(height=5, style='none', parent=column_1)
    pm.button(
        label='Copy Object to selected positions',
        parent=column_1,
        command=lambda x: CustomScripts.copyObjects(obj=object_name.getText(),
                                                    prFlg=prntChk.getValue(),
                                                    scFlg=sclChk.getValue()))

    pm.separator(height=20, style='in', parent=column_1)
    pm.button(label="copy orientation",
              parent=column_1,
              command=lambda x: CustomScripts.CopyJntOri())

    pm.showWindow(WINDOW)
    pm.window(WINDOW, edit=True, widthHeight=(200, 320))
    return None
# CustomScripts_UI()
