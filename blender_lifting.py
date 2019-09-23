# Importing global modules
import subprocess
import sys
import json
import os

ADDON_PATH = os.path.dirname(os.path.abspath(__file__))
sys.path.append(ADDON_PATH + "/blender_lifting_venv/Lib/site-packages")

# Importing blender_lifting specific modules
import numpy

#Importing Blender modules
import bpy
from mathutils import Vector

APP_PATH = ADDON_PATH + "/lifter.py"
CONNECTIONS = [ [0, 1], [1, 2], [2, 3], [0, 4], [4, 5], [5, 6], [0, 7], [7, 8],
                [8, 9], [9, 10], [8, 11], [11, 12], [12, 13], [8, 14], [14, 15],
                [15, 16] ]               
LIFTING_BONE_NAMES = ['pelvis_r', 'thigh_r', 'calf_r', 'pelvis_l', 'thigh_l', 'calf_l', 
                      'waist', 'chest', 'neck', 'head', 
                      'shoulder_l', 'arm_l', 'forearm_l', 'shoulder_r', 'arm_r', 'forearm_r']
LIFTING_BONE_PARENTS = {'pelvis_r': 'base', 
                        'thigh_r': 'pelvis_r', 
                        'calf_r': 'thigh_r', 
                        'pelvis_l': 'base', 
                        'thigh_l': 'pelvis_l', 
                        'calf_l': 'thigh_l', 
                        'waist': 'base', 
                        'chest': 'waist', 
                        'neck': 'chest', 
                        'head': 'neck', 
                        'shoulder_l': 'neck', 
                        'arm_l': 'shoulder_l', 
                        'forearm_l': 'arm_l', 
                        'shoulder_r': 'neck', 
                        'arm_r': 'shoulder_r', 
                        'forearm_r': 'arm_r'
                        }
        
image_path = ADDON_PATH + "/data/images/Tan-suit.jpeg"
session_path = ADDON_PATH + "/data/saved_sessions/init_session/init"
prob_model_path = ADDON_PATH + "/data/saved_sessions/prob_model/prob_model_params.mat"

def _add_bezier(v0, v1, name, scale=1.0, dimensions='3D', bevel_depth = 5): 
    '''
    Creates a bezier curve data object and scene object between two vectors 

    :param v0: World location of the first vertex as list
    :param v1: World location of the second vertex as list
    :param dimensions: Dimension of the bezier
    :param bevel_depth: Depth of the bevel or thickness of the curve
    '''
    # From https://blender.stackexchange.com/questions/110177/connecting-two-points-with-a-line-curve-via-python-script
    v0, v1 = Vector(v0), Vector(v1)  
    origin = (v0 + v1) / 2  

    curve = bpy.data.curves.new('Curve_dat' + name, 'CURVE')
    spline = curve.splines.new('BEZIER')
    
    bp0 = spline.bezier_points[0]
    bp0.co = v0 - origin
    bp0.handle_left_type = bp0.handle_right_type = 'AUTO'

    spline.bezier_points.add(count=1)
    bp1 = spline.bezier_points[1]
    bp1.co = v1 - origin
    bp1.handle_left_type = bp1.handle_right_type = 'AUTO'
    
    ob = bpy.data.objects.new('Curve_obj' + name, curve)
    ob.matrix_world.translation = origin
    bpy.data.objects['Curve_obj' + name].data.dimensions = dimensions
    bpy.data.objects['Curve_obj' + name].data.bevel_depth = bevel_depth * scale
    bpy.context.scene.collection.objects.link(bpy.data.objects['Curve_obj' + name])
    # return ob

def lift_image(img_path):
    '''
    Calls lifter.py in a separate process. This takes in an image and estimates a 3D pose from a 2D image. 

    :param img_path: Filepath to image that will be analyzed
    :return returned_val: a JSON object that contains the 3D coordinates of each joint.
    '''
    returned_bin = subprocess.check_output(['python', APP_PATH, img_path, session_path, prob_model_path])
    returned_val = json.loads(returned_bin.decode('utf-8'))
    return returned_val


def create_curve_skeleton(coordinates, name, scale=1.0):
    """
    Iterates through input coordinates acquired from lift_image() and creates a bezier curve skeleton. For preview use mainly. 
    Since create_armature has been implemented, this feature is rather useless

    :param coordinates: List of vertex coordinates from lifter
    :param name: Base name of the bezier_curves 
    :param scale: Scale of the skeleton TODO: Implement scaling
    """
    curve_nr = 0
    for conn in CONNECTIONS:
        _add_bezier(coordinates[conn[0]], coordinates[conn[1]], 'bez_' + LIFTING_BONE_NAMES[curve_nr], scale=scale)
        curve_nr += 1

def create_armature(coordinates, name, scale=1.0):
    """
    Creates an armature skeleton data object from the input coordinates acquired from lift_image(). 
    The skeleton's bones will have been appropriately labelled and parented.
    The skeleton data object will be implemented into the scene as well.

    :param coordinates: List of vertex coordinates from lifter
    :param name: Base name of the bezier_curves 
    :param scale: Scale of the skeleton TODO: Implement scaling
    """
    # Setting the scale to a hundredth already as the distances from lifting are considerably large.
    scale = scale * 0.01  
    arm_dat_name = 'Armature_dat_' + name
    arm_obj_name = 'Armature_obj_' + name
    
    arm_dat = bpy.data.armatures.new(arm_dat_name)
    arm_obj = bpy.data.objects.new(arm_obj_name, arm_dat)
    
    bpy.context.scene.collection.objects.link(arm_obj)
    bpy.context.view_layer.objects.active = arm_obj
    
    bpy.ops.object.mode_set(mode='EDIT', toggle=False)
    
    edit_bones = bpy.data.armatures[arm_dat_name].edit_bones
    
    b = edit_bones.new('base')
    b.head = [coordinates[0][0]*scale, coordinates[0][1]*scale + 200*scale, coordinates[0][2]*scale]
    b.tail = [coordinates[0][0]*scale, coordinates[0][1]*scale,             coordinates[0][2]*scale]
    
    bone_nr = 0
    for conn in CONNECTIONS:
        b = edit_bones.new(LIFTING_BONE_NAMES[bone_nr])
        b.head = [scale*item for item in coordinates[conn[0]]]
        b.tail = [scale*item for item in coordinates[conn[1]]]
        #b.parent = LIFTING_BONE_PARENTS[LIFTING_BONE_NAMES[bone_nr]]
        bone_nr += 1
    
    for bone in edit_bones:
        if str(bone.name) != 'base':
            edit_bones[str(bone.name)].parent = edit_bones[LIFTING_BONE_PARENTS[str(bone.name)]]

    bpy.ops.object.mode_set(mode='OBJECT')