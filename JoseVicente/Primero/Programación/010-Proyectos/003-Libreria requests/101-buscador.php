<?php
/*  emails_search.php  (single-file mini search engine)
    - Put this file in the SAME folder as emails_found.sqlite
    - Open in browser: http://localhost/emails_search.php
*/

declare(strict_types=1);
error_reporting(E_ALL);
ini_set('display_errors', '1');

$dbPath = __DIR__ . '/emails_found.sqlite';
if (!file_exists($dbPath)) {
  http_response_code(500);
  echo "DB not found: " . htmlspecialchars($dbPath, ENT_QUOTES, 'UTF-8');
  exit;
}

function h(string $s): string { return htmlspecialchars($s, ENT_QUOTES, 'UTF-8'); }

$q     = trim((string)($_GET['q'] ?? ''));
$field = (string)($_GET['field'] ?? 'all');     // all|email|url|title
$sort  = (string)($_GET['sort'] ?? 'last');     // last|first|email
$dir   = strtoupper((string)($_GET['dir'] ?? 'DESC')); // ASC|DESC
$dir   = in_array($dir, ['ASC','DESC'], true) ? $dir : 'DESC';
$page  = max(1, (int)($_GET['page'] ?? 1));
$per   = min(200, max(10, (int)($_GET['per'] ?? 25)));

$sortMap = [
  'last'  => 'last_seen',
  'first' => 'first_seen',
  'email' => 'email'
];
$orderBy = $sortMap[$sort] ?? 'last_seen';

$where = '';
$params = [];
if ($q !== '') {
  $like = '%' . $q . '%';
  switch ($field) {
    case 'email':
      $where = 'WHERE email LIKE :q';
      break;
    case 'url':
      $where = 'WHERE url LIKE :q';
      break;
    case 'title':
      $where = 'WHERE title LIKE :q';
      break;
    default:
      $where = 'WHERE email LIKE :q OR url LIKE :q OR title LIKE :q';
      break;
  }
  $params[':q'] = $like;
}

$pdo = new PDO('sqlite:' . $dbPath, null, null, [
  PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION,
  PDO::ATTR_DEFAULT_FETCH_MODE => PDO::FETCH_ASSOC,
]);

// Count
$countSql = "SELECT COUNT(*) AS c FROM found_emails $where";
$stmt = $pdo->prepare($countSql);
$stmt->execute($params);
$total = (int)$stmt->fetch()['c'];

$pages = max(1, (int)ceil($total / $per));
$page = min($page, $pages);
$offset = ($page - 1) * $per;

// Data
$dataSql = "
  SELECT email, url, title, first_seen, last_seen
  FROM found_emails
  $where
  ORDER BY $orderBy $dir
  LIMIT :limit OFFSET :offset
";
$stmt = $pdo->prepare($dataSql);
foreach ($params as $k => $v) $stmt->bindValue($k, $v, PDO::PARAM_STR);
$stmt->bindValue(':limit', $per, PDO::PARAM_INT);
$stmt->bindValue(':offset', $offset, PDO::PARAM_INT);
$stmt->execute();
$rows = $stmt->fetchAll();

function build_url(array $overrides = []): string {
  $base = $_GET;
  foreach ($overrides as $k => $v) {
    if ($v === null) unset($base[$k]);
    else $base[$k] = $v;
  }
  return '?' . http_build_query($base);
}

function arrow(string $col, string $currentSort, string $currentDir): string {
  if ($col !== $currentSort) return '';
  return $currentDir === 'ASC' ? ' ▲' : ' ▼';
}

