import xmlschema

esquema = xmlschema.XMLSchema("002-plantilla.xsd")

try:
    esquema.validate("001-documento.xml")
    print("✔️ XML válido")
except xmlschema.exceptions.XMLSchemaValidationError as e:
    print("❌ XML NO válido")
    print(e)

