

__version__  = '0.0.1'   #(2016.06.28) 


_USE_BPY     = True
try:
	import bpy
except ImportError:
	_USE_BPY = False


if _USE_BPY:
	from .commands import init_scene, quit, render, set_view2selected
	from .highlevel import plot_field, plot_geometry
	from .io import febio
	from . import mesh
	from . import tensor
	from .viz import Visualization
else:
	from .io import febio
	from . import tensor



if not _USE_BPY:
	def _disabled(*args, **kwdargs):
		raise(  UserWarning('This functionality is disabled outside of Blender.  The script must be run inside Blender.')  )
	init_scene        = _disabled
	quit              = _disabled
	render            = _disabled
	set_view2selected = _disabled
	plot_field        = _disabled
	plot_geometry     = _disabled
	


