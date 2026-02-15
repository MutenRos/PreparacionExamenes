import tkinter as tk

ventana = tk.Tk()

tk.Label("Indica el nombre de la carpeta a indexar").pack(padx = 20,pady = 20)
carpeta = tk.Entry()
carpeta.pack(padx = 20,pady = 20)

tk.Label("Indica el nombre del disco").pack(padx = 20,pady = 20)
disco = tk.Entry()
disco.pack(padx = 20,pady = 20)

tk.Button(text="Procesar",command = procesar)

ventana.mainloop()


