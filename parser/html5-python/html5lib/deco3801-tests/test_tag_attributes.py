from __future__ import absolute_import, division, unicode_literals

#from . import support
import unittest, html5lib
from html5lib import treebuilders

class TestTagAttributes(unittest.TestCase):
    """
    Provides a number of test cases related to basic page structure 
    for html5 documents.
    """

    def setUp(self):
        self.parser = html5lib.HTMLParser(tree=treebuilders.getTreeBuilder("etree"))

    def test_valid_relative_filepath(self):
        """
        Tests that valid relative file names are not reported as erroneous.

        Input:
        A HTML fragment which is contains two valid relative paths. One in a parent directory of the cwd,
        and the other in a child directory of the cwd.

        Expected Results:
        The resulting errors should NOT contain any error indicating an invalid file path.
        """
        inputFragment = '<img src="../image.jpg"><img src="directory2/image2.jpg">'
        files = ["image.jpg", "directory/", "directory/current.html", "directory/directory2/", "directory/directory2/image2.jpg"]
        filename = "directory/current.html"
       
        self.parser.parse(inputFragment, files=files, filename=filename)

        invalidPaths = [span for span, name, _ in self.parser.errors if name == "invalid-url-attrib"]

        self.assertEqual(invalidPaths, [], "Incorrectly reported a valid relative file path as invalid.")


    def test_invalid_relative_filepath(self):
        """
        Tests that invalid relative file names are reported as erroneous. That is, if a filepath is specified to a 
        non-existent file in a valid directory, the path is reported as erroneous.

        Input:
        A HTML fragment which is contains two invalid relative paths. One in a parent directory of the cwd,
        and the other in a child directory of the cwd. Both paths are within the directory structure, except that
        the files do not exists (that is, the directories themselves do exist).

        Expected Results:
        The resulting errors should contain two errors indicating invalid file paths.
         """
        inputFragment = '<img src="../image.jpg"><img src="directory2/image2.jpg">'
        files = ["directory/", "directory/current.html", "directory/directory2/", "directory/directory2/image3.jpg"]
        filename = "directory/current.html"
       
        self.parser.parse(inputFragment, files=files, filename=filename)

        invalidPaths = [span for span,name,_ in self.parser.errors if name == "invalid-url-attrib"]

        self.assertEqual(invalidPaths, [(5,23), (29, 56)], "Failed to report invalid relative file path attribute url.") 

    def test_nonexistent_relative_filepath(self):
        """
        Tests that relative file names are reported as erroneous. That is, if a filepath is specified to a 
        non-existent file in a non-existen directory, the path is reported as erroneous. This test differs from
        test_invalid_path in that the specified directories do not exist at all.

        Input:
        A HTML fragment which is contains two invalid relative paths. One in a non-existant directory above the cwd,
        and the other in a non-existant child directory of the cwd. 

        Expected Results:
        The resulting errors should contain two errors indicating invalid file paths.
         """
        inputFragment = '<img src="../../image.jpg"><img src="directory2/directory3/image2.jpg">'
        files = ["directory/", "directory/current.html", "directory/directory2/", "directory/directory2/image2.jpg", "image.jpg"]
        filename = "directory/current.html"
       
        self.parser.parse(inputFragment, files=files, filename=filename)

        invalidPaths = [span for (span,name,_) in self.parser.errors if name == "invalid-url-attrib"]

        self.assertEqual(invalidPaths, [(5,26), (32, 70)], "Failed to correctly report invalid relative file path attribute url.") 

    def test_valid_absolute_filepath(self):
        """
        Tests that valid absolute file names are not reported as erroneous.

        Input:
        A HTML fragment which is contains two valid absolute paths. One in a parent directory of the cwd,
        and the other in a child directory of the cwd.

        Expected Results:
        The resulting errors should NOT contain any error indicating an invalid file path.
        """
        inputFragment = '<img src="/image.jpg"><img src="/directory/directory2/image2.jpg">'
        files = ["image.jpg", "directory/", "directory/current.html", "directory/directory2/", "directory/directory2/image2.jpg"]
        filename = "directory/current.html"
       
        self.parser.parse(inputFragment, files=files, filename=filename)

        invalidPaths = [span for span,name,_ in self.parser.errors if name == "invalid-url-attrib"]

        self.assertEqual(invalidPaths, [], "Incorrectly reported a valid absolute file path as invalid.")


    def test_invalid_absolute_filepath(self):
        """
        Tests that invalid absolute file names are reported as erroneous. That is, if a filepath is specified to a 
        non-existent file in a valid directory, the path is reported as erroneous.

        Input:
        A HTML fragment which is contains two invalid absolute paths. Both paths are within the directory structure, 
        except that the files do not exists (that is, the directories themselves do exist).

        Expected Results:
        The resulting errors should contain two errors indicating invalid file paths.
         """
        inputFragment = '<img src="/image2.jpg"><img src="/directory/directory2/image3.jpg">'
        files = ["directory/", "directory/current.html", "directory/directory2/"]
        filename = "directory/current.html"
       
        self.parser.parse(inputFragment, files=files, filename=filename)

        invalidPaths = [span for (span,name,_) in self.parser.errors if name == "invalid-url-attrib"]

        self.assertEqual(invalidPaths, [(5,22), (28, 66)], "Failed to report invalid absolute file path attribute url.") 

    def test_nonexistent_absolute_filepath(self):
        """
        Tests that absolute file names are reported as erroneous. That is, if a filepath is specified to a 
        non-existent file in a non-existent directory, the path is reported as erroneous. This test differs from
        test_invalid_absolute_filepath in that the specified directories do not exist at all.

        Input:
        A HTML fragment which is contains an invalid absolute path.

        Expected Results:
        The resulting errors should contain one error indicating an invalid file path.
         """
        inputFragment = '<img src="/directory3/image.jpg">'
        files = ["directory/", "directory/current.html","directory/directory2/image2.jpg", "image.jpg"]
        filename = "directory/current.html"
       
        self.parser.parse(inputFragment, files=files, filename=filename)

        invalidPaths = [span for (span,name,_) in self.parser.errors if name == "invalid-url-attrib"]

        self.assertEqual(invalidPaths, [(5,32)] , "Failed to correctly report invalid absolute file path attribute url.") 

    def test_missing_input_attributes(self):
        """
        Test that missing required input attributes are reported as being missing.
        
        Input:
        A HTML fragment containing a form element with a single input element, which
        contains none of the required attributes (type, value, name).

        Expected Results:
        Errors should be thrown for each of the missing required attributes.
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

        self.assertIn(((53, 59), u'input-element-missing-type-attribute', {u'name': u'input'}),
            self.parser.errors, "Failed to report missing type attribute for a form element.")

        self.assertIn(((53, 59), u'input-element-missing-value-attribute', {u'name': u'input'}),
            self.parser.errors, "Failed to report missing value attribute for a form element.")

        self.assertIn(((53, 59), u'input-element-missing-name-attribute', {u'name': u'input'}),
            self.parser.errors, "Failed to report missing name attribute for a form element.")

    def test_a_tag_missing_attributes(self):
        """
        Test that missing attributes for the 'a' tag are reported as errors.
        
        Input:
        A HTML fragment containing an 'a' tag with no attributes.

        Expected Results:
        An error should be thrown for each of the missing attributes reporting that they 
        are missing.
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

        self.assertIn(((46, 48), u'a-element-missing-href-attribute', {u'name': u'a'}),
            self.parser.errors, "Failed to report missing href attribute for an 'a' tag.")

        self.assertIn(((46, 48), u'a-element-missing-href-attribute', {u'name': u'a'}),
            self.parser.errors, "Failed to report missing name attribute for an 'a' tag.")

    def test_a_tag_empty_attribute_values(self):
        """
        Test that required attributes for the 'a' tag don't have empty values.
        
        Input:
        A HTML fragment containing all required attributes for the 'a' tag but with empty
        values for these attributes.

        Expected Results:
        An error should be thrown reporting each of the attributes as having empty values.
        """

        inputFragment = """
<!DOCTYPE html>
<html>
<head>
</head>
<body>
<a name="" href="" rel="">
<footer>
</footer>
</body>
</html>
        """

        self.parser.parse(inputFragment)

        self.assertIn(((46, 71), u'a-href-attribute-empty', {u'attr': u''}),
            self.parser.errors, "Failed to report empty value for the href attribute of an 'a' tag.")

        self.assertIn(((46, 71), u'a-name-attribute-empty', {u'attr': u''}),
            self.parser.errors, "Failed to report empty value for the name attribute of an 'a' tag.")

        self.assertIn(((46, 71), u'a-rel-attribute-empty', {u'attr': u''}),
            self.parser.errors, "Failed to report empty value for the rel attribute of an 'a' tag.")

    def test_link_missing_attributes(self):
        """
        Test that any missing required attributes for a link tag are reported as missing.
        
        Input:
        A HTML fragment containing a link tag with no attributes.

        Expected Results:
        An error should be thrown for each of the missing required attributes (href, rel).
        """

        inputFragment = """
<!DOCTYPE html>
<html>
<head>
</head>
<body>
<link>
<footer>
</footer>
</body>
</html>
        """

        self.parser.parse(inputFragment)

        self.assertIn(((46, 51), u'link-element-missing-href-attribute', {u'name': u'link'}),
            self.parser.errors, "Failed to report missing href attribute for a link tag.")

        self.assertIn(((46, 51), u'link-element-missing-rel-attribute', {u'name': u'link'}),
            self.parser.errors, "Failed to report missing rel attribute for a link tag.")

    def test_link_tag_empty_attribute_values(self):
        """
        Test that empty values for the required attributes for a link tag are reported
        as errors.
        
        Input:
        A HTML fragment containing all required attributes for the link tag but with all
        attributes having empty values.

        Expected Results:
        An error should be thrown reporting that each attribute has an empty value.
        """

        inputFragment = """
<!DOCTYPE html>
<html>
<head>
</head>
<body>
<link href="" type="" rel="">
<footer>
</footer>
</body>
</html>
        """

        self.parser.parse(inputFragment)

        self.assertIn(((46, 74), u'link-href-attribute-empty', {u'attr': u''}),
            self.parser.errors, "Failed to report empty value for the href attribute of a link tag.")

        self.assertIn(((46, 74), u'link-type-attribute-empty', {u'attr': u''}),
            self.parser.errors, "Failed to report empty value for the type attribute of a link tag.")

        self.assertIn(((46, 74), u'link-rel-attribute-empty', {u'attr': u''}),
            self.parser.errors, "Failed to report empty value for the rel attribute of a link tag.")

    def test_footer_section(self):
        """
        Test that the opening and closing footer tags are reported as missing if they aren't 
        included in a HTML document.
        
        Input:
        A HTML fragment with the opening and closing footer tags omitted.

        Expected Results:
        An error should be thrown reporting that the footer tags are missing.
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

        self.assertIn(((-1, -1), u'footer-start-tag-missing', {}),
            self.parser.errors, "Failed to report missing footer start tag.")

        self.assertIn(((-1, -1), u'footer-end-tag-missing', {}),
            self.parser.errors, "Failed to report missing footer closing tag.")

if __name__ == '__main__':
    unittest.main()
