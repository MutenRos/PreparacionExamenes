cadena = input("Introduce algo de texto: ")

# Recorro la cadena
nuevacadena = ""
for letra in cadena:
  ascii = ord(letra)
  ascii -= 5
  nuevaletra = chr(ascii)
  nuevacadena += nuevaletra
  
print(nuevacadena)
