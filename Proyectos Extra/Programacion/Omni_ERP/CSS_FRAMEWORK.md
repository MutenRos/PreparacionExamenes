# Framework CSS de OmniERP

## Descripción General

Se ha implementado un sistema CSS moderno y consistente en toda la plataforma OmniERP, dividido en dos archivos complementarios:

1. **modules-base.css** (700+ líneas): Framework base con estilos fundamentales
2. **components-advanced.css** (950+ líneas): Componentes avanzados y módulos especializados

Ambos archivos están disponibles en `/static/` y se cargan automáticamente en todos los templates.

---

## modules-base.css - Framework Base

### Variables CSS Globales

```css
/* Colores principales */
--brand-primary: #3b82f6        /* Azul principal */
--brand-secondary: #1e40af      /* Azul secundario */
--color-success: #10b981        /* Verde */
--color-warning: #f59e0b        /* Ámbar */
--color-danger: #ef4444         /* Rojo */
--color-info: #0ea5e9           /* Azul claro */

/* Paleta de grises */
--text-primary: #1f2937         /* Negro suave */
--text-secondary: #6b7280       /* Gris oscuro */
--text-tertiary: #9ca3af        /* Gris claro */
--bg-primary: #ffffff           /* Blanco */
--bg-secondary: #f9fafb         /* Gris muy claro */
--bg-tertiary: #f3f4f6          /* Gris claro */
--border-color: #d1d5db         /* Gris medio */
--border-color-light: #e5e7eb   /* Gris claro */

/* Espaciado */
--spacing-xs: 4px
--spacing-sm: 8px
--spacing-md: 12px
--spacing-lg: 16px
--spacing-xl: 24px
--spacing-2xl: 32px

/* Otros */
--radius-sm: 4px                /* Border radius pequeño */
--radius-md: 8px                /* Border radius medio */
--radius-lg: 12px               /* Border radius grande */
--transition-fast: 150ms ease   /* Transición rápida */
--shadow-sm: 0 1px 2px rgba(...)  /* Sombra pequeña */
--shadow-md: 0 4px 6px rgba(...)  /* Sombra media */
--shadow-lg: 0 10px 25px rgba(...)/* Sombra grande */
```

### Secciones Principales

#### 1. HEADER & NAVIGATION
- `.header`: Encabezado principal con navegación
- `.navbar`: Barra de navegación
- `.nav-item`: Elemento de navegación
- `.breadcrumbs`: Rutas de navegación

#### 2. CONTAINERS
- `.container`: Contenedor principal (max-width: 1200px)
- `.page-container`: Contenedor de página
- `.section`: Sección de contenido
- `.sidebar`: Barra lateral

#### 3. CARDS & PANELS
- `.card`: Tarjeta principal con sombra
- `.card-header`: Encabezado de tarjeta
- `.card-body`: Cuerpo de tarjeta
- `.card-footer`: Pie de tarjeta
- `.panel`: Panel alternativo
- `.panel-small`: Panel compacto

#### 4. FORMULARIOS
- `.form-group`: Grupo de campo de formulario
- `.form-label`: Etiqueta de campo
- `.form-input`, `.form-textarea`, `.form-select`: Campos de entrada
- `.form-error`: Mensaje de error
- `.form-hint`: Sugerencia de campo
- `.checkbox-group`, `.radio-group`: Grupos de opciones

#### 5. BOTONES
- `.btn`: Botón principal (azul)
- `.btn-secondary`: Botón secundario
- `.btn-success`, `.btn-warning`, `.btn-danger`: Variantes de color
- `.btn-sm`, `.btn-lg`: Tamaños
- `.btn-block`: Botón ancho
- `.btn-disabled`: Botón deshabilitado

#### 6. BADGES & TAGS
- `.badge`: Insignia con fondo
- `.badge-success`, `.badge-warning`, `.badge-danger`: Variantes
- `.badge-sm`, `.badge-lg`: Tamaños
- `.tag`: Etiqueta de texto simple

#### 7. TABLAS
- `.table`: Tabla básica
- `.table-striped`: Tabla con filas alternadas
- `.table-hover`: Tabla con hover
- `.table-bordered`: Tabla con bordes
- `.table-sm`: Tabla compacta
- `.thead-dark`: Encabezado oscuro

#### 8. LISTAS
- `.list`: Lista estándar
- `.list-inline`: Lista horizontal
- `.list-numbered`: Lista numerada
- `.list-icon`: Lista con iconos

#### 9. TABS
- `.tabs-container`: Contenedor de tabs
- `.tabs-nav`: Navegación de tabs
- `.tabs-content`: Contenido de tabs
- `.tab-pane`: Panel de tab individual

#### 10. KPI CARDS
- `.kpi-card`: Tarjeta de KPI
- `.kpi-value`: Valor del KPI
- `.kpi-label`: Etiqueta del KPI
- `.kpi-change`: Cambio de KPI (puede incluir flecha)
- `.kpi-change.positive`: Cambio positivo (verde)
- `.kpi-change.negative`: Cambio negativo (rojo)

