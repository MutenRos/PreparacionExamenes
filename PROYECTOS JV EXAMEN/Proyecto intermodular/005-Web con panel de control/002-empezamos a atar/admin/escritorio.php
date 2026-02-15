<?php
  session_start();
  if(!isset($_SESSION['admin_ok'])){
    header("Location: index.php");
    exit;
  }

  if(isset($_GET['logout'])){
    session_destroy();
    header("Location: index.php");
    exit;
  }

  $c = new mysqli("localhost", "jocarsapress", "jocarsapress", "jocarsapress");
  if($c->connect_error){ die("Error de conexión"); }
  $c->set_charset("utf8mb4");

  function h($s){ return htmlspecialchars((string)$s, ENT_QUOTES | ENT_SUBSTITUTE, "UTF-8"); }

  // Detectar PK (para no asumir Identificador)
  function pk_de($c, $tabla){
    $tabla = preg_replace('/[^a-zA-Z0-9_]/', '', $tabla);
    $r = $c->query("SHOW COLUMNS FROM `$tabla`");
    if(!$r) return "id";
    while($f = $r->fetch_assoc()){
      if(isset($f['Key']) && $f['Key'] === 'PRI'){
        return $f['Field'];
      }
    }
    return "id";
  }

  $s = isset($_GET['s']) ? (string)$_GET['s'] : "paginas";   // seccion
  if($s !== "paginas" && $s !== "entradas"){ $s = "paginas"; }

  $a = isset($_GET['a']) ? (string)$_GET['a'] : "list";     // accion
  if(!in_array($a, ["list","new","edit","delete"], true)){ $a="list"; }

  $tabla = $s;
  $pk = pk_de($c, $tabla);

  // Campos editables (mínimo)
  $fields = [];
  if($s === "paginas"){
    $fields = ["titulo","contenido"];
  }else{
    $fields = ["fecha","titulo","contenido","categorias"];
  }

  // Procesar guardado (new/edit)
  $msg = "";
  if($_SERVER['REQUEST_METHOD'] === 'POST'){
    $post_action = isset($_POST['do']) ? (string)$_POST['do'] : "";
    if($post_action === "save"){
      $data = [];
      foreach($fields as $f){
        $data[$f] = isset($_POST[$f]) ? (string)$_POST[$f] : "";
      }

      // defaults
      if($s === "entradas" && trim($data["fecha"]) === ""){
        $data["fecha"] = date("Y-m-d");
      }

      $id = isset($_POST[$pk]) ? (string)$_POST[$pk] : "";

      if($id === ""){
        // INSERT
        $cols = implode(",", array_map(fn($x)=>"`$x`", array_keys($data)));
        $qs   = implode(",", array_fill(0, count($data), "?"));

        $sql = "INSERT INTO `$tabla` ($cols) VALUES ($qs)";
        $stmt = $c->prepare($sql);

        $types = str_repeat("s", count($data));
        $vals = array_values($data);

        $stmt->bind_param($types, ...$vals);
        if($stmt->execute()){
          $msg = "Guardado";
          $a = "list";
        }else{
          $msg = "Error al guardar";
        }

      }else{
        // UPDATE
        $set = implode(",", array_map(fn($x)=>"`$x` = ?", array_keys($data)));
        $sql = "UPDATE `$tabla` SET $set WHERE `$pk` = ? LIMIT 1";
        $stmt = $c->prepare($sql);

        $types = str_repeat("s", count($data))."s";
        $vals = array_values($data);
        $vals[] = $id;

        $stmt->bind_param($types, ...$vals);
        if($stmt->execute()){
          $msg = "Actualizado";
          $a = "list";
        }else{
          $msg = "Error al actualizar";
        }
      }
    }
  }

  // Procesar delete
  if($a === "delete" && isset($_GET['id'])){
    // Protección CSRF básica: solo aceptar si viene de confirmación JS
    $id = (string)$_GET['id'];
    $stmt = $c->prepare("DELETE FROM `$tabla` WHERE `$pk` = ? LIMIT 1");
    $stmt->bind_param("s", $id);
    if($stmt->execute()){
      $msg = "Eliminado";
      $a = "list";
    }else{
      $msg = "Error al eliminar";
      $a = "list";
    }
  }

  // Cargar item para edit
  $edit = null;
  if($a === "edit" && isset($_GET['id'])){
    $id = (string)$_GET['id'];
    $stmt = $c->prepare("SELECT * FROM `$tabla` WHERE `$pk` = ? LIMIT 1");
    $stmt->bind_param("s", $id);
    $stmt->execute();
    $res = $stmt->get_result();
    if($res && $res->num_rows){ $edit = $res->fetch_assoc(); }
  }

  // Listado
  $rows = [];
  if($a === "list"){
    $order = ($s === "entradas") ? "ORDER BY fecha DESC, `$pk` DESC" : "ORDER BY `$pk` DESC";
    $r = $c->query("SELECT * FROM `$tabla` $order");
    if($r){
      while($f = $r->fetch_assoc()){ $rows[] = $f; }
    }
  }
