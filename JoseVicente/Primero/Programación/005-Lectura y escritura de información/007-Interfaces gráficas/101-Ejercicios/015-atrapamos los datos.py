import tkinter as tk

def resuelve():
  o1 = float(operando1.get())
  o2 = float(operando2.get())
  print(o1+o2)

ventana = tk.Tk()
operando1 = tk.Entry(ventana)
operando1.pack(padx = 10, pady = 10)

operando2 = tk.Entry(ventana)
operando2.pack(padx = 10, pady = 10)

boton = tk.Button(text="Resolver",command=resuelve)
boton.pack(padx = 10, pady = 10)

resultado = tk.Entry(ventana)
resultado.pack(padx = 10, pady = 10) 

ventana.mainloop()
