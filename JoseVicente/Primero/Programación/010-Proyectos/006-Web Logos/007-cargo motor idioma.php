<?php include "motoridioma.php"; ?>
<!DOCTYPE html>
<html lang="<?= htmlspecialchars($currentLang) ?>">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title><?= htmlspecialchars($lang['Lenguaje de Programación Logos'] ?? 'Lenguaje de Programación Logos') ?></title>

  <link rel="stylesheet" href="style.css" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css" />
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet" />
  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/styles/atom-one-dark.min.css" />
</head>
<body>
  <!-- Selector de idioma -->
  <div class="lang-selector">
    <?php selectorIdioma(); ?>
  </div>

  <!-- Navegación -->
  <nav class="navbar">
    <div class="nav-container">
      <div class="nav-logo">
        λ <span id="nav-title"><?= $lang['Logos'] ?></span>
      </div>

      <ul class="nav-menu">
        <li><a href="#home" id="nav-home"><?= $lang['Inicio'] ?></a></li>
        <li><a href="#features" id="nav-features"><?= $lang['Características'] ?></a></li>
        <li><a href="#syntax" id="nav-syntax"><?= $lang['Sintaxis'] ?></a></li>
        <li><a href="#examples" id="nav-examples"><?= $lang['Ejemplos'] ?></a></li>
        <li><a href="#keywords" id="nav-keywords"><?= $lang['Palabras clave'] ?></a></li>
        <li><a href="#spec" id="nav-spec"><?= $lang['Núcleo'] ?></a></li>
        <li><a href="#faq" id="nav-faq"><?= $lang['FAQ'] ?></a></li>
        <li><a href="#download" id="nav-download"><?= $lang['Descargar'] ?></a></li>
        <li><a href="#docs" id="nav-docs"><?= $lang['Documentación'] ?></a></li>
        <li>
          <a href="https://github.com" target="_blank" id="nav-github">
            <i class="fab fa-github"></i> <?= $lang['GitHub'] ?>
          </a>
        </li>
      </ul>

      <button class="nav-toggle" aria-label="<?= htmlspecialchars($lang['Abrir menú']) ?>">
        <i class="fas fa-bars"></i>
      </button>
    </div>
  </nav>

  <!-- Sección Hero -->
  <section id="home" class="hero">
    <div class="hero-content">
      <h1 id="hero-title"><?= $lang['Lenguaje de Programación Logos'] ?></h1>
      <p id="hero-subtitle"><?= $lang['Simplicidad pythonica, léxico greco-latino y un núcleo minimalista'] ?></p>

      <div class="hero-badges">
        <span class="pill"><i class="fa-solid fa-indent"></i> <?= $lang['Indentación'] ?></span>
        <span class="pill"><i class="fa-solid fa-feather-pointed"></i> <?= $lang['Minimalista'] ?></span>
        <span class="pill"><i class="fa-solid fa-globe"></i> <?= $lang['Internacional'] ?></span>
        <span class="pill"><i class="fa-solid fa-cube"></i> <?= $lang['Núcleo + Stdlib'] ?></span>
      </div>

      <div class="hero-buttons">
        <a href="#download" class="btn btn-primary" id="hero-cta1"><?= $lang['Empezar'] ?></a>
        <a href="#examples" class="btn btn-secondary" id="hero-cta2"><?= $lang['Ver ejemplos'] ?></a>
      </div>

      <div class="hero-mini">
        <div class="mini-card">
          <div class="mini-title"><?= $lang['Versión'] ?></div>
          <div class="mini-value" id="hero-version">0.1.0</div>
        </div>
        <div class="mini-card">
          <div class="mini-title"><?= $lang['Licencia'] ?></div>
          <div class="mini-value">MIT</div>
        </div>
        <div class="mini-card">
          <div class="mini-title"><?= $lang['Compila con'] ?></div>
          <div class="mini-value">GCC / Clang</div>
        </div>
      </div>
    </div>

    <div class="hero-code">
      <div class="code-head">
        <span class="dot red"></span><span class="dot yellow"></span><span class="dot green"></span>
        <span class="code-title">main.logos</span>
        <button class="code-copy" data-copy="#hero-code-example"><i class="fa-regular fa-copy"></i> <?= $lang['Copiar'] ?></button>
      </div>
      <pre><code class="language-Logos" id="hero-code-example"># Logos: programa minimo + condicion
