import operator

import OCC.Core.BRepGProp
import OCC.Core.GProp
import ifcopenshell
import ifcopenshell, ifcopenshell.geom
import ifcopenshell.geom
import numpy
from OCC.Display.SimpleGui import init_display

fn = "Duplex_A_20110907_optimized.ifc"
f = ifcopenshell.open(fn)
s = ifcopenshell.geom.settings()
s.set(s.USE_PYTHON_OPENCASCADE, True)
shape = ifcopenshell.geom.create_shape(s, f.by_type("IfcSpace")[0])

viewer = ifcopenshell.geom.utils.initialize_display()
#display, start_display, add_menu, add_function_to_menu = init_display()
#display.DisplayShape(shape)

ifcopenshell.geom.utils.display_shape(shape)
viewer.FitAll()
