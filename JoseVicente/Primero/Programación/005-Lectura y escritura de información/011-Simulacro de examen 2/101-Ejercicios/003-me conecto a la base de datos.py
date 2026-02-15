import mysql.connector

conexion = mysql.connector.connect(
  host="localhost",
  user="portafolio",
  password="portafolio",
  database="portafolio"
)

print("Gestion de portafolio v0.1")
print("Escoge una opcion")
print("1.-Insertar")
print("2.-Listar")
print("3.-Actualizar")
print("4.-Eliminar")
opcion = int(input("Escoge una opcion: "))
print("La opción que has escogido es: ",opcion)

cursor = conexion.cursor() 
cursor.execute("SELECT * FROM piezas;")

lineas = cursor.fetchall()
for linea in lineas:
  print(linea)
