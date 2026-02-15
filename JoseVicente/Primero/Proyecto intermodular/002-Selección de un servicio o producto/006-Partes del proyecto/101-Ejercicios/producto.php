<?php
// producto.php — XML + XSD (con <media><image/>) + diseño Appleweb-like (tu estilo)

error_reporting(E_ALL);
ini_set('display_errors', 1);

function h($s){ return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }

// -------------------------------
// 1) Cargar XML de producto
//    Uso: producto.php?file=db/productos/gestion-academica-pro.xml
// -------------------------------
$defaultXml = __DIR__ . "/productos/".$_GET['p'].".xml";
$xmlFile = $_GET['file'] ?? $defaultXml;

// Permitir rutas relativas simples dentro del proyecto (sin ../)
if (!preg_match('/^[a-zA-Z0-9_\-\/\.]+$/', (string)$xmlFile) || str_contains((string)$xmlFile, '..')) {
  $xmlFile = $defaultXml;
}
if (!str_starts_with((string)$xmlFile, '/')) {
  $xmlFile = __DIR__ . '/' . ltrim((string)$xmlFile, '/');
}

if (!file_exists($xmlFile)) {
  http_response_code(404);
  die("XML no encontrado: ".h($xmlFile));
}

libxml_use_internal_errors(true);
$xml = simplexml_load_file($xmlFile);
if (!$xml) {
  http_response_code(500);
  $errs = libxml_get_errors();
  echo "Error leyendo XML<br>";
  foreach($errs as $e){ echo h($e->message)."<br>"; }
  exit;
}

// -------------------------------
// Helpers
// -------------------------------
function nodes_to_array($nodes) {
  $out = [];
  if (!$nodes) return $out;
  foreach ($nodes as $n) $out[] = trim((string)$n);
  return $out;
}

function read_image($node): array {
  // Devuelve ['src'=>..., 'alt'=>...] o ['src'=>'','alt'=>'']
  $src = "";
  $alt = "";
  if (isset($node->media->image)) {
    $src = (string)($node->media->image['src'] ?? '');
    $alt = (string)($node->media->image['alt'] ?? '');
  }
  return ['src'=>$src, 'alt'=>$alt];
}

function safe_img_src($src): string {
  // Acepta http(s) y rutas relativas simples (sin ../)
  $src = trim((string)$src);
  if ($src === "") return "";
  if (str_contains($src, '..')) return "";
  if (preg_match('#^https?://#i', $src)) return $src;
  // ruta relativa
  if (!preg_match('/^[a-zA-Z0-9_\-\/\.\%\=\?\&]+$/', $src)) return "";
  return $src;
}

// -------------------------------
// Datos
// -------------------------------
$metaTitle = (string)($xml->meta->title ?? $xml->hero->name ?? "Producto");

$heroImg   = read_image($xml->hero);
$heroName  = (string)($xml->hero->name ?? "");
$heroValue = (string)($xml->hero->valueProposition ?? "");
$heroSub   = (string)($xml->hero->subtitle ?? "");

$heroActions = [];
if (isset($xml->hero->actions->action)) {
  foreach ($xml->hero->actions->action as $a) {
    $heroActions[] = [
      'type' => (string)($a['type'] ?? ''),
      'text' => trim((string)$a),
    ];
  }
}
$badges = nodes_to_array($xml->hero->badges->badge ?? null);

// Secciones + imagen
$problemImg   = read_image($xml->problem);
$problemTitle = (string)($xml->problem->title ?? "Problemas");
$problemItems = nodes_to_array($xml->problem->items->item ?? null);

$solutionImg    = read_image($xml->solution);
$solutionTitle  = (string)($xml->solution->title ?? "La solución");
$solutionOverview = (string)($xml->solution->overview ?? "");
$solutionChanges  = nodes_to_array($xml->solution->whatChanges->change ?? null);

$featuresImg   = read_image($xml->keyFeatures);
$featuresTitle = (string)($xml->keyFeatures->title ?? "Funcionalidades");
$features = [];
if (isset($xml->keyFeatures->feature)) {
  foreach ($xml->keyFeatures->feature as $f) {
    $features[] = ['name'=>(string)$f->name, 'benefit'=>(string)$f->benefit];
  }
}

$audImg   = read_image($xml->targetAudience);
$audTitle = (string)($xml->targetAudience->title ?? "¿Para quién es?");
$profiles = [];
if (isset($xml->targetAudience->profiles->profile)) {
  foreach ($xml->targetAudience->profiles->profile as $p) {
    $profiles[] = ['name'=>(string)$p->name, 'fit'=>(string)$p->fit];
  }
}

