import sys
import os

import scriptcontext as sc 
import Rhino

from _config import RVinfo
from _config import verboseprint

def sys_path_init(): 
    info = RVinfo
    
    try:
        path = sc.sticky["path"]
        sys.path.append(path)
    except:
        verboseprint(info.message('i_init'))
        path = Rhino.PlugIns.PlugIn.PathFromName("rhinovault_V2")
        if path:
            path = os.path.split(path)[0]
            sys.path.append(path)
            sc.sticky["path"] = path
        else:
            info.message_box('e_plugin', 16)
            return None
    return True
        
        