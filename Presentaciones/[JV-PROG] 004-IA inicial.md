# IA Inicial — MicroChat con Ollama

![MicroChat con Ollama — interfaz de chat minimalista conectada a IA local](https://img.shields.io/badge/PHP-Ollama_API-777BB4?style=for-the-badge&logo=php&logoColor=white)

> 🔗 **GitHub Pages:** [https://mutenros.github.io/Programacion-004-IA-inicial/](https://mutenros.github.io/Programacion-004-IA-inicial/)

## Introducción

Este proyecto es un recorrido progresivo de 12 ejercicios que muestra cómo conectar una aplicación web PHP con un modelo de inteligencia artificial local ejecutándose en Ollama. Partiendo de una simple llamada cURL que imprime texto plano, se avanza paso a paso hasta construir un microchat estilizado con spinner de carga, gestión de sesiones, validación de entrada y soporte de modo oscuro automático. El objetivo pedagógico es entender cómo funcionan las APIs de IA generativa, cómo se consumen desde PHP y cómo se construye una interfaz de usuario amigable alrededor de la respuesta del modelo.

---

## Desarrollo de las partes

### 1. Conexión PHP con la API de Ollama (`cURL`)

La base de todo el proyecto es la comunicación con el servidor Ollama local. Se utiliza la extensión cURL de PHP para enviar una petición POST con el prompt en JSON y recibir la respuesta del modelo. Este patrón se repite en todos los ejercicios y se encapsula progresivamente en una función reutilizable.

```php
// Archivo: 101-Ejercicios/002-ollama pero lanza HTML.php, líneas 5-28
$data = [
    "model"  => "qwen2.5-coder:7b",
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
$result = json_decode($response, true);
echo $result["response"];
```

La petición va a `http://localhost:11434/api/generate` con `stream: false` para obtener la respuesta completa de una vez. Se decodifica el JSON de respuesta y se extrae el campo `response`.

---

### 2. Personalización del prompt del sistema

A partir del ejercicio 010, el prompt se enriquece con instrucciones adicionales que limitan la temática (solo programación), el idioma (español) y el formato (un párrafo, sin código). Esto demuestra el concepto de *system prompt* o *prompt engineering*.

```php
// Archivo: 101-Ejercicios/012-mejoras de estilo.php, líneas 8-12
$prompt = $userPrompt . "
  - responde en un solo párrafo, sin código, en prosa.
  - acepta solo preguntas relacionadas con programación, no aceptes otras temáticas
  - respuestas solo en español";
```

Estas restricciones evitan que el modelo responda sobre temas no deseados y aseguran que la respuesta se integre correctamente en la interfaz.

---

### 3. Función `ask_ollama()` — Encapsulación de la llamada

En los ejercicios avanzados (011, 012) se refactoriza la llamada a Ollama en una función PHP con tipado estricto. Esto permite reutilizarla y separar la lógica de la presentación.

```php
// Archivo: 101-Ejercicios/012-mejoras de estilo.php, líneas 7-32
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
  // ...cURL options...
  $response = curl_exec($ch);
  curl_close($ch);

  $result = json_decode($response ?? "", true);
  return $result["response"] ?? "Error: no se pudo obtener respuesta.";
}
```

El tipo de retorno `string` y el operador `??` con fallback de error hacen la función robusta ante fallos de conexión.

---

### 4. Gestión de sesiones y spinner de carga

Uno de los retos principales es que la llamada a Ollama puede tardar varios segundos. La solución implementada usa `session_start()` y un meta-refresh HTML para mostrar un spinner mientras se procesa la petición en segundo plano.

```php
// Archivo: 101-Ejercicios/012-mejoras de estilo.php, líneas 45-56
if ($_SERVER["REQUEST_METHOD"] === "POST" && isset($_POST["prompt"])) {
  $pregunta = trim((string)$_POST["prompt"]);
  // ...validación...
  $_SESSION["last_prompt"]  = $pregunta;
  $_SESSION["last_answer"]  = "";
  $_SESSION["answer_ready"] = false;

  $showSpinner = true;
  $metaRefresh = '<meta http-equiv="refresh" content="0.8;url=?step=answer">';
}
```

El flujo es: POST → mostrar spinner → `ob_flush()` + `fastcgi_finish_request()` para enviar HTML al navegador → computar respuesta en background → meta-refresh detecta `answer_ready` en la sesión.

---

### 5. Seguridad: `htmlspecialchars` y validación de entrada

La seguridad se aplica en dos capas: escapado de la salida con `htmlspecialchars()` para prevenir XSS, y validación del input con comprobación de longitud máxima.

```php
// Archivo: 101-Ejercicios/012-mejoras de estilo.php, líneas 47-51
// Validación: rechazar prompts vacíos o demasiado largos (máx. 500 caracteres)
if ($pregunta === "" || mb_strlen($pregunta) > 500) {
    $pregunta = null;
}
```

```php
// Archivo: 101-Ejercicios/012-mejoras de estilo.php, línea 283
<?= htmlspecialchars($pregunta, ENT_QUOTES, "UTF-8") ?>
```

En el ejercicio 009 también se añade sanitización de la entrada antes de enviarla al modelo:

```php
// Archivo: 101-Ejercicios/009-microchatgpt pero en funcionamiento.php, líneas 83-85
$userInput = htmlspecialchars(trim($_POST['prompt']), ENT_QUOTES, 'UTF-8');
$prompt = $userInput." - responde en un solo párrafo, sin código, en prosa.";
```

---

### 6. Generación de páginas web completas con IA

Los ejercicios 004 y 006 demuestran un uso avanzado: pedirle a Ollama que genere una página web HTML completa. Incluye parseo de la respuesta para extraer el documento HTML y un fallback si el modelo no genera HTML válido.

```php
// Archivo: 101-Ejercicios/004-creador web.php, líneas 56-64
$pos = stripos($html, "<!doctype");
if ($pos !== false) $html = substr($html, $pos);

// Last-resort fallback: show raw response if not HTML-ish
if (stripos($html, "<html") === false) {
  echo "<!doctype html><html><head><meta charset='utf-8'><title>Ollama Output</title></head><body><pre>";
  echo htmlspecialchars($html, ENT_QUOTES | ENT_SUBSTITUTE, "UTF-8");
  echo "</pre></body></html>";
}
```

---

### 7. Interfaz CSS con variables custom y diseño centrado

El ejercicio 012 implementa una interfaz chat profesional usando CSS custom properties (`--bg`, `--card`, `--ink`, etc.) que permiten cambiar todo el tema desde un solo sitio. El diseño es centrado con flexbox.

```css
/* Archivo: 101-Ejercicios/012-mejoras de estilo.php, líneas 82-92 */
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
```

Las burbujas de chat usan `border-radius` asimétrico para simular una interfaz de mensajería real, y la burbuja de respuesta tiene una animación `fadeIn` suave.

---

### 8. Modo oscuro automático (`prefers-color-scheme`)

Se añade soporte automático de modo oscuro mediante una media query CSS que detecta la preferencia del sistema operativo del usuario.

```css
/* Archivo: 101-Ejercicios/012-mejoras de estilo.php, líneas 260-271 */
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
}
```

Al usar CSS custom properties, basta redefinir las variables dentro de la media query para que todo el tema cambie automáticamente.

---

### 9. Contador de caracteres en JavaScript

Se añade un contador en tiempo real que muestra cuántos caracteres ha escrito el usuario de los 500 permitidos. Cambia a rojo cuando se acerca al límite.

```javascript
// Archivo: 101-Ejercicios/012-mejoras de estilo.php, líneas 309-316
const inp = document.getElementById('promptInput');
const cnt = document.getElementById('charCount');
if (inp && cnt) {
  inp.addEventListener('input', function() {
    const len = this.value.length;
    cnt.textContent = len + ' / 500';
    cnt.classList.toggle('warn', len > 450);
  });
}
```

Este JavaScript es mínimo, vanilla, y mejora la experiencia de usuario sin depender de librerías externas.

---

### 10. Accesibilidad (ARIA y semántica)

Se mejora la accesibilidad añadiendo atributos ARIA al spinner (`aria-hidden="true"`) y a la burbuja de respuesta (`role="status"`, `aria-live="polite"`) para que los lectores de pantalla anuncien la respuesta cuando aparezca.

```html
<!-- Archivo: 101-Ejercicios/012-mejoras de estilo.php, líneas 287-290 -->
<p id="respuesta" class="bubble" role="status" aria-live="polite">
  <?php if ($showSpinner): ?>
    <span class="spinner" aria-hidden="true"></span>
    <span class="muted">Pensando…</span>
```

El `<label>` oculto para el input, el `maxlength="500"` nativo del HTML y el `aria-label` en el campo de texto completan las mejoras de accesibilidad.

---

### 11. Progresión del proyecto: de texto plano a aplicación completa

El proyecto muestra una progresión clara de aprendizaje a lo largo de 12 ejercicios:

| Ejercicio | Líneas | Concepto nuevo |
|-----------|--------|----------------|
| 001 | — | Instalación de Ollama y modelos |
| 002 | 32 | Primera llamada cURL → texto plano |
| 003 | 37 | Respuesta dentro de HTML con estilo |
| 004 | 70 | IA genera una página web completa |
| 005 | — | Teoría: potencia de modelos de IA |
| 006 | 75 | Prompt más detallado (persona, grid, indigo) |
| 007 | 46 | Citas inspiradoras con color CSS por sentimiento |
| 008 | 81 | Interfaz de chat (solo maqueta, sin IA) |
| 009 | 111 | Chat funcional con Ollama + sanitización |
| 010 | 134 | Prompt limitado a programación + transiciones CSS |
| 011 | 153 | Spinner de carga + sesiones + meta-refresh |
| 012 | 358 | Estilo profesional + dark mode + validación + accesibilidad |

---

## Presentación del proyecto

Este proyecto es un recorrido didáctico que demuestra cómo integrar inteligencia artificial en una aplicación web real usando tecnologías accesibles. Arrancamos instalando Ollama, un servidor de modelos de IA que se ejecuta completamente en local, sin depender de la nube ni de APIs de pago.

Los primeros ejercicios muestran la mecánica básica: una simple petición cURL desde PHP al endpoint de Ollama, enviando un prompt en JSON y recibiendo la respuesta del modelo. A partir de ahí, cada ejercicio añade una capa: primero estilo HTML, luego CSS, después interactividad.

El salto cualitativo llega con los ejercicios de "creador web" (004, 006), donde le pedimos a la IA que genere una página web completa — incluyendo HTML, CSS y JavaScript — a partir de un prompt descriptivo. Esto demuestra que la IA no solo responde preguntas, sino que puede generar código funcional.

La parte central del proyecto es el microchat: una interfaz de mensajería donde el usuario escribe una pregunta sobre programación y recibe una respuesta del modelo. El reto técnico principal es que la llamada a Ollama puede tardar varios segundos, así que implementamos un spinner de carga usando sesiones PHP, `ob_flush()` y meta-refresh HTML — todo sin JavaScript asíncrono.

La versión final (012) incorpora un diseño profesional con CSS custom properties, modo oscuro automático, animaciones suaves, validación de entrada con límite de caracteres, y mejoras de accesibilidad con ARIA. Es una aplicación completa que demuestra frontend, backend, seguridad y UX en un solo archivo PHP.

---

## Conclusión

Este proyecto demuestra que conectar una aplicación web con un modelo de IA no requiere servicios en la nube ni infraestructura compleja. Con Ollama ejecutándose en local, PHP como backend y HTML/CSS/JS para la interfaz, se puede construir un asistente de chat funcional y seguro. La progresión de 12 ejercicios permite ver claramente cómo se van apilando conceptos: desde la petición HTTP más básica hasta la gestión de sesiones, la seguridad con `htmlspecialchars()`, el diseño responsive con CSS variables y el soporte de accesibilidad con ARIA. El resultado es una aplicación web completa que demuestra las competencias de programación del módulo aplicadas a un caso de uso real y actual: la inteligencia artificial generativa.
