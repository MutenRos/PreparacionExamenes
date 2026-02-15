# 🎪 Espectáculos Dani

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/MutenRos/ED)
[![License](https://img.shields.io/badge/license-Proprietary-red.svg)](LICENSE)
[![HTML5](https://img.shields.io/badge/HTML5-E34F26?logo=html5&logoColor=white)](https://developer.mozilla.org/es/docs/Web/HTML)
[![CSS3](https://img.shields.io/badge/CSS3-1572B6?logo=css3&logoColor=white)](https://developer.mozilla.org/es/docs/Web/CSS)
[![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?logo=javascript&logoColor=black)](https://developer.mozilla.org/es/docs/Web/JavaScript)
[![PHP](https://img.shields.io/badge/PHP-777BB4?logo=php&logoColor=white)](https://www.php.net/)

> **Sitio web oficial de Espectáculos Dani** - Empresa líder en servicios de entretenimiento, alquiler de hinchables, atracciones mecánicas, sonido profesional y más en Valencia.

---

## 📋 Tabla de Contenidos

- [Descripción](#-descripción)
- [Características](#-características)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Requisitos](#-requisitos)
- [Instalación](#-instalación)
- [Configuración](#-configuración)
- [API Reference](#-api-reference)
- [Despliegue](#-despliegue)
- [Desarrollo](#-desarrollo)
- [Licencia](#-licencia)

---

## 📝 Descripción

Espectáculos Dani es una empresa especializada en servicios de entretenimiento para eventos de todo tipo. Este repositorio contiene el código fuente del sitio web oficial, desarrollado con tecnologías web modernas siguiendo las mejores prácticas de desarrollo.

### Servicios Ofrecidos

| Servicio | Descripción |
|----------|-------------|
| 🏰 **Hinchables** | Castillos y estructuras inflables para niños y adultos |
| 💧 **Hinchables de Agua** | Atracciones acuáticas para el verano |
| 🎢 **Atracciones Mecánicas** | Toro mecánico, simuladores, etc. |
| 🎵 **Disco Móvil** | DJ y animación para fiestas |
| 🔊 **Sonido e Iluminación** | Equipos profesionales |
| 🎉 **Cañón de Espuma** | Fiestas de espuma |
| 🎭 **Escenarios** | Montaje de estructuras |
| 🪑 **Mobiliario** | Alquiler de carpas, mesas, sillas |

---

## ✨ Características

### Frontend
- ✅ **HTML5 Semántico** - Estructura accesible y SEO-friendly
- ✅ **CSS3 Moderno** - Variables CSS, Flexbox, Grid, animaciones
- ✅ **JavaScript ES6+** - Arquitectura modular con patrón Module
- ✅ **Diseño Responsive** - Mobile-first, adaptable a todos los dispositivos
- ✅ **Accesibilidad WCAG** - Roles ARIA, navegación por teclado
- ✅ **Optimización SEO** - Meta tags, Open Graph, Twitter Cards
- ✅ **Performance** - Lazy loading, preload, preconnect

### Backend
- ✅ **PHP 7.4+** - API RESTful para formularios
- ✅ **Validación Robusta** - Sanitización y validación de datos
- ✅ **Rate Limiting** - Protección contra spam
- ✅ **Logging** - Sistema de logs para debugging
- ✅ **Backup de Datos** - Almacenamiento JSON de solicitudes

### Extras
- 🥚 **Easter Egg** - ¡Descubre el código secreto! (Pista: ↑↑↓↓←→←→BA)

---

## 📁 Estructura del Proyecto

```
espectaculos-dani-web/
├── 📄 index.html              # Página principal
├── 📄 dashboard.html          # Panel de administración
├── 📄 README.md               # Este archivo
│
├── 📂 css/
│   ├── styles.css             # Estilos principales (~2000 líneas)
│   ├── services.css           # Estilos para páginas de servicios
│   └── dashboard.css          # Estilos del dashboard
│
├── 📂 js/
│   ├── app.js                 # Aplicación principal (modular, documentada)
│   └── dashboard.js           # Scripts del dashboard
│
├── 📂 servicios/
│   ├── hinchables.html        # Catálogo de hinchables
│   ├── hinchables-agua.html   # Hinchables acuáticos
│   ├── atracciones.html       # Atracciones mecánicas
│   ├── disco-movil.html       # Disco móvil
│   ├── sonido.html            # Sonido e iluminación
│   ├── canon-espuma.html      # Cañón de espuma
│   ├── escenarios.html        # Escenarios
│   └── mobiliario.html        # Mobiliario
│
├── 📂 api/
│   └── contact.php            # API de contacto
│
├── 📂 assets/
│   ├── images/                # Imágenes del sitio
│   └── icons/                 # Iconos y favicons
│
├── 📂 data/                   # Datos generados (gitignore)
│   └── requests.json          # Solicitudes de contacto
│
└── 📂 logs/                   # Logs del sistema (gitignore)
    └── contact_YYYY-MM.log    # Logs mensuales
```

---

## 📋 Requisitos

### Servidor de Producción
- **PHP** >= 7.4
- **Apache** >= 2.4 o **Nginx** >= 1.18
- Extensiones PHP: `json`, `mbstring`, `filter`
- Función `mail()` habilitada

### Desarrollo Local
- Navegador moderno (Chrome, Firefox, Safari, Edge)
- Servidor local (Live Server, PHP built-in, XAMPP, etc.)
- Git >= 2.0

---

## 🚀 Instalación

### 1. Clonar el repositorio

```bash
git clone https://github.com/MutenRos/ED.git espectaculos-dani-web
cd espectaculos-dani-web
```

### 2. Configurar servidor local

#### Opción A: PHP Built-in Server
```bash
php -S localhost:8000
```

#### Opción B: VS Code Live Server
Instalar extensión "Live Server" y click en "Go Live".

#### Opción C: XAMPP/WAMP/MAMP
Copiar proyecto a `htdocs` o `www`.

### 3. Crear directorios necesarios

```bash
mkdir -p data logs
```

### 4. Verificar instalación

Abrir `http://localhost:8000` en el navegador.

---

## ⚙️ Configuración

### Backend (API)

Editar constantes en `api/contact.php`:

```php
define('CONFIG', [
    'email_to' => 'tu-email@tudominio.com',
    'email_from' => 'noreply@tudominio.com',
    'email_from_name' => 'Tu Empresa Web',
    'rate_limit' => 5, // máx solicitudes/hora/IP
]);
```

### Variables CSS

En `css/styles.css`:

```css
:root {
    --color-primary: #ff6b35;
    --color-secondary: #2d3436;
    --color-accent: #00b894;
}
```

---

## 📡 API Reference

### POST /api/contact.php

Procesa el formulario de contacto.

#### Request

```json
{
    "nombre": "string (requerido)",
    "email": "string (requerido)", 
    "telefono": "string (opcional)",
    "servicio": "hinchables|atracciones|disco|sonido|espuma|escenarios|mobiliario|otro",
    "fecha": "YYYY-MM-DD (opcional)",
    "mensaje": "string (requerido, 10-1000 chars)",
    "llamar": "boolean (opcional)"
}
```

#### Response (200 OK)

```json
{
    "success": true,
    "message": "Tu mensaje ha sido enviado correctamente.",
    "timestamp": "2024-01-15T10:30:00+01:00"
}
```

#### Response (422 Validation Error)

```json
{
    "success": false,
    "message": "Por favor, corrige los errores del formulario.",
    "data": { "errors": { "email": "El email no es válido" } }
}
```

---

## 🌐 Despliegue

### GitHub Pages (Frontend estático)

1. Ve a Settings > Pages en GitHub
2. Selecciona branch `main` y folder `/root`
3. Tu sitio estará en: **https://mutenros.github.io/ED/**

> ⚠️ **Nota:** GitHub Pages solo sirve archivos estáticos. El backend PHP requiere un servidor con PHP.

### Servidor con PHP

1. Subir archivos por FTP/SFTP
2. Configurar emails en `api/contact.php`
3. Crear directorios `data/` y `logs/` con permisos 755
4. Verificar que `mail()` funcione

---

## 🛠️ Desarrollo

### Arquitectura JavaScript

```javascript
// Namespaces en window.EspectaculosDani
{
    CONFIG,      // Configuración global
    Utils,       // Utilidades (debounce, throttle)
    DOM,         // Cache de elementos
    Navigation,  // Menú móvil
    Gallery,     // Lightbox
    Forms,       // Validación
    Animations,  // Scroll animations
    App          // Inicializador
}
```

### Convenciones

| Lenguaje | Estilo |
|----------|--------|
| HTML | Semántico, ARIA, 4 espacios |
| CSS | BEM, variables, mobile-first |
| JavaScript | ES6+, JSDoc, camelCase |
| PHP | PSR-12, type hints |

---

## 📄 Licencia

**© 2024 Espectáculos Dani. Todos los derechos reservados.**

Este proyecto es propiedad privada. No se permite su uso comercial sin autorización.

---

## 📞 Contacto

- 🌐 Web: [espectaculosdani.es](https://espectaculosdani.es)
- 📧 Email: info@espectaculosdani.com
- 📍 Valencia, España

---

<div align="center">
    <sub>Desarrollado con ❤️ por Espectáculos Dani</sub>
</div>
