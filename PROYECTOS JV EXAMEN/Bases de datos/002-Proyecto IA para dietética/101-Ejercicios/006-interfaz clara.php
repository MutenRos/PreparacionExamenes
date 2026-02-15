<?php
function h($s): string { return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }

/**
 * Markdown -> HTML (safe, minimal)
 */
function md_to_html_safe(string $md): string {
  $md = str_replace(["\r\n", "\r"], "\n", $md);
  $md = h($md);

  // fenced code
  $md = preg_replace_callback('/```([a-zA-Z0-9_-]+)?\n([\s\S]*?)\n```/m', function($m){
    $lang = trim((string)($m[1] ?? ""));
    $code = (string)($m[2] ?? "");
    $class = $lang !== "" ? ' class="language-'.h($lang).'"' : '';
    return '<pre class="code"><code'.$class.'>'.$code.'</code></pre>';
  }, $md);

  // headings
  for ($i = 6; $i >= 1; $i--) {
    $md = preg_replace('/^' . str_repeat('#', $i) . '\s+(.+)$/m', "<h$i>$1</h$i>", $md);
  }

  // inline code / bold / italic (simple)
  $md = preg_replace('/`([^`\n]+)`/', '<code class="inline">$1</code>', $md);
  $md = preg_replace('/\*\*([^*\n]+)\*\*/', '<strong>$1</strong>', $md);
  $md = preg_replace('/\*([^*\n]+)\*/', '<em>$1</em>', $md);

  // ul
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

  // ol
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

  // paragraphs
  $parts = preg_split("/\n{2,}/", $md);
  $out = [];
  foreach ($parts as $p) {
    $p = trim($p);
    if ($p === "") continue;

    if (preg_match('/^(<h[1-6]>|<ul>|<ol>|<pre\b)/', $p)) {
      $out[] = $p;
    } else {
      $p = preg_replace("/\n/", "<br>", $p);
      $out[] = "<p>$p</p>";
    }
  }
  return implode("\n", $out);
}

$defaultPrompt = "";
$model   = $_POST["model"]   ?? "llama3:latest";
$prompt  = $_POST["prompt"]  ?? $defaultPrompt;
$baseUrl = $_POST["baseUrl"] ?? "http://127.0.0.1:11434";

$result = null;

if ($_SERVER["REQUEST_METHOD"] === "POST") {
  $userPrompt = trim($prompt);
  if ($userPrompt === "") $userPrompt = $defaultPrompt;

  // Limitar longitud del prompt (máx. 2000 caracteres)
  if (mb_strlen($userPrompt) > 2000) {
    $userPrompt = mb_substr($userPrompt, 0, 2000);
  }

  // Prompt reforzado: exige tabla con números + suma verificada
  $systemPrompt = <<<TXT
Eres un asesor informático. El usuario te dará un presupuesto y el uso del PC.

Tu respuesta DEBE cumplir estas reglas:
1) Propón una configuración por componentes (CPU, placa, RAM, GPU si aplica, SSD, PSU, caja, disipación si aplica).
2) Para cada componente indica un precio aproximado en EUR como número (sin rangos; un único valor).
3) Incluye una tabla final "DESGLOSE" con columnas: Componente | Modelo | Precio_EUR.
4) Después incluye un bloque "SUMA" con:
   - Lista de precios usados (solo números) en una línea.
   - Total_EUR = suma exacta de esos números.
5) Vuelve a comprobar la suma: repite el total en una segunda línea "Total_verificado_EUR" y debe coincidir.
6) Si el total supera el presupuesto, ajusta componentes hasta que Total_EUR <= presupuesto y deja margen para envío (si procede).
7) No inventes monedas ni uses USD. No uses notación ambigua. No uses "aprox. 300-350". Solo un número.

