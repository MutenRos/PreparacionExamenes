<?php
session_start();

// Conexión a la base de datos (una sola vez, al inicio del archivo)
$c = new mysqli("localhost","training_center","training_center","training_center");
if ($c->connect_error) {
  die("Error de conexión: " . $c->connect_error);
}
// Conexión a la base de datos (una sola vez, al inicio del archivo)
$c = new mysqli("localhost","training_center","training_center","training_center");
if ($c->connect_error) {
  die("Error de conexión: " . $c->connect_error);
}

/*-----------------------------------------------------------
  0-bis) Metadatos de columnas de la tabla inscripciones
         (incluye detección de BLOB)
-----------------------------------------------------------*/
$tableColumns = [];
$blobColumns  = [];

$colsRes = $c->query("
  SELECT COLUMN_NAME, DATA_TYPE
  FROM information_schema.columns
  WHERE table_schema='training_center'
    AND table_name='inscripciones'
  ORDER BY ORDINAL_POSITION
");
if ($colsRes) {
  while ($col = $colsRes->fetch_assoc()) {
    $name = $col['COLUMN_NAME'];
    $tableColumns[] = $name;
    $dataType = strtolower($col['DATA_TYPE']);
    if (in_array($dataType, ['blob','tinyblob','mediumblob','longblob'])) {
      $blobColumns[$name] = true;
    }
  }
}

/*-----------------------------------------------------------
  1) Tabla auxiliar para estados CRM (NO toca inscripciones)
-----------------------------------------------------------*/
$c->query("
  CREATE TABLE IF NOT EXISTS crm_estados_inscripciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_registro VARCHAR(255) NOT NULL UNIQUE,
    estado VARCHAR(50) NOT NULL,
    color VARCHAR(20) NOT NULL
  ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
");

/*-----------------------------------------------------------
  2) Estados típicos de CRM (en español) + colores
-----------------------------------------------------------*/
$estadosCRM = [
  'Nuevo'             => '#3498db', // azul
  'Contactado'        => '#9b59b6', // violeta
  'En seguimiento'    => '#f1c40f', // amarillo
  'Cualificado'       => '#2ecc71', // verde
  'No interesado'     => '#95a5a6', // gris
  'Ganado'            => '#27ae60', // verde fuerte
  'Perdido'           => '#e74c3c', // rojo
];

/*-----------------------------------------------------------
  3) Detectar columna PRIMARY KEY de inscripciones
-----------------------------------------------------------*/
$primaryKeyColumn = null;
$pkResult = $c->query("
  SELECT COLUMN_NAME 
  FROM information_schema.columns
  WHERE table_schema = 'training_center'
    AND table_name   = 'inscripciones'
    AND COLUMN_KEY   = 'PRI'
  LIMIT 1;
");
if ($pkResult && $pkResult->num_rows > 0) {
  $primaryKeyColumn = $pkResult->fetch_assoc()['COLUMN_NAME'];
}

/*-----------------------------------------------------------
  4) Detectar columna de email de inscripciones
-----------------------------------------------------------*/
$emailColumn = null;
$emailColResult = $c->query("
  SELECT COLUMN_NAME
  FROM information_schema.columns
  WHERE table_schema='training_center'
    AND table_name='inscripciones'
    AND (
      COLUMN_NAME LIKE '%mail%' OR
      COLUMN_NAME LIKE '%email%' OR
      COLUMN_NAME LIKE '%correo%'
    )
  LIMIT 1;
");
if ($emailColResult && $emailColResult->num_rows > 0) {
  $emailColumn = $emailColResult->fetch_assoc()['COLUMN_NAME'];
}

/*-----------------------------------------------------------
  5) Configuración de correo (SMTP + IMAP)
-----------------------------------------------------------*/
define('CRM_MAIL_USER', 'python@jocarsa.com');
define('CRM_MAIL_PASS', 'TAME123$');
define('CRM_SMTP_HOST', 'smtp.ionos.es');
define('CRM_SMTP_PORT', 587); // STARTTLS
define('CRM_IMAP_MAILBOX', '{imap.ionos.es:993/imap/ssl}INBOX');

// *** carpeta de ENVIADOS (ajústala si IONOS usa otro nombre) ***
define('CRM_IMAP_SENT_MAILBOX', '{imap.ionos.es:993/imap/ssl}Elementos enviados');

/*-----------------------------------------------------------
  6) Función: guardar un mensaje en la carpeta "Sent" por IMAP
-----------------------------------------------------------*/
function crm_append_to_sent($rawMessage) {
  if (!function_exists('imap_open')) {
    return;
  }

  $mailbox  = CRM_IMAP_SENT_MAILBOX;
  $user     = CRM_MAIL_USER;
  $password = CRM_MAIL_PASS;

  $imap = @imap_open($mailbox, $user, $password);
  if (!$imap) {
    // si falla, simplemente no se guarda; no rompemos nada
    return;
  }

  // Fecha formato IMAP
  $date = date('d-M-Y H:i:s O'); // ej. 02-Mar-2025 12:34:56 +0100

  // Marcar como \Seen para que no cuente como no leído
  @imap_append($imap, $mailbox, $rawMessage, "\\Seen", $date);

  imap_close($imap);
}

/*-----------------------------------------------------------
  7) Función: enviar correo via SMTP (con STARTTLS + guardar en Sent)
-----------------------------------------------------------*/
function crm_send_email_smtp($to, $subject, $body, &$errorMsg) {
  $errorMsg = '';
  $smtpHost = CRM_SMTP_HOST;
  $smtpPort = CRM_SMTP_PORT;
  $username = CRM_MAIL_USER;
  $password = CRM_MAIL_PASS;
  $from     = CRM_MAIL_USER;
  $fromName = 'CRM Training Center';

  $socket = @fsockopen($smtpHost, $smtpPort, $errno, $errstr, 30);
  if (!$socket) {
    $errorMsg = "No se pudo conectar al servidor SMTP: $errstr ($errno)";
    return false;
  }

  // Banner inicial
  $resp = fgets($socket, 515);
  if (substr($resp, 0, 3) != '220') {
    $errorMsg = "Respuesta inesperada del servidor SMTP: $resp";
    fclose($socket);
    return false;
  }

  // lector de respuestas multilínea tipo 250-... / 250 ...
  $readMultiline = function($expectedCode) use ($socket, &$errorMsg) {
    $response = '';
    while (($line = fgets($socket, 515)) !== false) {
      $response .= $line;
      if (substr($line, 0, 3) != $expectedCode) {
        $errorMsg = "Respuesta inesperada del servidor SMTP: $line";
        return false;
      }
      if (strlen($line) < 4 || $line[3] != '-') {
        break;
      }
    }
    return $response;
  };

  // comandos de una sola línea
  $sendCmdOneLine = function($cmd, $expectedCode) use ($socket, &$errorMsg) {
    fputs($socket, $cmd);
    $resp = fgets($socket, 515);
    if (substr($resp, 0, 3) != $expectedCode) {
      $errorMsg = "Error SMTP al enviar '$cmd': $resp";
      return false;
    }
    return true;
  };

  // 1) EHLO inicial (sin TLS)
  fputs($socket, "EHLO localhost\r\n");
  $ehloResp = $readMultiline("250");
  if ($ehloResp === false) {
    fclose($socket);
    return false;
  }

  // 2) STARTTLS
  fputs($socket, "STARTTLS\r\n");
  $resp = fgets($socket, 515);
  if (substr($resp, 0, 3) != '220') {
    $errorMsg = "Fallo al iniciar STARTTLS: $resp";
    fclose($socket);
    return false;
  }

  // 3) Activar cifrado TLS
  $cryptoOk = @stream_socket_enable_crypto(
    $socket,
    true,
    STREAM_CRYPTO_METHOD_TLS_CLIENT
  );
  if (!$cryptoOk) {
    $errorMsg = "No se pudo activar el cifrado TLS en el socket SMTP.";
    fclose($socket);
    return false;
  }

  // 4) EHLO otra vez, ya cifrado
  fputs($socket, "EHLO localhost\r\n");
  $ehloResp2 = $readMultiline("250");
  if ($ehloResp2 === false) {
    fclose($socket);
    return false;
  }

  // 5) AUTH LOGIN
  if (!$sendCmdOneLine("AUTH LOGIN\r\n", "334")) {
    fclose($socket);
    return false;
  }

  if (!$sendCmdOneLine(base64_encode($username) . "\r\n", "334")) {
    fclose($socket);
    return false;
  }

  if (!$sendCmdOneLine(base64_encode($password) . "\r\n", "235")) {
    fclose($socket);
    return false;
  }

  // 6) MAIL FROM
  if (!$sendCmdOneLine("MAIL FROM:<$from>\r\n", "250")) {
    fclose($socket);
    return false;
  }

  // 7) RCPT TO
  if (!$sendCmdOneLine("RCPT TO:<$to>\r\n", "250")) {
    fclose($socket);
    return false;
  }

  // 8) DATA
  if (!$sendCmdOneLine("DATA\r\n", "354")) {
    fclose($socket);
    return false;
  }

  // Cabeceras + cuerpo (mensaje completo RFC822)
  $headers  = "From: " . $fromName . " <" . $from . ">\r\n";
  $headers .= "To: <$to>\r\n";
  $headers .= "Subject: " . $subject . "\r\n";
  $headers .= "MIME-Version: 1.0\r\n";
  $headers .= "Content-Type: text/plain; charset=UTF-8\r\n";
  $headers .= "Content-Transfer-Encoding: 8bit\r\n";
  $headers .= "\r\n";

  $rawMessage = $headers . $body;

  $data = $rawMessage . "\r\n.\r\n";

  fputs($socket, $data);
  $resp = fgets($socket, 515);
  if (substr($resp, 0, 3) != '250') {
    $errorMsg = "Error al completar el envío: $resp";
    fclose($socket);
    return false;
  }

  fputs($socket, "QUIT\r\n");
  fclose($socket);

  // *** Guardar una copia en la carpeta "Sent" ***
  crm_append_to_sent($rawMessage);

  return true;
}

/*-----------------------------------------------------------
  8) Función: obtener comunicaciones (INBOX + Sent) para un contacto
-----------------------------------------------------------*/
function crm_fetch_emails_for_contact($contactEmail, $limit = 20) {
  $result = [
    'sent'     => [],
    'received' => [],
    'error'    => null
  ];

  if (!function_exists('imap_open')) {
    $result['error'] = "La extensión IMAP de PHP no está habilitada.";
    return $result;
  }

  $user     = CRM_MAIL_USER;
  $password = CRM_MAIL_PASS;
  $ourAddress = strtolower(CRM_MAIL_USER);
  $safeEmail  = str_replace('"', '\"', $contactEmail);

  // helper para escanear una carpeta (INBOX o Sent)
  $scanMailbox = function($mailbox) use (&$result, $user, $password, $safeEmail, $ourAddress, $limit) {
    $inbox = @imap_open($mailbox, $user, $password);
    if (!$inbox) {
      if ($result['error'] === null) {
        $result['error'] = imap_last_error();
      }
      return;
    }

    $emailsIds = [];

    // FROM contacto
    $fromIds = imap_search($inbox, 'FROM "' . $safeEmail . '"');
    if ($fromIds !== false) {
      $emailsIds = array_merge($emailsIds, $fromIds);
    }

    // TO contacto
    $toIds = imap_search($inbox, 'TO "' . $safeEmail . '"');
    if ($toIds !== false) {
      $emailsIds = array_merge($emailsIds, $toIds);
    }

    if (!empty($emailsIds)) {
      $emailsIds = array_values(array_unique($emailsIds));
      rsort($emailsIds);
      // opcional: podríamos limitar aquí por carpeta; lo dejamos completo
    } else {
      imap_close($inbox);
      return;
    }

    foreach ($emailsIds as $num) {
      $overview = imap_fetch_overview($inbox, $num, 0);
      if (!$overview) continue;
      $ov = $overview[0];

      $header = imap_headerinfo($inbox, $num);

      $from = isset($header->fromaddress) ? $header->fromaddress : ($ov->from ?? '');
      $to   = isset($header->toaddress)   ? $header->toaddress   : ($ov->to   ?? '');

      $subject = isset($ov->subject) ? imap_utf8($ov->subject) : '';
      $date    = isset($ov->date)    ? $ov->date : '';

      $body = imap_fetchbody($inbox, $num, 1);
      if (!$body) $body = '';
      $body = imap_qprint($body);
      $snippet = trim($body);
      if (function_exists('mb_substr')) {
        $snippet = mb_substr($snippet, 0, 200);
      } else {
        $snippet = substr($snippet, 0, 200);
      }

      $entry = [
        'subject' => $subject,
        'date'    => $date,
        'from'    => $from,
        'to'      => $to,
        'snippet' => $snippet
      ];

      $fromLower = strtolower($from);
      if (strpos($fromLower, $ourAddress) !== false) {
        $result['sent'][] = $entry;
      } else {
        $result['received'][] = $entry;
      }
    }

    imap_close($inbox);
  };

  // Escanear INBOX y Sent
  $scanMailbox(CRM_IMAP_MAILBOX);
  $scanMailbox(CRM_IMAP_SENT_MAILBOX);

  // Ordenar por fecha dentro de enviados y recibidos (descendente)
  $sortByDateDesc = function(&$arr) {
    usort($arr, function($a, $b) {
      $da = strtotime($a['date'] ?? '1970-01-01');
      $db = strtotime($b['date'] ?? '1970-01-01');
      return $db <=> $da;
    });
  };

  $sortByDateDesc($result['sent']);
  $sortByDateDesc($result['received']);

  // Aplicar límite por tipo
  if ($limit > 0) {
    $result['sent']     = array_slice($result['sent'], 0, $limit);
    $result['received'] = array_slice($result['received'], 0, $limit);
  }

  return $result;
}

/*-----------------------------------------------------------
  9) LOGIN / LOGOUT
-----------------------------------------------------------*/
$login_error = "";

if (isset($_GET['logout'])) {
  session_destroy();
  header("Location: " . $_SERVER['PHP_SELF']);
  exit;
}

if (isset($_POST['action']) && $_POST['action'] === 'login') {
  $usuario  = $_POST['usuario']  ?? '';
  $password = $_POST['password'] ?? '';

  if ($usuario === 'jocarsa' && $password === 'jocarsa') {
    $_SESSION['admin_logged'] = true;
    header("Location: " . $_SERVER['PHP_SELF']);
    exit;
  } else {
    $login_error = "Usuario o contraseña incorrectos.";
  }
}

$loggedIn = isset($_SESSION['admin_logged']) && $_SESSION['admin_logged'] === true;

/*-----------------------------------------------------------
  10) Actualización de estado CRM
-----------------------------------------------------------*/
if (
  $loggedIn &&
  isset($_POST['action']) &&
  $_POST['action'] === 'update_estado'
) {
  $id_registro = $_POST['id_registro'] ?? null;
  $estado      = $_POST['estado']      ?? null;

  if ($id_registro !== null && isset($estadosCRM[$estado])) {
    $color = $estadosCRM[$estado];

    $stmt = $c->prepare("
      INSERT INTO crm_estados_inscripciones (id_registro, estado, color)
      VALUES (?, ?, ?)
      ON DUPLICATE KEY UPDATE
        estado = VALUES(estado),
        color  = VALUES(color)
    ");
    if ($stmt) {
      $stmt->bind_param("sss", $id_registro, $estado, $color);
      $stmt->execute();
      $stmt->close();
    }
  }
}

/*-----------------------------------------------------------
  11) Envío de email desde el informe
-----------------------------------------------------------*/
$emailSendMessage = "";

if (
  $loggedIn &&
  isset($_POST['action']) &&
  $_POST['action'] === 'send_email'
) {
  $to      = $_POST['to']      ?? '';
  $subject = $_POST['subject'] ?? '';
  $body    = $_POST['body']    ?? '';

  if ($to && $subject && $body) {
    $errorMsg = '';
    $ok = crm_send_email_smtp($to, $subject, $body, $errorMsg);
    if ($ok) {
      $emailSendMessage = "Mensaje enviado correctamente.";
    } else {
      $emailSendMessage = "Error al enviar el mensaje: " . htmlspecialchars($errorMsg, ENT_QUOTES, 'UTF-8');
    }
  } else {
    $emailSendMessage = "Por favor, rellena todos los campos del mensaje.";
  }
}

/*-----------------------------------------------------------
  12) Estados actuales (para la tabla)
-----------------------------------------------------------*/
$estadosActuales = [];
if ($loggedIn) {
  $resEstados = $c->query("SELECT id_registro, estado, color FROM crm_estados_inscripciones");
  if ($resEstados) {
    while ($row = $resEstados->fetch_assoc()) {
      $estadosActuales[$row['id_registro']] = $row;
    }
  }
}

/*-----------------------------------------------------------
  13) Mapa de correos NO LEÍDOS por contacto (para la tabla)
-----------------------------------------------------------*/
// *** nueva funcionalidad: marcar si hay emails sin leer de cada contacto ***
$unreadByEmail = [];
if ($loggedIn && $emailColumn !== null && function_exists('imap_open')) {
  $mailbox  = CRM_IMAP_MAILBOX; // INBOX
  $user     = CRM_MAIL_USER;
  $password = CRM_MAIL_PASS;

  $inbox = @imap_open($mailbox, $user, $password);
  if ($inbox) {
    $unseenIds = imap_search($inbox, 'UNSEEN');
    if ($unseenIds !== false) {
      foreach ($unseenIds as $num) {
        $header = imap_headerinfo($inbox, $num);
        if (!empty($header->from)) {
          // from es un array de objetos (mailbox + host)
          foreach ($header->from as $fromObj) {
            $fromEmail = strtolower(trim($fromObj->mailbox . '@' . $fromObj->host));
            if ($fromEmail !== '' && $fromEmail !== strtolower(CRM_MAIL_USER)) {
              $unreadByEmail[$fromEmail] = true;
            }
          }
        }
      }
    }
    imap_close($inbox);
  }
}

/*-----------------------------------------------------------
  14) ID de informe (vista detalle)
-----------------------------------------------------------*/
$viewId = null;
if ($loggedIn && isset($_GET['view'])) {
  $viewId = $_GET['view'];
}

?>
<!doctype html>
<html lang="es">
  <head>
    <title>Panel de administración</title>
    <meta charset="utf-8">
    <style>
      :root{
        --primary: crimson;
        --primary-light: #ff8fa0;
        --bg: #f2f2f2;
        --text: #333;
        --border: #ddd;
      }

      *{
        box-sizing:border-box;
        margin:0;
        padding:0;
      }

      html, body{
        height:100%;
        font-family: "Segoe UI", sans-serif;
        color: var(--text);
        background: var(--bg);
      }

      body{
        display:flex;
        align-items:stretch;
      }

      /*---------------- LOGIN ----------------*/
      .login-wrapper{
        width:100%;
        display:flex;
        justify-content:center;
        align-items:center;
        padding:40px;
      }
      .login-card{
        background:white;
        padding:30px 40px;
        width:360px;
        border-radius:10px;
        box-shadow:0 4px 15px rgba(0,0,0,0.1);
        border-top:8px solid var(--primary);
      }
      .login-card h2{
        margin-bottom:20px;
        color:var(--primary);
        font-size:1.4em;
      }
      .login-card .form-group{
        margin-bottom:15px;
        display:flex;
        flex-direction:column;
        gap:6px;
      }
      .login-card label{
        font-size:0.95em;
        font-weight:600;
        color:var(--primary);
      }
      .login-card input[type="text"],
      .login-card input[type="password"]{
        padding:10px 12px;
        border-radius:6px;
        border:1px solid var(--border);
        font-size:1em;
      }
      .login-card input[type="submit"]{
        margin-top:10px;
        width:100%;
        padding:12px;
        border:none;
        border-radius:6px;
        background:var(--primary);
        color:white;
        font-size:1em;
        cursor:pointer;
      }
      .login-error{
        margin-bottom:10px;
        padding:8px 10px;
        border-radius:6px;
        background:#ffe6e6;
        border:1px solid #ffb3b3;
        font-size:0.9em;
        color:#b30000;
      }

      /*---------------- LAYOUT ADMIN ----------------*/
      nav{
        width:240px;
        background: var(--primary);
        padding:20px;
        display:flex;
        flex-direction:column;
        gap:10px;
        box-shadow: 4px 0 12px rgba(0,0,0,0.1);
      }

      nav h2{
        color:white;
        margin-bottom:15px;
        font-size:1.1em;
        font-weight:700;
      }

      nav button{
        background:white;
        border:none;
        padding:10px 14px;
        border-radius:999px;
        cursor:pointer;
        font-size:0.95em;
        text-align:left;
        transition: transform 0.15s, box-shadow 0.15s, background 0.15s;
      }

      nav button:hover{
        transform: translateY(-1px);
        box-shadow: 0 2px 6px rgba(0,0,0,0.15);
        background:#fff5f7;
      }

      main{
        flex:1;
        padding:30px 40px;
        display:flex;
        flex-direction:column;
        gap:15px;
      }

      header{
        display:flex;
        justify-content:space-between;
        align-items:center;
        margin-bottom:10px;
      }

      header h1{
        font-size:1.4em;
        color:var(--primary);
      }

      .user-actions{
        display:flex;
        gap:10px;
        align-items:center;
        font-size:0.9em;
      }
      .logout-link{
        padding:6px 10px;
        border-radius:999px;
        border:1px solid var(--primary-light);
        color:var(--primary);
        text-decoration:none;
        font-size:0.85em;
        background:white;
      }
      .back-link{
        padding:6px 10px;
        border-radius:999px;
        border:1px solid var(--border);
        color:#555;
        text-decoration:none;
        font-size:0.8em;
        background:white;
        margin-right:10px;
      }

      .table-card,
      .detail-card{
        background:white;
        border-radius:10px;
        padding:20px 24px;
        box-shadow:0 4px 15px rgba(0,0,0,0.08);
        border-top:8px solid var(--primary);
      }

      .table-card h3,
      .detail-card h3{
        margin-bottom:10px;
        font-size:1.1em;
        color:var(--primary);
      }

      .table-card p.description,
      .detail-card p.description{
        margin-bottom:10px;
        font-size:0.9em;
        color:#666;
      }

      table{
        width:100%;
        border-collapse:collapse;
        font-size:0.9em;
      }

      thead th{
        text-align:left;
        padding:10px 8px;
        border-bottom:2px solid var(--primary-light);
        color:var(--primary);
        font-weight:600;
      }

      tbody td{
        padding:8px 8px;
        border-bottom:1px solid var(--border);
        vertical-align:middle;
      }

      tbody tr:nth-child(even){
        background:#fafafa;
      }

      tbody tr:hover{
        background:#ffeef2;
      }

      .estado-pill{
        display:inline-block;
        padding:4px 10px;
        border-radius:999px;
        border:1px solid var(--border);
        font-size:0.8em;
        background:#f9f9f9;
      }
      .estado-pill--vacio{
        color:#999;
        border-style:dashed;
      }

      .form-estado{
        display:flex;
        gap:6px;
        align-items:center;
      }
      .form-estado select{
        padding:4px 6px;
        border-radius:4px;
        border:1px solid var(--border);
        font-size:0.85em;
      }
      .btn-estado{
        padding:4px 8px;
        border-radius:4px;
        border:none;
        background:var(--primary);
        color:white;
        font-size:0.8em;
        cursor:pointer;
      }

      .btn-informe{
        padding:4px 8px;
        border-radius:4px;
        border:none;
        background:#34495e;
        color:white;
        font-size:0.8em;
        cursor:pointer;
        text-decoration:none;
        display:inline-block;
      }

      .badge-unread{
        display:inline-flex;
        align-items:center;
        justify-content:center;
        min-width:22px;
        height:22px;
        border-radius:999px;
        background:#2ecc71;
        color:white;
        font-size:0.75em;
        font-weight:bold;
      }
      .badge-unread::before{
        content:"✉";
        margin-right:3px;
      }
      .badge-none{
        font-size:0.75em;
        color:#aaa;
      }

      /* Detalle */
      .detail-row-table{
        width:100%;
        border-collapse:collapse;
        margin-bottom:20px;
      }
      .detail-row-table th,
      .detail-row-table td{
        padding:6px 8px;
        border-bottom:1px solid var(--border);
        text-align:left;
      }
      .detail-row-table th{
        width:30%;
        color:var(--primary);
      }

      .email-section{
        margin-top:20px;
        display:grid;
        grid-template-columns:1.2fr 1.8fr;
        gap:20px;
      }
      .email-form-card,
      .email-log-card{
        background:#fafafa;
        border-radius:8px;
        padding:15px 18px;
        border:1px solid #e5e5e5;
      }
      .email-form-card h4,
      .email-log-card h4{
        margin-bottom:8px;
        color:#444;
      }
      .email-form-card .form-group{
        margin-bottom:10px;
        display:flex;
        flex-direction:column;
        gap:4px;
      }
      .email-form-card label{
        font-size:0.85em;
        font-weight:600;
      }
      .email-form-card input[type="text"],
      .email-form-card textarea{
        padding:8px 10px;
        border-radius:4px;
        border:1px solid var(--border);
        font-size:0.9em;
        resize:vertical;
      }
      .email-form-card textarea{
        min-height:120px;
      }
      .email-form-card input[type="submit"]{
        margin-top:8px;
        padding:8px 12px;
        border:none;
        border-radius:4px;
        background:var(--primary);
        color:white;
        font-size:0.9em;
        cursor:pointer;
      }
      .email-status-msg{
        margin-bottom:10px;
        padding:6px 8px;
        border-radius:6px;
        font-size:0.85em;
      }
      .email-status-ok{
        background:#e7f7ec;
        border:1px solid #9dd7b1;
        color:#217346;
      }
      .email-status-error{
        background:#ffe6e6;
        border:1px solid #ffb3b3;
        color:#b30000;
      }

      .mail-list{
        max-height:280px;
        overflow:auto;
        font-size:0.86em;
      }
      .mail-item{
        padding:8px 0;
        border-bottom:1px solid #e3e3e3;
      }
      .mail-item:last-child{
        border-bottom:none;
      }
      .mail-item strong{
        color:#333;
      }
      .mail-meta{
        font-size:0.8em;
        color:#777;
        margin-bottom:2px;
      }
      .mail-snippet{
        font-size:0.85em;
        color:#555;
      }

      @media (max-width: 900px){
        body{
          flex-direction:column;
        }
        nav{
          width:100%;
          flex-direction:row;
          flex-wrap:wrap;
          box-shadow:none;
        }
        nav h2{
          width:100%;
        }
        main{
          padding:20px;
        }
        .email-section{
          grid-template-columns:1fr;
        }
      }
      .thumb-image{
  max-width:60px;
  max-height:60px;
  border-radius:4px;
  cursor:zoom-in;
  object-fit:cover;
  box-shadow:0 0 0 1px rgba(0,0,0,0.1);
}

/* Modal de imagen */
.image-modal{
  position:fixed;
  inset:0;
  display:none;
  align-items:center;
  justify-content:center;
  z-index:9999;
}
.image-modal.is-visible{
  display:flex;
}
.image-modal__backdrop{
  position:absolute;
  inset:0;
  background:rgba(0,0,0,0.6);
}
.image-modal__content{
  position:relative;
  max-width:90%;
  max-height:90%;
  padding:10px;
  background:#fff;
  border-radius:8px;
  box-shadow:0 8px 24px rgba(0,0,0,0.4);
}
.image-modal__content img{
  max-width:100%;
  max-height:80vh;
  display:block;
}
.filters-row input{
  border:1px solid lightgray;
  padding:5px;
  width:100%;
}
    </style>
  </head>
  <body>

  <?php if (!$loggedIn): ?>

    <!-- ------------------ VISTA LOGIN ------------------ -->
    <div class="login-wrapper">
      <form method="post" class="login-card">
        <h2>Acceso al panel</h2>

        <?php if ($login_error !== ""): ?>
          <div class="login-error">
            <?= htmlspecialchars($login_error, ENT_QUOTES, 'UTF-8'); ?>
          </div>
        <?php endif; ?>

        <div class="form-group">
          <label for="usuario">Usuario</label>
          <input type="text" name="usuario" id="usuario" autocomplete="username">
        </div>

        <div class="form-group">
          <label for="password">Contraseña</label>
          <input type="password" name="password" id="password" autocomplete="current-password">
        </div>

        <input type="hidden" name="action" value="login">
        <input type="submit" value="Entrar">
      </form>
    </div>

  <?php else: ?>

    <!-- ------------------ PANEL ADMIN ------------------ -->
    <nav>
      <h2>Menú</h2>
      <button>Enlace 1</button>
      <button>Enlace 2</button>
      <button>Enlace 3</button>
    </nav>
    <main>
      <?php
        $title = $viewId ? "Informe de inscripción" : "Listado de inscripciones";
      ?>
      <header>
        <div style="display:flex; align-items:center; gap:8px;">
          <?php if ($viewId): ?>
            <a href="<?= htmlspecialchars($_SERVER['PHP_SELF'], ENT_QUOTES, 'UTF-8'); ?>" class="back-link">← Volver al listado</a>
          <?php endif; ?>
          <h1><?= htmlspecialchars($title, ENT_QUOTES, 'UTF-8'); ?></h1>
        </div>
        <div class="user-actions">
          <span>Conectado como <strong>jocarsa</strong></span>
          <a class="logout-link" href="?logout=1">Cerrar sesión</a>
        </div>
      </header>

      <?php if ($viewId && $primaryKeyColumn !== null): ?>

        <?php
          // Cargar la fila concreta
          $filaDetalle = null;
          $stmt = $c->prepare("SELECT * FROM inscripciones WHERE $primaryKeyColumn = ? LIMIT 1");
          if ($stmt) {
            $stmt->bind_param("s", $viewId);
            $stmt->execute();
            $result = $stmt->get_result();
            $filaDetalle = $result->fetch_assoc();
            $stmt->close();
          }
        ?>

        <?php if ($filaDetalle): ?>
          <?php
            // Determinar email de contacto (si existe columna de email)
            $contactEmail = null;
            if ($emailColumn !== null && isset($filaDetalle[$emailColumn])) {
              $contactEmail = $filaDetalle[$emailColumn];
            }

            // Obtener comunicaciones por email si tenemos correo
            $commReport = null;
            if ($contactEmail) {
              $commReport = crm_fetch_emails_for_contact($contactEmail, 20);
            }
          ?>

          <section class="detail-card">
            <h3>Datos de la inscripción (ID: <?= htmlspecialchars($viewId, ENT_QUOTES, 'UTF-8'); ?>)</h3>
            <p class="description">
              Detalle completo del registro seleccionado en la tabla
              <strong>inscripciones</strong>, junto con el historial de comunicaciones
              por correo electrónico asociado al contacto.
            </p>

            <table class="detail-row-table">
  <tbody>
    <?php foreach ($filaDetalle as $campo => $valor): ?>
      <tr>
        <th><?= htmlspecialchars($campo, ENT_QUOTES, 'UTF-8'); ?></th>
        <td>
          <?php if (isset($blobColumns[$campo]) && $valor !== null && $valor !== ''): ?>
            <?php
              $mime = 'image/jpeg';
              if (strpos($valor, "\x89PNG") === 0) {
                $mime = 'image/png';
              } elseif (strpos($valor, "GIF8") === 0) {
                $mime = 'image/gif';
              }
              $b64 = base64_encode($valor);
              $src = 'data:'.$mime.';base64,'.$b64;
            ?>
            <img src="<?= $src; ?>"
                 data-full="<?= $src; ?>"
                 class="thumb-image"
                 style="max-width:120px; max-height:120px;"
                 alt="Documento">
          <?php else: ?>
            <?= htmlspecialchars((string)$valor, ENT_QUOTES, 'UTF-8'); ?>
          <?php endif; ?>
        </td>
      </tr>
    <?php endforeach; ?>
  </tbody>
</table>


            <div class="email-section">
              <div class="email-form-card">
                <h4>Enviar mensaje al contacto</h4>

                <?php if ($emailSendMessage): ?>
                  <div class="email-status-msg <?= (strpos($emailSendMessage, 'correctamente') !== false) ? 'email-status-ok' : 'email-status-error'; ?>">
                    <?= $emailSendMessage; ?>
                  </div>
                <?php endif; ?>

                <?php if ($contactEmail): ?>
                  <p style="font-size:0.85em; margin-bottom:8px;">
                    Correo del contacto:
                    <strong><?= htmlspecialchars($contactEmail, ENT_QUOTES, 'UTF-8'); ?></strong><br>
                    Remitente usado: <code><?= htmlspecialchars(CRM_MAIL_USER, ENT_QUOTES, 'UTF-8'); ?></code>
                  </p>

                  <form method="post" action="?view=<?= urlencode($viewId); ?>">
                    <div class="form-group">
                      <label for="subject">Asunto</label>
                      <input type="text" id="subject" name="subject">
                    </div>
                    <div class="form-group">
                      <label for="body">Mensaje</label>
                      <textarea id="body" name="body"></textarea>
                    </div>
                    <input type="hidden" name="to" value="<?= htmlspecialchars($contactEmail, ENT_QUOTES, 'UTF-8'); ?>">
                    <input type="hidden" name="action" value="send_email">
                    <input type="submit" value="Enviar mensaje">
                  </form>
                <?php else: ?>
                  <p style="font-size:0.85em; color:#b30000;">
                    No se ha detectado ninguna columna de email para este registro.  
                    El envío de correos no está disponible.
                  </p>
                <?php endif; ?>
              </div>

              <div class="email-log-card">
                <h4>Comunicaciones por correo</h4>

                <?php if (!$contactEmail): ?>
                  <p style="font-size:0.85em; color:#555;">
                    No hay correo electrónico asociado a este registro.<br>
                    Por tanto, no se puede generar el informe de comunicaciones.
                  </p>
                <?php else: ?>
                  <?php if ($commReport && $commReport['error']): ?>
                    <p style="font-size:0.85em; color:#b30000;">
                      Error al acceder al buzón IMAP:
                      <?= htmlspecialchars($commReport['error'], ENT_QUOTES, 'UTF-8'); ?>
                    </p>
                  <?php else: ?>
                    <div class="mail-list">
                      <?php
                        $sent     = $commReport ? $commReport['sent']     : [];
                        $received = $commReport ? $commReport['received'] : [];
                      ?>

                      <p class="mail-meta">
                        Mensajes enviados: <?= count($sent); ?> |
                        Mensajes recibidos: <?= count($received); ?>
                      </p>

                      <?php if (empty($sent) && empty($received)): ?>
                        <p style="font-size:0.85em; color:#555;">
                          No se han encontrado mensajes relacionados con
                          <strong><?= htmlspecialchars($contactEmail, ENT_QUOTES, 'UTF-8'); ?></strong>.
                        </p>
                      <?php else: ?>

                        <?php if (!empty($sent)): ?>
                          <p style="margin-top:8px; font-weight:bold; font-size:0.9em;">Enviados (<?= count($sent); ?>)</p>
                          <?php foreach ($sent as $mail): ?>
                            <div class="mail-item">
                              <div class="mail-meta">
                                <strong>Asunto:</strong> <?= htmlspecialchars($mail['subject'], ENT_QUOTES, 'UTF-8'); ?><br>
                                <strong>Fecha:</strong> <?= htmlspecialchars($mail['date'], ENT_QUOTES, 'UTF-8'); ?><br>
                                <strong>De:</strong> <?= htmlspecialchars($mail['from'], ENT_QUOTES, 'UTF-8'); ?><br>
                                <strong>Para:</strong> <?= htmlspecialchars($mail['to'], ENT_QUOTES, 'UTF-8'); ?>
                              </div>
                              <div class="mail-snippet">
                                <?= nl2br(htmlspecialchars($mail['snippet'], ENT_QUOTES, 'UTF-8')); ?>
                              </div>
                            </div>
                          <?php endforeach; ?>
                        <?php endif; ?>

                        <?php if (!empty($received)): ?>
                          <p style="margin-top:10px; font-weight:bold; font-size:0.9em;">Recibidos (<?= count($received); ?>)</p>
                          <?php foreach ($received as $mail): ?>
                            <div class="mail-item">
                              <div class="mail-meta">
                                <strong>Asunto:</strong> <?= htmlspecialchars($mail['subject'], ENT_QUOTES, 'UTF-8'); ?><br>
                                <strong>Fecha:</strong> <?= htmlspecialchars($mail['date'], ENT_QUOTES, 'UTF-8'); ?><br>
                                <strong>De:</strong> <?= htmlspecialchars($mail['from'], ENT_QUOTES, 'UTF-8'); ?><br>
                                <strong>Para:</strong> <?= htmlspecialchars($mail['to'], ENT_QUOTES, 'UTF-8'); ?>
                              </div>
                              <div class="mail-snippet">
                                <?= nl2br(htmlspecialchars($mail['snippet'], ENT_QUOTES, 'UTF-8')); ?>
                              </div>
                            </div>
                          <?php endforeach; ?>
                        <?php endif; ?>

                      <?php endif; ?>
                    </div>
                  <?php endif; ?>
                <?php endif; ?>
              </div>
            </div>
          </section>
        <?php else: ?>
          <section class="detail-card">
            <h3>Registro no encontrado</h3>
            <p class="description">
              No se ha podido localizar la inscripción con identificador
              <strong><?= htmlspecialchars($viewId, ENT_QUOTES, 'UTF-8'); ?></strong>.
            </p>
          </section>
        <?php endif; ?>

      <?php else: ?>

        <!-- -------- LISTADO GENERAL DE INSCRIPCIONES -------- -->
        <section class="table-card">
          <h3>Tabla: inscripciones</h3>
          <p class="description">
            Registros actuales en la tabla <strong>inscripciones</strong> de la base de datos
            <strong>training_center</strong>. Puede asignar un estado CRM a cada registro,
            ver si hay correos nuevos sin leer y acceder a un informe detallado.
          </p>

         <table id="inscripciones-table">
  <thead>
    <tr>
      <?php
        // Cabeceras de las columnas originales
        foreach ($tableColumns as $colName) {
          echo '<th>'.htmlspecialchars($colName, ENT_QUOTES, 'UTF-8').'</th>';
        }

        // Columna Emails nuevos + Estado CRM + Acciones
        echo '<th>Emails nuevos</th>';
        echo '<th>Estado CRM</th>';
        echo '<th>Acciones</th>';
      ?>
    </tr>
    <tr class="filters-row">
      <?php
        $filterColsCount = count($tableColumns) + 3; // Emails nuevos + Estado CRM + Acciones
        for ($i = 0; $i < $filterColsCount; $i++) {
          echo '<th><input type="text" class="column-filter" placeholder="Filtrar..."></th>';
        }
      ?>
    </tr>
  </thead>
            <tbody>
              <?php
                $r = $c->query("SELECT * FROM inscripciones;");

                while($f = $r->fetch_assoc()) {
                  // ID del registro basado en la columna PK detectada (si existe)
                  $idRegistro = null;
                  if ($primaryKeyColumn !== null && isset($f[$primaryKeyColumn])) {
                    $idRegistro = (string)$f[$primaryKeyColumn];
                  }

                  // Normalizar email de este registro, si existe
                  $rowEmailNorm = null;
                  if ($emailColumn !== null && isset($f[$emailColumn]) && $f[$emailColumn] !== '') {
                    $rowEmailNorm = strtolower(trim($f[$emailColumn]));
                  }

                    echo '<tr>';

  // Mostrar todas las columnas originales (incluyendo BLOB como imagen)
  foreach($f as $clave=>$valor){
    // Si es columna BLOB, intentamos mostrar miniatura
    if (isset($blobColumns[$clave]) && $valor !== null && $valor !== '') {

      // Detección simple del tipo de imagen
      $mime = 'image/jpeg';
      if (strpos($valor, "\x89PNG") === 0) {
        $mime = 'image/png';
      } elseif (strpos($valor, "GIF8") === 0) {
        $mime = 'image/gif';
      }

      $b64 = base64_encode($valor);
      $src = 'data:'.$mime.';base64,'.$b64;

      // data-sort="imagen" para que el ordenado tenga un valor textual
      echo '<td data-sort="imagen">';
      echo '<img src="'.$src.'" data-full="'.$src.'" class="thumb-image" alt="Documento">';
      echo '</td>';
    } else {
      echo '<td>'.htmlspecialchars((string)$valor, ENT_QUOTES, 'UTF-8').'</td>';
    }
  }


                  // *** Columna Emails nuevos ***
                  echo '<td>';
                  if ($rowEmailNorm && isset($unreadByEmail[$rowEmailNorm])) {
                    echo '<span class="badge-unread" title="Nuevo(s) email(s) sin leer de este contacto.">!</span>';
                  } else {
                    echo '<span class="badge-none">—</span>';
                  }
                  echo '</td>';

                  // Columna "Estado CRM" (pastilla de color)
                  echo '<td>';
                  if ($idRegistro !== null && isset($estadosActuales[$idRegistro])) {
                    $estadoRow = $estadosActuales[$idRegistro];
                    $estadoTxt = htmlspecialchars($estadoRow['estado'], ENT_QUOTES, 'UTF-8');
                    $colorTxt  = htmlspecialchars($estadoRow['color'],  ENT_QUOTES, 'UTF-8');

                    echo '<span class="estado-pill" style="background:'.$colorTxt.'20; border-color:'.$colorTxt.'; color:'.$colorTxt.';">';
                    echo $estadoTxt;
                    echo '</span>';
                  } else {
                    echo '<span class="estado-pill estado-pill--vacio">Sin estado</span>';
                  }
                  echo '</td>';

                  // Columna "Acciones" (selector estado + botón + informe)
                  echo '<td>';
                  if ($idRegistro !== null) {
                    // Formulario de estado
                    echo '<form method="post" class="form-estado" style="margin-bottom:4px;">';
                    echo '<input type="hidden" name="action" value="update_estado">';
                    echo '<input type="hidden" name="id_registro" value="'.htmlspecialchars($idRegistro, ENT_QUOTES, 'UTF-8').'">';
                    echo '<select name="estado">';
                    foreach ($estadosCRM as $nombreEstado => $colorEstado) {
                      $selected = (
                        $idRegistro !== null &&
                        isset($estadosActuales[$idRegistro]) &&
                        $estadosActuales[$idRegistro]['estado'] === $nombreEstado
                      ) ? ' selected' : '';
                      echo '<option value="'.htmlspecialchars($nombreEstado, ENT_QUOTES, 'UTF-8').'"'.$selected.'>';
                      echo htmlspecialchars($nombreEstado, ENT_QUOTES, 'UTF-8');
                      echo '</option>';
                    }
                    echo '</select>';
                    echo '<button type="submit" class="btn-estado">Guardar</button>';
                    echo '</form>';

                    // Enlace a informe
                    $urlInforme = htmlspecialchars($_SERVER['PHP_SELF'], ENT_QUOTES, 'UTF-8') . '?view=' . urlencode($idRegistro);
                    echo '<a class="btn-informe" href="'.$urlInforme.'">Informe</a>';
                  }
                  echo '</td>';

                  echo '</tr>';
                }
              ?>
            </tbody>
          </table>
        </section>

      <?php endif; ?>

    </main>

  <?php endif; ?>
<div id="image-modal" class="image-modal">
  <div class="image-modal__backdrop"></div>
  <div class="image-modal__content">
    <img id="image-modal-img" src="" alt="Documento">
  </div>
</div>
<script>
document.addEventListener('DOMContentLoaded', function() {
  /*---------------- MODAL DE IMAGEN ----------------*/
  const modal    = document.getElementById('image-modal');
  const modalImg = document.getElementById('image-modal-img');

  if (modal && modalImg) {
    // Abrir modal al hacer clic en una miniatura
    document.body.addEventListener('click', function(e) {
      const thumb = e.target.closest('.thumb-image');
      if (thumb) {
        const src = thumb.getAttribute('data-full') || thumb.getAttribute('src');
        if (src) {
          modalImg.src = src;
          modal.classList.add('is-visible');
        }
      }
    });

    // Cerrar modal al hacer clic en fondo
    modal.addEventListener('click', function(e) {
      if (e.target === modal || e.target.classList.contains('image-modal__backdrop')) {
        modal.classList.remove('is-visible');
        modalImg.src = '';
      }
    });

    // Cerrar con Escape
    document.addEventListener('keydown', function(e) {
      if (e.key === 'Escape' && modal.classList.contains('is-visible')) {
        modal.classList.remove('is-visible');
        modalImg.src = '';
      }
    });
  }

  /*---------------- TABLA: ORDENACIÓN + FILTROS ----------------*/
  const table = document.getElementById('inscripciones-table');
  if (table && table.tBodies.length > 0) {
    const tbody = table.tBodies[0];

    // Obtener texto base para orden y filtro
    const getCellText = (row, idx) => {
      const cell = row.cells[idx];
      if (!cell) return '';
      const dataSort = cell.getAttribute('data-sort');
      if (dataSort !== null) {
        return dataSort.toLowerCase();
      }
      return (cell.textContent || '').trim().toLowerCase();
    };

    /*--- Ordenación al hacer clic en cabeceras ---*/
    const headerRow   = table.querySelector('thead tr:first-child');
    const headerCells = headerRow ? headerRow.querySelectorAll('th') : [];

    headerCells.forEach((th, index) => {
      th.style.cursor = 'pointer';
      th.addEventListener('click', function() {
        const rows = Array.from(tbody.rows);
        const currentDir = th.getAttribute('data-sort-dir') === 'asc' ? 'desc' : 'asc';

        // Limpiar indicador en otras columnas
        headerCells.forEach(h => h.removeAttribute('data-sort-dir'));
        th.setAttribute('data-sort-dir', currentDir);

        rows.sort((a, b) => {
          const va = getCellText(a, index);
          const vb = getCellText(b, index);

          // Intento de orden numérico si ambos parecen números
          const na = parseFloat(va.replace(',', '.'));
          const nb = parseFloat(vb.replace(',', '.'));
          const bothNumeric = !isNaN(na) && !isNaN(nb);

          if (bothNumeric) {
            return currentDir === 'asc' ? na - nb : nb - na;
          }
          return currentDir === 'asc'
            ? va.localeCompare(vb)
            : vb.localeCompare(va);
        });

        rows.forEach(r => tbody.appendChild(r));
      });
    });

    /*--- Filtros por columna (multicriterio) ---*/
    const filterInputs = table.querySelectorAll('thead .column-filter');

    const applyFilters = () => {
      const filters = Array.from(filterInputs).map(input =>
        (input.value || '').trim().toLowerCase()
      );

      Array.from(tbody.rows).forEach(row => {
        let visible = true;

        filters.forEach((value, colIdx) => {
          if (!value) return; // sin filtro en esta columna

          const cellText = getCellText(row, colIdx);
          if (cellText.indexOf(value) === -1) {
            visible = false;
          }
        });

        row.style.display = visible ? '' : 'none';
      });
    };

    filterInputs.forEach(input => {
      input.addEventListener('input', applyFilters);
    });
  }
});
</script>

  </body>
</html>

