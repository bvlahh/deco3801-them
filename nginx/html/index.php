<?php

require_once "php/header.php";
require_once "php/footer.php";

draw_header("THEM prototype", 0);

print <<<END
    
    <div style="width: 550px">
        
        <div class="indextitle">
            Welcome to The HTML5 Evaluation Machine
        </div>

        <div style="padding: 10px;">
        
        This web application allows you to directly input or upload HTML files and entire websites. These files are evaluated for their adherance to best style practices in four major categories:<br /><br />
        
        <div style="padding-left: 10px">Syntax / Semantics<br />
        Deprecated Elements<br />
        Accessibility<br />
        Poor Practice / Other Miscellenous Issues.<br /><br /></div>

        Start uploading now by clicking on <a href="/direct_input">Direct Input</a>, <a href="/upload_file">Upload File</a> or <a href="/upload_zip">Upload Zip</a> in the sidebar.<br \><br \>

        For more information on how everything works, check out the <a href="/help">help page</a>!
        
        </div>
        
        <div class="cb"></div>
        
    </div>
    
END;

draw_footer();

?>