Usuario:
{$userPrompt}
TXT;

  $payload = [
    "model"  => $model,
    "prompt" => $systemPrompt,
    "stream" => false
  ];

  $url = rtrim($baseUrl, "/") . "/api/generate";

  $startTime = microtime(true); // Medir tiempo de respuesta de la IA
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
      $elapsed = round(microtime(true) - $startTime, 2);
      $result = ["ok" => true, "out" => (string)($json["response"] ?? ""), "err" => "", "time" => $elapsed];
    }
  }
}
?>
<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>Ollama Web — Asesor de componentes PC</title>
  <meta name="description" content="Interfaz web PHP que consulta un modelo LLM local (Ollama) para recomendar componentes de PC según presupuesto y uso.">
  <style>
    :root{
      --bg: #f6f7f9;
      --panel: #ffffff;
      --border: #e6e8ee;
      --text: #111827;
      --muted: #6b7280;
      --accent: #2563eb;   /* blue */
      --accent2:#111827;   /* near-black */
      --shadow: 0 8px 24px rgba(17,24,39,.08);
      --radius: 14px;
      --mono: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
    }

    *{box-sizing:border-box}
    html,body{height:100%}
    body{
      margin:0;
      font-family: ui-sans-serif, system-ui, -apple-system, Segoe UI, Roboto, Ubuntu, Arial, sans-serif;
      background: var(--bg);
      color: var(--text);
    }

    .app{
      height:100vh;
      width:100vw;
      display:grid;
      grid-template-columns: minmax(320px, 420px) 1fr;
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
      gap: 12px;
      background: #fff;
    }

    .brand{
      display:flex; align-items:baseline; gap:10px; min-width:0;
    }
    .brand h1{
      font-size: 14px;
      margin:0;
      letter-spacing:.2px;
      font-weight: 750;
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

    .toolbar{display:flex; gap:8px; align-items:center}

    .btn{
      appearance:none;
      border:1px solid var(--border);
      background: #fff;
      color: var(--text);
      padding: 10px 12px;
      border-radius: 12px;
      cursor:pointer;
      font-weight: 700;
      transition: background .15s ease, border-color .15s ease, transform .05s ease;
      user-select:none;
    }
    .btn:hover{background:#f3f4f6}
    .btn:active{transform: translateY(1px)}
    .btnPrimary{
      background: var(--accent);
      color: #fff;
      border-color: rgba(37,99,235,.35);
    }
    .btnPrimary:hover{background:#1d4ed8}

    .content{
      padding: 14px 16px;
      overflow:auto;
      min-height:0;
    }

    label{
      display:block;
      margin: 12px 0 6px;
      font-weight: 750;
      font-size: 12px;
      color: var(--accent2);
      letter-spacing:.2px;
    }

    textarea, input{
      width:100%;
      background: #fff;
      border: 1px solid var(--border);
      color: var(--text);
      border-radius: 12px;
      padding: 12px 12px;
      font: inherit;
      outline: none;
      transition: border-color .15s ease, box-shadow .15s ease;
    }
    textarea:focus, input:focus{
      border-color: rgba(37,99,235,.55);
      box-shadow: 0 0 0 4px rgba(37,99,235,.10);
    }
    textarea{min-height: 44vh; resize: vertical}

    .hint{
      margin: 8px 0 0;
      font-size: 12px;
      color: var(--muted);
      line-height: 1.5;
    }

    details{
      margin-top: 12px;
      border: 1px solid var(--border);
      border-radius: 12px;
      background: #fff;
      overflow:hidden;
    }
    summary{
      cursor:pointer;
      list-style:none;
      padding: 12px 12px;
      font-weight: 750;
      font-size: 12px;
      color: var(--text);
    }
    summary::-webkit-details-marker{display:none}
    .settings{
      padding: 0 12px 12px;
      display:grid;
      grid-template-columns: 1fr;
      gap: 10px;
    }

    .badge{
      font-size: 11px;
      padding: 6px 10px;
      border-radius: 999px;
      border: 1px solid var(--border);
      color: var(--muted);
      background: #fff;
      white-space:nowrap;
    }

    .responseCard{
      border: 1px solid var(--border);
      border-radius: var(--radius);
      overflow:hidden;
      background:#fff;
    }

    .responseHead{
      padding: 12px 14px;
      border-bottom: 1px solid var(--border);
      display:flex;
      align-items:center;
      justify-content:space-between;
      gap: 10px;
      background:#fff;
    }

    .md{
      padding: 16px 16px 18px;
      line-height: 1.7;
      color: var(--text);
      font-size: 15px;
    }
    .md h1,.md h2,.md h3,.md h4,.md h5,.md h6{
      margin: 16px 0 10px;
      line-height: 1.2;
    }
    .md h1{font-size: 22px}
    .md h2{font-size: 18px}
    .md h3{font-size: 16px}
    .md p{margin: 10px 0}
    .md ul,.md ol{margin: 10px 0 10px 22px}
    .md li{margin: 6px 0}
    .md code.inline{
      font-family: var(--mono);
      font-size: .95em;
      padding: 2px 6px;
      border-radius: 8px;
      border: 1px solid var(--border);
      background: #f9fafb;
    }
    .md pre.code{
      margin: 12px 0;
      padding: 12px 12px;
      border-radius: 12px;
      background: #0b1220;
      border: 1px solid #0b1220;
      overflow:auto;
    }
    .md pre.code code{
      font-family: var(--mono);
      font-size: 13px;
      white-space: pre;
      display:block;
      color: #e5e7eb;
    }

    .emptyState{
      padding: 28px;
      text-align:center;
      color: var(--muted);
    }
    .emptyState .box{
      max-width: 520px;
      margin: 0 auto;
      border: 1px dashed var(--border);
      border-radius: var(--radius);
      padding: 18px 16px;
      background: #fafafa;
    }

    .err{
      margin: 14px 16px 16px;
      background: #fff1f2;
      border: 1px solid #fecdd3;
      color: #7f1d1d;
      padding: 12px 12px;
      border-radius: 12px;
      white-space: pre-wrap;
      word-wrap: break-word;
    }

    @media (max-width: 980px){
      .app{grid-template-columns: 1fr; height:auto; min-height:100vh}
      textarea{min-height: 32vh}
    }

    /* Mejora: scroll suave y accesibilidad focus-visible */
    html{scroll-behavior:smooth}
    .btn:focus-visible{outline:3px solid var(--accent);outline-offset:2px}
    textarea:focus-visible,input:focus-visible{outline:3px solid rgba(37,99,235,.4);outline-offset:1px}

    /* Mejora: animación de carga mientras espera la IA */
    @keyframes pulse{0%,100%{opacity:1}50%{opacity:.5}}
    .btn.loading{animation:pulse 1.2s ease-in-out infinite;pointer-events:none}

    /* Mejora: contador de caracteres */
    .charCount{font-size:11px;color:var(--muted);text-align:right;margin-top:4px}
  </style>
</head>
<body>

<div class="app">

  <!-- LEFT -->
  <section class="panel">
    <div class="panelHeader">
      <div class="brand">
        <h1>Ollama Web</h1>
        <p>Configuración PC</p>
      </div>
      <div class="toolbar">
        <button class="btn" type="button" id="clearBtn">Limpiar</button>
        <button class="btn btnPrimary" type="button" id="submitBtn">Enviar</button>
      </div>
    </div>

    <div class="content">
      <form method="post" id="theForm">
        <p class="hint">
          Escribe presupuesto (EUR) + uso. Ej.: “1200€ edición 4K + gaming 1440p”.
        </p>

        <label for="prompt">Petición</label>
        <textarea id="prompt" name="prompt" placeholder="Ejemplo: Tengo 900€ y quiero un PC para programar y algo de gaming."><?=h($prompt)?></textarea>
        <div class="charCount" id="charCount">0 / 2000</div>

        <details>
          <summary>Ajustes</summary>
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

        <button type="submit" style="display:none" aria-hidden="true" tabindex="-1"></button>
      </form>
    </div>
  </section>

  <!-- RIGHT -->
  <section class="panel">
    <div class="panelHeader">
      <div class="brand">
        <h1>Respuesta</h1>
        <p>Markdown → HTML</p>
      </div>
      <div class="toolbar">
        <span class="badge"><?=h($model)?></span>
        <button class="btn" type="button" id="copyBtn">Copiar</button>
      </div>
    </div>

    <div class="content">
      <div class="responseCard">
        <div class="responseHead">
          <span class="badge">
            <?php if ($result === null) echo "Sin consulta";
              else echo ($result["ok"] ? "OK" : "ERROR"); ?>
          </span>
          <?php if ($result !== null && $result["ok"] && isset($result["time"])): ?>
            <span class="badge"><?= h($result["time"]) ?>s</span>
          <?php endif; ?>
        </div>

        <?php if ($result === null): ?>
          <div class="emptyState">
            <div class="box">
              Envía una consulta desde la izquierda para ver la recomendación aquí.
            </div>
          </div>
        <?php elseif (!$result["ok"]): ?>
          <div class="err"><?=h($result["err"])?></div>
        <?php else: ?>
          <div class="md" id="mdOut"><?= md_to_html_safe($result["out"]) ?></div>
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

  // Mejora: enviar formulario con Ctrl+Enter desde el textarea
  promptEl.addEventListener('keydown', (e) => {
    if (e.ctrlKey && e.key === 'Enter') { e.preventDefault(); form.requestSubmit(); }
  });

  // Mejora: estado de carga visual al enviar consulta
  submitBtn.addEventListener('click', () => {
    submitBtn.classList.add('loading');
    submitBtn.textContent = 'Enviando…';
    form.requestSubmit();
  });
  clearBtn.addEventListener('click', () => { promptEl.value=''; updateCount(); promptEl.focus(); });

  // Mejora: contador de caracteres en tiempo real
  const charCount = document.getElementById('charCount');
  function updateCount() {
    const len = promptEl.value.length;
    charCount.textContent = len + ' / 2000';
    charCount.style.color = len > 2000 ? '#dc2626' : '';
  }
  promptEl.addEventListener('input', updateCount);
  updateCount();

  copyBtn.addEventListener('click', async () => {
    const mdOut = document.getElementById('mdOut');
    if (!mdOut) return;
    try{
      await navigator.clipboard.writeText(mdOut.innerText);
      copyBtn.textContent = 'Copiado';
      setTimeout(()=>copyBtn.textContent='Copiar', 900);
    }catch(e){
      copyBtn.textContent = 'No se pudo';
      setTimeout(()=>copyBtn.textContent='Copiar', 900);
    }
  });
</script>

</body>
</html>

