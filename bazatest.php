<?php

if (isset($_POST['dane'])) {
    $odebranedane= $_POST['dane'];
    if(filesize("baza_test.jos")!=0)
    {
        $dane = fread(fopen("baza_test.jos", "r"), filesize("baza_test.jos"));
        $skany=json_decode($dane);
        $skan=json_decode($odebranedane);
        $result = array_merge($skany,$skan);
        $dane=json_encode($result);
    }
   else
        $dane=$odebranedane;

    $fp = fopen("baza_test.jos", "w");
    fputs($fp,$dane);
    fclose($fp);
    echo  "dane wysłane";
  }
  else {
    echo "bład wysłania";
  }
 ?>

