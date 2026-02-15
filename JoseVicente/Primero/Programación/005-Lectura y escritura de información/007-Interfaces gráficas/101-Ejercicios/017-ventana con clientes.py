import tkinter as tk

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

tk.Button(ventana,text="Insertar un cliente").pack(padx=10,pady=2)

ventana.mainloop()
