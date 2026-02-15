# 🎮 MutenRos Portfolio

<div align="center">

![Synthwave](https://img.shields.io/badge/Theme-Synthwave-ff6b9d?style=for-the-badge)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=for-the-badge&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=for-the-badge&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=for-the-badge&logo=javascript&logoColor=black)
![PHP](https://img.shields.io/badge/PHP-777BB4?style=for-the-badge&logo=php&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)

**Portfolio personal con estética Synthwave/Retrowave**

[Ver Demo](https://mutenros.github.io) · [Reportar Bug](https://github.com/MutenRos/MutenRos.github.io/issues)

</div>

---

## ✨ Características

- 🌅 **Estética Synthwave** - Fondo animado con sol, grid y montañas
- 🎭 **Easter Egg Matrix** - Secuencia Konami Code (↑↑↓↓←→←→BA)
- 📱 **Diseño Responsive** - Adaptable a todos los dispositivos
- ⚡ **Rendimiento Optimizado** - Lazy loading, debounce, throttle
- ♿ **Accesible** - ARIA labels, navegación por teclado
- 🔗 **Integración GitHub API** - Muestra repositorios en tiempo real
- 📧 **Formulario de Contacto** - API PHP con validación

---

## 🏗️ Estructura del Proyecto

```
portfolio/
├── 📁 assets/
│   ├── 📁 css/                    # Estilos modularizados
│   │   ├── variables.css          # Variables CSS
│   │   ├── base.css               # Reset y base
│   │   ├── background.css         # Fondo animado
│   │   ├── layout.css             # Estructura
│   │   ├── components.css         # Componentes
│   │   ├── sections.css           # Secciones
│   │   └── main.css               # Entry point
│   │
│   └── 📁 js/
│       ├── config.js              # Configuración
│       ├── main.js                # Entry point
│       └── 📁 modules/
│           ├── utils.js           # Utilidades
│           ├── background.js      # Efectos fondo
│           ├── navigation.js      # Navegación
│           ├── projects.js        # GitHub API
│           └── matrix-easter-egg.js
│
├── 📁 api/
│   └── contact.php                # API de contacto
│
├── 📁 scripts/
│   └── github_stats.py            # Generador de stats
│
├── 📁 docs/
│   ├── ARCHITECTURE.md            # Arquitectura
│   └── API.md                     # Documentación API
│
├── 📁 cache/                      # Cache de datos
├── index.html                     # Página principal
└── README.md                      # Este archivo
```

---

## 🚀 Instalación

### Requisitos Previos

- Navegador moderno (Chrome, Firefox, Safari, Edge)
- Para desarrollo: Node.js (opcional), PHP 7.4+, Python 3.8+

### Uso Local

1. **Clonar el repositorio**
   ```bash
   git clone https://github.com/MutenRos/MutenRos.github.io.git
   cd MutenRos.github.io
   ```

2. **Iniciar servidor local**
   ```bash
   # Con Python
   python -m http.server 8000
   
   # Con PHP
   php -S localhost:8000
   
   # Con Node.js (npx)
   npx serve
   ```

3. **Abrir en navegador**
   ```
   http://localhost:8000
   ```

---

## ⚙️ Configuración

### Configuración JavaScript

Editar `assets/js/config.js`:

```javascript
export const CONFIG = Object.freeze({
    github: {
        username: 'TU_USUARIO',
        reposPerPage: 10
    },
    // ...
});
```

### Configuración PHP (API Contacto)

Editar `api/contact.php`:

```php
$CONFIG = [
    'email' => [
        'to' => 'tu-email@example.com',
        'from' => 'noreply@tu-dominio.com'
    ],
    'allowed_origins' => [
        'https://tu-dominio.com'
    ]
];
```

### Generar Cache de GitHub (Python)

```bash
# Instalar dependencias
pip install requests python-dotenv

# Ejecutar script
python scripts/github_stats.py --output cache/github_stats.json

# Con verbose
python scripts/github_stats.py -v --no-cache
```

---

## 🎨 Personalización

### Colores (CSS Variables)

Editar `assets/css/variables.css`:

```css
:root {
    --color-primary: #ff6b9d;     /* Rosa neón */
    --color-secondary: #00d4ff;   /* Cyan */
    --color-accent: #a855f7;      /* Púrpura */
    --color-bg-dark: #0a0a0f;     /* Fondo oscuro */
}
```

### Agregar Proyectos Privados

Editar `assets/js/config.js`:

```javascript
privateProjects: [
    {
        name: 'mi-proyecto',
        description: 'Descripción del proyecto',
        language: 'Python',
        stars: 0,
        repoUrl: 'https://github.com/usuario/repo',
        demoUrl: 'https://demo.com'
    }
]
```

---

## 🎮 Easter Egg

El portfolio incluye un Easter Egg inspirado en Matrix. Para activarlo:

1. Presiona la secuencia Konami Code: `↑ ↑ ↓ ↓ ← → ← → B A`
2. Disfruta la experiencia 🐇

---

## 📚 Documentación

- [Arquitectura del Proyecto](docs/ARCHITECTURE.md)
- [Documentación de API](docs/API.md)

---

## 🛠️ Stack Tecnológico

| Tecnología | Uso |
|------------|-----|
| **HTML5** | Estructura semántica, accesibilidad |
| **CSS3** | Diseño, animaciones, responsive |
| **JavaScript ES6+** | Módulos, clases, async/await |
| **PHP 7.4+** | API de contacto, validación |
| **Python 3.8+** | Scripts de utilidad, caché |

---

## 🤝 Contribuir

1. Fork el proyecto
2. Crear rama (`git checkout -b feature/nueva-caracteristica`)
3. Commit cambios (`git commit -m 'Añadir característica'`)
4. Push a la rama (`git push origin feature/nueva-caracteristica`)
5. Abrir Pull Request

---

## 📄 Licencia

Este proyecto está bajo la Licencia MIT - ver [LICENSE](LICENSE) para detalles.

---

## 👤 Autor

**Dario (MutenRos)**

- GitHub: [@MutenRos](https://github.com/MutenRos)
- LinkedIn: [Perfil](https://linkedin.com/in/tu-perfil)

---

<div align="center">

Hecho con ❤️ y mucho ☕

⭐ Si te gustó, dale una estrella ⭐

</div>
