'''
  Calcular el total de una factura
'''

def redondeoa2(entrada):
  return round(entrada,2)
  
def calculaIVA(entrada):
  iva = entrada*0.21
  return redondeoa2(iva)
  
def calculaIRPF(entrada):
  irpf = entrada*0.15
  return redondeoa2(irpf)

def totalFactura(baseimponible):
  baseimponible = float(baseimponible)
  baseimponible = redondeoa2(baseimponible)
  
  
  total = baseimponible + calculaIVA(baseimponible) - calculaIRPF(baseimponible)
  total = redondeoa2(total)
  return total
  
print(totalFactura(1000))
  
