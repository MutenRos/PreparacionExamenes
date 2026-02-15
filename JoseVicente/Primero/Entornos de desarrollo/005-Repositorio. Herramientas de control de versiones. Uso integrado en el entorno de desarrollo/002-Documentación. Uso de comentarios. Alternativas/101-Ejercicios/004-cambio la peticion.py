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
    '''
    Muestra el árbol de directorios y archivos de la ruta especificada.
    Parámetros:
    ruta_directorio (str): La ruta del directorio a mostrar.
    Retorna:    
    una cadena de texto con el árbol de directorios y archivos (no con print sino con return    )
    '''
    for raiz, carpetas, archivos in os.walk(ruta_directorio):   # Recorre el árbol de directorios
        nivel = raiz.replace(ruta_directorio, '').count(os.sep)  # Calcula el nivel de profundidad
        indentacion = ' ' * 4 * nivel  # Crea la indentación según el nivel
        print(f"{indentacion}📁 {os.path.basename(raiz)}/")  # Muestra la carpeta actual
        sub_indentacion = ' ' * 4 * (nivel + 1)  # Indentación para los archivos
        for archivo in archivos:  # Recorre los archivos en la carpeta actual
            print(f"{sub_indentacion}📄 {archivo}")  # Muestra cada archivo
      
        
    
    
      

# Ruta del directorio que queremos mostrar
ruta = input("Introduce la ruta: ")  # Puedes cambiar esto a cualquier ruta que desees
mostrar_arbol_directorio(ruta)