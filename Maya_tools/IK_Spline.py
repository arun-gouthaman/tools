import pymel.all as pm
import maya.OpenMaya as OpenMaya
from CustomScripts import curve_through_points, joints_along_curve


def stretch_expression(**kwargs):
    sel_jnts = kwargs.get("joints", [])
    curve_info_node = kwargs.get("curve_info_node", None)
    global_scale_attribute = kwargs.get("scale_attribute", None)
    expression_name = kwargs.get("expression_name", "ik_sretch_expression")
    connect_scale = kwargs.get("connect_scale", False)
    control_attribute = kwargs.get("ctrl_attr", None)
    global_scale = kwargs.get("glbl_scl_stat", False)
    global_attr = kwargs.get("glbl_scl_attr", None)
    control_obj = kwargs.get("control_obj", None)
    scale_joints = kwargs.get("scale_joints", None)

    total_len = 0.0
    count = str(len(sel_jnts) - 1)
    curve_length = str(curve_info_node) + ".arcLength"
    main_expression_name = expression_name

    exp_scale_str = ""
    exp_def_scale_str = ""
    exp_init_str = ""
    exp_stretch_str = ""
    exp_def_stretch_str = ""
    arc_len_str = ""
    scale_val_str = ""
    c_comp_str = ""
    a_comp_str = ""
    vertical_cal_str = ""
    depth_cal_str = ""
    polynomial_fun_ip = ""
    polynomial_fun_str = ""
    if connect_scale:
        polynomial_fun_ip = "float $depth_ip ="+control_obj+".EndDepth*\
                            clamp(-1,1, $len_diff/10);\n" + \
                            "float $hpos_ip ="+control_obj+".ShiftScale*\
                            clamp(-1,1, $len_diff/10);\n"  + \
                            "float $vpos_ip = "+control_obj+".Thickness*\
                            clamp(-1,1, $len_diff/10);\n" + \
                            "float $depth_val;\n" + \
                            "float $vertical_val;\n"

        polynomial_fun_str = "proc float poly(float $a, float $b,\
                                              float $c, float $x)\n" + \
                             "{\n" + \
                             "float $y=($a*pow($x,2)) + ($b*$x) + $c;\n" + \
                             "return $y;\n" + \
                             "}\n"

    for jnt in sel_jnts:
        exp_init_str = exp_init_str + "float $joint" + str(
            sel_jnts.index(jnt)) + "_tx" + "=" + str(
                jnt.translateX.get()) + ";\n"
        exp_stretch_str = exp_stretch_str + str(
            jnt) + ".translateX = $joint" + str(
                sel_jnts.index(jnt)) + "_tx + $len_diff;\n"
        exp_def_stretch_str = exp_def_stretch_str + str(
            jnt) + ".translateX = $joint" + str(sel_jnts.index(jnt)) + "_tx;\n"

    if connect_scale:
        if scale_joints:
            scale_param_val, total_len = set_scale_param(
                joint_list=scale_joints)
            scale_count = str((len(sel_jnts) - 1) / (len(scale_joints) - 1))
            vertical_cal_str = "$vertical_val = (exp(-$len_diff*" + str(
                scale_count) + "))*($vpos_ip+1);\n"
        else:
            scale_param_val, total_len = set_scale_param(joint_list=sel_jnts)
            vertical_cal_str = "$vertical_val = (exp(-$len_diff))*\
                                ($vpos_ip+1);\n"

        for key in scale_param_val.keys():
            exp_scale_str += str(key) + ".scaleY=" + str(
                key
            ) + ".scaleZ = poly($depth_val, $hpos_ip, $vertical_val, " + str(
                scale_param_val[key]) + ");\n"
            exp_def_scale_str = exp_def_scale_str + str(
                key) + ".scaleZ =" + str(key) + ".scaleY = 1;\n"
        depth_cal_str = "float $depth_val = ((1-exp(-$len_diff))/(" + str(
            total_len * 10) + "))*$depth_ip;\n"

    init_arc_length = str(pm.getAttr(curve_length))
    if (global_scale):
        arc_len_str = "float $arc_len = " + curve_length + "/" + \
                       global_attr + ";\n"
    else:
        arc_len_str = "float $arc_len = " + curve_length + ";\n"
    string_exp_str = arc_len_str+exp_init_str+polynomial_fun_str + \
        "if ($arc_len != "+init_arc_length+" && "+control_attribute+")\n" + \
        "{\n" + \
        "float $len_diff =(" + control_attribute + "/10)*($arc_len - " + \
        init_arc_length+")/"+count+";\n"+polynomial_fun_ip + \
        exp_stretch_str+vertical_cal_str + \
        depth_cal_str + \
        "\nfloat $scale_val = (-($arc_len - "+init_arc_length + \
        ")/100)+1;\n"+exp_scale_str + \
        "}\n" + \
        "else\n" + \
        "{\n"+exp_def_stretch_str+exp_def_scale_str + \
        "}\n"
    pm.expression(name=main_expression_name, string=string_exp_str)

    return None


