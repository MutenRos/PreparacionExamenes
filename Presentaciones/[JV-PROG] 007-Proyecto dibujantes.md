# Proyecto dibujantes — Portal web de tutoriales de dibujo

![Portada del proyecto](101-Ejercicios/005-Proyecto/thumbnails/WeM920s9xHA.jpg)

## Introducción

Este proyecto consiste en la creación de un portal web completo dedicado al canal de YouTube **@dibujantes**, que ofrece tutoriales de dibujo a mano alzada. El desarrollo abarca desde la extracción automatizada de datos de YouTube mediante Python y yt-dlp, pasando por el almacenamiento en SQLite, hasta la construcción de una interfaz web en PHP con estética de papel y lápiz. El resultado es un sitio funcional con página de inicio, galería, tutoriales, sección "sobre mí" y páginas legales, alimentado dinámicamente por los datos del canal.

---

## Desarrollo de las partes

### 1. Scraper inicial: conexión con YouTube

El primer ejercicio establece la conexión con el canal de YouTube utilizando `yt-dlp` como herramienta de extracción. Se descarga la lista de vídeos, se extraen metadatos (título, descripción, thumbnail, duración, fecha) y se almacenan en SQLite con modo incremental para no reprocesar vídeos ya guardados.

```python
# Archivo: 101-Ejercicios/001-conectar a youtube.py, líneas 35-38
CHANNEL_URL = "https://www.youtube.com/@dibujantes"
DB_PATH = "youtube_videos.sqlite"
SLEEP_BETWEEN_VIDEOS = 0.2
MAX_VIDEOS = 0              # 0 = todos
```

La función `upsert_video` utiliza `INSERT … ON CONFLICT` para escritura idempotente:

```python
# Archivo: 101-Ejercicios/001-conectar a youtube.py, líneas 133-155
conn.execute("""
    INSERT INTO videos (...)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    ON CONFLICT(video_id) DO UPDATE SET ...
""", (...))
```

### 2. Mejoras en la extracción de datos

La segunda iteración mejora la fiabilidad del scraper. Apunta explícitamente a la URL `/videos` del canal, filtra IDs que empiezan por "UC" (canales, no vídeos) y añade el campo `thumbnail_local_url` con formato `file://` al esquema de la base de datos.

```python
# Archivo: 101-Ejercicios/002-mejoras.py, líneas 17-18
CHANNEL_URL = "https://www.youtube.com/@dibujantes"
CHANNEL_VIDEOS_URL = CHANNEL_URL.rstrip("/") + "/videos"
```

```python
# Archivo: 101-Ejercicios/002-mejoras.py, líneas 137-144
def extract_video_id_from_entry(entry):
    for k in ("webpage_url", "url"):
        v = entry.get(k)
        if isinstance(v, str) and "watch?v=" in v:
            return v.split("watch?v=", 1)[1].split("&", 1)[0]
    vid = entry.get("id")
    if isinstance(vid, str) and not vid.startswith("UC"):
        return vid
```

### 3. Soporte de Shorts y tipos de vídeo

La tercera versión del scraper añade soporte para YouTube Shorts, extrayendo contenido tanto de `/videos` como de `/shorts`. La base de datos incorpora una columna `type` con restricción CHECK que solo admite `'video'` o `'short'`, permitiendo clasificar el contenido.

```python
# Archivo: 101-Ejercicios/003-mas mejoras.py, líneas 14-16
CHANNEL_VIDEOS_URL = CHANNEL_BASE + "/videos"
CHANNEL_SHORTS_URL = CHANNEL_BASE + "/shorts"
```

```sql
-- Archivo: 101-Ejercicios/003-mas mejoras.py, líneas 28-30 (esquema SQL)
CREATE TABLE IF NOT EXISTS videos (
  video_id TEXT PRIMARY KEY,
  type     TEXT NOT NULL CHECK(type IN ('video','short')),
  ...
);
```

Se incluye manejo de errores en la descarga de thumbnails para que un fallo no interrumpa el proceso:

```python
# Archivo: 101-Ejercicios/003-mas mejoras.py, líneas 138-145
if not os.path.exists(thumb_path):
    try:
        download_file(thumb_url, thumb_path)
    except Exception as e:
        print(f"[{i}/{total}] Aviso: no se pudo descargar thumbnail ({vid}): {e}")
        thumb_path = None
```

### 4. Prueba de concepto en PHP

Un ejercicio mínimo de 11 líneas que abre la base SQLite desde PHP y vuelca todos los registros como HTML. Demuestra la viabilidad de conectar el backend de datos con la capa web.

