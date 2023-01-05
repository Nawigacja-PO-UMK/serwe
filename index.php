<?php


$odebranedane= $_POST['dane'];

if (isset($odebranedane)) {
  try {
    $skany=json_decode($odebranedane);
    $client = new MongoClient("mongodb://localhost:27017");
    foreach($skany as $key => $value)
    {
      $client->skany->insert($value);
    }
    echo"dane wysłane";
  } catch (Exception $e) {
   echo $e->getMessage();
  }

  }

  else {
    echo 'bład wysłania';
  }
 ?>
