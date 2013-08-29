from __future__ import absolute_import, division, unicode_literals

#from . import support
import unittest, html5lib
from html5lib import treebuilders

class TestPageStructure(unittest.TestCase):
	"""
	Provides a number of test cases related to basic page structure 
	for html5 documents.

	Some examples include testing for correct page layout (html->head->body)
	and checking for multiple instances of tags that should only have one instance
	in a document.
	"""

	def setUp(self):
		self.parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("etree"))

	def test_singular_html(self):
		"""
		Test that a multiple-instance-singular-tag error is thrown
		for cases where more than one instance of the html tag is included.
		"""
		htmlSingleLine = "<html><html></html></html>"
		htmlMultiLine = "<html>\n<html>\n</html>\n</html>"
		htmlMultiInstance = "<html><html><html><html></html></html></html></html>"

		self.parser.parse(htmlSingleLine)

		self.assertIn(((6, 11), u'multiple-instance-singular-tag', {u'name': u'html'}), 
			self.parser.errors, "Multiple instances of html tag not reported (single line).")

		self.parser.reset()
		self.parser.parse(htmlMultiLine)

		self.assertIn(((2, 6), u'multiple-instance-singular-tag', {u'name': u'html'}), 
			self.parser.errors, "Multiple instances of html tag not reported (multi line).")

		self.parser.reset()
		self.parser.parse(htmlMultiInstance)

		self.assertIn(((1, 12), u'multiple-instance-singular-tag', {u'name': u'html'}), 
			self.parser.errors, "First repeated instance of html tag not reported (single line).")
		self.assertIn(((1, 18), u'multiple-instance-singular-tag', {u'name': u'html'}), 
			self.parser.errors, "Second instance of html tag not reported (single line).")
		self.assertIn(((1, 24), u'multiple-instance-singular-tag', {u'name': u'html'}), 
			self.parser.errors, "Third instance of html tag not reported (single line).")

	def test_singular_head(self):
		"""
		Test that a multiple-instance-singular-tag error is thrown
		for cases where more than one instance of the head tag is included.
		"""
		headSingleLine = "<head><head></head></head>"
		headMultiLine = "<head>\n<head>\n</head>\n</head>"
		headMultiInstance = "<head><head><head><head></head></head></head></head>"

		self.parser.parse(headSingleLine)

		self.assertIn(((1, 12), u'multiple-instance-singular-tag', {u'name': u'head'}), 
			self.parser.errors, "Multiple instances of head tag not reported (single line).")

		self.parser.reset()
		self.parser.parse(headMultiLine)

		self.assertIn(((2, 6), u'multiple-instance-singular-tag', {u'name': u'head'}), 
			self.parser.errors, "Multiple instances of head tag not reported (multi line).")

		self.parser.reset()
		self.parser.parse(headMultiInstance)

		self.assertIn(((1, 12), u'multiple-instance-singular-tag', {u'name': u'head'}), 
			self.parser.errors, "First repeated instance of head tag not reported (single line).")
		self.assertIn(((1, 18), u'multiple-instance-singular-tag', {u'name': u'head'}), 
			self.parser.errors, "Second instance of head tag not reported (single line).")
		self.assertIn(((1, 24), u'multiple-instance-singular-tag', {u'name': u'head'}), 
			self.parser.errors, "Third instance of head tag not reported (single line).")

	def test_singular_body(self):
		"""
		Test that a multiple-instance-singular-tag error is thrown
		for cases where more than one instance of the body tag is included.
		"""
		bodySingleLine = "<body><body></body></body>"
		bodyMultiLine = "<body>\n<body>\n</body>\n</body>"
		bodyMultiInstance = "<body><body><body><body></body></body></body></body>"

		self.parser.parse(bodySingleLine)

		self.assertIn(((1, 12), u'multiple-instance-singular-tag', {u'name': u'body'}), 
			self.parser.errors, "Multiple instances of body tag not reported (single line).")

		self.parser.reset()
		self.parser.parse(bodyMultiLine)

		self.assertIn(((2, 6), u'multiple-instance-singular-tag', {u'name': u'body'}), 
			self.parser.errors, "Multiple instances of body tag not reported (multi line).")

		self.parser.reset()
		self.parser.parse(bodyMultiInstance)

		self.assertIn(((1, 12), u'multiple-instance-singular-tag', {u'name': u'body'}), 
			self.parser.errors, "First repeated instance of body tag not reported (single line).")
		self.assertIn(((1, 18), u'multiple-instance-singular-tag', {u'name': u'body'}), 
			self.parser.errors, "Second instance of body tag not reported (single line).")
		self.assertIn(((1, 24), u'multiple-instance-singular-tag', {u'name': u'body'}), 
			self.parser.errors, "Third instance of body tag not reported (single line).")

if __name__ == '__main__':
	unittest.main()