import sonus

nomen = "Mundo"
salutatio = "salve " + nomen

si nomen == "Logos":
    sonus.dic("optime!")
alio:
    sonus.dic(salutatio)</code></pre>
    </div>
  </section>

  <!-- Características -->
  <section id="features" class="features">
    <div class="container">
      <h2 id="features-title"><?= $lang['¿Por qué Logos?'] ?></h2>

      <div class="features-grid" id="features-items">
        <div class="feature-card">
          <i class="fa-solid fa-indent"></i>
          <h3><?= $lang['Indentación y legibilidad'] ?></h3>
          <p><?= $lang['Bloques definidos por espacios. Sin llaves ni punto y coma.'] ?></p>
        </div>

        <div class="feature-card">
          <i class="fa-solid fa-language"></i>
          <h3><?= $lang['Léxico greco-latino'] ?></h3>
          <p><?= $lang['Palabras reservadas en minúsculas, sin acentos ni caracteres especiales.'] ?></p>
        </div>

        <div class="feature-card">
          <i class="fa-solid fa-layer-group"></i>
          <h3><?= $lang['Núcleo estable'] ?></h3>
          <p><?= $lang['El núcleo es pequeño y explícito. El resto vive en librerías/extensiones.'] ?></p>
        </div>

        <div class="feature-card">
          <i class="fa-solid fa-bolt"></i>
          <h3><?= $lang['Minimalista y expresivo'] ?></h3>
          <p><?= $lang['Asignación directa, control de flujo claro y una stdlib conceptual.'] ?></p>
        </div>
      </div>
    </div>
  </section>

  <!-- Sintaxis -->
  <section id="syntax" class="syntax">
    <div class="container">
      <h2 id="syntax-title"><?= $lang['Ejemplos de sintaxis'] ?></h2>

      <div class="syntax-grid">
        <div class="code-card">
          <h3 id="syntax-code1-title"><?= $lang['Hola mundo'] ?></h3>
          <pre><code class="language-Logos" id="syntax-code1">import sonus
sonus.dic("salve mundus!")</code></pre>
        </div>

        <div class="code-card">
          <h3 id="syntax-code2-title"><?= $lang['Condicionales'] ?></h3>
          <pre><code class="language-Logos" id="syntax-code2">import sonus

nomen = "Logos"

si nomen == "Logos":
    sonus.dic("optime!")
alio:
    sonus.dic("quis es?")</code></pre>
        </div>

        <div class="code-card">
          <h3 id="syntax-code3-title"><?= $lang['Operadores lógicos'] ?></h3>
          <pre><code class="language-Logos" id="syntax-code3">import sonus

x = 7

si x > 0 et x < 10:
    sonus.dic("en rango")
alio:
    sonus.dic("fuera de rango")</code></pre>
        </div>
      </div>

      <div class="syntax-grid" style="margin-top:2rem">
        <div class="code-card">
          <h3><?= $lang['Bucles: pro + series'] ?></h3>
          <pre><code class="language-Logos">import sonus

pro i in series(0, 5):
    sonus.dic(i)</code></pre>
        </div>

        <div class="code-card">
          <h3><?= $lang['Bucles: dum + perge/frange'] ?></h3>
          <pre><code class="language-Logos">import sonus

x = 0
dum x < 10:
    x = x + 1
    si x == 2:
        perge
    si x == 5:
        frange
    sonus.dic(x)</code></pre>
        </div>

        <div class="code-card">
          <h3><?= $lang['Funciones: munus + redit'] ?></h3>
          <pre><code class="language-Logos">import sonus

munus quadratum(x):
    redit x * x

sonus.dic(quadratum(9))</code></pre>
        </div>
      </div>
    </div>
  </section>

  <!-- Ejemplos -->
  <section id="examples" class="examples">
    <div class="container">
      <h2 id="examples-title"><?= $lang['Más ejemplos'] ?></h2>

      <div class="examples-grid" id="examples-items">
        <div class="example-card">
          <h3><?= $lang['Literales: verum/falsum/nulla'] ?></h3>
          <pre><code class="language-Logos">import sonus

activo = verum
valor = nulla

si activo et valor == nulla:
    sonus.dic("estado valido")
