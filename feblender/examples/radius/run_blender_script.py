
import os
from blenderSR import BlenderScriptRunner

dir0        = os.path.split(__file__)[0]
path2script = os.path.join(dir0, 'radius_plot_geom.py')
# path2script = os.path.join(dir0, 'radius_plot_strain_field.py')
bsr         = BlenderScriptRunner()
bsr.run(path2script)






