<?php
require 'vendor/autoload.php';

if (isset($_POST['dane'])) {
    $odebranedane= $_POST['dane'];
    $client = new MongoDB\Client("mongodb://localhost:27017");
    $dane=json_decode($odebranedane);
    foreach ($dane as $key => $skany)
                $client->skany->testy->insertone($skany);

    echo  "dane wysłane";
  }
  else {
    echo "bład wysłania";
  }
 ?>
