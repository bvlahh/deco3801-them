<?php

require_once "misc.php";
require_once "header.php";
require_once "footer.php";
require_once "JsonRpcClient.php";

if (! array_key_exists("input", $_POST) )
	redirect("/direct_input");

$input = $_POST["input"];

$parser = new JsonRpcClient("http://localhost:8080");

$parsed = $parser->parse_html($input);

$lines = $parsed == 1 ? "line" : "lines";

$num_lines = substr_count($input, "\n");

$line_nos = "";

for ($l=1; $l<$num_lines+2; $l++)
	$line_nos .= "$l\n";

$escaped_input = htmlspecialchars($input);

draw_header("THEM prototype - Direct Input");

print <<<END

<div class="file">
	
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

END;

draw_footer();

?>
