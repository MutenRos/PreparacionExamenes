import tkinter as tk
import os
import sqlite3
from datetime import datetime

ventana = tk.Tk()

def procesar():
    carpeta_inicial = carpeta.get().strip()
    nombre_disco = disco.get().strip()

    if not carpeta_inicial or not os.path.isdir(carpeta_inicial) or not nombre_disco:
        print("Carpeta o disco no válidos")
        return

    conn = sqlite3.connect("discos.db")
    cur = conn.cursor()

    for raiz, subdirs, archivos in os.walk(carpeta_inicial):
        for arch in archivos:
            ruta_completa = os.path.join(raiz, arch)
            try:
                tamanio = os.path.getsize(ruta_completa)
                creacion = datetime.fromtimestamp(os.path.getctime(ruta_completa)).isoformat(timespec="seconds")
                modificacion = datetime.fromtimestamp(os.path.getmtime(ruta_completa)).isoformat(timespec="seconds")

                cur.execute(
                    "INSERT INTO archivos (disco, ruta, archivo, tamanio, creacion, modificacion) VALUES (?,?,?,?,?,?)",
                    (nombre_disco, raiz, arch, str(tamanio), creacion, modificacion)
                )
            except Exception as e:
                # si algún archivo no se puede leer, lo saltamos
                continue

    conn.commit()
    conn.close()
    print("Proceso completado")


tk.Label(text="Indica el nombre de la carpeta a indexar").pack(padx = 20,pady = 20)
carpeta = tk.Entry()
carpeta.pack(padx = 20,pady = 20)

tk.Label(text="Indica el nombre del disco").pack(padx = 20,pady = 20)
disco = tk.Entry()
disco.pack(padx = 20,pady = 20)

tk.Button(text="Procesar",command = procesar).pack(padx = 20,pady = 20)

ventana.mainloop()

