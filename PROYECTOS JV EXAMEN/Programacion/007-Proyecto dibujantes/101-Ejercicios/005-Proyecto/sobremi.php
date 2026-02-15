<?php include "inc/cabecera.php"; ?>

  <section class="page-hero paper-panel">
    <div class="ribbon ribbon-red">SOBRE MÍ</div>
    <h1 class="page-title">Sobre mí</h1>
    <p class="page-sub">Un espacio para explicar tu enfoque, tu método y cómo seguir el canal.</p>
  </section>

  <section class="block block-split">
    <article class="paper-panel about">
      <div class="about-row">
        <div class="about-photo" aria-hidden="true"></div>
        <div>
          <h2 class="block-title">Hola, soy el autor del canal</h2>
          <p class="text">
            Aquí puedes presentar tu historia y el objetivo del canal: aprender dibujo a mano alzada
            con ejercicios claros, repetibles y orientados a resultados.
          </p>
          <p class="text">
            Puedes añadir tu frecuencia de publicación, materiales recomendados y cómo pedir sugerencias.
          </p>

          <div class="about-actions">
            <a class="btn btn-red" href="#">▶ Ver YouTube</a>
            <a class="btn btn-ghost" href="tutoriales.html">Ver tutoriales</a>
          </div>
        </div>
      </div>
    </article>

    <aside class="paper-panel">
      <h2 class="block-title">Contacto</h2>
      <p class="text muted">Formulario simple (puedes conectarlo a tu backend).</p>

      <form class="stack" action="#" method="post">
        <input class="input" type="text" name="nombre" placeholder="Tu nombre" required minlength="2" maxlength="80">
        <input class="input" type="email" name="email" placeholder="Tu correo" required maxlength="120">
        <textarea class="textarea" name="mensaje" placeholder="Tu mensaje" rows="6" required minlength="10" maxlength="1000"></textarea>
        <button class="btn btn-red" type="submit">ENVIAR</button>
      </form>
    </aside>
  </section>

<?php include "inc/piedepagina.php"; ?>
