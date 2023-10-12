"""
Script to create switch on layered texturing.
Each switch turns on a specific layer and turns off the rest.
Uses set driven keys to perform switching.

#####Creating Switch#####
Open UI, select the control and refresh the list to get the list
of enum attributes.
Select the attribute name in the list.
Select the layered texture node and create switch.

The number of enum values in attribute and,
   the number of layers in the layered texture node
   should match.
#####Creating Switch#####

#####Creating Enum Attribute#####
Open the UI
Enter the name for Enum attribute
Enter the values for Enum Attribute in Text Box below
   each line of string is considered as a value
   enter every value in new line
Select the controller and create Enum attribute
#####Creating Enum Attribute#####
"""

import pymel.all as pm


class LayerTexSwitch(object):
    def __init__(self):
        self.lyr_swtch_ui()
        self.populate_list()
        return None

    def create_attr(self):
        # Create enum attribute on selected control object
        sel = pm.ls(selection=True)
        if not sel:
            pm.displayWarning("Select Control object")
            return None
        attr = self.attr_nm.getText()
        attr_lst = self.enum_val.getText().split("\n")
        enum_attr_val = ""
        for index in range(len(attr_lst)):
            if attr_lst[index]:
                enum_attr_val += attr_lst[index]
                if not index == len(attr_lst) - 1:
                    enum_attr_val += ":"
        for obj in sel:
            pm.addAttr(obj,
                       longName=attr,
                       attributeType="enum",
                       enumName=enum_attr_val,
                       keyable=True,
                       readable=True,
                       storable=True,
                       writable=True)
        self.populate_list()
        return None

    def get_attr_name(self):
        # Return attributes of type enum from selected controller
        self.ctr = self.ctr[0]
        attrs = pm.listAttr(self.ctr, keyable=True)
        enum_attr_list = []
        for at in attrs:
            at_typ = pm.PyNode(str(self.ctr) + "." + at).type()
            if at_typ == "enum":
                enum_attr_list.append(at)
        return enum_attr_list

    def get_tex_layer_attrs(self):
        # Return list of isVisible attributes on the layeres texture node
        att = pm.Attribute(str(self.lyr_tex_sel) + ".inputs")
        ip_vis = filter(lambda x: x.endswith(".isVisible"), att.elements())
        return ip_vis

    def create_switching(self):
        # Create setDrivenKey on layered texture
        sel_switch = self.text_lst.getSelectItem()[0]
        enum_attr_list = pm.attributeQuery(sel_switch,
                                           node=self.ctr,
                                           listEnum=True)
        enum_attr_list = enum_attr_list[0].split(":")
        self.lyr_tex_sel = pm.ls(selection=True)
        if not self.lyr_tex_sel:
            pm.displayError("Please select layered texture node")
            return None
        self.lyr_tex_sel = self.lyr_tex_sel[0]
        if not isinstance(self.lyr_tex_sel, pm.LayeredTexture):
            pm.displayError("Please select layered texture node type")
            return None

        lyr_attr_lst = self.get_tex_layer_attrs()

        if not lyr_attr_lst:
            return None

        if not len(enum_attr_list) == len(lyr_attr_lst):
            pm.displayError("Switch and Layers number mismatch")
            return None

        driver_attr = self.ctr + "." + sel_switch
        for driver_index in range(len(enum_attr_list)):
            for driven_index in range(len(lyr_attr_lst)):
                driven_attr = self.lyr_tex_sel + "." + lyr_attr_lst[
                    driven_index]
                driven_val = 0
                if driver_index == driven_index:
                    driven_val = 1
                pm.setDrivenKeyframe(driven_attr,
                                     currentDriver=driver_attr,
                                     driverValue=driver_index,
                                     value=driven_val)

        return None

    def populate_list(self):
        # display the list of enum attributes
        self.text_lst.removeAll()
        self.ctr = pm.ls(selection=True)
        if not self.ctr:
            pm.displayWarning("Control not selected")
            return None
        attr_list = self.get_attr_name()
        if attr_list:
            self.text_lst.append(attr_list)
        return None

    def lyr_swtch_ui(self):

        self.MAIN_WINDOW = "Layered_texture_switch"
        if pm.window(self.MAIN_WINDOW, query=True, exists=True):
            pm.deleteUI(self.MAIN_WINDOW)
        pm.window(self.MAIN_WINDOW,
                  title="Layered Tex Switch",
                  iconName="LTS",
                  widthHeight=(150, 200))
        main_col = pm.columnLayout(adjustableColumn=True,
                                   height=100,
                                   parent=self.MAIN_WINDOW)

        but_col = pm.rowColumnLayout(parent=main_col, numberOfColumns=2)

        self.create_attr_btn = pm.button(
            label="Create ENUM Attribute",
            parent=main_col,
            command=lambda x: self.create_atr_ui())

        pm.separator(parent=main_col, style="in", height=10)

        pm.text(label="Enum Attribuite list", parent=main_col)
        pm.separator(parent=main_col, style="none", height=5)

        self.text_lst = pm.textScrollList(allowMultiSelection=False,
                                          parent=main_col,
                                          height=150)

        pm.separator(parent=main_col, style="none", height=5)

        but_col = pm.rowColumnLayout(parent=main_col, numberOfColumns=3)

        pm.button(label="Refresh List",
                  parent=but_col,
                  command=lambda x: self.populate_list())
        pm.separator(parent=but_col, horizontal=False)
        pm.button(label="Create Switch",
                  parent=but_col,
                  command=lambda x: self.create_switching())

        pm.showWindow(self.MAIN_WINDOW)
        pm.window(self.MAIN_WINDOW, edit=True, widthHeight=(150, 235))

        return None

    def create_atr_ui(self):
        self.ATTR_WINDOW = "Create_Attr"
        if pm.window(self.ATTR_WINDOW, query=True, exists=True):
            pm.deleteUI(self.ATTR_WINDOW)
        pm.window(self.ATTR_WINDOW,
                  title="create attribute",
                  iconName="CA",
                  widthHeight=(250, 200))
        attr_main_col = pm.columnLayout(adjustableColumn=True,
                                        parent=self.ATTR_WINDOW)

        attr_nm_col = pm.rowColumnLayout(parent=attr_main_col,
                                         numberOfColumns=2)

        pm.text(label="Enum Attribute Name  :  ", parent=attr_nm_col)

        self.attr_nm = pm.textField("", parent=attr_nm_col, width=120)

        pm.separator(parent=attr_main_col, style="in")

        attr_val_col = pm.rowColumnLayout(parent=attr_main_col,
                                          numberOfColumns=2,
                                          columnOffset=(1, "right", 5))

        attr_val_ch_col = pm.rowColumnLayout(parent=attr_val_col,
                                             numberOfRows=2)

        attr_val_btn_ch_col = pm.rowColumnLayout(parent=attr_val_col,
                                                 numberOfRows=2)

        pm.text(label="Enum Attribute values", parent=attr_val_ch_col)

        self.enum_val = pm.scrollField(parent=attr_val_ch_col,
                                       width=130,
                                       height=150)

        pm.text(label=" ", parent=attr_val_btn_ch_col)

        pm.button(label="Create Attr\non selected\ncontrol",
                  parent=attr_val_btn_ch_col,
                  height=150,
                  width=100,
                  command=lambda x: self.create_attr())
        pm.showWindow(self.ATTR_WINDOW)
        pm.window(self.ATTR_WINDOW, edit=True, widthHeight=(250, 200))

        return None


LayerTexSwitch()
