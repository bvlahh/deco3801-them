#coding=utf-8
import html5lib
import sys
from html5lib import treewalkers
from html5lib import treebuilders

parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("etree"))

files = ""
filename = ""

fragment = """<head>"""

if len(sys.argv) == 2:
    fi = open(sys.argv[1], 'r')
    fragment = fi.read().decode("utf-8")
else:
    fragment = fragment.decode("utf-8")

minidom_document = parser.parse(fragment, files=files, filename=filename)
#<html><html><body><body></body></body></html></html>
#<html><html><head><head></head></head></html></html>
#<html><html><footer><footer></footer></footer></html></html>
#<html><html><body><footer></footer></body><footer><footer></footer></footer></html></html>
#<html><html><body><footer></footer></body><footer><footer></footer></footer></html></html>
#<html><html><body><html></html><body></html></html>
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
