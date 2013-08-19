<?php

function draw_error_bar($t1, $t2, $t3) {
	
	$total = $t1 + $t2 + $t3;
	
	$total_wide = 500;
	
	$t1_wide = ($t1/$total) * $total_wide;
	$t2_wide = ($t2/$total) * $total_wide;
	$t3_wide = ($t3/$total) * $total_wide;
	
	print <<<END
		
		<div style="width: ${total_wide}px; border: 1px solid #DDDDDD;">
			
			<div style="float: left; width: ${t1_wide}px; background-color: #CD2626; text-align: center;">$t1</div>
			
			<div style="float: left; width: ${t2_wide}px; background-color: #7171C6; text-align: center;">$t2</div>
			
			<div style="float: left; width: ${t3_wide}px; background-color: #FFD700; text-align: center;">$t3</div>
			
			<div class="cb"></div>
			
		</div>
		
END;
	
}

?>