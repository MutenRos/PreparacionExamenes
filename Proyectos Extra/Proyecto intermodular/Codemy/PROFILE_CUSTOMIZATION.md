# 🎨 Sistema de Perfiles Personalizables

## Descripción

Los usuarios de Code Dungeon ahora pueden personalizar completamente su perfil con tres opciones diferentes:

### 1. 🤖 Perfil Autogenerado (Por defecto)
- Perfil generado automáticamente
- Muestra estadísticas, logros y actividad reciente
- Actualización automática según el progreso del usuario
- Ideal para usuarios que prefieren simplicidad

### 2. 📝 Perfil Markdown
- Los usuarios escriben su perfil en Markdown
- Sintaxis simple y fácil de aprender
- Conversión automática a HTML con estilos del tema dungeon
- Preview en tiempo real

**Características soportadas:**
- Títulos: `#`, `##`, `###`
- Negrita: `**texto**`
- Cursiva: `*texto*`
- Enlaces: `[texto](url)`
- Código inline: `` `código` ``
- Bloques de código: ` ```código``` `
- Listas (automático con `-` o `*`)

### 3. 💻 Perfil HTML Personalizado
- Control total sobre el diseño
- Permite HTML con estilos inline
- Sanitización automática (remueve scripts y eventos peligrosos)
- Preview en tiempo real
- Ideal para usuarios avanzados

**Seguridad:**
- Scripts removidos automáticamente
- Event handlers bloqueados
- Solo estilos inline permitidos
- Protección XSS

## Uso

### Para cambiar el tipo de perfil:

1. Ve a tu perfil (`/profile`)
2. Haz clic en la pestaña "🎨 Personalizar"
3. Selecciona el tipo de perfil deseado
4. Edita el contenido según el tipo seleccionado
5. Usa el botón "Preview" para ver los cambios
6. Haz clic en "Guardar Personalización"

### Plantillas Disponibles

El sistema incluye 4 plantillas prediseñadas:

1. **Plantilla Markdown Simple**: Perfil básico con secciones estándar
2. **Plantilla HTML Moderna**: Diseño con gradientes y cards
3. **Plantilla Profesional**: Formato tipo CV
4. **Plantilla Gamer**: Estilo gaming con estadísticas destacadas

## Ejemplo de Markdown

```markdown
# ¡Hola! Soy Juan 👋

## Sobre mí
Soy un desarrollador apasionado por Python y JavaScript.

## Habilidades
- 🐍 Python
- 🌐 Desarrollo Web
- 💻 JavaScript

[Mi GitHub](https://github.com/usuario)
```

## Ejemplo de HTML

```html
<div style="padding: 24px; background: #1c1917; border-radius: 12px;">
  <h1 style="color: #d97706; font-size: 32px;">
    Mi Perfil Personalizado
  </h1>
  <p style="color: #d6d3d1; margin-top: 16px;">
    Desarrollador Full Stack apasionado por crear experiencias increíbles.
  </p>
</div>
```

## Almacenamiento

Los perfiles personalizados se guardan en localStorage:

- `profile_type`: Tipo de perfil seleccionado ('auto', 'markdown', 'html')
- `profile_markdown`: Contenido Markdown del usuario
- `profile_html`: Contenido HTML del usuario

## Estilos

Los estilos personalizados están en `/app/profile/profile-custom.css` e incluyen:

- Estilos para contenido Markdown renderizado
- Estilos para contenido HTML personalizado
- Colores del tema dungeon integrados
- Diseño responsive

## Paleta de Colores Recomendada

Para mantener consistencia con el tema dungeon:

- **Fondos**: `#1c1917` (stone-950), `#292524` (stone-900), `#44403c` (stone-800)
- **Texto**: `#fafaf9` (stone-100), `#d6d3d1` (stone-300)
- **Acentos**: `#d97706` (amber-700), `#fbbf24` (amber-400)
- **Bordes**: `#78716c` (stone-700)

## Funciones de Seguridad

### sanitizeHTML(html: string)
Remueve elementos peligrosos del HTML:
- Elimina todas las etiquetas `<script>`
- Remueve event handlers (`onclick`, `onload`, etc.)
- Permite solo estilos inline seguros

### markdownToHTML(markdown: string)
Convierte Markdown a HTML con clases Tailwind:
- Procesa títulos, negrita, cursiva
- Convierte links con target="_blank"
- Aplica clases CSS del tema dungeon
- Maneja bloques de código

## Mejoras Futuras

- [ ] Importar/Exportar perfiles
- [ ] Galería de perfiles de la comunidad
- [ ] Más plantillas prediseñadas
- [ ] Editor WYSIWYG para HTML
- [ ] Sintaxis highlight mejorada
- [ ] Soporte para imágenes (con límite de tamaño)
- [ ] Temas personalizados
- [ ] Compartir perfil público con URL

## Notas Técnicas

- El sistema usa `dangerouslySetInnerHTML` con sanitización previa
- Los estilos son compatibles con el tema dungeon existente
- Preview en tiempo real sin guardar cambios
- Responsive en móviles y desktop
- Compatible con todos los navegadores modernos
