import sys
import os

import scriptcontext as sc 
import Rhino

from config import RVinfo

def sys_path_init(): 
    info = RVinfo
    
    try:
        path = sc.sticky["path"]
        sys.path.append(path)
    except:
        print info.message('i_init')
        path = Rhino.PlugIns.PlugIn.PathFromName("rhinovault_V2s")
        if path:
            path = os.path.split(path)[0]
            sys.path.append(path)
            sc.sticky["path"] = path
        else:
            info.message_box('e_plugin', 16)
            return None
    return True
        
        