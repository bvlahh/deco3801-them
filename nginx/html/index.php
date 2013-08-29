<?php

require_once "php/header.php";
require_once "php/footer.php";

draw_header("THEM prototype", 0);

print <<<END
    
    <div class="startbuttons">
        
        <div>
            Welcome to The HTML5 Evaluation Machine
        </div>
        
        <a href="/direct_input" >
            Direct Input
        </a>
        
        <a href="/upload_file" >
            Upload File
        </a>
        
        <br />
        
        <a href="/upload_zip" >
            Upload ZIP
        </a>
        
        <a href="/help" >
            Help
        </a>
        
        <div class="cb"></div>
        
    </div>
    
END;

draw_footer();

?>
