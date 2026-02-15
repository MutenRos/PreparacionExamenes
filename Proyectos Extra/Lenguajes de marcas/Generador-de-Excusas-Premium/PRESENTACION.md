# Generador de Excusas Premium 💎

![Generador de Excusas Premium](https://img.shields.io/badge/Excusas-Premium-gold)

## Introducción

El Generador de Excusas Premium es una aplicación web interactiva que genera excusas absurdas y creativas combinando aleatoriamente sujetos, verbos, objetos y contextos humorísticos. El usuario puede introducir el motivo para el que necesita la excusa y la aplicación construye una frase completa personalizada. Incluye historial de excusas guardado en localStorage y la posibilidad de copiar cada excusa al portapapeles.

El proyecto está desarrollado con HTML5, CSS3 y JavaScript ES6+ (módulos), utilizando Vite como herramienta de desarrollo. El diseño visual sigue una estética dark premium con acentos dorados y animaciones suaves.

---

## Desarrollo de las partes

### 1. Estructura HTML Semántica

El archivo HTML define la interfaz de la aplicación: un contenedor principal con título, campo de entrada para el motivo, botón de generación, área de resultado con `aria-live` para accesibilidad, botón de copiar al portapapeles, y una sección de historial con lista y botón de borrado.

```html
<!-- Archivo: index.html, líneas 12-28 -->
<!-- Ruta: /index.html -->
<div id="app">
  <h1>Generador de Excusas Premium 💎</h1>
  
  <div class="input-container">
    <label for="reasonInput" class="input-label">Necesito una excusa para...:</label>
    <input type="text" id="reasonInput" 
           placeholder="¿De qué quieres librarte?" 
           autocomplete="off" maxlength="80">
    <small id="charCounter" class="char-counter">0 / 80</small>
  </div>

  <div class="card">
    <button id="salvarmeBtn" type="button">¡SALVARME!</button>
  </div>
  
  <div id="excusaContainer" class="excusa-box" 
       aria-live="polite" aria-atomic="true">
    <p class="placeholder">Pulsa el botón para recibir tu salvación.</p>
  </div>
</div>
```

El atributo `aria-live="polite"` permite que los lectores de pantalla anuncien automáticamente la excusa generada sin interrumpir al usuario. El `maxlength="80"` limita la longitud del input.

### 2. Base de Datos de Vocabulario

El motor del generador se basa en cuatro arrays de vocabulario en JavaScript: sujetos (14 opciones absurdas), verbos (13 acciones disparatadas), objetos (11 elementos cotidianos) y contextos (10 circunstancias hilarantes). La combinación aleatoria de estos cuatro arrays produce miles de excusas únicas.

```javascript
// Archivo: main.js, líneas 2-37
// Ruta: /main.js
const subjects = [
    "mi gato hacker", "el espíritu de mi bisabuelo comunista", 
    "un mapache con sombrero de copa", "la mafia de las palomas",
    "mi doble de otra dimensión", "un algoritmo deprimido",
    "el presidente de la comunidad de vecinos", "mi tostadora consciente",
    // ... 14 sujetos en total
];

const verbs = [
    "secuestró", "demandó a", "se comió", "borró", "invocó a",
    "declaró ilegal", "abdujo a", "convirtió en NFT a",
    // ... 13 verbos en total
];

const objects = [
    "mi router", "mis ganas de vivir", "mi coche",
    "tu regalo de cumpleaños", "las llaves de casa",
    // ... 11 objetos en total
];
```

Con 14 × 13 × 11 × 10 = **20.020 combinaciones posibles**, la probabilidad de repetición es muy baja.

### 3. Algoritmo de Generación

La función `generateExcuse()` es asíncrona para permitir un efecto de carga de 600ms que añade suspense. Primero genera una excusa base combinando aleatoriamente un elemento de cada array, luego la personaliza con el motivo del usuario si lo ha introducido.

```javascript
// Archivo: main.js, líneas 71-100
// Ruta: /main.js
async function generateExcuse() {
  const reason = reasonInput.value.trim();

  // Efecto de carga dramático
  container.innerHTML = '<p class="placeholder">Calculando variables de causalidad...</p>';
  btnSalvarme.disabled = true;

  await new Promise(r => setTimeout(r, 600));

  let excusaBase = generateRandomExcuse();
  excusaBase = excusaBase.charAt(0).toLowerCase() + excusaBase.slice(1);

  let finalExcuse = "";
  if (reason) {
      finalExcuse = `Mira, lo de ${reason}... es que ${excusaBase}`;
  } else {
      finalExcuse = excusaBase;
  }
  
  finalExcuse = finalExcuse.charAt(0).toUpperCase() + finalExcuse.slice(1);
  container.innerHTML = `<p class="excusa-text">"${finalExcuse}"</p>`;
}
```

El manejo de mayúsculas/minúsculas asegura que la frase siempre comience con mayúscula aunque se concatene con el prefijo personalizado.

### 4. Sistema de Historial con localStorage

El historial guarda las últimas 20 excusas generadas en `localStorage` bajo la clave `excuseHistory`. Las nuevas excusas se añaden al principio del array y se renderiza cada una como un `<li>` con animación de entrada. El botón de borrado ahora incluye confirmación para evitar pérdida accidental.

```javascript
// Archivo: main.js, líneas 47-62
// Ruta: /main.js
function saveExcuse(text) {
  const history = JSON.parse(localStorage.getItem('excuseHistory')) || [];
  history.unshift(text); // Añadir al principio
  if (history.length > 20) history.pop(); // Mantener máximo 20
  localStorage.setItem('excuseHistory', JSON.stringify(history));
}

// Confirmacion antes de borrar historial
btnClear.addEventListener('click', () => {
    if (historyList.children.length === 0) return;
    if (confirm('¿Seguro que quieres borrar todo el historial?')) {
        localStorage.removeItem('excuseHistory');
        loadHistory();
    }
});
```

### 5. Diseño Visual Dark Premium

El CSS implementa un tema oscuro elegante con fondo `#242424`, contenedor con bordes redondeados y sombra, y un título con degradado dorado usando `background-clip: text`. Los botones tienen efecto de escala al pulsarlos y brillo dorado al pasar el ratón. El diseño es responsive con `max-width: 1280px` y `width: 90%`.

```css
/* Archivo: style.css, líneas 42-50 */
/* Ruta: /style.css */
h1 {
  font-size: 3.2em;
  line-height: 1.1;
  background: linear-gradient(to right, #bf953f, #fcf6ba, #b38728, #fbf5b7, #aa771c);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
  margin-bottom: 20px;
}
```

La caja de excusa usa un borde dorado (`#d4af37`) y las excusas aparecen con una animación `fadeIn` de 0.5 segundos.

### 6. Interactividad y Eventos

La aplicación maneja múltiples eventos: click en el botón principal, tecla Enter en el input, click en copiar al portapapeles (usando `navigator.clipboard.writeText()` con feedback visual), contador de caracteres en tiempo real con indicador visual cuando se acerca al límite, y confirmación antes de borrar el historial.

```javascript
// Archivo: main.js, líneas 112-126
// Ruta: /main.js
// Copiar excusa al portapapeles
btnCopy.addEventListener('click', () => {
    const excusaText = container.querySelector('.excusa-text');
    if (excusaText) {
        navigator.clipboard.writeText(excusaText.textContent).then(() => {
            btnCopy.textContent = '✅ ¡Copiada!';
            setTimeout(() => { btnCopy.textContent = '📋 Copiar excusa'; }, 1500);
        });
    }
});

// Contador de caracteres
reasonInput.addEventListener('input', () => {
    const len = reasonInput.value.length;
    charCounter.textContent = `${len} / 80`;
    charCounter.classList.toggle('near-limit', len >= 70);
});
```

### 7. Accesibilidad y Buenas Prácticas

Se han implementado varias mejoras de accesibilidad: `aria-live="polite"` en el contenedor de excusas para lectores de pantalla, estilos `focus-visible` con contorno dorado para navegación por teclado, `prefers-reduced-motion` que desactiva animaciones para usuarios con sensibilidad al movimiento, y `label` asociado al input con `for`.

```css
/* Archivo: style.css, líneas 137-148 */
/* Ruta: /style.css */
/* Accesibilidad: Foco visible para teclado */
*:focus-visible {
  outline: 3px solid #d4af37;
  outline-offset: 2px;
}

/* Reducir animaciones si el usuario lo prefiere */
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

---

## Presentación del proyecto

El Generador de Excusas Premium es una aplicación web de humor que permite al usuario generar excusas absurdas para cualquier situación. Al abrir la aplicación, aparece una interfaz oscura y elegante con un título dorado brillante.

El usuario puede escribir opcionalmente el motivo por el que necesita una excusa (por ejemplo, "ir a trabajar" o "la cena con mis suegros") y pulsar el botón "¡SALVARME!". Tras un breve efecto de carga dramático ("Calculando variables de causalidad..."), la aplicación combina aleatoriamente elementos absurdos para generar frases como: *"Mira, lo de ir a trabajar... es que la mafia de las palomas secuestró mi router durante un eclipse lunar"*.

Cada excusa generada puede copiarse al portapapeles con un botón dedicado y se guarda automáticamente en el historial (máximo 20 entradas) que persiste entre sesiones gracias a localStorage. El historial muestra las excusas de más reciente a más antigua y puede borrarse con confirmación.

La base de datos de vocabulario contiene 14 sujetos, 13 verbos, 11 objetos y 10 contextos, produciendo más de 20.000 combinaciones únicas posibles. El diseño responsive se adapta a cualquier tamaño de pantalla y cumple con estándares de accesibilidad web.

---

## Conclusión

El Generador de Excusas Premium demuestra cómo una aplicación web puede ser a la vez divertida y técnicamente completa utilizando solo tecnologías front-end estándar. El proyecto combina HTML semántico con accesibilidad (ARIA, labels, focus-visible), CSS moderno con variables, gradientes y animaciones controladas, y JavaScript ES6+ con módulos, async/await, localStorage, Clipboard API y manejo de eventos.

A pesar de su naturaleza humorística, el código sigue buenas prácticas: separación de responsabilidades entre HTML/CSS/JS, persistencia de datos con localStorage, UX cuidada con feedback visual en cada acción, confirmaciones de seguridad y soporte de accesibilidad. Con más de 20.000 combinaciones posibles, la aplicación ofrece suficiente variedad para que cada excusa se sienta única e inesperada.
