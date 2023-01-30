
<?php





$path="/var/www/html/gueryWays.py " +$_POST['S_X'] +" "+$_POST['S_Y']+" "+ $_POST['S_L']+" "+$_POST['E_X']+" "+$_POST['E_Y']+ " "$_POST['E_L'] ;
$cmd="python3 $path";

$command=escapeshellcmd($cmd);

$output=shell_exec($command);

echo($output);
?>
