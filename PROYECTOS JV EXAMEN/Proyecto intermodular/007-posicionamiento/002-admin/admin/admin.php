<?php
declare(strict_types=1);

/*
  admin.php (admin/admin.php)
  - Panel admin (login + CRUD categorias/productos + analítica logs)
  - DB: ../recortables.db

  Notas:
  - Este admin crea el usuario jocarsa/jocarsa si no existe (como tu versión actual).
  - Usa PDO SQLite con consultas preparadas.
  - Incluye CSRF simple para acciones POST.
*/

session_start();

$db_path = __DIR__ . '/../recortables.db';

function e(string $s): string { return htmlspecialchars($s, ENT_QUOTES, 'UTF-8'); }
function is_post(): bool { return ($_SERVER['REQUEST_METHOD'] ?? '') === 'POST'; }

function csrf_token(): string {
  if (empty($_SESSION['_csrf'])) $_SESSION['_csrf'] = bin2hex(random_bytes(16));
  return (string)$_SESSION['_csrf'];
}
function csrf_check(): bool {
  if (!is_post()) return true;
  $in = (string)($_POST['_csrf'] ?? '');
  $ss = (string)($_SESSION['_csrf'] ?? '');
  return $in !== '' && $ss !== '' && hash_equals($ss, $in);
}

function redirect(string $to): void {
  header("Location: $to");
  exit;
}

$flash = $_SESSION['_flash'] ?? null;
unset($_SESSION['_flash']);
function flash(string $msg): void {
  $_SESSION['_flash'] = $msg;
}

