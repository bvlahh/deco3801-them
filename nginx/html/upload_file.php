<?php

require_once "header.php";
require_once "footer.php";

draw_header("THEM prototype - Upload File", 2);

print <<<END
    
    <div class="datainput">
        Upload HTML File
        <form action="do_upload_file" method="post" enctype="multipart/form-data" >
            <div id="files">
                <input type="file" name="file1" onclick="addFileUpload();" />
            </div>
            <div>
                <input type="submit" value="Validate" class="button" />
            </div>
        </form>
    </div>
	<script type="text/javascript">
	var divSection = document.getElementById("files"),
	    fileCount = 2;

	function addFileUpload() {
	    divSection.innerHTML += '<br /><input type="file" name="file'+ fileCount + '" onclick="addFileUpload();" />'
	    fileCount++;
    }
    
END;

draw_footer();

?>
