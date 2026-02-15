import xml.etree.ElementTree as ET

xsd_file = "schema/esquema.xsd"   

tree = ET.parse(xsd_file)
root = tree.getroot()

XS = "{http://www.w3.org/2001/XMLSchema}"

fields = []

for element in root.findall(f"{XS}element"):
    if element.get("name") == "persona":
        complex_type = element.find(f"{XS}complexType")
        sequence = complex_type.find(f"{XS}sequence")

        for child in sequence.findall(f"{XS}element"):
            fields.append(child.get("name"))

print("Campos de <persona>:", fields)

