from PIL import Image

img = Image.open("josevicente.jpeg")

pixels = img.load()
pixels[0, 0] = (0, 0, 0)

img.save("josevicente2.jpeg")