def set_scale_param(**kwargs):
    total_len = 0.0
    joint_values = {}
    sel_jnts = kwargs.get("joint_list", None)
    if not sel_jnts:
        sel_jnts = pm.ls(selection=True)
    vec1 = OpenMaya.MVector(0, 0, 0)
    vec2 = OpenMaya.MVector(0, 0, 0)
    vec3 = OpenMaya.MVector(0, 0, 0)
    joint_values[sel_jnts[0]] = 0.0
    for index in range(len(sel_jnts) - 1):
        pos = pm.xform(sel_jnts[index],
                       query=True,
                       worldSpace=True,
                       translation=True)
        vec1.x = pos[0]
        vec1.y = pos[1]
        vec1.z = pos[2]
        pos = pm.xform(sel_jnts[index + 1],
                       query=True,
                       worldSpace=True,
                       translation=True)
        vec2.x = pos[0]
        vec2.y = pos[1]
        vec2.z = pos[2]
        vec3 = vec2 - vec1
        total_len += vec3.length()
        joint_values[sel_jnts[index + 1]] = total_len

    mid = total_len / 2
    for key in joint_values.keys():
        joint_values[key] = joint_values[key] - mid
    return joint_values, total_len


def dense_chain(**kwargs):
    import pymel.core.datatypes as dt
    joints = kwargs.get("joints", None)
    joints_inbetween = kwargs.get("joints_inbetween", 5)
    if not joints:
        joints = pm.ls(selection=True)
    joints.pop(-1)

    for jnt in joints:
        child = jnt.getChildren()
        pos = pm.xform(jnt, query=True, translation=True, worldSpace=True)
        vpos1 = dt.Vector(pos)
        pos = pm.xform(child[0], query=True, translation=True, worldSpace=True)
        vpos2 = dt.Vector(pos)
        vpos = vpos2 - vpos1
        div_vec = vpos / (joints_inbetween + 1)
        out_vec = vpos1
        cur_jnt = jnt
        for i in range(joints_inbetween):
            out_vec = (out_vec + div_vec)
            pos = [out_vec.x, out_vec.y, out_vec.z]
            print "JOINT TEST", cur_jnt
            new_jnt = pm.insertJoint(cur_jnt)
            new_jnt = pm.joint(new_jnt,
                               edit=True,
                               component=True,
                               position=pos,
                               name=str(jnt) + "_" + str(i))
            cur_jnt = new_jnt
    return None


