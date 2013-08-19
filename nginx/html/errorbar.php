<?php

function draw_error_bar($t1, $t2, $t3) {
	
	$total = $t1 + $t2 + $t3;
	
	$total_wide = 500;
	
	$t1_wide = ($t1/$total) * $total_wide;
	$t2_wide = ($t2/$total) * $total_wide;
	$t3_wide = ($t3/$total) * $total_wide;
	
	print <<<END
		
		<div style="width: ${total_wide}px; border: 1px solid #DDDDDD;">
			
			<div style="float: left; width: ${t1_wide}px; background-color: #7fff7f; text-align: center; padding: 10px 0px 10px 0px;">$t1</div>
			
			<div style="float: left; width: ${t2_wide}px; background-color: #ffff7f; text-align: center; padding: 10px 0px 10px 0px;">$t2</div>
			
			<div style="float: left; width: ${t3_wide}px; background-color: #ff7f7f; text-align: center; padding: 10px 0px 10px 0px;">$t3</div>
			
			<div class="cb"></div>
			
		</div>
		
END;
	
}

?>