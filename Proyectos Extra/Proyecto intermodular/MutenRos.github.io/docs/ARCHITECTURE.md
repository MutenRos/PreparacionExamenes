# 🏗️ Arquitectura del Proyecto

## Visión General

Este portfolio utiliza una arquitectura modular y escalable, separando claramente las responsabilidades entre capas.

```
┌─────────────────────────────────────────────────────────────┐
│                        FRONTEND                              │
│  ┌──────────┐  ┌───────────┐  ┌────────────────────────┐   │
│  │   HTML   │  │    CSS    │  │      JavaScript        │   │
│  │ Semantic │  │  Modular  │  │      ES6 Modules       │   │
│  └──────────┘  └───────────┘  └────────────────────────┘   │
└─────────────────────────┬───────────────────────────────────┘
                          │
┌─────────────────────────▼───────────────────────────────────┐
│                        BACKEND                               │
│  ┌──────────────────┐  ┌──────────────────────────────┐    │
│  │   PHP API        │  │      Python Scripts          │    │
│  │  (Contact Form)  │  │   (GitHub Stats Cache)       │    │
│  └──────────────────┘  └──────────────────────────────┘    │
└─────────────────────────────────────────────────────────────┘
```

## Estructura de Directorios

```
portfolio/
├── 📁 assets/              # Recursos estáticos
│   ├── 📁 css/            # Estilos modularizados
│   │   ├── variables.css  # Variables CSS (colores, tipografía)
│   │   ├── base.css       # Reset y estilos base
│   │   ├── background.css # Fondo synthwave animado
│   │   ├── layout.css     # Estructura (header, footer)
│   │   ├── components.css # Componentes reutilizables
│   │   ├── sections.css   # Estilos por sección
│   │   └── main.css       # Punto de entrada CSS
│   │
│   └── 📁 js/             # JavaScript modular
│       ├── config.js      # Configuración centralizada
│       ├── main.js        # Punto de entrada JS
│       └── 📁 modules/    # Módulos ES6
│           ├── utils.js           # Utilidades
│           ├── background.js      # Efectos de fondo
│           ├── navigation.js      # Navegación
│           ├── projects.js        # Integración GitHub
│           └── matrix-easter-egg.js # Easter egg
│
├── 📁 api/                 # Backend PHP
│   └── contact.php        # API de contacto
│
├── 📁 scripts/             # Scripts de utilidad
│   └── github_stats.py    # Generador de estadísticas
│
├── 📁 cache/               # Archivos de caché
│   └── github_stats.json  # Caché de repositorios
│
├── 📁 docs/                # Documentación
│   ├── ARCHITECTURE.md    # Este archivo
│   └── API.md             # Documentación de API
│
├── index.html             # Página principal
└── README.md              # Documentación general
```

## Capas de la Aplicación

### 1. Capa de Presentación (HTML)

**Archivo:** `index.html`

- HTML5 semántico con elementos como `<header>`, `<main>`, `<section>`, `<article>`
- Atributos ARIA para accesibilidad
- Meta tags optimizados para SEO
- Preconnect para recursos externos
- Estructura de clases BEM

```html
<section class="section projects" id="projects" aria-label="Proyectos">
    <article class="project-card" aria-labelledby="project-title-1">
        <!-- Contenido del proyecto -->
    </article>
</section>
```

### 2. Capa de Estilos (CSS)

**Directorio:** `assets/css/`

#### Arquitectura ITCSS Modificada

1. **Settings** (`variables.css`)
   - Variables CSS personalizadas
   - Paleta de colores synthwave
   - Escala tipográfica
   - Espaciado y breakpoints

2. **Generic** (`base.css`)
   - Reset CSS moderno
   - Estilos de elementos base
   - Clases de utilidad

3. **Components** (`components.css`)
   - Botones, tarjetas, enlaces
   - Estados hover/focus/active
   - Transiciones

4. **Layout** (`layout.css`)
   - Header y navegación
   - Footer
   - Sistema de grid

5. **Sections** (`sections.css`)
   - Hero, About, Skills
   - Projects, Contact

6. **Trumps** (`background.css`)
   - Efectos visuales especiales
   - Animaciones del fondo

### 3. Capa de Lógica (JavaScript)

**Directorio:** `assets/js/`

#### Patrón de Módulos ES6

```javascript
// Cada módulo exporta una clase principal
export class Navigation {
    constructor() { /* ... */ }
    init() { /* ... */ }
}

// El punto de entrada orquesta todos los módulos
import { Navigation } from './modules/navigation.js';
const nav = new Navigation();
nav.init();
```

