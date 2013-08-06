<?php

function exit_404() {
    
    header("Status: 404 Not Found");
    exit();
    
}

function redirect($url) {
    
    header("Location: $url");
    exit();
    
}

?>
