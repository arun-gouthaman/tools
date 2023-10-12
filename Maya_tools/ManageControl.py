import pymel.all as pm
import GetCurPath


class Manage_Control():
    def __init__(self):
        self.EXISTS = "exists"
        current_path_obj = GetCurPath.Get_Cur_Path()
        self.current_path = current_path_obj.get_cur_path()
        self.shape_path = self.current_path + "\\Shapes.py"
        self.list_path = self.current_path + "\\shape_list.txt"
        self.shapes_script = self.read_file(file_name=self.shape_path)
        self.shapes_list = self.read_file(file_name=self.list_path)
        self.manage_shape_ui()
        self.populate_shape_list()
        return None

    def get_stripped_text(self, **kwargs):
        ip_txt = kwargs.get("ip_txt", "")
        ip_txt = ((str(ip_txt).strip()).replace("\n", "")).replace("\r", "")
        return ip_txt

    def populate_shape_list(self):
        self.shp_lst_bx.removeAll()
        for shp in self.shapes_list:
            shp = self.get_stripped_text(ip_txt=shp)
            self.shp_lst_bx.append(shp)
        return None

    def get_selection_from_list(self):
        sel_items = self.shp_lst_bx.getSelectItem()
        ret_lst = []
        for item in sel_items:
            item = self.get_stripped_text(ip_txt=item)
            ret_lst.append(item)
        return ret_lst

    def check_exists_in_list(self, **kwargs):
        existing_list = kwargs.get("existing_list", [])
        new_text = kwargs.get("new_text", "")
        for btn_nm in existing_list:
            btn_nm = self.get_stripped_text(ip_txt=btn_nm)
            if btn_nm == new_text:
                return self.EXISTS
        return None

    def rename_selection(self, **kwargs):
        new_name = kwargs.get("new_name", "")
        sel_items = self.get_selection_from_list()[0]
        sel_items = self.get_stripped_text(ip_txt=sel_items)

        check_exists = self.check_exists_in_list(
            existing_list=self.shapes_list, new_text=new_name)
        if check_exists == self.EXISTS:
            pm.displayError("Shape name already exists")
            return None

        new_lst = []
        for ln in self.shapes_list:
            check = self.get_stripped_text(ip_txt=ln)
            if check == sel_items:
                new_lst.append(new_name + "\n")
            else:
                new_lst.append(ln)
        new_lst[-1] = self.get_stripped_text(ip_txt=new_lst[-1])
        self.rewrite_file(file_name=self.list_path, txt=new_lst)

        self.shapes_script = self.read_file(file_name=self.shape_path)
        new_txt = []
        check_txt = "def " + sel_items + "(self):"
        for ln in self.shapes_script:
            if ln.find(check_txt) > -1:
                ln = ln.replace(sel_items, new_name)
            new_txt.append(ln)
        new_txt[-1] = (new_txt[-1].replace("\n", "")).replace("\r", "")
        self.rewrite_file(file_name=self.shape_path, txt=new_txt)
        import Shapes
        reload(Shapes)
        self.shapes_list = self.read_file(file_name=self.list_path)
        self.populate_shape_list()
        return None

    def delete_selection(self):
        sel_items = self.get_selection_from_list()
        for shp in sel_items:
            self.remove_ctrl(control_name=shp)
        import Shapes
        reload(Shapes)
        self.shapes_list = self.read_file(file_name=self.list_path)
        self.populate_shape_list()
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
        btn_exist = self.read_file(file_name=self.list_path)
        nm = self.get_stripped_text(ip_txt=nm)
        if nm.find(" ") > -1:
            pm.displayError("Names cannot contain spaces")
            return None
        check_name = self.check_exists_in_list(existing_list=btn_exist,
                                               new_text=nm)
        if check_name == self.EXISTS:
            pm.displayError("Shape name already exists")
            return None
        ind = "    "
        cmd_str = "\n\n" + ind + "def " + nm + "(self):\n    "
        cmd_str += ind + "shp = mel.eval('" + cmd + "')\n"
        cmd_str += ind + "    return shp"
        shape_file = open(self.shape_path, "a")
        shape_file.write(cmd_str)
        shape_file.close()
        list_file = open(self.list_path, "a")
        list_file.write("\n")
        list_file.write(nm)
        list_file.close()
        import Shapes
        reload(Shapes)
        self.shapes_list = self.read_file(file_name=self.list_path)
        self.populate_shape_list()
        return None

    def read_file(self, **kwargs):
        file_name = kwargs.get("file_name", None)
        shape_file = open(file_name, "r")
        file_text = shape_file.readlines()
        shape_file.close()
        return file_text

    def rewrite_file(self, **kwargs):
        file_name = kwargs.get("file_name", "")
        txt = kwargs.get("txt", "")
        cur_file = open(file_name, "w")
        if isinstance(txt, str):
            cur_file.write(txt)
            return None
        for ln in txt:
            check = (str(ln).replace("\n", "")).replace("\r", "")
            if not check:
                continue
            if ln:
                if ln.find("def") > -1:
                    cur_file.write("\n")
                cur_file.write(ln)
        cur_file.close()
        return None

    def remove_ctrl(self, **kwargs):
        control_name = kwargs.get("control_name", "")
        shape_text = self.read_file(file_name=self.shape_path)
        new_txt = []
        flag = 1
        for ln in shape_text:
            if ln.find("def " + control_name) > -1:
                flag = 0
            if not flag and ln.find("return") > -1:
                flag = 1
                continue
            if not flag:
                continue
            if (ln.replace("\n", "")).replace("\r", ""):
                new_txt.append(ln)
        new_txt[-1] = (new_txt[-1].replace("\n", "")).replace("\r", "")
        self.rewrite_file(file_name=self.shape_path, txt=new_txt)

        list_text = self.read_file(file_name=self.list_path)
        new_lst = []
        for ln in list_text:
            chk_txt = (ln.replace("\n", "")).replace("\r", "")
            print repr(control_name), "---", repr(ln)
            if chk_txt == control_name:
                continue
            new_lst.append(ln)
        new_lst[-1] = (new_lst[-1].replace("\n", "")).replace("\r", "")
        self.rewrite_file(file_name=self.list_path, txt=new_lst)
        return None

    def manage_shape_ui(self):
        WINDOW = "add_control"
        chk_win = pm.window(WINDOW, query=True, exists=True)
        if chk_win:
            pm.deleteUI(WINDOW)
        pm.window(WINDOW, title="Manage_Shapes", iconName="MS")
        main_col = pm.columnLayout(parent=WINDOW, adjustableColumn=True)

        main_split_col = pm.rowColumnLayout(parent=main_col,
                                            numberOfColumns=2,
                                            columnOffset=(2, "left", 5))
        cmd_col = pm.columnLayout(parent=main_split_col)
        pm.separator(parent=main_col, height=10)
        mel_cmd_col = pm.columnLayout(parent=cmd_col,
                                      columnOffset=("left", 10))
        pm.text("\t\t\t\tShape Name", parent=mel_cmd_col)
        nm_txt = pm.textField(text="", parent=mel_cmd_col, width=300)
        pm.text("\t\t\t\tShape mel command", parent=mel_cmd_col)
        txt = pm.scrollField("",
                             wordWrap=True,
                             parent=mel_cmd_col,
                             height=130,
                             width=300)
        pm.separator(parent=main_col, height=10)
        add_btn_col = pm.columnLayout(parent=cmd_col,
                                      columnOffset=("left", 100))
        pm.button("add",
                  parent=add_btn_col,
                  width=100,
                  command=lambda x: self.add_ctr(cmd=txt.getText(),
                                                 nm=nm_txt.getText()))

        list_col = pm.columnLayout(parent=main_split_col)
        pm.text("\t\tExisting Shapes", parent=list_col)
        self.shp_lst_bx = pm.textScrollList(parent=list_col,
                                            height=165,
                                            width=170)

        edit_btn_col = pm.rowColumnLayout(numberOfColumns=3, parent=list_col)
        pm.button("Delete",
                  parent=edit_btn_col,
                  width=82,
                  command=lambda x: self.delete_selection())
        pm.separator(parent=edit_btn_col, horizontal=False)
        pm.button("rename",
                  parent=edit_btn_col,
                  width=82,
                  command=lambda x: self.rename_ui())

        pm.showWindow(WINDOW)
        pm.window(WINDOW, edit=True, widthHeight=(500, 220))
        return None

    def rename_ui(self, **kwargs):
        self.rename_ip = pm.promptDialog(title="Rename Object",
                                         message="Enter name",
                                         button=["Ok", "Cancel"],
                                         cancelButton="Cancel",
                                         dismissString="Cancel")
        if self.rename_ip == "Ok":
            txt = pm.promptDialog(query=True, text=True)
            txt = self.get_stripped_text(ip_txt=txt)
            if txt.find(" ") > -1:
                pm.displayError("Names cannot contain spaces")
                return None
            self.rename_selection(new_name=txt)
