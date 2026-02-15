<?php
declare(strict_types=1);

/**
 * Devuelve una conexión PDO a SQLite con ERRMODE_EXCEPTION.
 */
function sqlite(string $path): PDO {
    $db = new PDO('sqlite:' . $path);
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
    return $db;
}

/**
 * Ejecuta una consulta y devuelve JSON con el formato:
 * [ { "clave": ..., "valor": ... }, ... ]
 */
function consulta_json(PDO $db, string $sql, array $params = []): string {
    $stmt = $db->prepare($sql);
    $stmt->execute($params);
    $rows = $stmt->fetchAll(PDO::FETCH_ASSOC);
    return json_encode($rows, JSON_UNESCAPED_UNICODE);
}

$db = sqlite('posts.db');

$sql_por_hora = "
    SELECT
        strftime('%H', \"datetime\") AS clave,
        COUNT(*) AS valor
    FROM logs
    GROUP BY clave
    ORDER BY clave;
";

$sql_por_dia_semana = "
    SELECT
        CASE strftime('%w', \"datetime\")
            WHEN '0' THEN 'Sunday'
            WHEN '1' THEN 'Monday'
            WHEN '2' THEN 'Tuesday'
            WHEN '3' THEN 'Wednesday'
            WHEN '4' THEN 'Thursday'
            WHEN '5' THEN 'Friday'
            WHEN '6' THEN 'Saturday'
        END AS clave,
        COUNT(*) AS valor
    FROM logs
    GROUP BY strftime('%w', \"datetime\")
    ORDER BY strftime('%w', \"datetime\");
";

?>
<!doctype html>
<html>
  <head>
    <script src="graficas.js"></script>
    <style>
      canvas{padding:20px;border-radius:10px;border:1px solid lightgray;}
    </style>
  </head>
  <body>
    <canvas id="lienzo"></canvas>
    <script>grafica("#lienzo", <?= consulta_json($db, $sql_por_hora) ?>, "Visitas por hora");</script>

    <canvas id="lienzo2"></canvas>
    <script>grafica("#lienzo2", <?= consulta_json($db, $sql_por_dia_semana) ?>, "Visitas por día de la semana");</script>
  </body>
</html>

