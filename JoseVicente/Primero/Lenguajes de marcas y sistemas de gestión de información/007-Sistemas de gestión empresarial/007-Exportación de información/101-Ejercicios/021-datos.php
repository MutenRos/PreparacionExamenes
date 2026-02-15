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
				let lienzo = document.querySelector(selector)
				let contexto = lienzo.getContext("2d")
				
				lienzo.width = 512
				lienzo.height = 512
				
				contexto.moveTo(0,0)
				contexto.lineTo(0,512)
				contexto.lineTo(512,512);
				contexto.stroke();
				
				datos.forEach(function(dato,i){
					contexto.fillRect(i*20,510,17,0-dato.valor)
				})
					
				
			}
			grafica("#lienzo",[{'clave':'uno','valor':10},{'clave':'dos','valor':20},{'clave':'tres','valor':30}]);
		</script>
	</body>
</html>

