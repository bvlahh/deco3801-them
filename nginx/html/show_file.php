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
$parsed_errors = json_decode($file["cached_parse"]);

// remove the carrage return before inserting show error tags, to keep
// the char indices correct
$input = str_replace("\r", "", $input);

// chop it into chunks
// structure of each chunk:
// text (string), original start (int), original end (int), errors (list)

$general_document_errors = array();
$in_document_errors = array();

foreach ( $parsed_errors as $parsed_error ) {
    
    if ( $parsed_error[1] == -1 )
        $general_document_errors[] = $parsed_error;
    else
        $in_document_errors[] = $parsed_error;
    
}

$chunks = array();

$chunks[] = array(
    "text" => $input,
    "start" => 0,
    "end" => strlen($input),
    "errors" => array()
    );

foreach ( $in_document_errors as $in_document_error ) {
    
    // the end index from the parser is the last char inclusive
    $in_document_error[2]++;
    
    // split the chunk that contains the start of the new error
    
    $start_chunk = 0;
    
    // find the chunk to start split
    for ($ci = 0; $ci<count($chunks); $ci++)
        if ( ($in_document_error[1] >= $chunks[$ci]["start"]) && ($in_document_error[1] <= $chunks[$ci]["end"]) ) {
            $start_chunk = $ci;
            break;
        }
    
    // shove everything along to make room for the split
    for ($ci=count($chunks)-1; $ci > $start_chunk; $ci--)
        $chunks[$ci+1] = $chunks[$ci];
    
    // $orig_start_chunk is the start chunk to split
    $orig_start_chunk = $chunks[$start_chunk];
    
    // chunk index to split at
    $start_split_index = $in_document_error[1] - $orig_start_chunk["start"];
    
    // chunk is untouched
    // chunk + 1 is the part with the new error
    
    $chunks[$start_chunk] = array(
        "text" => substr($orig_start_chunk["text"], 0, $start_split_index),
        "start" => $orig_start_chunk["start"],
        "end" => $orig_start_chunk["start"] + $start_split_index,
        "errors" => $orig_start_chunk["errors"]
    );
    
    $chunks[$start_chunk+1] = array(
        "text" => substr($orig_start_chunk["text"], $start_split_index, strlen($orig_start_chunk["text"]) - $start_split_index),
        "start" => $orig_start_chunk["start"] + $start_split_index,
        "end" => $orig_start_chunk["end"],
        "errors" => $orig_start_chunk["errors"]
    );
    
    // split the chunk that contains the end of the new error
    
    $end_chunk = 0;
    
    // find the chunk to end split
    for ($ci = 0; $ci<count($chunks); $ci++)
        if ( ($in_document_error[2] >= $chunks[$ci]["start"]) && ($in_document_error[2] <= $chunks[$ci]["end"]) ) {
            $end_chunk = $ci;
            break;
        }
    
    // shove everything along to make room for the split
    for ($ci=count($chunks)-1; $ci > $end_chunk; $ci--)
        $chunks[$ci+1] = $chunks[$ci];
    
    // $orig_end_chunk is the end chunk to split
    $orig_end_chunk = $chunks[$end_chunk];
    
    // chunk index to split at
    $end_split_index = $in_document_error[2] - $orig_end_chunk["start"];
    
    // end_chunk is the part with the new error
    // end_chunk + 1 is untouched
    
    $chunks[$end_chunk] = array(
        "text" => substr($orig_end_chunk["text"], 0, $end_split_index),
        "start" => $orig_end_chunk["start"],
        "end" => $orig_end_chunk["start"] + $end_split_index,
        "errors" => $orig_end_chunk["errors"]
    );
    
    $chunks[$end_chunk+1] = array(
        "text" => substr($orig_end_chunk["text"], $end_split_index, strlen($orig_end_chunk["text"]) - $end_split_index),
        "start" => $orig_end_chunk["start"] + $end_split_index,
        "end" => $orig_end_chunk["end"],
        "errors" => $orig_end_chunk["errors"]
    );
    
    // mark all the chunks between the outer new chunks (exclusive) as having the new error
    
    for ( $error_chunk = $start_chunk + 1; $error_chunk <= $end_chunk; $error_chunk++ )
        $chunks[$error_chunk]["errors"][] = $in_document_error[0];
    
}

$top_info = "";

foreach ( $general_document_errors as $general_document_error ) {
    
    $err_no = $general_document_error[0];
    
    $err_message_output = htmlspecialchars( Errors::errorString($err_no) );
    
    $top_info .= $err_message_output . "<br />";
    
}

$error_lines = array();
$escaped_document = "";
$error_semantics = 0;
$error_access = 0;
$error_deprecated = 0;
$error_misc = 0;

foreach ( $chunks as $chunk ) {
    
    $start_span = "";
    $end_span = "";
    
    if ( count($chunk["errors"]) != 0 ) {
        
        $err_no = min($chunk["errors"]);
        $err_nos = htmlspecialchars(json_encode($chunk["errors"]));
        $err_colour = Errors::errorColour($err_no);
        
        $start_span = "<a href=\"#\" style=\"background-color: $err_colour; text-decoration: none; border-left: 1px solid #fbfbfb; border: 1px solid #fbfbfb;\" onclick=\"messagebox(&quot;$err_nos&quot;); return false;\">";
        $end_span = "</a>";
        
        // mark the line for line number highlighting
        $error_lines[ $chunk["start"] > 0 ? substr_count($input, "\n", 0, $chunk["start"]) : 0] = $err_colour;

        if ($err_colour == "#ffff7f") {
            /* poor practice */
            $error_misc++;
        } else if ($err_colour == "#7f7fff") {
            /* accessibiity */
            $error_access++;
        } else if ($err_colour == "#ffbb77") {
            /* deprecated tags */
            $error_deprecated++;
        } else {
            /* syntax, semantics */
            $error_semantics++;
        }
        
    }
    
    $escaped_document .= $start_span . htmlspecialchars($chunk["text"]) . $end_span;
    
}

// Generates a line count of the original HTML document.
$num_lines = substr_count($input, "\n");

$line_nos = "";

// A string of the line count
for ($l=1; $l<$num_lines+2; $l++) {
    
    if (array_key_exists($l-1, $error_lines))
        $line_nos .= "<span style=\"background-color: ${error_lines[$l-1]};\">$l</span>\n";
    else
        $line_nos .= "$l\n";
    
}

$set = $file["upload_set"];
$count_files = count(get_set($set));

draw_header("THEM prototype - $filename");

$upload_set = "";

if ($count_files > 1)
    $upload_set = <<<END
        <a class="uploadset_back" href="show_set?set=$set">
            Uploaded Files
        </a>
END;

print <<<END

<div>
    
    $upload_set
    
    <span style="font-size: 140%;">
    $filename
    </span>
    
</div>

<div style="margin-bottom: 10px;">

END;

if ( count($parsed_errors) == 0 )
    draw_error_bar(0, 0, 0, 0, 1, 1010, 10);
else
    draw_error_bar($error_access, $error_semantics, $error_deprecated, $error_misc, 0, 1010, 10);

print <<<END

</div>

<div class="top_infobox" id="top_infobox">$top_info</div>

<div style="padding: 10px;">Click on highlighted text for more information.</div>

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
