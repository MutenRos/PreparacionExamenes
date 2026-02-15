<!doctype html>
<html lang="es">
  <head>
    <title>Tienda online</title>
    <meta charset="utf-8">
    <link rel="stylesheet" href="css/estilo.css">
  </head>
  <body>
    <header>
      <h1>Tienda online</h1>
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
