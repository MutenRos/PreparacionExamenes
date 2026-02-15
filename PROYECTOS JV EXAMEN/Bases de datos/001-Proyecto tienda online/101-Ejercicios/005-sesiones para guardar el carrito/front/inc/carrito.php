<?php
  $cantidad = $_POST['unidades'];
  $producto = $_POST['producto'];
  array_push($_SESSION["carrito"], [
    "unidades" => $cantidad,
    "producto" => $producto
  ]);
  var_dump($_SESSION["carrito"]);
?>

<section class="finalizacion">
  <table>
    <thead>
      <tr>
        <th>Producto</th>
        <th>Precio</th>
        <th>Unidades</th>
      </tr>
    </thead>
    <tbody>
      <tr>
        <td>Producto</td>
        <td>Precio</td>
        <td>Unidades</td>
      </tr>
      <tr>
        <td>Producto</td>
        <td>Precio</td>
        <td>Unidades</td>
      </tr>
      <tr>
        <td colspan=2>Total</td>
        <td>Total</td>
      </tr>
    </tbody>
  </table>
  <a href="?operacion=finalizacion">Confirmar compra</a>
</section>