alio:
    sonus.dic("estado mixtus")</code></pre>
        </div>

        <div class="example-card">
          <h3><?= $lang['Entrada/salida: sonus.lege'] ?></h3>
          <pre><code class="language-Logos">import sonus

nomen = sonus.lege("nomen? ")
sonus.dic("salve " + nomen)</code></pre>
        </div>

        <div class="example-card">
          <h3><?= $lang['Excepciones: conare/nisi/denique'] ?></h3>
          <pre><code class="language-Logos">import sonus

conare:
    x = divide(10, 0)
nisi:
    sonus.dic("error")
denique:
    sonus.dic("fin")</code></pre>
        </div>

        <div class="example-card">
          <h3><?= $lang['Lanzar excepción: iacta'] ?></h3>
          <pre><code class="language-Logos">import sonus

munus valida(x):
    si x == nulla:
        iacta Error("valor invalidus")
    redit x</code></pre>
        </div>
      </div>
    </div>
  </section>

  <!-- Palabras clave -->
  <section id="keywords" class="keywords">
    <div class="container">
      <h2 id="keywords-title"><?= $lang['Palabras clave en latín'] ?></h2>

      <div class="keywords-table-container">
        <table class="keywords-table">
          <thead>
            <tr>
              <th><?= $lang['Palabra clave Logos'] ?></th>
              <th><?= $lang['Equivalente'] ?></th>
              <th><?= $lang['Uso'] ?></th>
            </tr>
          </thead>
          <tbody id="keywords-table">
            <tr><td>si</td><td>if</td><td><?= $lang['Condicional'] ?></td></tr>
            <tr><td>aliosi</td><td>elif</td><td><?= $lang['Condición encadenada'] ?></td></tr>
            <tr><td>alio</td><td>else</td><td><?= $lang['Alternativa final'] ?></td></tr>

            <tr><td>pro</td><td>for</td><td><?= $lang['Iteración'] ?></td></tr>
            <tr><td>dum</td><td>while</td><td><?= $lang['Bucle condicionado'] ?></td></tr>
            <tr><td>frange</td><td>break</td><td><?= $lang['Interrumpe bucle'] ?></td></tr>
            <tr><td>perge</td><td>continue</td><td><?= $lang['Siguiente iteración'] ?></td></tr>

            <tr><td>munus</td><td>def</td><td><?= $lang['Definir función'] ?></td></tr>
            <tr><td>redit</td><td>return</td><td><?= $lang['Devolver valor'] ?></td></tr>

            <tr><td>conare</td><td>try</td><td><?= $lang['Bloque de intento'] ?></td></tr>
            <tr><td>nisi</td><td>except</td><td><?= $lang['Captura excepción'] ?></td></tr>
            <tr><td>denique</td><td>finally</td><td><?= $lang['Siempre se ejecuta'] ?></td></tr>
            <tr><td>iacta</td><td>raise</td><td><?= $lang['Lanza excepción'] ?></td></tr>

            <tr><td>import</td><td>import</td><td><?= $lang['Importar módulo (estándar internacional)'] ?></td></tr>

            <tr><td>verum</td><td>true</td><td><?= $lang['Literal booleano'] ?></td></tr>
            <tr><td>falsum</td><td>false</td><td><?= $lang['Literal booleano'] ?></td></tr>
            <tr><td>nulla</td><td>null</td><td><?= $lang['Ausencia de valor'] ?></td></tr>

            <tr><td>et</td><td>and</td><td><?= $lang['AND lógico'] ?></td></tr>
            <tr><td>aut</td><td>or</td><td><?= $lang['OR lógico'] ?></td></tr>
            <tr><td>non</td><td>not</td><td><?= $lang['NOT lógico'] ?></td></tr>
          </tbody>
        </table>
      </div>
    </div>
  </section>

  <!-- Núcleo del lenguaje (spec) -->
  <section id="spec" class="spec">
    <div class="container">
      <div class="spec-head">
        <div>
          <h2><?= $lang['Núcleo de Logos'] ?></h2>
          <p class="spec-sub">
            <?= $lang['Resumen práctico del documento: literales, control de flujo, funciones, excepciones y módulos.'] ?>
          </p>
        </div>

        <div class="spec-actions">
          <a class="btn btn-primary btn-small" href="#download"><i class="fa-solid fa-rocket"></i> <?= $lang['Instalar'] ?></a>
          <a class="btn btn-secondary btn-small" href="#docs"><i class="fa-solid fa-book"></i> <?= $lang['Docs'] ?></a>
        </div>
      </div>

      <div class="spec-grid">
        <article class="spec-card">
          <h3><i class="fa-solid fa-cube"></i> <?= $lang['Principios'] ?></h3>
          <ul class="spec-list">
            <li><?= $lang['Indentación como delimitador de bloque'] ?></li>
            <li><?= $lang['Reservadas en minúsculas (sin acentos)'] ?></li>
            <li><?= $lang['Asignación directa (sin declaración)'] ?></li>
            <li><?= $lang['Núcleo estable + librerías/extensiones'] ?></li>
          </ul>
        </article>

        <article class="spec-card">
          <h3><i class="fa-solid fa-toggle-on"></i> <?= $lang['Literales'] ?></h3>
          <div class="spec-pillrow">
            <span class="pill mono">verum</span>
            <span class="pill mono">falsum</span>
            <span class="pill mono">nulla</span>
          </div>
          <pre class="spec-pre"><code class="language-Logos">x = nulla
