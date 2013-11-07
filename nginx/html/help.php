<?php

// The help page. The page for the user to get the best information about the web app.

require_once "php/header.php";
require_once "php/footer.php";
require_once "php/errorbar.php";

draw_header("THEM - Help");

?>

    <div style="width: 1000px">

	    <div style="text-align: center; font-size: 150%; padding: 10px;">Help Section</div>

	    <div>
	    	<div style="padding: 10px; width: 520px; float: left;">

	    		<div style="font-size: 120%">Uploading Your Code</div>

	    		<div style="margin: 20px;">There are three main ways you can upload your code - either by <a href="direct_input" target="_blank">directly inputting</a> your code into a textbox (good for short snippets of code and personal testing), or <a href="upload_file" target="_blank">uploading files</a> you have stored on your computer. When adding files, you can select multiple files in the window, or use the Add File button provided. You can even upload your whole HTML 5 website <a href="upload_zip" target="_blank">as a zip</a>.</div>

	    		<div style="font-size: 120%">Understanding Outputs</div>

	    		<div style="margin: 20px;">After you've uploaded your code, you will be directed to one of two pages. If you've uploaded a single file, or used Direct Input, you'll be sent to the file page straight away. An example file page can be viewed <a name="Example" href="/file?file=-1" target="_blank">here</a>. It will open in a new window or tab, and you can use it to follow along with the next section of the workshop.</div>

			</div>

		    <div style="float: left; padding: 20px;"><iframe width="420" height="315" src="//www.youtube.com/embed/ZSZPTFxE29Q" frameborder="0" allowfullscreen></iframe></div>

            <div class="cb"></div>

        </div>

    <div>

        <div style="margin: 20px; width: 640px; margin: auto auto; background-color: #EEEEEE; border: 1px solid #DDDDDD;">

        <div style="padding-top: 10px; padding-left: 20px; color: #333333;">The error bar</div>

        <div style="padding: 10px 20px 20px 20px; width: 600px;">

        <?php draw_error_bar(3, 6, 4, 2, 0, 500, 10); ?>
    
        <div style="margin-top: 10px; margin-left: 150px;">

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

        </div>

    </div>

    <div style="width: 950px; margin: auto auto;">

        <div style="margin: 20px;">As the legend says, each colour refers to a different type of error. Structural and semantic errors are those that affect how your webpage is seen, while Accessibility errors are relevant to cover all web users, including the blind. Deprecated errors refer to tags that no longer perform as expected by all browsers, and will likely be phased out in the next web standard. The remaining errors are cases of Poor Practice which are less pertinent than the other errors but still important to achieve best practices.</div>

        <div style="margin: 20px;">The error bar shows the relative amounts of each error in your webpage. General errors that aren't tied to a specific section of the code are displayed at the top with its corresponding coloured square. Any part of the code that is itself erroneous is highlighted, and these highlighted tags can be clicked to learn more about that particular error. Try a couple out on the example to see how they work.</div>

        <div style="font-size: 120%">Uploaded Zips</div>

        <div style="margin: 20px;">Uploading a zip allows you to see a tree-like structure of your website. Any HTML files that are part of the upload can also be clicked to navigate to the file page we were just working with for that HTML. The parser also checks the links you've included in your files, e.g. tags that require a src or a href. If you don't have the specific link in your files, then it gives an error on the file page. On the file page, there is a handy Uploaded Files button that you can use to get back to the set you originally uploaded. Try it out with your own website!</div>

    </div>
    
    </div>

</div>

<?php

draw_footer();

?>
