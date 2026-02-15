<?php include "inc/cabecera.php"; ?>

<section>
  <h1 class="title">Contacto</h1>
  <p class="sub">
    ¿Tienes dudas, sugerencias o quieres pedir un recortable concreto? Escríbenos.
  </p>

  <div class="product">
    <!-- Info -->
    <div class="card">
      <h3 style="margin:0 0 8px;color:#1b5f92;font-weight:900">Cómo te ayudamos</h3>
      <p style="margin:0;color:#265a79;font-weight:800;line-height:1.5">
        Respondemos consultas sobre descargas, impresión, montaje y propuestas de nuevos modelos.
        Si reportas un problema, indica el nombre del recortable y, si puedes, adjunta capturas o detalles.
      </p>

      <div class="details">
        <div class="card" style="padding:14px">
          <h3>Temas habituales</h3>
          <div class="list">
            <div><span>📄</span><span>Problemas al descargar el PDF</span></div>
            <div><span>🖨️</span><span>Configuración de impresión (A4, escala, calidad)</span></div>
            <div><span>✂️</span><span>Dudas de montaje / instrucciones</span></div>
            <div><span>💡</span><span>Sugerencias y peticiones de nuevos recortables</span></div>
          </div>
        </div>

        <p class="note">✅ Tiempo de respuesta habitual: 24–72 horas laborables.</p>
      </div>
    </div>

    <!-- Formulario -->
    <div class="card">
      <h2 class="p-title" style="font-size:26px">Escríbenos</h2>
      <p class="p-sub">Rellena el formulario y te contestaremos lo antes posible.</p>

      <form action="#" method="post" style="display:grid;gap:12px">
        <div class="panel" style="border-top:0;padding-top:0">
          <label for="nombre">Nombre</label>
          <input id="nombre" name="nombre" type="text" placeholder="Tu nombre" required>
        </div>

        <div class="panel">
          <label for="email">Email</label>
          <input id="email" name="email" type="email" placeholder="tu@email.com" required>
        </div>

        <div class="panel">
          <label for="motivo">Motivo</label>
          <select id="motivo" name="motivo" required>
            <option value="">Selecciona una opción</option>
            <option>Consulta</option>
            <option>Problema con una descarga</option>
            <option>Sugerencia</option>
            <option>Petición de recortable</option>
            <option>Otro</option>
          </select>
        </div>

        <div class="panel">
          <label for="recortable">Recortable (opcional)</label>
          <input id="recortable" name="recortable" type="text" placeholder="Ej: Castillo Medieval, Robot XL...">
        </div>

        <div class="panel">
          <label for="mensaje">Mensaje</label>
          <textarea id="mensaje" name="mensaje" rows="6" placeholder="Cuéntanos en detalle tu consulta..." required
            style="width:100%;padding:10px 12px;border-radius:12px;border:1px solid #dfeffc;outline:0;
                   background:linear-gradient(180deg,#ffffff,#f6fbff);box-shadow:0 6px 14px rgba(11,42,69,.06);
                   font:inherit;color:#204b66;resize:vertical"></textarea>
        </div>

        <div class="panel">
          <div class="row">
            <label for="privacidad">He leído y acepto la política de privacidad</label>
            <input id="privacidad" name="privacidad" type="checkbox" required>
          </div>
        </div>

        <div class="actions" style="margin-top:0">
          <button class="btn primary" type="submit" style="width:100%;cursor:pointer">Enviar mensaje</button>
          <a class="btn secondary" href="index.php">Volver a inicio</a>
        </div>
      </form>
    </div>
  </div>
</section>

<?php include "inc/piedepagina.php"; ?>

