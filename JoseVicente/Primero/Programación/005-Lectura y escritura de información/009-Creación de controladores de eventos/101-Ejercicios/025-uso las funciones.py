import mysql.connector

# Me conecto a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="blogexamen",
    password="Blogexamen123$",
    database="blogexamen"
)

cursor = conexion.cursor()
######################################## FUNCIONES

def bienvenida():
  print("Gestión de posts")
  print("v0.1 Jose Vicente Carratalá")

def menu():
  print("Escoge una opción:")
  print("1.-Crear entrada nueva")
  print("2.-Listar entradas")
  print("3.-Actualizar entrada")
  print("4.-Eliminar entradas")
  opcion = int(input("Escoge una opcion: "))

def insertar():
  titulo = input("Introduce el titulo: ")
  fecha = input("Introduce la fecha: ")
  contenido = input("Introduce el contenido: ")
  autor = input("Introduce el id del autor: ")
  cursor.execute("INSERT INTO posts VALUES (NULL,'"+titulo+"','"+fecha+"','"+contenido+"',"+autor+");")
  conexion.commit() 
  
def listar():
  cursor.execute("SELECT * FROM posts;")
  filas = cursor.fetchall()
  for fila in filas:
    print(fila)

def actualizar():
  identificador = input("Introduce el id de la entrada a actualizar: ")
  titulo = input("Introduce el titulo: ")
  fecha = input("Introduce la fecha: ")
  contenido = input("Introduce el contenido: ")
  autor = input("Introduce el id del autor: ")
  cursor.execute("UPDATE posts SET titulo = '"+titulo+"', fecha = '"+fecha+"', contenido = '"+contenido+"', autor = "+autor+" WHERE Identificador = "+identificador+";")
  conexion.commit()
  
def eliminar():
  identificador = input("Introduce el id de la entrada a eliminar: ")
  cursor.execute("DELETE FROM posts WHERE Identificador = "+identificador+";")
  conexion.commit()
######################################## FUNCIONES  

bienvenida()
while True:
  menu()
  
  if opcion == 1:
    insertar()
  elif opcion == 2:
    listar()
  elif opcion == 3:
    actualizar()
  elif opcion == 4:
    eliminar()
    
    
cursor.close()
conexion.close()
