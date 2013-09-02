<?php

/**
* Draws the error bar, with each error type taking up a fraction of the total defined width
* based on the number of errors of that type as a fraction of the total number of errors.
*
* @param int $blue          The number of "blue" errors.
* @param int $red           The number of "red" errors.
* @param int $orange        The number of "orange" errors.
* @param int $yellow        The number of "yellow" errors.
* @param int $green         The number of "green" errors.
* @param int $total_wide    The total width of the error bar object in pixels.
* @param int $total_height  The total height of the error bar object in pixels.
*
* NOTE: The error colours haven't yet been assigned a meaning (eg. structural error)
*/
function draw_error_bar($blue, $red, $orange, $yellow, $green, $total_wide, $total_height, $show_numbers = false) {
    
    $total = $blue + $red + $orange + $yellow + $green;
    
    $blue_wide = ($blue/$total) * $total_wide;
    $red_wide = ($red/$total) * $total_wide;
    $orange_wide = ($orange/$total) * $total_wide;
    $yellow_wide = ($yellow/$total) * $total_wide;
    $green_wide = ($green/$total) * $total_wide;
    
    if (! $show_numbers) {
        
        $blue = "";
        $red = "";
        $orange = "";
        $yellow = "";
        $green = "";
        
    } else {
        
        if ($blue == 0)
            $blue = "";
        
        if ($red == 0)
            $red = "";
        
        if ($orange == 0)
            $orange = "";
        
        if ($yellow == 0)
            $yellow = "";
        
        if ($green == 0)
            $green = "";
        //else
        //    $green = "YAY";
        
    }
    
    print <<<END
        <div style="width: ${total_wide}px; border: 1px solid #DDDDDD; margin: 10px;">
            <div style="float: left; width: ${blue_wide}px; background-color: #7f7fff; text-align: center; padding: 10px 0px 10px 0px;">${blue}</div>
            <div style="float: left; width: ${red_wide}px; background-color: #ff7f7f; text-align: center; padding: 10px 0px 10px 0px;">${red}</div>
            <div style="float: left; width: ${orange_wide}px; background-color: #ffbb77; text-align: center; padding: 10px 0px 10px 0px;">${orange}</div>
            <div style="float: left; width: ${yellow_wide}px; background-color: #ffff7f; text-align: center; padding: 10px 0px 10px 0px;">${yellow}</div>
            <div style="float: left; width: ${green_wide}px; background-color: #7fff7f; text-align: center; padding: 10px 0px 10px 0px;">${green}</div>
            <div class="cb"></div>
        </div>
END;
    
}

?>
