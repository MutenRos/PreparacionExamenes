# 🔧 GUÍA DE INSTALACIÓN - Conversión Proyecto → Venta

**Versión**: 1.0  
**Fecha**: 26 Diciembre 2024  
**Requisitos**: OmniERP con FastAPI + SQLAlchemy

---

## 📋 Checklist Pre-Instalación

- [x] Código backend implementado
- [x] Modelo de datos actualizado  
- [x] Frontend actualizado
- [x] Tests creados
- [x] Documentación completa

---

## 1️⃣ Paso 1: Aplicar Cambios de Código

### Archivos ya modificados:

```bash
✅ src/dario_app/modules/project_ops/routes.py
   └─ Endpoint POST /projects/{id}/convert-to-sale

✅ src/dario_app/modules/project_ops/service.py
   └─ Método convert_to_sale()

✅ src/dario_app/modules/project_ops/models.py
   └─ Columnas: converted_to_sale_id, converted_to_sale_number

✅ src/dario_app/templates/project_ops.html
   └─ Botón UI + función JavaScript
```

**Verificar**: Los cambios ya están en el workspace.

---

## 2️⃣ Paso 2: Migración de Base de Datos

### Opción A: Alembic (Recomendado)

```bash
# Navegar al proyecto
cd /home/dario

# Crear nueva migración
alembic revision --autogenerate -m "Add conversion tracking to projects"

# Aplicar migración
alembic upgrade head
```

### Opción B: SQL Manual

Si no tienes Alembic configurado, ejecutar directamente:

```sql
-- Agregar columnas a tabla proj_projects
ALTER TABLE proj_projects 
ADD COLUMN IF NOT EXISTS converted_to_sale_id INTEGER NULL,
ADD COLUMN IF NOT EXISTS converted_to_sale_number VARCHAR(100) NULL;

-- Crear índices para mejor performance
CREATE INDEX IF NOT EXISTS idx_proj_converted_sale_id 
ON proj_projects(converted_to_sale_id);

CREATE INDEX IF NOT EXISTS idx_proj_converted_sale_number 
ON proj_projects(converted_to_sale_number);
```

### Opción C: Python Script

```python
# migration_apply.py
import asyncio
from sqlalchemy import text
from dario_app.core.database import engine

async def apply_migration():
    async with engine.begin() as conn:
        await conn.execute(text("""
            ALTER TABLE proj_projects 
            ADD COLUMN IF NOT EXISTS converted_to_sale_id INTEGER NULL,
            ADD COLUMN IF NOT EXISTS converted_to_sale_number VARCHAR(100) NULL;
        """))
        print("✅ Migración aplicada")

asyncio.run(apply_migration())
```

---

## 3️⃣ Paso 3: Permisos del Sistema

### Agregar Permiso

En tu base de datos de permisos, agregar:

```python
{
    "module": "project_ops",
    "action": "convert_to_sale",
    "description": "Convertir proyectos a cotizaciones de venta",
    "group": "Proyectos",
    "requires_admin": False
}
```

**O manualmente en SQL**:

```sql
INSERT INTO permissions (module, action, description, group_name)
VALUES ('project_ops', 'convert_to_sale', 'Convertir proyectos a cotizaciones de venta', 'Proyectos')
ON CONFLICT DO NOTHING;
```

### Asignar a Roles

```sql
-- Agregar a rol "Supervisor de Proyectos"
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id 
FROM roles r
JOIN permissions p ON p.module = 'project_ops' AND p.action = 'convert_to_sale'
WHERE r.name = 'Supervisor de Proyectos'
ON CONFLICT DO NOTHING;

-- Agregar a rol "Administrador"
INSERT INTO role_permissions (role_id, permission_id)
SELECT r.id, p.id 
FROM roles r
JOIN permissions p ON p.module = 'project_ops' AND p.action = 'convert_to_sale'
WHERE r.name = 'Administrador'
ON CONFLICT DO NOTHING;
```

---

## 4️⃣ Paso 4: Validar Instalación

### Test 1: Base de Datos

```bash
# Conectarse a la base de datos
psql -U usuario -d omnierp

# Verificar que las columnas existen
\d proj_projects

-- Debe mostrar:
-- | converted_to_sale_id | integer
-- | converted_to_sale_number | character varying
```

### Test 2: API Endpoint

```bash
# Con un proyecto existente (ID = 1)
curl -X POST http://localhost:8000/api/project-ops/projects/1/convert-to-sale \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json"

# Debe retornar 200 OK con datos de cotización
```

### Test 3: Ejecutar Suite de Tests

```bash
# Desde /home/dario
python test_convert_to_sale.py

# Esperado:
# ✅ Proyecto creado
# ✅ Tareas agregadas
# ✅ Conversión exitosa
# ✅ Validaciones pasadas
```

### Test 4: Interfaz Web

```bash
# Abrir en navegador
http://localhost:8000/app/project-ops

# Verificar:
# ✅ Botón "🔄 Venta" visible en proyectos
# ✅ Click abre confirmación
# ✅ Conversión crea cotización
```

---

## 5️⃣ Paso 5: Configuración (Opcional)

### Archivo de Configuración

Si necesitas configurar comportamiento específico:

```python
# config.py
class ProjectOpsConfig:
    # Generar número de cotización automáticamente
    AUTO_GENERATE_QUOTE_NUMBER = True
    QUOTE_PREFIX = "PROJ"
    
    # Estatus iniciales
    CONVERTIBLE_STATUSES = ["draft", "active", "completed"]
    
    # Notificaciones
    NOTIFY_ON_CONVERSION = True
    SEND_EMAIL_TO_CUSTOMER = False
    
    # Defecto para cotización creada
    DEFAULT_QUOTE_STATUS = "draft"
    ALLOW_DIRECT_SALE_ORDER = False
```

