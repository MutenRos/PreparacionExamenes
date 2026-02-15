<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>recortabl.es · Producto</title>

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Delius&display=swap" rel="stylesheet">

  <style>
    :root{
      --bg: #eef5fb;
      --ink: #0b2a45;
      --muted: #527089;
      --brand: #2a84d8;
      --brand2:#1f6fbe;
      --card:#ffffff;
      --line:#d9e8f6;
      --shadow: 0 10px 22px rgba(11,42,69,.10);
      --shadow2: 0 6px 14px rgba(11,42,69,.10);
      --radius: 16px;
    }

    *{box-sizing:border-box}
    html,body{height:100%}
    body{
      margin:0;
      font-family:Delius,system-ui,-apple-system,Segoe UI,Roboto,Arial,sans-serif;
      color:var(--ink);
      background:linear-gradient(#f6fbff 0%, var(--bg) 30%, #f4f9ff 100%);
    }
    a{color:inherit;text-decoration:none}
    img{max-width:100%;display:block}

    .wrap{max-width:1100px;margin:0 auto;padding:0 18px}
    main{padding:18px 0 10px}
    section{padding:18px 0}
    h1,h2,h3{margin:0}

    /* ===== Header ===== */
    header{
      position:sticky; top:0; z-index:50;
      background:#fff;
      border-bottom:1px solid #e8f1fb;
      box-shadow:0 6px 18px rgba(11,42,69,.08);
    }
    header .wrap{
      display:flex;align-items:center;justify-content:space-between;
      gap:14px;padding:12px 18px;
    }
    .brand{
      display:flex;align-items:center;gap:10px;
      font-weight:700;letter-spacing:.2px;
    }
    .brand .logo{
      width:38px;height:38px;border-radius:10px;
      background:linear-gradient(145deg,#e9f6ff,#ffffff);
      border:1px solid #d8ecff;
      box-shadow:0 6px 14px rgba(42,132,216,.15);
      display:grid;place-items:center;
      font-size:20px;
    }
    .brand span{font-size:26px}
    .brand span b{color:#ff4d3d}
    .brand span i{font-style:normal;color:#2a84d8}

    nav{
      display:flex;align-items:center;gap:14px;flex-wrap:wrap;
      justify-content:flex-end;color:#2b5a7a;font-weight:600;
    }
    nav a{padding:8px 10px;border-radius:10px}
    nav a:hover{background:#f2f8ff}

    .search{
      display:flex;align-items:center;gap:10px;
      background:#2a84d8;padding:8px 10px;border-radius:12px;
      box-shadow:0 10px 18px rgba(42,132,216,.25);
    }
    .search input{
      width:190px;border:0;outline:0;background:transparent;color:#fff;font:inherit;
    }
    .search input::placeholder{color:rgba(255,255,255,.85)}
    .search .icon{
      width:26px;height:26px;border-radius:9px;
      background:rgba(255,255,255,.18);
      display:grid;place-items:center;color:#fff;font-size:14px;
    }

    /* ===== Breadcrumbs ===== */
    .crumbs{
      display:flex;
      flex-wrap:wrap;
      gap:8px;
      align-items:center;
      color:var(--muted);
      font-weight:800;
      margin:6px 0 14px;
    }
    .crumbs a{
      padding:6px 10px;
      border-radius:999px;
      background:linear-gradient(180deg,#ffffff,#f6fbff);
      border:1px solid #dfeffc;
      box-shadow:0 6px 14px rgba(11,42,69,.06);
      color:#2b5a7a;
      font-weight:900;
    }
    .crumbs span{opacity:.9}

    /* ===== Product layout ===== */
    .product{
      display:grid;
      grid-template-columns: 1.05fr .95fr;
      gap:16px;
      align-items:start;
    }

    .card{
      background:var(--card);
      border:1px solid #e4effa;
      border-radius:var(--radius);
      box-shadow:var(--shadow);
      padding:14px;
    }

    .gallery{
      display:grid;
      gap:12px;
    }
    .hero-img{
    width:100%;
      border-radius:14px;
      background:linear-gradient(180deg,#eaf4ff,#ffffff);
      border:1px solid #dfeffc;
      aspect-ratio: 4 / 3;
      object-fit:cover;
      box-shadow:0 10px 18px rgba(11,42,69,.10);
    }
    .thumbs{
      display:grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap:10px;
    }
    .thumbs a{
      border-radius:12px;
      border:1px solid #dfeffc;
      background:#fff;
      box-shadow:var(--shadow2);
      padding:6px;
    }
    .thumbs img{
      border-radius:10px;
      aspect-ratio: 4 / 3;
      object-fit:cover;
      background:linear-gradient(180deg,#eaf4ff,#ffffff);
      border:1px solid #dfeffc;
    }

    .p-title{
      color:#1b5f92;
      font-size:30px;
      font-weight:900;
      margin:2px 0 8px;
      line-height:1.1;
    }
    .p-sub{
      color:var(--muted);
      font-weight:800;
      margin:0 0 12px;
    }
    .meta-row{
      display:flex;
      flex-wrap:wrap;
      gap:10px;
      align-items:center;
      margin:0 0 12px;
    }
    .pill{
      padding:7px 10px;
      border-radius:999px;
      border:1px solid #dfeffc;
      background:linear-gradient(180deg,#ffffff,#f6fbff);
      box-shadow:0 6px 14px rgba(11,42,69,.06);
      color:#2b5a7a;
      font-weight:900;
      font-size:13px;
      white-space:nowrap;
    }
    .stars{
      color:#f1b400;
      letter-spacing:1px;
      font-weight:900;
    }

    .actions{
      display:grid;
      gap:10px;
      margin:14px 0 10px;
    }
    .btn{
      display:inline-flex;
      align-items:center;
      justify-content:center;
      gap:10px;
      width:100%;
      padding:12px 14px;
      border-radius:14px;
      font-weight:900;
      border:1px solid rgba(0,0,0,.08);
      box-shadow:0 14px 22px rgba(42,132,216,.22);
      cursor:pointer;
    }
    .btn.primary{
      background:linear-gradient(180deg,#2e8fe8,#1f70be);
      color:#fff;
    }
    .btn.secondary{
      background:linear-gradient(180deg,#ffffff,#eaf4ff);
      color:#1a5f92;
      border-color:rgba(11,42,69,.12);
      box-shadow:0 14px 22px rgba(0,0,0,.10);
    }
    .btn.primary:after{content:"›";font-size:18px;opacity:.95}
    .btn.secondary:after{content:"›";font-size:18px;opacity:.75}

    .note{
      margin:0;
      color:#2b5a7a;
      font-weight:800;
      background:linear-gradient(180deg,#fff,#f6fbff);
      border:1px dashed rgba(82,112,137,.35);
      border-radius:14px;
      padding:10px 12px;
    }

    /* ===== Details blocks ===== */
    .details{
      display:grid;
      gap:12px;
      margin-top:14px;
    }
    .details h3{
      color:#1b5f92;
      font-size:18px;
      font-weight:900;
      margin:0 0 8px;
    }
    .details p{
      margin:10px 0 0;
      color:#265a79;
      font-weight:800;
      line-height:1.35;
    }
    .list{
      display:grid;
      gap:8px;
      margin-top:8px;
      color:#265a79;
      font-weight:800;
    }
    .list div{
      display:flex;
      gap:10px;
      align-items:flex-start;
    }

    /* ===== Similar products ===== */
    .title{
      color:#1b5f92;
      font-size:22px;
      font-weight:900;
      margin:0 0 12px;
    }
    .grid{
      display:grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap:14px;
    }
    article{
      background:var(--card);
      border:1px solid #e4effa;
      border-radius:16px;
      box-shadow:var(--shadow);
      padding:12px;
      display:flex;
      flex-direction:column;
      gap:10px;
    }
    article img{
      border-radius:14px;
      background:linear-gradient(180deg,#eaf4ff,#ffffff);
      border:1px solid #dfeffc;
      aspect-ratio: 4 / 3;
      object-fit:cover;
      box-shadow:0 10px 18px rgba(11,42,69,.10);
    }
    .card-body{padding:2px 6px 6px}
    .card-title{
      margin:0 0 6px;
      font-weight:900;
      color:#1f5777;
      font-size:16px;
      line-height:1.15;
    }
    .meta{
      display:flex;align-items:center;justify-content:space-between;gap:10px;
      color:var(--muted);font-weight:800;font-size:13px;margin:0 0 10px;
    }
    .tag{
      padding:5px 8px;border-radius:999px;border:1px solid #dfeffc;
      background:linear-gradient(180deg,#ffffff,#f6fbff);
      box-shadow:0 6px 14px rgba(11,42,69,.06);
      color:#2b5a7a;font-weight:900;font-size:12px;white-space:nowrap;
    }
    .download{
      margin-top:auto;
      display:inline-flex;align-items:center;justify-content:center;gap:10px;
      width:100%;
      padding:10px 12px;
      border-radius:12px;
      background:linear-gradient(180deg,#2e8fe8,#1f70be);
      color:#fff;
      font-weight:900;
      border:1px solid rgba(0,0,0,.08);
      box-shadow:0 14px 22px rgba(42,132,216,.22);
    }
    .download:after{content:"›";font-size:18px;opacity:.95}

    /* Footer */
    footer{padding:18px 0 28px;color:#2b5a7a}
    footer .wrap{
      border-top:2px dashed rgba(82,112,137,.25);
      padding-top:16px;
      display:flex;
      gap:14px;
      justify-content:center;
      flex-wrap:wrap;
      align-items:center;
    }
    footer a{padding:8px 10px;border-radius:10px;font-weight:800}
    footer a:hover{background:#f2f8ff}
    .social a{
      width:36px;height:36px;display:inline-grid;place-items:center;
      border-radius:12px;background:#fff;border:1px solid #e4effa;
      box-shadow:var(--shadow2);padding:0;font-weight:900;
    }

    /* Responsive */
    @media (max-width:1100px){
      .product{grid-template-columns: 1fr;}
      .grid{grid-template-columns: repeat(3, minmax(0, 1fr));}
    }
    @media (max-width:820px){
      .grid{grid-template-columns: repeat(2, minmax(0, 1fr));}
      .search input{width:120px}
    }
    @media (max-width:520px){
      .grid{grid-template-columns: 1fr;}
      .thumbs{grid-template-columns: repeat(3, minmax(0, 1fr));}
    }
  </style>
</head>

<body>
  <header>
    <div class="wrap">
      <a class="brand" href="/">
        <div class="logo">🤖</div>
        <span><b>rec</b><i>ortabl.es</i></span>
      </a>

      <nav>
        <a href="#">Categorías ▾</a>
        <a href="#">Sobre nosotros</a>
        <a href="#">Descargas</a>
        <a href="#">Login</a>
        <div class="search" role="search">
          <div class="icon">🔎</div>
          <input type="search" placeholder="Buscar..." aria-label="Buscar" />
        </div>
      </nav>
    </div>
  </header>

  <main class="wrap">
    <div class="crumbs" aria-label="Migas de pan">
      <a href="#">Inicio</a>
      <span>›</span>
      <a href="#">Catálogo</a>
      <span>›</span>
      <a href="#">Animales</a>
      <span>›</span>
      <span>Dinosaurio T-Rex</span>
    </div>
	<?php
		$db = new SQLite3('recortables.db');
		$peticion = "
		SELECT 
				productos.titulo AS tituloproducto,
				categorias.titulo AS categoriaproducto,
				productos.imagen AS imagenproducto,
				productos.descripcion AS descripcionproducto
				FROM productos
				LEFT JOIN categorias
				ON productos.categoria = categorias.Identificador
		 WHERE productos.Identificador = ".$_GET['id']."";
		$resultado = $db->query($peticion);
		while ($fila = $resultado->fetchArray(SQLITE3_ASSOC)) {
	?>
    <section class="product">
      <!-- Left: gallery -->
      <div class="card gallery">
        <img class="hero-img" src="<?= $fila['imagenproducto']?>" alt="Vista previa del recortable" />
        <div class="thumbs" aria-label="Vistas previas">
          <a href="#"><img src="imgcategoria.png" alt=""></a>
          <a href="#"><img src="imgcategoria.png" alt=""></a>
          <a href="#"><img src="imgcategoria.png" alt=""></a>
          <a href="#"><img src="imgcategoria.png" alt=""></a>
        </div>
      </div>

      <!-- Right: product info -->
      <div class="card">
        <h1 class="p-title"><?= $fila['tituloproducto']?></h1>
        <p class="p-sub">Recortable listo para imprimir · PDF en alta calidad</p>

        <div class="meta-row">
          <span class="pill">Categoría: <?= $fila['categoriaproducto']?></span>
          <span class="pill">Dificultad: Media</span>
          <span class="pill">Páginas: 4</span>
          <span class="pill"><span class="stars">★★★★★</span> (128)</span>
        </div>

        <div class="actions">
          <a class="btn primary" href="#">Descargar PDF</a>
          <a class="btn secondary" href="#">Ver instrucciones</a>
        </div>

        <p class="note">✅ Incluye pestañas para pegar · ✅ Recomendado a partir de 6 años · ✅ Ideal para aula</p>

        <div class="details">
          <div class="card" style="padding:14px">
            <h3>Descripción</h3>
            <p>
              <?= $fila['descripcionproducto']?>
            </p>
          </div>

          <div class="card" style="padding:14px">
            <h3>Qué incluye</h3>
            <div class="list">
              <div><span>📄</span><span>PDF listo para imprimir (A4)</span></div>
              <div><span>✂️</span><span>Plantilla de recorte + pestañas de pegado</span></div>
              <div><span>🧩</span><span>Montaje guiado en pasos</span></div>
              <div><span>🎨</span><span>Diseño a color (opción para imprimir en B/N)</span></div>
            </div>
          </div>

          <div class="card" style="padding:14px">
            <h3>Consejos de impresión</h3>
            <div class="list">
              <div><span>🖨️</span><span>Papel recomendado: 160–200 g/m²</span></div>
              <div><span>🧴</span><span>Mejor con pegamento de barra o cola blanca</span></div>
              <div><span>📐</span><span>Recorta con tijeras y usa regla en pliegues</span></div>
            </div>
          </div>
        </div>
      </div>
    </section>
	<?php } ?>
    <section>
      <h2 class="title">Recortables similares</h2>
      <div class="grid">
      <?php
			$db = new SQLite3('recortables.db');
			$peticion = "
				SELECT 
				productos.titulo AS tituloproducto,
				categorias.titulo AS categoriaproducto,
				productos.imagen AS imagenproducto
				FROM productos
				LEFT JOIN categorias
				ON productos.categoria = categorias.Identificador
				ORDER BY RANDOM() LIMIT 4;";
			$resultado = $db->query($peticion);
			while ($fila = $resultado->fetchArray(SQLITE3_ASSOC)) {
		?>
        <article>
          <img src="<?= $fila['imagenproducto'] ?>" alt="">
          <div class="card-body">
            <p class="card-title"><?= $fila['tituloproducto'] ?></p>
            <p class="meta"><span class="stars">★★★★☆</span><span class="tag"><?= $fila['categoriaproducto'] ?></span></p>
            <a class="download" href="#">Descargar PDF</a>
          </div>
        </article>
		<?php } ?>
        
      </div>
    </section>
  </main>

  <footer>
    <div class="wrap">
      <a href="#">Acerca de</a>
      <a href="#">Contacto</a>
      <a href="#">Licencias</a>
      <a href="#">Aviso Legal</a>

      <span class="social" aria-label="Redes sociales">
        <a href="#" title="Facebook" aria-label="Facebook">f</a>
        <a href="#" title="X" aria-label="X">x</a>
        <a href="#" title="YouTube" aria-label="YouTube">▶</a>
        <a href="#" title="Instagram" aria-label="Instagram">⌁</a>
      </span>
    </div>
  </footer>
</body>
</html>

