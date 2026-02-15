<?php
  class Gato{
    private $color;
    private $edad;
    
    public function __construct($color,$edad){
      $this->color = $color;
      $this->edad = $edad;
    }
    public function setEdad($nuevaedad){
      $this->edad = $nuevaedad;
    }
    public function setColor($nuevocolor){
      $this->color = $nuevocolor;
    }
    public function getEdad(){
      return $this->edad;
    }
    public function getColor(){
      return $this->color;
    }
  }
  
  $gato1 = new Gato("blanco",0);
  
  
  echo $gato1->getColor();
  echo $gato1->getEdad();
?>
