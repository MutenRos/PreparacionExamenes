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
    echo  "<span class='barra' style='width:".($fila['visits']/10)."px'>".$fila['hour'].":".$fila['visits']."</span><br>";
}
?>
<style>
	.barra{
		height: 11px;
		 background: blue;
		 display: inline-block;
		 color: white;
		 font-family: sans-serif;
		 padding: 5px;
		 margin: 1px;
		 border-radius: 50px;
		 font-size: 10px;
		 font-weight: bold;
	}
</style>
