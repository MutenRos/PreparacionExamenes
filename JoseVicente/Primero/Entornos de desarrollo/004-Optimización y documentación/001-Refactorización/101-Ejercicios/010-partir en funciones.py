'''
  Calcular el total de una factura
'''

def totalFactura(baseimponible):
  # Primero me aseguro de que la base imponible sea un número
  baseimponible = float(baseimponible)
  # Ahora quiero redondear a dos digitos
  baseimponible = round(baseimponible,2)
  total = baseimponible
  # Calculamos el IRPF que es el 15%
  irpf = baseimponible*0.15
  irpf = round(irpf,2)
  # ahora calculamos un iva del 21%
  iva = baseimponible*0.21
  iva = round(iva,2)
  # Y ahora el calculo final
  total = baseimponible + iva - irpf
  total = round(total,2)
  return total
  
print(totalFactura(1000))
  
