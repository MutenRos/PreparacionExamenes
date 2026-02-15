<!doctype html>
<html lang="es">
  <head>
    <title>JOCARSA</title>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
      * {
        box-sizing: border-box;
      }

      body,html { margin:0; padding:0; font-family:sans-serif;}

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
justify-content: center;
      }

      main > article {
        border:1px solid #ddd;
        padding:30px;
        text-align:center;
        color:white;
        display:flex;
        flex-direction:column;
        gap:10px;
        justify-content: center;
  align-items: center;
      }
      main > article strong{
        font-size:32px;
      }
      main > article em{
        font-size:12px;
      }
      main > article a{
        background:white;
        padding:10px 20px;
        border-radius:30px;
        color:inherit;
        text-decoration:none;
        margin-top:30px;
        transition: opacity 0.3s, transform 0.3s;
      }
      main > article a:hover{
        opacity:0.85;
        transform:scale(1.05);
      }
      main > article a:focus-visible{
        outline:2px solid white;
        outline-offset:2px;
      }
      main > article{
        transition: transform 0.3s, box-shadow 0.3s;
      }
      main > article:hover{
        transform:translateY(-4px);
        box-shadow:0 8px 24px rgba(0,0,0,0.2);
      }
      footer{
        background:#222;
        color:#aaa;
        text-align:center;
        padding:20px;
        font-size:13px;
      }
      @media(prefers-reduced-motion:reduce){
        *{transition:none!important;}
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
        if ($xml === false) {
            echo "<p>Error: no se pudo cargar el archivo de productos.</p>";
        } else {
        foreach ($xml->producto as $producto) {
            $nombre      = htmlspecialchars((string)$producto->nombre);
            $descripcion = htmlspecialchars((string)$producto->descripcion);
            $logo        = htmlspecialchars((string)$producto->logo);
            $enlace      = htmlspecialchars((string)$producto->enlace); // Puede estar vacío

            echo "<article style='background:".str_replace("jocarsa |","",$nombre).";'>
            ";
            echo "  <img src='$logo' alt='$nombre' style='width:80px'>
            ";
            echo "  <strong>$nombre</strong>
            ";
            echo "  <em>$descripcion</em>
            ";
            echo "  <a href='$enlace' style='color:".str_replace("jocarsa |","",$nombre).";'>Más información</a>
            ";
            echo "</article>
            ";
        }
        } // fin del else
      ?>
    </main>
    <footer>
      <p>&copy; <?php echo date('Y'); ?> JOCARSA &mdash; Soluciones de software empresarial</p>
    </footer>
  </body>
</html>
