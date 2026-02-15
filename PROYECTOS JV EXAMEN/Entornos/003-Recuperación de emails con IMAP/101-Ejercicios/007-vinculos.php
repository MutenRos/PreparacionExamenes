<?php
// ----------------------------------------------------
// CONFIGURACIÓN IMAP
// ----------------------------------------------------
$hostname = '{imap.ionos.es:993/imap/ssl}INBOX'; // Cambiar si no se usa Gmail
$username = 'python@jocarsa.com';
$password = 'TAME123$';

// Longitud del resumen (portada)
define('EXCERPT_LENGTH', 400);

// ----------------------------------------------------
// FUNCIÓN: decodificar contenido según encoding IMAP
// ----------------------------------------------------
function decodePart($content, $encoding)
{
    switch ($encoding) {
        case 3: // BASE64
            return base64_decode($content);
        case 4: // QUOTED-PRINTABLE
            return quoted_printable_decode($content);
        default:
            return $content;
    }
}

// ----------------------------------------------------
// FUNCIONES PARA EXTRAER CUERPO E IMAGEN DESTACADA
// ----------------------------------------------------

/**
 * Extrae cuerpo HTML / texto y primera imagen encontrada.
 * Devuelve:
 * [
 *   'html'  => string|null,
 *   'text'  => string|null (HTML-safe),
 *   'image' => ['dataUri' => string, 'filename' => string]|null
 * ]
 */
