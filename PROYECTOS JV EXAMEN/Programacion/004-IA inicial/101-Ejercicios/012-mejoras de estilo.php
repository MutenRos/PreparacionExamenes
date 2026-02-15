<?php
session_start();

/**
 * Call Ollama (blocking) and return the response text.
 */
function ask_ollama(string $userPrompt): string {
  $prompt = $userPrompt . "
  - responde en un solo párrafo, sin código, en prosa.
  - acepta solo preguntas relacionadas con programación, no aceptes otras temáticas
  - respuestas solo en español";

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

/**
 * STEP A: POST -> show page immediately with spinner, compute answer after flush,
 * then page auto-refreshes to show answer.
 */
if ($_SERVER["REQUEST_METHOD"] === "POST" && isset($_POST["prompt"])) {
  $pregunta = trim((string)$_POST["prompt"]);

  // Validación: rechazar prompts vacíos o demasiado largos (máx. 500 caracteres)
  if ($pregunta === "" || mb_strlen($pregunta) > 500) {
    $pregunta = null;
  }

  if ($pregunta !== null) {
  $_SESSION["last_prompt"]  = $pregunta;
  $_SESSION["last_answer"]  = "";
  $_SESSION["answer_ready"] = false;

  $showSpinner = true;
  $metaRefresh = '<meta http-equiv="refresh" content="0.8;url=?step=answer">';
  } // fin validación
}

/**
 * STEP B: answer step (after refresh)
 */
if (isset($_GET["step"]) && $_GET["step"] === "answer") {
  $pregunta = $_SESSION["last_prompt"] ?? null;

  if (!empty($_SESSION["answer_ready"])) {
    $respuesta = $_SESSION["last_answer"] ?? "";
    $showSpinner = false;
  } else {
    $showSpinner = true;
    $metaRefresh = '<meta http-equiv="refresh" content="0.8;url=?step=answer">';
  }
}
?>
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>jocarsa | microchat</title>

  <?= $metaRefresh ?>

  <style>
    :root{
      --bg: #eef1f4;
      --card: #ffffff;
      --ink: #111827;
      --muted: #6b7280;
      --line: #e5e7eb;
      --soft: #f3f4f6;
      --shadow: 0 18px 50px rgba(0,0,0,.12);
      --shadow-soft: 0 10px 25px rgba(0,0,0,.08);
      --radius: 22px;
    }

    *{ box-sizing:border-box; }

    html,body{
      width:100%;
      height:100%;
      margin:0;
      padding:0;
      font-family: Ubuntu, system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
      color: var(--ink);
      background:
        radial-gradient(1200px 600px at 20% 10%, rgba(255,255,255,.7), transparent 60%),
        radial-gradient(900px 500px at 90% 30%, rgba(255,255,255,.55), transparent 55%),
        var(--bg);
    }

    body{
      display:flex;
      align-items:center;
      justify-content:center;
      padding:24px;
    }

    section{
      width:min(560px, 100%);
      height:min(560px, 100%);
      background:var(--card);
      border:1px solid rgba(0,0,0,.06);
      border-radius: calc(var(--radius) + 6px);
      box-shadow: var(--shadow);
      padding:22px;
      display:flex;
      flex-direction:column;
      gap:14px;
      overflow:hidden;
    }

    .titleWrap{
      display:flex;
      align-items:flex-start;
      justify-content:space-between;
      gap:12px;
      padding-bottom:10px;
      border-bottom:1px solid var(--line);
    }

    h1{
      margin:0;
      font-size:18px;
      letter-spacing:.2px;
      font-weight:700;
      line-height:1.2;
    }

    .badge{
      font-size:12px;
      color:var(--muted);
      background:var(--soft);
      border:1px solid rgba(0,0,0,.05);
      padding:6px 10px;
      border-radius:999px;
      white-space:nowrap;
    }

    h3{
      margin:6px 0 0 0;
      text-align:center;
      font-size:14px;
      font-weight:600;
      color:var(--muted);
    }

    .messages{
      flex:1;
      display:flex;
      flex-direction:column;
      gap:12px;
      padding:6px 2px;
      overflow:auto;
    }

    .bubble{
      width:fit-content;
      max-width: 86%;
      padding:12px 14px;
      background:var(--soft);
      border:1px solid rgba(0,0,0,.06);
      border-radius:16px;
      box-shadow: var(--shadow-soft);
      line-height:1.35;
      font-size:14px;
      white-space:pre-wrap;
      word-break:break-word;
    }

    #pregunta{
      align-self:flex-start;
      border-top-left-radius:8px;
    }

    #respuesta{
      align-self:flex-end;
      border-top-right-radius:8px;
      display:flex;
      align-items:center;
      gap:10px;
      min-height:46px;
      animation: fadeIn .4s ease-out;
    }

    form{
      padding-top:12px;
      border-top:1px solid var(--line);
    }

    form input{
      width:100%;
      padding:12px 14px;
      border-radius:999px;
      border:1px solid var(--line);
      background:#fff;
      outline:none;
      font-size:14px;
      box-shadow: 0 1px 0 rgba(0,0,0,.02);
      transition: border-color .2s ease, box-shadow .2s ease, background .2s ease;
    }

    form input::placeholder{ color:#9ca3af; }

    form input:focus{
      border-color: rgba(17,24,39,.35);
      box-shadow: 0 0 0 4px rgba(17,24,39,.08);
      background:#fff;
    }

    .spinner{
      width:16px;
      height:16px;
      border-radius:50%;
      border:3px solid rgba(17,24,39,0.12);
      border-top-color: rgba(17,24,39,0.55);
      animation: spin .8s linear infinite;
      flex:0 0 auto;
    }
    @keyframes spin { to { transform: rotate(360deg); } }

    /* Animación de aparición suave para la burbuja de respuesta */
    @keyframes fadeIn {
      from { opacity: 0; transform: translateY(6px); }
      to   { opacity: 1; transform: translateY(0); }
    }

    .muted{
      font-size:13px;
      color:var(--muted);
    }

    .messages::-webkit-scrollbar{ width:10px; }
    .messages::-webkit-scrollbar-thumb{
      background: rgba(0,0,0,.10);
      border-radius:999px;
      border:3px solid transparent;
      background-clip: content-box;
    }

    @media (max-width: 520px){
      section{ height: 92vh; padding:18px; }
      .bubble{ max-width: 92%; }
    }

    /* Modo oscuro automático según preferencia del sistema */
    @media (prefers-color-scheme: dark){
      :root{
        --bg: #0f1117;
        --card: #1a1d27;
        --ink: #e5e7eb;
        --muted: #9ca3af;
        --line: #2d3140;
        --soft: #23262f;
      }
      form input{ background: var(--soft); color: var(--ink); border-color: var(--line); }
      form input::placeholder{ color: var(--muted); }
    }

    /* Contador de caracteres */
    .charCount{
      text-align:right;
      font-size:11px;
      color:var(--muted);
      padding:4px 14px 0;
      transition: color .2s;
    }
    .charCount.warn{ color:#ef4444; }
  </style>
</head>
<body>
  <section>
    <div class="titleWrap">
      <h1>jocarsa | microchat</h1>
      <span class="badge">local</span>
    </div>

    <div class="messages">
      <?php if (!$pregunta): ?>
        <h3>¿Qué quieres hacer hoy?</h3>
      <?php else: ?>
        <p id="pregunta" class="bubble"><?= htmlspecialchars($pregunta, ENT_QUOTES, "UTF-8") ?></p>

        <p id="respuesta" class="bubble" role="status" aria-live="polite">
          <?php if ($showSpinner): ?>
            <span class="spinner" aria-hidden="true"></span>
            <span class="muted">Pensando…</span>
          <?php else: ?>
            <?= htmlspecialchars((string)$respuesta, ENT_QUOTES, "UTF-8") ?>
          <?php endif; ?>
        </p>
      <?php endif; ?>
    </div>

    <form method="POST" action="?">
      <label for="promptInput" class="muted" style="display:none;">Pregunta</label>
      <input
        id="promptInput"
        type="text"
        name="prompt"
        placeholder="Escribe una pregunta sobre programación y pulsa Enter…"
        autocomplete="off"
        autofocus
        maxlength="500"
        aria-label="Escribe tu pregunta sobre programación"
      >
      <div class="charCount" id="charCount" aria-live="polite">0 / 500</div>
    </form>
    <script>
      // Contador de caracteres en tiempo real
      const inp = document.getElementById('promptInput');
      const cnt = document.getElementById('charCount');
      if (inp && cnt) {
        inp.addEventListener('input', function() {
          const len = this.value.length;
          cnt.textContent = len + ' / 500';
          cnt.classList.toggle('warn', len > 450);
        });
      }
    </script>
  </section>
</body>
</html>
<?php
// If we came from POST, compute the answer after the HTML has been sent
// so the user sees the spinner immediately.
if ($_SERVER["REQUEST_METHOD"] === "POST" && isset($_POST["prompt"])) {
  @ob_flush(); @flush();

  if (function_exists("fastcgi_finish_request")) {
    @fastcgi_finish_request();
  }

  $ans = ask_ollama($_SESSION["last_prompt"] ?? "");
  $_SESSION["last_answer"]  = $ans;
  $_SESSION["answer_ready"] = true;
}

