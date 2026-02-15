<?php
function h($s): string { return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }

/**
 * Markdown -> HTML (seguro)
 * - Escapa HTML primero (evita inyección)
 * - Soporta: #..######, **bold**, *italic*, `code`, ```fenced code```, listas -, *, 1., párrafos
 */
function md_to_html_safe(string $md): string {
  $md = str_replace(["\r\n", "\r"], "\n", $md);
  $md = h($md);

  // Fenced code blocks ```lang?\n...\n```
  $md = preg_replace_callback('/```([a-zA-Z0-9_-]+)?\n([\s\S]*?)\n```/m', function($m){
    $lang = trim((string)($m[1] ?? ""));
    $code = (string)($m[2] ?? "");
    $class = $lang !== "" ? ' class="language-'.h($lang).'"' : '';
    return '<pre class="code"><code'.$class.'>'.$code.'</code></pre>';
  }, $md);

  // Headings
  for ($i = 6; $i >= 1; $i--) {
    $md = preg_replace('/^' . str_repeat('#', $i) . '\s+(.+)$/m', "<h$i>$1</h$i>", $md);
  }

  // Inline code
  $md = preg_replace('/`([^`\n]+)`/', '<code class="inline">$1</code>', $md);

  // Bold / italic (simple)
  $md = preg_replace('/\*\*([^*\n]+)\*\*/', '<strong>$1</strong>', $md);
  $md = preg_replace('/\*([^*\n]+)\*/', '<em>$1</em>', $md);

  // Unordered lists (- or *)
  $md = preg_replace_callback('/(?:^|\n)(?:- |\* ).+(?:\n(?:- |\* ).+)*/m', function($m){
    $block = trim($m[0], "\n");
    $lines = preg_split("/\n/", $block);
    $items = [];
    foreach ($lines as $ln) {
      $ln = preg_replace('/^(?:- |\* )/', '', $ln);
      $items[] = "<li>$ln</li>";
    }
    return "\n<ul>\n" . implode("\n", $items) . "\n</ul>\n";
  }, $md);

  // Ordered lists (1. 2. ...)
  $md = preg_replace_callback('/(?:^|\n)(?:\d+\. ).+(?:\n(?:\d+\. ).+)*/m', function($m){
    $block = trim($m[0], "\n");
    $lines = preg_split("/\n/", $block);
    $items = [];
    foreach ($lines as $ln) {
      $ln = preg_replace('/^\d+\. /', '', $ln);
      $items[] = "<li>$ln</li>";
    }
    return "\n<ol>\n" . implode("\n", $items) . "\n</ol>\n";
  }, $md);

  // Paragraphs: split by blank lines, wrap non-blocks
  $parts = preg_split("/\n{2,}/", $md);
  $out = [];
  foreach ($parts as $p) {
    $p = trim($p);
    if ($p === "") continue;

    // If it starts with a block tag, keep as-is
    if (preg_match('/^(<h[1-6]>|<ul>|<ol>|<pre\b)/', $p)) {
      $out[] = $p;
    } else {
      // Preserve single newlines inside paragraphs
      $p = preg_replace("/\n/", "<br>", $p);
      $out[] = "<p>$p</p>";
    }
  }

  return implode("\n", $out);
}

$defaultPrompt = "";
$model   = $_POST["model"]   ?? "llama3:latest";
$prompt  = $_POST["prompt"]  ?? $defaultPrompt;
$baseUrl = $_POST["baseUrl"] ?? "http://127.0.0.1:11434"; // Ollama server

$result = null;

