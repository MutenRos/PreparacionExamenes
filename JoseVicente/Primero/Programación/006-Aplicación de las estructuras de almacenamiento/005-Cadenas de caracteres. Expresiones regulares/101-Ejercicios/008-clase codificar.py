class Codificador():
  def codifica(self,cadena):
    nuevacadena = ""
    for letra in cadena:
      ascii = ord(letra)
      ascii += 5
      nuevaletra = chr(ascii)
      nuevacadena += nuevaletra
    return nuevacadena
  def descodifica(self,cadena):
    nuevacadena = ""
    for letra in cadena:
      ascii = ord(letra)
      ascii -= 5
      nuevaletra = chr(ascii)
      nuevacadena += nuevaletra
    return nuevacadena
    
original = "Jose Vicente"
codificador = Codificador()
codificado = codificador.codifica(original)
descodificado = codificador.descodifica(codificado)

print(original)
print(codificado)
print(descodificado)
