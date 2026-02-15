import pickle

archivo = open("cliente.bin",'rb')

mensaje = pickle.load(archivo)
print(mensaje)
archivo.close()
