<?php

/**
* The results page. 
* Displays the HTML document including line numbers and adds a span over each
* tag containing an error, coloured to match the error type. 
*/

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

/**
* $input is the original HTML document.
* $parsed is the array of error information returned by the parser.
*/

$filename = $file["filename"];
$input = base64_decode($file["document"]);
$parsed = json_decode($file["cached_parse"]);

// remove the carrage return before inserting show error tags, to keep
// the char indices correct
$input = str_replace("\r", "", $input);

// the issue that will crop up with this is indices changing when error
// spans are inserted and content html escaped

$escaped_document = "";
$top_info = "";
$err_message = "";
$current_index = 0;

$error_lines = array();

/**
* Process each of the returned errors.
* The array of errors contains arrays of the form [error_number, starting_position, end_position]
* where starting_position and end_position represent the start and end of the tag for which the
* error applies to.
*/
foreach( $parsed as $parse ) {
    
    $err_no = $parse[0];
    $err_colour = Errors::errorColor($err_no);
    $start_tag = $parse[1];
    $end_tag = $parse[2] + 1; // substr takes in end-index exclusive
    
    if ($start_tag >= 0) {
        $start_span = "<span style=\"background-color: $err_colour;\" onclick=\"messagebox($err_no);\">";
        $end_span = "</span>";
        
        //$error_lines[] = array(substr_count(substr($input, 0, $start_tag), "\n"), $err_colour);
        $error_lines[substr_count(substr($input, 0, $start_tag), "\n")] = $err_colour;
        
        /**
        * Generates a formatted version of the original HTML document containing all errors 
        * by inserting the spans representing the errors found in the document into the original
        * string representation of the HTML document.
        */
        $escaped_document = $escaped_document . htmlspecialchars(substr($input, $current_index, $start_tag - $current_index)) . 
            $start_span . htmlspecialchars(substr($input, $start_tag, $end_tag - $start_tag)) . $end_span;

        $current_index = $end_tag;
        
    } else {
        foreach ( Errors::$error_strings as $err_number => $err_message ) {
            if ($err_no == $err_number)
                $err_message_output = $err_message
        }
        $top_info = $top_info . "<span style=\"background-color: $err_colour;>" . $err_message . "</span><br />";
    } 
    
}

$escaped_document = $escaped_document . htmlspecialchars(substr($input, $current_index, strlen($input) - $current_index));

// Generates a line count of the original HTML document.
$num_lines = substr_count($input, "\n");

$line_nos = "";

// A string of the line count
for ($l=1; $l<$num_lines+2; $l++) {
    if (array_key_exists($l-1, $error_lines)) {
        //$bgc = ${error_lines[$l]};
        $line_nos .= "<span style=\"background-color: ${error_lines[$l-1]};\">$l</span>\n";
    } else {
        $line_nos .= "$l\n";
    }
}

draw_header("THEM prototype - $filename");

if ( count($parsed) == 0 )
    draw_error_bar(0, 0, 0, 0, 1, 500, 10);
else
    draw_error_bar(0, 1, 0, 0, 0, 500, 10);

print <<<END

<div class="top_infobox" id="top_infobox">$top_info</div>

<div class="file" style="float: left; margin-top: 10px">
    
    <div class="file_lines">
        <pre>$line_nos</pre>
    </div>
    
    <div class="file_body">
        <pre>$escaped_document</pre>
    </div>
    
    <div class="cb"></div>
    
</div>

<div class="infobox" id="infobox">

</div>

<div class="cb"></div>

<script type="text/javascript" src="errorlabels.js"></script>

END;

draw_footer();

?>
