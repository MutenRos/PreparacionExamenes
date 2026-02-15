import tkinter as tk
import sqlite3
import ttkbootstrap as tb
from ttkbootstrap import ttk

conexion = sqlite3.connect("clientes.db")
cursor = conexion.cursor()

#ventana = tk.Tk()
ventana = tb.Window(themename="darkly")

def insertaCliente():
  cursor.execute('INSERT INTO clientes VALUES(NULL,"'+nombre.get()+'","'+apellidos.get()+'","'+email.get()+'")')
  conexion.commit()

nombre = tk.Entry(ventana)
nombre.pack(padx = 20,pady = 20)

apellidos = tk.Entry(ventana)
apellidos.pack(padx = 20,pady = 20)

email = tk.Entry(ventana)
email.pack(padx = 20,pady = 20)

boton = tk.Button(ventana,text="Insertar cliente",command=insertaCliente)
boton.pack(padx = 20,pady = 20)

ventana.mainloop()


