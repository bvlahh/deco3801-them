<?php

require_once "php/misc.php";
require_once "php/header.php";
require_once "php/footer.php";
require_once "php/files.php";
require_once "php/errors.php";
require_once "php/errorbar.php";

if (! array_key_exists("file", $_GET) )
    redirect("/");

$file = $_GET["file"];

$file = get_file($file);

if (! $file)
    redirect("/");

$filename = $file["filename"];
$input = base64_decode($file["document"]);
$parsed = json_decode($file["cached_parse"]);

// remove the carrage return before inserting show error tags, to keep
// the char indices correct
$input = str_replace("\r", "", $input);

// the issue that will crop up with this is indices changing when error
// spans are inserted and content html escaped

$escaped_document = "";
$current_index = 0;

foreach( $parsed as $parse ) {
    
    $err_no = $parse[0];
    $err_colour = Errors::errorColor($err_no);
    $start_tag = $parse[1];
    $end_tag = $parse[2] + 1; // substr takes in end-index exclusive
    
    $start_span = "<span style=\"background-color: $err_colour;\" onclick=\"messagebox($err_no);\">";
    $end_span = "</span>";
    
    $escaped_document = $escaped_document . htmlspecialchars(substr($input, $current_index, $start_tag - $current_index)) . 
        $start_span . htmlspecialchars(substr($input, $start_tag, $end_tag - $start_tag)) . $end_span;  
    
    $current_index = $end_tag;
    
}

$escaped_document = $escaped_document . htmlspecialchars(substr($input, $current_index, strlen($input) - $current_index));

$num_lines = substr_count($input, "\n");

$line_nos = "";

for ($l=1; $l<$num_lines+2; $l++)
    $line_nos .= "$l\n";

draw_header("THEM prototype - $filename");

if ( count($parsed) == 0 )
    draw_error_bar(0, 0, 0, 0, 1, 500, 10);
else
    draw_error_bar(0, 1, 0, 0, 0, 500, 10);

print <<<END

<div class="file" style="float: left; margin-top: 10px">
    
    <div class="file_lines">
        <pre>$line_nos</pre>
    </div>
    
    <div class="file_body">
        <pre>$escaped_document</pre>
    </div>
    
    <div class="cb"></div>
    
</div>

<div style="float: left; border: 1px solid #DDDDDD; margin-top: 10px; margin-left: 10px; padding: 5px;" id="infobox">

</div>

<div class="cb"></div>


<script type="text/javascript" src="errorlabels.js"></script>

END;

draw_footer();

?>
