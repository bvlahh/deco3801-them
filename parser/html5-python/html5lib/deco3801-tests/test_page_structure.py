from __future__ import absolute_import, division, unicode_literals

#from . import support
import unittest, html5lib
from html5lib import treebuilders

class TestPageStructure(unittest.TestCase):
	"""
	Provides a number of test cases related to basic page structure 
	for html5 documents.
	"""

	def setUp(self):
		self.parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("etree"))

	def test_singular_tags(self):
		"""
		Test that the multiple-instance-singular-tag error is thrown
		for cases where more than one instance of a singular tag block is 
		present.

		Input: 
		Nested blocks of singular tags (html, body, head).
		eg. <html><html></html></html>

		Ouput:
		All three test cases should report a multiple instance of both
		the start and closing tags for each of the three singular tags.
		"""
		multipleHTMLInstances = "<html><html></html></html>"
		multipleHeadInstances = "<html><head><head></head></head><body></body></html>"
		multipleBodyInstances = "<html><head></head><body><body></body></body></html>"

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

		self.assertIn(((25, 30), u'multiple-instance-singular-tag', {u'name': u'body'}), 
			self.parser.errors, "Multiple instances of starting HTML tag not reported.")

		self.assertIn(((38, 44), u'unexpected-end-tag-after-body', {u'name': u'body'}),
			self.parser.errors, "Multiple instances of closing body tag not reported.")

	def test_missing_doctype(self):
		"""
		Test that the expected-doctype-but-got-start-tag error is thrown
		for cases where no DOCTYPE is declared.

		Input:
		Nested blocks of singular tags (html, body, head), all of which
		are missing the DOCTYPE declaration.
		eg. <html><html></html></html>

		Expected Results:
		All test cases should report a missing DOCTYPE declaration.
		"""
		startTagBeforeDoctype = "<html><html></html></html>"
		endTagBeforeDoctype = "</head></head>"
		eofBeforeDoctype = ""

		self.parser.parse(startTagBeforeDoctype)
		
		self.assertIn(((0, 5), u'expected-doctype-but-got-start-tag', {u'name': u'html'}),
			self.parser.errors, "Failed to report missing DOCTYPE declaration (start tag before doctype.")

		self.parser.reset()
		self.parser.parse(endTagBeforeDoctype)

		self.assertIn(((0, 6), u'expected-doctype-but-got-end-tag', {u'name': u'head'}),
			self.parser.errors, "Failed to report missing DOCTYPE declaration (closing tag before doctype.")

		self.parser.reset()
		self.parser.parse(eofBeforeDoctype)

		self.assertIn(((-1, -1), u'expected-doctype-but-got-eof', {}),
			self.parser.errors, "Failed to report missing DOCTYPE declaration (EOF before doctype.")

	
	def test_closing_html(self):
		"""
		Test that a missing HTML closing tag is reported when none
		are present in the document.

		Input:
		Nested blocks of singular tags (head, body).

		Expected Results:
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
		Test that both start and closing tags occurring before the head
		section are reported as being misplaced.

		Input:
		A number of instances of start and closing tags being placed before
		the head section.

		Expected Results:
		Report whether or not the tags preceding the head section are reported
		as being misplaced.
		"""
		misplacedHeadTags = "<html><body></body><head></head></html>"
		misplacedLinkTags = "<html><a></a><head></head><body></body></html>"

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

	def test_incorrect_tags_in_head(self):
		"""
		Test that tags which don't belong in the head section
		are reported as misplaced using the 'incorrect-start-tag-placement-in-head'
		and 'incorrect-end-tag-placement-in-head' errors.

		Input:
		A HTML fragment with a pair of head tags enclosing a tag
		pair which doesn't belong in the head phase.

		Expected Results:
		Inclusion of the 'incorrect-start-tag-placement-in-head'
		and 'incorrect-end-tag-placement-in-head' errors being reported
		as part of the returned array of error codes.
		"""
		inputFragment = "<html><head><a></a></head></html>"

		self.parser.parse(inputFragment)

		self.assertIn(((12, 14), u'incorrect-start-tag-placement-in-head', {u'name': u'a'}),
			self.parser.errors, "Failed to report starting tag which doesn't belong in the head section.")

	def test_tags_after_eof(self):
		"""
		Tests that starting and closing tags occurring after the last
		instace of a closing HTML tag are reported as an error.

		Input:
		A HTML fragment with a start and closing tag pair occurring
		after the start and closing HTML pair.

		Expected Results:
		An error being thrown for both the start and closing tags occurring
		after the HTML tags.
		"""

		inputFragment = "<html></html><a></a>"

		self.parser.parse(inputFragment)

		self.assertIn(((13, 15), u'expected-eof-but-got-start-tag', {u'name': u'a'}),
			self.parser.errors, "Failed to report start tag after closing HTML tag.")

		self.assertIn(((16, 19), u'expected-eof-but-got-end-tag', {u'name': u'a'}),
			self.parser.errors, "Failed to report closing tag after closing HTML tag.")

	def test_missing_start_tag(self):
		"""
		Tests that a missing start tag is reported in the case
		that a closing tag is found without a matching start tag.

		Input:
		A HTML fragment containing a closing tag without a matching
		start tag.

		Expected Results:
		An error being thrown reporting that the matching start tag
		is missing.
		"""

		inputFragment = "<html><head></head><body></a></body></html>"

		self.parser.parse(inputFragment)

		self.assertIn(((25, 28), u'unexpected-end-tag', {u'name': u'a'}),
			self.parser.errors, "Failed to report the lack of a matching start tag.")

	def test_misplaced_tags_after_body(self):
		"""
		Tests that any tags occurring after the body phase
		are reported as being incorrectly placed.

		Input:
		A HTML fragment with a pair of start and closing tags placed
		after the closing body tag.

		Expected Results:
		An error should be thrown for both the start and closing
		tags found after the closing body tag.
		"""

		inputFragment = "<html><head></head><body></body><a></a></html>"

		self.parser.parse(inputFragment)

		self.assertIn(((32, 34), u'unexpected-start-tag-after-body', {u'name': u'a'}),
			self.parser.errors, "Failed to report misplaced starting tag found after the closing body tag.")

		self.assertIn(((35, 38), u'unexpected-end-tag-after-body', {u'name': u'a'}),
			self.parser.errors, "Failed to report misplaced closing tag found after the closing body tag.")

	def test_missing_closing_html_tag(self):
		"""
		Test that a missing closing HTML tag is reported.

		Input:
		A HTML fragment missing a closing HTML tag.

		Expected Results:
		An error should be thrown stating that the closing HTML tag is missing.
		"""

		inputFragment = "<html><head></head><body></body>"

		self.parser.parse(inputFragment)

		self.assertIn(((-1, -1), u'no-closing-html-tag', {}),
			self.parser.errors, "Failed to report missing closing HTML tag.")

	def test_early_termination_before_head(self):
		"""
		Test that an early closing HTML tag before the head phase
		is reported as an error.

		Input:
		A HTML fragment with the head and body sections placed after
		a closed set of HTML tags.

		Expected Results:
		An error should be thrown stating that the closing HTML tag
		has been found before the head phase.
		"""

		inputFragment = "<html></html><head></head><body></body>"

		self.parser.parse(inputFragment)

		self.assertIn(((6, 12), u'early-termination-before-head', {u'name': u'html'}),
			self.parser.errors, "Failed to report early termination before head section.")

	def test_early_termination_in_head(self):
		"""
		Test that an early closing HTML tag in the head phase
		is reported as an error.

		Input:
		A HTML fragment with the closing HTML tag placed within
		the set of head tags.

		Expected Results:
		An error should be thrown stating that the closing HTML tag
		has been found in the head phase.
		"""

		inputFragment = "<html><head></html></head><body></body>"

		self.parser.parse(inputFragment)

		self.assertIn(((12, 18), u'early-termination-in-head', {u'name': u'html'}),
			self.parser.errors, "Failed to report early termination before head section.")

	def test_early_termination_before_body(self):
		"""
		Test that an early closing HTML tag before the body phase
		is reported as an error.

		Input:
		A HTML fragment with the closing HTML tag placed before the body
		section.

		Expected Results:
		An error should be thrown stating that the closing HTML tag
		has been found before the body phase.
		"""

		inputFragment = "<html><head></head></html><body></body>"

		self.parser.parse(inputFragment)

		self.assertIn(((19, 25), u'early-termination-before-body', {u'name': u'html'}),
			self.parser.errors, "Failed to report early termination before head section.")

	def test_early_termination_in_body(self):
		"""
		Test that an early closing HTML tag in the body phase
		is reported as an error.

		Input:
		A HTML fragment with the closing HTML tag placed within
		the set of body tags.

		Expected Results:
		An error should be thrown stating that the closing HTML tag
		has been found in the head phase.
		"""

		inputFragment = "<html><head></head><body></html></body>"

		self.parser.parse(inputFragment)

		self.assertIn(((25, 31), u'early-termination-in-body', {u'name': u'html'}),
			self.parser.errors, "Failed to report early termination before head section.")

	def test_tags_between_head_body(self):
		"""
		Test that a set of tags placed after the head section
		but before the body section is reported as an error.

		Input:
		A HTML fragment with a set of tags between the head
		and body sections.

		Expected Results:
		An error should be thrown stating that the set of tags
		can't be placed between the head and body sections.
		"""

		inputFragment = "<html><head></head><a></a><body></body></html>"

		self.parser.parse(inputFragment)

		self.assertIn(((19, 21), u'start-tag-before-body-after-head', {u'name': u'a'}),
			self.parser.errors, "Failed to report start tag after head phase but before body phase.")

		self.assertIn(((22, 25), u'end-tag-before-body-after-head', {u'name': u'a'}),
			self.parser.errors, "Failed to report closing tag after head phase but before body phase.")

	def test_missing_starting_html_tag(self):
		"""
		Test that a missing starting HTML tag is reported as an error.

		Input:
		A HTML fragment missing a starting HTML tag.

		Expected Results:
		An error should be thrown indicating that the fragment doesn't
		contain a starting HTML tag.
		"""

		inputFragment = "<head></head><body></body></html>"

		self.parser.parse(inputFragment)

		self.assertIn(((-1, -1), u'no-starting-html-tag', {}),
			self.parser.errors, "Failed to report missing starting HTML tag.")

	def test_unknown_doctype(self):
		"""
		Test that a doctype with an invalid name is reported as being
		an unknown doctype.

		Input:
		A HTML fragment containing an invalid doctype name.

		Expected Results:
		An error should be thrown reporting that the doctype name is invalid.
		"""

		inputFragment = '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">'

		self.parser.parse(inputFragment)

		self.assertIn(((0, 89), u'unknown-doctype', {}),
			self.parser.errors, "Failed to report unknown doctype.")

	def test_space_after_doctype(self):
		"""
		Test that a doctype tag has a space between the doctype declaration
		and the doctype name.

		Input:
		A HTML fragment containing a doctype with no space between the doctype
		declaration and the doctype name.

		Expected Results:
		An error should be thrown reporting that there is no space between
		the doctype declaration and the doctype name.
		"""

		inputFragment = '<!DOCTYPEhtml>'

		self.parser.parse(inputFragment)

		self.assertIn(((0, 8), u'need-space-after-doctype', {}),
			self.parser.errors, "Failed to report missing space after the doctype declaration.")

	def test_end_tag_before_doctype(self):
		"""
		Test that a closing tag isn't placed before the doctype declaration.

		Input:
		A HTML fragment containing a single closing tag.

		Expected Results:
		An error should be thrown reporting that a closing tag has been 
		placed before the doctype declaration.
		"""

		inputFragment = '</html>'

		self.parser.parse(inputFragment)

		self.assertIn(((0, 6), u'expected-doctype-but-got-end-tag', {u'name': u'html'}),
			self.parser.errors, "Failed to report closing tag before doctype declaration.")

	def test_EOF_before_doctype(self):
		"""
		Test that an error is reported if the document is blank.
		
		Input:
		A blank document containing no characters of any kind.

		Expected Results:
		An error should be thrown reporting that the EOF was reached before
		a doctype was declared.
		"""

		inputFragment = """

		"""

		self.parser.parse(inputFragment)

		self.assertIn(((-1, -1), u'expected-doctype-but-got-eof', {}),
			self.parser.errors, "Failed to report the EOF occurring before the doctype declaration.")

	def test_form_element_not_in_form(self):
		"""
		Test that form elements must be contained in wrapping form tags.
		
		Input:
		A HTML fragment containing form elements which aren't wrapped in 
		form tags.

		Expected Results:
		An error should be thrown reporting that the form elements aren't contained
		in wrapping form tags.
		"""

		inputFragment = """
<!DOCTYPE html>
<html>
<head>
</head>
<body>
<datalist></datalist>
<fieldset></fieldset>
<input></input>
<label></label>
<output></output>
</body>
</html>
		"""

		self.parser.parse(inputFragment)

		self.assertIn(((46, 55), u'form-element-not-in-form', {u'name': u'datalist'}),
			self.parser.errors, "Failed to report datalist tag outside of wrapping form tags.")

		self.assertIn(((68, 77), u'form-element-not-in-form', {u'name': u'fieldset'}),
			self.parser.errors, "Failed to report fieldset tag outside of wrapping form tags.")

		self.assertIn(((90, 96), u'form-element-not-in-form', {u'name': u'input'}),
			self.parser.errors, "Failed to report input tag outside of wrapping form tags.")

		self.assertIn(((106, 112), u'form-element-not-in-form', {u'name': u'label'}),
			self.parser.errors, "Failed to report label tag outside of wrapping form tags.")

		self.assertIn(((122, 129), u'form-element-not-in-form', {u'name': u'output'}),
			self.parser.errors, "Failed to report output tag outside of wrapping form tag.")

	def test_duplicate_id_value(self):
		"""
		Test that the occurrence of duplicate id values is reported as an error.
		
		Input:
		A HTML fragment containing 2 elements with the same value for their id attribute.

		Expected Results:
		An error should be thrown reporting that an id attribute has the same value of a previously declared id
		attribute.
		"""

		inputFragment = """
<!DOCTYPE html>
<html>
<head>
</head>
<body>
<p id="blah"></p>
<p id="blah"></p>
</body>
</html>
		"""

		self.parser.parse(inputFragment)

		self.assertIn(((64, 76), u'duplicate-id-attribute', {u'name': u'p', u'original': u'p'}),
			self.parser.errors, "Failed to report duplicate id value usage.")

	def test_duplicate_page_title(self):
		"""
		Test that a duplicate title element is reported as an error.
		
		Input:
		A HTML fragment containing duplicate title elements.

		Expected Results:
		An error should be thrown reporting that a duplicate instance of the page 
		title has been found.
		"""

		inputFragment = """
<!DOCTYPE html>
<html>
<head>
<title>blah</title>
<title>blah</title>
</head>
<body>
</body>
</html>
		"""

		self.parser.parse(inputFragment)

		self.assertIn(((51, 57), u'duplicate-title-in-head', {u'name': u'title'}),
			self.parser.errors, "Failed to report duplicate title element.")

	def test_missing_title_element(self):
		"""
		Test that a missing title element as part of the head section
		is reported as missing.
		
		Input:
		A HTML fragment containing a basic page structure but missing the required
		title element in the head section.

		Expected Results:
		An error should be thrown reporting that the title element is missing from
		the head sectionself.
		"""

		inputFragment = """
<!DOCTYPE html>
<html>
<head>
</head>
<body>
</body>
</html>
		"""

		self.parser.parse(inputFragment)

		self.assertIn(((-1, -1), u'title-element-missing-from-head', {}),
			self.parser.errors, "Failed to report missing title element.")

	def test_img_missing_alt_attribute(self):
		"""
		Test that an img tag missing the required alt attribute is reported
		as an error.
		
		Input:
		A HTML fragment containing an img tag missing the required alt attribute.

		Expected Results:
		An error should be thrown reporting that the alt attribute is missing for the 
		given img tag.
		"""

		inputFragment = """
<!DOCTYPE html>
<html>
<head>
</head>
<body>
<img>
</body>
</html>
		"""

		self.parser.parse(inputFragment)

		self.assertIn(((46, 50), u'img-element-missing-alt-attribute', {u'name': u'img'}),
			self.parser.errors, "Failed to report missing alt attribute for the given img tag.")

	def test_img_alt_attribute_empty(self):
		"""
		Test that an img tag's alt attribute, when empty, is reported as an error.
		
		Input:
		A HTML fragment containing an img tag with an empty alt attribute.

		Expected Results:
		An error should be thrown reporting that the alt attribute is empty.
		"""

		inputFragment = """
<!DOCTYPE html>
<html>
<head>
</head>
<body>
<img alt="">
</body>
</html>
		"""

		self.parser.parse(inputFragment)

		self.assertIn(((46, 57), u'img-alt-attribute-empty', {u'attr': u''}),
			self.parser.errors, "Failed to report empty alt attriubte for img tag.")

	def test_missing_closing_tag_before_footer(self):
		"""
		Test that any open tags (missing the closing tag) are reported if the 
		footer section occurs before closing tag.
		
		Input:
		A HTML fragment containing an open 'a' tag which is missing the closing tag, 
		followed by the footer section.

		Expected Results:
		An error should be thrown reporting that the closing tag wasn't found before
		the footer section.
		"""

		inputFragment = """
<!DOCTYPE html>
<html>
<head>
</head>
<body>
<a>
<footer>
</footer>
</body>
</html>
		"""

		self.parser.parse(inputFragment)

		self.assertIn(((50, 57), u'missing-end-tag-before-footer', {u'name': u'a'}),
			self.parser.errors, "Failed to report missing end tag before footer section.")

	def test_missing_closing_tags_footer_section(self):
		"""
		Test that missing closing tags in the footer section are reported.
		
		Input:
		A HTML fragment containing an 'a' tag with a missing closing tag.

		Expected Results:
		An error should be thrown reporting that the closing tag is missing within the footer
		section.
		"""

		inputFragment = """
<!DOCTYPE html>
<html>
<head>
</head>
<body>
<footer>
<a>
</footer>
</body>
</html>
		"""

		self.parser.parse(inputFragment)

		self.assertIn(((59, 67), u'missing-closing-tags-in-footer', {u'name': u'a'}),
			self.parser.errors, "Failed to report missing closing tag in footer section.")

	def test_invalid_tag_name(self):
		"""
		Test that tags with invalid tag names are reported as errors.
		
		Input:
		A HTML fragment containing a tag with an invalid name "blah".

		Expected Results:
		An error should be thrown reporting that the tag name is invalid.
		"""

		inputFragment = """
<!DOCTYPE html>
<html>
<head>
</head>
<body>
<blah></blah>
<footer>
</footer>
</body>
</html>
		"""

		self.parser.parse(inputFragment)

		self.assertIn(((46, 51), u'invalid-element-name', {u'name': u'blah'}),
			self.parser.errors, "Failed to report invalid tag name.")

	def test_missing_closing_tag(self):
		"""
		Test that any missing closing tags are reported as errors.
		
		Input:
		A HTML fragment containing an opening 'a' tag with a missing closing tag.

		Expected Results:
		An error should be thrown reporting that the closing tag is missing.
		"""

		inputFragment = """
<!DOCTYPE html>
<html>
<head>
</head>
<body>
<a>
<footer>
</footer>
</body>
</html>
		"""

		self.parser.parse(inputFragment)

		self.assertIn(((46, 48), u'missing-end-tag', {u'name': u'a'}),
			self.parser.errors, "Failed to report missing closing tag.")

if __name__ == '__main__':
	unittest.main()
