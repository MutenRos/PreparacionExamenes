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
 * Query -> array rows
 */
function consulta_array(PDO $db, string $sql, array $params = []): array {
    $stmt = $db->prepare($sql);
    $stmt->execute($params);
    return $stmt->fetchAll(PDO::FETCH_ASSOC);
}

/**
 * Query -> JSON
 */
function consulta_json(PDO $db, string $sql, array $params = []): string {
    return json_encode(consulta_array($db, $sql, $params), JSON_UNESCAPED_UNICODE);
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
        $w[] = "\"datetime\" >= :from";
        $p[':from'] = $from . ' 00:00:00';
    }
    if ($to !== '') {
        $w[] = "\"datetime\" <= :to";
        $p[':to'] = $to . ' 23:59:59';
    }

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

/**
 * Escape
 */
function h(string $s): string { return htmlspecialchars($s, ENT_QUOTES, 'UTF-8'); }

/**
 * Best-effort domain from referer
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
    CASE
      WHEN instr(referer, '/') > 0 THEN substr(referer, 1, instr(referer, '/') - 1)
      ELSE referer
    END
END
";

/**
 * UA class
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

$db = sqlite('posts.db');
[$WHERE, $PARAMS] = build_filters();

// KPIs (respect filters)
$kpi_total = (int)(consulta_array($db, "SELECT COUNT(*) AS n FROM logs $WHERE", $PARAMS)[0]['n'] ?? 0);
$kpi_ips   = (int)(consulta_array($db, "SELECT COUNT(DISTINCT ip) AS n FROM logs $WHERE", $PARAMS)[0]['n'] ?? 0);
$kpi_sess  = (int)(consulta_array($db, "SELECT COUNT(DISTINCT session_id) AS n FROM logs $WHERE", $PARAMS)[0]['n'] ?? 0);

// views/clicks as KPIs (respect filters but force type AND conditions)
$WHERE_VIEW  = (trim($WHERE) === '') ? "WHERE event_type='view'"  : ($WHERE . " AND event_type='view'");
$WHERE_CLICK = (trim($WHERE) === '') ? "WHERE event_type='click'" : ($WHERE . " AND event_type='click'");

$kpi_views  = (int)(consulta_array($db, "SELECT COUNT(*) AS n FROM logs $WHERE_VIEW", $PARAMS)[0]['n'] ?? 0);
$kpi_clicks = (int)(consulta_array($db, "SELECT COUNT(*) AS n FROM logs $WHERE_CLICK", $PARAMS)[0]['n'] ?? 0);

// Active filter line
$activeFilters = [];
foreach (['from','to','event_type','post_id','category','host','exclude_bots'] as $k) {
    if (isset($_GET[$k]) && trim((string)$_GET[$k]) !== '') {
        $activeFilters[] = $k . '=' . (string)$_GET[$k];
    }
}
$filtersLine = (count($activeFilters) > 0) ? implode('&', $activeFilters) : '(none)';

// Chart catalog (type + options)
$charts = [
    // Time series
    [
        'id' => 'c_day',
        'title' => 'Eventos por día',
        'type' => 'line',
        'sql' => "
            SELECT strftime('%Y-%m-%d', \"datetime\") AS clave, COUNT(*) AS valor
            FROM logs
            $WHERE
            GROUP BY clave
            ORDER BY clave;
        ",
        'options' => ['yLabel' => 'Eventos'],
    ],
    [
        'id' => 'c_hour',
        'title' => 'Eventos por hora (00-23)',
        'type' => 'bar',
        'sql' => "
            SELECT strftime('%H', \"datetime\") AS clave, COUNT(*) AS valor
            FROM logs
            $WHERE
            GROUP BY clave
            ORDER BY clave;
        ",
        'options' => ['sort' => 'none'],
    ],
    [
        'id' => 'c_weekday',
        'title' => 'Eventos por día de la semana',
        'type' => 'bar',
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
        'options' => ['sort' => 'none'],
    ],
    [
        'id' => 'c_month',
        'title' => 'Eventos por mes',
        'type' => 'line',
        'sql' => "
            SELECT strftime('%Y-%m', \"datetime\") AS clave, COUNT(*) AS valor
            FROM logs
            $WHERE
            GROUP BY clave
            ORDER BY clave;
        ",
        'options' => ['yLabel' => 'Eventos'],
    ],

    // Distributions
    [
        'id' => 'c_event_type',
        'title' => 'Eventos por tipo',
        'type' => 'donut',
        'sql' => "
            SELECT COALESCE(event_type, '(null)') AS clave, COUNT(*) AS valor
            FROM logs
            $WHERE
            GROUP BY clave
            ORDER BY valor DESC;
        ",
        'options' => ['topN' => 12],
    ],
    [
        'id' => 'c_category',
        'title' => 'Eventos por categoría',
        'type' => 'bar',
        'sql' => "
            SELECT COALESCE(category, '(none)') AS clave, COUNT(*) AS valor
            FROM logs
            $WHERE
            GROUP BY clave
            ORDER BY valor DESC
            LIMIT 30;
        ",
        'options' => ['topN' => 20],
    ],
    [
        'id' => 'c_referer_domain',
        'title' => 'Referer por dominio',
        'type' => 'bar',
        'sql' => "
            SELECT $REFERER_DOMAIN_EXPR AS clave, COUNT(*) AS valor
            FROM logs
            $WHERE
            GROUP BY clave
            ORDER BY valor DESC
            LIMIT 30;
        ",
        'options' => ['topN' => 20],
    ],
    [
        'id' => 'c_user_agent_class',
        'title' => 'User-Agent (clasificación)',
        'type' => 'donut',
        'sql' => "
            SELECT $UA_CLASS_EXPR AS clave, COUNT(*) AS valor
            FROM logs
            $WHERE
            GROUP BY clave
            ORDER BY valor DESC;
        ",
        'options' => ['topN' => 12],
    ],

    // Content
    [
        'id' => 'c_top_posts',
        'title' => 'Top posts (eventos)',
        'type' => 'bar',
        'sql' => "
            SELECT CAST(post_id AS TEXT) AS clave, COUNT(*) AS valor
            FROM logs
            $WHERE
            GROUP BY post_id
            ORDER BY valor DESC
            LIMIT 30;
        ",
        'options' => ['topN' => 15],
    ],
    [
        'id' => 'c_top_posts_views',
        'title' => 'Top posts (views)',
        'type' => 'bar',
        'sql' => "
            SELECT CAST(post_id AS TEXT) AS clave, COUNT(*) AS valor
            FROM logs
            $WHERE_VIEW
            GROUP BY post_id
            ORDER BY valor DESC
            LIMIT 30;
        ",
        'options' => ['topN' => 15],
    ],
    [
        'id' => 'c_top_posts_clicks',
        'title' => 'Top posts (clicks)',
        'type' => 'bar',
        'sql' => "
            SELECT CAST(post_id AS TEXT) AS clave, COUNT(*) AS valor
            FROM logs
            $WHERE_CLICK
            GROUP BY post_id
            ORDER BY valor DESC
            LIMIT 30;
        ",
        'options' => ['topN' => 15],
    ],

    // Routes
    [
        'id' => 'c_uri_top',
        'title' => 'URI (top)',
        'type' => 'bar',
        'sql' => "
            SELECT COALESCE(uri, '(none)') AS clave, COUNT(*) AS valor
            FROM logs
            $WHERE
            GROUP BY clave
            ORDER BY valor DESC
            LIMIT 30;
        ",
        'options' => ['topN' => 15],
    ],
    [
        'id' => 'c_search_query',
        'title' => 'Búsquedas internas',
        'type' => 'bar',
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
        'options' => ['topN' => 15],
    ],
];

?>
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>Analytics</title>
  
  <style>
    :root{
      --bg:#0b0c0f;
      --card:#11131a;
      --muted:#a9b0c3;
      --text:#eef1ff;
      --stroke:rgba(255,255,255,.08);
      --shadow: 0 10px 30px rgba(0,0,0,.35);
      --accent:#7c5cff;
      --accent2:#22c55e;
      --danger:#ef4444;
      --chip: rgba(255,255,255,.06);
      --input: rgba(255,255,255,.06);
    }
    [data-theme="light"]{
      --bg:#f6f7fb;
      --card:#ffffff;
      --muted:#556079;
      --text:#0b1220;
      --stroke:rgba(2,6,23,.10);
      --shadow: 0 10px 30px rgba(15,23,42,.10);
      --accent:#4f46e5;
      --accent2:#16a34a;
      --danger:#dc2626;
      --chip: rgba(79,70,229,.08);
      --input: rgba(2,6,23,.06);
    }

    *{box-sizing:border-box}
    body{
      margin:0;
      font-family: system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Cantarell, Noto Sans, sans-serif;
      background: var(--bg);
      color: var(--text);
    }
    .wrap{max-width: 1400px; margin: 0 auto; padding: 18px;}
    .topbar{
      display:flex; gap:12px; align-items:center; justify-content:space-between;
      margin-bottom: 14px;
    }
    .brand{display:flex; flex-direction:column; gap:2px}
    .brand h1{margin:0; font-size: 18px; letter-spacing:.2px}
    .brand .sub{color:var(--muted); font-size:12px}

    .actions{display:flex; gap:10px; align-items:center}
    .btn{
      border:1px solid var(--stroke);
      background: var(--card);
      color: var(--text);
      padding: 10px 12px;
      border-radius: 12px;
      cursor:pointer;
      box-shadow: var(--shadow);
      font-weight: 600;
      font-size: 12px;
    }
    .btn:active{transform: translateY(1px)}
    .btn.primary{
      border-color: transparent;
      background: linear-gradient(135deg, var(--accent), #00d4ff);
      color: #0b0c0f;
    }

    .kpis{
      display:grid;
      grid-template-columns: repeat(5, minmax(180px,1fr));
      gap: 12px;
      margin-bottom: 14px;
    }
    @media (max-width: 1100px){
      .kpis{grid-template-columns: repeat(2, minmax(180px,1fr));}
    }
    .kpi{
      background: var(--card);
      border:1px solid var(--stroke);
      border-radius: 16px;
      padding: 14px;
      box-shadow: var(--shadow);
    }
    .kpi .label{color:var(--muted); font-size:12px}
    .kpi .value{font-size:26px; font-weight: 800; margin-top: 6px}
    .kpi .hint{color:var(--muted); font-size:12px; margin-top: 8px}

    .filters{
      background: var(--card);
      border:1px solid var(--stroke);
      border-radius: 16px;
      padding: 14px;
      box-shadow: var(--shadow);
      margin-bottom: 14px;
    }
    .filters form{
      display:grid;
      grid-template-columns: repeat(7, minmax(150px,1fr));
      gap: 10px;
      align-items:end;
    }
    @media (max-width: 1100px){
      .filters form{grid-template-columns: repeat(2, minmax(150px,1fr));}
    }
    label{display:flex; flex-direction:column; gap:6px; font-size:12px; color: var(--muted)}
    input{
      padding: 10px 10px;
      border-radius: 12px;
      border:1px solid var(--stroke);
      outline:none;
      background: var(--input);
      color: var(--text);
    }
    .row{
      display:flex; gap:10px; flex-wrap:wrap; align-items:center; margin-top: 10px;
      color: var(--muted); font-size: 12px;
    }
    .chip{
      display:inline-flex; align-items:center; gap:8px;
      padding: 8px 10px;
      border-radius: 999px;
      background: var(--chip);
      border: 1px solid var(--stroke);
    }
    .link{color: var(--text); text-decoration:none; font-weight:600}

    .grid{
      display:grid;
      grid-template-columns: repeat(auto-fit, minmax(420px, 1fr));
      gap: 14px;
      align-items: start;
    }
    .card{
      background: var(--card);
      border: 1px solid var(--stroke);
      border-radius: 16px;
      padding: 14px;
      box-shadow: var(--shadow);
      position: relative;
      overflow: hidden;
    }
    .card h3{margin:0 0 8px 0; font-size: 14px; font-weight:800; letter-spacing:.2px}
    .card .meta{color: var(--muted); font-size: 12px; margin-bottom: 10px}

    .chartwrap{
      border: 1px solid var(--stroke);
      border-radius: 14px;
      overflow: hidden;
      background: rgba(0,0,0,.08);
    }
    [data-theme="light"] .chartwrap{background: rgba(2,6,23,.03);}
    canvas{width:100%; height: 320px; display:block;}

    .cardtools{
      display:flex; gap:8px; align-items:center; justify-content:flex-end;
      margin-top: 10px;
    }
    .small{
      padding: 8px 10px;
      border-radius: 10px;
      font-size: 12px;
      box-shadow: none;
    }
    .note{
      margin-top: 8px;
      color: var(--muted);
      font-size: 12px;
    }

    /* tooltip */
    .tooltip{
      position: fixed;
      pointer-events:none;
      z-index: 9999;
      background: rgba(0,0,0,.88);
      color: #fff;
      padding: 8px 10px;
      border-radius: 10px;
      font-size: 12px;
      border: 1px solid rgba(255,255,255,.12);
      transform: translate(-50%, calc(-100% - 12px));
      max-width: 360px;
      display:none;
      white-space: nowrap;
    }
    [data-theme="light"] .tooltip{
      background: rgba(2,6,23,.92);
    }
  </style>
