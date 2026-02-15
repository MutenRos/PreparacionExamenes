import tkinter as tk
  
ventana = tk.Tk()

boton1 = tk.Button(text="Pulsame1")
boton1.grid(row=0,column=0)

boton2 = tk.Button(text="Pulsame2")
boton2.grid(row=0,column=1)

boton3 = tk.Button(text="Pulsame3")
boton3.grid(row=1,column=0)

boton4 = tk.Button(text="Pulsame4")
boton4.grid(row=1,column=1)

ventana.mainloop()
