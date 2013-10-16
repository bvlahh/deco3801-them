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
<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">
<html>
	<head>

		<title>Vintage Rides</title>
		<link rel="stylesheet" type="text/css" href="css/style.css" />
		<link rel="stylesheet" type="text/css" href="css/contact.css" />
		<link rel="stylesheet" type="text/css" href="css/navigation.css">
		<script type="text/Javascript" src="js/contact.js"></script>
	</head>


	<body>
	<div id="titleBar">
			<div id="logoContainer">
			<div id="logo">Vintage Rides</div>
		</div>
		<div id="menuContainer">
		<div id="menu">
			<ul>
				<li><a href="index.html">Home</a></li>
				<li><a href="specialOffers.html">Special Offers</a></li> 
				<li><a href="cars.html">Cars</a></li> 
				<li><a href="about.html">About</a></li>
				<li><a href="contact.html">Contact</a></li>  
			</ul>
		</div>	
		</div>
		</div>
	
	<div class="wrapper">

				
		<div id="contact-area" onsubmit="return ValidateForm();">
		
		<p>Please do not hesitate to contact us for any further information.</p>
			<form class="contactForm" name="ContactForm" action="#" method="post" onsubmit="return ValidateForm();">
				<div id="fname"></div>
				<label for="firstName">First Name</label>
				<input type="text" class="input" name="firstName" id="fname">
				
				<br><br><div id="error1"></div>
				<label for="lname">Last Name</label>
				<input type="text" class="input" name="lastName" id="lname">
				
				<br><br><div id="email"></div>
				<label for="email">Email</label>
				<input type="text" class="inpute" name="email" id="email">
				
				<br><br><div id="phone"></div>
				<label for="phone">Phone</label>
				<input type="text" class="inputp" name="phone" id="phone">
				
				<br><br><div id="message"></div>
				<label for="Message">Message</label><br><br>
				<textarea name="Message" rows="20" cols="55" id="Message"></textarea>

				<br><br><br><input type="submit" value="Submit" class="submit">
				
				<div class="success" style="display: none;">
							<p>Booking successfully processed!</p>
							</div>
			
				
			</form>
			
			<div class="email">
			<div class="text">Email <br> johnfarnsworth@vintagerides.com</div>
			</div>
			
			<br><br><div class="phone">
			<div class="text">Phone <br> 5447 5528</div>
			</div>
			
	
		
		</div>
	

	
	

	

	</body>
</html>
"""


parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("etree"))

files = ""
filename = ""

blah = """<!DOCTYPE html><html><head><title></head></title><body></body></html>"""

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
fragment = error.decode("utf-8")

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

walker = treewalkers.getTreeWalker("etree")
stream = walker(minidom_document)

print '---------------------'

print fragment

print '---------------------'

for error in parser.errors:
	print error

print '---------------------'

print parser.parseErrors()

print '---------------------'

#for item in stream:
	#print item
