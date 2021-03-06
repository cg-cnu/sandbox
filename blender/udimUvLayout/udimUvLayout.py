 
import bpy

def main(context):

    Obj = bpy.context.object
    Ops = bpy.ops
    object_active = bpy.context.active_object
    object_data = bpy.data.objects[object_active.name].data

    # get the list of the material sot items.
    material_slots = len(object_active.material_slots.items())
    slot = x_tran = y_tran = 0
    
    # add  new uv Map 
    Ops.mesh.uv_texture_add()
    
    # rename it to the objectName_uvMap_Mari
    object_data.uv_textures.active.name = object_active.name + '_UVMap_Mari' 

    #iterate through the list of material slots
    while slot < material_slots:

        # set the index of the mtl to the current active mtl
        Obj.active_material_index = slot

        # select the vertices from the current mtl slot
        Ops.object.material_slot_select()

        # select the uvs from the vertices
        Ops.uv.select_all()    

        # Move the uv layout to the next grid
        Ops.transform.translate(value=(x_tran, y_tran, 0))

        # deselect the selected mtl slot
        Ops.object.material_slot_deselect()

        # increase slot 
        slot += 1
        value = str(slot) 
        if slot < 10:
            x_tran, y_tran = int(value[0]), 0           
        else:
            x_tran, y_tran = int(value[1]), int(value[0])

class udimUvLayout(bpy.types.Operator):
    """Layouts uvs in the mari uv format - UDIM """
    bl_idname = "object.udim_uv_layout"
    bl_label = "udim uv layout"

    @classmethod
    def poll(cls, context):
        return context.active_object is not None

    def execute(self, context):
        main(context)
        return {'FINISHED'}

def register():
    bpy.utils.register_class(udimUvLayout)
    km = bpy.context.window_manager.keyconfigs.default.keymaps['UV Editor']
    kmi = km.keymap_items.new("object.udim_uv_layout", 'U', 'PRESS', shift=True)

def unregister():
    bpy.utils.unregister_class(udimUvLayout)
    km = bpy.context.window_manager.keyconfigs.default.keymaps['UV Editor']
    for kmi in (kmi for kmi in km.keymap_items if kmi.idname in {"object.udim_uv_layout", }):
        km.keymap_items.remove(kmi) 

if __name__ == "__main__":
    register()