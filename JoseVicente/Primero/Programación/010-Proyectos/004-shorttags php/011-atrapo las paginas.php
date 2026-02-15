<?php
  $c = new mysqli("localhost", "jocarsapress", "jocarsapress", "jocarsapress");
?>
<!doctype html>
<html>
  <head>
    <style>
      <?php include "JVestilo/JVestilo.php";?>
    </style>
  </head>
  <body class="flex fd-column fj-center fa-center b-lightgrey ff-sans-serif p-20">
    <header class="w-800 b-white p-20 ta-center flex fd-column g-20">
      <h1 class="p-0 m-0 fs-36">Jose Vicente Carratala</h1>
      <h2 class="p-0 m-0 fs-16">Desarrollador, profesor y diseñador</h2>
      <nav class="flex g-1 fa-center fj-center">
        <a href="?" class="b-lightgray p-10 c-black td-none fs-10 w-70">Inicio</a>
        <?php
        $r = $c->query("SELECT * FROM paginas;");
        while($f = $r->fetch_assoc()){?>
           <a href="?p=<?= $f['titulo'] ?>" class="b-lightgray p-10 c-black td-none fs-10 w-70"><?= $f['titulo'] ?></a>    
        <?php } ?>
        <a href="?p=blog" class="b-lightgray p-10 c-black td-none fs-10 w-70">Blog</a>
      </nav>
    </header>
    <main class="w-800 b-white p-20 flex fd-column g-20">
      <?php if(!isset($_GET['p'])){ ?>
      <section id="heroe" class="w-800 h-400 b-lightgray p-20" style="box-sizing:border-box;">
        Heroe
      </section>
      <section class="grid gc-2 g-20">
        <article class="ta-center h-200 flex fd-column fa-center fj-center b-lightgray">
          <h3>Titulo</h3>
          <p>texto</p>
        </article>
        <article class="ta-center h-200 flex fd-column fa-center fj-center b-lightgray">
          <h3>Titulo</h3>
          <p>texto</p>
        </article>
      </section>
      <section class="grid gc-3 g-20">
        <article class="ta-center b-lightgray">
          <h3>Titulo</h3>
          <p>texto</p>
        </article>
        <article class="ta-center b-lightgray">
          <h3>Titulo</h3>
          <p>texto</p>
        </article>
        <article class="ta-center b-lightgray">
          <h3>Titulo</h3>
          <p>texto</p>
        </article>
        <article class="ta-center b-lightgray">
          <h3>Titulo</h3>
          <p>texto</p>
        </article>
        <article class="ta-center b-lightgray">
          <h3>Titulo</h3>
          <p>texto</p>
        </article>
        <article class="ta-center b-lightgray">
          <h3>Titulo</h3>
          <p>texto</p>
        </article>
        <article class="ta-center b-lightgray">
          <h3>Titulo</h3>
          <p>texto</p>
        </article>
      </section>
      <?php }else{
        if($_GET['p'] == "blog"){ ?>
        <section class="grid gc-3 g-20">
          <?php
          $r = $c->query("SELECT * FROM entradas;");
          while($f = $r->fetch_assoc()){?>
             <article>
                <h3><?= $f['titulo']?></h3>
                <time><?= $f['fecha']?></time>
                <p><?= htmlspecialchars($f['contenido'])?></p>
             </article>  
          <?php } ?>
        </section>
      <?php 
        }else{?>
          <section class="flex fd-column g-20">
          <?php
          $r = $c->query("SELECT * FROM paginas WHERE titulo='".$_GET['p']."';");
          while($f = $r->fetch_assoc()){?>
             <article>
                <h3><?= $f['titulo']?></h3>
                <p><?= htmlspecialchars($f['contenido']) ?></p>
             </article>  
          <?php } ?>
        </section>
        <?php }
      }?>
    </main>
    <footer class="w-800 b-white p-20 ta-center">
      Piedepagina
    </footer>
  </body>
</html>