if ($_SERVER["REQUEST_METHOD"] === "POST") {
  $prompt = trim("Eres un consejero informático. El usuario te va a indicar el presupuesto económico que tiene, y para qué quiere usar su ordenador. Debes detallar los componentes que el usuario debe adquirir, su precio aproximado y luego la suma del total (importante - calcula realmente el total de la suma de los componentes): ".$prompt);
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
    :root{
      --bg: #0b1020;
      --panel: rgba(255,255,255,.06);
      --panel2: rgba(255,255,255,.08);
      --border: rgba(255,255,255,.12);
      --text: rgba(255,255,255,.92);
      --muted: rgba(255,255,255,.68);
      --accent: #7dd3fc; /* cyan-300 */
      --accent2: #a78bfa; /* violet-400 */
      --dangerBg: rgba(255,80,80,.12);
      --dangerBorder: rgba(255,80,80,.35);
      --dangerText: #ffd6d6;
      --shadow: 0 20px 60px rgba(0,0,0,.45);
      --radius: 16px;
    }

    *{box-sizing:border-box}
    html,body{height:100%}
    body{
      margin:0;
      font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Arial, sans-serif;
      background:
        radial-gradient(1200px 700px at 10% 10%, rgba(125,211,252,.14), transparent 55%),
        radial-gradient(1000px 650px at 85% 20%, rgba(167,139,250,.12), transparent 60%),
        radial-gradient(900px 600px at 40% 95%, rgba(34,197,94,.08), transparent 55%),
        var(--bg);
      color: var(--text);
    }

    .app{
      height:100vh;
      width:100vw;
      display:grid;
      grid-template-columns: minmax(340px, 420px) 1fr;
      gap: 14px;
      padding: 14px;
    }

    .panel{
      background: var(--panel);
      border: 1px solid var(--border);
      border-radius: var(--radius);
      box-shadow: var(--shadow);
      overflow:hidden;
      display:flex;
      flex-direction:column;
      min-height:0;
    }

    .panelHeader{
      padding: 14px 16px;
      border-bottom: 1px solid var(--border);
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap: 10px;
      background: linear-gradient(to bottom, rgba(255,255,255,.06), rgba(255,255,255,.03));
    }

    .brand{
      display:flex; align-items:center; gap:10px;
      min-width:0;
    }
    .dot{
      width:12px;height:12px;border-radius:999px;
      background: linear-gradient(135deg, var(--accent), var(--accent2));
      box-shadow: 0 0 0 4px rgba(125,211,252,.12);
      flex: 0 0 auto;
    }
    .brand h1{
      font-size: 14px;
      margin:0;
      letter-spacing:.2px;
      white-space:nowrap;
      overflow:hidden;
      text-overflow:ellipsis;
    }
    .brand p{
      margin:0;
      font-size: 12px;
      color: var(--muted);
      white-space:nowrap;
      overflow:hidden;
      text-overflow:ellipsis;
    }

    .toolbar{
      display:flex; gap:8px; align-items:center;
      flex: 0 0 auto;
    }

    .btn{
      appearance:none;
      border:1px solid var(--border);
      background: rgba(255,255,255,.06);
      color: var(--text);
      padding: 10px 12px;
      border-radius: 12px;
      cursor:pointer;
      font-weight: 650;
      transition: transform .05s ease, background .15s ease, border-color .15s ease;
      user-select:none;
    }
    .btn:hover{background: rgba(255,255,255,.10); border-color: rgba(255,255,255,.18)}
    .btn:active{transform: translateY(1px)}
    .btnPrimary{
      border-color: rgba(125,211,252,.35);
      background: linear-gradient(135deg, rgba(125,211,252,.18), rgba(167,139,250,.14));
    }

    .content{
      padding: 14px 16px;
      overflow:auto;
      min-height:0;
    }

    label{
      display:block;
      margin: 12px 0 6px;
      font-weight: 700;
      font-size: 12px;
      color: rgba(255,255,255,.80);
      letter-spacing:.2px;
    }

    textarea, input{
      width:100%;
      background: rgba(0,0,0,.18);
      border: 1px solid rgba(255,255,255,.14);
      color: var(--text);
      border-radius: 14px;
      padding: 12px 12px;
      font: inherit;
      outline: none;
      transition: border-color .15s ease, background .15s ease;
    }
    textarea:focus, input:focus{
      border-color: rgba(125,211,252,.45);
      background: rgba(0,0,0,.22);
    }
    textarea{min-height: 42vh; resize: vertical}

    .hint{
      margin: 10px 0 0;
      font-size: 12px;
      color: var(--muted);
      line-height: 1.45;
    }

    details{
      margin-top: 12px;
      border: 1px solid rgba(255,255,255,.12);
      border-radius: 14px;
      background: rgba(255,255,255,.04);
      overflow:hidden;
    }
    summary{
      cursor:pointer;
      list-style:none;
      padding: 12px 12px;
      font-weight: 700;
      font-size: 12px;
      color: rgba(255,255,255,.85);
    }
    summary::-webkit-details-marker{display:none}
    .settings{
      padding: 0 12px 12px;
      display:grid;
      grid-template-columns: 1fr;
      gap: 10px;
    }

    /* RIGHT PANEL (response) */
    .responseWrap{
      display:flex;
      flex-direction:column;
      min-height:0;
    }

    .responseBody{
      padding: 14px 16px;
      overflow:auto;
      min-height:0;
    }

    .responseCard{
      background: rgba(0,0,0,.55);
      border: 1px solid rgba(255,255,255,.14);
      border-radius: var(--radius);
      box-shadow: inset 0 0 0 1px rgba(255,255,255,.03);
      overflow:hidden;
    }

    .responseHead{
      padding: 12px 14px;
      border-bottom: 1px solid rgba(255,255,255,.12);
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap: 10px;
      background: linear-gradient(to bottom, rgba(255,255,255,.06), rgba(255,255,255,.02));
    }

    .responseTitle{
      display:flex; align-items:center; gap:10px; min-width:0;
    }
    .badge{
      font-size: 11px;
      padding: 6px 10px;
      border-radius: 999px;
      border: 1px solid rgba(255,255,255,.16);
      color: rgba(255,255,255,.82);
      background: rgba(255,255,255,.06);
      white-space:nowrap;
    }

    /* Markdown typography */
    .md{
      padding: 16px 16px 18px;
      line-height: 1.65;
      color: rgba(255,255,255,.92);
      font-size: 15px;
    }
    .md h1,.md h2,.md h3,.md h4,.md h5,.md h6{
      margin: 16px 0 10px;
      line-height: 1.2;
      letter-spacing:.2px;
    }
    .md h1{font-size: 22px}
    .md h2{font-size: 18px}
    .md h3{font-size: 16px}
    .md p{margin: 10px 0}
    .md ul,.md ol{margin: 10px 0 10px 22px}
    .md li{margin: 6px 0}
    .md strong{color: rgba(255,255,255,.98)}
    .md em{color: rgba(255,255,255,.86)}
    .md code.inline{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
      font-size: .95em;
      padding: 2px 6px;
      border-radius: 8px;
      border: 1px solid rgba(255,255,255,.14);
      background: rgba(255,255,255,.06);
      color: rgba(255,255,255,.92);
    }
    .md pre.code{
      margin: 12px 0;
      padding: 12px 12px;
      border-radius: 14px;
      background: rgba(0,0,0,.55);
      border: 1px solid rgba(255,255,255,.14);
      overflow:auto;
    }
    .md pre.code code{
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
      font-size: 13px;
      white-space: pre;
      display:block;
      color: rgba(255,255,255,.90);
    }

    .emptyState{
      height:100%;
      display:flex;
      align-items:center;
      justify-content:center;
      padding: 28px;
      text-align:center;
      color: var(--muted);
    }
    .emptyState .box{
      max-width: 520px;
      border: 1px dashed rgba(255,255,255,.18);
      border-radius: var(--radius);
      padding: 22px 18px;
      background: rgba(255,255,255,.03);
    }

    .err{
      margin: 14px 16px 16px;
      background: var(--dangerBg);
      border: 1px solid var(--dangerBorder);
      color: var(--dangerText);
      padding: 12px 12px;
      border-radius: 14px;
      white-space: pre-wrap;
      word-wrap: break-word;
    }

    /* Responsive */
    @media (max-width: 980px){
      .app{grid-template-columns: 1fr; height:auto; min-height:100vh}
      textarea{min-height: 32vh}
    }
  </style>
</head>
<body>

<div class="app">

  <!-- LEFT: FORM -->
  <section class="panel">
    <div class="panelHeader">
      <div class="brand">
        <span class="dot" aria-hidden="true"></span>
        <div style="min-width:0">
          <h1>Ollama Web</h1>
          <p>Componentes PC por presupuesto y uso</p>
        </div>
      </div>
      <div class="toolbar">
        <button class="btn" type="button" id="clearBtn" title="Limpiar formulario">Limpiar</button>
        <button class="btn btnPrimary" type="button" id="submitBtn" title="Enviar consulta">Enviar</button>
      </div>
    </div>

    <div class="content">
      <form method="post" id="theForm">
        <p class="hint">
          Indica <strong>presupuesto</strong> (p. ej. 900€) y <strong>uso</strong> (ofimática, edición de vídeo, IA, gaming, etc.).
          La respuesta se mostrará a la derecha con formato legible.
        </p>

        <label for="prompt">Tu petición</label>
        <textarea id="prompt" name="prompt" placeholder="Ejemplo: Tengo 1200€ y lo quiero para edición de vídeo 4K y algo de gaming."><?=h($prompt)?></textarea>

        <details>
          <summary>Ajustes (modelo y URL)</summary>
          <div class="settings">
            <div>
              <label for="model">Modelo</label>
              <input id="model" name="model" value="<?=h($model)?>" placeholder="llama3:latest">
            </div>
            <div>
              <label for="baseUrl">Ollama URL</label>
              <input id="baseUrl" name="baseUrl" value="<?=h($baseUrl)?>" placeholder="http://127.0.0.1:11434">
            </div>
          </div>
        </details>

        <!-- submit real (hidden) -->
        <button type="submit" style="display:none" aria-hidden="true" tabindex="-1"></button>
      </form>
    </div>
  </section>

  <!-- RIGHT: RESPONSE -->
  <section class="panel responseWrap">
    <div class="panelHeader">
      <div class="brand">
        <span class="dot" aria-hidden="true"></span>
        <div style="min-width:0">
          <h1>Respuesta</h1>
          <p>Render Markdown → HTML</p>
        </div>
      </div>
      <div class="toolbar">
        <span class="badge"><?=h($model)?></span>
      </div>
    </div>

    <div class="responseBody">
      <div class="responseCard">
        <div class="responseHead">
          <div class="responseTitle">
            <span class="badge">Salida</span>
            <?php if ($result !== null): ?>
              <span class="badge"><?= $result["ok"] ? "OK" : "ERROR" ?></span>
            <?php else: ?>
              <span class="badge">Sin consulta</span>
            <?php endif; ?>
          </div>
          <button class="btn" type="button" id="copyBtn" title="Copiar respuesta">Copiar</button>
        </div>

        <?php if ($result === null): ?>
          <div class="emptyState">
            <div class="box">
              Escribe tu presupuesto y el uso del ordenador en el panel izquierdo y pulsa <strong>Enviar</strong>.
            </div>
          </div>
        <?php elseif (!$result["ok"]): ?>
          <div class="err"><?=h($result["err"])?></div>
        <?php else: ?>
          <div class="md" id="mdOut">
            <?= md_to_html_safe($result["out"]) ?>
          </div>
        <?php endif; ?>
      </div>
    </div>
  </section>

</div>

<script>
  const form = document.getElementById('theForm');
  const submitBtn = document.getElementById('submitBtn');
  const clearBtn  = document.getElementById('clearBtn');
  const promptEl  = document.getElementById('prompt');
  const copyBtn   = document.getElementById('copyBtn');

  submitBtn.addEventListener('click', () => form.requestSubmit());

  clearBtn.addEventListener('click', () => {
    promptEl.value = '';
    promptEl.focus();
  });

  copyBtn.addEventListener('click', async () => {
    const mdOut = document.getElementById('mdOut');
    if (!mdOut) return;
    const text = mdOut.innerText;
    try{
      await navigator.clipboard.writeText(text);
      copyBtn.textContent = 'Copiado';
      setTimeout(() => copyBtn.textContent = 'Copiar', 900);
    }catch(e){
      copyBtn.textContent = 'No se pudo';
      setTimeout(() => copyBtn.textContent = 'Copiar', 900);
    }
  });

  // Si hay respuesta, sube al principio del panel derecho (mejor lectura)
  const mdOut = document.getElementById('mdOut');
  if (mdOut) {
    mdOut.scrollIntoView({block:'start'});
  }
</script>

</body>
</html>

