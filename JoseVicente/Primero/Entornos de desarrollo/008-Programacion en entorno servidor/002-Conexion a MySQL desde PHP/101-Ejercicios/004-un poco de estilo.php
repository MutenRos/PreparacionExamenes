<!doctype html>
  <html>
  <head>
    <style>
      body{background:indigo;font-family:sans-serif;}
      header,main,footer{background:white;padding:20px;margin:auto;width:600px;}
      header,footer{text-align:center;}
      article{border-bottom:1px solid indigo;}
    </style>
  </head>
  <body>
    <header>
      <h1>El blog de Jose Vicente</h1>
    </header>
    <main>
      <?php
        // Me conecto a la base de datos
        $mysqli = new mysqli("localhost", "blog2526", "blog2526", "blog2526");

        // Ahora le pido algo a las entradas
        $sql = "SELECT * FROM entradas";
        $resultado = $mysqli->query($sql);

        while ($fila = $resultado->fetch_assoc()) {
            echo '
              <article>
                <h3>'.$fila['titulo'].'</h3>
                <time>'.$fila['fecha'].'</time>
                <p>'.$fila['autor'].'</p>
                <p>'.$fila['contenido'].'</p>
              </article>
            ';
        }
      ?>
    </main>
    <footer>
      (c) 2025 Jose Vicente Carratala
    </footer>
  </body>
</html>


