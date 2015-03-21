# ability to refresh nodes
# ability to pick the channel naming convention
# get the frames name right
# get the node names and labels right. Why both names and labesl..? How to use it right..?
# have to give both name and labes.
# labes for representation on the screen. can give it more visually.
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
        # sub folders check ? 
        # group check ?
        # format... ?
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
        udimGroupName = bpy.context.scene['udimGroupName']
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
        group = bpy.data.node_groups.new(type="ShaderNodeTree", name=udimGroupName)
        # get the nodes of the group
        nodes = group.nodes
        # get the links of the group
        links = group.links

        # get the textues from the list
        textures = os.listdir(udimPath)
        # textures = []
		# for rootPath, folders, files in os.walk(udimPath):
		# 	for file in files:
		# 		textures.append( os.path.join(rootPath, file) )
		
		print(textures)

        #if not texture:
        	# print a message saying no textures found.

        # need to find out the formats in which the regular mari / mudbox stuff is written out.
        # based on that need to change the way in which we can organize it in the revers order

        # may be take the input from the user regarding the naming conventions ???

        # get the udims in reverse orde
        udims = []
        for texture in textures:
            udim = texture.split(".")[-2]
            # check if its an udim using re
            # if not exclude it.
            udims.append(udim)
        udims.sort(reverse=True)

        # get sorted textures based on the udim.
        sortedTextures = []
        for udim in udims:
            for texture in textures:
                if udim in texture:
                    sortedTextures.append(texture)
        # print (sortedTextures)

        # create a texture coordinate node and later connect all the mapping nodes to this node
        texCordNode = nodes.new("ShaderNodeTexCoord")
        texCordNode.label = udimGroupName+"TexCoord"
        texCordNode.location.y = ( 100 )
        texCordNode.location.x = -( 100 )
        texCordNode.select = False 

        prevTexCheckerInput = None

        for index, texture in enumerate(sortedTextures):  

            # how to we define this one...? 
            udim = texture.split('.')[-2]
            # frame the nodes
            frame = nodes.new(type='NodeFrame')
            frame.label = udim
            frame.select = False

            # create checker node
            texCheckerNode = nodes.new('ShaderNodeTexChecker')
            texCheckerNode.label = udim + "_texChecker"
            texCheckerNode.inputs[3].default_value = 1

            texCheckerNode.location.x = 800
            texCheckerNode.parent = frame

            # may be finish it off and connect it to the ouput nodes directly over here...? 
            # create the asset directly
            # connect the first guy directly to output.
            if index == 0:
                output_node = group.nodes.new("NodeGroupOutput")
                # get proper location on this guy
                output_node.location.x = ( int( sortedTextures[0].split(".")[-2][-1] ) + 1 ) * 1000
                output_node.location.y = ( int( sortedTextures[0].split(".")[-2][-2] ) + 2 ) * 400
                group.outputs.new('NodeSocketColor', 'color')
                links.new(texCheckerNode.outputs[0], output_node.inputs["color"])

            # link the checker node to prevous checker node if it already exists 
            if prevTexCheckerInput:
                links.new(texCheckerNode.outputs[0], prevTexCheckerInput)
            else:
                swapNodes = False
            # get the texture
            # do some better optimizations in terms of what if the textures are already there in the file.
            # right now its loading directly into it.
            texPath = os.path.join(udimPath, texture)
            tex = bpy.data.images.get(texPath)
            if not tex:
               tex = load_image(texPath)

            # create texture node and set the texture
            texImgNode = nodes.new('ShaderNodeTexImage')
            texImgNode.label = udim + "_texImage"
            texImgNode.name =  "_".join(texture.split(".")[:-4] )

            #texImgNode.location.y = -( 400 * index )
            texImgNode.location.x = ( 400  )
            texImgNode.parent = frame

            # set and enable the texture
            texImgNode.image = tex
            # is it needed... ?
            texImgNode.show_texture = True


            #### link checker map and the texture ####
            if swapNodes:
                links.new(texImgNode.outputs[0], texCheckerNode.inputs[2])
                prevTexCheckerInput = texCheckerNode.inputs[1]   
                swapNodes = True
            else:
                links.new(texImgNode.outputs[0], texCheckerNode.inputs[1])
                # need a better name for this guy... 
                prevTexCheckerInput = texCheckerNode.inputs[2]
                swapNodes = False

            #### create a mapping node and set the values ####
            mappingNode = nodes.new('ShaderNodeMapping')
            mappingNode.vector_type = "POINT"
            mappingNode.use_min = True
            mappingNode.use_max = True
            
            mappingNode.parent = frame

            # better algo over here..? 
            # can make it more crypitc by reducing the lines... :P
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

            # link the mapping node and the checker node
            links.new(mappingNode.outputs[0], texCheckerNode.inputs[0])
            # link the mappingNode to texCordNode 
            links.new(texCordNode.outputs[2], mappingNode.inputs[0])

            # define the location of the frame
            if udim[-1] == "0":
                frame.location.x = ( int( 9 ) * 1100 )
                frame.location.y = ( int( udim[-2] ) ) * 600
            else:
                frame.location.x = ( int( udim[-1] ) -1 ) * 1100
                frame.location.y = ( int( udim[-2] ) +1 ) * 600
        
        bpy.ops.node.group_edit(exit=False)

        return {'FINISHED'}

def register():
    bpy.utils.register_class(UdimNodeCreator)
    bpy.utils.register_class(UIPanel)
   
def unregister():
    bpy.utils.unregister_class(UdimNodeCreator)
    bpy.utils.unregister_class(UIPanel)

if __name__ == "__main__":
    register()

