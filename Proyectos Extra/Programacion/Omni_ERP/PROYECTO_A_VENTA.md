# Conversión de Proyectos a Ventas - OmniERP

## Descripción General

Se ha implementado la funcionalidad de **convertir un Proyecto en una Orden de Venta (Cotización)** en OmniERP. Esto permite que cuando un proyecto está completado o aprobado, pueda ser fácilmente convertido en una venta formal.

## Caso de Uso

### Flujo Típico:

1. **Crear Proyecto** en `project-ops`
   - Definir nombre, cliente, presupuesto
   - Asignar tareas y recursos
   - Establecer cronograma

2. **Ejecutar Proyecto**
   - Registrar horas de trabajo (timesheets)
   - Registrar gastos
   - Completar tareas

3. **Aprobar Actividades**
   - Aprobar timesheets (horas trabajadas)
   - Aprobar gastos incurridos
   - Generar eventos de facturación

4. **Convertir a Venta** ← **NUEVO**
   - Proyecto completado → Click "Convertir a Venta"
   - Sistema crea automáticamente:
     - Cotización (Quote) en módulo de ventas
     - Líneas de cotización (una por tarea del proyecto)
     - Vinculación proyecto↔venta para tracking

## API Endpoint

### Convertir Proyecto a Venta

```http
POST /api/project-ops/projects/{project_id}/convert-to-sale
Content-Type: application/json
Authorization: Bearer {token}
```

#### Parámetros
- `project_id` (path): ID del proyecto a convertir

#### Permisos Requeridos
- `project_ops.convert_to_sale`

#### Respuesta Exitosa (200)

```json
{
  "success": true,
  "project_id": 123,
  "quote_id": 45,
  "quote_number": "PROJ-PRJ-001",
  "message": "Proyecto 'Website Redesign' convertido a cotización de venta #PROJ-PRJ-001",
  "quote": {
    "id": 45,
    "number": "PROJ-PRJ-001",
    "customer": "Acme Corporation",
    "total": 15000.00,
    "items_count": 4
  }
}
```

#### Errores Posibles

```json
{
  "detail": "Cannot convert project with status 'canceled'. Only 'draft', 'active', or 'completed' projects can be converted to sales."
}
```

## Cambios en Base de Datos

### Tabla `proj_projects` - Nuevas Columnas

```sql
ALTER TABLE proj_projects ADD COLUMN converted_to_sale_id INTEGER;
ALTER TABLE proj_projects ADD COLUMN converted_to_sale_number VARCHAR(100);
```

Estas columnas permiten:
- Rastrear qué venta se creó a partir del proyecto
- Verificar si un proyecto ya fue convertido

### Estados del Proyecto Actualizados

```python
Status posibles:
- "draft"              # Borrador
- "active"             # En ejecución
- "completed"          # Completado
- "canceled"           # Cancelado
- "converted_to_sale"  # Convertido a venta (NUEVO)
```

## Lógica de Conversión

Cuando se convierte un proyecto:

### 1. **Validación**
```python
✓ Proyecto debe existir
✓ Estado debe ser: draft, active, o completed
✗ No se puede convertir: canceled, converted_to_sale
```

### 2. **Creación de Cotización**
```python
Cotización:
  - quote_number: "PROJ-{project_code}"
  - customer_id: Del proyecto
  - customer_name: Del proyecto
  - total_amount: Presupuesto del proyecto
  - description: "Convertido del Proyecto: {project.name}"
  - status: "draft"
```

### 3. **Creación de Líneas**
```python
Para cada tarea del proyecto:
  - description: Nombre de la tarea
  - quantity: 1
  - unit_price: Presupuesto / número_de_tareas
  - line_amount: Presupuesto / número_de_tareas
```

### 4. **Actualización de Proyecto**
```python
project.status = "converted_to_sale"
project.converted_to_sale_id = quote.id
project.converted_to_sale_number = quote.quote_number
```

## Ejemplo de Uso (Frontend)

### HTML Button

```html
<button class="btn btn-success" onclick="convertProjectToSale(123)">
  🔄 Convertir a Venta
</button>
```

### JavaScript

```javascript
async function convertProjectToSale(projectId) {
  try {
    const response = await fetch(`/api/project-ops/projects/${projectId}/convert-to-sale`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      }
    });
    
    const data = await response.json();
    
    if (data.success) {
      showSuccessMessage(data.message);
      // Redirigir a la cotización creada
      window.location.href = `/app/ventas/quotes/${data.quote_id}`;
    } else {
      showErrorMessage(data.detail);
    }
  } catch (error) {
    console.error('Error:', error);
    showErrorMessage('Error al convertir proyecto');
  }
}
```

## Beneficios

✅ **Automatización**: No hay que crear manualmente la cotización  
✅ **Precisión**: Los datos se copian automáticamente del proyecto  
✅ **Trazabilidad**: Vinculación proyecto↔venta para auditoría  
✅ **Eficiencia**: Un click para convertir proyectos completados  
✅ **Integración**: Conecta project-ops con ventas automáticamente  

## Consideraciones

### ✓ Lo que se copia:
- Cliente y datos del cliente
- Presupuesto como total de la cotización
- Tareas del proyecto como líneas de cotización
- Fecha y usuario que hace la conversión

### ✗ Lo que NO se copia:
- Timesheets (quedan registrados en el proyecto)
- Gastos (quedan registrados en el proyecto)
- Cambios al cliente (la cotización toma snapshot actual)

### 🔄 El Proyecto:
- Cambia su estado a "converted_to_sale"
- Guarda referencia a la cotización creada
- Permanece intacto (no se elimina)
- Puede ser consultado después

## Próximas Mejoras Potenciales

- [ ] Convertir directamente a Orden de Venta (no solo cotización)
- [ ] Copiar condiciones de pago/términos si están en el proyecto
- [ ] Crear automáticamente items de facturación basados en timesheets
- [ ] Vincular gastos del proyecto a líneas de facturación
- [ ] Auditoría completa: quién, cuándo, qué se convirtió
- [ ] Opción de "reconvertir" si la venta fue rechazada

## Archivos Modificados

1. **`src/dario_app/modules/project_ops/routes.py`**
   - Nuevo endpoint: POST `/api/project-ops/projects/{id}/convert-to-sale`

2. **`src/dario_app/modules/project_ops/service.py`**
   - Nuevo método: `convert_to_sale()`
   - Lógica de validación y conversión

3. **`src/dario_app/modules/project_ops/models.py`**
   - Nuevas columnas en Project: `converted_to_sale_id`, `converted_to_sale_number`

## Permiso Requerido

```python
# Agregar a la lista de permisos del usuario:
"project_ops.convert_to_sale"
```

---

**Versión**: 1.0  
**Fecha**: 26 Diciembre 2024  
**Estado**: ✅ Implementado
