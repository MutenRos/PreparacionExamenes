# Bombas Bloch - Tienda Online de Bombas Hidráulicas

![Bombas Bloch - Desde 1915](https://img.shields.io/badge/Bombas_Bloch-Desde_1915-1a4f8b?style=for-the-badge&logo=shopify&logoColor=white)

> 🔗 **GitHub Pages:** [https://mutenros.github.io/BB/](https://mutenros.github.io/BB/)

## Introducción

![E-commerce de bombas hidráulicas](https://img.shields.io/badge/HTML5-CSS3-JS-E34F26?style=flat-square&logo=html5&logoColor=white)

Bombas Bloch es una tienda online completa que recrea la web de la empresa real Bombas Bloch (fundada en 1915 en Badalona, actualmente en Massalfassar, Valencia). El proyecto implementa un e-commerce funcional con catálogo de 16 productos, carrito de compras con localStorage, sistema de autenticación simulado, checkout con pasarela de pago demo (tarjeta, PayPal, transferencia, Bizum), blog de contenidos técnicos, página de descargas de catálogos, y BIPS (Bloch Intelligent Pump Selector), un selector inteligente con una base de datos de 80+ modelos de bombas reales. Todo desarrollado en HTML5, CSS3 y JavaScript vanilla sin frameworks.

## Desarrollo de las partes

### 1. Estructura HTML y página principal (index.html)

La página principal establece la estructura completa del sitio con barra superior (teléfono + email + redes sociales), header con navegación, hero con lema corporativo "Creando sistemas de bombeo desde 1915", sección de acceso rápido (Productos, Novedades, Compra Online, Outlet), servicios (Presupuesto, Post-venta, Blog, Contacto), 12 categorías de productos, sección "Sobre Nosotros" con datos históricos, galería y mapa de ubicación.

```html
<!-- Acceso rápido con 4 tarjetas enlazadas a secciones principales -->
<!-- Archivo: index.html, líneas 93-120 -->
<section class="quick-access">
    <div class="container">
        <div class="quick-grid">
            <a href="productos.html" class="quick-card">
                <div class="quick-icon"><i class="fas fa-box-open"></i></div>
                <h3>PRODUCTOS</h3>
                <p>Entra en una de las gamas más profesionales y competitivas del mercado</p>
            </a>
            <!-- Novedades, Compra Online, Outlet... -->
        </div>
    </div>
</section>
```

Se añadieron meta tags Open Graph para SEO y roles ARIA en la navegación y footer para accesibilidad.

### 2. Sistema de estilos CSS con variables (styles.css)

El archivo styles.css (809+ líneas) define toda la identidad visual del proyecto basándose en los colores corporativos de Bombas Bloch: azul oscuro (#1a4f8b) como primario, verde (#28a745) como secundario y naranja (#f4a261) como acento. Usa las fuentes Montserrat (títulos) y Roboto (cuerpo), con un sistema responsive completo para 1024px, 768px y 480px.

```css
/* Variables globales del diseño corporativo */
/* Archivo: styles.css, líneas 4-26 */
:root {
    --primary: #1a4f8b;
    --primary-dark: #0d3a6a;
    --primary-light: #2a6cb8;
    --secondary: #28a745;
    --accent: #f4a261;
    --dark: #1d1d1d;
    --shadow: 0 2px 10px rgba(0,0,0,0.1);
    --radius: 8px;
    --transition: all 0.3s ease;
}
```

Se añadieron estilos `focus-visible` para accesibilidad con teclado y transiciones en enlaces del footer.

### 3. JavaScript general y animaciones (script.js)

El archivo script.js (110+ líneas) gestiona la funcionalidad de las páginas: banner de cookies con localStorage, navegación móvil con hamburguesa/X toggle, scroll suave con IntersectionObserver, efecto de sombra dinámica en el header al hacer scroll, animaciones de entrada (fadeInUp) para tarjetas con IntersectionObserver, y validación del formulario de contacto con simulación de envío.

```javascript
/* Animaciones al hacer scroll con IntersectionObserver */
/* Archivo: script.js, líneas 68-84 */
const animateOnScroll = () => {
    const elements = document.querySelectorAll('.quick-card, .category-card, .service-card, .feature');
    elements.forEach(el => {
        const rect = el.getBoundingClientRect();
        const windowHeight = window.innerHeight;
        if (rect.top < windowHeight * 0.85) {
            el.style.opacity = '1';
            el.style.transform = 'translateY(0)';
        }
    });
};
```

También incluye un easter egg con el código Konami (↑↑↓↓←→←→BA) que redirige a un portfolio oculto.

### 4. Carrito de compras con localStorage (js/cart.js)

La clase `ShoppingCart` (249 líneas) implementa un carrito completo persistente. Gestiona el localStorage con clave `bb_cart`, calcula subtotales, IVA al 21%, envío gratuito para pedidos mayores de 500€, muestra notificaciones toast animadas, y renderiza una tabla interactiva con controles +/- de cantidad. Usa delegación de eventos para capturar clics en botones `.add-to-cart` con data attributes.

```javascript
/* Cálculo del total con IVA y gastos de envío condicionales */
/* Archivo: js/cart.js, líneas 240-245 */
getFinalTotal() {
    const subtotal = this.getTotal();
    const iva = subtotal * 0.21;
    const envio = subtotal > 500 ? 0 : 15;
    return subtotal + iva + envio;
}
```

### 5. Sistema de autenticación simulado (js/auth.js)

La clase `AuthSystem` (211 líneas) simula registro/login de usuarios con localStorage. Gestiona roles (admin/customer), actualización de perfil, creación de pedidos con historial, y panel de administración. Se crea automáticamente un usuario admin por defecto. La UI se actualiza dinámicamente mostrando nombre del usuario logueado o enlaces de login/registro.

```javascript
/* Login con verificación de credenciales almacenadas */
/* Archivo: js/auth.js, líneas 72-86 */
login(email, password) {
    const user = this.users.find(u => u.email === email && u.password === password);
    if (!user) {
        return { success: false, message: 'Email o contraseña incorrectos' };
    }
    this.currentUser = { ...user };
    delete this.currentUser.password;
    localStorage.setItem('bb_user', JSON.stringify(this.currentUser));
    this.updateAuthUI();
    return { success: true, message: 'Sesión iniciada', user: this.currentUser };
}
```

### 6. Checkout con pasarela de pago simulada (js/checkout.js)

La clase `CheckoutSystem` (405 líneas) implementa un proceso de compra en 3 pasos: datos de envío (con autorelleno si hay sesión), selección de pago (tarjeta demo 4242..., PayPal, transferencia o Bizum) y confirmación con número de pedido. Todo funciona en modo demo controlado, mostrando banners informativos de que no se realizan cargos reales.

```javascript
/* Renderizado del resumen del pedido en el sidebar */
/* Archivo: js/checkout.js, líneas 290-320 */
renderOrderSummary() {
    return `
        <div class="order-summary-box">
            <h3>Resumen del Pedido</h3>
            <div class="summary-totals">
                <div class="summary-row">
                    <span>Subtotal</span>
                    <span>${cart.getTotal().toFixed(2)} €</span>
                </div>
                <div class="summary-row">
                    <span>IVA (21%)</span>
                    <span>${(cart.getTotal() * 0.21).toFixed(2)} €</span>
                </div>
                ...
            </div>
        </div>
    `;
}
```

### 7. BIPS - Selector inteligente de bombas (bips.js)

BIPS (Bloch Intelligent Pump Selector) contiene una base de datos de 80+ modelos reales de bombas organizados en series: H (horizontales domésticas), H Industrial, HXN (inox), JET (autoaspirantes), PR (periféricas), CPA (centrífugas), DA (doble rodete), HG (circuladoras), VE (verticales), SP4/SP6 (sumergibles), VORTEX/DRAIN/FEKA (achique), SOLAR, GP/VARIBLOCH (presión) y CI (contra incendios). El algoritmo busca por caudal y altura con tolerancia progresiva.

```javascript
/* Búsqueda aproximada con tolerancia ampliable y fallback por distancia */
/* Archivo: bips.js, líneas 107-128 */
function buscarBombaAproximada(caudalRequerido, alturaRequerida) {
    let resultados = buscarBomba(caudalRequerido, alturaRequerida, 0.2);
    if (resultados.length === 0) {
        resultados = buscarBomba(caudalRequerido, alturaRequerida, 0.4);
    }
    if (resultados.length === 0) {
        resultados = bombasBloch.map(bomba => {
            const distancia = Math.sqrt(
                Math.pow((bomba.caudal - caudalRequerido) / caudalRequerido, 2) +
                Math.pow((bomba.altura - alturaRequerida) / alturaRequerida, 2)
            );
            return { ...bomba, distancia };
        }).sort((a, b) => a.distancia - b.distancia).slice(0, 5);
    }
    return resultados;
}
```

Se añadió validación para evitar búsquedas sin parámetros.

### 8. Formulario de contacto avanzado (contacto.html + conocenos.css)

La página de contacto combina una tarjeta de información (dirección del polígono industrial, teléfono, email, horario, redes sociales) con un formulario completo: nombre, apellidos, email, teléfono, empresa, asunto (select con opciones), mensaje con contador de caracteres (máx. 1000), checkbox de privacidad y mapa embebido de Google Maps.

```html
<!-- Formulario con select de asuntos predefinidos -->
<!-- Archivo: contacto.html, líneas 148-159 -->
<select id="asunto" name="asunto" required>
    <option value="">Selecciona una opción</option>
    <option value="info">Información general</option>
    <option value="presupuesto">Solicitud de presupuesto</option>
    <option value="sat">Servicio técnico (SAT)</option>
    <option value="repuestos">Repuestos</option>
    <option value="asesoramiento">Asesoramiento técnico</option>
    <option value="otro">Otro</option>
</select>
```

Se añadió validación del teléfono en formato español (9 dígitos, 6-9) y un contador dinámico de caracteres que cambia a rojo al superar los 900.

## Presentación del proyecto

Bombas Bloch es la recreación completa de la web de un fabricante histórico de bombas hidráulicas fundado en 1915, transformada en una tienda online funcional con identidad corporativa en tonos azul oscuro y naranja.

Al acceder a la web, el usuario ve una barra superior con datos de contacto y redes sociales, seguida de un header con el logo "BOMBAS BLOCH" y navegación completa. El hero muestra el lema corporativo "Creando sistemas de bombeo desde 1915" con CTAs a productos y presupuesto. La sección de acceso rápido presenta cuatro tarjetas (Productos, Novedades, Compra Online, Outlet) y una franja de servicios (Presupuesto, Post-venta, Blog, Contacto).

El catálogo organiza los productos en 12 categorías: Horizontales Domésticas, Horizontales Industriales, Verticales, Sumergibles para Pozos, Solar, Achiques, Controladores, Equipos de Presión, Contra Incendios, Cuadros Eléctricos, Accesorios y el Selector BIPS.

La Tienda Online presenta 16 productos con imágenes reales de bombasbloch.com, filtros por categoría y precio, y buscador de texto. Cada producto se puede añadir al carrito con notificación animada. El proceso de checkout guía al usuario en 3 pasos con múltiples métodos de pago simulados.

BIPS es la herramienta estrella: con 80+ modelos de bombas reales en su base de datos, el cliente introduce caudal y altura deseados y recibe recomendaciones ordenadas por eficiencia energética, con búsqueda aproximada que se amplía progresivamente si no encuentra resultados exactos.

La sección "Conócenos" detalla la historia de la empresa desde 1915, el equipo y las instalaciones. El Blog ofrece artículos técnicos sobre bombeo. La página de Descargas permite acceder a catálogos PDF. Todo funciona sin servidor gracias a localStorage.

## Conclusión

Este proyecto demuestra que con tecnologías web puras (HTML5, CSS3, JavaScript vanilla) se puede construir un e-commerce completo con funcionalidad real. Más allá de la tienda online con carrito, autenticación y checkout, el sistema BIPS con sus 80+ modelos de bombas y algoritmo de búsqueda aproximada por eficiencia energética aporta un valor añadido único que diferencia a este proyecto de un e-commerce genérico.

Las 12 categorías de productos, los datos reales de la empresa, las páginas legales (RGPD, cookies, privacidad), el blog técnico y la página de descargas completan una web que podría servir como base real para el negocio. Las mejoras de accesibilidad (ARIA, focus-visible), la validación de formularios con formatos españoles y el diseño responsive aseguran una experiencia de usuario profesional en cualquier dispositivo.

El resultado es un proyecto integral que abarca diseño, desarrollo frontend, gestión de datos con localStorage y experiencia de usuario, todo desplegable estáticamente en GitHub Pages.
