<?php
  class Gato{
    private $color;
    private $edad;
    
    public function constructor(){
      $this->color;
      $this->edad;
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
  
  $gato1 = new Gato();
  $gato2 = new Gato();
  
  
  $gato1->setColor("blanco");
  $gato1->setEdad(0);
  
  echo $gato1->getColor();
  echo $gato1->getEdad();
?>
