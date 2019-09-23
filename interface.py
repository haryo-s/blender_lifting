from . import blender_lifting

#Importing Blender modules
import bpy
from mathutils import Vector

# ------------------------------------------------------------------------
#    Interface
# ------------------------------------------------------------------------

from bpy.props import (StringProperty,
                       BoolProperty,
                       IntProperty,
                       FloatProperty,
                       FloatVectorProperty,
                       EnumProperty,
                       PointerProperty,
                       )
from bpy.types import (Panel,
                       Menu,
                       Operator,
                       PropertyGroup,
                       )


# ------------------------------------------------------------------------
#    Scene Properties
# ------------------------------------------------------------------------

class MyProperties(PropertyGroup):
    armature_name_field: StringProperty(
        name="Armature name",
        description="Armature name",
        default="",
        maxlen=1024,
        )
    image_path_field : StringProperty(
        name = "Image path",
        description="Choose an image to analyze:",
        default="",
        maxlen=1024,
        subtype='FILE_PATH'
        )
    scale_field: FloatProperty(
        name = "Scale",
        description = "Scale of the resulting armature",
        default = 1.0,
        min = 0.01,
        max = 100.0
        )
    prob_model_path_field: StringProperty(
        name = "ADVANCED: Probability Model",
        description="Choose a directory:",
        default=blender_lifting.prob_model_path,
        maxlen=1024,
        subtype='FILE_PATH'
        )
    sessions_path_field: StringProperty(
        name = "ADVANCED: Saved Sessions",
        description="Choose a directory:",
        default=blender_lifting.session_path,
        maxlen=1024,
        subtype='FILE_PATH'
        )
        
# ------------------------------------------------------------------------
#    Operators
# ------------------------------------------------------------------------

class WM_OT_CreateArmature(Operator):
    bl_label = "Create an armature from a 2D image"
    bl_idname = "wm.create_armature"

    def execute(self, context):
        scene = context.scene
        mytool = scene.my_tool

        # print the values to the console
        print(str(mytool.image_path_field))
        coordinates = blender_lifting.lift_image(mytool.image_path_field)
        blender_lifting.create_armature(coordinates, mytool.armature_name_field)

        return {'FINISHED'}

# ------------------------------------------------------------------------
#    Menus
# ------------------------------------------------------------------------

class OBJECT_MT_CustomMenu(bpy.types.Menu):
    bl_label = "Select"
    bl_idname = "OBJECT_MT_custom_menu"

    def draw(self, context):
        layout = self.layout

        # Built-in operators
        layout.operator("object.select_all", text="Select/Deselect All").action = 'TOGGLE'
        layout.operator("object.select_all", text="Inverse").action = 'INVERT'
        layout.operator("object.select_random", text="Random")

# ------------------------------------------------------------------------
#    Panel in Object Mode
# ------------------------------------------------------------------------

class OBJECT_PT_BlenderLiftingPanel(Panel):
    bl_label = "blender_lifting"
    bl_idname = "OBJECT_PT_custom_panel"
    bl_space_type = "VIEW_3D"   
    bl_region_type = "UI"
    bl_category = "Tools"
    bl_context = "objectmode"   


    @classmethod
    def poll(self,context):
        return context.object is not None

    def draw(self, context):
        layout = self.layout
        scene = context.scene
        mytool = scene.my_tool

        layout.prop(mytool, "image_path_field")
        layout.prop(mytool, "scale_field")
        layout.prop(mytool, "armature_name_field") 
        layout.operator("wm.create_armature")
        
        layout.prop(mytool, "prob_model_path_field")
        layout.prop(mytool, "sessions_path_field")

        layout.separator()

# ------------------------------------------------------------------------
#    Registration
# ------------------------------------------------------------------------

classes = (
    MyProperties,
    WM_OT_CreateArmature,
    OBJECT_MT_CustomMenu,
    OBJECT_PT_BlenderLiftingPanel
)

def register():
    from bpy.utils import register_class
    for cls in classes:
        register_class(cls)

    bpy.types.Scene.my_tool = PointerProperty(type=MyProperties)

def unregister():
    from bpy.utils import unregister_class
    for cls in reversed(classes):
        unregister_class(cls)
    del bpy.types.Scene.my_tool

if __name__ == "__main__":
    register()