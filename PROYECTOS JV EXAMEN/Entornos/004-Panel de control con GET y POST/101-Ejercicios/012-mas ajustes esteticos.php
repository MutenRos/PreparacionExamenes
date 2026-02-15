<?php
// Mejora: conexion unica a la base de datos (reutilizable)
$mysqli = new mysqli("localhost", "miempresa", "miempresa", "miempresa");

// Mejora: comprobar que el parametro tabla existe antes de usarlo
$tablaSeleccionada = isset($_GET['tabla']) ? $_GET['tabla'] : '';
?>
<!doctype html>
  <html lang="es">
  <head>
    <!-- Mejora: meta charset para codificacion correcta -->
    <meta charset="UTF-8">
    <title>Panel de control — miempresa</title>
    <style>
      html,body{width:100%;height:100%;padding:0px;margin:0px;font-family:sans-serif;}
     body{display:flex;}
      nav{flex:1;background:indigo;color:white;padding:20px;display:flex;flex-direction:column;gap:20px;}
      main{flex:5;background:aliceblue;padding:20px;}
      nav a{border:none;background:white;padding:20px;text-decoration:none;color:indigo;text-transform:uppercase;font-weight:bold;border-radius:5px;display:flex;align-items:center;gap:20px;}
      table{width:100%;border:3px solid indigo;border-collapse:collapse;border-radius:5px;}
      table tr td{padding:10px;}
      table tr th{background:indigo;color:white;padding:10px;}
      .redondeado {
            border: 3px solid indigo;
            border-radius: 5px;
            border-collapse: separate; /* important */
            overflow: hidden;          /* keeps corners clean */
        }
        table tr:nth-child(even){
          background:white;
        }
        .inicial{
          display:block;
          width:20px;
          height:20px;
          background:indigo;
          color:white;
          text-align:center;
          padding:10px;
          border-radius:5px;
          line-height:20px;
        }
        /* Mejora: efecto hover en enlaces del menu */
        nav a:hover{
          background:#e0d0ff;
          transform:scale(1.03);
        }
        nav a{
          transition: background 0.2s ease, transform 0.2s ease;
        }
        /* Mejora: resaltar la tabla seleccionada */
        nav a.activo{
          background:#c7b3ff;
          border:2px solid white;
        }
        /* Mejora: responsive para pantallas pequeñas */
        @media (max-width: 768px){
          body{flex-direction:column;}
          nav{flex-direction:row;flex-wrap:wrap;}
        }

    </style>
  </head>
  <body>
    <nav>
      <?php
        // Mejora: reutilizo la conexion creada arriba en vez de abrir otra
        $sql = "SHOW TABLES";
        $resultado = $mysqli->query($sql);
        while ($fila = $resultado->fetch_assoc()) {
            $nombreTabla = $fila['Tables_in_miempresa'];
            // Mejora: htmlspecialchars para evitar XSS
            $nombreSeguro = htmlspecialchars($nombreTabla, ENT_QUOTES, 'UTF-8');
            // Mejora: clase 'activo' si es la tabla seleccionada
            $claseActivo = ($nombreTabla === $tablaSeleccionada) ? ' activo' : '';
            echo '<a href="?tabla='.$nombreSeguro.'" class="'.$claseActivo.'">
              <span class="inicial">'.$nombreSeguro[0].'</span>
             '.$nombreSeguro.'
             </a>';
        }
      ?>
    </nav>
    <main>
      <?php if ($tablaSeleccionada): ?>
      <table class="redondeado">
        <thead>
          <?php
            ///////////////////////// ESTO MUESTRA LAS CABECERAS
            // Mejora: reutilizo conexion y uso la variable validada
            $sql = "SELECT * FROM `" . $mysqli->real_escape_string($tablaSeleccionada) . "` LIMIT 1;";
            $resultado = $mysqli->query($sql);
            if ($resultado) {
              while ($fila = $resultado->fetch_assoc()) {
                echo "<tr>";
                foreach($fila as $clave=>$valor){
                  // Mejora: htmlspecialchars en las cabeceras
                  echo "<th>".htmlspecialchars($clave, ENT_QUOTES, 'UTF-8')."</th>";
                }
                echo "</tr>";
              }
            }
          ?>
          </thead>
          <tbody>
          <?php
            ///////////////////////// ESTO MUESTRA LOS DATOS
            // Mejora: reutilizo conexion y escapo el nombre de tabla
            $sql = "SELECT * FROM `" . $mysqli->real_escape_string($tablaSeleccionada) . "`";
            $resultado = $mysqli->query($sql);
            if ($resultado) {
              while ($fila = $resultado->fetch_assoc()) {
                echo "<tr>";
                foreach($fila as $clave=>$valor){
                  // Mejora: htmlspecialchars en los datos
                  echo "<td>".htmlspecialchars($valor ?? '', ENT_QUOTES, 'UTF-8')."</td>";
                }
                echo "</tr>";
              }
            }
          ?>
        </tbody>
      </table>
      <?php else: ?>
        <!-- Mejora: mensaje cuando no hay tabla seleccionada -->
        <p style="color:#666;font-size:1.2rem;">Selecciona una tabla del menú lateral para ver sus datos.</p>
      <?php endif; ?>
    </main>
  </body>
</html>


