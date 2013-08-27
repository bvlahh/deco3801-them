<?php

require_once "misc.php";
require_once "header.php";
require_once "footer.php";
require_once "rpc_client.php";
require_once "errorbar.php";

if (! array_key_exists("input", $_POST) )
    redirect("/direct_input");

$input = $_POST["input"];

$parsed = rpc_validate(array(), base64_encode($input) );

$len = strlen($input);

draw_header("THEM prototype - Direct Input");

//draw_error_bar(15, 10, 5, 10, 0, 500, 30, true);
draw_error_bar(0, 0, 0, 0, 1, 500, 30, true);

print "<div>RPC Says:<pre>";
print_r( $parsed );
print "</pre></div>";

$input = str_replace("\r", "", $input); // remove the return before inserting show error tags
$escaped_document = "";
$current_index = 0;
// the issue that will crop up with this is indices changing when error spans
// are inserted and content html escaped

foreach( $parsed as $parse ) {
    $err_no = $parse[0];
    $start_tag = $parse[1];
    $end_tag = $parse[2] + 1; // substr takes in end-index exclusive

    
    $s1 = "<span style=\"background-color: #ff7f7f;\" onclick=\"messagebox($err_no);\">";
    $s2 = "</span>";
    $escaped_document = $escaped_document . htmlspecialchars(substr($input, $current_index, $start_tag - $current_index)) . 
        $s1 . htmlspecialchars(substr($input, $start_tag, $end_tag - $start_tag)) . $s2;  
    $current_index = $end_tag;
}
$escaped_document = $escaped_document . htmlspecialchars(substr($input, $current_index, strlen($input) - $start));

$num_lines = substr_count($input, "\n");

$line_nos = "";

for ($l=1; $l<$num_lines+2; $l++)
    $line_nos .= "$l\n";

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
