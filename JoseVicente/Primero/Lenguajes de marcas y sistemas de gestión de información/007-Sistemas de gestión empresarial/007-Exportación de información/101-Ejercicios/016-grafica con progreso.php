<!doctype html>
<html>
	<head>
		<style>
			progress{
				margin:0px;
				block-size: 2em;
			 	inline-size: 15em;
			 	vertical-align: -0.1em;
			 	
			 }
			/* Chrome / Edge / Safari */
			progress::-webkit-progress-bar {
			  background-color: red;
			  border-radius: 10px;
			}

			progress::-webkit-progress-value {
			  background-color: #4caf50;
			  border-radius: 10px;
			}

			/* Firefox */
			progress::-moz-progress-bar {
			  background-color: #4caf50;
			  border-radius: 10px;
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
						ORDER BY visits DESC LIMIT 1;
				";
				$stmt = $db->query($sql);
				while ($fila = $stmt->fetch(PDO::FETCH_ASSOC)) {
					$maximo = $fila['visits'];
				}
				
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
					echo $fila['visits']."<progress value='".($fila['visits']/$maximo)."'></progress><br>";
				}
				?>
			</div>
		</div>
		
		
		
	</body>
</html>

