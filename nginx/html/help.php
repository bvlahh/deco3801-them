<?php

// The help page. The page for the user to get the best information about the web app.

require_once "php/header.php";
require_once "php/footer.php";
require_once "php/errorbar.php";

draw_header("THEM - Help");

print <<<END
    
    <div>Help Section</div>
    
END;

print <<<END
    
    <iframe width="420" height="315" src="//www.youtube.com/embed/ZSZPTFxE29Q" frameborder="0" allowfullscreen></iframe>
    
END;

draw_footer();

?>
