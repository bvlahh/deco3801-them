<?php

require_once "php/header.php";
require_once "php/footer.php";

draw_header("THEM - Typed HTML5 Evaluation Machine");

print <<<END
    
    <div style="width: 1000px">
        
        <div style="text-align: center; font-size: 150%;">
            Welcome to The HTML5 Evaluation Machine
        </div>
        
        <div style="padding: 30px;">
            
            This web application allows you to directly input or upload HTML files and entire websites. These files are evaluated for their adherance to best style practices in four major categories:<br /><br />
            
            <div style="float: left; margin-left: 250px; padding: 15px; border: 1px solid #DDDDDD;">
                
                <div>
                    <div style="width: 10px; height: 10px; border: 1px solid #DDDDDD; background-color: #ff6f6f; float: left; margin: 5px;"></div>
                    <div style="float: left;">
                        Syntax / Semantics
                    </div>
                    <div class="cb"></div>
                </div>
                
                <div>
                    <div style="width: 10px; height: 10px; border: 1px solid #DDDDDD; background-color: #ffbb66; float: left; margin: 5px;"></div>
                    <div style="float: left;">
                        Deprecated Elements
                    </div>
                    <div class="cb"></div>
                </div>
                
                <div>
                    <div style="width: 10px; height: 10px; border: 1px solid #DDDDDD; background-color: #6f6fff; float: left; margin: 5px;"></div>
                    <div style="float: left;">
                        Accessibility
                    </div>
                    <div class="cb"></div>
                </div>
                
                <div>
                    <div style="width: 10px; height: 10px; border: 1px solid #DDDDDD; background-color: #ffff6f; float: left; margin: 5px;"></div>
                    <div style="float: left;">
                        Poor Practice / Other Miscellenous Issues
                    </div>
                    <div class="cb"></div>
                </div>
                
            </div>
            
            <div class="cb"></div>
                
            <div style="padding-top: 15px;">
                For more information on how everything works, check out the <a href="/help">Help Section</a>
            </div>
            
        </div>
        
    </div>
    
END;

draw_footer();

?>
