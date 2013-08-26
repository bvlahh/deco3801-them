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

$lines = $parsed == 1 ? "line" : "lines";

$len = strlen($input);

draw_header("THEM prototype - Direct Input");

//draw_error_bar(15, 10, 5, 10, 500, 30);

print "<div>RPC Says:<pre>";
print_r( $parsed );
print "</pre></div>";

print <<<END

<script type="text/javascript">

function set_message(text) {
    
    document.getElementById("infobox").innerHTML = text;
    
}

function messagebox(number) {
    
    if (number == 1)
        set_message("something something doctype");
    
}

</script>

END;

$escaped_document = "";
$start = 0;

// the issue that will crop up with this is indices changing when error spans
// are inserted and content html escaped
foreach( $parsed as $parse ) {
    
    $err_no = $parse[0];
    $start_tag = $parse[1];
    $end_tag = $parse[2];
    
    $s1 = "<span style=\"background-color: #ff7f7f;\" onclick=\"messagebox($err_no);\">";
    $s2 = "</span>";
    
    $escaped_document = $escaped_document . htmlspecialchars( substr($input, $start, $start_tag) ) . $s1 . htmlspecialchars( substr($input, $start_tag, $end_tag - $start_tag) ) . $s2;
    $start = $end_tag;

}
$escaped_document = $escaped_document . htmlspecialchars( substr($input, $start, $len));

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
Default
</div>

<div class="cb"></div>

END;

draw_footer();

?>
