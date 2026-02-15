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
<?php
  if(isset($_GET['operacion']) && $_GET['operacion'] == "eliminar"){
    $mysqli = new mysqli("localhost", "discos", "discos", "discos");
    $sql = "
      DELETE FROM discos
      WHERE id = ".$_GET['id'].";
    ";
    $result = $mysqli->query($sql);
  }
?>
<!doctype html>
<html>
  <head>
    <style>
      html,body{width:100%;height:100%;background:indigo;padding:0px;margin:0px;}
      body{display:flex;justify-content:center;align-items:center;font-family:sans-serif;}
      main{width:1200px;height:600px;background:white;padding:20px;border-radius:10px;}
      main section{display:flex;gap:20px;}
      #insertar{flex:1;}
      #insertar form{display:flex;flex-direction:column;gap:20px;}
      #listar{flex:4;}
      table{width:100%;border:1px solid indigo;padding:10px;border-radius:10px;}
      form input{padding:10px;border-radius:5px;border:1px solid indigo;}
      h1{text-align:center;}
      table thead{background:indigo;color:white;}
      form input[type="submit"]{background:indigo;color:white;}
      table td,table th{padding:5px;}
    </style>
  </head>
  <body>
    <main>
    <h1>💿 Aplicación de gestión de discos</h1>
    <section>
      <article id="insertar">
        <h3>Insertar un disco</h3>
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
      </article>
      <article id="listar">
        <h3>Listado de discos</h3>
        <table>
          <thead>
          <?php
            ///////////////////////// ESTO MUESTRA LAS CABECERAS
            $mysqli = new mysqli("localhost", "miempresa", "miempresa", "miempresa");
            $sql = "SELECT * FROM clientes LIMIT 1;";
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
            $mysqli = new mysqli("localhost", "discos", "discos", "discos");
            $sql = "SELECT * FROM discos";
            $resultado = $mysqli->query($sql);
            while ($fila = $resultado->fetch_assoc()) {
                echo "<tr>";
                foreach($fila as $clave=>$valor){
                  echo "<td>".$valor."</td>";
                }
                echo "<td><a href='?operacion=eliminar&id=".$fila['id']."'>❌</a></td>";
                echo "</tr>";
            }
          ?>
          </tbody>
        </table>
      </article>
      </section>
    </main>
  </body>
</html>
