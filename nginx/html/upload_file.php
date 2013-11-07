<?php

/**
* Input page for single and multiple HTML file uploads.
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

draw_header("THEM - Upload File");

print <<<END
    $errormessage
    <div style="padding-left: 50px; padding-top: 20px;">
        <div class="datainput">
            Upload HTML File
            <form action="do_upload_file" method="post" enctype="multipart/form-data" >
                <div id="files">
                    <input type="file" name="file[]" class="filepicker" multiple="multiple" />
                </div>
                <div>
                    <div style="float: left;">
                        <button type="button" onclick="addFileUpload(); return false;" class="button">Add File</button>
                    </div>
                    <div style="float: right;">
                        <input type="submit" value="Validate" class="button" />
                    </div>
                    <div class="cb"></div>
                </div>
            </form>
        </div>
	</div>
    
    <script type="text/javascript">
    //<![CDATA[
        
        var fileDiv = document.getElementById("files");
        
        function addFileUpload() {
            
            var newInput = document.createElement("input");
            
            newInput.setAttribute( "type", "file" );
            newInput.setAttribute( "name", "file[]" );
            newInput.setAttribute( "class", "filepicker" );
            newInput.setAttribute( "multiple", "multiple" );
            
            fileDiv.appendChild(newInput);
            
        }
        
    //]]>
    </script>
    
END;

draw_footer();

?>
