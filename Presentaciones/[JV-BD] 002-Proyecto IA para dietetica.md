# Proyecto IA para Dietética — Interfaz Web PHP con Ollama

![Interfaz de la aplicación web Ollama — panel de consulta y respuesta](docs/img/screenshot-interfaz.png)

> 🔗 **GitHub Pages:** [https://mutenros.github.io/Bases-de-datos-002-Proyecto-IA-para-diettica/](https://mutenros.github.io/Bases-de-datos-002-Proyecto-IA-para-diettica/)

## Introducción

Este proyecto consiste en una **aplicación web en PHP** que se conecta a un modelo de lenguaje (LLM) ejecutado en local mediante **Ollama**, un servidor de inferencia de IA. La aplicación evolucionó en 6 fases: desde una simple llamada por terminal hasta una interfaz profesional de dos paneles con renderizado de Markdown, ingeniería de prompts y funcionalidades JavaScript avanzadas. El caso de uso inicial es un **consejero dietético** que genera recetas saludables con los ingredientes que el usuario tiene disponibles, y posteriormente se amplió a un **asesor de componentes de PC** por presupuesto.

---

## Desarrollo de las partes

### 1. Función de escape HTML — Seguridad contra XSS

Toda la aplicación parte de una función auxiliar `h()` que envuelve `htmlspecialchars`. Se utiliza en cada punto donde se muestra contenido del usuario o de la IA en el HTML, previniendo ataques de inyección XSS.

- **Archivo:** `101-Ejercicios/006-interfaz clara.php` — **Línea 2**
  ```php
  function h($s): string { return htmlspecialchars((string)$s, ENT_QUOTES, 'UTF-8'); }
  ```
- Esta función se usa de forma consistente en los 5 archivos PHP del proyecto (002 a 006), y es la base de seguridad de toda la aplicación.

---

### 2. Llamada HTTP a Ollama con cURL

El núcleo del backend es la comunicación con el servidor Ollama mediante la extensión **cURL de PHP**. Se construye un payload JSON con el modelo, el prompt y la opción `stream: false`, se envía por POST y se parsea la respuesta.

- **Archivo:** `101-Ejercicios/006-interfaz clara.php` — **Líneas 102–139**
- Configuración de cURL con opciones de seguridad:
  ```php
  // Líneas 114-121
  $ch = curl_init($url);
  curl_setopt_array($ch, [
      CURLOPT_POST           => true,
      CURLOPT_RETURNTRANSFER => true,
      CURLOPT_HTTPHEADER     => ["Content-Type: application/json"],
      CURLOPT_POSTFIELDS     => json_encode($payload, JSON_UNESCAPED_UNICODE),
      CURLOPT_CONNECTTIMEOUT => 5,
      CURLOPT_TIMEOUT        => 90,
  ]);
  ```
- **Manejo de errores robusto** (líneas 125–139): se cubren tres casos — error de cURL, código HTTP no 2xx, y respuesta no-JSON. Solo si todo es correcto se extrae `$json["response"]`.

---

### 3. Ingeniería de Prompts — Del prompt abierto al cerrado

Una parte fundamental del proyecto es la evolución del **prompt engineering**:

- **Fase 002** (`002-llamada desde PHP.php`): Prompt abierto — el usuario escribe lo que quiera y se envía directamente a la IA.
- **Fase 003** (`003-cerrar prompt.php` — **Línea 12**): Prompt cerrado para dietética — se antepone un contexto de sistema:
  ```php
  $prompt = trim("Eres un consejero dietético. El usuario te va a proporcionar
  una serie de ingrediente que tiene un nevera. Debes elaborar una receta
  dietética, lo más saludable y sabrosa posible, con los ingredientes que
  el usuario te proporcione, que son estos: ".$prompt);
  ```
- **Fase 006** (`006-interfaz clara.php` — **Líneas 87–101**): Prompt avanzado con heredoc `<<<TXT` que incluye 7 reglas estrictas: forzar tabla de componentes, precios únicos en EUR, suma verificada, etc.

---

### 4. Parser Markdown → HTML seguro

A partir de la fase 005, se implementó un conversor Markdown a HTML en PHP puro (`md_to_html_safe`), que permite renderizar la respuesta de la IA con formato legible.

- **Archivo:** `101-Ejercicios/006-interfaz clara.php` — **Líneas 7–67**
- Soporta: encabezados (`#`…`######`), **negrita**, *cursiva*, `código inline`, bloques de código cercados (` ``` `), listas ordenadas y desordenadas, y párrafos con `<br>`.
- **Seguridad:** la primera operación es `$md = h($md)` — se escapa el HTML antes de convertir Markdown, evitando inyección.
- El resultado se muestra dentro de un `<div class="md">` (línea 498) con tipografía específica: fuentes monoespaciadas para código, márgenes para listas, fondos para bloques de código.

---

### 5. Interfaz de dos paneles con CSS Grid

La versión final (006) presenta un diseño profesional de **dos paneles** lado a lado usando CSS Grid, con tema claro y variables CSS personalizadas.

- **Archivo:** `101-Ejercicios/006-interfaz clara.php` — **Líneas 146–405**
- Variables CSS con custom properties (líneas 146–157):
  ```css
  :root{
    --bg: #f6f7f9;
    --panel: #ffffff;
    --accent: #2563eb;   /* blue */
    --shadow: 0 8px 24px rgba(17,24,39,.08);
    --radius: 14px;
  }
  ```
- Grid layout de dos columnas (líneas 174–180):
  ```css
  .app{
    display:grid;
    grid-template-columns: minmax(320px, 420px) 1fr;
  }
  ```
- **Responsive** (línea 403): en pantallas < 980px cambia a una sola columna.
- Panel izquierdo: formulario con modelo, URL y textarea del prompt.
- Panel derecho: tarjeta de respuesta con renderizado Markdown.

---

### 6. JavaScript interactivo — Copiar, limpiar, enviar

La interfaz incluye tres botones funcionales implementados en JavaScript vanilla:

- **Archivo:** `101-Ejercicios/006-interfaz clara.php` — **Líneas 508–548**
- **Botón Enviar** (línea 521): envía el formulario con `form.requestSubmit()` y activa un estado de carga visual:
  ```javascript
  submitBtn.addEventListener('click', () => {
    submitBtn.classList.add('loading');
    submitBtn.textContent = 'Enviando…';
    form.requestSubmit();
  });
  ```
- **Botón Limpiar** (línea 526): borra el textarea y pone el foco para escribir de nuevo.
- **Botón Copiar** (líneas 538–548): usa la **Clipboard API** del navegador para copiar el texto de la respuesta al portapapeles, con feedback visual ("Copiado" / "No se pudo").
- **Atajo Ctrl+Enter** (líneas 515–517): envía el formulario directamente desde el textarea sin necesidad de hacer clic.

---

### 7. Mejoras aplicadas — Validación, tiempo de respuesta y accesibilidad

Se añadieron mejoras mixtas para demostrar profundización en el aprendizaje:

- **PHP — Validación de longitud del prompt** (`006-interfaz clara.php` — **Líneas 82–84**):
  ```php
  if (mb_strlen($userPrompt) > 2000) {
    $userPrompt = mb_substr($userPrompt, 0, 2000);
  }
  ```
- **PHP — Medición de tiempo de respuesta** (línea 113 y 138): `microtime(true)` antes y después de la llamada cURL, mostrando los segundos en un badge.
- **CSS — Accesibilidad** (líneas 407–416): `scroll-behavior:smooth`, `focus-visible` para teclado, animación `pulse` durante la carga.
- **JS — Contador de caracteres** (líneas 529–535): se actualiza en tiempo real y cambia a rojo si supera 2000.
- **HTML — Meta tags y placeholder** (líneas 142–143, 444): `<meta description>` para SEO y `placeholder` descriptivo en el textarea.
- **003 — Mejoras CSS al dietético** (`003-cerrar prompt.php` — **Líneas 58–59, 66–67, 94**): título descriptivo, meta description, botón con color y hover, placeholder en textarea.

---

## Presentación del proyecto

Este proyecto demuestra cómo integrar un **modelo de inteligencia artificial local** (Ollama/LLaMA3) con una aplicación web PHP, sin depender de APIs comerciales ni de la nube.

La evolución en 6 fases refleja el proceso de aprendizaje: empezamos probando Ollama por terminal (fase 1), luego hicimos la primera llamada desde PHP con cURL (fase 2), aprendimos a cerrar el prompt para un caso de uso concreto —recetas dietéticas— (fase 3), cambiamos el dominio a asesor de PCs (fase 4), creamos una interfaz oscura con parser Markdown (fase 5) y finalmente una interfaz limpia y clara con todas las funcionalidades pulidas (fase 6).

Cada archivo PHP es **autocontenido**: incluye todo el backend, HTML, CSS y JavaScript en un solo fichero, lo que facilita el despliegue y la comprensión. El proyecto no necesita base de datos ni frameworks, solo PHP con la extensión cURL y un servidor Ollama ejecutándose en local.

Las mejoras finales añaden profundidad: validación de entrada con `mb_strlen`, medición del rendimiento con `microtime`, accesibilidad con `focus-visible`, e interacción avanzada con `Ctrl+Enter` y contador de caracteres.

---

## Conclusión

Con este proyecto hemos aprendido a:

- **Consumir una API REST desde PHP** usando cURL, gestionando errores HTTP y parseando respuestas JSON.
- **Aplicar ingeniería de prompts** para guiar a un LLM hacia respuestas estructuradas y útiles.
- **Implementar un parser Markdown en PHP puro**, con escape previo de HTML para mantener la seguridad.
- **Diseñar interfaces web modernas** con CSS Grid, custom properties, y diseño responsive.
- **Añadir interactividad con JavaScript vanilla**: Clipboard API, atajos de teclado, estados de carga.
- **Ejecutar modelos de IA en local** con Ollama, sin depender de servicios externos de pago.

El resultado es una aplicación funcional que conecta el mundo del backend PHP con la inteligencia artificial, demostrando que se pueden crear herramientas útiles con tecnologías accesibles y conocimientos de primer curso.
