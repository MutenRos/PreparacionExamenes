<?php
declare(strict_types=1);

/**
 * PDO SQLite
 */
function sqlite(string $path): PDO {
    $db = new PDO('sqlite:' . $path);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    return $db;
}

/**
 * Query -> JSON [{clave, valor}, ...]
 */
function consulta_json(PDO $db, string $sql, array $params = []): string {
    $stmt = $db->prepare($sql);
    $stmt->execute($params);
    $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);
    return json_encode($rows, JSON_UNESCAPED_UNICODE);
}

/**
 * Build WHERE clause + params from GET filters
 */
function build_filters(): array {
    $w = [];
    $p = [];

    // Date range (inclusive)
    $from = isset($_GET['from']) ? trim((string)$_GET['from']) : '';
    $to   = isset($_GET['to'])   ? trim((string)$_GET['to'])   : '';

    if ($from !== '') {
        // from 00:00:00
        $w[] = "\"datetime\" >= :from";
        $p[':from'] = $from . ' 00:00:00';
    }
    if ($to !== '') {
        // to 23:59:59
        $w[] = "\"datetime\" <= :to";
        $p[':to'] = $to . ' 23:59:59';
    }

    // Basic dimensions
    $event_type = isset($_GET['event_type']) ? trim((string)$_GET['event_type']) : '';
    if ($event_type !== '') {
        $w[] = "event_type = :event_type";
        $p[':event_type'] = $event_type;
    }

    $post_id = isset($_GET['post_id']) ? trim((string)$_GET['post_id']) : '';
    if ($post_id !== '' && ctype_digit($post_id)) {
        $w[] = "post_id = :post_id";
        $p[':post_id'] = (int)$post_id;
    }

    $category = isset($_GET['category']) ? trim((string)$_GET['category']) : '';
    if ($category !== '') {
        $w[] = "category = :category";
        $p[':category'] = $category;
    }

    $host = isset($_GET['host']) ? trim((string)$_GET['host']) : '';
    if ($host !== '') {
        $w[] = "host = :host";
        $p[':host'] = $host;
    }

    // Exclude bots (basic heuristics)
    $exclude_bots = isset($_GET['exclude_bots']) ? trim((string)$_GET['exclude_bots']) : '';
    if ($exclude_bots === '1') {
        $w[] = "NOT (
            lower(user_agent) LIKE '%bot%' OR
            lower(user_agent) LIKE '%spider%' OR
            lower(user_agent) LIKE '%crawl%' OR
            lower(user_agent) LIKE '%slurp%' OR
            lower(user_agent) LIKE '%facebookexternalhit%' OR
            lower(user_agent) LIKE '%linkedinbot%' OR
            lower(user_agent) LIKE '%whatsapp%' OR
            lower(user_agent) LIKE '%telegram%' OR
            lower(user_agent) LIKE '%preview%'
        )";
    }

    $where_sql = (count($w) > 0) ? ('WHERE ' . implode(' AND ', $w)) : '';
    return [$where_sql, $p];
}

$db = sqlite('posts.db');
[$WHERE, $PARAMS] = build_filters();

/**
 * Helper: extract "domain" from referer in SQLite (best effort).
 * - If referer empty -> '(direct)'
 * - If referer contains '://' -> take host part until next '/'
 */
$REFERER_DOMAIN_EXPR = "
CASE
  WHEN referer IS NULL OR trim(referer) = '' THEN '(direct)'
  WHEN instr(referer, '://') > 0 THEN
    CASE
      WHEN instr(substr(referer, instr(referer, '://') + 3), '/') > 0 THEN
        substr(
          substr(referer, instr(referer, '://') + 3),
          1,
          instr(substr(referer, instr(referer, '://') + 3), '/') - 1
        )
      ELSE
        substr(referer, instr(referer, '://') + 3)
    END
  ELSE
    -- no scheme, try up to first '/'
    CASE
      WHEN instr(referer, '/') > 0 THEN substr(referer, 1, instr(referer, '/') - 1)
      ELSE referer
    END
END
";

/**
 * Helper: classify UA (rough)
 */
