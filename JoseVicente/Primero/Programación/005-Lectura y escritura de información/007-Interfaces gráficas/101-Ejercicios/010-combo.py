import tkinter as tk
from tkinter.ttk import Combobox

ventana = tk.Tk()
desplegable = Combobox(ventana,values = ["manzana","pera","platano"])
desplegable.pack(padx=40,pady=40)

ventana.mainloop()
