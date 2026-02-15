<?php
  $datos = [
    ["titulo"=>"Titulo 1","contenido"=>"Este es el contenido del articulo 1"],
    ["titulo"=>"Titulo 2","contenido"=>"Este es el contenido del articulo 2"],
    ["titulo"=>"Titulo 3","contenido"=>"Este es el contenido del articulo 3"],
    ["titulo"=>"Titulo 4","contenido"=>"Este es el contenido del articulo 4"],
    ["titulo"=>"Titulo 5","contenido"=>"Este es el contenido del articulo 5"],
    ];

  for($i = 0;$i<count($datos);$i++){ ?>
      <article>
        <h3><?= $datos[$i]["titulo"] ?></h3>
        <p><?= $datos[$i]["contenido"] ?></p>
      </article>
<?php } ?>