#### Módulos Principales

| Módulo | Responsabilidad |
|--------|-----------------|
| `config.js` | Configuración centralizada (inmutable) |
| `utils.js` | Funciones de utilidad |
| `background.js` | Efectos visuales del fondo |
| `navigation.js` | Scroll suave, menú activo |
| `projects.js` | Fetch de repos, renderizado |
| `matrix-easter-egg.js` | Easter egg Konami code |

### 4. Capa de Backend (PHP)

**Directorio:** `api/`

#### API REST para Contacto

```
POST /api/contact.php
Content-Type: application/json

{
    "name": "string",
    "email": "string", 
    "subject": "string",
    "message": "string"
}
```

**Características:**
- Validación de entrada
- Rate limiting (5 req/hora/IP)
- Sanitización contra XSS
- Logging de submissions
- CORS configurado

### 5. Capa de Scripts (Python)

**Directorio:** `scripts/`

#### GitHub Stats Generator

```bash
python scripts/github_stats.py --output cache/github_stats.json
```

**Características:**
- Fetch de repositorios vía API
- Caché de resultados (1 hora)
- Cálculo de estadísticas agregadas
- Soporte para token autenticado

## Flujo de Datos

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│   Usuario   │────>│   Browser    │────>│  index.html │
└─────────────┘     └──────────────┘     └──────┬──────┘
                                                 │
                    ┌────────────────────────────┼────────────────┐
                    │                            │                │
                    ▼                            ▼                ▼
            ┌───────────┐              ┌─────────────┐    ┌───────────┐
            │  main.css │              │   main.js   │    │ config.js │
            └─────┬─────┘              └──────┬──────┘    └─────┬─────┘
                  │                           │                 │
    ┌─────────────┼─────────────┐            │                 │
    │    @import chain          │            │                 │
    ▼    ▼    ▼    ▼    ▼    ▼ │            ▼                 │
┌──────┬────┬────┬────┬────┬───┘     ┌─────────────┐          │
│vars  │base│bg  │lay │comp│sect│     │   Modules   │◄─────────┘
└──────┴────┴────┴────┴────┴────┘     └──────┬──────┘
                                             │
                    ┌────────────────────────┼───────────────────┐
                    │                        │                   │
                    ▼                        ▼                   ▼
           ┌────────────┐          ┌─────────────┐      ┌────────────┐
           │ background │          │  projects   │      │    API     │
           └────────────┘          └──────┬──────┘      │ (contact)  │
                                          │             └────────────┘
                                          ▼
                                   ┌─────────────┐
                                   │  GitHub API │
                                   └─────────────┘
```

## Patrones de Diseño Utilizados

### 1. Singleton (Configuración)
```javascript
// config.js - Objeto inmutable
export const CONFIG = Object.freeze({
    github: { /* ... */ }
});
```

### 2. Module Pattern (ES6)
```javascript
// Cada archivo es un módulo con scope propio
export class MyModule { /* ... */ }
```

### 3. Observer (Scroll Events)
```javascript
// navigation.js - Observa scroll para actualizar UI
window.addEventListener('scroll', throttle(updateActiveSection, 100));
```

### 4. Factory (Creación de elementos)
```javascript
// utils.js
export function createElement(tag, className, content) { /* ... */ }
```

## Consideraciones de Rendimiento

1. **CSS Critical Path**: Estilos inline para above-the-fold
2. **Lazy Loading**: Imágenes con `loading="lazy"`
3. **Debounce/Throttle**: Eventos de scroll optimizados
4. **Preconnect**: DNS prefetch para GitHub API
5. **Cache Python**: Reduce llamadas a GitHub API

## Seguridad

1. **XSS Prevention**: Escape de HTML en contenido dinámico
2. **CORS**: Headers configurados en PHP
3. **Rate Limiting**: Protección contra abuso
4. **Input Validation**: Validación server-side
5. **Content Security Policy**: Headers de seguridad

## Accesibilidad (A11y)

1. **ARIA Labels**: En secciones y elementos interactivos
2. **Skip Links**: Navegación por teclado
3. **Focus Visible**: Indicadores de foco claros
4. **Screen Reader Only**: Clase `.sr-only`
5. **Reduced Motion**: Respeta preferencias del usuario

## Testing

### Manual
1. Verificar navegación en todos los navegadores
2. Probar formulario de contacto
3. Verificar responsividad
4. Testear easter egg (↑↑↓↓←→←→BA)

### Automatizado (Futuro)
- Lighthouse para performance/a11y
- Jest para JavaScript
- PHPUnit para API
