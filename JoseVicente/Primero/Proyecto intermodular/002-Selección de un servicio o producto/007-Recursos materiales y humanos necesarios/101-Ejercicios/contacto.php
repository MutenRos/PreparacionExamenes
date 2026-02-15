<?php
// contacto.php — Página de contacto (formulario + datos + mapa OpenStreetMap)
// Estilo Appleweb-like (tu estilo) + header/footer desde db/*.json

error_reporting(E_ALL);
ini_set('display_errors', 1);

function h($s){ return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }

// ===============================
// CONFIG CONTACTO (edita aquí)
// ===============================
const CONTACT_EMAIL = "contacto@tudominio.com";
const CONTACT_PHONE = "+34 600 000 000";

// Coordenadas del mapa (edita aquí)
const MAP_LAT = 39.4699;
const MAP_LNG = -0.3763;
const MAP_ZOOM = 14;

// (Opcional) Envío de email con mail()
// - En muchos servidores requiere configuración del MTA.
// - Si prefieres guardarlo en SQLite o mandarlo por SMTP, dímelo y te lo adapto.
const SEND_EMAIL = false;
const EMAIL_TO = "contacto@tudominio.com";

// ===============================
// Cargar header/footer JSON (como tu web)
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
// Procesar formulario (POST)
// ===============================
$ok = false;
$error = "";

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
  // Honeypot anti-spam
  $hp = trim($_POST['empresa_web'] ?? '');
  if ($hp !== "") {
    $error = "Solicitud no válida.";
  } else {
    $nombre  = trim($_POST['nombre'] ?? '');
    $centro  = trim($_POST['centro'] ?? '');
    $email   = trim($_POST['email'] ?? '');
    $telefono= trim($_POST['telefono'] ?? '');
    $mensaje = trim($_POST['mensaje'] ?? '');

    if ($nombre === "" || $centro === "" || $email === "" || $mensaje === "") {
      $error = "Por favor, completa los campos obligatorios.";
    } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
      $error = "El email no parece válido.";
    } else {
      // Aquí puedes guardar en DB, mandar por API, etc.
      if (SEND_EMAIL) {
        $subject = "Contacto web — " . $nombre . " (" . $centro . ")";
        $body =
          "Nombre: $nombre\n".
          "Centro: $centro\n".
          "Email: $email\n".
          "Teléfono: $telefono\n\n".
          "Mensaje:\n$mensaje\n";
        $headers = "From: ".CONTACT_EMAIL."\r\nReply-To: $email\r\n";
        @mail(EMAIL_TO, $subject, $body, $headers);
      }
      $ok = true;
    }
  }
}
?>
<!doctype html>
<html lang="es">
  <head>
    <title>Contacto · jocarsa</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width,initial-scale=1">

    <!-- Leaflet (OpenStreetMap) -->
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css">
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

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
        position:sticky;
        top:0;
        background:rgba(255,255,255,0.95);
        backdrop-filter:saturate(180%) blur(12px);
        z-index:10;
      }
      header img{width:30px;}
      header a{text-decoration:none;color:indigo;font-size:11px;}

      .wrap{width:min(1100px, calc(100% - 24px)); margin:0 auto;}

      /* HERO */
      .hero{padding:60px 0 20px 0;text-align:center;}
      .hero h1{font-family:UbuntuB,Ubuntu,sans-serif;font-size:52px;margin:0;letter-spacing:-0.5px;}
      .hero p{margin:12px 0 0 0;color:#555;font-size:14px;line-height:1.5;}

      /* GRID */
      main{
        width:100%;
        display:grid;
        grid-template-columns:1fr;
        gap:10px;
        padding:10px 0 30px 0;
      }

      article{
        width:100%;
        background:linear-gradient(180deg, #f2f2f7, #ffffff);
        border-radius:18px;
        border:1px solid rgba(0,0,0,0.08);
        box-shadow:0px 10px 30px rgba(0,0,0,0.06);
        overflow:hidden;
      }

      .articleMedia{
        width:100%;
        height:190px;
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
        padding:22px 24px 24px 24px;
        box-sizing:border-box;
        display:flex;
        flex-direction:column;
        gap:12px;
        align-items:center;
      }

      h3{padding:0;margin:0;text-align:center;font-family:UbuntuB,Ubuntu,sans-serif;font-size:28px;letter-spacing:-0.3px;}
      h4{padding:0;margin:0;text-align:center;font-size:13px;color:#555;font-weight:normal;line-height:1.5;max-width:760px;}

      /* CONTACT CARDS */
      .twocol{width:min(900px, 100%);display:grid;grid-template-columns:1fr;gap:10px;}
      .card{
        background:rgba(255,255,255,0.7);
        border:1px solid rgba(0,0,0,0.06);
        border-radius:14px;
        padding:14px;
        display:flex;
        flex-direction:column;
        gap:6px;
      }
      .card b{font-family:UbuntuB,Ubuntu,sans-serif;}
      .card a{color:indigo;text-decoration:none;font-size:13px;}
      .card p{margin:0;font-size:13px;color:#444;line-height:1.45;}

      /* FORM */
      form{width:min(650px, 100%);display:grid;grid-template-columns:1fr;gap:10px;margin-top:6px;}
      input, textarea{
        width:100%;
        padding:12px 12px;
        border-radius:12px;
        border:1px solid rgba(0,0,0,0.12);
        font-family:Ubuntu,sans-serif;
        font-size:13px;
        box-sizing:border-box;
        outline:none;
        background:#fff;
      }
      textarea{min-height:140px;resize:vertical;}
      .submit{
        background:indigo;border:1px solid indigo;color:white;
        padding:12px 16px;border-radius:999px;cursor:pointer;
        font-size:12px;justify-self:center;width:220px;
      }

      .note{
        width:min(650px, 100%);
        font-size:12px;
        color:#666;
        text-align:center;
        line-height:1.45;
      }

      .alert{
        width:min(650px, 100%);
        border-radius:14px;
        padding:12px 14px;
        border:1px solid rgba(0,0,0,0.06);
        background:rgba(255,255,255,0.7);
        font-size:13px;
        text-align:center;
      }
      .alert.ok{ border-color: rgba(0,128,0,0.25); }
      .alert.err{ border-color: rgba(180,0,0,0.25); }

      /* MAP */
      #map{
        width:min(900px, 100%);
        height:360px;
        border-radius:18px;
        overflow:hidden;
        border:1px solid rgba(0,0,0,0.08);
        box-shadow:0px 10px 30px rgba(0,0,0,0.06);
        background:#f2f2f7;
      }

      @media (min-width:800px){
        .twocol{grid-template-columns:1fr 1fr;}
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
        <h1>Contacto</h1>
        <p>Cuéntanos tu caso y te respondemos con una propuesta clara y práctica.</p>
      </div>
    </section>

    <main class="wrap">

      <!-- 1) Formulario -->
      <article>
        <div class="articleMedia">
          <img src="https://static.jocarsa.com/demo/edu/cta.jpg" alt="Contacto" loading="lazy">
        </div>

        <div class="articleBody">
          <h3>Escríbenos</h3>
          <h4>Te contestamos con información directa, sin rodeos.</h4>

          <?php if($ok){ ?>
            <div class="alert ok">Mensaje enviado correctamente. Te responderemos lo antes posible.</div>
          <?php } elseif($error !== "") { ?>
            <div class="alert err"><?= h($error) ?></div>
          <?php } ?>

          <form method="post" action="contacto.php">
            <!-- Honeypot invisible -->
            <input type="text" name="empresa_web" value="" style="display:none" tabindex="-1" autocomplete="off">

            <input type="text" name="nombre" placeholder="Nombre *" required value="<?= h($_POST['nombre'] ?? '') ?>">
            <input type="text" name="centro" placeholder="Centro / Empresa *" required value="<?= h($_POST['centro'] ?? '') ?>">
            <input type="email" name="email" placeholder="Email *" required value="<?= h($_POST['email'] ?? '') ?>">
            <input type="tel" name="telefono" placeholder="Teléfono" value="<?= h($_POST['telefono'] ?? '') ?>">
            <textarea name="mensaje" placeholder="Mensaje *" required><?= h($_POST['mensaje'] ?? '') ?></textarea>

            <button class="submit" type="submit">Enviar</button>
          </form>

          <div class="note">
            También puedes escribir a <a href="mailto:<?= h(CONTACT_EMAIL) ?>" style="color:indigo;text-decoration:none;"><?= h(CONTACT_EMAIL) ?></a>
            o llamar al <a href="tel:<?= h(CONTACT_PHONE) ?>" style="color:indigo;text-decoration:none;"><?= h(CONTACT_PHONE) ?></a>.
          </div>
        </div>
      </article>

      <!-- 2) Datos de contacto -->
      <article>
        <div class="articleMedia">
          <img src="https://static.jocarsa.com/demo/edu/trust.jpg" alt="Datos de contacto" loading="lazy">
        </div>

        <div class="articleBody">
          <h3>Datos</h3>
          <h4>Canales directos para hablar contigo con rapidez.</h4>

          <div class="twocol">
            <div class="card">
              <b>Email</b>
              <p>Respuesta ágil y con detalles.</p>
              <a href="mailto:<?= h(CONTACT_EMAIL) ?>"><?= h(CONTACT_EMAIL) ?></a>
            </div>

            <div class="card">
              <b>Teléfono</b>
              <p>Para consultas rápidas o coordinación.</p>
              <a href="tel:<?= h(CONTACT_PHONE) ?>"><?= h(CONTACT_PHONE) ?></a>
            </div>
          </div>
        </div>
      </article>

      <!-- 3) Mapa OpenStreetMap (Leaflet) -->
      <article>
        <div class="articleMedia">
          <img src="https://static.jocarsa.com/demo/edu/map.jpg" alt="Mapa" loading="lazy">
        </div>

        <div class="articleBody">
          <h3>Ubicación</h3>
          <h4>Mapa basado en OpenStreetMap.</h4>

          <div id="map"></div>

          <div class="note">
            Si prefieres reunión online, también podemos hacer una demo por videollamada.
          </div>
        </div>
      </article>

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

    <script>
      // OpenStreetMap con Leaflet
      const lat = <?= json_encode(MAP_LAT) ?>;
      const lng = <?= json_encode(MAP_LNG) ?>;
      const zoom = <?= json_encode(MAP_ZOOM) ?>;

      const map = L.map('map', { scrollWheelZoom: false }).setView([lat, lng], zoom);

      L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; OpenStreetMap contributors'
      }).addTo(map);

      const marker = L.marker([lat, lng]).addTo(map);
      marker.bindPopup("<?= h('JOCARSA · Contacto') ?>").openPopup();
    </script>

  </body>
</html>

