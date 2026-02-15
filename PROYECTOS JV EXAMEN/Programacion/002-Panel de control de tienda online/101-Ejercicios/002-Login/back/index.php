<?php
  session_start();
  if(isset($_POST['usuario'])){
    if($_POST['usuario'] == 'jocarsa' && $_POST['contrasena'] == 'jocarsa'){
      $_SESSION['usuario'] = 'jocarsa';
    }
  }
?>
<?php
  if(isset($_SESSION['usuario'])){
    if($_SESSION['usuario'] == 'jocarsa'){
  }
?>
  Te voy a mostrar el panel de control
<?php
  }else{ 
?>
<!doctype html>
<html>
  <head>
    <style>
      html,body{padding:0px;margin:0px;width:100%;height:100%;}
      body{display:flex;justify-content:center;align-items:center;background:orange;}
      form{width:200px;height:200px;padding:20px;background:white;display:flex;flex-direction:column;gap:20px;justify-content:center;}
      form input{padding:10px;}
    </style>
  </head>
  <body>
    <form method="POST" action="?"><input type="text" name="usuario"><input type="password" name="contrasena">
    <input type="submit"></form>
  </body>
</html>
<?php
  }
?>
