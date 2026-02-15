<section class="producto">
  <?php 
    $conexion = new mysqli("localhost", "tiendadam", "Tiendadam123$", "tiendadam");
    $resultado = $conexion->query("SELECT * FROM producto WHERE id = ".$_GET['producto']."");
    while($fila = $resultado->fetch_assoc()){
  ?>
    <div class="izquierda">
      <img src="img/<?= $fila['imagen'] ?>">
      <p>Indica cuantas unidades quieres</p>
      <form action="?operacion=carrito" method="POST">
        <input type="number" name="unidades" value="1" min=1 max=100>
        <input type="hidden" name="producto" value="<?= $fila['id'] ?>">
        <input type="submit" value="🛍 Comprar">
      </form>
    </div>
    <div class="derecha">
      <h3><?= $fila['titulo'] ?></h3>
      <p><?= $fila['descripcion'] ?></p>
      <p><?= $fila['precio'] ?>€</p>
    </div>
   <?php } ?>
</section>
