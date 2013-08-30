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

?>
