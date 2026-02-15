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

<section class="carrito"> 
  <div class="izquierda">
    <form action="?operacion=finalizacion" method="POST">
      <p>Introduce tu nombre</p>
      <input type="text" name="nombre">
      <p>Introduce tus apellidos</p>
      <input type="text" name="apellidos">
      <p>Introduce tu email</p>
      <input type="text" name="email">
      <input type="submit" value="Finalizar compra">
    </form>
  </div>
  <div class="derecha">
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
  
  </div>
</section>
