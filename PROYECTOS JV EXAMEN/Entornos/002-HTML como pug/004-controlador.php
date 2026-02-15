<?php
// Controlador principal: carga datos de MySQL y renderiza la plantilla JVpug
require __DIR__ . "/jvpug.php";

// Mejora: manejo de errores en la conexión a base de datos
mysqli_report(MYSQLI_REPORT_ERROR | MYSQLI_REPORT_STRICT);
try {
    $c = new mysqli("localhost", "jocarsapress", "jocarsapress", "jocarsapress");
    $c->set_charset("utf8mb4");
} catch (mysqli_sql_exception $e) {
    die("Error de conexión a la base de datos: " . htmlspecialchars($e->getMessage(), ENT_QUOTES, 'UTF-8'));
}

ob_start();
include __DIR__ . "/JVestilo/JVestilo.php";
$css = ob_get_clean();

// Mejora: sanitizar parámetro GET
$p = isset($_GET['p']) ? trim($_GET['p']) : null;

$paginas = [];
$r = $c->query("SELECT * FROM paginas;");
while ($f = $r->fetch_assoc()) $paginas[] = $f;

$entradas = [];
$pagina = [];

if ($p === "blog") {
  $r = $c->query("SELECT * FROM entradas;");
  while ($f = $r->fetch_assoc()) {
    // aquí decides: antes escapabas contenido; en pug lo estamos mostrando como texto normal
    // si tu contenido trae HTML y lo quieres permitir, cambia en jvpug a !{...}
    $entradas[] = $f;
  }
} elseif ($p !== null) {
  $stmt = $c->prepare("SELECT * FROM paginas WHERE titulo = ?");
  $stmt->bind_param("s", $p);
  $stmt->execute();
  $res = $stmt->get_result();
  while ($f = $res->fetch_assoc()) $pagina[] = $f;
  $stmt->close();
}

// Mejora: cabecera Content-Type para asegurar UTF-8 en el navegador
header('Content-Type: text/html; charset=utf-8');

echo JVpug::renderFile(__DIR__ . "/miweb.jvpug", [
  "css" => $css,
  "p" => $p,
  "paginas" => $paginas,
  "entradas" => $entradas,
  "pagina" => $pagina,
]);

// Mejora: cerrar la conexión MySQL al terminar
$c->close();

