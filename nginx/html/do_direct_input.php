<?php

/**
* Send the input entered into the direct input form to the parser and redirect to the 
* results page.
*/

require_once "php/misc.php";
require_once "php/header.php";
require_once "php/footer.php";
require_once "php/validation.php";
require_once "php/files.php";

if (! array_key_exists("input", $_POST) )
    redirect("/direct_input");

$set = create_set("");

$input = $_POST["input"];

$encoded_input = base64_encode($input);

// send it to the parser
$parsed = -1;
$f = finfo_open();
$mime = finfo_buffer($f, $input, FILEINFO_MIME_TYPE);
if ($mime == "text/html" || $mime == "text/plain")
    $parsed = validate(array(), "", $encoded_input );

$encoded_parsed = json_encode($parsed);

// put it in the db
$file = add_file($set, "Direct Input", $encoded_input, $encoded_parsed);

redirect("/file?file=$file");

?>
