import base64
import mysql.connector
from flask import Flask
from datetime import date

aplicacion = Flask(__name__)

conexion = mysql.connector.connect(
  host="localhost",
  user="portafolio",
  password="portafolio",
  database="portafolio"
)

# ========= Helper: safe inline SVG (Base64) =========
# Avoids issues putting long SVG data URIs inside HTML attributes (quotes/commas/newlines)
svg_markup = (
    """
<svg xmlns='http://www.w3.org/2000/svg' width='1200' height='800' viewBox='0 0 1200 800' role='img' aria-label='Sin imagen'>
  <defs>
    <linearGradient id='g' x1='0' y1='0' x2='1' y2='1'>
      <stop offset='0%' stop-color='#132020'/>
      <stop offset='100%' stop-color='#102020'/>
    </linearGradient>
    <pattern id='grid' width='40' height='40' patternUnits='userSpaceOnUse'>
      <path d='M40 0 L0 0 0 40' fill='none' stroke='#2a3b3b' stroke-width='1'/>
    </pattern>
  </defs>
  <rect width='1200' height='800' fill='url(#g)'/>
  <rect width='1200' height='800' fill='url(#grid)' opacity='.2'/>
  <g fill='none' stroke='#87f0d6' stroke-width='6' opacity='.25'>
    <path d='M160 600 L420 340 L560 460 L720 300 L980 520'/>
    <circle cx='940' cy='260' r='40'/>
  </g>
  <text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle'
        font-family='system-ui, -apple-system, Segoe UI, Roboto, Arial'
        font-size='34' fill='#cfe7e3'>Sin imagen</text>
</svg>
""".strip()
)
placeholder_svg_b64 = base64.b64encode(svg_markup.encode("utf-8")).decode("ascii")
PLACEHOLDER_DATA_URI = f"data:image/svg+xml;base64,{placeholder_svg_b64}"


