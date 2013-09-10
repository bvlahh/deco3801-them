<?php

/**
* Send one or more HTML files to the parser, generating a list of links to the
* results page for each of the files parsed.
*/

require_once "php/misc.php";
require_once "php/header.php";
require_once "php/footer.php";
require_once "php/validation.php";
require_once "php/files.php";

$uploaded_files = array();
$f = 0;

while ( array_key_exists("file$f", $_FILES) ) {
    
    if ($_FILES["file$f"] != "")
        $uploaded_files[] = $_FILES["file$f"];
    
    $f++;
    
}

$num_files = count($uploaded_files);

if ( $num_files == 0 )
    redirect("/upload_file");

$set = create_set("");

/**
* Parse each of the uploaded files and generate a link to the results page
* for each file.
*/

foreach ($uploaded_files as $uploaded_file) {
    
    $file_name = $uploaded_file["name"];
    $tmp_file = $uploaded_file["tmp_name"];
    
    $file_data = file_get_contents($tmp_file);
    $encoded_input = base64_encode($file_data);
    
    $parsed = validate(array(), $file_name, $encoded_input);
    
    $encoded_parsed = json_encode($parsed);
    
    add_file($set, $file_name, $encoded_input, $encoded_parsed);
    
}

redirect("/show_set?set=$set");

?>
