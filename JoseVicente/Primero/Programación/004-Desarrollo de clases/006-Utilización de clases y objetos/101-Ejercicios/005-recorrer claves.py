class Cliente:
  def __init__(self,nuevonombre,nuevoemail,nuevadireccion):
    self.nombre = nuevonombre
    self.email = nuevoemail
    self.direccion = nuevadireccion
    
print("Programa clientes por Jose Vicente Carratala")

nombrecliente = input("Introduce el nombre de un cliente: ")
emailcliente = input("Introduce el email de un cliente: ")
direccioncliente = input("Introduce la dirección de un cliente: ")

cliente1 = Cliente(nombrecliente,emailcliente,direccioncliente)

for clave in cliente1.__dict__:
  print("La pieza de información ",clave,"vale: ",cliente1.__dict__[clave])
