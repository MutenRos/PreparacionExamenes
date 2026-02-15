import tkinter as tk

def insertaCliente():
  archivo = open("clientes.csv","a")
  archivo.write(nombre.get()+","+apellidos.get()+","+email.get()+"\n")
  archivo.close()
  listaClientes()
  
def listaClientes():
  texto.delete(1.0,tk.END)
  archivo = open("clientes.csv","r")
  lineas = archivo.readlines()
  for linea in lineas:
    texto.insert(tk.END,linea)
  archivo.close()
  
ventana = tk.Tk()

tk.Label(ventana,text="Introduce el nombre del cliente").pack(padx=10,pady=2)
nombre = tk.Entry(ventana)
nombre.pack(padx=10,pady=2)

tk.Label(ventana,text="Introduce los apellidos del cliente").pack(padx=10,pady=2)
apellidos = tk.Entry(ventana)
apellidos.pack(padx=10,pady=2)

tk.Label(ventana,text="Introduce el email del cliente").pack(padx=10,pady=2)
email = tk.Entry(ventana)
email.pack(padx=10,pady=2)

tk.Button(ventana,text="Insertar un cliente",command=insertaCliente).pack(padx=10,pady=2)

texto = tk.Text(ventana,height=5,width=30)
texto.pack(padx=10,pady=2)

listaClientes()

ventana.mainloop()
