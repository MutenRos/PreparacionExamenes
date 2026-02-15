<?php
// Me conecto a la base de datos
$mysqli = new mysqli("localhost", "discos", "discos", "discos");

// Ahora le pido algo a las entradas
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

?>