</head>

<body>
  <div class="wrap">

    <div class="topbar">
      <div class="brand">
        <h1>Analytics</h1>
        <div class="sub">SQLite + PHP + Canvas · Filters applied to KPIs and charts</div>
      </div>
      <div class="actions">
        <button class="btn" id="toggleTheme" type="button">Toggle theme</button>
        <a class="btn primary" href="<?= h(strtok((string)($_SERVER['REQUEST_URI'] ?? ''), '?')) ?>">Reset filters</a>
      </div>
    </div>

    <div class="kpis">
      <div class="kpi">
        <div class="label">Total events</div>
        <div class="value"><?= h((string)$kpi_total) ?></div>
        <div class="hint">All event types</div>
      </div>
      <div class="kpi">
        <div class="label">Unique IPs</div>
        <div class="value"><?= h((string)$kpi_ips) ?></div>
        <div class="hint">COUNT(DISTINCT ip)</div>
      </div>
      <div class="kpi">
        <div class="label">Unique sessions</div>
        <div class="value"><?= h((string)$kpi_sess) ?></div>
        <div class="hint">COUNT(DISTINCT session_id)</div>
      </div>
      <div class="kpi">
        <div class="label">Views</div>
        <div class="value"><?= h((string)$kpi_views) ?></div>
        <div class="hint">event_type = view</div>
      </div>
      <div class="kpi">
        <div class="label">Clicks</div>
        <div class="value"><?= h((string)$kpi_clicks) ?></div>
        <div class="hint">event_type = click</div>
      </div>
    </div>

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
          <input name="host" value="<?= h((string)($_GET['host'] ?? '')) ?>" placeholder="example.com">
        </label>
        <label>exclude_bots (1/empty)
          <input name="exclude_bots" value="<?= h((string)($_GET['exclude_bots'] ?? '')) ?>" placeholder="1">
        </label>

        <button class="btn primary" type="submit">Apply</button>
      </form>

      <div class="row">
        <span class="chip">Active filters: <strong><?= h($filtersLine) ?></strong></span>

        <!-- quick ranges (client-side helpers) -->
        <span class="chip">
          Quick:
          <a class="link" href="#" data-quick="7d">Last 7d</a> ·
          <a class="link" href="#" data-quick="30d">Last 30d</a> ·
          <a class="link" href="#" data-quick="mtd">MTD</a>
        </span>
      </div>
    </div>

    <div class="grid">
      <?php foreach ($charts as $ch): ?>
        <?php
          $data = consulta_array($db, $ch['sql'], $PARAMS);
          $payload = [
            'id' => $ch['id'],
            'title' => $ch['title'],
            'type' => $ch['type'],
            'data' => $data,
            'options' => $ch['options'] ?? new stdClass(),
            'filters' => $filtersLine,
          ];
        ?>
        <div class="card">
          <h3><?= h($ch['title']) ?></h3>
          <div class="meta"><?= h($ch['type']) ?> · filters: <?= h($filtersLine) ?></div>

          <div class="chartwrap">
            <canvas id="<?= h($ch['id']) ?>" data-chart="1"></canvas>
          </div>

          <div class="cardtools">
            <button class="btn small" type="button" data-export="png" data-target="<?= h($ch['id']) ?>">Export PNG</button>
            <button class="btn small" type="button" data-export="csv" data-target="<?= h($ch['id']) ?>">Export CSV</button>
          </div>

          <?php
				  $json = json_encode(
					 $payload,
					 JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES
				  );

				  // Evita que aparezca accidentalmente </script> dentro del JSON
				  $json = str_replace('</', '<\/', $json);
				?>
				<script type="application/json" data-payload="<?= h($ch['id']) ?>">
				<?= $json ?>
				</script>

        </div>
      <?php endforeach; ?>
    </div>

  </div>

  <div class="tooltip" id="tt"></div>
