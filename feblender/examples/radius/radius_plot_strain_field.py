
import os
import feblender


#(0) Import geometry:
dir0           = os.path.split(__file__)[0]
fnameFEB       = os.path.join(dir0, 'radius.feb.gz')
print( 'Loading geometry from FEB file...')
nodes,elements = feblender.febio.load_geometry(fnameFEB)
print( 'Loading strain field from LOG file...')
fnameLOG       = os.path.join(dir0, 'radius.log.gz')
Y              = feblender.febio.load_log(fnameLOG)
print( 'Computing effective strain...')
y              = feblender.tensor.strain_tensor_field_to_effective_strain_field(Y)



#(1) Plot the geometry:
print( 'Plotting strain field...')
feblender.plot_field(nodes, elements, y, smin=y.min(), smax=y.max(), cmapname='jet')


#(2) Render to file (optional):
print( 'Rendering to file...')
fnamePNG  = os.path.join(dir0, 'radius_strain_field.png')
feblender.render(fnamePNG)
feblender.quit()  #optionally quit Blender



print( 'Done.')