?>
<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Email DB Search</title>
  <style>
    :root{
      --bg:#0b0c10;
      --card:#11131a;
      --muted:#8b93a7;
      --text:#e7eaf2;
      --border:#23283a;
      --accent:#6aa6ff;
      --accent2:#7ee787;
      --danger:#ff6a6a;
      --shadow: 0 10px 30px rgba(0,0,0,.35);
      --radius:16px;
    }
    *{box-sizing:border-box}
    body{
      margin:0;
      font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Arial, "Noto Sans", "Liberation Sans", sans-serif;
      background: radial-gradient(1200px 800px at 10% 10%, rgba(106,166,255,.12), transparent 40%),
                  radial-gradient(1200px 800px at 90% 30%, rgba(126,231,135,.10), transparent 45%),
                  var(--bg);
      color:var(--text);
    }
    .wrap{max-width:1100px;margin:28px auto;padding:0 16px}
    header{
      display:flex; gap:14px; align-items:flex-start; justify-content:space-between;
      margin-bottom:16px;
    }
    .title h1{margin:0;font-size:20px;letter-spacing:.2px}
    .title p{margin:6px 0 0;color:var(--muted);font-size:13px}
    .card{
      background: linear-gradient(180deg, rgba(255,255,255,.03), rgba(255,255,255,.01));
      border:1px solid var(--border);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      padding:14px;
    }
    form{
      display:grid;
      grid-template-columns: 1fr 160px 130px 110px 90px auto;
      gap:10px;
      align-items:center;
    }
    @media (max-width: 900px){
      form{grid-template-columns: 1fr 1fr; }
      .span2{grid-column: span 2;}
    }
    input[type="text"], select{
      width:100%;
      padding:10px 12px;
      border-radius:12px;
      border:1px solid var(--border);
      background:#0f1220;
      color:var(--text);
      outline:none;
    }
    input[type="text"]::placeholder{color:#6b738a}
    button{
      padding:10px 12px;
      border-radius:12px;
      border:1px solid var(--border);
      background: #10162a;
      color:var(--text);
      cursor:pointer;
    }
    button.primary{
      background: linear-gradient(180deg, rgba(106,166,255,.25), rgba(106,166,255,.12));
      border-color: rgba(106,166,255,.35);
    }
    a.btn{
      display:inline-block;
      padding:10px 12px;
      border-radius:12px;
      border:1px solid var(--border);
      text-decoration:none;
      color:var(--text);
      background:#0f1220;
      text-align:center;
    }
    .meta{
      display:flex; gap:10px; align-items:center; justify-content:space-between;
      margin-top:12px;
      color:var(--muted);
      font-size:13px;
      flex-wrap:wrap;
    }
    table{
      width:100%;
      border-collapse:separate;
      border-spacing:0;
      margin-top:14px;
      overflow:hidden;
      border-radius: var(--radius);
      border:1px solid var(--border);
    }
    thead th{
      text-align:left;
      font-size:12px;
      color:var(--muted);
      padding:12px 12px;
      background:#0f1220;
      border-bottom:1px solid var(--border);
      white-space:nowrap;
    }
    tbody td{
      padding:12px 12px;
      border-bottom:1px solid rgba(35,40,58,.65);
      vertical-align:top;
      font-size:13px;
    }
    tbody tr:hover{background:rgba(255,255,255,.03)}
    tbody tr:last-child td{border-bottom:0}
    .pill{
      display:inline-block;
      padding:2px 8px;
      border-radius:999px;
      font-size:12px;
      border:1px solid rgba(255,255,255,.10);
      color:var(--muted);
      background: rgba(255,255,255,.02);
    }
    .email{font-weight:600}
    .url a{
      color: var(--accent);
      text-decoration:none;
      word-break:break-all;
    }
    .url a:hover{text-decoration:underline}
    .small{color:var(--muted);font-size:12px}
    .pager{display:flex;gap:8px;align-items:center;flex-wrap:wrap}
    .pager a{
      color:var(--text);
      text-decoration:none;
      padding:8px 10px;
      border:1px solid var(--border);
      border-radius:12px;
      background:#0f1220;
    }
    .pager a.current{
      border-color: rgba(106,166,255,.45);
      background: rgba(106,166,255,.10);
    }
    .right{margin-left:auto}
    .hint{margin-top:8px;color:var(--muted);font-size:12px}
  </style>
</head>
<body>
  <div class="wrap">
    <header>
      <div class="title">
        <h1>Email DB Search</h1>
        <p>Search in <span class="pill"><?=h(basename($dbPath))?></span> • Total: <span class="pill"><?=number_format($total)?></span></p>
      </div>
      <div class="right">
        <a class="btn" href="<?=h(build_url(['q'=>'','page'=>1]))?>">Reset</a>
      </div>
    </header>

    <div class="card">
      <form method="get" action="">
        <input class="span2" type="text" name="q" value="<?=h($q)?>" placeholder="Search (email, url, title)...">
        <select name="field">
          <option value="all"   <?= $field==='all'?'selected':'' ?>>All fields</option>
          <option value="email" <?= $field==='email'?'selected':'' ?>>Email</option>
          <option value="url"   <?= $field==='url'?'selected':'' ?>>URL</option>
          <option value="title" <?= $field==='title'?'selected':'' ?>>Title</option>
        </select>
        <select name="sort">
          <option value="last"  <?= $sort==='last'?'selected':'' ?>>Sort: last_seen</option>
          <option value="first" <?= $sort==='first'?'selected':'' ?>>Sort: first_seen</option>
          <option value="email" <?= $sort==='email'?'selected':'' ?>>Sort: email</option>
        </select>
        <select name="dir">
          <option value="DESC" <?= $dir==='DESC'?'selected':'' ?>>DESC</option>
          <option value="ASC"  <?= $dir==='ASC'?'selected':'' ?>>ASC</option>
        </select>
        <select name="per">
          <?php foreach ([10,25,50,100,200] as $n): ?>
            <option value="<?=$n?>" <?= $per===$n?'selected':'' ?>><?=$n?> / page</option>
          <?php endforeach; ?>
        </select>
        <button class="primary" type="submit">Search</button>
      </form>

      <div class="meta">
        <div>
          Showing <span class="pill"><?=number_format($total ? ($offset+1) : 0)?></span>
          –
          <span class="pill"><?=number_format(min($offset + $per, $total))?></span>
          of <span class="pill"><?=number_format($total)?></span>
        </div>
        <div class="pager">
          <?php
            $basePageUrl = function(int $p) { return build_url(['page'=>$p]); };
            $prev = max(1, $page-1);
            $next = min($pages, $page+1);
          ?>
          <a href="<?=h($basePageUrl(1))?>">« First</a>
          <a href="<?=h($basePageUrl($prev))?>">‹ Prev</a>

          <?php
            $start = max(1, $page-2);
            $end   = min($pages, $page+2);
            for ($p=$start; $p<=$end; $p++):
          ?>
            <a class="<?= $p===$page ? 'current' : '' ?>" href="<?=h($basePageUrl($p))?>"><?= $p ?></a>
          <?php endfor; ?>

          <a href="<?=h($basePageUrl($next))?>">Next ›</a>
          <a href="<?=h($basePageUrl($pages))?>">Last »</a>
        </div>
      </div>

      <table>
        <thead>
          <tr>
            <th>
              <a style="color:inherit;text-decoration:none"
                 href="<?=h(build_url(['sort'=>'email','dir'=>($sort==='email' && $dir==='ASC')?'DESC':'ASC','page'=>1]))?>">
                Email<?=arrow('email',$sort,$dir)?>
              </a>
            </th>
            <th>Title</th>
            <th>URL</th>
            <th>
              <a style="color:inherit;text-decoration:none"
                 href="<?=h(build_url(['sort'=>'first','dir'=>($sort==='first' && $dir==='ASC')?'DESC':'ASC','page'=>1]))?>">
                First seen<?=arrow('first',$sort,$dir)?>
              </a>
            </th>
            <th>
              <a style="color:inherit;text-decoration:none"
                 href="<?=h(build_url(['sort'=>'last','dir'=>($sort==='last' && $dir==='ASC')?'DESC':'ASC','page'=>1]))?>">
                Last seen<?=arrow('last',$sort,$dir)?>
              </a>
            </th>
          </tr>
        </thead>
        <tbody>
          <?php if (!$rows): ?>
            <tr><td colspan="5" class="small">No results.</td></tr>
          <?php else: ?>
            <?php foreach ($rows as $r): ?>
              <tr>
                <td class="email"><?=h((string)$r['email'])?></td>
                <td><?=h((string)($r['title'] ?? ''))?></td>
                <td class="url">
                  <?php if (!empty($r['url'])): ?>
                    <a href="<?=h((string)$r['url'])?>" target="_blank" rel="noopener"><?=h((string)$r['url'])?></a>
                  <?php endif; ?>
                </td>
                <td class="small"><?=h((string)$r['first_seen'])?></td>
                <td class="small"><?=h((string)$r['last_seen'])?></td>
              </tr>
            <?php endforeach; ?>
          <?php endif; ?>
        </tbody>
      </table>

      <div class="hint">
        Tips: search by partial text (e.g. <span class="pill">@tameformacion</span>), use field selector to narrow results.
      </div>
    </div>
  </div>
</body>
</html>