try {
  $db = new PDO('sqlite:' . $db_path);
  $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
  $db->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_ASSOC);
  $db->exec("PRAGMA foreign_keys = ON");

  // Asegurar tabla users (tu front ya la crea, pero aquí lo garantizamos)
  $db->exec("
    CREATE TABLE IF NOT EXISTS users (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      username TEXT NOT NULL,
      email TEXT NOT NULL UNIQUE,
      password_hash TEXT NOT NULL,
      created_at TEXT NOT NULL DEFAULT (datetime('now'))
    );
  ");
  $db->exec("CREATE UNIQUE INDEX IF NOT EXISTS idx_users_email ON users(email)");
  $db->exec("CREATE UNIQUE INDEX IF NOT EXISTS idx_users_username ON users(username)");

  // Crear usuario jocarsa/jocarsa si no existe
  $st = $db->prepare("SELECT id FROM users WHERE username = :u LIMIT 1");
  $st->execute([':u' => 'jocarsa']);
  $exists = $st->fetchColumn();

  if (!$exists) {
    $hash = password_hash('jocarsa', PASSWORD_DEFAULT);
    $ins = $db->prepare("INSERT INTO users (username, email, password_hash) VALUES (:u,:e,:p)");
    $ins->execute([
      ':u' => 'jocarsa',
      ':e' => 'jocarsa@example.com',
      ':p' => $hash
    ]);
  }

  // Asegurar tabla logs (según tu log.php)
  $db->exec("
    CREATE TABLE IF NOT EXISTS logs (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      created_at TEXT NOT NULL,

      ip TEXT,
      ip_raw TEXT,

      method TEXT,
      scheme TEXT,
      host TEXT,
      url TEXT,
      path TEXT,
      query_string TEXT,

      referer TEXT,
      user_agent TEXT,

      accept TEXT,
      accept_language TEXT,
      accept_encoding TEXT,
      dnt TEXT,

      session_id TEXT,
      user_id INTEGER,

      remote_port INTEGER,
      server_ip TEXT,
      server_port INTEGER,
      protocol TEXT,

      headers_json TEXT,
      server_json TEXT,
      cookies_json TEXT
    );
  ");
  $db->exec("CREATE INDEX IF NOT EXISTS idx_logs_created_at ON logs(created_at)");
  $db->exec("CREATE INDEX IF NOT EXISTS idx_logs_path ON logs(path)");
  $db->exec("CREATE INDEX IF NOT EXISTS idx_logs_ip ON logs(ip)");

} catch (Throwable $ex) {
  http_response_code(500);
  echo "Error DB: " . e($ex->getMessage());
  exit;
}

/* ===========================
   AUTH (login/logout)
=========================== */
if (isset($_GET['logout'])) {
  session_destroy();
  redirect('admin.php');
}

if (isset($_POST['login'])) {
  if (!csrf_check()) {
    flash('Sesión caducada. Reintenta.');
    redirect('admin.php');
  }

  $username = trim((string)($_POST['username'] ?? ''));
  $password = (string)($_POST['password'] ?? '');

  if ($username === '' || $password === '') {
    $error = "Completa usuario y contraseña.";
  } else {
    $stmt = $db->prepare("SELECT id, username, password_hash FROM users WHERE username = :u LIMIT 1");
    $stmt->execute([':u' => $username]);
    $user = $stmt->fetch();

    if ($user && password_verify($password, (string)$user['password_hash'])) {
      session_regenerate_id(true);
      $_SESSION['admin_user_id'] = (int)$user['id'];
      $_SESSION['admin_username'] = (string)$user['username'];
      redirect('admin.php');
    } else {
      $error = "Usuario o contraseña incorrectos.";
    }
  }
}

$logged = isset($_SESSION['admin_user_id']);

/* ===========================
   Helpers CRUD
=========================== */
function q_single(PDO $db, string $sql, array $params = []) {
  $st = $db->prepare($sql);
  $st->execute($params);
  return $st->fetchColumn();
}

function q_all(PDO $db, string $sql, array $params = []): array {
  $st = $db->prepare($sql);
  $st->execute($params);
  return $st->fetchAll();
}

/* ===========================
   CRUD actions (solo si logged)
=========================== */
if ($logged && is_post()) {
  if (!csrf_check()) {
    flash('Sesión caducada. Reintenta.');
    redirect('admin.php');
  }

  $action = (string)($_POST['action'] ?? '');

  // CATEGORIAS
  if ($action === 'cat_save') {
    $id     = (int)($_POST['id'] ?? 0);
    $titulo = trim((string)($_POST['titulo'] ?? ''));
    $imagen = trim((string)($_POST['imagen'] ?? ''));

    if ($titulo === '') {
      flash('La categoría debe tener título.');
      redirect('admin.php?section=categorias');
    }

    if ($id > 0) {
      $st = $db->prepare("UPDATE categorias SET titulo = :t, imagen = :i WHERE Identificador = :id");
      $st->execute([':t'=>$titulo, ':i'=>$imagen, ':id'=>$id]);
      flash('Categoría actualizada.');
    } else {
      $st = $db->prepare("INSERT INTO categorias (titulo, imagen) VALUES (:t,:i)");
      $st->execute([':t'=>$titulo, ':i'=>$imagen]);
      flash('Categoría creada.');
    }
    redirect('admin.php?section=categorias');
  }

  if ($action === 'cat_delete') {
    $id = (int)($_POST['id'] ?? 0);
    if ($id > 0) {
      // Si hay productos asociados, puedes decidir qué hacer:
      // - bloquear borrado, o
      // - poner categoria = NULL/0 (depende de tu esquema)
      // Aquí: bloqueamos si hay productos.
      $cnt = (int)q_single($db, "SELECT COUNT(*) FROM productos WHERE categoria = :id", [':id'=>$id]);
      if ($cnt > 0) {
        flash("No se puede borrar: hay $cnt producto(s) en esta categoría.");
      } else {
        $st = $db->prepare("DELETE FROM categorias WHERE Identificador = :id");
        $st->execute([':id'=>$id]);
        flash('Categoría borrada.');
      }
    }
    redirect('admin.php?section=categorias');
  }

  // PRODUCTOS
  if ($action === 'prod_save') {
    $id = (int)($_POST['id'] ?? 0);

    $titulo = trim((string)($_POST['titulo'] ?? ''));
    $descripcion = trim((string)($_POST['descripcion'] ?? ''));
    $precio = trim((string)($_POST['precio'] ?? ''));
    $archivo = trim((string)($_POST['archivo'] ?? ''));
    $categoria = (int)($_POST['categoria'] ?? 0);
    $imagen = trim((string)($_POST['imagen'] ?? ''));

    if ($titulo === '') {
      flash('El producto debe tener título.');
      redirect('admin.php?section=productos');
    }

    // precio: lo guardamos como texto si tu esquema es texto; si es numérico, lo puedes normalizar.
    if ($id > 0) {
      $st = $db->prepare("
        UPDATE productos
        SET titulo = :t, descripcion = :d, precio = :p, archivo = :a, categoria = :c, imagen = :i
        WHERE Identificador = :id
      ");
      $st->execute([
        ':t'=>$titulo, ':d'=>$descripcion, ':p'=>$precio, ':a'=>$archivo, ':c'=>$categoria, ':i'=>$imagen, ':id'=>$id
      ]);
      flash('Producto actualizado.');
    } else {
      $st = $db->prepare("
        INSERT INTO productos (titulo, descripcion, precio, archivo, categoria, imagen)
        VALUES (:t,:d,:p,:a,:c,:i)
      ");
      $st->execute([
        ':t'=>$titulo, ':d'=>$descripcion, ':p'=>$precio, ':a'=>$archivo, ':c'=>$categoria, ':i'=>$imagen
      ]);
      flash('Producto creado.');
    }
    redirect('admin.php?section=productos');
  }

  if ($action === 'prod_delete') {
    $id = (int)($_POST['id'] ?? 0);
    if ($id > 0) {
      $st = $db->prepare("DELETE FROM productos WHERE Identificador = :id");
      $st->execute([':id'=>$id]);
      flash('Producto borrado.');
    }
    redirect('admin.php?section=productos');
  }
}

/* ===========================
   UI routing
=========================== */
$section = (string)($_GET['section'] ?? 'categorias');
$allowed = ['categorias','productos','analitica'];
if (!in_array($section, $allowed, true)) $section = 'categorias';

// edit load
$edit_cat_id = (int)($_GET['edit_cat'] ?? 0);
$edit_prod_id = (int)($_GET['edit_prod'] ?? 0);

$cat_edit = null;
$prod_edit = null;

if ($logged && $section === 'categorias' && $edit_cat_id > 0) {
  $st = $db->prepare("SELECT Identificador, titulo, imagen FROM categorias WHERE Identificador = :id LIMIT 1");
  $st->execute([':id'=>$edit_cat_id]);
  $cat_edit = $st->fetch() ?: null;
}
if ($logged && $section === 'productos' && $edit_prod_id > 0) {
  $st = $db->prepare("SELECT * FROM productos WHERE Identificador = :id LIMIT 1");
  $st->execute([':id'=>$edit_prod_id]);
  $prod_edit = $st->fetch() ?: null;
}

// Data common
$csrf = csrf_token();

?><!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1">
  <title>Administración · recortabl.es</title>
  <link rel="stylesheet" href="estilo.css">
</head>
<body>

<?php if (!$logged): ?>
  <div class="login-shell">
    <div class="login-card">
      <div class="login-brand">
        <div class="badge">⚙️</div>
        <div>
          <div class="brand-title">Panel de administración</div>
          <div class="brand-sub">recortabl.es</div>
        </div>
      </div>

      <?php if ($flash): ?>
        <div class="notice"><?= e((string)$flash) ?></div>
      <?php endif; ?>

      <?php if (!empty($error)): ?>
        <div class="notice danger"><?= e((string)$error) ?></div>
      <?php endif; ?>

      <form method="post" class="form">
        <input type="hidden" name="_csrf" value="<?= e($csrf) ?>">
        <label>
          <span>Usuario</span>
          <input type="text" name="username" placeholder="jocarsa" required autofocus>
        </label>
        <label>
          <span>Contraseña</span>
          <input type="password" name="password" placeholder="••••••••" required>
        </label>

        <button class="btn primary" type="submit" name="login">Entrar</button>
        <p class="help">Usuario por defecto: <b>jocarsa</b> · Contraseña: <b>jocarsa</b></p>
      </form>
    </div>
  </div>

<?php else: ?>

  <div class="app">
    <aside class="sidebar">
      <div class="side-head">
        <div class="badge">🧩</div>
        <div>
          <div class="side-title">Admin</div>
          <div class="side-sub"><?= e((string)($_SESSION['admin_username'] ?? '')) ?></div>
        </div>
      </div>

      <nav class="menu">
        <a class="<?= $section==='categorias'?'active':'' ?>" href="admin.php?section=categorias">Categorías</a>
        <a class="<?= $section==='productos'?'active':'' ?>" href="admin.php?section=productos">Productos</a>
        <a class="<?= $section==='analitica'?'active':'' ?>" href="admin.php?section=analitica">Analítica</a>
      </nav>

      <div class="side-foot">
        <a class="btn ghost" href="../index.php">Ver web</a>
        <a class="btn danger" href="admin.php?logout=1">Cerrar sesión</a>
      </div>
    </aside>

    <main class="main">
      <header class="topbar">
        <div>
          <h1>
            <?php
              if ($section==='categorias') echo 'Categorías';
              elseif ($section==='productos') echo 'Productos';
              else echo 'Analítica';
            ?>
          </h1>
          <p class="muted">
            Base de datos: <code><?= e(basename($db_path)) ?></code>
          </p>
        </div>
      </header>

      <?php if ($flash): ?>
        <div class="notice"><?= e((string)$flash) ?></div>
      <?php endif; ?>

      <?php if ($section === 'categorias'): ?>
        <?php
          $cats = q_all($db, "SELECT Identificador, titulo, imagen FROM categorias ORDER BY Identificador DESC");
          $totalCats = count($cats);
        ?>

        <section class="grid2">
          <div class="card">
            <h2><?= $cat_edit ? 'Editar categoría' : 'Nueva categoría' ?></h2>
            <form method="post" class="form">
              <input type="hidden" name="_csrf" value="<?= e($csrf) ?>">
              <input type="hidden" name="action" value="cat_save">
              <input type="hidden" name="id" value="<?= (int)($cat_edit['Identificador'] ?? 0) ?>">

              <label>
                <span>Título</span>
                <input type="text" name="titulo" required value="<?= e((string)($cat_edit['titulo'] ?? '')) ?>" placeholder="Ej: Vehículos">
              </label>

              <label>
                <span>Imagen (ruta/URL)</span>
                <input type="text" name="imagen" value="<?= e((string)($cat_edit['imagen'] ?? '')) ?>" placeholder="Ej: img/categorias/vehiculos.png">
              </label>

              <div class="row">
                <button class="btn primary" type="submit"><?= $cat_edit ? 'Guardar cambios' : 'Crear categoría' ?></button>
                <?php if ($cat_edit): ?>
                  <a class="btn ghost" href="admin.php?section=categorias">Cancelar</a>
                <?php endif; ?>
              </div>
            </form>
          </div>

          <div class="card">
            <div class="card-head">
              <h2>Listado (<?= (int)$totalCats ?>)</h2>
              <div class="muted">Acciones seguras y consistentes</div>
            </div>

            <div class="table-wrap">
              <table class="table">
                <thead>
                  <tr>
                    <th style="width:90px">ID</th>
                    <th>Título</th>
                    <th>Imagen</th>
                    <th style="width:190px">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  <?php foreach ($cats as $c): ?>
                    <tr>
                      <td><?= (int)$c['Identificador'] ?></td>
                      <td><b><?= e((string)$c['titulo']) ?></b></td>
                      <td class="muted"><?= e((string)$c['imagen']) ?></td>
                      <td>
                        <a class="btn mini" href="admin.php?section=categorias&edit_cat=<?= (int)$c['Identificador'] ?>">Editar</a>

                        <form method="post" class="inline" onsubmit="return confirm('¿Borrar la categoría?');">
                          <input type="hidden" name="_csrf" value="<?= e($csrf) ?>">
                          <input type="hidden" name="action" value="cat_delete">
                          <input type="hidden" name="id" value="<?= (int)$c['Identificador'] ?>">
                          <button class="btn mini danger" type="submit">Borrar</button>
                        </form>
                      </td>
                    </tr>
                  <?php endforeach; ?>

                  <?php if (!$cats): ?>
                    <tr><td colspan="4" class="muted">No hay categorías todavía.</td></tr>
                  <?php endif; ?>
                </tbody>
              </table>
            </div>

            <p class="help">
              Tip: si una categoría tiene productos asociados, el borrado se bloquea (para evitar incoherencias).
            </p>
          </div>
        </section>

      <?php elseif ($section === 'productos'): ?>
        <?php
          $cats = q_all($db, "SELECT Identificador, titulo FROM categorias ORDER BY titulo ASC");
          $prods = q_all($db, "
            SELECT p.Identificador, p.titulo, p.precio, p.archivo, p.imagen, p.categoria,
                   c.titulo AS categoria_titulo
            FROM productos p
            LEFT JOIN categorias c ON c.Identificador = p.categoria
            ORDER BY p.Identificador DESC
          ");
        ?>

        <section class="grid2">
          <div class="card">
            <h2><?= $prod_edit ? 'Editar producto' : 'Nuevo producto' ?></h2>

            <form method="post" class="form">
              <input type="hidden" name="_csrf" value="<?= e($csrf) ?>">
              <input type="hidden" name="action" value="prod_save">
              <input type="hidden" name="id" value="<?= (int)($prod_edit['Identificador'] ?? 0) ?>">

              <label>
                <span>Título</span>
                <input type="text" name="titulo" required value="<?= e((string)($prod_edit['titulo'] ?? '')) ?>" placeholder="Ej: Castillo Medieval">
              </label>

              <label>
                <span>Descripción</span>
                <textarea name="descripcion" rows="5" placeholder="Descripción corta..."><?= e((string)($prod_edit['descripcion'] ?? '')) ?></textarea>
              </label>

              <div class="cols">
                <label>
                  <span>Precio</span>
                  <input type="text" name="precio" value="<?= e((string)($prod_edit['precio'] ?? '')) ?>" placeholder="0.00">
                </label>
                <label>
                  <span>Categoría</span>
                  <select name="categoria">
                    <option value="0">— Sin categoría —</option>
                    <?php foreach ($cats as $c): ?>
                      <?php $sel = ((int)($prod_edit['categoria'] ?? 0) === (int)$c['Identificador']) ? 'selected' : ''; ?>
                      <option value="<?= (int)$c['Identificador'] ?>" <?= $sel ?>>
                        <?= e((string)$c['titulo']) ?>
                      </option>
                    <?php endforeach; ?>
                  </select>
                </label>
              </div>

              <label>
                <span>Archivo (ruta del PDF)</span>
                <input type="text" name="archivo" value="<?= e((string)($prod_edit['archivo'] ?? '')) ?>" placeholder="Ej: pdf/recortable.pdf">
              </label>

              <label>
                <span>Imagen (ruta/URL)</span>
                <input type="text" name="imagen" value="<?= e((string)($prod_edit['imagen'] ?? '')) ?>" placeholder="Ej: img/productos/castillo.png">
              </label>

              <div class="row">
                <button class="btn primary" type="submit"><?= $prod_edit ? 'Guardar cambios' : 'Crear producto' ?></button>
                <?php if ($prod_edit): ?>
                  <a class="btn ghost" href="admin.php?section=productos">Cancelar</a>
                <?php endif; ?>
              </div>
            </form>
          </div>

          <div class="card">
            <div class="card-head">
              <h2>Listado (<?= count($prods) ?>)</h2>
              <div class="muted">Productos de recortabl.es</div>
            </div>

            <div class="table-wrap">
              <table class="table">
                <thead>
                  <tr>
                    <th style="width:90px">ID</th>
                    <th>Título</th>
                    <th style="width:140px">Categoría</th>
                    <th style="width:120px">Precio</th>
                    <th>Archivo</th>
                    <th style="width:190px">Acciones</th>
                  </tr>
                </thead>
                <tbody>
                  <?php foreach ($prods as $p): ?>
                    <tr>
                      <td><?= (int)$p['Identificador'] ?></td>
                      <td><b><?= e((string)$p['titulo']) ?></b></td>
                      <td class="muted"><?= e((string)($p['categoria_titulo'] ?? '—')) ?></td>
                      <td class="muted"><?= e((string)($p['precio'] ?? '')) ?></td>
                      <td class="muted"><?= e((string)($p['archivo'] ?? '')) ?></td>
                      <td>
                        <a class="btn mini" href="admin.php?section=productos&edit_prod=<?= (int)$p['Identificador'] ?>">Editar</a>

                        <form method="post" class="inline" onsubmit="return confirm('¿Borrar el producto?');">
                          <input type="hidden" name="_csrf" value="<?= e($csrf) ?>">
                          <input type="hidden" name="action" value="prod_delete">
                          <input type="hidden" name="id" value="<?= (int)$p['Identificador'] ?>">
                          <button class="btn mini danger" type="submit">Borrar</button>
                        </form>
                      </td>
                    </tr>
                  <?php endforeach; ?>

                  <?php if (!$prods): ?>
                    <tr><td colspan="6" class="muted">No hay productos todavía.</td></tr>
                  <?php endif; ?>
                </tbody>
              </table>
            </div>

            <p class="help">Consejo: usa rutas relativas coherentes (ej. <code>img/...</code>, <code>pdf/...</code>) para simplificar despliegues.</p>
          </div>
        </section>

      <?php else: /* ANALITICA */ ?>

        <?php
          // Filtros
          $q = trim((string)($_GET['q'] ?? ''));
          $from = trim((string)($_GET['from'] ?? ''));
          $to   = trim((string)($_GET['to'] ?? ''));

          // Normalizar fechas (YYYY-MM-DD)
          $fromOk = preg_match('/^\d{4}-\d{2}-\d{2}$/', $from) ? $from : '';
          $toOk   = preg_match('/^\d{4}-\d{2}-\d{2}$/', $to) ? $to : '';

          // KPIs
          $total = (int)q_single($db, "SELECT COUNT(*) FROM logs");
          $last24 = (int)q_single($db, "SELECT COUNT(*) FROM logs WHERE created_at >= datetime('now','-1 day')");
          $uniqIp = (int)q_single($db, "SELECT COUNT(DISTINCT ip) FROM logs WHERE ip IS NOT NULL AND ip != ''");
          $uniqPath = (int)q_single($db, "SELECT COUNT(DISTINCT path) FROM logs WHERE path IS NOT NULL AND path != ''");

          // Top páginas
          $topPages = q_all($db, "
            SELECT COALESCE(path,'') AS k, COUNT(*) AS n
            FROM logs
            WHERE COALESCE(path,'') != ''
            GROUP BY COALESCE(path,'')
            ORDER BY n DESC
            LIMIT 10
          ");

          // Top IPs
          $topIps = q_all($db, "
            SELECT COALESCE(ip,'') AS k, COUNT(*) AS n
            FROM logs
            WHERE COALESCE(ip,'') != ''
            GROUP BY COALESCE(ip,'')
            ORDER BY n DESC
            LIMIT 10
          ");

          // Top referers
          $topRef = q_all($db, "
            SELECT COALESCE(referer,'(directo)') AS k, COUNT(*) AS n
            FROM logs
            GROUP BY COALESCE(referer,'(directo)')
            ORDER BY n DESC
            LIMIT 10
          ");

          // Serie diaria (últimos 14 días)
          $daily = q_all($db, "
            SELECT substr(created_at,1,10) AS d, COUNT(*) AS n
            FROM logs
            WHERE created_at >= datetime('now','-14 day')
            GROUP BY substr(created_at,1,10)
            ORDER BY d ASC
          ");

          // Tabla últimas visitas con filtros
          $where = [];
          $params = [];

          if ($q !== '') {
            $where[] = "(url LIKE :q OR path LIKE :q OR ip LIKE :q OR user_agent LIKE :q OR referer LIKE :q)";
            $params[':q'] = '%' . $q . '%';
          }
          if ($fromOk !== '') {
            $where[] = "created_at >= datetime(:from || ' 00:00:00')";
            $params[':from'] = $fromOk;
          }
          if ($toOk !== '') {
            $where[] = "created_at <= datetime(:to || ' 23:59:59')";
            $params[':to'] = $toOk;
          }

          $sql = "
            SELECT id, created_at, ip, method, path, url, referer, user_agent
            FROM logs
          ";
          if ($where) $sql .= " WHERE " . implode(" AND ", $where);
          $sql .= " ORDER BY datetime(created_at) DESC LIMIT 200";

          $recent = q_all($db, $sql, $params);
        ?>

        <section class="kpis">
          <div class="kpi">
            <div class="kpi-title">Visitas (total)</div>
            <div class="kpi-val"><?= $total ?></div>
          </div>
          <div class="kpi">
            <div class="kpi-title">Últimas 24h</div>
            <div class="kpi-val"><?= $last24 ?></div>
          </div>
          <div class="kpi">
            <div class="kpi-title">IPs únicas</div>
            <div class="kpi-val"><?= $uniqIp ?></div>
          </div>
          <div class="kpi">
            <div class="kpi-title">Páginas únicas</div>
            <div class="kpi-val"><?= $uniqPath ?></div>
          </div>
        </section>

        <section class="grid3">
          <div class="card">
            <h2>Top páginas</h2>
            <div class="mini-list">
              <?php foreach ($topPages as $r): ?>
                <div><span class="mono"><?= e((string)$r['k']) ?></span><b><?= (int)$r['n'] ?></b></div>
              <?php endforeach; ?>
              <?php if (!$topPages): ?><div class="muted">Sin datos.</div><?php endif; ?>
            </div>
          </div>

          <div class="card">
            <h2>Top IPs</h2>
            <div class="mini-list">
              <?php foreach ($topIps as $r): ?>
                <div><span class="mono"><?= e((string)$r['k']) ?></span><b><?= (int)$r['n'] ?></b></div>
              <?php endforeach; ?>
              <?php if (!$topIps): ?><div class="muted">Sin datos.</div><?php endif; ?>
            </div>
          </div>

          <div class="card">
            <h2>Top referers</h2>
            <div class="mini-list">
              <?php foreach ($topRef as $r): ?>
                <div><span class="mono"><?= e((string)$r['k']) ?></span><b><?= (int)$r['n'] ?></b></div>
              <?php endforeach; ?>
              <?php if (!$topRef): ?><div class="muted">Sin datos.</div><?php endif; ?>
            </div>
          </div>
        </section>

        <section class="card">
          <div class="card-head">
            <h2>Serie diaria (últimos 14 días)</h2>
            <div class="muted">Conteo por día</div>
          </div>

          <div class="table-wrap">
            <table class="table compact">
              <thead>
                <tr><th>Día</th><th style="width:160px">Visitas</th></tr>
              </thead>
              <tbody>
                <?php foreach ($daily as $r): ?>
                  <tr>
                    <td class="mono"><?= e((string)$r['d']) ?></td>
                    <td><b><?= (int)$r['n'] ?></b></td>
                  </tr>
                <?php endforeach; ?>
                <?php if (!$daily): ?>
                  <tr><td colspan="2" class="muted">Sin datos.</td></tr>
                <?php endif; ?>
              </tbody>
            </table>
          </div>
        </section>

        <section class="card">
          <div class="card-head">
            <h2>Últimas visitas</h2>
            <div class="muted">Máximo 200 · con filtros</div>
          </div>

          <form method="get" class="filters">
            <input type="hidden" name="section" value="analitica">
            <label>
              <span>Buscar</span>
              <input type="search" name="q" value="<?= e($q) ?>" placeholder="path, ip, user agent, referer...">
            </label>
            <label>
              <span>Desde</span>
              <input type="date" name="from" value="<?= e($fromOk) ?>">
            </label>
            <label>
              <span>Hasta</span>
              <input type="date" name="to" value="<?= e($toOk) ?>">
            </label>
            <div class="row">
              <button class="btn primary" type="submit">Aplicar</button>
              <a class="btn ghost" href="admin.php?section=analitica">Limpiar</a>
            </div>
          </form>

          <div class="table-wrap">
            <table class="table">
              <thead>
                <tr>
                  <th style="width:190px">Fecha</th>
                  <th style="width:150px">IP</th>
                  <th style="width:90px">Método</th>
                  <th>Path / URL</th>
                  <th>Referer</th>
                </tr>
              </thead>
              <tbody>
                <?php foreach ($recent as $r): ?>
                  <tr>
                    <td class="mono"><?= e((string)$r['created_at']) ?></td>
                    <td class="mono"><?= e((string)($r['ip'] ?? '')) ?></td>
                    <td class="mono"><?= e((string)($r['method'] ?? '')) ?></td>
                    <td>
                      <div class="mono"><?= e((string)($r['path'] ?? '')) ?></div>
                      <div class="muted small"><?= e((string)($r['url'] ?? '')) ?></div>
                      <details class="ua">
                        <summary>User-Agent</summary>
                        <div class="muted small"><?= e((string)($r['user_agent'] ?? '')) ?></div>
                      </details>
                    </td>
                    <td class="muted small"><?= e((string)($r['referer'] ?? '(directo)')) ?></td>
                  </tr>
                <?php endforeach; ?>

                <?php if (!$recent): ?>
                  <tr><td colspan="5" class="muted">Sin datos para esos filtros.</td></tr>
                <?php endif; ?>
              </tbody>
            </table>
          </div>
        </section>

      <?php endif; ?>

      <footer class="foot muted">
        Admin recortabl.es · SQLite · <?= e(date('Y-m-d H:i')) ?>
      </footer>
    </main>
  </div>

<?php endif; ?>

</body>
</html>

