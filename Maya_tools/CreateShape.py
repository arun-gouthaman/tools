import pymel.all as pm
import Shapes
import ControllerSetup
import random
from functools import partial
import os
import GetCurPath


class Create_Shape():
    def __init__(self):
        reload(Shapes)
        current_path_obj = GetCurPath.Get_Cur_Path()
        self.current_path = current_path_obj.get_cur_path()
        self.icon_path = self.current_path + "\\" + "Ctrl_Icons"
        self.shape_list_path = self.current_path + "\\" + "shape_list.txt"
        self.shape_script_path = self.current_path + "\\" + "Shapes.py"
        self.shp_obj = Shapes.Shapes_Class()
        self.create_control_ui()
        self.setup_obj = ControllerSetup.Controller_Setup()
        self.ctrl_lst = []
        return None

    def read_shapes(self):
        list_file = open(self.shape_list_path, "r")
        file_text = list_file.readlines()
        btns = []
        for ln in file_text:
            btns.append(ln)
        return btns

    def create_joint(self, **kwargs):
        crv = kwargs.get("crv_node", "")
        if isinstance(crv, list):
            crv = pm.PyNode(crv[0])
        crv = pm.PyNode(crv)
        shp = crv.getShape()
        pm.select(clear=True)
        ctr = pm.joint()
        pm.parent(shp, ctr, relative=True, shape=True)
        pm.delete(crv)
        return ctr

    def create_shape(self, **kwargs):
        nm = kwargs.get("nm", None)
        fun_nm = getattr(self.shp_obj, nm)
        sel = pm.ls(selection=True)
        id_val = ""
        ctrl = None
        if not sel:
            crv = fun_nm()
            self.setup_obj.set_color(obj=crv)
            if self.get_joint_shape():
                ctrl = self.create_joint(crv_node=crv)
            else:
                ctrl = crv
            if self.get_ctrl_nm_chk():
                self.setup_obj.name_control(ctr=ctrl,
                                            ctrl_nm=self.get_control_name(),
                                            ctrl_sfx=self.get_suffix_name())
            if self.get_zero_node_flag():
                frm_nm = ""
                if self.get_ctrl_nm_chk():
                    frm_nm = self.get_suffix_name()
                self.setup_obj.create_zero_group(
                    ctr=ctrl,
                    from_nm=frm_nm,
                    zero_nm=self.get_zero_node_name())
            return None
        if len(sel) > 1:
            id_val = 1
        for obj in sel:
            ctr = None
            ctr_crv = fun_nm()
            self.setup_obj.set_color(obj=ctr_crv)
            if isinstance(ctr_crv, list):
                ctr_crv = ctr_crv[0]
            if not isinstance(ctr_crv, pm.PyNode):
                ctr_crv = pm.PyNode(ctr_crv)
            if self.get_joint_shape():
                ctr = self.create_joint(crv_node=ctr_crv)
            else:
                ctr = ctr_crv
            self.ctrl_lst.append(ctr)
            self.setup_obj.run(cur_obj=obj,
                               cur_ctrl=ctr,
                               ctr_mode=self.get_ctrl_type(),
                               con_opn=self.get_const_opn(),
                               connect_ctrl=self.get_connect_mode(),
                               from_txt=self.get_from_text(),
                               to_txt=self.get_to_text(),
                               ctrl_nm_opn=self.get_ctrl_nm_chk(),
                               ctrl_nm_txt=self.get_control_name(),
                               ctrl_sfx_txt=self.get_suffix_name(),
                               zero_node_opn=self.get_zero_node_flag(),
                               zero_nd_nm=self.get_zero_node_name(),
                               lock_scl_opn=self.get_lock_scale(),
                               scale_check=self.get_scale_check_flg(),
                               ctrl_sz_offset=self.get_ctrl_sale_offset_val(),
                               obj_pos_flag=self.get_control_position_val(),
                               pos_sel_lbl=self.get_position_selection(),
                               id_num=id_val)
            if id_val:
                id_val += 1
        sel = None
        return None

    def add_ctr(self, **kwargs):
        cmd = kwargs.get("cmd", "")
        nm = kwargs.get("nm", "")
        if not nm:
            pm.displayError("Please enter Shape name")
            return None
        if not cmd:
            pm.displayError("Please enter mel command to create shape")
            return None
        btn_exist = self.read_shapes()
        if nm in btn_exist:
            pm.displayError("Shape name already exists")
            return None
        ind = "    "
        cmd_str = "\n\n" + ind + "def " + nm + "(self):\n    "
        cmd_str += ind + "shp = mel.eval('" + cmd + "')\n"
        cmd_str += ind + "    return shp"
        shape_file = open(self.shape_script_path, "a")
        shape_file.write(cmd_str)
        shape_file.close()
        list_file = open(self.shape_list_path, "a")
        list_file.write("\n")
        list_file.write(nm)
        reload(Shapes)
        return None

    def get_connect_mode(self):
        con_mode = self.connect_chk_bx.getValue()
        return con_mode

    def get_ctrl_type(self):
        sel_option = self.ctr_typ_rad_collection.getSelect()
        option_label = pm.radioButton(sel_option, query=True, label=True)
        return option_label

    def get_const_opn(self):
        pr_chk = self.pr_chk_bx.getValue()
        sc_chk = self.sc_chk_bx.getValue()
        return [pr_chk, sc_chk]

    def get_joint_shape(self):
        return self.jnt_cr_chk_bx.getValue()

    def get_from_text(self):
        return self.msh_nm.getText()

    def get_to_text(self):
        return self.ctrl_nm.getText()

    def get_ctrl_nm_chk(self):
        return self.new_nm_chk_bx.getValue()

    def get_control_name(self):
        return self.ctr_new_nm.getText()

    def get_suffix_name(self):
        return self.suf_nm.getText()

    def get_zero_node_flag(self):
        return self.zero_gp_chk_bx.getValue()

    def get_lock_scale(self):
        return self.scl_lk_chk_bx.getValue()

    def get_zero_node_name(self):
        return self.zero_nd_txt.getText()

    def get_scale_check_flg(self):
        return self.scl_ctr_chk_bx.getValue()

    def get_ctrl_sale_offset_val(self):
        return self.scl_offset_val_txt.getText()

    def get_control_position_val(self):
        return self.ctrl_pos_chk_bx.getValue()

    def get_position_selection(self):
        sel_opn = self.pos_rad_collection.getSelect()
        option_label = pm.radioButton(sel_opn, query=True, label=True)
        return option_label

    def open_help(self):
        import webbrowser
        file_path = self.current_path + "\\CreateControl_Help.txt"
        webbrowser.open(file_path)
        return None

    def set_ui_edit_mode(self, **kwargs):
        flag = kwargs.get("flag", None)

        if flag == "position":
            val = self.ctrl_pos_chk_bx.getValue()
            self.top_rad_btn.setEditable(not (val))
            self.bot_rad_btn.setEditable(not (val))
            self.left_rad_btn.setEditable(not (val))
            self.right_rad_btn.setEditable(not (val))
            self.front_rad_btn.setEditable(not (val))
            self.back_rad_btn.setEditable(not (val))
            return None

        if flag == "no_joint":
            val = self.connect_chk_bx.getValue()
            self.skin_rad_btn.setSelect(False)
            self.con_rad_btn.setSelect(True)
            self.pr_chk_bx.setEditable(val)
            self.sc_chk_bx.setEditable(val)
            return None

        if flag == "connect":
            val = self.connect_chk_bx.getValue()
            self.skin_rad_btn.setEditable(val)
            self.con_rad_btn.setEditable(val)
            if self.get_ctrl_type().lower() == "skin":
                self.pr_chk_bx.setEditable(False)
                self.sc_chk_bx.setEditable(False)
            else:
                self.pr_chk_bx.setEditable(True * val)
                self.sc_chk_bx.setEditable(True * val)
            return None

        if flag == "rename_field":
            rename_val = self.new_nm_chk_bx.getValue()
            self.ctr_new_nm.setEditable(rename_val)
            self.ctr_new_nm.setEnable(rename_val)
            self.msh_nm.setEditable(not (rename_val))
            self.msh_nm.setEnable(not (rename_val))
            self.ctrl_nm.setEditable(not (rename_val))
            self.ctrl_nm.setEnable(not (rename_val))
            self.suf_lbl.setEnable(not (rename_val))
            self.msh_nm_lbl.setEnable(not (rename_val))
            self.ctrl_nm_lbl.setEnable(not (rename_val))
            self.suf_lbl.setEnable(rename_val)
            self.suf_nm.setEditable(rename_val)
            self.suf_nm.setEnable(rename_val)
            return None

        if flag == "zero_node":
            val = self.zero_gp_chk_bx.getValue()
            self.zero_nd_txt.setEditable(val)
            self.zero_nd_txt.setEnable(val)
            return None

        if flag == "no_scale":
            val = self.scl_ctr_chk_bx.getValue()
            self.ctrl_nm_lbl.setEnable(val)
            return None

        if flag.lower() == "skin":
            self.pr_chk_bx.setEditable(False)
            self.sc_chk_bx.setEditable(False)
            self.jnt_cr_chk_bx.setValue(True)
        else:
            self.pr_chk_bx.setEditable(True)
            self.sc_chk_bx.setEditable(True)
        return None

    def create_control_ui(self):
        btns = self.read_shapes()
        WINDOW = "create_control"
        chk_win = pm.window(WINDOW, query=True, exists=True)
        if chk_win:
            pm.deleteUI(WINDOW)
        pm.window(WINDOW, title="Create_Control", iconName="CC")

        main_split_col = pm.rowColumnLayout(parent=WINDOW, numberOfColumns=3)

        left_main_col = pm.columnLayout(parent=main_split_col,
                                        adjustableColumn=True)
        hlp_btn_col = pm.columnLayout(parent=left_main_col,
                                      columnOffset=("left", 110))
        pm.button("?",
                  parent=hlp_btn_col,
                  width=50,
                  command=lambda x: self.open_help())

        pm.separator(parent=left_main_col, style="in", height=10)
        con_obj_col = pm.columnLayout(parent=left_main_col,
                                      columnOffset=("left", 70))
        self.connect_chk_bx = pm.checkBox("Skinning/Constraint",
                                          parent=con_obj_col,
                                          value=True)
        pm.separator(parent=left_main_col, style="none")
        ctrl_typ_col = pm.rowColumnLayout(parent=left_main_col,
                                          numberOfColumns=3,
                                          columnOffset=(1, "left", 20),
                                          columnSpacing=(2, 10))
        pm.text("Control type", parent=ctrl_typ_col)
        rad_col = pm.columnLayout(parent=ctrl_typ_col)
        self.ctr_typ_rad_collection = pm.radioCollection(parent=rad_col)
        self.skin_rad_btn = pm.radioButton(
            label='Skin',
            parent=rad_col,
            select=True,
            onCommand=lambda x: self.set_ui_edit_mode(flag="Skin"))
        self.con_rad_btn = pm.radioButton(
            label='Constraint',
            parent=rad_col,
            onCommand=lambda x: self.set_ui_edit_mode(flag="Constraint"))
        con_typ_col = pm.columnLayout(parent=ctrl_typ_col)
        self.pr_chk_bx = pm.checkBox("Parent",
                                     parent=con_typ_col,
                                     value=True,
                                     editable=False)
        self.sc_chk_bx = pm.checkBox("Scale",
                                     parent=con_typ_col,
                                     editable=False)
        jnt_opn_col = pm.columnLayout(parent=left_main_col,
                                      columnOffset=("left", 100))
        self.jnt_cr_chk_bx = pm.checkBox(
            label="Create Joint",
            value=True,
            parent=jnt_opn_col,
            offCommand=lambda x: self.set_ui_edit_mode(flag="no_joint"))

        pm.separator(parent=left_main_col, height=10, style="in")
        pm.text("Control name", parent=left_main_col)
        re_name_col = pm.gridLayout(parent=left_main_col,
                                    numberOfRowsColumns=(2, 2),
                                    cellWidthHeight=(138, 20),
                                    allowEmptyCells=False)
        self.msh_nm_lbl = pm.text("Text from Mesh Name", parent=re_name_col)
        self.ctrl_nm_lbl = pm.text("Rename to Control", parent=re_name_col)
        self.msh_nm = pm.textField(text="_MSH", parent=re_name_col)
        self.ctrl_nm = pm.textField(text="_CTRL", parent=re_name_col)
        pm.separator(parent=left_main_col, height=10, style="none")
        new_name_col = pm.rowColumnLayout(parent=left_main_col,
                                          numberOfColumns=2,
                                          columnOffset=(1, "left", 10))
        self.new_nm_chk_bx = pm.checkBox(
            label="Control Name:    ",
            parent=new_name_col,
            changeCommand=lambda x: self.set_ui_edit_mode(flag="rename_field"))
        self.ctr_new_nm = pm.textField(text="Control",
                                       parent=new_name_col,
                                       width=150,
                                       editable=False)
        suf_name_col = pm.rowColumnLayout(parent=left_main_col,
                                          numberOfColumns=2,
                                          columnOffset=(1, "left", 10))
        self.suf_lbl = pm.text("Control Suffix Text:  ", parent=suf_name_col)
        self.suf_nm = pm.textField(text="_CTRL",
                                   parent=suf_name_col,
                                   width=163,
                                   editable=False)
        pm.separator(parent=left_main_col, height=10, style="none")
        zero_gp_col = pm.rowColumnLayout(parent=left_main_col,
                                         numberOfColumns=2,
                                         columnOffset=(1, "left", 50))
        self.zero_gp_chk_bx = pm.checkBox(
            "Zero Node",
            parent=zero_gp_col,
            value=True,
            changeCommand=lambda x: self.set_ui_edit_mode(flag="zero_node"))
        self.zero_nd_txt = pm.textField(text="_CTRLT", parent=zero_gp_col)

        scl_lk_col = pm.columnLayout(parent=left_main_col,
                                     columnOffset=("left", 50))
        self.scl_lk_chk_bx = pm.checkBox("Lock Scale/Visibility/Radius(Joint)",
                                         parent=scl_lk_col,
                                         value=True)
        scl_chk_col = pm.columnLayout(parent=left_main_col,
                                      columnOffset=("left", 50))
        self.scl_ctr_chk_bx = pm.checkBox(
            "Scale Control to match object",
            value=True,
            parent=scl_chk_col,
            changeCommand=lambda x: self.set_ui_edit_mode(flag="no_scale"))
        scl_offset_col = pm.rowColumnLayout(parent=left_main_col,
                                            numberOfColumns=2,
                                            columnOffset=(1, "left", 30))
        self.ctrl_off_sz_lbl = pm.text("Control size offset value",
                                       parent=scl_offset_col)
        self.scl_offset_val_txt = pm.textField(text="1", parent=scl_offset_col)

        pm.separator(parent=left_main_col, height=10, style="in")
        ctrl_pvt_col = pm.rowColumnLayout(parent=left_main_col,
                                          numberOfColumns=2,
                                          columnOffset=(1, "left", 80))
        self.ctrl_pos_chk_bx = pm.checkBox(
            "Control at object pivot",
            parent=ctrl_pvt_col,
            value=True,
            changeCommand=lambda x: self.set_ui_edit_mode(flag="position"))

        pos_rad_col = pm.gridLayout(parent=left_main_col,
                                    numberOfRowsColumns=(3, 2),
                                    cellWidthHeight=(140, 20),
                                    allowEmptyCells=False)

        self.pos_rad_collection = pm.radioCollection(parent=pos_rad_col)
        self.top_rad_btn = pm.radioButton(label="Top(Y Axis)",
                                          parent=pos_rad_col,
                                          editable=False)
        self.bot_rad_btn = pm.radioButton(label="Bottom(Y Axis)",
                                          parent=pos_rad_col,
                                          select=True,
                                          editable=False)
        self.left_rad_btn = pm.radioButton(label="Left(X Axis)",
                                           parent=pos_rad_col,
                                           editable=False)
        self.right_rad_btn = pm.radioButton(label="Right(X Axis)",
                                            parent=pos_rad_col,
                                            editable=False)
        self.front_rad_btn = pm.radioButton(label="Front(Z Axis)",
                                            parent=pos_rad_col,
                                            editable=False)
        self.back_rad_btn = pm.radioButton(label="Back(Z Axis)",
                                           parent=pos_rad_col,
                                           editable=False)

        pm.separator(parent=main_split_col,
                     height=10,
                     style="in",
                     horizontal=False)
        scr_lay = pm.scrollLayout(parent=main_split_col)
        grid_col = pm.gridLayout(parent=scr_lay,
                                 numberOfRowsColumns=(1, 5),
                                 autoGrow=True,
                                 cellWidthHeight=(50, 50),
                                 allowEmptyCells=False)
        for btn in btns:
            btn = btn.replace("\r", "")
            btn = btn.replace("\n", "")
            img = self.icon_path + btn + ".png"
            if os.path.exists(img):
                pm.iconTextButton(parent=grid_col,
                                  label=btn,
                                  style='iconOnly',
                                  image=img,
                                  command=partial(self.create_shape, nm=btn))
            else:
                rgb = [
                    random.uniform(.5, 1),
                    random.uniform(.5, 1),
                    random.uniform(.5, 1)
                ]
                pm.iconTextButton(parent=grid_col,
                                  label=btn,
                                  style='iconAndTextVertical',
                                  backgroundColor=rgb,
                                  command=partial(self.create_shape, nm=btn))
        pm.checkBox(
            self.connect_chk_bx,
            edit=True,
            changeCommand=lambda x: self.set_ui_edit_mode(flag="connect"))
        pm.showWindow(WINDOW)
        pm.window(WINDOW, edit=True, widthHeight=(540, 420))
        return None
