import scriptcontext as sc
import rhinoscriptsyntax as rs
import Rhino
import System

import time

from compas.datastructures.mesh import Mesh

from compas.utilities import geometric_key
from compas.geometry import centroid_points

from compas_rv.commands._config import verboseprint


if __name__ == "__main__":

    layer = 'Layer 01'
    
    try:
        mesh = sc.sticky["mesh"]
        verboseprint('Mesh variable found.')
    except:
        verboseprint('NO mesh variable found.')
        mesh = None

    tic = time.time()
    mesh = mesh_from_rhino(mesh, layer)
    if not mesh:
        verboseprint('No mesh data found. New mesh initialised from lines.')
        mesh = initiate_mesh(layer)
    tac = time.time()
    verboseprint('Time to read mesh data (s): ' + str(tac-tic))
     
    
    
    for u,v, attr in mesh.edges(True):
        attr['color'] = [random.random()*255, 0, 100]
        if random.random() > .5:
            attr['passive'] = False
    
    
    #mesh = None
    
    
    tic = time.time()
    mesh_to_rhino(mesh, layer)
    tac = time.time()
    verboseprint('Time to write mesh data (s): ' + str(tac-tic))
    
    sc.sticky["mesh"] = mesh