<script defer src="analytics.js"></script>
  <script>
    // quick ranges
    (function(){
      function pad(n){ return String(n).padStart(2,'0'); }
      function fmt(d){ return d.getFullYear()+'-'+pad(d.getMonth()+1)+'-'+pad(d.getDate()); }

      function setParam(url, k, v){
        if (v === null || v === '') { url.searchParams.delete(k); return; }
        url.searchParams.set(k, v);
      }

      document.querySelectorAll('[data-quick]').forEach(a=>{
        a.addEventListener('click', (e)=>{
          e.preventDefault();
          const mode = a.getAttribute('data-quick');
          const now = new Date();
          const url = new URL(window.location.href);

          if (mode === '7d' || mode === '30d'){
            const days = (mode === '7d') ? 7 : 30;
            const from = new Date(now.getTime() - (days*24*60*60*1000));
            setParam(url, 'from', fmt(from));
            setParam(url, 'to', fmt(now));
          }
          if (mode === 'mtd'){
            const from = new Date(now.getFullYear(), now.getMonth(), 1);
            setParam(url, 'from', fmt(from));
            setParam(url, 'to', fmt(now));
          }
          window.location.href = url.toString();
        });
      });
    })();

    // theme toggle (persist)
    (function(){
      const key = 'analytics_theme';
      const root = document.documentElement;
      const btn = document.getElementById('toggleTheme');

      function apply(t){
        root.setAttribute('data-theme', t);
        localStorage.setItem(key, t);
      }

      const saved = localStorage.getItem(key);
      if (saved === 'light' || saved === 'dark') apply(saved);

      btn.addEventListener('click', ()=>{
        const cur = root.getAttribute('data-theme') || 'dark';
        apply(cur === 'dark' ? 'light' : 'dark');
      });
    })();
  </script>
</body>
</html>

