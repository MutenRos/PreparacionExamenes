import mysql.connector
from flask import Flask

aplicacion = Flask(__name__)

conexion = mysql.connector.connect(
  host="localhost",
  user="portafolio",
  password="portafolio",
  database="portafolio"
)

@aplicacion.route("/")
def raiz():
  cursor = conexion.cursor()
  cursor.execute("SELECT * FROM portafolio;")

  # SVG placeholder (texto: "Sin imagen")
  placeholder_svg = """data:image/svg+xml;utf8,\
<svg xmlns='http://www.w3.org/2000/svg' width='800' height='600' viewBox='0 0 800 600' role='img' aria-label='Sin imagen'>\
  <defs>\
    <linearGradient id='g' x1='0' y1='0' x2='1' y2='1'>\
      <stop offset='0%' stop-color='%23232B2B'/>\
      <stop offset='100%' stop-color='%23374444'/>\
    </linearGradient>\
  </defs>\
  <rect width='800' height='600' fill='url(#g)'/>\
  <g fill='none' stroke='%238CA3A3' stroke-width='4' opacity='0.35'>\
    <path d='M120 480 L320 280 L440 380 L560 240 L680 360'/>\
    <circle cx='610' cy='210' r='35'/>\
  </g>\
  <text x='50%' y='50%' dominant-baseline='middle' text-anchor='middle'\
        font-family='system-ui, -apple-system, Segoe UI, Roboto, Arial'\
        font-size='28' fill='%23C7D1D1'>Sin imagen</text>\
</svg>"""

  cadena = f'''
<!doctype html>
<html lang="es">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width,initial-scale=1" />
    <title>Portafolio | Jose Vicente Carratala</title>
    <style>
      /* ----- Reset mínimo + variables ----- */
      *,*::before,*::after {{ box-sizing: border-box; }}
      html,body {{ height: 100%; }}
      body {{
        margin: 0;
        --bg: #0f1717;             /* DarkSlateGray-ish */
        --bg-soft: #132020;
        --card: #162525;
        --text: #d6d9d9;           /* LightGray */
        --muted: #9fb1b1;
        --accent: #87f0d6;
        --ring: #2ee6b9;
        --shadow: 0 10px 30px rgba(0,0,0,.35), 0 2px 8px rgba(0,0,0,.2);
        background: radial-gradient(1200px 800px at 10% 0%, #112020 0%, var(--bg) 60%) fixed;
        color: var(--text);
        font-family: system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif;
        line-height: 1.5;
      }}
      a {{ color: inherit; }}

      /* ----- Layout ----- */
      .wrap {{ max-width: 1200px; margin: 0 auto; padding: 24px; }}
      header, footer {{ text-align: center; }}
      header h1 {{
        margin: 0 0 6px 0;
        letter-spacing: .5px;
        font-size: clamp(28px, 3vw, 40px);
        font-weight: 800;
        text-shadow: 0 1px 0 rgba(0,0,0,.25);
      }}
      header h2 {{
        margin: 0;
        font-weight: 500;
        color: var(--muted);
      }}

      /* ----- Cinta decorativa debajo del header ----- */
      .ribbon {{
        height: 4px;
        margin: 18px auto 28px;
        width: min(220px, 50%);
        background: linear-gradient(90deg, transparent, var(--ring), transparent);
        filter: blur(.5px);
        border-radius: 999px;
      }}

      /* ----- Grid de tarjetas ----- */
      main.grid {{
        display: grid;
        gap: 22px;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
      }}

      article.card {{
        background: linear-gradient(180deg, var(--card), var(--bg-soft));
        border: 1px solid rgba(255,255,255,.06);
        border-radius: 16px;
        box-shadow: var(--shadow);
        overflow: hidden;
        position: relative;
        transition: transform .25s ease, box-shadow .25s ease, border-color .25s ease;
        outline: 0;
      }}
      article.card::after {{
        /* borde luminoso sutil al pasar el ratón */
        content: "";
        position: absolute; inset: 0;
        pointer-events: none;
        border-radius: inherit;
        border: 1px solid transparent;
        background: linear-gradient(180deg, transparent, rgba(46,230,185,.18), transparent) border-box;
        mask: linear-gradient(#000 0 0) padding-box, linear-gradient(#000 0 0);
        mask-composite: exclude;
        opacity: 0; transition: opacity .25s ease;
      }}
      article.card:hover {{ transform: translateY(-2px); box-shadow: 0 18px 40px rgba(0,0,0,.45); border-color: rgba(46,230,185,.25); }}
      article.card:hover::after {{ opacity: 1; }}

      .thumb {{
        width: 100%;
        aspect-ratio: 16/10;
        object-fit: cover;
        display: block;
        background: #1b2a2a;
      }}
      .thumb.skeleton {{
        animation: pulse 1.6s ease-in-out infinite;
        background: linear-gradient(90deg, #1a2626 25%, #223535 37%, #1a2626 63%);
        background-size: 400% 100%;
      }}
      @keyframes pulse {{ 0% {{ background-position: 100% 0; }} 100% {{ background-position: 0 0; }} }}

      .content {{ padding: 14px 16px 18px; }}
      .content h3 {{
        margin: 2px 0 8px;
        font-size: 18px;
        line-height: 1.25;
      }}
      .content p {{
        margin: 0;
        color: var(--muted);
        font-size: 14px;
      }}

      /* ----- Modal ----- */
      #contienemodal {{
        position: fixed; inset: 0;
        display: none; /* se activa en JS */
        align-items: center; justify-content: center;
        background: rgba(0,0,0,.6);
        backdrop-filter: blur(2px);
        padding: 24px;
        z-index: 999;
      }}
      #modal {{
        position: relative;
        width: min(100%, 1000px);
        background: #0e1515;
        border: 1px solid rgba(255,255,255,.08);
        border-radius: 14px;
        box-shadow: var(--shadow);
        padding: 10px;
      }}
      #modal img {{
        width: 100%;
        max-height: calc(100vh - 160px);
        object-fit: contain;
        border-radius: 8px;
        display: block;
        background: #0b1212;
      }}
      #cerrar {{
        position: absolute; top: 8px; right: 8px;
        background: rgba(20,30,30,.8);
        border: 1px solid rgba(255,255,255,.12);
        color: var(--text);
        padding: 6px 10px;
        border-radius: 999px;
        cursor: pointer;
        font-size: 14px;
      }}
      #cerrar:hover {{ background: rgba(30,45,45,.9); }}

      footer {{
        margin-top: 28px;
        color: var(--muted);
        font-size: 13px;
      }}
    </style>
  </head>
  <body>
    <header class="wrap">
      <h1>Jose Vicente Carratala</h1>
      <h2>Portafolio</h2>
      <div class="ribbon" aria-hidden="true"></div>
    </header>

    <main class="wrap grid">
  '''

  lineas = cursor.fetchall()
  for linea in lineas:
    titulo = str(linea[1])
    descripcion = str(linea[2])
    imagen = str(linea[3])
    # Evita 'None' literal en src y aplica fallback en onerror
    safe_src = imagen if imagen and imagen.lower() != "none" else placeholder_svg
    cadena += f"""
      <article class="card">
        <img class="thumb skeleton"
             src="{safe_src}"
             alt="{titulo}"
             loading="lazy"
             onload="this.classList.remove('skeleton')"
             onerror="this.onerror=null; this.src=this.dataset.fallback; this.classList.remove('skeleton')"
             data-fallback="{placeholder_svg}">
        <div class="content">
          <h3>{titulo}</h3>
          <p>{descripcion}</p>
        </div>
      </article>
    """

  cadena += '''
    </main>

    <footer class="wrap">
      © ''' + str(__import__('datetime').date.today().year) + ''' · Portafolio
    </footer>

    <!-- Modal -->
    <div id="contienemodal" aria-hidden="true">
      <div id="modal" role="dialog" aria-modal="true" aria-label="Vista ampliada de la imagen">
        <button id="cerrar" type="button" aria-label="Cerrar (Esc)">✕</button>
        <img id="modal-img" alt="Imagen ampliada">
      </div>
    </div>

    <script>
      // Abrir modal al hacer clic en una miniatura válida
      const overlay = document.getElementById('contienemodal');
      const modalImg = document.getElementById('modal-img');
      const closeBtn = document.getElementById('cerrar');

      document.addEventListener('click', (e) => {
        const img = e.target.closest('.card .thumb');
        if (img) {
          // No abrir si es el placeholder (comparación por data-fallback)
          const isFallback = img.getAttribute('src') === img.dataset.fallback;
          if (!isFallback) {
            modalImg.src = img.currentSrc || img.src;
            overlay.style.display = 'flex';
            overlay.setAttribute('aria-hidden', 'false');
          }
        }
      });

      // Cerrar: botón, clic fuera o Esc
      closeBtn.addEventListener('click', () => cerrarModal());
      overlay.addEventListener('click', (e) => {
        if (e.target === overlay) cerrarModal();
      });
      document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') cerrarModal();
      });

      function cerrarModal() {
        overlay.style.display = 'none';
        overlay.setAttribute('aria-hidden', 'true');
        modalImg.removeAttribute('src');
      }
    </script>
  </body>
</html>
  '''
  return cadena

if __name__ == "__main__":
  aplicacion.run(debug=True)

