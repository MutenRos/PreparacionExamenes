<?php
// ...obtén $fila con titulo/categoria/imagen (como ya haces)

$titulo = $fila['tituloproducto'] ?? 'Recortable';
$categoria = $fila['categoriaproducto'] ?? 'Recortables';
$imagen = $fila['imagenproducto'] ?? 'img/imgcategoria.png';

$SEO = [
  "title" => $titulo . " – Recortable en PDF para imprimir | recortabl.es",
  "description" => "Descarga el recortable “$titulo” en PDF. Juguete de papel para imprimir, recortar y montar. Categoría: $categoria.",
  "og_type" => "product",
  "image" => $imagen,
  "jsonld" => [
    "@context" => "https://schema.org",
    "@type" => "Product",
    "name" => $titulo,
    "image" => [ $scheme.'://'.$host.'/'.ltrim($imagen,'/') ],
    "brand" => [ "@type" => "Brand", "name" => "recortabl.es" ],
    "category" => $categoria,
    "offers" => [
      "@type" => "Offer",
      "price" => "0.00",
      "priceCurrency" => "EUR",
      "availability" => "https://schema.org/InStock",
      "url" => $scheme.'://'.$host.$_SERVER['REQUEST_URI']
    ]
  ]
];

include "inc/cabecera.php";
?>

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
		// Consulta preparada para evitar SQL Injection
		$stmt = $db->prepare("
		SELECT 
				productos.titulo AS tituloproducto,
				categorias.titulo AS categoriaproducto,
				productos.imagen AS imagenproducto,
				productos.descripcion AS descripcionproducto
				FROM productos
				LEFT JOIN categorias
				ON productos.categoria = categorias.Identificador
		 WHERE productos.Identificador = :id");
		$stmt->bindValue(':id', (int)$_GET['id'], SQLITE3_INTEGER);
		$resultado = $stmt->execute();
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
  <?php include "inc/piedepagina.php"; ?>

