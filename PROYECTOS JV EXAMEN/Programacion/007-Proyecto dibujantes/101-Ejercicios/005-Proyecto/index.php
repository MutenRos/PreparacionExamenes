<?php include "inc/cabecera.php"; ?>

  <!-- HERO -->
  <section class="hero">
    <div class="hero-left paper-panel">
      <h1 class="hero-title">
        APRENDE A <span>DIBUJAR</span><br>
        A <span>MANO ALZADA</span>
      </h1>
      <p class="hero-sub">Tutoriales y consejos para artistas</p>

      <div class="hero-sketches" aria-hidden="true">
        <div class="sketch-card">
          <div class="sketch-thumb"></div>
        </div>
        <div class="sketch-card">
          <div class="sketch-thumb"></div>
        </div>
      </div>
    </div>

    <aside class="hero-right featured paper-panel" aria-label="Video destacado">
      <div class="ribbon ribbon-red">NUEVO VIDEO</div>

      <div class="featured-frame">
        <div class="featured-thumb" role="img" aria-label="Miniatura del vídeo destacado"></div>
        <a class="btn btn-red btn-big" href="#">▶ VER AHORA</a>
      </div>
    </aside>
  </section>

  <!-- QUICK LINKS -->
  <section class="quick" aria-label="Accesos rápidos">
  
   <?php
		$basededatos = new SQLite3('youtube_videos.sqlite');
		$resultado = $basededatos->query("SELECT * FROM playlists LIMIT 3");
		while ($fila = $resultado->fetchArray(SQLITE3_ASSOC)) {
		 $codigo = str_replace(".jpg","",str_replace("thumbnails/playlists/","",$fila['thumbnail_path']));
			 /* htmlspecialchars protege contra XSS en datos dinámicos */
			 $tituloPlaylist = htmlspecialchars($fila['title'], ENT_QUOTES, 'UTF-8');
			 echo '
			 	<a class="quick-card paper-card" href="https://www.youtube.com/watch?v=YqPMgVdBRQY&list='.$codigo.'&index=1">
					<div class="quick-top quick-top-gold">'.$tituloPlaylist.'</div>
					<div class="quick-body">
					  <div class="quick-thumb" style="background:url(\''.$fila['thumbnail_path'].'\');background-size:cover;background-position:center center;"></div>
					  <span class="btn btn-red">▶ VER VIDEO</span>
					</div>
				 </a>
			 ';
		}
		?> 
  
    

    
  </section>

  <!-- LATEST VIDEOS -->
  <section class="block" aria-label="Últimos videos">
    <div class="block-head">
      <h2 class="block-title">ÚLTIMOS <span>VIDEOS</span></h2>
    </div>

    <div class="grid-3">
      
      <?php
		$basededatos = new SQLite3('youtube_videos.sqlite');
		$resultado = $basededatos->query("SELECT * FROM videos ORDER BY upload_date DESC LIMIT 6");
		while ($fila = $resultado->fetchArray(SQLITE3_ASSOC)) {
		 $codigo = str_replace(".jpg","",str_replace("thumbnails/","",$fila['thumbnail_path']));
			 /* Saneamos la salida para evitar inyección de HTML */
			 $tituloVideo = htmlspecialchars($fila['title'], ENT_QUOTES, 'UTF-8');
			 $tipoVideo   = htmlspecialchars($fila['type'],  ENT_QUOTES, 'UTF-8');
			 echo '
			 	<a class="media-card paper-card" href="https://www.youtube.com/watch?v='.$codigo.'">
				  <div class="media-thumb media-thumb-shading" aria-hidden="true" style="background:url(\''.$fila['thumbnail_path'].'\'');background-size:cover;background-position:center center;">
				    <div class="media-label">
				      <b>'.$tipoVideo.'</b><br><b>'.$tituloVideo.'</b>
				    </div>
				  </div>
				  <span class="btn btn-red btn-center">▶ VER VIDEO</span>
				</a>
			 ';
		}
		?> 

      

      
    </div>
  </section>

  <!-- COURSES + NEWSLETTER -->
  <section class="block block-split" aria-label="Cursos y suscripción">
    <article class="paper-panel">
      <div class="block-head">
        <h2 class="block-title">CURSOS DESTACADOS</h2>
      </div>

      <div class="course-card">
        <div class="course-thumb" aria-hidden="true"></div>

        <div class="course-info">
          <div class="course-title">Curso de Retrato</div>
          <div class="course-sub">De cero a sombreado con lápiz</div>
        </div>

        <a class="btn btn-red" href="#">▶ VER CURSO</a>
      </div>
    </article>

    <aside class="paper-panel newsletter">
      <div class="newsletter-inner">
        <h2 class="newsletter-title">¡ÚNETE A LA COMUNIDAD!</h2>
        <p class="newsletter-sub">Recibe tips y novedades en tu correo</p>

        <form class="newsletter-form" action="#" method="post">
          <input class="input" type="email" name="email" placeholder="Tu correo electrónico" required>
          <button class="btn btn-red" type="submit">SUSCRIBIRME</button>
        </form>
      </div>
    </aside>
  </section>


<?php include "inc/piedepagina.php"; ?>
