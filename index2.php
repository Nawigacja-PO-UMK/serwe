<?php


$odebranedane= $_POST['dane'];

if (isset($odebranedane)) {
    echo"dane wysłane";
  }
  else {
    echo 'bład wysłania';
  }
///przyszła obróbka danych

//zapis
$fp = fopen("baza_pozycji.jos", "a");
fputs($fp,$odebranedane);
fclose($fp);
 ?>
