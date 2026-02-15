<?php include "inc/cabecera.php"; ?>

  <section class="page-hero paper-panel">
    <div class="ribbon">GALERÍA DE DIBUJOS</div>
    <h1 class="page-title">Galería</h1>
    <p class="page-sub">Selección de dibujos y estudios. Puedes organizar por tema o técnica.</p>
  </section>

  <section class="block">
    <div class="block-head">
      <h2 class="block-title">Colecciones</h2>
    </div>

    <div class="grid-3">
      <a class="gallery-card paper-card" href="#">
        <div class="gallery-thumb g1"></div>
        <div class="caption">
          <b>Retratos</b>
          <small>Estudios de rostro</small>
        </div>
      </a>

      <a class="gallery-card paper-card" href="#">
        <div class="gallery-thumb g2"></div>
        <div class="caption">
          <b>Objetos</b>
          <small>Volumen y materiales</small>
        </div>
      </a>

      <a class="gallery-card paper-card" href="#">
        <div class="gallery-thumb g3"></div>
        <div class="caption">
          <b>Paisajes</b>
          <small>Composición y profundidad</small>
        </div>
      </a>
    </div>
  </section>

  <section class="block">
    <div class="block-head">
      <h2 class="block-title">Últimas piezas</h2>
    </div>

    <div class="masonry">
    <?php
		$basededatos = new SQLite3('youtube_videos.sqlite');
		$resultado = $basededatos->query("SELECT * FROM videos");
		while ($fila = $resultado->fetchArray(SQLITE3_ASSOC)) {
			 /* htmlspecialchars evita XSS en títulos con caracteres especiales */
			 $titulo = htmlspecialchars($fila['title'], ENT_QUOTES, 'UTF-8');
			 $thumb  = htmlspecialchars($fila['thumbnail_path'], ENT_QUOTES, 'UTF-8');
			 echo '<a class="shot paper-card" href="#">
			 	<span class="shot-img s1" style="background:url(\''.$thumb.'\'');background-size:contain;background-position:center center;"></span>
			 	<span class="shot-cap">'.$titulo.'</span></a>';
		}
		?> 
    </div>
  </section>

<?php include "inc/piedepagina.php"; ?>

