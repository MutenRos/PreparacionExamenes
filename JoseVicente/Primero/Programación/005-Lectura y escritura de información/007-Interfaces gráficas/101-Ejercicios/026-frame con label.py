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

marco1 = tk.LabelFrame(text="Insertar un cliente")

tk.Label(marco1,text="Introduce el nombre del cliente").pack(padx=10,pady=2)
nombre = tk.Entry(marco1)
nombre.pack(padx=10,pady=2)

tk.Label(marco1,text="Introduce los apellidos del cliente").pack(padx=10,pady=2)
apellidos = tk.Entry(marco1)
apellidos.pack(padx=10,pady=2)

tk.Label(marco1,text="Introduce el email del cliente").pack(padx=10,pady=2)
email = tk.Entry(marco1)
email.pack(padx=10,pady=2)

tk.Button(marco1,text="Insertar un cliente",command=insertaCliente).pack(padx=10,pady=2)

marco1.grid(row=0,column=0,padx=10,pady=10)

texto = tk.Text(ventana,height=5,width=30)
texto.grid(row=0,column=1)

listaClientes()

ventana.mainloop()