$UA_CLASS_EXPR = "
CASE
  WHEN user_agent IS NULL OR trim(user_agent) = '' THEN '(empty)'
  WHEN lower(user_agent) LIKE '%facebookexternalhit%' THEN 'Facebook crawler'
  WHEN lower(user_agent) LIKE '%linkedinbot%' THEN 'LinkedIn bot'
  WHEN lower(user_agent) LIKE '%twitterbot%' THEN 'Twitter bot'
  WHEN lower(user_agent) LIKE '%telegram%' THEN 'Telegram'
  WHEN lower(user_agent) LIKE '%whatsapp%' THEN 'WhatsApp'
  WHEN lower(user_agent) LIKE '%bot%' OR lower(user_agent) LIKE '%spider%' OR lower(user_agent) LIKE '%crawl%' THEN 'Other bot'
  WHEN lower(user_agent) LIKE '%android%' THEN 'Android'
  WHEN lower(user_agent) LIKE '%iphone%' OR lower(user_agent) LIKE '%ipad%' OR lower(user_agent) LIKE '%ios%' THEN 'iOS'
  WHEN lower(user_agent) LIKE '%windows%' THEN 'Windows'
  WHEN lower(user_agent) LIKE '%mac os%' OR lower(user_agent) LIKE '%macintosh%' THEN 'macOS'
  WHEN lower(user_agent) LIKE '%linux%' THEN 'Linux'
  ELSE 'Other'
END
";

/**
 * Charts catalog:
 * id => canvas id
 * title => chart title
 * sql => query returning {clave, valor}
 */
