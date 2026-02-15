archivo = open("clientes.txt","rb")
linea = archivo.readline()
print(linea.decode("utf-8"))
archivo.close()
