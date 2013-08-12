<?php

require_once "header.php";
require_once "footer.php";

draw_header("THEM prototype - Upload File", 2);

print <<<END
    
    <div class="datainput">
        Upload HTML File
        <form action="do_upload_file" method="post" enctype="multipart/form-data" >
            <input type="file" name="file" />
            <div>
                <input type="submit" value="Validate" class="button" />
            </div>
        </form>
    </div>
    
END;

draw_footer();

?>
