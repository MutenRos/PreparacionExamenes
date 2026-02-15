<!doctype html>
  <html>
  <head>
    <style>
      html,body{width:100%;height:100%;padding:0px;margin:0px;font-family:sans-serif;}
     body{display:flex;}
      nav{flex:1;background:indigo;color:white;padding:20px;display:flex;flex-direction:column;gap:20px;}
      main{flex:5;background:aliceblue;padding:20px;}
      nav a{border:none;background:white;padding:20px;}
      table{width:100%;border:3px solid indigo;border-collapse:collapse;}
      table tr td{padding:10px;}
      table tr th{background:indigo;color:white;padding:10px;}
    </style>
  </head>
  <body>
    <nav>
      <?php
        $mysqli = new mysqli("localhost", "miempresa", "miempresa", "miempresa");
        $sql = "SHOW TABLES";
        $resultado = $mysqli->query($sql);
        while ($fila = $resultado->fetch_assoc()) {
            // Fuerzo (truco) un parametro GET de url
            echo '<a href="?tabla='.$fila['Tables_in_miempresa'].'"> '.$fila['Tables_in_miempresa'].'</a>';
        }
      ?>
    </nav>
    <main>
      <table>
        <thead>
          <?php
            ///////////////////////// ESTO MUESTRA LAS CABECERAS
            $mysqli = new mysqli("localhost", "miempresa", "miempresa", "miempresa");
            $sql = "SELECT * FROM ".$_GET['tabla']." LIMIT 1;";
            $resultado = $mysqli->query($sql);
            while ($fila = $resultado->fetch_assoc()) {
                echo "<tr>";
                foreach($fila as $clave=>$valor){
                  echo "<th>".$clave."</th>";
                }
                echo "</tr>";
            }
          ?>
          </thead>
          <tbody>
          <?php
            ///////////////////////// ESTO MUESTRA LOS DATOS
            $mysqli = new mysqli("localhost", "miempresa", "miempresa", "miempresa");
            $sql = "SELECT * FROM ".$_GET['tabla'].";";
            $resultado = $mysqli->query($sql);
            while ($fila = $resultado->fetch_assoc()) {
                echo "<tr>";
                foreach($fila as $clave=>$valor){
                  echo "<td>".$valor."</td>";
                }
                echo "</tr>";
            }
          ?>
        </tbody>
      </table>
    </main>
  </body>
</html>


