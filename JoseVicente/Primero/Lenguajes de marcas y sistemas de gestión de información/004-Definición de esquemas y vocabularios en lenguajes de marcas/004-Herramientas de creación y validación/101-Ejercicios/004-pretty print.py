import xml.etree.ElementTree as ET
from xml.dom import minidom

# Fichero XSD
xsd_file = "schema/esquema.xsd"
# Fichero de salida XML
output_file = "persona.xml"

# Namespace de XML Schema
XS = "{http://www.w3.org/2001/XMLSchema}"

# Cargar XSD
tree = ET.parse(xsd_file)
root = tree.getroot()

fields = []

# Buscar el elemento <xs:element name="persona">
for element in root.findall(f"{XS}element"):
    if element.get("name") == "persona":
        complex_type = element.find(f"{XS}complexType")
        if complex_type is None:
            continue

        sequence = complex_type.find(f"{XS}sequence")
        if sequence is None:
            continue

        # Obtener los nombres de los hijos de persona
        for child in sequence.findall(f"{XS}element"):
            fields.append(child.get("name"))

# Pedir los valores por consola
entradas = []
for campo in fields:
    valor = input(f"Introduce el valor para {campo}: ")
    entradas.append(valor)

# Construir el XML de instancia
persona = ET.Element("persona")

for campo, valor in zip(fields, entradas):
    hijo = ET.SubElement(persona, campo)
    hijo.text = valor

# Pretty print con minidom
rough_string = ET.tostring(persona, 'utf-8')
reparsed = minidom.parseString(rough_string)
pretty_xml = reparsed.toprettyxml(indent="  ", encoding="utf-8")

# Guardar archivo
with open(output_file, "wb") as f:
    f.write(pretty_xml)

print(f"XML formateado guardado en {output_file}")

