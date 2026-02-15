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
    if self.edad == nuevaedad - 1:
      self.edad = nuevaedad
    else:
      print("operación no permitida")
    
gato1 = Gato()
print(gato1.maulla())
print("ahora mismo el gato tiene",gato1.edad,"años")
gato1.setEdad(5)  # Esto es mucho más seguro
print("ahora mismo el gato tiene",gato1.edad,"años")
