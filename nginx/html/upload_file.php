<?php

require_once "header.php";
require_once "footer.php";

draw_header("THEM prototype - Upload File", 2);

print <<<END
    
    <div class="datainput">
        Upload HTML File
        <form action="do_upload_file" method="post" enctype="multipart/form-data" >
            <div id="files">
                <input type="file" name="file1" class="filepicker" />
            </div>
            <div>
                <div style="float: left;">
                    <button onclick="addFileUpload(); return false;" class="button">Add File</button>
                </div>
                <div style="float: right;">
                    <input type="submit" value="Validate" class="button" />
                </div>
                <div class="cb"></div>
            </div>
        </form>
    </div>
	
    <script type="text/javascript">
        
        var fileDiv = document.getElementById("files");
        var fileCount = 2;
        
        function addFileUpload() {
            
            fileDiv.innerHTML += '<input type="file" name="file'+ fileCount + '" class="filepicker" />';
            fileCount++;
            
        }
        
    </script>
    
END;

draw_footer();

?>
