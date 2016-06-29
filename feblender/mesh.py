

import bpy
import os
from math import pi,radians
import numpy as np


PATH2CMAPS = os.path.join( os.path.split(__file__)[0] , 'cmaps')



class MeshSingleColor(object):
	def __init__(self, XYZ, CONN, color=(1,1,1), specular=0.2, alpha=1.0):
		self.XYZ      = XYZ
		self.CONN     = CONN
		# self.mesh     = None
		self.color    = color
		self.specular = float(specular)
		self.alpha    = float(alpha)
		self.nverts   = 0
		self._generate_mesh()


	def _get_verts_edges_faces(self, conn):
		verts          = self.XYZ[conn].tolist()
		n              = len(conn)
		if n==3:    #triangle
			edges0     = np.array([(0,1), (1,2), (2,0)])
			faces0     = np.array([(0,1,2)])
		elif n==4:  #tetrahedron
			edges0     = np.array([(0,1), (1,2), (2,0),   (1,3), (3,0), (2,3), (3,0)])
			faces0     = np.array([(0,1,2), (0,1,3), (0,2,3),  (1,2,3)])
		elif n==8:  #hexahedron
			edges0     = np.array([(0,1),(1,2),(2,3),(3,0),  (4,5),(5,6),(6,7),(7,4),  (0,4),(1,5),(2,6),(3,7)])
			faces0     = np.array([(0,1,2,3), (4,5,6,7),   (0,1,5,4), (3,2,6,7),   (0,3,7,4), (1,2,6,5)])
		else:
			raise( ValueError('Unknown element type.  Must be 3-, 4- or 8-connected.')  )
		###
		edges          = (edges0 + self.nverts).tolist()
		faces          = (faces0 + self.nverts).tolist()
		self.nverts   += n
		return verts,edges,faces
	
	def _generate_mesh(self):
		VERTS,EDGES,FACES = [],[],[]
		for conn in self.CONN:
			v,e,f  = self._get_verts_edges_faces(conn)
			VERTS += v
			EDGES += e
			FACES += f
		self.VERTS = VERTS
		self.EDGES = EDGES
		self.FACES = FACES


	def add_to_scene(self, scene):
		### create mesh
		mesh      = bpy.data.meshes.new('MeshSingleColor')
		mesh.from_pydata(self.VERTS, self.EDGES, self.FACES)
		obj       = bpy.data.objects.new('MeshSingleColor', mesh)
		scene.objects.link(obj)
		### create material:
		mat                          = bpy.data.materials.new('MeshGroup-Material')
		mat.diffuse_color            = self.color
		mat.specular_intensity       = self.specular
		mat.use_transparency         = True
		mat.alpha                    = self.alpha
		obj.data.materials.append(mat)
		obj.select                   = True



class MeshColorMapped(object):
	def __init__(self, XYZ, CONN, S, smin=None, smax=None, cmapname='jet', specular=0.5, alpha=1):
		self.XYZ      = XYZ
		self.CONN     = CONN
		self.S        = S
		self.CMAP     = None
		self.CID      = None
		self.nColors  = 64
		self.smin     = S.min() if smin is None else smin
		self.smax     = S.max() if smax is None else smax
		self.meshes   = None
		self.specular = float(specular)
		self.alpha    = float(alpha)
		self._set_colormap(cmapname)
		self._set_element_data()
		self._generate_meshes()


	def _generate_meshes(self):
		self.meshes   = []
		for u,color in zip(self.uPART, self.colors):
			conn      = self.CONN[ self.PART==u ]
			mesh      = MeshSingleColor(self.XYZ, conn, color=color, specular=self.specular, alpha=self.alpha)
			self.meshes.append(mesh)

	def _set_colormap(self, cmap='jet'):
		if cmap is None:
			self.CMAP   = np.array([(0,0,1)]*64)
		else:
			fname       = os.path.join(PATH2CMAPS, '%s.npy' %str(cmap))
			self.CMAP   = np.load(fname)

	def _set_element_data(self):
		S,smin,smax   = self.S, self.smin, self.smax
		nColors       = self.nColors
		CID           = np.array([0]*S.size)
		s_upper       = np.linspace(smin, smax, nColors+1)
		for i,x in enumerate(s_upper):
			CID[S>=x] = i
		CID[S<=smin]  = 0
		CID[S>=smax]  = nColors-1
		self.CID      = CID
		
	def _generate_meshes(self):
		self.meshes   = []
		for i,c in enumerate(self.CMAP):
			conn      = self.CONN[ self.CID==i ]
			mesh      = MeshSingleColor(self.XYZ, conn, color=c)
			self.meshes.append(mesh)
	

	def add_to_scene(self, scene):
		for mesh in self.meshes:
			mesh.add_to_scene(scene)








class MultiPartMeshSingleColors(object):
	def __init__(self, XYZ, CONN, PART, colors):
		self.XYZ      = XYZ
		self.CONN     = CONN
		self.PART     = PART
		self.uPART    = np.unique(PART)
		self.colors   = colors
		self.meshes   = None
		self._generate_meshes()

	def _generate_meshes(self):
		self.meshes   = []
		for u,color in zip(self.uPART, self.colors):
			conn      = self.CONN[ self.PART==u ]
			mesh      = MeshSingleColor(self.XYZ, conn, color=color)
			self.meshes.append(mesh)


	def add_to_scene(self, scene):
		for mesh in self.meshes:
			mesh.add_to_scene(scene)





