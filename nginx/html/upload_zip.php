<?php

/**
* Input page for zip file uploads.
*/

require_once "php/header.php";
require_once "php/footer.php";

draw_header("THEM - Upload ZIP", 3);

print <<<END
    
    <div class="datainput">
        Upload ZIP
        <form action="do_upload_zip" method="post" enctype="multipart/form-data" >
            <div>
                <input type="file" name="archive" class="filepicker" />
            </div>
            <div>
                <input type="submit" value="Validate" class="button" />
            </div>
        </form>
    </div>
    
END;

draw_footer();

?>
