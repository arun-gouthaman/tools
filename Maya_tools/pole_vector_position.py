import pymel.all as pm
import maya.OpenMaya as openmaya


def set_poleLocator(**kwargs):
    """
        Select 3 joints parent to child in order to which pole
            vector has to be placed
        Select 3 joints and ik handle in order, to create the pole
            vector object and constraint
    """
    distance_scale = kwargs.get("distance_scale", 1)
    pole_vector_locator = kwargs.get("pole_vector", "poleLocator")
    selected_joint = pm.ls(selection=True)
    if len(selected_joint) < 3:
        print("please select 3 joints")
        return None
    joint1_position = pm.xform(selected_joint[0],
                               query=True,
                               worldSpace=True,
                               translation=True)
    joint2_position = pm.xform(selected_joint[1],
                               query=True,
                               worldSpace=True,
                               translation=True)
    joint3_position = pm.xform(selected_joint[2],
                               query=True,
                               worldSpace=True,
                               translation=True)

    joint1_vector = openmaya.MVector(joint1_position[0], joint1_position[1],
                                     joint1_position[2])
    joint2_vector = openmaya.MVector(joint2_position[0], joint2_position[1],
                                     joint2_position[2])
    joint3_vector = openmaya.MVector(joint3_position[0], joint3_position[1],
                                     joint3_position[2])

    joint1_joint2_vector = joint2_vector - joint1_vector
    joint1_joint2_vector.normalize()
    joint2_joint3_vector = joint3_vector - joint2_vector
    joint2_joint3_vector.normalize()
    plane_normal = joint1_joint2_vector ^ joint2_joint3_vector
    plane_normal.normalize()

    joint1_joint3_vector = joint3_vector - joint1_vector
    joint1_joint3_vector.normalize

    pole_vector = joint1_joint3_vector ^ plane_normal
    mag_vec = pole_vector * distance_scale

    pole_position = joint2_vector + mag_vec

    loc_pos = [pole_position.x, pole_position.y, pole_position.z]
    pole_locator = pm.spaceLocator(name=pole_vector_locator)
    locator_group = pm.group(pole_locator, name=pole_vector_locator + "_group")
    pm.xform(locator_group, translation=loc_pos)
    print("Pole object placed at ", str(loc_pos))
    if len(selected_joint) == 4:
        ik_handle = selected_joint[3]
        pm.poleVectorConstraint(pole_locator, ik_handle)
        print("Pole Vector Constraint applied")
    return None


set_poleLocator(distance_scale=1, pole_vector="r_leg_pole_vector_locator")
