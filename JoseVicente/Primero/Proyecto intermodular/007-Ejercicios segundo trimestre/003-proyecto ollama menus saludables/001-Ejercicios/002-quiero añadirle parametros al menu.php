<?php
// Endpoint local de Ollama
$url = "http://localhost:11434/api/generate";

// Pregunta al modelo
$data = [
    "model" => "llama3.1:8b-instruct-q4_0",          // Ajusta al modelo que tengas cargado
    "prompt" => "Genera un menú saludable para un día completo, en español. Debe contener los siguiente ingredientes: manzana, avena, aguacate, zanahoria, frambuesa.",
    "stream" => false                  // Lo ponemos en false para recibir todo el texto de una vez
];

// Inicializar cURL
$ch = curl_init($url);

// Configuración de cURL
curl_setopt($ch, CURLOPT_POST, true);
curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
curl_setopt($ch, CURLOPT_HTTPHEADER, [
    "Content-Type: application/json"
]);
curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));

// Ejecutar petición
$response = curl_exec($ch);

// Cerrar conexión
curl_close($ch);

// Decodificar la respuesta JSON
$result = json_decode($response, true);

// Mostrar solo el texto generado
echo "<pre>";
echo $result["response"];
echo "</pre>";

