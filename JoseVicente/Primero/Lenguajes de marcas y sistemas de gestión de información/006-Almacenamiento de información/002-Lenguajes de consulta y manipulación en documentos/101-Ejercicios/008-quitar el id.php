<!doctype html>
<html lang="es">
  <head>
    <title>Formulario</title>
    <meta charset="utf-8">
    <style>
      body,html{background:lightgray;display:flex;
        width:100%;justify-content:center;font-family:sans-serif;}
      form{background:white;padding:20px;width:600px;}
      form fieldset{display:flex;flex-direction:column;gap:20px;border:none;}
      form fieldset input{padding:10px;border:1px solid lightgray;}
      .control_formulario{display:flex;}
      .control_formulario label,.control_formulario input{flex:1;}
    </style>
  </head>
  <body>
    <form>
      <fieldset>
        <legend>Formulario de recogida de datos</legend>
        <?php
          $c = new mysqli("localhost","training_center","training_center","training_center");
          $r = $c->query("SHOW COLUMNS FROM inscripciones;");
          while($f = $r->fetch_assoc()){
            if($f['Key'] != "PRI" || $f['Extra'] == "DEFAULT_GENERATED"){
              echo '<div class="control_formulario"><label for="nombre">Introduce '.$f['Field'].'</label>'; 
              if (str_contains($f['Type'], "varchar")) {
                 echo '<input type="text" name="'.$f['Field'].'" id="'.$f['Field'].'">';
              }else if($f['Type'] == "date"){
                  echo '<input type="date" name="'.$f['Field'].'" id="'.$f['Field'].'">';
              }
              echo'</div>';
             }
          }
          ?>
        <input type="submit">
      </fieldset>
    </form>
  </body>
</html>
