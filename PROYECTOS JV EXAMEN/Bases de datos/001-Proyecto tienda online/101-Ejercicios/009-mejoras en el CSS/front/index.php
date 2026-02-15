<?php 
  session_start();
  if(!isset($_SESSION['carrito'])){                     // Si no tenías un carrito
    $_SESSION['carrito'] = [];                          // Ahora tienes un carrito vacío
  }                                                     // Como cuando entras en el supermercado
  $carrito_count = count($_SESSION['carrito']);
?>
<!doctype html>
<html lang="es">
  <head>
    <title>Tienda online</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="css/estilo.css">
  </head>
  <body>
    <header>
      <a href="?"><h1>Tienda online</h1></a>
      <div class="header-actions">
        <a class="carrito-link" href="?operacion=carrito">
          Carrito
          <span class="badge"><?= $carrito_count ?></span>
        </a>
      </div>
    </header>
    <main>
      <?php
        if(isset($_GET['operacion'])){                  // Si hay operacion
          if($_GET['operacion'] == "producto"){         // Y esa operacion es producto
            include "inc/producto.php";                 // Enseñame el producto
          }else if($_GET['operacion'] == "carrito"){    // Si la operacion es carrito
            include "inc/carrito.php";                  // Enseñame el carrito                 
          }else if($_GET['operacion'] == "finalizacion"){  // Si es finalizacion
            include "inc/finalizacion.php";             // enseñame la finalizacion
          } 
        }else{                                          // En caso contrario
          include "inc/catalogo.php";                   // Enseñame el catalogo
        } 
      ?>
    </main>
    <footer>
      (c) Jose Vicente Carratala
    </footer>
  </body>
</html>
