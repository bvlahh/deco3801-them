<?php

/**
* Header template.
*
* @param string $title The title of the page.
* @param bool $show_legend Show the legend in the sidebar?
*/
function draw_header($title, $show_legend=false) {
    
    $legend = "";
    
    if ($show_legend)
        $legend = <<<END
            <div style="padding: 5px; border: 1px solid #DDDDDD; background-color: #EEEEEE; font-size: 90%; margin: 10px;">
            
            <div>
                <div style="width: 10px; height: 10px; border: 1px solid #DDDDDD; background-color: #ff6f6f; float: left; margin: 5px;"></div>
                <div style="float: left;">
                    Syntax
                </div>
                <div class="cb"></div>
            </div>
            
            <div>
                <div style="width: 10px; height: 10px; border: 1px solid #DDDDDD; background-color: #ffbb66; float: left; margin: 5px;"></div>
                <div style="float: left;">
                    Deprecated
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
                    Best Practice
                </div>
                <div class="cb"></div>
            </div>
            
        </div>
END;
    
    print <<<END
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN"
"http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="en" lang="en">
    <head>

        <title>$title</title>

        <link rel="stylesheet" type="text/css" href="http://fonts.googleapis.com/css?family=Sintony" />

        <link rel="icon" type="image/png" href="/images/32px-HTML5_Badge.svg.png" />
		<link rel="stylesheet" type="text/css" href="/style/style.css" />

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

                    $legend

				</div>
				
			</div>
			
			<div class="contentpane" id="contentpane">
				
END;
    
}

?>
