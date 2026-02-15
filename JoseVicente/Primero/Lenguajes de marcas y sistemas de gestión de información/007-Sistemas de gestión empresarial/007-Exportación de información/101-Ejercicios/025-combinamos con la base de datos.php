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
			function grafica(selector,datos){
				let max = 0;
				datos.forEach(function(dato,i){
					if(dato.valor > max){max = dato.valor;}
				})
				let lienzo = document.querySelector(selector)
				let contexto = lienzo.getContext("2d")
				
				lienzo.width = 512
				lienzo.height = 512
				
				contexto.moveTo(0,0)
				contexto.lineTo(0,512)
				contexto.lineTo(512,512);
				contexto.stroke();
				let longitud = datos.length
				
				datos.forEach(function(dato,i){
					contexto.textAlign = "center"
					if(!dato.color){
						contexto.fillStyle = "blue";
					}else{
						contexto.fillStyle = dato.color;
					}
					
					contexto.fillRect((i/longitud)*512,510,(512/longitud-2),0-(dato.valor/max)*510)
					contexto.fillStyle = "white";
					contexto.fillText(
						dato.valor,
						(i/longitud)*512+(512/longitud-2)/2,
						500
						)
				})
					
				
			}
			grafica("#lienzo",<?= $datos ?>);
		</script>
	</body>
</html>

