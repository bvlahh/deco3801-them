<?php

require_once "php/misc.php";
require_once "php/header.php";
require_once "php/footer.php";
require_once "php/rpc_client.php";
require_once "php/errorbar.php";

if (! array_key_exists("input", $_POST) )
    redirect("/direct_input");

$set = create_set();

$input = $_POST["input"];

$encoded_input = base64_encode($input);

// send it to the parser
$parsed = rpc_validate(array(), $encoded_input );

// put it in the db
$row = array($set, "Direct Input", $encoded_input, $parsed);

$file = 0;

redirect("/show_file?file=$file");

?>
