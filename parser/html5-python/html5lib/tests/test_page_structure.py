from __future__ import absolute_import, division, unicode_literals

from . import support

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

	def test_singular_tags(self):
		"""
		Test that the multiple-instance-singular-tag error is thrown
		for cases where more than one instance of a singular tag block is 
		present.

		Inputs: 
		Nested blocks of singular tags (html, body, head).
		eg. <html><html></html></html>

		Ouputs:
		All three test cases should report a multiple instance of both
		the start and closing tags for each of the three singular tags.
		"""
		multipleHTMLInstances = "<html><html></html></html>"
		multipleHeadInstances = "<html><head><head></head></head></html>"
		multipleBodyInstances = "<html><body><body></body></body></html>"

		self.parser.parse(multipleHTMLInstances)


		self.assertIn(((6, 11), u'multiple-instance-singular-tag', {u'name': u'html'}), 
			self.parser.errors, "Multiple instances of starting HTML tag not reported.")

		self.assertIn(((12, 18), u'incorrect-placement-html-end-tag', {u'name': u'html'}),
			self.parser.errors, "Multiple instances of closing HTML tag not reported.")

		self.parser.reset()
		self.parser.parse(multipleHeadInstances)

		self.assertIn(((12, 17), u'multiple-instance-singular-tag', {u'name': u'head'}), 
			self.parser.errors, "Multiple instances of starting HTML tag not reported.")

		self.assertIn(((25, 31), u'incorrect-placement-singular-end-tag', {u'name': u'head'}),
			self.parser.errors, "Multiple instances of closing head tag not reported.")

		self.parser.reset()
		self.parser.parse(multipleBodyInstances)

		self.assertIn(((12, 17), u'multiple-instance-singular-tag', {u'name': u'body'}), 
			self.parser.errors, "Multiple instances of starting HTML tag not reported.")

		self.assertIn(((25, 31), u'unexpected-end-tag-after-body', {u'name': u'body'}),
			self.parser.errors, "Multiple instances of closing body tag not reported.")

	def test_missing_doctype(self):
		"""
		Test that the expected-doctype-but-got-start-tag error is thrown
		for cases where no DOCTYPE is declared.

		Inputs:
		Nested blocks of singular tags (html, body, head), all of which
		are missing the DOCTYPE declaration.
		eg. <html><html></html></html>

		Output:
		All test cases should report a missing DOCTYPE declaration.
		"""
		multipleHTMLInstances = "<html><html></html></html>"
		multipleHeadInstances = "<head><head></head></head>"
		multipleBodyInstances = "<body><body></body></body>"

		self.parser.parse(multipleHTMLInstances)
		
		self.assertIn(((0, 5), u'expected-doctype-but-got-start-tag', {u'name': u'html'}),
			self.parser.errors, "Failed to report missing DOCTYPE declaration.")

		self.parser.reset()
		self.parser.parse(multipleHeadInstances)

		self.assertIn(((0, 5), u'expected-doctype-but-got-start-tag', {u'name': u'head'}),
			self.parser.errors, "Failed to report missing DOCTYPE declaration.")

		self.parser.reset()
		self.parser.parse(multipleBodyInstances)

		self.assertIn(((0, 5), u'expected-doctype-but-got-start-tag', {u'name': u'body'}),
			self.parser.errors, "Failed to report missing DOCTYPE declaration.")

	
	def test_closing_html(self):
		"""
		Test that a missing HTML closing tag is reported when none
		are present in the document.

		Input:
		Nested blocks of singular tags (head, body).

		Output:
		Report whether the the closing HTML tag is present.
		"""
		multipleHeadInstances = "<head><head></head></head>"
		multipleBodyInstances = "<body><body></body></body>"

		self.parser.parse(multipleHeadInstances);

		self.assertIn(((-1, -1), u'no-closing-html-tag', {}),
			self.parser.errors, "Failed to report missing closing HTML tag.")

		self.parser.reset()
		self.parser.parse(multipleBodyInstances)

		self.assertIn(((-1, -1), u'no-closing-html-tag', {}),
			self.parser.errors, "Failed to report missing closing HTML tag.")

	def test_misplaced_tags_before_head(self):
		"""
		Test that both start and closing tags occuring before the head
		section are reported as being misplaced.

		Input:
		A number of instances of start and closing tags being placed before
		the head section.

		Output:
		Report whether or not the tags preceding the head section are reported
		as being misplaced.
		"""
		misplacedHeadTags = "<html><body></body><head></head></html>"
		misplacedLinkTags = "<html><a></a><head></head></html>"

		self.parser.parse(misplacedHeadTags)

		self.assertIn(((6, 11), u'incorrect-start-tag-placement-before-head', {u'name': u'body'}),
			self.parser.errors, "Failed to report start body tag before head section.")

		self.assertIn(((12, 18), u'incorrect-end-tag-placement-before-head', {u'name': u'body'}),
			self.parser.errors, "Failed to report closing body tag before head section.")

		self.parser.reset()
		self.parser.parse(misplacedLinkTags)

		self.assertIn(((6, 8), u'incorrect-start-tag-placement-before-head', {u'name': u'a'}),
			self.parser.errors, "Failed to report start link (a) tag before head section.")

		self.assertIn(((9, 12), u'incorrect-end-tag-placement-before-head', {u'name': u'a'}),
			self.parser.errors, "Failed to report closing link (a) tag before head section.")

if __name__ == '__main__':
	unittest.main()
