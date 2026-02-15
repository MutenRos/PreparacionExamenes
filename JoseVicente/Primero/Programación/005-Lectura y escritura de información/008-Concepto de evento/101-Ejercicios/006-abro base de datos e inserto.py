import tkinter as tk
import sqlite3

conexion = sqlite3.connect("clientes.db")
cursor = conexion.cursor()

ventana = tk.Tk()

def insertaCliente():
  cursor.execute('INSERT INTO clientes VALUES(NULL,"","","")')
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


