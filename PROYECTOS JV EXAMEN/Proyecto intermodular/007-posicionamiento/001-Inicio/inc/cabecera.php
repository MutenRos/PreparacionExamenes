<?php
// inc/cabecera.php
// Uso: en cada página, define $SEO = [...] antes del include, y luego include "inc/cabecera.php";

if (!isset($SEO) || !is_array($SEO)) $SEO = [];

// Base URL (auto)
$scheme = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http';
$host   = $_SERVER['HTTP_HOST'] ?? 'recortabl.es';
$base   = $scheme . '://' . $host;

// Path actual (sin fragment)
$requestUri = $_SERVER['REQUEST_URI'] ?? '/';
$canonical  = $base . preg_replace('/\?.*/', '', $requestUri);

// Defaults SEO (site-wide)
$siteName   = 'recortabl.es';
$defaultTitle = 'Recortables para imprimir | Juguetes de papel en PDF – recortabl.es';
$defaultDesc  = 'Descarga recortables infantiles en PDF: juguetes educativos para imprimir, recortar y jugar. Ideal para familias y aulas.';
$defaultImg   = $base . '/img/imgcategoria.png';

// Merge
$title = trim((string)($SEO['title'] ?? $defaultTitle));
$desc  = trim((string)($SEO['description'] ?? $defaultDesc));
$img   = trim((string)($SEO['image'] ?? $defaultImg));
$robots = trim((string)($SEO['robots'] ?? 'index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1'));

// Canonical específico (si se define)
if (!empty($SEO['canonical'])) $canonical = (string)$SEO['canonical'];

// URL de la página para OG
$pageUrl = $base . $requestUri;

// Helpers de escape
function seo_e(string $s): string { return htmlspecialchars($s, ENT_QUOTES, 'UTF-8'); }

// JSON-LD: WebSite + Organization (mínimo sólido)
$websiteJsonLd = [
  "@context" => "https://schema.org",
  "@type" => "WebSite",
  "name" => $siteName,
  "url" => $base . "/",
  "inLanguage" => "es",
  "description" => $defaultDesc,
  "publisher" => [
    "@type" => "Organization",
    "name" => $siteName,
    "url" => $base . "/"
  ]
];

// JSON-LD extra por página (si lo pasas desde $SEO['jsonld'])
$extraJsonLd = $SEO['jsonld'] ?? null;

?>
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />

  <title><?= seo_e($title) ?></title>
  <meta name="description" content="<?= seo_e($desc) ?>" />
  <meta name="robots" content="<?= seo_e($robots) ?>" />
  <meta name="referrer" content="strict-origin-when-cross-origin">

  <link rel="canonical" href="<?= seo_e($canonical) ?>" />
  <link rel="alternate" hreflang="es" href="<?= seo_e($canonical) ?>" />

  <!-- Open Graph -->
  <meta property="og:site_name" content="<?= seo_e($siteName) ?>" />
  <meta property="og:type" content="<?= seo_e($SEO['og_type'] ?? 'website') ?>" />
  <meta property="og:title" content="<?= seo_e($title) ?>" />
  <meta property="og:description" content="<?= seo_e($desc) ?>" />
  <meta property="og:url" content="<?= seo_e($pageUrl) ?>" />
  <meta property="og:image" content="<?= seo_e($img) ?>" />

  <!-- Twitter -->
  <meta name="twitter:card" content="summary_large_image" />
  <meta name="twitter:title" content="<?= seo_e($title) ?>" />
  <meta name="twitter:description" content="<?= seo_e($desc) ?>" />
  <meta name="twitter:image" content="<?= seo_e($img) ?>" />

  <!-- Performance -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>

  <!-- Fonts -->
  <link href="https://fonts.googleapis.com/css2?family=Delius&display=swap" rel="stylesheet">

  <!-- CSS -->
  <link rel="stylesheet" href="estilo/estilo.css">

  <!-- Sitemap / RSS hooks (aunque aún no exista RSS) -->
  <link rel="sitemap" type="application/xml" title="Sitemap" href="<?= seo_e($base) ?>/sitemap.xml" />

  <!-- JSON-LD -->
  <script type="application/ld+json"><?= json_encode($websiteJsonLd, JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES) ?></script>
  <?php if (is_array($extraJsonLd)) : ?>
    <script type="application/ld+json"><?= json_encode($extraJsonLd, JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES) ?></script>
  <?php endif; ?>
</head>

<body>
  <header>
    <div class="wrap">
      <a class="brand" href="index.php">
        <div class="logo">🤖</div>
        <span><b>rec</b><i>ortabl.es</i></span>
      </a>

      <nav>
        <a href="categorias.php">Categorías ▾</a>
        <a href="sobrenosotros.php">Sobre nosotros</a>
        <a href="descargas.php">Descargas</a>
        <a href="login.php">Login</a>
        <div class="search" role="search">
          <div class="icon">🔎</div>
          <form action="catalogo.php" method="POST">
            <input type="search" placeholder="Buscar..." aria-label="Buscar" name="buscar"/>
          </form>
        </div>
      </nav>
    </div>
  </header>

  <main class="wrap">

