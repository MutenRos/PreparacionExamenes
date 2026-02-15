# 🏭 Almacén - Arquitectura Unificada

## Visión General

Se ha completado una **reescritura completa** del módulo de almacén, eliminando fragmentación y creando una interfaz coherente y unificada.

### Cambios Principales

#### ❌ Eliminado
- ❌ "Configuración del almacén" (sección global redundante)
- ❌ "Edición por bloques" (complejidad innecesaria)
- ❌ Múltiples secciones desconectadas
- ❌ Flujo de datos confuso (configuración global vs individual)

#### ✅ Nuevo Enfoque
- ✅ **Navegación por tabs** clara y lógica
- ✅ **Configuración individual por pasillo** (para almacenes irregulares)
- ✅ **Configuración individual de estanterías** (nombre, capacidad, estado)
- ✅ **Sistema binario lleno/disponible** (no capacidad numérica)
- ✅ **Una sola fuente de verdad**: localStorage `configAlmacenIndividual`
- ✅ **Estadísticas en tiempo real** integradas

---

## Estructura de Tabs

```
🏭 Almacén
├─ 🔧 Configurar Pasillos (DEFAULT)
├─ 🔒 Gestionar Parcelas
├─ 📦 Ver Ubicaciones
└─ 📋 Productos
```

### Tab 1: 🔧 Configurar Pasillos

**Objetivo**: Crear y editar pasillos, y configurar cada estantería individualmente.

**Componentes**:
- **Estadísticas superiores**: Pasillos, Estanterías Total, Alturas Total, Parcelas Llenas
- **Panel Izquierdo**: Lista de pasillos guardados (con + Nueva Pasillo)
- **Panel Derecho**: Formulario de edición de pasillo
- **Sección Adicional**: 🏗️ Configurar Estanterías (cuando hay pasillo seleccionado)

**Flujo de Pasillos**:
1. Click en "+ Nueva Pasillo" → Formulario vacío en panel derecho
2. Completa: Número, Nombre (opcional), Estanterías (1-26), Alturas (1-20)
3. Click en "💾 Guardar" → Se guarda en localStorage
4. Click en pasillo de la lista → Cargar en panel derecho para editar
5. **NEW**: Click en "⚙️ Configurar Estanterías" → Abre sección de estanterías
6. Click "🗑️ Eliminar" → Eliminar (con confirmación)

**Flujo de Estanterías**:
1. Desde panel de pasillo, click "⚙️ Configurar Estanterías"
2. Se abre sección con 2 sub-tabs:
   - **📋 Vista General**: Grid de estanterías (A, B, C...)
   - **✏️ Editar Estantería**: Formulario para editar una específica
3. Click en cualquier tarjeta de estantería → Abre formulario de edición
4. Completa: Nombre, Capacidad (kg/unidades), Estado (Activa/Inactiva)
5. Click "💾 Guardar" → Se guarda en localStorage bajo `estanterias_config`

**Data Model**:
```javascript
configPasillos = {
  1: {
    num: 1,
    nombre: "Pasillo A",
    estanterias: 26,
    alturas: 6,
    estanterias_config: {
      1: { nombre: "Estantería A", capacidad: 100, activa: true },
      2: { nombre: "Bomba Especial", capacidad: 200, activa: true },
      3: { nombre: "Moto Parts", capacidad: 150, activa: false },
      ...
    },
    parcelas: {
      1: { 1: { lleno: false }, 2: { lleno: true }, ... },
      2: { ... },
      ...
    }
  },
  2: { ... }
}
```

**Persistencia**: `localStorage.configAlmacenIndividual` (JSON)

---

### Tab 2: 🔒 Gestionar Parcelas

**Objetivo**: Marcar parcelas (altura × estantería) como llenas o disponibles.

**Componentes**:
- Selector dropdown de pasillos
- Grid dinámico de estanterías (A, B, C, ...)
- Para cada estantería: Checkboxes de alturas con estado visual

**Flujo**:
1. Selecciona pasillo del dropdown → Carga grid de parcelas
2. Para cada altura: checkbox "Marcar como lleno"
3. Estado visual: 🔒 LLENO (rojo) vs ✓ Disponible (verde)
4. Click "💾 Guardar Cambios" → Actualiza `configPasillos[pasillo].parcelas`

**Estado Visual**:
```
✓ Disponible  → Fondo verde, background #d4edda
🔒 LLENO      → Fondo rojo, background #f8d7da
```

---

### Tab 3: 📦 Ver Ubicaciones

**Objetivo**: Visualizar almacén en vista de pasillos/estanterías.

**Componentes**:
- Vista integrada con datos de BD (cuando estén disponibles)
- Placeholder actual: "Almacén integrado con ubicaciones en BD"

**Próximamente**: Visualización en grid de pasillos, estanterías y parcelas.

---

### Tab 4: 📋 Productos

**Objetivo**: Buscar productos y ver su ubicación en almacén.

**Componentes**:
- Input de búsqueda (código o nombre)
- Tabla: Código | Nombre | Categoría | Ubicación

**Datos**: Desde `/api/inventario?limit=500`

**Búsqueda**: En tiempo real, case-insensitive, busca en código y nombre

---

## Data Model Unificado

