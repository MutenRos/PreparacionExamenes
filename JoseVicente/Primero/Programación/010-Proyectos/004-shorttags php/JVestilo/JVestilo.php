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
    echo ".h-".$i."{height:".$i."px;}";
    echo ".fs-".$i."{font-size:".$i."px;}";
    echo ".g-".$i."{gap:".$i."px;}";
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
.grid{display:grid;}
.
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
