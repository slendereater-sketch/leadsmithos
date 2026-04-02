import bpy
from bpy.types import Menu

class VIEW3D_MT_z2a_forge_pie(Menu):
    bl_label = "Ally Forge"

    def draw(self, context):
        layout = self.layout
        pie = layout.menu_pie()
        # 4-way radial menu for quick access
        pie.operator("transform.translate", text="Grab (Stick L)", icon='MOVE')
        pie.operator("transform.rotate", text="Rotate (Stick R)", icon='ROTATE')
        pie.operator("transform.resize", text="Scale (Triggers)", icon='FULLSCREEN_ENTER')
        pie.operator("mesh.extrude_region_move", text="Extrude (Button A)", icon='EXTRUDE')

def register():
    bpy.utils.register_class(VIEW3D_MT_z2a_forge_pie)
    
    # Set UI Scale for handheld
    bpy.context.preferences.view.ui_scale = 1.4
    
    # Set up a keybinding to trigger the pie menu (e.g., mapping to a key that the gamepad bridge can send)
    # For now, we'll map it to 'V'
    wm = bpy.context.window_manager
    kc = wm.keyconfigs.addon
    if not kc:
        kc = wm.keyconfigs.new('ally_controls')
    km = kc.keymaps.new(name='3D View', space_type='VIEW_3D')
    kmi = km.keymap_items.new("wm.call_menu_pie", 'V', 'PRESS')
    kmi.properties.name = "VIEW3D_MT_z2a_forge_pie"

    # Enable Pie Menus official addon
    if "ui_pie_menus_official" not in bpy.context.preferences.addons:
        try:
            bpy.ops.preferences.addon_enable(module="ui_pie_menus_official")
        except:
            pass

    print("LeadSmith Ally Forge Module Loaded - Press 'V' for Radial Menu")

def unregister():
    bpy.utils.unregister_class(VIEW3D_MT_z2a_forge_pie)

if __name__ == "__main__":
    register()

