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
<!DOCTYPE>
<head>
<a>
</head>
"""
misplacedLinkTags = "<html><head><head>/head></head></html>"
tag = "<!DOCTYPE html><html><head></head><body><form><input></input></form></body></html>"

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
fragment = tag.decode("utf-8") #bigdoc.decode("utf-8")

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
