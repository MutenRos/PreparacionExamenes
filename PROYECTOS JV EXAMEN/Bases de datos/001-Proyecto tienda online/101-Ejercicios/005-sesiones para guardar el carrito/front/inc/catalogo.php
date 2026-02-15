<section class="catalogo">
  <?php 
    $conexion = new mysqli("localhost", "tiendadam", "Tiendadam123$", "tiendadam");
    $resultado = $conexion->query("SELECT * FROM producto");
    while($fila = $resultado->fetch_assoc()){
  ?>
    <article>
      <div class="imagen" style="background:url(img/<?php echo $fila['imagen'] ?>);background-size:cover;background-position:center center;"></div>
      <h3><?= $fila['titulo'] ?></h3>
      <p><?= $fila['descripcion'] ?></p>
      <p><?= $fila['precio'] ?>€</p>
      <a href="?operacion=producto&producto=<?= $fila['id'] ?>">🛍 Comprar</a>
    </article>
  <?php } ?>
</section>
