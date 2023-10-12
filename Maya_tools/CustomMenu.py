import pymel.all as pm

pm.selectPref(trackSelectionOrder=True)


def obj_creat():
    import object_creator_ui
    object_creator_ui.object_creator_ui()
    return None


def cus_tls():
    import CustomScriptsUI
    CustomScriptsUI.CustomScripts_UI()
    return None


def tank_trd():
    import LoopMotionPath
    LoopMotionPath.Loop_Motion_Path()
    return None


def jnt_along_loop():
    import Jntpos
    Jntpos.jnt_along_loop()
    return None


def jnt_at_obj_mid():
    import Jntpos
    Jntpos.jnt_at_object_mid()
    return None


def jnt_at_comp_mid():
    import CustomScripts
    CustomScripts.jntAtmid()
    return None


def jnt_mid_aimed():
    import Jntpos
    Jntpos.jnt_at_mid_vertex_orient()
    return None


def insert_joints():
    import insertJointsUI
    insertJointsUI.insert_joints_UI()
    return None


def spline_ik_setup():
    import Ik_Spline_Setup_Ui
    Ik_Spline_Setup_Ui.spline_ik_setup_UI()
    return None


def curve_points():
    import CustomScripts
    CustomScripts.curve_through_points()
    return None


def del_dis_lyr():
    import CustomScripts
    CustomScripts.delete_layers()
    return None


def hist_nodes_rename():
    import RenameNodes
    RenameNodes.Rename_Nodes()
    return None


def loop_from_edge():
    import Jntpos
    Jntpos.get_loop_from_edge()
    return None


def rearng_def():
    import RearrangeDeformers
    RearrangeDeformers.Rearrange_Nodes()
    return None


def sequential_loops():
    import SequentialLoops
    SequentialLoops.Sequential_Loops()
    return None


def create_shape():
    import CreateShape
    CreateShape.Create_Shape()
    return None


def manage_control():
    import ManageControl
    ManageControl.Manage_Control()
    return None


def replace_instance():
    from ReplaceInstance import replaceInstance
    replaceInstance().getShapeNode()
    pass


menuName = "Custom_Menu"
mainMenu = pm.PyUI(pm.getMelGlobal('string', 'gMainWindow'))

try:
    if pm.menu(Custom_Tools, query=True, exists=True):
        pm.deleteUI(Custom_Tools)
except:
    print("Creating New Menu")

with mainMenu:
    if pm.menu(menuName, query=True, exists=True):
        pm.menu(menuName, edit=True, deleteAllItems=True)
    Custom_Tools = pm.menu(label=menuName, tearOff=True)

    with Custom_Tools:
        obj_cr_btn = pm.menuItem(label="Object creator",
                                 command=lambda x: obj_creat())
        cus_tls_btn = pm.menuItem(label="Custom Tools",
                                  command=lambda x: cus_tls())
        tnk_trd_bth = pm.menuItem(label="MotionPath Loop (arun)",
                                  command=lambda x: tank_trd())
        joint_place_btn = pm.menuItem(subMenu=True,
                                      label="Joint Placement",
                                      tearOff=True)
        joint_place_sub1_btn = pm.menuItem(label="Center(object)",
                                           command=lambda x: jnt_at_obj_mid())
        joint_place_sub2_btn = pm.menuItem(label="Center(Components)",
                                           command=lambda x: jnt_at_comp_mid())
        joint_place_sub3_btn = pm.menuItem(label="Insert Joints",
                                           command=lambda x: insert_joints())
        joint_place_sub4_btn = pm.menuItem(label="Center aimed at vertex",
                                           command=lambda x: jnt_mid_aimed())
        joint_place_sub5_btn = pm.menuItem(label="Chain along edge loops",
                                           command=lambda x: jnt_along_loop())
        joint_place_sub6_btn = pm.menuItem(label="Loop from edge",
                                           command=lambda x: loop_from_edge())
        joint_place_sub7_btn = pm.menuItem(
            label="Continue along loops", command=lambda x: sequential_loops())

        pm.setParent('..', menu=True)

        spline_ik = pm.menuItem(label="IK spline setup (arun)",
                                command=lambda x: spline_ik_setup())

        curve_through_points = pm.menuItem(label="curve through points",
                                           command=lambda x: curve_points())

        del_dis_layer = pm.menuItem(label="delete display layers",
                                    command=lambda x: del_dis_lyr())

        reord_def = pm.menuItem(label="rearragne deformers",
                                command=lambda x: rearng_def())
        def_node_rename_btn = pm.menuItem(
            label="Rename Deformer Nodes",
            command=lambda x: hist_nodes_rename())

        create_control_menu = pm.menuItem(subMenu=True,
                                          label="Controls",
                                          tearOff=True)
        create_control__btn = pm.menuItem(label="Create Control",
                                          command=lambda x: create_shape())
        manage_shapes_btn = pm.menuItem(label="manage Shapes",
                                        command=lambda x: manage_control())
        pm.setParent('..', menu=True)
        replace_instance_btn = pm.menuItem(
            label="replace instance nodes",
            command=lambda x: replace_instance())

pass
