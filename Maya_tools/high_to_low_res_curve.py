"""Get the length of high res curve and draw low res curve
at equal length intervals
"""
# and add joints to control the curve

import maya.OpenMaya as OpenMaya
import pymel.all as pm


def curve_through_points(**kwargs):
    curve_name = kwargs.get("curve_name", "")
    curve_degree = kwargs.get("curve_degree", 1)
    points_locations = kwargs.get("curve_points", [])
    pm.select(clear=True)
    current_curve = pm.curve(degree=curve_degree,
                             worldSpace=True,
                             point=points_locations)
    pm.rename(current_curve, curve_name)
    return current_curve


crv = pm.ls(selection=True)[0]


def getDagPath(objectName):
    if isinstance(objectName, list):
        oNodeList = []
        for o in objectName:
            selectionList = OpenMaya.MSelectionList()
            selectionList.add(o)
            oNode = OpenMaya.MDagPath()
            selectionList.getDagPath(0, oNode)
            oNodeList.append(oNode)
        return oNodeList
    else:
        selectionList = OpenMaya.MSelectionList()
        selectionList.add(objectName)
        oNode = OpenMaya.MDagPath()
        selectionList.getDagPath(0, oNode)
        return oNode


def createJoint(positionList):
    for pos in position_list:
        pm.select(clear=True)
        new_joint = pm.joint(position=pos)
        new_joint.radius.set(0.2)
        pm.select(clear=True)
    return None


crv = str(pm.ls(selection=True)[0])
curveFn = OpenMaya.MFnNurbsCurve(getDagPath(crv))
point_at_param = OpenMaya.MPoint()
curve_len = curveFn.length()
print(curve_len)
part_length = float(curve_len) / 4
sum_len = 0
param_util = OpenMaya.MScriptUtil()
param_at_len = param_util.asDoublePtr()
position_list = []
while sum_len < curve_len or sum_len == curve_len:
    param_at_len = curveFn.findParamFromLength(sum_len)
    curveFn.getPointAtParam(param_at_len, point_at_param,
                            OpenMaya.MSpace.kObject)
    print(sum_len, param_at_len, "====>", point_at_param[0], point_at_param[
            1], point_at_param[2])
    point_position = (point_at_param[0], point_at_param[1], point_at_param[2])
    position_list.append(point_position)
    sum_len = sum_len + part_length
joint_list = []
curve_create = curve_through_points(curve_name="low_res_curve",
                                    curve_degree=3,
                                    curve_points=position_list)
createJoint(position_list)
