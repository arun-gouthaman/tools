import pymel.all as pm


class replaceInstance(object):
    def getShapeNode(self):
        parentNode = pm.ls(selection=True)
        pm.select(hierarchy=True)
        shapeNodes = self.extractShapeNodeNames()
        instanceNodes = self.getInstances(parentNode, shapeNodes)
        self.replaceInstances(parentNode, instanceNodes)
        pm.select(clear=True)
        pm.select(parentNode)

    def getInstances(self, parentNode, shapeNodes):
        instanceNodes = []
        pm.select(all=True)
        pm.select(parentNode, deselect=True, hierarchy=True)
        curSelTrnsNds = pm.ls(selection=True, transforms=True)
        pm.select(clear=True)
        for curSelTrnsNd in curSelTrnsNds:
            pm.select(curSelTrnsNd, hierarchy=True)
            shp = self.extractShapeNodeNames()
            if shp == shapeNodes:
                instanceNodes.append(curSelTrnsNd)
        return instanceNodes

    def extractShapeNodeNames(self):
        shapeNodes = []
        shapes = pm.ls(pm.ls(selection=True, shapes=True))
        if shapes:
            for shape in shapes:
                shapeNodes.append(str(shape))
            for i in range(len(shapeNodes)):
                shapeNodes[i] = shapeNodes[i].split('|')
                for shapeNd in shapeNodes[i]:
                    if shapeNd.find('Shape'):
                        shapeNodes[i] = shapeNd
            return shapeNodes

    def replaceInstances(self, parentNode, instanceNodes):
        for instanceNode in instanceNodes:
            trans = pm.getAttr(str(instanceNode) + '.translate')
            rot = pm.getAttr(str(instanceNode) + '.rotate')
            scl = pm.getAttr(str(instanceNode) + '.scale')
            pm.delete(instanceNode)
            pm.duplicate(parentNode, name=str(instanceNode))
            pm.setAttr(str(instanceNode) + '.translate', trans)
            pm.setAttr(str(instanceNode) + '.rotate', rot)
            pm.setAttr(str(instanceNode) + '.scale', scl)
        return


test = replaceInstance()
test.getShapeNode()
