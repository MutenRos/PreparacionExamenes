import os
import fnmatch

def buscar_y_reemplazar():
    carpeta = input("Carpeta donde buscar: ").strip()
    patron = input("Patrón de nombre (ej: *.py, *.txt) [vacío = todos]: ").strip()
    texto_buscar = input("Texto a buscar: ")
    texto_reemplazar = input("Texto de reemplazo [vacío = solo buscar, sin cambiar]: ")

    if not os.path.isdir(carpeta):
        print("La carpeta no existe.")
        return

    if not texto_buscar:
        print("No has indicado texto a buscar. Saliendo.")
        return

    if patron == "":
        patron = "*"  # todos los archivos

    solo_buscar = (texto_reemplazar == "")

    print(f"\nBuscando '{texto_buscar}' en archivos que coincidan con '{patron}' dentro de '{carpeta}'...\n")
    if solo_buscar:
        print("Modo: SOLO BÚSQUEDA (no se modificará ningún archivo)\n")
    else:
        print(f"Modo: BUSCAR Y REEMPLAZAR POR '{texto_reemplazar}'\n")

    archivos_procesados = 0
    archivos_con_coincidencias = 0
    total_coincidencias = 0
    total_reemplazos = 0

    for ruta_actual, subdirs, archivos in os.walk(carpeta):
        for nombre_archivo in archivos:
            if fnmatch.fnmatch(nombre_archivo, patron):
                ruta_completa = os.path.join(ruta_actual, nombre_archivo)
                archivos_procesados += 1

                try:
                    with open(ruta_completa, "r", encoding="utf-8", errors="ignore") as f:
                        contenido = f.read()
                except Exception as e:
                    print(f"[ERROR] No se puede leer: {ruta_completa} ({e})")
                    continue

                # Contar coincidencias
                coincidencias_en_archivo = contenido.count(texto_buscar)
                if coincidencias_en_archivo > 0:
                    archivos_con_coincidencias += 1
                    total_coincidencias += coincidencias_en_archivo
                    print(f"- {ruta_completa} ({coincidencias_en_archivo} coincidencia(s))")

                    if not solo_buscar:
                        nuevo_contenido = contenido.replace(texto_buscar, texto_reemplazar)
                        try:
                            with open(ruta_completa, "w", encoding="utf-8", errors="ignore") as f:
                                f.write(nuevo_contenido)
                            total_reemplazos += coincidencias_en_archivo
                        except Exception as e:
                            print(f"[ERROR] No se pudo escribir en: {ruta_completa} ({e})")

    print("\nResumen:")
    print(f"  Archivos procesados:          {archivos_procesados}")
    print(f"  Archivos con coincidencias:   {archivos_con_coincidencias}")
    print(f"  Total de coincidencias:       {total_coincidencias}")
    if solo_buscar:
        print("  Total de reemplazos:          0 (solo búsqueda)")
    else:
        print(f"  Total de reemplazos realizados: {total_reemplazos}")


if __name__ == "__main__":
    buscar_y_reemplazar()

