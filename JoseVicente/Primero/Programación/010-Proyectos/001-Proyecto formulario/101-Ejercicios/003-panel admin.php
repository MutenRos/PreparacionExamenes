

<!doctype html>
<html lang="es">
  <head>
    <title>Formulario</title>
    <meta charset="utf-8">
    <style>
      body,html{width:100%;height:100%;padding:0px;margin:0px;}
      body{display:flex;}
      nav{flex:1;background:crimson;padding:10px;display:flex;flex-direction:column;gap:10px;}
      main{flex:5;padding:10px;}
      table{border:1px solid crimson;padding:10px;width:100%;border-collapse:collapse;}
      nav button{background:white;border:none;padding:10px;border-radius:20px;}
      table tr:nth-child(odd){background:rgb(255,220,220);}
      table td{padding:10px;}
    </style>
  </head>
  <body>
    <nav>
      <button>Enlace 1</button>
      <button>Enlace 2</button>
      <button>Enlace 3</button>
    </nav>
    <main>
      <table>
        <?php for($i = 0;$i<30;$i++){ ?>
          <tr>
            <td>Nombre</td><td>Apellidos</td><td>Email</td><td>Direccion</td><td>Codigo</td>
          </tr>
        <?php } ?>
      </table>
    </main>
  </body>
</html>
