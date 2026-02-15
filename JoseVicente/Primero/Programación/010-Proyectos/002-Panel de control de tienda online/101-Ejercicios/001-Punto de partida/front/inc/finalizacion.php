<?php 
  // Me conecto a la base de datos
    $conexion = new mysqli("localhost", "tiendadam", "Tiendadam123$", "tiendadam");
  // Inserto cliente y obtengo id
    $resultado = $conexion->query("INSERT INTO cliente VALUES(
                                                  NULL,
                                                  '".$_POST['nombre']."',
                                                  '".$_POST['apellidos']."',
                                                  '".$_POST['email']."'
                                                  );");
    $id_cliente = $conexion->insert_id;
  // Inserto pedido y obtengo id
    $resultado = $conexion->query("INSERT INTO pedido VALUES(
                                                  NULL,
                                                  '".date('Y-m-d H:i:s')."',
                                                  ".$id_cliente."
                                                  );");
    $id_pedido = $conexion->insert_id;
  // Ahora inserto las lineas de pedido
    foreach($_SESSION["carrito"] as $clave=>$valor){
      $resultado = $conexion->query("INSERT INTO lineapedido VALUES(
                                                  NULL,
                                                  ".$id_pedido.",
                                                  '".$valor['producto']."',
                                                  '".$valor['unidades']."'
                                                  );");
    }
  // Y por ultimo vacio el carrito
    $_SESSION["carrito"] = [];
?>

<section class="finalizacion">
  <h3>Pedido finalizado</h3>
  <p>Muchas gracias por tu compra</p>
  <a href="?">Pulsa aqui para continuar navegando</a>
</section>
