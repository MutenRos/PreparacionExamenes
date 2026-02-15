import pickle

mensaje = "esto es un mensaje"
archivo = open("cliente.bin",'wb')

pickle.dump(mensaje, archivo)
archivo.close()
