from funcionesbasededatos import presentaMenu,insertar,seleccionar, actualizar,eliminar

print("Gestion de portafolio v0.1")
while True:
  presentaMenu()
  opcion = int(input("Escoge una opcion: "))
  print("La opción que has escogido es: ",opcion)
  if opcion == 1:
    insertar()
  elif opcion == 2:
    seleccionar()
  elif opcion == 3:
    actualizar()
  elif opcion == 4:
    eliminar()