```php
<!-- Archivo: 101-Ejercicios/004-web minima.php, líneas 1-11 -->
<?php
$basededatos = new SQLite3('youtube_videos.sqlite');
$resultado = $basededatos->query("SELECT * FROM videos");
while ($fila = $resultado->fetchArray(SQLITE3_ASSOC)) {
    echo '<article>';
    foreach($fila as $clave=>$valor){
        echo '<p>'.$clave.": ".$valor.'</p>';
    }
    echo '</article>';
}
?>
```

### 5. Scraper completo con playlists

La versión final del scraper añade la extracción de **playlists** del canal. Se crea una tabla `playlists` independiente con campos específicos como `entry_count`. Los thumbnails de vídeos y playlists se separan en subdirectorios distintos.

```python
# Archivo: 101-Ejercicios/005-Proyecto/videos y playlists.py, líneas 54-67
CREATE TABLE IF NOT EXISTS playlists (
  playlist_id         TEXT PRIMARY KEY,
  channel_url         TEXT NOT NULL,
  title               TEXT,
  description         TEXT,
  thumbnail_url       TEXT,
  thumbnail_path      TEXT,
  thumbnail_local_url TEXT,
  entry_count         INTEGER,
  added_at_utc        TEXT NOT NULL,
  updated_at_utc      TEXT NOT NULL
);
```

```python
# Archivo: 101-Ejercicios/005-Proyecto/videos y playlists.py, líneas 101-112
def extract_playlist_id(entry):
    for k in ("webpage_url", "url", "original_url"):
        v = entry.get(k)
        if isinstance(v, str) and "list=" in v:
            after = v.split("list=", 1)[1]
            pid = after.split("&", 1)[0]
            if pid:
                return pid
```

### 6. Cabecera PHP con SEO y datos estructurados

El archivo de cabecera compartido incluye metadatos SEO completos: Open Graph, Twitter Card, JSON-LD para `WebSite` y `Organization`, favicon, canonical, preload del CSS y navegación principal con enlace activo.

```php
<!-- Archivo: 101-Ejercicios/005-Proyecto/inc/cabecera.php, líneas 10-15 -->
<meta name="description" content="Tutoriales de dibujo a mano alzada: anime, superhéroes, retrato...">
<meta name="keywords" content="dibujar, dibujo a mano alzada, tutoriales de dibujo...">
<meta name="robots" content="index,follow,max-image-preview:large,...">
```

```html
<!-- Archivo: 101-Ejercicios/005-Proyecto/inc/cabecera.php, líneas 60-73 -->
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "WebSite",
  "name": "dibujant.es",
  "url": "https://dibujant.es/",
  ...
}
</script>
```

### 7. Página de inicio dinámica

La página de inicio combina secciones estáticas (hero, cursos, newsletter) con contenido dinámico extraído de SQLite. Muestra las 3 primeras playlists como accesos rápidos y los 6 últimos vídeos ordenados por fecha. Se aplica `htmlspecialchars` a toda la salida dinámica para prevenir XSS.

```php
<!-- Archivo: 101-Ejercicios/005-Proyecto/index.php, líneas 75-82 -->
$resultado = $basededatos->query("SELECT * FROM videos ORDER BY upload_date DESC LIMIT 6");
while ($fila = $resultado->fetchArray(SQLITE3_ASSOC)) {
    $tituloVideo = htmlspecialchars($fila['title'], ENT_QUOTES, 'UTF-8');
    $tipoVideo   = htmlspecialchars($fila['type'],  ENT_QUOTES, 'UTF-8');
    echo '<a class="media-card paper-card" href="https://www.youtube.com/watch?v='.$codigo.'">';
```

### 8. Galería con cuadrícula masonry

La página de galería presenta colecciones estáticas (Retratos, Objetos, Paisajes) y una sección dinámica "Últimas piezas" que carga todos los vídeos en una cuadrícula masonry de 4 columnas aplicando los thumbnails como fondo CSS.

```php
<!-- Archivo: 101-Ejercicios/005-Proyecto/galeria.php, líneas 50-57 -->
$basededatos = new SQLite3('youtube_videos.sqlite');
$resultado = $basededatos->query("SELECT * FROM videos");
while ($fila = $resultado->fetchArray(SQLITE3_ASSOC)) {
    $titulo = htmlspecialchars($fila['title'], ENT_QUOTES, 'UTF-8');
    $thumb  = htmlspecialchars($fila['thumbnail_path'], ENT_QUOTES, 'UTF-8');
    echo '<a class="shot paper-card" href="#">
        <span class="shot-img s1" style="background:url(\''.$thumb.'\')..."></span>
        <span class="shot-cap">'.$titulo.'</span></a>';
```

### 9. Hoja de estilos: estética papel y lápiz

