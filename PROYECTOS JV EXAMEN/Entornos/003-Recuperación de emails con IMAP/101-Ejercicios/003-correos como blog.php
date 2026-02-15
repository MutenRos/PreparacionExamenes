<?php
// ----------------------------------------------------
// CONFIGURACIÓN IMAP
// ----------------------------------------------------
$hostname = '{imap.ionos.es:993/imap/ssl}INBOX'; // Cambia si no usas Gmail
$username = 'python@jocarsa.com';
$password = 'TAME123$';

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

    // Resultado acumulado
    $result = [
        'html'  => null,
        'text'  => null,
        'image' => null,
    ];

    // Mensaje simple (sin multipart)
    if (!isset($structure->parts)) {
        $content = imap_body($imap, $msgno);
        $content = decodePart($content, $structure->encoding ?? 0);

        // Si es texto
        if ($structure->type == 0) {
            $subtype = isset($structure->subtype) ? strtoupper($structure->subtype) : '';
            if ($subtype === 'HTML') {
                $result['html'] = $content;
            } else {
                $result['text'] = nl2br(htmlspecialchars($content, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'));
            }
        }

        // Si fuese una única imagen (no es lo habitual)
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

    // Si es multipart, recorremos recursivamente
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

        // Si tiene subpartes, recursión
        if (isset($part->parts) && count($part->parts) > 0) {
            traverseParts($imap, $msgno, $part, $partNumber, $result);
            continue;
        }

        $type    = $part->type ?? null;   // 0 = text, 5 = image
        $subtype = isset($part->subtype) ? strtoupper($part->subtype) : '';
        $content = imap_fetchbody($imap, $msgno, $partNumber);
        $content = decodePart($content, $part->encoding ?? 0);

        // TEXTO
        if ($type === 0) {
            if ($subtype === 'HTML' && $result['html'] === null) {
                $result['html'] = $content;
            } elseif ($subtype === 'PLAIN' && $result['text'] === null) {
                $result['text'] = nl2br(htmlspecialchars($content, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'));
            }
        }

        // IMAGEN (adjunto o inline)
        if ($type === 5 && $result['image'] === null) {
            // Intentar obtener nombre de archivo
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
// CONEXIÓN IMAP Y LECTURA DE CORREOS
// ----------------------------------------------------
$inbox = @imap_open($hostname, $username, $password);

if (!$inbox) {
    die('Error IMAP: ' . imap_last_error());
}

// Puedes cambiar el criterio a 'UNSEEN', 'FROM "alguien"', etc.
$emails = imap_search($inbox, 'ALL');
?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Blog de correos</title>
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

        .empty {
            margin-top: 2rem;
            text-align: center;
            color: var(--muted);
        }

        @media (max-width: 640px) {
            .layout {
                padding-inline: 1rem;
            }
        }
    </style>
</head>
<body>
<div class="layout">
    <header class="site-header">
        <h1 class="site-title">Blog desde la bandeja de entrada</h1>
        <p class="site-subtitle">
            Cada correo se muestra como si fuera una entrada de blog.
        </p>
    </header>

    <section class="posts">
        <?php
        if ($emails) {
            // Ordenar: más recientes primero
            rsort($emails);

            // Por ejemplo, mostrar solo los 15 primeros
            $emails = array_slice($emails, 0, 15);

            foreach ($emails as $email_number) {
                $overviewList = imap_fetch_overview($inbox, $email_number, 0);
                $overview     = $overviewList[0] ?? null;

                if (!$overview) {
                    continue;
                }

                $subject = isset($overview->subject) ? imap_utf8($overview->subject) : '(Sin asunto)';
                $from    = isset($overview->from)    ? imap_utf8($overview->from)    : '(Desconocido)';
                $date    = isset($overview->date)    ? $overview->date               : '';

                // Sanitizar cabeceras
                $subject_safe = htmlspecialchars($subject, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
                $from_safe    = htmlspecialchars($from,    ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
                $date_safe    = htmlspecialchars($date,    ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');

                // Extraer cuerpo (HTML / texto) e imagen destacada
                $parts   = extractEmailParts($inbox, $email_number);
                $body    = $parts['html'] ?? $parts['text'] ?? '<em>Sin contenido legible.</em>';
                $image   = $parts['image']; // null o array

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
                                <!-- Podrías enlazar a una vista detallada si creas una página por email -->
                                <a href="#email-<?php echo (int)$email_number; ?>">
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

                        <div class="post-body" id="email-<?php echo (int)$email_number; ?>">
                            <?php echo $body; ?>
                        </div>
                    </div>
                </article>
                <?php
            }
        } else {
            ?>
            <p class="empty">No se han encontrado correos para mostrar.</p>
            <?php
        }

        imap_close($inbox);
        ?>
    </section>
</div>
</body>
</html>

