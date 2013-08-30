<?php

// The help page. Currently a test bed for the error bars.

require_once "php/header.php";
require_once "php/footer.php";
require_once "php/errorbar.php";

draw_header("THEM prototype - Help", 4);

print <<<END
    
    Help Section
    
END;

print <<<END
    
    <br />
    <br />
    
    Error Bars - Any size you want:
    
END;

draw_error_bar(1, 1, 1, 1, 1, 500, 10);
draw_error_bar(1, 1, 1, 1, 1, 500, 10, true);
draw_error_bar(1, 1, 1, 1, 1, 250, 10);
draw_error_bar(1, 1, 1, 1, 1, 250, 10, true);

draw_footer();

?>
