<?php
  // Mejora: htmlspecialchars para evitar inyeccion XSS en los datos del formulario
  echo "Tu nombre es: ".htmlspecialchars($_POST['nombre'], ENT_QUOTES, 'UTF-8');
  echo "<br>";
  echo "Tus apellidos son: ".htmlspecialchars($_POST['apellidos'], ENT_QUOTES, 'UTF-8');
?>
