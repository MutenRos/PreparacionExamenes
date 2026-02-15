import json
import xml.etree.ElementTree as ET

# -------------------------
# Recursive converter
# -------------------------
def build_xml(key, value):
    element = ET.Element(key)

    if isinstance(value, dict):
        for k, v in value.items():
            element.append(build_xml(k, v))

    elif isinstance(value, list):
        # each item gets the singular tag (simple heuristic)
        item_tag = key[:-1] if key.endswith('s') else "item"
        for item in value:
            element.append(build_xml(item_tag, item))

    else:
        # simple value
        element.text = str(value)

    return element


# -------------------------
# Pretty printing helper
# -------------------------
def indent(elem, level=0):
    spacing = "  "
    i = "\n" + level * spacing
    if len(elem):
        if not elem.text or not elem.text.strip():
            elem.text = i + spacing
        for child in elem:
            indent(child, level + 1)
        if not elem.tail or not elem.tail.strip():
            elem.tail = i
    else:
        if not elem.tail or not elem.tail.strip():
            elem.tail = i


# -------------------------
# Load JSON and convert
# -------------------------
with open("persona.json") as f:
    data = json.load(f)

root_key = next(iter(data))
root = build_xml(root_key, data[root_key])

indent(root)  # pretty print

tree = ET.ElementTree(root)
tree.write("persona.xml", encoding="utf-8", xml_declaration=True)

