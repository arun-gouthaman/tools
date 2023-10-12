import pymel.all as pm
import random


class Controller_Setup(object):
    def __init__(self):
        self.color_list = [
            6, 10, 11, 12, 13, 14, 15, 17, 20, 21, 22, 23, 24, 25, 26, 27, 28,
            29, 30
        ]
        self.SUCCESS = 1
        self.FAIL = 0
        self.TYPE_ERROR = "invalid_type"
        return None

    def get_bound_parameters(self, **kwargs):
        bound_box = kwargs.get("bound", None)
        if not bound_box:
            return self.FAIL
        obj_type = str((type(bound_box))).split('.')[-1].replace("'>", "")
        if not obj_type == "BoundingBox":
            return self.TYPE_ERROR
        bound_box_param = [1, 1, 1]
        # x_width
        bound_box_param[0] = bound_box.width()
        # y_height
        bound_box_param[1] = bound_box.height()
        # z_depth
        bound_box_param[2] = bound_box.depth()
        return bound_box_param

    def parent_scale_const(self, **kwargs):
        obj = kwargs.get("cur_obj", None)
        ctr = kwargs.get("ctr", None)
        scl_flg = kwargs.get("scl_flg", False)
        pm.parentConstraint(obj, ctr, maintainOffset=True)
        if scl_flg:
            pm.scaleConstraint(obj, ctr, maintainOffset=True)
        return None

    def set_control_position(self, **kwargs):
        obj = kwargs.get("cur_obj", None)
        ctr = kwargs.get("ctr", None)
        tmp_con = pm.parentConstraint(obj, ctr, maintainOffset=False)
        pm.delete(tmp_con)
        return None

    def skin(self, **kwargs):
        obj = kwargs.get("cur_obj", None)
        ctr = kwargs.get("ctr", None)
        pm.select(clear=True)
        shp = obj.getShape()
        if not shp:
            shp = pm.ls(obj, dag=True, type=["mesh", "nurbsCurve"])
        else:
            shp = [shp]
        if shp:
            for item in shp:
                try:
                    pm.skinCluster(ctr, item)
                except Exception, e:
                    pm.displayWarning(str(e) + " Skipping skin bind operation")
        return None

    def scale_uniform(self, **kwargs):
        ctr = kwargs.get("ctr", None)
        size_offset = kwargs.get("size_offset", 0.5)
        cur_scl = ctr.getScale()
        new_scl = [
            cur_scl[0] + size_offset, cur_scl[1] + size_offset,
            cur_scl[2] + size_offset
        ]
        pm.scale(ctr, new_scl, objectCenterPivot=True, worldSpace=True)
        pm.makeIdentity(ctr, apply=True, scale=True)
        return None

    def scale_ctr_to_obj(self, **kwargs):
        obj = kwargs.get("cur_obj", None)
        ctr = kwargs.get("ctr", None)
        size_offset = kwargs.get("size_offset", 0.5)
        dup_obj = None
        attr_ip_chk = self.check_attr_input(chk_obj=obj)
        if attr_ip_chk:
            dup_obj = pm.duplicate(obj)[0]
            ch_nd = dup_obj.getChildren()
            sh_nd = dup_obj.getShape()
            for nd in ch_nd:
                if not nd == sh_nd:
                    pm.delete(nd)
            obj = dup_obj
        obj_bnd_bx = obj.getBoundingBox()
        obj_x_y_z_param = self.get_bound_parameters(bound=obj_bnd_bx)
        if obj_x_y_z_param == self.FAIL:
            pm.displayError("Bound parameters not obtained")
            return None
        ctr_bnd_bx = ctr.getBoundingBox()
        ctr_x_y_z_param = self.get_bound_parameters(bound=ctr_bnd_bx)
        if ctr_x_y_z_param == self.FAIL:
            pm.displayError("Bound parameters not obtained")
            return None
        scale_val = [1, 1, 1]
        for index in range(len(ctr_x_y_z_param)):
            if round(float(ctr_x_y_z_param[index]), 2) > 0:
                scale_val[index] = float(obj_x_y_z_param[index] /
                                         ctr_x_y_z_param[index]) + size_offset
            else:
                scale_val[index] = 1
        if dup_obj:
            pm.delete(dup_obj)
        pm.scale(ctr, scale_val, objectCenterPivot=True, worldSpace=True)
        pm.makeIdentity(ctr, apply=True, scale=True)
        return None

    def create_zero_group(self, **kwargs):
        ctr = kwargs.get("ctr", None)
        from_name = kwargs.get("from_nm", "")
        z_name = kwargs.get("zero_nm", "")
        if not z_name:
            z_name = "_ZeroNode"
        node_nm = str(ctr) + z_name
        grp_nd = pm.group(name="null", empty=True)
        if from_name:
            if str(ctr).find(from_name) > -1:
                node_nm = str(ctr).replace(from_name, z_name)
        self.set_control_position(cur_obj=ctr, ctr=grp_nd)
        pm.parent(ctr, grp_nd)
        pm.rename(grp_nd, node_nm)
        return None

    def rename_ctrl_from_obj(self, **kwargs):
        obj = kwargs.get("cur_obj", None)
        ctrl = kwargs.get("ctr", None)
        replace_from_str = kwargs.get("replace_from_str", "")
        replace_to_str = kwargs.get("replace_to_str", "")
        if not (obj) or not (ctrl):
            pm.displayError("Object and Control needed as input")
            return None
        ctr_nm = str(obj).replace(replace_from_str, replace_to_str)
        pm.rename(ctrl, ctr_nm)
        return None

    def get_boundary_position(self, **kwargs):
        bnd_bx = kwargs.get("bnd_bx", None)
        pos_sel = kwargs.get("pos_sel", None)
        if pos_sel == "Top(Y Axis)":
            return ((bnd_bx[1])[1])
        elif pos_sel == "Bottom(Y Axis)":
            return ((bnd_bx[0])[1])
        elif pos_sel == "Left(X Axis)":
            return ((bnd_bx[0])[0])
        elif pos_sel == "Right(X Axis)":
            return ((bnd_bx[1])[0])
        elif pos_sel == "Front(Z Axis)":
            return ((bnd_bx[1])[2])
        elif pos_sel == "Back(Z Axis)":
            return ((bnd_bx[0])[2])
        return None

    def name_control(self, **kwargs):
        ctrl = kwargs.get("ctr", None)
        ctrl_nm = kwargs.get("ctrl_nm", "")
        ctrl_sfx = kwargs.get("ctrl_sfx", "")
        id_val = kwargs.get("id_val", "")
        ctrl_new_nm = ctrl_nm + id_val + ctrl_sfx
        pm.rename(ctrl, ctrl_new_nm)
        return None

    def set_color(self, **kwargs):
        obj = kwargs.get("obj", None)
        if not obj:
            return None
        if isinstance(obj, list):
            obj = obj[0]
        obj = pm.PyNode(obj)
        sh = obj.getShape()
        sh.overrideEnabled.set(1)
        sh.overrideColor.set(random.choice(self.color_list))
        return None

    def lock_scale_vis_rad(self, **kwargs):
        ctrl = kwargs.get("ctr")
        ctrl.scale.setLocked(True)
        ctrl.visibility.setLocked(True)
        ctrl.scaleX.setKeyable(False)
        ctrl.scaleX.showInChannelBox(False)
        ctrl.scaleY.setKeyable(False)
        ctrl.scaleY.showInChannelBox(False)
        ctrl.scaleZ.setKeyable(False)
        ctrl.scaleZ.showInChannelBox(False)
        ctrl.visibility.setKeyable(False)
        ctrl.visibility.showInChannelBox(False)
        try:
            ctrl.radius.setLocked(True)
            ctrl.radius.setKeyable(False)
            ctrl.radius.showInChannelBox(False)
        except e:
            pm.displayWarning(e+"\nradius attribute not found")
        return None

    def check_attr_input(self, **kwargs):
        obj = kwargs.get("chk_obj", None)
        attr_lst = [".translate", ".rotate", ".scale"]
        axis_lst = ["X", "Y", "Z"]
        if not obj:
            return None
        for atr in attr_lst:
            for axis in axis_lst:
                obj_attr = str(obj) + atr + axis
                ip_connection = pm.connectionInfo(obj_attr,
                                                  sourceFromDestination=True)
                if ip_connection:
                    return ip_connection
        return None

    def run(self, **kwargs):
        obj = kwargs.get("cur_obj", None)
        ctrl = kwargs.get("cur_ctrl", None)
        ctr_mode = kwargs.get("ctr_mode", None).lower()
        con_opn = kwargs.get("con_opn", None)
        connect_ctrl = kwargs.get("connect_ctrl", None)
        from_txt = kwargs.get("from_txt", "")
        to_txt = kwargs.get("to_txt", "")
        ctrl_nm_opn = kwargs.get("ctrl_nm_opn", None)
        ctrl_nm_txt = kwargs.get("ctrl_nm_txt", "")
        ctrl_sufx = kwargs.get("ctrl_sfx_txt", "")
        zero_node_opn = kwargs.get("zero_node_opn", None)
        zero_node_nm = kwargs.get("zero_nd_nm", "")
        lock_scl_opn = kwargs.get("lock_scl_opn", None)
        scale_check = kwargs.get("scale_check", False)
        ctrl_sz_offset = str(kwargs.get("ctrl_sz_offset", "0.5"))
        id_num = str(kwargs.get("id_num", ""))
        position_flag = kwargs.get("obj_pos_flag", False)
        pos_sel_lbl = kwargs.get("pos_sel_lbl", None)
        try:
            ctrl_sz_offset = float(ctrl_sz_offset)
        except ValueError:
            pm.displayError("invalid input for size offset value")
            return None

        z_frm_txt = ""
        if ctrl_nm_opn:
            z_frm_txt = ctrl_sufx
        else:
            z_frm_txt = to_txt

        self.set_control_position(cur_obj=obj, ctr=ctrl)

        if not position_flag:
            bound_box = obj.getBoundingBox()
            pos = self.get_boundary_position(bnd_bx=bound_box,
                                             pos_sel=pos_sel_lbl)
            ctr_pos = pm.xform(ctrl,
                               query=True,
                               translation=True,
                               worldSpace=True)
            if pos_sel_lbl.find("X") > -1:
                ctr_pos[0] = pos
            elif pos_sel_lbl.find("Y") > -1:
                ctr_pos[1] = pos
            elif pos_sel_lbl.find("Z") > -1:
                ctr_pos[2] = pos

            #base_location = (bound_box[0])[1]
            ctrl.translate.set(ctr_pos)

        if scale_check:
            self.scale_ctr_to_obj(cur_obj=obj,
                                  ctr=ctrl,
                                  size_offset=ctrl_sz_offset)
        else:
            self.scale_uniform(ctr=ctrl, size_offset=ctrl_sz_offset)

        if not ctrl_nm_opn:
            self.rename_ctrl_from_obj(cur_obj=obj,
                                      ctr=ctrl,
                                      replace_from_str=from_txt,
                                      replace_to_str=to_txt)
        else:
            self.name_control(ctr=ctrl,
                              ctrl_nm=ctrl_nm_txt,
                              ctrl_sfx=ctrl_sufx,
                              id_val=id_num)

        if zero_node_opn:
            self.create_zero_group(ctr=ctrl,
                                   from_nm=z_frm_txt,
                                   zero_nm=zero_node_nm)

        if connect_ctrl:
            if ctr_mode == "skin":
                self.skin(cur_obj=obj, ctr=ctrl)
            else:
                if con_opn[0]:
                    pm.parentConstraint(ctrl, obj, maintainOffset=True)
                if con_opn[1]:
                    pm.scaleConstraint(ctrl, obj, maintainOffset=True)

        if lock_scl_opn:
            self.lock_scale_vis_rad(ctr=ctrl)

        return None
