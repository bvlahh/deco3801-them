<?php

require_once "JsonRpcClient.php";

/**
* Creates a new JsonRpcClient communicating on port 8080 over localhost before
* attempting to call the "parse_html" function on the JSON-RPC server using the 
* provided file list array and document.
*
* @param string[]  $files     An array containing the file structure of a site
* which has been uploaded as a zip.
* @param string    $document  The HTML document which is to be parsed.
*/
function validate($files, $document) {
	
	$parser = new JsonRpcClient("http://localhost:8080");
	
	return $parser->parse_html(
			array(
					"files" => $files,
					"document" => $document
				)
		);
	
}

?>
