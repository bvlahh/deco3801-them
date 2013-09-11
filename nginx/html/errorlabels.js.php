<?php

/**
* Displays the error message associated with the given error code in the "infobox"
* element when a user clicks an error span in the results page.
*/

require_once "php/errors.php";

header("Content-type: application/x-javascript");

print <<<END
    
    function set_message(text) {
        
        document.getElementById("infobox").innerHTML = text;
        
    }
    
    function messagebox(number) {
        
        
END;

foreach ( Errors::$error_strings as $err_number => $err_message ) {
    
    $escaped_message = htmlspecialchars($err_message);
    
    print <<<END
        
        if (number == $err_number)
            set_message("$escaped_message");
        
END;
    
}

print <<<END
    
    }
    
END;

?>
