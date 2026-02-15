<?php
declare(strict_types=1);

/*
  index.php
  - Two views in one file:
      ?page=home   (default)  -> frontpage (hero + playlist rows)
      ?page=videos             -> all videos grid + search
  - Same modal behavior in both views
  - Left nav: playlists list + scroll to playlist (home view)
  - SEO meta + JSON-LD
*/

header('Content-Type: text/html; charset=utf-8');

$jsonFile = __DIR__ . '/channel_playlists_with_videos.json';

/* =========================
   SITE CONFIG (SEO)
========================= */
$SITE_NAME = 'ScreenSaver.es';
$TAGLINE   = 'Free screensavers · 4K & 10-hour videos';
$BASE_URL  = './';         // <-- set to your real domain (with trailing slash)
$CANONICAL = $BASE_URL;                          // for home; videos page will override canonical
$OG_IMAGE  = $BASE_URL . 'og.png';               // 1200x630 recommended
$FAVICON   = $BASE_URL . 'favicon.png';

$page = (string)($_GET['page'] ?? 'home');
$page = ($page === 'videos') ? 'videos' : 'home';

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

/* =========================
   Load JSON
========================= */
$data = null;
if (is_file($jsonFile)) {
  $raw = file_get_contents($jsonFile);
  if ($raw !== false) {
    $tmp = json_decode($raw, true);
    if (is_array($tmp)) $data = $tmp;
  }
}
$playlists = is_array($data['playlists'] ?? null) ? $data['playlists'] : [];

/* =========================
   Derived counts + flatten videos
========================= */
$playlistCount = count($playlists);
$videoCount = 0;
$playlistTitles = [];
$allVideos = []; // flattened: each item has playlist_title, playlist_id, etc.

foreach ($playlists as $pl) {
  $plTitle = (string)($pl['title'] ?? '');
  $plTitlesOk = trim($plTitle) !== '';
  if ($plTitlesOk) $playlistTitles[] = $plTitle;

  $plId    = slug_id($plTitle ?: 'playlist');
  $plDesc  = (string)($pl['description'] ?? '');
  $plUrl   = (string)($pl['url'] ?? '#');
  $plThumb = safe_rel_path((string)($pl['thumbnail_file'] ?? ''));
  $plThumbExists = $plThumb && is_file(__DIR__ . '/' . $plThumb);
  $plThumbSrc = $plThumbExists ? $plThumb : '';

  $videos = is_array($pl['videos'] ?? null) ? $pl['videos'] : [];
  $videoCount += count($videos);

  foreach ($videos as $v) {
    $vttl = (string)($v['title'] ?? 'Untitled');
    $vurl = (string)($v['url'] ?? '#');
    $vdesc = (string)($v['description'] ?? ($v['descripcion'] ?? ''));

    $thumb = safe_rel_path((string)($v['thumbnail_file'] ?? ''));
    $thumbExists = $thumb && is_file(__DIR__ . '/' . $thumb);
    $thumbSrc = $thumbExists ? $thumb : '';

    $allVideos[] = [
      'title' => $vttl,
      'url' => $vurl,
      'description' => $vdesc,
      'thumbnail' => $thumbSrc,
      'playlist_title' => $plTitle ?: 'Playlist',
      'playlist_id' => $plId,
      'playlist_url' => $plUrl,
      'playlist_thumb' => $plThumbSrc,
      'playlist_desc' => $plDesc,
    ];
  }
}

$KEYWORDS = 'free screensavers, screensaver, screensavers 4k, 10 hour screensaver, ambient screensaver, screensaver videos, relaxing screensaver, space screensaver, fluid screensaver';

$DESCRIPTION_HOME = "Free screensavers in 4K and 10-hour videos. Browse {$playlistCount} playlists and {$videoCount} videos: ambient loops, space, fluids, relax visuals.";
$DESCRIPTION_VIDEOS = "All free screensaver videos in one place: {$videoCount} videos searchable by title. 4K, long loops, ambient visuals.";

// canonical varies by page
$canonical = ($page === 'videos') ? ($BASE_URL . '?page=videos') : $CANONICAL;
$metaDesc  = ($page === 'videos') ? $DESCRIPTION_VIDEOS : $DESCRIPTION_HOME;
$title     = ($page === 'videos')
  ? ($SITE_NAME . ' · All Videos · ' . $TAGLINE)
  : ($SITE_NAME . ' · ' . $TAGLINE);

/* =========================
   JSON-LD: WebSite + CollectionPage
========================= */
$ldPlaylists = [];
foreach ($playlists as $pl) {
  $plTitle = (string)($pl['title'] ?? 'Playlist');
  $plUrl   = (string)($pl['url'] ?? '');
  $plDesc  = (string)($pl['description'] ?? '');
  $plId    = slug_id($plTitle);

  $thumb = safe_rel_path((string)($pl['thumbnail_file'] ?? ''));
  $thumbExists = $thumb && is_file(__DIR__ . '/' . $thumb);
  $thumbAbs = $thumbExists ? rtrim($BASE_URL, '/') . '/' . ltrim($thumb, '/') : $OG_IMAGE;

  $ldPlaylists[] = [
    '@type' => 'CreativeWorkSeries',
    'name' => $plTitle,
    'url'  => $plUrl ?: ($BASE_URL . '#' . $plId),
    'description' => $plDesc ?: null,
    'image' => $thumbAbs,
  ];
}

