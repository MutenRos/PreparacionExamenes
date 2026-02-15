'''
  Programa refugio
  (c) 2025 Jose Vicente Carratala
  Este programa gestiona un refugio
'''

class Animal:
  '''
    Clase Animal: define color (str), edad (int) y raza (privada)
  '''
  def __init__(self):
    self.color = ""
    self.edad = 0
    self.__raza = ""

  def setEdad(self, nuevaedad):
    # Solo permite incrementos de 1 en 1
    if self.edad == nuevaedad - 1:
      self.edad += 1
    else:
      print("operación no permitida")

  def getEdad(self):
    return self.edad

  def setRaza(self, nuevaraza):
    self.__raza = str(nuevaraza)

  def getRaza(self):
    return self.__raza

  def descripcion(self):
    return "Edad: " + str(self.edad) + ", Color: " + self.color + ", Raza: " + self.__raza


class Gato(Animal):
  def __init__(self):
    super().__init__()
  def maulla(self):
    print("miau")


class Perro(Animal):
  def __init__(self):
    super().__init__()
  def ladra(self):
    print("guau")


EDAD_MAX_GATO = 25
EDAD_MAX_PERRO = 30

print("Hoy soy Jose Vicente y bienvenido a mi refugio")

perro = Perro()
gato = Gato()

# --- Entrada de datos con validación básica ---
gato.color = input("Introduce el color del gato: ")
perro.color = input("Introduce el color del perro: ")

gato.setRaza(input("Introduce la raza del gato: "))
perro.setRaza(input("Introduce la raza del perro: "))

try:
  gato.edad = int(input("Introduce la edad del gato (entero): "))
except:
  print("Edad del gato inválida, se establece a 0")
  gato.edad = 0

try:
  perro.edad = int(input("Introduce la edad del perro (entero): "))
except:
  print("Edad del perro inválida, se establece a 0")
  perro.edad = 0

# Aserciones: no negativas
assert gato.edad >= 0 and perro.edad >= 0, "hay un error: edad negativa"

# --- Clasificación por edad ---
def clasifica_edad(edad):
  if edad < 1:
    return "cachorro"
  elif edad < 7:
    return "adulto joven"
  else:
    return "adulto"

print("El gato es:", clasifica_edad(gato.edad))
print("El perro es:", clasifica_edad(perro.edad))

# --- Simulación de crecimiento del gato respetando setEdad ---
try:
  edad_maxima = int(input("¿Hasta qué edad quieres simular para el gato? "))
except:
  print("Edad de simulación inválida, se usará la edad actual del gato")
  edad_maxima = gato.edad

if edad_maxima > EDAD_MAX_GATO:
  print("Aviso: superaría EDAD_MAX_GATO, se limitará a", EDAD_MAX_GATO)
  edad_maxima = EDAD_MAX_GATO

edad_actual = gato.getEdad()
# Avanza de uno en uno usando setEdad (desde la siguiente edad)
objetivo = edad_maxima
siguiente = edad_actual + 1
while siguiente <= objetivo:
  gato.setEdad(siguiente)
  print("Gato ahora tiene:", gato.getEdad())
  siguiente += 1

# --- Mostrar descripciones finales ---
print("Ficha del gato:", gato.descripcion())
print("Ficha del perro:", perro.descripcion())

# --- Recorrer propiedades públicas del perro ---
print("Propiedades públicas del perro:")
for clave in perro.__dict__:
  # __raza está name-mangled y no aparecerá como clave simple, mostramos lo visible
  print(clave, ":", perro.__dict__[clave])

