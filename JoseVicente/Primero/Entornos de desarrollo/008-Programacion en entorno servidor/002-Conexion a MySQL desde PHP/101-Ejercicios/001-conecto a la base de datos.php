<?php
// Me conecto a la base de datos
$mysqli = new mysqli("localhost", "blog2526", "blog2526", "blog2526");

// Ahora le pido algo a las entradas
$sql = "SELECT * FROM entradas";
$result = $mysqli->query($sql);

while ($row = $result->fetch_assoc()) {
    var_dump($row);
    echo "<br>";
}


