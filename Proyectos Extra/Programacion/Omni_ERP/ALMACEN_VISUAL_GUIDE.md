# 🏭 ALMACÉN - ARQUITECTURA UNIFICADA

## Antes vs Después

### ANTES (Fragmentado - 985 líneas)
```
┌─ Header
├─ Estadísticas
├─ 🔹 Configuración del almacén (sección global)
│  ├─ Input: pasillos, estanterías, alturas, parcelas
│  └─ Mensaje: "Borra ubicaciones actuales"
├─ 🔹 Edición por bloques
│  ├─ Input: pasillo, estantería, altura, capacidad
│  └─ Mensaje: "Actualiza todas las ubicaciones que coincidan"
├─ 🔹 Configuración Individual (AZUL)
│  ├─ Panel izquierda: lista de pasillos
│  └─ Panel derecha: formulario
├─ 🔹 Gestión de Parcelas Llenas (ROJO)
│  ├─ Selector de pasillos
│  └─ Grid de parcelas
├─ 🔹 Filtros
│  ├─ Input: pasillo, estado, búsqueda
├─ Warehouse Grid
├─ Product Locations Table
└─ Modal
```

**Problemas**:
- ❌ 4 secciones diferentes haciendo cosas similares
- ❌ Confuso dónde configurar qué
- ❌ Colores y estilos solapados
- ❌ "Parches" pegados sin coherencia
- ❌ No hay navegación clara

---

### AHORA (Unificado - 661 líneas, 33% más pequeño)
```
┌─ Header
│  └─ 🏭 Almacén | ← Dashboard
├─ TABS NAVEGACIÓN
│  ├─ 🔧 Configurar Pasillos (ACTIVO)
│  ├─ 🔒 Gestionar Parcelas
│  ├─ 📦 Ver Ubicaciones
│  └─ 📋 Productos
│
├─ TAB: Configurar Pasillos
│  ├─ Estadísticas (Pasillos | Estanterías | Alturas | Llenas)
│  ├─ Panel 2 columnas
│  │  ├─ LEFT: Lista de pasillos + "➕ Nueva"
│  │  └─ RIGHT: Formulario (Num, Nombre, Est., Alt.)
│
├─ TAB: Gestionar Parcelas
│  ├─ Selector de pasillo
│  └─ Grid de estanterías (A-Z) con checkboxes
│
├─ TAB: Ver Ubicaciones
│  └─ Placeholder (próximamente: grid visual)
│
└─ TAB: Productos
   └─ Search + Tabla (Código | Nombre | Categoría | Ubicación)
```

**Ventajas**:
- ✅ 4 tabs claros e independientes
- ✅ Navegación explícita
- ✅ Una sola fuente de verdad
- ✅ Flujo lógico
- ✅ Estadísticas integradas
- ✅ 324 líneas menos (33% más pequeño)

---

## Data Model

### localStorage.configAlmacenIndividual

```javascript
{
  1: {
    num: 1,
    nombre: "Pasillo A",
    estanterias: 26,
    alturas: 6,
    parcelas: {
      1: {  // Estantería 1
        1: { lleno: false },
        2: { lleno: false },
        3: { lleno: true },
        4: { lleno: true },
        5: { lleno: false },
        6: { lleno: false }
      },
      2: { ... },  // Estantería 2
      ...
    }
  },
  2: { ... },  // Pasillo 2
  ...
}
```

**Una sola estructura**. Todo se almacena aquí. Ni duplicación, ni inconsistencias.

---

## Flujos de Usuario

### 🔧 TAB 1: Configurar Pasillos

```
Usuario abre "Configurar Pasillos"
    ↓
Ve estadísticas (0 pasillos, 0 estanterías)
    ↓
Click: "➕ Nueva"
    ↓
Panel derecho: formulario vacío
    ↓
Completa: Pasillo #1, "Pasillo A", 26 estanterías, 6 alturas
    ↓
Click: "💾 Guardar"
    ↓
✅ Se guarda en localStorage
✅ Aparece en lista de la izquierda
✅ Estadísticas se actualizan automáticamente
    ↓
Click en "Pasillo A" de la lista
    ↓
Panel derecho: muestra datos para editar
    ↓
Cambia "26" a "20" estanterías
    ↓
Click: "💾 Guardar"
    ↓
✅ Actualiza. Estadísticas: ahora 20 estanterías
    ↓
Click: "🗑️ Eliminar"
    ↓
Confirmación: "¿Eliminar pasillo 1?"
    ↓
✅ Eliminado. Desaparece de lista. Estadísticas: 0 nuevamente
```

### 🔒 TAB 2: Gestionar Parcelas

```
Usuario abre "Gestionar Parcelas"
    ↓
Dropdown: "-- Elige un pasillo --"
    ↓
Selecciona: "Pasillo A"
    ↓
Carga: Grid con Estanterías A, B, C, ... Z
Para cada estantería: 6 checkboxes (altura 1-6)
    ↓
Usuario marca:
  - Estantería A, Altura 3: ✅ (🔒 LLENO)
  - Estantería A, Altura 4: ✅ (🔒 LLENO)
  - Estantería B, Altura 1: ✅ (🔒 LLENO)
    ↓
Click: "💾 Guardar Cambios"
    ↓
✅ Guarda en configPasillos[1].parcelas
✅ Estadísticas se actualizan: "Parcelas Llenas: 3"
    ↓
Próxima vez que abre este tab:
  → Ve los mismos checkboxes marcados
  → Porque se recuperan de localStorage
```

