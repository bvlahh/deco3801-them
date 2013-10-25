<?php

/**
* The direct input entry form.
*/

require_once "php/header.php";
require_once "php/footer.php";

draw_header("THEM - Direct Input");

print <<<END
    
    <div class="datainput">
        Direct Input
        <form action="do_direct_input" method="post">
            <div>
                <textarea name="input" rows="" cols=""></textarea>
            </div>
            <div>
                <input type="submit" value="Validate" class="button" />
            </div>
        </form>
    </div>
    
END;

draw_footer();

?>
