import mysql.connector

conexion = mysql.connector.connect(
  host="localhost",
  user="portafolio",
  password="portafolio",
  database="portafolio"
)
cursor = conexion.cursor() 

def presentaMenu():
  # Esta función simplemente pinta un menu en pantalla con prints
  print("Escoge una opcion")
  print("1.-Insertar")
  print("2.-Listar")
  print("3.-Actualizar")
  print("4.-Eliminar")
  
def insertar():
  # Esta funcion le pide una serie de inputs al usuario y los inserta en la base de datos
  titulo = input("Introduce el titulo de la nueva pieza: ")
  descripcion = input("Introduce la descripcion de la nueva pieza: ")
  fecha = input("Introduce la fecha de la nueva pieza: ")
  imagen = input("Introduce el nombre de la imagen de la nueva pieza: ")
  cursor.execute("INSERT INTO piezas VALUES (NULL,'"+titulo+"','"+descripcion+"','"+fecha+"',1,'"+imagen+"');")
  conexion.commit()
def seleccionar():
  #Esta función selecciona todo de la tabla y lo presenta en pantalla
  cursor.execute("SELECT * FROM piezas;")
  lineas = cursor.fetchall()
  for linea in lineas:
    print(linea)
def actualizar():
  identificador = input("Introduce el Identificador a actualizar: ")
  titulo = input("Introduce el titulo de la nueva pieza: ")
  descripcion = input("Introduce la descripcion de la nueva pieza: ")
  fecha = input("Introduce la fecha de la nueva pieza: ")
  imagen = input("Introduce el nombre de la imagen de la nueva pieza: ")
  cursor.execute('''
    UPDATE piezas 
    SET
    titulo = "'''+titulo+'''",
    descripcion = "'''+descripcion+'''",
    fecha = "'''+fecha+'''",
    imagen = "'''+imagen+'''"
    WHERE Identificador = '''+identificador+'''
  ''')
  conexion.commit()
def eliminar():
  identificador = input("Introduce el Identificador a eliminar: ")
  cursor.execute("DELETE FROM piezas WHERE Identificador = "+identificador+";")
  conexion.commit()