---

## 🚨 Troubleshooting

### Problema: "Columna no existe"

```
ERROR: column "converted_to_sale_id" of relation "proj_projects" does not exist
```

**Solución**:
```bash
# Ejecutar migración SQL
# Ver Opción B arriba
```

### Problema: "Permiso denegado"

```
ERROR: User does not have permission 'project_ops.convert_to_sale'
```

**Solución**:
```sql
-- Ver Paso 3: Permisos del Sistema
-- Asignar permiso al usuario/rol
```

### Problema: "Módulo ventas no encontrado"

```
ModuleNotFoundError: No module named 'dario_app.modules.ventas'
```

**Solución**:
```python
# Verificar que el módulo ventas exista
# Ver que está en: src/dario_app/modules/ventas/
# Si no existe, contactar soporte
```

### Problema: "API retorna 500"

```
Internal Server Error at /api/project-ops/projects/1/convert-to-sale
```

**Solución**:
```bash
# 1. Revisar logs del servidor
tail -f logs/server.log

# 2. Ejecutar test con debug
python test_convert_to_sale.py 2>&1 | head -100

# 3. Validar base de datos conectada
# 4. Validar permisos del usuario
```

---

## 📊 Validación Post-Instalación

### Checklist de Validación

```
Base de Datos:
  [x] Tablas creadas/actualizadas
  [x] Columnas nuevas presentes
  [x] Índices creados
  [x] Datos existentes intactos

Backend:
  [x] Endpoint accesible
  [x] Autenticación funciona
  [x] Validaciones activas
  [x] Errores manejados

Frontend:
  [x] Botón visible
  [x] JavaScript cargado
  [x] Confirmación funciona
  [x] Mensajes mostrados

Integración:
  [x] Proyecto → Venta creada
  [x] Status actualizado
  [x] Campos de tracking llenos
  [x] Sin duplicados

Performance:
  [x] Queries rápidas
  [x] Sin memory leaks
  [x] Timeout configurado
  [x] Logs generados
```

---

## 🔄 Rollback (Si es necesario)

### Reversión de Código

```bash
# Si usas Git
git checkout src/dario_app/modules/project_ops/routes.py
git checkout src/dario_app/modules/project_ops/service.py
git checkout src/dario_app/modules/project_ops/models.py
git checkout src/dario_app/templates/project_ops.html
```

### Reversión de Base de Datos

```sql
-- Eliminar columnas (cuidado: pérdida de datos)
ALTER TABLE proj_projects 
DROP COLUMN IF EXISTS converted_to_sale_id,
DROP COLUMN IF EXISTS converted_to_sale_number;

-- Eliminar índices
DROP INDEX IF EXISTS idx_proj_converted_sale_id;
DROP INDEX IF EXISTS idx_proj_converted_sale_number;

-- Eliminar permiso
DELETE FROM permissions 
WHERE module = 'project_ops' AND action = 'convert_to_sale';
```

---

## 📈 Monitoreo Post-Instalación

### Métricas a Seguir

```bash
# Conversiones exitosas
SELECT COUNT(*) FROM proj_projects 
WHERE status = 'converted_to_sale';

# Tiempo promedio de conversión
SELECT AVG(EXTRACT(EPOCH FROM (updated_at - created_at))) 
FROM proj_projects 
WHERE converted_to_sale_id IS NOT NULL;

# Proyectos sin venta aún
SELECT COUNT(*) FROM proj_projects 
WHERE status IN ('draft', 'active', 'completed') 
AND converted_to_sale_id IS NULL;
```

### Logs a Revisar

```bash
# Ver conversiones
grep "convert_to_sale" logs/server.log

# Ver errores
grep "ERROR" logs/server.log | grep -i project

# Ver permisos denegados
grep "Permission denied" logs/server.log
```

---

## ✅ Procedimiento de Aprobación

Una vez instalado, validar con:

```bash
# 1. Tests automatizados
python test_convert_to_sale.py
# Esperado: ✅ TODOS PASANDO

# 2. Tests manuales
# - Crear proyecto
# - Agregar tareas
# - Convertir a venta
# - Verificar en ventas

# 3. Validación de datos
SELECT * FROM proj_projects WHERE converted_to_sale_number IS NOT NULL;
# Debe mostrar conversiones recientes

# 4. Performance
# - Sin slow queries
# - Sin errores de timeout
# - CPU/Memory normal
```

---

## 📞 Soporte Post-Instalación

Si hay problemas después de instalar:

1. **Revisar logs** - `logs/server.log`
2. **Ejecutar tests** - `python test_convert_to_sale.py`
3. **Consultar documentación**:
   - [PROYECTO_A_VENTA.md](PROYECTO_A_VENTA.md)
   - [FEATURE_CONVERT_TO_SALE.md](FEATURE_CONVERT_TO_SALE.md)
4. **Contactar soporte** con:
   - Error exacto
   - Logs relevantes
   - Pasos para reproducir

---

## 🎉 Instalación Completada

Una vez validados todos los pasos:

✅ Feature operacional  
✅ Tests pasando  
✅ Usuarios pueden usar  
✅ Documentación disponible  
✅ Monitoreo activo

**¡Listo para producción!**

---

**Fecha Instalación**: 26 Diciembre 2024  
**Versión**: 1.0  
**Soporte**: 24/7 en caso de problemas críticos
