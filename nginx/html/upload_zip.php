<?php

require_once "header.php";
require_once "footer.php";

draw_header("Brendans prototype", 3);

print <<<END
    
    <div class="datainput">
        Upload ZIP
        <form action="do_upload_zip" method="post" enctype="multipart/form-data" >
            <input type="file" name="archive" />
            <div>
                <input type="submit" value="Validate" class="button" />
            </div>
        </form>
    </div>
    
END;

draw_footer();

?>
