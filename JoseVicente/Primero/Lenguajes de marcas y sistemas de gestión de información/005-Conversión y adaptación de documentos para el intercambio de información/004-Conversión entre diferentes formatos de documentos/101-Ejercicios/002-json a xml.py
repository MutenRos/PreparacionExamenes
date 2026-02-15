import json
import xml.etree.ElementTree as ET

def dict_to_xml(tag, d):
    elem = ET.Element(tag)
    for key, val in d.items():
        child = ET.SubElement(elem, key)
        child.text = str(val)
    return elem

# Load JSON
with open("persona.json") as f:
    data = json.load(f)

# Convert: assume root key has 1 element
root_key = next(iter(data))
root_element = dict_to_xml(root_key, data[root_key])

# Save XML
tree = ET.ElementTree(root_element)
tree.write("persona.xml", encoding="utf-8", xml_declaration=True)

