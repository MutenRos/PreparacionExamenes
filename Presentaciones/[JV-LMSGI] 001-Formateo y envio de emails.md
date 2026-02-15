# Formateo y envío de emails HTML

![Newsletter JOCARSA](101-Ejercicios/banner.jpg)

## Introducción

Este proyecto aborda la maquetación de newsletters corporativas en formato HTML compatibles con clientes de correo electrónico. A diferencia del desarrollo web moderno, los emails HTML requieren técnicas de maquetación basadas en tablas, ya que la mayoría de clientes de correo (Gmail, Outlook, Thunderbird) no soportan CSS Grid, Flexbox ni muchas propiedades CSS actuales. A lo largo de 10 ejercicios evolutivos, se construye paso a paso un email profesional para la empresa ficticia JOCARSA, desde una tabla básica hasta un newsletter completo con imagen corporativa, sección destacada, banner, bloques de contenido y pie de página normativo RGPD.

## Desarrollo de las partes

### 1. Introducción teórica — Limitaciones del email HTML

Se parte de la base teórica de que los clientes de correo soportan HTML y CSS, pero solo un subconjunto muy limitado. No se puede usar Grid, Flexbox ni maquetación moderna; todo debe hacerse con tablas anidadas y estilos inline.

```
Los clientes de correo electrónico soportan HTML y CSS
Pero - no soportan la mayor parte de las características modernas
Por ejemplo, todo se tiene que hacer con tablas
```

- **Archivo:** `101-Ejercicios/001-Introduccion.md`
- **Líneas:** 1-10
- **Ruta:** `101-Ejercicios/001-Introduccion.md`

### 2. Tabla base de tres columnas

Se crea la estructura fundamental: una tabla HTML con tres columnas (izquierda, centro, derecha). Las columnas laterales actúan como márgenes y la central aloja el contenido del email.

```html
<table border=1>
  <tr>
    <td>Izquierda</td>
    <td>Centro</td>
    <td>Derecha</td>
  </tr>
</table>
```

- **Archivo:** `101-Ejercicios/002-tabla de inicio.html`
- **Líneas:** 1-9
- **Ruta:** `101-Ejercicios/002-tabla de inicio.html`

### 3. Control de anchuras

Se asigna `width=100%` a la tabla exterior para que ocupe todo el ancho y `width=400px` a la celda central para fijar el ancho del contenido del email.

```html
<table border=1 width=100%>
  <tr>
    <td></td>
    <td width=400px>Centro</td>
    <td></td>
  </tr>
</table>
```

- **Archivo:** `101-Ejercicios/003-anchura de las celdas.html`
- **Líneas:** 1-9
- **Ruta:** `101-Ejercicios/003-anchura de las celdas.html`

### 4. Subtabla con secciones del email

Dentro de la celda central se introduce una subtabla con cinco filas que representan las secciones típicas de un newsletter: Logo, Destacado, Banner, Razones y Pie de página.

```html
<table border=1 width=100%>
  <tr><td>Logo</td></tr>
  <tr><td>Destacado</td></tr>
  <tr><td>Banner</td></tr>
  <tr><td>Razones</td></tr>
  <tr><td>Pie de pagina</td></tr>
</table>
```

- **Archivo:** `101-Ejercicios/004-subtabla.html`
- **Líneas:** 7-20
- **Ruta:** `101-Ejercicios/004-subtabla.html`

### 5. Imagen corporativa (logo + marca)

Se desarrolla la sección del logo: una tabla interna con el logotipo SVG de JOCARSA a la derecha, y a su lado el nombre de la empresa (`<h1>`) y el eslogan (`<h2>`), todo sobre un fondo color índigo con texto blanco.

```html
<tr style="background:indigo;color:white;">
  <td>
    <table>
      <tr>
        <td><img src="https://static.jocarsa.com/logos/jocarsa%20%7C%20White.svg" width=100px></td>
        <td>
          <h1 style="margin:0px;">JOCARSA</h1>
          <h2 style="font-size:12px;margin:0px;">Soluciones de software empresarial</h2>
        </td>
      </tr>
    </table>
  </td>
</tr>
```

