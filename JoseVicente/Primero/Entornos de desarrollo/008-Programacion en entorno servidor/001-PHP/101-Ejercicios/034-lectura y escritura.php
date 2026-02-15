<?php
  class Gato{
    function constructor(){
      $this->color;
      $this->edad;
    }
  }
  
  $gato1 = new Gato();
  $gato2 = new Gato();
  
  var_dump($gato1);
  
  $gato1->color = "blanco";
  $gato1->edad = 0;
  
  echo $gato1->color;
  echo $gato1->edad;
?>
