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

$escaped_input = htmlspecialchars($input);

draw_header("THEM prototype - Direct Input");

draw_error_bar(15, 25, 5);

$len = strlen($escaped_input);

print <<<END

<script type="text/javascript">

function infobox(number) {
	
	document.getElementById("infobox").innerHTML = "info number " + number;
		
}

</script>

END;

if ( $len > 100 ) {
	
	$info = rand(0, 10);
	
	$s1 = "<span style=\"background-color: #00FF00;\" onclick=\"infobox($info)\">";
	$s2 = "</span>";
	
	$start_tag = rand(0, $len-1);
	$end_tag = rand($start_tag+1, $len);
	
	$escaped_input = substr($escaped_input, 0, $start_tag) . $s1 . substr($escaped_input, $start_tag, $end_tag - $start_tag) . $s2 . substr($escaped_input, $end_tag, $len - $end_tag);
	
}

$num_lines = substr_count($escaped_input, "\n");

$line_nos = "";

for ($l=1; $l<$num_lines+2; $l++)
	$line_nos .= "$l\n";

print <<<END

<div class="file" style="float: left;">
	
	<div class="file_lines">
		<pre>$line_nos</pre>
	</div>
	
	<div class="file_body">
		<pre>$escaped_input</pre>
	</div>
    
	<div class="cb"></div>
    
    <div style="background-color: #EEEEEE; text-align: center;">
        <pre>$parsed $lines</pre>
    </div>
	
</div>

<div style="float: left; border: 1px solid #DDDDDD;" id="infobox">
Default
</div>

<div class="cb"></div>

END;

draw_footer();

?>
