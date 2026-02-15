# 🎨 Guía de Paleta de Colores - OmniERP

## Introducción

Este documento define la **paleta de colores unificada** del sistema OmniERP. Todos los desarrolladores deben usar estas variables CSS en lugar de colores hardcodeados.

## 📁 Archivos CSS del Sistema

### Orden de Carga (Importar en este orden):

1. **`/static/css/variables.css`** - Variables del sistema de diseño
2. **`/static/css/base.css`** - Estilos base y componentes
3. **`/static/global.css`** - Estilos globales enterprise
4. **`/static/components.css`** - Componentes específicos
5. **`/static/aaaaa-animations.css`** - Animaciones
6. **`/static/assistant.css`** - Estilos del asistente
7. **`/static/css/tutorial.css`** - Tutorial

### Ejemplo en HTML:

```html
<head>
    <!-- CSS Variables & Design System -->
    <link rel="stylesheet" href="/static/css/variables.css">
    <link rel="stylesheet" href="/static/css/base.css">
    <!-- Component Styles -->
    <link rel="stylesheet" href="/static/global.css">
    <link rel="stylesheet" href="/static/components.css">
    <link rel="stylesheet" href="/static/aaaaa-animations.css">
    <link rel="stylesheet" href="/static/assistant.css">
    <link rel="stylesheet" href="/static/css/tutorial.css">
</head>
```

---

## 🎨 Paleta de Colores Principal

### Colores de Marca (Brand Colors)

```css
var(--brand-primary)       /* #667eea - Púrpura principal */
var(--brand-primary-dark)  /* #5568d3 - Púrpura oscuro */
var(--brand-primary-light) /* #8b9eff - Púrpura claro */
var(--brand-secondary)     /* #764ba2 - Secundario morado */
var(--brand-accent)        /* #10b981 - Verde acento */
```

**Uso:**
- Botones principales
- Enlaces importantes
- Headers y títulos destacados
- Elementos interactivos principales

**Ejemplos:**
```css
.btn-primary {
    background: linear-gradient(135deg, var(--brand-primary) 0%, var(--brand-primary-dark) 100%);
    color: var(--text-inverse);
}

.link {
    color: var(--brand-primary);
}

.link:hover {
    color: var(--brand-primary-dark);
}
```

---

### Colores Semánticos

#### ✅ Success (Éxito)
```css
var(--color-success)       /* #10b981 - Verde principal */
var(--color-success-light) /* #d1fae5 - Verde claro */
var(--color-success-dark)  /* #059669 - Verde oscuro */
```

**Uso:** Mensajes de éxito, confirmaciones, estados positivos

#### ❌ Danger (Error/Peligro)
```css
var(--color-danger)        /* #ef4444 - Rojo principal */
var(--color-danger-light)  /* #fee2e2 - Rojo claro */
var(--color-danger-dark)   /* #dc2626 - Rojo oscuro */
```

**Uso:** Errores, alertas críticas, acciones destructivas

#### ⚠️ Warning (Advertencia)
```css
var(--color-warning)       /* #f59e0b - Naranja principal */
var(--color-warning-light) /* #fef3c7 - Naranja claro */
var(--color-warning-dark)  /* #d97706 - Naranja oscuro */
```

**Uso:** Advertencias, precauciones, estados pendientes

#### ℹ️ Info (Información)
```css
var(--color-info)          /* #3b82f6 - Azul principal */
var(--color-info-light)    /* #dbeafe - Azul claro */
var(--color-info-dark)     /* #2563eb - Azul oscuro */
```

**Uso:** Información general, tooltips, notas

---

## 🖤 Escala de Grises

### Colores Neutrales

```css
var(--gray-50)   /* #fafafa - Casi blanco */
var(--gray-100)  /* #f3f4f6 - Muy claro */
var(--gray-200)  /* #e5e7eb - Claro */
var(--gray-300)  /* #d1d5db - Medio claro */
var(--gray-400)  /* #9ca3af - Medio */
var(--gray-500)  /* #6b7280 - Medio oscuro */
var(--gray-600)  /* #4b5563 - Oscuro */
var(--gray-700)  /* #374151 - Muy oscuro */
var(--gray-800)  /* #1f2937 - Casi negro */
var(--gray-900)  /* #111827 - Negro */
```

### Colores Base

```css
var(--color-white) /* #ffffff - Blanco puro */
var(--color-black) /* #111111 - Negro */
```

---

## 🖼️ Fondos (Backgrounds)

