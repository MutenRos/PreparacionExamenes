<?php
session_start();
include "inc/cabecera.php";

$flash = $_SESSION['flash'] ?? null;
unset($_SESSION['flash']);

function e(string $s): string { return htmlspecialchars($s, ENT_QUOTES, 'UTF-8'); }

// CSRF token (simple)
if (empty($_SESSION['csrf'])) {
  $_SESSION['csrf'] = bin2hex(random_bytes(16));
}
$csrf = $_SESSION['csrf'];
?>

<section>
  <h1 class="title">Acceso</h1>
  <p class="sub">Inicia sesión con tu cuenta o crea una nueva.</p>

  <?php if ($flash): ?>
    <p class="note" style="margin-bottom:14px"><?= e($flash) ?></p>
  <?php endif; ?>

  <div class="product">
    <!-- LOGIN -->
    <div class="card">
      <h2 class="p-title" style="font-size:26px;margin-bottom:6px">Iniciar sesión</h2>
      <p class="p-sub">Accede con tu email y contraseña.</p>

      <form action="auth_login.php" method="post" style="display:grid;gap:12px">
        <input type="hidden" name="csrf" value="<?= e($csrf) ?>">

        <div class="panel" style="border-top:0;padding-top:0">
          <label for="login_email">Email</label>
          <input id="login_email" name="email" type="email" placeholder="tu@email.com" required>
        </div>

        <div class="panel">
          <label for="login_pass">Contraseña</label>
          <input id="login_pass" name="password" type="password" placeholder="••••••••" required>
        </div>

        <div class="actions" style="margin-top:0">
          <button class="btn primary" type="submit" style="width:100%;cursor:pointer">Entrar</button>
        </div>
      </form>
    </div>

    <!-- SIGNUP -->
    <div class="card">
      <h2 class="p-title" style="font-size:26px;margin-bottom:6px">Crear cuenta</h2>
      <p class="p-sub">Regístrate para guardar tus descargas y preferencias (si lo activas más adelante).</p>

      <form action="auth_signup.php" method="post" style="display:grid;gap:12px">
        <input type="hidden" name="csrf" value="<?= e($csrf) ?>">

        <div class="panel" style="border-top:0;padding-top:0">
          <label for="su_user">Nombre de usuario</label>
          <input id="su_user" name="username" type="text" placeholder="Tu nombre" required minlength="2" maxlength="40">
        </div>

        <div class="panel">
          <label for="su_email">Email</label>
          <input id="su_email" name="email" type="email" placeholder="tu@email.com" required>
        </div>

        <div class="panel">
          <label for="su_pass">Contraseña</label>
          <input id="su_pass" name="password" type="password" placeholder="Mínimo 7 caracteres" required minlength="7">
        </div>

        <div class="panel">
          <label for="su_pass2">Repetir contraseña</label>
          <input id="su_pass2" name="password2" type="password" placeholder="Repite la contraseña" required minlength="7">
        </div>

        <div class="panel">
          <div class="row">
            <label for="su_terms">Acepto las condiciones y la política de privacidad</label>
            <input id="su_terms" name="terms" type="checkbox" required>
          </div>
        </div>

        <div class="actions" style="margin-top:0">
          <button class="btn primary" type="submit" style="width:100%;cursor:pointer">Crear cuenta</button>
        </div>
      </form>
    </div>
  </div>
</section>

<?php include "inc/piedepagina.php"; ?>

