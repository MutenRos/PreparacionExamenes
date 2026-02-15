<?php
// pagina.php — Cargador genérico de páginas informativas desde XML
// Uso: pagina.php?file=db/paginas/sobrenosotros.xml

error_reporting(E_ALL);
ini_set('display_errors', 1);

function h($s){ return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }

function safe_path($rel){
  $rel = (string)$rel;
  if (!preg_match('/^[a-zA-Z0-9_\-\/\.]+$/', $rel) || str_contains($rel, '..')) return "";
  return __DIR__ . '/' . ltrim($rel, '/');
}

function safe_img_src($src): string {
  $src = trim((string)$src);
  if ($src === "") return "";
  if (str_contains($src, '..')) return "";
  if (preg_match('#^https?://#i', $src)) return $src;
  if (!preg_match('/^[a-zA-Z0-9_\-\/\.\%\=\?\&]+$/', $src)) return "";
  return $src;
}

// ===============================
// 1) Cargar XML
// ===============================
$defaultRel = "paginas/".$_GET['p'].".xml";
$relFile = $_GET['file'] ?? $defaultRel;
$xmlPath = safe_path($relFile);
if ($xmlPath === "" || !file_exists($xmlPath)) {
  http_response_code(404);
  die("XML no encontrado: ".h($relFile));
}

libxml_use_internal_errors(true);
$xml = simplexml_load_file($xmlPath);
if (!$xml) {
  http_response_code(500);
  $errs = libxml_get_errors();
  echo "Error leyendo XML<br>";
  foreach($errs as $e){ echo h($e->message)."<br>"; }
  exit;
}

// ===============================
// 2) Cargar header/footer JSON
// ===============================
$cats = [];
$catsFile = __DIR__ . "/db/categorias.json";
if (file_exists($catsFile)) {
  $cats = json_decode(file_get_contents($catsFile), true);
  if (!is_array($cats)) $cats = [];
}

$footerJson = [];
$footerFile = __DIR__ . "/db/piedepagina.json";
if (file_exists($footerFile)) {
  $footerJson = json_decode(file_get_contents($footerFile), true);
  if (!is_array($footerJson)) $footerJson = [];
}

// ===============================
// 3) Leer estructura de página
// ===============================
$title = (string)($xml->meta->title ?? $xml->hero->title ?? "Página");
$subtitle = (string)($xml->hero->subtitle ?? "");

$heroImg = [
  'src' => (string)($xml->hero->media->image['src'] ?? ''),
  'alt' => (string)($xml->hero->media->image['alt'] ?? ''),
];

$badges = [];
if (isset($xml->hero->badges->badge)) {
  foreach ($xml->hero->badges->badge as $b) $badges[] = trim((string)$b);
}

$actions = [];
if (isset($xml->hero->actions->action)) {
  foreach ($xml->hero->actions->action as $a) {
    $actions[] = [
      'type' => (string)($a['type'] ?? ''),
      'text' => trim((string)$a),
      'href' => (string)($a['href'] ?? ''), // opcional
    ];
  }
}

// Sections
$sections = [];
if (isset($xml->sections->section)) {
  foreach ($xml->sections->section as $s) {
    $img = [
      'src' => (string)($s->media->image['src'] ?? ''),
      'alt' => (string)($s->media->image['alt'] ?? ''),
    ];

    $items = [];
    if (isset($s->items->item)) {
      foreach ($s->items->item as $it) $items[] = trim((string)$it);
    }

    $cards = [];
    if (isset($s->cards->card)) {
      foreach ($s->cards->card as $c) {
        $cards[] = [
          'title' => (string)($c->title ?? ''),
          'text'  => (string)($c->text ?? ''),
        ];
      }
    }

    $faqs = [];
    if (isset($s->faq->qa)) {
      foreach ($s->faq->qa as $qa) {
        $faqs[] = ['q'=>(string)$qa->q, 'a'=>(string)$qa->a];
      }
    }

    $sections[] = [
      'id' => (string)($s['id'] ?? ''),
      'layout' => (string)($s['layout'] ?? 'list'), // list|cards|faq|text
      'title' => (string)($s->title ?? ''),
      'subtitle' => (string)($s->subtitle ?? ''),
      'text' => (string)($s->text ?? ''),
      'image' => $img,
      'items' => $items,
      'cards' => $cards,
      'faqs'  => $faqs,
    ];
  }
}

