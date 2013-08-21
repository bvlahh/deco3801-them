<?php

function draw_error_bar($t1, $t2, $t3, $t4, $total_wide, $total_height) {
    
    $total = $t1 + $t2 + $t3 + $t4;
    
    $t1_wide = ($t1/$total) * $total_wide;
    $t2_wide = ($t2/$total) * $total_wide;
    $t3_wide = ($t3/$total) * $total_wide;
    $t4_wide = ($t4/$total) * $total_wide;
    
    print <<<END
        <div style="width: ${total_wide}px; border: 1px solid #DDDDDD;">
END;
    
    if ($t1 != 0)
        print <<<END
            <div style="float: left; width: ${t1_wide}px; background-color: #7f7fff; text-align: center; padding: 10px 0px 10px 0px;">$t1</div>
END;
    
    if ($t2 != 0)
        print <<<END
            <div style="float: left; width: ${t2_wide}px; background-color: #ff7fff; text-align: center; padding: 10px 0px 10px 0px;">$t2</div>
END;
    
    if ($t3 != 0)
        print <<<END
            <div style="float: left; width: ${t3_wide}px; background-color: #ff7f7f; text-align: center; padding: 10px 0px 10px 0px;">$t3</div>
END;
    
    if ($t4 != 0)
        print <<<END
            <div style="float: left; width: ${t4_wide}px; background-color: #ffff7f; text-align: center; padding: 10px 0px 10px 0px;">$t4</div>
END;
    
    print <<<END
            <div class="cb"></div>
        </div>
END;
    
}

?>
