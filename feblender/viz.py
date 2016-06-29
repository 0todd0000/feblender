


import bpy,os
from math import pi,radians
import numpy as np






class Visualization(object):
	def __init__(self, delete_lamp=False):
		self.scene    = bpy.data.scenes[0]
		self.camera   = self.scene.objects['Camera']
		self.colorbar = None
		self.model    = None
		self.sun      = None
	# 	self._init_scene(delete_lamp=delete_lamp)
	#
	# def _init_scene(self, delete_lamp=False):
	# 	self.scene.objects.unlink( self.scene.objects['Cube' ] )
	# 	if delete_lamp:
	# 		self.scene.objects.unlink( self.scene.objects['Lamp' ] )

	
	def _create_scene_composite(self):
		self.scene.use_nodes  = True
		### change to compositing screen:
		screen_compositing = bpy.data.screens['Compositing']
		bpy.context.window.screen = screen_compositing
		### create node tree:
		tree = self.scene.node_tree
		[tree.links.remove(link) for link in tree.links]
		node_composite = tree.nodes[0]
		node_render_overlay = tree.nodes[1]
		### new overlay node:
		node_render_main = tree.nodes.new('CompositorNodeRLayers')
		node_render_main.scene = self.scene
		### new mix node:
		node_mix = tree.nodes.new('CompositorNodeMixRGB')
		node_mix.inputs[0].default_value = 1.0
		node_mix.use_alpha = True
		### new blur node:
		node_blur = tree.nodes.new('CompositorNodeBlur')
		node_blur.size_x = 0
		node_blur.size_y = 0
		### layout nodes on screen:
		node_render_main.location     = 0,400
		node_render_overlay.location  = 0,0
		node_blur.location            = 200,400
		node_mix.location = 400,400
		node_composite.location = 600,400
		### create links amongst nodes:
		### connect main image (background) to the blur node:
		tree.links.new(node_render_main.outputs['Image'],  node_blur.inputs['Image'])
		### connect images to color mixer:
		tree.links.new(node_blur.outputs[0],  node_mix.inputs[1])
		tree.links.new(node_render_overlay.outputs[0],  node_mix.inputs[2])
		### connect mixer output to the compositor:
		tree.links.new(node_mix.outputs[0],  node_composite.inputs[0])


		
	
	def add_colorbar(self, xy=(0.05,0.2), w=0.01, h=0.6, label='', label_offset=0.15, label_size=0.15, label_side='left', nTicks=5, ticks_color=(1,1,1), ticks_side='left', asint=False, model=None):
		if model is None:
			CMAP     = np.array([(0,0,1)]*64)
			smin     = 0
			smax     = 10
		else:
			CMAP     = model.CMAP
			smin     = model.smin
			smax     = model.smax
		self.colorbar   = Colorbar(CMAP, xy=xy, w=w, h=h)
		self.colorbar.add_ticks(smin, smax, nTicks=nTicks, color=ticks_color, side=ticks_side, asint=asint)
		self.colorbar.add_label(label, side=label_side, offset=label_offset, size=label_size, color=ticks_color)
		self._create_scene_composite()


		
	
	# def add_model(self, model, specular=0.2, alpha=1.0):
	# 	self.model    = model
	# 	for mesh in model.meshes:
	# 		mesh.add_to_scene(self.scene, specular=specular, alpha=alpha)
	
	def add_mesh(self, mesh):
		mesh.add_to_scene(self.scene)

	def add_meshes(self, *meshes):
		for m in meshes:
			m.add_to_scene(self.scene)



	def add_lamp(self, type='POINT', radius=1, location=(2,0,3), rotation=(0,0,0), shadow=True):
		rotation = [radians(a) for a in rotation]
		bpy.ops.object.lamp_add(type=type, radius=radius, location=tuple(location), rotation=tuple(rotation))
		lamp    = bpy.data.objects[-1]
		lamp.data.use_shadow = shadow


	def add_sun(self, radius=1, location=(2,0,3), rotation=(0,0,0), shadow=True, shadow_color=(0,0,0)):
		rotation = [radians(a) for a in rotation]
		bpy.ops.object.lamp_add(type='SUN', radius=1, location=tuple(location), rotation=tuple(rotation))
		self.sun    = bpy.data.objects['Sun']
		self.sun.data.use_shadow = shadow
		self.sun.data.shadow_color = shadow_color
	
	def set_camera_position(self, location=(0,0,0), rotation=(0,0,0)):
		self.camera.location       = location
		self.camera.rotation_euler = np.radians(rotation)

	def set_horizon_color(self, color):
		self.scene.world.horizon_color = color
	
	def quit_blender(self):
		bpy.ops.wm.quit_blender()

	def render(self, filename):
		self.scene.render.filepath = str(filename)
		bpy.ops.render.render(write_still=True)














