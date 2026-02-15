<?php
$basededatos = new SQLite3('youtube_videos.sqlite');
$resultado = $basededatos->query("SELECT * FROM videos");
while ($fila = $resultado->fetchArray(SQLITE3_ASSOC)) {
    echo '<article>';
    foreach($fila as $clave=>$valor){
    	echo '<p>'.$clave.": ".$valor.'</p>';
    }
    echo '</article>';
}
?>