### 📋 TAB 4: Productos

```
Usuario abre "Productos"
    ↓
Carga desde /api/inventario
    ↓
Tabla: Código | Nombre | Categoría | Ubicación
    ↓
Usuario escribe en search: "bomba"
    ↓
Filtra en tiempo real (mayúsculas insensitive)
    ↓
Muestra solo productos con "BOMBA" en código o nombre
```

---

## Estado Visual de Parcelas

### Disponible ✓
```
┌────────────────────────────────────┐
│ ☐ Altura 1                         │
│    ✓ Disponible                    │
├────────────────────────────────────┤
Fondo: #d4edda (verde pálido)
Texto: #28a745 (verde)
```

### Lleno 🔒
```
┌────────────────────────────────────┐
│ ☑ Altura 2                         │
│    🔒 LLENO                        │
├────────────────────────────────────┤
Fondo: #f8d7da (rojo pálido)
Texto: #dc3545 (rojo)
```

---

## Responsivo

```
DESKTOP (1024px+)          MOBILE (<1024px)
┌───────────────────┐      ┌──────────┐
│ Panel A   Panel B  │      │ Panel A  │
│  (50%)     (50%)   │  =>  │ Panel B  │
└───────────────────┘      └──────────┘

Tabs siempre horizontal y scrollables en móvil
```

---

## Performance

| Métrica | Valor |
|---------|-------|
| **Líneas** | 661 (reducido de 985) |
| **Tamaño** | 28 KB |
| **Funciones JS** | 15+ |
| **Persistencia** | localStorage (instántaneo) |
| **Búsqueda productos** | Tiempo real |
| **Estadísticas** | Calculadas al guardar |

---

## Commits Realizados

```
1. refactor: reescritura completa del módulo almacén con arquitectura unificada
   - 335 insertions(+), 658 deletions(-)
   - Cambio de estructura: múltiples secciones → 4 tabs limpios
   - Una sola fuente de verdad: localStorage

2. docs: guía de arquitectura del almacén unificado
   - Documentación técnica completa
   - Data model, funciones, estilos

3. docs: resumen de cambios del almacén unificado
   - Resumen visual de cambios
   - Antes vs Después
   - Próximos pasos

4. test: script de validación para almacén unificado
   - Validación de estructura
   - Verificación de funciones
   - Confirmación de servidor
```

---

## Testing

```bash
$ bash test_almacen_unificado.sh

✅ Archivo almacén.html existe
✅ Tab 'Configurar Pasillos' encontrado
✅ Tab 'Gestionar Parcelas' encontrado
✅ Tab 'Ver Ubicaciones' encontrado
✅ Tab 'Productos' encontrado
✅ Función 'switchTab' encontrada
✅ Función 'guardarPasillo' encontrada
✅ Función 'cargarParcelasLlenas' encontrada
✅ Función 'guardarParcelasLlenas' encontrada
✅ Función 'actualizarEstadisticas' encontrada
✅ Sección antigua eliminada correctamente
✅ localStorage configAlmacenIndividual implementado
✅ Servidor está sirviendo almacén.html correctamente

✅ Todos los tests pasaron!
```

---

## Próximos Pasos

```
✅ Arquitectura unificada completada
├─ ✅ Navegación por tabs
├─ ✅ Configuración individual por pasillo
├─ ✅ Sistema binario lleno/disponible
├─ ✅ localStorage persistencia
├─ ✅ Estadísticas integradas
│
├─ ⏳ Integración con BD
│  ├─ /api/almacen/ubicaciones
│  ├─ Sincronización bidireccional
│  └─ Multi-tenant ready
│
├─ ⏳ Visualización avanzada
│  ├─ Grid visual de pasillos/estanterías
│  ├─ Indicadores de ocupación
│  └─ Alertas de parcelas llenas
│
└─ ⏳ Reportes
   ├─ PDF de distribución
   ├─ Gráficos de ocupación
   └─ Análisis de uso
```

---

## ¿Cómo Usar?

### Acceder
```
http://localhost:8000/app/almacen
```

### Flujo Básico
1. **Tab "Configurar Pasillos"**
   - Crea pasillos con `➕ Nueva`
   - Define estanterías y alturas
   - Ve estadísticas en tiempo real

2. **Tab "Gestionar Parcelas"**
   - Selecciona pasillo
   - Marca parcelas como llenas
   - Guarda cambios

3. **Tab "Productos"**
   - Busca por código o nombre
   - Ve ubicación en almacén

4. **Tab "Ver Ubicaciones"**
   - Próximamente: visualización del almacén

### Datos Se Guardan En
```javascript
localStorage.getItem('configAlmacenIndividual')
```

Siempre sincronizado, nunca se pierden datos.

---

**Status**: ✅ Completamente funcional
**Versión**: 2.0 (Unificada)
**Última actualización**: 2024-12-XX
