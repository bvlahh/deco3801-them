<?php

require_once "header.php";
require_once "footer.php";

draw_header("THEM prototype", 0);

print <<<END
    
    <div class="startbuttons">
        
        <div>
            Welcome to THEM
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