si x == nulla:
    sonus.dic("vacuum")</code></pre>
        </article>

        <article class="spec-card">
          <h3><i class="fa-solid fa-code-branch"></i> <?= $lang['Condicionales'] ?></h3>
          <pre class="spec-pre"><code class="language-Logos">si nota >= 9:
    sonus.dic("excellentia")
aliosi nota >= 5:
    sonus.dic("aprobatus")
alio:
    sonus.dic("suspensus")</code></pre>
        </article>

        <article class="spec-card">
          <h3><i class="fa-solid fa-rotate"></i> <?= $lang['Bucles'] ?></h3>
          <pre class="spec-pre"><code class="language-Logos">pro i in series(0, 10):
    si i == 5:
        frange
    si i == 2:
        perge
    sonus.dic(i)

x = 0
dum x < 3:
    x = x + 1</code></pre>
        </article>

        <article class="spec-card">
          <h3><i class="fa-solid fa-function"></i> <?= $lang['Funciones'] ?></h3>
          <pre class="spec-pre"><code class="language-Logos">munus saluta(nomen):
    redit "salve " + nomen</code></pre>
        </article>

        <article class="spec-card">
          <h3><i class="fa-solid fa-triangle-exclamation"></i> <?= $lang['Excepciones'] ?></h3>
          <pre class="spec-pre"><code class="language-Logos">conare:
    x = divide(10, 0)
nisi:
    sonus.dic("error")
denique:
    sonus.dic("fin")</code></pre>
        </article>

        <article class="spec-card">
          <h3><i class="fa-solid fa-box"></i> <?= $lang['Módulos'] ?></h3>
          <pre class="spec-pre"><code class="language-Logos">import sonus
sonus.dic("salve")</code></pre>
          <p class="spec-note">
            <span class="pill mini"><?= $lang['Nota'] ?></span> <strong>import</strong> <?= $lang['se mantiene por estándar internacional.'] ?>
          </p>
        </article>

        <article class="spec-card">
          <h3><i class="fa-solid fa-layer-group"></i> <?= $lang['Operadores lógicos'] ?></h3>
          <div class="spec-pillrow">
            <span class="pill mono">et</span>
            <span class="pill mono">aut</span>
            <span class="pill mono">non</span>
          </div>
          <pre class="spec-pre"><code class="language-Logos">si non (x == 0) et x < 10:
    sonus.dic("ok")</code></pre>
        </article>

        <article class="spec-card">
          <h3><i class="fa-solid fa-list-check"></i> <?= $lang['Resumen del núcleo'] ?></h3>
          <div class="spec-kv">
            <div class="kv">
              <div class="k"><?= $lang['Reservadas'] ?></div>
              <div class="v mono">si, aliosi, alio, pro, dum, frange, perge, munus, redit, conare, nisi, denique, iacta, import</div>
            </div>
            <div class="kv">
              <div class="k"><?= $lang['Literales'] ?></div>
              <div class="v mono">verum, falsum, nulla</div>
            </div>
            <div class="kv">
              <div class="k"><?= $lang['Lógicos'] ?></div>
              <div class="v mono">et, aut, non</div>
            </div>
          </div>
        </article>
      </div>

      <!-- Quickstart -->
      <div class="quickstart">
        <div class="quickstart-left">
          <h3><?= $lang['Quickstart'] ?></h3>
          <p><?= $lang['Programa mínimo y estructura típica. Ideal para la primera ejecución.'] ?></p>
          <ul>
            <li><strong>1.</strong> <?= $lang['Importa librerías'] ?></li>
            <li><strong>2.</strong> <?= $lang['Define'] ?> <span class="mono">munus init()</span></li>
            <li><strong>3.</strong> <?= $lang['Usa'] ?> <span class="mono">sonus.dic</span> <?= $lang['y'] ?> <span class="mono">sonus.lege</span></li>
          </ul>
        </div>
        <div class="quickstart-right">
          <div class="code-head small">
            <span class="code-title">init.logos</span>
            <button class="code-copy" data-copy="#qs-code"><i class="fa-regular fa-copy"></i> <?= $lang['Copiar'] ?></button>
          </div>
          <pre><code class="language-Logos" id="qs-code">import sonus

