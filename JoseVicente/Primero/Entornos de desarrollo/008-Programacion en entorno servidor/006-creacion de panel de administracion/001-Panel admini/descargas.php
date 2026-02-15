<?php
session_start();
include "inc/cabecera.php";
?>

<section>
  <h1 class="title">Descargas</h1>
  <p class="sub">
    Accede a los recortables disponibles para descargar.
  </p>

  <?php if (!isset($_SESSION['user'])): ?>
    <p class="note">
      🔐 Debes <a href="login.php" style="text-decoration:underline">iniciar sesión</a>
      para acceder a tus descargas personalizadas.
    </p>
  <?php endif; ?>

  <div class="toolbar">
    <div class="toolbar-top">
      <div class="counts">
        <?php
          $db = new SQLite3('recortables.db');
          $total = $db->querySingle("SELECT COUNT(*) FROM productos");
          echo "Mostrando $total recortables";
        ?>
      </div>

      <div class="sort">
        <span>Ordenar</span>
        <select onchange="location.href='descargas.php?o='+this.value">
          <?php $o = $_GET['o'] ?? 'new'; ?>
          <option value="new" <?= $o==='new' ? 'selected' : '' ?>>Más recientes</option>
          <option value="az"  <?= $o==='az'  ? 'selected' : '' ?>>A–Z</option>
          <option value="za"  <?= $o==='za'  ? 'selected' : '' ?>>Z–A</option>
        </select>
      </div>
    </div>
  </div>

  <div class="grid">
    <?php
      $order = "Identificador DESC";
      if ($o === 'az') $order = "titulo ASC";
      if ($o === 'za') $order = "titulo DESC";

      $res = $db->query("
        SELECT 
          productos.Identificador,
          productos.titulo,
          productos.imagen,
          categorias.titulo AS categoria
        FROM productos
        LEFT JOIN categorias ON productos.categoria = categorias.Identificador
        ORDER BY $order
      ");

      while ($fila = $res->fetchArray(SQLITE3_ASSOC)) {
    ?>
      <article>
        <img src="<?= htmlspecialchars($fila['imagen'] ?? 'img/imgcategoria.png') ?>" alt="">
        <div class="card-body">
          <p class="card-title"><?= htmlspecialchars($fila['titulo']) ?></p>
          <p class="meta">
            <span class="tag"><?= htmlspecialchars($fila['categoria'] ?? 'Sin categoría') ?></span>
            <span class="stars">★★★★☆</span>
          </p>

          <?php if (isset($_SESSION['user'])): ?>
            <a class="download" href="producto.php?id=<?= (int)$fila['Identificador'] ?>">
              Descargar PDF
            </a>
          <?php else: ?>
            <a class="download" href="login.php">
              Inicia sesión para descargar
            </a>
          <?php endif; ?>
        </div>
      </article>
    <?php } ?>
  </div>

  <div class="subtle-rule"></div>
</section>

<?php include "inc/piedepagina.php"; ?>

