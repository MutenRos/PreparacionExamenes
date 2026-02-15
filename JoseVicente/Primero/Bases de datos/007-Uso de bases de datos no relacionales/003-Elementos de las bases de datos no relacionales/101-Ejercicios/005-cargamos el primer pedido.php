<?php
// Conexión al servidor MongoDB
$manager = new MongoDB\Driver\Manager("mongodb://localhost:27017");

// Consulta: primer documento (sin filtros, límite 1)
$query = new MongoDB\Driver\Query(
    [],                 // filtro
    ['limit' => 1]      // opciones
);

// Ejecutar consulta
$cursor = $manager->executeQuery('tiendaonline.pedidos', $query);

// Obtener el primer documento
foreach ($cursor as $doc) {
    var_dump($doc);
    break;
}

// Si no hay documentos
if (!isset($doc)) {
    echo "La colección 'pedidos' está vacía\n";
}

