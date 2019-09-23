bl_info = {
    "name": "Blender Lifting",
    "author": "Haryo Sukmawanto",
    "version": (0, 0, 1),
    "blender": (2, 80, 0),
    "location": "View3D > Properties",
    "description": "Blender add-on for Lifting From The Deep",
    "category": "Animation"
    }

from . import blender_lifting
from . import interface

def register():
    interface.register()

def unregister():
    interface.unregister()