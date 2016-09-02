
import bpy


def init_scene(delete_lamp=False):
	scene    = bpy.data.scenes[0]
	if 'Cube' in scene.objects.keys():
		scene.objects.unlink( scene.objects['Cube'] )
	if delete_lamp:
		scene.objects.unlink( scene.objects['Lamp'] )
	return scene
	


def render(fname):
	scene = bpy.data.scenes[0]
	scene.render.filepath = fname
	bpy.ops.render.render(write_still=True)


def set_view2selected():
	for area in bpy.context.screen.areas:
		if area.type == 'VIEW_3D':
			### set view to selected:
			ctx           = bpy.context.copy()
			ctx['area']   = area
			ctx['region'] = area.regions[-1]
			bpy.ops.view3d.view_selected(ctx)
			bpy.ops.view3d.camera_to_view_selected(ctx)
			### set camera view:
			for space in area.spaces:
				space.region_3d.view_perspective = 'CAMERA'


def quit():
	bpy.ops.wm.quit_blender()