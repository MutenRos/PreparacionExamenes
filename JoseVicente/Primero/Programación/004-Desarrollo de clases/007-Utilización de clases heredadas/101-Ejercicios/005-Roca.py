class Animal():
  def __init__(self):
    self.color = ""
    self.edad = 0

class Gato(Animal):
  def __init__(self):
    super().__init__()
    
class Perro(Animal):
  def __init__(self):
    super().__init__()
    
gato1 = Gato()
print(gato1.edad)
