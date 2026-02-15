<!doctype html>
<html>
  <head>
    <style>
      html,body{background:grey;width:100%;height:100%;padding:0px;margin:0px;font-family:sans-serif;}
      body{display:flex;align-items:center;justify-content:center;}
      h1{width:800px;height:300px;padding:20px;background:white;display:flex;align-items:center;justify-content:center;font-style:italic;border-radius:10px;}
    </style>
  </head>
  <body>
    <h1>
      <?php
        $prompt = "
          Dame una cita inspiradora, solo  una frase.
          Introducela en un <span> HTML
          En el span, introduce un estilo color CSS
          el color CSS debe transmitir el sentimiento que transmita la frase (por ejemplo: rojo = pasión)
          Dame solo el span con el color, no me des explicaciones
          Tampoco me pongas fences
          ";
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
    </h1>
  </body>
</html>


