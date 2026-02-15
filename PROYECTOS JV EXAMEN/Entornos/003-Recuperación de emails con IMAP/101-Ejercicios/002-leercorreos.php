<?php
// ----------------------------------------------------
// CONFIGURACIÓN IMAP
// Lectura básica de correos electrónicos usando el protocolo IMAP
// con conexión SSL al puerto 993
// ----------------------------------------------------
$hostname = '{imap.ionos.es:993/imap/ssl}INBOX'; // Cambia esto si no usas Gmail
$username = 'python@jocarsa.com';
$password = 'TAME123$';

// Mejora: cabecera Content-Type para asegurar codificacion UTF-8
header('Content-Type: text/html; charset=utf-8');

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
// FUNCIÓN RECURSIVA: obtener la parte HTML (o texto)
// ----------------------------------------------------
function getHtmlBody($imap, $msgno)
{
    $structure = imap_fetchstructure($imap, $msgno);

    // Correo simple (sin multipart)
    if (!isset($structure->parts)) {
        $body = imap_body($imap, $msgno);
        $body = decodePart($body, $structure->encoding ?? 0);

        // Si el subtipo es HTML lo devolvemos tal cual
        if (isset($structure->subtype) && strtoupper($structure->subtype) === 'HTML') {
            return $body;
        }

        // Si es texto plano, lo convertimos a HTML básico
        return nl2br(htmlspecialchars($body, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'));
    }

    // Correo multipart: buscamos parte HTML
    $htmlBody = null;
    $textBody = null;

    foreach ($structure->parts as $index => $part) {
        $partNumber = $index + 1;

        // Si la parte tiene subpartes (multipart anidado)
        if (isset($part->parts)) {
            // Llamada recursiva: tratamos este subárbol como mensaje
            $subBody = getMultipartBody($imap, $msgno, $part, $partNumber);
            if ($subBody['html'] !== null && $htmlBody === null) {
                $htmlBody = $subBody['html'];
            }
            if ($subBody['text'] !== null && $textBody === null) {
                $textBody = $subBody['text'];
            }
            continue;
        }

        // Solo partes de tipo texto (type 0)
        if ($part->type == 0) {
            $content = imap_fetchbody($imap, $msgno, $partNumber);
            $content = decodePart($content, $part->encoding ?? 0);

            $subtype = isset($part->subtype) ? strtoupper($part->subtype) : '';

            if ($subtype === 'HTML') {
                if ($htmlBody === null) {
                    $htmlBody = $content;
                }
            } elseif ($subtype === 'PLAIN') {
                if ($textBody === null) {
                    $textBody = nl2br(htmlspecialchars($content, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'));
                }
            }
        }
    }

    // Preferimos HTML; si no, texto plano
    if ($htmlBody !== null) {
        return $htmlBody;
    }
    if ($textBody !== null) {
        return $textBody;
    }

    return '<em>Sin contenido legible.</em>';
}

/**
 * Función auxiliar para recorrer partes multipart anidadas.
 */
function getMultipartBody($imap, $msgno, $structure, $prefix)
{
    $htmlBody = null;
    $textBody = null;

    foreach ($structure->parts as $index => $part) {
        $partNumber = $prefix . '.' . ($index + 1);

        if (isset($part->parts)) {
            $sub = getMultipartBody($imap, $msgno, $part, $partNumber);
            if ($sub['html'] !== null && $htmlBody === null) {
                $htmlBody = $sub['html'];
            }
            if ($sub['text'] !== null && $textBody === null) {
                $textBody = $sub['text'];
            }
            continue;
        }

        if ($part->type == 0) {
            $content = imap_fetchbody($imap, $msgno, $partNumber);
            $content = decodePart($content, $part->encoding ?? 0);
            $subtype = isset($part->subtype) ? strtoupper($part->subtype) : '';

            if ($subtype === 'HTML') {
                if ($htmlBody === null) {
                    $htmlBody = $content;
                }
            } elseif ($subtype === 'PLAIN') {
                if ($textBody === null) {
                    $textBody = nl2br(htmlspecialchars($content, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8'));
                }
            }
        }
    }

    return [
        'html' => $htmlBody,
        'text' => $textBody
    ];
}

// ----------------------------------------------------
// CONEXIÓN IMAP Y LECTURA DE CORREOS
// ----------------------------------------------------
$inbox = @imap_open($hostname, $username, $password);

if (!$inbox) {
    die('Error IMAP: ' . imap_last_error());
}

// Aquí puedes cambiar el criterio, por ejemplo: 'UNSEEN', 'FROM "alguien"', etc.
$emails = imap_search($inbox, 'ALL');

?>
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <title>Listado de correos</title>
    <style>
        body {
            font-family: system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
            background: #f5f5f5;
            margin: 0;
            padding: 1.5rem;
        }
        h1 {
            margin-bottom: 1rem;
        }
        article {
            background: #ffffff;
            border-radius: 8px;
            padding: 1rem 1.5rem;
            margin-bottom: 1rem;
            box-shadow: 0 2px 4px rgba(0,0,0,0.08);
        }
        article header {
            border-bottom: 1px solid #e0e0e0;
            margin-bottom: 0.75rem;
            padding-bottom: 0.5rem;
        }
        article h2 {
            margin: 0;
            font-size: 1rem;
        }
        .meta {
            font-size: 0.85rem;
            color: #666;
        }
        .email-body {
            margin-top: 0.5rem;
        }
    </style>
</head>
<body>
    <h1>Correos de la bandeja de entrada</h1>

    <?php
    if ($emails) {
        // Ordenar: más recientes primero
        rsort($emails);

        // Por ejemplo, mostrar solo los 20 primeros
        $emails = array_slice($emails, 0, 20);

        foreach ($emails as $email_number) {
            $overview = imap_fetch_overview($inbox, $email_number, 0)[0] ?? null;

            if (!$overview) {
                continue;
            }

            $subject = isset($overview->subject) ? imap_utf8($overview->subject) : '(Sin asunto)';
            $from    = isset($overview->from)    ? imap_utf8($overview->from)    : '(Desconocido)';
            $date    = isset($overview->date)    ? $overview->date                : '';

            // Sanitizar para HTML en cabeceras
            $subject_safe = htmlspecialchars($subject, ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
            $from_safe    = htmlspecialchars($from,    ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');
            $date_safe    = htmlspecialchars($date,    ENT_QUOTES | ENT_SUBSTITUTE, 'UTF-8');

            // Obtener cuerpo (HTML preferente)
            $bodyHtml = getHtmlBody($inbox, $email_number);
            ?>
            <article>
                <header>
                    <h2><?php echo $subject_safe; ?></h2>
                    <div class="meta">
                        De: <?php echo $from_safe; ?><br>
                        Fecha: <?php echo $date_safe; ?>
                    </div>
                </header>
                <div class="email-body">
                    <?php echo $bodyHtml; ?>
                </div>
            </article>
            <?php
        }
    } else {
        echo '<p>No se han encontrado correos.</p>';
    }

    imap_close($inbox);
    ?>
</body>
</html>

