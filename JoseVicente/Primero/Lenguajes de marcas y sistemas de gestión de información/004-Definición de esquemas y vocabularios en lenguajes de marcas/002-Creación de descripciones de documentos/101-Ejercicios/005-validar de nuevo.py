import xmlschema

esquema = xmlschema.XMLSchema("002-plantilla.xsd")

try:
    esquema.validate("004-documento no valido.xml")
    print("✔️ XML válido")
except xmlschema.exceptions.XMLSchemaValueError as e:
    print("❌ XML NO válido")
    print(e)

