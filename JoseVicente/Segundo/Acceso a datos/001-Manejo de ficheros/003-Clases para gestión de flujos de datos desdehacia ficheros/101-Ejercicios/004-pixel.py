from PIL import Image

img = Image.open("josevicente.jpeg")

pixel = img.getpixel((0, 0))

print(pixel) 
