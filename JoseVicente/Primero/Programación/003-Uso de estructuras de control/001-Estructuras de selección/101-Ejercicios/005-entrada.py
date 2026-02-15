print("Clasificador incómodo por edades")
edad = input("Introduce tu edad: ")         # Por defecto devuelve string
edad = int(edad)

if edad < 10:
  print("Eres un niño!")
elif edad >= 10 and edad < 20:
  print("Eres un adolescente")
elif edad >= 20 and edad < 30:
  print("Eres un joven")
else:
  print("Ya no eres un joven")
