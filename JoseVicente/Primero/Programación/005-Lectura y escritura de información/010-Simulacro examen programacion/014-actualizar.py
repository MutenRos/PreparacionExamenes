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
  print("4.-Eliminar una entrada")
  opcion = int(input("Introduce la opción escogida: "))
  
  if opcion == 1:
    titulo = input("Introduce el titulo del articulo: ")
    contenido = input("Introduce el contenido del articulo: ")
    fecha = input("Introduce la fecha del articulo: ")
    autor = input("Introduce el autor del articulo: ")
    cursor.execute("INSERT INTO entradas VALUES (NULL,'"+titulo+"','"+contenido+"','"+fecha+"',"+autor+")")
    conexion.commit()
  elif opcion == 2:
    cursor.execute("SELECT * FROM entradas_con_autores;")
    lineas = cursor.fetchall()
    for linea in lineas:
      print("|",linea[0],"|",linea[1],"|",linea[2],"|",linea[3],"|",linea[4],"|",linea[5])
  elif opcion == 3:
    identificador = input("Introduce el id del elemento a actualizar: ")
    titulo = input("Introduce el nuevo titulo del articulo: ")
    contenido = input("Introduce el nuevo contenido del articulo: ")
    fecha = input("Introduce la nueva fecha del articulo: ")
    autor = input("Introduce el nuevo autor del articulo: ")
    cursor.execute('''
      UPDATE entradas
      SET 
      titulo = "'''+titulo+'''",
      contenido = "'''+contenido+'''",
      fecha = "'''+fecha+'''",
      autor = '''+autor+'''
      WHERE
      Identificador = '''+identificador+'''
    ''')
    conexion.commit()
  elif opcion == 4:
    identificador = input("Introduce el id del elemento a eliminar: ")
    cursor.execute("DELETE FROM entradas WHERE Identificador = "+identificador+";")
    conexion.commit()
    
    
    
