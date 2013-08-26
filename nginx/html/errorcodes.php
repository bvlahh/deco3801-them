<?php

function error_string($error_number) {
    
    $error_strings = array(
        
        1 => "missing doctype",
        
    );
    
    return $error_strings[$error_number];
    
}

?>
