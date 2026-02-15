<?php

// Recoger datos (con valores por defecto)
$usuario   = $_GET['usuario']   ?? '';
$pregunta  = $_GET['pregunta']  ?? '';
$respuesta = $_GET['respuesta'] ?? '';
$opciones  = $_GET['opciones']  ?? '[]';

// Decodificar opciones (por si quieres validar)
$opciones_array = json_decode($opciones, true);
if (!is_array($opciones_array)) {
    $opciones_array = [];
}

// Re-encode limpio para CSV
$opciones_json = json_encode($opciones_array, JSON_UNESCAPED_UNICODE);

// Abrir CSV en modo append
$fp = fopen("respuestas.csv", "a");

// Usar fputcsv para evitar problemas con comas, saltos de línea, etc.
fputcsv($fp, [
    $usuario,
    $pregunta,
    $respuesta,
    $opciones_json
]);

fclose($fp);

