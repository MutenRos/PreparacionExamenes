# Guía Rápida: Sistema CSS de OmniERP

## 🚀 Inicio Rápido

Agregar a cualquier template HTML:

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

---

## 📦 Componentes Esenciales

### 1. Cards - Contenedores
```html
<div class="card">
    <div class="card-header">
        <h2>Título</h2>
    </div>
    <div class="card-body">
        Contenido
    </div>
    <div class="card-footer">
        <button class="btn btn-primary">Acción</button>
    </div>
</div>
```

### 2. Botones
```html
<button class="btn btn-primary">Primario</button>
<button class="btn btn-secondary">Secundario</button>
<button class="btn btn-success">Éxito</button>
<button class="btn btn-warning">Advertencia</button>
<button class="btn btn-danger">Peligro</button>

<!-- Tamaños -->
<button class="btn btn-sm">Pequeño</button>
<button class="btn btn-lg">Grande</button>
<button class="btn btn-block">Ancho completo</button>
```

### 3. Formularios
```html
<form class="form">
    <div class="form-group">
        <label class="form-label">Email *</label>
        <input type="email" class="form-input">
        <div class="form-hint">Campo requerido</div>
    </div>
    
    <div class="form-group">
        <label class="form-label">Mensaje</label>
        <textarea class="form-textarea" rows="4"></textarea>
    </div>
    
    <div class="form-group">
        <label class="form-label">País</label>
        <select class="form-select">
            <option>Seleccione</option>
        </select>
    </div>
    
    <div class="form-group">
        <label class="checkbox-group">
            <input type="checkbox"> Acepto términos
        </label>
    </div>
</form>
```

### 4. Tablas
```html
<table class="table table-striped table-hover">
    <thead class="thead-dark">
        <tr>
            <th>Columna 1</th>
            <th>Columna 2</th>
        </tr>
    </thead>
    <tbody>
        <tr>
            <td>Dato 1</td>
            <td>Dato 2</td>
        </tr>
    </tbody>
</table>
```

### 5. KPI Cards
```html
<div class="grid grid-4">
    <div class="kpi-card">
        <div class="kpi-value">$45,231</div>
        <div class="kpi-label">Ingresos</div>
        <div class="kpi-change positive">↑ 12.5%</div>
    </div>
</div>
```

### 6. Badges y Tags
```html
<span class="badge">Info</span>
<span class="badge badge-success">Completado</span>
<span class="badge badge-warning">Pendiente</span>
<span class="badge badge-danger">Error</span>

<span class="tag">Python</span>
<span class="tag">FastAPI</span>
```

### 7. Modales
```html
<div class="modal active">
    <div class="modal-content">
        <div class="modal-header">
            <h2>Título</h2>
            <button class="modal-close">&times;</button>
        </div>
        <div class="modal-body">
            Contenido
        </div>
        <div class="modal-footer">
            <button class="btn btn-secondary">Cancelar</button>
            <button class="btn btn-primary">Guardar</button>
        </div>
    </div>
</div>
```

### 8. Tabs
```html
<div class="tabs-container">
    <div class="tabs-nav">
        <button class="tab-btn active" onclick="switchTab(0)">Tab 1</button>
        <button class="tab-btn" onclick="switchTab(1)">Tab 2</button>
    </div>
    <div class="tabs-content">
        <div class="tab-pane active">Contenido 1</div>
        <div class="tab-pane">Contenido 2</div>
    </div>
</div>
```

### 9. Acordeones
```html
<div class="accordion">
    <div class="accordion-item">
        <button class="accordion-trigger" onclick="toggleAccordion(this)">
            Sección 1
        </button>
        <div class="accordion-content">
            <div class="accordion-body">
                Contenido
            </div>
        </div>
    </div>
</div>
```

### 10. Barras de Progreso
```html
<div class="progress">
    <div class="progress-bar" style="width: 65%"></div>
</div>

<div class="progress">
    <div class="progress-bar success" style="width: 100%"></div>
</div>

<div class="progress">
    <div class="progress-bar warning" style="width: 50%"></div>
</div>

<div class="progress">
    <div class="progress-bar danger" style="width: 75%"></div>
</div>
```

