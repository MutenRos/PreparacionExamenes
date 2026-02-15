<!doctype html>
<html lang="es">
  <head>
    <title>JOCARSA</title>
    <meta charset="utf-8">
    <style>
      * {
        box-sizing: border-box;
      }

      body,html { margin:0; padding:0; }

      header {
        background:black;
        color:white;
        display:flex;
        justify-content:center;
        align-items:center;
        font-size:12px;
        gap:20px;
        padding:10px 20px;
      }

      header a {
        color:inherit;
        text-decoration:none;
        font-size:1em;
      }

      main {
        display:flex;
        flex-wrap:wrap;
        gap:10px;           /* separación entre tarjetas */
        padding:10px;
      }

      main > article {
        border:1px solid #ddd;
        padding:10px;
      }

      /* 1–4: 100% */
      main > article:nth-child(-n+4) {
        flex: 0 0 100%;
      }

      /* 5–8: 2 por fila -> 50%, restando el gap aproximado */
      main > article:nth-child(n+5):nth-child(-n+8) {
        flex: 0 0 calc(50% - 10px);
      }

      /* 9+: 3 por fila -> 33.333%, restando un poco para gaps */
      main > article:nth-child(n+9) {
        flex: 0 0 calc(33.333% - 10px);
      }
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

            echo "<article>";
            echo "<img src='$logo' alt='$nombre' style='width:80px'><br>";
            echo "<strong>$nombre</strong><br>";
            echo "<em>$descripcion</em><br>";
            echo "<a href='$enlace'>Más información</a><br>";
            echo "</article>
            ";
        }
      ?>
    </main>
    <footer>
    </footer>
  </body>
</html>
