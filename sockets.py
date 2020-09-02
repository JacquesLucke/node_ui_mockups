import bpy

class BaseSocket:
    color = (0, 0, 0, 0)
    input_link_limit = 1
    output_link_limit = 0 # no limit

    def draw_color(self, context, node):
        return self.color

    def draw(self, context, layout, node, text):
        layout.label(text=text)

class InfluencesSocket(bpy.types.NodeSocket, BaseSocket):
    bl_idname = "InfluencesSocket"
    bl_label = "Influences Socket"
    color = (0.8, 0.8, 0.2, 1.0)
    input_link_limit = 0

class DynamicsSocket(bpy.types.NodeSocket, BaseSocket):
    bl_idname = "DynamicsSocket"
    bl_label = "Dynamics Socket"
    color = (0.8, 0.2, 0.2, 1.0)
    input_link_limit = 0

class GeometrySocket(bpy.types.NodeSocket, BaseSocket):
    bl_idname = "GeometrySocket"
    bl_label = "Geometry Socket"
    color = (0.2, 0.8, 0.2, 1.0)
    input_link_limit = 0

def find_socket_cls_by_idname(idname):
    def recursive_find(base_class):
        if getattr(base_class, "bl_idname", "") == idname:
            return base_class
        for sub_class in base_class.__subclasses__():
            found_cls = recursive_find(sub_class)
            if found_cls is not None:
                return found_cls
    return recursive_find(bpy.types.NodeSocket)
