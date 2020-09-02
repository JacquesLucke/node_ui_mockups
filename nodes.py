from __future__ import annotations
import bpy
from .sockets import find_socket_cls_by_idname

class BaseNode:
    def init(self, context):
        builder = NodeBuilder()
        self.declaration(builder)
        builder.refresh_node(self)

    def declaration(self, builder: NodeBuilder):
        pass

    def draw_buttons(self, context, layout):
        self.draw(layout)

    def draw(self, layout):
        pass

class NodeBuilder:
    def __init__(self):
        self._inputs = []
        self._outputs = []

    def input(self, idname, name):
        self._inputs.append((idname, name))

    def output(self, idname, name):
        self._outputs.append((idname, name))

    def refresh_node(self, node):
        node.inputs.clear()
        node.outputs.clear()
        for idname, name in self._inputs:
            socket_cls = find_socket_cls_by_idname(idname)
            socket = node.inputs.new(idname, name, identifier=name)
            socket.link_limit = getattr(socket_cls, "input_link_limit", 1)
        for idname, name in self._outputs:
            socket_cls = find_socket_cls_by_idname(idname)
            socket = node.outputs.new(idname, name, identifier=name)
            socket.link_limit = getattr(socket_cls, "output_link_limit", 0)

class ParticleDynamicsNode(bpy.types.Node, BaseNode):
    bl_idname = "ParticleDynamicsNode"
    bl_label = "Particle Dynamics"
    bl_icon = 'PHYSICS'

    def declaration(self, builder):
        builder.input("InfluencesSocket", "Influences")
        builder.output("DynamicsSocket", "Particle Dynamics")

    def draw(self, layout):
        layout.prop(self, "name", text="", icon='PARTICLES')

class AddInfluencesNode(bpy.types.Node, BaseNode):
    bl_idname = "AddInfluencesNode"
    bl_label = "Add Influences"

    def declaration(self, builder):
        builder.input("DynamicsSocket", "Dynamics")
        builder.input("InfluencesSocket", "Influences")
        builder.output("DynamicsSocket", "Dynamics")

class SimulateParticlesNode(bpy.types.Node, BaseNode):
    bl_idname = "SimulateParticlesNode"
    bl_label = "Simulate Particles"
    bl_icon = 'PHYSICS'

    def declaration(self, builder):
        builder.input("DynamicsSocket", "Particle Dynamics")
        builder.input("InfluencesSocket", "Global Influences")
        builder.output("GeometrySocket", "Particles Geometry")

class ParticleMeshEmitterNode(bpy.types.Node, BaseNode):
    bl_idname = "ParticleMeshEmitterNode"
    bl_label = "Particle Mesh Emitter"

    def declaration(self, builder):
        builder.input("GeometrySocket", "Geometry")
        builder.input("NodeSocketFloat", "Rate")
        builder.input("NodeSocketFloat", "...")
        builder.output("InfluencesSocket", "Emitter")

class ForcesFromSceneNode(bpy.types.Node, BaseNode):
    bl_idname = "ForcesFromSceneNode"
    bl_label = "Forces from Scene"

    def declaration(self, builder):
        builder.input("NodeSocketFloat", "Gravity Strength")
        builder.input("NodeSocketFloat", "Vortex Strength")
        builder.input("NodeSocketFloat", "...")
        builder.output("InfluencesSocket", "Forces")

class ColliderGeometryNode(bpy.types.Node, BaseNode):
    bl_idname = "ColliderGeometryNode"
    bl_label = "Collider Geometry"

    def declaration(self, builder):
        builder.input("GeometrySocket", "Geometry")
        builder.input("NodeSocketFloat", "Stickiness")
        builder.input("NodeSocketFloat", "Damping")
        builder.input("NodeSocketFloat", "...")
        builder.output("InfluencesSocket", "Collider")

class GeometryFromObjectNode(bpy.types.Node, BaseNode):
    bl_idname = "GeometryFromObjectNode"
    bl_label = "Geometry From Object"

    def declaration(self, builder):
        builder.input("NodeSocketObject", "Object")
        builder.output("GeometrySocket", "Geometry")

class FilterDynamicsNode(bpy.types.Node, BaseNode):
    bl_idname = "FilterDynamicsNode"
    bl_label = "Filter Dynamics"

    def declaration(self, builder):
        builder.input("DynamicsSocket", "Dynamics")
        builder.input("Geometry", "Geometry")
        builder.output("Geometry", "Geometry")