La hoja CSS de 577+ líneas define una identidad visual completa basada en papel artesanal. Utiliza variables CSS, gradientes radiales para simular textura, líneas de esbozo con `repeating-linear-gradient` y un efecto vignette sutil. Incluye accesibilidad con `:focus-visible` y respeta `prefers-reduced-motion`.

```css
/* Archivo: 101-Ejercicios/005-Proyecto/style.css, líneas 1-20 */
:root{
  --ink:#1f2328;   --muted:#5e6a76;
  --paper:#f6f1e7; --paper2:#efe6d6; --paper3:#fbf7ef;
  --line:#d7cdbb;  --line2:#cbbfa9;
  --red:#c62828;   --red2:#a81818;
  --gold:#d6a23b;  --brown:#8b5e3b;
  --radius:18px;   --wrap:1100px;
}
```

```css
/* Archivo: 101-Ejercicios/005-Proyecto/style.css, accesibilidad */
:focus-visible{
  outline:2px solid var(--red);
  outline-offset:2px;
}
@media (prefers-reduced-motion: reduce){
  *{transition-duration:0s !important;animation-duration:0s !important}
}
```

### 10. Formulario de contacto con validación

La página "Sobre mí" incluye un formulario de contacto con validación HTML5: campos requeridos, longitudes mínimas y máximas para nombre, email y mensaje, proporcionando feedback inmediato al usuario sin necesidad de JavaScript.

```php
<!-- Archivo: 101-Ejercicios/005-Proyecto/sobremi.php, líneas 38-43 -->
<input class="input" type="text" name="nombre" placeholder="Tu nombre"
       required minlength="2" maxlength="80">
<input class="input" type="email" name="email" placeholder="Tu correo"
       required maxlength="120">
<textarea class="textarea" name="mensaje" placeholder="Tu mensaje"
          rows="6" required minlength="10" maxlength="1000"></textarea>
```

### 11. Pie de página y enlace corregido

El footer compartido incluye enlaces a redes sociales y páginas legales. Se detectó y corrigió un error donde el enlace "Aviso legal" apuntaba incorrectamente a `politicaprivacidad.php` en lugar de `avisolegal.php`.

```php
<!-- Archivo: 101-Ejercicios/005-Proyecto/inc/piedepagina.php, línea 10 -->
<!-- ANTES (bug): ambos enlaces apuntaban a politicaprivacidad.php -->
<!-- DESPUÉS (corregido): -->
<a href="politicaprivacidad.php">POLÍTICA DE PRIVACIDAD</a> ·
<a href="avisolegal.php">AVISO LEGAL</a>
```

---

## Presentación del proyecto

Este proyecto demuestra un flujo completo de desarrollo web: desde la obtención de datos reales hasta su presentación en un portal funcional.

En primer lugar, se desarrolló un scraper en Python que se conecta al canal de YouTube **@dibujantes** usando `yt-dlp`. A lo largo de cuatro iteraciones, el scraper fue mejorando: la primera versión extraía vídeos básicos; la segunda mejoró la fiabilidad del parsing de IDs; la tercera añadió soporte para Shorts con clasificación por tipo; y la versión final incorpora la extracción de playlists con su propia tabla en la base de datos.

Los datos extraídos — más de 200 vídeos, shorts y 2 playlists — se almacenan en una base de datos SQLite con esquema normalizado, índices y escritura idempotente mediante UPSERT.

La capa web está construida en PHP con SQLite3, usando un sistema de includes para cabecera y pie de página que garantiza consistencia. La página de inicio carga dinámicamente las playlists más recientes y los últimos 6 vídeos. La galería muestra todos los vídeos en una cuadrícula masonry. Cada página aplica `htmlspecialchars` para prevenir inyección XSS.

El diseño visual sigue una estética de "papel y lápiz" coherente con la temática de dibujo: fondos con textura de papel, gradientes que simulan sombreado a lápiz, líneas de esbozo con CSS puro y un sistema de tarjetas con bordes suaves. La hoja de estilos incluye accesibilidad (`:focus-visible`, `prefers-reduced-motion`) y es responsive con breakpoints a 980px y 520px.

El sitio incluye páginas de soporte completas: tutoriales con categorías, "Sobre mí" con formulario de contacto validado, aviso legal y política de privacidad con estructura GDPR.

---

## Conclusión

El proyecto **dibujantes** muestra la integración práctica de múltiples tecnologías: Python para automatización y scraping, SQLite como almacén de datos ligero, PHP para renderizado dinámico y CSS avanzado para una identidad visual distintiva. La evolución iterativa del scraper — desde una versión básica hasta una que gestiona vídeos, shorts y playlists — refleja un proceso de desarrollo incremental real. Cada mejora aplicada (protección XSS, validación de formularios, accesibilidad, corrección de enlaces) demuestra atención al detalle y buenas prácticas de desarrollo web que van más allá de la funcionalidad básica.
