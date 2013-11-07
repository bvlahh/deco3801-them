<?php

/**
* Header template.
*
* @param string $title The title of the page.
*/
function draw_header($title) {
    
    print <<<END
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
    <head>
		
        <title>$title</title>
        
        <link rel="icon" type="image/png" href="/images/32px-HTML5_Badge.svg.png" />
		<link rel="stylesheet" type="text/css" href="/style/style.css" />
        <link rel="stylesheet" type="text/css" href="http://fonts.googleapis.com/css?family=Sintony">
    </head>
	
	<body>
		
		<div class="topbox">
            
            <span class="topbox_top"><a href="/">THEM</a></span>
            <span class="topbox_bottom">Typed HTML5 Evaluation Machine</span>
            
        </div>
		
		<div class="contentbox">
			
			<div class="sidebar">
				
				<div class="sidebuttons">
					
                    <a href="/direct_input" >
                        Direct Input
                    </a>
                    
                    <a href="/upload_file" >
                        Upload File
                    </a>
                    
                    <a href="/upload_zip" >
                        Upload ZIP
                    </a>
                    
                    <a href="/help" >
                        Help
                    </a>
                    
				</div>
				
			</div>
			
			<div class="contentpane" id="contentpane">
				
END;
    
}

?>
