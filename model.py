'''
InfraGOTApp: module for database management (PostgreSQL)
@author Sara Guerra de Oliveira, Andrej Tibaut
@modified 
@version 1.0
'''

### LIBRARIES in use

import ifc
import db
import file
from pathlib import Path
from datetime import datetime
# library for IfcOpenShell
import ifcopenshell


class Model:

    def __init__(self):
        # initially create database tables
        db.create_tables()
        

# 
# program flow
# fpn="/Users/andrejt/Research/Programiranje/Python/InfraGOT/LameziaGEO_UTM8433N_complete_4x1.ifc"
# 
# excelFile = file.readExcel("Runway_Radargram_Results.xlsx", "Radargram CL")
# print("Column headings:")
# print(excelFile.columns)

#### METHODS



# Reads db's latest value for the propertyname and prints it out
# def read_db_latest_property(docid, objectid, propertyname):
#     print()
#     print("*** Read DB's latest IFC properties ***")
# 
#     doc = db.get_document(docid)
#     print("Document id=" + str(docid) + ", file pathname=" + doc.fileLocation + ", file type=" + doc.fileCategory)
#     if doc.fileCategory == "IFC":
#         propertysets = ifc.get_ifc_element_propertyset(doc.fileLocation, objectid)
#         for property in enumerate(propertysets):
#             print(property)
#     return


# Reads Ifc file location from the db and prints out elements
# def read_model_ifc_elements(docid, ifcclass):
#     print()
#     print("*** Test IFC element ***")
#     
#     doc = db.get_document(docid)
#     print("Document id=" + str(docid) + ", file pathname=" + doc.fileLocation + ", file type=" + doc.fileCategory)
#     if  doc.fileCategory == "IFC":
#         ifc_elements = ifc.get_ifc_elements_by_type(doc.fileLocation, ifcclass)
#         for element in enumerate(ifc_elements):
#             print(element)
#     return    
                

# def read_model_ifc_properties(docid, objectid):
#     print()
#     print("*** Read IFC properties ***")
# 
#     doc = db.get_document(docid)
#     print("Document id=" + str(docid) + ", file pathname=" + doc.fileLocation + ", file type=" + doc.fileCategory)
#     if doc.fileCategory == "IFC":
#         propertysets = ifc.get_ifc_element_propertyset(doc.fileLocation, objectid)
#         for property in enumerate(propertysets):
#             print(property)
#     return


# def update_model_ifcproperty(docid, objectid, ifcproperty):
#     print()
#     print("*** Update IFC property in the model ***")
# 
#     doc = db.get_document(docid)
#     print("Document id=" + str(docid) + ", file pathname=" + doc.fileLocation + ", file type=" + doc.fileCategory)
#     if doc.fileCategory == "IFC":
#         myproperty = ifc.get_ifc_element_property(doc.fileLocation, objectid, ifcproperty)
#         print(myproperty)
# #            if prop.Name==ifcproperty:
#     return



#            if prop.Name==ifcproperty:
                
                # # Create and assign property set
#  property_values = [
#      ifcfile.createIfcPropertySingleValue("Reference", "Reference", ifcfile.create_entity
#  ("IfcText", "Describe the Reference"), None),
#      ifcfile.createIfcPropertySingleValue("IsExternal", "IsExternal", ifcfile.create_entity
#  ("IfcBoolean", True), None),
#      ifcfile.createIfcPropertySingleValue("ThermalTransmittance", "ThermalTransmittance", 
#  ifcfile.create_entity("IfcReal", 2.569), None),
#      ifcfile.createIfcPropertySingleValue("IntValue", "IntValue", ifcfile.create_entity
#  ("IfcInteger", 2), None)
#  ]
#  property_set = ifcfile.createIfcPropertySet(create_guid(), owner_history, 
#  "Pset_WallCommon", None, property_values)
#  ifcfile.createIfcRelDefinesByProperties(create_guid(), owner_history, None, None, [wall], 
#  property_set)
                




