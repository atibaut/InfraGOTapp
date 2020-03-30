'''
# InfraGOTApp: module for file management
@author Sara Guerra de Oliveira, Andrej Tibaut
@modified 
@version 1.0
'''

### LIBRARIES in use
from datetime import datetime
# a library "pandas" that supports work with Excel documents 
import pandas as pd
###

documentList = []

# classes  

class Document:    
    """__init__() functions as the class constructor"""
    def __init__(self, fileLocation, fileCategory):
        self.fileLocation = fileLocation
        self.fileCategory = fileCategory    


#### METHODS


def populate_documents():

# new object Document
    # 0
    documentList.append(Document(fileLocation="PZI_3-3_1441_LIN_PRO_M-M3.ifc", fileCategory="IFC"))
    # 1
    documentList.append(Document(fileLocation="maribor_junction_pariske-komune_4.ifc", fileCategory="IFC"))
    # 2
    documentList.append(Document(fileLocation="PZI_9-1_1441_LIN_CES_1-17c-O_M-M3.ifc", fileCategory="IFC"))


def print_documents():
    print('*** Print documents ***')
    for d in documentList:
        print('Document file pathname is ', d.fileLocation + ", file category is " + d.fileCategory)
    print()


def test_documents():
    print()
    print_documents()



def get_document(document_id):
    d = documentList[document_id]
    return d 

def readFileContent(filePathname):
    with open(filePathname, 'r') as f:
        data = f.read()
    return data 

# read sheet "Sheet1" from the file "File.xlsx"
# the file is in the project folder
def readExcel(filePathname, sheetName):
    theFile = pd.read_excel(filePathname, sheet_name=sheetName)
    return theFile 

 

# program flow
# make a list of class Documents(s)
# populate_documents()
# test_documents()