?>
<!doctype html>
<html class="w-100pc h-100pc p-0 m-0" lang="es">
  <head>
    <meta charset="utf-8">
    <style>
      <?php include("../JVestilo/JVestilo.php"); ?>
      body{background:#f4f7f7;}
      .card{border:1px solid #e6ebef;border-radius:14px;background:white;}
      .btn{border-radius:10px;border:1px solid #d7dee5;background:#eef2f7;}
      .btn-teal{background:teal;color:white;border:1px solid teal;}
      .muted{color:#5b6b78;}
      table{border-collapse:collapse;}
      th,td{padding:10px;border-bottom:1px solid #eef2f7;vertical-align:top;}
      textarea{min-height:220px;}
      input,textarea{width:100%;box-sizing:border-box;transition:border-color 0.2s;}
      input:focus,textarea:focus{border-color:teal;outline:none;}
      tr:hover{background:#f9fbfc;}
    </style>
  </head>

  <body class="w-100pc h-100pc p-0 m-0 flex">

    <nav class="f-1 p-20 flex fd-column g-10" style="background:linear-gradient(180deg, teal, #0ea5a5);">
      <div class="p-10 bradius-14" style="background:rgba(255,255,255,.12);color:white;">
        <div class="fs-16"><strong>Panel</strong></div>
        <div class="fs-10" style="opacity:.9;">JocarsaPress</div>
      </div>

      <a href="?s=paginas" class="p-10 td-none bradius-10" style="background:white;color:teal;">Páginas</a>
      <a href="?s=entradas" class="p-10 td-none bradius-10" style="background:white;color:teal;">Entradas</a>

      <div style="height:10px;"></div>
      <a href="?logout=1" class="p-10 td-none bradius-10" style="background:rgba(255,255,255,.18);color:white;">Salir</a>
    </nav>

    <main class="f-5 p-20">
      <div class="flex fd-row fa-center" style="justify-content:space-between;gap:10px;">
        <h1 class="m-0 c-teal fs-22"><?= $s === "paginas" ? "Páginas" : "Entradas" ?></h1>
        <div class="flex g-10">
          <a class="p-10 btn-teal td-none" href="?s=<?= h($s) ?>&a=new">Nueva</a>
          <a class="p-10 btn td-none c-teal" href="?s=<?= h($s) ?>&a=list">Listado</a>
        </div>
      </div>

      <?php if($msg){ ?>
        <p class="muted"><?= h($msg) ?></p>
      <?php } ?>

      <?php if($a === "list"){ ?>
        <div class="card shadow-1" style="margin-top:15px;overflow:auto;">
          <table class="w-100pc">
            <thead style="background:#eef2f7;">
              <tr>
                <th><?= h($pk) ?></th>
                <?php foreach($fields as $f){ ?>
                  <th><?= h($f) ?></th>
                <?php } ?>
                <th>Acciones</th>
              </tr>
            </thead>
            <tbody>
              <?php foreach($rows as $row){ ?>
                <tr>
                  <td><?= h($row[$pk] ?? "") ?></td>
                  <?php foreach($fields as $f){ ?>
                    <td class="muted" style="max-width:420px;">
                      <?php
                        $val = (string)($row[$f] ?? "");
                        if($f === "contenido"){
                          echo h(mb_substr($val, 0, 180)).(mb_strlen($val)>180 ? "…" : "");
                        }else{
                          echo h($val);
                        }
                      ?>
                    </td>
                  <?php } ?>
                  <td>
                    <a class="td-none c-teal" href="?s=<?= h($s) ?>&a=edit&id=<?= urlencode($row[$pk]) ?>">Editar</a>
                    <span class="muted"> | </span>
                    <a class="td-none" style="color:#b91c1c;" href="?s=<?= h($s) ?>&a=delete&id=<?= urlencode($row[$pk]) ?>" onclick="return confirm('¿Seguro que quieres eliminar este registro? Esta acción no se puede deshacer.')">Eliminar</a>
                  </td>
                </tr>
              <?php } ?>
              <?php if(!count($rows)){ ?>
                <tr><td colspan="<?= 2+count($fields) ?>" class="muted">Sin registros</td></tr>
              <?php } ?>
            </tbody>
          </table>
        </div>

      <?php } else { ?>

        <?php
          $is_edit = ($a === "edit" && $edit);
          $val = function($k) use ($is_edit, $edit){
            if($is_edit && isset($edit[$k])) return (string)$edit[$k];
            return "";
          };
        ?>

        <form method="post" class="card shadow-1 p-20" style="margin-top:15px;">
          <input type="hidden" name="do" value="save">
          <?php if($is_edit){ ?>
            <input type="hidden" name="<?= h($pk) ?>" value="<?= h($edit[$pk]) ?>">
          <?php } ?>

          <?php foreach($fields as $f){ ?>
            <div class="flex fd-column g-5" style="margin-bottom:12px;">
              <label class="muted fs-10"><?= h($f) ?></label>

              <?php if($f === "contenido"){ ?>
                <textarea name="contenido" class="p-10 bradius-10 br-1-solid-lightgray"><?= h($val("contenido")) ?></textarea>
                <div class="muted fs-10">Escribe en Markdown (en el front se renderiza a HTML).</div>

              <?php } else if($f === "fecha"){ ?>
                <input name="fecha" type="date" class="p-10 bradius-10 br-1-solid-lightgray" value="<?= h($val("fecha")) ?>">

              <?php } else { ?>
                <input name="<?= h($f) ?>" type="text" class="p-10 bradius-10 br-1-solid-lightgray" value="<?= h($val($f)) ?>">
              <?php } ?>
            </div>
          <?php } ?>

          <div class="flex g-10">
            <input type="submit" value="Guardar" class="p-10 btn-teal">
            <a class="p-10 btn td-none c-teal" href="?s=<?= h($s) ?>&a=list">Cancelar</a>
          </div>
        </form>

      <?php } ?>

    </main>

  </body>
</html>

