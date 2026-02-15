<?php
// sitemap.php
// Inclúyelo silenciosamente (igual que log.php) al final del footer.
// Genera/actualiza sitemap.xml con caché para no regenerar en cada request.

declare(strict_types=1);

try {
  $root = __DIR__;
  $dbPath = $root . '/recortables.db';
  $outXml = $root . '/sitemap.xml';
  $tmpXml = $root . '/sitemap.xml.tmp';
  $cache  = $root . '/.sitemap.cache.json';

  if (!is_file($dbPath)) return;

  // Base URL
  $scheme = (!empty($_SERVER['HTTPS']) && $_SERVER['HTTPS'] !== 'off') ? 'https' : 'http';
  $host   = $_SERVER['HTTP_HOST'] ?? 'recortabl.es';
  $base   = $scheme . '://' . $host;

  // Caducidad (segundos): 6 horas
  $ttl = 6 * 3600;

  // DB fingerprint (barato)
  $db = new SQLite3($dbPath);
  $db->busyTimeout(1000);

  $prodCount = (int)$db->querySingle("SELECT COUNT(*) FROM productos");
  $catCount  = (int)$db->querySingle("SELECT COUNT(*) FROM categorias");
  $prodMaxId = (int)$db->querySingle("SELECT IFNULL(MAX(Identificador),0) FROM productos");
  $catMaxId  = (int)$db->querySingle("SELECT IFNULL(MAX(Identificador),0) FROM categorias");

  $fingerprint = hash('sha256', $prodCount.'|'.$catCount.'|'.$prodMaxId.'|'.$catMaxId);

  // Leer cache
  $cacheData = [
    'ts' => 0,
    'fingerprint' => ''
  ];
  if (is_file($cache)) {
    $raw = @file_get_contents($cache);
    $j = $raw ? json_decode($raw, true) : null;
    if (is_array($j)) $cacheData = array_merge($cacheData, $j);
  }

  $tooSoon = (time() - (int)$cacheData['ts']) < $ttl;
  $sameFp  = (string)$cacheData['fingerprint'] === $fingerprint;

  // Si sitemap existe y no ha caducado y no hay cambios -> no regenerar
  if (is_file($outXml) && $tooSoon && $sameFp) return;

  // URLs estáticas (añade/quita según tu proyecto)
  $static = [
    '/index.php'       => 'weekly',
    '/catalogo.php'    => 'daily',
    '/categorias.php'  => 'weekly',
    '/descargas.php'   => 'daily',
    '/acercade.php'    => 'monthly',
    '/sobrenosotros.php'=> 'monthly',
    '/licencias.php'   => 'yearly',
    '/contacto.php'    => 'yearly',
    '/avisolegal.php'  => 'yearly',
    // '/login.php'     => (normalmente no se indexa; mejor no meterlo)
  ];

  $urls = [];

  // Helper to add
  $add = function(string $path, string $freq, ?string $lastmod = null, string $priority = '0.6') use (&$urls, $base) {
    $u = [
      'loc' => $base . $path,
      'changefreq' => $freq,
      'priority' => $priority
    ];
    if ($lastmod) $u['lastmod'] = $lastmod;
    $urls[] = $u;
  };

  // Añadir estáticas
  foreach ($static as $path => $freq) {
    $prio = ($path === '/index.php') ? '1.0' : (($path === '/catalogo.php') ? '0.9' : '0.7');
    $add($path, $freq, null, $prio);
  }

  // Categorías -> catalogo.php?cat=ID (útil para SEO de long-tail)
  $resCat = $db->query("SELECT Identificador FROM categorias ORDER BY Identificador DESC");
  while ($row = $resCat->fetchArray(SQLITE3_ASSOC)) {
    $id = (int)$row['Identificador'];
    if ($id > 0) $add('/catalogo.php?cat='.$id, 'weekly', null, '0.6');
  }

  // Productos -> producto.php?id=ID
  $resProd = $db->query("SELECT Identificador FROM productos ORDER BY Identificador DESC");
  while ($row = $resProd->fetchArray(SQLITE3_ASSOC)) {
    $id = (int)$row['Identificador'];
    if ($id > 0) $add('/producto.php?id='.$id, 'monthly', null, '0.8');
  }

  // Construir XML
  $dom = new DOMDocument('1.0', 'UTF-8');
  $dom->formatOutput = true;

  $urlset = $dom->createElement('urlset');
  $urlset->setAttribute('xmlns', 'http://www.sitemaps.org/schemas/sitemap/0.9');
  $dom->appendChild($urlset);

  foreach ($urls as $u) {
    $url = $dom->createElement('url');

    $loc = $dom->createElement('loc');
    $loc->appendChild($dom->createTextNode($u['loc']));
    $url->appendChild($loc);

    if (!empty($u['lastmod'])) {
      $lm = $dom->createElement('lastmod');
      $lm->appendChild($dom->createTextNode($u['lastmod']));
      $url->appendChild($lm);
    }

    $cf = $dom->createElement('changefreq', $u['changefreq']);
    $url->appendChild($cf);

    $pr = $dom->createElement('priority', $u['priority']);
    $url->appendChild($pr);

    $urlset->appendChild($url);
  }

  // Escribir atomico
  $xml = $dom->saveXML();
  if ($xml === false) return;

  @file_put_contents($tmpXml, $xml, LOCK_EX);
  @rename($tmpXml, $outXml);

  // Guardar cache
  $cacheWrite = [
    'ts' => time(),
    'fingerprint' => $fingerprint
  ];
  @file_put_contents($cache, json_encode($cacheWrite, JSON_UNESCAPED_UNICODE|JSON_UNESCAPED_SLASHES), LOCK_EX);

} catch (Throwable $e) {
  // Silencioso: no romper la web por el sitemap
  // error_log("sitemap.php error: ".$e->getMessage());
}