function render_article_image(array $img){
  $src = safe_img_src($img['src'] ?? '');
  if ($src === "") return;
  $alt = trim((string)($img['alt'] ?? ''));
  ?>
  <div class="articleMedia">
    <img src="<?= h($src) ?>" alt="<?= h($alt) ?>" loading="lazy">
  </div>
  <?php
}
?>
<!doctype html>
<html lang="es">
  <head>
    <title><?= h($title) ?> · jocarsa</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">
    <style>
      @font-face {font-family: Ubuntu;src: url(estilo/Ubuntu-R.ttf);}
      @font-face {font-family: UbuntuB;src: url(estilo/Ubuntu-B.ttf);}

      html,body{padding:0;margin:0;font-family:Ubuntu,sans-serif;width:100%;height:100%;background:#fff;color:#111;}

      header{
        width:100%;
        display:flex;
        justify-content:center;
        align-items:center;
        box-shadow:0px 2px 4px rgba(0,0,0,0.3);
        gap:20px;
        padding:10px;
        position:sticky;top:0;
        background:rgba(255,255,255,0.95);
        backdrop-filter:saturate(180%) blur(12px);
        z-index:10;
      }
      header img{width:30px;}
      header a{text-decoration:none;color:indigo;font-size:11px;}

      .wrap{width:min(1100px, calc(100% - 24px)); margin:0 auto;}

      .hero{padding:60px 0 20px 0;text-align:center;}
      .hero h1{font-family:UbuntuB,Ubuntu,sans-serif;font-size:52px;margin:0;letter-spacing:-0.5px;}
      .hero p{margin:12px 0 0 0;color:#555;font-size:14px;line-height:1.5;}

      .badges{margin-top:16px;display:flex;justify-content:center;gap:10px;flex-wrap:wrap;}
      .badge{font-size:11px;padding:6px 10px;border-radius:999px;background:rgba(75,0,130,0.08);color:indigo;border:1px solid rgba(75,0,130,0.15);}

      .actions{margin-top:22px;display:flex;justify-content:center;gap:10px;flex-wrap:wrap;}
      .btn{text-decoration:none;padding:10px 18px;border-radius:999px;font-size:12px;display:inline-flex;align-items:center;gap:8px;border:1px solid rgba(0,0,0,0.12);background:#fff;color:#111;}
      .btn.primary{background:indigo;border-color:indigo;color:#fff;}

      main{width:100%;display:grid;grid-template-columns:1fr;gap:10px;padding:10px 0 30px 0;}

      main article{
        width:100%;
        min-height:320px;
        display:flex;
        justify-content:flex-start;
        align-items:center;
        background:linear-gradient(180deg, #f2f2f7, #ffffff);
        flex-direction:column;
        gap:12px;
        border-radius:18px;
        border:1px solid rgba(0,0,0,0.08);
        box-shadow:0px 10px 30px rgba(0,0,0,0.06);
        padding:0px;
        box-sizing:border-box;
        overflow:hidden;
      }

      .articleMedia{
        width:100%;
        height:170px;
        overflow:hidden;
        background:rgba(0,0,0,0.03);
        border-bottom:1px solid rgba(0,0,0,0.06);
      }
      .articleMedia img{
        width:100%;
        height:100%;
        object-fit:cover;
        display:block;
        transform:scale(1.02);
      }

      .articleBody{
        width:100%;
        padding:22px 24px 24px 24px;
        box-sizing:border-box;
        display:flex;
        flex-direction:column;
        align-items:center;
        gap:12px;
      }

      h3{padding:0;margin:0;text-align:center;font-family:UbuntuB,Ubuntu,sans-serif;font-size:28px;letter-spacing:-0.3px;}
      h4{padding:0;margin:0;text-align:center;font-size:13px;color:#555;font-weight:normal;line-height:1.5;max-width:760px;}

      .content{width:min(900px, 100%);display:flex;flex-direction:column;gap:10px;}

      .list{
        width:min(900px, 100%);
        margin:0 auto;
        padding:0;
        list-style:none;
        display:flex;
        flex-direction:column;
        gap:8px;
      }
      .list li{
        background:rgba(255,255,255,0.7);
        border:1px solid rgba(0,0,0,0.06);
        border-radius:12px;
        padding:10px 12px;
        font-size:13px;
        line-height:1.45;
      }

      .twocol{width:min(900px, 100%);display:grid;grid-template-columns:1fr;gap:10px;}
      .card{
        background:rgba(255,255,255,0.7);
        border:1px solid rgba(0,0,0,0.06);
        border-radius:14px;
        padding:14px;
        display:flex;
        flex-direction:column;
        gap:6px;
        min-height:120px;
      }
      .card b{font-family:UbuntuB,Ubuntu,sans-serif;}
      .card p{margin:0;font-size:13px;color:#444;line-height:1.45;}

      details{
        width:min(900px, 100%);
        background:rgba(255,255,255,0.7);
        border:1px solid rgba(0,0,0,0.06);
        border-radius:14px;
        padding:12px 14px;
      }
      summary{cursor:pointer;font-family:UbuntuB,Ubuntu,sans-serif;font-size:13px;color:#111;}
      details p{margin:10px 0 0 0;font-size:13px;color:#444;line-height:1.5;}

      @media (min-width:600px){
        .twocol{grid-template-columns:1fr 1fr;}
        .articleMedia{height:190px;}
      }

      footer{
        display:flex;justify-content:center;gap:20px;
        padding:20px;font-size:11px;border-top:1px solid rgba(0,0,0,0.08);
      }
      footer article{display:flex;flex-direction:column;gap:10px;}
      footer article a{text-decoration:none;color:indigo;}
    </style>
  </head>
  <body>

    <header>
      <a href="index.php"><img src="https://static.jocarsa.com/logos/jocarsa%20%7C%20Indigo.svg" alt="jocarsa"></a>
      <?php for($i=0;$i<count($cats);$i++){ ?>
        <a href="index.php?cat=<?= h($cats[$i]) ?>"><?= h($cats[$i]) ?></a>
      <?php } ?>
      <a href="pagina.php?p=sobrenosotros">Sobre nosotros</a>
      <a href="contacto.php">Contacto</a>
    </header>

    <section class="hero">
      <div class="wrap">
        <?php
          $heroSrc = safe_img_src($heroImg['src'] ?? '');
          if ($heroSrc !== "") { ?>
            <div style="width:min(1100px, calc(100% - 24px));margin:0 auto 18px auto;border-radius:18px;overflow:hidden;border:1px solid rgba(0,0,0,0.08);box-shadow:0px 10px 30px rgba(0,0,0,0.06);">
              <img src="<?= h($heroSrc) ?>" alt="<?= h($heroImg['alt'] ?? '') ?>" style="width:100%;height:240px;object-fit:cover;display:block;">
            </div>
        <?php } ?>

        <h1><?= h($title) ?></h1>
        <?php if($subtitle !== ""){ ?><p><?= h($subtitle) ?></p><?php } ?>

        <?php if(count($badges)){ ?>
          <div class="badges">
            <?php foreach($badges as $b){ ?><span class="badge"><?= h($b) ?></span><?php } ?>
          </div>
        <?php } ?>

        <?php if(count($actions)){ ?>
          <div class="actions">
            <?php foreach($actions as $a){
              $cls = ($a['type']==='primary') ? 'btn primary' : 'btn';
              $href = trim($a['href'] ?? '');
              if ($href === "") $href = "#";
            ?>
              <a class="<?= h($cls) ?>" href="<?= h($href) ?>"><?= h($a['text']) ?></a>
            <?php } ?>
          </div>
        <?php } ?>
      </div>
    </section>

    <main class="wrap">
      <?php foreach($sections as $sec){ ?>
        <article id="<?= h($sec['id']) ?>">
          <?php render_article_image($sec['image']); ?>
          <div class="articleBody">
            <h3><?= h($sec['title']) ?></h3>
            <?php if(trim($sec['subtitle']) !== ""){ ?><h4><?= h($sec['subtitle']) ?></h4><?php } ?>

            <?php if($sec['layout'] === 'text'){ ?>
              <?php if(trim($sec['text']) !== ""){ ?><h4><?= h($sec['text']) ?></h4><?php } ?>

            <?php } elseif($sec['layout'] === 'list'){ ?>
              <?php if(trim($sec['text']) !== ""){ ?><h4><?= h($sec['text']) ?></h4><?php } ?>
              <?php if(count($sec['items'])){ ?>
                <ul class="list">
                  <?php foreach($sec['items'] as $it){ ?><li><?= h($it) ?></li><?php } ?>
                </ul>
              <?php } ?>

            <?php } elseif($sec['layout'] === 'cards'){ ?>
              <?php if(trim($sec['text']) !== ""){ ?><h4><?= h($sec['text']) ?></h4><?php } ?>
              <div class="twocol">
                <?php foreach($sec['cards'] as $c){ ?>
                  <div class="card">
                    <b><?= h($c['title']) ?></b>
                    <p><?= h($c['text']) ?></p>
                  </div>
                <?php } ?>
              </div>

            <?php } elseif($sec['layout'] === 'faq'){ ?>
              <?php if(trim($sec['text']) !== ""){ ?><h4><?= h($sec['text']) ?></h4><?php } ?>
              <?php foreach($sec['faqs'] as $qa){ ?>
                <details>
                  <summary><?= h($qa['q']) ?></summary>
                  <p><?= h($qa['a']) ?></p>
                </details>
              <?php } ?>

            <?php } else { ?>
              <?php if(trim($sec['text']) !== ""){ ?><h4><?= h($sec['text']) ?></h4><?php } ?>
            <?php } ?>
          </div>
        </article>
      <?php } ?>
    </main>

    <footer>
      <?php
        $catsFooter = $footerJson['categorias'] ?? [];
        $linksFooter = $footerJson['enlaces'] ?? [];
      ?>
      <article class="categorias">
        <?php if(is_array($catsFooter)) for($i=0;$i<count($catsFooter);$i++){ ?>
          <a href="index.php?cat=<?= h($catsFooter[$i]) ?>"><?= h($catsFooter[$i]) ?></a>
        <?php } ?>
      </article>

      <article class="paginas">
        <?php if(is_array($linksFooter)) for($i=0;$i<count($linksFooter);$i++){ ?>
          <a href="<?= h($linksFooter[$i]['enlace'] ?? '#') ?>"><?= h($linksFooter[$i]['nombre'] ?? '') ?></a>
        <?php } ?>
      </article>
    </footer>

  </body>
</html>

