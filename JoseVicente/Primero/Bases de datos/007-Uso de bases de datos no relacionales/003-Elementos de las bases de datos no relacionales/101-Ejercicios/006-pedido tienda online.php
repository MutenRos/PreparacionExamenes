<?php
// factura.php  (PECL mongodb, sin Composer)

function euro($n): string {
    return number_format((float)$n, 2, ',', '.') . " €";
}

$IVA_PCT = 21; // ajusta si procede

try {
    $manager = new MongoDB\Driver\Manager("mongodb://localhost:27017");
    $query = new MongoDB\Driver\Query([], ['limit' => 1]);
    $cursor = $manager->executeQuery('tiendaonline.pedidos', $query);

    $doc = null;
    foreach ($cursor as $d) { $doc = $d; break; }

    if (!$doc) {
        header('Content-Type: text/plain; charset=utf-8');
        echo "No hay pedidos en tiendaonline.pedidos\n";
        exit;
    }

    // Extraer campos con valores por defecto
    $id      = isset($doc->_id) ? (string)$doc->_id : '';
    $cliente = $doc->cliente ?? (object)[];
    $pedido  = $doc->pedido ?? (object)[];
    $items   = $doc->productos ?? [];

    $nombre    = trim(($cliente->nombre ?? '') . ' ' . ($cliente->apellidos ?? ''));
    $email     = $cliente->email ?? '';
    $fecha     = $pedido->fecha ?? '';
    $numero    = $pedido->numero ?? '';

    // Calcular totales
    $base = 0.0;
    foreach ($items as $it) {
        $cant = (int)($it->cantidad ?? 0);
        $precio = (float)($it->precio ?? 0);
        $base += $cant * $precio;
    }
    $iva = $base * ($IVA_PCT / 100.0);
    $total = $base + $iva;

    // Salida HTML sencilla estilo factura
    header('Content-Type: text/html; charset=utf-8');

} catch (Throwable $e) {
    header('Content-Type: text/plain; charset=utf-8');
    echo "ERROR: " . $e->getMessage() . "\n";
    exit;
}
?>
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <title>Factura <?= htmlspecialchars($numero) ?></title>
  <style>
    body{font-family:Arial,Helvetica,sans-serif;background:#f3f3f3;margin:0;padding:24px;}
    .invoice{max-width:900px;margin:0 auto;background:#fff;border:1px solid #ddd;border-radius:12px;overflow:hidden;}
    header{padding:24px;border-bottom:1px solid #eee;display:flex;justify-content:space-between;gap:16px;}
    h1{margin:0;font-size:22px;}
    .muted{color:#666;font-size:13px;line-height:1.4;}
    .box{padding:18px 24px;display:flex;gap:24px;flex-wrap:wrap;}
    .col{min-width:260px;flex:1;}
    table{width:100%;border-collapse:collapse;}
    th,td{padding:12px 10px;border-bottom:1px solid #eee;text-align:left;}
    th{background:#fafafa;font-size:13px;color:#444;}
    td.num, th.num{text-align:right;}
    .totals{padding:18px 24px;display:flex;justify-content:flex-end;}
    .totals table{width:360px;}
    .totals td{border-bottom:none;padding:8px 10px;}
    .totals tr.total td{font-weight:bold;font-size:16px;border-top:1px solid #ddd;padding-top:12px;}
    footer{padding:18px 24px;border-top:1px solid #eee;}
    .badge{display:inline-block;background:#111;color:#fff;border-radius:999px;padding:6px 10px;font-size:12px;}
  </style>
</head>
<body>
  <div class="invoice">
    <header>
      <div>
        <h1>Factura <span class="badge">#<?= htmlspecialchars($numero) ?></span></h1>
        <div class="muted">
          Fecha: <?= htmlspecialchars($fecha) ?><br>
          ID pedido: <?= htmlspecialchars($id) ?>
        </div>
      </div>
      <div class="muted" style="text-align:right;">
        <strong>TiendaOnline</strong><br>
        Ejemplo S.L.<br>
        soporte@tiendaonline.local
      </div>
    </header>

    <section class="box">
      <div class="col">
        <div class="muted"><strong>Facturar a</strong></div>
        <div style="margin-top:6px;">
          <?= htmlspecialchars($nombre ?: '—') ?><br>
          <?= htmlspecialchars($email ?: '') ?>
        </div>
      </div>
      <div class="col">
        <div class="muted"><strong>Detalle del pedido</strong></div>
        <div style="margin-top:6px;">
          Número: <?= htmlspecialchars($numero ?: '—') ?><br>
          Fecha: <?= htmlspecialchars($fecha ?: '—') ?>
        </div>
      </div>
    </section>

    <section style="padding:0 24px 18px 24px;">
      <table>
        <thead>
          <tr>
            <th>Producto</th>
            <th class="num">Cantidad</th>
            <th class="num">Precio</th>
            <th class="num">Subtotal</th>
          </tr>
        </thead>
        <tbody>
        <?php foreach ($items as $it): 
          $pname = (string)($it->nombre ?? '');
          $cant  = (int)($it->cantidad ?? 0);
          $precio= (float)($it->precio ?? 0);
          $sub   = $cant * $precio;
        ?>
          <tr>
            <td><?= htmlspecialchars($pname) ?></td>
            <td class="num"><?= $cant ?></td>
            <td class="num"><?= euro($precio) ?></td>
            <td class="num"><?= euro($sub) ?></td>
          </tr>
        <?php endforeach; ?>
        </tbody>
      </table>
    </section>

    <section class="totals">
      <table>
        <tr>
          <td class="muted">Base imponible</td>
          <td class="num"><?= euro($base) ?></td>
        </tr>
        <tr>
          <td class="muted">IVA (<?= (int)$IVA_PCT ?>%)</td>
          <td class="num"><?= euro($iva) ?></td>
        </tr>
        <tr class="total">
          <td>Total</td>
          <td class="num"><?= euro($total) ?></td>
        </tr>
      </table>
    </section>

    <footer class="muted">
      Gracias por tu compra. Conserva esta factura para tus registros.
    </footer>
  </div>
</body>
</html>

