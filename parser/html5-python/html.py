import html5lib
from html5lib import treewalkers
from html5lib import treebuilders

parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("etree"))

minidom_document = parser.parse('<html><body><head><br></head><body><head></body></body></html>')
# <html><html><body><body></body></body></html></html>
# <html><html><head><head></head></head></html></html>
# <html><html><footer><footer></footer></footer></html></html>
# <html><html><body><footer></footer></body><footer><footer></footer></footer></html></html>
# <html><html><body><footer></footer></body><footer><footer></footer></footer></html></html>
# <html><html><body><html></html><body></html></html>
#<html><html><head><html></html></head></html></html>
#<html><html><head><html></html></head><footer></footer></html></html>
#<html></head><head><body></head><body></body></html>

walker = treewalkers.getTreeWalker("etree")
stream = walker(minidom_document)

for error in parser.errors:
	print error

print '---------------------'

print parser.parseErrors()

print '---------------------'
print minidom_document
print '---------------------'

#for item in stream:
	#print item
