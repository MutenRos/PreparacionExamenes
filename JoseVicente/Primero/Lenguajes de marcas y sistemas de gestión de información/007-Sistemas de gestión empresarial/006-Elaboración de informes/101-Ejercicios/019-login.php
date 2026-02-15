<?php
// ============================================================
// Login + sesión (user: jocarsa / pass: jocarsa)
// + Reemplazar SIEMPRE preguntas.json con lo enviado (sin tocar HTML base)
// ============================================================

session_start();

// --- credenciales ---
const LOGIN_USER = "jocarsa";
const LOGIN_PASS = "jocarsa";

// --- logout ---
if (isset($_GET["logout"])) {
    $_SESSION = [];
    if (ini_get("session.use_cookies")) {
        $p = session_get_cookie_params();
        setcookie(session_name(), "", time() - 42000, $p["path"], $p["domain"], $p["secure"], $p["httponly"]);
    }
    session_destroy();
    header("Location: ?");
    exit;
}

// --- procesar login ---
$login_error = "";
if ($_SERVER["REQUEST_METHOD"] === "POST" && ($_POST["accion"] ?? "") === "login") {
    $u = trim($_POST["usuario"] ?? "");
    $p = trim($_POST["password"] ?? "");

    if ($u === LOGIN_USER && $p === LOGIN_PASS) {
        $_SESSION["auth"] = true;
        header("Location: ?");
        exit;
    } else {
        $login_error = "Credenciales incorrectas";
    }
}

// --- si NO está logueado, mostrar login (minimal) y salir ---
if (empty($_SESSION["auth"])) {
    ?>
    <!doctype html>
    <html lang="es">
    <head>
      <meta charset="utf-8" />
      <meta name="viewport" content="width=device-width,initial-scale=1" />
      <title>Login</title>
      <style>
        html,body{padding:0;margin:0;width:100%;height:100%;}
        body{display:flex;justify-content:center;align-items:center;font-family:sans-serif;}
        form{width:80%;max-width:420px;display:flex;flex-direction:column;gap:20px;}
        input{padding:10px;border:1px solid indigo;border-radius:50px;outline:none;}
        input[type=submit]{background:indigo;color:white;border-radius:50px;border:none;}
        .error{color:crimson;text-align:center;}
      </style>
    </head>
    <body>
      <form action="?" method="POST">
        <h3>Acceso</h3>
        <?php if ($login_error): ?><div class="error"><?= htmlspecialchars($login_error) ?></div><?php endif; ?>
        <input type="hidden" name="accion" value="login">
        <input type="text" name="usuario" placeholder="Usuario" autocomplete="username" required>
        <input type="password" name="password" placeholder="Password" autocomplete="current-password" required>
        <input type="submit" value="Entrar">
      </form>
    </body>
    </html>
    <?php
    exit;
}

// ============================================================
// Ya logueado: guardar preguntas.json (tu lógica)
// ============================================================

if ($_SERVER["REQUEST_METHOD"] === "POST" && empty($_POST["accion"])) {

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
         a.logout{position:fixed;top:10px;right:10px;color:indigo;text-decoration:none;font-weight:bold;}
	  </style>
	</head>
	<body>
      <a class="logout" href="?logout=1">Salir</a>
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

