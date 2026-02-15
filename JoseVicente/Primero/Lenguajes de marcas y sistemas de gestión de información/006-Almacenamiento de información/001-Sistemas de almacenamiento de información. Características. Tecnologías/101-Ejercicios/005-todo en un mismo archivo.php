<?php
  if(isset($_GET['operacion']) && $_GET['operacion'] == "insertar"){
    $mysqli = new mysqli("localhost", "discos", "discos", "discos");
    $sql = "
      INSERT INTO discos
      VALUES(
        NULL,
        '".$_POST['titulo']."',
        '".$_POST['artista']."',
        '".$_POST['anio']."',
        '".$_POST['genero']."',
        '".$_POST['duracion_minutos']."',
        '".$_POST['fecha_compra']."',
        '".$_POST['precio']."'
      );
    ";
    $result = $mysqli->query($sql);
  }
?>
<!doctype html>
<html>
  <head>
  </head>
  <body>
    <form action="?operacion=insertar" method="POST">
      <input type="text" name="titulo" placeholder="titulo">
      <input type="text" name="artista" placeholder="artista">
      <input type="text" name="anio" placeholder="anio">
      <input type="text" name="genero" placeholder="genero">
      <input type="number" name="duracion_minutos" placeholder="duracion_minutos">
      <input type="date" name="fecha_compra" placeholder="fecha_compra">
      <input type="number" name="precio" placeholder="precio">
      <input type="submit">
    </form>
  </body>
</html>
