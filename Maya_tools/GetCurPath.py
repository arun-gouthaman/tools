import os
class Get_Cur_Path(object):
    def __init__(self):
        return None

    def get_cur_path(self, **kwargs):
        file_name = kwargs.get("file_name", None)
        path = os.path.abspath(__file__)
        path = os.path.dirname(path)
        if file_name:
            path = path+"\\"+file_name
        return path