$useImg   = read_image($xml->useCases);
$useTitle = (string)($xml->useCases->title ?? "Casos de uso");
$useCases = [];
if (isset($xml->useCases->case)) {
  foreach ($xml->useCases->case as $c) {
    $useCases[] = ['name'=>(string)$c->name, 'description'=>(string)$c->description];
  }
}

$benefitsImg   = read_image($xml->benefits);
$benefitsTitle = (string)($xml->benefits->title ?? "Beneficios");
$benefitItems  = nodes_to_array($xml->benefits->items->item ?? null);

$integrationsImg   = isset($xml->integrations) ? read_image($xml->integrations) : ['src'=>'','alt'=>''];
$integrationsTitle = (string)($xml->integrations->title ?? "");
$integrationsNotes = (string)($xml->integrations->notes ?? "");
$integrationsItems = nodes_to_array($xml->integrations->items->item ?? null);

$trustImg    = read_image($xml->trust);
$trustTitle  = (string)($xml->trust->title ?? "Confianza");
$trustPoints = nodes_to_array($xml->trust->points->point ?? null);

$ctaImg   = read_image($xml->finalCTA);
$ctaTitle = (string)($xml->finalCTA->title ?? "¿Hablamos?");
$ctaDesc  = (string)($xml->finalCTA->description ?? "");

$ctaActions = [];
if (isset($xml->finalCTA->actions->action)) {
  foreach ($xml->finalCTA->actions->action as $a) {
    $ctaActions[] = ['type'=>(string)($a['type'] ?? ''), 'text'=>trim((string)$a)];
  }
}

$contactEmail = (string)($xml->finalCTA->contact->email ?? "");
$formFields = [];
if (isset($xml->finalCTA->contact->form->field)) {
  foreach ($xml->finalCTA->contact->form->field as $f) {
    $formFields[] = [
      'name' => (string)($f['name'] ?? ''),
      'type' => (string)($f['type'] ?? 'text'),
      'required' => ((string)($f['required'] ?? 'false')) === 'true',
    ];
  }
}

$faqImg   = read_image($xml->faq);
$faqTitle = (string)($xml->faq->title ?? "Preguntas frecuentes");
$faqs = [];
if (isset($xml->faq->qa)) {
  foreach ($xml->faq->qa as $qa) {
    $faqs[] = ['q'=>(string)$qa->q, 'a'=>(string)$qa->a];
  }
}

$footerSummary = (string)($xml->footer->summary ?? "");

// Header/footer JSON como tu web
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

