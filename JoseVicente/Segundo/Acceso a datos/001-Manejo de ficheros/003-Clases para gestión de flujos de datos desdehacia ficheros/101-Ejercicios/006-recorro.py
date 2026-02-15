from PIL import Image

img = Image.open("josevicente.jpeg")
tamanio = img.size
for x in range(0,tamanio[0]):
  for y in range(0,tamanio[1]):
    pixel = img.getpixel((x, y))
    print(pixel) 
