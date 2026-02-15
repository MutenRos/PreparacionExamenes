<?php
  $cantidad = $_POST['unidades'];
  $producto = $_POST['producto'];
  $titulo = $_POST['titulo'];
  $precio = $_POST['precio'];
  array_push($_SESSION["carrito"], [
    "unidades" => $cantidad,
    "producto" => $producto,
    "titulo" => $titulo,
    "precio" => $precio
  ]);
?>

<section class="finalizacion">
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
      foreach($_SESSION["carrito"] as $clave=>$valor){
      ?>
      <tr>
        <td><?= $valor['unidades'] ?></td>
        <td><?= $valor['titulo'] ?></td>
        <td><?= $valor['precio'] ?></td>
        <td><?= $valor['unidades']*$valor['precio'] ?></td>
      </tr>
      <?php } ?>
    </tbody>
  </table>
  <a href="?operacion=finalizacion">Confirmar compra</a>
</section>
