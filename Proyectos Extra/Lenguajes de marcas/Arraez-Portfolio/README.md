# Portfolio Arte y Diseño 3D

Portfolio web moderno y responsive para mostrar trabajos de arte y diseño 3D. Optimizado para GitHub Pages.

## 🚀 Vista Previa

Abre `index.html` en tu navegador para ver el portfolio.

## 📁 Estructura del Proyecto

```
PortfolioArraez/
├── index.html          # Página principal
├── css/
│   └── styles.css      # Estilos y tema oscuro
├── js/
│   └── main.js         # Interactividad y animaciones
├── assets/
│   └── images/         # Imágenes del portfolio
└── README.md           # Este archivo
```

## ✨ Características

- 🎨 **Tema Oscuro** - Diseño elegante con gradientes morados/rosas
- 📱 **Responsive** - Se adapta a móviles, tablets y desktop
- ⚡ **Animaciones** - Efectos suaves al hacer scroll
- 🖼️ **Galería Filtrable** - Filtra proyectos por categoría
- 📧 **Formulario de Contacto** - Listo para integrar con servicios
- 🔍 **SEO Friendly** - Meta tags optimizados

## 🛠️ Personalización

### Cambiar información personal

1. Abre `index.html`
2. Busca y reemplaza:
   - `Tu Nombre` por tu nombre real
   - `tu@email.com` por tu email
   - Actualiza los enlaces de redes sociales

### Agregar tus proyectos

1. Coloca tus imágenes en `assets/images/`
2. En `index.html`, reemplaza los `<div class="placeholder-image">` por:
   ```html
   <img src="assets/images/tu-proyecto.jpg" alt="Descripción del proyecto">
   ```

### Cambiar colores

En `css/styles.css`, modifica las variables CSS:
```css
:root {
    --color-accent: #8b5cf6;        /* Color principal */
    --color-gradient-start: #8b5cf6; /* Inicio del gradiente */
    --color-gradient-end: #ec4899;   /* Fin del gradiente */
}
```

## 🌐 Despliegue en GitHub Pages

1. **Crear repositorio en GitHub**
   ```bash
   git init
   git add .
   git commit -m "Portfolio inicial"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
   git push -u origin main
   ```

2. **Activar GitHub Pages**
   - Ve a tu repositorio en GitHub
   - Settings → Pages
   - Source: selecciona `main` y `/ (root)`
   - Save

3. **¡Listo!** Tu portfolio estará en:
   `https://TU_USUARIO.github.io/TU_REPOSITORIO`

## 📧 Configurar Formulario de Contacto

Para que el formulario envíe emails reales, puedes usar:

### Opción 1: Formspree (Recomendado)
1. Crea cuenta en [formspree.io](https://formspree.io)
2. Cambia el form en `index.html`:
   ```html
   <form action="https://formspree.io/f/TU_ID" method="POST">
   ```

### Opción 2: EmailJS
1. Crea cuenta en [emailjs.com](https://www.emailjs.com)
2. Sigue su documentación para integrar con JavaScript

## 📝 Licencia

Este proyecto es de uso libre para fines personales y educativos.

---

Hecho con 💜 para el mundo del arte 3D
