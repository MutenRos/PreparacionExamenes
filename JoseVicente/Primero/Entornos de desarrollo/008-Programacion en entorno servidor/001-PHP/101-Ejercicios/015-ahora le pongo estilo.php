<!doctype html>
<html>
  <head>
    <style>
      body{
        display:grid;
        grid-template-columns:repeat(7,50px);
      }
      div{
        width:40px;
        height:40px;
        border:1px solid grey;
        padding:5px;
      }
    </style>
  </head>
  <body>
    <?php
      for($dia = 1;$dia<31;$dia++){
        echo "<div>".$dia."</div>
        ";
      }
    ?>
  </body>
</html>
