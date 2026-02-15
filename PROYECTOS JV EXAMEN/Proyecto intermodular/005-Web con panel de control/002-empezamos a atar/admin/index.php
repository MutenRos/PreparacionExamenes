<?php
  session_start();

  $error = "";

  if($_SERVER['REQUEST_METHOD'] === 'POST'){
    $u = isset($_POST['usuario']) ? (string)$_POST['usuario'] : "";
    $p = isset($_POST['contrasena']) ? (string)$_POST['contrasena'] : "";

    if($u === "jocarsa" && $p === "jocarsa"){
      $_SESSION['admin_ok'] = 1;
      header("Location: escritorio.php");
      exit;
    }else{
      $error = "Usuario o contraseña incorrectos";
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
    </style>
  </head>

  <body class="flex fa-center fj-center w-100pc h-100pc p-0 m-0">
    <form method="post" class="w-300 p-20 flex fd-column g-15 card shadow-1">
      <h2 class="m-0 c-teal ta-center">Acceso</h2>
      <input name="usuario" type="text" placeholder="usuario" class="p-10 bradius-10 br-1-solid-lightgray" required minlength="3">
      <input name="contrasena" type="password" placeholder="contraseña" class="p-10 bradius-10 br-1-solid-lightgray" required minlength="3">
      <input type="submit" value="Entrar" class="p-10 btn-teal">

      <?php if($error){ ?>
        <p class="m-0 muted ta-center"><?= htmlspecialchars($error, ENT_QUOTES, "UTF-8") ?></p>
      <?php } ?>
    </form>
  </body>
</html>

