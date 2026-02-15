<section class="catalogo">
        <?php for($i = 0;$i<30;$i++){ ?>
          <article>
            <div class="imagen" style="background:url(producto.webp);background-size:cover;background-position:center center;"></div>
            <h3>Nombre del producto</h3>
            <p>Breve descripción del producto</p>
            <p>4.33€</p>
            <a href="?operacion=producto&producto=1">🛍 Comprar</a>
          </article>
        <?php } ?>
        </section>
