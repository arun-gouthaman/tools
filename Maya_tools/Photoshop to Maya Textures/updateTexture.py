import pymel.all as pm

class texUpd(object):
    def __init__(self, fileList):
        self.fileList = fileList
        self.update(self.fileList)
        pass
    
    def update(self, fileList):
        fileNames = fileList.split(',')
        texs = pm.ls(textures=True)
        
        for tex in texs:
            for fileName in fileNames:
                texName = tex.fileTextureName.get()
                if texName.find(fileName+'.')!=-1: 
                    tex.fileTextureName.set(texName)
                    print texName + " UPDATED"
                    
        
        
        import os
        path = texs[0].fileTextureName.get().split('/')
        path[-1] = 'run.bat'
        fileLoc = "/".join(path)
        os.remove(fileLoc)
        
