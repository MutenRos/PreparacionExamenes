# Salvapantallas Netflix — Plataforma de Screensavers

![Salvapantallas Netflix](https://mutenros.github.io/Programacion-003-Proyecto-SalvantallasNetflix/)

## Introducción

Este proyecto es una plataforma web tipo Netflix dedicada a salvapantallas gratuitos (screensavers). La aplicación PHP lee un catálogo de playlists y vídeos de YouTube desde un fichero JSON generado automáticamente por un script Python (yt-dlp), y los presenta en una interfaz visual inspirada en las plataformas de streaming: hero slider, filas horizontales desplazables, ventana modal de detalle, grid con búsqueda en tiempo real y SEO optimizado con JSON-LD. El proyecto ha pasado por 6 versiones progresivas (001 a 006), cada una añadiendo funcionalidades sobre la anterior: desde la estructura básica hasta la vista completa con buscador de vídeos.

## Desarrollo de las partes

### 1. Lectura y decodificación del JSON con PHP

El archivo `index.php` comienza cargando el JSON generado por el script Python. Usa `file_get_contents()` para leer el fichero y `json_decode()` con el flag `true` para convertirlo en un array asociativo. Se valida que el fichero exista y que el JSON sea correcto antes de continuar.

```php
// 001-Ejercicios/006-lista de videos/index.php — Líneas 62-71: Carga del JSON
$data = null;
if (is_file($jsonFile)) {
  $raw = file_get_contents($jsonFile);
  if ($raw !== false) {
    $tmp = json_decode($raw, true);
    if (is_array($tmp)) $data = $tmp;
  }
}
$playlists = is_array($data['playlists'] ?? null) ? $data['playlists'] : [];
```

**Archivo:** `001-Ejercicios/006-lista de videos/index.php` · Líneas 62–71 · Ruta: `/001-Ejercicios/006-lista de videos/index.php`

### 2. Funciones de seguridad y normalización

Se definen funciones auxiliares para la seguridad del HTML. `h()` usa `htmlspecialchars()` con flags `ENT_QUOTES | ENT_SUBSTITUTE` para prevenir XSS en todas las salidas. `safe_rel_path()` previene ataques de directory traversal rechazando rutas con `..`. `slug_id()` genera identificadores URL-friendly para las playlists.

```php
// 001-Ejercicios/006-lista de videos/index.php — Líneas 33-51: Funciones de seguridad
function h(string $s): string {
  return htmlspecialchars($s, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
}

function safe_rel_path(string $path): string {
  $path = str_replace('\\', '/', $path);
  $path = ltrim($path, '/');
  if (str_contains($path, '..')) return '';
  return $path;
}

function slug_id(string $s): string {
  $s = trim(mb_strtolower($s, 'UTF-8'));
  $s = preg_replace('~[^\pL\pN]+~u', '-', $s) ?? '';
  $s = trim($s, '-');
  if ($s === '') $s = 'playlist';
  return 'pl-' . $s;
}
```

**Archivo:** `001-Ejercicios/006-lista de videos/index.php` · Líneas 33–51 · Ruta: `/001-Ejercicios/006-lista de videos/index.php`

### 3. SEO con Open Graph, Twitter Cards y JSON-LD

Se generan metaetiquetas SEO dinámicas según la página activa (`home` o `videos`). Open Graph y Twitter Card muestran datos del catálogo. Además, se construye un bloque JSON-LD `@graph` con tipos `WebSite` y `CollectionPage` que lista las playlists como `CreativeWorkSeries`, lo que mejora el posicionamiento en buscadores.

```php
// 001-Ejercicios/006-lista de videos/index.php — Líneas 127-163: JSON-LD schema
$schema = [
  '@context' => 'https://schema.org',
  '@graph' => [
    [
      '@type' => 'WebSite',
      'name' => $SITE_NAME,
      'url' => $BASE_URL,
    ],
    [
      '@type' => 'CollectionPage',
      'name' => $title,
      'url' => $canonical,
      'hasPart' => $ldPlaylists,
    ]
  ]
];
```

**Archivo:** `001-Ejercicios/006-lista de videos/index.php` · Líneas 127–163 · Ruta: `/001-Ejercicios/006-lista de videos/index.php`

### 4. Hero slider con carousel de playlists

La página principal muestra un hero slider con las playlists destacadas. Cada slide tiene la thumbnail como fondo, un degradado (`heroShade`), el título, descripción y dos botones de acción (abrir en YouTube / ver vídeos abajo). Las flechas y los dots de navegación permiten cambiar de slide. La rotación automática usa `setInterval` cada 5 segundos y se pausa al hacer hover.

```php
// 001-Ejercicios/006-lista de videos/index.php — Líneas 665-690: Generación de slides
<div class="heroSlide <?= $activeClass ?>"
     data-index="<?= (int)$idx ?>"
     data-plid="<?= h($plId) ?>"
     data-url="<?= h($plUrl) ?>"
     style="<?= $bg ?>">
  <div class="heroShade"></div>
  <div class="heroInner">
    <div class="heroText">
      <div class="heroKicker">Free screensavers playlist</div>
      <div class="heroTitle"><?= h($plTitle) ?></div>
      <div class="heroDesc"><?= h(trim($plDesc)) ?></div>
    </div>
  </div>
</div>
```

**Archivo:** `001-Ejercicios/006-lista de videos/index.php` · Líneas 665–690 · Ruta: `/001-Ejercicios/006-lista de videos/index.php`

### 5. Filas horizontales de vídeos estilo Netflix

Las playlists se renderizan como filas horizontales con scroll lateral. Cada vídeo es un `<article>` con la thumbnail de fondo y metadatos. Los botones `.izquierda` y `.derecha` desplazan la tira usando JS que modifica `tira.style.left`. El contenedor usa `width:20000px` con `flex` para crear el efecto de scroll infinito.

```php
// 001-Ejercicios/006-lista de videos/index.php — Líneas 750-775: Artículo de vídeo
<article
  data-url="<?= h($vurl) ?>"
  data-title="<?= h($vttl) ?>"
  data-desc="<?= h($desc) ?>"
  data-thumb="<?= h($thumbSrc) ?>"
  style="<?= $thumbSrc ? 'background:url('.h($thumbSrc).');background-size:cover;' : '' ?>"
>
  <div class="meta">
    <div class="vtitle"><?= h($vttl) ?></div>
    <div class="vlink"><?= h($vurl) ?></div>
  </div>
</article>
```

**Archivo:** `001-Ejercicios/006-lista de videos/index.php` · Líneas 750–775 · Ruta: `/001-Ejercicios/006-lista de videos/index.php`

### 6. Ventana modal de detalle del vídeo

Al hacer clic en cualquier vídeo (fila o grid), se abre una ventana modal superpuesta con la thumbnail ampliada, título, URL, descripción y un botón para ver en YouTube. La modal se cierra con `Escape`, clic fuera o el botón ✕. El JS extrae los datos de los atributos `data-*` del elemento clicado.

```javascript
// 001-Ejercicios/006-lista de videos/index.php — Líneas 937-952: Apertura del modal
function openModal({title, desc, url, thumb}){
  mTitle.textContent = title || "Untitled";
  mUrl.textContent   = url || "";
  mGo.href           = url || "#";
  const d = (desc || "").trim();
  mDesc.textContent = d ? d : "No description available.";
  if (thumb) {
    mThumb.src = thumb;
    mThumb.style.display = "block";
  } else {
    mThumb.removeAttribute("src");
    mThumb.style.display = "none";
  }
  overlay.classList.add("abierto");
}
```

**Archivo:** `001-Ejercicios/006-lista de videos/index.php` · Líneas 937–952 · Ruta: `/001-Ejercicios/006-lista de videos/index.php`

### 7. Vista "All videos" con grid responsive y búsqueda

La página `?page=videos` muestra todos los vídeos en un grid CSS responsive que se adapta de 5 a 1 columna con media queries. El buscador filtra en tiempo real comparando el texto con `data-search` (título + url + playlist), sin recargar la página. Un contador muestra cuántos vídeos coinciden.

```javascript
// 001-Ejercicios/006-lista de videos/index.php — Líneas 1055-1067: Filtro de búsqueda
function applyFilter(){
  if(!q || !grid) return;
  const needle = (q.value || "").trim().toLowerCase();
  let shown = 0;
  grid.querySelectorAll(".gridItem").forEach(function(item){
    const hay = (item.getAttribute("data-search") || "");
    const ok = !needle || hay.includes(needle);
    item.style.display = ok ? "" : "none";
    if(ok) shown++;
  });
  if(countVisible) countVisible.textContent = String(shown);
}
```

**Archivo:** `001-Ejercicios/006-lista de videos/index.php` · Líneas 1055–1067 · Ruta: `/001-Ejercicios/006-lista de videos/index.php`

### 8. Menú hamburguesa con navegación lateral

El menú lateral (nav) se despliega con el icono hamburguesa ☰ usando la clase CSS `.sacado`. La transición animada mueve la nav de `left:-320px` a `left:0`. El nav lista todas las playlists con su número de vídeos y permite hacer scroll suave a cada sección de la página.

```css
/* 001-Ejercicios/006-lista de videos/index.php — Líneas 221-230: CSS del nav lateral */
nav{
  width:320px;
  background:midnightblue;
  position:fixed;
  height:100%;
  padding:18px 16px;
  box-sizing:border-box;
  left:-320px;
  transition:all 400ms ease;
  z-index:1000;
}
.sacado{ left:0px; }
```

**Archivo:** `001-Ejercicios/006-lista de videos/index.php` · Líneas 221–230 · Ruta: `/001-Ejercicios/006-lista de videos/index.php`

### 9. Script Python — Scraping de YouTube con yt-dlp

El script `listas.py` es el motor de datos del proyecto. Usa `subprocess` para ejecutar `yt-dlp` con `--dump-single-json`, descarga los metadatos de todas las playlists del canal YouTube, filtra vídeos privados/eliminados, descarga las thumbnails a disco y genera el JSON que PHP consume.

```python
# 001-Ejercicios/006-lista de videos/listas.py — Líneas 26-48: Ejecución de yt-dlp
def run_ytdlp_json(url: str, flat: bool = True) -> Dict[str, Any]:
    cmd = ["yt-dlp", "--dump-single-json", "--no-warnings"]
    if flat:
        cmd.append("--flat-playlist")
    cmd.append(url)
    res = subprocess.run(
        cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    if res.returncode != 0:
        raise RuntimeError(f"yt-dlp failed for URL: {url}")
    return json.loads(res.stdout)
```

**Archivo:** `001-Ejercicios/006-lista de videos/listas.py` · Líneas 26–48 · Ruta: `/001-Ejercicios/006-lista de videos/listas.py`

### 10. Descarga de thumbnails y generación del JSON

El script Python descarga cada thumbnail con `urllib.request.urlretrieve()` en formato WebP, las guarda en carpetas locales (`thumbnails/` y `playlist_thumbnails/`), y anota la ruta relativa en el JSON. Al final muestra un resumen con estadísticas del scraping (playlists, vídeos, errores).

```python
# 001-Ejercicios/006-lista de videos/listas.py — Líneas 97-120: Descarga de thumbnail
def download_thumbnail(video_url: str, dest_dir: str) -> Optional[str]:
    try:
        info = run_ytdlp_json(video_url, flat=False)
    except Exception:
        return None
    thumb_url = _pick_best_thumbnail_url(info.get("thumbnails"))
    if not thumb_url:
        return None
    vid = info.get("id") or "unknown"
    ext = _guess_ext(thumb_url)
    out_path = os.path.join(dest_dir, f"{vid}.{ext}")
    urllib.request.urlretrieve(thumb_url, out_path)
    return out_path
```

**Archivo:** `001-Ejercicios/006-lista de videos/listas.py` · Líneas 97–120 · Ruta: `/001-Ejercicios/006-lista de videos/listas.py`

### 11. CSS responsive y diseño adaptativo

El diseño se adapta a todos los tamaños de pantalla. El grid de vídeos usa `grid-template-columns: repeat(auto-fit, minmax())` con media queries a 1400, 1100, 820 y 520px. La modal cambia de layout horizontal a vertical en pantallas pequeñas (<780px). Toda la interfaz oscura usa `rgba()` para transparencias consistentes.

```css
/* 001-Ejercicios/006-lista de videos/index.php — Líneas 468-472: Media queries grid */
.grid{ display:grid; grid-template-columns: repeat(5, minmax(0, 1fr)); gap:12px; }
@media (max-width: 1400px){ .grid{ grid-template-columns: repeat(4, minmax(0,1fr)); } }
@media (max-width: 1100px){ .grid{ grid-template-columns: repeat(3, minmax(0,1fr)); } }
@media (max-width: 820px){ .grid{ grid-template-columns: repeat(2, minmax(0,1fr)); } }
@media (max-width: 520px){ .grid{ grid-template-columns: repeat(1, minmax(0,1fr)); } }
```

**Archivo:** `001-Ejercicios/006-lista de videos/index.php` · Líneas 468–472 · Ruta: `/001-Ejercicios/006-lista de videos/index.php`

### 12. Mejoras aplicadas — UX y accesibilidad

Se agregaron mejoras sobre el código original: `scroll-behavior:smooth` para navegación suave, transiciones `transform:scale(1.03)` en hover de las tarjetas, `focus-visible` para navegación con teclado, un botón flotante "back to top" que aparece al hacer scroll, y estadísticas del catálogo en el footer (playlists + vídeos).

```css
/* 001-Ejercicios/006-lista de videos/index.php — Líneas 203-212: Mejoras CSS */
html{ scroll-behavior:smooth; }
:focus-visible{
  outline:2px solid rgba(120,160,255,.7);
  outline-offset:2px;
}
section.row article{ transition: border-color .25s ease, transform .25s ease; }
section.row article:hover{ transform: scale(1.03); }
```

**Archivo:** `001-Ejercicios/006-lista de videos/index.php` · Líneas 203–212 · Ruta: `/001-Ejercicios/006-lista de videos/index.php`

### 13. Progresión del proyecto — 6 versiones

El proyecto muestra la evolución del aprendizaje a través de 6 carpetas numeradas, cada una construyendo sobre la anterior: 001-Inicio (estructura básica y lectura JSON, 281 líneas), 002-Ventana modal (modal de detalle, 464 líneas), 004-Título y héroe (hero slider, 687 líneas), 005-Mejoras SEO (metaetiquetas y JSON-LD, 916 líneas), 006-Lista de vídeos (grid responsive con búsqueda, 1093 líneas).

```
001-Ejercicios/
├── 001-Inicio/              → 281 líneas — Estructura base + JSON
├── 002-Ventana modal/       → 464 líneas — Modal de detalle
├── 003-recapitulacion.md    → Notas sobre publicación web
├── 004-titulo y heroe/      → 687 líneas — Hero slider
├── 005-Mejoras SEO/         → 916 líneas — SEO + JSON-LD
└── 006-lista de videos/     → 1093 líneas — Grid + Búsqueda (final)
```

**Archivo:** Estructura completa de 001-Ejercicios/ · Ruta: `/001-Ejercicios/`

## Presentación del proyecto

ScreenSaver.es es una plataforma web tipo Netflix que presenta vídeos de salvapantallas gratuitos organizados por playlists temáticas: Motivational Sentences, Colors, Fish Tank, Matrix, Espirógrafos, Relojes y Fluidos. El catálogo incluye más de 230 vídeos con thumbnails descargadas y un total de 8 playlists.

La página principal tiene un hero slider que rota entre las playlists destacadas, mostrando la thumbnail de la playlist como fondo con un degradado cinematográfico. Debajo, las filas horizontales estilo Netflix permiten explorar los vídeos de cada playlist con botones de desplazamiento lateral. Al hacer clic en cualquier vídeo se abre una ventana modal con la imagen ampliada, la descripción y un botón para verlo directamente en YouTube.

La vista "All videos" muestra los más de 230 vídeos en un grid responsive que se adapta de 5 a 1 columna según el ancho de pantalla. Un buscador en tiempo real filtra vídeos por título, URL o playlist sin recargar la página. El menú hamburguesa despliega una navegación lateral con todas las playlists y su número de vídeos.

Todo el contenido procede de un script Python que usa yt-dlp para extraer automáticamente los metadatos y thumbnails del canal de YouTube. El JSON generado es consumido por PHP, separando la obtención de datos (Python) de la presentación (PHP+HTML+CSS+JS). Este es un proyecto multitecnología: Python para el scraping, PHP para el backend, HTML/CSS para la maquetación responsive y JavaScript para la interactividad del slider, modal, scroll y buscador.

## Conclusión

Este proyecto demuestra cómo construir una plataforma web completa combinando cuatro tecnologías: Python para la obtención automática de datos desde YouTube, PHP para el procesamiento del servidor y la generación dinámica de HTML, CSS para un diseño responsive tipo streaming con tema oscuro, y JavaScript para la interactividad (slider, modal, scroll, búsqueda). La progresión en 6 versiones muestra el aprendizaje iterativo: cada paso añade una funcionalidad concreta sin romper lo anterior. La implementación de medidas de seguridad (htmlspecialchars, safe_rel_path), SEO (Open Graph, JSON-LD) y accesibilidad (focus-visible, aria-labels, noscript) refleja las buenas prácticas del desarrollo web moderno a nivel de primer curso de DAM.
