#coding=utf-8
import html5lib
from html5lib import treewalkers
from html5lib import treebuilders

parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("etree"))

blah = """<html><head></head><body><footer><big></big></footer></body></html>"""

fragment = blah.decode("utf-8")

minidom_document = parser.parse(fragment)
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
