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
      form fieldset input,
      form fieldset select,
      form fieldset textarea{padding:10px;border:1px solid lightgray;width:50%;}
      .control_formulario{display:flex;}
      .control_formulario label,.control_formulario input{flex:1;}
    </style>
  </head>
  <body>
    <form action="" method="POST" encoding="multipart/form-data">
      <fieldset>
        <legend>Formulario de recogida de datos</legend>
        <?php
          $c = new mysqli("localhost","training_center","training_center","training_center");
          $r = $c->query("SHOW COLUMNS FROM inscripciones;");
          while($f = $r->fetch_assoc()){
            if($f['Key'] != "PRI" && $f['Default'] != "CURRENT_TIMESTAMP"){
              echo '<div class="control_formulario"><label for="nombre">Introduce '.$f['Field'].'</label>'; 
              if (str_contains($f['Type'], "varchar")) {
                 echo '<input type="text" name="'.$f['Field'].'" id="'.$f['Field'].'">';
              }else if($f['Type'] == "date"){
                  echo '<input type="date" name="'.$f['Field'].'" id="'.$f['Field'].'">';
              }else if($f['Type'] == "int"){
                  echo '<input type="number" name="'.$f['Field'].'" id="'.$f['Field'].'">';
              }else if (str_contains($f['Type'], "decimal")) {
                 echo '<input type="number" name="'.$f['Field'].'" id="'.$f['Field'].'" step="0.01">';
              }else if (str_contains($f['Type'], "tinyint")) {
                 echo '<input type="checkbox" name="'.$f['Field'].'" id="'.$f['Field'].'" step="0.01">';
              }else if (str_contains($f['Type'], "enum")) {
                 echo '<select name="'.$f['Field'].'" id="'.$f['Field'].'" >';
                 preg_match_all("/'([^']+)'/", $f['Type'], $matches);
                 $enumValues = $matches[1];
                 var_dump($enumValues);
                 foreach($enumValues as $clave=>$valor){
                  echo '<option value="'.$valor.'">'.$valor.'</option>';
                 }
                 echo '</select>';
              }else if($f['Type'] == "text"){
                  echo '<textarea name="'.$f['Field'].'" id="'.$f['Field'].'"></textarea>';
              }else if (str_contains($f['Type'], "blob")) {
                 echo '<input type="file" name="'.$f['Field'].'" id="'.$f['Field'].'" step="0.01">';
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
