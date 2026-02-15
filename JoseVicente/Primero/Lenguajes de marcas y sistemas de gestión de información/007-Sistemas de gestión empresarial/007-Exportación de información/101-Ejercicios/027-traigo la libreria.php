<?php
$db = new PDO('sqlite:posts.db');
$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$sql = "
	SELECT
    strftime('%H', \"datetime\") AS clave,
    COUNT(*) AS valor
	FROM logs
	GROUP BY clave
	ORDER BY clave;
";
$stmt = $db->query($sql);
$datos = [];
while ($fila = $stmt->fetch(PDO::FETCH_ASSOC)) {
    $datos[] = $fila;
}
$datos = json_encode($datos);

?>

<?php
$db = new PDO('sqlite:posts.db');
$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

$sql = "
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
$stmt = $db->query($sql);
$datos2 = [];
while ($fila = $stmt->fetch(PDO::FETCH_ASSOC)) {
    $datos2[] = $fila;
}
$datos2 = json_encode($datos2);

?>

<!doctype html>
<html>
	<head>
		<script src="graficas.js"></script>
	</head>
	<body>
		<canvas id="lienzo"></canvas>
		<script>grafica("#lienzo", <?= $datos ?>);</script>
		<canvas id="lienzo2"></canvas>
		<script>grafica("#lienzo2", <?= $datos2 ?>);</script>
	</body>
</html>

