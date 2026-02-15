<?php 

$SEO = [
  "title" => "Recortables para imprimir | Juguetes de papel en PDF – recortabl.es",
  "description" => "Recortables infantiles y educativos en PDF para imprimir, recortar y montar. Actividades perfectas para casa y para el aula.",
  "og_type" => "website",
];
include "inc/cabecera.php"; ?>
    <section id="heroe">
      <div class="hero">
        <div class="hero-inner">
          <div>
            <h3>Juguetes recortables para imprimir y jugar</h3>
            <h4>Descarga · Imprime · Recorta · Pega · Juega</h4>
            <div class="actions">
              <a class="btn primary" href="catalogo.php">Explorar recortables</a>
              <a class="btn secondary" href="#">Cómo funciona</a>
            </div>
          </div>

          <!-- Sustituye estos “bloques” por ilustraciones reales (coche / tren / etc.) si las tienes -->
          <div class="hero-art" aria-hidden="true">
            <div class="toy">🚗<br>Vehículos</div>
            <div class="toy">🚂<br>Juguetes</div>
          </div>
        </div>
        <div class="hero-wave"></div>
        <div class="hero-floor"></div>
      </div>
    </section>

    <section id="categoriasprincipales">
      <div class="title">Categorías principales</div>
      <div class="contenedor">
      	<?php
      		$db = new SQLite3('recortables.db');
      		$peticion = "SELECT * FROM categorias";
      		$resultado = $db->query($peticion);
      		while ($fila = $resultado->fetchArray(SQLITE3_ASSOC)) {
      	?>
        <article><img src="<?= htmlspecialchars($fila['imagen'], ENT_QUOTES, 'UTF-8') ?>" alt="Categoría <?= htmlspecialchars($fila['titulo'], ENT_QUOTES, 'UTF-8') ?>"><p><?= htmlspecialchars($fila['titulo'], ENT_QUOTES, 'UTF-8') ?></p></article>
        <?php } ?>
      </div>
      <div class="subtle-rule"></div>
    </section>

    <section id="recortablesdestacados">
      <div class="title">Recortables destacados</div>

      <div class="contenedor">
        <article>
          <img src="imgcategoria.png" alt="">
          <div class="card-body">
            <p class="card-title">Castillo Medieval</p>
            <p class="stars">★★★★☆</p>
            <a class="download" href="#">Descargar PDF</a>
          </div>
        </article>

        <article>
          <img src="imgcategoria.png" alt="">
          <div class="card-body">
            <p class="card-title">Coche de Fórmula 1</p>
            <p class="stars">★★★★☆</p>
            <a class="download" href="#">Descargar PDF</a>
          </div>
        </article>

        <article>
          <img src="imgcategoria.png" alt="">
          <div class="card-body">
            <p class="card-title">Dinosaurio T-Rex</p>
            <p class="stars">★★★★☆</p>
            <a class="download" href="#">Descargar PDF</a>
          </div>
        </article>

        <article>
          <img src="imgcategoria.png" alt="">
          <div class="card-body">
            <p class="card-title">Robot XL</p>
            <p class="stars">★★★★☆</p>
            <a class="download" href="#">Descargar PDF</a>
          </div>
        </article>
      </div>

      <div class="subtle-rule"></div>
    </section>

    <section id="galeria">
      <div class="strip">
        <a href="#"><img src="imgcategoria.png" alt=""></a>
        <a href="#"><img src="imgcategoria.png" alt=""></a>
        <a href="#"><img src="imgcategoria.png" alt=""></a>
        <a href="#"><img src="imgcategoria.png" alt=""></a>
        <a href="#"><img src="imgcategoria.png" alt=""></a>
      </div>
    </section>

    <section id="informacion">
      <div class="contenedor">
        <div>
          <h3>Para familias y educación</h3>
          <p>✅ Manualidades educativas</p>
          <p>✅ Desarrollo de psicomotricidad</p>
          <p>✅ Uso en aula y en casa</p>
          <p>✅ PDFs listos para imprimir</p>
        </div>

        <!-- Sustituye por una ilustración real si la tienes -->
        <div class="info-art" aria-hidden="true">
          👩‍🏫👧🧒<br>
          Zona ilustración (familias / aula)
        </div>
      </div>
    </section>
  
<?php include "inc/piedepagina.php"; ?>
