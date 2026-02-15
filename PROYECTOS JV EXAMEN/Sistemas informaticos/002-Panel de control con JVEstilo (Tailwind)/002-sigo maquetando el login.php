<!doctype html>
<html class="w-100pc h-100pc p-0 m-0">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>Login — Panel de control</title>
    <style>
      <?php include("JVestilo/JVestilo.php"); ?>
    </style>
    <!-- Estilos extra para hover y transiciones -->
    <style>
      input[type="submit"]{
        cursor:pointer;
        transition: background .2s ease, transform .15s ease;
      }
      input[type="submit"]:hover{
        background:#b0b0b0;
        transform:translateY(-1px);
      }
      input[type="text"]:focus,
      input[type="password"]:focus{
        outline:none;
        border-color:teal;
        box-shadow:0 0 0 3px rgba(0,128,128,.15);
      }
    </style>
  </head>
  <body class="b-lightgray flex fa-center fj-center w-100pc h-100pc p-0 m-0">
    <form class="w-200 h-200 b-white p-20 flex fd-column g-20 fj-center bradius-10"
          onsubmit="return validarLogin(this)">
      <input type="text" placeholder="usuario" class="p-10 br-1-solid-lightgray bradius-5" required>
      <input type="password" placeholder="contraseña" class="p-10 br-1-solid-lightgray bradius-5" required>
      <input type="submit" value="Entrar" class="p-10 br-1-solid-lightgray b-lightgray bradius-5">
    </form>
    <!-- Validación JS del formulario -->
    <script>
      function validarLogin(form) {
        var usuario = form.querySelector('[type="text"]');
        var password = form.querySelector('[type="password"]');
        if (usuario.value.trim().length < 3) {
          alert('El usuario debe tener al menos 3 caracteres.');
          usuario.focus();
          return false;
        }
        if (password.value.length < 4) {
          alert('La contraseña debe tener al menos 4 caracteres.');
          password.focus();
          return false;
        }
        return true;
      }
    </script>
  </body>
</html>