### 11. Paginación
```html
<div class="pagination">
    <a href="#">« Anterior</a>
    <a href="#">1</a>
    <a href="#" class="active">2</a>
    <a href="#">3</a>
    <a href="#">Siguiente »</a>
</div>
```

### 12. Timeline
```html
<div class="timeline">
    <div class="timeline-item completed">
        <div class="timeline-title">Paso 1</div>
        <div class="timeline-content">Completado</div>
    </div>
    <div class="timeline-item">
        <div class="timeline-title">Paso 2</div>
        <div class="timeline-content">En progreso</div>
    </div>
</div>
```

### 13. DataGrids
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
            <div class="datagrid-actions">
                <button class="btn btn-sm">Editar</button>
            </div>
        </div>
    </div>
</div>
```

---

## 🎨 Clases de Utilidad

### Espaciado (Margin & Padding)
```html
<!-- Margin Top -->
<div class="mt-xs">4px</div>
<div class="mt-sm">8px</div>
<div class="mt-md">12px</div>
<div class="mt-lg">16px</div>
<div class="mt-xl">24px</div>
<div class="mt-2xl">32px</div>

<!-- Margin Bottom, Left, Right (igual sufijos) -->
<div class="mb-lg">Margin bottom 16px</div>
<div class="ml-md">Margin left 12px</div>
<div class="mr-sm">Margin right 8px</div>

<!-- Padding (sufijo 'p') -->
<div class="p-lg">Padding 16px</div>
<div class="px-md">Padding horizontal 12px</div>
<div class="py-sm">Padding vertical 8px</div>
```

### Flexbox
```html
<div class="flex">Flex row</div>
<div class="flex-col">Flex column</div>
<div class="flex-center">Centrado</div>
<div class="flex-between">Espaciado entre</div>
<div class="flex-wrap">Con wrap</div>
```

### Grid
```html
<div class="grid grid-2">Dos columnas</div>
<div class="grid grid-3">Tres columnas</div>
<div class="grid grid-4">Cuatro columnas</div>
```

### Texto
```html
<p class="text-center">Centrado</p>
<p class="text-right">Derecha</p>
<p class="text-bold">Negrita</p>
<p class="text-muted">Gris secundario</p>
<p class="text-sm">Texto pequeño</p>
```

### Display
```html
<div class="hidden">Oculto</div>
<div class="block">Block</div>
<div class="inline">Inline</div>
<div class="inline-block">Inline-block</div>
```

---

## 🎯 Colores

### Variables CSS
```css
--brand-primary: #3b82f6        /* Azul principal */
--brand-secondary: #1e40af      /* Azul secundario */
--color-success: #10b981        /* Verde */
--color-warning: #f59e0b        /* Ámbar */
--color-danger: #ef4444         /* Rojo */
--color-info: #0ea5e9           /* Azul claro */

--text-primary: #1f2937         /* Negro */
--text-secondary: #6b7280       /* Gris oscuro */
--bg-primary: #ffffff           /* Blanco */
--bg-secondary: #f9fafb         /* Gris muy claro */
--border-color: #d1d5db         /* Gris */
```

### Usar en CSS
```css
button {
    background: var(--brand-primary);
    color: white;
    border-color: var(--border-color);
}
```

---

## 📱 Responsive Breakpoints

```css
/* Escritorio (default) */
/* > 1024px */

/* Tablet */
@media (max-width: 1024px) {
    /* Ajustes para tablet */
}

/* Móvil */
@media (max-width: 768px) {
    /* Ajustes para móvil */
    .grid { grid-template-columns: 1fr; }
    .card { border-radius: 4px; }
}

