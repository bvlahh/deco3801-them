<?php

require_once "php/misc.php";
require_once "php/header.php";
require_once "php/footer.php";
require_once "php/files.php";
require_once "php/errors.php";
require_once "php/errorbar.php";

if (! array_key_exists("set", $_GET) )
    redirect("/");

$set = $_GET["set"];

$set = get_set($set);

if ( count($set) < 2 )
    redirect("/show_file?file=" . $set[0]["id"]);

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

function draw_file($file) {
    
    $filename = $file["filename"];
    
    $filename = preg_replace("/.*\\//", "", $filename);
    
    $fid = $file["id"];
    
    print <<<END
        <a class="files_file" href="/show_file?file=${fid}">
            <img src="/images/white_file.png" alt="" />
            <span>
                ${filename}
            </span>
        </a>
END;
    
}

function draw_folder($folder_name, $folder) {
    
    $escaped_folder_name = htmlspecialchars($folder_name);
    
    print <<<END
        <div class="files_folder">
            <div class="files_folder_title">
                ${escaped_folder_name}
            </div>
            <div class="files_folder_contents">
                <div>
END;
    
    foreach ( $folder["folders"] as $subfolder_name => $subfolder)
        draw_folder($subfolder_name, $subfolder);
    
    print <<<END
            </div>
            <div class="cb"></div>
            <div>
END;
    
    foreach ( $folder["files"] as $display_name => $file)
        draw_file($file);
    
    print <<<END
                </div>
                <div class="cb"></div>
            </div>
        </div>
END;
    
}

draw_header("THEM prototype - Uploaded Files");

// Uploaded Files or Uploaded Zip if the files[] != []
draw_folder("Uploaded Files", $filetree);

draw_footer();

?>
