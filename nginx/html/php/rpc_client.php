<?php

require_once "JsonRpcClient.php";

function rpc_validate($files, $document) {
	
	$parser = new JsonRpcClient("http://localhost:8080");
	
	return $parser->parse_html(
			array(
					"files" => $files,
					"document" => $document
				)
		);
	
}

?>
