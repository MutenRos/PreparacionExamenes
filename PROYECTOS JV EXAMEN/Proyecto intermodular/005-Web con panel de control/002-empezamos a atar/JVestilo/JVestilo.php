<?php
  include "colores.php";
  foreach($colores as $color){
    echo ".b-".strtolower($color)."{background:".strtolower($color).";}";
    echo ".c-".strtolower($color)."{color:".strtolower($color).";}";
  }
  for($i = 0;$i<2000;$i++){
    echo ".p-".$i."{padding:".$i."px;}";
    echo ".m-".$i."{margin:".$i."px;}";
    echo ".w-".$i."{width:".$i."px;}";
    echo ".w-".$i."pc{width:".$i."%;}";
    echo ".h-".$i."{height:".$i."px;}";
    echo ".h-".$i."pc{height:".$i."%;}";
    echo ".fs-".$i."{font-size:".$i."px;}";
    echo ".g-".$i."{gap:".$i."px;}";
    echo ".bradius-".$i."{border-radius:".$i."px;}";
    echo ".f-".$i."{flex:".$i.";}";
  }
?>
.flex{display:flex;}
.fd-row{flex-direction:row;}
.fd-column{flex-direction:column;}
.fj-center{justify-content:center;}
.fa-center{align-items:center;}

<?php
  include "familiasfuentes.php";
  foreach($familias as $familia){
    echo ".ff-".strtolower($familia)."{font-family:".strtolower($familia).";}";
  }
?>

.grid{display:grid;} /* <-- FIX: antes había un '.' suelto aquí, y rompía CSS */

<?php
  for($i = 0;$i<20;$i++){
    echo ".gc-".$i."{grid-template-columns:repeat(".$i.",100fr);}";
  }
?>

<?php
  $alineaciones = ['left','right','center','justify'];
  foreach($alineaciones as $alineacion){
    echo ".ta-".$alineacion."{text-align:".$alineacion.";}";
  }
?>

.td-none{text-decoration:none;}

/* BORDES  //////////////////// */
<?php
  $tiposLineaCss = [
      "none","hidden","solid","dashed","dotted","double","groove","ridge","inset","outset"
  ];
  for($i = 0;$i<20;$i++){
    foreach($tiposLineaCss as $tipo){
      foreach($colores as $color){
        echo ".br-".$i."-".$tipo."-".strtolower($color)."{border:".$i."px ".$tipo." ".$color.";}";
      }
    }
  }
?>

/* MINIMO EXTRA (solo lo necesario) */
.br-1-solid{border:1px solid #e5e7eb;}
.shadow-1{box-shadow:0 10px 25px rgba(0,0,0,.08);}
.shadow-2{box-shadow:0 18px 45px rgba(0,0,0,.12);}
.radius-10{border-radius:10px;}

