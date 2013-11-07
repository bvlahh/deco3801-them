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

		def test_input_missing_label(self):
		"""
		Test that input elements must require a corresponding label element.
		
		Input:
		A HTML fragment containing an input element but no matching label element.

		Expected Results:
		An error should be thrown reporting that the label element is missing.
		"""

		inputFragment = """
<!DOCTYPE html>
<html>
<head>
</head>
<body>
<form>
<input></input>
</form>
</body>
</html>
		"""

		self.parser.parse(inputFragment)

		self.assertIn(((53, 59), u'input-element-missing-label', {u'name': u'input'}),
			self.parser.errors, "Failed to report missing label element for given input element.")

if __name__ == '__main__':
	unittest.main()