class Colorbar(object):
	def __init__(self, CMAP, xy=(0.5,0.5), w=0.1, h=1, d=0.05, ztop=0, scene=0):
		self.CMAP     = np.asarray(CMAP, dtype=float)
		self.scene    = None
		self.camera   = None
		self.xy       = np.asarray(xy, dtype=float)
		self.w        = float(w)
		self.h        = float(h)
		self.d        = float(d)
		self.ztop     = float(ztop)
		self._init_scene()
		self._generate_mesh()
		

	def _init_scene(self):
		### create an overlay scene:
		bpy.ops.scene.new()
		self.scene                          = bpy.data.scenes[-1]
		self.scene.name                     = 'Overlay'
		self.scene.render.layers[0].use_sky = False
		### add camera
		bpy.ops.object.camera_add()
		self.camera                = self.scene.objects[0]
		self.camera.name           = 'Camera.Overlay'
		self.camera.data.type      = 'ORTHO'
		self.camera.location       = 0, 0, 1
		self.camera.rotation_euler = 0, 0, 0
		self.scene.camera          = self.camera  ### SET THE SCENE's CAMERA !!!!!!!!!!!!!
		### add lamp:
		(x,y),w,h = self.get_global_coords(self.xy, self.w, self.h)
		bpy.ops.object.lamp_add(type='SUN', radius=1, location=(x+0.5*w, y+0.5*h, 5))
		point     = bpy.data.objects[-1]
		point.data.use_specular = False
		point.data.energy = 1.0
		# point.data.distance = 10000
		
		
	def _generate_mesh(self):
		(x,y),w,h = self.get_global_coords(self.xy, self.w, self.h)
		d         = self.d
		nColors   = self.CMAP.shape[0]
		hblock    = h / nColors
		ypos      = np.linspace(y, y+h, nColors+1)[:-1]
		unit_cube = np.array([(0,0,-1), (1,0,-1), (1,1,-1), (0,1,-1),   (0,0,0), (1,0,0), (1,1,0), (0,1,0)])
		edges     = [(0,1), (1,2), (2,3), (3,0),    (4,5), (5,6), (6,7), (7,4),   (0,4),(1,5),(2,6),(3,7)]
		faces     = [(0,1,2,3), (4,5,6,7), (0,1,5,4),  (3,2,6,7),  (0,3,7,4),  (1,2,6,5) ]
		for y,color in zip(ypos, self.CMAP):
			vertices       = (x,y,0) + unit_cube  * (w,hblock,d)
			vertices[:,2] += self.ztop
			### create mesh
			mesh      = bpy.data.meshes.new('ColorbarBlock')
			mesh.from_pydata(vertices, edges, faces)
			# mesh.update(calc_edges=True)
			obj       = bpy.data.objects.new('ColorbarBlock', mesh)
			self.scene.objects.link(obj)
			### create material:
			mat                          = bpy.data.materials.new('Colorbar-Material')
			mat.diffuse_color            = color
			mat.specular_intensity       = 0.3
			mat.use_transparency         = False
			mat.alpha                    = 1.0
			obj.data.materials.append(mat)
			
			
	def add_label(self, s, color=(1,1,1), side='right', size=0.1, offset=0.1):
		(x,y),w,h = self.get_global_coords(self.xy, self.w, self.h)
		if side=='right':
			x  = x + w + 0.01 + offset
			align = 'CENTER'
		else:
			x  = x - 0.01 - offset
			align = 'CENTER'
		y      = y + 0.5*h
		### create material:
		mat                          = bpy.data.materials.new('Colorbar-Text-Material')
		mat.diffuse_color            = color
		mat.specular_intensity       = 1.0
		mat.use_transparency         = False
		mat.alpha                    = 1.0
		### create text objects:
		bpy.ops.object.text_add(location=(x,y,0))
		obj            = bpy.context.object
		obj.rotation_euler = (0, 0, pi/2)
		obj.data.body  = str(s)
		obj.data.size  = size
		obj.data.align = align
		obj.data.materials.append(mat)
	
	def add_ticks(self, xmin, xmax, nTicks=3, color=(1,1,1), side='right', size=0.1, asint=False):
		(x,y),w,h = self.get_global_coords(self.xy, self.w, self.h)
		if side=='right':
			x  = x + w + 0.01
			align = 'LEFT'
		else:
			x  = x - 0.01
			align = 'RIGHT'
		yy = np.linspace(y, y+h, nTicks) - 0.5*size
		qq = np.linspace(xmin, xmax, nTicks)
		### create material:
		mat                          = bpy.data.materials.new('Colorbar-Text-Material')
		mat.diffuse_color            = color
		mat.specular_intensity       = 1.0
		mat.use_transparency         = False
		mat.alpha                    = 1.0
		### create text objects:
		for y,q in zip(yy,qq):
			bpy.ops.object.text_add(location=(x,y,0))
			obj            = bpy.context.object
			obj.data.body  = str(int(q)) if asint else str(q)
			obj.data.size  = 0.1
			obj.data.align = align
			obj.data.materials.append(mat)


	
	def get_global_coords(self, xy, w, h):
		# xspan  = 3.65 * 2
		# yspan  = 2.05 * 2
		xspan  = 3.0 * 2
		yspan  = 1.68 * 2
		x,y    = (xy[0] - 0.5)*xspan, (xy[1] - 0.5)*yspan
		w,h    = w*xspan, h*yspan
		return (x,y), w, h
		
		






