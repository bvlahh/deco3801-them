<?php

/**
* Footer template.
*/
function draw_footer() {
    
    /*
        
        http://www.w3.org/html/logo/
        
        http://www.w3.org/html/logo/downloads/HTML5_Logo.svg
        http://www.w3.org/html/logo/downloads/HTML5_Badge.svg
        http://www.w3.org/html/logo/downloads/HTML5_1Color_Black.svg
        http://www.w3.org/html/logo/downloads/HTML5_1Color_White.svg
        
        http://www.w3.org/html/logo/downloads/HTML5_sticker.svg
        
        http://www.w3.org/TR/html5-author/
        http://www.w3.org/TR/html5/
        
    */
    
    print <<<END
            
			</div>
			
			<div class="cb"></div>
			
		</div>
        
		<div class="footer">
            <div class="footer_html5">
                <a href="http://www.w3.org/TR/html5-author/">
                    <img src="/images/HTML5_Badge.svg" alt="HTML5 Logo"/>
                </a>
            </div>
			<div class="footer_navigation">
                <span>Navigation</span>
                <a href="/">
                    Home
                </a>
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
            <div class="footer_about">
                <div class="footer_about_title">
                    About
                </div>
                <div class="footer_about_body">
                    THEM was developed in response to the tolerant nature of the HTML5 specification. Its primary aim is an educational tool for students learning web design. Because of this purpose it is built to validate for best practice which exceeds standards compliance.
                </div>
            </div>
            <div class="cb"></div>
		</div>
		
	</body>
	
</html>

END;
    
}

?>