function extractEmailParts($imap, $msgno)
{
    $structure = imap_fetchstructure($imap, $msgno);

    $result = [
        'html'  => null,
        'text'  => null,
        'image' => null,
    ];

    // Mensaje simple (sin multipart)
    if (!isset($structure->parts)) {
        $content = imap_body($imap, $msgno);
        $content = decodePart($content, $structure->encoding ?? 0);

        if ($structure->type == 0) { // texto
            $subtype = isset($structure->subtype) ? strtoupper($structure->subtype) : '';
            if ($subtype === 'HTML') {
                $result['html'] = $content;
            } else {
                $result['text'] = nl2br(htmlspecialchars($content, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'));
            }
        }

        // Caso raro: único contenido es una imagen
        if ($structure->type == 5) {
            $subtype = isset($structure->subtype) ? strtolower($structure->subtype) : 'jpeg';
            $mime = 'image/' . $subtype;
            $dataUri = 'data:' . $mime . ';base64,' . base64_encode($content);
            $result['image'] = [
                'dataUri'  => $dataUri,
                'filename' => 'image.' . $subtype,
            ];
        }

        return $result;
    }

    // Multipart: recorrer recursivamente
    traverseParts($imap, $msgno, $structure, '', $result);

    return $result;
}

/**
 * Recorre recursivamente las partes MIME.
 * Rellena $result por referencia.
 */
function traverseParts($imap, $msgno, $structure, $prefix, &$result)
{
    if (!isset($structure->parts)) {
        return;
    }

    foreach ($structure->parts as $index => $part) {
        $partNumber = $prefix === '' ? (string)($index + 1) : $prefix . '.' . ($index + 1);

        if (isset($part->parts) && count($part->parts) > 0) {
            traverseParts($imap, $msgno, $part, $partNumber, $result);
            continue;
        }

        $type    = $part->type ?? null;   // 0 = text, 5 = image
        $subtype = isset($part->subtype) ? strtoupper($part->subtype) : '';
        $content = imap_fetchbody($imap, $msgno, $partNumber);
        $content = decodePart($content, $part->encoding ?? 0);

        // Texto
        if ($type === 0) {
            if ($subtype === 'HTML' && $result['html'] === null) {
                $result['html'] = $content;
            } elseif ($subtype === 'PLAIN' && $result['text'] === null) {
                $result['text'] = nl2br(htmlspecialchars($content, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'));
            }
        }

        // Imagen (adjunto o inline)
        if ($type === 5 && $result['image'] === null) {
            $filename = null;

            if (!empty($part->dparameters)) {
                foreach ($part->dparameters as $param) {
                    if (isset($param->attribute) && in_array(strtoupper($param->attribute), ['NAME', 'FILENAME'])) {
                        $filename = $param->value;
                        break;
                    }
                }
            }

            if (!$filename && !empty($part->parameters)) {
                foreach ($part->parameters as $param) {
                    if (isset($param->attribute) && in_array(strtoupper($param->attribute), ['NAME', 'FILENAME'])) {
                        $filename = $param->value;
                        break;
                    }
                }
            }

            if (!$filename) {
                $filename = 'imagen_' . $partNumber . '.jpg';
            }

            $mimeSubtype = strtolower($subtype ?: 'jpeg');
            $mime        = 'image/' . $mimeSubtype;
            $dataUri     = 'data:' . $mime . ';base64,' . base64_encode($content);

            $result['image'] = [
                'dataUri'  => $dataUri,
                'filename' => $filename,
            ];
        }
    }
}

// ----------------------------------------------------
// FUNCIÓN PARA GENERAR EXCERPT DEL CUERPO
// ----------------------------------------------------
function makeExcerpt($html, $length = EXCERPT_LENGTH)
{
    // Quitar etiquetas y normalizar espacios
    $text = trim(strip_tags($html));
    $text = preg_replace('/\s+/', ' ', $text);

    if (function_exists('mb_strlen') && function_exists('mb_substr')) {
        if (mb_strlen($text, 'UTF-8') <= $length) {
            return $text;
        }
        return mb_substr($text, 0, $length, 'UTF-8') . '…';
    } else {
        if (strlen($text) <= $length) {
            return $text;
        }
        return substr($text, 0, $length) . '…';
    }
}

// ----------------------------------------------------
// CONEXIÓN IMAP
// ----------------------------------------------------
$inbox = @imap_open($hostname, $username, $password);

if (!$inbox) {
    die('Error IMAP: ' . imap_last_error());
}

// Si hay parámetro ?id=NNN, se muestra vista detallada
$selectedId = isset($_GET['id']) ? (int)$_GET['id'] : null;

// En vista detalle, no necesitamos buscar todos
if ($selectedId) {
    $emails = [$selectedId];
    $isDetail = true;
} else {
    // Portada: listar varios correos
    $emails = imap_search($inbox, 'ALL');
    $isDetail = false;
}
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>
        <?php echo $isDetail ? 'Entrada del blog' : 'Blog de correos'; ?>
    </title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0, user-scalable=no">
    <!-- Mejora: meta description para SEO -->
    <meta name="description" content="Blog personal de Jose Vicente Carratalá — correos electrónicos mostrados como entradas de blog usando PHP e IMAP">
    <style>
        :root {
            --bg: #f4f4f5;
            --bg-card: #ffffff;
            --border: #e4e4e7;
            --text: #18181b;
            --muted: #71717a;
            --accent: #2563eb;
        }

        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            padding: 0;
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background: var(--bg);
            color: var(--text);
        }

        .layout {
            max-width: 960px;
            margin: 0 auto;
            padding: 2rem 1.5rem 3rem;
        }

        header.site-header {
            margin-bottom: 2rem;
            border-bottom: 1px solid var(--border);
            padding-bottom: 1rem;
            display:flex;
            align-items:center;
            justify-content:space-between;
        }
        .social img{
          width: 35px;
          margin-left: 5px;
          /* Mejora: transicion suave en iconos sociales */
          transition: transform 0.2s ease, opacity 0.2s ease;
        }
        /* Mejora: efecto hover en iconos sociales */
        .social a:hover img{
          transform: scale(1.15);
          opacity: 0.8;
        }

        .site-title {
            font-size: 2rem;
            margin: 0 0 0.25rem;
        }

        .site-subtitle {
            margin: 0;
            color: var(--muted);
            font-size: 0.95rem;
        }

        .back-link {
            display: inline-block;
            margin-bottom: 1.5rem;
            font-size: 0.9rem;
            color: var(--accent);
            text-decoration: none;
        }

        .back-link:hover {
            text-decoration: underline;
        }

        .posts {
            display: grid;
            gap: 1.5rem;
        }

        article.post {
            background: var(--bg-card);
            border-radius: 16px;
            overflow: hidden;
            border: 1px solid var(--border);
            box-shadow: 0 8px 20px rgba(15, 23, 42, 0.06);
            display: flex;
            flex-direction: column;
        }

        .post-hero {
            position: relative;
            max-height: 260px;
            overflow: hidden;
        }

        .post-hero img {
            width: 100%;
            display: block;
            object-fit: cover;
            object-position: center center; /* centrar en overflow */
            transition: transform 0.4s ease;
        }

        article.post:hover .post-hero img {
            transform: scale(1.03);
        }

        .post-content {
            padding: 1.25rem 1.5rem 1.5rem;
        }

        .post-header {
            margin-bottom: 0.75rem;
        }

        .post-title {
            margin: 0 0 0.25rem;
            font-size: 1.25rem;
            line-height: 1.25;
        }

        .post-title a {
            color: var(--text);
            text-decoration: none;
        }

        .post-title a:hover {
            color: var(--accent);
        }

        .post-meta {
            font-size: 0.85rem;
            color: var(--muted);
        }

        .post-meta span + span::before {
            content: "•";
            margin: 0 0.4rem;
        }

        .post-body {
            margin-top: 0.75rem;
            font-size: 0.95rem;
            line-height: 1.6;
        }

        .post-body img {
            max-width: 100%;
            height: auto;
        }

        .read-more {
            margin-top: 0.75rem;
            font-size: 0.9rem;
        }

        .read-more a {
            color: var(--accent);
            text-decoration: none;
            font-weight: 500;
        }

        .read-more a:hover {
            text-decoration: underline;
        }

        .empty {
            margin-top: 2rem;
            text-align: center;
            color: var(--muted);
        }

        @media (max-width: 640px) {
            .layout {
                padding-inline: 1rem;
            }
            /* Mejora: header en columna en movil */
            header.site-header {
                flex-direction: column;
                text-align: center;
                gap: 1rem;
            }
        }

        /* Mejora: footer con creditos */
        footer.site-footer {
            margin-top: 3rem;
            padding-top: 1.5rem;
            border-top: 1px solid var(--border);
            text-align: center;
            color: var(--muted);
            font-size: 0.85rem;
        }
    </style>
</head>
<body>
<div class="layout">
    <header class="site-header">
      <div class="corporativo">
        <h1 class="site-title">
            Jose Vicente Carratala Sanchis
        </h1>
        <p class="site-subtitle">
            Programador, profesor y diseñador en Valencia, España.
        </p>
       </div>
       <div class="social">
          <!-- Mejora: atributos alt descriptivos para accesibilidad -->
          <a href="https://facebook.com/carratala" title="Facebook"><img src="logos/facebook.png" alt="Facebook"></a>
          <a href="https://www.instagram.com/jvcarratala/" title="Instagram"><img src="logos/instagram.png" alt="Instagram"></a>
          <a href="mailto:info@josevicentecarratala.com" title="Email"><img src="logos/email.png" alt="Email"></a>
          <a href="https://github.com/jocarsa" title="GitHub"><img src="logos/github.png" alt="GitHub"></a>
          <a href="https://jocarsa.com" title="Web personal"><img src="logos/home.png" alt="Web personal"></a>
          <a href="https://www.linkedin.com/in/jvcarratala/" title="LinkedIn"><img src="logos/linkedin.png" alt="LinkedIn"></a>
          <a href="https://wa.me/34620891718" title="WhatsApp"><img src="logos/whatsapp.png" alt="WhatsApp"></a>
          <a href="https://www.youtube.com/@VicenteCarratala" title="YouTube"><img src="logos/youtube.png" alt="YouTube"></a>
          
       </div>
    </header>

    <?php if ($isDetail): ?>
        <a href="<?php echo strtok($_SERVER['REQUEST_URI'], '?'); ?>" class="back-link">← Volver al listado</a>
    <?php endif; ?>

    <section class="posts">
        <?php
        if ($emails) {
            if (!$isDetail) {
                // Portada: ordenamos y limitamos
                rsort($emails);
                $emails = array_slice($emails, 0, 15);
            }

            foreach ($emails as $email_number) {
                $overviewList = imap_fetch_overview($inbox, $email_number, 0);
                $overview     = $overviewList[0] ?? null;

                if (!$overview) {
                    continue;
                }

                $subject = isset($overview->subject) ? imap_utf8($overview->subject) : '(Sin asunto)';
                $from    = isset($overview->from)    ? imap_utf8($overview->from)    : '(Desconocido)';
                $date    = isset($overview->date)    ? $overview->date               : '';

                $subject_safe = htmlspecialchars($subject, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
                $from_safe    = htmlspecialchars($from,    ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
                $date_safe    = htmlspecialchars($date,    ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');

                $parts = extractEmailParts($inbox, $email_number);
                $bodyFullHtml = $parts['html'] ?? $parts['text'] ?? '<em>Sin contenido legible.</em>';
                $image        = $parts['image'];

                // En portada mostramos excerpt, en detalle el cuerpo completo
                if ($isDetail) {
                    $bodyToShow = $bodyFullHtml;
                } else {
                    $excerptText = makeExcerpt($bodyFullHtml, EXCERPT_LENGTH);
                    // El excerpt es texto plano; se escapa para HTML
                    $bodyToShow  = '<p>' . htmlspecialchars($excerptText, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8') . '</p>';
                }

                $detailUrl = strtok($_SERVER['REQUEST_URI'], '?') . '?id=' . (int)$email_number;
                ?>
                <article class="post">
                    <?php if ($image): ?>
                        <div class="post-hero">
                            <img src="<?php echo $image['dataUri']; ?>"
                                 alt="<?php echo htmlspecialchars($image['filename'], ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'); ?>">
                        </div>
                    <?php endif; ?>

                    <div class="post-content">
                        <header class="post-header">
                            <h2 class="post-title">
                                <a href="<?php echo $detailUrl; ?>">
                                    <?php echo $subject_safe; ?>
                                </a>
                            </h2>
                            <div class="post-meta">
                                <span>De: <?php echo $from_safe; ?></span>
                                <?php if ($date_safe): ?>
                                    <span><?php echo $date_safe; ?></span>
                                <?php endif; ?>
                            </div>
                        </header>

                        <div class="post-body">
                            <?php echo $bodyToShow; ?>
                        </div>

                        <?php if (!$isDetail): ?>
                            <div class="read-more">
                                <a href="<?php echo $detailUrl; ?>">Leer más →</a>
                            </div>
                        <?php endif; ?>
                    </div>
                </article>
                <?php
                // En vista detalle solo se muestra una entrada
                if ($isDetail) {
                    break;
                }
            }
        } else {
            ?>
            <p class="empty">No se han encontrado correos para mostrar.</p>
            <?php
        }

        imap_close($inbox);
        ?>
    </section>

    <!-- Mejora: footer con informacion del sitio -->
    <footer class="site-footer">
        <p>&copy; 2025 Jose Vicente Carratalá Sanchis &mdash; Blog generado desde bandeja IMAP con PHP</p>
    </footer>
</div>
</body>
</html>