```css
var(--bg-primary)   /* Fondo principal (blanco) */
var(--bg-secondary) /* Fondo secundario (gris muy claro) */
var(--bg-tertiary)  /* Fondo terciario (gris claro) */
var(--bg-dark)      /* Fondo oscuro */
var(--bg-overlay)   /* Overlay semitransparente */
```

**Uso:**
```css
.card {
    background: var(--bg-primary);
}

.sidebar {
    background: var(--bg-secondary);
}

.modal-overlay {
    background: var(--bg-overlay);
}
```

---

## 📝 Colores de Texto

```css
var(--text-primary)   /* Texto principal (#111111) */
var(--text-secondary) /* Texto secundario (#6b7280) */
var(--text-tertiary)  /* Texto terciario (#9ca3af) */
var(--text-inverse)   /* Texto inverso (blanco) */
var(--text-brand)     /* Texto con color de marca */
```

**Uso:**
```css
h1, h2, h3 {
    color: var(--text-primary);
}

p {
    color: var(--text-secondary);
}

.label {
    color: var(--text-tertiary);
}

.btn-primary {
    color: var(--text-inverse);
}
```

---

## 🔲 Bordes

```css
var(--border-color)       /* Borde principal (#e5e7eb) */
var(--border-color-light) /* Borde claro (#f3f4f6) */
var(--border-color-dark)  /* Borde oscuro (#d1d5db) */
```

### Border Radius

```css
var(--border-radius)      /* 8px - Radio estándar */
var(--border-radius-sm)   /* 4px - Radio pequeño */
var(--border-radius-lg)   /* 12px - Radio grande */
var(--border-radius-full) /* 9999px - Redondo completo */
```

---

## 💫 Sombras

```css
var(--shadow-sm)  /* Sombra pequeña */
var(--shadow)     /* Sombra estándar */
var(--shadow-md)  /* Sombra media */
var(--shadow-lg)  /* Sombra grande */
var(--shadow-xl)  /* Sombra extra grande */
```

**Uso:**
```css
.card {
    box-shadow: var(--shadow);
}

.card:hover {
    box-shadow: var(--shadow-lg);
}

.modal {
    box-shadow: var(--shadow-xl);
}
```

---

## 📏 Espaciado

```css
var(--spacing-xs)  /* 0.25rem - Extra pequeño */
var(--spacing-sm)  /* 0.5rem  - Pequeño */
var(--spacing-md)  /* 1rem    - Medio */
var(--spacing-lg)  /* 1.5rem  - Grande */
var(--spacing-xl)  /* 2rem    - Extra grande */
var(--spacing-2xl) /* 3rem    - Extra extra grande */
```

**Uso:**
```css
.container {
    padding: var(--spacing-lg);
    margin-bottom: var(--spacing-xl);
}

.btn {
    padding: var(--spacing-sm) var(--spacing-lg);
}
```

---

## 🔤 Tipografía

### Font Family

```css
var(--font-sans) /* Sans-serif principal */
var(--font-mono) /* Monospace */
```

### Font Size

```css
var(--font-size-xs)   /* 0.75rem  */
var(--font-size-sm)   /* 0.875rem */
var(--font-size-base) /* 1rem     */
var(--font-size-lg)   /* 1.125rem */
var(--font-size-xl)   /* 1.25rem  */
var(--font-size-2xl)  /* 1.5rem   */
var(--font-size-3xl)  /* 1.875rem */
var(--font-size-4xl)  /* 2.25rem  */
```

### Font Weight

```css
var(--font-weight-normal)    /* 400 */
var(--font-weight-medium)    /* 500 */
var(--font-weight-semibold)  /* 600 */
var(--font-weight-bold)      /* 700 */
```

---

## ⚡ Transiciones

```css
var(--transition-fast) /* 150ms ease */
var(--transition-base) /* 200ms ease */
var(--transition-slow) /* 300ms ease */
```

**Uso:**
```css
.btn {
    transition: all var(--transition-base);
}

.link {
    transition: color var(--transition-fast);
}
```

---

## 📚 Clases Utilitarias

### Texto

```css
.text-center   /* Centrado */
.text-right    /* Derecha */
.text-left     /* Izquierda */
```

### Márgenes

```css
.mt-1, .mt-2, .mt-3, .mt-4, .mt-5  /* Margin top */
.mb-1, .mb-2, .mb-3, .mb-4, .mb-5  /* Margin bottom */
```

### Padding

```css
.p-1, .p-2, .p-3, .p-4, .p-5  /* Padding */
```

### Display

```css
.d-none     /* display: none */
.d-block    /* display: block */
.d-flex     /* display: flex */
.d-grid     /* display: grid */
```

