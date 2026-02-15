import tkinter as tk


ventana = tk.Tk()
operando1 = tk.Entry(ventana)
operando1.pack(padx = 10, pady = 10)

operando2 = tk.Entry(ventana)
operando2.pack(padx = 10, pady = 10)

boton = tk.Button(text="Resolver")
boton.pack(padx = 10, pady = 10)

resultado = tk.Entry(ventana)
resultado.pack(padx = 10, pady = 10) 

ventana.mainloop()
