# Marc Arraez Ortigosa — Portfolio de Concept Art y Modelado 3D

![Portfolio](assets/images/Retrato_relajado_de_un_joven.png)

## Introducción

Portfolio profesional de Marc Arraez Ortigosa, un artista digital especializado en Concept Art y Modelado de Personajes 3D. Esta web single-page presenta sus trabajos, habilidades y datos de contacto en una experiencia visual inmersiva construida con HTML5, CSS3 y JavaScript vanilla. El diseño oscuro con acentos violeta/rosa refleja la estética del arte digital y los videojuegos, creando una primera impresión impactante para cualquier reclutador o cliente potencial.

---

## Desarrollo de las partes

### 1. Estructura HTML Semántica y SEO

El proyecto se articula en un único archivo HTML con secciones semánticas claramente diferenciadas: navegación, hero, portfolio, sobre mí, habilidades, contacto y footer. Se incluyen meta tags de Open Graph para optimizar la presencia en redes sociales y atributos ARIA para accesibilidad.

```html
<!-- index.html, líneas 1-14 — Head con meta tags SEO y OG -->
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Marc Arraez Ortigosa | Arte y Diseño 3D</title>
<meta name="description" content="Portfolio de Marc Arraez Ortigosa - Concept Art y Modelado de Personajes 3D">
<meta property="og:title" content="Marc Arraez Ortigosa | Arte y Diseño 3D">
<meta property="og:description" content="Portfolio profesional de Concept Art y Modelado de Personajes 3D">
```

La navegación utiliza una estructura `<nav>` con atributos `role` y `aria-label` para lectores de pantalla, y el botón hamburger para dispositivos móviles con `aria-label="Toggle navigation"`.

```html
<!-- index.html, líneas 16-34 — Navegación accesible -->
<nav class="navbar" role="navigation" aria-label="Navegación principal">
    <a href="#" class="logo">PORTFOLIO</a>
    <button class="nav-toggle" aria-label="Toggle navigation">
        <span></span><span></span><span></span>
    </button>
    <ul class="nav-menu">
        <li><a href="#inicio" class="nav-link">Inicio</a></li>
        <li><a href="#portfolio" class="nav-link">Portfolio</a></li>
        ...
    </ul>
</nav>
```

### 2. Sistema de Variables CSS y Diseño Visual

El CSS está organizado con variables CSS personalizadas que definen toda la paleta cromática, tipografía, espaciado, transiciones y sombras. Esto permite mantener consistencia visual y facilita enormemente cualquier cambio de tema.

```css
/* css/styles.css, líneas 3-43 — Variables globales del tema */
:root {
    --color-bg: #0a0a0f;
    --color-bg-secondary: #12121a;
    --color-accent: #8b5cf6;
    --color-accent-light: #a78bfa;
    --color-gradient-start: #8b5cf6;
    --color-gradient-end: #ec4899;
    --font-primary: 'Space Grotesk', sans-serif;
    --font-secondary: 'Inter', sans-serif;
    --transition-fast: 0.2s ease;
    --shadow-glow: 0 0 30px rgba(139, 92, 246, 0.3);
}
```

Se utilizan gradientes como `linear-gradient(135deg, var(--color-gradient-start), var(--color-gradient-end))` para los acentos principales, los botones y las barras de progreso de habilidades, creando una identidad visual cohesiva.

### 3. Hero Section con Animaciones CSS

El hero ocupa 100vh con una cuadrícula de dos columnas: texto animado a la izquierda y formas flotantes decorativas a la derecha. Las animaciones se implementan con `@keyframes fadeInUp` y delays escalonados para crear un efecto de entrada secuencial.

```css
/* css/styles.css, líneas 296-310 — Animaciones escalonadas del hero */
.greeting {
    opacity: 0;
    animation: fadeInUp 0.8s ease forwards;
}
.hero-title .name {
    opacity: 0;
    animation: fadeInUp 0.8s ease 0.2s forwards;
}
.hero-title .title-line {
    opacity: 0;
    animation: fadeInUp 0.8s ease 0.4s forwards;
}
```

Las formas flotantes del fondo (`floating-shape`) usan la animación `float` con diferentes `animation-delay` y un `filter: blur(60px)` para crear un efecto de ambiente luminoso sutil.

### 4. Portfolio con Filtrado Dinámico y Galería

La sección de portfolio muestra 6 proyectos alojados en Cara.app, organizados por categorías (Personajes 3D, Concept Art, Escultura Digital). El filtro se implementa con `data-category` en los artículos y botones que muestran/ocultan con transiciones suaves.

```javascript
// js/main.js, líneas 126-151 — Filtro de portfolio con animación
filterBtns.forEach(btn => {
    btn.addEventListener('click', () => {
        filterBtns.forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        const filter = btn.dataset.filter;

        portfolioItems.forEach(item => {
            const category = item.dataset.category;
            if (filter === 'all' || category === filter) {
                item.style.display = 'block';
                setTimeout(() => {
                    item.style.opacity = '1';
                    item.style.transform = 'translateY(0)';
                }, 10);
            } else {
                item.style.opacity = '0';
                item.style.transform = 'translateY(20px)';
                setTimeout(() => { item.style.display = 'none'; }, 300);
            }
        });
    });
});
```

Cada tarjeta de portfolio tiene un overlay con gradiente que aparece en hover, mostrando título, descripción y enlace al proyecto en Cara.app. Las imágenes tienen lazy loading nativo con `loading="lazy"`.

