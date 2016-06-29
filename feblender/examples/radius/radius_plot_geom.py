
import os
import feblender


#(0) Import geometry:
dir0           = os.path.split(__file__)[0]
fnameFEB       = os.path.join(dir0, 'radius.feb.gz')
print( 'Loading geometry from FEB file...')
nodes,elements = feblender.febio.load_geometry(fnameFEB)


#(1) Plot the geometry:
print( 'Plotting geometry...')
feblender.plot_geometry(nodes, elements, color=(1,1,1))


# #(2) Render to file (optional):
# print( 'Rendering to file...')
# fnamePNG  = os.path.join(dir0, 'radius_geom.png')
# feblender.render(fnamePNG)
# feblender.quit()  #optionally quit Blender



print( 'Done.')