# Resumen — Formateo y envío de emails

## Conceptos clave

- Los clientes de correo electrónico soportan **HTML y CSS**, pero solo un subconjunto limitado.
- **No se pueden usar** CSS Grid, Flexbox, `position`, ni la mayoría de propiedades CSS modernas.
- Toda la maquetación debe hacerse con **tablas HTML** (`<table>`, `<tr>`, `<td>`), como se hacía hace décadas.
- Los estilos deben ser **inline** (atributo `style=""`), ya que muchos clientes ignoran `<style>` en `<head>`.

## Estructura típica de un email HTML

1. **Tabla exterior** con `width=100%` para centrar el contenido.
2. **Tres columnas**: izquierda vacía | centro con contenido (ancho fijo, ej. 600px) | derecha vacía.
3. **Subtabla interior** con las secciones del email:
   - Logo / imagen corporativa
   - Sección destacada (slogan + CTA)
   - Imagen de banner
   - Bloques de contenido (razones / productos)
   - Pie de página normativo (RGPD)

## Buenas prácticas

- Usar `cellpadding="0"` y `cellspacing="0"` para control preciso del espaciado.
- Incluir `alt` en todas las imágenes por accesibilidad.
- Usar `border="0"` en imágenes para evitar bordes azules en algunos clientes.
- Preferir `<a>` estilizado sobre `<button>` para los botones de acción (CTA), ya que `<button>` no funciona en todos los clientes de correo.
- Incluir pie de página normativo con información de protección de datos (RGPD).
- Usar `lang="es"` en `<html>` y `<meta charset="utf-8">` para la correcta codificación de caracteres.
