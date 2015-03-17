# ability to refresh nodes
# ability to pick the channel naming convention
# get the frames name right
# get the node names and labels right.
# generate based on the subfolders

bl_info = {
    "name": "UDIM tools",
    "description": " Create the udim network out of the maps on disk ",
    "author": "Sreenivas Alapati",
    "version": (1, 0),
    "blender": (2, 45, 0),
    "category": "Node"}

import os
import bpy
from bpy.props import StringProperty

bpy.types.Scene.udimPath = StringProperty(
                                name = "Map Path",
                                description = "Provide the path to the maps.")

bpy.types.Scene.udimGroupName = StringProperty(
                                name = "Group Name",
                                description = "Provide the name of the group.")

from bpy_extras.image_utils import load_image


class UIPanel(bpy.types.Panel):
    bl_label = "Property panel"
    bl_space_type = "NODE_EDITOR"
    bl_region_type = "UI"
    bl_label = "UDIM Tools"
 
    def draw(self, context):
        layout = self.layout
        scn = bpy.context.scene
        # sub folders... ? 
        #layout.prop(scn, 'MyBool')
        layout.prop(scn, 'udimPath')
        layout.prop(scn, 'udimGroupName')
        layout.operator("node.create_udim_node")

class UdimNodeCreator(bpy.types.Operator):
    """ Displays wire frame on shaded with draw all edges on all objects"""
    bl_idname = "node.create_udim_node"
    bl_label = "create UDIM node"
    bl_description = "Create udim node network from the given path"
    bl_options = {'REGISTER', 'UNDO'}
    #label_prop = StringProperty(name='Label', default=' ', description='The visual name of the frame node')
    #color_prop = FloatVectorProperty(name="Color", description="The color of the frame node", default=(0.6, 0.6, 0.6),
                                     # min=0, max=1, step=1, precision=3, subtype='COLOR_GAMMA', size=3)


    @classmethod
    def poll(cls, context):
        space = context.space_data
        valid = False
        if space.type == 'NODE_EDITOR':
            if space.node_tree is not None:
                valid = True
        return valid

    def execute(self, context):

        ### INPUT PATH OVER HERE ###
        #path = "/home/salaati/Downloads/oslUdim/maps/"
        #path = "/home/salaati/Downloads/rhAbnTitanGGTex/diffuse"

        udimPath = bpy.context.scene["udimPath"]
        # clear the input
        # bpy.context.scene["udimPath"] = ""
        # clear the input
        # bpy.context.scene["udimPath"] = ""
        # print (udimPath)
        # udimGroupName = bpy.context.scene['udimGroupName']
        # print (groupName)
        #################################


        # get the active material
        activeMaterial = bpy.context.object.active_material

        # if not activeMaterial:
            # raise an error

        # if use nodes not enabled ? enable it
        if activeMaterial.use_nodes == False:
            activeMaterial.use_nodes = True

        # create new group
        group = bpy.data.node_groups.new(type="ShaderNodeTree", name="testgroup")
        # get the nodes of the group
        nodes = group.nodes
        # get the links of the group
        links = group.links

        # get the textues from the list
        textures = os.listdir(udimPath)
        #print(textures)

        # get the udims in reverse orde
        udims = []
        for texture in textures:
            udim = texture.split(".")[-2]
            udims.append(udim)
        udims.sort(reverse=True)

        # get sorted textures:
        sortedTextures = []
        for udim in udims:
            for texture in textures:
                if udim in texture:
                    sortedTextures.append(texture)
        # print (sortedTextures)


        # create a texture coordinate node and later connect all the mapping nodes to this node
        texCordNode = nodes.new("ShaderNodeTexCoord")
        texCordNode.location.y = ( 100 )
        texCordNode.location.x = -( 100 )
        texCordNode.select = False 

        prevTexCheckerNode = None

        for index, texture in enumerate(sortedTextures):  

            # how to we define this one...? 
            udim = texture.split('.')[-2]
            # frame the nodes
            frame = nodes.new(type='NodeFrame')
            frame.label = udim
            frame.select = False
            # nodesCreated.append(frame)            

            #### create checker node ###
            # create a checker map
            # bpy.ops.node.add_node(type="ShaderNodeTexChecker", use_transform=True)
            texCheckerNode = nodes.new('ShaderNodeTexChecker')
            texCheckerNode.name = texture+ "_texCheckNode"
            texCheckerNode.inputs[3].default_value = 1

            #texCheckerNode.location.y = -( 400 * index )
            texCheckerNode.location.x = 800
            texCheckerNode.parent = frame

            # nodesCreated.append(texCheckerNode)

            #### link the checker node to prevous checker node if it already exists ####
            if prevTexCheckerNode:
                output_socket = texCheckerNode.outputs[0]
                links.new(output_socket, prevTexCheckerNode)
            else:
                firstNode = True
                if index == 0:
                    firstNodeOut = texCheckerNode.outputs[0]

            #### create texture node and set the image ####
            texImgNode = nodes.new('ShaderNodeTexImage')
            texImgNode.name =  "_".join(texture.split(".")[:-4] )

            #texImgNode.location.y = -( 400 * index )
            texImgNode.location.x = ( 400  )

            texImgNode.parent = frame

            # nodesCreated.append(texImgNode)

            print(texImgNode.dimensions[0])
            for i in dir(texImgNode):
                if "dimensions" in i.lower():
                    print (i)

            # set the image
            #bpy.ops.image.open(filepath="//bpy", directory="/home/salaati/Downloads/", files=[{"name":"rhAbnormalTitanC.diffuse.1002.tif", "name":"rhAbnormalTitanC.diffuse.1002.tif"}], relative_path=True)
            texPath = os.path.join(udimPath, texture)
            tex = bpy.data.images.get(texPath)
            if not tex:
               tex = load_image(texPath)
            # set and enable the texture
            texImgNode.image = tex
            texImgNode.show_texture = True

            #### link checker map and the texture ####
            # get the output socket
            if firstNode:
                output_socket = texImgNode.outputs[0]
                # get the input socket 
                input_socket = texCheckerNode.inputs[1]
                # create the link between the output and the input
                links.new(output_socket, input_socket)
                prevTexCheckerNode = texCheckerNode.inputs[2]
                firstNode = False
            else:
                output_socket = texImgNode.outputs[0]
                # get the input socket 
                input_socket = texCheckerNode.inputs[2]
                # create the link between the output and the input
                links.new(output_socket, input_socket)
                prevTexCheckerNode = texCheckerNode.inputs[1]   
                firstNode = True

            #### create a mapping node and set the values ####
            #bpy.ops.node.add_node(type="ShaderNodeMapping", use_transform=True)
            mappingNode = nodes.new('ShaderNodeMapping')
            # change the type to vector
            # mappingNode.vector_type = "VECTOR"
            mappingNode.vector_type = "POINT"
            mappingNode.use_min = True
            mappingNode.use_max = True

            # nodesCreated.append(mappingNode)
            #mappingNode.location.y = -( 400 )
            #mappingNode.location.x = -( 800  )
             
            mappingNode.parent = frame

            if udim[-1] == "0":
                xMax = 10
                yMin = 0
            else:
                xMax = int(udim[-1])
                yMin = int( udim[-2] )

            xMin = int(xMax) - 1
            yMax = int(yMin) + 1
                
            # set min x
            mappingNode.min[0] = int( xMin )
            # set max x 
            mappingNode.max[0] = int( xMax )
            # set min y
            mappingNode.min[1] = int( yMin )
            # set max y
            mappingNode.max[1] = int( yMax )

            #### link the mapping node and the checker node ####
            output_socket = mappingNode.outputs[0]
            input_socket = texCheckerNode.inputs[0]
            links.new(output_socket, input_socket) 

            #### link the mappingNOde to texCordNode ####
            output_socket = texCordNode.outputs[2] 
            input_socket = mappingNode.inputs[0]
            links.new(output_socket, input_socket)
             
            # save the checkerNode second color parameter for the next loop
            # prevTexCheckerNode = texCheckerNode.inputs[2]
            #frame.location.x = 0
            #frame.location.y = 0

            if udim[-1] == "0":
                frame.location.x = ( int( 9 ) * 1100 )
                frame.location.y = ( int( udim[-2] ) ) * 600
            else:
                frame.location.x = ( int( udim[-1] ) -1 ) * 1100
                frame.location.y = ( int( udim[-2] ) +1 ) * 600
        
        # for node in nodesCreated:
            # if node.select == False:
            #     node.select = True

        # bpy.ops.node.group_make()

        # nodes = bpy.context.space_data.node_tree.nodes
        # links = bpy.context.space_data.node_tree.links
        # print (nodes)
        # tree = active.node_tree
        # nodes = tree.nodes
        # links = tree.links
        #nodeGrp.active_output = 0
        # for node in nodes:
            # print ( dir(node) )
            # print (node.type)
            # if node.type == "GROUP":
            #     groupNodes = node.node_tree.nodes
            #     for groupNode in groupNodes:
            #         print ( node.type )
            #         if groupNode.type == "GROUP_OUTPUT":
            #             groupOutput = groupNode
        # print ( dir( groupOutput.inputs ) )
        output_node = group.nodes.new("NodeGroupOutput")
        # get proper location on this guy
        output_node.location.x = ( int( sortedTextures[0].split(".")[-2][-1] ) + 1 ) * 1000
        output_node.location.y = ( int( sortedTextures[0].split(".")[-2][-2] ) + 2 ) * 400
        group.outputs.new('NodeSocketColor', 'color')
        # output_node.location = (600, 0)
        # print (( groupOutput.inputs[1]) )
        # print (firstNodeOut)
        links.new(firstNodeOut, output_node.inputs["color"])
        #if groupOutput:
        #links.new(firstNodeOut, )
        bpy.ops.node.group_edit(exit=False)

#################################

        return {'FINISHED'}

def register():
    bpy.utils.register_class(UdimNodeCreator)
    bpy.utils.register_class(UIPanel)
   
def unregister():
    bpy.utils.unregister_class(UdimNodeCreator)
    bpy.utils.unregister_class(UIPanel)

if __name__ == "__main__":
    register()