- **Archivo:** `101-Ejercicios/005-imagen corporativa.html`
- **Líneas:** 10-24
- **Ruta:** `101-Ejercicios/005-imagen corporativa.html`

### 6. Sección destacada con llamada a la acción (CTA)

Se crea la sección comercial destacada con un eslogan (`<h4>`), un mensaje principal (`<h3>`), un párrafo descriptivo y un botón de "Saber más". Todos los estilos están aplicados inline.

```html
<tr>
  <td style="text-align:center;">
    <h4 style="text-align:center;margin:0px;">Slogan del destacado</h4>
    <h3 style="text-align:center;margin:0px;">Mensaje principal</h3>
    <p style="text-align:justify;margin:10px;font-size:10px;">Texto atractivo...</p>
    <button style="text-align:center;margin:0px;margin:auto;">Saber más</button>
  </td>
</tr>
```

- **Archivo:** `101-Ejercicios/006-creamos el destacado.html`
- **Líneas:** 25-40
- **Ruta:** `101-Ejercicios/006-creamos el destacado.html`

### 7. Inserción de imagen banner y eliminación de bordes

Se añade `<meta charset="utf-8">` para la correcta codificación de caracteres especiales. Se cambia `border=1` a `border=0` para que las tablas sean invisibles (como en un email real). Se incluye una imagen de banner en la fila correspondiente.

```html
<meta charset="utf-8">
...
<table border=0 width=100% style="font-family:sans-serif;">
...
<tr>
  <td><img src="josevicente.jpg"></td>
</tr>
```

- **Archivo:** `101-Ejercicios/007-insercion de imagen.html`
- **Líneas:** 1-4, 7, 41-43
- **Ruta:** `101-Ejercicios/007-insercion de imagen.html`

### 8. Imagen del logo en base64

Se sustituye la referencia al logo SVG externo por una imagen PNG codificada en base64 directamente incrustada en el HTML. Esto garantiza que el logo se muestre correctamente en clientes de correo que bloquean imágenes externas por seguridad.

```html
<td>
  <img src="data:image/png;base64,iVBORw0KGgoAAAA..." width=100px>
</td>
```

- **Archivo:** `101-Ejercicios/008-destacados.html`
- **Líneas:** 14 (logo base64), 43 (banner base64)
- **Ruta:** `101-Ejercicios/008-destacados.html`

### 9. Ampliación de ancho y sección de razones

Se amplía el ancho de la celda central de 400px a 600px para mejorar la legibilidad. Se desarrolla la sección "Razones" con tres filas, cada una conteniendo una imagen y un bloque de texto justificado (50%/50%), simulando las ventajas del producto.

```html
<td width=600px>
...
<table width=100%>
  <tr>
    <td width=50%><img src="destacado.jpg" width=100%></td>
    <td width=50% style="font-size:10px;text-align:justify;padding-left:10px;">
      Lorem ipsum dolor sit amet...
    </td>
  </tr>
  <!-- Se repite 3 veces -->
</table>
```

- **Archivo:** `101-Ejercicios/009-ampliamos un poco.html`
- **Líneas:** 10 (width=600px), 48-79 (razones)
- **Ruta:** `101-Ejercicios/009-ampliamos un poco.html`

### 10. Pie de página normativo (RGPD)

Se añade la sección final del email: un pie de página con texto normativo de protección de datos conforme al RGPD. Incluye información sobre el responsable del tratamiento, la finalidad del envío, los derechos del usuario (acceso, rectificación, supresión, etc.) y las instrucciones para darse de baja.

```html
<tr>
  <td style="text-align:center;font-size:10px;color:grey;padding:10px;">
    Protección de datos:<br>
    Recibe esta comunicación porque forma parte de nuestra base
    de datos de contactos comerciales...
    Usted puede ejercer en cualquier momento sus derechos de acceso,
    rectificación, supresión, oposición...
  </td>
</tr>
```

- **Archivo:** `101-Ejercicios/010-pie de pagina normativo.html`
- **Líneas:** 82-93
- **Ruta:** `101-Ejercicios/010-pie de pagina normativo.html`

