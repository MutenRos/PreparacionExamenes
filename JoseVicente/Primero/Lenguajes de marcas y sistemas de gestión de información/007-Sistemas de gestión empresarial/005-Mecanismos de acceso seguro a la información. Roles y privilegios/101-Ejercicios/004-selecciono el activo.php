<?php
	session_start();
	if(!isset($_SESSION['lang'])){$_SESSION['lang'] = "es";}
	if(isset($_GET['lang'])){$_SESSION['lang'] = $_GET['lang'];}
<!doctype html>
<html lang="es">
	<head>
		<meta charset="utf-8">
	</head>
	<body>
		<select id="idioma">
			<option value="es">Español 🇪🇸</option>
			<option value="en">English 🇬🇧</option>
			<option value="fr">Français 🇫🇷</option>
			<option value="de">Deutsch 🇩🇪</option>
			<option value="it">Italiano 🇮🇹</option>
			<option value="pt">Português 🇵🇹</option>
			<option value="nl">Nederlands 🇳🇱</option>
			<option value="sv">Svenska 🇸🇪</option>
			<option value="da">Dansk 🇩🇰</option>
			<option value="fi">Suomi 🇫🇮</option>
			<option value="no">Norsk 🇳🇴</option>
			<option value="pl">Polski 🇵🇱</option>
			<option value="cs">Čeština 🇨🇿</option>
			<option value="sk">Slovenčina 🇸🇰</option>
			<option value="hu">Magyar 🇭🇺</option>
			<option value="ro">Română 🇷🇴</option>
			<option value="bg">Български 🇧🇬</option>
			<option value="el">Ελληνικά 🇬🇷</option>
			<option value="hr">Hrvatski 🇭🇷</option>
			<option value="sl">Slovenščina 🇸🇮</option>
			<option value="et">Eesti 🇪🇪</option>
			<option value="lv">Latviešu 🇱🇻</option>
			<option value="lt">Lietuvių 🇱🇹</option>
			<option value="mt">Malti 🇲🇹</option>
			<option value="ga">Gaeilge 🇮🇪</option>
		</select>
		<script>
			let selector = document.querySelector("#idioma")
			selector.onchange = function(){
				window.location = window.location+"?lang="+this.value
			}
		</script>
	</body>
</html>

