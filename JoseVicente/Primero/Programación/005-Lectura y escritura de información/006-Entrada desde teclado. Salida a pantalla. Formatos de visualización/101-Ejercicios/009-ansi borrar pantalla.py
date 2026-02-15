import time

contador = 0

while True:
  print("\033[2J")  # Borrar pantalla
  print("⬜"*(contador)+"◽"*(10-contador))
  contador += 1
  if contador > 10:
    exit()
  time.sleep(1)
  

