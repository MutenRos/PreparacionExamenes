# ELECE BARBER - Sitio Web Premium de Barbería

Sitio web moderno y profesional para ELECE Barber, una barbería premium ubicada en Albuixech, Valencia, España.

## 🌟 Características

- **Diseño Moderno**: Diseño limpio y profesional con estética premium de barbería
- **Diseño Responsive**: Enfoque mobile-first con diseño completamente adaptable
- **Integración de Reservas Online**: Integración directa con sistema de reservas Booksy
- **Escaparate de Servicios**: Presentación detallada de todos los servicios de barbería
- **Galería Interactiva**: Galería de fotos profesionales integrada con Instagram
- **Reseñas de Clientes**: Carrusel de testimonios de Booksy para generar confianza
- **Información de Contacto**: Detalles completos de contacto y ubicación
- **Animaciones Suaves**: UI/UX moderna con scroll suave y efectos hover
- **Optimizado para SEO**: HTML semántico y meta tags para optimización en buscadores

## 🚀 Servicios Ofrecidos

- **Corte caballero** - 13€
- **Recorte de barba** - 6€
- **Corte y barba** - 16€
- **Corte y lavado** - 15€

## 🛠️ Tecnologías Utilizadas

- **HTML5**: Marcado semántico con características de accesibilidad
- **CSS3**: Estilos modernos con flexbox, grid y animaciones
- **JavaScript**: Funcionalidad interactiva y experiencia de usuario fluida
- **Font Awesome**: Iconos profesionales
- **Google Fonts**: Familias tipográficas Playfair Display e Inter
- **Diseño Responsive**: Enfoque mobile-first

## 📁 Estructura del Proyecto

```
ELECE-BARBER/
├── index.html              # Archivo HTML principal
├── css/
│   └── styles.css          # Todos los estilos CSS y diseño responsive
├── js/
│   └── script.js           # Funcionalidad JavaScript
├── images/
│   └── elece-logo.png      # Logo de ELECE Barber
├── .github/
│   └── copilot-instructions.md  # Contexto del proyecto para desarrollo
├── INSTAGRAM-INTEGRATION.md     # Documentación de integración con Instagram
└── README.md               # Documentación del proyecto
```

## 🚀 Cómo Empezar

### Requisitos Previos
- Un navegador web moderno
- VS Code (recomendado) o cualquier editor de texto
- Extensión Live Server para VS Code (opcional, para desarrollo)

### Instalación

1. **Clonar o descargar el proyecto**
   ```bash
   git clone https://github.com/MutenRos/elece-barber.git
   cd elece-barber
   ```

2. **Abrir en VS Code**
   ```bash
   code .
   ```

3. **Ejecutar con Live Server**
   - Instala la extensión "Live Server" en VS Code
   - Haz clic derecho en `index.html`
   - Selecciona "Open with Live Server"
   - El sitio web se abrirá en `http://localhost:5500`

### Alternativa: Servidor HTTP Simple

Si tienes Python instalado:
```bash
# Python 3
python -m http.server 8000

# Python 2
python -m SimpleHTTPServer 8000
```

Luego abre `http://localhost:8000` en tu navegador.

## 🎨 Personalización

### Colores
El sitio web utiliza un esquema de colores profesional en blanco y negro:
- Blanco: `#ffffff`
- Negro: `#000000`
- Gris oscuro: `#1a1a1a`
- Gris claro: `#f5f5f5`

### Tipografías
- Encabezados: 'Playfair Display' (serif)
- Texto del cuerpo: 'Inter' (sans-serif)

### Integración con Instagram
La galería se conecta automáticamente con el feed de Instagram @elecebarber_. Para actualizar las fotos, simplemente sube nuevas publicaciones a Instagram.

## 📱 Breakpoints Responsive

- Móvil: 480px e inferior
- Tablet: 768px e inferior  
- Desktop: 769px y superior

## 🔧 Desarrollo

### Organización de Archivos
- Mantén todo el CSS en `css/styles.css`
- Mantén todo el JavaScript en `js/script.js`
- Agrega nuevas imágenes a la carpeta `images/`

### Optimización de Rendimiento
- Las imágenes deben estar optimizadas (formato WebP recomendado)
- CSS y JavaScript están listos para minificación
- Las fuentes se cargan de forma asíncrona

## 🌐 Compatibilidad de Navegadores

- Chrome (última versión)
- Firefox (última versión)
- Safari (última versión)
- Edge (última versión)
- Internet Explorer 11+ (con degradación elegante)

## 📞 Información del Negocio

**ELECE BARBER**
- Ubicación: Albuixech, Valencia, España
- Dirección: C/ Miguel Hernández, 23, 46110 Albuixech, Valencia
- Horario: 
  - Lunes: Cerrado
  - Martes-Viernes: 09:30 - 13:00, 16:00 - 20:00
  - Sábado: 09:00 - 14:00
  - Domingo: Cerrado
- Instagram: [@elecebarber_](https://instagram.com/elecebarber_)
- Reservas: [Booksy](https://booksy.com/es-es/115570_elece-barber_barberia_57381_albuixech)

## 🔮 Mejoras Futuras

- [ ] Añadir más fotos y videos profesionales
- [ ] Implementar formulario de contacto con backend
- [ ] Añadir soporte multi-idioma (Valenciano/Catalán)
- [ ] Capacidades PWA (Progressive Web App)
- [ ] Integración de analytics de rendimiento
- [ ] Sistema de valoraciones en tiempo real

## 📄 Licencia

Este proyecto fue creado para ELECE BARBER. Todos los derechos reservados.

## 👨‍💻 Notas de Desarrollo

- El sitio web está diseñado para ser fácilmente mantenible
- Todas las dependencias externas se cargan vía CDN
- El código está bien comentado para fácil comprensión
- El diseño responsive sigue principios mobile-first
- Características de accesibilidad integradas (HTML semántico, ratios de contraste apropiados)

## 🚀 Despliegue

El sitio web puede ser desplegado en cualquier servicio de hosting estático:
- GitHub Pages
- Netlify
- Vercel
- Hosting web tradicional

Simplemente sube todos los archivos al directorio raíz del servidor web.

---

**Creado con ❤️ para ELECE BARBER - Barbería Profesional en Albuixech, Valencia**