### En Cliente (localStorage)

```javascript
localStorage.configAlmacenIndividual = JSON.stringify({
  1: {
    num: 1,
    nombre: "Pasillo A",
    estanterias: 26,
    alturas: 6,
    parcelas: {
      // [numEstanteria][altura] = { lleno: boolean }
      1: { 1: { lleno: false }, 2: { lleno: false }, 3: { lleno: true }, ... },
      2: { 1: { lleno: false }, ... },
      ...
    }
  },
  2: { ... },
  // ... más pasillos
})
```

### En Servidor (BD)

- **Tabla ubicaciones_almacen**: Datos de ubicaciones (cuando se integre)
- **Tabla productos**: Campo `ubicacion_almacen` para referencia

---

## Estilos y Componentes

### Design System
- **Colores**: Azul #667eea (primario), Gris #e0e0e0 (secundario)
- **Sombras**: `0 1px 3px rgba(0,0,0,0.08)` (subtle)
- **Bordes**: Left border 4px en tarjetas principales
- **Espaciado**: 16-24px gaps, 20px padding

### Elementos Reutilizables
- `.card`: Contenedor blanco con sombra
- `.panel`: Panel en grid 2 columnas
- `.form-group`: Label + Input/Select
- `.checkbox-group`: Checkbox con estado
- `.list-item`: Elemento clickeable con hover
- `.empty-state`: Placeholder cuando sin datos

### Estados
- `:hover` en items lista → Desplaza padding-left
- `:focus` en inputs → Border azul + shadow
- `.active` en tabs → Color azul + bottom border
- `.full` / `.available` en checkboxes → Colores diferenciados

---

## Funciones Principales

### Tab 1: Pasillos
```javascript
nuevoConfigPasillo()           // Crear nuevo
mostrarFormPasillo(numPasillo) // Editar existente
guardarPasillo()               // Guardar cambios
eliminarPasillo(num)           // Eliminar
limpiarForm()                  // Limpiar panel derecho
mostrarListaPasillos()         // Renderizar lista izquierda
```

### Tab 2: Parcelas
```javascript
actualizarSelectorParcelasLlenas() // Poblar dropdown
cargarParcelasLlenas()              // Cargar grid de parcelas
guardarParcelasLlenas()             // Guardar estado
```

### Estadísticas
```javascript
actualizarEstadisticas()  // Calcular y mostrar stats
```

### Persistencia
```javascript
guardarConfigLocal()              // Guardar en localStorage
cargarConfigAlmacenGuardada()     // Cargar al iniciar
```

### Tabs Auxiliares
```javascript
switchTab(tabName)  // Cambiar tab visible
loadAlmacen()       // Cargar ubicaciones (BD)
loadProductos()     // Cargar productos (API)
renderProductos()   // Renderizar tabla productos
```

---

## Flujo de Usuario Completo

### Caso 1: Configurar almacén nuevo
1. **Tab "Configurar Pasillos"**
2. Click "+ Nueva Pasillo"
3. Ingresa Pasillo 1, nombre "Pasillo A", 26 estanterías, 6 alturas
4. Click "💾 Guardar" → Aparece en lista
5. Repite para Pasillos 2, 3, etc.
6. Estadísticas se actualizan automáticamente

### Caso 2: Marcar parcelas como llenas
1. **Tab "Gestionar Parcelas"**
2. Selecciona "Pasillo A" del dropdown
3. Ve grid de Estanterías A-Z
4. Para estantería B: Marca alturas 1 y 3 como llenas
5. Click "💾 Guardar Cambios"
6. Estadísticas muestran "Parcelas Llenas: N"

### Caso 3: Buscar producto
1. **Tab "Productos"**
2. Escribe código o nombre en input
3. Tabla filtra en tiempo real
4. Ve ubicación en almacén (cuando esté disponible)

---

## Mejoras vs Versión Anterior

| Aspecto | Antes | Ahora |
|--------|-------|-------|
| **Estructura** | 4 secciones fragmentadas | 4 tabs unificados |
| **Configuración** | Global + Individual (confuso) | Solo individual (claro) |
| **Parcelas** | Capacidad numérica vaga | Binario lleno/disponible |
| **Flujo** | Múltiples puntos de verdad | Una sola fuente (localStorage) |
| **Estadísticas** | Manuales | Automáticas |
| **Usabilidad** | Sobrecargas | Limpia y enfocada |

---

## Próximos Pasos

- [ ] Integración con `/api/almacen/ubicaciones` (BD)
- [ ] Visualización en Tab 3 (grid de pasillos)
- [ ] Sincronización bidireccional con BD
- [ ] Multi-tenant ready
- [ ] Usar capacidad de estanterías en cálculos de ocupación
- [ ] Alertas de estanterías desactivadas
- [ ] Reportes de capacidad por pasillo

---

## Stack Técnico

- **Frontend**: Vanilla JavaScript + CSS3
- **Persistencia Local**: localStorage
- **APIs Backend**: 
  - `/api/almacen/ubicaciones` (TODO)
  - `/api/inventario`
- **Design System**: global.css + components.css + custom styles

---

**Estado**: ✅ Completamente funcional y unificado
**Última actualización**: 2024-12-XX
