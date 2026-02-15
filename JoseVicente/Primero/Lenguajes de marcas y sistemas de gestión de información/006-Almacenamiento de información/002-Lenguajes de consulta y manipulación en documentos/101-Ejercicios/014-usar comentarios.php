<!doctype html>
<html lang="es">
  <head>
    <title>Formulario</title>
    <meta charset="utf-8">

    <style>
      /* Tus estilos originales tal cual */
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
      .control_formulario_checkbox{
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
      }
      .control_formulario_checkbox input[type="checkbox"]{
        appearance: none;
        width: 52px;
        height: 28px;
        border-radius: 999px;
        background: #ccc;
        cursor: pointer;
        border: 1px solid #bbb;
        transition: background .25s;
        position: relative;
      }
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
        transition: transform 0.25s;
      }
      .control_formulario_checkbox input[type="checkbox"]:checked{
        background: var(--primary);
        border-color: var(--primary);
      }
      .control_formulario_checkbox input[type="checkbox"]:checked::before{
        transform: translate(22px, -50%);
      }

      input[type="submit"]{
        background: var(--primary);
        color: white;
        padding: 14px;
        border: none;
        border-radius: 6px;
        font-size: 1.1em;
        cursor: pointer;
        margin-top: 10px;
      }
    </style>

  </head>
  <body>
    <form action="" method="POST" enctype="multipart/form-data">
      <fieldset>
        <legend>Formulario de recogida de datos</legend>

        <?php
          $c = new mysqli("localhost","training_center","training_center","training_center");

          /* COMENTARIO DE LA TABLA */
          $tableComment = $c->query("
            SELECT TABLE_COMMENT
            FROM information_schema.tables
            WHERE table_schema='training_center'
              AND table_name='inscripciones'
          ")->fetch_assoc()['TABLE_COMMENT'];

          if ($tableComment != "") {
              echo "<p style='color:#555; margin-top:-5px; margin-bottom:20px;'>$tableComment</p>";
          }

          /* COLUMNAS CON SUS COMENTARIOS */
          $r = $c->query("
            SELECT COLUMN_NAME, COLUMN_TYPE, COLUMN_KEY, COLUMN_DEFAULT, COLUMN_COMMENT
            FROM information_schema.columns
            WHERE table_schema='training_center'
              AND table_name='inscripciones'
          ");

          while($f = $r->fetch_assoc()) {

            $campo = $f['COLUMN_NAME'];
            $tipo  = $f['COLUMN_TYPE'];
            $comentario = $f['COLUMN_COMMENT'];

            /* NO tocar esta lógica: respetar exclusiones */
            if($f['COLUMN_KEY'] == "PRI" || $f['COLUMN_DEFAULT'] == "CURRENT_TIMESTAMP") continue;

            echo '<div class="control_formulario">';

            // LABEL = nombre técnico de la columna (como pediste)
            echo '<label for="'.$campo.'">Introduce '.$campo.'</label>';

            // PÁRRAFO = comentario explicativo
            if ($comentario != "") {
              echo '<p style="margin:0; font-size:0.85em; color:#666;">'.$comentario.'</p>';
            }

            /* ---------- Mantener tus tipos de campo exactamente ---------- */

            if (str_contains($tipo, "varchar")) {
               echo '<input type="text" name="'.$campo.'" id="'.$campo.'">';
            }
            else if ($tipo == "date") {
               echo '<input type="date" name="'.$campo.'" id="'.$campo.'">';
            }
            else if ($tipo == "int") {
               echo '<input type="number" name="'.$campo.'" id="'.$campo.'">';
            }
            else if (str_contains($tipo, "decimal")) {
               echo '<input type="number" name="'.$campo.'" id="'.$campo.'" step="0.01">';
            }
            else if (str_contains($tipo, "tinyint")) {
               echo '<div class="control_formulario_checkbox">';
               echo '<label for="'.$campo.'">Introduce '.$campo.'</label>';
               echo '<input type="checkbox" name="'.$campo.'" id="'.$campo.'">';
               echo '</div>';
            }
            else if (str_contains($tipo, "enum")) {
               echo '<select name="'.$campo.'" id="'.$campo.'">';
               preg_match_all("/'([^']+)'/", $tipo, $matches);
               foreach($matches[1] as $valor){
                 echo '<option value="'.$valor.'">'.$valor.'</option>';
               }
               echo '</select>';
            }
            else if ($tipo == "text") {
               echo '<textarea name="'.$campo.'" id="'.$campo.'"></textarea>';
            }
            else if (str_contains($tipo, "blob")) {
               echo '<input type="file" name="'.$campo.'" id="'.$campo.'">';
            }

            echo '</div>';
          }
        ?>

        <input type="submit">
      </fieldset>
    </form>
  </body>
</html>

