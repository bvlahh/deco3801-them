<?php

require_once "misc.php";
require_once "header.php";
require_once "footer.php";

if (! array_key_exists("file", $_FILES) )
    redirect("/upload_file");

$filename = $_FILES["file"]["name"];
$file = $_FILES["file"]["tmp_name"];

$file_contents = htmlspecialchars( file_get_contents($file) );

draw_header("");

print <<<END
    
    <div>
        <pre>$filename</pre>
    </div>
    <div>
        <pre>$file_contents</pre>
    </div>
    
END;

draw_footer();

?>
