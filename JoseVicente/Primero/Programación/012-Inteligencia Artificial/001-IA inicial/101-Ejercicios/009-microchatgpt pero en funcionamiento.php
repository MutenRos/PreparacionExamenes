<!doctype html>
<html>
  <head>
    <style>
  html,body{
    background:grey;
    width:100%;
    height:100%;
    padding:0;
    margin:0;
    font-family:sans-serif;
  }

  body{
    display:flex;
    align-items:center;
    justify-content:center;
  }

  section{
    width:500px;
    height:500px;
    padding:20px;
    background:white;
    display:flex;
    flex-direction:column;
    justify-content:space-between;
    align-items:stretch;
    border-radius:30px;
  }

  form input{
    width:100%;
    box-sizing:border-box;
    padding:10px;
    border:1px solid lightgrey;
    border-radius:30px;
    outline:none;
  }

  form input:focus{
    background:lightgray;
  }

  #pregunta{
    background:lightgray;
    width:80%;
    padding:20px;
    border-radius:0 15px 15px 15px;
    align-self:flex-start;
  }

  #respuesta{
    background:lightgray;
    width:80%;
    padding:20px;
    border-radius:15px 0 15px 15px;
    align-self:flex-end; /* ← THIS is the key */
    text-align:left;
  }
  p{
    margin:0px;
    padding:0px;
  }
  h1{
    text-align:center;
  }
</style>

  </head>
  <body>
    <section>
      <h1>jocarsa | microchat</h1>
      <p id="pregunta">
        <?php
          if(isset($_POST['prompt'])){echo $_POST['prompt'];}
        ?>
      </p>
      <p id="respuesta">
        <?php
          if(isset($_POST['prompt'])){
            $prompt = $_POST['prompt']." - responde en un solo párrafo, sin código, en prosa.";
            $data = [
                "model"  => "qwen2.5:7b-instruct-q4_0",
                "prompt" => $prompt,
                "stream" => false
            ];
            $ch = curl_init("http://localhost:11434/api/generate"); // Hago una petición a local
            curl_setopt_array($ch, [
                CURLOPT_RETURNTRANSFER => true,
                CURLOPT_POST           => true,
                CURLOPT_HTTPHEADER     => ["Content-Type: application/json"],
                CURLOPT_POSTFIELDS     => json_encode($data),
            ]);
            $response = curl_exec($ch);                           // Ejecuto curl
            curl_close($ch);                                      // cierro curl
            $result = json_decode($response, true);               // Paso la respuesta a json
            echo $result["response"];                             // Y la pinto en pantalla
          }
        ?>
      </p>
      <form method="POST" action="?">
        <input type="text" name="prompt">
      </form>
    </section>
  </body>
</html>