### 5. Barras de Habilidades con Intersection Observer

Las habilidades emplean barras de progreso animadas que solo se activan cuando el usuario las ve por primera vez, usando `IntersectionObserver`. El porcentaje se define mediante una variable CSS personalizada `--progress` en cada barra.

```javascript
// js/main.js, líneas 258-275 — Animación de barras con observer
function initSkillBars() {
    const skillCards = document.querySelectorAll('.skill-card');
    const skillObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const progressBar = entry.target.querySelector('.skill-progress');
                if (progressBar) {
                    const progress = getComputedStyle(progressBar)
                        .getPropertyValue('--progress');
                    progressBar.style.width = progress;
                }
            }
        });
    }, { threshold: 0.5 });
    skillCards.forEach(card => skillObserver.observe(card));
}
```

```html
<!-- index.html, líneas 216-222 — Skill card con progress variable -->
<div class="skill-card">
    <div class="skill-icon">🖌️</div>
    <h3>ZBrush</h3>
    <p>Escultura digital y personajes high poly</p>
    <div class="skill-bar">
        <div class="skill-progress" style="--progress: 90%"></div>
    </div>
</div>
```

### 6. Formulario de Contacto con Formspree y Validación

El formulario de contacto se envía a Formspree.io de forma asíncrona via `fetch` con `FormData`, mostrando feedback visual al usuario. Se incluye validación de longitud mínima del nombre y gestión de errores de red.

```javascript
// js/main.js, líneas 157-205 — Envío async con validación y feedback
form?.addEventListener('submit', async (e) => {
    e.preventDefault();
    // Validación del nombre (mínimo 2 caracteres)
    const nameInput = form.querySelector('input[name="name"]');
    if (nameInput && nameInput.value.trim().length < 2) {
        statusMsg.textContent = 'Por favor, introduce un nombre válido.';
        statusMsg.style.color = '#ef4444';
        return;
    }
    submitBtn.textContent = 'Enviando...';
    submitBtn.disabled = true;
    try {
        const response = await fetch(form.action, {
            method: 'POST',
            body: new FormData(form),
            headers: { 'Accept': 'application/json' }
        });
        if (response.ok) {
            statusMsg.textContent = '¡Mensaje enviado correctamente!';
            statusMsg.style.color = '#10b981';
            form.reset();
        } else {
            statusMsg.textContent = 'Error al enviar. Inténtalo de nuevo.';
            statusMsg.style.color = '#ef4444';
        }
    } catch (error) { ... }
});
```

### 7. Easter Egg — Código Konami

Como detalle creativo, el portfolio incluye un easter egg activable con el código Konami (↑↑↓↓←→←→BA). Al activarse, la página se voltea y aparece un overlay con efecto arcoíris que enlaza a un portal secreto.

```javascript
// js/main.js, líneas 345-398 — Easter egg con Konami code
const konamiCode = [
    'ArrowUp', 'ArrowUp', 'ArrowDown', 'ArrowDown',
    'ArrowLeft', 'ArrowRight', 'ArrowLeft', 'ArrowRight',
    'KeyB', 'KeyA'
];
document.addEventListener('keydown', (e) => {
    if (e.code === konamiCode[konamiIndex]) {
        konamiIndex++;
        if (konamiIndex === konamiCode.length) {
            activateEasterEgg(); // Voltea la página y muestra overlay rainbow
        }
    } else { konamiIndex = 0; }
});
```

El efecto visual usa CSS con `transform: rotate(180deg)` y un gradiente animado con `background-size: 400% 100%` y `@keyframes rainbow`.

---

## Presentación del proyecto

Este portfolio muestra la identidad artística de Marc Arraez Ortigosa como Concept Artist y Modelador de Personajes 3D. Al entrar, un hero a pantalla completa con animaciones escalonadas presenta el nombre, la especialización y dos botones de acción. Las formas flotantes de fondo con blur crean profundidad visual.

La sección de portfolio presenta 6 trabajos reales publicados en Cara.app, filtrables por categoría: Personajes 3D, Concept Art y Escultura Digital. Cada pieza se muestra con overlay informativo en hover y enlace directo a la publicación original.

La sección "Sobre mí" combina una foto de perfil con texto biográfico y tres estadísticas impactantes (30 proyectos, espíritu 1986, creatividad infinita). Las habilidades se visualizan con tarjetas que incluyen barras de progreso animadas al hacer scroll, cubriendo herramientas como ZBrush, Blender, Substance Painter y Photoshop.

El contacto integra email, ubicación y redes sociales con un formulario funcional conectado a Formspree para recibir mensajes reales, con validación y feedback visual de envío.

Todo está construido con HTML5 semántico, CSS3 con variables y gradientes, y JavaScript vanilla con Intersection Observer para las animaciones de scroll, demostrando un dominio completo del frontend sin dependencias externas.

---

## Conclusión

Este portfolio demuestra que con HTML, CSS y JavaScript puros se puede crear una experiencia web profesional, visualmente impactante y completamente funcional. El uso de variables CSS para mantener coherencia visual, Intersection Observer para animaciones performantes, y Formspree para el formulario de contacto, muestra un enfoque práctico y moderno del desarrollo frontend. Los detalles como el Código Konami, las animaciones escalonadas del hero y el filtrado dinámico del portfolio añaden capas de interactividad que elevan la experiencia del usuario. Es un proyecto que sirve tanto como carta de presentación artística como demostración de competencias técnicas en desarrollo web.
