<?php

require_once "php/misc.php";
require_once "php/header.php";
require_once "php/footer.php";
require_once "php/validation.php";
require_once "php/files.php";

if (! array_key_exists("file", $_FILES) )
    redirect("/upload_file");

$uploaded_files = array();
$f = 0;

while ( array_key_exists("file$f", $_FILES) ) {
    
    $uploaded_files[] = $_FILES["file$f"];
    $f++;
    
}

draw_header("THEM prototype - Uploaded Files");

$num_files = count($uploaded_files);
$files = $num_files == 1 ? "file" : "files";

print <<<END
    
    <span style="font-weight: bold;">Uploaded Files</span><br />
    $num_files $files<br />
    <br />
    
END;

$set = create_set("");

foreach ($uploaded_files as $uploaded_file) {
    
    $file_name = $uploaded_file["name"];
    $tmp_file = $uploaded_file["tmp_name"];
    
    $file_data = file_get_contents($tmp_file);
    $encoded_input = base64_encode($file_data);
    
    $parsed = validate(array(), $encoded_input);
    
    $encoded_parsed = json_encode($parsed);
    
    $file = add_file($set, $file_name, $encoded_input, $encoded_parsed);
    
    print <<<END
        <a href="show_file?file=$file">$file_name</a><br />
END;
    
}

draw_footer();

?>
