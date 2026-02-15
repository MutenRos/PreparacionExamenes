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
    echo $fila['hour'].":".$fila['visits']."<br>";
}
?>

