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

        self.assertEqual(invalidPaths, [(0,23), (24, 56)], "Failed to report invalid relative file path attribute url.") 

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

        self.assertEqual(invalidPaths, [(0,26), (27, 70)], "Failed to correctly report invalid relative file path attribute url.") 

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

        self.assertEqual(invalidPaths, [(0,22), (23, 66)], "Failed to report invalid absolute file path attribute url.") 

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

        self.assertEqual(invalidPaths, [(0,32)] , "Failed to correctly report invalid absolute file path attribute url.") 

if __name__ == '__main__':
    unittest.main()
