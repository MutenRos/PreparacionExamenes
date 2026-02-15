from PIL import Image

img = Image.open("josevicente.jpeg")
tamanio = img.size
print(tamanio)
pixel = img.getpixel((0, 0))

print(pixel) 