// Render helper (imagen en cabecera de article)
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
    <title><?= h($metaTitle) ?> · jocarsa</title>
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

      .hero{padding:60px 0 30px 0;text-align:center;}
      .hero h1{font-family:UbuntuB,Ubuntu,sans-serif;font-size:52px;margin:0;letter-spacing:-0.5px;}
      .hero .value{font-size:18px;color:#333;margin:14px 0 0 0;}
      .hero .sub{font-size:14px;color:#666;margin:10px 0 0 0;line-height:1.5;}

      .badges{margin-top:16px;display:flex;justify-content:center;gap:10px;flex-wrap:wrap;}
      .badge{font-size:11px;padding:6px 10px;border-radius:999px;background:rgba(75,0,130,0.08);color:indigo;border:1px solid rgba(75,0,130,0.15);}

      .actions{margin-top:22px;display:flex;justify-content:center;gap:10px;flex-wrap:wrap;}
      .btn{text-decoration:none;padding:10px 18px;border-radius:999px;font-size:12px;display:inline-flex;align-items:center;gap:8px;border:1px solid rgba(0,0,0,0.12);background:#fff;color:#111;}
      .btn.primary{background:indigo;border-color:indigo;color:#fff;}

      main{width:100%;display:grid;grid-template-columns:1fr;gap:10px;padding:10px 0 30px 0;}

      main article{
        width:100%;
        min-height:360px;
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
        position:relative;
      }

      /* IMAGEN ARRIBA DEL ARTICLE ////////////////////////////// */
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

      main article h3, main article h4{padding:0;margin:0;text-align:center;}
      main article h3{font-family:UbuntuB,Ubuntu,sans-serif;font-size:28px;letter-spacing:-0.3px;}
      main article h4{font-size:13px;color:#555;font-weight:normal;line-height:1.5;max-width:760px;}

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

      main article:nth-child(-n+3){grid-column:1 / -1;}

      @media (min-width:600px){
        main{grid-template-columns:1fr 1fr;}
        main article:nth-child(-n+3){grid-column:1 / -1;}
        .twocol{grid-template-columns:1fr 1fr;}
        .articleMedia{height:190px;}
      }

      details{
        width:min(900px, 100%);
        background:rgba(255,255,255,0.7);
        border:1px solid rgba(0,0,0,0.06);
        border-radius:14px;
        padding:12px 14px;
      }
      summary{cursor:pointer;font-family:UbuntuB,Ubuntu,sans-serif;font-size:13px;color:#111;}
      details p{margin:10px 0 0 0;font-size:13px;color:#444;line-height:1.5;}

      .ctaBox{width:min(900px, 100%);display:flex;flex-direction:column;gap:10px;align-items:center;}
      .mini{font-size:12px;color:#666;text-align:center;line-height:1.45;}
      .email{font-size:12px;color:indigo;text-decoration:none;}

      form{width:min(650px, 100%);display:grid;grid-template-columns:1fr;gap:10px;margin-top:6px;}
      input, textarea, select{
        width:100%;
        padding:12px 12px;
        border-radius:12px;
        border:1px solid rgba(0,0,0,0.12);
        font-family:Ubuntu,sans-serif;
        font-size:13px;
        box-sizing:border-box;
        outline:none;
      }
      textarea{min-height:120px;resize:vertical;}
      .submit{
        background:indigo;border:1px solid indigo;color:white;
        padding:12px 16px;border-radius:999px;cursor:pointer;
        font-size:12px;justify-self:center;width:220px;
      }

      footer{
        display:flex;justify-content:center;gap:20px;
        padding:20px;font-size:11px;border-top:1px solid rgba(0,0,0,0.08);
      }
      footer article{display:flex;flex-direction:column;gap:10px;}
      footer article a{text-decoration:none;color:indigo;}
      .footerSummary{padding:0 0 30px 0;text-align:center;color:#666;font-size:11px;}
    </style>
  </head>
  <body>

    <header>
      <a href="index.php"><img src="https://static.jocarsa.com/logos/jocarsa%20%7C%20Indigo.svg" alt="jocarsa"></a>
      <?php for($i=0;$i<count($cats);$i++){ ?>
        <a href="index.php?cat=<?= h($cats[$i]) ?>"><?= h($cats[$i]) ?></a>
      <?php } ?>
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

        <h1><?= h($heroName ?: $metaTitle) ?></h1>
        <?php if($heroValue !== ""){ ?><p class="value"><?= h($heroValue) ?></p><?php } ?>
        <?php if($heroSub !== ""){ ?><p class="sub"><?= h($heroSub) ?></p><?php } ?>

        <?php if(count($badges)){ ?>
          <div class="badges">
            <?php foreach($badges as $b){ ?><span class="badge"><?= h($b) ?></span><?php } ?>
          </div>
        <?php } ?>

        <?php if(count($heroActions)){ ?>
          <div class="actions">
            <?php foreach($heroActions as $a){
              $cls = ($a['type']==='primary') ? 'btn primary' : 'btn';
              $anchor = '#contacto';
              if (stripos($a['text'], 'cómo') !== false || stripos($a['text'], 'funciona') !== false) $anchor = '#como';
              if (stripos($a['text'], 'contact') !== false) $anchor = '#contacto';
            ?>
              <a class="<?= h($cls) ?>" href="<?= h($anchor) ?>"><?= h($a['text']) ?></a>
            <?php } ?>
          </div>
        <?php } ?>
      </div>
    </section>

    <main class="wrap">

      <article id="problema">
        <?php render_article_image($problemImg); ?>
        <div class="articleBody">
          <h3><?= h($problemTitle) ?></h3>
          <h4>Lo que normalmente frena a un centro cuando quiere crecer sin perder control.</h4>
          <ul class="list">
            <?php foreach($problemItems as $it){ ?><li><?= h($it) ?></li><?php } ?>
          </ul>
        </div>
      </article>

      <article id="solucion">
        <?php render_article_image($solutionImg); ?>
        <div class="articleBody">
          <h3><?= h($solutionTitle) ?></h3>
          <div class="content">
            <?php if($solutionOverview !== ""){ ?><h4><?= h($solutionOverview) ?></h4><?php } ?>
            <?php if(count($solutionChanges)){ ?>
              <ul class="list">
                <?php foreach($solutionChanges as $ch){ ?><li><?= h($ch) ?></li><?php } ?>
              </ul>
            <?php } ?>
          </div>
        </div>
      </article>

      <article id="como">
        <?php render_article_image($featuresImg); ?>
        <div class="articleBody">
          <h3><?= h($featuresTitle) ?></h3>
          <h4>Lo esencial, explicado desde el beneficio.</h4>
          <div class="twocol">
            <?php foreach($features as $f){ ?>
              <div class="card">
                <b><?= h($f['name']) ?></b>
                <p><?= h($f['benefit']) ?></p>
              </div>
            <?php } ?>
          </div>
        </div>
      </article>

      <article>
        <?php render_article_image($audImg); ?>
        <div class="articleBody">
          <h3><?= h($audTitle) ?></h3>
          <h4>Si te reconoces aquí, esto está hecho para tu día a día.</h4>
          <div class="twocol">
            <?php foreach($profiles as $p){ ?>
              <div class="card">
                <b><?= h($p['name']) ?></b>
                <p><?= h($p['fit']) ?></p>
              </div>
            <?php } ?>
          </div>
        </div>
      </article>

      <article>
        <?php render_article_image($useImg); ?>
        <div class="articleBody">
          <h3><?= h($useTitle) ?></h3>
          <h4>Situaciones reales donde se nota el cambio.</h4>
          <div class="twocol">
            <?php foreach($useCases as $c){ ?>
              <div class="card">
                <b><?= h($c['name']) ?></b>
                <p><?= h($c['description']) ?></p>
              </div>
            <?php } ?>
          </div>
        </div>
      </article>

      <article>
        <?php render_article_image($benefitsImg); ?>
        <div class="articleBody">
          <h3><?= h($benefitsTitle) ?></h3>
          <h4>Resultados prácticos para el centro y el equipo.</h4>
          <ul class="list">
            <?php foreach($benefitItems as $it){ ?><li><?= h($it) ?></li><?php } ?>
          </ul>
        </div>
      </article>

      <?php if($integrationsTitle !== "" || count($integrationsItems)){ ?>
      <article>
        <?php render_article_image($integrationsImg); ?>
        <div class="articleBody">
          <h3><?= h($integrationsTitle ?: "Integración y compatibilidad") ?></h3>
          <?php if($integrationsNotes !== ""){ ?><h4><?= h($integrationsNotes) ?></h4><?php } ?>
          <ul class="list">
            <?php foreach($integrationsItems as $it){ ?><li><?= h($it) ?></li><?php } ?>
          </ul>
        </div>
      </article>
      <?php } ?>

      <article>
        <?php render_article_image($trustImg); ?>
        <div class="articleBody">
          <h3><?= h($trustTitle) ?></h3>
          <h4>Para decidir con tranquilidad.</h4>
          <ul class="list">
            <?php foreach($trustPoints as $it){ ?><li><?= h($it) ?></li><?php } ?>
          </ul>
        </div>
      </article>

      <article id="contacto">
        <?php render_article_image($ctaImg); ?>
        <div class="articleBody">
          <h3><?= h($ctaTitle) ?></h3>
          <?php if($ctaDesc !== ""){ ?><h4><?= h($ctaDesc) ?></h4><?php } ?>

          <div class="ctaBox">
            <?php if(count($ctaActions)){ ?>
              <div class="actions">
                <?php foreach($ctaActions as $a){
                  $cls = ($a['type']==='primary') ? 'btn primary' : 'btn';
                ?>
                  <a class="<?= h($cls) ?>" href="#contacto"><?= h($a['text']) ?></a>
                <?php } ?>
              </div>
            <?php } ?>

            <?php if($contactEmail !== ""){ ?>
              <div class="mini">Contacto directo: <a class="email" href="mailto:<?= h($contactEmail) ?>"><?= h($contactEmail) ?></a></div>
            <?php } ?>

            <?php if(count($formFields)){ ?>
              <form method="post" action="enviar.php">
                <?php foreach($formFields as $f){
                  $name = $f['name'];
                  $type = $f['type'];
                  $req  = $f['required'] ? 'required' : '';
                  $ph = ucfirst(str_replace('_',' ', $name));

                  if ($type === 'textarea') { ?>
                    <textarea name="<?= h($name) ?>" placeholder="<?= h($ph) ?>" <?= $req ?>></textarea>
                  <?php } else { ?>
                    <input type="<?= h($type === 'tel' ? 'tel' : ($type === 'email' ? 'email' : 'text')) ?>"
                           name="<?= h($name) ?>"
                           placeholder="<?= h($ph) ?>"
                           <?= $req ?>>
                  <?php } ?>
                <?php } ?>
                <button class="submit" type="submit">Enviar</button>
              </form>
              <div class="mini">Puedes conectar <b>enviar.php</b> a tu CRM o a un correo.</div>
            <?php } ?>
          </div>
        </div>
      </article>

      <article>
        <?php render_article_image($faqImg); ?>
        <div class="articleBody">
          <h3><?= h($faqTitle) ?></h3>
          <h4>Respuestas rápidas a dudas habituales.</h4>
          <?php foreach($faqs as $qa){ ?>
            <details>
              <summary><?= h($qa['q']) ?></summary>
              <p><?= h($qa['a']) ?></p>
            </details>
          <?php } ?>
        </div>
      </article>

    </main>

    <?php if($footerSummary !== ""){ ?>
      <div class="footerSummary wrap"><?= h($footerSummary) ?></div>
    <?php } ?>

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

