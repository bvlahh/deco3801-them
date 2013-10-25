#coding=utf-8
import html5lib
from html5lib import treewalkers
from html5lib import treebuilders


error = """
<!DOCTYPE html>
<html><head><title>My First Evaluated Webpage</table></head>
<body><h2>I bet I can sneak in a lower header... or maybe not!</h2><h1>Look at the majesty of my multiple heading ones!!</h1><h1>Wait that's a bad thing</h1><frame>I can use frames, right?</frame><p>Dang, what about leaving a tag open, with a image <img src=""> and no alt text!</body></html>
"""

bigdoc = """
<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8" />

    <link rel="stylesheet" type="text/css" href="demo.css" />
    <link rel="stylesheet" href="http://ajax.googleapis.com/ajax/libs/jqueryui/1.7.2/themes/ui-darkness/jquery-ui.css" type="text/css" media="all" />
    <link rel="stylesheet" type="text/css" href="fancybox/jquery.fancybox-1.2.6.css" />

    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.3.2/jquery.min.js"></script>
    <script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jqueryui/1.7.2/jquery-ui.min.js"></script>
    <script type="text/javascript" src="fancybox/jquery.fancybox-1.2.6.pack.js"></script>

    <script type="text/javascript" src="script.js"></script>

    <script>

        var randLeft = 0;
        var randTop = 0;
        var randRot = 0;
        var apiKey = "jsk1qqntnrj7qbvf";
        var stageWidth=600; 
        var stageHeight=400;
        var newspaperTitles = []; 

        $(document).ready(function(){
            $("form#searchTrove").submit(function() {
                newspaperTitles = [];

                //get input values
                var searchTerm = $("#searchTerm").val().trim();
                searchTerm = searchTerm.replace(/ /g,"%20");
                var sortBy = $("#sortBy").val();

                //create searh query
                var url = "http://api.trove.nla.gov.au/result?key=" 
                + apiKey + "&encoding=json&zone=newspaper" 
                + "&sortby=" + sortBy
                + "&q=" + searchTerm + "&callback=?";

                //print JSON object
                console.log(url);

                //get the JSON information we need to display the images
                $.getJSON(url, function(data) {
                    $('#output').empty();
                    for (var i = 0; i < data.response.zone[0].records.article.length; i++) {
                        try{
                            newspaperTitles.push(data.response.zone[0].records.article[i].heading);
                        } catch(e){}
                    }

                    for (var i = 0; i < 20; i++) {
                        /*Generate random values for the position and rotation */
                        randLeft = Math.floor(Math.random() * stageWidth) + 1;
                        randTop = Math.floor(Math.random() * stageHeight) + 1;
                        randRot = Math.floor(Math.random() * 80) + 1 - 40;

                        /*Makes sure that it doesn't leave the boundaries*/
                        if (randTop>stageHeight-100 && randLeft>stageWidth-100){
                            randTop -=150;
                            randLeft -= 150;
                        }

                        //set position of the paper
                    //  document.getElementById('pic-' + i).innerHTML = newspaperTitles[i];
                        
                        //
                        document.getElementById('sp-' + i).innerHTML = newspaperTitles[i];
                        
                        document.getElementById('pic-' + i).style.top = randTop + 'px';
                        document.getElementById('pic-' + i).style.left = randLeft + 'px';
                    }
                });
            });
        });
    </script>

    </head>

    <body>

        <div class="troveSearch">
            <form action="#" id="searchTrove">
                <input id="searchTerm" type="text" />
                <select id="sortBy">
                    <option>dateasc</option>
                    <option>datedesc</option>
                    <option>relevance</option>
                </select>
                <button type="submit" id="searchbtn">Search</button>
            </form>
        </div>

        <div id="gallery">

            <script>

            for (var i = 0; i < 20; i++) {

                var newCollageItem = '<a z-index="-1" tabindex="1" rel="group" href="http://fancybox.net/" class="fancybox"><div id="pic-'+i+'" class="pic ui-draggable" tabindex="1"><span z-index="1" id="sp-'+i+'" style="colour:white;"></span></div></a>';

                $('#gallery').append(newCollageItem);
            }

            </script>

        </div>

    </body>
</html>
"""

parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("etree"))

files = ""
filename = ""

blah = """<html><head><title>ye</title></head><body><frame></frame></body></html>"""

table = """
<html><head></head><body>
<table border="1">
<tr>
<td>row 1, cell 1</td>
<td>row 1, cell 2</td>
</tr>
<tr>
<td>row 2, cell 1</td>
<td>row 2, cell 2</td>
</tr>
</table>
<footer></footer></body></html>
"""
fragment = bigdoc.decode("utf-8")

minidom_document = parser.parse(fragment, files=files, filename=filename)
# <html><html><body><body></body></body></html></html>
# <html><html><head><head></head></head></html></html>
# <html><html><footer><footer></footer></footer></html></html>
# <html><html><body><footer></footer></body><footer><footer></footer></footer></html></html>
# <html><html><body><footer></footer></body><footer><footer></footer></footer></html></html>
# <html><html><body><html></html><body></html></html>
#<html><html><head><html></html></head></html></html>
#<html><html><head><html></html></head><footer></footer></html></html>
#<html></head><head><body></head><body></body></html>

# Causes a number of undefined errors.
#<html><*body></body /></body></html>

def parseAgain():
    minidom_document = parser.parse(fragment, files=files, filename=filename)


walker = treewalkers.getTreeWalker("etree")
stream = walker(minidom_document)

print '---------------------'

#print fragment

print '---------------------'

for error in parser.errors:
	print error

print '---------------------'

print parser.parseErrors()

print '---------------------'

#for item in stream:
	#print item
