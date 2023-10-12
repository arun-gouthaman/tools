import pymel.all as pm
import CustomScripts
class Sequential_Loops(object):
    
    def __init__(self):
        self.init_var()
        self.ui()
        self.FAIL = "fail"
        self.SUCCESS = "success"        
        return None
    
    def init_var(self):
        self.loop = []
        self.init_loop = []
        self.transform_node = None
        self.shape_node = None
        self.init_flag = True
        self.safe_count = 0
        self.stop_edge = None
        return None
    
    def get_vertices(self, **kwargs):
        edges = kwargs.get("edges", None)
        if not edges:
            return None
        if not isinstance(edges, list):
            try:
                edges  = list(pm.PyNode(edges))
            except:
                return self.FAIL
        vert_list = set() 
        for edg in edges:
            con_vrt = edg.connectedVertices()
            for vrt in con_vrt:
                #print vrt
                vert_list.add(vrt)
        vert_list = list(vert_list)
        if not vert_list:
            return None
        return vert_list
    
    
    def get_loop_from_edge(self, **kwargs):
        edg = kwargs.get("edg", None)
        obj = kwargs.get("obj", None)
        edg_num = int((edg.split("[")[1]).replace("]", ""))
        pm.polySelect(obj, edgeLoopOrBorder = edg_num)
        edg_loop = pm.ls(selection = True, flatten = True)
        pm.select(clear = True)
        return edg_loop
    
    def get_next_edge(self, **kwargs):
        con_edg = kwargs.get("edg_con", None)
        loop = kwargs.get("edg_loop", None)
        prev_con_edg = kwargs.get("prev_edg_con", None)
        bridge_edge = set(con_edg).difference(set(loop))
        bridge_edge = list(bridge_edge.difference(set(prev_con_edg)))
        next_loop_edge = None
        if len(bridge_edge)>1:
            bridge_edge_connect = []
            for edg in bridge_edge:
                con_edg = pm.ls(edg.connectedEdges(), flatten = True)
                if bridge_edge_connect:
                    next_loop_edge = set(bridge_edge_connect).intersection(con_edg)
                    next_loop_edge = list(next_loop_edge.difference(set(loop)))
                bridge_edge_connect = con_edg
        return next_loop_edge
    
    def get_transform_from_component(self, **kwargs):
        comp = kwargs.get("comp", None)
        shape_node = pm.PyNode(str(comp).split(".")[0])
        transform_node = shape_node.parent(0)
        return (transform_node, shape_node)
    
    def place_objects(self, **kwargs):
        interval = kwargs.get("skip", 0)
        if not self.loop:
            pm.displayError("no Loops received")
            return None
        if interval>len(self.loop):
            pm.displayError("Skipping value larger than number of edges present")
            return self.FAIL
        jnt_lst = []
        index = 0
        max_len = len(self.loop)
        while index<max_len:
            pos = CustomScripts.midPos(selected_items = self.loop[index])
            jnt_lst.append(pm.joint(position = pos))
            if len(jnt_lst)>1:
                pm.parent(jnt_lst[-1], jnt_lst[-2])
                pm.joint(jnt_lst[-2], edit=True, orientJoint='xyz', 
                             secondaryAxisOrient='yup', zeroScaleOrient=True)
            index+=interval+1
        pm.select(jnt_lst[-2], jnt_lst[-1])
        CustomScripts.CopyJntOri()
        return jnt_lst
        
        
    def extract_loops(self, **kwargs):
        max_count = kwargs.get("max", 0)
        if not max_count:
            max_count = 2
        prev_con_edg = kwargs.get("prev_con_edg", [])
        selected_edges = kwargs.get("next_edg", [])
        self.safe_count+=1
        if self.safe_count>max_count:
            pm.displayWarning("Loop not ending")
            return self.FAIL
        if not selected_edges:
            selected_edges = pm.ls(orderedSelection = True, flatten = True)
        if self.init_flag:
            if len(selected_edges)<2:
                pm.displayError("Minimum 2 edge selection needed")
                return self.FAIL
            if len(selected_edges)>3:
                pm.displayError("More than 3 edges selected")
                return self.FAIL
            if len(selected_edges) == 3:
                self.stop_edge = selected_edges.pop(2)
            
            self.transform_node, self.shape_node = self.get_transform_from_component(comp = selected_edges[0])
            max_count = len(pm.ls(str(self.transform_node)+".e[*]", flatten = True))    
            

        next_edge = None
        for sel_edg in selected_edges:
            loop = self.get_loop_from_edge(edg = sel_edg, obj = self.transform_node)
            self.loop.append(loop)
            con_edg = pm.ls(sel_edg.connectedEdges(), flatten = True)
            if self.init_flag:
                self.init_flag = False
                prev_con_edg = con_edg
                self.init_loop = loop
                continue
            next_edge = self.get_next_edge(edg_con = con_edg, edg_loop = loop, prev_edg_con = prev_con_edg)
            if self.stop_edge in loop:
                return None
        if next_edge and len(next_edge)==1:
            if next_edge[0] in self.init_loop:
                return None
            self.extract_loops(prev_con_edg = con_edg, next_edg = next_edge, max = max_count)

        return self.SUCCESS
    
    
    def get_skin_cluster(self, **kwargs):
        node = kwargs.get("node", None)
        if isinstance(node, str):
            node = pm.PyNode(node)
        if isinstance(node, pm.Transform):
            node = node.getShape()
        if not node:
            return self.FAIL
        skin_cluster = pm.listConnections(node, type = "skinCluster")
        if skin_cluster:
            return skin_cluster[0]
        return skin_cluster
    
    
    def add_influence(self, **kwargs):
        skn_cls = kwargs.get("skin_cls", None)
        jnt_lst = kwargs.get("inf_lst", [])
        #skin_cluster = self.get_skin_cluster(node = self.shape_node)
        influence_objects = skn_cls.getInfluence()
        for inf_obj in influence_objects:
            pm.skinCluster(skn_cls, edit=True, influence=str(inf_obj), lockWeights=True)
        skn_cls.addInfluence(jnt_lst)
        for inf_obj in influence_objects:
            pm.skinCluster(skn_cls, edit=True, influence=str(inf_obj), lockWeights=False)
        return None
        
    def skin(self, **kwargs):
        skip = kwargs.get("skip", 0)
        jnt_lst = kwargs.get("joints", [])
        vert_lst = kwargs.get("vert_lst", [])
        skin_cluster = self.get_skin_cluster(node = self.shape_node)
        pm.select(clear = True)
        if not skin_cluster:
            skin_cluster = pm.skinCluster(jnt_lst[0], self.shape_node, toSelectedBones = True)
            self.add_influence(skin_cls = skin_cluster, inf_lst = jnt_lst[1:])
        else:
            self.add_influence(skin_cls = skin_cluster, inf_lst = jnt_lst)
            """
            influence_objects = skin_cluster.getInfluence()
            for inf_obj in influence_objects:
                pm.skinCluster(skin_cluster, edit=True, influence=str(inf_obj), lockWeights=True)
            skin_cluster.addInfluence(jnt_lst)
            for inf_obj in influence_objects:
                pm.skinCluster(skin_cluster, edit=True, influence=str(inf_obj), lockWeights=False)
            """
        if skin_cluster.getMaximumInfluences()<2:
            skin_cluster.setMaximumInfluences(2)
        jnt_index = 0
        jnt = str(jnt_lst[jnt_index])
        for verts in vert_lst:
            if (vert_lst.index(verts)>0) and (vert_lst.index(verts)%(skip+1) == 0):
                if skip<(len(jnt_lst)):
                    jnt_index+=1
                    jnt = str(jnt_lst[jnt_index])
            for vert in verts:
                pm.skinPercent(skin_cluster, vert, transformValue = (jnt,1.0))
        return None
    
    def run(self):
        skip_count = self.skip_val.getText()
        if not skip_count:
            skip_count = 0
        try:
            skip_count = int(skip_count)
        except ValueError:
            pm.displayError("invalid data type")
            return None
        
        extract = self.extract_loops()
        if extract == self.FAIL:
            self.init_var()
            return None
        joints_placed = self.place_objects(skip = skip_count)
        vtx = []
        for edg in self.loop:
            vertices = self.get_vertices(edges = edg)
            if vertices == self.FAIL:
                pm.displayError("Extracting Vertices failed at "+str(edg))
                self.init_var()
                return None
            vtx.append(vertices)
        if self.skn_chk.getValue():
            self.skin(joints = joints_placed, vert_lst = vtx, skip = skip_count)
        self.init_var()
        return None    


    def ui(self):
        WINDOW = "jointSequence"
        if pm.window(WINDOW, query = True, exists = True):
            pm.deleteUI(WINDOW)
        pm.window(WINDOW, title = "Continue Joints along loops", iconName = "JNTS")
        main_col = pm.columnLayout(adjustableColumn = True)
        guide_col = pm.columnLayout(parent = main_col)
        info_txt = "INFO:"+\
                   "\nFrom selected edges as starting point and"+\
                   "\ndirection guide, every next edge loop is"+\
                   "\nobtained till it reaches the end or the"+\
                   "\nstaring selection edge or the selected end point"
        guide_txt = "GUIDE:\nSelect 2 edges, each from adjacent loops"+\
                    "\nfirst edge is the starting point"+\
                    "\nsecond edge to guide the direction"+\
                    "\nif third edge is selected, acts as end point"
        pm.text(guide_txt, align = "left", parent = guide_col)
        pm.separator(parent = guide_col, height = 5, style = "in")
        pm.text(info_txt, align = "left", parent = guide_col)
        pm.separator(parent = main_col, height = 10)
        text_col = pm.rowColumnLayout(parent = main_col, numberOfColumns = 2, columnOffset = (2, "left",25))
        pm.text("number of loops to\nskip inbetween", parent = text_col)
        self.skip_val = pm.textField(text = "0", parent = text_col, width = 50)
        check_col = pm.rowColumnLayout(numberOfColumns = 2, parent = main_col, columnOffset = (2,"left", 120))
        pm.text("", parent = check_col)
        self.skn_chk = pm.checkBox("skin", parent = check_col)
        pm.separator(parent = main_col, style = "none", height = 5)
        pm.button("create", parent = main_col, command = lambda x: self.run())
                        
        pm.showWindow(WINDOW)
        pm.window(WINDOW, edit = True, widthHeight = (220, 230))
        return None