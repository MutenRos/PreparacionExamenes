# 📱 ELECE Barber - Versión Móvil

Versión optimizada para dispositivos móviles de la web de ELECE Barber.

## 🎯 Características Móviles

### Diseño
- ✅ **Mobile-First**: Diseñado específicamente para pantallas pequeñas
- ✅ **Interfaz Táctil**: Botones grandes y áreas de toque optimizadas
- ✅ **Navegación Drawer**: Menú lateral deslizante
- ✅ **Bottom CTA**: Botón de acción flotante siempre visible

### Interacciones
- 👆 **Swipe Gestures**: Desliza para navegar y cerrar menús
- 📱 **Haptic Feedback**: Vibración suave al tocar botones
- 🎭 **Scroll Effects**: Animaciones al hacer scroll
- 🔄 **Carrusel Táctil**: Desliza para ver reseñas

### Performance
- ⚡ **Carga Rápida**: CSS y JS optimizados para móvil
- 💾 **PWA**: Instalable como app nativa
- 🔌 **Offline**: Funciona sin conexión (Service Worker)
- 📦 **Lazy Loading**: Carga inteligente de contenido

### UX Móvil
- 📲 **Quick Actions**: Accesos rápidos a funciones clave
- 📍 **Mapa Integrado**: Google Maps embebido
- ☎️ **Click to Call**: Llamada directa con un toque
- 📅 **Reserva Rápida**: Botón CTA fijo en la parte inferior

## 📁 Estructura

```
mobile-version/
├── index.html          # HTML optimizado para móvil
├── manifest.json       # PWA manifest
├── css/
│   └── mobile.css      # Estilos móviles
├── js/
│   └── mobile.js       # JavaScript con gestos táctiles
└── images/
    └── elece-logo.png  # Logo
```

## 🚀 Uso

### Desarrollo Local
1. Abre `index.html` en tu navegador
2. O usa un servidor local:
   ```bash
   python -m http.server 8000
   ```
3. Abre en móvil: `http://localhost:8000/mobile-version/`

### Vista Móvil en Desktop
- Chrome DevTools: F12 → Toggle device toolbar (Ctrl+Shift+M)
- Selecciona un dispositivo móvil (iPhone, Samsung, etc.)

## ✨ Diferencias con la Versión Desktop

| Característica | Desktop | Móvil |
|---------------|---------|-------|
| Navegación | Horizontal fija | Drawer lateral |
| Hero | Video/imagen grande | Compacto con badge |
| Servicios | Grid de tarjetas | Lista vertical |
| Galería | Grid 3x2 | Grid 2x2 + carousel |
| Reseñas | Carousel horizontal | Swipe carousel |
| CTA | En hero | Fixed bottom |
| Mapa | Grande embebido | Compacto + botón |
| Tamaño botones | Estándar | Extra grandes (44px+) |
| Animaciones | Complejas | Simples y rápidas |

## 📱 Optimizaciones Móviles

### Touch Targets
- Todos los botones: mínimo 44x44px
- Espaciado entre elementos táctiles
- Sin hover states (solo :active)

### Gestos
- Swipe horizontal: Navegar reseñas
- Swipe derecha: Cerrar menú
- Tap: Todas las interacciones
- Scroll: Ocultar/mostrar CTA

### Performance
- Sin parallax pesado
- Animaciones CSS (no JS)
- Lazy loading de imágenes
- Fuentes del sistema

### Accesibilidad
- Contraste WCAG AAA
- Textos legibles (16px+)
- Áreas táctiles grandes
- Focus visible

## 🎨 Paleta de Colores

```css
--primary: #000000    /* Negro */
--secondary: #333333  /* Gris oscuro */
--accent: #ffffff     /* Blanco */
--bg-light: #f8f8f8   /* Gris claro */
```

## 📊 Métricas de Rendimiento

- **First Contentful Paint**: < 1.5s
- **Time to Interactive**: < 3.5s
- **Cumulative Layout Shift**: < 0.1
- **Lighthouse Score**: 95+

## 🔧 Tecnologías

- HTML5 semántico
- CSS3 con Flexbox y Grid
- JavaScript vanilla (sin frameworks)
- Service Worker para PWA
- Touch events API
- Intersection Observer API

## 📲 Instalación como App

1. Abre la web en Safari (iOS) o Chrome (Android)
2. iOS: Compartir → "Añadir a pantalla de inicio"
3. Android: Menú → "Instalar app" o "Añadir a pantalla de inicio"

## 🎯 Best Practices Implementadas

✅ Mobile-first design
✅ Touch-friendly interface
✅ Fast loading times
✅ Offline capabilities
✅ Native app feel
✅ Smooth animations
✅ Accessible design
✅ SEO optimized

---

**Versión móvil creada para ELECE Barber - Noviembre 2025**