/* Móvil pequeño */
@media (max-width: 480px) {
    /* Ajustes para móvil pequeño */
    .btn { width: 100%; }
}
```

---

## 🔗 Enlaces Útiles

| Recurso | URL |
|---------|-----|
| **Documentación completa** | `/CSS_FRAMEWORK.md` |
| **Ejemplo interactivo** | `/app/example` |
| **CSS Base** | `/static/modules-base.css` |
| **CSS Avanzado** | `/static/components-advanced.css` |

---

## 💡 Tips Prácticos

### 1. Estructura básica de módulo
```html
<div class="container">
    <section class="section">
        <h1>Título del módulo</h1>
        <div class="grid grid-3">
            <div class="card">
                <div class="card-body">
                    <!-- Contenido -->
                </div>
            </div>
        </div>
    </section>
</div>
```

### 2. Formulario con validación
```html
<div class="card">
    <div class="card-header">
        <h3>Nuevo Registro</h3>
    </div>
    <div class="card-body">
        <form class="form">
            <div class="form-group">
                <label class="form-label">Nombre *</label>
                <input type="text" class="form-input" required>
                <div class="form-error" style="display: none;">Campo requerido</div>
            </div>
            <button type="submit" class="btn btn-primary">Guardar</button>
        </form>
    </div>
</div>
```

### 3. Tabla con acciones
```html
<div class="table-wrapper">
    <table class="table table-striped table-hover">
        <thead class="thead-dark">
            <tr>
                <th>Nombre</th>
                <th>Estado</th>
                <th>Acciones</th>
            </tr>
        </thead>
        <tbody>
            <tr>
                <td>Producto A</td>
                <td><span class="badge badge-success">Activo</span></td>
                <td>
                    <button class="btn btn-sm">Editar</button>
                    <button class="btn btn-sm btn-danger">Eliminar</button>
                </td>
            </tr>
        </tbody>
    </table>
</div>
```

### 4. Dashboard con KPIs
```html
<div class="grid grid-4 mb-lg">
    <div class="kpi-card">
        <div class="kpi-value">1,234</div>
        <div class="kpi-label">Ventas</div>
        <div class="kpi-change positive">↑ 12%</div>
    </div>
    <div class="kpi-card">
        <div class="kpi-value">$45K</div>
        <div class="kpi-label">Ingresos</div>
        <div class="kpi-change positive">↑ 8%</div>
    </div>
    <!-- Más KPIs -->
</div>
```

---

## 📝 Crear componentes personalizados

```css
/* En tu archivo CSS personalizado */

.my-custom-card {
    background: var(--bg-primary);
    border: 1px solid var(--border-color);
    border-radius: var(--radius-md);
    padding: var(--spacing-lg);
    box-shadow: var(--shadow-md);
}

.my-custom-button {
    background: linear-gradient(
        90deg,
        var(--brand-primary) 0%,
        var(--brand-secondary) 100%
    );
    color: white;
    padding: var(--spacing-md) var(--spacing-lg);
    border: none;
    border-radius: var(--radius-sm);
    cursor: pointer;
    transition: all var(--transition-fast);
}

.my-custom-button:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}
```

---

## 🚨 Solución de Problemas

### "Los estilos no se aplican"
1. Verifica que ambos archivos CSS se cargan
2. Abre DevTools (F12) → Network
3. Verifica que modules-base.css y components-advanced.css tengan status 200

### "Comportamiento responsive no funciona"
1. Abre DevTools → Responsive Design Mode (Ctrl+Shift+M)
2. Verifica los breakpoints: 1024px, 768px, 480px
3. Revisa las media queries en ambos CSS

### "Colores no se ven como esperado"
1. Usa las variables CSS: `var(--brand-primary)`
2. No escribas colores hardcoded (#3b82f6)
3. Esto facilita cambios globales

---

## 📈 Rendimiento

- **modules-base.css**: 15.6 KB
- **components-advanced.css**: 18.3 KB
- **Total**: ~34.9 KB (minificado y comprimido en servidor)
- **Carga**: < 50ms en conexión 4G

---

*Última actualización: Diciembre 2024*
*OmniERP CSS Framework v2.0*
