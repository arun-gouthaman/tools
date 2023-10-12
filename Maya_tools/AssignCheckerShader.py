import pymel.all as pm


class AssignShader(object):
    def __init__(self):
        # Edit the path and file name as per file structure
        self.tex_path = "E:\\Pics\\test\\"
        self.tex_dict = {
            "myChLambert1": "1.jpg",
            "myChLambert2": "2.jpg",
            "myChLambert3": "3.jpg",
            "myChLambert4": "4.jpg",
            "myChLambert5": "5.jpg"
        }
        self.UI()
        self.init_read()

    def init_read(self):
        '''
        check for existing shaders with specific names and display the
        UV tile values
        '''
        if pm.objExists("myChLambert1"):
            self.disp_uv_tile_val("myChLambert1", self.ch1_U_tx, self.ch1_V_tx)
        if pm.objExists("myChLambert2"):
            self.disp_uv_tile_val("myChLambert2", self.ch2_U_tx, self.ch2_V_tx)
        if pm.objExists("myChLambert3"):
            self.disp_uv_tile_val("myChLambert3", self.ch3_U_tx, self.ch3_V_tx)
        if pm.objExists("myChLambert4"):
            self.disp_uv_tile_val("myChLambert4", self.ch4_U_tx, self.ch4_V_tx)
        if pm.objExists("myChLambert5"):
            self.disp_uv_tile_val("myChLambert5", self.ch5_U_tx, self.ch5_V_tx)
        return None

    def create_shader(self, sh):
        lamb = pm.shadingNode("lambert", asShader=True, name=sh)
        tex_nd = pm.shadingNode("file",
                                asTexture=True,
                                name=sh + "_fileTexture")
        tex_nd.fileTextureName.set(self.tex_path + self.tex_dict[sh])
        tex2d_nd = pm.shadingNode("place2dTexture",
                                  asUtility=True,
                                  name=sh + "_2dTex")

        att_list = [
            ".vertexUvOne", ".rotateUV", ".offset", ".repeatUV", ".stagger",
            ".wrapV", ".mirrorU", ".mirrorV", ".coverage", ".wrapU",
            ".vertexCameraOne", ".vertexUvThree", ".rotateFrame",
            ".vertexUvTwo", ".translateFrame", ".noiseUV"
        ]

        pm.connectAttr(str(tex2d_nd) + ".outUV", str(tex_nd) + ".uv")
        pm.connectAttr(
            str(tex2d_nd) + ".outUvFilterSize",
            str(tex_nd) + ".uvFilterSize")
        for att in att_list:
            pm.connectAttr(str(tex2d_nd) + att, str(tex_nd) + att)

        tex_nd.outColor.connect(lamb.color)
        return None

    def assign_shader(self, sh, Utile, Vtile):
        self.sel = pm.ls(selection=True)
        if not pm.objExists(sh):
            self.create_shader(sh)
        pm.select(self.sel)
        pm.hyperShade(assign=pm.PyNode(sh))
        self.disp_uv_tile_val(sh, Utile, Vtile)
        return None

    def copy_shader(self):
        cp_sel = pm.ls(selection=True)
        sel_shader = None
        sh_eng = pm.ls(pm.listHistory(cp_sel[0], f=1), type="shadingEngine")[0]
        if sh_eng:
            sel_shader = pm.listConnections(str(sh_eng) + ".surfaceShader")[0]
        if sel_shader:
            pm.hyperShade(cp_sel[1], assign=sel_shader)
        return None

    def delete_shader(self, sh, Utile, Vtile):

        if not pm.objExists(sh):
            pm.displayWarning("Shader does not exist")
            return None

        # get the shading engine connected
        sh_con = pm.listConnections(sh + ".outColor")
        obj = None
        for con in sh_con:
            print(con)
            # find the mesh connected with the shading engine
            obj = pm.listConnections(con, type="mesh")

        pm.delete(sh)
        pm.delete(sh + "_fileTexture")
        pm.delete(sh_con)
        pm.delete(sh + "_2dTex")
        if obj:
            pm.select(obj)
            pm.hyperShade(assign="lambert1")
        self.clear_uv_tile_val(sh, Utile, Vtile)
        return None

    def tile_uv_val(self, sh, U, V, Uval, Vval, inc, uText, vText):
        tex = pm.PyNode(sh + "_2dTex")
        if not pm.objExists(tex):
            pm.displayError("texture does not exist")
            return None
        if U:
            if Uval:
                u_val = float(Uval.getText())
                tex.repeatU.set(u_val)
            else:
                u_val = tex.repeatU.get()
                if inc:
                    tex.repeatU.set(u_val + 1)
                else:
                    if (u_val - 1) > 0:
                        tex.repeatU.set(u_val - 1)

        if V:
            if Vval:
                v_val = float(Vval.getText())
                tex.repeatV.set(v_val)
            else:
                v_val = tex.repeatV.get()
                if inc:
                    tex.repeatV.set(v_val + 1)
                else:
                    if (v_val - 1) > 0:
                        tex.repeatV.set(v_val - 1)

        if uText or vText:
            self.disp_uv_tile_val(sh, uText, vText)
        return None

    def disp_uv_tile_val(self, sh, Utile, Vtile):
        tex = pm.PyNode(sh + "_2dTex")
        if Utile:
            Utile.setText(tex.repeatU.get())
        if Vtile:
            Vtile.setText(tex.repeatV.get())
        return None

    def clear_uv_tile_val(self, sh, Utile, Vtile):
        if Utile:
            Utile.setText("")
        if Vtile:
            Vtile.setText("")
        return None

    def UI(self):
        self.WINDOW = "Checker_Material"
        if pm.window(self.WINDOW, query=True, exists=True):
            pm.deleteUI(self.WINDOW)
        pm.window(self.WINDOW,
                  title="Checker Material",
                  iconName="CHM",
                  widthHeight=(290, 110))
        self.main_col = pm.columnLayout(adjustableColumn=True,
                                        height=100,
                                        parent=self.WINDOW)

        self.button_col = pm.rowColumnLayout(parent=self.main_col,
                                             numberOfColumns=9)
        pm.separator(parent=self.main_col, style="in")
        self.del_col = pm.rowColumnLayout(parent=self.main_col,
                                          numberOfColumns=9)
        pm.separator(parent=self.main_col, style="in")
        self.uv_ch_col = pm.rowColumnLayout(parent=self.main_col,
                                            numberOfColumns=9)
        pm.separator(parent=self.main_col, style="in")
        self.uv_ful_ch_col = pm.rowColumnLayout(parent=self.main_col,
                                                numberOfColumns=9)
        pm.separator(parent=self.main_col, style="in")
        self.copy_btn_col = pm.columnLayout(parent=self.main_col,
                                            adjustableColumn=True)

        self.tex1_but = pm.button(
            label="checker1",
            parent=self.button_col,
            height=50,
            command=lambda x: self.assign_shader("myChLambert1", self.ch1_U_tx,
                                                 self.ch1_V_tx))
        pm.separator(parent=self.button_col, horizontal=False, style="in")
        self.tex2_but = pm.button(
            label="checker2",
            parent=self.button_col,
            height=50,
            command=lambda x: self.assign_shader("myChLambert2", self.ch2_U_tx,
                                                 self.ch2_V_tx))
        pm.separator(parent=self.button_col, horizontal=False, style="in")
        self.tex3_but = pm.button(
            label="checker3",
            parent=self.button_col,
            height=50,
            command=lambda x: self.assign_shader("myChLambert3", self.ch3_U_tx,
                                                 self.ch3_V_tx))
        pm.separator(parent=self.button_col, horizontal=False, style="in")
        self.tex4_but = pm.button(
            label="checker4",
            parent=self.button_col,
            height=50,
            command=lambda x: self.assign_shader("myChLambert4", self.ch4_U_tx,
                                                 self.ch4_V_tx))
        pm.separator(parent=self.button_col, horizontal=False, style="in")
        self.tex5_but = pm.button(
            label="checker5",
            parent=self.button_col,
            height=50,
            command=lambda x: self.assign_shader("myChLambert5", self.ch5_U_tx,
                                                 self.ch5_V_tx))

        self.del1_but = pm.button(
            label="delete\nchecker1",
            parent=self.del_col,
            height=50,
            width=55,
            command=lambda x: self.delete_shader("myChLambert1", self.ch1_U_tx,
                                                 self.ch1_V_tx))
        pm.separator(parent=self.del_col, horizontal=False, style="in")

        self.del2_but = pm.button(
            label="delete\nchecker2",
            parent=self.del_col,
            height=50,
            width=55,
            command=lambda x: self.delete_shader("myChLambert2", self.ch2_U_tx,
                                                 self.ch2_V_tx))
        pm.separator(parent=self.del_col, horizontal=False, style="in")

        self.del3_but = pm.button(
            label="delete\nchecker3",
            parent=self.del_col,
            height=50,
            width=55,
            command=lambda x: self.delete_shader("myChLambert3", self.ch3_U_tx,
                                                 self.ch3_V_tx))
        pm.separator(parent=self.del_col, horizontal=False, style="in")

        self.del4_but = pm.button(
            label="delete\nchecker4",
            parent=self.del_col,
            height=50,
            width=55,
            command=lambda x: self.delete_shader("myChLambert4", self.ch4_U_tx,
                                                 self.ch4_V_tx))
        pm.separator(parent=self.del_col, horizontal=False, style="in")

        self.del5_but = pm.button(
            label="delete\nchecker5",
            parent=self.del_col,
            height=50,
            width=55,
            command=lambda x: self.delete_shader("myChLambert5", self.ch5_U_tx,
                                                 self.ch5_V_tx))
        pm.separator(parent=self.del_col, horizontal=False, style="in")

        grid_cell_width = 27
        sep_width = 4

        self.ch1_txt_grid_col = pm.gridLayout(parent=self.uv_ch_col,
                                              numberOfRowsColumns=(4, 2),
                                              cellWidth=grid_cell_width)
        self.ch1_U_tx = pm.textField(parent=self.ch1_txt_grid_col)
        pm.button(label="U",
                  parent=self.ch1_txt_grid_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert1", True, False, self.ch1_U_tx, None,
                              False, None, None))
        self.ch1_V_tx = pm.textField(parent=self.ch1_txt_grid_col)
        pm.button(label="V",
                  parent=self.ch1_txt_grid_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert1", False, True, None, self.ch1_V_tx,
                              False, None, None))
        pm.button(label="U+",
                  parent=self.ch1_txt_grid_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert1", True, False, None, None, True,
                              self.ch1_U_tx, None))
        pm.button(label="V+",
                  parent=self.ch1_txt_grid_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert1", False, True, None, None, True,
                              None, self.ch1_V_tx))
        pm.button(label="U-",
                  parent=self.ch1_txt_grid_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert1", True, False, None, None, False,
                              self.ch1_U_tx, None))
        pm.button(label="V-",
                  parent=self.ch1_txt_grid_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert1", False, True, None, None, False,
                              None, self.ch1_V_tx))
        pm.separator(parent=self.uv_ch_col,
                     horizontal=False,
                     style="in",
                     width=sep_width)

        self.ch2_txt_grid_col = pm.gridLayout(parent=self.uv_ch_col,
                                              numberOfRowsColumns=(4, 2),
                                              cellWidth=grid_cell_width)
        self.ch2_U_tx = pm.textField(parent=self.ch2_txt_grid_col)
        pm.button(label="U",
                  parent=self.ch2_txt_grid_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert2", True, False, self.ch2_U_tx, None,
                              False, None, None))
        self.ch2_V_tx = pm.textField(parent=self.ch2_txt_grid_col)
        pm.button(label="V",
                  parent=self.ch2_txt_grid_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert2", False, True, None, self.ch2_V_tx,
                              False, None, None))
        pm.button(label="U+",
                  parent=self.ch2_txt_grid_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert2", True, False, None, None, True,
                              self.ch2_U_tx, None))
        pm.button(label="V+",
                  parent=self.ch2_txt_grid_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert2", False, True, None, None, True,
                              None, self.ch2_V_tx))
        pm.button(label="U-",
                  parent=self.ch2_txt_grid_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert2", True, False, None, None, False,
                              self.ch2_U_tx, None))
        pm.button(label="V-",
                  parent=self.ch2_txt_grid_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert2", False, True, None, None, False,
                              None, self.ch2_V_tx))
        pm.separator(parent=self.uv_ch_col,
                     horizontal=False,
                     style="in",
                     width=sep_width)

        self.ch3_txt_grid_col = pm.gridLayout(parent=self.uv_ch_col,
                                              numberOfRowsColumns=(4, 2),
                                              cellWidth=grid_cell_width)
        self.ch3_U_tx = pm.textField(parent=self.ch3_txt_grid_col)
        pm.button(label="U",
                  parent=self.ch3_txt_grid_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert3", True, False, self.ch3_U_tx, None,
                              False, None, None))
        self.ch3_V_tx = pm.textField(parent=self.ch3_txt_grid_col)
        pm.button(label="V",
                  parent=self.ch3_txt_grid_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert3", False, True, None, self.ch3_V_tx,
                              False, None, None))
        pm.button(label="U+",
                  parent=self.ch3_txt_grid_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert3", True, False, None, None, True,
                              self.ch3_U_tx, None))
        pm.button(label="V+",
                  parent=self.ch3_txt_grid_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert3", False, True, None, None, True,
                              None, self.ch3_V_tx))
        pm.button(label="U-",
                  parent=self.ch3_txt_grid_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert3", True, False, None, None, False,
                              self.ch3_U_tx, None))
        pm.button(label="V-",
                  parent=self.ch3_txt_grid_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert3", False, True, None, None, False,
                              None, self.ch3_V_tx))
        pm.separator(parent=self.uv_ch_col,
                     horizontal=False,
                     style="in",
                     width=sep_width)

        self.ch4_txt_grid_col = pm.gridLayout(parent=self.uv_ch_col,
                                              numberOfRowsColumns=(4, 2),
                                              cellWidth=grid_cell_width)
        self.ch4_U_tx = pm.textField(parent=self.ch4_txt_grid_col)
        pm.button(label="U",
                  parent=self.ch4_txt_grid_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert4", True, False, self.ch4_U_tx, None,
                              False, None, None))
        self.ch4_V_tx = pm.textField(parent=self.ch4_txt_grid_col)
        pm.button(label="V",
                  parent=self.ch4_txt_grid_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert4", False, True, None, self.ch4_V_tx,
                              False, None, None))
        pm.button(label="U+",
                  parent=self.ch4_txt_grid_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert4", True, False, None, None, True,
                              self.ch4_U_tx, None))
        pm.button(label="V+",
                  parent=self.ch4_txt_grid_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert4", False, True, None, None, True,
                              None, self.ch4_V_tx))
        pm.button(label="U-",
                  parent=self.ch4_txt_grid_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert4", True, False, None, None, False,
                              self.ch4_U_tx, None))
        pm.button(label="V-",
                  parent=self.ch4_txt_grid_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert4", False, True, None, None, False,
                              None, self.ch4_V_tx))
        pm.separator(parent=self.uv_ch_col,
                     horizontal=False,
                     style="in",
                     width=sep_width)

        self.ch5_txt_grid_col = pm.gridLayout(parent=self.uv_ch_col,
                                              numberOfRowsColumns=(4, 2),
                                              cellWidth=grid_cell_width)
        self.ch5_U_tx = pm.textField(parent=self.ch5_txt_grid_col)
        pm.button(label="U",
                  parent=self.ch5_txt_grid_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert5", True, False, self.ch5_U_tx, None,
                              False, None, None))
        self.ch5_V_tx = pm.textField(parent=self.ch5_txt_grid_col)
        pm.button(label="V",
                  parent=self.ch5_txt_grid_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert5", False, True, None, self.ch5_V_tx,
                              False, None, None))
        pm.button(label="U+",
                  parent=self.ch5_txt_grid_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert5", True, False, None, None, True,
                              self.ch5_U_tx, None))
        pm.button(label="V+",
                  parent=self.ch5_txt_grid_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert5", False, True, None, None, True,
                              None, self.ch5_V_tx))
        pm.button(label="U-",
                  parent=self.ch5_txt_grid_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert5", True, False, None, None, False,
                              self.ch5_U_tx, None))
        pm.button(label="V-",
                  parent=self.ch5_txt_grid_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert5", False, True, None, None, False,
                              None, self.ch5_V_tx))

        self.ch1_UV_col = pm.gridLayout(parent=self.uv_ful_ch_col,
                                        numberOfRowsColumns=(2, 1),
                                        cellWidth=grid_cell_width * 2)
        pm.button(label="UV+",
                  parent=self.ch1_UV_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert1", True, True, None, None, True,
                              self.ch1_U_tx, self.ch1_V_tx))
        pm.button(label="UV-",
                  parent=self.ch1_UV_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert1", True, True, None, None, False,
                              self.ch1_U_tx, self.ch1_V_tx))
        pm.separator(parent=self.uv_ful_ch_col,
                     horizontal=False,
                     style="in",
                     width=sep_width)

        self.ch2_UV_col = pm.gridLayout(parent=self.uv_ful_ch_col,
                                        numberOfRowsColumns=(2, 1),
                                        cellWidth=grid_cell_width * 2)
        pm.button(label="UV+",
                  parent=self.ch2_UV_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert2", True, True, None, None, True,
                              self.ch2_U_tx, self.ch2_V_tx))
        pm.button(label="UV-",
                  parent=self.ch2_UV_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert2", True, True, None, None, False,
                              self.ch2_U_tx, self.ch2_V_tx))
        pm.separator(parent=self.uv_ful_ch_col,
                     horizontal=False,
                     style="in",
                     width=sep_width)

        self.ch3_UV_col = pm.gridLayout(parent=self.uv_ful_ch_col,
                                        numberOfRowsColumns=(2, 1),
                                        cellWidth=grid_cell_width * 2)
        pm.button(label="UV+",
                  parent=self.ch3_UV_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert3", True, True, None, None, True,
                              self.ch3_U_tx, self.ch3_V_tx))
        pm.button(label="UV-",
                  parent=self.ch3_UV_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert3", True, True, None, None, False,
                              self.ch3_U_tx, self.ch3_V_tx))
        pm.separator(parent=self.uv_ful_ch_col,
                     horizontal=False,
                     style="in",
                     width=sep_width)

        self.ch4_UV_col = pm.gridLayout(parent=self.uv_ful_ch_col,
                                        numberOfRowsColumns=(2, 1),
                                        cellWidth=grid_cell_width * 2)
        pm.button(label="UV+",
                  parent=self.ch4_UV_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert4", True, True, None, None, True,
                              self.ch4_U_tx, self.ch4_V_tx))
        pm.button(label="UV-",
                  parent=self.ch4_UV_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert4", True, True, None, None, False,
                              self.ch4_U_tx, self.ch4_V_tx))
        pm.separator(parent=self.uv_ful_ch_col,
                     horizontal=False,
                     style="in",
                     width=sep_width)

        self.ch5_UV_col = pm.gridLayout(parent=self.uv_ful_ch_col,
                                        numberOfRowsColumns=(2, 1),
                                        cellWidth=grid_cell_width * 2)
        pm.button(label="UV+",
                  parent=self.ch5_UV_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert5", True, True, None, None, True,
                              self.ch5_U_tx, self.ch5_V_tx))
        pm.button(label="UV-",
                  parent=self.ch5_UV_col,
                  command=lambda x: self.
                  tile_uv_val("myChLambert5", True, True, None, None, False,
                              self.ch5_U_tx, self.ch5_V_tx))
        pm.separator(parent=self.uv_ful_ch_col,
                     horizontal=False,
                     style="in",
                     width=sep_width)

        pm.button(label="copy shader",
                  parent=self.copy_btn_col,
                  command=lambda x: self.copy_shader())

        pm.showWindow(self.WINDOW)
        pm.window(self.WINDOW, edit=True, widthHeight=(290, 340))


AssignShader()
