import tkinter as tk

def resuelve():
  o1 = int(operando1.get())
  o2 = int(operando2.get())
  r = o1+o2
  resultado.delete(0,tk.END)
  resultado.insert(0,r)
  

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