@aplicacion.route("/")
def raiz():
  cursor = conexion.cursor()
  cursor.execute("SELECT * FROM portafolio;")

  cadena = f"""<!doctype html>
<html lang=\"es\">
  <head>
    <meta charset=\"utf-8\" />
    <meta name=\"viewport\" content=\"width=device-width,initial-scale=1\" />
    <title>Portafolio | Jose Vicente Carratalá</title>
    <style>
      /* ===== Reset & tokens ===== */
      *,*::before,*::after {{ box-sizing: border-box; }}
      html,body {{ height:100%; }}
      :root {{
        --bg: #0f1717;
        --bg-soft: #111d1d;
        --card: rgba(20, 32, 32, .8);
        --edge: rgba(255,255,255,.08);
        --text: #e2e8e8;
        --muted: #a7b7b7;
        --accent: #87f0d6;
        --ring: #2ee6b9;
        --shadow-lg: 0 18px 40px rgba(0,0,0,.45);
        --shadow: 0 10px 30px rgba(0,0,0,.35), 0 2px 8px rgba(0,0,0,.2);
        --radius: 16px;
      }}
      body {{
        margin:0;
        background:
          radial-gradient(1200px 800px at 12% -10%, #112020 0%, var(--bg) 60%) fixed;
        color: var(--text);
        font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
        line-height: 1.5;
      }}
      .wrap {{ max-width: 1200px; margin: 0 auto; padding: 24px; }}

      /* ===== Header ===== */
      header {{ text-align:center; }}
      h1 {{
        margin: 0 0 6px;
        font-size: clamp(28px, 3vw, 40px);
        font-weight: 800;
        letter-spacing: .3px;
        text-shadow: 0 1px 0 rgba(0,0,0,.25);
      }}
      h2 {{ margin: 0; font-weight: 500; color: var(--muted); }}
      .ribbon {{
        height: 4px; margin: 18px auto 28px; width: min(260px, 60%);
        background: linear-gradient(90deg, transparent, var(--ring), transparent);
        border-radius: 999px; filter: blur(.5px);
      }}

      /* ===== Toolbar ===== */
      .toolbar {{ display:flex; gap:12px; align-items:center; justify-content:flex-end; margin-bottom:16px; }}
      .chip {{
        padding: 6px 10px; border:1px solid var(--edge); border-radius: 999px;
        background: rgba(255,255,255,.02); color: var(--muted); font-size:13px;
      }}

      /* ===== Grid & Cards ===== */
      main.grid {{
        display:grid; gap: 22px;
        grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
      }}
      .card {{
        background: var(--card);
        border:1px solid var(--edge);
        border-radius: var(--radius);
        box-shadow: var(--shadow);
        overflow: hidden; position: relative;
        transition: transform .25s ease, box-shadow .25s ease, border-color .25s ease, background .25s ease;
        outline: none;
      }}
      .card:focus-visible {{ box-shadow: 0 0 0 3px rgba(46,230,185,.35), var(--shadow); }}
      .card::after {{
        content:""; position:absolute; inset:0; pointer-events:none; border-radius: inherit;
        background: linear-gradient(180deg, transparent, rgba(46,230,185,.18), transparent);
        opacity: 0; transition: opacity .25s ease;
      }}
      .card:hover {{
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
        border-color: rgba(46,230,185,.25);
        background: rgba(22, 36, 36, .85);
      }}
      .card:hover::after {{ opacity: 1; }}

      .thumb {{
        width:100%; aspect-ratio: 16/10; object-fit: cover; display:block;
        background: #0c1414; cursor: zoom-in;
      }}
      .thumb.skeleton {{
        animation: pulse 1.6s ease-in-out infinite;
        background: linear-gradient(90deg, #122020 25%, #1a2c2c 37%, #122020 63%);
        background-size: 400% 100%;
      }}
      @keyframes pulse {{
        0% {{ background-position: 100% 0; }}
        100% {{ background-position: 0 0; }}
      }}

      .content {{ padding: 14px 16px 18px; }}
      .content h3 {{ margin: 2px 0 8px; font-size: 18px; line-height: 1.25; }}
      .content p {{ margin:0; color: var(--muted); font-size: 14px; min-height: 2.6em; }}

      /* ===== Modal ===== */
      #overlay {{
        position: fixed; inset: 0; display: none;
        align-items: center; justify-content: center;
        padding: 24px; z-index: 9999;
        background: rgba(0,0,0,.6); backdrop-filter: blur(2px);
      }}
      #modal {{
        position: relative; width: min(100%, 1100px);
        background: rgba(14, 21, 21, .95);
        border:1px solid var(--edge);
        border-radius: 14px;
        box-shadow: var(--shadow-lg);
        padding: 10px;
      }}
      #modal-img {{
        width: 100%; max-height: calc(100vh - 160px);
        object-fit: contain; border-radius: 8px; display:block; background:#0b1212;
      }}
      #close {{
        position: absolute; top: 8px; right: 8px;
        background: rgba(20,30,30,.9);
        border:1px solid rgba(255,255,255,.12);
        color: var(--text);
        padding: 6px 10px; border-radius: 999px; cursor: pointer; font-size: 14px;
      }}
      #close:hover {{ background: rgba(30,45,45,.95); }}
      #overlay[aria-hidden="false"] {{ display:flex; }}

      footer {{ margin-top: 28px; color: var(--muted); font-size: 13px; text-align:center; }}
    </style>
  </head>
  <body>
    <header class=\"wrap\">
      <h1>Jose Vicente Carratalá</h1>
      <h2>Portafolio</h2>
      <div class=\"ribbon\" aria-hidden=\"true\"></div>
      <div class=\"toolbar\">
        <span class=\"chip\">Total: {cursor.rowcount if hasattr(cursor, 'rowcount') else ''}</span>
      </div>
    </header>

    <main class=\"wrap grid\">
"""

  lineas = cursor.fetchall()
  for linea in lineas:
    titulo = str(linea[1])
    descripcion = str(linea[2]) if linea[2] is not None else ""
    imagen = str(linea[3]) if linea[3] is not None else ""

    # Decide si la tarjeta empieza ya con placeholder
    has_image = bool(imagen.strip()) and imagen.lower() != "none"
    safe_src = imagen if has_image else PLACEHOLDER_DATA_URI
    is_fallback = "0" if has_image else "1"

    cadena += f"""
      <article class=\"card\" tabindex=\"0\">
        <img class=\"thumb skeleton\"
             src=\"{safe_src}\"
             alt=\"{titulo}\"
             loading=\"lazy\"
             data-fallback=\"{PLACEHOLDER_DATA_URI}\"
             data-is-fallback=\"{is_fallback}\"
             onload=\"this.classList.remove('skeleton')\"
             onerror=\"this.dataset.isFallback='1'; this.src=this.dataset.fallback; this.classList.remove('skeleton')\">
        <div class=\"content\">
          <h3>{titulo}</h3>
          <p>{descripcion}</p>
        </div>
      </article>
    """

  year = date.today().year

  cadena += f"""
    </main>

    <footer class=\"wrap\">© {year} · Portafolio</footer>

    <!-- Modal -->
    <div id=\"overlay\" aria-hidden=\"true\">
      <div id=\"modal\" role=\"dialog\" aria-modal=\"true\" aria-label=\"Vista ampliada de la imagen\">
        <button id=\"close\" type=\"button\" aria-label=\"Cerrar (Esc)\">✕</button>
        <img id=\"modal-img\" alt=\"Imagen ampliada\">
      </div>
    </div>

    <script>
      // ========= Modal =========
      const overlay = document.getElementById('overlay');
      const modalImg = document.getElementById('modal-img');
      const closeBtn = document.getElementById('close');

      // Open modal on image click (only if not placeholder)
      document.addEventListener('click', (ev) => {{
        const img = ev.target.closest('.thumb');
        if (!img) return;
        if (img.dataset.isFallback === '1') return; // don't open placeholder
        ev.preventDefault();
        modalImg.src = img.currentSrc || img.src;
        overlay.setAttribute('aria-hidden', 'false');
      }});

      // Close behaviors
      function closeModal() {{
        overlay.setAttribute('aria-hidden', 'true');
        modalImg.removeAttribute('src');
      }}
      closeBtn.addEventListener('click', closeModal);
      overlay.addEventListener('click', (ev) => {{ if (ev.target === overlay) closeModal(); }});
      document.addEventListener('keydown', (ev) => {{ if (ev.key === 'Escape') closeModal(); }});

      // Ensure any image errors show the fallback and disable modal open for those
      document.querySelectorAll('.thumb').forEach(img => {{
        if (!img.getAttribute('src')) {{
          img.src = img.dataset.fallback;
          img.dataset.isFallback = '1';
          img.classList.remove('skeleton');
        }}
      }});
    </script>
  </body>
</html>
"""
  return cadena

if __name__ == "__main__":
  aplicacion.run(debug=True)

