<!doctype html>
<html>
  <head>
    <style>
      html,body{background:grey;width:100%;height:100%;padding:0px;margin:0px;}
      body{display:flex;align-items:center;justify-content:center;}
      section{width:800px;height:300px;padding:20px;background:white;}
    </style>
  </head>
  <body>
    <section>
      <?php
        $prompt = "¿Que es HTML? - responde solo en texto, sin ejemplos, máximo un párrafo";
        $data = [
            "model"  => "qwen2.5-coder:7b",
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
      ?>
    </section>
  </body>
</html>


