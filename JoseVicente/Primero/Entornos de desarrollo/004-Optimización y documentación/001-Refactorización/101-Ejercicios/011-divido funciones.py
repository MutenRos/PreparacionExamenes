'''
  Calcular el total de una factura
'''

def redondeoa2(entrada):
  return round(entrada,2)

def totalFactura(baseimponible):
  # Primero me aseguro de que la base imponible sea un número
  baseimponible = float(baseimponible)
  # Ahora quiero redondear a dos digitos
  baseimponible = redondeoa2(baseimponible)
  total = baseimponible
  # Calculamos el IRPF que es el 15%
  irpf = baseimponible*0.15
  irpf = redondeoa2(irpf)
  # ahora calculamos un iva del 21%
  iva = baseimponible*0.21
  iva = redondeoa2(irpf)
  # Y ahora el calculo final
  total = baseimponible + iva - irpf
  total = redondeoa2(total)
  return total
  
print(totalFactura(1000))
  