def setup_ik_spline(**kwargs):
    curve = kwargs.get("curve", None)
    joint_chain = kwargs.get("joint_chain", None)
    auto_curve = kwargs.get("auto_curve", True)
    use_curve = kwargs.get("use_curve", None)
    spans = kwargs.get("number_of_spans", 4)
    ctrl_jnts = kwargs.get("num_control_joints", 3)
    ik_name = kwargs.get("ik_name", "ikHandle")
    scale_stretch = kwargs.get("scale_stretch", False)
    create_dense_chain = kwargs.get("dense_chain", False)
    dense_division = kwargs.get("dense_chain_divisions", 3)
    auto_simplify = kwargs.get("auto_simplify_curve", False)
    stretch_exp = kwargs.get("stretch_exp", False)
    global_scale_check = kwargs.get("global_scale_check", False)
    global_scale_attr = kwargs.get("global_scale_attr", None)
    obj = None

    pm.select(joint_chain, hierarchy=True)
    joint_chain = pm.ls(selection=True)
    for i in range(len(joint_chain)):
        pm.rename(joint_chain[i], ik_name + str(i) + "_IK_JNT")
        joint_chain[i] = pm.PyNode(ik_name + str(i) + "_IK_JNT")
    print joint_chain
    if not isinstance(joint_chain[0], pm.Joint):
        pm.displayInfo("selection should be of type joint")
        return None
    if len(joint_chain) < 2:
        pm.displayInfo("Chain should consist of more than one joint")
        return None

    if (global_scale_check):
        if (global_scale_attr is None):
            pm.displayInfo("Please input global scale attribute")
            return None
        else:
            obj = global_scale_attr.split(".")[0]
            global_attr = global_scale_attr.split(".")[1]
            check_global_attr = pm.attributeQuery(global_attr,
                                                  node=obj,
                                                  exists=True)
            if not check_global_attr:
                pm.displayInfo("Invalid global scale attribute")
                return None

    start_jnt = joint_chain[0]
    end_joint = joint_chain[-1]

    if create_dense_chain:
        rep_chain = pm.duplicate(joint_chain)
        print "DUPLICATE"

        for i in range(len(rep_chain)):
            pm.rename(rep_chain[i], str(joint_chain[i]) + "_DnsJnt")
            rep_chain[i] = pm.PyNode(str(joint_chain[i]) + "_DnsJnt")

        print rep_chain
        start_jnt = rep_chain[0]
        end_joint = rep_chain[-1]
        dense_chain(joints=rep_chain, joints_inbetween=dense_division)
        rep_chain.append(end_joint)
        for index in range(len(joint_chain)):
            pm.parentConstraint(rep_chain[index],
                                joint_chain[index],
                                maintainOffset=False)
        pm.select(start_jnt, hierarchy=True)
        new_chain = pm.ls(selection=True)

    crv = ""
    if auto_curve:
        ik_handle, eff, crv = pm.ikHandle(startJoint=start_jnt,
                                          createCurve=auto_curve,
                                          solver="ikSplineSolver",
                                          numSpans=spans,
                                          endEffector=end_joint,
                                          simplifyCurve=auto_simplify)

    else:
        crv = pm.PyNode(use_curve)
        ik_handle, eff = pm.ikHandle(startJoint=start_jnt,
                                     curve=use_curve,
                                     solver="ikSplineSolver",
                                     endEffector=end_joint,
                                     createCurve=False)

    crv.inheritsTransform.set(0)

    pm.rename(ik_handle, ik_name + "IK_Handle")
    pm.rename(crv, ik_name + "IK_Curve")

    ik_curve_shp = crv.getShape()
    crv_info_node = pm.createNode("curveInfo")
    pm.connectAttr(ik_curve_shp + ".worldSpace", crv_info_node + ".inputCurve")
    if ctrl_jnts:
        if ctrl_jnts == 1:
            print "Minimum 2 joints needed as controllers"
            print "skipping control joint creation process"
            pm.displayInfo("Minimum 2 joints needed as controllers")
        else:
            ctrl_jnts = joints_along_curve(number_of_joints=ctrl_jnts,
                                           curve=crv,
                                           bind_curve_to_joint=True)
            pm.select(clear=True)
            ctr_jnt_gp = pm.group(ctrl_jnts,
                                  name=ik_name + "_control_joints_GP")
        for i in range(len(ctrl_jnts)):
            pm.rename(ctrl_jnts[i], ik_name + str(i + 1) + "_IK_CTRL")
            ctrl_jnts[i] = pm.PyNode(ik_name + str(i + 1) + "_IK_CTRL")
    if stretch_exp:
        pm.addAttr(ctrl_jnts[-1],
                   longName="Stretch",
                   attributeType="float",
                   minValue=0,
                   maxValue=10,
                   keyable=True)
        print "ATTRIBUTE TO", str(ctrl_jnts[-1])
        if scale_stretch:
            pm.addAttr(ctrl_jnts[-1],
                       longName="EndDepth",
                       attributeType="float",
                       keyable=True)
            pm.addAttr(ctrl_jnts[-1],
                       longName="Thickness",
                       attributeType="float",
                       keyable=True)
            pm.addAttr(ctrl_jnts[-1],
                       longName="ShiftScale",
                       attributeType="float",
                       keyable=True)

        if create_dense_chain:
            stretch_expression(joints=new_chain,
                               curve_info_node=crv_info_node,
                               connect_scale=scale_stretch,
                               expression_name=ik_name + "_stretch_expression",
                               ctrl_attr=str(ctrl_jnts[-1]) + ".Stretch",
                               glbl_scl_stat=global_scale_check,
                               glbl_scl_attr=global_scale_attr,
                               control_obj=str(ctrl_jnts[-1]),
                               scale_joints=joint_chain)
        else:
            stretch_expression(joints=joint_chain,
                               curve_info_node=crv_info_node,
                               connect_scale=scale_stretch,
                               expression_name=ik_name + "_stretch_expression",
                               ctrl_attr=str(ctrl_jnts[-1]) + ".Stretch",
                               glbl_scl_stat=global_scale_check,
                               glbl_scl_attr=global_scale_attr,
                               control_obj=str(ctrl_jnts[-1]))

    final_group = pm.group(name=ik_name + "_ik_group", empty=True)
    pm.parent(joint_chain[0], final_group)
    pm.parent(crv, final_group)
    pm.parent(ik_handle, final_group)
    if ctrl_jnts > 1:
        pm.parent(ctr_jnt_gp, final_group)
    if create_dense_chain:
        pm.select(clear=True)
        dense_grp = pm.group(start_jnt, name="dense_chain_group")
        pm.parent(dense_grp, final_group)
    if obj:
        pm.scaleConstraint(obj, final_group)

    return None
