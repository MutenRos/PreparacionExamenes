class Gato:
  def __init__(self): # El constructor se llama cuando se instancia el objeto
    self.color = ""   # Una clase tiene propiedades (estáticas)
    self.edad = ""    # La visibilidad por defecto es pública
    self.raza = ""
  def maulla(self):   # Un método es una acción que realiza el objeto
    print("miau")
    
gato1 = Gato()
gato1.color = "naranja"          # Desde fuera puedo escribir la propiedad
print("El gato es de color",gato1.color)  # Desde fuera puedo leer la propiedad
