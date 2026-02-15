<!doctype html>
<html lang="es">
  <head>
    <title>JOCARSA</title>
    <meta charset="utf-8">
    <style>
    body,html{padding:0px;margin:0px;}
      header{background:black;color:white;display:flex;justify-content: center;
  align-items: center;font-size:12px;gap:20px;}
  header a{color:inherit;text-decoration:none;font-size:1em;}
    </style>
  </head>
  <body>
    <header>
      <h1>JOCARSA | Soluciones de software empresarial</h1>
      <nav>
        <a href="">Quienes somos</a>
      </nav>
    </header>
    <main>
      <?php
        $xml = simplexml_load_file("productos.xml");
        foreach ($xml->producto as $producto) {

            $nombre      = (string)$producto->nombre;
            $descripcion = (string)$producto->descripcion;
            $logo        = (string)$producto->logo;
            $enlace      = (string)$producto->enlace; // Puede estar vacío

            echo "<div class='producto'>";
            echo "<img src='$logo' alt='$nombre' style='width:80px'><br>";
            echo "<strong>$nombre</strong><br>";
            echo "<em>$descripcion</em><br>";
            
            echo "</div>
            ";
        }
      ?>
    </main>
    <footer>
    </footer>
  </body>
</html>
