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
    font-style:italic;
    border-radius:10px;
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
</style>

  </head>
  <body>
    <section>
      <p id="pregunta">
        <?php
          if(isset($_POST['prompt'])){echo $_POST['prompt'];}
        ?>
      </p>
      <p id="respuesta">Respuesta</p>
      <form method="POST" action="?">
        <input type="text" name="prompt">
      </form>
    </section>
  </body>
</html>


