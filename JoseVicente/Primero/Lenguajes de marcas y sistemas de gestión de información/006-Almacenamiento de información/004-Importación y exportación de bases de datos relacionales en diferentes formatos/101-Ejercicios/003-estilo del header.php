<!doctype html>
<html lang="es">
  <head>
    <title>jocarsa</title>
    <meta charset="utf-8">
    <style>
      html,body{padding:0px;margin:0px;font-family:sans-serif;}
      header{
      width:100%;display:flex;justify-content:center;
      align-items:center;box-shadow:0px 2px 4px rgba(0,0,0,0.3);gap:20px;padding:10px;}
      header img{width:30px;}
      header a{text-decoration:none;color:indigo;font-size:11px;}
    </style>
  </head>
  <body>
    <header>
      <a href="?"><img src="https://static.jocarsa.com/logos/jocarsa%20%7C%20Indigo.svg"></a>
      <?php for($i = 0;$i<8;$i++){ ?>
        <a href="?">Elemento <?= $i?></a>
      <?php }?>
    </header>
    <main>
    </main>
    <footer>
    </footer>
  </body>
</html>
