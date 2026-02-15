<table border=1>
<?php
		echo '<tr><td>HTTP_USER_AGENT</td><td>'.$_SERVER['HTTP_USER_AGENT'].'</td></tr>';
		echo '<tr><td>HTTP_REFERER</td><td>'.$_SERVER['HTTP_REFERER'].'</td></tr>';
		
		echo '<tr><td>HTTP_ACCEPT_LANGUAGE</td><td>'.$_SERVER['HTTP_ACCEPT_LANGUAGE'].'</td></tr>';
		echo '<tr><td>HTTP_COOKIE</td><td>'.$_SERVER['HTTP_COOKIE'].'</td></tr>';
		echo '<tr><td>REMOTE_ADDR</td><td>'.$_SERVER['REMOTE_ADDR'].'</td></tr>';
		echo '<tr><td>REQUEST_URI</td><td>'.$_SERVER['REQUEST_URI'].'</td></tr>';
		echo '<tr><td>REQUEST_TIME</td><td>'.$_SERVER['REQUEST_TIME'].'</td></tr>';
?>
</table>
