
import os
import feblender


#(0) Import geometry:
dir0           = os.path.split(__file__)[0]
fnameFEB       = os.path.join(dir0, 'simple_beam.feb')
nodes,elements = feblender.febio.load_geometry(fnameFEB)


#(1) Plot the geometry:
feblender.plot_geometry(nodes, elements, color=(1,0,0))


# #(2) Render to file (optional):
# fnamePNG       = os.path.join(dir0, 'simple_beam_geom.png')
# feblender.render(fnamePNG)
# feblender.quit()  #optionally quit Blender