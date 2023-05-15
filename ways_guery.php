<?php

$path= $_POST["S_X"]. " " . $_POST["S_Y"] . " ". $_POST['S_L']." ".$_POST['E_X']." ".$_POST['E_Y']. " ".$_POST['E_L'] ;
$cmd="/var/www/html/server/env/bin/python /var/www/html/server/serwe/gueryWays.py " .$path ." 2>&1 ";

$output=shell_exec($cmd);


echo($output);
?>
