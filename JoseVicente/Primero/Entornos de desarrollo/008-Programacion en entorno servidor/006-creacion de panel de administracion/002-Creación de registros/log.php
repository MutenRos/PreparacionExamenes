<?php
declare(strict_types=1);

/*
  log.php
  - Inclúyelo al final del footer (antes de </body>), por ejemplo:
      <?php include __DIR__ . '/log.php'; ?>
    o desde inc/piedepagina.php:
      <?php include __DIR__ . '/../log.php'; ?>

  - Registra una visita por request.
*/

if (headers_sent()) {
  // No pasa nada; no dependemos de headers, pero evitamos warnings raros en algunos entornos.
}

function _log_try_get_headers(): array {
  if (function_exists('getallheaders')) {
    $h = getallheaders();
    if (is_array($h)) return $h;
  }
  // Fallback (no siempre completo)
  $headers = [];
  foreach ($_SERVER as $k => $v) {
    if (str_starts_with($k, 'HTTP_')) {
      $name = str_replace('_', '-', substr($k, 5));
      $headers[$name] = $v;
    }
  }
  return $headers;
}

function _log_client_ip(array $headers): string {
  // Prioriza proxies habituales, pero sin “confiar” ciegamente: guardamos también la cadena raw.
  $candidates = [
    'CF-Connecting-IP',
    'True-Client-IP',
    'X-Real-IP',
    'X-Forwarded-For',
  ];
  foreach ($candidates as $h) {
    foreach ($headers as $k => $v) {
      if (strcasecmp($k, $h) === 0 && is_string($v) && trim($v) !== '') {
        if (strcasecmp($h, 'X-Forwarded-For') === 0) {
          // Puede traer varios: "ip1, ip2, ip3"
          $parts = array_map('trim', explode(',', $v));
          if (!empty($parts[0])) return $parts[0];
        }
        return trim($v);
      }
    }
  }
  return (string)($_SERVER['REMOTE_ADDR'] ?? '');
}

function _log_json($x): string {
  $j = json_encode($x, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES);
  return $j === false ? '{}' : $j;
}

function _log_hash_cookie_value(string $value): string {
  // Para evitar guardar valores sensibles en claro.
  return hash('sha256', $value);
}

