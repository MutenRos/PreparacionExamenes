<?php
require __DIR__ . "/jvpug.php";

$c = new mysqli("localhost", "jocarsapress", "jocarsapress", "jocarsapress");
$c->set_charset("utf8mb4");

ob_start();
include __DIR__ . "/JVestilo/JVestilo.php";
$css = ob_get_clean();

$p = $_GET['p'] ?? null;

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

echo JVpug::renderFile(__DIR__ . "/miweb.jvpug", [
  "css" => $css,
  "p" => $p,
  "paginas" => $paginas,
  "entradas" => $entradas,
  "pagina" => $pagina,
]);

