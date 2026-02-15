<?php
// index.php (single file)
// Minimal markup: the whole page comes from Ollama (it must return a full HTML document).

$prompt = <<<PROMPT
Generate a COMPLETE single-page personal website as a FULL HTML DOCUMENT.

Requirements:
- Output ONLY the HTML document (starting with <!doctype html>), no explanations, no markdown.
- Include inline CSS in <style> and any tiny JS in <script> (no external assets).
- Modern, clean, professional design.
- Sections: Hero (name + role + short bio), Skills/Services, Portfolio (3 items), About, Contact (email + social placeholders), Footer.
- Add a light/dark toggle.
- Use semantic HTML and responsive layout.
- Content language: Spanish.

IMPORTANT: Return ONLY the final HTML document.
PROMPT;

$data = [
  "model"  => "qwen2.5-coder:7b",
  "prompt" => $prompt,
  "stream" => false,
  // optional: keep it deterministic-ish
  "options" => [
    "temperature" => 0.6,
    "num_predict" => 1600
  ]
];

$ch = curl_init("http://localhost:11434/api/generate");
curl_setopt_array($ch, [
  CURLOPT_RETURNTRANSFER => true,
  CURLOPT_POST           => true,
  CURLOPT_HTTPHEADER     => ["Content-Type: application/json"],
  CURLOPT_POSTFIELDS     => json_encode($data, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES),
  CURLOPT_TIMEOUT        => 60000000,
]);

$response = curl_exec($ch);
$err      = curl_error($ch);
$code     = curl_getinfo($ch, CURLINFO_HTTP_CODE);
curl_close($ch);

if ($response === false || $code < 200 || $code >= 300) {
  header("Content-Type: text/plain; charset=utf-8");
  echo "Ollama request failed.\nHTTP: $code\nError: $err\n";
  exit;
}

$result = json_decode($response, true);
$html   = $result["response"] ?? "";

// Ensure browser interprets it as HTML
header("Content-Type: text/html; charset=utf-8");

// If model returned extra text, try to cut from first doctype
$pos = stripos($html, "<!doctype");
if ($pos !== false) $html = substr($html, $pos);

// Last-resort fallback (still minimal): show raw response if not HTML-ish
if (stripos($html, "<html") === false) {
  echo "<!doctype html><html><head><meta charset='utf-8'><title>Ollama Output</title></head><body><pre>";
  echo htmlspecialchars($html, ENT_QUOTES | ENT_SUBSTITUTE, "UTF-8");
  echo "</pre></body></html>";
  exit;
}

echo $html;