### Flexbox

```css
.flex-column      /* flex-direction: column */
.flex-row         /* flex-direction: row */
.align-center     /* align-items: center */
.justify-center   /* justify-content: center */
.justify-between  /* justify-content: space-between */
```

### Gaps

```css
.gap-1, .gap-2, .gap-3, .gap-4, .gap-5  /* Gap spacing */
```

---

## ❌ NO HACER - Colores Hardcodeados

**INCORRECTO:**
```css
/* ❌ NO USAR COLORES HARDCODEADOS */
.button {
    background: #667eea;
    color: #fff;
    border: 1px solid #e5e7eb;
}

.text {
    color: #333;
}
```

**CORRECTO:**
```css
/* ✅ USAR VARIABLES CSS */
.button {
    background: var(--brand-primary);
    color: var(--text-inverse);
    border: 1px solid var(--border-color);
}

.text {
    color: var(--text-primary);
}
```

---

## 🎯 Ejemplos de Uso Completos

### Botón Primario

```css
.btn-primary {
    background: linear-gradient(135deg, var(--brand-primary) 0%, var(--brand-primary-dark) 100%);
    color: var(--text-inverse);
    padding: var(--spacing-sm) var(--spacing-lg);
    border-radius: var(--border-radius);
    border: none;
    font-weight: var(--font-weight-medium);
    transition: all var(--transition-base);
    box-shadow: var(--shadow);
}

.btn-primary:hover {
    transform: translateY(-2px);
    box-shadow: var(--shadow-lg);
}
```

### Card

```css
.card {
    background: var(--bg-primary);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius-lg);
    padding: var(--spacing-xl);
    box-shadow: var(--shadow);
    transition: all var(--transition-base);
}

.card:hover {
    box-shadow: var(--shadow-md);
    transform: translateY(-2px);
}

.card-title {
    color: var(--text-primary);
    font-size: var(--font-size-xl);
    font-weight: var(--font-weight-semibold);
    margin-bottom: var(--spacing-md);
}

.card-text {
    color: var(--text-secondary);
    line-height: 1.6;
}
```

### Alerta de Éxito

```css
.alert-success {
    background: var(--color-success-light);
    border-left: 4px solid var(--color-success);
    color: var(--color-success-dark);
    padding: var(--spacing-md) var(--spacing-lg);
    border-radius: var(--border-radius);
    margin-bottom: var(--spacing-md);
}
```

### Formulario

```css
.form-control {
    width: 100%;
    padding: var(--spacing-sm) var(--spacing-md);
    font-size: var(--font-size-base);
    color: var(--text-primary);
    background: var(--bg-primary);
    border: 1px solid var(--border-color);
    border-radius: var(--border-radius);
    transition: all var(--transition-fast);
}

.form-control:focus {
    outline: none;
    border-color: var(--brand-primary);
    box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
}
```

---

## 🌙 Soporte de Dark Mode

El sistema incluye soporte automático para modo oscuro usando `prefers-color-scheme`:

```css
@media (prefers-color-scheme: dark) {
    :root {
        --bg-primary: #111827;
        --bg-secondary: #1f2937;
        --text-primary: #f3f4f6;
        --text-secondary: #d1d5db;
        /* etc... */
    }
}
```

---

## 📋 Checklist de Implementación

Al crear nuevos componentes o páginas:

- [ ] Importar archivos CSS en el orden correcto
- [ ] Usar **solo** variables CSS, no colores hardcodeados
- [ ] Usar clases utilitarias cuando sea posible
- [ ] Aplicar colores semánticos apropiados
- [ ] Usar escalas de espaciado consistentes
- [ ] Aplicar transiciones para interactividad
- [ ] Usar sombras para profundidad
- [ ] Mantener jerarquía tipográfica

---

## 🔧 Mantenimiento

### Actualizar Colores Globalmente

Si necesitas cambiar un color en todo el sistema, simplemente actualiza la variable en `/static/css/variables.css`:

```css
:root {
    --brand-primary: #667eea;  /* Cambiar aquí afecta todo el sistema */
}
```

### Agregar Nuevas Variables

1. Abre `/static/css/variables.css`
2. Agrega tu variable en la sección correspondiente
3. Documenta su uso en esta guía
4. Usa la variable en tus componentes

---

## 📞 Contacto y Soporte

Para preguntas sobre la paleta de colores o el sistema de diseño, consulta este documento primero. Si tienes dudas adicionales, contacta al equipo de desarrollo.

---

**Última actualización:** Diciembre 2024  
**Versión:** 1.0.0
