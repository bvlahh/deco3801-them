<?php

function draw_header($title, $selected_tab=0) {
    
    print <<<END

<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
    <head>
		<title>$title</title>
		<link rel="stylesheet" type="text/css" href="/style.css" />
    </head>
	
	<body>
		
		<div class="topbox">
            
            <span class="topbox_top">THEM</span>
            <span class="topbox_bottom">Typed HTML5 Evaluation Machine</span>
            
            <!--
            <a href="/">
            </a>
            -->
            
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
