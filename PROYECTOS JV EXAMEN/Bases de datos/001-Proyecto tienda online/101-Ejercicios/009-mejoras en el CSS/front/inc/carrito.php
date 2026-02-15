<?php
  if($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_POST['unidades'], $_POST['producto'])){
    $cantidad = max(1, min(100, (int)$_POST['unidades']));
    $producto = (int)$_POST['producto'];
    $titulo = isset($_POST['titulo']) ? trim($_POST['titulo']) : '';
    $precio = isset($_POST['precio']) ? (float)$_POST['precio'] : 0;
    array_push($_SESSION["carrito"], [
      "unidades" => $cantidad,
      "producto" => $producto,
      "titulo" => $titulo,
      "precio" => $precio
    ]);
  }
  $carrito_vacio = empty($_SESSION["carrito"]);
?>

<section class="carrito"> 
  <div class="izquierda">
    <h3>Datos de entrega</h3>
    <form action="?operacion=finalizacion" method="POST">
      <p>Introduce tu nombre</p>
      <input type="text" name="nombre" required>
      <p>Introduce tus apellidos</p>
      <input type="text" name="apellidos" required>
      <p>Introduce tu email</p>
      <input type="email" name="email" placeholder="tucorreo@email.com" required>
      <input type="submit" value="Finalizar compra">
    </form>
    <div class="acciones">
      <a class="boton-secundario" href="util/borrar.php" id="vaciar-carrito">Vaciar carrito</a>
    </div>
  </div>
  <div class="derecha">
  <?php if($carrito_vacio){ ?>
    <p class="aviso">Tu carrito esta vacio. Vuelve al catalogo para anadir productos.</p>
  <?php }else{ ?>
    <table>
      <thead>
        <tr>
          <th>Unidades</th>
          <th>Producto</th>
          <th>Precio</th>
          <th>Subtotal</th>
        </tr>
      </thead>
      <tbody>
        <?php 
        $total = 0;
        foreach($_SESSION["carrito"] as $clave=>$valor){
          $titulo = htmlspecialchars($valor['titulo']);
          $precio = number_format((float)$valor['precio'], 2, ',', '.');
          $subtotal_num = $valor['unidades'] * $valor['precio'];
          $subtotal = number_format((float)$subtotal_num, 2, ',', '.');
          $total += $subtotal_num;
        ?>
        <tr>
          <td><?= $valor['unidades'] ?></td>
          <td><?= $titulo ?></td>
          <td><?= $precio ?>€</td>
          <td><?= $subtotal ?>€</td>
        </tr>
        <?php } ?>
      </tbody>
      <tfoot>
        <tr>
          <td colspan="3" class="total-label">Total</td>
          <td class="total-valor"><?= number_format($total, 2, ',', '.') ?>€</td>
        </tr>
      </tfoot>
    </table>
  <?php } ?>
  </div>
</section>

<script>
  const vaciar = document.getElementById('vaciar-carrito');
  if (vaciar) {
    vaciar.addEventListener('click', (event) => {
      const ok = confirm('Seguro que quieres vaciar el carrito?');
      if (!ok) event.preventDefault();
    });
  }
</script>
