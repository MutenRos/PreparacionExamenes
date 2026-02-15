<?php
session_start();

function ask_ollama(string $userPrompt): string {
  $prompt = $userPrompt . "
  - responde en un solo párrafo, sin código, en prosa.
  - acepta solo preguntas relacionadas con programación, no aceptes otras temáticas";

  $data = [
    "model"  => "qwen2.5:7b-instruct-q4_0",
    "prompt" => $prompt,
    "stream" => false
  ];

  $ch = curl_init("http://localhost:11434/api/generate");
  curl_setopt_array($ch, [
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_POST           => true,
    CURLOPT_HTTPHEADER     => ["Content-Type: application/json"],
    CURLOPT_POSTFIELDS     => json_encode($data),
  ]);
  $response = curl_exec($ch);
  curl_close($ch);

  $result = json_decode($response ?? "", true);
  return $result["response"] ?? "Error: no se pudo obtener respuesta.";
}

$pregunta = null;
$respuesta = null;
$showSpinner = false;
$metaRefresh = "";

// Step A: user submits -> render page with spinner, compute answer on server AFTER flush
if ($_SERVER["REQUEST_METHOD"] === "POST" && isset($_POST["prompt"])) {
  $pregunta = trim((string)$_POST["prompt"]);
  $_SESSION["last_prompt"] = $pregunta;
  $_SESSION["answer_ready"] = false;
  $_SESSION["last_answer"] = "";

  $showSpinner = true;

  // Auto-refresh once to replace spinner with answer (no JS)
  $metaRefresh = '<meta http-equiv="refresh" content="0.8;url=?step=answer">';

  // Render immediately (spinner visible)
  // Then finish request and compute answer (so user sees spinner right away)
  // ---- render starts below ----

  // We'll compute after output is flushed (down below).
}

// Step B: answer page (after refresh)
if (isset($_GET["step"]) && $_GET["step"] === "answer") {
  $pregunta = $_SESSION["last_prompt"] ?? null;

  if (!empty($_SESSION["answer_ready"])) {
    $respuesta = $_SESSION["last_answer"] ?? "";
    $showSpinner = false;
  } else {
    // If answer not ready yet, keep spinner + refresh again
    $showSpinner = true;
    $metaRefresh = '<meta http-equiv="refresh" content="0.8;url=?step=answer">';
  }
}
?>
<!doctype html>
<html>
<head>
  <style>
    html,body{background:lightgray;width:100%;height:100%;padding:0;margin:0;font-family:Ubuntu,sans-serif;}
    body{display:flex;align-items:center;justify-content:center;}
    section{width:500px;height:500px;padding:20px;background:white;display:flex;flex-direction:column;justify-content:space-between;align-items:stretch;border-radius:30px;}
    form input{width:100%;box-sizing:border-box;padding:10px;border:1px solid lightgrey;border-radius:30px;outline:none;transition:all 1s;}
    form input:focus{background:lightgray;box-shadow:0px 10px 20px rgba(0,0,0,0.3) inset;}
    #pregunta{background:lightgray;width:80%;padding:20px;border-radius:0 15px 15px 15px;align-self:flex-start;}
    #respuesta{background:lightgray;width:80%;padding:20px;border-radius:15px 0 15px 15px;align-self:flex-end;text-align:left;min-height:54px;display:flex;align-items:center;gap:12px;}
    p{margin:0;padding:0;}
    h1,h3{text-align:center;}

    /* Simple spinner */
    .spinner{
      width:18px;height:18px;border-radius:50%;
      border:3px solid rgba(0,0,0,0.15);
      border-top-color: rgba(0,0,0,0.55);
      animation: spin .8s linear infinite;
      flex: 0 0 auto;
    }
    @keyframes spin { to { transform: rotate(360deg); } }
    .muted{opacity:.7;font-size:13px;}
  </style>
  <?= $metaRefresh ?>
</head>
<body>
<section>
  <h1>jocarsa | microchat</h1>

  <?php if (!$pregunta): ?>
    <h3>¿Qué quieres hacer hoy?</h3>
  <?php else: ?>
    <p id="pregunta"><?= htmlspecialchars($pregunta, ENT_QUOTES, "UTF-8") ?></p>

    <p id="respuesta">
      <?php if ($showSpinner): ?>
        <span class="spinner"></span>
        <span class="muted">Pensando…</span>
      <?php else: ?>
        <?= htmlspecialchars((string)$respuesta, ENT_QUOTES, "UTF-8") ?>
      <?php endif; ?>
    </p>
  <?php endif; ?>

  <form method="POST" action="?">
    <input type="text" name="prompt" autocomplete="off" autofocus>
  </form>
</section>
</body>
</html>
<?php
// If we came from POST, compute the answer after sending HTML so spinner shows immediately.
if ($_SERVER["REQUEST_METHOD"] === "POST" && isset($_POST["prompt"])) {
  // Try to flush output so browser renders spinner
  @ob_flush(); @flush();

  // If PHP-FPM, this sends response to client and continues running server-side
  if (function_exists("fastcgi_finish_request")) {
    @fastcgi_finish_request();
  }

  $ans = ask_ollama($_SESSION["last_prompt"] ?? "");
  $_SESSION["last_answer"] = $ans;
  $_SESSION["answer_ready"] = true;
}

