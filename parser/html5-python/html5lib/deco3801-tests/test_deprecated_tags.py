from __future__ import absolute_import, division, unicode_literals

#from . import support
import unittest, html5lib
from html5lib import treebuilders

class TestSyntax(unittest.TestCase):
	"""
	Provides a number of test cases to test correct error reporting of deprecated
	tags
	"""

	def setUp(self):
		self.parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("etree"))

	def test_deprecated_tags(self):
		"""
		Test that
		
		Input:

		Expected Results:

		"""

		inputFragment = """
<!DOCTYPE>
<html>
<head>
</head>
<body>
    <acronym></acronym>
    <applet></applet>
    <b></b>
    <basefont></basefont>
    <big></big>
    <center></center>
    <dir></dir>
    <font></font>
    <frame></frame>
    <frameset></frameset>
    <i></i>
    <noframes></noframes>
    <small></small>
    <strike></strike>
    <tt></tt>
</body>
</html>
		"""

		self.parser.parse(inputFragment.decode("utf-8"))

		for error in self.parser.errors:
			print error

		self.assertIn(((45, 53), u'deprecated-tag', {u'name': u'acronym'}),
			self.parser.errors, "Failed to report deprecated acronym tag.")

		self.assertIn(((69, 76), u'deprecated-tag', {u'name': u'applet'}),
			self.parser.errors, "Failed to report deprecated applet tag.")

		self.assertIn(((91, 93), u'deprecated-tag', {u'name': u'b'}),
			self.parser.errors, "Failed to report deprecated b tag.")

		self.assertIn(((103, 112), u'deprecated-tag', {u'name': u'basefont'}),
			self.parser.errors, "Failed to report deprecated basefont tag.")

		self.assertIn(((129, 133), u'deprecated-tag', {u'name': u'big'}),
			self.parser.errors, "Failed to report deprecated big tag.")

		self.assertIn(((145, 152), u'deprecated-tag', {u'name': u'center'}),
			self.parser.errors, "Failed to report deprecated center tag.")

		self.assertIn(((167, 171), u'deprecated-tag', {u'name': u'dir'}),
			self.parser.errors, "Failed to report deprecated dir tag.")

		self.assertIn(((183, 188), u'deprecated-tag', {u'name': u'font'}),
			self.parser.errors, "Failed to report deprecated font tag.")

		self.assertIn(((201, 207), u'deprecated-frame-element', {u'name': u'frame'}),
			self.parser.errors, "Failed to report deprecated frame tag.")

		self.assertIn(((221, 230), u'deprecated-frame-element', {u'name': u'frameset'}),
			self.parser.errors, "Failed to report deprecated frameset tag.")

		self.assertIn(((247, 249), u'deprecated-tag', {u'name': u'i'}),
			self.parser.errors, "Failed to report deprecated i tag.")

		self.assertIn(((259, 268), u'deprecated-frame-element', {u'name': u'noframes'}),
			self.parser.errors, "Failed to report deprecated noframes tag.")

		self.assertIn(((285, 291), u'deprecated-tag', {u'name': u'small'}),
			self.parser.errors, "Failed to report deprecated small tag.")

		self.assertIn(((305, 312), u'deprecated-tag', {u'name': u'strike'}),
			self.parser.errors, "Failed to report deprecated strike tag.")

		self.assertIn(((327, 330), u'deprecated-tag', {u'name': u'tt'}),
			self.parser.errors, "Failed to report deprecated tt tag.")

if __name__ == '__main__':
	unittest.main()
