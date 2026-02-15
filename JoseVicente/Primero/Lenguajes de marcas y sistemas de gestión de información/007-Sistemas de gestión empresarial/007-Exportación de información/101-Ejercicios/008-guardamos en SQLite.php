<?php
	$db = new PDO('sqlite:log.sqlite');
	$db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
	$epoch = $_SERVER['REQUEST_TIME'];

	$dt = new DateTime("@$epoch"); // el @ indica epoch
	$dt->setTimezone(new DateTimeZone("Europe/Madrid"));

	$fecha =  $dt->format("Y-m-d H:i:s");
	$sql = "
		 INSERT INTO logs
		 VALUES (
		 	NULL,
		 	'".$_SERVER['REQUEST_TIME']."',
		 	'".$_SERVER['HTTP_USER_AGENT']."',
		 	'".$_SERVER['HTTP_REFERER']."',
		 	'".$_SERVER['HTTP_ACCEPT_LANGUAGE']."',
		 	'".$_SERVER['HTTP_COOKIE']."',
		 	'".$_SERVER['REMOTE_ADDR']."',
		 	'".$_SERVER['REQUEST_URI']."',
		 	'".$fecha."'
		 )
	";

	$db->exec($sql);
?>

