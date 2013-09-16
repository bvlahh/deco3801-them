from __future__ import absolute_import, division, unicode_literals

#from . import support
import unittest, html5lib
from html5lib import treebuilders

class TestSyntax(unittest.TestCase):
	"""
	Provides a number of test cases to test the syntax used
	in the document.
	"""

	def setUp(self):
		self.parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("etree"))

	def test_malformed_tag_name(self):
		"""
		Test that the tag name isn't an invalid symbol.

		Input:
		A HTML fragment containing a tag with an invalid tag name.

		Expected Results:
		An error should be thrown reporting an invalid tag name.
		"""

		inputFragmentEmptyName = "<html>< ></body>"
		inputFragmentQuestionMark = "<html><?></body>"
		inputFragmentRightBracket = "<html><></html>"

		self.parser.parse(inputFragmentEmptyName)

		self.assertIn(((6, 6), u'expected-tag-name', {u'data': u' '}),
			self.parser.errors, "Failed to report invalid tag name. Get ")

		self.parser.reset()
		self.parser.parse(inputFragmentQuestionMark)

		self.assertIn(((6, 6), u'expected-tag-name-but-got-question-mark', {}),
			self.parser.errors, "Failed to report valid tag name. Got question mark instead.")

		self.parser.reset()
		self.parser.parse(inputFragmentRightBracket)

		self.assertIn(((6, 7), u'expected-tag-name-but-got-right-bracket', {}),
			self.parser.errors, "Failed to report valid tag name. Got question mark instead.")

	def test_self_closing_end_tag(self):
		"""
		Test that a closing tag with a misplaced forwardslash  
		raises an error.

		Input:
		A HTML fragment containing a closing tag with a misplaced forwardslash.

		Expected Results:
		An error should be thrown reporting an invalid tag name.
		"""

		inputFragment = "<html><a></a /></html>"

		self.parser.parse(inputFragment)

		self.assertIn(((9, 14), u'self-closing-flag-on-end-tag', {}),
			self.parser.errors, "Failed to report misplaced forwardslash in closing tag.")

	def test_invalid_self_closing_tag(self):
		"""
		Test that the use of a self closing tag for a tag
		which isn't considered a self closing tag returns
		an error.

		Input:
		A HTML fragment containing a start tag with a trailing forwardslash 
		(self-closing) for a tag type which isn't a self closing tag.

		Expected Results:
		An error should be thrown reporting the given tag type isn't a self-closing
		tag.
		"""

		inputFragment = "<html><a /></html>"

		self.parser.parse(inputFragment)

		self.assertIn(((6, 10), u'non-void-element-with-trailing-solidus', {u'name': u'a'}),
			self.parser.errors, "Failed to report invalid self-closing tag.")

	def test_attributes_in_end_tag(self):
		"""
		Test that attributes occuring in a closing tag are 
		reported as an error.

		Input:
		A HTML fragment containing a closing tag which contains
		at least one attribute.

		Expected Results:
		An error should be thrown reporting that the closing tag shouldn't contain
		attributes.
		"""

		inputFragment = '<html><a></a src="blah"></html>'

		self.parser.parse(inputFragment)

		self.assertIn(((9, 23), u'attributes-in-end-tag', {}),
			self.parser.errors, "Failed to report attributes in closing tag.")

if __name__ == '__main__':
	unittest.main()
