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
  <!doctype html>
<html>
  <head>
    <style>
     html,body{padding:0px;margin:0px;width:100%;height:100%;}
     body{display:flex;}
     nav{background:orange;flex:1;display:flex;flex-direction:column;padding:20px;gap:20px;}
     main{background:white;flex:4;padding:20px;}
     nav a{background:white;padding:10px;color:inherit;text-decoration:none;}
     main table{width:100%;border:2px solid orange;border-collapse:collapse;}
     main table th{background:orange;}
     main table th, main table td{padding:10px;}
    </style>
  </head>
  <body>
    <nav>
      <a href="?tabla=producto">Productos</a>
      <a href="?tabla=cliente">Clientes</a>
      <a href="?tabla=pedido">Pedidos</a>
    </nav>
    <main>
        <table>
        <?php
            // Conexión común
            $conexion = new mysqli("localhost", "tiendadam", "Tiendadam123$", "tiendadam");
            // Cabecera de la tabla
            $resultado = $conexion->query("SELECT * FROM ".$_GET['tabla']." LIMIT 1;");
            while($fila = $resultado->fetch_assoc()){
              echo '<tr>';
              foreach($fila as $clave=>$valor){
                echo "<th>".$clave."</th>";
              }
              echo '</tr>';
            }
            // Cuerpo de la tabla
            $resultado = $conexion->query("SELECT * FROM ".$_GET['tabla']);
            while($fila = $resultado->fetch_assoc()){
              echo '<tr>';
              foreach($fila as $clave=>$valor){
                echo "<td>".$valor."</td>";
              }
              echo '</tr>';
            }
          ?>
        </table>
      
    </main>
  </body>
</html>
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
