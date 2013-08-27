<?php

require_once "errors.php";

header("Content-type: application/x-javascript");

print <<<END
    
    function set_message(text) {
        
        document.getElementById("infobox").innerHTML = text;
        
    }
    
    function messagebox(number) {
        
        
END;

foreach ( Errors::$error_strings as $err_number => $err_message ) {
    
    print <<<END
        
        if (number == $err_number)
            set_message("$err_message");
        
END;
    
}

print <<<END
    
    }
    
END;

?>
