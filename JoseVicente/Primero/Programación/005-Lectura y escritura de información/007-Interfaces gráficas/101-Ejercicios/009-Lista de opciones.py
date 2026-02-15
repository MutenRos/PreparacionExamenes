import tkinter as tk

ventana = tk.Tk()
frutas = ["manzana","pera","platano","limon"]
lista = tk.Listbox(ventana)
for fruta in frutas:
  lista.insert(tk.END,fruta)
  
lista.pack()

ventana.mainloop()
