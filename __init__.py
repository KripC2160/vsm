
import bpy 
import os 

from bpy.types import Operator 
from bpy.props import (EnumProperty)

bl_info = {
    "name": "VMS",
    "catergory": "Import and Downloader"
} 

class vms_search_local(Operator):
    bl_idname = "vms.searchlocal"
    bl_label = "Search Skins"
    bl_property = "loc_search"
    
    folder = bpy.path.abspath("C:\\Users\\user\\Desktop\\valimptestfolder")
    blends = [f for f in os.listdir(folder) if f.endswith(".blend")]
    
    items = ()
    
    for blend in blends:
        blend_path = os.path.join(folder, blend)
        with bpy.data.libraries.load(blend_path) as (data_from, _):
            for c in data_from.collections:
                collitem = (c, c, "")
                items = (collitem,) + items
    
    loc_search: EnumProperty(
        name="Local Search",
        items = items,
    )
    
    def execute(self, context):
        return {"FINISHED"}
    
    def invoke(self, context, event):
        context.window_manager.invoke_search_popup(self)
        return {"RUNNING_MODAL"}
        

class vms_main(bpy.types.Panel):
    bl_label = "VMS"
    bl_idname = __name__
    bl_space_type = "VIEW_3D"
    bl_region_type = "UI"
    bl_category = "VMS"
    bl_label = "VMS"
    
    def draw(self, context):
        layout = self.layout
        
        layout.operator(vms_search_local.bl_idname, text = "Search Skins", icon="SORT_ASC")

classes = (
    vms_search_local,
    vms_main,
)

def register():
    for cls in classes:
        bpy.utils.register_class(cls)
    
def unregister():
    for cls in classes:
        bpy.utils.unregister_class(cls)
        
if __name__ == "__main__":
    register()