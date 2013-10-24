<?php

/**
* Processes a zip file, creating an array containing the file structure of the files contained 
* within and parsing each of the HTML files found. Creates a list of links to the results pages 
* for each of the HTML files.
*/

require_once "php/misc.php";
require_once "php/header.php";
require_once "php/footer.php";
require_once "php/validation.php";
require_once "php/files.php";

if (! array_key_exists("archive", $_FILES) )
    redirect("/upload_zip?upload_failed");

$filename = $_FILES["archive"]["name"];
$file = $_FILES["archive"]["tmp_name"];

$zip = new ZipArchive();

// Attempt to open the zip file.
if (! $zip->open($file) )
    redirect("/upload_zip?upload_failed");

/**
* Generate an array of filenames contained within the zip.
* Used by the parser to check for valid file referencing.
*/

$filenames = array();
for ($i=0; $i<($zip->numFiles);$i++)
	$filenames[] = $zip->getNameIndex($i);

$set = create_set("");

/**
* Parses each of the HTML files within the zip, generating a link to the results
* page for each HTML document.
*/

for ($i=0; $i<($zip->numFiles); $i++) {
    
    $file_name = $zip->getNameIndex($i);
    
    $file_data = $zip->getFromIndex($i);
    
    $encoded_input = base64_encode($file_data);
    
    
    $parsed = validate($filenames, $file_name, $encoded_input);
    
    $encoded_parsed = json_encode($parsed);
    
    add_file($set, $file_name, $encoded_input, $encoded_parsed);
    
}

$zip->close();

redirect("/set?set=$set");

?>
