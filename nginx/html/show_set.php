<?php

require_once "php/misc.php";
require_once "php/header.php";
require_once "php/footer.php";
require_once "php/files.php";
require_once "php/errors.php";
require_once "php/errorbar.php";

if (! array_key_exists("set", $_GET) )
    redirect("/");

$set = $_GET["set"];

$set = get_set($set);

draw_header("THEM prototype - Uploaded Files");

foreach( $set as $file ) {
    
    //${file["cached_parse"]}
    
    print <<<END
        <a href="/show_file?file=${file["id"]}">${file["filename"]}</a><br />
END;
    
}

draw_footer();

?>
