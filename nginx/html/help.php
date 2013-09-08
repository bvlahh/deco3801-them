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

draw_error_bar(1, 6, 3, 2, 0, 500, 10);

print <<<END

	<br />This bar shows the relative ratios of each error in a document. In order, this highlights:<br /><br />

	put the types here in order.<br />

	If the file has no errors, a green bar will display instead.<br />

END;

draw_error_bar(0, 0, 0, 0, 1, 500, 10);

print <<<END

	more text here.

END;

draw_error_bar(1, 1, 1, 1, 1, 250, 10);
draw_error_bar(1, 1, 1, 1, 1, 250, 10, true);

draw_footer();

?>
