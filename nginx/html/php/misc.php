<?php

/**
* 404 error handler.
*/
function exit_404() {
    
    header("Status: 404 Not Found");
    exit();
    
}

/**
* Page redirect.
*/
function redirect($url) {
    
    header("Location: $url");
    exit();
    
}

/**
* Rearrange the uploaded files to be indexed more sensibly
* eg [name][0] to [0][name]
*/
function rearrange_files( $arr ){
    
    foreach( $arr as $key => $all ){
        foreach( $all as $i => $val ){
            $new[$i][$key] = $val;   
        }   
    }
    
    return $new;
    
}

?>
