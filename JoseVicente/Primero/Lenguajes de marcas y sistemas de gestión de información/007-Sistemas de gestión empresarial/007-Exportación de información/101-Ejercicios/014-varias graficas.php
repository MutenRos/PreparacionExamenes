<!doctype html>
<html>
	<head>
		<style>
			.grafica{
				display: inline-block;
				    display: inline-block;
			 padding: 20px;
			 border: 1px solid lightgray;
			 border-radius: 20px;
			 margin: 20px;	
			}

			.grafica .contenedor{
				display: inline-flex;
				flex-direction: column;
				
				width: fit-content;
			}

			.barra{
				height: 11px;
				background: blue;
				display: inline-flex;
				align-items: center;
				color: white;
				font-family: sans-serif;
				padding: 5px 8px;
				margin: 2px 0;
				border-radius: 50px;
				font-size: 10px;
				font-weight: bold;
				white-space: nowrap;
			}
		</style>
	</head>
	<body>
		<div class="grafica">
			<h3>Visitas por hora</h3>
			<div class="contenedor">
				<?php
				$db = new PDO('sqlite:posts.db');
				$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

				$sql = "
					SELECT
						strftime('%H', \"datetime\") AS hour,
						COUNT(*) AS visits
					FROM logs
					GROUP BY hour
					ORDER BY hour;
				";
				$stmt = $db->query($sql);

				while ($fila = $stmt->fetch(PDO::FETCH_ASSOC)) {
					echo "<span class='barra' style='width:" . ($fila['visits'] / 10) . "px'>
							{$fila['hour']}: {$fila['visits']}
						  </span>";
				}
				?>
			</div>
		</div>
		<div class="grafica">
			<h3>Visitas por dia de la semana</h3>
			<div class="contenedor">
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
					 END AS weekday,
					 COUNT(*) AS visits
				FROM logs
				GROUP BY strftime('%w', \"datetime\")
				ORDER BY strftime('%w', \"datetime\");
				";
				$stmt = $db->query($sql);

				while ($fila = $stmt->fetch(PDO::FETCH_ASSOC)) {
					echo "<span class='barra' style='width:" . ($fila['visits'] / 30) . "px'>
							{$fila['weekday']}: {$fila['visits']}
						  </span>";
				}
				?>
			</div>
		</div>
		<div class="grafica">
			<h3>Visitas por página</h3>
			<div class="contenedor">
				<?php
				$db = new PDO('sqlite:posts.db');
				$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

				$sql = "
					SELECT COUNT(uri) AS numero,uri as pagina
					FROM logs
					GROUP BY uri
					ORDER BY COUNT(uri) DESC
					LIMIT 10
				";
				$stmt = $db->query($sql);

				while ($fila = $stmt->fetch(PDO::FETCH_ASSOC)) {
					echo "<span class='barra' style='width:" . ($fila['numero'] / 1) . "px'>
							{$fila['numero']}: {$fila['pagina']}
						  </span>";
				}
				?>
			</div>
		</div>
		
		
	</body>
</html>

