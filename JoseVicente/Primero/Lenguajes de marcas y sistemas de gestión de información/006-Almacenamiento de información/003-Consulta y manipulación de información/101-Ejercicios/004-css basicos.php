<!doctype html>
<html lang="es">
  <head>
    <title>Tienda online</title>
    <meta charset="utf-8">
    <style>
      header,main,footer{width:800px;margin:auto;text-align:center;font-family:sans-serif;}
      main{display:grid;grid-template-columns:repeat(3,100fr);gap:20px;}
      main article .imagen{height:100px;}
      main article a{background:orange;color:white;text-decoration:none;padding:10px;border-radius:10px;}
    </style>
  </head>
  <body>
    <header>
      <h1>Tienda online</h1>
    </header>
    <main>
      <?php for($i = 0;$i<30;$i++){ ?>
        <article>
          <div class="imagen" style="background:url(producto.webp);background-size:cover;background-position:center center;"></div>
          <h3>Nombre del producto</h3>
          <p>Breve descripción del producto</p>
          <p>4.33€</p>
          <a href="comprar.php">🛍 Comprar</a>
        </article>
      <?php } ?>
    </main>
    <footer>
    </footer>
  </body>
</html>
