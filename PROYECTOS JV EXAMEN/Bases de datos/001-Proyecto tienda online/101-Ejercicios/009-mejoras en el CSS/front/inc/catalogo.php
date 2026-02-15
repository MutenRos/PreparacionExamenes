<section class="catalogo">
  <?php 
    $conexion = new mysqli("localhost", "tiendadam", "Tiendadam123$", "tiendadam");
    if($conexion->connect_error){
      echo "<p class=\"aviso\">No se pudo conectar a la base de datos.</p>";
      return;
    }
    $resultado = $conexion->query("SELECT * FROM producto");
    while($fila = $resultado->fetch_assoc()){
      $titulo = htmlspecialchars($fila['titulo']);
      $descripcion = htmlspecialchars($fila['descripcion']);
      $precio = number_format((float)$fila['precio'], 2, ',', '.');
      $imagen = htmlspecialchars($fila['imagen'] ?: 'blanco.png');
  ?>
    <article>
      <div class="imagen" style="background:url(img/<?= $imagen ?>);background-size:cover;background-position:center center;"></div>
      <h3><?= $titulo ?></h3>
      <p><?= $descripcion ?></p>
      <p><?= $precio ?>€</p>
      <a href="?operacion=producto&producto=<?= $fila['id'] ?>">🛍 Comprar</a>
    </article>
  <?php } ?>
</section>
