'''
InfraGOTApp is a prototype program in Python that supports IFC workflow for infrastructure projects
with the use of Object-Relational Mapper (Pony ORM), database (PostgreSQL) and IfcOpenShell
@author Sara Guerra de Oliveira, Andrej Tibaut
@modified 2019, 2020 
@version 1.0
'''

# ## LIBRARIES in use

from controller import Controller

# start of the main module
if __name__ == '__main__':
    c = Controller() # initialize a controller
    c.run() # run the controller
