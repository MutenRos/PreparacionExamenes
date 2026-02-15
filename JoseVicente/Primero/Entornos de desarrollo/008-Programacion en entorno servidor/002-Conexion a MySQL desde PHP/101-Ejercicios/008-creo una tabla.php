<!doctype html>
  <html>
  <head>
    <style>
      html,body{width:100%;height:100%;padding:0px;margin:0px;}
     body{display:flex;}
      nav{flex:1;background:indigo;color:white;padding:20px;display:flex;flex-direction:column;gap:20px;}
      main{flex:5;background:aliceblue;padding:20px;}
      nav button{border:none;background:white;padding:20px;}
    </style>
  </head>
  <body>
    <nav>
      <?php
        $mysqli = new mysqli("localhost", "miempresa", "miempresa", "miempresa");
        $sql = "SHOW TABLES";
        $resultado = $mysqli->query($sql);
        while ($fila = $resultado->fetch_assoc()) {
            echo '<button> '.$fila['Tables_in_miempresa'].'</button>';
        }
      ?>
    </nav>
    <main>
      <table>
        <?php
          $mysqli = new mysqli("localhost", "miempresa", "miempresa", "miempresa");
          $sql = "SELECT * FROM clientes;";
          $resultado = $mysqli->query($sql);
          while ($fila = $resultado->fetch_assoc()) {
              echo "<tr>";
              foreach($fila as $clave=>$valor){
                echo "<td>".$valor."</td>";
              }
              echo "</tr>";
          }
        ?>
      </table>
    </main>
  </body>
</html>


