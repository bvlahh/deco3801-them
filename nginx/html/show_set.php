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

if ( count($set) < 2 )
    redirect("/show_file?file=" . $set[0]["id"]);

draw_header("THEM prototype - Uploaded Files");

foreach( $set as $file ) {
    
    //${file["cached_parse"]}
    
    print <<<END
        <a href="/show_file?file=${file["id"]}">${file["filename"]}</a>
END;

	$parsed = json_decode($file["cached_parse"]);

	if ( count($parsed) == 0 )
	    draw_error_bar(0, 0, 0, 0, 1, 500, 10);
	else
	    draw_error_bar(0, 1, 0, 0, 0, 500, 10);
    
    print <<<END
    	<br />
END;
}

draw_footer();

?>
