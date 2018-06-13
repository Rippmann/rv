

import Rhino
import rhinoscriptsyntax as rs
import scriptcontext as sc
import System.Array, System.Drawing.Color
import random
import string
import time

try:
   import cPickle as pickle
except:
   import pickle

from compas.datastructures.mesh import Mesh

from compas.utilities import geometric_key
from compas.geometry import centroid_points
from Rhino.RhinoMath import UnsetIntIndex

from utilities import verboseprint

add_line = sc.doc.Objects.AddLine
point_3d = Rhino.Geometry.Point3d
find_id = sc.doc.Objects.FindId
line_curve = Rhino.Geometry.LineCurve
replace_obj = sc.doc.Objects.Replace
from_rgb = System.Drawing.Color.FromArgb
color_from_object = Rhino.DocObjects.ObjectColorSource.ColorFromObject


def mesh_to_rhino(mesh, layer):

    # initiate group
    mesh_name = str(mesh.name)
    index = sc.doc.Groups.Add(mesh_name)
    rc = sc.doc.Groups.GroupName(index)

    # get layer index
    layer_index = sc.doc.Layers.FindByFullPath(layer, UnsetIntIndex)
    layer_rh = sc.doc.Layers[layer_index]
    index = layer_rh.LayerIndex
    
    # get objects by layer
    rh_objs = sc.doc.Objects.FindByLayer(layer)
    
    # all object ids on layer
    guids_layer = set([rhobj.Id for rhobj in rh_objs])
    
    guids_current = []
    count = 0
    for u,v, attr in mesh.edges(True):
        
        # skip passive edges
        if not attr['passive']:

            # get start and end points of the edge
            s_pt = mesh.vertex_coordinates(u)
            e_pt = mesh.vertex_coordinates(v)
            
            # set master back to False
            attr['master'] = False
            # get obj guid form mesh
            guid = attr['id']
            guid = System.Guid(guid)
            
            if guid:
                # update line objects if they exist
                start = point_3d(*s_pt)
                end = point_3d(*e_pt)
                line_rh = line_curve(start,end)
                flag = replace_obj(guid,line_rh)

                # add new line object if the guid cannot be found
                if not flag:
                    count += 1
                    guid = add_line(start, end)
                    # save new guid to mesh edge attributes
                    attr['id'] = str(guid)
                
                # update or apply attributes to line object
                rh_obj = find_id(guid)
                if not flag:
                    name = 'e_' + str(u) + '_' + str(v)
                    rh_obj.Attributes.Name = name
                
                rh_obj.Attributes.LayerIndex = index
                color = attr['color']
                rh_obj.Attributes.ObjectColor = from_rgb(*color)
                rh_obj.Attributes.ColorSource = color_from_object
                rh_obj.CommitChanges()
                
                
            # all guids represented by edges in the current mesh
            guids_current.append(guid)
            
            u_last, v_last = u, v
    
    verboseprint('Numer of lines modified: ' + str(len(guids_current) - count))
    verboseprint('Numer of new lines added: ' + str(count))
    
    
    sc.doc.Groups.AddToGroup(index,rs.coerceguidlist(guids_current))
    
    
    # save a pickled version of the mesh.data to the "last" edge (master edges)
    mesh_data = pickle.dumps(mesh.data)
        
        
    rh_obj = find_id(guid)
    rh_obj.Attributes.SetUserString('mesh_data', mesh_data)
    rh_obj.CommitChanges()
    mesh.set_edge_attribute((u_last, v_last),'master',True)
    
    # delete all objects on layer that are not stored in the mesh object
    guids_current = set(guids_current)
    to_del_objs = list(guids_layer.difference(guids_current))
    
    verboseprint('Numer of objects deleted: ' + str(len(to_del_objs)))
    for id in to_del_objs:
        sc.doc.Objects.Delete(id, True)

    # redraw 
    sc.doc.Views.Redraw()
    

def mesh_from_rhino(mesh, layer):
    
    # get objects by layer
    rh_objs = sc.doc.Objects.FindByLayer(layer)
    
    # iterate over all objects on layer
    coords = {}
    mesh_data = None
    index = None
    index_u, index_v = None, None
    for i, rh_obj in enumerate(rh_objs):
        # check if curve object
        object_type = rh_obj.ObjectType
        if object_type == Rhino.DocObjects.ObjectType.Curve:
            
            # get start and end points of line
            curve = rh_obj.Geometry
            start = curve.PointAtStart
            end = curve.PointAtEnd
            
            # get name
            name = rh_obj.Attributes.Name
            # check if name exists and is valid
            if name:
                data = name.split('_')
                if len(data) == 3:
                    u,v  = int(data[1]), int(data[2])
                    coords[u] = start
                    coords[v] = end
                    # read in mesh data from user string
                    if mesh_data == None:
                        mesh_data = rh_obj.Attributes.GetUserString('mesh_data')
                        if mesh_data:
                            index = i
                            index_u, index_v = u, v
                            
    
    if index == None and not mesh: return None
    
    verboseprint('Index at which mesh_data UserString was found: ' + str(index))
    verboseprint('u and v where mesh_data UserString was found: ' + str((index_u, index_v)))
    
    
    if not mesh_data:
        verboseprint('No geometry found. Mesh solely constructed from sticky variable.')

    if not mesh and mesh_data:
        verboseprint('No mesh object found. Mesh constructed from unpickled data.')
        mesh_data = pickle.loads(mesh_data)
        mesh = Mesh()
        mesh.data = mesh_data
    
    for key, attr in mesh.vertices(True):
        if key in coords:
            x, y, z = coords[key]
            attr['x'] = x
            attr['y'] = y
            attr['z'] = z
            
    return mesh

def initiate_mesh(layer):
    
    objs = rs.ObjectsByLayer(layer)
    lines = [(rs.CurveStartPoint(crv), rs.CurveEndPoint(crv)) for crv in objs]
    rs.DeleteObjects(objs)
    
    objs_dict = {}
    for i, pts in enumerate(lines):
        cent = centroid_points(pts)
        objs_dict[geometric_key(cent)] = str(objs[i]) 
        
    mesh = Mesh.from_lines(lines)
    
    for u,v, attr in mesh.edges(True):
        cent = centroid_points([mesh.vertex_coordinates(u), mesh.vertex_coordinates(v)])
        attr['master'] = False
        attr['color'] = [50, 255, 100]
        attr['passive'] = False
        attr['id'] = objs_dict[geometric_key(cent)]
        name = 'e_' + str(u) + '_' + str(v)
        
    return mesh


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


