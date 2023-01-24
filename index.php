<?php

if (isset($_POST['dane'])) {
    $odebranedane= $_POST['dane'];
    if(filesize("baza_pozycji.jos")!=0)
    {
        $dane = fread(fopen("baza_pozycji.jos", "r"), filesize("baza_pozycji.jos"));
        $skany=json_decode($dane);
        $skan=json_decode($odebranedane);
        $result = array_merge($skany,$skan);
        $dane=json_encode($result);
    }
   else
        $dane=$odebranedane;

    $fp = fopen("baza_pozycji.jos", "w");
    fputs($fp,$dane);
    fclose($fp);
    echo  "dane wysłane";
  }
  else {
    echo "bład wysłania";
  }
 ?>
