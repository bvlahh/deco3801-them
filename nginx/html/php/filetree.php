<?php

function draw_file_tree($tree) {
    
    print <<<END
        
        <div class="files_collection">
        
END;
    
    draw_folder("Uploaded Files", $tree);
    
    print <<<END
        
        </div>
        
END;
    
}

function draw_file($file) {
    
    $filename = $file["filename"];
    
    $filename = preg_replace("/.*\\//", "", $filename);
    
    $fid = $file["id"];
    
    $parsed_errors = json_decode($file["cached_parse"]);
    
    $error_access = 0;
    $error_semantics = 0;
    $error_deprecated = 0;
    $error_misc = 0;
    
    // count the errors
    foreach ( $parsed_errors as $parsed_error ) {
        
        $err_no = $parsed_error[0];
        
        $err_colour = Errors::errorColour($err_no);
        
        if ($err_colour == "#ffff7f") {
            /* poor practice */
            $error_misc++;
        } else if ($err_colour == "#7f7fff") {
            /* accessibiity */
            $error_access++;
        } else if ($err_colour == "#ffbb77") {
            /* deprecated tags */
            $error_deprecated++;
        } else {
            /* syntax, semantics */
            $error_semantics++;
        }
        
    }
    
    print <<<END
        <a class="files_file" href="/file?file=${fid}">
            <img src="/images/file.png" alt="" />
            <span>
END;
    
    if ( count($parsed_errors) == 0 )
        draw_error_bar(0, 0, 0, 0, 1, 48, 5);
    else
        draw_error_bar($error_access, $error_semantics, $error_deprecated, $error_misc, 0, 48, 5);
    
    print <<<END
            </span>
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
                <img src="/images/folder.png" style="height: 18px; width: 24px; margin-right: 5px;" alt="" />${escaped_folder_name}
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

?>