#### 11. CLASES DE UTILIDAD
- **Espaciado**: `.mt-4`, `.mb-8`, `.p-12`, `.px-8`, `.py-4`
- **Flexbox**: `.flex`, `.flex-center`, `.flex-between`, `.flex-col`
- **Grid**: `.grid`, `.grid-2`, `.grid-3`, `.grid-4`
- **Texto**: `.text-center`, `.text-right`, `.text-bold`, `.text-muted`
- **Display**: `.hidden`, `.block`, `.inline`, `.inline-block`
- **Alineación**: `.text-top`, `.text-middle`, `.text-bottom`

### Ejemplo de Uso

```html
<div class="container mt-lg">
  <div class="card">
    <div class="card-header">
      <h2>Título</h2>
    </div>
    <div class="card-body">
      <form class="form">
        <div class="form-group">
          <label class="form-label">Campo:</label>
          <input type="text" class="form-input">
        </div>
        <button class="btn btn-primary">Guardar</button>
      </form>
    </div>
  </div>
</div>
```

---

## components-advanced.css - Componentes Avanzados

### Modales

```html
<div class="modal active">
  <div class="modal-content">
    <div class="modal-header">
      <h2>Título del Modal</h2>
      <button class="modal-close">&times;</button>
    </div>
    <div class="modal-body">
      Contenido aquí
    </div>
    <div class="modal-footer">
      <button class="btn btn-secondary">Cancelar</button>
      <button class="btn btn-primary">Guardar</button>
    </div>
  </div>
</div>
```

**Clases:**
- `.modal`: Contenedor del modal (fixed, display: none)
- `.modal.active`: Modal visible
- `.modal-content`: Caja del modal con animación slideUp
- `.modal-header`, `.modal-body`, `.modal-footer`

---

### DataGrids

```html
<div class="datagrid">
  <div class="datagrid-header">
    <input type="checkbox">
    <span>Seleccionar todo</span>
  </div>
  <div class="datagrid-body">
    <div class="datagrid-row">
      <div class="datagrid-cell">
        <input type="checkbox">
      </div>
      <div class="datagrid-cell">Datos</div>
      <div class="datagrid-cell">Más datos</div>
      <div class="datagrid-actions">
        <button class="btn btn-sm">Editar</button>
      </div>
    </div>
  </div>
</div>
```

**Clases:**
- `.datagrid`: Contenedor
- `.datagrid-header`: Encabezado con filtros
- `.datagrid-body`: Cuerpo scrolleable (max-height: 500px)
- `.datagrid-row`: Fila individual
- `.datagrid-row.selected`: Fila seleccionada
- `.datagrid-cell`: Celda
- `.datagrid-actions`: Botones de acciones

---

### Tooltips

```html
<div class="tooltip">
  <span>Pasar el mouse aquí</span>
  <span class="tooltiptext">Este es el tooltip</span>
</div>
```

**Características:**
- Aparece en hover
- Posicionado arriba del elemento
- Animación de fade-in

---

### Dropdowns

```html
<div class="dropdown">
  <button class="dropdown-btn">Menú ▼</button>
  <div class="dropdown-content">
    <a href="#">Opción 1</a>
    <a href="#">Opción 2</a>
    <hr>
    <a href="#">Opción 3</a>
  </div>
</div>
```

**Clases:**
- `.dropdown`: Contenedor
- `.dropdown-btn`: Botón activador
- `.dropdown-content`: Menú (display: none por defecto)
- `.dropdown-content.active`: Menú visible

---

### Barras de Progreso

```html
<div class="progress">
  <div class="progress-bar" style="width: 65%"></div>
</div>
<div class="progress-text">65% completado</div>
```

**Variantes:**
- `.progress-bar`: Azul (default)
- `.progress-bar.success`: Verde
- `.progress-bar.warning`: Ámbar
- `.progress-bar.danger`: Rojo

---

### Spinners y Loaders

```html
<div class="spinner"></div>
<div class="spinner sm"></div>
<div class="spinner lg"></div>

<div class="loader">
  <div class="loader-dot"></div>
  <div class="loader-dot"></div>
  <div class="loader-dot"></div>
</div>
```

---

### Acordeones

```html
<div class="accordion">
  <div class="accordion-item">
    <button class="accordion-trigger">Sección 1</button>
    <div class="accordion-content">
      <div class="accordion-body">
        Contenido de la sección 1
      </div>
    </div>
  </div>
  <div class="accordion-item">
    <button class="accordion-trigger">Sección 2</button>
    <div class="accordion-content">
      <div class="accordion-body">
        Contenido de la sección 2
      </div>
    </div>
  </div>
</div>
```

**Uso JavaScript:**
```javascript
document.querySelectorAll('.accordion-trigger').forEach(trigger => {
  trigger.addEventListener('click', function() {
    this.classList.toggle('active');
    this.nextElementSibling.classList.toggle('active');
  });
});
```

