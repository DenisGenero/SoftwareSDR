from tkinter import *
from tkinter import messagebox #Para ventanas emergentes
from tkinter import filedialog #Para manejar archivos

#Root definition and configuration
raiz=Tk()
raiz.title("Medido SDR - F.I-U.N.E.R - Denis Genero")
raiz.iconbitmap("icono.ico")
raiz.config(bg="grey64")

# -------------------------- Menu desplegable --------------------------

barraMenu=Menu(raiz)
raiz.config(menu=barraMenu)

# ----------- Funciones ----------- #

def infoAdicional():
    messagebox.showinfo("Software del Deni", "Versión del sistema: 1.0")

def avisoLicencia():
    messagebox.showwarning("Licencia", "No pagaste por la licencia, deja de ROBAR!")

def salirAplicacion():
    valorSalida = messagebox.askokcancel("Salir", "Desea salir de la aplicacion?")
    if valorSalida==True:
        raiz.destroy()

def cerrarDocumento():
    valor=messagebox.askretrycancel("Reintentar", "No es posible cerrar el documento")
    if valor==False:
        raiz.destroy()

def abrirArchivo():
    archivo=filedialog.askopenfilename(title="Abrir",initialdir="C:", filetypes=(("Archivos de excel", "*.xlsx"),
                ("Archivos de texto", "*.txt"), ("Todos los archivos","*.*")))
    print(archivo)

# ----------- Interfaz ----------- #

#Archivo
ArchivoMenu=Menu(barraMenu, tearoff=0)
ArchivoMenu.add_command(label="Guardar estudio")
ArchivoMenu.add_command(label="Cargar estudio", command=abrirArchivo)
ArchivoMenu.add_command(label="Nuevo estudio")
ArchivoMenu.add_separator()
ArchivoMenu.add_command(label="Cerrar estudio", command=cerrarDocumento)
ArchivoMenu.add_command(label="Salir", command=salirAplicacion)

#Dispositivo
DispositivoMenu=Menu(barraMenu, tearoff=0)
DispositivoMenu.add_command(label="Conectar con dispositivo")
DispositivoMenu.add_command(label="Apagar dispositivo")

#Pacientes
PacientesMenu=Menu(barraMenu, tearoff=0)
PacientesMenu.add_command(label="Buscar paciente")

AyudaMenu=Menu(barraMenu, tearoff=0)
AyudaMenu.add_command(label="Licencia", command=avisoLicencia)
AyudaMenu.add_command(label="Versión del sistema", command=infoAdicional)

barraMenu.add_cascade(label="Archivo", menu=ArchivoMenu)
barraMenu.add_cascade(label="Pacientes", menu=PacientesMenu)
barraMenu.add_cascade(label="Dispositivo", menu=DispositivoMenu)
barraMenu.add_cascade(label="Ayuda", menu=AyudaMenu)

# ----------------------------------------------------------------------

#Frame definition and configuration
miFrame=Frame()
miFrame.pack()
miFrame.config(bg="white", width="650", height="400")
#miFrame.config(relief= "groove",bd=10)

raiz.mainloop()