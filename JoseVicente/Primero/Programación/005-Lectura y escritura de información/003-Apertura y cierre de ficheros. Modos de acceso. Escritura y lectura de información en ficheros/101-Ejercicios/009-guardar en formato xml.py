import xml.etree.ElementTree as ET

clientes = [
    {
        "nombre": "jose Vicente",
        "apellidos": "Carratala Sanchis",
        "email": "info@jocarsa.com"
    },
    {
        "nombre": "Juan",
        "apellidos": "Garcia Lopez",
        "email": "juan@jocarsa.com"
    }
]

root = ET.Element("clientes")

for c in clientes:
    cliente = ET.SubElement(root, "cliente")
    ET.SubElement(cliente, "nombre").text = c["nombre"]
    ET.SubElement(cliente, "apellidos").text = c["apellidos"]
    ET.SubElement(cliente, "email").text = c["email"]

tree = ET.ElementTree(root)
ET.indent(tree, space="  ")
tree.write("clientes.xml", encoding="utf-8", xml_declaration=True)

