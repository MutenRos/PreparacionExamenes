# Guía de Componentes CSS

Esta guía documenta todos los componentes CSS disponibles en el sistema de diseño de Bombas Ideal.

---

## Índice

1. [Botones](#botones)
2. [Navegación](#navegación)
3. [Hero / Slider](#hero--slider)
4. [Cards](#cards)
5. [Formularios](#formularios)
6. [Secciones](#secciones)
7. [Modales](#modales)
8. [Footer](#footer)
9. [BIPS](#bips)

---

## Botones

**Archivo:** `src/css/components/buttons.css`

### Uso Básico

```html
<button class="btn btn-primary">Botón primario</button>
<a href="#" class="btn btn-secondary">Enlace secundario</a>
```

### Variantes

| Clase | Descripción |
|-------|-------------|
| `.btn-primary` | Fondo azul, texto blanco |
| `.btn-secondary` | Fondo cyan, texto oscuro |
| `.btn-outline` | Borde azul, fondo transparente |
| `.btn-ghost` | Sin fondo ni borde |
| `.btn-danger` | Fondo rojo |
| `.btn-success` | Fondo verde |
| `.btn-bips` | Degradado especial BIPS |

### Tamaños

| Clase | Padding |
|-------|---------|
| `.btn-sm` | Pequeño |
| `.btn` | Normal (default) |
| `.btn-lg` | Grande |
| `.btn-xl` | Extra grande |

### Modificadores

```html
<!-- Ancho completo -->
<button class="btn btn-primary btn-block">Ancho completo</button>

<!-- Con icono -->
<button class="btn btn-primary btn-icon">
    <i class="fas fa-download"></i>
    Descargar
</button>

<!-- Solo icono -->
<button class="btn btn-primary btn-icon-only">
    <i class="fas fa-search"></i>
</button>

<!-- Estado loading -->
<button class="btn btn-primary btn-loading">
    <span class="btn-spinner"></span>
    Cargando...
</button>
```

---

## Navegación

**Archivo:** `src/css/components/navbar.css`

### Estructura

```html
<div class="top-bar">
    <div class="container">
        <div class="top-bar-left">...</div>
        <div class="top-bar-right">...</div>
    </div>
</div>

<nav class="navbar">
    <div class="nav-container">
        <a href="/" class="logo">
            <img src="logo.png" class="logo-img" alt="Bombas Ideal">
        </a>
        
        <ul class="nav-menu">
            <li><a href="#" class="nav-link">Inicio</a></li>
            <li class="has-dropdown">
                <a href="#" class="nav-link">Productos <i class="fa fa-chevron-down"></i></a>
                <div class="dropdown-menu">
                    <a href="#">Subitem 1</a>
                    <a href="#">Subitem 2</a>
                </div>
            </li>
            <li><a href="bips.html" class="nav-link bips-link">BIPS</a></li>
        </ul>
        
        <div class="nav-actions">
            <a href="tel:+34936525366" class="nav-phone">
                <i class="fas fa-phone"></i>
                <span>936 525 366</span>
            </a>
        </div>
        
        <div class="hamburger">
            <span></span>
            <span></span>
            <span></span>
        </div>
    </div>
</nav>
```

### Estados

- `.navbar.scrolled` - Se añade cuando hay scroll
- `.nav-menu.active` - Menú móvil abierto
- `.hamburger.active` - Hamburger en X
- `.top-bar.hidden` - Top bar oculto

---

## Hero / Slider

**Archivo:** `src/css/components/hero.css`

### Estructura

```html
<section class="hero">
    <div class="hero-slider">
        <div class="slide active">
            <img src="slide1.jpg" class="slide-bg" alt="">
            <div class="slide-content">
                <h1 class="slide-title">
                    Bombas <span class="highlight">Ideal</span>
                </h1>
                <p class="slide-subtitle">Descripción del slide</p>
                <div class="slide-actions">
                    <a href="#" class="btn btn-primary">Acción principal</a>
                    <a href="#" class="btn btn-outline">Acción secundaria</a>
                </div>
            </div>
        </div>
        <!-- Más slides... -->
    </div>
    
    <div class="slider-controls">
        <button class="slider-btn slider-btn-prev"></button>
        <button class="slider-btn slider-btn-next"></button>
    </div>
    
    <div class="slider-indicators">
        <button class="indicator active"></button>
        <button class="indicator"></button>
    </div>
</section>
```

### Variantes

| Clase | Descripción |
|-------|-------------|
| `.hero--static` | Sin slider, imagen fija |
| `.hero--small` | Altura reducida (páginas internas) |

---

## Cards

**Archivo:** `src/css/components/cards.css`

### Card Básica

```html
<div class="card">
    <div class="card-image">
        <img src="imagen.jpg" alt="">
        <span class="card-badge">Nuevo</span>
    </div>
    <div class="card-body">
        <span class="card-category">Categoría</span>
        <h3 class="card-title">Título de la card</h3>
        <p class="card-text">Descripción de la card...</p>
    </div>
    <div class="card-footer">
        <a href="#" class="btn btn-primary btn-sm">Ver más</a>
    </div>
</div>
```

### Variantes

| Clase | Descripción |
|-------|-------------|
| `.card--product` | Tarjeta de producto |
| `.card--service` | Tarjeta de servicio con icono |
| `.card--news` | Tarjeta de noticia |
| `.card--horizontal` | Layout horizontal |
| `.card--featured` | Con borde destacado |
| `.card--clickable` | Toda la card es clickeable |

### Grid de Cards

```html
<div class="card-grid card-grid--3">
    <div class="card">...</div>
    <div class="card">...</div>
    <div class="card">...</div>
</div>
```

---

## Formularios

**Archivo:** `src/css/components/forms.css`

### Estructura

```html
<form class="form">
    <div class="form-group">
        <label class="form-label form-label--required">Campo</label>
        <input type="text" class="form-control" placeholder="Placeholder">
        <span class="form-hint">Texto de ayuda</span>
    </div>
</form>
```

### Tipos de Input

```html
<!-- Input normal -->
<input type="text" class="form-control">

<!-- Con icono -->
<div class="input-group">
    <i class="input-group-icon fas fa-user"></i>
    <input type="text" class="form-control">
</div>

<!-- Select -->
<select class="form-control form-select">
    <option>Opción 1</option>
</select>

<!-- Textarea -->
<textarea class="form-control" rows="4"></textarea>

<!-- Checkbox -->
<label class="form-check">
    <input type="checkbox" class="form-check-input">
    <span class="form-check-label">Acepto los términos</span>
</label>

<!-- Switch -->
<label class="form-switch">
    <input type="checkbox" class="form-switch-input">
    <span>Activar notificaciones</span>
</label>
```

### Estados de Validación

```html
<input type="text" class="form-control is-valid">
<input type="text" class="form-control is-invalid">
<span class="form-feedback form-feedback--invalid">Error message</span>
```

### Layout Grid

```html
<form class="form form--grid">
    <div class="form-group">...</div>
    <div class="form-group">...</div>
    <div class="form-group form-group--full">...</div>
</form>
```

---

## Secciones

**Archivo:** `src/css/components/sections.css`

### Estructura Básica

```html
<section class="section">
    <div class="container">
        <div class="section-header">
            <span class="section-subtitle">Subtítulo</span>
            <h2 class="section-title">Título de la sección</h2>
            <p class="section-description">Descripción...</p>
        </div>
        
        <!-- Contenido -->
    </div>
</section>
```

### Variantes de Fondo

| Clase | Descripción |
|-------|-------------|
| `.section--gray` | Fondo gris claro |
| `.section--dark` | Fondo oscuro, texto claro |
| `.section--primary` | Fondo degradado azul |
| `.section--gradient` | Degradado personalizado |

### Tamaños de Padding

| Clase | Padding vertical |
|-------|-----------------|
| `.section--sm` | Reducido |
| `.section` | Normal (default) |
| `.section--lg` | Aumentado |

### Tipos de Sección

- **Features Grid** - Grid de características/servicios
- **About** - Imagen + texto
- **Stats** - Estadísticas/números
- **CTA** - Call to action
- **Testimonials** - Grid de testimonios
- **Partners** - Logos de partners

---

## Modales

**Archivo:** `src/css/components/modals.css`

### Estructura

```html
<div class="modal" id="myModal">
    <div class="modal-overlay"></div>
    <div class="modal-container">
        <div class="modal-header">
            <h3 class="modal-title">Título</h3>
            <button class="modal-close" data-modal-close>&times;</button>
        </div>
        <div class="modal-body">
            <!-- Contenido -->
        </div>
        <div class="modal-footer">
            <button class="btn btn-secondary" data-modal-close>Cancelar</button>
            <button class="btn btn-primary">Confirmar</button>
        </div>
    </div>
</div>
```

### Tamaños

| Clase | Max-width |
|-------|-----------|
| `.modal--sm` | 400px |
| `.modal` | 500px (default) |
| `.modal--lg` | 700px |
| `.modal--xl` | 900px |
| `.modal--full` | 95vw |

### Variantes

| Clase | Descripción |
|-------|-------------|
| `.modal--confirm` | Modal de confirmación centrado |
| `.modal--gallery` | Para galería de imágenes |

### Animaciones

| Clase | Animación |
|-------|-----------|
| `.modal--slide-down` | Entra desde arriba |
| `.modal--slide-up` | Entra desde abajo |
| `.modal--zoom` | Efecto zoom |

---

## Footer

**Archivo:** `src/css/components/footer.css`

### Estructura

```html
<footer class="footer">
    <div class="container">
        <div class="footer-main">
            <div class="footer-brand">
                <a href="/" class="footer-logo">
                    <img src="logo.png" alt="Bombas Ideal">
                </a>
                <p class="footer-description">...</p>
                <div class="footer-social">
                    <a href="#" class="linkedin"><i class="fab fa-linkedin"></i></a>
                    <a href="#" class="youtube"><i class="fab fa-youtube"></i></a>
                </div>
            </div>
            
            <div class="footer-links">
                <h4 class="footer-links-title">Enlaces</h4>
                <ul class="footer-links-list">
                    <li><a href="#">Enlace 1</a></li>
                </ul>
            </div>
            
            <div class="footer-contact">
                <h4 class="footer-links-title">Contacto</h4>
                <div class="footer-contact-list">
                    <div class="footer-contact-item">
                        <div class="footer-contact-icon"><i class="fas fa-phone"></i></div>
                        <div class="footer-contact-text">
                            <strong>Teléfono</strong>
                            +34 936 525 366
                        </div>
                    </div>
                </div>
            </div>
            
            <div class="footer-newsletter">
                <h4 class="footer-links-title">Newsletter</h4>
                <form class="newsletter-form">
                    <input type="email" placeholder="Tu email">
                    <button class="btn btn-primary">Suscribir</button>
                </form>
            </div>
        </div>
        
        <div class="footer-bottom">
            <p class="footer-copyright">
                © 2024 Bombas Ideal S.A. Todos los derechos reservados.
            </p>
            <div class="footer-legal">
                <a href="#">Aviso Legal</a>
                <a href="#">Privacidad</a>
            </div>
        </div>
    </div>
</footer>

<!-- Botón scroll to top -->
<button class="scroll-top">
    <i class="fas fa-arrow-up"></i>
</button>
```

---

## BIPS

**Archivo:** `src/css/components/bips.css`

### Estructura Principal

```html
<div class="bips-container">
    <div class="bips-header">
        <h1 class="bips-title">Selector de Bombas</h1>
        <p class="bips-subtitle">Encuentra la bomba ideal...</p>
    </div>
    
    <div class="bips-layout">
        <aside class="bips-sidebar">
            <div class="bips-panel">
                <div class="bips-panel-header">
                    <i class="fas fa-sliders-h"></i>
                    <h3>Parámetros</h3>
                </div>
                <div class="bips-panel-body">
                    <!-- Formulario de filtros -->
                </div>
            </div>
        </aside>
        
        <main class="bips-results">
            <!-- Resultados -->
        </main>
    </div>
</div>
```

### Estados

```html
<!-- Loading -->
<div class="bips-loading">
    <div class="bips-loading-spinner"></div>
    <p class="bips-loading-text">Buscando productos...</p>
</div>

<!-- Empty -->
<div class="bips-empty">
    <div class="bips-empty-icon">🔍</div>
    <h3 class="bips-empty-title">Sin resultados</h3>
    <p class="bips-empty-text">Ajusta los parámetros...</p>
</div>

<!-- Initial -->
<div class="bips-initial">
    <div class="bips-initial-icon">💧</div>
    <h3 class="bips-initial-title">Introduce tus parámetros</h3>
</div>
```

---

## Utilidades

**Archivo:** `src/css/utilities.css`

### Contenedores

```html
<div class="container">Max 1280px, centrado</div>
<div class="container-sm">Max 640px</div>
<div class="container-lg">Max 1024px</div>
<div class="container-xl">Max 1280px</div>
<div class="container-full">100% width</div>
```

### Flexbox

```html
<div class="flex">Display flex</div>
<div class="flex items-center justify-between">Alineado</div>
<div class="flex-col gap-4">Columna con gap</div>
```

### Espaciado

```html
<div class="m-4">Margin 16px</div>
<div class="p-8">Padding 32px</div>
<div class="mt-4 mb-8">Margin top/bottom</div>
```

### Texto

```html
<p class="text-center">Centrado</p>
<p class="text-sm text-muted">Pequeño y gris</p>
<h2 class="text-2xl font-bold">Grande y bold</h2>
```