try {
  // Ajusta esta ruta si tu include se hace desde otra carpeta.
  $dbPath = __DIR__ . '/recortables.db';

  $db = new SQLite3($dbPath);
  $db->busyTimeout(2000);

  $headers = _log_try_get_headers();

  $scheme = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http';
  $host   = (string)($_SERVER['HTTP_HOST'] ?? $_SERVER['SERVER_NAME'] ?? '');
  $uri    = (string)($_SERVER['REQUEST_URI'] ?? '');
  $url    = ($host !== '') ? ($scheme . '://' . $host . $uri) : $uri;

  $ip = _log_client_ip($headers);

  $method   = (string)($_SERVER['REQUEST_METHOD'] ?? '');
  $referrer = (string)($_SERVER['HTTP_REFERER'] ?? '');
  $ua       = (string)($_SERVER['HTTP_USER_AGENT'] ?? '');
  $acceptLang = (string)($_SERVER['HTTP_ACCEPT_LANGUAGE'] ?? '');
  $accept     = (string)($_SERVER['HTTP_ACCEPT'] ?? '');
  $encoding   = (string)($_SERVER['HTTP_ACCEPT_ENCODING'] ?? '');
  $dnt        = (string)($_SERVER['HTTP_DNT'] ?? '');

  $path = (string)(parse_url($uri, PHP_URL_PATH) ?? '');
  $queryString = (string)($_SERVER['QUERY_STRING'] ?? '');

  // Cookies: guardamos nombres + hash del valor (no el valor en claro)
  $cookies = [];
  foreach ($_COOKIE as $ck => $cv) {
    $cookies[(string)$ck] = _log_hash_cookie_value((string)$cv);
  }

  // Session (si existe)
  $sessionId = '';
  if (session_status() === PHP_SESSION_ACTIVE) {
    $sessionId = session_id();
  }

  // Usuario (si tu proyecto usa $_SESSION['user'] como en login.php)
  $userId = null;
  if (session_status() === PHP_SESSION_ACTIVE && isset($_SESSION['user']['id'])) {
    $userId = (int)$_SESSION['user']['id'];
  }

  $remotePort = (int)($_SERVER['REMOTE_PORT'] ?? 0);
  $serverIp   = (string)($_SERVER['SERVER_ADDR'] ?? '');
  $serverPort = (int)($_SERVER['SERVER_PORT'] ?? 0);
  $protocol   = (string)($_SERVER['SERVER_PROTOCOL'] ?? '');

  // Guardamos “todo lo posible” en JSON para no perder campos (y poder ampliar sin migraciones)
  $headersJson = _log_json($headers);
  $serverJson  = _log_json($_SERVER);
  $cookiesJson = _log_json($cookies);

  $stmt = $db->prepare("
    INSERT INTO logs (
      created_at,
      ip, ip_raw,
      method, scheme, host, url, path, query_string,
      referer, user_agent,
      accept, accept_language, accept_encoding, dnt,
      session_id, user_id,
      remote_port, server_ip, server_port, protocol,
      headers_json, server_json, cookies_json
    ) VALUES (
      datetime('now'),
      :ip, :ip_raw,
      :method, :scheme, :host, :url, :path, :query_string,
      :referer, :user_agent,
      :accept, :accept_language, :accept_encoding, :dnt,
      :session_id, :user_id,
      :remote_port, :server_ip, :server_port, :protocol,
      :headers_json, :server_json, :cookies_json
    )
  ");

  // ip_raw: guardamos los headers “de ip” por si quieres auditar proxies
  $ipRaw = [
    'REMOTE_ADDR' => $_SERVER['REMOTE_ADDR'] ?? null,
    'X-Forwarded-For' => $headers['X-Forwarded-For'] ?? $headers['X-FORWARDED-FOR'] ?? null,
    'X-Real-IP' => $headers['X-Real-IP'] ?? $headers['X-REAL-IP'] ?? null,
    'CF-Connecting-IP' => $headers['CF-Connecting-IP'] ?? $headers['CF-CONNECTING-IP'] ?? null,
    'True-Client-IP' => $headers['True-Client-IP'] ?? $headers['TRUE-CLIENT-IP'] ?? null,
  ];

  $stmt->bindValue(':ip', $ip, SQLITE3_TEXT);
  $stmt->bindValue(':ip_raw', _log_json($ipRaw), SQLITE3_TEXT);

  $stmt->bindValue(':method', $method, SQLITE3_TEXT);
  $stmt->bindValue(':scheme', $scheme, SQLITE3_TEXT);
  $stmt->bindValue(':host', $host, SQLITE3_TEXT);
  $stmt->bindValue(':url', $url, SQLITE3_TEXT);
  $stmt->bindValue(':path', $path, SQLITE3_TEXT);
  $stmt->bindValue(':query_string', $queryString, SQLITE3_TEXT);

  $stmt->bindValue(':referer', $referrer, SQLITE3_TEXT);
  $stmt->bindValue(':user_agent', $ua, SQLITE3_TEXT);

  $stmt->bindValue(':accept', $accept, SQLITE3_TEXT);
  $stmt->bindValue(':accept_language', $acceptLang, SQLITE3_TEXT);
  $stmt->bindValue(':accept_encoding', $encoding, SQLITE3_TEXT);
  $stmt->bindValue(':dnt', $dnt, SQLITE3_TEXT);

  $stmt->bindValue(':session_id', $sessionId, SQLITE3_TEXT);
  if ($userId === null) $stmt->bindValue(':user_id', null, SQLITE3_NULL);
  else $stmt->bindValue(':user_id', $userId, SQLITE3_INTEGER);

  $stmt->bindValue(':remote_port', $remotePort, SQLITE3_INTEGER);
  $stmt->bindValue(':server_ip', $serverIp, SQLITE3_TEXT);
  $stmt->bindValue(':server_port', $serverPort, SQLITE3_INTEGER);
  $stmt->bindValue(':protocol', $protocol, SQLITE3_TEXT);

  $stmt->bindValue(':headers_json', $headersJson, SQLITE3_TEXT);
  $stmt->bindValue(':server_json', $serverJson, SQLITE3_TEXT);
  $stmt->bindValue(':cookies_json', $cookiesJson, SQLITE3_TEXT);

  $stmt->execute();

} catch (Throwable $e) {
  // Silencioso: al ser un include de footer, no debe romper la web.
  // Si quieres depurar:
  // error_log("log.php error: " . $e->getMessage());
}

