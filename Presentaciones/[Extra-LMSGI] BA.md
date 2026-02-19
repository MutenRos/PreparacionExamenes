# Bombas Asoin Murcia - Tienda Online de Bombas de Agua

![Bombas Asoin - Hero principal](https://img.shields.io/badge/Bombas_Asoin-Tienda_Online-2e7d32?style=for-the-badge&logo=shopify&logoColor=white)

> 🔗 **GitHub Pages:** [https://mutenros.github.io/BA/](https://mutenros.github.io/BA/)

## Introducción

![E-commerce de bombas de agua](https://img.shields.io/badge/HTML5-CSS3-JS-E34F26?style=flat-square&logo=html5&logoColor=white)

Bombas Asoin Murcia es una tienda online completa desarrollada en HTML5, CSS3 y JavaScript vanilla, inspirada en la web real de asoinbombas.es. El proyecto recrea una experiencia de e-commerce profesional con catálogo de productos, carrito de compras con localStorage, sistema de autenticación simulado, pasarela de pago en modo demo, un blog de contenidos técnicos, y BIPS, un selector inteligente de bombas que ayuda al usuario a encontrar el modelo ideal según sus necesidades de caudal y altura. Todo ello sin ningún framework ni backend, demostrando el potencial de las tecnologías web puras.

## Desarrollo de las partes

### 1. Estructura HTML y página principal (index.html)

La página principal establece la estructura base del sitio con un header fijo, hero de bienvenida, secciones de servicios (Agricultura, Abastecimiento, Achique, Piscinas), zona "Conócenos", productos destacados con precios, banner del selector BIPS, CTA de asesoramiento y footer completo.

```html
<!-- Secciones de servicios con iconos Font Awesome y enlaces a categorías -->
<!-- Archivo: index.html, líneas 76-113 -->
<section class="services-section" id="servicios">
    <div class="container">
        <h2 class="section-title">Servicios</h2>
        <div class="services-grid">
            <a href="tienda.html#agricultura" class="service-card">
                <div class="service-image agriculture">
                    <i class="fas fa-seedling"></i>
                </div>
                <h3>AGRICULTURA</h3>
                <p>Bombas para riego agrícola y sistemas de fertirrigación</p>
            </a>
            <!-- ... más categorías -->
        </div>
    </div>
</section>
```

Se usan meta tags de Open Graph y roles ARIA para mejorar SEO y accesibilidad (líneas 8-12 y 30).

### 2. Sistema de estilos CSS con variables (styles.css)

El archivo styles.css (791+ líneas) implementa un sistema de diseño completo basado en CSS custom properties. Se definen colores corporativos (verde #2e7d32, naranja #ff6f00), tipografías (Poppins/Open Sans), sombras, transiciones y un layout totalmente responsive con breakpoints a 1024px, 768px y 480px.

```css
/* Variables globales del proyecto */
/* Archivo: styles.css, líneas 8-31 */
:root {
    --primary-color: #2e7d32;      /* Verde */
    --primary-dark: #1b5e20;
    --primary-light: #4caf50;
    --secondary-color: #ff6f00;    /* Naranja */
    --text-dark: #212121;
    --bg-light: #f5f5f5;
    --font-primary: 'Poppins', sans-serif;
    --font-secondary: 'Open Sans', sans-serif;
    --shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
    --transition: all 0.3s ease;
}
```

Se añadieron estilos de accesibilidad `focus-visible` (líneas finales de styles.css) para navegación con teclado, y transiciones en enlaces del footer.

### 3. JavaScript general y validación de formularios (script.js)

El archivo script.js (220+ líneas) gestiona funcionalidad general del sitio: banner de cookies con localStorage, navegación móvil con toggle hamburguesa, efecto scroll del header, animaciones con IntersectionObserver, smooth scroll con offset, validación del formulario de contacto (nombre, email, teléfono español) y lazy loading de imágenes.

```javascript
/* Validación del teléfono en formato español (9 dígitos, 6-9 inicio) */
/* Archivo: script.js, líneas 126-131 */
if (telefono && telefono.value.trim() !== '' && !/^[6-9]\d{8}$/.test(telefono.value.replace(/\s/g, ''))) {
    showError(telefono, 'Teléfono no válido (9 dígitos, empieza por 6-9)');
    valid = false;
} else if (telefono && telefono.value.trim() !== '') {
    clearError(telefono);
}
```

También incluye un easter egg con el código Konami (↑↑↓↓←→←→BA) que redirige al portfolio del desarrollador.

### 4. Carrito de compras con localStorage (js/cart.js)

La clase `ShoppingCart` (249 líneas) implementa un carrito completo persistente en localStorage. Incluye métodos para añadir/eliminar productos, actualizar cantidades, calcular subtotales con IVA al 21%, envío gratuito para pedidos mayores de 500€, notificaciones animadas tipo toast y renderizado dinámico de la tabla del carrito.

```javascript
/* Cálculo del total final con IVA y envío */
/* Archivo: js/cart.js, líneas 240-245 */
getFinalTotal() {
    const subtotal = this.getTotal();
    const iva = subtotal * 0.21;
    const envio = subtotal > 500 ? 0 : 15;
    return subtotal + iva + envio;
}
```

El sistema usa delegación de eventos globales para capturar clics en botones `.add-to-cart` con data attributes, permitiendo añadir productos desde cualquier página.

### 5. Sistema de autenticación simulado (js/auth.js)

La clase `AuthSystem` (211 líneas) simula un sistema completo de usuarios usando localStorage. Incluye registro con validación de email único, login/logout, gestión de roles (admin/customer), actualización de perfil, creación de pedidos, y panel de administración. Se crea automáticamente un usuario admin por defecto (admin@asoinbombas.es / admin123).

```javascript
/* Actualización dinámica de la UI según estado de autenticación */
/* Archivo: js/auth.js, líneas 107-127 */
updateAuthUI() {
    const authLinks = document.getElementById('auth-links');
    if (!authLinks) return;
    if (this.isAuthenticated()) {
        authLinks.innerHTML = `
            <a href="cuenta.html" class="auth-link">
                <i class="fas fa-user"></i> ${this.currentUser.name}
            </a>
            ${this.isAdmin() ? '<a href="admin.html" ...>Admin</a>' : ''}
            <a href="#" onclick="auth.logout();">Salir</a>
        `;
    } else {
        authLinks.innerHTML = `
            <a href="login.html">Iniciar Sesión</a>
            <a href="registro.html">Registro</a>
        `;
    }
}
```

### 6. Checkout con pasarela de pago simulada (js/checkout.js)

La clase `CheckoutSystem` (405 líneas) implementa un proceso de compra en 3 pasos: envío (formulario de dirección con autorelleno si el usuario está logueado), pago (tarjeta demo 4242..., PayPal, transferencia o Bizum) y confirmación con número de pedido. Todo en modo demo, sin cargos reales.

```javascript
/* Procesamiento del pago simulado en 2 segundos */
/* Archivo: js/checkout.js, líneas 347-370 */
processPayment(form) {
    const paymentMethod = formData.get('paymentMethod');
    const payBtn = form.querySelector('.btn-pay');
    payBtn.innerHTML = '<i class="fas fa-spinner fa-spin"></i> Procesando...';
    payBtn.disabled = true;
    setTimeout(() => {
        const order = auth.createOrder({
            ...this.orderData,
            items: cart.items,
            total: cart.getFinalTotal(),
            paymentMethod: paymentMethod
        });
        this.orderData.orderId = order.id;
        cart.clear();
        this.goToStep(3);
    }, 2000);
}
```

### 7. BIPS - Selector inteligente de bombas (bips.js + bips.html)

BIPS (Búsqueda Inteligente de Productos y Soluciones) es una herramienta que permite al usuario encontrar la bomba ideal introduciendo caudal (m³/h) y altura (m) deseados, con filtro opcional por categoría. El sistema busca en una base de datos de 60 modelos reales de bombas Asoin, ordena los resultados por mejor ajuste y marca la mejor opción con una etiqueta destacada.

```javascript
/* Base de datos de 60 modelos de bombas Asoin con especificaciones reales */
/* Archivo: bips.js, líneas 7-75 (extracto) */
const bombasAsoin = [
    { modelo: "VIP V 2-80", serie: "VIP V", categoria: "abastecimiento",
      caudalMax: 2.4, alturaMax: 56, potencia: 0.75, precio: 781 },
    { modelo: "VIPH 2/3", serie: "VIPH", categoria: "agricultura",
      caudalMax: 3, alturaMax: 28, potencia: 0.37, precio: 331 },
    { modelo: "VORTEX 150", serie: "VORTEX", categoria: "achique",
      caudalMax: 18, alturaMax: 8, potencia: 1.1, precio: 822 },
    // ... 57 modelos más de series VIP V, GIP, VIPH, VARI IP, HHG, IPE, HXN...
];
```

Se añadió validación de entrada: ahora el sistema avisa al usuario si no introduce ningún valor antes de buscar.

### 8. Página de contacto con formulario avanzado (contacto.html + contacto.css)

La página de contacto incluye una sección con tarjetas informativas (teléfono fijo/móvil, dirección, horario, redes sociales), formulario con campos de nombre, apellidos, email, teléfono, selector de asunto, textarea con contador de caracteres (máx. 1000), checkbox de privacidad obligatorio, y un mapa embebido de Google Maps con la ubicación real de la tienda en Murcia.

```html
<!-- Textarea con contador de caracteres dinámico -->
<!-- Archivo: contacto.html, líneas 161-164 -->
<textarea id="mensaje" name="mensaje" rows="5" required maxlength="1000"
    placeholder="Describe tu consulta..."></textarea>
<small class="char-counter" id="charCounter">0 / 1000 caracteres</small>
```

El contador cambia a rojo cuando se superan los 900 caracteres, avisando visualmente al usuario.

## Presentación del proyecto

Bombas Asoin Murcia es una recreación completa de la web de una empresa real de bombas de agua, transformada en una tienda online funcional con todas las características que un e-commerce profesional necesita.

Al entrar en la web, el usuario encuentra un diseño limpio en tonos verdes y naranjas que transmite profesionalidad. El header fijo permite navegar en todo momento entre Inicio, Tienda, Blog, Contacto y el selector BIPS. La página principal muestra las 4 categorías de productos (Agricultura, Abastecimiento, Achique, Piscinas) con iconos descriptivos y 6 productos destacados con precios reales.

La Tienda Online presenta un catálogo de 16 productos con imágenes reales de asoinbombas.es, filtros por categoría y rango de precios, y buscador de texto. Cada producto puede añadirse al carrito con un clic, mostrando una notificación animada de confirmación.

El Carrito de Compra muestra los productos seleccionados en una tabla interactiva con controles de cantidad, cálculo automático de subtotal, IVA (21%) y envío (gratis a partir de 500€). El proceso de Checkout guía al usuario en 3 pasos claros con indicador de progreso visual.

La herramienta BIPS es el diferenciador del proyecto: un calculador donde el cliente introduce sus necesidades de caudal y altura, filtra por categoría y obtiene recomendaciones ordenadas de entre 60 modelos reales de bombas, con la mejor opción destacada.

El Blog ofrece 6 artículos técnicos sobre mantenimiento de bombas, eficiencia energética, riego por goteo, calidad del agua, bombas solares y protección contra heladas, posicionando a la marca como referente técnico.

Todo el sistema funciona sin servidor: los datos de usuario, carrito y pedidos se gestionan con localStorage, haciendo que el proyecto sea completamente portable y funcional como demo estática.

## Conclusión

Este proyecto demuestra que con HTML5, CSS3 y JavaScript vanilla se puede construir un e-commerce completo y funcional sin necesidad de frameworks ni backend. Desde el diseño responsive con variables CSS hasta el sistema de pagos simulado con múltiples métodos, pasando por el selector inteligente BIPS con su base de datos de 60 bombas reales, cada componente ha sido diseñado pensando en la experiencia del usuario final.

Las mejoras de accesibilidad (ARIA, focus-visible), la validación de formularios con formatos españoles, el sistema de cookies RGPD y las páginas legales completas demuestran atención al detalle profesional. El uso de localStorage como pseudo-backend permite que toda la funcionalidad de carrito, autenticación y pedidos funcione perfectamente en un despliegue estático en GitHub Pages.

El resultado es una web que cualquier tienda de bombas de agua podría usar como punto de partida para su presencia online, con un diseño modernoa la altura de proyectos profesionales.
