
import bpy 
import os 
import requests
import json

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
    
    skin_codenames = []
    skin_realnames = []
    items = ()
    gun_names = ['Ares', 'Bucky', 'Bulldog', 'Classic', 'Frenzy', 'Ghost', 'Guardian', 'Judge', 'Marshal', 'Odin',
                 'Operator', 'Phantom', 'Sheriff', 'Shorty', 'Spectre', 'Stinger', 'Vandal', 'Knife'
    ]
                
    json_file = "https://raw.githubusercontent.com/KripC2160/vsm/main/weapons.json" #retreives the json file from the github repo
    r = requests.get(json_file)
    
    with open("C:\\Users\\user\\Desktop\\weapons.json", 'wb') as f:
        f.write(r.content)

    input_content = open('C:\\Users\\user\\Desktop\\weapons.json')#r.content
    json_array = json.load(input_content)
    
    for item in json_array:
        skin_codenames.append(item['codename'])
        skin_realnames.append(item['name'])
    
    for i in skin_realnames:
        for gun in gun_names:
            jsonitem = (i+' '+gun, i+' '+gun, "")
            items = (jsonitem,) + items #adds the item in the tuple to be used for the search list


    
    #print(items)
    
    loc_search: EnumProperty(
        name="Local Search",
        items = items,
    )
    
    def execute(self, context):
        self.report({'INFO'}, "Selected:" + self.loc_search)
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