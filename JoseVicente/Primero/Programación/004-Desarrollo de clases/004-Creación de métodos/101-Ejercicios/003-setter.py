class Gato:
  def __init__(self): # El constructor se llama cuando se instancia el objeto
    self.color = ""   # Una clase tiene propiedades (estáticas)
    self.edad = 0    # La visibilidad por defecto es pública
    self.raza = ""
    self.nombre = ""
    self.color_ojos = ""
  def maulla(self):   # Un método es una acción que realiza el objeto
    return "miau"
  def setEdad(self,nuevaedad):
    self.edad = nuevaedad
    
gato1 = Gato()
print(gato1.maulla())
print("ahora mismo el gato tiene",gato1.edad,"años")
gato1.edad = 1    # Esto no se recomienda
gato1.setEdad(1)  # Esto es mucho más seguro
print("ahora mismo el gato tiene",gato1.edad,"años")
