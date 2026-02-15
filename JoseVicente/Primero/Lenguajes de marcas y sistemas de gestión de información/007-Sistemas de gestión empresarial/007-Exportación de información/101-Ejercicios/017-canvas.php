<!doctype html>
<html>
	<head>
		<style>
			canvas{border:1px solid grey;}
		</style>
	</head>
	<body>
		<canvas id="lienzo"></canvas>
		<script>
			let lienzo = document.querySelector("canvas")
			let contexto = lienzo.getContext("2d")
			
			lienzo.width = 512
			lienzo.height = 512
			// Rectangulo
			contexto.fillRect(10,10,20,20)
			// Circulo
			contexto.beginPath()
			// arc: ox, oy, radio, ang_inicio, ang_final
			contexto.arc(200,200,50,0,Math.PI*2)
			contexto.fill()
		</script>
	</body>
</html>

