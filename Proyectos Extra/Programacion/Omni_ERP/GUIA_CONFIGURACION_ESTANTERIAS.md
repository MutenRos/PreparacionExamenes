# 🏗️ Configuración de Estanterías - Guía Rápida

## ¿Qué es Nuevo?

Ahora puedes configurar cada estantería individualmente dentro de un pasillo, personalizando:
- **Nombre**: Cambiar la letra A, B, C por nombres personalizados
- **Capacidad**: Definir la capacidad máxima en kg o unidades
- **Estado**: Activar/desactivar una estantería

---

## Flujo de Uso

### 1️⃣ Selecciona un Pasillo
En tab "🔧 Configurar Pasillos", haz clic en un pasillo de la lista izquierda.

### 2️⃣ Haz Clic en "⚙️ Configurar Estanterías"
Aparece un botón verde en el panel derecho (solo si el pasillo está guardado).

### 3️⃣ Ves la Vista General
Se abre una sección "🏗️ Configurar Estanterías" con:
- Grid de tarjetas (una por cada estantería)
- Letra (A, B, C...)
- Nombre personalizado
- Estado (✓ Activa / ⊘ Inactiva)

### 4️⃣ Haz Clic en una Estantería para Editar
Se abre el formulario con:
- **Nombre**: Campo de texto (por defecto la letra)
- **Capacidad**: Número en kg o unidades
- **Estado**: Checkbox para activar/desactivar

### 5️⃣ Guarda los Cambios
Click "💾 Guardar" y vuelves a la vista general.

---

## Ejemplo Práctico

**Pasillo 1: "Pasillo A"**
- 26 estanterías (A-Z)
- 6 alturas

### Configuración de Estanterías:

| Estantería | Nombre | Capacidad | Estado |
|------------|--------|-----------|---------|
| A | Estantería A | 100 kg | ✓ Activa |
| B | Bomba Especial | 200 kg | ✓ Activa |
| C | Moto Parts | 150 kg | ⊘ Inactiva |
| D | Válvulas | 80 kg | ✓ Activa |
| ... | ... | ... | ... |

**Resultado**: Cada estantería tiene propiedades únicas y el sistema respeta su estado.

---

## Data Model

```javascript
configPasillos = {
  1: {
    num: 1,
    nombre: "Pasillo A",
    estanterias: 26,
    alturas: 6,
    estanterias_config: {
      1: {  // Estantería A
        nombre: "Estantería A",
        capacidad: 100,
        activa: true
      },
      2: {  // Estantería B
        nombre: "Bomba Especial",
        capacidad: 200,
        activa: true
      },
      3: {  // Estantería C
        nombre: "Moto Parts",
        capacidad: 150,
        activa: false
      },
      ...
    },
    parcelas: { ... }
  },
  ...
}
```

---

## Funcionalidades

### Vista General (📋 Vista General)
- Grid de tarjetas para todas las estanterías
- Click en cualquier tarjeta para editar
- Cambio visual cuando está seleccionada (azul)
- Muestra estado actual (Activa/Inactiva)

### Editar Estantería (✏️ Editar Estantería)
- Formulario con 3 campos:
  - Nombre (texto)
  - Capacidad (número)
  - Estado (checkbox)
- Botones: Guardar, Cancelar
- La tarjeta de la estantería seleccionada se resalta

---

## Sub-Tabs

Dentro de "🏗️ Configurar Estanterías" hay 2 sub-tabs:

1. **📋 Vista General**: Ves todas las estanterías de un vistazo
2. **✏️ Editar Estantería**: Editas una específica

Se pueden cambiar haciendo clic en los botones.

---

## Validaciones

- ✅ Capacidad debe ser mayor a 0
- ✅ Nombre puede estar vacío (se usa la letra por defecto)
- ✅ Se guarda en localStorage automáticamente
- ✅ Los datos persisten al recargar

---

## Próximos Pasos

- [ ] Usar capacidad en cálculos de ocupación
- [ ] Alertas cuando una estantería desactiva
- [ ] Reportes de capacidad por pasillo
- [ ] Historial de cambios en estanterías
- [ ] Importar/exportar configuración

---

## Commit

```
feat: agregar configuración individual de estanterías

- Nuevo botón 'Configurar Estanterías' en panel derecho
- Nueva sección con vista general y edición
- Sub-tabs: Vista General + Editar Estantería
- Configurable: nombre, capacidad, estado activo/inactivo
- Persistencia en localStorage
```

---

**Estado**: ✅ Completamente funcional
**Acceso**: http://localhost:8000/app/almacen