munus init():
    sonus.dic("salve mundus")</code></pre>
        </div>
      </div>
    </div>
  </section>

  <!-- FAQ -->
  <section id="faq" class="faq">
    <div class="container">
      <h2><?= $lang['FAQ'] ?></h2>

      <div class="faq-grid">
        <details class="faq-item" open>
          <summary><?= $lang['¿Por qué palabras greco-latinas?'] ?></summary>
          <p><?= $lang['Para lograr un léxico distintivo, consistente y sin dependencia total del inglés, manteniendo legibilidad.'] ?></p>
        </details>

        <details class="faq-item">
          <summary><?= $lang['¿Por qué import está en inglés?'] ?></summary>
          <p><?= $lang['Se conserva por ser un estándar internacional consolidado y familiar para la mayoría de programadores.'] ?></p>
        </details>

        <details class="faq-item">
          <summary><?= $lang['¿Hay declaración de variables?'] ?></summary>
          <p><?= $lang['No. Una variable existe al asignarle un valor:'] ?> <span class="mono">x = 10</span>.</p>
        </details>

        <details class="faq-item">
          <summary><?= $lang['¿Dónde está la librería estándar?'] ?></summary>
          <p><?= $lang['El núcleo define el lenguaje. La stdlib se modela como módulos (por ejemplo sonus y series).'] ?></p>
        </details>
      </div>
    </div>
  </section>

  <!-- Descarga -->
  <section id="download" class="download">
    <div class="container">
      <h2 id="download-title"><?= $lang['Obtén Logos'] ?></h2>
      <p id="download-description" class="download-desc"><?= $lang['Descarga la última versión o compílala desde el código fuente'] ?></p>

      <div class="download-info">
        <div class="version-badge" id="download-version"><?= $lang['Versión actual: 0.1.0'] ?></div>
        <div class="download-requirements" id="download-requirements"><?= $lang['Requisitos: compilador C (GCC/Clang), Make'] ?></div>
      </div>

      <div class="download-buttons">
        <a href="https://github.com/yourusername/Logos" target="_blank" class="btn btn-primary">
          <i class="fab fa-github"></i> <span id="download-btn-source"><?= $lang['Código fuente'] ?></span>
        </a>
        <a href="#" class="btn btn-secondary" id="download-btn-binary"><?= $lang['Descargar binario'] ?></a>
      </div>

      <!-- Build snippet -->
      <div class="download-build">
        <div class="code-head small">
          <span class="code-title">build.sh</span>
          <button class="code-copy" data-copy="#build-code"><i class="fa-regular fa-copy"></i> <?= $lang['Copiar'] ?></button>
        </div>
        <pre><code class="language-bash" id="build-code">git clone https://github.com/yourusername/Logos