### 11. Mejoras aplicadas por el alumno

Se han realizado las siguientes mejoras sobre el archivo más avanzado (010):

- **`lang="es"`** en la etiqueta `<html>` para indicar el idioma del documento.
- **`<title>`** en el `<head>` para SEO y accesibilidad.
- **Atributos `alt`** en todas las imágenes `destacado.jpg` para accesibilidad.
- **`border="0"`** en imágenes para evitar bordes azules en ciertos clientes de correo.
- **`cellpadding` y `cellspacing`** en las tablas para un control preciso del espaciado.
- **Sustitución de `<button>` por `<a>` estilizado** como botón, ya que `<button>` no funciona en la mayoría de clientes de correo.
- **Comentarios HTML** descriptivos para identificar cada sección del email.
- **Datos reales en el pie RGPD**, sustituyendo los marcadores `[Nombre de la empresa]`, `[correo de bajas]`, etc.
- **Resumen de conceptos** en `301-Resumen/001-Resumen.md`.

- **Archivo:** `101-Ejercicios/010-pie de pagina normativo.html`
- **Líneas:** 1-3 (lang, title), 39-41 (enlace CTA), 53-57 (alt+border en imgs), 82 (comentario RGPD)
- **Ruta:** `101-Ejercicios/010-pie de pagina normativo.html`

## Presentación del proyecto

Este proyecto demuestra cómo se construye, paso a paso, un newsletter corporativo en HTML compatible con clientes de correo electrónico. Partiendo de una simple tabla de tres columnas, se va añadiendo complejidad progresivamente hasta obtener un email completo y profesional.

![Banner del newsletter](101-Ejercicios/banner.jpg)

El resultado final es un email de la empresa JOCARSA con las siguientes secciones:

1. **Cabecera corporativa** con el logotipo de la empresa sobre fondo índigo y el eslogan "Soluciones de software empresarial".
2. **Sección destacada** con un mensaje comercial central y un botón de llamada a la acción (CTA) "Saber más".
3. **Banner visual** con una imagen a ancho completo que refuerza la identidad visual del email.
4. **Tres bloques de contenido** ("Razones") que combinan imagen y texto, presentando las ventajas del producto o servicio.
5. **Pie de página normativo** con toda la información legal requerida por el RGPD: responsable del tratamiento, finalidad, derechos del usuario y procedimiento de baja.

![Imagen de contenido destacado](101-Ejercicios/destacado.jpg)

La técnica de maquetación con tablas, aunque arcaica comparada con el desarrollo web actual, es la única forma fiable de conseguir que un email se muestre correctamente en la inmensa diversidad de clientes de correo existentes (Gmail, Outlook, Yahoo Mail, Apple Mail, Thunderbird, etc.). Cada uno interpreta el HTML y CSS de manera diferente, y las tablas son el denominador común.

Las imágenes del logo y el banner se han incrustado en formato base64 para garantizar su visualización incluso cuando el cliente de correo bloquea las imágenes externas por defecto.

## Conclusión

Este proyecto es una introducción práctica y progresiva al mundo de la maquetación de emails HTML. A través de 10 ejercicios incrementales, hemos pasado de una tabla vacía a un newsletter corporativo completo que incluye todos los elementos que encontraríamos en un email comercial real: identidad de marca, contenido destacado, imágenes, bloques informativos y cumplimiento normativo RGPD.

La principal lección aprendida es que el email HTML opera bajo restricciones muy diferentes a las del desarrollo web moderno. No se puede confiar en CSS moderno, JavaScript ni hojas de estilo externas. Todo debe resolverse con tablas anidadas, estilos inline y técnicas que ya se consideraban obsoletas en el desarrollo web, pero que siguen siendo el estándar de facto en el email marketing.

Las mejoras aplicadas (accesibilidad con `alt`, compatibilidad con `<a>` en lugar de `<button>`, atributos de tabla, datos RGPD reales) demuestran una comprensión no solo de la técnica de maquetación, sino también de las buenas prácticas de accesibilidad, compatibilidad cross-client y cumplimiento legal que todo desarrollador debe conocer al trabajar con emails HTML.