---

### Switches/Toggles

```html
<label class="switch">
  <input type="checkbox">
  <span class="toggle"></span>
  <span>Activar opción</span>
</label>
```

---

### Timeline

```html
<div class="timeline">
  <div class="timeline-item">
    <div class="timeline-title">Paso 1</div>
    <div class="timeline-content">Descripción del paso 1</div>
  </div>
  <div class="timeline-item completed">
    <div class="timeline-title">Paso 2 (Completado)</div>
    <div class="timeline-content">Descripción del paso 2</div>
  </div>
</div>
```

---

### Paginación

```html
<div class="pagination">
  <a href="#">« Anterior</a>
  <a href="#">1</a>
  <a href="#" class="active">2</a>
  <a href="#">3</a>
  <a href="#">Siguiente »</a>
</div>
```

---

## Responsive Design

Ambos archivos CSS incluyen breakpoints responsive:

```css
/* Tablet (1024px y menor) */
@media (max-width: 1024px) {
  /* Ajustes para tablets */
}

/* Móvil (768px y menor) */
@media (max-width: 768px) {
  /* Ajustes para móviles */
}

/* Móvil pequeño (480px y menor) */
@media (max-width: 480px) {
  /* Ajustes para móviles pequeños */
}
```

### Cambios responsive principales:

- Las tarjetas se apilan en una columna
- Los formularios se adaptan a pantalla completa
- Las tablas se vuelven scrolleables horizontalmente
- Los modales ocupan 95% del ancho
- Los botones se expanden a ancho completo en móviles

---

## Guía de Implementación

### 1. Agregar referencias en nuevos templates:

```html
<!DOCTYPE html>
<html>
<head>
    <link rel="stylesheet" href="/static/modules-base.css">
    <link rel="stylesheet" href="/static/components-advanced.css">
</head>
<body>
    <!-- Tu contenido aquí -->
</body>
</html>
```

### 2. Estructura recomendada:

```html
<div class="container">
  <section class="section">
    <h1>Título de Sección</h1>
    
    <div class="card">
      <div class="card-header">
        <h2>Tarjeta</h2>
      </div>
      <div class="card-body">
        <!-- Contenido -->
      </div>
    </div>
  </section>
</div>
```

### 3. Combinar componentes:

```html
<!-- Grid de KPIs con Cards -->
<div class="grid grid-4">
  <div class="kpi-card">
    <div class="kpi-value">1,234</div>
    <div class="kpi-label">Ventas Totales</div>
    <div class="kpi-change positive">↑ 12%</div>
  </div>
</div>

<!-- Tabla con Acciones -->
<div class="table-wrapper">
  <table class="table table-striped table-hover">
    <thead class="thead-dark">
      <tr>
        <th>Columna 1</th>
        <th>Acciones</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Dato</td>
        <td>
          <button class="btn btn-sm">Editar</button>
        </td>
      </tr>
    </tbody>
  </table>
</div>
```

---

## Colores en Contexto

| Clase/Variable | Color | Uso |
|---|---|---|
| `--brand-primary` / `.btn-primary` | Azul (#3b82f6) | Acciones principales |
| `--color-success` / `.badge-success` | Verde (#10b981) | Éxito, completado |
| `--color-warning` / `.badge-warning` | Ámbar (#f59e0b) | Advertencia, pendiente |
| `--color-danger` / `.badge-danger` | Rojo (#ef4444) | Error, peligro, cancelado |
| `--color-info` | Azul claro (#0ea5e9) | Información |
| `--text-secondary` / `.text-muted` | Gris (#6b7280) | Texto secundario |

---

## Mejores Prácticas

1. **Utiliza las variables CSS**: No escribas colores hardcoded, usa las variables
2. **Consistencia de espaciado**: Usa las clases de espaciado (`mt-`, `mb-`, `p-`)
3. **Componentes reutilizables**: Implementa componentes como cards, modales, etc.
4. **Mobile-first**: Diseña pensando primero en móvil
5. **Prueba responsive**: Verifica en breakpoints (1024px, 768px, 480px)
6. **Validación visual**: Usa badges y colores para estados (success, warning, danger)
7. **Accesibilidad**: Mantén suficiente contraste de colores y texto legible

---

## Archivos CSS Disponibles

```
/static/
├── modules-base.css (15.6 KB)
│   └── Framework base, variables, componentes principales
└── components-advanced.css (18.3 KB)
    └── Modales, datagrids, tooltips, etc.
```

Ambos se cargan en todos los templates (53 archivos actualizados).

---

## Soporte y Mantenimiento

Para agregar nuevos estilos:
1. Si es un componente básico → `modules-base.css`
2. Si es un componente complejo → `components-advanced.css`
3. Mantén las variables CSS actualizadas
4. Documenta nuevas clases en este archivo
5. Prueba en los tres breakpoints responsive

---

*Última actualización: Diciembre 2024*
*Framework CSS v2.0 - OmniERP*
