function grafica(selector,datos,titulo){
		
		let lienzo = document.querySelector(selector);
		let contexto = lienzo.getContext("2d");
		lienzo.width = 512;
		lienzo.height = 512;
		contexto.textAlign = "center";
		contexto.fillStyle = "black";
		contexto.font = "30px Arial";
		contexto.fillText(titulo,256,40)
		
		let max = 0;
		datos.forEach(function(dato){
			if(dato.valor > max){ max = dato.valor; }
		});

		

		

		contexto.moveTo(0,0);
		contexto.lineTo(0,512);
		contexto.lineTo(512,512);
		contexto.stroke();

		let longitud = datos.length;

		datos.forEach(function(dato,i){
			
			contexto.font = "12px Arial";
			// bar color
			contexto.fillStyle = dato.color ? dato.color : "blue";

			let x = (i/longitud)*512+2;
			let w = (512/longitud-2);
			let h = (dato.valor/max)*410;

			contexto.fillRect(x, 510, w, -h);

			// rotated value label
			let cx = x + w/2;
			let cy = 500;

			contexto.save();
			contexto.translate(cx, cy);
			contexto.rotate(-Math.PI / 2); // -90 degrees
			contexto.fillStyle = "white";
			contexto.textAlign = "left";
			contexto.textBaseline = "middle";
			contexto.fillText(dato.valor+" - "+dato.clave, 15, 0);
			contexto.restore();
		});
	}
