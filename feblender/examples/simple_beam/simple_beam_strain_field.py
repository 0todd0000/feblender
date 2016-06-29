
import os
import feblender


#(0) Import geometry and strain field:
### import geometry from FEB file:
dir0           = os.path.split(__file__)[0]
fnameFEB       = os.path.join(dir0, 'simple_beam.feb')
nodes,elements = feblender.febio.load_geometry(fnameFEB)
### import strain field from LOG file:
fnameLOG       = os.path.join(dir0, 'simple_beam.log')
Y              = feblender.febio.load_log(fnameLOG)
y              = feblender.tensor.strain_tensor_field_to_effective_strain_field(Y)



#(1) Plot the strain field:
# feblender.plot_field(nodes, elements, y, smin=8.0e-4, smax=8.3e-4, cmapname='jet')
feblender.plot_field(nodes, elements, y, smin=y.min(), smax=y.max(), cmapname='jet')



# #(2) Render to file (optional):
# fnamePNG       = os.path.join(dir0, 'simple_beam_strain_field.png')
# feblender.render(fnamePNG)
# feblender.quit()  #optionally quit Blender


