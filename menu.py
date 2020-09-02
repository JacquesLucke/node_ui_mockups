import bpy
from . nodes import BaseNode

class MockupNodesMenu(bpy.types.Menu):
    bl_idname = "NODE_MT_mockup_nodes_menu"
    bl_label = "Mockup Nodes"

    def draw(self, context):
        for node_class in BaseNode.__subclasses__():
            self.add_node(node_class.bl_idname, node_class.bl_label)

    def add_node(self, idname, name):
        props = self.layout.operator("node.add_node", text=name)
        props.type = idname
        props.use_transform = True

def draw_menu(self, context):
    self.layout.menu(MockupNodesMenu.bl_idname, text="Mockups")

def register():
    bpy.types.NODE_MT_add.append(draw_menu)

def unregister():
    bpy.types.NODE_MT_add.remove(draw_menu)
