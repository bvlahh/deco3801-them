<?php

require_once "php/misc.php";
require_once "php/header.php";
require_once "php/footer.php";
require_once "php/files.php";
require_once "php/errors.php";
require_once "php/errorbar.php";
require_once "php/filetree.php";

if (! array_key_exists("set", $_GET) )
    redirect("/");

$set = $_GET["set"];

$set = get_set($set);

if ( count($set) < 2 ) {
    
    if ( json_decode($set[0]["cached_parse"]) == -1 )
        redirect("/");
    else
        redirect("/file?file=" . $set[0]["id"]);
    
}

$filetree = array(
    "files" => array(),
    "folders" => array()
);

foreach ( $set as $file ) {
    
    $filename = $file["filename"];
    
    $filepath = explode("/", $filename);
    
    // start at the root
    $filetreeparent = &$filetree;
    
    // loop over the folders leading to the file
    for ($f=0; $f<(count($filepath) - 1); $f++) {
        
        // if the folder doesn't exist in the tree, make it.
        if (! array_key_exists($filepath[$f], $filetreeparent["folders"]) )
            $filetreeparent["folders"][$filepath[$f]] = array(
                "files" => array(),
                "folders" => array()
            );
        
        // set that as the current parent
        $filetreeparent = &$filetreeparent["folders"][$filepath[$f]];
        
    }
    
    // if it's a file put it in the files array
    if ( $filepath[ count($filepath) - 1 ] != "" )
        $filetreeparent["files"][ $filepath[count($filepath) - 1] ] = $file;
    
}

draw_header("THEM - Uploaded Files");

print <<<END

<div class="legendbox2">

<div>
    <div style="width: 10px; height: 10px; border: 1px solid #DDDDDD; background-color: #ff6f6f; float: left; margin: 5px;"></div>
    <div style="float: left;">
        Syntax / Semantics
    </div>

    <div style="width: 10px; height: 10px; border: 1px solid #DDDDDD; background-color: #ffbb66; float: left; margin: 5px;"></div>
    <div style="float: left;">
        Deprecated Elements
    </div>

    <div style="width: 10px; height: 10px; border: 1px solid #DDDDDD; background-color: #6f6fff; float: left; margin: 5px;"></div>
    <div style="float: left;">
        Accessibility
    </div>

    <div style="width: 10px; height: 10px; border: 1px solid #DDDDDD; background-color: #ffff6f; float: left; margin: 5px;"></div>
    <div style="float: left;">
        Poor Practice / Other Miscellenous Issues
    </div>
    <div class="cb"></div>
</div>

</div>

END;

draw_file_tree($filetree);

draw_footer();

?>
