import pymel.all as pm
import maya.mel as mel
import math
import random


class Ref_Scale_UV(object):
    def __init__(self):
        self.ref_shell = None
        self.ratioREF = 0.0
        self.uv_ratio_UI()
        self.uv_shells_list = {}
        return None

    # get seperate shells from selected faces
    def split_shells(self, uv_list, ref_count, count):
        # from selected UV pick a random uv and find the uv shell
        # from the total uv list, remove the above selected uv shell list
        # iterate through uvs in the total uv list till the list is empty
        pm.select(uv_list[0])
        ref_uv = pm.ls(selection=True)[0]
        mel.eval('ConvertSelectionToUVShell')
        cur_uv = set(pm.ls(selection=True, flatten=True))
        mel.eval('ConvertSelectionToFaces')
        shell_face = pm.ls(selection=True, flatten=True)
        self.uv_shells_list[ref_uv] = shell_face
        new_list = list(set(uv_list).difference(set(cur_uv)))
        if new_list:
            # if the loop keeps running more than tne count of total uv
            # the loop has failed to succeed and is running infinite
            # break the execution and return "Infinite_loop" flag
            count += 1
            if count > ref_count:
                return "Infinite loop"
            pm.select(new_list)
            self.split_shells(new_list, ref_count, count)
        return None

    # get mesh area, uv area and ratio of mesh area to uv area
    def get_area_ratio(self, **kwargs):
        flag = kwargs.get("flag", None)
        sel_face = kwargs.get("sel_face", None)
        sel_face = pm.ls(sel_face, flatten=True)
        if not sel_face:
            pm.displayWarning("NO FACES SELECTED")
            return None
        mesh_world_area = 0.0
        uv_area = 0.0
        print(sel_face)
        for fc in sel_face:
            mesh_world_area += fc.getArea(space="world")
            uv_area += fc.getUVArea()
        ratio = mesh_world_area / uv_area
        if flag == "CUR":
            return mesh_world_area, uv_area, ratio
        else:
            return ratio
        return None

    # assign the scale ratio to selceted shells
    def rescale_uv(self, **kwargs):
        # if no reference shell is selected stop execution
        if not self.ref_shell:
            pm.displayWarning("Reference shell not set")
            return None
        sel_shell_lst = []
        skipped_selection = []
        mesh_check = self.ch_bx.getValue()
        # if the selection is object get the faces of the object
        if mesh_check:
            print("SELECT MESH")
            sel_obj = pm.ls(selection=True)
            for obj in sel_obj:
                if isinstance(obj.getShape(), pm.Mesh):
                    obj_faces = pm.ls(str(obj) + ".f[*]", flatten=True)
                    sel_shell_lst += obj_faces
                else:
                    skipped_selection.append(obj)
        else:
            sel_shell_lst = pm.ls(selection=True)
        if not sel_shell_lst:
            pm.displayWarning("No face selected")
            return None
        # convert all faces to UV selection
        mel.eval('ConvertSelectionToUVs')
        all_uv = pm.ls(selection=True, flatten=True)
        if not isinstance(sel_shell_lst[0], pm.MeshFace):
            pm.displayWarning("Please select shells")
            return None
        ref_count = len(all_uv)
        # call shell split function to get a list of separate shells
        run_shellp_split = self.split_shells(all_uv, ref_count, count=0)
        # if the self.split_shells runs more than
        #     the number ofvertices, terminate
        if run_shellp_split == "Infinite loop":
            pm.displayError("MAX COUNT REACHED, Shell separation FAIL!!!!!!")
            return None
        # for each shell, find the required area ratio to
        #     match with the reference area ratio
        # scale the shell to tha amount needed
        for ref_uv in self.uv_shells_list:
            sel_faces = pm.ls(self.uv_shells_list[ref_uv])
            mesh_areaCUR, uv_areaCUR, ratioCUR = self.get_area_ratio(
                flag="CUR", sel_face=sel_faces)
            if not self.ratioREF == ratioCUR:
                needed_area = mesh_areaCUR / self.ratioREF
                scaleval = math.sqrt(needed_area / uv_areaCUR)
                pm.select(ref_uv)
                ref = pm.polyEditUVShell(ref_uv,
                                         query=True,
                                         pivotU=True,
                                         pivotV=True)
                pm.polyEditUVShell(pivotU=ref[0],
                                   pivotV=ref[1],
                                   scaleU=scaleval,
                                   scaleV=scaleval)
        self.uv_shells_list = {}
        if skipped_selection:
            print "########Objects skipped########"
            for obj in skipped_selection:
                print obj
            pm.displayWarning("objects have been skipped, check script editor")
        return None

    def set_ref_shell(self):
        self.ref_shell = pm.ls(selection=True, flatten=True)
        if not self.ref_shell:
            pm.button(self.ref_shell_btn,
                      edit=True,
                      backgroundColor=(.863, 0.078, 0.235))
            self.ref_shell = None
            self.assign_btn.setEnable(False)
            self.sel_shell_btn.setEnable(False)
            self.ch_bx.setEnable(False)
            return None
        if not isinstance(self.ref_shell[0], pm.MeshFace):
            pm.displayWarning("Please select shells")
            return None
        r = round(random.uniform(0.000, 0.500), 3)
        b = round(random.uniform(0.000, 0.500), 3)
        pm.button(self.ref_shell_btn, edit=True, backgroundColor=(r, .545, b))
        self.ratioREF = self.get_area_ratio(flag="REF",
                                            sel_face=self.ref_shell)
        self.assign_btn.setEnable(True)
        self.sel_shell_btn.setEnable(True)
        self.ch_bx.setEnable(True)
        return None

    def sel_ref_shell(self):
        pm.select(self.ref_shell)
        return None

    def uv_ratio_UI(self):
        UV_RATIO_WINDOW = "UVratio"
        if pm.window(UV_RATIO_WINDOW, query=True, exists=True):
            pm.deleteUI(UV_RATIO_WINDOW)

        pm.window(UV_RATIO_WINDOW, title="uv ratio", iconName="UVR")

        main_col = pm.columnLayout(adjustableColumn=True)
        self.ref_shell_btn = pm.button("set reference shell",
                                       height=40,
                                       parent=main_col,
                                       backgroundColor=(.863, 0.078, 0.235),
                                       command=lambda x: self.set_ref_shell())
        pm.separator(parent=main_col, style="in", height=5)
        self.sel_shell_btn = pm.button("select assigned reference shell",
                                       parent=main_col,
                                       enable=False,
                                       command=lambda x: self.sel_ref_shell())
        pm.separator(parent=main_col, style="in", height=10)
        self.assign_btn = pm.button("apply uv ratio on\n selected Shells",
                                    height=40,
                                    parent=main_col,
                                    enable=False,
                                    command=lambda x: self.rescale_uv())
        #self.assign_btn.setEnable(False)
        pm.separator(parent=main_col, height=5, style="in")
        ch_bx_col = pm.rowColumnLayout(numberOfColumns=2,
                                       parent=main_col,
                                       columnOffset=(1, "left", 40))
        pm.text("", parent=ch_bx_col)
        self.ch_bx = pm.checkBox(label="Object Selection",
                                 parent=ch_bx_col,
                                 enable=False)
        pm.text("Check above option to select mesh\ninstead of shell",
                parent=main_col)

        pm.showWindow(UV_RATIO_WINDOW)
        pm.window(UV_RATIO_WINDOW, edit=True, widthHeight=(200, 170))
        return None

Ref_Scale_UV()
