import time

contador = 0

while True:
  print("⬜"*(contador)+"◽"*(10-contador))
  contador += 1
  if contador > 10:
    exit()
  time.sleep(1)
  

