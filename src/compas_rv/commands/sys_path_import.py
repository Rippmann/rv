import sys
import os

import scriptcontext 
import Rhino

from config import RVinfo
info = RVinfo

try:
    path = sc.sticky["path"]
    sys.path.append(path)
except:
    print info.message('i_init')
    path = Rhino.PlugIns.PlugIn.PathFromName("rhinovault_V2")
    if path:
        path = os.path.split(path)[0]
        sys.path.append(path)
        scriptcontext.sticky["path"] = path
    else:
        info.message_box('e_plugin', 16)
        raise Exception()
        
        