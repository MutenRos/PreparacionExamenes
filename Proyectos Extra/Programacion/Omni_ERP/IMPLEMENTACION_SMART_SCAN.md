# Implementación de Smart Scan (OCR de Gastos)

Se ha añadido la funcionalidad de **Smart Scan** para digitalización certificada de gastos, una característica destacada de SimpliGest y otros ERPs modernos.

## Cambios Realizados

### 1. Modelos de Datos (`src/dario_app/modules/financial/models.py`)
- **ExpenseReceipt**: Modelo para almacenar tickets y facturas simplificadas.
    - Campos: `image_path`, `merchant`, `date`, `total_amount`, `tax_amount`, `category`, `ocr_raw_data`.
    - Estado: `pending`, `processing`, `verified`, `rejected`.

### 2. Base de Datos (`src/dario_app/database/__init__.py`)
- Registrado el modelo `ExpenseReceipt` en el sistema.

### 3. Lógica de Negocio (`src/dario_app/modules/financial/service.py`)
- Implementado método `process_receipt_image`:
    - Simula un proceso de OCR (Optical Character Recognition).
    - Extrae automáticamente datos (importe, fecha, proveedor) basados en el nombre del archivo o datos simulados.
    - En un entorno real, esto se conectaría a Google Vision API o AWS Textract.

### 4. API (`src/dario_app/modules/financial/routes.py`)
- `POST /api/financial/expenses/upload`: Endpoint para subir imágenes de tickets.
- `GET /api/financial/expenses`: Listar gastos procesados.

### 5. Frontend (`src/dario_app/templates/financial.html`)
- Añadida tarjeta "Smart Scan (Gastos)".
- Botón para subir archivos de imagen.
- Lista de tickets procesados con sus datos extraídos automáticamente.

## Cómo Probar
1. Ir a la sección "Finanzas".
2. En la tarjeta "Smart Scan", seleccionar una imagen (cualquier .jpg/.png).
3. Pulsar "Subir y Escanear".
4. El sistema procesará la imagen y mostrará los datos extraídos (Proveedor, Importe, Categoría) en la lista inferior.
