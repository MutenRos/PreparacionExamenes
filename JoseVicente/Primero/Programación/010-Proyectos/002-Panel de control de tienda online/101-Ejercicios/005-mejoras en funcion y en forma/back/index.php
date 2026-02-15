<?php
session_start();

/* ==========================
   1. LOGIN SENCILLO
   ========================== */
if (isset($_POST['usuario'], $_POST['contrasena'])) {
    if ($_POST['usuario'] === 'jocarsa' && $_POST['contrasena'] === 'jocarsa') {
        $_SESSION['usuario'] = 'jocarsa';
    } else {
        $error_login = "Usuario o contraseña incorrectos.";
    }
}

// Logout opcional
if (isset($_GET['logout'])) {
    session_destroy();
    header("Location: ?");
    exit;
}

/* ==========================
   2. SI NO ESTÁ LOGUEADO: FORMULARIO
   ========================== */
if (!isset($_SESSION['usuario']) || $_SESSION['usuario'] !== 'jocarsa') {
    ?>
    <!doctype html>
    <html>
    <head>
      <meta charset="utf-8">
      <title>Panel de control</title>
      <style>
        :root{
          --color-principal:#ff8a00;
          --color-principal-oscuro:#e67600;
          --color-fondo:#f5f5f7;
          --color-texto:#222;
          --radio:14px;
          --sombra:0 12px 30px rgba(0,0,0,0.15);
        }
        *{box-sizing:border-box;font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;}
        html,body{padding:0;margin:0;width:100%;height:100%;}
        body{
          display:flex;
          justify-content:center;
          align-items:center;
          background:radial-gradient(circle at top left,#ffe3b0,var(--color-principal));
        }
        .card-login{
          width:320px;
          padding:30px 24px;
          background:white;
          border-radius:var(--radio);
          box-shadow:var(--sombra);
          display:flex;
          flex-direction:column;
          gap:18px;
        }
        .card-login h1{
          margin:0;
          font-size:1.4rem;
          text-align:center;
          color:var(--color-texto);
        }
        .card-login label{
          font-size:.87rem;
          color:#555;
        }
        .card-login input[type="text"],
        .card-login input[type="password"]{
          padding:10px 12px;
          border-radius:10px;
          border:1px solid #ddd;
          width:100%;
          outline:none;
          transition:border .2s, box-shadow .2s;
        }
        .card-login input[type="text"]:focus,
        .card-login input[type="password"]:focus{
          border-color:var(--color-principal);
          box-shadow:0 0 0 3px rgba(255,138,0,0.25);
        }
        .card-login input[type="submit"]{
          margin-top:8px;
          padding:10px 14px;
          border-radius:999px;
          border:none;
          cursor:pointer;
          background:linear-gradient(135deg,var(--color-principal),var(--color-principal-oscuro));
          color:white;
          font-weight:600;
          letter-spacing:.03em;
          text-transform:uppercase;
          font-size:.8rem;
        }
        .card-login input[type="submit"]:hover{
          filter:brightness(1.05);
        }
        .error{
          background:#ffe0e0;
          color:#a00000;
          padding:8px 10px;
          border-radius:8px;
          font-size:.8rem;
        }
      </style>
    </head>
    <body>
      <form method="POST" action="?" class="card-login">
        <h1>Acceso al panel</h1>
        <?php if(isset($error_login)): ?>
          <div class="error"><?php echo htmlspecialchars($error_login); ?></div>
        <?php endif; ?>
        <div>
          <label>Usuario</label>
          <input type="text" name="usuario" autocomplete="off">
        </div>
        <div>
          <label>Contraseña</label>
          <input type="password" name="contrasena">
        </div>
        <input type="submit" value="Entrar">
      </form>
    </body>
    </html>
    <?php
    exit;
}

/* ==========================
   3. CONEXIÓN COMÚN
   ========================== */
$conexion = new mysqli("localhost", "tiendadam", "Tiendadam123$", "tiendadam");
if ($conexion->connect_errno) {
    die("Error de conexión: ".$conexion->connect_error);
}
$conexion->set_charset("utf8mb4");

/* ==========================
   4. RUTADO BÁSICO
   ========================== */
$tabla  = isset($_GET['tabla']) ? $_GET['tabla'] : 'producto';
$accion = isset($_GET['accion']) ? $_GET['accion'] : 'listar';

// Solo permitimos estas tablas para evitar inyecciones
$tablas_permitidas = ['producto','cliente','pedido'];
if (!in_array($tabla, $tablas_permitidas)) {
    $tabla = 'producto';
}

/* ==========================
   5. FUNCIONES AUXILIARES
   ========================== */
function h($str){
    return htmlspecialchars($str ?? '', ENT_QUOTES, 'UTF-8');
}

/* ==========================
   6. LÓGICA CRUD POR TABLA
   ========================== */

// ---- PRODUCTO ----
if ($tabla === 'producto') {

    // Crear
    if ($accion === 'crear' && $_SERVER['REQUEST_METHOD']==='POST') {
        $titulo      = $_POST['titulo'] ?? '';
        $descripcion = $_POST['descripcion'] ?? '';
        $precio      = $_POST['precio'] ?? '';
        $imagen      = $_POST['imagen'] ?? '';

        $stmt = $conexion->prepare("INSERT INTO producto (titulo, descripcion, precio, imagen) VALUES (?,?,?,?)");
        $stmt->bind_param("ssss", $titulo, $descripcion, $precio, $imagen);
        $stmt->execute();
        $stmt->close();
        header("Location: ?tabla=producto&accion=listar");
        exit;
    }

    // Actualizar
    if ($accion === 'actualizar' && $_SERVER['REQUEST_METHOD']==='POST' && isset($_GET['id'])) {
        $id          = (int)$_GET['id'];
        $titulo      = $_POST['titulo'] ?? '';
        $descripcion = $_POST['descripcion'] ?? '';
        $precio      = $_POST['precio'] ?? '';
        $imagen      = $_POST['imagen'] ?? '';

        $stmt = $conexion->prepare("UPDATE producto SET titulo=?, descripcion=?, precio=?, imagen=? WHERE id=?");
        $stmt->bind_param("ssssi", $titulo, $descripcion, $precio, $imagen, $id);
        $stmt->execute();
        $stmt->close();
        header("Location: ?tabla=producto&accion=listar");
        exit;
    }

    // Borrar
    if ($accion === 'borrar' && isset($_GET['id'])) {
        $id = (int)$_GET['id'];
        // Borramos posibles líneas de pedido que usen ese producto
        $conexion->query("DELETE FROM lineapedido WHERE producto_id=".$id);
        $conexion->query("DELETE FROM producto WHERE id=".$id);
        header("Location: ?tabla=producto&accion=listar");
        exit;
    }
}

// ---- CLIENTE ----
if ($tabla === 'cliente') {

    // Crear
    if ($accion === 'crear' && $_SERVER['REQUEST_METHOD']==='POST') {
        $nombre    = $_POST['nombre'] ?? '';
        $apellidos = $_POST['apellidos'] ?? '';
        $email     = $_POST['email'] ?? '';

        $stmt = $conexion->prepare("INSERT INTO cliente (nombre, apellidos, email) VALUES (?,?,?)");
        $stmt->bind_param("sss", $nombre, $apellidos, $email);
        $stmt->execute();
        $stmt->close();
        header("Location: ?tabla=cliente&accion=listar");
        exit;
    }

    // Actualizar
    if ($accion === 'actualizar' && $_SERVER['REQUEST_METHOD']==='POST' && isset($_GET['id'])) {
        $id        = (int)$_GET['id'];
        $nombre    = $_POST['nombre'] ?? '';
        $apellidos = $_POST['apellidos'] ?? '';
        $email     = $_POST['email'] ?? '';

        $stmt = $conexion->prepare("UPDATE cliente SET nombre=?, apellidos=?, email=? WHERE id=?");
        $stmt->bind_param("sssi", $nombre, $apellidos, $email, $id);
        $stmt->execute();
        $stmt->close();
        header("Location: ?tabla=cliente&accion=listar");
        exit;
    }

    // Borrar
    if ($accion === 'borrar' && isset($_GET['id'])) {
        $id = (int)$_GET['id'];
        // Borrado en cascada manual: lineas -> pedidos -> cliente
        $resPed = $conexion->query("SELECT id FROM pedido WHERE cliente_id=".$id);
        while($p = $resPed->fetch_assoc()){
            $conexion->query("DELETE FROM lineapedido WHERE pedido_id=".$p['id']);
        }
        $conexion->query("DELETE FROM pedido WHERE cliente_id=".$id);
        $conexion->query("DELETE FROM cliente WHERE id=".$id);
        header("Location: ?tabla=cliente&accion=listar");
        exit;
    }
}

// ---- PEDIDO + LINEAPEDIDO ----
if ($tabla === 'pedido') {

    // Crear pedido
    if ($accion === 'crear' && $_SERVER['REQUEST_METHOD']==='POST') {
        $fecha      = $_POST['fecha'] ?? date("Y-m-d");
        $cliente_id = (int)($_POST['cliente_id'] ?? 0);

        $stmt = $conexion->prepare("INSERT INTO pedido (fecha, cliente_id) VALUES (?,?)");
        $stmt->bind_param("si", $fecha, $cliente_id);
        $stmt->execute();
        $nuevo_id = $stmt->insert_id;
        $stmt->close();
        header("Location: ?tabla=pedido&accion=detalle&id=".$nuevo_id);
        exit;
    }

    // Borrar pedido completo
    if ($accion === 'borrar' && isset($_GET['id'])) {
        $id = (int)$_GET['id'];
        $conexion->query("DELETE FROM lineapedido WHERE pedido_id=".$id);
        $conexion->query("DELETE FROM pedido WHERE id=".$id);
        header("Location: ?tabla=pedido&accion=listar");
        exit;
    }

    // Añadir línea
    if ($accion === 'agregar_linea' && $_SERVER['REQUEST_METHOD']==='POST' && isset($_GET['id'])) {
        $pedido_id   = (int)$_GET['id'];
        $producto_id = (int)($_POST['producto_id'] ?? 0);
        $cantidad    = $_POST['cantidad'] ?? '1';

        $stmt = $conexion->prepare("INSERT INTO lineapedido (pedido_id, producto_id, cantidad) VALUES (?,?,?)");
        $stmt->bind_param("iis", $pedido_id, $producto_id, $cantidad);
        $stmt->execute();
        $stmt->close();
        header("Location: ?tabla=pedido&accion=detalle&id=".$pedido_id);
        exit;
    }

    // Borrar línea
    if ($accion === 'borrar_linea' && isset($_GET['id'], $_GET['linea_id'])) {
        $pedido_id = (int)$_GET['id'];
        $linea_id  = (int)$_GET['linea_id'];
        $conexion->query("DELETE FROM lineapedido WHERE id=".$linea_id);
        header("Location: ?tabla=pedido&accion=detalle&id=".$pedido_id);
        exit;
    }
}

?>
<!doctype html>
<html>
  <head>
    <meta charset="utf-8">
    <title>Panel de control</title>
    <style>
      :root{
        --color-principal:#ff8a00;
        --color-principal-oscuro:#e67600;
        --color-principal-suave:#fff1dd;
        --color-fondo:#f5f5f7;
        --color-nav:#1f1f23;
        --color-texto:#222;
        --radio:14px;
        --sombra-suave:0 10px 25px rgba(0,0,0,0.1);
        --borde-suave:1px solid rgba(0,0,0,0.06);
      }
      *{box-sizing:border-box;font-family:system-ui,-apple-system,BlinkMacSystemFont,"Segoe UI",sans-serif;}
      html,body{padding:0;margin:0;width:100%;height:100%;}
      body{
        display:flex;
        background:radial-gradient(circle at top left,#fff8ee,#ffe4bd);
        color:var(--color-texto);
      }
      nav{
        background:linear-gradient(180deg,#25252b,#17171b);
        width:230px;
        padding:20px 16px;
        display:flex;
        flex-direction:column;
        gap:18px;
        color:white;
      }
      nav .brand{
        font-size:1.1rem;
        font-weight:700;
        letter-spacing:.05em;
        text-transform:uppercase;
        padding:6px 4px 12px;
        border-bottom:1px solid rgba(255,255,255,0.08);
        display:flex;
        justify-content:space-between;
        align-items:center;
      }
      nav .brand span.logo-dot{
        width:18px;height:18px;border-radius:999px;
        background:radial-gradient(circle at 30% 30%,#ffe7c1,var(--color-principal));
        box-shadow:0 0 12px rgba(255,138,0,0.7);
      }
      nav .section-title{
        font-size:.78rem;
        text-transform:uppercase;
        letter-spacing:.12em;
        color:rgba(255,255,255,0.55);
        margin-top:10px;
      }
      nav a{
        background:transparent;
        padding:9px 10px;
        color:rgba(255,255,255,0.85);
        text-decoration:none;
        font-size:.9rem;
        border-radius:999px;
        display:flex;
        align-items:center;
        gap:8px;
        border:1px solid transparent;
        transition:background .15s, border .15s, transform .1s;
      }
      nav a span.icon{font-size:1.1rem;}
      nav a:hover{
        background:rgba(255,255,255,0.06);
        border-color:rgba(255,255,255,0.08);
        transform:translateY(-1px);
      }
      nav a.activo{
        background:linear-gradient(135deg,var(--color-principal),var(--color-principal-oscuro));
        color:#1b1203;
        box-shadow:0 8px 18px rgba(0,0,0,0.4);
      }
      nav .logout{
        margin-top:auto;
        font-size:.8rem;
        opacity:.8;
      }

      main{
        flex:1;
        padding:24px 32px;
        display:flex;
        flex-direction:column;
        gap:18px;
        overflow:auto;
      }
      header.panel-header{
        display:flex;
        justify-content:space-between;
        align-items:center;
        gap:10px;
      }
      .panel-header h1{
        margin:0;
        font-size:1.4rem;
      }
      .badge{
        display:inline-flex;
        align-items:center;
        gap:6px;
        padding:4px 10px;
        border-radius:999px;
        background:var(--color-principal-suave);
        color:var(--color-principal-oscuro);
        font-size:.78rem;
        font-weight:500;
      }

      .card{
        background:white;
        border-radius:var(--radio);
        padding:16px 18px;
        box-shadow:var(--sombra-suave);
        border:var(--borde-suave);
      }
      .card-header{
        display:flex;
        justify-content:space-between;
        align-items:center;
        margin-bottom:10px;
      }
      .card-header h2{
        margin:0;
        font-size:1.05rem;
      }
      .btn{
        display:inline-flex;
        align-items:center;
        gap:6px;
        padding:7px 12px;
        font-size:.82rem;
        border-radius:999px;
        border:none;
        cursor:pointer;
        text-decoration:none;
        background:var(--color-principal);
        color:#2b1400;
        font-weight:500;
        box-shadow:0 4px 10px rgba(0,0,0,0.15);
      }
      .btn:hover{filter:brightness(1.05);}
      .btn-secundario{
        background:transparent;
        color:#555;
        box-shadow:none;
        border:1px solid #ddd;
      }
      .btn-peligro{
        background:#ff4d4d;
        color:white;
        box-shadow:0 4px 10px rgba(255,77,77,0.4);
      }

      table{
        width:100%;
        border-collapse:collapse;
        font-size:.88rem;
      }
      table th, table td{
        padding:8px 10px;
        text-align:left;
        border-bottom:1px solid #eee;
      }
      table th{
        background:linear-gradient(180deg,#ffe6c4,var(--color-principal-suave));
        position:sticky;
        top:0;
        z-index:1;
      }
      table tr:nth-child(even) td{
        background:#fafafa;
      }
      table tr:hover td{
        background:#fff5e8;
      }
      .acciones{
        display:flex;
        gap:6px;
        flex-wrap:wrap;
      }

      form.form-inline,
      form.form-grid{
        display:flex;
        flex-wrap:wrap;
        gap:12px 16px;
        align-items:flex-end;
      }
      form.form-grid{
        margin-top:10px;
      }
      .campo{
        display:flex;
        flex-direction:column;
        gap:4px;
        min-width:180px;
        flex:1;
      }
      .campo label{
        font-size:.8rem;
        color:#555;
      }
      .campo input, .campo select{
        padding:8px 9px;
        border-radius:9px;
        border:1px solid #ddd;
        font-size:.86rem;
        outline:none;
        transition:border .2s, box-shadow .2s, background .2s;
      }
      .campo input:focus, .campo select:focus{
        border-color:var(--color-principal);
        box-shadow:0 0 0 2px rgba(255,138,0,0.25);
        background:#fffdf8;
      }

      .tag{
        display:inline-flex;
        padding:2px 8px;
        border-radius:999px;
        font-size:.75rem;
        background:#eee;
      }
      .tag-ok{background:#d8fadd;color:#155724;}
      .tag-info{background:#e0f0ff;color:#004085;}
      .tag-warn{background:#fff3cd;color:#856404;}
    </style>
  </head>
  <body>
    <nav>
      <div class="brand">
        <div>Panel tienda</div>
        <span class="logo-dot"></span>
      </div>
      <div class="section-title">Gestión</div>
      <a href="?tabla=producto" class="<?php echo $tabla==='producto'?'activo':''; ?>">
        <span class="icon">📦</span><span>Productos</span>
      </a>
      <a href="?tabla=cliente" class="<?php echo $tabla==='cliente'?'activo':''; ?>">
        <span class="icon">👤</span><span>Clientes</span>
      </a>
      <a href="?tabla=pedido" class="<?php echo $tabla==='pedido'?'activo':''; ?>">
        <span class="icon">🧾</span><span>Pedidos</span>
      </a>

      <a href="?logout=1" class="logout">
        <span class="icon">🚪</span> Cerrar sesión
      </a>
    </nav>
    <main>
      <header class="panel-header">
        <h1>
          <?php
            if ($tabla==='producto') echo "Productos";
            elseif ($tabla==='cliente') echo "Clientes";
            else echo "Pedidos";
          ?>
        </h1>
        <div class="badge">
          <span>Panel activo</span> <span>●</span>
        </div>
      </header>

      <?php if ($tabla === 'producto'): ?>

        <?php if ($accion === 'listar'): ?>
          <section class="card">
            <div class="card-header">
              <h2>Listado de productos</h2>
              <a class="btn" href="?tabla=producto&accion=nuevo">➕ Nuevo producto</a>
            </div>
            <table>
              <tr>
                <th>ID</th>
                <th>Título</th>
                <th>Descripción</th>
                <th>Precio</th>
                <th>Imagen</th>
                <th>Acciones</th>
              </tr>
              <?php
              $res = $conexion->query("SELECT * FROM producto ORDER BY id DESC");
              while($fila = $res->fetch_assoc()):
              ?>
                <tr>
                  <td><?php echo h($fila['id']); ?></td>
                  <td><?php echo h($fila['titulo']); ?></td>
                  <td><?php echo h($fila['descripcion']); ?></td>
                  <td><?php echo h($fila['precio']); ?></td>
                  <td><?php echo h($fila['imagen']); ?></td>
                  <td class="acciones">
                    <a class="btn btn-secundario" href="?tabla=producto&accion=editar&id=<?php echo $fila['id']; ?>">✏️ Editar</a>
                    <a class="btn btn-peligro" href="?tabla=producto&accion=borrar&id=<?php echo $fila['id']; ?>" onclick="return confirm('¿Borrar este producto?');">🗑 Borrar</a>
                  </td>
                </tr>
              <?php endwhile; ?>
            </table>
          </section>

        <?php elseif ($accion === 'nuevo'): ?>
          <section class="card">
            <div class="card-header">
              <h2>Nuevo producto</h2>
            </div>
            <form method="POST" action="?tabla=producto&accion=crear" class="form-grid">
              <div class="campo">
                <label>Título</label>
                <input type="text" name="titulo" required>
              </div>
              <div class="campo">
                <label>Descripción</label>
                <input type="text" name="descripcion">
              </div>
              <div class="campo">
                <label>Precio</label>
                <input type="text" name="precio">
              </div>
              <div class="campo">
                <label>Imagen (URL o ruta)</label>
                <input type="text" name="imagen">
              </div>
              <button type="submit" class="btn">💾 Guardar</button>
              <a href="?tabla=producto" class="btn btn-secundario">← Volver</a>
            </form>
          </section>

        <?php elseif ($accion === 'editar' && isset($_GET['id'])): ?>
          <?php
            $id = (int)$_GET['id'];
            $res = $conexion->query("SELECT * FROM producto WHERE id=".$id);
            $prod = $res->fetch_assoc();
          ?>
          <section class="card">
            <div class="card-header">
              <h2>Editar producto #<?php echo h($id); ?></h2>
            </div>
            <?php if($prod): ?>
              <form method="POST" action="?tabla=producto&accion=actualizar&id=<?php echo $id; ?>" class="form-grid">
                <div class="campo">
                  <label>Título</label>
                  <input type="text" name="titulo" value="<?php echo h($prod['titulo']); ?>" required>
                </div>
                <div class="campo">
                  <label>Descripción</label>
                  <input type="text" name="descripcion" value="<?php echo h($prod['descripcion']); ?>">
                </div>
                <div class="campo">
                  <label>Precio</label>
                  <input type="text" name="precio" value="<?php echo h($prod['precio']); ?>">
                </div>
                <div class="campo">
                  <label>Imagen (URL o ruta)</label>
                  <input type="text" name="imagen" value="<?php echo h($prod['imagen']); ?>">
                </div>
                <button type="submit" class="btn">💾 Guardar cambios</button>
                <a href="?tabla=producto" class="btn btn-secundario">← Volver</a>
              </form>
            <?php else: ?>
              <p>Producto no encontrado.</p>
            <?php endif; ?>
          </section>
        <?php endif; ?>

      <?php elseif ($tabla === 'cliente'): ?>

        <?php if ($accion === 'listar'): ?>
          <section class="card">
            <div class="card-header">
              <h2>Listado de clientes</h2>
              <a class="btn" href="?tabla=cliente&accion=nuevo">➕ Nuevo cliente</a>
            </div>
            <table>
              <tr>
                <th>ID</th>
                <th>Nombre</th>
                <th>Apellidos</th>
                <th>Email</th>
                <th>Acciones</th>
              </tr>
              <?php
              $res = $conexion->query("SELECT * FROM cliente ORDER BY id DESC");
              while($fila = $res->fetch_assoc()):
              ?>
                <tr>
                  <td><?php echo h($fila['id']); ?></td>
                  <td><?php echo h($fila['nombre']); ?></td>
                  <td><?php echo h($fila['apellidos']); ?></td>
                  <td><?php echo h($fila['email']); ?></td>
                  <td class="acciones">
                    <a class="btn btn-secundario" href="?tabla=cliente&accion=editar&id=<?php echo $fila['id']; ?>">✏️ Editar</a>
                    <a class="btn btn-peligro" href="?tabla=cliente&accion=borrar&id=<?php echo $fila['id']; ?>" onclick="return confirm('Se borrará el cliente y sus pedidos asociados. ¿Continuar?');">🗑 Borrar</a>
                  </td>
                </tr>
              <?php endwhile; ?>
            </table>
          </section>

        <?php elseif ($accion === 'nuevo'): ?>
          <section class="card">
            <div class="card-header">
              <h2>Nuevo cliente</h2>
            </div>
            <form method="POST" action="?tabla=cliente&accion=crear" class="form-grid">
              <div class="campo">
                <label>Nombre</label>
                <input type="text" name="nombre" required>
              </div>
              <div class="campo">
                <label>Apellidos</label>
                <input type="text" name="apellidos">
              </div>
              <div class="campo">
                <label>Email</label>
                <input type="email" name="email">
              </div>
              <button type="submit" class="btn">💾 Guardar</button>
              <a href="?tabla=cliente" class="btn btn-secundario">← Volver</a>
            </form>
          </section>

        <?php elseif ($accion === 'editar' && isset($_GET['id'])): ?>
          <?php
            $id = (int)$_GET['id'];
            $res = $conexion->query("SELECT * FROM cliente WHERE id=".$id);
            $cli = $res->fetch_assoc();
          ?>
          <section class="card">
            <div class="card-header">
              <h2>Editar cliente #<?php echo h($id); ?></h2>
            </div>
            <?php if($cli): ?>
              <form method="POST" action="?tabla=cliente&accion=actualizar&id=<?php echo $id; ?>" class="form-grid">
                <div class="campo">
                  <label>Nombre</label>
                  <input type="text" name="nombre" value="<?php echo h($cli['nombre']); ?>" required>
                </div>
                <div class="campo">
                  <label>Apellidos</label>
                  <input type="text" name="apellidos" value="<?php echo h($cli['apellidos']); ?>">
                </div>
                <div class="campo">
                  <label>Email</label>
                  <input type="email" name="email" value="<?php echo h($cli['email']); ?>">
                </div>
                <button type="submit" class="btn">💾 Guardar cambios</button>
                <a href="?tabla=cliente" class="btn btn-secundario">← Volver</a>
              </form>
            <?php else: ?>
              <p>Cliente no encontrado.</p>
            <?php endif; ?>
          </section>
        <?php endif; ?>

      <?php elseif ($tabla === 'pedido'): ?>

        <?php if ($accion === 'listar'): ?>
          <section class="card">
            <div class="card-header">
              <h2>Pedidos</h2>
              <a class="btn" href="?tabla=pedido&accion=nuevo">➕ Nuevo pedido</a>
            </div>
            <table>
              <tr>
                <th>ID</th>
                <th>Fecha</th>
                <th>Cliente</th>
                <th>Líneas</th>
                <th>Acciones</th>
              </tr>
              <?php
              $sql = "SELECT p.id, p.fecha, c.nombre, c.apellidos,
                             (SELECT COUNT(*) FROM lineapedido l WHERE l.pedido_id=p.id) AS num_lineas
                      FROM pedido p
                      LEFT JOIN cliente c ON p.cliente_id=c.id
                      ORDER BY p.id DESC";
              $res = $conexion->query($sql);
              while($fila = $res->fetch_assoc()):
              ?>
                <tr>
                  <td><?php echo h($fila['id']); ?></td>
                  <td><?php echo h($fila['fecha']); ?></td>
                  <td><?php echo h(trim(($fila['nombre'] ?? '')." ".($fila['apellidos'] ?? ''))); ?></td>
                  <td>
                    <span class="tag <?php echo ($fila['num_lineas']>0?'tag-ok':'tag-info'); ?>">
                      <?php echo (int)$fila['num_lineas']; ?> líneas
                    </span>
                  </td>
                  <td class="acciones">
                    <a class="btn btn-secundario" href="?tabla=pedido&accion=detalle&id=<?php echo $fila['id']; ?>">🔍 Ver/editar</a>
                    <a class="btn btn-peligro" href="?tabla=pedido&accion=borrar&id=<?php echo $fila['id']; ?>" onclick="return confirm('¿Borrar este pedido y sus líneas?');">🗑 Borrar</a>
                  </td>
                </tr>
              <?php endwhile; ?>
            </table>
          </section>

        <?php elseif ($accion === 'nuevo'): ?>
          <section class="card">
            <div class="card-header">
              <h2>Nuevo pedido</h2>
            </div>
            <form method="POST" action="?tabla=pedido&accion=crear" class="form-grid">
              <div class="campo">
                <label>Fecha</label>
                <input type="date" name="fecha" value="<?php echo date('Y-m-d'); ?>">
              </div>
              <div class="campo">
                <label>Cliente</label>
                <select name="cliente_id" required>
                  <option value="">-- Selecciona cliente --</option>
                  <?php
                  $resCli = $conexion->query("SELECT * FROM cliente ORDER BY apellidos, nombre");
                  while($c = $resCli->fetch_assoc()):
                  ?>
                    <option value="<?php echo $c['id']; ?>">
                      <?php echo h(trim($c['apellidos']." ".$c['nombre'])); ?>
                    </option>
                  <?php endwhile; ?>
                </select>
              </div>
              <button type="submit" class="btn">💾 Crear pedido</button>
              <a href="?tabla=pedido" class="btn btn-secundario">← Volver</a>
            </form>
          </section>

        <?php elseif ($accion === 'detalle' && isset($_GET['id'])): ?>
          <?php
            $id = (int)$_GET['id'];
            $sql = "SELECT p.*, c.nombre, c.apellidos
                    FROM pedido p
                    LEFT JOIN cliente c ON p.cliente_id=c.id
                    WHERE p.id=".$id;
            $res = $conexion->query($sql);
            $ped = $res->fetch_assoc();
          ?>
          <section class="card">
            <div class="card-header">
              <h2>Pedido #<?php echo h($id); ?></h2>
              <a href="?tabla=pedido" class="btn btn-secundario">← Volver a pedidos</a>
            </div>
            <?php if($ped): ?>
              <p>
                <strong>Fecha:</strong> <?php echo h($ped['fecha']); ?><br>
                <strong>Cliente:</strong> <?php echo h(trim(($ped['apellidos'] ?? '')." ".($ped['nombre'] ?? ''))); ?>
              </p>

              <h3>Líneas de pedido</h3>
              <table>
                <tr>
                  <th>ID línea</th>
                  <th>Producto</th>
                  <th>Cantidad</th>
                  <th>Acciones</th>
                </tr>
                <?php
                $sqlLineas = "SELECT l.id, l.cantidad, pr.titulo
                              FROM lineapedido l
                              LEFT JOIN producto pr ON l.producto_id=pr.id
                              WHERE l.pedido_id=".$id."
                              ORDER BY l.id ASC";
                $resLin = $conexion->query($sqlLineas);
                while($lin = $resLin->fetch_assoc()):
                ?>
                  <tr>
                    <td><?php echo h($lin['id']); ?></td>
                    <td><?php echo h($lin['titulo']); ?></td>
                    <td><?php echo h($lin['cantidad']); ?></td>
                    <td>
                      <a class="btn btn-peligro" href="?tabla=pedido&accion=borrar_linea&id=<?php echo $id; ?>&linea_id=<?php echo $lin['id']; ?>" onclick="return confirm('¿Borrar esta línea?');">🗑 Borrar línea</a>
                    </td>
                  </tr>
                <?php endwhile; ?>
              </table>

              <h3 style="margin-top:18px;">Añadir nueva línea</h3>
              <form method="POST" action="?tabla=pedido&accion=agregar_linea&id=<?php echo $id; ?>" class="form-inline">
                <div class="campo">
                  <label>Producto</label>
                  <select name="producto_id" required>
                    <option value="">-- Selecciona producto --</option>
                    <?php
                    $resProd = $conexion->query("SELECT * FROM producto ORDER BY titulo");
                    while($p = $resProd->fetch_assoc()):
                    ?>
                      <option value="<?php echo $p['id']; ?>">
                        <?php echo h($p['titulo']); ?>
                      </option>
                    <?php endwhile; ?>
                  </select>
                </div>
                <div class="campo" style="max-width:120px;">
                  <label>Cantidad</label>
                  <input type="number" name="cantidad" value="1" min="1">
                </div>
                <button type="submit" class="btn">➕ Añadir línea</button>
              </form>
            <?php else: ?>
              <p>Pedido no encontrado.</p>
            <?php endif; ?>
          </section>
        <?php endif; ?>

      <?php endif; ?>

    </main>
  </body>
</html>

