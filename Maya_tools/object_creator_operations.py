# Import pymel library
import pymel.all as pm


def obtain_selection_position():
    """This method creates a list of positions from user selection

    returns : position_list
    """
    user_selection = pm.ls(selection=True, flatten=True)
    position_list = []
    for selected in user_selection:
        position_list.append(
            pm.xform(selected, query=True, worldSpace=True, translation=True))
    return position_list


def create_locator(*args):
    """This methos creates Locators at user selected positions

    function call format : create_locator("String", Integer)

    User Inputs:
        args[0] : Object name
        args[1] : object Id to start with

    Returns : None
    """
    # If number of parameters mismatch, return with message
    if len(args) != 2:
        print("arguments mismatch")
        return None

    # Call to method to obtain list of selected position
    position_list = obtain_selection_position()

    # If user selected nothing, return with message display
    if not position_list:
        print("please make selection")
        return None

    # Obtain object name from *args
    object_name = args[0]
    # Obtain the object ID from *args as integer
    object_id = int(args[1])

    # create Locators at selected positions and
    # increment the ID to name the next locator in loop
    for object_position in position_list:
        locator_name = object_name + str(object_id) + '_Locator'
        space_locator = pm.spaceLocator(name=locator_name)
        pm.xform(space_locator, translation=object_position)
        object_id = object_id + 1
    return None


def create_joint(*args):
    """This method creates Joints at user selected positions

    function call format : create_locator("String", Integer)

    User Inputs:
        args[0] : Object name
        args[1] : object Id to start with

    Returns : None
    """
    # If number of parameters mismatch, return with message
    if len(args) != 2:
        print("arguments mismatch")
        return None

    # Call to method to obtain list of selected position
    position_list = obtain_selection_position()

    # If user selected nothing, return with message display
    if not position_list:
        print('please make selection')
        return None

    # clear all selections to create the root joint in current chain
    pm.select(clear=True)
    # Create empty list to store the joints being created
    joint_list = []

    # Obtain object name from args
    object_name = args[0]
    # Obtain the object ID from args as integer
    object_id = int(args[1])

    # Create joints at selected positions and increment
    # ID value to name the next joint in loop
    for index in range(len(position_list)):
        if object_id < 10:
            joint_name = object_name + "0" + str(object_id) + '_Joint'
        else:
            joint_name = object_name + str(object_id) + '_Joint'

        # First joint in chain is created at specified location
        if index < 1:
            created_joint = pm.joint(name=joint_name,
                                     position=position_list[index])
        # Create a child joint by selecting the previous joint as parent and
        # The previous joint orientation is edited so its X Axis points child
        else:
            pm.select(joint_list[index - 1])
            created_joint = pm.joint(name=joint_name,
                                     position=position_list[index])
            pm.joint(joint_list[index - 1],
                     edit=True,
                     orientJoint='xyz',
                     secondaryAxisOrient='yup',
                     zeroScaleOrient=True)

        # New joint created is appended to joint_list
        joint_list.append(created_joint)

        # Object id value is incremented by one for next joint name
        object_id = object_id + 1
    return None


def create_group(*args):
    """This method creates empty group at user selected positions

    function call format : create_locator("String", Integer)

    User Inputs:
        args[0] : Object name
        args[1] : object Id to start with

    Returns : None
    """

    # If number of parameters mismatch, return with message
    if len(args) != 2:
        print("arguments mismatch")
        return None

    # Call to method to obtain list of selected position
    position_list = obtain_selection_position()

    # If user selected nothing, return with message display
    if not position_list:
        print('please make selection')
        return None

    # Obtain object name from args
    object_name = args[0]
    # Obtain the object ID from args as integer
    object_id = int(args[1])

    # Create empty roup and move the empty group to
    # selected position, and increment the ID value to name
    # the next group in loop
    for objectPosition in position_list:
        group_name = object_name + str(object_id) + '_Group'
        created_group = pm.group(name=group_name, empty=True)
        pm.xform(created_group, translation=objectPosition, worldSpace=True)
        object_id = object_id + 1
    return None
