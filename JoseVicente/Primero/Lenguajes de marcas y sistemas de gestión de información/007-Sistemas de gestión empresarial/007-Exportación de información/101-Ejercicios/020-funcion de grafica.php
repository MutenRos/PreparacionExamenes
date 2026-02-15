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
				
				for(let i = 0;i<20;i++){
					contexto.fillRect(i*20,510,17,Math.random()*(-300))
				}
			}
			grafica("#lienzo",0);
			grafica("#lienzo2",0);
		</script>
	</body>
</html>

