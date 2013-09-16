import html5lib
from html5lib import treewalkers
from html5lib import treebuilders

parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("etree"))

filename ="directory/current.html"
files = ['directory/', 'directory/directory2/','directory/directory2/image3.jpg', 'imagd.jpg']
#fragment = '<head></head><body></body></html>'
#fragment = '<html><a></a src="blah"></html>'
fragment = '<img src="../image.jpg"><img src="directory2/image2.jpg">'

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
