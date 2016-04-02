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
import random
from bpy.props import StringProperty

bpy.types.Scene.udimPath = StringProperty(
								name = "Map Path",
								description = "Provide the path to the maps.")

# bpy.types.Scene.udimGroupName = StringProperty(
# 								name = "Group Name",
# 								description = "Provide the name of the group.")

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
		# layout.prop(scn, 'udimGroupName')
		layout.operator("node.create_udim_node")

class UdimNodeCreator(bpy.types.Operator):
	""" Displays wire frame on shaded with draw all edges on all objects"""
	bl_idname = "node.create_udim_node"
	bl_label = "create UDIM node"
	bl_description = "Create udim node network from the given path"
	bl_options = {'REGISTER', 'UNDO'}


	@classmethod
	def poll(cls, context):
		space = context.space_data
		valid = False
		if space.type == 'NODE_EDITOR':
			if space.node_tree is not None:
				valid = True
		return valid

	def execute(self, context):


		udimPath = bpy.context.scene["udimPath"]
		activeMaterial = bpy.context.object.active_material


		# if use nodes not enabled ? enable it
		if activeMaterial.use_nodes == False:
			activeMaterial.use_nodes = True
		
		assetId = os.path.basename(udimPath)
		# create new group
		group = bpy.data.node_groups.new(type="ShaderNodeTree", name=assetId)
		# get the nodes of the group
		nodes = group.nodes
		# get the links of the group
		links = group.links

		oldChannelFrameWidth = 0

		textures = []
		for rootPath, folders, files in os.walk(udimPath):
			print  ("test", rootPath, folders, files)
			for f in files:
				channel = f.split(".")[1] 
				maxUdim = max([ 1001, int( f.split(".")[-2] ) ])

				textures.append( os.path.join(rootPath, f) )
				# print ( textures )

			try:
				# print ( channel, maxUdim )

				prevTexCheckerInput = None
				swapNodes = True

				channelFrame = nodes.new(type="NodeFrame")
				channelFrame.label = channel
				channelFrame.label_size = 64
				channelFrame.name = channel
				channelFrame.select = False
				# print( random.random() )
				channelFrame.use_custom_color = True
				channelFrame.color = (random.random(), random.random(), random.random())

				# create a texture coordinate node and later connect all the mapping nodes to this node
				texCordNode = nodes.new("ShaderNodeTexCoord")
				texCordNode.label = channel+"TexCoord"
				texCordNode.location.y = ( 100 )
				texCordNode.location.x = -( 100 )
				texCordNode.select = False 

				texCordNode.parent = channelFrame
				print ( maxUdim )

				for udim in reversed(range(1001, maxUdim + 1)):
					print (udim)
					udim = str(udim)
					# frame the nodes
					frame = nodes.new(type='NodeFrame')
					frame.name = udim
					frame.label = udim
					frame.select = False
					frame.label_size = 32
					frame.parent = channelFrame

					# create checker node
					texCheckerNode = nodes.new('ShaderNodeTexChecker')
					texCheckerNode.label = udim + "_texChecker"
					texCheckerNode.inputs[3].default_value = 1

					texCheckerNode.location.x = 800
					texCheckerNode.parent = frame

					# print ( "test", udim, maxUdim)
					if int(udim) == maxUdim:
						output_node = nodes.new("NodeGroupOutput")
						# output_node.location.x = ( int( sortedTextures[0].split(".")[-2][-1] ) + 1 ) * 1000
						# output_node.location.y = ( int( sortedTextures[0].split(".")[-2][-2] ) + 2 ) * 400
						group.outputs.new('NodeSocketColor', channel)
						links.new(texCheckerNode.outputs[0], output_node.inputs[channel])
						output_node.parent = channelFrame

					# link the checker node to prevous checker node if it already exists 
					if prevTexCheckerInput:
						links.new(texCheckerNode.outputs[0], prevTexCheckerInput)
					else:
						swapNodes = False

					# create texture node and set the texture
					texImgNode = nodes.new('ShaderNodeTexImage')
					texImgNode.label = udim + "_texImage"
					# texImgNode.name =  "_".join(texture.split(".")[:-4] )

					#texImgNode.location.y = -( 400 * index )
					texImgNode.location.x = ( 400  )
					# texImgNode.hide = True
					texImgNode.parent = frame

					#try:
					texxs = [texx for texx in textures if udim in texx]
					print ( texxs )

					if texxs:
						texture = texxs[0]
						print ( texture )
						tex = bpy.data.images.get(texture)
						if not tex:
						   tex = load_image(texture)

						# set and enable the texture
						texImgNode.image = tex
						# is it needed... ?
						texImgNode.show_texture = True
						texImgNode.name =  os.path.basename(texture)
					# except IndexError:
					# 	pass

					#### link checker map and the texture ####
					if swapNodes:
						links.new(texImgNode.outputs[0], texCheckerNode.inputs[2])
						prevTexCheckerInput = texCheckerNode.inputs[1]   
						swapNodes = False
					else:
						links.new(texImgNode.outputs[0], texCheckerNode.inputs[1])
						# need a better name for this guy... 
						prevTexCheckerInput = texCheckerNode.inputs[2]
						swapNodes = True

					#### create a mapping node and set the values ####
					mappingNode = nodes.new('ShaderNodeMapping')
					mappingNode.vector_type = "POINT"
					mappingNode.use_min = True
					mappingNode.use_max = True
					
					# mappingNode.hide = True				
					mappingNode.parent = frame

					# better algo over here..? 
					# can make it more crypitc by reducing the lines... :P
					if udim [-1] == "0":
						xMax = 10
						yMin = 0
					else:
						xMax = int( udim[-1] )
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

			except UnboundLocalError:
				pass

		return {'FINISHED'}

def register():
	bpy.utils.register_class(UdimNodeCreator)
	bpy.utils.register_class(UIPanel)
   
def unregister():
	bpy.utils.unregister_class(UdimNodeCreator)
	bpy.utils.unregister_class(UIPanel)

if __name__ == "__main__":
	register()

