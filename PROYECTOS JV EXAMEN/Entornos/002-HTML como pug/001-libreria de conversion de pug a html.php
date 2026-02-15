<?php
/* =========================================================
   mini_pug.php — render Pug-like (muy simple) a HTML
   - Indentación: 2 espacios por nivel
   - Sintaxis por línea: tag [atributos] [texto]
   - Atributos soportados: class="..."
   - Texto: lo que sobra al final de la línea
   ========================================================= */

// Mejora: comprobar que el archivo de plantilla existe antes de leerlo
$archivoPlantilla = "index.jvpug";
if (!file_exists($archivoPlantilla)) {
    die("Error: no se encontró la plantilla " . htmlspecialchars($archivoPlantilla, ENT_QUOTES, 'UTF-8'));
}
$pug = file_get_contents($archivoPlantilla);

function render_mini_pug(string $src): string {
  $lines = preg_split("/\r\n|\r|\n/", $src);
  $out = [];
  $stack = []; // tags abiertos
  $prevLevel = 0;

  foreach ($lines as $raw) {
    if (trim($raw) === '') continue;

    // Contar indent (2 espacios = 1 nivel)
    preg_match('/^( *)/', $raw, $m);
    $spaces = strlen($m[1]);
    $level = intdiv($spaces, 2);

    $line = trim($raw);

    // Si subimos hacia arriba, cerramos tags
    while (count($stack) > $level) {
      $tag = array_pop($stack);
      $out[] = str_repeat("  ", count($stack)) . "</{$tag}>";
    }

    // Parse: tag + (opcional) class="..." + (opcional) texto
    // Ej: h1 class="rojo" Texto
    if (!preg_match('/^([a-zA-Z][a-zA-Z0-9]*)\s*(.*)$/', $line, $mm)) {
      continue;
    }
    $tag = $mm[1];
    $rest = trim($mm[2]);

    $attrs = '';
    $text = '';

    if ($rest !== '') {
      // Capturar class="..."
      if (preg_match('/^class="([^"]*)"\s*(.*)$/', $rest, $am)) {
        $class = $am[1];
        $attrs .= ' class="' . htmlspecialchars($class, ENT_QUOTES, 'UTF-8') . '"';
        $rest = trim($am[2]);
      }
      // Lo que quede es texto
      $text = $rest;
    }

    $indent = str_repeat("  ", $level);

    // Si hay texto, abrimos y cerramos en la misma línea
    if ($text !== '') {
      $out[] = $indent . "<{$tag}{$attrs}>" . htmlspecialchars($text, ENT_QUOTES, 'UTF-8') . "</{$tag}>";
    } else {
      $out[] = $indent . "<{$tag}{$attrs}>";
      $stack[] = $tag;
    }

    $prevLevel = $level;
  }

  // Cerrar lo que quede abierto
  while (!empty($stack)) {
    $tag = array_pop($stack);
    $out[] = str_repeat("  ", count($stack)) . "</{$tag}>";
  }

  return implode("\n", $out);
}

// Mejora: añadir doctype HTML5 antes de renderizar
echo "<!DOCTYPE html>\n";
echo render_mini_pug($pug);

?>

