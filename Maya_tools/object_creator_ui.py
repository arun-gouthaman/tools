import pymel.all as pm

from object_creator_operations import create_joint
from object_creator_operations import create_locator
from object_creator_operations import create_group


def object_creator_ui():
    """This method creates user interface to input object details

        User Inputs:
            - Object name
            - Object ID

    Returns : None
    """
    WINDOW = 'ObjectCreator'
    if pm.window(WINDOW, query=True, exists=True):
        pm.deleteUI(WINDOW)
    pm.window(WINDOW,
              title="Object creator",
              iconName='OC',
              widthHeight=(200, 250))
    column_1 = pm.columnLayout(adjustableColumn=True)

    pm.Text(label="Enter Object Name", parent=column_1)
    object_name = pm.TextField(text='Object', parent=column_1)

    pm.separator(height=20, style='in', parent=column_1)
    pm.Text(label="Enter ID to start with", parent=column_1)
    object_id = pm.TextField(text='01', parent=column_1)

    pm.separator(height=20, style='in', parent=column_1)
    pm.button(label='Create Joint',
              command=lambda x: create_joint(object_name.getText(),
                                             object_id.getText()),
              parent=column_1)

    pm.separator(height=20, style='in', parent=column_1)
    pm.button(label='Create Locator',
              command=lambda x: create_locator(object_name.getText(),
                                               object_id.getText()),
              parent=column_1)

    pm.separator(height=20, style='in', parent=column_1)
    pm.button(label='Create Group',
              command=lambda x: create_group(object_name.getText(),
                                             object_id.getText()),
              parent=column_1)

    pm.showWindow(WINDOW)
    pm.window(WINDOW, edit=True, widthHeight=(200, 250))
    return None


object_creator_ui()
