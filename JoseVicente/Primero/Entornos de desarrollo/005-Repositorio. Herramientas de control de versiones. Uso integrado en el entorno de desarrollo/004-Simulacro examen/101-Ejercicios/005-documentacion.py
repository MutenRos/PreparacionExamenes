'''
  Programa de examen
  Este es un crud de piezas de portafolio
  (c) 2025 Jose Vicente Carratala
'''

# Las funciones de tratamiento de bases de datos se encuentran en libreria externa
from funcionesbasededatos import presentaMenu,insertar,seleccionar, actualizar,eliminar

print("Gestion de portafolio v0.1")
while True:                                       # Usamos while para entrar en un bucle infinito
  presentaMenu()
  opcion = int(input("Escoge una opcion: "))
  print("La opción que has escogido es: ",opcion)
  if opcion == 1:                                 # if-elif para atrapar las opciones
    insertar()
  elif opcion == 2:
    seleccionar()
  elif opcion == 3:
    actualizar()
  elif opcion == 4:
    eliminar()
