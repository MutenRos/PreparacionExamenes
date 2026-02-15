import mysql.connector

# Me conecto a la base de datos
conexion = mysql.connector.connect(
    host="localhost",
    user="blogexamen",
    password="Blogexamen123$",
    database="blogexamen"
)

cursor = conexion.cursor()

print("Gestión de posts")
print("v0.1 Jose Vicente Carratalá")

while True:
  print("Escoge una opción:")
  print("1.-Crear entrada nueva")
  print("2.-Listar entradas")
  print("3.-Actualizar entrada")
  print("4.-Eliminar entradas")
  opcion = int(input("Escoge una opcion: "))
  
  if opcion == 1:
    titulo = input("Introduce el titulo: ")
    fecha = input("Introduce la fecha: ")
    contenido = input("Introduce el contenido: ")
    autor = input("Introduce el id del autor: ")
    cursor.execute("INSERT INTO posts VALUES (NULL,'"+titulo+"','"+fecha+"','"+contenido+"',"+autor+");")
    conexion.commit()
  elif opcion == 2:
    cursor.execute("SELECT * FROM posts;")
    filas = cursor.fetchall()
    for fila in filas:
      print(fila)
    pass
  elif opcion == 3:
    identificador = input("Introduce el id de la entrada a actualizar: ")
    titulo = input("Introduce el titulo: ")
    fecha = input("Introduce la fecha: ")
    contenido = input("Introduce el contenido: ")
    autor = input("Introduce el id del autor: ")
    cursor.execute("UPDATE posts SET titulo = '"+titulo+"', fecha = '"+fecha+"', contenido = '"+contenido+"', autor = "+autor+" WHERE Identificador = "+identificador+";")
    conexion.commit()
    pass
  elif opcion == 4:
    pass
    
    
cursor.close()
conexion.close()
