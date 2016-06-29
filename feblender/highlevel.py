

from . import commands, mesh, viz


def plot_geometry(nodes, elements, color=(1,1,1)):
	commands.init_scene()
	m    = mesh.MeshSingleColor(nodes, elements, color=color)
	v    = viz.Visualization()
	v.add_mesh(m)
	commands.set_view2selected()


def plot_field(nodes, elements, S, smin=None, smax=None, cmapname='jet'):
	commands.init_scene()
	m    = mesh.MeshColorMapped(nodes, elements, S, smin=smin, smax=smax, cmapname=cmapname, specular=0.5, alpha=1)
	v    = viz.Visualization()
	v.add_mesh(m)
	commands.set_view2selected()
