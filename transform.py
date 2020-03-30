'''
InfraGOTApp: module for transformation of IFC files
@author Sara Guerra de Oliveira, Andrej Tibaut
@modified 
@version 1.0
'''


import ifcopenshell
import tempfile
import time
import uuid


# create_guid = lambda: ifcopenshell.guid.compress(uuid.uuid1().hex)
# 
# IFC template creation
create_guid = lambda: ifcopenshell.guid.compress(uuid.uuid1().hex)
 
filename = "hello_wall.ifc"
timestamp = time.time()
timestring = time.strftime("%Y-%m-%dT%H:%M:%S", time.gmtime(timestamp))
creator = "Kianwee Chen"
organization = "ETHZ"
application, application_version = "IfcOpenShell", "0.5"
project_globalid, project_name = create_guid(), "Hello Wall"

# A template IFC file to quickly populate entity instances for an IfcProject with its dependencies
template = """ISO-10303-21;
HEADER;
FILE_DESCRIPTION(('ViewDefinition [CoordinationView]'),'2;1');
FILE_NAME('%(filename)s','%(timestring)s',('%(creator)s'),('%(organization)s'),'%(application)s','%(application)s','');
FILE_SCHEMA(('IFC2X3'));
ENDSEC;
DATA;
#1=IFCPERSON($,$,'%(creator)s',$,$,$,$,$);
#2=IFCORGANIZATION($,'%(organization)s',$,$,$);
#3=IFCPERSONANDORGANIZATION(#1,#2,$);
#4=IFCAPPLICATION(#2,'%(application_version)s','%(application)s','');
#5=IFCOWNERHISTORY(#3,#4,$,.ADDED.,$,#3,#4,%(timestamp)s);
#6=IFCDIRECTION((1.,0.,0.));
#7=IFCDIRECTION((0.,0.,1.));
#8=IFCCARTESIANPOINT((0.,0.,0.));
#9=IFCAXIS2PLACEMENT3D(#8,#7,#6);
#10=IFCDIRECTION((0.,1.,0.));
#11=IFCGEOMETRICREPRESENTATIONCONTEXT($,'Model',3,1.E-05,#9,#10);
#12=IFCDIMENSIONALEXPONENTS(0,0,0,0,0,0,0);
#13=IFCSIUNIT(*,.LENGTHUNIT.,$,.METRE.);
#14=IFCSIUNIT(*,.AREAUNIT.,$,.SQUARE_METRE.);
#15=IFCSIUNIT(*,.VOLUMEUNIT.,$,.CUBIC_METRE.);
#16=IFCSIUNIT(*,.PLANEANGLEUNIT.,$,.RADIAN.);
#17=IFCMEASUREWITHUNIT(IFCPLANEANGLEMEASURE(0.017453292519943295),#16);
#18=IFCCONVERSIONBASEDUNIT(#12,.PLANEANGLEUNIT.,'DEGREE',#17);
#19=IFCUNITASSIGNMENT((#13,#14,#15,#18));
#20=IFCPROJECT('%(project_globalid)s',#5,'%(project_name)s',$,$,$,$,(#11),#19);
ENDSEC;
END-ISO-10303-21;
""" % locals()

f1 = ifcopenshell.open("IfcOpenHouse_IFC2x3.ifc")
filename = "new_file.ifc"
# Write the template to a temporary file 
temp_handle, temp_filename = tempfile.mkstemp(suffix=".ifc")
with open(temp_filename, "w") as f:
    f.write(template)
# Obtain references to instances defined in template
f2 = ifcopenshell.open(temp_filename)
     

my_wall = f1.by_type("IfcWall")[0]
# For wall and forward references
for x in f1.traverse(my_wall):
  f2.add(x)
# For material association (layerset)
for assoc in my_wall.HasAssociations:
  f2.add(assoc)
# For neighbouring elements
for path in my_wall.ConnectedFrom + my_wall.ConnectedTo:
  f2.add(path)
f2.write(filename)