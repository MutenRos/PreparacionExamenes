<?php
// Conexión a la base de datos (una sola vez, al inicio del archivo)
$c = new mysqli("localhost","training_center","training_center","training_center");
if ($c->connect_error) {
  die("Error de conexión: " . $c->connect_error);
}
?>
<!doctype html>
<html lang="es">
  <head>
    <title>Formulario</title>
    <meta charset="utf-8">
    <style>
      body,html{width:100%;height:100%;padding:0px;margin:0px;}
      body{display:flex;}
      nav{flex:1;background:crimson;padding:10px;display:flex;flex-direction:column;gap:10px;}
      main{flex:5;padding:10px;}
      table{border:1px solid crimson;padding:10px;width:100%;border-collapse:collapse;}
      nav button{background:white;border:none;padding:10px;border-radius:20px;}
      table tr:nth-child(odd){background:rgb(255,220,220);}
      table td{padding:10px;}
    </style>
  </head>
  <body>
    <nav>
      <button>Enlace 1</button>
      <button>Enlace 2</button>
      <button>Enlace 3</button>
    </nav>
    <main>
      <table>
        <thead>
          <tr>
            <?php
            /* COLUMNAS CON SUS COMENTARIOS */
              $r = $c->query("
                SELECT COLUMN_NAME, COLUMN_TYPE, COLUMN_KEY, COLUMN_DEFAULT, COLUMN_COMMENT
                FROM information_schema.columns
                WHERE table_schema='training_center'
                  AND table_name='inscripciones'
              ");

              while($f = $r->fetch_assoc()) {
                echo '<th>'.$f['COLUMN_NAME'].'</th>';
              
              }
            ?>
          </tr>
        </thead>
        <tbody>
          <?php
            $r = $c->query("SELECT * FROM inscripciones;");

              while($f = $r->fetch_assoc()) {
              echo '<tr>';
              foreach($f as $clave=>$valor){
                echo '<td>'.$valor.'</td>';
              }
              echo  '</tr>';
              
              }
          ?>
        </tbody>
      </table>
    </main>
  </body>
</html>
