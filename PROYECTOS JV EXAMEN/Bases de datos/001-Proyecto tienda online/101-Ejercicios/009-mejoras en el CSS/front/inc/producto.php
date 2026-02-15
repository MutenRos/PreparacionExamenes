<section class="producto">
  <?php 
    $producto_id = filter_input(INPUT_GET, 'producto', FILTER_VALIDATE_INT);
    if($producto_id === null || $producto_id === false){
      echo "<p class=\"aviso\">Producto no valido.</p>";
      return;
    }
    $conexion = new mysqli("localhost", "tiendadam", "Tiendadam123$", "tiendadam");
    if($conexion->connect_error){
      echo "<p class=\"aviso\">No se pudo conectar a la base de datos.</p>";
      return;
    }
    $stmt = $conexion->prepare("SELECT * FROM producto WHERE id = ?");
    $stmt->bind_param("i", $producto_id);
    $stmt->execute();
    $resultado = $stmt->get_result();
    if($resultado->num_rows === 0){
      echo "<p class=\"aviso\">No encontramos ese producto.</p>";
      return;
    }
    while($fila = $resultado->fetch_assoc()){
      $titulo = htmlspecialchars($fila['titulo']);
      $descripcion = htmlspecialchars($fila['descripcion']);
      $precio = number_format((float)$fila['precio'], 2, ',', '.');
      $imagen = htmlspecialchars($fila['imagen'] ?: 'blanco.png');
  ?>
    <div class="izquierda">
      <img src="img/<?= $imagen ?>" alt="<?= $titulo ?>">
      <p>Indica cuantas unidades quieres</p>
      <form action="?operacion=carrito" method="POST">
        <input type="number" name="unidades" value="1" min="1" max="100" step="1" required>
        <input type="hidden" name="producto" value="<?= $fila['id'] ?>">
        <input type="hidden" name="precio" value="<?= $fila['precio'] ?>">
        <input type="hidden" name="titulo" value="<?= $titulo ?>">
        <input type="submit" value="🛍 Comprar">
      </form>
    </div>
    <div class="derecha">
      <h3><?= $titulo ?></h3>
      <p><?= $descripcion ?></p>
      <p><?= $precio ?>€</p>
    </div>
   <?php } ?>
</section>
