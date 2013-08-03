<?php

require_once "header.php";
require_once "footer.php";

draw_header("Brendans prototype", 1);

print <<<END
    
    <div class="datainput">
        Direct Input
        <form action="" method="">
            <textarea name=""></textarea>
            <div>
                <input type="submit" value="Validate" class="button" />
            </div>
        </form>
    </div>
    
END;

draw_footer();

?>