cd Logos
make
./logos examples/salve.logos</code></pre>
      </div>
    </div>
  </section>

  <!-- Docs anchor (placeholder) -->
  <section id="docs" class="docs">
    <div class="container">
      <h2><?= $lang['Documentación'] ?></h2>
      <div class="docs-grid">
        <a class="docs-card" href="#spec">
          <div class="docs-ico"><i class="fa-solid fa-cube"></i></div>
          <div>
            <h3><?= $lang['Núcleo'] ?></h3>
            <p><?= $lang['Palabras reservadas, literales y control de flujo.'] ?></p>
          </div>
        </a>

        <a class="docs-card" href="#syntax">
          <div class="docs-ico"><i class="fa-solid fa-code"></i></div>
          <div>
            <h3><?= $lang['Sintaxis'] ?></h3>
            <p><?= $lang['Ejemplos cortos y patrones de uso.'] ?></p>
          </div>
        </a>

        <a class="docs-card" href="#examples">
          <div class="docs-ico"><i class="fa-solid fa-book-open"></i></div>
          <div>
            <h3><?= $lang['Ejemplos'] ?></h3>
            <p><?= $lang['Programas prácticos y fragmentos reutilizables.'] ?></p>
          </div>
        </a>

        <a class="docs-card" href="#download">
          <div class="docs-ico"><i class="fa-solid fa-download"></i></div>
          <div>
            <h3><?= $lang['Instalación'] ?></h3>
            <p><?= $lang['Compilación, binarios y primeros pasos.'] ?></p>
          </div>
        </a>
      </div>
    </div>
  </section>

  <!-- Pie de página -->
  <footer class="footer">
    <div class="container">
      <div class="footer-content">
        <div class="footer-about">
          <div class="footer-logo">λ <?= $lang['Logos'] ?></div>
          <p id="footer-description"><?= $lang['Logos es un lenguaje de programación de código abierto diseñado para la simplicidad y la elegancia.'] ?></p>
        </div>

        <div class="footer-links">
          <h4><?= $lang['Enlaces'] ?></h4>
          <ul id="footer-links">
            <li><a href="#spec"><?= $lang['Núcleo'] ?></a></li>
            <li><a href="#examples"><?= $lang['Ejemplos'] ?></a></li>
            <li><a href="#download"><?= $lang['Descargar'] ?></a></li>
            <li><a href="#docs"><?= $lang['Documentación'] ?></a></li>
          </ul>
        </div>

        <div class="footer-social">
          <h4><?= $lang['Comunidad'] ?></h4>
          <div class="social-icons">
            <a href="https://github.com" target="_blank" aria-label="<?= htmlspecialchars($lang['GitHub']) ?>"><i class="fab fa-github"></i></a>
            <a href="#" aria-label="<?= htmlspecialchars($lang['Discord']) ?>"><i class="fab fa-discord"></i></a>
            <a href="#" aria-label="<?= htmlspecialchars($lang['Twitter']) ?>"><i class="fab fa-twitter"></i></a>
            <a href="#" aria-label="<?= htmlspecialchars($lang['Stack Overflow']) ?>"><i class="fab fa-stack-overflow"></i></a>
          </div>
        </div>
      </div>

      <div class="footer-bottom">
        <p id="footer-copyright">© 2024 <?= $lang['Proyecto del Lenguaje Logos. Licencia MIT.'] ?></p>
      </div>
    </div>
  </footer>

  <!-- JavaScript -->
  <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.8.0/highlight.min.js"></script>

  <script>
    // highlight.js
    document.addEventListener("DOMContentLoaded", () => {
      if (window.hljs) hljs.highlightAll();
    });

    // Mobile nav
    const toggle = document.querySelector(".nav-toggle");
    const menu = document.querySelector(".nav-menu");
    if (toggle && menu) {
      toggle.addEventListener("click", () => menu.classList.toggle("active"));
    }

    // Copy buttons
    document.querySelectorAll(".code-copy").forEach(btn => {
      btn.addEventListener("click", async () => {
        const sel = btn.getAttribute("data-copy");
        const el = sel ? document.querySelector(sel) : null;
        const text = el ? el.textContent : "";
        if (!text) return;

        try {
          await navigator.clipboard.writeText(text);
          const old = btn.innerHTML;
          btn.innerHTML = '<i class="fa-solid fa-check"></i> <?= addslashes($lang['Copiado']) ?>';
          setTimeout(() => (btn.innerHTML = old), 1200);
        } catch (e) {
          alert("no");
        }
      });
    });

    // Language change (motoridioma.php uses ?lang=)
    const idioma = document.getElementById("idioma");
    if (idioma) {
      idioma.addEventListener("change", function () {
        const url = new URL(window.location.href);
        url.searchParams.set("lang", this.value);
        window.location.href = url.toString();
      });
    }
  </script>
</body>
</html>

