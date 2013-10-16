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
    
    function messagebox(data) {
        
        var errors = JSON.parse(data);
        
        var message = "";
        
        for ( var i=0; i<errors.length; i++ )
            message += "<div class=\"error_message\">" + err_message(errors[i]) + "</div>";
        
        set_message(message);
        
    }
    
    function err_message(number) {
    
END;

foreach ( Errors::$error_strings as $err_number => $err_message ) {
    
    $escaped_message = htmlspecialchars($err_message);
    
    print <<<END
        
        if (number == $err_number)
            return "$escaped_message";
        
END;

}

print <<<END
    
    }
    
END;

?>
