class Gato:

  def __init__(self,nuevocolor): # El constructor se llama cuando se instancia el objeto
    self.color = nuevocolor   # Una clase tiene propiedades (estáticas)
    self.edad = 0    # La visibilidad por defecto es pública
    
  def maulla(self):   # Un método es una acción que realiza el objeto
    return "miau"
    
  def setEdad(self,nuevaedad):
    if self.edad == nuevaedad - 1:
      self.edad = nuevaedad
    else:
      print("operación no permitida")
      
  def getEdad(self):
    return self.edad
    
gato1 = Gato("naranja")       # La edad no tiene sentido si cubrimos el nacimiento de un gato
gato2 = Gato("negro")       # La edad no tiene sentido si cubrimos el nacimiento de un gato

