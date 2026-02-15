import tkinter as tk

ventana = tk.Tk()

def insertaCliente():
  print("Voy a insertar un cliente")

nombre = tk.Entry(ventana)
nombre.pack(padx = 20,pady = 20)

apellidos = tk.Entry(ventana)
apellidos.pack(padx = 20,pady = 20)

email = tk.Entry(ventana)
email.pack(padx = 20,pady = 20)

boton = tk.Button(ventana,text="Insertar cliente",command=insertaCliente)
boton.pack(padx = 20,pady = 20)

ventana.mainloop()


