class Objeto():
  def __init__(self):
    self.x = 0
    self.y = 0
    self.z = 0  

class Roca(Objeto):
  def __init__(self):
    super().__init__()

class Animal(Objeto):
  def __init__(self):
    super().__init__()
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
