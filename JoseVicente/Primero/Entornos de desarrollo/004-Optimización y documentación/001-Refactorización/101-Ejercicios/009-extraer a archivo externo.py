'''
  Programa agenda v0.1
  Jose Vicente Carratala
'''

from funciones import imprimeBienvenida, muestraMenu, insertarCliente, listadoClientes, actualizaClientes, borraClientes
  
################## DEFINICION DE VARIABLES GLOBALES #######################################3

clientes = ""

################## BUCLE PRINCIPAL #######################################3

imprimeBienvenida()

while True:
  muestraMenu()
  opcion = input("Elige tu opcion: ")
  opcion = int(opcion)
  
  if opcion == 1:
    insertarCliente()
  elif opcion == 2:
    listadoClientes()
  elif opcion == 3:
    actualizaClientes()
  elif opcion == 4:
    borraClientes()
  
  
