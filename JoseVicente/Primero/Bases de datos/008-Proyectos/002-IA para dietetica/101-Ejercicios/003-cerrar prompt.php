<?php
function h($s): string { return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }

$defaultPrompt = "";
$model   = $_POST["model"]   ?? "llama3:latest";
$prompt  = $_POST["prompt"]  ?? $defaultPrompt;
$baseUrl = $_POST["baseUrl"] ?? "http://127.0.0.1:11434"; // Ollama server

$result = null;

if ($_SERVER["REQUEST_METHOD"] === "POST") {
  $prompt = trim("Eres un consejero dietético. El usuario te va a proporcionar una serie de ingrediente que tiene un nevera. Debes elaborar una receta dietética, lo más saludable y sabrosa posible, con los ingredientes que el usuario te proporcione, que son estos: ".$prompt);
  if ($prompt === "") $prompt = $defaultPrompt;

  $payload = [
    "model"  => $model,
    "prompt" => $prompt,
    "stream" => false
  ];

  $url = rtrim($baseUrl, "/") . "/api/generate";

  $ch = curl_init($url);
  curl_setopt_array($ch, [
    CURLOPT_POST           => true,
    CURLOPT_RETURNTRANSFER => true,
    CURLOPT_HTTPHEADER     => ["Content-Type: application/json"],
    CURLOPT_POSTFIELDS     => json_encode($payload, JSON_UNESCAPED_UNICODE),
    CURLOPT_CONNECTTIMEOUT => 5,
    CURLOPT_TIMEOUT        => 90,
  ]);

  $raw = curl_exec($ch);
  $httpCode = (int)curl_getinfo($ch, CURLINFO_HTTP_CODE);
  $curlErr  = curl_error($ch);
  curl_close($ch);

  if ($raw === false) {
    $result = ["ok" => false, "err" => "cURL error: " . $curlErr, "out" => ""];
  } elseif ($httpCode < 200 || $httpCode >= 300) {
    $result = ["ok" => false, "err" => "HTTP $httpCode\n$raw", "out" => ""];
  } else {
    $json = json_decode($raw, true);
    if (!is_array($json)) {
      $result = ["ok" => false, "err" => "Respuesta no-JSON:\n$raw", "out" => ""];
    } else {
      // Ollama devuelve normalmente {"response": "...", "done": true, ...}
      $result = ["ok" => true, "out" => (string)($json["response"] ?? ""), "err" => ""];
    }
  }
}
?>
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Ollama Web (PHP → HTTP API)</title>
  <style>
    body{font-family:system-ui,-apple-system,Segoe UI,Roboto,Ubuntu,Arial,sans-serif;max-width:900px;margin:40px auto;padding:0 16px;line-height:1.4}
    .card{border:1px solid #e5e5e5;border-radius:12px;padding:16px;margin:16px 0}
    label{display:block;font-weight:600;margin:10px 0 6px}
    textarea,input{width:100%;padding:10px;border:1px solid #d6d6d6;border-radius:10px;font:inherit}
    textarea{min-height:140px}
    button{padding:10px 14px;border:0;border-radius:10px;cursor:pointer;font-weight:600}
    .row{display:grid;grid-template-columns:1fr 1fr;gap:12px}
    pre{white-space:pre-wrap;word-wrap:break-word;background:#0b0b0b;color:#f1f1f1;padding:12px;border-radius:12px;overflow:auto}
    .err{background:#fff3f3;border:1px solid #ffd0d0;color:#7a0000;padding:12px;border-radius:12px}
    @media (max-width:700px){.row{grid-template-columns:1fr}}
    .row{display:none;}
  </style>
</head>
<body>

<h1>Ollama Web (PHP → HTTP API)</h1>

<div class="card">
  <form method="post">
    <div class="row">
      <div>
        <label for="model">Modelo</label>
        <input id="model" name="model" value="<?=h($model)?>" placeholder="llama3:latest">
      </div>
      <div>
        <label for="baseUrl">Ollama URL</label>
        <input id="baseUrl" name="baseUrl" value="<?=h($baseUrl)?>" placeholder="http://127.0.0.1:11434">
      </div>
    </div>
    <p>Vamos a crear recetas saludables - a continuación indica los alimentos que tienes en la nevera<br>
    La inteligencia artificial te creará recetas saludables con ellos.</p>
    <label for="prompt">Indica qué alimentos tienes en tu cocina:</label>
    <textarea id="prompt" name="prompt"><?=h($prompt)?></textarea>

    <div style="margin-top:12px;">
      <button type="submit">Preguntar</button>
    </div>
  </form>
</div>

<?php if ($result !== null): ?>
  <div class="card">
    <h2>Respuesta</h2>
    <?php if (!$result["ok"]): ?>
      <div class="err"><?=nl2br(h($result["err"]))?></div>
    <?php else: ?>
      <pre><?=h($result["out"])?></pre>
    <?php endif; ?>
  </div>
<?php endif; ?>

<div class="card">
  <small>
    Si esto te da HTTP 404/connection refused, el problema no es PHP: es que Ollama no está escuchando en esa URL/puerto
    o no permite conexiones desde el contexto donde corre Apache.
  </small>
</div>

</body>
</html>

