<?php

require_once "misc.php";
require_once "header.php";
require_once "footer.php";

if (! array_key_exists("file", $_FILES) )
    redirect("/upload_file");

$filename = $_FILES["file"]["name"];
$file = $_FILES["file"]["tmp_name"];

$input = file_get_contents($file);

$num_lines = substr_count($input, "\n");

$line_nos = "";

for ($l=1; $l<$num_lines+2; $l++)
	$line_nos .= "$l\n";

$escaped_input = htmlspecialchars($input);

draw_header("THEM prototype - Uploaded File");

print <<<END
    
    <div style="font-weight: bold;">
        $filename
    </div>
    
    <div class="file">
	    
	    <div class="file_lines">
		    <pre>$line_nos</pre>
	    </div>
	    
	    <div class="file_body">
		    <pre>$escaped_input</pre>
	    </div>
        
	    <div class="cb"></div>
        
    </div>
    
END;

draw_footer();

?>
