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
					contexto.fillStyle = dato.color;
					contexto.fillRect((i/longitud)*512,510,(512/longitud-2),0-(dato.valor/max)*510)
				})
					
				
			}
			grafica("#lienzo",[
				{'clave':'uno','valor':10,'color':'red'},
				{'clave':'dos','valor':20,'color':'blue'},
				{'clave':'tres','valor':30,'color':'orange'},
				{'clave':'cuatro','valor':40,'color':'green'},
				{'clave':'cinco','valor':140,'color':'red'}
				]);
		</script>
	</body>
</html>

