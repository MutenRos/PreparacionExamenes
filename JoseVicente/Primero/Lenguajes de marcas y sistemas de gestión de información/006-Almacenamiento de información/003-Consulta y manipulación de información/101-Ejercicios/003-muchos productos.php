<!doctype html>
<html lang="es">
  <head>
    <title>Tienda online</title>
    <meta charset="utf-8">
  </head>
  <body>
    <header>
      <h1>Tienda online</h1>
    </header>
    <main>
      <?php for($i = 0;$i<30;$i++){ ?>
        <article>
          <div class="imagen" style="background:url(producto.webp);"></div>
          <h3>Nombre del producto</h3>
          <p>Breve descripción del producto</p>
          <p>4.33€</p>
          <a href="comprar.php"></a>
        </article>
      <?php } ?>
    </main>
    <footer>
    </footer>
  </body>
</html>
