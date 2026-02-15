import json

clientes = [
  {
    "nombre":"jose Vicente",
    "apellidos":"Carratala Sanchis",
    "email":"info@jocarsa.com"
  },
  {
    "nombre":"Juan",
    "apellidos":"Garcia Lopez",
    "email":"juan@jocarsa.com"
  }
]

archivo = open("clientes.json","w")

json.dump(clientes, archivo, indent=4, ensure_ascii=False)

