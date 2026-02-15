<!doctype html>
<html lang="es">
  <head>
    <title>Tienda online</title>
    <meta charset="utf-8">
    <style>
      html,body{padding:0px;margin:0px;}
      header,main,footer{width:800px;margin:auto;text-align:center;font-family:sans-serif;}
      main{display:grid;grid-template-columns:repeat(3,100fr);gap:20px;}
      main article .imagen{height:100px;}
      main article a{background:orange;color:white;text-decoration:none;padding:10px;border-radius:10px;}
      header{width:100%;height:200px;background:url("blanco.png"),url("blanco.png"),url("cabeceratienda.avif");padding:20px;background-size:cover;background-position:center top;margin-bottom:20px;display:flex;justify-content:center;align-items:center;}
    </style>
  </head>
  <body>
    <header>
      <h1>Tienda online</h1>
    </header>
    <main>
      <?php
        if(isset($_GET['producto'])){
      ?>
      
      <?php }else{ ?>
        <?php for($i = 0;$i<30;$i++){ ?>
          <article>
            <div class="imagen" style="background:url(producto.webp);background-size:cover;background-position:center center;"></div>
            <h3>Nombre del producto</h3>
            <p>Breve descripción del producto</p>
            <p>4.33€</p>
            <a href="?producto=1">🛍 Comprar</a>
          </article>
        <?php } ?>
      <?php } ?>
    </main>
    <footer>
      (c) Jose Vicente Carratala
    </footer>
  </body>
</html>
