class Gato:

  def __init__(self,nuevocolor,nuevaedad): # El constructor se llama cuando se instancia el objeto
    self.color = nuevocolor   # Una clase tiene propiedades (estáticas)
    self.edad = nuevaedad    # La visibilidad por defecto es pública
    
  def maulla(self):   # Un método es una acción que realiza el objeto
    return "miau"
    
  def setEdad(self,nuevaedad):
    if self.edad == nuevaedad - 1:
      self.edad = nuevaedad
    else:
      print("operación no permitida")
      
  def getEdad(self):
    return self.edad
    
gato1 = Gato("naranja",0)       # La edad no tiene sentido si cubrimos el nacimiento de un gato

