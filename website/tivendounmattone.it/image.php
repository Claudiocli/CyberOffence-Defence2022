
<?php
function getImage()
{
  $file = 'www/web/images/goldenwall4admin.jpg';

  if (isset($_GET['file'])) {
    $file = $_GET['file'];
  }

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
  if ($pos === false) {
    echo "Permission denied!";
  } else {
    $imageData = base64_encode(file_get_contents($file));
    $src = 'data: image/jpeg;base64,' . $imageData;

    echo '<img src="' . $src . '">';
  }
}
getImage();
?>
