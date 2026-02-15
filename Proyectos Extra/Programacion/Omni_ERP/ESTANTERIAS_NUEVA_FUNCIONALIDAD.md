# 🏗️ ESTANTERÍAS - Configuración Individual Agregada

## Lo Nuevo

Has pedido poder configurar estanterías, y ya está hecho. 

Ahora cada estantería dentro de un pasillo es configurable con:
- ✅ **Nombre** personalizado
- ✅ **Capacidad** máxima (kg o unidades)
- ✅ **Estado** (Activa/Inactiva)

---

## Flujo Visual

```
1. Tab "🔧 Configurar Pasillos"
   ├─ Selecciona pasillo "Pasillo A"
   └─ Panel derecho muestra: Número, Nombre, Estanterías, Alturas
      + NUEVO BOTÓN: "⚙️ Configurar Estanterías" (verde)

2. Click en "⚙️ Configurar Estanterías"
   ├─ Nueva sección: "🏗️ Configurar Estanterías"
   ├─ Sub-tabs: 📋 Vista General | ✏️ Editar Estantería
   │
   └─ 📋 Vista General (DEFAULT)
      ├─ Grid de tarjetas (A, B, C, D, ... Z)
      ├─ Cada tarjeta muestra:
      │  ├─ Letra (A)
      │  ├─ Nombre ("Estantería A")
      │  └─ Estado ("✓ Activa")
      └─ Click en tarjeta → Abre formulario de edición

3. Click en tarjeta (ej: Estantería B)
   ├─ Cambia a sub-tab "✏️ Editar Estantería"
   ├─ Formulario con:
   │  ├─ Nombre: "Bomba Especial"
   │  ├─ Capacidad: "200" kg
   │  └─ Estado: ✓ Checkbox "Estantería Activa"
   └─ Botones: 💾 Guardar | Cancelar

4. Click "💾 Guardar"
   ├─ Guarda en localStorage
   ├─ Vuelve a Vista General
   └─ Tarjeta actualiza: muestra nuevo nombre y estado
```

---

## Ejemplo Real

### Pasillo 1: "Pasillo A" (26 estanterías)

**Antes**: Todas las estanterías eran iguales (A, B, C, ...)

**Ahora**:

| Tarjeta | Nombre | Capacidad | Estado |
|---------|--------|-----------|---------|
| A | Estantería A | 100 kg | ✓ Activa |
| B | Bomba Especial | 200 kg | ✓ Activa |
| C | Moto Parts | 150 kg | ⊘ Inactiva |
| D | Válvulas Hidráulicas | 80 kg | ✓ Activa |
| E | Sellos | 50 kg | ✓ Activa |
| ... | ... | ... | ... |

**Resultado**: Cada estantería puede tener propiedades únicas.

---

## Interfaz

### Vista General (Grid)

```
┌─────────────┐  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
│      A      │  │      B      │  │      C      │  │      D      │
│ Estantería  │  │  Bomba Esp. │  │ Moto Parts  │  │  Válvulas   │
│ ✓ Activa    │  │ ✓ Activa    │  │ ⊘ Inactiva  │  │ ✓ Activa    │
└─────────────┘  └─────────────┘  └─────────────┘  └─────────────┘
      ↓              ↓                  ↓              ↓
   Click aquí para editar
```

### Formulario de Edición

```
┌──────────────────────────────────────┐
│ Letra (Estantería B)                 │
│ ┌────────────────────────────────┐   │
│ │ Bomba Especial        [campo]  │   │
│ └────────────────────────────────┘   │
├──────────────────────────────────────┤
│ Capacidad Máxima (kg/unidades)       │
│ ┌────────────────────────────────┐   │
│ │ 200                   [número] │   │
│ └────────────────────────────────┘   │
├──────────────────────────────────────┤
│ ☑ Estantería Activa    [checkbox]    │
├──────────────────────────────────────┤
│ [💾 Guardar] [Cancelar]              │
└──────────────────────────────────────┘
```

---

## Datos Guardados

```javascript
localStorage.configAlmacenIndividual = {
  1: {
    num: 1,
    nombre: "Pasillo A",
    estanterias: 26,
    alturas: 6,
    estanterias_config: {
      1: {
        nombre: "Estantería A",
        capacidad: 100,
        activa: true
      },
      2: {
        nombre: "Bomba Especial",
        capacidad: 200,
        activa: true
      },
      3: {
        nombre: "Moto Parts",
        capacidad: 150,
        activa: false
      },
      4: {
        nombre: "Válvulas Hidráulicas",
        capacidad: 80,
        activa: true
      },
      // ... más estanterías
    },
    parcelas: { ... }  // Mantiene la configuración de parcelas llenas
  },
  // ... más pasillos
}
```

---

## Funciones JavaScript Agregadas

| Función | Qué Hace |
|---------|----------|
| `mostrarConfigEstanterias(numPasillo)` | Abre la sección de estanterías |
| `mostrarVistaPasilloEstanterias(numPasillo)` | Renderiza el grid de tarjetas |
| `editarEstanteria(numPasillo, numEstanteria)` | Abre formulario de edición |
| `guardarEstanteria(numPasillo, numEstanteria)` | Guarda cambios en localStorage |
| `limpiarFormEstanteria()` | Limpia formulario y deselecciona tarjeta |
| `switchSubTab(subTabName)` | Cambia entre Vista General y Editar |

---

## Validaciones

- ✅ Capacidad debe ser > 0
- ✅ Nombre puede estar vacío (usa letra por defecto)
- ✅ Se guarda automáticamente en localStorage
- ✅ Persiste al recargar
- ✅ No hay límite de estanterías a configurar

---

## Cambios en el Código

### Antes
```html
<!-- Solo configuración de pasillo -->
<button onclick="guardarPasillo()">💾 Guardar</button>
<button onclick="eliminarPasillo()">🗑️ Eliminar</button>
```

### Ahora
```html
<!-- Configuración de pasillo + estanterías -->
<button onclick="guardarPasillo()">💾 Guardar</button>
<button onclick="mostrarConfigEstanterias(${numPasillo})">⚙️ Configurar Estanterías</button>
<button onclick="eliminarPasillo()">🗑️ Eliminar</button>
```

---

## Commits

```
1. feat: agregar configuración individual de estanterías
   - Nuevo botón en panel de pasillos
   - Nueva sección con estanterías_config
   - Grid visual y formulario de edición
   - Sub-tabs: Vista General + Editar

2. docs: guía de configuración individual de estanterías
   - Ejemplo práctico
   - Flujo de uso
   - Data model

3. docs: actualizar documentación con nueva funcionalidad
   - Actualización en ALMACEN_ARQUITECTURA_UNIFICADA.md
   - Data model extendido
   - Próximos pasos
```

---

## Próximos Pasos Posibles

- Usar la capacidad de estanterías en cálculos de ocupación
- Alertas cuando se intenta añadir producto a estantería inactiva
- Reportes de capacidad por pasillo/estantería
- Historial de cambios
- Importar/exportar configuración

---

**Status**: ✅ Completamente funcional
**Acceso**: http://localhost:8000/app/almacen → Tab "🔧 Configurar Pasillos" → Selecciona pasillo → "⚙️ Configurar Estanterías"
