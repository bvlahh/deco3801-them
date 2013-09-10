<?php

// The help page. Currently a test bed for the error bars.

require_once "php/header.php";
require_once "php/footer.php";
require_once "php/errorbar.php";

draw_header("THEM prototype - Help", 4);

print <<<END
    
    Help Section
    
END;

print <<<END
    
    Understanding the Error Bars:<br />

    Here you can see an error bar, with corresponding error numbers included.<br />
    
END;

draw_error_bar(1, 6, 3, 2, 0, 500, 20, true);

print <<<END

	<br />This bar shows the relative ratios of each error in a document. In order, this highlights:<br /><br />

	Accessibility, Structure / Syntax, Deprecated Elements and General Poor Practice / Other Misc. Errors<br /><br />

	If the file has no errors, a green bar will display instead.<br />

END;

draw_error_bar(0, 0, 0, 0, 1, 500, 10);

print <<<END

	In some instances, you will see short forms of lines underneath files you upload via the <a href="/upload_zip">Upload Zip</a> page.

END;

draw_error_bar(1, 1, 1, 1, 1, 50, 10);

print <<<END

	These bars will also display on the multiple file upload page, next to the files they represent.

END;

draw_footer();

?>
