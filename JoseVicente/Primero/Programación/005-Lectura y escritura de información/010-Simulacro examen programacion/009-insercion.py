import mysql.connector

conexion = mysql.connector.connect(
  host="localhost",
  user="blog2526",
  password="blog2526",
  database="blog2526"
)

cursor = conexion.cursor()

class Entrada():
  def __init__(self,titulo,contenido,fecha,autor):
    self.titulo = titulo
    self.contenido = contenido
    self.fecha = fecha
    self.autor = autor
    
print("Entradas de un blog")
while True:
  print("Elige una opcion: ")
  print("1.-Insertar una entrada")
  print("2.-Listar las entradas")
  print("3.-Actualizar una entrada")
  print("4.-Listar una entrada")
  opcion = int(input("Introduce la opción escogida: "))
  
  if opcion == 1:
    titulo = input("Introduce el titulo del articulo: ")
    contenido = input("Introduce el contenido del articulo: ")
    fecha = input("Introduce la fecha del articulo: ")
    autor = input("Introduce el autor del articulo: ")
    cursor.execute("INSERT INTO entradas VALUES (NULL,'"+titulo+"','"+contenido+"','"+fecha+"',"+autor+")")
    conexion.commit()
  elif opcion == 2:
    pass
  elif opcion == 3:
    pass
  elif opcion == 4:
    pass
