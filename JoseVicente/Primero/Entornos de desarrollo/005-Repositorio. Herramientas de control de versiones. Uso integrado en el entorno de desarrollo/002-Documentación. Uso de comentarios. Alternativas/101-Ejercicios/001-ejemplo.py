'''
    Vamos a crear un programa en Python
    Que muestre el arbol de carpetas y archivos de un directorio
    Para ello usaremos la libreria os
    Y la funcion os.walk para recorrer el arbol de directorios
    El programa pedira al usuario la ruta del directorio a mostrar
    Y mostrara el arbol de carpetas y archivos en la consola
    Y para ello usará caracteres ASCII para el arbol de directorios
    Y emojis para las carpetas y archivos
'''

import os

def mostrar_arbol_directorio(ruta_directorio):
    for raiz, carpetas, archivos in os.walk(ruta_directorio):
        nivel = raiz.replace(ruta_directorio, '').count(os.sep)
        indentacion = ' ' * 4 * nivel
        print(f"{indentacion}📁 {os.path.basename(raiz)}/")
        sub_indentacion = ' ' * 4 * (nivel + 1)
        for archivo in archivos:
            print(f"{sub_indentacion}📄 {archivo}")
    
    
      

# Ruta del directorio que queremos mostrar
ruta = input("Introduce la ruta: ")  # Puedes cambiar esto a cualquier ruta que desees
mostrar_arbol_directorio(ruta)