$schema = [
  '@context' => 'https://schema.org',
  '@graph' => [
    [
      '@type' => 'WebSite',
      'name' => $SITE_NAME,
      'url' => $BASE_URL,
      'description' => $DESCRIPTION_HOME,
      'inLanguage' => 'en',
    ],
    [
      '@type' => 'CollectionPage',
      'name' => $title,
      'url' => $canonical,
      'description' => $metaDesc,
      'inLanguage' => 'en',
      'hasPart' => $ldPlaylists,
    ]
  ]
];
?>
<!doctype html>
<html lang="en">
  <head>
    <title><?= h($title) ?></title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1" />

    <!-- SEO -->
    <meta name="description" content="<?= h($metaDesc) ?>">
    <meta name="keywords" content="<?= h($KEYWORDS) ?>">
    <meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1,max-video-preview:-1">
    <meta name="theme-color" content="#000000">
    <link rel="canonical" href="<?= h($canonical) ?>">
    <link rel="icon" href="<?= h($FAVICON) ?>">

    <!-- Open Graph -->
    <meta property="og:type" content="website">
    <meta property="og:site_name" content="<?= h($SITE_NAME) ?>">
    <meta property="og:title" content="<?= h($title) ?>">
    <meta property="og:description" content="<?= h($metaDesc) ?>">
    <meta property="og:url" content="<?= h($canonical) ?>">
    <meta property="og:image" content="<?= h($OG_IMAGE) ?>">
    <meta property="og:image:width" content="1200">
    <meta property="og:image:height" content="630">

    <!-- Twitter -->
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:title" content="<?= h($title) ?>">
    <meta name="twitter:description" content="<?= h($metaDesc) ?>">
    <meta name="twitter:image" content="<?= h($OG_IMAGE) ?>">

    <script type="application/ld+json"><?= json_encode($schema, JSON_UNESCAPED_SLASHES|JSON_UNESCAPED_UNICODE) ?></script>

    <link rel="preconnect" href="https://www.youtube.com">
    <link rel="preconnect" href="https://i.ytimg.com">

    <style>
      *{margin:0;padding:0;}
      /* Mejora: scroll suave nativo para mejor UX */
      html{
        scroll-behavior:smooth;
      }
      html,body{
        width:100%;
        height:100%;
        background:black;
        color:white;
        font-family:ubuntu,system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;
        overflow-x:hidden;
      }
      /* Mejora: estilos de foco accesible para navegacion con teclado */
      :focus-visible{
        outline:2px solid rgba(120,160,255,.7);
        outline-offset:2px;
      }

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
        overflow:auto;
      }
      .sacado{ left:0px; }
      nav .navTitle{font-weight:900;font-size:16px;margin-bottom:8px;}
      nav .navMeta{opacity:.85;font-size:12px;margin-bottom:12px;}
      .navList{list-style:none;display:flex;flex-direction:column;gap:8px;}
      .navItem a{
        display:block;
        padding:10px 10px;
        border-radius:10px;
        color:white;
        text-decoration:none;
        background:rgba(255,255,255,.08);
        border:1px solid rgba(255,255,255,.12);
        font-weight:800;
        font-size:13px;
        line-height:1.2;
      }
      .navItem a:hover{background:rgba(255,255,255,.14);border-color:rgba(255,255,255,.18);}
      .navItem small{display:block;margin-top:6px;opacity:.80;font-weight:600;}

      header,main,footer{padding:20px;}
      header{
        display:flex;
        align-items:center;
        justify-content: space-between;
        position:fixed;
        top:0;
        width:100%;
        background:black;
        box-sizing:border-box;
        z-index:900;
        border-bottom:1px solid rgba(255,255,255,0.06);
        gap:14px;
      }
      main{padding-top:92px;}

      h1{font-size:20px;}
      .tagline{font-size:12px;opacity:.9;}

      .topActions{
        display:flex;
        align-items:center;
        gap:10px;
        flex-wrap:wrap;
        justify-content:flex-end;
      }
      .btnTop{
        display:inline-flex;
        align-items:center;
        justify-content:center;
        padding:9px 10px;
        border-radius:10px;
        border:1px solid rgba(255,255,255,.16);
        background:rgba(255,255,255,.06);
        color:white;
        text-decoration:none;
        cursor:pointer;
        font-weight:900;
        font-size:13px;
        user-select:none;
        white-space:nowrap;
      }
      .btnTop:hover{background:rgba(255,255,255,.12);}
      .btnTopPrimary{
        border-color: rgba(120,160,255,.40);
        background: rgba(120,160,255,.16);
      }
      .btnTopPrimary:hover{ background: rgba(120,160,255,.24); }

      /* HERO */
      .hero{
        position:relative;
        width:100%;
        min-height:380px;
        border-bottom:1px solid rgba(255,255,255,0.08);
        overflow:hidden;
        margin-bottom:18px;
      }
      .heroSlides{ position:relative; width:100%; height:380px; }
      .heroSlide{
        position:absolute; inset:0;
        opacity:0;
        transform:scale(1.02);
        transition:opacity .6s ease, transform .8s ease;
        background:#0b0b0b;
        background-size:cover;
        background-position:center;
      }
      .heroSlide.activo{ opacity:1; transform:scale(1.0); }
      .heroShade{
        position:absolute; inset:0;
        background:
          linear-gradient(90deg, rgba(0,0,0,.78) 0%, rgba(0,0,0,.40) 55%, rgba(0,0,0,.20) 100%),
          radial-gradient(60% 70% at 20% 30%, rgba(0,0,0,.55), rgba(0,0,0,0));
        pointer-events:none;
      }
      .heroInner{
        position:relative;
        height:380px;
        display:flex;
        align-items:flex-end;
        box-sizing:border-box;
        padding:22px 20px;
      }
      .heroText{ max-width:980px; }
      .heroKicker{
        font-size:12px;
        opacity:.80;
        margin-bottom:8px;
        letter-spacing:.08em;
        text-transform:uppercase;
      }
      .heroTitle{
        font-size:34px;
        line-height:1.08;
        font-weight:900;
        margin-bottom:10px;
        text-shadow:0 4px 20px rgba(0,0,0,.5);
      }
      .heroDesc{
        font-size:14px;
        line-height:1.5;
        opacity:.92;
        max-width:920px;
        max-height:110px;
        overflow:auto;
        padding-right:8px;
      }
      .heroDesc::-webkit-scrollbar{ width:8px; }
      .heroDesc::-webkit-scrollbar-thumb{ background:rgba(255,255,255,.12); border-radius:8px; }
      .heroActions{ margin-top:14px; display:flex; gap:10px; flex-wrap:wrap; }
      .btn{
        display:inline-flex;align-items:center;justify-content:center;
        padding:10px 12px;border-radius:10px;
        border:1px solid rgba(255,255,255,.16);
        background:rgba(255,255,255,.06);
        color:white;text-decoration:none;cursor:pointer;
        font-weight:900;font-size:13px;user-select:none;
      }
      .btn:hover{ background:rgba(255,255,255,.12); }
      .btnPrimary{
        border-color: rgba(120,160,255,.40);
        background: rgba(120,160,255,.16);
      }
      .btnPrimary:hover{ background: rgba(120,160,255,.24); }
      .heroDots{
        position:absolute;left:20px;right:20px;bottom:16px;
        display:flex;gap:8px;align-items:center;justify-content:flex-end;z-index:3;
      }
      .dot{
        width:10px;height:10px;border-radius:999px;
        border:1px solid rgba(255,255,255,.35);
        background:rgba(255,255,255,.08);
        cursor:pointer;opacity:.9;
      }
      .dot.activo{ background:rgba(255,255,255,.85);border-color:rgba(255,255,255,.85); }
      .heroArrows{ position:absolute; inset:0; pointer-events:none; z-index:3; }
      .heroPrev,.heroNext{
        pointer-events:auto;position:absolute;top:50%;transform:translateY(-50%);
        width:44px;height:44px;border-radius:999px;
        border:1px solid rgba(255,255,255,.18);
        background:rgba(0,0,0,.35);color:white;font-size:22px;line-height:42px;text-align:center;
        cursor:pointer;user-select:none;opacity:.35;transition:opacity .2s ease, background .2s ease;
      }
      .heroPrev:hover,.heroNext:hover{ opacity:.95; background:rgba(0,0,0,.55); }
      .heroPrev{ left:14px; }
      .heroNext{ right:14px; }

      /* SEO block (home) */
      .seoBlock{
        padding:14px 0 2px 0;
        opacity:.92;font-size:13px;line-height:1.55;max-width:1100px;
      }
      .seoBlock a{ color:white; text-decoration:underline; }

      /* Rows (home) */
      section.row{width:100%;position:relative;margin-bottom:22px; scroll-margin-top:110px;}
      section.row h2{margin:0 0 10px 0;font-weight:900;font-size:18px;}
      section.row .contenedor{
        display:flex;gap:20px;width:20000px;position:relative;
        transition:all 350ms ease;left:10px;
      }
      section.row article{
        width:300px;height:170px;background:#1a1a1a;padding:10px;box-sizing:border-box;border-radius:5px;
        display:flex;gap:10px;align-items:flex-end;cursor:pointer;
        border:1px solid rgba(255,255,255,0.08);position:relative;overflow:hidden;
      }
      /* Mejora: transicion suave en hover de las tarjetas */
      section.row article{ transition: border-color .25s ease, transform .25s ease; }
      section.row article:hover{ border-color: rgba(255,255,255,0.20); transform: scale(1.03); }
      .meta{
        display:flex;flex-direction:column;gap:6px;min-width:0;
        text-shadow:0 0 2px black,0 0 3px black,0 0 4px black;
      }
      .vtitle{
        font-size:14px;line-height:1.2;font-weight:900;
        white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:240px;
      }
      .vlink{
        font-size:12px;opacity:.75;
        white-space:nowrap;overflow:hidden;text-overflow:ellipsis;max-width:240px;
      }
      .izquierda,.derecha{
        position:absolute;top:50%;transform:translateY(-50%);
        background:black;color:white;width:40px;height:40px;font-size:20px;line-height:40px;text-align:center;
        border-radius:40px;transition:opacity 250ms ease;opacity:0.12;font-weight:bold;user-select:none;cursor:pointer;
      }
      .izquierda{left:0px;}
      .derecha{right:0px;}
      .izquierda:hover,.derecha:hover{opacity:0.95;}

      .empty{ padding:10px; opacity:.75; }

      /* =========================
         VIDEOS PAGE (grid + search)
      ========================= */
      .videosWrap{
        max-width:100%;
      }
      .searchBar{
        display:flex;
        gap:10px;
        align-items:center;
        margin:10px 0 14px 0;
        flex-wrap:wrap;
      }
      .searchInput{
        flex:1 1 320px;
        background:rgba(255,255,255,.06);
        border:1px solid rgba(255,255,255,.16);
        border-radius:12px;
        padding:12px 12px;
        color:white;
        font-weight:800;
        outline:none;
      }
      .searchInput::placeholder{ color:rgba(255,255,255,.55); font-weight:700; }
      .searchMeta{
        font-size:12px;
        opacity:.85;
        white-space:nowrap;
      }

      .grid{
        display:grid;
        grid-template-columns: repeat(5, minmax(0, 1fr));
        gap:12px;
      }
      @media (max-width: 1400px){ .grid{ grid-template-columns: repeat(4, minmax(0,1fr)); } }
      @media (max-width: 1100px){ .grid{ grid-template-columns: repeat(3, minmax(0,1fr)); } }
      @media (max-width: 820px){ .grid{ grid-template-columns: repeat(2, minmax(0,1fr)); } }
      @media (max-width: 520px){ .grid{ grid-template-columns: repeat(1, minmax(0,1fr)); } }

      .gridItem{
        position:relative;
        border-radius:12px;
        overflow:hidden;
        background:#111;
        border:1px solid rgba(255,255,255,0.10);
        cursor:pointer;
        min-height:170px;
      }
      /* Mejora: transicion suave en tarjetas del grid */
      .gridItem{ transition: border-color .25s ease, transform .25s ease, box-shadow .25s ease; }
      .gridItem:hover{ border-color: rgba(255,255,255,0.22); transform: translateY(-3px); box-shadow: 0 8px 24px rgba(0,0,0,.4); }
      .gridThumb{
        position:absolute; inset:0;
        background:#111;
        background-size:cover;
        background-position:center;
        filter:saturate(1.05);
        transform:scale(1.02);
      }
      .gridShade{
        position:absolute; inset:0;
        background:linear-gradient(0deg, rgba(0,0,0,.86) 0%, rgba(0,0,0,.20) 70%, rgba(0,0,0,.10) 100%);
      }
      .gridMeta{
        position:absolute;
        left:10px; right:10px; bottom:10px;
        display:flex;
        flex-direction:column;
        gap:6px;
        text-shadow:0 0 3px rgba(0,0,0,.8);
      }
      .gridTitle{
        font-weight:900;
        font-size:13px;
        line-height:1.2;
        display:-webkit-box;
        -webkit-line-clamp:2;
        -webkit-box-orient:vertical;
        overflow:hidden;
      }
      .gridSub{
        font-size:12px;
        opacity:.85;
        white-space:nowrap;
        overflow:hidden;
        text-overflow:ellipsis;
      }

      /* MODAL */
      .modalOverlay{
        position:fixed; inset:0;
        background:rgba(0,0,0,.72);
        display:none;
        align-items:center;
        justify-content:center;
        z-index:2000;
        padding:20px;
        box-sizing:border-box;
      }
      .modalOverlay.abierto{ display:flex; }
      .modalCard{
        width:min(920px, 96vw);
        background:#0f0f0f;
        border:1px solid rgba(255,255,255,.12);
        border-radius:10px;
        overflow:hidden;
        box-shadow:0 20px 60px rgba(0,0,0,.6);
        display:flex;
      }
      .modalMedia{
        width:min(520px, 55vw);
        background:#111;
        position:relative;
        flex:0 0 auto;
      }
      .modalMedia img{
        width:100%;
        height:100%;
        max-height:420px;
        object-fit:cover;
        display:block;
        background:#222;
      }
      .modalBody{
        padding:16px 16px 14px 16px;
        box-sizing:border-box;
        display:flex;
        flex-direction:column;
        gap:10px;
        flex:1 1 auto;
        min-width:0;
      }
      .modalTop{display:flex;align-items:flex-start;justify-content:space-between;gap:12px;}
      .modalTitle{font-size:18px;font-weight:900;line-height:1.2;max-width:100%;overflow:hidden;text-overflow:ellipsis;}
      .modalClose{
        flex:0 0 auto;
        width:34px;height:34px;border-radius:999px;
        border:1px solid rgba(255,255,255,.16);
        background:rgba(255,255,255,.06);
        color:white;cursor:pointer;font-size:18px;line-height:32px;text-align:center;user-select:none;
      }
      .modalClose:hover{ background:rgba(255,255,255,.12); }
      .modalMetaLine{font-size:12px;opacity:.75;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;}
      .modalDesc{font-size:13px;line-height:1.45;opacity:.90;max-height:180px;overflow:auto;padding-right:6px;}
      .modalDesc::-webkit-scrollbar{ width:8px; }
      .modalDesc::-webkit-scrollbar-thumb{ background:rgba(255,255,255,.12); border-radius:8px; }
      .modalActions{display:flex;gap:10px;margin-top:auto;padding-top:6px;}
      @media (max-width: 780px){
        .modalCard{ flex-direction:column; }
        .modalMedia{ width:100%; }
        .modalMedia img{ max-height:260px; }
      }
    </style>
  </head>
  <body>
    <nav aria-label="Playlists navigation">
      <div class="navTitle">Playlists</div>
      <div class="navMeta">
        <?= (int)$playlistCount ?> playlists · <?= (int)$videoCount ?> videos
      </div>

      <?php if (!$playlists): ?>
        <div class="navMeta">No playlists found.</div>
      <?php else: ?>
        <ul class="navList">
          <?php foreach ($playlists as $pl): ?>
            <?php
              $plTitle = (string)($pl['title'] ?? 'Playlist');
              $plDesc  = (string)($pl['description'] ?? '');
              $plId    = slug_id($plTitle);
              $videos  = is_array($pl['videos'] ?? null) ? $pl['videos'] : [];
            ?>
            <li class="navItem">
              <a href="#<?= h($plId) ?>" data-scroll="#<?= h($plId) ?>">
                <?= h($plTitle) ?>
                <small><?= (int)count($videos) ?> videos<?= $plDesc ? ' · ' . h(mb_strimwidth(trim($plDesc), 0, 60, '…', 'UTF-8')) : '' ?></small>
              </a>
            </li>
          <?php endforeach; ?>
        </ul>
      <?php endif; ?>
    </nav>

    <header>
      <div>
        <h1><?= h($SITE_NAME) ?></h1>
        <div class="tagline"><?= h($TAGLINE) ?></div>
      </div>

      <div class="topActions">
        <!-- page switch buttons -->
        <a class="btnTop <?= $page === 'home' ? 'btnTopPrimary' : '' ?>" href="<?= h($BASE_URL) ?>?page=home">Frontpage</a>
        <a class="btnTop <?= $page === 'videos' ? 'btnTopPrimary' : '' ?>" href="<?= h($BASE_URL) ?>?page=videos">All videos</a>

        <!-- hamburger -->
        <div id="hamburguesa" class="btnTop" style="font-size:18px;padding:9px 12px;" aria-label="Open navigation" role="button" tabindex="0">☰</div>
      </div>
    </header>

    <main>
      <?php if (!$playlists): ?>
        <div class="empty">
          Could not read <b><?= h(basename($jsonFile)) ?></b> or it contains no playlists.<br>
          Ensure the JSON exists at: <code><?= h($jsonFile) ?></code>
        </div>
      <?php else: ?>

        <?php if ($page === 'home'): ?>
          <!-- =========================
               HOME VIEW
          ========================== -->

          <section class="hero" id="hero" aria-label="Featured playlists slider">
            <div class="heroSlides" id="heroSlides">
              <?php foreach ($playlists as $idx => $pl): ?>
                <?php
                  $plTitle = (string)($pl['title'] ?? 'Playlist');
                  $plDesc  = (string)($pl['description'] ?? '');
                  $plUrl   = (string)($pl['url'] ?? '#');
                  $plId    = slug_id($plTitle);

                  $plThumb = safe_rel_path((string)($pl['thumbnail_file'] ?? ''));
                  $plThumbExists = $plThumb && is_file(__DIR__ . '/' . $plThumb);
                  $plThumbSrc = $plThumbExists ? $plThumb : '';

                  $bg = $plThumbSrc ? "background-image:url(" . h($plThumbSrc) . ");" : "";
                  $activeClass = ($idx === 0) ? "activo" : "";
                ?>
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
                      <div class="heroDesc"><?= h(trim($plDesc) ?: "Browse free screensaver videos. 4K loops, long ambient visuals, and relaxing motion graphics.") ?></div>
                      <div class="heroActions">
                        <a class="btn btnPrimary" href="<?= h($plUrl) ?>" target="_blank" rel="noopener">Open playlist on YouTube</a>
                        <div class="btn" data-scroll-to="#<?= h($plId) ?>">See videos below</div>
                      </div>
                    </div>
                  </div>
                </div>
              <?php endforeach; ?>
            </div>

            <div class="heroArrows" aria-hidden="true">
              <div class="heroPrev" id="heroPrev">‹</div>
              <div class="heroNext" id="heroNext">›</div>
            </div>

            <div class="heroDots" id="heroDots" aria-label="Slider pagination">
              <?php foreach ($playlists as $idx => $_): ?>
                <div class="dot <?= ($idx===0?'activo':'') ?>" data-dot="<?= (int)$idx ?>"></div>
              <?php endforeach; ?>
            </div>
          </section>

          <section class="seoBlock" aria-label="About free screensavers">
            <h2 style="font-size:18px;font-weight:900;margin-bottom:8px;">Free screensavers for any screen</h2>
            <p>
              <?= h($SITE_NAME) ?> is a free library of long videos designed to work as <strong>screensavers</strong> on TVs, desktops, tablets, and digital signage.
              Explore playlists like
              <?php
                $sample = array_slice($playlistTitles, 0, 6);
                $links = [];
                foreach ($sample as $t) {
                  $links[] = '<a href="#' . h(slug_id($t)) . '">' . h($t) . '</a>';
                }
                echo implode(', ', $links);
              ?>,
              and use any video as a <strong>4K screensaver</strong> or a <strong>10-hour ambient loop</strong>.
            </p>
          </section>

          <?php foreach ($playlists as $pl): ?>
            <?php
              $plTitle = (string)($pl['title'] ?? 'Playlist');
              $plDesc  = (string)($pl['description'] ?? '');
              $plUrl   = (string)($pl['url'] ?? '#');
              $plId    = slug_id($plTitle);
              $videos  = is_array($pl['videos'] ?? null) ? $pl['videos'] : [];
            ?>
            <section class="row" id="<?= h($plId) ?>" data-pl-title="<?= h($plTitle) ?>" aria-label="Playlist <?= h($plTitle) ?>">
              <h2><?= h($plTitle) ?></h2>

              <?php if (trim($plDesc) !== ''): ?>
                <p style="opacity:.85;font-size:13px;line-height:1.5;margin:-4px 0 10px 0;max-width:1100px;">
                  <?= h($plDesc) ?>
                  <?php if ($plUrl && $plUrl !== '#'): ?>
                    <span style="opacity:.85;">· <a href="<?= h($plUrl) ?>" target="_blank" rel="noopener" style="color:white;text-decoration:underline;">YouTube playlist</a></span>
                  <?php endif; ?>
                </p>
              <?php endif; ?>

              <div class="contenedor" style="left:0px;">
                <?php if (!$videos): ?>
                  <article style="width:300px;height:120px;align-items:center;">
                    <div class="meta">
                      <div class="vtitle">No videos</div>
                      <div class="vlink">—</div>
                    </div>
                  </article>
                <?php endif; ?>

                <?php foreach ($videos as $v): ?>
                  <?php
                    $vttl  = (string)($v['title'] ?? 'Untitled');
                    $vurl  = (string)($v['url'] ?? '#');
                    $desc  = (string)($v['description'] ?? ($v['descripcion'] ?? ''));

                    $thumb = safe_rel_path((string)($v['thumbnail_file'] ?? ''));
                    $thumbExists = $thumb && is_file(__DIR__ . '/' . $thumb);
                    $thumbSrc = $thumbExists ? $thumb : '';
                  ?>
                  <article
                    data-url="<?= h($vurl) ?>"
                    data-title="<?= h($vttl) ?>"
                    data-desc="<?= h($desc) ?>"
                    data-thumb="<?= h($thumbSrc) ?>"
                    style="<?= $thumbSrc ? 'background:url('.h($thumbSrc).');background-size:cover;background-position:center;' : '' ?>"
                    role="button"
                    aria-label="Open video details: <?= h($vttl) ?>"
                  >
                    <div class="meta">
                      <div class="vtitle" title="<?= h($vttl) ?>"><?= h($vttl) ?></div>
                      <div class="vlink" title="<?= h($vurl) ?>"><?= h($vurl) ?></div>
                    </div>
                  </article>
                <?php endforeach; ?>
              </div>

              <div class="izquierda" aria-label="Scroll left">🡠</div>
              <div class="derecha" aria-label="Scroll right">🡢</div>
            </section>
          <?php endforeach; ?>

        <?php else: ?>
          <!-- =========================
               VIDEOS VIEW
          ========================== -->
          <div class="videosWrap" aria-label="All videos">
            <h2 style="font-size:22px;font-weight:900;margin-bottom:10px;">All videos</h2>

            <div class="searchBar">
              <input id="q" class="searchInput" type="search" placeholder="Search videos (title / url / playlist)…" autocomplete="off">
              <div class="searchMeta">
                <span id="countVisible"><?= (int)count($allVideos) ?></span> / <?= (int)count($allVideos) ?> shown
              </div>
            </div>

            <div class="grid" id="grid">
              <?php foreach ($allVideos as $i => $v): ?>
                <?php
                  $vttl = (string)$v['title'];
                  $vurl = (string)$v['url'];
                  $vdesc = (string)$v['description'];
                  $thumb = (string)$v['thumbnail'];
                  $plt = (string)$v['playlist_title'];
                ?>
                <article
                  class="gridItem"
                  data-url="<?= h($vurl) ?>"
                  data-title="<?= h($vttl) ?>"
                  data-desc="<?= h($vdesc) ?>"
                  data-thumb="<?= h($thumb) ?>"
                  data-search="<?= h(mb_strtolower($vttl.' '.$vurl.' '.$plt, 'UTF-8')) ?>"
                  role="button"
                  aria-label="Open video details: <?= h($vttl) ?>"
                >
                  <div class="gridThumb" style="<?= $thumb ? 'background-image:url('.h($thumb).');' : '' ?>"></div>
                  <div class="gridShade"></div>
                  <div class="gridMeta">
                    <div class="gridTitle"><?= h($vttl) ?></div>
                    <div class="gridSub"><?= h($plt) ?></div>
                  </div>
                </article>
              <?php endforeach; ?>
            </div>
          </div>
        <?php endif; ?>

      <?php endif; ?>
    </main>

    <!-- Mejora: boton para volver arriba, util en paginas largas -->
    <div id="backToTop" style="position:fixed;bottom:24px;right:24px;width:44px;height:44px;border-radius:50%;background:rgba(120,160,255,.25);border:1px solid rgba(120,160,255,.4);color:white;font-size:20px;line-height:44px;text-align:center;cursor:pointer;opacity:0;transition:opacity .3s ease;z-index:999;user-select:none;" title="Volver arriba" aria-label="Volver arriba">↑</div>

    <footer style="padding:20px;border-top:1px solid rgba(255,255,255,.08);opacity:.85;font-size:12px;">
      <div>
        <?= h($SITE_NAME) ?> · Free screensavers · Updated:
        <?= isset($data['generated_at_epoch']) ? h(date('Y-m-d', (int)$data['generated_at_epoch'])) : h(date('Y-m-d')) ?>
      </div>
      <!-- Mejora: mostrar estadisticas del catalogo en el pie de pagina -->
      <div style="margin-top:6px;opacity:.7;">
        <?= (int)$playlistCount ?> playlists · <?= (int)$videoCount ?> videos · Screensaver catalog
      </div>
    </footer>

    <!-- MODAL -->
    <div class="modalOverlay" id="modalOverlay" aria-hidden="true">
      <div class="modalCard" role="dialog" aria-modal="true" aria-label="Video details" id="modalCard">
        <div class="modalMedia">
          <img id="modalThumb" alt="Video thumbnail" src="" loading="lazy" decoding="async">
        </div>
        <div class="modalBody">
          <div class="modalTop">
            <div style="min-width:0;">
              <div class="modalTitle" id="modalTitle"></div>
              <div class="modalMetaLine" id="modalUrl"></div>
            </div>
            <div class="modalClose" id="modalClose" title="Close" aria-label="Close">✕</div>
          </div>

          <div class="modalDesc" id="modalDesc"></div>

          <div class="modalActions">
            <a class="btn btnPrimary" id="modalGo" href="#" target="_blank" rel="noopener">Watch on YouTube</a>
            <div class="btn" id="modalCancel">Close</div>
          </div>
        </div>
      </div>
    </div>

    <noscript>
      <div style="padding:20px; background:#111; border-top:1px solid rgba(255,255,255,.12);">
        This site works best with JavaScript enabled (slider + modal + search).
      </div>
    </noscript>

    <script>
      // HAMBURGUESA
      var abierto = false;
      let hamburguesa = document.querySelector("#hamburguesa")
      let navegacion = document.querySelector("nav");

      function toggleMenu(){
        if(abierto){
           hamburguesa.textContent = "☰"
           navegacion.classList.remove("sacado");
           abierto = false;
        }else{
          hamburguesa.textContent = "🗙"
          navegacion.classList.add("sacado");
          abierto = true;
        }
      }
      hamburguesa.onclick = toggleMenu;
      hamburguesa.addEventListener("keydown", function(e){
        if(e.key === "Enter" || e.key === " ") { e.preventDefault(); toggleMenu(); }
      });

      // NAV scroll-to (only meaningful on home, but harmless elsewhere)
      document.querySelectorAll('nav a[data-scroll]').forEach(function(a){
        a.addEventListener("click", function(e){
          const targetSel = this.getAttribute("data-scroll");
          if(!targetSel) return;
          // if we're on videos page, let the link work normally (it won't find the target)
          if (window.location.search.includes("page=videos")) return;

          e.preventDefault();
          const sec = document.querySelector(targetSel);
          if(sec){
            sec.scrollIntoView({behavior:"smooth", block:"start"});
            if(abierto) toggleMenu();
          }
        });
      });

      // SCROLLERS IZQ/DER (home rows)
      document.querySelectorAll(".izquierda").forEach(function(izquierda){
        izquierda.onclick = function(){
          let tira = this.parentElement.querySelector(':scope > .contenedor');
          if(!tira) return;
          let actual = parseFloat(tira.style.left || "0")
          tira.style.left = (actual+320)+"px"
        }
      })
      document.querySelectorAll(".derecha").forEach(function(derecha){
        derecha.onclick = function(){
          let tira = this.parentElement.querySelector(':scope > .contenedor');
          if(!tira) return;
          let actual = parseFloat(tira.style.left || "0")
          tira.style.left = (actual-320)+"px"
        }
      })

      // MODAL (shared)
      const overlay   = document.getElementById("modalOverlay");
      const card      = document.getElementById("modalCard");
      const mThumb    = document.getElementById("modalThumb");
      const mTitle    = document.getElementById("modalTitle");
      const mDesc     = document.getElementById("modalDesc");
      const mUrl      = document.getElementById("modalUrl");
      const mGo       = document.getElementById("modalGo");
      const mClose    = document.getElementById("modalClose");
      const mCancel   = document.getElementById("modalCancel");

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
        overlay.setAttribute("aria-hidden", "false");
        mClose.focus?.();
      }

      function closeModal(){
        overlay.classList.remove("abierto");
        overlay.setAttribute("aria-hidden", "true");
        mGo.href = "#";
      }

      // click handler for ANY element with data-url + data-title (rows + grid)
      document.querySelectorAll("[data-url][data-title]").forEach(function(el){
        el.addEventListener("click", function(){
          const url   = this.getAttribute("data-url")   || "";
          const title = this.getAttribute("data-title") || "";
          const desc  = this.getAttribute("data-desc")  || "";
          const thumb = this.getAttribute("data-thumb") || "";
          if(!url || url === "#") return;
          openModal({title, desc, url, thumb});
        });
      });

      mClose.addEventListener("click", closeModal);
      mCancel.addEventListener("click", closeModal);
      overlay.addEventListener("click", function(e){
        if (e.target === overlay) closeModal();
      });
      card.addEventListener("click", function(e){ e.stopPropagation(); });
      document.addEventListener("keydown", function(e){
        if(e.key === "Escape" && overlay.classList.contains("abierto")) closeModal();
      });

      // HERO SLIDER (only if exists)
      const hero = document.getElementById("hero");
      const slidesWrap = document.getElementById("heroSlides");
      const slides = slidesWrap ? Array.from(slidesWrap.querySelectorAll(".heroSlide")) : [];
      const dotsWrap = document.getElementById("heroDots");
      const dots = dotsWrap ? Array.from(dotsWrap.querySelectorAll(".dot")) : [];
      const prevBtn = document.getElementById("heroPrev");
      const nextBtn = document.getElementById("heroNext");

      let heroIndex = 0;
      let heroTimer = null;
      let heroPaused = false;

      function setHero(i){
        if(!slides.length) return;
        heroIndex = (i + slides.length) % slides.length;
        slides.forEach((s, idx) => s.classList.toggle("activo", idx === heroIndex));
        dots.forEach((d, idx) => d.classList.toggle("activo", idx === heroIndex));
      }
      function nextHero(){ setHero(heroIndex + 1); }
      function prevHero(){ setHero(heroIndex - 1); }
      function startHero(){
        if(!slides.length) return;
        stopHero();
        heroTimer = setInterval(function(){
          if(!heroPaused) nextHero();
        }, 5000);
      }
      function stopHero(){
        if(heroTimer) clearInterval(heroTimer);
        heroTimer = null;
      }

      if (prevBtn) prevBtn.addEventListener("click", function(){ prevHero(); startHero(); });
      if (nextBtn) nextBtn.addEventListener("click", function(){ nextHero(); startHero(); });

      dots.forEach(function(d){
        d.addEventListener("click", function(){
          const i = parseInt(this.getAttribute("data-dot") || "0", 10);
          setHero(i);
          startHero();
        });
      });

      // "See videos below" button (home)
      document.querySelectorAll("[data-scroll-to]").forEach(function(b){
        b.addEventListener("click", function(e){
          const target = this.getAttribute("data-scroll-to") || "";
          const sec = document.querySelector(target);
          if(sec) sec.scrollIntoView({behavior:"smooth", block:"start"});
        });
      });

      if (hero){
        hero.addEventListener("mouseenter", () => heroPaused = true);
        hero.addEventListener("mouseleave", () => heroPaused = false);
      }
      setHero(0);
      startHero();

      // VIDEOS SEARCH (only if q exists)
      const q = document.getElementById("q");
      const grid = document.getElementById("grid");
      const countVisible = document.getElementById("countVisible");

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

      if(q){
        q.addEventListener("input", applyFilter);
        applyFilter();
      }

      // Mejora: boton "volver arriba" que aparece al hacer scroll
      var backToTop = document.getElementById("backToTop");
      if(backToTop){
        window.addEventListener("scroll", function(){
          backToTop.style.opacity = (window.scrollY > 400) ? "1" : "0";
        });
        backToTop.addEventListener("click", function(){
          window.scrollTo({top:0, behavior:"smooth"});
        });
      }
    </script>
  </body>
</html>