$charts = [

    // --- TIME ---
    [
        'id' => 'c_hour',
        'title' => 'Visitas por hora (00-23)',
        'sql' => "
            SELECT strftime('%H', \"datetime\") AS clave, COUNT(*) AS valor
            FROM logs
            $WHERE
            GROUP BY clave
            ORDER BY clave;
        ",
    ],
    [
        'id' => 'c_weekday',
        'title' => 'Visitas por día de la semana',
        'sql' => "
            SELECT
              CASE strftime('%w', \"datetime\")
                WHEN '0' THEN 'Sunday'
                WHEN '1' THEN 'Monday'
                WHEN '2' THEN 'Tuesday'
                WHEN '3' THEN 'Wednesday'
                WHEN '4' THEN 'Thursday'
                WHEN '5' THEN 'Friday'
                WHEN '6' THEN 'Saturday'
              END AS clave,
              COUNT(*) AS valor
            FROM logs
            $WHERE
            GROUP BY strftime('%w', \"datetime\")
            ORDER BY strftime('%w', \"datetime\");
        ",
    ],
    [
        'id' => 'c_day',
        'title' => 'Visitas por día (YYYY-MM-DD)',
        'sql' => "
            SELECT strftime('%Y-%m-%d', \"datetime\") AS clave, COUNT(*) AS valor
            FROM logs
            $WHERE
            GROUP BY clave
            ORDER BY clave;
        ",
    ],
    [
        'id' => 'c_month',
        'title' => 'Visitas por mes (YYYY-MM)',
        'sql' => "
            SELECT strftime('%Y-%m', \"datetime\") AS clave, COUNT(*) AS valor
            FROM logs
            $WHERE
            GROUP BY clave
            ORDER BY clave;
        ",
    ],
    [
        'id' => 'c_year',
        'title' => 'Visitas por año (YYYY)',
        'sql' => "
            SELECT strftime('%Y', \"datetime\") AS clave, COUNT(*) AS valor
            FROM logs
            $WHERE
            GROUP BY clave
            ORDER BY clave;
        ",
    ],

    // --- EVENT TYPE ---
    [
        'id' => 'c_event_type',
        'title' => 'Eventos por tipo (event_type)',
        'sql' => "
            SELECT COALESCE(event_type, '(null)') AS clave, COUNT(*) AS valor
            FROM logs
            $WHERE
            GROUP BY clave
            ORDER BY valor DESC;
        ",
    ],
    [
        'id' => 'c_event_type_hour',
        'title' => 'Eventos por hora (filtrable por event_type)',
        'sql' => "
            SELECT strftime('%H', \"datetime\") AS clave, COUNT(*) AS valor
            FROM logs
            $WHERE
            GROUP BY clave
            ORDER BY clave;
        ",
    ],

    // --- CONTENT / POSTS ---
    [
        'id' => 'c_top_posts',
        'title' => 'Top posts por eventos (post_id)',
        'sql' => "
            SELECT CAST(post_id AS TEXT) AS clave, COUNT(*) AS valor
            FROM logs
            $WHERE
            GROUP BY post_id
            ORDER BY valor DESC
            LIMIT 30;
        ",
    ],
    [
        'id' => 'c_top_posts_views',
        'title' => 'Top posts (solo views)',
        'sql' => "
            SELECT CAST(post_id AS TEXT) AS clave, COUNT(*) AS valor
            FROM logs
            " . (trim($WHERE) === '' ? "WHERE event_type='view'" : $WHERE . " AND event_type='view'") . "
            GROUP BY post_id
            ORDER BY valor DESC
            LIMIT 30;
        ",
    ],
    [
        'id' => 'c_top_posts_clicks',
        'title' => 'Top posts (solo clicks)',
        'sql' => "
            SELECT CAST(post_id AS TEXT) AS clave, COUNT(*) AS valor
            FROM logs
            " . (trim($WHERE) === '' ? "WHERE event_type='click'" : $WHERE . " AND event_type='click'") . "
            GROUP BY post_id
            ORDER BY valor DESC
            LIMIT 30;
        ",
    ],
    [
        'id' => 'c_category',
        'title' => 'Eventos por categoría',
        'sql' => "
            SELECT COALESCE(category, '(none)') AS clave, COUNT(*) AS valor
            FROM logs
            $WHERE
            GROUP BY clave
            ORDER BY valor DESC
            LIMIT 30;
        ",
    ],

    // --- TRAFFIC SOURCES ---
    [
        'id' => 'c_referer_domain',
        'title' => 'Referer por dominio (top 30)',
        'sql' => "
            SELECT $REFERER_DOMAIN_EXPR AS clave, COUNT(*) AS valor
            FROM logs
            $WHERE
            GROUP BY clave
            ORDER BY valor DESC
            LIMIT 30;
        ",
    ],
    [
        'id' => 'c_referer_full',
        'title' => 'Referer completo (top 30)',
        'sql' => "
            SELECT COALESCE(referer, '(null)') AS clave, COUNT(*) AS valor
            FROM logs
            $WHERE
            GROUP BY clave
            ORDER BY valor DESC
            LIMIT 30;
        ",
    ],

    // --- TECH / CLIENT ---
    [
        'id' => 'c_method',
        'title' => 'Método HTTP (GET/POST/...)',
        'sql' => "
            SELECT COALESCE(method, '(none)') AS clave, COUNT(*) AS valor
            FROM logs
            $WHERE
            GROUP BY clave
            ORDER BY valor DESC;
        ",
    ],
    [
        'id' => 'c_https',
        'title' => 'HTTPS on/off',
        'sql' => "
            SELECT
              CASE
                WHEN https IS NULL OR trim(https) = '' THEN '(empty)'
                ELSE https
              END AS clave,
              COUNT(*) AS valor
            FROM logs
            $WHERE
            GROUP BY clave
            ORDER BY valor DESC;
        ",
    ],
    [
        'id' => 'c_host',
        'title' => 'Host (top 30)',
        'sql' => "
            SELECT COALESCE(host, '(none)') AS clave, COUNT(*) AS valor
            FROM logs
            $WHERE
            GROUP BY clave
            ORDER BY valor DESC
            LIMIT 30;
        ",
    ],
    [
        'id' => 'c_server_name',
        'title' => 'Server name (top 30)',
        'sql' => "
            SELECT COALESCE(server_name, '(none)') AS clave, COUNT(*) AS valor
            FROM logs
            $WHERE
            GROUP BY clave
            ORDER BY valor DESC
            LIMIT 30;
        ",
    ],
    [
        'id' => 'c_accept_language',
        'title' => 'Accept-Language (top 30)',
        'sql' => "
            SELECT
              CASE
                WHEN accept_language IS NULL OR trim(accept_language) = '' THEN '(empty)'
                ELSE accept_language
              END AS clave,
              COUNT(*) AS valor
            FROM logs
            $WHERE
            GROUP BY clave
            ORDER BY valor DESC
            LIMIT 30;
        ",
    ],
    [
        'id' => 'c_user_agent_class',
        'title' => 'Clasificación de User-Agent',
        'sql' => "
            SELECT $UA_CLASS_EXPR AS clave, COUNT(*) AS valor
            FROM logs
            $WHERE
            GROUP BY clave
            ORDER BY valor DESC;
        ",
    ],
    [
        'id' => 'c_user_agent_top',
        'title' => 'User-Agent completo (top 20)',
        'sql' => "
            SELECT
              CASE
                WHEN user_agent IS NULL OR trim(user_agent) = '' THEN '(empty)'
                ELSE user_agent
              END AS clave,
              COUNT(*) AS valor
            FROM logs
            $WHERE
            GROUP BY clave
            ORDER BY valor DESC
            LIMIT 20;
        ",
    ],

    // --- URL / ROUTES ---
    [
        'id' => 'c_uri_top',
        'title' => 'URI (top 30)',
        'sql' => "
            SELECT COALESCE(uri, '(none)') AS clave, COUNT(*) AS valor
            FROM logs
            $WHERE
            GROUP BY clave
            ORDER BY valor DESC
            LIMIT 30;
        ",
    ],
    [
        'id' => 'c_url_top',
        'title' => 'URL (top 30)',
        'sql' => "
            SELECT COALESCE(url, '(none)') AS clave, COUNT(*) AS valor
            FROM logs
            $WHERE
            GROUP BY clave
            ORDER BY valor DESC
            LIMIT 30;
        ",
    ],
    [
        'id' => 'c_query_string_top',
        'title' => 'Query string (top 30)',
        'sql' => "
            SELECT
              CASE
                WHEN query_string IS NULL OR trim(query_string) = '' THEN '(none)'
                ELSE query_string
              END AS clave,
              COUNT(*) AS valor
            FROM logs
            $WHERE
            GROUP BY clave
            ORDER BY valor DESC
            LIMIT 30;
        ",
    ],

    // --- SEARCH / INTERNAL ---
    [
        'id' => 'c_search_query',
        'title' => 'Búsquedas internas (search_query top 30)',
        'sql' => "
            SELECT
              CASE
                WHEN search_query IS NULL OR trim(search_query) = '' THEN '(none)'
                ELSE search_query
              END AS clave,
              COUNT(*) AS valor
            FROM logs
            $WHERE
            GROUP BY clave
            ORDER BY valor DESC
            LIMIT 30;
        ",
    ],

    // --- USERS / SESSIONS ---
    [
        'id' => 'c_unique_ips_daily',
        'title' => 'IPs únicas por día',
        'sql' => "
            SELECT strftime('%Y-%m-%d', \"datetime\") AS clave, COUNT(DISTINCT ip) AS valor
            FROM logs
            $WHERE
            GROUP BY clave
            ORDER BY clave;
        ",
    ],
    [
        'id' => 'c_top_ips',
        'title' => 'Top IPs por eventos (top 30)',
        'sql' => "
            SELECT COALESCE(ip, '(none)') AS clave, COUNT(*) AS valor
            FROM logs
            $WHERE
            GROUP BY clave
            ORDER BY valor DESC
            LIMIT 30;
        ",
    ],
    [
        'id' => 'c_sessions_top',
        'title' => 'Top session_id por eventos (top 30)',
        'sql' => "
            SELECT
              CASE
                WHEN session_id IS NULL OR trim(session_id) = '' THEN '(none)'
                ELSE session_id
              END AS clave,
              COUNT(*) AS valor
            FROM logs
            $WHERE
            GROUP BY clave
            ORDER BY valor DESC
            LIMIT 30;
        ",
    ],
    [
        'id' => 'c_unique_sessions_daily',
        'title' => 'Sesiones únicas por día',
        'sql' => "
            SELECT strftime('%Y-%m-%d', \"datetime\") AS clave, COUNT(DISTINCT session_id) AS valor
            FROM logs
            $WHERE
            GROUP BY clave
            ORDER BY clave;
        ",
    ],

    // --- NETWORK ---
    [
        'id' => 'c_remote_port',
        'title' => 'Remote port (top 30)',
        'sql' => "
            SELECT
              CASE
                WHEN remote_port IS NULL OR trim(remote_port) = '' THEN '(none)'
                ELSE CAST(remote_port AS TEXT)
              END AS clave,
              COUNT(*) AS valor
            FROM logs
            $WHERE
            GROUP BY clave
            ORDER BY valor DESC
            LIMIT 30;
        ",
    ],
];

// Basic page metadata
function h(string $s): string { return htmlspecialchars($s, ENT_QUOTES, 'UTF-8'); }

$activeFilters = [];
foreach (['from','to','event_type','post_id','category','host','exclude_bots'] as $k) {
    if (isset($_GET[$k]) && trim((string)$_GET[$k]) !== '') {
        $activeFilters[] = $k . '=' . (string)$_GET[$k];
    }
}
$filtersLine = (count($activeFilters) > 0) ? implode('&', $activeFilters) : '(none)';

?>
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <title>Analytics</title>
  <script src="graficas.js"></script>
  <style>
    body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Cantarell,Noto Sans,sans-serif;margin:20px;}
    .meta{color:#555;margin-bottom:16px;font-size:14px}
    .grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(520px,1fr));gap:18px;}
    .card{border:1px solid #e6e6e6;border-radius:12px;padding:14px;}
    .card h3{margin:0 0 10px 0;font-size:16px;font-weight:600;}
    canvas{width:100%;border:1px solid #eee;border-radius:10px;}
    .filters{border:1px solid #e6e6e6;border-radius:12px;padding:14px;margin-bottom:18px;}
    .filters form{display:flex;flex-wrap:wrap;gap:10px;align-items:end}
    .filters label{display:flex;flex-direction:column;font-size:12px;color:#555}
    .filters input{padding:8px 10px;border:1px solid #ddd;border-radius:8px;min-width:150px}
    .filters button{padding:10px 14px;border:0;border-radius:10px;background:#111;color:#fff;cursor:pointer}
    .filters a{font-size:12px;color:#111;text-decoration:none}
  </style>
</head>
<body>

  <div class="filters">
    <form method="get">
      <label>from (YYYY-MM-DD)
        <input name="from" value="<?= h((string)($_GET['from'] ?? '')) ?>" placeholder="2025-12-01">
      </label>
      <label>to (YYYY-MM-DD)
        <input name="to" value="<?= h((string)($_GET['to'] ?? '')) ?>" placeholder="2025-12-31">
      </label>
      <label>event_type
        <input name="event_type" value="<?= h((string)($_GET['event_type'] ?? '')) ?>" placeholder="view / click">
      </label>
      <label>post_id
        <input name="post_id" value="<?= h((string)($_GET['post_id'] ?? '')) ?>" placeholder="1459">
      </label>
      <label>category
        <input name="category" value="<?= h((string)($_GET['category'] ?? '')) ?>" placeholder="">
      </label>
      <label>host
        <input name="host" value="<?= h((string)($_GET['host'] ?? '')) ?>" placeholder="josevicentecarratala.com">
      </label>
      <label>exclude_bots (1/empty)
        <input name="exclude_bots" value="<?= h((string)($_GET['exclude_bots'] ?? '')) ?>" placeholder="1">
      </label>
      <button type="submit">Apply</button>
      <a href="<?= h(strtok((string)($_SERVER['REQUEST_URI'] ?? ''), '?')) ?>">Reset</a>
    </form>
    <div class="meta">Active filters: <?= h($filtersLine) ?></div>
  </div>

  <div class="grid">
    <?php foreach ($charts as $ch): ?>
      <div class="card">
        <h3><?= h($ch['title']) ?></h3>
        <canvas id="<?= h($ch['id']) ?>"></canvas>
        <script>
          grafica(
            "#<?= h($ch['id']) ?>",
            <?= consulta_json($db, $ch['sql'], $PARAMS) ?>,
            "<?= h($ch['title']) ?>"
          );
        </script>
      </div>
    <?php endforeach; ?>
  </div>

</body>
</html>

