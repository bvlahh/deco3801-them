<?php

require_once "misc.php";
require_once "header.php";
require_once "footer.php";
require_once "rpc_client.php";
require_once "errorbar.php";

if (! array_key_exists("input", $_POST) )
    redirect("/direct_input");

$input = $_POST["input"];

$parsed = rpc_validate(array(), $input);

$lines = $parsed == 1 ? "line" : "lines";

$len = strlen($input);

draw_header("THEM prototype - Direct Input");

draw_error_bar(15, 10, 5, 10, 500);

print <<<END

<script type="text/javascript">

function infobox(number) {
    
    document.getElementById("infobox").innerHTML = "info number " + number;
        
}

</script>

END;

if ( $len > 100 ) {
    
    $info = rand(0, 10);
    
    $s1 = "<span style=\"background-color: #00FF00;\" onclick=\"infobox($info);\">";
    $s2 = "</span>";
    
    $start_tag = rand(0, $len-1);
    $end_tag = rand($start_tag+1, $len);
    
    $escaped_document = htmlspecialchars( substr($input, 0, $start_tag) ) . $s1 . htmlspecialchars( substr($input, $start_tag, $end_tag - $start_tag) ) . $s2 . htmlspecialchars( substr($input, $end_tag, $len - $end_tag) );
    
}

$num_lines = substr_count($escaped_input, "\n");

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
