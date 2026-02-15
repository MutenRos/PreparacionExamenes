class Gato:
  def __init__(self): # El constructor se llama cuando se instancia el objeto
    self.color = ""   # Una clase tiene propiedades (estáticas)
    self.edad = ""
    self.raza = ""
  def maulla(self):   # Un método es una acción que realiza el objeto
    print("miau")
    
gato1 = Gato()
print(gato1)
gato1.maulla()
