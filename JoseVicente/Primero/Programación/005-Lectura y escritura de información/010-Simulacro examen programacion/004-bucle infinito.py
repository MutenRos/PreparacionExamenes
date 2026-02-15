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
  opcion = input("Introduce la opción escogida: ")
