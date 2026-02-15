'''
  Programa clasificador de pilotos
  (c) 2025 Jose Vicente Carratala
  Este programa clasifica a los pilotos de carreras
'''

# Importaciones: Este programa no necesita importaciones


# Variables  globales
posicion_final = ""
mensaje = ""

# Clases / funciones: este programa no necesita clases o funciones

## Método o función principal
# Introducción de datos
posicion_final = input("Introduce la posición en la que has quedado: ")
posicion_final = int(posicion_final) # Tengo que convertir la cadena a numero entero
# Realización de cálculos
if posicion_final == 1:
  mensaje = "¡Eres el campeón de la carrera!"
elif posicion_final == 2 or posicion_final == 3:
  mensaje = "Subes al podio, gran trabajo."
elif posicion_final >=4 and posicion_final <=10:
  mensaje = "Has puntuado en el campeonato."
elif posicion_final >=11:
  mensaje = "No conseguiste puntos esta vez, sigue entrenando."
  
# Impresión de respuestas
print(mensaje)
