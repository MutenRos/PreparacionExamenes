import os
import fnmatch

def buscar_archivos():
    carpeta = input("Carpeta donde buscar: ").strip()
    patron = input("Patrón de nombre (ej: *.pdf): ").strip()

    if not os.path.isdir(carpeta):
        print("La carpeta no existe.")
        return

    print(f"\nBuscando archivos que coincidan con '{patron}' en '{carpeta}'...\n")

    encontrados = []

    for ruta_actual, subdirs, archivos in os.walk(carpeta):
        for archivo in archivos:
            if fnmatch.fnmatch(archivo, patron):
                ruta_completa = os.path.join(ruta_actual, archivo)
                encontrados.append(ruta_completa)
                print(ruta_completa)

    if not encontrados:
        print("No se encontró ningún archivo con ese patrón.")
    else:
        print(f"\nTotal encontrados: {len(encontrados)}")

if __name__ == "__main__":
    buscar_archivos()

