<?php

/**
* Input page for zip file uploads.
*/

require_once "php/header.php";
require_once "php/footer.php";

$errormessage = "";

if ( array_key_exists("upload_failed", $_GET) )
    $errormessage = <<<END
        <div style="background-color: #FFDDDD; color: #000000; border: 1px solid #DDDDDD; text-align: center; padding: 15px;">
            Upload Failed
        </div>
END;

draw_header("THEM - Upload ZIP");

print <<<END
    $errormessage
    <div style="padding-left: 50px; padding-top: 20px;">
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
    </div>
END;

draw_footer();

?>
