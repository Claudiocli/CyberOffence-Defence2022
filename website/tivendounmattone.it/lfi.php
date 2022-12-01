
<?php
$file = $_GET['file'];

while (true) {
  if (strpos($file, "../") === false) { //OLD php version
    //if(str_contains($file,"../") === false){ //new php version
    break;
  }
  $file = str_replace("../", "", $file);
}

if (strtolower(PHP_OS) == "windows") {
  $file = str_replace("/", "\\", $file);
} else {
  $file = str_replace("\\", "/", $file);
}

$regex = 'www/web/images';
$pos = strpos($file, $regex);
//$pos = str_contains($file,$regex);
if ($pos === false) {
  echo "Permission denied!";
} else {
  // Dio ca
  $content = file_get_contents($file);
  // header('Content-Type: image/jpeg');
  echo $content;
}

?>
