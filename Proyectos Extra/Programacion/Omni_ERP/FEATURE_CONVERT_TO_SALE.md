# ✅ FEATURE: Conversión de Proyectos a Ventas - IMPLEMENTADO

**Fecha**: 26 Diciembre 2024  
**Estado**: ✅ COMPLETADO Y FUNCIONAL  
**Versión**: 1.0

---

## 🎯 Objetivo

Permitir que proyectos completados o aprobados en el módulo `project-ops` se conviertan automáticamente en cotizaciones de venta en el módulo `ventas`, eliminando la necesidad de crear manualmente las ventas.

## 🚀 Lo Que Se Implementó

### 1. **Backend - API Endpoint**

```http
POST /api/project-ops/projects/{project_id}/convert-to-sale
```

**Ubicación**: [src/dario_app/modules/project_ops/routes.py](src/dario_app/modules/project_ops/routes.py#L220-L240)

**Características**:
- ✅ Autenticación requerida
- ✅ Permiso necesario: `project_ops.convert_to_sale`
- ✅ Multi-tenant (aislamiento por organización)
- ✅ Validación de estado del proyecto
- ✅ Respuesta estructurada con detalles de la cotización creada

### 2. **Backend - Lógica de Negocio**

**Ubicación**: [src/dario_app/modules/project_ops/service.py](src/dario_app/modules/project_ops/service.py#L150-L180)

**Método**: `ProjectOpsService.convert_to_sale()`

**Flujo**:
1. Valida que el proyecto existe
2. Verifica estado (debe ser: draft, active, o completed)
3. Rechaza estados: canceled, converted_to_sale
4. Obtiene todas las tareas del proyecto
5. Crea `VentaQuote` (cotización) con:
   - Cliente del proyecto
   - Presupuesto como total
   - Descripción automática
   - Status = "draft"
6. Crea `VentaQuoteItem` por cada tarea (línea de cotización)
7. Actualiza proyecto:
   - Status → "converted_to_sale"
   - Vincula con la venta creada
8. Retorna respuesta con detalles

### 3. **Base de Datos - Modelo**

**Ubicación**: [src/dario_app/modules/project_ops/models.py](src/dario_app/modules/project_ops/models.py#L35-L36)

**Nuevas Columnas en Tabla `proj_projects`**:

```python
converted_to_sale_id: Mapped[Optional[int]]
    # Referencia al ID de la cotización creada
    
converted_to_sale_number: Mapped[Optional[str]]
    # Número de cotización (ej: "PROJ-PRJ-001")
```

**SQL Equivalente**:
```sql
ALTER TABLE proj_projects 
    ADD COLUMN converted_to_sale_id INTEGER NULL,
    ADD COLUMN converted_to_sale_number VARCHAR(100) NULL;
```

### 4. **Frontend - UI**

**Ubicación**: [src/dario_app/templates/project_ops.html](src/dario_app/templates/project_ops.html#L575-L590)

**Cambios**:
- ✅ Botón "🔄 Venta" en cada proyecto (visible solo si es convertible)
- ✅ Se muestra solo para proyectos en estado: draft, active, completed
- ✅ Deshabilitado para proyectos: canceled, converted_to_sale
- ✅ Click-stop para no expandir la fila al hacer clic
- ✅ Confirmación de diálogo antes de convertir
- ✅ Mensajes de éxito/error al usuario

**Función JavaScript**: `convertProjectToSale(projectId)`

```javascript
async function convertProjectToSale(projectId) {
    // Valida estado del proyecto
    // Solicita confirmación
    // Llama al endpoint
    // Muestra resultado (número de cotización)
    // Recarga lista de proyectos
}
```

### 5. **Integración Cross-Module**

**Patrón Implementado**: Importación dinámica para evitar dependencias circulares

```python
# En service.py
from dario_app.modules.ventas.models import VentaQuote, VentaQuoteItem

# En moment de conversión:
quote = VentaQuote(
    quote_number="PROJ-" + project.project_code,
    customer_id=project.customer_id,
    customer_name=project.customer_name,
    total_amount=project.budget_amount,
    description=f"Convertido del Proyecto: {project.name}",
    status="draft",
    organization_id=organization_id
)
```

---

## 📊 Flujo de Uso

### Escenario: Proyecto completado que se vuelve venta

```
1. CREAR PROYECTO
   └─ Status: draft
   └─ Presupuesto: €15,000
   └─ Cliente: Acme Corp

2. AGREGAR TAREAS
   ├─ Análisis (€3,750)
   ├─ Diseño (€3,750)
   ├─ Desarrollo (€5,000)
   └─ Testing (€2,500)

3. EJECUTAR PROYECTO
   ├─ Registrar timesheets
   ├─ Registrar gastos
   └─ Status: completed

4. CONVERTIR A VENTA ← AQUÍ
   │
   ├─ Click "🔄 Venta"
   ├─ Confirmación
   │
   └─ Sistema crea:
      ├─ Cotización #PROJ-PRJ-001
      ├─ 4 líneas (una por tarea)
      ├─ Total €15,000
      └─ Status: draft (lista para editar)

5. PROYECTO ACTUALIZADO
   └─ Status: converted_to_sale
   └─ Vinculado con Venta #PROJ-PRJ-001
```

---

## 🔧 Ejemplo de Respuesta API

### ✅ Éxito (200)

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

### ❌ Error - Proyecto Cancelado

```json
{
  "detail": "Cannot convert project with status 'canceled'. Only 'draft', 'active', or 'completed' projects can be converted to sales."
}
```

### ❌ Error - No Encontrado

```json
{
  "detail": "Project not found"
}
```

---

## 🧪 Testing

### Ejecutar Test Suite

```bash
# Desde el directorio /home/dario
python test_convert_to_sale.py
```

**Test que ejecuta**:
1. ✅ Crear proyecto
2. ✅ Agregar múltiples tareas
3. ✅ Convertir a venta exitosamente
4. ✅ Validar que proyecto está marcado como "converted_to_sale"
5. ✅ Intentar convertir nuevamente (validar rechazo)
6. ✅ Casos de error (proyecto cancelado)

---

## 📋 Checklist de Implementación

### Backend
- [x] Endpoint API creado y documentado
- [x] Lógica de servicio implementada
- [x] Validaciones de estado
- [x] Modelo de datos actualizado
- [x] Manejo de errores
- [x] Integración cross-module (ventas)
- [x] Multi-tenant soportado
- [x] Autenticación y permisos

### Database
- [x] Nuevas columnas en Project
- [x] Script SQL de migración
- [x] Valores por defecto configurados
- [x] Índices si es necesario

### Frontend
- [x] Botón UI agregado
- [x] Lógica JavaScript implementada
- [x] Confirmación de diálogo
- [x] Mensajes de éxito/error
- [x] Recarga de datos después de conversión
- [x] Validación de estado visible

### Testing
- [x] Test script creado
- [x] Casos de éxito cubiertos
- [x] Casos de error cubiertos
- [x] Validaciones de respuesta

### Documentación
- [x] Guía técnica creada ([PROYECTO_A_VENTA.md](PROYECTO_A_VENTA.md))
- [x] Respuesta API documentada
- [x] Casos de uso explicados
- [x] Cambios de estado documentados

---

## 🔐 Seguridad

### Autenticación & Autorización
```python
# Requerido en endpoint
@router.post("/projects/{project_id}/convert-to-sale")
async def convert_to_sale(
    project_id: int,
    session: AsyncSession = Depends(get_tenant_db),
    org_id: int = Depends(get_org_id),
    # Permiso requerido ↓
    _: None = Depends(require_permission("project_ops.convert_to_sale"))
):
    ...
```

### Aislamiento de Datos
- ✅ Validación de `organization_id` en todas las queries
- ✅ Proyecto y venta creada en la misma organización
- ✅ No se puede acceder a datos de otra organización

---

## 🎓 Próximas Mejoras Potenciales

### Fase 2
- [ ] Convertir directamente a **Orden de Venta** (sin pasar por cotización)
- [ ] Opción de incluir **timesheets** como líneas de venta
- [ ] Copiar **términos de pago** si existen en proyecto
- [ ] Notificación automática al cliente vía email

### Fase 3
- [ ] Historial de conversiones (quién, cuándo, qué se convirtió)
- [ ] Opción de "reconvertir" si la venta fue rechazada
- [ ] Vinculación bidireccional (venta → proyecto)
- [ ] Dashboard de conversiones exitosas

---

## 📁 Archivos Modificados

| Archivo | Cambio | Líneas |
|---------|--------|--------|
| `routes.py` | Nuevo endpoint POST | 220-240 |
| `service.py` | Nuevo método convert_to_sale() | 150-180 |
| `models.py` | 2 nuevas columnas en Project | 35-36 |
| `project_ops.html` | Botón + función JavaScript | 575-590, 810-835 |

---

## 🔗 Referencias Relacionadas

- **Módulo Ventas**: `/home/dario/src/dario_app/modules/ventas/`
- **Módulo Project-Ops**: `/home/dario/src/dario_app/modules/project_ops/`
- **Documentación Técnica**: [PROYECTO_A_VENTA.md](PROYECTO_A_VENTA.md)
- **Test Script**: [test_convert_to_sale.py](test_convert_to_sale.py)

---

## ✨ Conclusión

La funcionalidad **"Convertir Proyectos a Ventas"** está **completamente implementada** y lista para usar. 

**Beneficios**:
- ⚡ Una sola acción convierte proyecto en cotización
- 📊 Automación del flujo proyecto → venta
- 🔗 Trazabilidad completa de conversión
- ✅ Multi-tenant seguro
- 📱 Interfaz intuitiva

**El sistema ahora responde**: "Sí, hay manera de convertir un proyecto en una venta" 🎉

---

**Estado**: ✅ **IMPLEMENTADO Y FUNCIONAL**  
**Prueba**: Ejecutar `python test_convert_to_sale.py`  
**Documentación**: Ver [PROYECTO_A_VENTA.md](PROYECTO_A_VENTA.md)
