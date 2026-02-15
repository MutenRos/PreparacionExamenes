<!doctype html>
<html lang="es">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width,initial-scale=1" />
  <title>recortabl.es</title>

  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Delius&display=swap" rel="stylesheet">

  <link rel="stylesheet" href="estilo/estilo.css">
</head>

<body>
  <header>
    <div class="wrap">
      <a class="brand" href="index.php">
        <div class="logo">🤖</div>
        <span><b>rec</b><i>ortabl.es</i></span>
      </a>

      <nav>
        <a href="categorias.php">Categorías ▾</a>
        <a href="sobrenosotros.php">Sobre nosotros</a>
        <a href="descargas.php">Descargas</a>
        <a href="login.php">Login</a>
        <div class="search" role="search">
          <div class="icon">🔎</div>
          <form action="catalogo.php" method="POST">
          	<input type="search" placeholder="Buscar..." aria-label="Buscar" name="buscar"/>
          </form>
        </div>
      </nav>
    </div>
  </header>

  <main class="wrap">
