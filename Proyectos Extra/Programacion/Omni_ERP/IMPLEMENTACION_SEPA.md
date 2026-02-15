# Implementación de Remesas SEPA (Direct Debit)

Se ha añadido la funcionalidad completa para gestionar remesas bancarias SEPA (ISO 20022), una característica clave para competir con Holded.

## Cambios Realizados

### 1. Modelos de Datos (`src/dario_app/modules/financial/models.py`)
- **SEPARemittance**: Cabecera de la remesa (ID, fecha ejecución, esquema, estado, XML generado).
- **SEPARemittanceLine**: Líneas de la remesa (Deudor, IBAN, Importe, Mandato).
- Actualizado `BankAccount` para incluir soporte de SWIFT/BIC si no existía explícitamente.

### 2. Base de Datos (`src/dario_app/database/__init__.py`)
- Registrados los nuevos modelos en `create_tenant_db` y `init_db` para asegurar que se crean las tablas y se detectan en migraciones.

### 3. Lógica de Negocio (`src/dario_app/modules/financial/service.py`)
- Implementado método `generate_sepa_xml` que genera el fichero XML estándar ISO 20022 (pain.008.001.02).
- Soporte para esquemas CORE y B2B.

### 4. API (`src/dario_app/modules/financial/routes.py`)
- `POST /api/financial/sepa/remittances`: Crear nueva remesa con líneas.
- `GET /api/financial/sepa/remittances`: Listar remesas.
- `POST /api/financial/sepa/remittances/{id}/generate-xml`: Generar y guardar el XML.

### 5. Frontend (`src/dario_app/templates/financial.html`)
- Añadida nueva tarjeta "Remesas SEPA" en el módulo financiero.
- Interfaz para crear remesas manualmente (añadir líneas, seleccionar banco y fecha).
- Visualización de remesas creadas y descarga/visualización del XML generado.

## Cómo Probar
1. Ir a la sección "Finanzas".
2. En la tarjeta "Remesas SEPA", introducir ID de cuenta bancaria y fecha.
3. Añadir líneas con deudor, IBAN e importe.
4. Crear remesa.
5. Pulsar "Generar XML" para obtener el fichero listo para subir al banco.
