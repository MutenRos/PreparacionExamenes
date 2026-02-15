<?php
// ============================================================
// Reemplazar SIEMPRE preguntas.json con lo enviado (sin tocar HTML)
// ============================================================

if ($_SERVER["REQUEST_METHOD"] === "POST") {

    $pregunta = trim($_POST["pregunta"] ?? "");

    $respuestas = [
        trim($_POST["respuesta1"] ?? ""),
        trim($_POST["respuesta2"] ?? ""),
        trim($_POST["respuesta3"] ?? ""),
        trim($_POST["respuesta4"] ?? ""),
        trim($_POST["respuesta5"] ?? ""),
        trim($_POST["respuesta6"] ?? "")
    ];

    // eliminar respuestas vacías
    $respuestas = array_values(array_filter($respuestas, fn($r) => $r !== ""));

    if ($pregunta !== "" && count($respuestas) > 0) {

        $registro = [
            "pregunta"   => $pregunta,
            "respuestas" => $respuestas
        ];

        $archivo = __DIR__ . "/preguntas.json";

        // REEMPLAZA el archivo (no acumula)
        file_put_contents(
            $archivo,
            json_encode($registro, JSON_UNESCAPED_UNICODE | JSON_PRETTY_PRINT),
            LOCK_EX
        );
    }
}
?>

<!doctype html>
<html lang="es">
	<head>
	  <meta charset="utf-8" />
	  <meta name="viewport" content="width=device-width,initial-scale=1" />
	  <title>Resultados (CSV)</title>
	  <style>
		 html,body{padding:0px;margin:0px;width:100%;height:100%;}
		 body{display:flex;justify-content:center;align-items:center;font-family:sans-serif;}
		 form{width:80%;height:80%;display:flex;flex-direction:column;gap:20px;}
		 input{padding:10px;border:1px solid indigo;border-radius:50px;outline:none;}
		 input[type=submit]{background:indigo;color:white;border-radius:50px;}
	  </style>
	</head>
	<body>
	  <form action="?" method="POST">
	  	<h3>Introduce una nueva pregunta</h3>
	  	<input type="text" name="pregunta" placeholder="Introduce la pregunta">
	  	<input type="text" name="respuesta1" placeholder="Introduce la respuesta nº1">
	  	<input type="text" name="respuesta2" placeholder="Introduce la respuesta nº2">
	  	<input type="text" name="respuesta3" placeholder="Introduce la respuesta nº3">
	  	<input type="text" name="respuesta4" placeholder="Introduce la respuesta nº4">
	  	<input type="text" name="respuesta5" placeholder="Introduce la respuesta nº5">
	  	<input type="text" name="respuesta6" placeholder="Introduce la respuesta nº6">
	  	<input type="submit">
	  </form>
	</body>
</html>

