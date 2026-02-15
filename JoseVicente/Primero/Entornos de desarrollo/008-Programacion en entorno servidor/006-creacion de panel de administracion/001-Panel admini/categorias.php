<?php include "inc/cabecera.php"; ?>

<section>
  <h1 class="title">Categorías</h1>
  <p class="sub">Explora los recortables por temática. Elige una categoría para ver sus modelos.</p>

  <div class="toolbar">
    <div class="toolbar-top">
      <div class="counts">
        <?php
          $db = new SQLite3('recortables.db');
          $total = $db->querySingle("SELECT COUNT(*) FROM categorias");
          echo "Mostrando $total categorías";
        ?>
      </div>

      <div class="sort">
        <span>Ordenar</span>
        <select onchange="location.href='categorias.php?o='+this.value">
          <?php $o = $_GET['o'] ?? 'az'; ?>
          <option value="az"  <?= $o==='az'  ? 'selected' : '' ?>>A–Z</option>
          <option value="za"  <?= $o==='za'  ? 'selected' : '' ?>>Z–A</option>
          <option value="new" <?= $o==='new' ? 'selected' : '' ?>>Recientes</option>
        </select>
      </div>
    </div>
  </div>

  <div class="grid">
    <?php
      $order = "titulo ASC";
      if (($o ?? '') === 'za')  $order = "titulo DESC";
      if (($o ?? '') === 'new') $order = "Identificador DESC";

      $db = $db ?? new SQLite3('recortables.db');
      $res = $db->query("SELECT Identificador, titulo, imagen FROM categorias ORDER BY $order");

      while ($fila = $res->fetchArray(SQLITE3_ASSOC)) {
        $id = (int)$fila['Identificador'];
        $titulo = $fila['titulo'] ?? 'Categoría';
        $img = $fila['imagen'] ?? 'img/imgcategoria.png';

        // Count products in category (optional but useful)
        $count = (int)$db->querySingle("SELECT COUNT(*) FROM productos WHERE categoria = $id");
    ?>
      <article>
        <img src="<?= htmlspecialchars($img, ENT_QUOTES, 'UTF-8') ?>" alt="">
        <div class="card-body">
          <p class="card-title"><?= htmlspecialchars($titulo, ENT_QUOTES, 'UTF-8') ?></p>
          <p class="meta">
            <span class="tag"><?= $count ?> recortables</span>
            <span class="stars">★★★★☆</span>
          </p>
          <a class="download" href="catalogo.php?cat=<?= $id ?>">Ver recortables</a>
        </div>
      </article>
    <?php } ?>
  </div>

  <div class="subtle-rule"></div>
</section>

<?php include "inc/piedepagina.php"; ?>

