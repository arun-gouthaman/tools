import pymel.all as pm
import maya.OpenMaya as OpenMaya
import CustomScripts


class Loop_Motion_Path(object):
    def __init__(self):
        self.DATA_TYPE_FAIL = "Invalid Data Type"
        self.INVALID_INPUT_FAIL = "Invalid Input"
        self.NO_OBJECT_FAIL = "Object Not Found"
        self.tread_create_ui()
        return None

    def set_path_name(self):
        sel = str(pm.ls(selection=True)[0])
        self.curve_name.setText(sel)
        return None

    def set_sample_object(self):
        sel = pm.ls(selection=True)
        if sel:
            return self.sample_name.setLabel(str(sel[0]))
        else:
            return self.sample_name.setLabel("")
        return None

    def getDagPath(self, **kwargs):
        objectName = str(kwargs.get("objectName", None))
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

    def getuParamVal(self, **kwargs):
        pnt = kwargs.get("pnt", [])
        crv = kwargs.get("crv", None)
        point = OpenMaya.MPoint(pnt[0], pnt[1], pnt[2])
        curveFn = OpenMaya.MFnNurbsCurve(self.getDagPath(objectName=crv))
        paramUtill = OpenMaya.MScriptUtil()
        paramPtr = paramUtill.asDoublePtr()
        isOnCurve = curveFn.isPointOnCurve(point)
        if isOnCurve:
            curveFn.getParamAtPoint(point, paramPtr, 0.001,
                                    OpenMaya.MSpace.kWorld)
        else:
            point = curveFn.closestPoint(point, paramPtr, 0.001,
                                         OpenMaya.MSpace.kWorld)
            curveFn.getParamAtPoint(point, paramPtr, 0.001,
                                    OpenMaya.MSpace.kWorld)
        param = paramUtill.getDouble(paramPtr)
        return param

    def get_setup_name(self):
        if not self.tread_name.getText():
            return self.INVALID_INPUT_FAIL
        return self.tread_name.getText()

    def get_duplicate_flag(self):
        return self.dup_crv_chk_bx.getValue()

    def get_duplicate_path(self, **kwargs):
        path_crv = kwargs.get("path_crv", None)
        if path_crv:
            duplicate_crv = pm.duplicate(path_crv)[0]
        return duplicate_crv

    def get_use_selection(self):
        return self.sel_obj_chk_bx.getValue()

    def get_placement_type(self):
        sel_option = self.jnt_typ_radio.getSelect()
        option_label = pm.radioButton(sel_option, query=True, label=True)
        return option_label

    def get_division_count(self):
        divisions_count = self.divisions.getText()
        if not divisions_count:
            return self.INVALID_INPUT_FAIL
        try:
            divisions_count = int(divisions_count)
            return divisions_count
        except ValueError:
            return self.DATA_TYPE_FAIL

    def get_sample_objects(self):
        sample_obj = str(self.sample_name.getLabel())
        if sample_obj:
            if not pm.objExists(sample_obj):
                return self.NO_OBJECT_FAIL
        return self.sample_name.getLabel()

    def get_path_name(self):
        path_name = self.curve_name.getText()
        if not path_name:
            return self.INVALID_INPUT_FAIL
        if not pm.objExists(path_name):
            return self.NO_OBJECT_FAIL
        shape_node = pm.PyNode(path_name).getShape()
        if not isinstance(shape_node, pm.NurbsCurve):
            return self.DATA_TYPE_FAIL
        return self.curve_name.getText()

    def createTreadExpression(self, **kwargs):
        motionpaths = kwargs.get("mtnPth", [])
        run_ip = kwargs.get("runAttr", "")
        speed_ip = kwargs.get("speedAttr", "")
        expression_name = kwargs.get("exp_nm", "")
        ip_str = "float $ipVal = " + run_ip + "*" + speed_ip + ";\n"
        computeOffset = ""
        counter = 1
        for mp in motionpaths:
            offset = pm.getAttr(str(mp) + ".uValue")
            computeOffset += "float $newVal" + str(counter) + " = " + str(
                offset) + "+($ipVal - floor(" + str(offset) + "+$ipVal));\n"
            computeOffset += str(mp) + ".uValue = $newVal" + str(
                counter) + ";\n"
            counter += 1
        expression_string = ip_str + computeOffset
        pm.expression(name=expression_name, string=expression_string)

    def at_selection(self, **kwargs):
        # get inputs
        setup_name = kwargs.get("name", None)
        path_name = kwargs.get("path", None)
        sample_obj = kwargs.get("sample", None)
        obj_lst = kwargs.get("selection_list", None)
        full_length = pm.arclen(path_name)
        paramVal = []
        uVal = []
        for obj in obj_lst:
            pos = pm.xform(obj, query=True, translation=True, worldSpace=True)
            param = self.getuParamVal(pnt=pos, crv=path_name)
            paramVal.append(param)
        crv_shp = pm.listRelatives(path_name, shapes=True)[0]
        arcLen = pm.arcLengthDimension(crv_shp + ".u[0]")
        for val in paramVal:
            pm.setAttr(str(arcLen) + ".uParamValue", val)
            len_at_pos = pm.getAttr(str(arcLen) + ".arcLength")
            uVal.append(len_at_pos / full_length)
        pm.delete(arcLen)
        path_anim_list = []
        if not self.get_use_selection():
            obj_lst = []
            if sample_obj:
                for i in uVal:
                    obj_lst.append(
                        pm.duplicate(sample_obj,
                                     name=setup_name + str(i + 1) + "_OBJECT"))
            else:
                for i in uVal:
                    pm.select(clear=True)
                    obj_lst.append(
                        pm.joint(name=setup_name + str(i + 1) + "_JNT"))

        index = 0
        for u in uVal:
            pm.select(clear=True)
            pathanim = pm.pathAnimation(obj_lst[index],
                                        curve=path_name,
                                        fractionMode=True,
                                        follow=True,
                                        followAxis="x",
                                        worldUpType="vector",
                                        worldUpVector=(0, 1, 0))
            index += 1
            path_anim_list.append(pathanim)
            pm.setAttr(str(pathanim) + ".uValue", u)
            pm.disconnectAttr(str(pathanim) + ".u")
        return (obj_lst, path_anim_list)

    def uniform_distribution(self, **kwargs):
        setup_name = kwargs.get("name", None)
        path_name = kwargs.get("path", None)
        sample_obj = kwargs.get("sample", None)
        divisions = kwargs.get("divisions", None)
        count = 0
        part = float(1) / float(divisions)
        init = 0
        obj_lst = []
        path_anim_list = []

        if not sample_obj:
            for i in range(divisions):
                pm.select(clear=True)
                obj_lst.append(pm.joint(name=setup_name + str(i + 1) + "_JNT"))

        else:
            for i in range(divisions):
                obj_lst.append(
                    pm.duplicate(sample_obj,
                                 name=setup_name + str(i + 1) + "_Object"))

        index = 0

        while count < divisions:
            pathanim = pm.pathAnimation(obj_lst[index],
                                        curve=path_name,
                                        fractionMode=True,
                                        follow=True,
                                        followAxis="x",
                                        worldUpType="vector",
                                        worldUpVector=(0, 1, 0))
            index += 1
            path_anim_list.append(pathanim)
            pm.setAttr(str(pathanim) + ".uValue", init)
            pm.disconnectAttr(str(pathanim) + ".u")
            init += part
            count += 1

        return (obj_lst, path_anim_list)

    def setup_motion_path(self):
        setup_name = self.get_setup_name()
        path_name = self.get_path_name()
        sample_obj = self.get_sample_objects()
        duplicate_flag = self.get_duplicate_flag()
        placement_type = self.get_placement_type()
        division_count = self.get_division_count()

        if setup_name == self.INVALID_INPUT_FAIL:
            pm.displayError("Invalid Input Entered for setup name")
            return None

        if path_name == self.INVALID_INPUT_FAIL:
            pm.displayError("Invalid Input Entered for path name")
            return None

        if path_name == self.NO_OBJECT_FAIL:
            pm.displayError("path Curve does not exist")
            return None

        if path_name == self.DATA_TYPE_FAIL:
            pm.displayError("Path can be only Nurb Curves")
            return None

        if division_count == self.INVALID_INPUT_FAIL:
            pm.displayError("Invalid Input Entered for divisions")
            return None

        if division_count == self.DATA_TYPE_FAIL:
            pm.displayError("Divisions can take only integer values")
            return None

        if sample_obj == self.NO_OBJECT_FAIL:
            pm.displayError("Sample Object not found")
            return None

        obj_list = []
        path_anim_list = []

        sel_objs = pm.ls(selection=True)

        if duplicate_flag:
            path_name = self.get_duplicate_path(path_crv=path_name)
        path_name = pm.rename(path_name, setup_name + "_path_CRV")

        if placement_type == "uniform":
            obj_list, path_anim_list = self.uniform_distribution(
                name=setup_name,
                path=path_name,
                sample=sample_obj,
                divisions=division_count)
        else:
            if not sel_objs:
                pm.displayError("No Objects selected")
            for obj in sel_objs:
                if not pm.objExists(obj):
                    pm.displayWarning(str(obj), "does not exist")
                    return None
            obj_list, path_anim_list = self.at_selection(
                name=setup_name,
                path=path_name,
                sample=sample_obj,
                selection_list=sel_objs)

        loc_pos = CustomScripts.midPos(selected_items=path_name)
        loc = pm.spaceLocator(name=setup_name + "_up_loc")
        pm.xform(loc, translation=loc_pos)
        control_crv = pm.circle(name=setup_name + "CTRL",
                                normalX=1,
                                normalY=0,
                                normalZ=0)
        pm.xform(control_crv[0], translation=loc_pos, worldSpace=True)
        pm.select(clear=True)
        # add run and speed attributes on parent nurb curve
        pm.addAttr(control_crv[0],
                   longName="run",
                   attributeType="float",
                   keyable=True)
        pm.addAttr(control_crv[0],
                   longName="speed",
                   attributeType="float",
                   keyable=True,
                   minValue=0.0,
                   defaultValue=0.5)
        # edit the existing motion path to assign up locator
        for mtPth in path_anim_list:
            pm.pathAnimation(mtPth,
                             edit=True,
                             worldUpType="object",
                             worldUpObject=loc)
        # parent the setup under the parent nurb curve
        pm.parent(path_name, control_crv[0])
        pm.parent(loc, control_crv[0])
        pm.select(clear=True)
        gp = pm.group(name=setup_name + "GP")
        pm.xform(gp, translation=loc_pos)
        pm.select(clear=True)
        obj_gp = pm.group(obj_list, name=setup_name + "object_GP")
        pm.parent(control_crv[0], gp)
        pm.parent(obj_gp, gp)
        # call to create expression function
        self.createTreadExpression(mtnPth=path_anim_list,
                                   runAttr=str(control_crv[0]) + ".run",
                                   speedAttr=str(control_crv[0]) + ".speed",
                                   exp_nm=setup_name)
        return None

    def ui_set_selection_enable(self, **kwargs):
        flag = kwargs.get("flag", None)
        if flag == "uniform":
            self.divisions.setEditable(True)
            self.sel_obj_chk_bx.setEditable(False)
            self.sel_obj_chk_bx.setValue(False)
            self.chk_bx_info.setEnable(False)
            self.chk_bx_info.setLabel("")
            pm.window(self.WINDOW, edit=True, widthHeight=(200, 320))
        else:
            self.divisions.setEditable(False)
            self.sel_obj_chk_bx.setEditable(True)
            self.sel_obj_chk_bx.setValue(True)
            self.chk_bx_info.setEnable(True)
            self.chk_bx_info.setLabel(
                "If checked off, sample objects or\njoints \
                will be placed in positions"
            )
            pm.window(self.WINDOW, edit=True, widthHeight=(200, 335))
        return None

    def tread_create_ui(self):
        self.WINDOW = 'Loop_Motion_Path'
        if pm.window(self.WINDOW, query=True, exists=True):
            pm.deleteUI(self.WINDOW)
        pm.window(self.WINDOW,
                  title="Loop Motion Path",
                  iconName='TR',
                  widthHeight=(200, 220))
        column_1 = pm.columnLayout(adjustableColumn=True)
        pm.separator(height=20, style='none', parent=column_1)
        self.tread_name = pm.TextField(text='Setup_Name', parent=column_1)
        pm.separator(height=20, style='none', parent=column_1)
        # get parent name
        row_col_1 = pm.rowColumnLayout(numberOfColumns=2,
                                       columnWidth=(1, 150),
                                       parent=column_1,
                                       columnOffset=(2, 'left', 10))
        self.curve_name = pm.TextField(text='PathCurve', parent=row_col_1)
        pm.button(label='<<',
                  parent=row_col_1,
                  command=lambda x: self.set_path_name())

        chk_bx_col = pm.rowColumnLayout(parent=column_1,
                                        numberOfColumns=2,
                                        columnWidth=(1, 20))
        pm.text("", parent=chk_bx_col)
        self.dup_crv_chk_bx = pm.checkBox("Duplicate Curve",
                                          parent=chk_bx_col,
                                          value=True)
        pm.separator(height=20, style='in', parent=column_1)
        self.jnt_type_lbl = pm.text(label="object placement type",
                                    align="left",
                                    parent=column_1)
        pm.separator(height=5, style='none', parent=column_1)
        self.jnt_typ_radio = pm.radioCollection(parent=column_1)

        row_layout = pm.rowLayout(numberOfColumns=2,
                                  height=20,
                                  parent=column_1)
        sel_chk_bx_col = pm.rowColumnLayout(parent=column_1,
                                            numberOfColumns=2,
                                            columnWidth=(1, 20))

        info_chk_bx_col = pm.ColumnLayout(parent=column_1)
        self.chk_bx_info = pm.text("", parent=info_chk_bx_col, enable=False)
        pm.text("", parent=sel_chk_bx_col)
        self.sel_obj_chk_bx = pm.checkBox("Use Selection On Curve",
                                          parent=sel_chk_bx_col,
                                          value=False,
                                          enable=False)
        self.divisions = pm.TextField(text='1', parent=column_1)

        pm.radioButton(
            label='uniform',
            parent=row_layout,
            select=True,
            onCommand=lambda x: self.ui_set_selection_enable(flag="uniform"))
        pm.radioButton(
            label='selection',
            parent=row_layout,
            onCommand=lambda x: self.ui_set_selection_enable(flag="selection"))

        pm.separator(height=20, style='none', parent=column_1)
        pm.text("Input sample object (default joint)", parent=column_1)

        sample_row_col = pm.rowColumnLayout(numberOfColumns=2,
                                            columnWidth=(1, 150),
                                            parent=column_1,
                                            columnOffset=(2, 'left', 10))
        self.sample_name = pm.text(label="", parent=sample_row_col)
        pm.button(label='<<',
                  parent=sample_row_col,
                  command=lambda x: self.set_sample_object())
        pm.separator(height=20, style='none', parent=column_1)
        pm.button(label='Create',
                  parent=column_1,
                  command=lambda x: self.setup_motion_path())
        pm.showWindow(self.WINDOW)
        pm.window(self.WINDOW, edit=True, widthHeight=(200, 320))
        return None


"""
Call script in Maya Script Editor
import LoopMotionPath
LoopMotionPath.Loop_Motion_Path()
"""
