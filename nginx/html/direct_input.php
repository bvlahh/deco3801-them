<?php

require_once "header.php";
require_once "footer.php";

draw_header("THEM prototype - Direct Input", 1);

print <<<END
    
    <div class="datainput">
        Direct Input
        <form action="do_direct_input" method="post">
            <textarea name="input"></textarea>
            <div>
                <input type="submit" value="Validate" class="button" />
            </div>
        </form>
    </div>
    
END;

draw_footer();

?>
