<?php
$SEO = [
  "title" => "Categorías de recortables infantiles | recortabl.es",
  "description" => "Explora recortables para imprimir por categorías: vehículos, edificios, animales, fantasía y más. Elige una temática y descarga tu PDF.",
  "og_type" => "website",
];
include "inc/cabecera.php";
?>

    <section>
      <h1 class="title">Catálogo de recortables</h1>
      <p class="sub">Explora todos los modelos. Filtra por categoría, nivel y valoración.</p>

      <div class="catalog">
        <aside>
          <h3>Filtros</h3>

          <div class="panel">
            <label for="q">Buscar</label>
            <input id="q" type="search" placeholder="Ej: dinosaurio, coche, castillo..." />
          </div>

          <div class="panel">
            <label for="cat">Categoría</label>
            <select id="cat">
              <option>Todas</option>
              <option>Vehículos</option>
              <option>Edificios</option>
              <option>Robots</option>
              <option>Animales</option>
              <option>Navidad</option>
              <option>Educativos</option>
              <option>Muñecos</option>
            </select>
          </div>

          <div class="panel">
            <label for="lvl">Dificultad</label>
            <select id="lvl">
              <option>Todas</option>
              <option>Fácil</option>
              <option>Media</option>
              <option>Difícil</option>
            </select>
          </div>

          <div class="panel">
            <div class="row">
              <label>Valoración</label>
              <span style="color:var(--muted);font-weight:800">mínimo</span>
            </div>
            <div class="chips" role="listbox" aria-label="Valoración mínima">
              <span class="chip" aria-current="true">Todas</span>
              <span class="chip">3★+</span>
              <span class="chip">4★+</span>
              <span class="chip">5★</span>
            </div>
          </div>

          <div class="panel">
            <div class="row">
              <label for="free">Solo gratis</label>
              <input id="free" type="checkbox" checked />
            </div>
            <div class="row">
              <label for="new">Novedades</label>
              <input id="new" type="checkbox" />
            </div>
          </div>
        </aside>

        <div>
          <div class="toolbar">
            <div class="toolbar-top">
              <div class="counts">Mostrando 1–16 de 128</div>
              <div class="sort">
                <span>Ordenar</span>
                <select>
                  <option>Relevancia</option>
                  <option>Más descargados</option>
                  <option>Mejor valorados</option>
                  <option>Novedades</option>
                  <option>A–Z</option>
                </select>
              </div>
            </div>
          </div>

          <div class="grid">
            <!-- Repite/inyecta desde backend. Por ahora, ejemplo con placeholders -->
            <?php
            	if(!isset($_POST['buscar'])){
            		$_POST['buscar'] = "";
            	}
		   		$db = new SQLite3('recortables.db');
		   		// Consulta preparada para evitar SQL Injection
		   		$stmt = $db->prepare("SELECT * FROM productos WHERE titulo LIKE :buscar");
		   		$stmt->bindValue(':buscar', '%'.$_POST['buscar'].'%', SQLITE3_TEXT);
		   		$resultado = $stmt->execute();
		   		while ($fila = $resultado->fetchArray(SQLITE3_ASSOC)) {
		   	?>
            <article>
              <img src="imgcategoria.png" alt="Recortable <?= htmlspecialchars($fila['titulo'], ENT_QUOTES, 'UTF-8') ?>">
              <div class="card-body">
                <p class="card-title"><?= htmlspecialchars($fila['titulo'], ENT_QUOTES, 'UTF-8') ?></p>
                <p class="meta"><span class="stars">★★★★☆</span><span class="tag">Edificios</span></p>
                <a class="download" href="producto.php?id=<?= (int)$fila['Identificador']?>">Descargar PDF</a>
              </div>
            </article>
			<?php } ?>
            
          </div>

          <div class="pager" aria-label="Paginación">
            <a href="#" aria-label="Anterior">‹</a>
            <a href="#" aria-current="true">1</a>
            <a href="#">2</a>
            <a href="#">3</a>
            <a href="#">4</a>
            <a href="#" aria-label="Siguiente">›</a>
          </div>
        </div>
      </div>
    </section>
  <?php include "inc/piedepagina.php"; ?>
