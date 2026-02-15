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

<!doctype html>
<html>
	<head>
		<style>
		</style>
	</head>
	<body>
		<canvas id="lienzo"></canvas>
		<canvas id="lienzo2"></canvas>
		<script>
			

			grafica("#lienzo", <?= $datos ?>);
		</script>

	</body>
</html>

