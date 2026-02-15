#!/usr/bin/env python3
import tkinter as tk
from tkinter import ttk

# Datos de muestra
datos = [
    (1, "Manzana", 0.99),
    (2, "Banana", 0.59),
    (3, "Cereza", 2.49),
    (4, "Durazno", 1.49),
]

ventana = tk.Tk()

# Creo una vista de arbol que me sirve para jerarquias y para tablas
columnas = ("id", "producto", "precio")
arbol = ttk.Treeview(ventana, columns=columnas)

# --- Defino las cabeceras
arbol.heading("id", text="ID")
arbol.heading("producto", text="Producto")
arbol.heading("precio", text="Precio (€)")


for fila in datos:
    arbol.insert("", "end", values=fila)

arbol.pack(padx=10, pady=10)

ventana.mainloop()

