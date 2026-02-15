<!doctype html>
<html lang="es">
  <head>
    <title>jocarsa</title>
    <meta charset="utf-8">
    <style>
      @font-face {font-family: Ubuntu;src: url(estilo/Ubuntu-R.ttf);}
      @font-face {font-family: UbuntuB;src: url(estilo/Ubuntu-B.ttf);}
      /* ESTILOS GENERALES /////////////////////////////////////// */
      html,body{
        padding:0px;
        margin:0px;
        font-family:Ubuntu,sans-serif;
        width:100%;
        height:100%; 
      }

      /* ESTILOS CABECERA  /////////////////////////////////////// */
      header{
        width:100%;
        display:flex;
        justify-content:center;
        align-items:center;
        box-shadow:0px 2px 4px rgba(0,0,0,0.3);
        gap:20px;
        padding:10px;
      }
      header img{width:30px;}
      header a{text-decoration:none;color:indigo;font-size:11px;}

      /* ESTILOS PRODUCTOS  /////////////////////////////////////// */
      main{
        width:100%;
        display:grid;
        grid-template-columns:1fr;
        gap:10px;
      }

      /* ARTÍCULOS 1–3 (IGUAL QUE AHORA) ///////////////////////// */
      main article{
        width:100%;
        height:400px;
        display:flex;
        justify-content:center;
        align-items:center;
        background:lightgrey;
        flex-direction:column;
        gap:10px;
      }
      main article h3,main article h4{padding:0px;margin:0px;}
      main article h3{font-size:32px;}
      main article a{background:indigo;text-decoration:none;color:white;padding:10px 20px;border-radius:50px;}

      /* LOS 3 PRIMEROS OCUPAN TODA LA FILA ////////////////////// */
      main article:nth-child(-n+3){
        grid-column:1 / -1;
      }

      /* ARTÍCULOS 4+ EN DOS COLUMNAS /////////////////////////// */
      @media (min-width:600px){
        main{
          grid-template-columns:1fr 1fr;
        }

        main article:nth-child(-n+3){
          grid-column:1 / -1;
        }
      }
      footer{display:flex;justify-content:center;gap:20px;padding:20px;font-size:11px;}
      footer article{display:flex;flex-direction:column;gap:10px;}
      footer article a{text-decoration:none;color:indigo;}
    </style>

  </head>
  <body>
    <header>
      <a href="?"><img src="https://static.jocarsa.com/logos/jocarsa%20%7C%20Indigo.svg"></a>
      <?php 
      $archivo = file_get_contents('db/categorias.json');
      $json = json_decode($archivo, true);
      for($i = 0;$i<count($json);$i++){ ?>
        <a href="?"><?= $json[$i] ?></a>
      <?php }?>
    </header>
    <main>
      <?php 
        $archivo = file_get_contents('db/productos.json');
        $json = json_decode($archivo, true);
        for($i = 0;$i<count($json);$i++){ ?>
        <article>
          <h3><?= $json[$i]['nombre'] ?></h3>
          <h4><?= $json[$i]['slogan'] ?></h4>
          <a href="producto.php?p=<?= $json[$i]['nombre'] ?>">Saber más</a>
        </article>
      <?php }?>
    </main>
    <footer>
      <?php 
        $archivo = file_get_contents('db/piedepagina.json');
        $json = json_decode($archivo, true);
         ?>
        <article class="categorias">
          <?php for($i = 0;$i<count($json['categorias']);$i++){?>
            <a href="?cat=<?= $json['categorias'][$i] ?>"><?= $json['categorias'][$i] ?></a>
          <?php } ?>
        </article>
        <article class="paginas">
          <?php for($i = 0;$i<count($json['enlaces']);$i++){?>
            <a href="?cat=<?= $json['enlaces'][$i]['enlace'] ?>"><?= $json['enlaces'][$i]['nombre'] ?></a>
          <?php } ?>
        </article>
     
    </footer>
  </body>
</html>
