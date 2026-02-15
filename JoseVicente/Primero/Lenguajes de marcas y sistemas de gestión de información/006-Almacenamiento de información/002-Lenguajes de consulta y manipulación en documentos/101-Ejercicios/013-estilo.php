<!doctype html>
<html lang="es">
  <head>
    <title>Formulario</title>
    <meta charset="utf-8">
    <style>
  :root{
    --primary: crimson;
    --primary-light: #ff8fa0;
    --bg: #f2f2f2;
    --text: #333;
    --border: #ddd;
  }

  body, html{
    background: var(--bg);
    display: flex;
    justify-content: center;
    padding: 40px;
    font-family: "Segoe UI", sans-serif;
    color: var(--text);
  }

  form{
    background: white;
    padding: 30px 40px;
    width: 650px;
    border-radius: 10px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.1);
    border-top: 8px solid var(--primary);
  }

  legend{
    font-size: 1.4em;
    font-weight: bold;
    color: var(--primary);
    margin-bottom: 10px;
  }

  form fieldset{
    display: flex;
    flex-direction: column;
    gap: 20px;
    border: none;
    padding: 0;
  }

  .control_formulario{
    display: flex;
    flex-direction: column;
    gap: 6px;
  }

  .control_formulario label{
    font-size: 0.95em;
    font-weight: 600;
    color: var(--primary);
  }

  /* Campos de texto, selects, textarea (excluimos checkbox) */
  form fieldset input:not([type="checkbox"]),
  form fieldset select,
  form fieldset textarea{
    padding: 12px 14px;
    border: 1px solid var(--border);
    border-radius: 6px;
    width: 100%;
    font-size: 1em;
    transition: border 0.3s, box-shadow 0.3s;
    box-sizing:border-box;
  }

  form fieldset input:not([type="checkbox"]):focus,
  form fieldset select:focus,
  form fieldset textarea:focus{
    border-color: var(--primary);
    box-shadow: 0 0 0 3px var(--primary-light);
    outline: none;
  }

  /* ---------- INTERRUPTOR ANIMADO PARA CHECKBOX ---------- */

  /* Contenedor del checkbox: alineamos horizontalmente label + switch */
  .control_formulario_checkbox{
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
  }
  .control_formulario_checkbox label{
    margin: 0;
  }

  /* Estilo base del checkbox como switch */
  .control_formulario_checkbox input[type="checkbox"]{
    appearance: none;
    -webkit-appearance: none;
    width: 52px;
    height: 28px;
    border-radius: 999px;
    background: #ccc;
    position: relative;
    cursor: pointer;
    outline: none;
    border: 1px solid #bbb;
    transition: background 0.25s ease-in-out, border-color 0.25s ease-in-out;
    flex-shrink: 0;
  }

  /* “Botón” circular del switch */
  .control_formulario_checkbox input[type="checkbox"]::before{
    content: "";
    position: absolute;
    width: 22px;
    height: 22px;
    border-radius: 50%;
    background: white;
    top: 50%;
    left: 3px;
    transform: translateY(-50%);
    box-shadow: 0 2px 6px rgba(0,0,0,0.25);
    transition: transform 0.25s ease-in-out;
  }

  /* Estado activado: color crimson y botón a la derecha */
  .control_formulario_checkbox input[type="checkbox"]:checked{
    background: var(--primary);
    border-color: var(--primary);
  }

  .control_formulario_checkbox input[type="checkbox"]:checked::before{
    transform: translate(22px, -50%);
  }

  /* Pequeño efecto al hacer focus vía teclado */
  .control_formulario_checkbox input[type="checkbox"]:focus-visible{
    box-shadow: 0 0 0 3px var(--primary-light);
  }

  /* ------------------------------------------------------ */

  input[type="submit"]{
    background: var(--primary);
    color: white;
    padding: 14px;
    border: none;
    border-radius: 6px;
    font-size: 1.1em;
    cursor: pointer;
    margin-top: 10px;
    transition: background 0.3s;
  }

  input[type="submit"]:hover{
    background: #b30021;
  }
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
              } else if (str_contains($f['Type'], "tinyint")) {
                    echo '<div class="control_formulario control_formulario_checkbox">';
                    echo '<label for="'.$f['Field'].'">Introduce '.$f['Field'].'</label>'; 
                    echo '<input type="checkbox" name="'.$f['Field'].'" id="'.$f['Field'].'">';
                    echo '</div>';

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
