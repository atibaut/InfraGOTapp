'''
InfraGOTApp: a View according to the MVC pattern
@author Sara Guerra de Oliveira, Andrej Tibaut
@modified 
@version 1.0
'''

from pathlib import Path   
from tkinter import filedialog
from tkinter import ttk
import tkinter as Tk
from PIL import Image, ImageTk # pip install Pillow


class View:

    def __init__(self, controller, root):
        self.controller = controller
        
        # Button custom style
        self.style = ttk.Style()
        self.style.map("C.TButton",
              foreground=[('pressed', 'red'), ('active', 'blue')],
              background=[('pressed', '!disabled', 'black'),
                          ('active', 'white')])
        
        
        # Treeview custom style
        #style = Style()
        #style.configure(".", font=('Helvetica', 10), foreground="white")
        #style.configure("Treeview", foreground='black')
        #style.configure("Treeview.Heading", foreground='green')  #<----

        # String variables
        self.msgIfc = Tk.StringVar()
        self.msgData = Tk.StringVar()
        self.msgIfcConvert = Tk.StringVar()
        self.msgIfcExport = Tk.StringVar()

        # frame for the title label
        self.frameTitle = Tk.Frame(root, padx=5, pady=5)
        self.frameTitle.grid(row=0, column=0, columnspan=3, sticky=Tk.W + Tk.E)
        self.lblTitle = Tk.Label(self.frameTitle, text="InfraGOTapp (=INFRAstructure GOT APPlication)", background="gray", justify=Tk.CENTER)
        self.lblTitle.grid(row=0, column=0, sticky=Tk.W + Tk.E)
        
        # labeled frame for the IFC model and data loading     
        self.frameModel = Tk.LabelFrame(root, text='Select open BIM model and domain specific data', padx=5, pady=5)
        self.frameModel.grid(row=1, column=0, rowspan=2, padx=5, sticky=Tk.N + Tk.S + Tk.E + Tk.W)
        self.btnIfcUpgrade = ttk.Button(self.frameModel, text="Load IFC model", cursor="hand2", command=self.selectIfc, style="C.TButton")
        self.btnIfcUpgrade.grid(row=0, column=0, padx=5, pady=5, sticky=Tk.W)
        self.lblIfc = Tk.Label(self.frameModel, borderwidth=2, relief="ridge", textvariable=self.msgIfc)
        self.lblIfc.grid(row=0, column=1, padx=5, pady=5, sticky=Tk.W)
        self.btnIfcLinkdb = ttk.Button(self.frameModel, text="Load data", cursor="hand2", command=self.selectData, style="C.TButton")
        self.btnIfcLinkdb.grid(row=1, column=0, padx=5, pady=5, sticky=Tk.W)
        self.lblData = Tk.Label(self.frameModel, borderwidth=2, relief="ridge", textvariable=self.msgData)
        self.lblData.grid(row=1, column=1, padx=5, pady=5, sticky=Tk.W)
        
        # self.sep1 = ttk.Separator(root).grid(row=2, column=0, columnspan=2, sticky=(Tk.W, Tk.E))

        self.frameTree = Tk.LabelFrame(root, text='Loaded open BIM model and domain specific data', padx=5, pady=5)
        self.frameTree.grid(row=3, column=0, padx=5, sticky=Tk.N + Tk.S + Tk.E + Tk.W)
        self.treeModelAndData = ttk.Treeview(self.frameTree, columns=("Type"))
        self.treeModelAndData.grid(row=0, column=0, padx=5, sticky=Tk.N + Tk.S + Tk.E + Tk.W)
        self.treeModelAndData.heading("#0", text="Model", anchor=Tk.W)
        self.treeModelAndData.heading("Type", text="Type", anchor=Tk.CENTER)
        self.treeModelAndData.column("#0", anchor=Tk.W)
        self.treeModelAndData.column("Type", anchor=Tk.CENTER)   
        # self.treeModelAndData.insert("", 1, text="<empty>", values=("<empty>"))

        # self.sep2 = ttk.Separator(self.frameModel).grid(row=7, column=0, columnspan=2, sticky=(Tk.W, Tk.E))
        
        # labeled frame for the IFC model and data loading 
        self.frameIfcworkflow = Tk.LabelFrame(root, text='IFC model upgrade, link and export', padx=5, pady=5)
        self.frameIfcworkflow.grid(row=4, column=0, padx=5, sticky=Tk.N + Tk.S + Tk.E + Tk.W)
        self.btnIfcUpgrade = ttk.Button(self.frameIfcworkflow, text="Upgrade IFC model to IFC 4.3", cursor="hand2", command=self.upgradeIfc, style="C.TButton")
        self.btnIfcUpgrade.grid(row=0, column=0, padx=(5), pady=5, sticky=Tk.W)
        self.btnIfcLinkdb = ttk.Button(self.frameIfcworkflow, text="Link IFC model to database", cursor="hand2", command=self.linkIfcToDatabase, style="C.TButton")
        self.btnIfcLinkdb.grid(row=0, column=1, padx=(5), pady=5, sticky=Tk.W)
        self.btnIfcExport = ttk.Button(self.frameIfcworkflow, text="Export IFC model", cursor="hand2", command=self.exportIfc, style="C.TButton")
        self.btnIfcExport.grid(row=0, column=2, padx=(5), pady=5, sticky=Tk.W)
        
        # frame for content visualization        
        self.frameImage = Tk.LabelFrame(root, text='Preview', padx=5, pady=5, width=700, height=500)
        self.frameImage.grid(row=1, column=1, padx=(0, 5), rowspan=4, sticky=Tk.N + Tk.S + Tk.E + Tk.W)
        self.imageOriginal1 = Image.open("data/Radargram.jpg")        #self.imageResized = self.imageOriginal1.resize((400, 400), Image.ANTIALIAS)

        self.imageOriginal2 = ImageTk.PhotoImage(self.imageOriginal1)
        self.imageDisplay = Tk.Canvas(self.frameImage, width=500, height=300)
        self.imageDisplay.create_image(0, 0, image=self.imageOriginal2, anchor=Tk.NW, tags="IMG")
        self.imageDisplay.grid(row=0, column=0, sticky=Tk.N + Tk.S + Tk.E + Tk.W)
        self.frameImage.bind("<Configure>", self.resizeContentWindow)

        # Frame for the console window
        self.frameConsole = Tk.LabelFrame(root, text='Console', padx=5, pady=5)
        self.frameConsole.grid(row=5, column=0, padx=5, columnspan=3, sticky=Tk.N + Tk.S + Tk.E + Tk.W)
        self.scrbConsole = Tk.Scrollbar(self.frameConsole)
        self.console = Tk.Text(self.frameConsole, height=5, bg="white", fg="black")
        self.scrbConsole.config(command=self.console.yview)
        self.console.configure(yscrollcommand=self.scrbConsole.set)  
        self.console.grid(row=0, column=0, columnspan=2, sticky=Tk.N + Tk.S + Tk.E + Tk.W)

        # frame for the Quit button
        self.frameClosing = Tk.Frame(root, padx=5, pady=5)
        self.frameClosing.grid(row=6, column=0, sticky=Tk.W + Tk.E)
        self.btnQuit = ttk.Button(self.frameClosing, text="Close", cursor="hand2", command=self.quit, style="C.TButton")
        self.btnQuit.grid(row=0, column=0, padx=(5), pady=5, sticky=Tk.W)

        # resize options
        root.columnconfigure(0, weight=1)
        self.frameTitle.columnconfigure(0, weight=1)
        self.frameModel.columnconfigure(0, weight=1)
        
        self.frameConsole.columnconfigure(0, weight=1)
        self.frameTree.columnconfigure(0, weight=1)
        
        
    def resizeContentWindow(self, event):
        size = (event.width, event.height)
        resized = self.imageOriginal1.resize(size,Image.ANTIALIAS)
        self.image1 = ImageTk.PhotoImage(resized)
        self.imageDisplay.delete("IMG")
        self.imageDisplay.create_image(0, 0, image=self.image1, anchor=Tk.NW, tags="IMG")
        return
        
    def selectIfc(self):
        self.filename = filedialog.askopenfilename(initialdir=".", title="Select IFC model", filetypes=(("IFC files", "*.ifc"), ("all files", "*.*")))
        self.msgIfc.set(Path(self.filename).name) 
        print (self.filename + " selected.")
        txt = 'loading IFC model: ' + self.filename + '\n'
        self.console.insert(Tk.END, txt)
        print(txt)

        # load, check and store the file to the database 
        self.controller.loadAndStoreIfcFile(self.filename)

        # insert entry to the list of IFC files
        self.folder1 = self.treeModelAndData.insert("", 1, text=Path(self.filename).stem, values=(Path(self.filename).suffix))
        return

    def selectData(self):
        self.filename = filedialog.askopenfilename(initialdir=".", title="Select data set file")
        self.msgData.set(Path(self.filename).name) 
        print (self.filename + " selected.")
        txt = "Loading data file: " + self.filename + '\n'
        self.console.insert(Tk.END, txt)
        print(txt)

        # self.treeModelAndData.insert(self.folder1, 1, "end", text=Path(self.filename).stem, values=(Path(self.filename).suffix))
        self.treeModelAndData.insert(self.folder1, "end", text=Path(self.filename).stem, values=(Path(self.filename).suffix))
        return

    def upgradeIfc(self):
        txt = 'Upgrading IFC model %s to IFC 4.3...' % (self.msgIfc.get()) + '\n'
        self.console.insert(Tk.END, txt)
        print(txt)
        return

    def linkIfcToDatabase(self):
        txt = 'Linking IFC model %s to the InfraGOTdb database...' % (self.msgIfc.get()) + '\n'
        self.console.insert(Tk.END, txt)
        print(txt)
        return

    def exportIfc(self):
        txt = 'Exporting IFC model %s_export%s compliant with the IFC 4.3 schema...' % (Path(self.msgIfc.get()).stem, Path(self.msgIfc.get()).suffix) + '\n'
        self.console.insert(Tk.END, txt)
        print(txt)
        return

    def quit(self):
        print("exiting InfraGOTdata.")
        exit()

