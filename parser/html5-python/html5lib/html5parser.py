from __future__ import absolute_import, division, unicode_literals
from six import with_metaclass

import os
import types

from . import inputstream
from . import tokenizer

from . import treebuilders
from .treebuilders._base import Marker

from . import utils
from . import constants
from .constants import spaceCharacters, asciiUpper2Lower
from .constants import specialElements
from .constants import headingElements
from .constants import cdataElements, rcdataElements
from .constants import tokenTypes, ReparseException, namespaces
from .constants import htmlIntegrationPointElements, mathmlTextIntegrationPointElements
from .constants import adjustForeignAttributes as adjustForeignAttributesMap

# DECO3801 - Imports
from .constants import singularTags, errorCodes, deprecatedTags, urlTags, urlTagMap
from .constants import formElements, formInputType, allowedElementNames

def parse(doc, treebuilder="etree", encoding=None,
          namespaceHTMLElements=True):
    """Parse a string or file-like object into a tree"""
    tb = treebuilders.getTreeBuilder(treebuilder)
    p = HTMLParser(tb, namespaceHTMLElements=namespaceHTMLElements)
    return p.parse(doc, encoding=encoding)


def parseFragment(doc, container="div", treebuilder="etree", encoding=None,
                  namespaceHTMLElements=True):
    tb = treebuilders.getTreeBuilder(treebuilder)
    p = HTMLParser(tb, namespaceHTMLElements=namespaceHTMLElements)
    return p.parseFragment(doc, container=container, encoding=encoding)


def method_decorator_metaclass(function):
    class Decorated(type):
        def __new__(meta, classname, bases, classDict):
            for attributeName, attribute in classDict.items():
                if isinstance(attribute, types.FunctionType):
                    attribute = function(attribute)

                classDict[attributeName] = attribute
            return type.__new__(meta, classname, bases, classDict)
    return Decorated


class HTMLParser(object):
    """HTML parser. Generates a tree structure from a stream of (possibly
        malformed) HTML"""

    def __init__(self, tree=None, tokenizer=tokenizer.HTMLTokenizer,
                 strict=False, namespaceHTMLElements=True, debug=False):
        """
        strict - raise an exception when a parse error is encountered

        tree - a treebuilder class controlling the type of tree that will be
        returned. Built in treebuilders can be accessed through
        html5lib.treebuilders.getTreeBuilder(treeType)

        tokenizer - a class that provides a stream of tokens to the treebuilder.
        This may be replaced for e.g. a sanitizer which converts some tags to
        text
        """

        # Raise an exception on the first error encountered
        self.strict = strict

        if tree is None:
            tree = treebuilders.getTreeBuilder("etree")
        self.tree = tree(namespaceHTMLElements)
        self.tokenizer_class = tokenizer
        self.errors = []

        # DECO3801 - Keeps count of any instances of singular tags encountered
        # to prevent multiple instaces.
        self.singular = []
        self.singularEndTags = []
        self.remainingTokens = []

        # DECO3801 - List of 'for' attributes for label tags associated
        # with form input elements.
        self.forLabels = []

        # DECO3801 - Dictionary of tag ID's used to check for 
        # multiple tags using the same ID value.
        self.idDict = {}

        # DECO3801 - Boolean flag used to check whether or not a HTML document
        # contains a title within the head section or not.
        self.hasTitle = False

        # DECO3801 - Arrays to track open tags.
        self.openStartTags = []
        self.remainingClosingTags = []

        self.phases = dict([(name, cls(self, self.tree)) for name, cls in
                            getPhases(debug).items()])

    def _parse(self, stream, innerHTML=False, container="div",
               encoding=None, parseMeta=True, useChardet=True, files=None, filename=None, **kwargs):

        self.innerHTMLMode = innerHTML
        self.container = container
        self.tokenizer = self.tokenizer_class(stream, encoding=encoding,
                                              parseMeta=parseMeta,
                                              useChardet=useChardet,
                                              parser=self, **kwargs)
        
        # DECO3801 - Tokenizer to generate the list of tags used to track the 
        # remaining tags to be processed. Used in a number of error checks 
        # in an attempt to check if the current token is the only remaining 
        # instance of that token in the file.
        self.tokenizerRemaining = self.tokenizer_class(stream, encoding=encoding,
                                              parseMeta=parseMeta,
                                              useChardet=useChardet,
                                              parser=self, **kwargs)
        # DECO3801 - List of files and directories
        self.files = files
        # DECO3801 - The full file name of the file currently being parsed
        self.cwd = ""

        if filename is not None:
            self.cwd = filename.split(os.sep)[:-1]

        self.reset()

        while True:
            try:
                self.mainLoop()
                break
            except ReparseException:
                self.reset()

    def reset(self):
        self.tree.reset()
        self.firstStartTag = False
        self.errors = []

        # DECO3801 - Reset processing lists.
        self.singular = []
        self.singularEndTags = []
        self.remainingTokens = []

        self.log = []  # only used with debug mode
        # "quirks" / "limited quirks" / "no quirks"
        self.compatMode = "no quirks"

        if self.innerHTMLMode:
            self.innerHTML = self.container.lower()

            if self.innerHTML in cdataElements:
                self.tokenizer.state = self.tokenizer.rcdataState
            elif self.innerHTML in rcdataElements:
                self.tokenizer.state = self.tokenizer.rawtextState
            elif self.innerHTML == 'plaintext':
                self.tokenizer.state = self.tokenizer.plaintextState
            else:
                # state already is data state
                # self.tokenizer.state = self.tokenizer.dataState
                pass
            self.phase = self.phases["beforeHtml"]
            self.phase.insertHtmlElement()
            self.resetInsertionMode()
        else:
            self.innerHTML = False
            self.phase = self.phases["initial"]

        self.lastPhase = None

        self.beforeRCDataPhase = None

        self.framesetOK = True

    # DECO3801 - Returns a formatted array of error entries made up of arrays
    # containing error information in the format:
    # [error code, tag start position, tag end position]
    def parseErrors(self):
        formattedErrors = []
        for error in self.errors:
            if not (errorCodes.get(error[1]) == None):
                formattedErrors.append([errorCodes.get(error[1]),
                    error[0][0], error[0][1], error[2]])
 
        return formattedErrors

    def isHTMLIntegrationPoint(self, element):
        if (element.name == "annotation-xml" and
                element.namespace == namespaces["mathml"]):
            return ("encoding" in element.attributes and
                    element.attributes["encoding"].translate(
                        asciiUpper2Lower) in
                    ("text/html", "application/xhtml+xml"))
        else:
            return (element.namespace, element.name) in htmlIntegrationPointElements

    def isMathMLTextIntegrationPoint(self, element):
        return (element.namespace, element.name) in mathmlTextIntegrationPointElements

    def mainLoop(self):
        CharactersToken = tokenTypes["Characters"]
        SpaceCharactersToken = tokenTypes["SpaceCharacters"]
        StartTagToken = tokenTypes["StartTag"]
        EndTagToken = tokenTypes["EndTag"]
        CommentToken = tokenTypes["Comment"]
        DoctypeToken = tokenTypes["Doctype"]
        ParseErrorToken = tokenTypes["ParseError"]

        self.generateRemainingTokens()

        for token in self.normalizedTokens():
            new_token = token

            # DECO3801 - Removes a token to maintain parity with the 
            # list of tokens which have yet to be processed.
            self.remainingTokens.pop(0)

            if new_token is not None and 'name' in new_token:
                # DECO3801 - Check tag contains a valid tag name.
                if new_token["name"] not in allowedElementNames:
                    self.parseError("invalid-element-name", {"name": new_token["name"]})
                # DECO3801 - Check for deprecated tags.
                if new_token["name"] in deprecatedTags:
                    if new_token["name"] in ["frame", "frameset", "noframes"]:
                        self.parseError("deprecated-frame-element", {"name": new_token["name"]})
                    else:
                        self.parseError("deprecated-tag", {"name": new_token["name"]})

                # DECO3801 - Updates the dictionary of ID's and tracks duplicate
                # entries. Reports duplicate instances of the same ID being used.
                if new_token["type"] == StartTagToken and "id" in new_token["data"]:
                    if not new_token["data"]["id"] in self.idDict:
                        self.idDict[new_token["data"]["id"]] = {"original": new_token, "duplicates": []}
                    else:
                        self.idDict[new_token["data"]["id"]]["duplicates"].append(new_token)
                        # DECO3801 TODO: If we implement tag positions within the token information
                        # we can update the error checking accordingly.
                        self.parseError("duplicate-id-attribute", 
                            {"name": new_token["name"], "original": self.idDict[new_token["data"]["id"]]["original"]["name"]})

                # DECO3801 - Check img tags have a valid alt attribute.
                if new_token["type"] == StartTagToken and new_token["name"] == "img":
                    if not "alt" in new_token["data"]:
                        self.parseError("img-element-missing-alt-attribute", {"name": new_token["name"]})
                    else:
                        if new_token["data"]["alt"][0] == "":
                            # DECO3801 TODO - Update with proper error check once attribute positions
                            # are added to tokens.
                            self.parseError("img-alt-attribute-empty", {"attr": new_token["data"]["alt"]})

                # DECO3801 - Check link tags have valid attributes.
                if new_token["type"] == StartTagToken and new_token["name"] == "a":
                    if not "href" in new_token["data"]:
                        self.parseError("a-element-missing-href-attribute", {"name": new_token["name"]})
                    else:
                        if new_token["data"]["href"][0] == "":
                            print "test"
                            self.parseError("a-href-attribute-empty", {"attr": new_token["data"]["href"]})

                    if not "name" in new_token["data"]:
                        self.parseError("a-element-missing-name-attribute", {"name": new_token["name"]})
                    else:
                        if new_token["data"]["name"][0] == "":
                            self.parseError("a-name-attribute-empty", {"attr": new_token["data"]["name"]})

                # DECO3801 - File name attribute checking for zip file uploads.
                if self.files is not None and new_token.get("name") in urlTags:
                    self.checkURL(new_token)

            while new_token is not None:
                currentNode = self.tree.openElements[-1] if self.tree.openElements else None
                currentNodeNamespace = currentNode.namespace if currentNode else None
                currentNodeName = currentNode.name if currentNode else None

                if "name" in new_token:
                    if new_token["name"] in formElements:
                        self.checkFormElement(new_token)

                type = new_token["type"]

                if type == ParseErrorToken:
                    self.parseError(new_token["data"], new_token.get("datavars", {}))
                    new_token = None
                else:
                    if (len(self.tree.openElements) == 0 or
                        currentNodeNamespace == self.tree.defaultNamespace or
                        (self.isMathMLTextIntegrationPoint(currentNode) and
                         ((type == StartTagToken and
                           token["name"] not in frozenset(["mglyph", "malignmark"])) or
                          type in (CharactersToken, SpaceCharactersToken))) or
                        (currentNodeNamespace == namespaces["mathml"] and
                         currentNodeName == "annotation-xml" and
                         token["name"] == "svg") or
                        (self.isHTMLIntegrationPoint(currentNode) and
                         type in (StartTagToken, CharactersToken, SpaceCharactersToken))):
                        phase = self.phase
                    else:
                        phase = self.phases["inForeignContent"]
                    
                    if type == CharactersToken:
                        new_token = phase.processCharacters(new_token)
                    elif type == SpaceCharactersToken:
                        new_token = phase.processSpaceCharacters(new_token)
                    elif type == StartTagToken:
                        self.openStartTags.append(new_token)
                        new_token = phase.processStartTag(new_token)
                    elif type == EndTagToken:
                        self.checkClosingTags(new_token)
                        new_token = phase.processEndTag(new_token)
                    elif type == CommentToken:
                        new_token = phase.processComment(new_token)
                    elif type == DoctypeToken:
                        new_token = phase.processDoctype(new_token)

            if (type == StartTagToken and token["selfClosing"]
                    and not token["selfClosingAcknowledged"]):
                self.parseError("non-void-element-with-trailing-solidus",
                                {"name": token["name"]})
        
        # DECO3801 - Check for closing html tag
        if "html" not in self.singularEndTags:
           self.parseError("no-closing-html-tag");

        if "html" not in self.singular:
            self.parseError("no-starting-html-tag")

        # DECO3801 - Check that a valid closing head tag exists in the document.
        if "head" not in self.singular:
            self.parseError("head-start-tag-missing")

        if "head" not in self.singularEndTags:
            self.parseError("head-end-tag-missing")

        # DECO3801 - Check that the document contains a valid
        # body section.
        if "body" not in self.singular:
            self.parseError("body-start-tag-missing")

        if "body" not in self.singularEndTags:
            self.parseError("body-end-tag-missing")

        # DECO3801 - Check that the document contains a valid
        # footer section.
        if "footer" not in self.singular:
            self.parseError("footer-start-tag-missing")

        if "footer" not in self.singularEndTags:
            self.parseError("footer-end-tag-missing")

        if not self.hasTitle:
            self.parseError("title-element-missing-from-head")
 
        # When the loop finishes it's EOF
        reprocess = True
        phases = []
        while reprocess:
            phases.append(self.phase)
            reprocess = self.phase.processEOF()
            if reprocess:
                assert self.phase not in phases

        # DECO3801 - Report missing closing tags.
        for tag in self.openStartTags:            
            self.parseErrorWithPos((tag['startPos'], tag['endPos']), "missing-end-tag", {"name": tag["name"]})

    # DECO3801 - Process end tags, removing the corresponding start tag from the
    # openStartTags list. If a closing tag cannot be matched to any of the starting
    # tags seen so far, it is added to the remainingClosingTags list which
    # tracks closing tags with no matching opening tag.
    def checkClosingTags(self, token):
        tempTokens = []
        while(self.openStartTags):
            currentToken = self.openStartTags.pop()
            if currentToken['name'] == token['name']:
                break

            tempTokens.append(currentToken)

        if not self.openStartTags:
            self.remainingClosingTags.append(token)

        while tempTokens:
            self.openStartTags.append(tempTokens.pop())

    # DECO3801 - Checks local URLs for validity. This function works for both absolute and relative
    # local file paths. Checks all html5 tags for which the specification indicates a URL attribute,
    # i.e. the 'src' attribute of an img tag, the 'href' attribute of an 'a' tag, or the 'data' attribute
    # of an 'object' tag.
    def checkURL(self, token):
        data = token.get("data")

        # Check for the case where no attributes are present and ignore
        # any further attribute checking.
        if not data:
            return

        for urlAttr in urlTagMap[token.get("name")]:

            pair = data.get(urlAttr)

            if(pair is None):
                continue

            url, pos = pair

            if "http://" in url or "https://" in url: # We ignore Web urls
                continue

            if url.find("/") == 0: # the path was lead by a "/", meaning the path is absolute.
                if url[1:] not in self.files: # slice the leading "/" as our directory structure removes this
                    self.parseErrorWithPos(pos, "invalid-url-attrib", {"name": token["name"], "attr": urlAttr})
                continue

            # split url into directories (and the final filename
            url = url.split(os.sep)
            
            upDirs = url.count('..')
            # If the '..' directory command is used
            if upDirs > len(self.cwd):
                self.parseErrorWithPos(pos, "invalid-url-attrib", {"name": token["name"], "attr": urlAttr})
                continue
            elif upDirs is not 0:
                abUrl = os.sep.join(self.cwd[:-upDirs] + url[upDirs:])
            else:
                abUrl = os.sep.join(self.cwd + url)

            if abUrl not in self.files:
                self.parseErrorWithPos(pos, "invalid-url-attrib", {"name": token["name"], "attr": urlAttr})

    # DECO3801 - Checks form elements for proper formatting and that they
    # are contained within a form element.
    def checkFormElement(self, token):
        
        # DECO3801 - Check that form elements are contained within enclosing
        # form tags.
        openFormList = []

        if self.tree.openElements:
            for currentElement in self.tree.openElements:
                if currentElement.name == "form":
                    openFormList.append(currentElement)
            if not openFormList:
                self.parseError("form-element-not-in-form", {"name": token["name"]})
        else:
            self.parseError("form-element-not-in-form", {"name": token["name"]})

        # DECO3801 - Check that input elements contain valid value, 
        # name and type attributes.
        if token["type"] == tokenTypes["StartTag"] and token["name"] == "input":
            if not "type" in token["data"]:
                self.parseError("input-element-missing-type-attribute", {"name": token["name"]})
                
                if not "value" in token["data"]:
                    self.parseError("input-element-missing-value-attribute", {"name": token["name"]})
            else:
                
                if not "value" in token["data"] and not token["data"]["type"] == "file":
                    self.parseError("input-element-missing-value-attribute", {"name": token["name"]})
                elif "value" in token["data"] and token["data"]["type"] == "file":
                    self.parseError("illegal-file-input-element-value-attribute", {"name": token["name"]})

                if token["data"]["type"] not in formInputType:
                    self.parseError("invalid-input-element-type-attribute", {"attr": token["data"]["type"]})

            if not "name" in token["data"]:
                self.parseError("input-element-missing-name-attribute", {"name": token["name"]})

            # DECO3801 - Check that input elements have an associated label tag.
            if "id" in token["data"]:
                if not token["data"]["id"] in self.forLabels and not self.tree.openElements[-1].name == "label":
                    self.parseError("input-element-missing-label", {"name": token["name"]})
            else:
                if not self.tree.openElements[-1].name == "label":
                    self.parseError("input-element-missing-label", {"name": token["name"]})

        # DECO3801 - Maintains a list of 'for' attributes which
        # are used to tie label tags to matching input tag IDs.
        if token["type"] == tokenTypes["StartTag"] and token["name"] == "label":
            if "for" in token["data"]:
                self.forLabels.append(token["data"]["for"])

    def normalizedTokens(self):
        for token in self.tokenizer:
            yield self.normalizeToken(token)

    # DECO3801 - Creates a copy of the tokens which remain to be processed
    # after the current token.
    def generateRemainingTokens(self):
        self.remainingTokens = []
        for token in self.tokenizerRemaining:
            self.remainingTokens.append(token)

    def parse(self, stream, encoding=None, parseMeta=True, useChardet=True, files=None, filename=None):
        """Parse a HTML document into a well-formed tree

        stream - a filelike object or string containing the HTML to be parsed

        The optional encoding parameter must be a string that indicates
        the encoding.  If specified, that encoding will be used,
        regardless of any BOM or later declaration (such as in a meta
        element)
        """
        self._parse(stream, innerHTML=False, encoding=encoding,
                    parseMeta=parseMeta, useChardet=useChardet, files=files, filename=filename)
        return self.tree.getDocument()

    def parseFragment(self, stream, container="div", encoding=None,
                      parseMeta=False, useChardet=True):
        """Parse a HTML fragment into a well-formed tree fragment

        container - name of the element we're setting the innerHTML property
        if set to None, default to 'div'

        stream - a filelike object or string containing the HTML to be parsed

        The optional encoding parameter must be a string that indicates
        the encoding.  If specified, that encoding will be used,
        regardless of any BOM or later declaration (such as in a meta
        element)
        """
        self._parse(stream, True, container=container, encoding=encoding)
        return self.tree.getFragment()

    def parseError(self, errorcode="XXX-undefined-error", datavars={}):
        # XXX The idea is to make errorcode mandatory.
        self.errors.append((self.tokenizer.stream.position(), errorcode, datavars))
        if self.strict:
            raise ParseError

    # DECO3801 - Raises a parse error using the position stored within the
    # given token
    def parseErrorWithPos(self, position, errorcode="XXX-undefined-error", datavars={}):
        self.errors.append((position, errorcode, datavars))

    def normalizeToken(self, token):
        """ HTML5 specific normalizations to the token stream """

        if token["type"] == tokenTypes["StartTag"]:
            token["data"] = dict(token["data"][::-1])

        return token

    def adjustMathMLAttributes(self, token):
        replacements = {"definitionurl": "definitionURL"}
        for k, v in replacements.items():
            if k in token["data"]:
                token["data"][v] = token["data"][k]
                del token["data"][k]

    def adjustSVGAttributes(self, token):
        replacements = {
            "attributename": "attributeName",
            "attributetype": "attributeType",
            "basefrequency": "baseFrequency",
            "baseprofile": "baseProfile",
            "calcmode": "calcMode",
            "clippathunits": "clipPathUnits",
            "contentscripttype": "contentScriptType",
            "contentstyletype": "contentStyleType",
            "diffuseconstant": "diffuseConstant",
            "edgemode": "edgeMode",
            "externalresourcesrequired": "externalResourcesRequired",
            "filterres": "filterRes",
            "filterunits": "filterUnits",
            "glyphref": "glyphRef",
            "gradienttransform": "gradientTransform",
            "gradientunits": "gradientUnits",
            "kernelmatrix": "kernelMatrix",
            "kernelunitlength": "kernelUnitLength",
            "keypoints": "keyPoints",
            "keysplines": "keySplines",
            "keytimes": "keyTimes",
            "lengthadjust": "lengthAdjust",
            "limitingconeangle": "limitingConeAngle",
            "markerheight": "markerHeight",
            "markerunits": "markerUnits",
            "markerwidth": "markerWidth",
            "maskcontentunits": "maskContentUnits",
            "maskunits": "maskUnits",
            "numoctaves": "numOctaves",
            "pathlength": "pathLength",
            "patterncontentunits": "patternContentUnits",
            "patterntransform": "patternTransform",
            "patternunits": "patternUnits",
            "pointsatx": "pointsAtX",
            "pointsaty": "pointsAtY",
            "pointsatz": "pointsAtZ",
            "preservealpha": "preserveAlpha",
            "preserveaspectratio": "preserveAspectRatio",
            "primitiveunits": "primitiveUnits",
            "refx": "refX",
            "refy": "refY",
            "repeatcount": "repeatCount",
            "repeatdur": "repeatDur",
            "requiredextensions": "requiredExtensions",
            "requiredfeatures": "requiredFeatures",
            "specularconstant": "specularConstant",
            "specularexponent": "specularExponent",
            "spreadmethod": "spreadMethod",
            "startoffset": "startOffset",
            "stddeviation": "stdDeviation",
            "stitchtiles": "stitchTiles",
            "surfacescale": "surfaceScale",
            "systemlanguage": "systemLanguage",
            "tablevalues": "tableValues",
            "targetx": "targetX",
            "targety": "targetY",
            "textlength": "textLength",
            "viewbox": "viewBox",
            "viewtarget": "viewTarget",
            "xchannelselector": "xChannelSelector",
            "ychannelselector": "yChannelSelector",
            "zoomandpan": "zoomAndPan"
        }
        for originalName in list(token["data"].keys()):
            if originalName in replacements:
                svgName = replacements[originalName]
                token["data"][svgName] = token["data"][originalName]
                del token["data"][originalName]

    def adjustForeignAttributes(self, token):
        replacements = adjustForeignAttributesMap

        for originalName in token["data"].keys():
            if originalName in replacements:
                foreignName = replacements[originalName]
                token["data"][foreignName] = token["data"][originalName]
                del token["data"][originalName]

    def reparseTokenNormal(self, token):
        self.parser.phase()

    def resetInsertionMode(self):
        # The name of this method is mostly historical. (It's also used in the
        # specification.)
        last = False
        newModes = {
            "select": "inSelect",
            "td": "inCell",
            "th": "inCell",
            "tr": "inRow",
            "tbody": "inTableBody",
            "thead": "inTableBody",
            "tfoot": "inTableBody",
            "caption": "inCaption",
            "colgroup": "inColumnGroup",
            "table": "inTable",
            "head": "inBody",
            "body": "inBody",
            "frameset": "inFrameset",
            "html": "beforeHead"
        }
        for node in self.tree.openElements[::-1]:
            nodeName = node.name
            new_phase = None
            if node == self.tree.openElements[0]:
                assert self.innerHTML
                last = True
                nodeName = self.innerHTML
            # Check for conditions that should only happen in the innerHTML
            # case
            if nodeName in ("select", "colgroup", "head", "html"):
                assert self.innerHTML

            if not last and node.namespace != self.tree.defaultNamespace:
                continue

            if nodeName in newModes:
                new_phase = self.phases[newModes[nodeName]]
                break
            elif last:
                new_phase = self.phases["inBody"]
                break

        self.phase = new_phase

    def parseRCDataRawtext(self, token, contentType):
        """Generic RCDATA/RAWTEXT Parsing algorithm
        contentType - RCDATA or RAWTEXT
        """
        assert contentType in ("RAWTEXT", "RCDATA")

        self.tree.insertElement(token)

        if contentType == "RAWTEXT":
            self.tokenizer.state = self.tokenizer.rawtextState
        else:
            self.tokenizer.state = self.tokenizer.rcdataState

        self.originalPhase = self.phase

        self.phase = self.phases["text"]


def getPhases(debug):
    def log(function):
        """Logger that records which phase processes each token"""
        type_names = dict((value, key) for key, value in
                          constants.tokenTypes.items())

        def wrapped(self, *args, **kwargs):
            if function.__name__.startswith("process") and len(args) > 0:
                token = args[0]
                try:
                    info = {"type": type_names[token['type']]}
                except:
                    raise
                if token['type'] in constants.tagTokenTypes:
                    info["name"] = token['name']

                self.parser.log.append((self.parser.tokenizer.state.__name__,
                                        self.parser.phase.__class__.__name__,
                                        self.__class__.__name__,
                                        function.__name__,
                                        info))
                return function(self, *args, **kwargs)
            else:
                return function(self, *args, **kwargs)
        return wrapped

    def getMetaclass(use_metaclass, metaclass_func):
        if use_metaclass:
            return method_decorator_metaclass(metaclass_func)
        else:
            return type

    class Phase(with_metaclass(getMetaclass(debug, log))):
        """Base class for helper object that implements each phase of processing
        """

        def __init__(self, parser, tree):
            self.parser = parser
            self.tree = tree

        def processEOF(self):
            raise NotImplementedError

        def processComment(self, token):
            # For most phases the following is correct. Where it's not it will be
            # overridden.
            self.tree.insertComment(token, self.tree.openElements[-1])

        def processDoctype(self, token):
            self.parser.parseError("unexpected-doctype")

        def processCharacters(self, token):
            self.tree.insertText(token["data"])

        def processSpaceCharacters(self, token):
            self.tree.insertText(token["data"])

        def processStartTag(self, token):
            return self.startTagHandler[token["name"]](token)

        def startTagHtml(self, token):
            if not self.parser.firstStartTag and not token["name"] == "html":
                self.parser.parseError("non-html-root")
            # XXX Need a check here to see if the first start tag token emitted is
            # this token... If it's not, invoke self.parser.parseError().

            # DECO3801 - Checks for a single instance of the html tag.
            if token["name"] == 'html':
                self.parser.singular.append(token["name"])
                if self.parser.singular.count(token["name"]) > 1:
                    self.parser.parseError("multiple-instance-singular-tag", 
                        {"name": token["name"]})

            for attr, value in token["data"].items():
                if attr not in self.tree.openElements[0].attributes:
                    self.tree.openElements[0].attributes[attr] = value
            self.parser.firstStartTag = False

        def processEndTag(self, token):
            return self.endTagHandler[token["name"]](token)

    class InitialPhase(Phase):
        def processSpaceCharacters(self, token):
            pass

        def processComment(self, token):
            self.tree.insertComment(token, self.tree.document)

        def processDoctype(self, token):
            name = token["name"]
            publicId = token["publicId"]
            systemId = token["systemId"]
            correct = token["correct"]

            if (name != "html" or publicId is not None or
                    systemId is not None and systemId != "about:legacy-compat"):
                self.parser.parseError("unknown-doctype")

            if publicId is None:
                publicId = ""

            self.tree.insertDoctype(token)

            if publicId != "":
                publicId = publicId.translate(asciiUpper2Lower)

            if (not correct or token["name"] != "html"
                or publicId.startswith(
                    ("+//silmaril//dtd html pro v0r11 19970101//",
                     "-//advasoft ltd//dtd html 3.0 aswedit + extensions//",
                     "-//as//dtd html 3.0 aswedit + extensions//",
                     "-//ietf//dtd html 2.0 level 1//",
                     "-//ietf//dtd html 2.0 level 2//",
                     "-//ietf//dtd html 2.0 strict level 1//",
                     "-//ietf//dtd html 2.0 strict level 2//",
                     "-//ietf//dtd html 2.0 strict//",
                     "-//ietf//dtd html 2.0//",
                     "-//ietf//dtd html 2.1e//",
                     "-//ietf//dtd html 3.0//",
                     "-//ietf//dtd html 3.2 final//",
                     "-//ietf//dtd html 3.2//",
                     "-//ietf//dtd html 3//",
                     "-//ietf//dtd html level 0//",
                     "-//ietf//dtd html level 1//",
                     "-//ietf//dtd html level 2//",
                     "-//ietf//dtd html level 3//",
                     "-//ietf//dtd html strict level 0//",
                     "-//ietf//dtd html strict level 1//",
                     "-//ietf//dtd html strict level 2//",
                     "-//ietf//dtd html strict level 3//",
                     "-//ietf//dtd html strict//",
                     "-//ietf//dtd html//",
                     "-//metrius//dtd metrius presentational//",
                     "-//microsoft//dtd internet explorer 2.0 html strict//",
                     "-//microsoft//dtd internet explorer 2.0 html//",
                     "-//microsoft//dtd internet explorer 2.0 tables//",
                     "-//microsoft//dtd internet explorer 3.0 html strict//",
                     "-//microsoft//dtd internet explorer 3.0 html//",
                     "-//microsoft//dtd internet explorer 3.0 tables//",
                     "-//netscape comm. corp.//dtd html//",
                     "-//netscape comm. corp.//dtd strict html//",
                     "-//o'reilly and associates//dtd html 2.0//",
                     "-//o'reilly and associates//dtd html extended 1.0//",
                     "-//o'reilly and associates//dtd html extended relaxed 1.0//",
                     "-//softquad software//dtd hotmetal pro 6.0::19990601::extensions to html 4.0//",
                     "-//softquad//dtd hotmetal pro 4.0::19971010::extensions to html 4.0//",
                     "-//spyglass//dtd html 2.0 extended//",
                     "-//sq//dtd html 2.0 hotmetal + extensions//",
                     "-//sun microsystems corp.//dtd hotjava html//",
                     "-//sun microsystems corp.//dtd hotjava strict html//",
                     "-//w3c//dtd html 3 1995-03-24//",
                     "-//w3c//dtd html 3.2 draft//",
                     "-//w3c//dtd html 3.2 final//",
                     "-//w3c//dtd html 3.2//",
                     "-//w3c//dtd html 3.2s draft//",
                     "-//w3c//dtd html 4.0 frameset//",
                     "-//w3c//dtd html 4.0 transitional//",
                     "-//w3c//dtd html experimental 19960712//",
                     "-//w3c//dtd html experimental 970421//",
                     "-//w3c//dtd w3 html//",
                     "-//w3o//dtd w3 html 3.0//",
                     "-//webtechs//dtd mozilla html 2.0//",
                     "-//webtechs//dtd mozilla html//"))
                or publicId in
                    ("-//w3o//dtd w3 html strict 3.0//en//",
                     "-/w3c/dtd html 4.0 transitional/en",
                     "html")
                or publicId.startswith(
                    ("-//w3c//dtd html 4.01 frameset//",
                     "-//w3c//dtd html 4.01 transitional//")) and
                    systemId is None
                    or systemId and systemId.lower() == "http://www.ibm.com/data/dtd/v11/ibmxhtml1-transitional.dtd"):
                self.parser.compatMode = "quirks"
            elif (publicId.startswith(
                    ("-//w3c//dtd xhtml 1.0 frameset//",
                     "-//w3c//dtd xhtml 1.0 transitional//"))
                  or publicId.startswith(
                      ("-//w3c//dtd html 4.01 frameset//",
                       "-//w3c//dtd html 4.01 transitional//")) and
                  systemId is not None):
                self.parser.compatMode = "limited quirks"

            self.parser.phase = self.parser.phases["beforeHtml"]

        def anythingElse(self):
            self.parser.compatMode = "quirks"
            self.parser.phase = self.parser.phases["beforeHtml"]

        def processCharacters(self, token):
            self.parser.parseError("expected-doctype-but-got-chars")
            self.anythingElse()
            return token

        def processStartTag(self, token):
            self.parser.parseError("expected-doctype-but-got-start-tag",
                                   {"name": token["name"]})
            self.anythingElse()
            return token

        def processEndTag(self, token):
            self.parser.parseError("expected-doctype-but-got-end-tag",
                                   {"name": token["name"]})
            self.anythingElse()
            return token

        def processEOF(self):
            self.parser.parseError("expected-doctype-but-got-eof")
            self.anythingElse()
            return True

    class BeforeHtmlPhase(Phase):
        # DECO3801 - Restructured the phase to comply with the 
        # format used for other phases. Added start and end tag
        # handler methods to detect invalid tags before the starting
        # HTML tag.
        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)

            self.startTagHandler = utils.MethodDispatcher([
                ("html", self.startTagHtml)
            ])
            self.startTagHandler.default = self.startTagOther

            self.endTagHandler = utils.MethodDispatcher([])
            self.endTagHandler.default = self.endTagOther
        
        # helper methods
        def insertHtmlElement(self):
            self.tree.insertRoot(impliedTagToken("html", "StartTag"))
            self.parser.phase = self.parser.phases["beforeHead"]

        # other
        def processEOF(self):
            #self.insertHtmlElement()
            return False

        def processComment(self, token):
            self.tree.insertComment(token, self.tree.document)

        def processSpaceCharacters(self, token):
            pass

        def processCharacters(self, token):
            #self.insertHtmlElement()
            #return token
            pass

        # DECO3801 - Starting HTML tag handler method.
        def startTagHtml(self, token):
            self.parser.firstStartTag = True
            self.tree.insertRoot(token)
            self.parser.singular.append(token["name"])
            self.parser.phase = self.parser.phases["beforeHead"]

        # DECO3801 - Start tag handler method.
        def startTagOther(self, token):
            self.parser.parseError("start-tag-before-starting-html", {"name": token["name"]})

        # DECO3801 - Replaced with proper start tag checking.
        #def processStartTag(self, token):
        #    if token["name"] == "html":
        #        self.parser.firstStartTag = True
        #    self.insertHtmlElement()
        #    return token

        # DECO3801 - Closing tag hangler method.
        def endTagOther(self, token):
            self.parser.parseError("end-tag-before-starting-html", {"name": token["name"]})

        # DECO3801 - Replaced with proper closing tag checking.
        #def processEndTag(self, token):
        #    if token["name"] not in ("head", "body", "html", "br"):
        #        self.parser.parseError("unexpected-end-tag-before-html",
        #                               {"name": token["name"]})
        #    else:
        #        self.insertHtmlElement()
        #        return token

    class BeforeHeadPhase(Phase):
        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)

            self.startTagHandler = utils.MethodDispatcher([
                ("html", self.startTagHtml),
                ("head", self.startTagHead)
            ])
            self.startTagHandler.default = self.startTagOther

            self.endTagHandler = utils.MethodDispatcher([
                ("br", self.endTagImplyHead),
                # DECO3801 - Closing HTML tag handler.
                ("html", self.endTagHtml)
            ])
            self.endTagHandler.default = self.endTagOther

        def processEOF(self):
            #self.startTagHead(impliedTagToken("head", "StartTag"))
            return False

        def processSpaceCharacters(self, token):
            pass

        def processCharacters(self, token):
            #self.startTagHead(impliedTagToken("head", "StartTag"))
            #return token
            pass

        def startTagHtml(self, token):
            return self.parser.phases["inBody"].processStartTag(token)

        def startTagHead(self, token):
            self.parser.singular.append(token["name"])
            self.tree.insertElement(token)
            self.tree.headPointer = self.tree.openElements[-1]
            self.parser.phase = self.parser.phases["inHead"]

        def startTagOther(self, token):
            # DEO3801 - Check that the document contains an opening head tag.
            # If not, the head opening and closing tags are added and the 
            # phase is advanced to the afterHead phase.

            hasHeadStart = False
            for remaining in self.parser.remainingTokens:
                if remaining.get('name') == "head" and remaining.get('type') == tokenTypes["StartTag"]:
                    hasHeadStart = True

            if hasHeadStart:
                self.parser.parseError("incorrect-start-tag-placement-before-head",
                                   {"name": token["name"]})
            else:
                self.parser.parseError("head-start-tag-missing",
                                   {"name": token["name"]})
                #self.startTagHead(impliedTagToken("head", "StartTag")) 
                #self.parser.phases["inHead"].endTagHead(impliedTagToken("head"))
                self.parser.phase = self.parser.phases["afterHead"]
                return token
            

        def endTagImplyHead(self, token):
            #self.startTagHead(impliedTagToken("head", "StartTag"))
            return token

        def endTagOther(self, token):
            # DECO3801 - Error check for invalid end tags appearing
            # before the head section of the document.
            # Old:
            # self.parser.parseError("end-tag-after-implied-root",
            #                        {"name": token["name"]})
            self.parser.parseError("incorrect-end-tag-placement-before-head",
                                   {"name": token["name"]})

        # DECO3801 - Error checking for a closing HTML tag occuring before
        # the starting head tag. If no other closing HTML tag is found
        # after this instance, the current closing HTML tag is considered
        # the closing tag for the document and any tags occuring after it
        # will be reported as errors.
        def endTagHtml(self, token):
            hasClosingHtml = False
            self.parser.singularEndTags.append(token["name"])
            for remaining in self.parser.remainingTokens:
                if remaining.get('name') == "html" and remaining.get('type') == tokenTypes["EndTag"]:
                    hasClosingHtml = True

            if hasClosingHtml:
                self.parser.parseError("incorrect-placement-html-end-tag",
                                   {"name": token["name"]})
            else:
                # DECO3801 - Redirects to the after body phase, causing all
                # remaining tags to be treated as being misplaced.
                self.parser.parseError("early-termination-before-head",
                                   {"name": token["name"]})
                self.parser.phase = self.parser.phases["afterBody"]
                return token

    class InHeadPhase(Phase):
        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)

            self.startTagHandler = utils.MethodDispatcher([
                ("html", self.startTagHtml),
                ("title", self.startTagTitle),
                (("noscript", "noframes", "style"), self.startTagNoScriptNoFramesStyle),
                ("script", self.startTagScript),
                (("base", "basefont", "bgsound", "command", "link"),
                 self.startTagBaseLinkCommand),
                ("meta", self.startTagMeta),
                ("head", self.startTagHead),
            ])
            self.startTagHandler.default = self.startTagOther

            self. endTagHandler = utils.MethodDispatcher([
                ("head", self.endTagHead),
                # DECO3801 - HTML end tag check. Old end tag check removed
                # due to original error checking conflicting with our check.
                # Old:
                # (("br", "html", "body"), self.endTagHtmlBodyBr)
                ("html", self.endTagHtml),
            ])
            self.endTagHandler.default = self.endTagOther

        # the real thing
        def processEOF(self):
            self.anythingElse()
            return True

        def processCharacters(self, token):
            self.anythingElse()
            return token

        def startTagHtml(self, token):
            return self.parser.phases["inBody"].processStartTag(token)

        def startTagHead(self, token):
            # DECO3801 - Multiple head tags found, throws singular tag
            # error. Replaced original error message.
            # Old: self.parser.parseError("two-heads-are-not-better-than-one")
            self.parser.parseError("multiple-instance-singular-tag", 
                        {"name": token["name"]})

        def startTagBaseLinkCommand(self, token):
            self.tree.insertElement(token)
            self.tree.openElements.pop()
            token["selfClosingAcknowledged"] = True

        def startTagMeta(self, token):
            self.tree.insertElement(token)
            self.tree.openElements.pop()
            token["selfClosingAcknowledged"] = True

            attributes = token["data"]
            if self.parser.tokenizer.stream.charEncoding[1] == "tentative":
                if "charset" in attributes:
                    self.parser.tokenizer.stream.changeEncoding(attributes["charset"])
                elif ("content" in attributes and
                      "http-equiv" in attributes and
                      attributes["http-equiv"].lower() == "content-type"):
                    # Encoding it as UTF-8 here is a hack, as really we should pass
                    # the abstract Unicode string, and just use the
                    # ContentAttrParser on that, but using UTF-8 allows all chars
                    # to be encoded and as a ASCII-superset works.
                    data = inputstream.EncodingBytes(attributes["content"].encode("utf-8"))
                    parser = inputstream.ContentAttrParser(data)
                    codec = parser.parse()
                    self.parser.tokenizer.stream.changeEncoding(codec)

        def startTagTitle(self, token):
            # DECO3801 - Check for multiple title tags appearing in the head section.
            if self.parser.hasTitle:
                self.parser.parseError("duplicate-title-in-head", {"name": token["name"]})
            self.parser.hasTitle = True
            self.parser.parseRCDataRawtext(token, "RCDATA")

        def startTagNoScriptNoFramesStyle(self, token):
            # Need to decide whether to implement the scripting-disabled case
            self.parser.parseRCDataRawtext(token, "RAWTEXT")

        def startTagScript(self, token):
            self.tree.insertElement(token)
            self.parser.tokenizer.state = self.parser.tokenizer.scriptDataState
            self.parser.originalPhase = self.parser.phase
            self.parser.phase = self.parser.phases["text"]

        def startTagOther(self, token):
            # DECO3801 TODO: Error checking for start tags in wrong section.
            # Old:
            # self.anythingElse()
            # return token
            self.parser.parseError("incorrect-start-tag-placement-in-head",
                                   {"name": token["name"]})

        # DECO3801 - Checks if the body tag found comes before a closing
        # head tag. If no closing head tag is found, a closing tag is inserted
        # and the parsing loop enters the body phase. Otherwise, the starting body
        # tag is reported as a misplaced body tag and the in head processing continues.
        def startTagBody(self, token):
            hasClosing = False
            for remaining in self.parser.remainingTokens:
                if remaining.get('name') == "head" and remaining.get('type') == tokenTypes["EndTag"]:
                    hasClosing = True

            if hasClosing:
                self.parser.parseError("incorrect-placement-singular-tag",
                                   {"name": token["name"]})
            else:
                self.parser.parseError("head-end-tag-missing",
                                   {"name": token["name"]})
                self.endTagHead(impliedTagToken("head"))
                self.parser.phase = self.parser.phases["afterHead"]
                return token

        def endTagHead(self, token):
            self.parser.singularEndTags.append(token["name"])
            node = self.parser.tree.openElements.pop()
            assert node.name == "head", "Expected head got %s" % node.name
            self.parser.phase = self.parser.phases["afterHead"]

        def endTagHtmlBodyBr(self, token):
            self.anythingElse()
            return token

        def endTagOther(self, token):
            self.parser.parseError("incorrect-end-tag-placement-in-head", {"name": token["name"]})

        def anythingElse(self):
            self.endTagHead(impliedTagToken("head"))

        # DECO3801 - Error checking for a closing HTML tag occuring inside
        # the head tags. If no other closing HTML tag is found
        # after this instance, the current closing HTML tag is considered
        # the closing tag for the document and any tags occuring after it
        # will be reported as errors.
        def endTagHtml(self, token):
            hasClosingHtml = False
            self.parser.singularEndTags.append(token["name"])
            for remaining in self.parser.remainingTokens:
                if remaining.get('name') == "html" and remaining.get('type') == tokenTypes["EndTag"]:
                    hasClosingHtml = True

            if hasClosingHtml:
                self.parser.parseError("incorrect-placement-html-end-tag",
                                   {"name": token["name"]})
            else:
                # DECO3801 - Redirects to the after body phase, causing all
                # remaining tags to be treated as being misplaced.
                self.parser.parseError("early-termination-in-head",
                                   {"name": token["name"]})
                self.parser.phase = self.parser.phases["afterBody"]
                return token

    # XXX If we implement a parser for which scripting is disabled we need to
    # implement this phase.
    #
    # class InHeadNoScriptPhase(Phase):
    class AfterHeadPhase(Phase):
        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)

            self.startTagHandler = utils.MethodDispatcher([
                ("html", self.startTagHtml),
                ("body", self.startTagBody),
                ("frameset", self.startTagFrameset),
                (("base", "basefont", "bgsound", "link", "meta", "noframes", "script",
                  "style", "title"),
                 self.startTagFromHead),
                ("head", self.startTagHead)
            ])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = utils.MethodDispatcher([
                (("body"), self.endTagBody),
                # DECO3801 - Handler methods for head and html end tags.
                ("head", self.endTagHead),
                ("html", self.endTagHtml),
            ])
            self.endTagHandler.default = self.endTagOther

        def processEOF(self):
            # DECO3801 - Replaced the original implementation
            # to reflect the removal of the original insertion of
            # tags which has been replaced with our error checks.
            # If the parser reaches here, the document doesn't contain
            # an expected body phase.
            # OLD: 
            # self.anythingElse()
            # return True
            return False

        def processCharacters(self, token):
            # DECO3801 - Replaced with error. Prevents shift to in-body
            # phase.
            # Old:
            # self.anythingElse()
            # return token
            # TODO: Correct the error message.
            self.parser.parseError("placeholder-type")

        def startTagHtml(self, token):
            # DECO3801 - Replaced shift to in-body phase with correct
            # error checking.
            # Old:
            # return self.parser.phases["inBody"].processStartTag(token)
            self.parser.parseError("incorrect-placement-singular-tag", 
                {"name": token["name"]})

        def startTagBody(self, token):
            self.parser.framesetOK = False
            self.tree.insertElement(token)
            self.parser.singular.append(token["name"])
            self.parser.phase = self.parser.phases["inBody"]

        def startTagFrameset(self, token):
            self.tree.insertElement(token)
            self.parser.phase = self.parser.phases["inFrameset"]

        def startTagFromHead(self, token):
            self.parser.parseError("unexpected-start-tag-out-of-my-head",
                                   {"name": token["name"]})
            self.tree.openElements.append(self.tree.headPointer)
            self.parser.phases["inHead"].processStartTag(token)
            for node in self.tree.openElements[::-1]:
                if node.name == "head":
                    self.tree.openElements.remove(node)
                    break

        def startTagHead(self, token):
            # DECO3801 - Check for a head start tag appearing after an initial
            # head block.
            # Old: self.parser.parseError("unexpected-start-tag", {"name": token["name"]})
            self.parser.parseError("multiple-instance-singular-tag", 
                        {"name": token["name"]})

        def startTagOther(self, token):
            # DECO3801 - Report start tags occuring after the head section
            # and before the body section as being misplaced.
            self.parser.parseError("start-tag-before-body-after-head", 
                {"name": token["name"]})

        # DECO3801 - Handler method for head end tags after a completed head
        # block.
        def endTagHead(self, token):
            self.parser.parseError("incorrect-placement-singular-end-tag", 
                {"name": token["name"]})

        def endTagBody(self, token):
            self.parser.parseError("incorrect-placement-singular-end-tag", 
                {"name": token["name"]})

        def endTagOther(self, token):
            self.parser.parseError("end-tag-before-body-after-head", {"name": token["name"]})

        # DECO3801 - Removed as the original functionality of this phase
        # has been revamped.
        # Old:
        # def anythingElse(self):
        #     self.tree.insertElement(impliedTagToken("body", "StartTag"))
        #     self.parser.phase = self.parser.phases["inBody"]
        #     self.parser.framesetOK = True

        # DECO3801 - Error checking for a closing HTML tag occuring before
        # the body section. If no other closing HTML tag is found
        # after this instance, the current closing HTML tag is considered
        # the closing tag for the document and any tags occuring after it
        # will be reported as errors.
        def endTagHtml(self, token):
            hasClosingHtml = False
            self.parser.singularEndTags.append(token["name"])
            for remaining in self.parser.remainingTokens:
                if remaining.get('name') == "html" and remaining.get('type') == tokenTypes["EndTag"]:
                    hasClosingHtml = True

            if hasClosingHtml:
                self.parser.parseError("incorrect-placement-html-end-tag",
                                   {"name": token["name"]})
            else:
                # DECO3801 - Redirects to the after body phase, causing all
                # remaining tags to be treated as being misplaced.
                self.parser.parseError("early-termination-before-body",
                                   {"name": token["name"]})
                self.parser.phase = self.parser.phases["afterBody"]
                return token

    class InBodyPhase(Phase):
        # http://www.whatwg.org/specs/web-apps/current-work/#parsing-main-inbody
        # the really-really-really-very crazy mode
        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)

            # Keep a ref to this for special handling of whitespace in <pre>
            self.processSpaceCharactersNonPre = self.processSpaceCharacters

            self.startTagHandler = utils.MethodDispatcher([
                ("html", self.startTagHtml),
                (("base", "basefont", "bgsound", "command", "link", "meta",
                  "noframes", "script", "style", "title"),
                 self.startTagProcessInHead),
                ("body", self.startTagBody),
                ("frameset", self.startTagFrameset),
                (("address", "article", "aside", "blockquote", "center", "details",
                  "details", "dir", "div", "dl", "fieldset", "figcaption", "figure",
                  "header", "hgroup", "main", "menu", "nav", "ol", "p",
                  "section", "summary", "ul"),
                 self.startTagCloseP),
                ("footer", self.startTagFooter),
                (headingElements, self.startTagHeading),
                (("pre", "listing"), self.startTagPreListing),
                ("form", self.startTagForm),
                (("li", "dd", "dt"), self.startTagListItem),
                ("plaintext", self.startTagPlaintext),
                ("a", self.startTagA),
                (("b", "big", "code", "em", "font", "i", "s", "small", "strike",
                  "strong", "tt", "u"), self.startTagFormatting),
                ("nobr", self.startTagNobr),
                ("button", self.startTagButton),
                (("applet", "marquee", "object"), self.startTagAppletMarqueeObject),
                ("xmp", self.startTagXmp),
                ("table", self.startTagTable),
                (("area", "br", "embed", "img", "keygen", "wbr"),
                 self.startTagVoidFormatting),
                (("param", "source", "track"), self.startTagParamSource),
                ("input", self.startTagInput),
                ("hr", self.startTagHr),
                ("image", self.startTagImage),
                ("isindex", self.startTagIsIndex),
                ("textarea", self.startTagTextarea),
                ("iframe", self.startTagIFrame),
                (("noembed", "noframes", "noscript"), self.startTagRawtext),
                ("select", self.startTagSelect),
                (("rp", "rt"), self.startTagRpRt),
                (("option", "optgroup"), self.startTagOpt),
                (("math"), self.startTagMath),
                (("svg"), self.startTagSvg),
                (("caption", "col", "colgroup",
                  "tbody", "td", "tfoot", "th", "thead",
                  "tr"), self.startTagMisplaced),
                # DECO3801 - Error check for head start tags found within the main
                # body section.
                ("head", self.startTagHead)
            ])
            self.startTagHandler.default = self.startTagOther

            self.endTagHandler = utils.MethodDispatcher([
                ("body", self.endTagBody),
                ("html", self.endTagHtml),
                (("address", "article", "aside", "blockquote", "button", "center",
                  "details", "dialog", "dir", "div", "dl", "fieldset", "figcaption", "figure",
                  "header", "hgroup", "listing", "main", "menu", "nav", "ol", "pre",
                  "section", "summary", "ul"), self.endTagBlock),
                ("footer", self.endTagFooter),
                ("form", self.endTagForm),
                ("p", self.endTagP),
                (("dd", "dt", "li"), self.endTagListItem),
                (headingElements, self.endTagHeading),
                (("a", "b", "big", "code", "em", "font", "i", "nobr", "s", "small",
                  "strike", "strong", "tt", "u"), self.endTagFormatting),
                (("applet", "marquee", "object"), self.endTagAppletMarqueeObject),
                ("br", self.endTagBr),
            ])
            self.endTagHandler.default = self.endTagOther

        def isMatchingFormattingElement(self, node1, node2):
            if node1.name != node2.name or node1.namespace != node2.namespace:
                return False
            elif len(node1.attributes) != len(node2.attributes):
                return False
            else:
                attributes1 = sorted(node1.attributes.items())
                attributes2 = sorted(node2.attributes.items())
                for attr1, attr2 in zip(attributes1, attributes2):
                    if attr1 != attr2:
                        return False
            return True

        # helper
        def addFormattingElement(self, token):
            self.tree.insertElement(token)
            element = self.tree.openElements[-1]

            matchingElements = []
            for node in self.tree.activeFormattingElements[::-1]:
                if node is Marker:
                    break
                elif self.isMatchingFormattingElement(node, element):
                    matchingElements.append(node)

            assert len(matchingElements) <= 3
            if len(matchingElements) == 3:
                self.tree.activeFormattingElements.remove(matchingElements[-1])
            self.tree.activeFormattingElements.append(element)

        # the real deal
        def processEOF(self):
            allowed_elements = frozenset(("dd", "dt", "li", "p", "tbody", "td",
                                          "tfoot", "th", "thead", "tr", "body",
                                          "html"))
            for node in self.tree.openElements[::-1]:
                if node.name not in allowed_elements:
                    self.parser.parseError("expected-closing-tag-but-got-eof")
                    break
            # Stop parsing

        def processSpaceCharactersDropNewline(self, token):
            # Sometimes (start of <pre>, <listing>, and <textarea> blocks) we
            # want to drop leading newlines
            data = token["data"]
            self.processSpaceCharacters = self.processSpaceCharactersNonPre
            if (data.startswith("\n") and
                self.tree.openElements[-1].name in ("pre", "listing", "textarea")
                    and not self.tree.openElements[-1].hasContent()):
                data = data[1:]
            if data:
                self.tree.reconstructActiveFormattingElements()
                self.tree.insertText(data)

        def processCharacters(self, token):
            if token["data"] == "\u0000":
                # The tokenizer should always emit null on its own
                return
            self.tree.reconstructActiveFormattingElements()
            self.tree.insertText(token["data"])
            # This must be bad for performance
            if (self.parser.framesetOK and
                any([char not in spaceCharacters
                     for char in token["data"]])):
                self.parser.framesetOK = False

        def processSpaceCharacters(self, token):
            self.tree.reconstructActiveFormattingElements()
            self.tree.insertText(token["data"])

        def startTagProcessInHead(self, token):
            return self.parser.phases["inHead"].processStartTag(token)

        def startTagBody(self, token):
            # DECO3801 - Removed old error message. Replaced with singular
            # tag error (body).
            # Old: self.parser.parseError("unexpected-start-tag", {"name": "body"})
            self.parser.parseError("multiple-instance-singular-tag", 
                        {"name": token["name"]})

            if (len(self.tree.openElements) == 1
                    or self.tree.openElements[1].name != "body"):
                assert self.parser.innerHTML
            else:
                self.parser.framesetOK = False
                for attr, value in token["data"].items():
                    if attr not in self.tree.openElements[1].attributes:
                        self.tree.openElements[1].attributes[attr] = value

        def startTagFrameset(self, token):
            self.parser.parseError("unexpected-start-tag", {"name": "frameset"})
            if (len(self.tree.openElements) == 1 or self.tree.openElements[1].name != "body"):
                assert self.parser.innerHTML
            elif not self.parser.framesetOK:
                pass
            else:
                if self.tree.openElements[1].parent:
                    self.tree.openElements[1].parent.removeChild(self.tree.openElements[1])
                while self.tree.openElements[-1].name != "html":
                    self.tree.openElements.pop()
                self.tree.insertElement(token)
                self.parser.phase = self.parser.phases["inFrameset"]

        def startTagCloseP(self, token):
            if self.tree.elementInScope("p", variant="button"):
                self.endTagP(impliedTagToken("p"))
            self.tree.insertElement(token)

        # DECO3801 - Handler method which checks that no more than one
        # instance of the footer tag is in use.
        def startTagFooter(self, token):
            self.parser.singular.append(token["name"])
            if self.parser.singular.count(token["name"]) > 1:
                self.parser.parseError("multiple-instance-singular-tag", 
                    {"name": token["name"]})
            else:
                if not self.parser.tree.openElements[-1].name == "body":
                    self.parser.parseError("missing-end-tag-before-footer", {"name": self.parser.tree.openElements[-1].name})

                self.tree.insertElement(token)

        def startTagPreListing(self, token):
            if self.tree.elementInScope("p", variant="button"):
                self.endTagP(impliedTagToken("p"))
            self.tree.insertElement(token)
            self.parser.framesetOK = False
            self.processSpaceCharacters = self.processSpaceCharactersDropNewline

        def startTagForm(self, token):
            if self.tree.formPointer:
                self.parser.parseError("unexpected-start-tag", {"name": "form"})
            else:
                if self.tree.elementInScope("p", variant="button"):
                    self.endTagP(impliedTagToken("p"))
                self.tree.insertElement(token)
                self.tree.formPointer = self.tree.openElements[-1]

        def startTagListItem(self, token):
            self.parser.framesetOK = False

            stopNamesMap = {"li": ["li"],
                            "dt": ["dt", "dd"],
                            "dd": ["dt", "dd"]}
            stopNames = stopNamesMap[token["name"]]
            for node in reversed(self.tree.openElements):
                if node.name in stopNames:
                    self.parser.phase.processEndTag(
                        impliedTagToken(node.name, "EndTag"))
                    break
                if (node.nameTuple in specialElements and
                        node.name not in ("address", "div", "p")):
                    break

            if self.tree.elementInScope("p", variant="button"):
                self.parser.phase.processEndTag(
                    impliedTagToken("p", "EndTag"))

            self.tree.insertElement(token)

        def startTagPlaintext(self, token):
            if self.tree.elementInScope("p", variant="button"):
                self.endTagP(impliedTagToken("p"))
            self.tree.insertElement(token)
            self.parser.tokenizer.state = self.parser.tokenizer.plaintextState

        def startTagHeading(self, token):
            if self.tree.elementInScope("p", variant="button"):
                self.endTagP(impliedTagToken("p"))
            if self.tree.openElements[-1].name in headingElements:
                self.parser.parseError("unexpected-start-tag", {"name": token["name"]})
                self.tree.openElements.pop()
            self.tree.insertElement(token)

        def startTagA(self, token):
            afeAElement = self.tree.elementInActiveFormattingElements("a")
            if afeAElement:
                self.parser.parseError("unexpected-start-tag-implies-end-tag",
                                       {"startName": "a", "endName": "a"})
                self.endTagFormatting(impliedTagToken("a"))
                if afeAElement in self.tree.openElements:
                    self.tree.openElements.remove(afeAElement)
                if afeAElement in self.tree.activeFormattingElements:
                    self.tree.activeFormattingElements.remove(afeAElement)
            self.tree.reconstructActiveFormattingElements()
            self.addFormattingElement(token)

        def startTagFormatting(self, token):
            self.tree.reconstructActiveFormattingElements()
            self.addFormattingElement(token)

        def startTagNobr(self, token):
            self.tree.reconstructActiveFormattingElements()
            if self.tree.elementInScope("nobr"):
                self.parser.parseError("unexpected-start-tag-implies-end-tag",
                                       {"startName": "nobr", "endName": "nobr"})
                self.processEndTag(impliedTagToken("nobr"))
                # XXX Need tests that trigger the following
                self.tree.reconstructActiveFormattingElements()
            self.addFormattingElement(token)

        def startTagButton(self, token):
            if self.tree.elementInScope("button"):
                self.parser.parseError("unexpected-start-tag-implies-end-tag",
                                       {"startName": "button", "endName": "button"})
                self.processEndTag(impliedTagToken("button"))
                return token
            else:
                self.tree.reconstructActiveFormattingElements()
                self.tree.insertElement(token)
                self.parser.framesetOK = False

        def startTagAppletMarqueeObject(self, token):
            self.tree.reconstructActiveFormattingElements()
            self.tree.insertElement(token)
            self.tree.activeFormattingElements.append(Marker)
            self.parser.framesetOK = False

        def startTagXmp(self, token):
            if self.tree.elementInScope("p", variant="button"):
                self.endTagP(impliedTagToken("p"))
            self.tree.reconstructActiveFormattingElements()
            self.parser.framesetOK = False
            self.parser.parseRCDataRawtext(token, "RAWTEXT")

        def startTagTable(self, token):
            if self.parser.compatMode != "quirks":
                if self.tree.elementInScope("p", variant="button"):
                    self.processEndTag(impliedTagToken("p"))
            self.tree.insertElement(token)
            self.parser.framesetOK = False
            self.parser.phase = self.parser.phases["inTable"]

        def startTagVoidFormatting(self, token):
            self.tree.reconstructActiveFormattingElements()
            self.tree.insertElement(token)
            self.tree.openElements.pop()
            token["selfClosingAcknowledged"] = True
            self.parser.framesetOK = False

        def startTagInput(self, token):
            framesetOK = self.parser.framesetOK
            self.startTagVoidFormatting(token)
            if ("type" in token["data"] and
                    token["data"]["type"].translate(asciiUpper2Lower) == "hidden"):
                # input type=hidden doesn't change framesetOK
                self.parser.framesetOK = framesetOK

        def startTagParamSource(self, token):
            self.tree.insertElement(token)
            self.tree.openElements.pop()
            token["selfClosingAcknowledged"] = True

        def startTagHr(self, token):
            if self.tree.elementInScope("p", variant="button"):
                self.endTagP(impliedTagToken("p"))
            self.tree.insertElement(token)
            self.tree.openElements.pop()
            token["selfClosingAcknowledged"] = True
            self.parser.framesetOK = False

        def startTagImage(self, token):
            # No really...
            self.parser.parseError("unexpected-start-tag-treated-as",
                                   {"originalName": "image", "newName": "img"})
            self.processStartTag(impliedTagToken("img", "StartTag",
                                                 attributes=token["data"],
                                                 selfClosing=token["selfClosing"]))

        def startTagIsIndex(self, token):
            self.parser.parseError("deprecated-tag", {"name": "isindex"})
            if self.tree.formPointer:
                return
            form_attrs = {}
            if "action" in token["data"]:
                form_attrs["action"] = token["data"]["action"]
            self.processStartTag(impliedTagToken("form", "StartTag",
                                                 attributes=form_attrs))
            self.processStartTag(impliedTagToken("hr", "StartTag"))
            self.processStartTag(impliedTagToken("label", "StartTag"))
            # XXX Localization ...
            if "prompt" in token["data"]:
                prompt = token["data"]["prompt"]
            else:
                prompt = "This is a searchable index. Enter search keywords: "
            self.processCharacters(
                {"type": tokenTypes["Characters"], "data": prompt})
            attributes = token["data"].copy()
            if "action" in attributes:
                del attributes["action"]
            if "prompt" in attributes:
                del attributes["prompt"]
            attributes["name"] = "isindex"
            self.processStartTag(impliedTagToken("input", "StartTag",
                                                 attributes=attributes,
                                                 selfClosing=
                                                 token["selfClosing"]))
            self.processEndTag(impliedTagToken("label"))
            self.processStartTag(impliedTagToken("hr", "StartTag"))
            self.processEndTag(impliedTagToken("form"))

        def startTagTextarea(self, token):
            self.tree.insertElement(token)
            self.parser.tokenizer.state = self.parser.tokenizer.rcdataState
            self.processSpaceCharacters = self.processSpaceCharactersDropNewline
            self.parser.framesetOK = False

        def startTagIFrame(self, token):
            self.parser.framesetOK = False
            self.startTagRawtext(token)

        def startTagRawtext(self, token):
            """iframe, noembed noframes, noscript(if scripting enabled)"""
            self.parser.parseRCDataRawtext(token, "RAWTEXT")

        def startTagOpt(self, token):
            if self.tree.openElements[-1].name == "option":
                self.parser.phase.processEndTag(impliedTagToken("option"))
            self.tree.reconstructActiveFormattingElements()
            self.parser.tree.insertElement(token)

        def startTagSelect(self, token):
            self.tree.reconstructActiveFormattingElements()
            self.tree.insertElement(token)
            self.parser.framesetOK = False
            if self.parser.phase in (self.parser.phases["inTable"],
                                     self.parser.phases["inCaption"],
                                     self.parser.phases["inColumnGroup"],
                                     self.parser.phases["inTableBody"],
                                     self.parser.phases["inRow"],
                                     self.parser.phases["inCell"]):
                self.parser.phase = self.parser.phases["inSelectInTable"]
            else:
                self.parser.phase = self.parser.phases["inSelect"]

        def startTagRpRt(self, token):
            if self.tree.elementInScope("ruby"):
                self.tree.generateImpliedEndTags()
                if self.tree.openElements[-1].name != "ruby":
                    self.parser.parseError()
            self.tree.insertElement(token)

        def startTagMath(self, token):
            self.tree.reconstructActiveFormattingElements()
            self.parser.adjustMathMLAttributes(token)
            self.parser.adjustForeignAttributes(token)
            token["namespace"] = namespaces["mathml"]
            self.tree.insertElement(token)
            # Need to get the parse error right for the case where the token
            # has a namespace not equal to the xmlns attribute
            if token["selfClosing"]:
                self.tree.openElements.pop()
                token["selfClosingAcknowledged"] = True

        def startTagSvg(self, token):
            self.tree.reconstructActiveFormattingElements()
            self.parser.adjustSVGAttributes(token)
            self.parser.adjustForeignAttributes(token)
            token["namespace"] = namespaces["svg"]
            self.tree.insertElement(token)
            # Need to get the parse error right for the case where the token
            # has a namespace not equal to the xmlns attribute
            if token["selfClosing"]:
                self.tree.openElements.pop()
                token["selfClosingAcknowledged"] = True

        def startTagMisplaced(self, token):
            """ Elements that should be children of other elements that have a
            different insertion mode; here they are ignored
            "caption", "col", "colgroup", "frame", "frameset", "head",
            "option", "optgroup", "tbody", "td", "tfoot", "th", "thead",
            "tr", "noscript"
            """
            self.parser.parseError("unexpected-start-tag-ignored", {"name": token["name"]})

        # DECO3801 - Error check for head start tag occurring within the body
        # section.
        def startTagHead(self, token):
            self.parser.parseError("incorrect-placement-singular-tag",
                {"name": token["name"]})

        def startTagOther(self, token):
            self.tree.reconstructActiveFormattingElements()
            self.tree.insertElement(token)

        def endTagP(self, token):
            if not self.tree.elementInScope("p", variant="button"):
                self.startTagCloseP(impliedTagToken("p", "StartTag"))
                self.parser.parseError("unexpected-end-tag", {"name": "p"})
                self.endTagP(impliedTagToken("p", "EndTag"))
            else:
                self.tree.generateImpliedEndTags("p")
                if self.tree.openElements[-1].name != "p":
                    self.parser.parseError("unexpected-end-tag", {"name": "p"})
                node = self.tree.openElements.pop()
                while node.name != "p":
                    node = self.tree.openElements.pop()

        def endTagBody(self, token):
            if not self.tree.elementInScope("body"):
                self.parser.parseError()
                return
            elif self.tree.openElements[-1].name != "body":
                for node in self.tree.openElements[2:]:
                    # DECO3801 - Added 'footer' to the frozenset to prevent
                    # a false positive during checking of incorrect footer end
                    # tag placement.
                    if node.name not in frozenset(("dd", "dt", "li", "optgroup",
                                                   "option", "p", "rp", "rt",
                                                   "tbody", "td", "tfoot",
                                                   "th", "thead", "tr", "body",
                                                   "html", "footer")):
                        # Not sure this is the correct name for the parse error
                        self.parser.parseError(
                            "expected-one-end-tag-but-got-another",
                            {"expectedName": "body", "gotName": node.name})
                        break
            self.parser.singularEndTags.append(token["name"])
            self.parser.phase = self.parser.phases["afterBody"]

        # DECO3801 - Error checking for a closing HTML tag occuring before
        # the body section. If no other closing HTML tag is found
        # after this instance, the current closing HTML tag is considered
        # the closing tag for the document and any tags occuring after it
        # will be reported as errors.
        def endTagHtml(self, token):
            hasClosingHtml = False
            self.parser.singularEndTags.append(token["name"])
            for remaining in self.parser.remainingTokens:
                if remaining.get('name') == "html" and remaining.get('type') == tokenTypes["EndTag"]:
                    hasClosingHtml = True

            if hasClosingHtml:
                self.parser.parseError("incorrect-placement-html-end-tag",
                                   {"name": token["name"]})
            else:
                # DECO3801 - Redirects to the after body phase, causing all
                # remaining tags to be treated as being misplaced.
                self.parser.parseError("early-termination-in-body",
                                   {"name": token["name"]})
                self.parser.phase = self.parser.phases["afterBody"]
                return token

                # DECO3801 - Old implementation:
                # if self.tree.elementInScope("body"):
                #    self.endTagBody(impliedTagToken("body"))
                #    return token

        def endTagBlock(self, token):
            # Put us back in the right whitespace handling mode
            if token["name"] == "pre":
                self.processSpaceCharacters = self.processSpaceCharactersNonPre
            inScope = self.tree.elementInScope(token["name"])
            if inScope:
                # DECO3801 TODO: This may cause issues for end tag checking.
                # Requires more research.
                self.tree.generateImpliedEndTags()
            if self.tree.openElements[-1].name != token["name"]:
                self.parser.parseError("end-tag-too-early", {"name": token["name"]})
            if inScope:
                node = self.tree.openElements.pop()
                while node.name != token["name"]:
                    node = self.tree.openElements.pop()

        # DECO3801 - Handler method to check for excessive instances of
        # footer end tags.
        def endTagFooter(self, token):
            hasClosingFooter = False
            self.parser.singularEndTags.append(token["name"])
            for remaining in self.parser.remainingTokens:
                if remaining.get('name') == "footer" and remaining.get('type') == tokenTypes["EndTag"]:
                    hasClosingFooter = True

            if hasClosingFooter:
                self.parser.parseError("incorrect-placement-singular-end-tag",
                                   {"name": token["name"]})
            else:
                inScope = self.tree.elementInScope(token["name"])
                if inScope:
                    self.tree.generateImpliedEndTags()
                    if self.tree.openElements[-1].name != token["name"]:
                        node = self.tree.openElements.pop()
                        while node.name != token["name"]:
                            # DECO3801 - Report missing closing tags for any remaining open
                            # tags in the footer section.
                            self.parser.parseError("missing-closing-tags-in-footer", {"name": node.name})
                            node = self.tree.openElements.pop()

        def endTagForm(self, token):
            node = self.tree.formPointer
            self.tree.formPointer = None
            if node is None or not self.tree.elementInScope(node):
                self.parser.parseError("unexpected-end-tag",
                                       {"name": "form"})
            else:
                self.tree.generateImpliedEndTags()
                if self.tree.openElements[-1] != node:
                    self.parser.parseError("end-tag-too-early-ignored",
                                           {"name": "form"})
                self.tree.openElements.remove(node)

        def endTagListItem(self, token):
            if token["name"] == "li":
                variant = "list"
            else:
                variant = None
            if not self.tree.elementInScope(token["name"], variant=variant):
                self.parser.parseError("unexpected-end-tag", {"name": token["name"]})
            else:
                self.tree.generateImpliedEndTags(exclude=token["name"])
                if self.tree.openElements[-1].name != token["name"]:
                    self.parser.parseError(
                        "end-tag-too-early",
                        {"name": token["name"]})
                node = self.tree.openElements.pop()
                while node.name != token["name"]:
                    node = self.tree.openElements.pop()

        def endTagHeading(self, token):
            for item in headingElements:
                if self.tree.elementInScope(item):
                    self.tree.generateImpliedEndTags()
                    break
            if self.tree.openElements[-1].name != token["name"]:
                self.parser.parseError("end-tag-too-early", {"name": token["name"]})

            for item in headingElements:
                if self.tree.elementInScope(item):
                    item = self.tree.openElements.pop()
                    while item.name not in headingElements:
                        item = self.tree.openElements.pop()
                    break

        def endTagFormatting(self, token):
            """The much-feared adoption agency algorithm"""
            # http://svn.whatwg.org/webapps/complete.html#adoptionAgency revision 7867
            # XXX Better parseError messages appreciated.

            # Step 1
            outerLoopCounter = 0

            # Step 2
            while outerLoopCounter < 8:

                # Step 3
                outerLoopCounter += 1

                # Step 4:

                # Let the formatting element be the last element in
                # the list of active formatting elements that:
                # - is between the end of the list and the last scope
                # marker in the list, if any, or the start of the list
                # otherwise, and
                # - has the same tag name as the token.
                formattingElement = self.tree.elementInActiveFormattingElements(
                    token["name"])
                if (not formattingElement or
                    (formattingElement in self.tree.openElements and
                     not self.tree.elementInScope(formattingElement.name))):
                    # If there is no such node, then abort these steps
                    # and instead act as described in the "any other
                    # end tag" entry below.
                    self.endTagOther(token)
                    return

                # Otherwise, if there is such a node, but that node is
                # not in the stack of open elements, then this is a
                # parse error; remove the element from the list, and
                # abort these steps.
                elif formattingElement not in self.tree.openElements:
                    self.parser.parseError("adoption-agency-1.2", {"name": token["name"]})
                    self.tree.activeFormattingElements.remove(formattingElement)
                    return

                # Otherwise, if there is such a node, and that node is
                # also in the stack of open elements, but the element
                # is not in scope, then this is a parse error; ignore
                # the token, and abort these steps.
                elif not self.tree.elementInScope(formattingElement.name):
                    self.parser.parseError("adoption-agency-4.4", {"name": token["name"]})
                    return

                # Otherwise, there is a formatting element and that
                # element is in the stack and is in scope. If the
                # element is not the current node, this is a parse
                # error. In any case, proceed with the algorithm as
                # written in the following steps.
                else:
                    if formattingElement != self.tree.openElements[-1]:
                        self.parser.parseError("adoption-agency-1.3", {"name": token["name"]})

                # Step 5:

                # Let the furthest block be the topmost node in the
                # stack of open elements that is lower in the stack
                # than the formatting element, and is an element in
                # the special category. There might not be one.
                afeIndex = self.tree.openElements.index(formattingElement)
                furthestBlock = None
                for element in self.tree.openElements[afeIndex:]:
                    if element.nameTuple in specialElements:
                        furthestBlock = element
                        break

                # Step 6:

                # If there is no furthest block, then the UA must
                # first pop all the nodes from the bottom of the stack
                # of open elements, from the current node up to and
                # including the formatting element, then remove the
                # formatting element from the list of active
                # formatting elements, and finally abort these steps.
                if furthestBlock is None:
                    element = self.tree.openElements.pop()
                    while element != formattingElement:
                        element = self.tree.openElements.pop()
                    self.tree.activeFormattingElements.remove(element)
                    return

                # Step 7
                commonAncestor = self.tree.openElements[afeIndex - 1]

                # Step 8:
                # The bookmark is supposed to help us identify where to reinsert
                # nodes in step 15. We have to ensure that we reinsert nodes after
                # the node before the active formatting element. Note the bookmark
                # can move in step 9.7
                bookmark = self.tree.activeFormattingElements.index(formattingElement)

                # Step 9
                lastNode = node = furthestBlock
                innerLoopCounter = 0

                index = self.tree.openElements.index(node)
                while innerLoopCounter < 3:
                    innerLoopCounter += 1
                    # Node is element before node in open elements
                    index -= 1
                    node = self.tree.openElements[index]
                    if node not in self.tree.activeFormattingElements:
                        self.tree.openElements.remove(node)
                        continue
                    # Step 9.6
                    if node == formattingElement:
                        break
                    # Step 9.7
                    if lastNode == furthestBlock:
                        bookmark = self.tree.activeFormattingElements.index(node) + 1
                    # Step 9.8
                    clone = node.cloneNode()
                    # Replace node with clone
                    self.tree.activeFormattingElements[
                        self.tree.activeFormattingElements.index(node)] = clone
                    self.tree.openElements[
                        self.tree.openElements.index(node)] = clone
                    node = clone
                    # Step 9.9
                    # Remove lastNode from its parents, if any
                    if lastNode.parent:
                        lastNode.parent.removeChild(lastNode)
                    node.appendChild(lastNode)
                    # Step 9.10
                    lastNode = node

                # Step 10
                # Foster parent lastNode if commonAncestor is a
                # table, tbody, tfoot, thead, or tr we need to foster
                # parent the lastNode
                if lastNode.parent:
                    lastNode.parent.removeChild(lastNode)

                if commonAncestor.name in frozenset(("table", "tbody", "tfoot", "thead", "tr")):
                    parent, insertBefore = self.tree.getTableMisnestedNodePosition()
                    parent.insertBefore(lastNode, insertBefore)
                else:
                    commonAncestor.appendChild(lastNode)

                # Step 11
                clone = formattingElement.cloneNode()

                # Step 12
                furthestBlock.reparentChildren(clone)

                # Step 13
                furthestBlock.appendChild(clone)

                # Step 14
                self.tree.activeFormattingElements.remove(formattingElement)
                self.tree.activeFormattingElements.insert(bookmark, clone)

                # Step 15
                self.tree.openElements.remove(formattingElement)
                self.tree.openElements.insert(
                    self.tree.openElements.index(furthestBlock) + 1, clone)

        def endTagAppletMarqueeObject(self, token):
            if self.tree.elementInScope(token["name"]):
                self.tree.generateImpliedEndTags()
            if self.tree.openElements[-1].name != token["name"]:
                self.parser.parseError("end-tag-too-early", {"name": token["name"]})

            if self.tree.elementInScope(token["name"]):
                element = self.tree.openElements.pop()
                while element.name != token["name"]:
                    element = self.tree.openElements.pop()
                self.tree.clearActiveFormattingElements()

        def endTagBr(self, token):
            self.parser.parseError("unexpected-end-tag-treated-as",
                                   {"originalName": "br", "newName": "br element"})
            self.tree.reconstructActiveFormattingElements()
            self.tree.insertElement(impliedTagToken("br", "StartTag"))
            self.tree.openElements.pop()

        def endTagOther(self, token):
            for node in self.tree.openElements[::-1]:
                if node.name == token["name"]:
                    self.tree.generateImpliedEndTags(exclude=token["name"])
                    if self.tree.openElements[-1].name != token["name"]:
                        self.parser.parseError("unexpected-end-tag", {"name": token["name"]})
                    while self.tree.openElements.pop() != node:
                        pass
                    break
                else:
                    if node.nameTuple in specialElements:
                        self.parser.parseError("unexpected-end-tag", {"name": token["name"]})
                        break

    class TextPhase(Phase):
        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = utils.MethodDispatcher([])
            self.startTagHandler.default = self.startTagOther
            self.endTagHandler = utils.MethodDispatcher([
                ("script", self.endTagScript)])
            self.endTagHandler.default = self.endTagOther

        def processCharacters(self, token):
            self.tree.insertText(token["data"])

        def processEOF(self):
            self.parser.parseError("expected-named-closing-tag-but-got-eof",
                                   {"name": self.tree.openElements[-1].name})
            self.tree.openElements.pop()
            self.parser.phase = self.parser.originalPhase
            return True

        def startTagOther(self, token):
            assert False, "Tried to process start tag %s in RCDATA/RAWTEXT mode" % token['name']

        def endTagScript(self, token):
            node = self.tree.openElements.pop()
            assert node.name == "script"
            self.parser.phase = self.parser.originalPhase
            # The rest of this method is all stuff that only happens if
            # document.write works

        def endTagOther(self, token):
            self.tree.openElements.pop()
            self.parser.phase = self.parser.originalPhase

    class InTablePhase(Phase):
        # http://www.whatwg.org/specs/web-apps/current-work/#in-table
        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = utils.MethodDispatcher([
                ("html", self.startTagHtml),
                ("caption", self.startTagCaption),
                ("colgroup", self.startTagColgroup),
                ("col", self.startTagCol),
                (("tbody", "tfoot", "thead"), self.startTagRowGroup),
                (("td", "th", "tr"), self.startTagImplyTbody),
                ("table", self.startTagTable),
                (("style", "script"), self.startTagStyleScript),
                ("input", self.startTagInput),
                ("form", self.startTagForm)
            ])
            self.startTagHandler.default = self.startTagOther

            self.endTagHandler = utils.MethodDispatcher([
                ("table", self.endTagTable),
                (("body", "caption", "col", "colgroup", "html", "tbody", "td",
                  "tfoot", "th", "thead", "tr"), self.endTagIgnore)
            ])
            self.endTagHandler.default = self.endTagOther

        # helper methods
        def clearStackToTableContext(self):
            # "clear the stack back to a table context"
            while self.tree.openElements[-1].name not in ("table", "html"):
                # self.parser.parseError("unexpected-implied-end-tag-in-table",
                #  {"name":  self.tree.openElements[-1].name})
                self.tree.openElements.pop()
            # When the current node is <html> it's an innerHTML case

        # processing methods
        def processEOF(self):
            if self.tree.openElements[-1].name != "html":
                self.parser.parseError("eof-in-table")
            else:
                assert self.parser.innerHTML
            # Stop parsing

        def processSpaceCharacters(self, token):
            originalPhase = self.parser.phase
            self.parser.phase = self.parser.phases["inTableText"]
            self.parser.phase.originalPhase = originalPhase
            self.parser.phase.processSpaceCharacters(token)

        def processCharacters(self, token):
            originalPhase = self.parser.phase
            self.parser.phase = self.parser.phases["inTableText"]
            self.parser.phase.originalPhase = originalPhase
            self.parser.phase.processCharacters(token)

        def insertText(self, token):
            # If we get here there must be at least one non-whitespace character
            # Do the table magic!
            self.tree.insertFromTable = True
            self.parser.phases["inBody"].processCharacters(token)
            self.tree.insertFromTable = False

        def startTagCaption(self, token):
            self.clearStackToTableContext()
            self.tree.activeFormattingElements.append(Marker)
            self.tree.insertElement(token)
            self.parser.phase = self.parser.phases["inCaption"]

        def startTagColgroup(self, token):
            self.clearStackToTableContext()
            self.tree.insertElement(token)
            self.parser.phase = self.parser.phases["inColumnGroup"]

        def startTagCol(self, token):
            self.startTagColgroup(impliedTagToken("colgroup", "StartTag"))
            return token

        def startTagRowGroup(self, token):
            self.clearStackToTableContext()
            self.tree.insertElement(token)
            self.parser.phase = self.parser.phases["inTableBody"]

        def startTagImplyTbody(self, token):
            self.startTagRowGroup(impliedTagToken("tbody", "StartTag"))
            return token

        def startTagTable(self, token):
            self.parser.parseError("unexpected-start-tag-implies-end-tag",
                                   {"startName": "table", "endName": "table"})
            self.parser.phase.processEndTag(impliedTagToken("table"))
            if not self.parser.innerHTML:
                return token

        def startTagStyleScript(self, token):
            return self.parser.phases["inHead"].processStartTag(token)

        def startTagInput(self, token):
            if ("type" in token["data"] and
                    token["data"]["type"].translate(asciiUpper2Lower) == "hidden"):
                self.parser.parseError("unexpected-hidden-input-in-table")
                self.tree.insertElement(token)
                # XXX associate with form
                self.tree.openElements.pop()
            else:
                self.startTagOther(token)

        def startTagForm(self, token):
            self.parser.parseError("unexpected-form-in-table")
            if self.tree.formPointer is None:
                self.tree.insertElement(token)
                self.tree.formPointer = self.tree.openElements[-1]
                self.tree.openElements.pop()

        def startTagOther(self, token):
            self.parser.parseError("unexpected-start-tag-implies-table-voodoo", {"name": token["name"]})
            # Do the table magic!
            self.tree.insertFromTable = True
            self.parser.phases["inBody"].processStartTag(token)
            self.tree.insertFromTable = False

        def endTagTable(self, token):
            if self.tree.elementInScope("table", variant="table"):
                self.tree.generateImpliedEndTags()
                if self.tree.openElements[-1].name != "table":
                    self.parser.parseError("end-tag-too-early-named",
                                           {"gotName": "table",
                                            "expectedName": self.tree.openElements[-1].name})
                while self.tree.openElements[-1].name != "table":
                    self.tree.openElements.pop()
                self.tree.openElements.pop()
                self.parser.resetInsertionMode()
            else:
                # innerHTML case
                assert self.parser.innerHTML
                self.parser.parseError()

        def endTagIgnore(self, token):
            self.parser.parseError("unexpected-end-tag", {"name": token["name"]})

        def endTagOther(self, token):
            self.parser.parseError("unexpected-end-tag-implies-table-voodoo", {"name": token["name"]})
            # Do the table magic!
            self.tree.insertFromTable = True
            self.parser.phases["inBody"].processEndTag(token)
            self.tree.insertFromTable = False

    class InTableTextPhase(Phase):
        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.originalPhase = None
            self.characterTokens = []

        def flushCharacters(self):
            data = "".join([item["data"] for item in self.characterTokens])
            if any([item not in spaceCharacters for item in data]):
                token = {"type": tokenTypes["Characters"], "data": data}
                self.parser.phases["inTable"].insertText(token)
            elif data:
                self.tree.insertText(data)
            self.characterTokens = []

        def processComment(self, token):
            self.flushCharacters()
            self.parser.phase = self.originalPhase
            return token

        def processEOF(self):
            self.flushCharacters()
            self.parser.phase = self.originalPhase
            return True

        def processCharacters(self, token):
            if token["data"] == "\u0000":
                return
            self.characterTokens.append(token)

        def processSpaceCharacters(self, token):
            # pretty sure we should never reach here
            self.characterTokens.append(token)
    #        assert False

        def processStartTag(self, token):
            self.flushCharacters()
            self.parser.phase = self.originalPhase
            return token

        def processEndTag(self, token):
            self.flushCharacters()
            self.parser.phase = self.originalPhase
            return token

    class InCaptionPhase(Phase):
        # http://www.whatwg.org/specs/web-apps/current-work/#in-caption
        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)

            self.startTagHandler = utils.MethodDispatcher([
                ("html", self.startTagHtml),
                (("caption", "col", "colgroup", "tbody", "td", "tfoot", "th",
                  "thead", "tr"), self.startTagTableElement)
            ])
            self.startTagHandler.default = self.startTagOther

            self.endTagHandler = utils.MethodDispatcher([
                ("caption", self.endTagCaption),
                ("table", self.endTagTable),
                (("body", "col", "colgroup", "html", "tbody", "td", "tfoot", "th",
                  "thead", "tr"), self.endTagIgnore)
            ])
            self.endTagHandler.default = self.endTagOther

        def ignoreEndTagCaption(self):
            return not self.tree.elementInScope("caption", variant="table")

        def processEOF(self):
            self.parser.phases["inBody"].processEOF()

        def processCharacters(self, token):
            return self.parser.phases["inBody"].processCharacters(token)

        def startTagTableElement(self, token):
            self.parser.parseError()
            # XXX Have to duplicate logic here to find out if the tag is ignored
            ignoreEndTag = self.ignoreEndTagCaption()
            self.parser.phase.processEndTag(impliedTagToken("caption"))
            if not ignoreEndTag:
                return token

        def startTagOther(self, token):
            return self.parser.phases["inBody"].processStartTag(token)

        def endTagCaption(self, token):
            if not self.ignoreEndTagCaption():
                # AT this code is quite similar to endTagTable in "InTable"
                self.tree.generateImpliedEndTags()
                if self.tree.openElements[-1].name != "caption":
                    self.parser.parseError("expected-one-end-tag-but-got-another",
                                           {"gotName": "caption",
                                            "expectedName": self.tree.openElements[-1].name})
                while self.tree.openElements[-1].name != "caption":
                    self.tree.openElements.pop()
                self.tree.openElements.pop()
                self.tree.clearActiveFormattingElements()
                self.parser.phase = self.parser.phases["inTable"]
            else:
                # innerHTML case
                assert self.parser.innerHTML
                self.parser.parseError()

        def endTagTable(self, token):
            self.parser.parseError()
            ignoreEndTag = self.ignoreEndTagCaption()
            self.parser.phase.processEndTag(impliedTagToken("caption"))
            if not ignoreEndTag:
                return token

        def endTagIgnore(self, token):
            self.parser.parseError("unexpected-end-tag", {"name": token["name"]})

        def endTagOther(self, token):
            return self.parser.phases["inBody"].processEndTag(token)

    class InColumnGroupPhase(Phase):
        # http://www.whatwg.org/specs/web-apps/current-work/#in-column

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)

            self.startTagHandler = utils.MethodDispatcher([
                ("html", self.startTagHtml),
                ("col", self.startTagCol)
            ])
            self.startTagHandler.default = self.startTagOther

            self.endTagHandler = utils.MethodDispatcher([
                ("colgroup", self.endTagColgroup),
                ("col", self.endTagCol)
            ])
            self.endTagHandler.default = self.endTagOther

        def ignoreEndTagColgroup(self):
            return self.tree.openElements[-1].name == "html"

        def processEOF(self):
            if self.tree.openElements[-1].name == "html":
                assert self.parser.innerHTML
                return
            else:
                ignoreEndTag = self.ignoreEndTagColgroup()
                self.endTagColgroup(impliedTagToken("colgroup"))
                if not ignoreEndTag:
                    return True

        def processCharacters(self, token):
            ignoreEndTag = self.ignoreEndTagColgroup()
            self.endTagColgroup(impliedTagToken("colgroup"))
            if not ignoreEndTag:
                return token

        def startTagCol(self, token):
            self.tree.insertElement(token)
            self.tree.openElements.pop()

        def startTagOther(self, token):
            ignoreEndTag = self.ignoreEndTagColgroup()
            self.endTagColgroup(impliedTagToken("colgroup"))
            if not ignoreEndTag:
                return token

        def endTagColgroup(self, token):
            if self.ignoreEndTagColgroup():
                # innerHTML case
                assert self.parser.innerHTML
                self.parser.parseError()
            else:
                self.tree.openElements.pop()
                self.parser.phase = self.parser.phases["inTable"]

        def endTagCol(self, token):
            self.parser.parseError("no-end-tag", {"name": "col"})

        def endTagOther(self, token):
            ignoreEndTag = self.ignoreEndTagColgroup()
            self.endTagColgroup(impliedTagToken("colgroup"))
            if not ignoreEndTag:
                return token

    class InTableBodyPhase(Phase):
        # http://www.whatwg.org/specs/web-apps/current-work/#in-table0
        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = utils.MethodDispatcher([
                ("html", self.startTagHtml),
                ("tr", self.startTagTr),
                (("td", "th"), self.startTagTableCell),
                (("caption", "col", "colgroup", "tbody", "tfoot", "thead"),
                 self.startTagTableOther)
            ])
            self.startTagHandler.default = self.startTagOther

            self.endTagHandler = utils.MethodDispatcher([
                (("tbody", "tfoot", "thead"), self.endTagTableRowGroup),
                ("table", self.endTagTable),
                (("body", "caption", "col", "colgroup", "html", "td", "th",
                  "tr"), self.endTagIgnore)
            ])
            self.endTagHandler.default = self.endTagOther

        # helper methods
        def clearStackToTableBodyContext(self):
            while self.tree.openElements[-1].name not in ("tbody", "tfoot",
                                                          "thead", "html"):
                # self.parser.parseError("unexpected-implied-end-tag-in-table",
                #  {"name": self.tree.openElements[-1].name})
                self.tree.openElements.pop()
            if self.tree.openElements[-1].name == "html":
                assert self.parser.innerHTML

        # the rest
        def processEOF(self):
            self.parser.phases["inTable"].processEOF()

        def processSpaceCharacters(self, token):
            return self.parser.phases["inTable"].processSpaceCharacters(token)

        def processCharacters(self, token):
            return self.parser.phases["inTable"].processCharacters(token)

        def startTagTr(self, token):
            self.clearStackToTableBodyContext()
            self.tree.insertElement(token)
            self.parser.phase = self.parser.phases["inRow"]

        def startTagTableCell(self, token):
            self.parser.parseError("unexpected-cell-in-table-body",
                                   {"name": token["name"]})
            self.startTagTr(impliedTagToken("tr", "StartTag"))
            return token

        def startTagTableOther(self, token):
            # XXX AT Any ideas on how to share this with endTagTable?
            if (self.tree.elementInScope("tbody", variant="table") or
                self.tree.elementInScope("thead", variant="table") or
                    self.tree.elementInScope("tfoot", variant="table")):
                self.clearStackToTableBodyContext()
                self.endTagTableRowGroup(
                    impliedTagToken(self.tree.openElements[-1].name))
                return token
            else:
                # innerHTML case
                assert self.parser.innerHTML
                self.parser.parseError()

        def startTagOther(self, token):
            return self.parser.phases["inTable"].processStartTag(token)

        def endTagTableRowGroup(self, token):
            if self.tree.elementInScope(token["name"], variant="table"):
                self.clearStackToTableBodyContext()
                self.tree.openElements.pop()
                self.parser.phase = self.parser.phases["inTable"]
            else:
                self.parser.parseError("unexpected-end-tag-in-table-body",
                                       {"name": token["name"]})

        def endTagTable(self, token):
            if (self.tree.elementInScope("tbody", variant="table") or
                self.tree.elementInScope("thead", variant="table") or
                    self.tree.elementInScope("tfoot", variant="table")):
                self.clearStackToTableBodyContext()
                self.endTagTableRowGroup(
                    impliedTagToken(self.tree.openElements[-1].name))
                return token
            else:
                # innerHTML case
                assert self.parser.innerHTML
                self.parser.parseError()

        def endTagIgnore(self, token):
            self.parser.parseError("unexpected-end-tag-in-table-body",
                                   {"name": token["name"]})

        def endTagOther(self, token):
            return self.parser.phases["inTable"].processEndTag(token)

    class InRowPhase(Phase):
        # http://www.whatwg.org/specs/web-apps/current-work/#in-row
        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = utils.MethodDispatcher([
                ("html", self.startTagHtml),
                (("td", "th"), self.startTagTableCell),
                (("caption", "col", "colgroup", "tbody", "tfoot", "thead",
                  "tr"), self.startTagTableOther)
            ])
            self.startTagHandler.default = self.startTagOther

            self.endTagHandler = utils.MethodDispatcher([
                ("tr", self.endTagTr),
                ("table", self.endTagTable),
                (("tbody", "tfoot", "thead"), self.endTagTableRowGroup),
                (("body", "caption", "col", "colgroup", "html", "td", "th"),
                 self.endTagIgnore)
            ])
            self.endTagHandler.default = self.endTagOther

        # helper methods (XXX unify this with other table helper methods)
        def clearStackToTableRowContext(self):
            while self.tree.openElements[-1].name not in ("tr", "html"):
                self.parser.parseError("unexpected-implied-end-tag-in-table-row",
                                       {"name": self.tree.openElements[-1].name})
                self.tree.openElements.pop()

        def ignoreEndTagTr(self):
            return not self.tree.elementInScope("tr", variant="table")

        # the rest
        def processEOF(self):
            self.parser.phases["inTable"].processEOF()

        def processSpaceCharacters(self, token):
            return self.parser.phases["inTable"].processSpaceCharacters(token)

        def processCharacters(self, token):
            return self.parser.phases["inTable"].processCharacters(token)

        def startTagTableCell(self, token):
            self.clearStackToTableRowContext()
            self.tree.insertElement(token)
            self.parser.phase = self.parser.phases["inCell"]
            self.tree.activeFormattingElements.append(Marker)

        def startTagTableOther(self, token):
            ignoreEndTag = self.ignoreEndTagTr()
            self.endTagTr(impliedTagToken("tr"))
            # XXX how are we sure it's always ignored in the innerHTML case?
            if not ignoreEndTag:
                return token

        def startTagOther(self, token):
            return self.parser.phases["inTable"].processStartTag(token)

        def endTagTr(self, token):
            if not self.ignoreEndTagTr():
                self.clearStackToTableRowContext()
                self.tree.openElements.pop()
                self.parser.phase = self.parser.phases["inTableBody"]
            else:
                # innerHTML case
                assert self.parser.innerHTML
                self.parser.parseError()

        def endTagTable(self, token):
            ignoreEndTag = self.ignoreEndTagTr()
            self.endTagTr(impliedTagToken("tr"))
            # Reprocess the current tag if the tr end tag was not ignored
            # XXX how are we sure it's always ignored in the innerHTML case?
            if not ignoreEndTag:
                return token

        def endTagTableRowGroup(self, token):
            if self.tree.elementInScope(token["name"], variant="table"):
                self.endTagTr(impliedTagToken("tr"))
                return token
            else:
                self.parser.parseError()

        def endTagIgnore(self, token):
            self.parser.parseError("unexpected-end-tag-in-table-row",
                                   {"name": token["name"]})

        def endTagOther(self, token):
            return self.parser.phases["inTable"].processEndTag(token)

    class InCellPhase(Phase):
        # http://www.whatwg.org/specs/web-apps/current-work/#in-cell
        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)
            self.startTagHandler = utils.MethodDispatcher([
                ("html", self.startTagHtml),
                (("caption", "col", "colgroup", "tbody", "td", "tfoot", "th",
                  "thead", "tr"), self.startTagTableOther)
            ])
            self.startTagHandler.default = self.startTagOther

            self.endTagHandler = utils.MethodDispatcher([
                (("td", "th"), self.endTagTableCell),
                (("body", "caption", "col", "colgroup", "html"), self.endTagIgnore),
                (("table", "tbody", "tfoot", "thead", "tr"), self.endTagImply)
            ])
            self.endTagHandler.default = self.endTagOther

        # helper
        def closeCell(self):
            if self.tree.elementInScope("td", variant="table"):
                self.endTagTableCell(impliedTagToken("td"))
            elif self.tree.elementInScope("th", variant="table"):
                self.endTagTableCell(impliedTagToken("th"))

        # the rest
        def processEOF(self):
            self.parser.phases["inBody"].processEOF()

        def processCharacters(self, token):
            return self.parser.phases["inBody"].processCharacters(token)

        def startTagTableOther(self, token):
            if (self.tree.elementInScope("td", variant="table") or
                    self.tree.elementInScope("th", variant="table")):
                self.closeCell()
                return token
            else:
                # innerHTML case
                assert self.parser.innerHTML
                self.parser.parseError()

        def startTagOther(self, token):
            return self.parser.phases["inBody"].processStartTag(token)

        def endTagTableCell(self, token):
            if self.tree.elementInScope(token["name"], variant="table"):
                self.tree.generateImpliedEndTags(token["name"])
                if self.tree.openElements[-1].name != token["name"]:
                    self.parser.parseError("unexpected-cell-end-tag",
                                           {"name": token["name"]})
                    while True:
                        node = self.tree.openElements.pop()
                        if node.name == token["name"]:
                            break
                else:
                    self.tree.openElements.pop()
                self.tree.clearActiveFormattingElements()
                self.parser.phase = self.parser.phases["inRow"]
            else:
                self.parser.parseError("unexpected-end-tag", {"name": token["name"]})

        def endTagIgnore(self, token):
            self.parser.parseError("unexpected-end-tag", {"name": token["name"]})

        def endTagImply(self, token):
            if self.tree.elementInScope(token["name"], variant="table"):
                self.closeCell()
                return token
            else:
                # sometimes innerHTML case
                self.parser.parseError()

        def endTagOther(self, token):
            return self.parser.phases["inBody"].processEndTag(token)

    class InSelectPhase(Phase):
        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)

            self.startTagHandler = utils.MethodDispatcher([
                ("html", self.startTagHtml),
                ("option", self.startTagOption),
                ("optgroup", self.startTagOptgroup),
                ("select", self.startTagSelect),
                (("input", "keygen", "textarea"), self.startTagInput),
                ("script", self.startTagScript)
            ])
            self.startTagHandler.default = self.startTagOther

            self.endTagHandler = utils.MethodDispatcher([
                ("option", self.endTagOption),
                ("optgroup", self.endTagOptgroup),
                ("select", self.endTagSelect)
            ])
            self.endTagHandler.default = self.endTagOther

        # http://www.whatwg.org/specs/web-apps/current-work/#in-select
        def processEOF(self):
            if self.tree.openElements[-1].name != "html":
                self.parser.parseError("eof-in-select")
            else:
                assert self.parser.innerHTML

        def processCharacters(self, token):
            if token["data"] == "\u0000":
                return
            self.tree.insertText(token["data"])

        def startTagOption(self, token):
            # We need to imply </option> if <option> is the current node.
            if self.tree.openElements[-1].name == "option":
                self.tree.openElements.pop()
            self.tree.insertElement(token)

        def startTagOptgroup(self, token):
            if self.tree.openElements[-1].name == "option":
                self.tree.openElements.pop()
            if self.tree.openElements[-1].name == "optgroup":
                self.tree.openElements.pop()
            self.tree.insertElement(token)

        def startTagSelect(self, token):
            self.parser.parseError("unexpected-select-in-select")
            self.endTagSelect(impliedTagToken("select"))

        def startTagInput(self, token):
            self.parser.parseError("unexpected-input-in-select")
            if self.tree.elementInScope("select", variant="select"):
                self.endTagSelect(impliedTagToken("select"))
                return token
            else:
                assert self.parser.innerHTML

        def startTagScript(self, token):
            return self.parser.phases["inHead"].processStartTag(token)

        def startTagOther(self, token):
            self.parser.parseError("unexpected-start-tag-in-select",
                                   {"name": token["name"]})

        def endTagOption(self, token):
            if self.tree.openElements[-1].name == "option":
                self.tree.openElements.pop()
            else:
                self.parser.parseError("unexpected-end-tag-in-select",
                                       {"name": "option"})

        def endTagOptgroup(self, token):
            # </optgroup> implicitly closes <option>
            if (self.tree.openElements[-1].name == "option" and
                    self.tree.openElements[-2].name == "optgroup"):
                self.tree.openElements.pop()
            # It also closes </optgroup>
            if self.tree.openElements[-1].name == "optgroup":
                self.tree.openElements.pop()
            # But nothing else
            else:
                self.parser.parseError("unexpected-end-tag-in-select",
                                       {"name": "optgroup"})

        def endTagSelect(self, token):
            if self.tree.elementInScope("select", variant="select"):
                node = self.tree.openElements.pop()
                while node.name != "select":
                    node = self.tree.openElements.pop()
                self.parser.resetInsertionMode()
            else:
                # innerHTML case
                assert self.parser.innerHTML
                self.parser.parseError()

        def endTagOther(self, token):
            self.parser.parseError("unexpected-end-tag-in-select",
                                   {"name": token["name"]})

    class InSelectInTablePhase(Phase):
        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)

            self.startTagHandler = utils.MethodDispatcher([
                (("caption", "table", "tbody", "tfoot", "thead", "tr", "td", "th"),
                 self.startTagTable)
            ])
            self.startTagHandler.default = self.startTagOther

            self.endTagHandler = utils.MethodDispatcher([
                (("caption", "table", "tbody", "tfoot", "thead", "tr", "td", "th"),
                 self.endTagTable)
            ])
            self.endTagHandler.default = self.endTagOther

        def processEOF(self):
            self.parser.phases["inSelect"].processEOF()

        def processCharacters(self, token):
            return self.parser.phases["inSelect"].processCharacters(token)

        def startTagTable(self, token):
            self.parser.parseError("unexpected-table-element-start-tag-in-select-in-table", {"name": token["name"]})
            self.endTagOther(impliedTagToken("select"))
            return token

        def startTagOther(self, token):
            return self.parser.phases["inSelect"].processStartTag(token)

        def endTagTable(self, token):
            self.parser.parseError("unexpected-table-element-end-tag-in-select-in-table", {"name": token["name"]})
            if self.tree.elementInScope(token["name"], variant="table"):
                self.endTagOther(impliedTagToken("select"))
                return token

        def endTagOther(self, token):
            return self.parser.phases["inSelect"].processEndTag(token)

    class InForeignContentPhase(Phase):
        breakoutElements = frozenset(["b", "big", "blockquote", "body", "br",
                                      "center", "code", "dd", "div", "dl", "dt",
                                      "em", "embed", "h1", "h2", "h3",
                                      "h4", "h5", "h6", "head", "hr", "i", "img",
                                      "li", "listing", "menu", "meta", "nobr",
                                      "ol", "p", "pre", "ruby", "s", "small",
                                      "span", "strong", "strike", "sub", "sup",
                                      "table", "tt", "u", "ul", "var"])

        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)

        def adjustSVGTagNames(self, token):
            replacements = {"altglyph": "altGlyph",
                            "altglyphdef": "altGlyphDef",
                            "altglyphitem": "altGlyphItem",
                            "animatecolor": "animateColor",
                            "animatemotion": "animateMotion",
                            "animatetransform": "animateTransform",
                            "clippath": "clipPath",
                            "feblend": "feBlend",
                            "fecolormatrix": "feColorMatrix",
                            "fecomponenttransfer": "feComponentTransfer",
                            "fecomposite": "feComposite",
                            "feconvolvematrix": "feConvolveMatrix",
                            "fediffuselighting": "feDiffuseLighting",
                            "fedisplacementmap": "feDisplacementMap",
                            "fedistantlight": "feDistantLight",
                            "feflood": "feFlood",
                            "fefunca": "feFuncA",
                            "fefuncb": "feFuncB",
                            "fefuncg": "feFuncG",
                            "fefuncr": "feFuncR",
                            "fegaussianblur": "feGaussianBlur",
                            "feimage": "feImage",
                            "femerge": "feMerge",
                            "femergenode": "feMergeNode",
                            "femorphology": "feMorphology",
                            "feoffset": "feOffset",
                            "fepointlight": "fePointLight",
                            "fespecularlighting": "feSpecularLighting",
                            "fespotlight": "feSpotLight",
                            "fetile": "feTile",
                            "feturbulence": "feTurbulence",
                            "foreignobject": "foreignObject",
                            "glyphref": "glyphRef",
                            "lineargradient": "linearGradient",
                            "radialgradient": "radialGradient",
                            "textpath": "textPath"}

            if token["name"] in replacements:
                token["name"] = replacements[token["name"]]

        def processCharacters(self, token):
            if token["data"] == "\u0000":
                token["data"] = "\uFFFD"
            elif (self.parser.framesetOK and
                  any(char not in spaceCharacters for char in token["data"])):
                self.parser.framesetOK = False
            Phase.processCharacters(self, token)

        def processStartTag(self, token):
            currentNode = self.tree.openElements[-1]
            if (token["name"] in self.breakoutElements or
                (token["name"] == "font" and
                 set(token["data"].keys()) & set(["color", "face", "size"]))):
                self.parser.parseError("unexpected-html-element-in-foreign-content",
                                       {"name": token["name"]})
                while (self.tree.openElements[-1].namespace !=
                       self.tree.defaultNamespace and
                       not self.parser.isHTMLIntegrationPoint(self.tree.openElements[-1]) and
                       not self.parser.isMathMLTextIntegrationPoint(self.tree.openElements[-1])):
                    self.tree.openElements.pop()
                return token

            else:
                if currentNode.namespace == namespaces["mathml"]:
                    self.parser.adjustMathMLAttributes(token)
                elif currentNode.namespace == namespaces["svg"]:
                    self.adjustSVGTagNames(token)
                    self.parser.adjustSVGAttributes(token)
                self.parser.adjustForeignAttributes(token)
                token["namespace"] = currentNode.namespace
                self.tree.insertElement(token)
                if token["selfClosing"]:
                    self.tree.openElements.pop()
                    token["selfClosingAcknowledged"] = True

        def processEndTag(self, token):
            nodeIndex = len(self.tree.openElements) - 1
            node = self.tree.openElements[-1]
            if node.name != token["name"]:
                self.parser.parseError("unexpected-end-tag", {"name": token["name"]})

            while True:
                if node.name.translate(asciiUpper2Lower) == token["name"]:
                    # XXX this isn't in the spec but it seems necessary
                    if self.parser.phase == self.parser.phases["inTableText"]:
                        self.parser.phase.flushCharacters()
                        self.parser.phase = self.parser.phase.originalPhase
                    while self.tree.openElements.pop() != node:
                        assert self.tree.openElements
                    new_token = None
                    break
                nodeIndex -= 1

                node = self.tree.openElements[nodeIndex]
                if node.namespace != self.tree.defaultNamespace:
                    continue
                else:
                    new_token = self.parser.phase.processEndTag(token)
                    break
            return new_token

    class AfterBodyPhase(Phase):
        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)

            self.startTagHandler = utils.MethodDispatcher([
                ("html", self.startTagHtml)
            ])
            self.startTagHandler.default = self.startTagOther

            self.endTagHandler = utils.MethodDispatcher([("html", self.endTagHtml)])
            self.endTagHandler.default = self.endTagOther

        def processEOF(self):
            # Stop parsing
            pass

        def processComment(self, token):
            # This is needed because data is to be appended to the <html> element
            # here and not to whatever is currently open.
            self.tree.insertComment(token, self.tree.openElements[0])

        def processCharacters(self, token):
            self.parser.parseError("unexpected-char-after-body")
            self.parser.phase = self.parser.phases["inBody"]
            return token

        def startTagHtml(self, token):
            return self.parser.phases["inBody"].processStartTag(token)

        def startTagOther(self, token):
            # DECO3801 - Hide error if token is body tag. Prevents
            # overlap with singular tag error checking.
            if not token["name"] == 'body':
                self.parser.parseError("unexpected-start-tag-after-body",
                                   {"name": token["name"]})
            # DECO3801 - Old implementation.    
            #self.parser.phase = self.parser.phases["inBody"]
            #return token

        def endTagHtml(self, name):
            # DECO3801 - Error checking for the closing HTML tag.
            self.parser.singularEndTags.append(name["name"])
            if self.parser.innerHTML:
                self.parser.parseError("unexpected-end-tag-after-body-innerhtml")
            else:
                self.parser.phase = self.parser.phases["afterAfterBody"]

        def endTagOther(self, token):
            self.parser.parseError("unexpected-end-tag-after-body",
                                   {"name": token["name"]})
            # DECO3801 - Old implementation.
            #self.parser.phase = self.parser.phases["inBody"]
            #return token

    class InFramesetPhase(Phase):
        # http://www.whatwg.org/specs/web-apps/current-work/#in-frameset
        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)

            self.startTagHandler = utils.MethodDispatcher([
                ("html", self.startTagHtml),
                ("frameset", self.startTagFrameset),
                ("frame", self.startTagFrame),
                ("noframes", self.startTagNoframes)
            ])
            self.startTagHandler.default = self.startTagOther

            self.endTagHandler = utils.MethodDispatcher([
                ("frameset", self.endTagFrameset)
            ])
            self.endTagHandler.default = self.endTagOther

        def processEOF(self):
            if self.tree.openElements[-1].name != "html":
                self.parser.parseError("eof-in-frameset")
            else:
                assert self.parser.innerHTML

        def processCharacters(self, token):
            self.parser.parseError("unexpected-char-in-frameset")

        def startTagFrameset(self, token):
            self.tree.insertElement(token)

        def startTagFrame(self, token):
            self.tree.insertElement(token)
            self.tree.openElements.pop()

        def startTagNoframes(self, token):
            return self.parser.phases["inBody"].processStartTag(token)

        def startTagOther(self, token):
            self.parser.parseError("unexpected-start-tag-in-frameset",
                                   {"name": token["name"]})

        def endTagFrameset(self, token):
            if self.tree.openElements[-1].name == "html":
                # innerHTML case
                self.parser.parseError("unexpected-frameset-in-frameset-innerhtml")
            else:
                self.tree.openElements.pop()
            if (not self.parser.innerHTML and
                    self.tree.openElements[-1].name != "frameset"):
                # If we're not in innerHTML mode and the the current node is not a
                # "frameset" element (anymore) then switch.
                self.parser.phase = self.parser.phases["afterFrameset"]

        def endTagOther(self, token):
            self.parser.parseError("unexpected-end-tag-in-frameset",
                                   {"name": token["name"]})

    class AfterFramesetPhase(Phase):
        # http://www.whatwg.org/specs/web-apps/current-work/#after3
        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)

            self.startTagHandler = utils.MethodDispatcher([
                ("html", self.startTagHtml),
                ("noframes", self.startTagNoframes)
            ])
            self.startTagHandler.default = self.startTagOther

            self.endTagHandler = utils.MethodDispatcher([
                ("html", self.endTagHtml)
            ])
            self.endTagHandler.default = self.endTagOther

        def processEOF(self):
            # Stop parsing
            pass

        def processCharacters(self, token):
            self.parser.parseError("unexpected-char-after-frameset")

        def startTagNoframes(self, token):
            return self.parser.phases["inHead"].processStartTag(token)

        def startTagOther(self, token):
            self.parser.parseError("unexpected-start-tag-after-frameset",
                                   {"name": token["name"]})

        def endTagHtml(self, token):
            self.parser.phase = self.parser.phases["afterAfterFrameset"]

        def endTagOther(self, token):
            self.parser.parseError("unexpected-end-tag-after-frameset",
                                   {"name": token["name"]})

    class AfterAfterBodyPhase(Phase):
        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)

            self.startTagHandler = utils.MethodDispatcher([
                ("html", self.startTagHtml)
            ])
            self.startTagHandler.default = self.startTagOther

        def processEOF(self):
            pass

        def processComment(self, token):
            self.tree.insertComment(token, self.tree.document)

        def processSpaceCharacters(self, token):
            return self.parser.phases["inBody"].processSpaceCharacters(token)

        def processCharacters(self, token):
            self.parser.parseError("expected-eof-but-got-char")
            self.parser.phase = self.parser.phases["inBody"]
            return token

        def startTagHtml(self, token):
            return self.parser.phases["inBody"].processStartTag(token)

        def startTagOther(self, token):
            self.parser.parseError("expected-eof-but-got-start-tag",
                                   {"name": token["name"]})
            # DECO3801 - Removed to prevent false reporting of start tags detected
            # after the end HTML tag.
            # self.parser.phase = self.parser.phases["inBody"]
            # return token

        def processEndTag(self, token):
            self.parser.parseError("expected-eof-but-got-end-tag",
                                   {"name": token["name"]})
            # DECO3801 - Removed to prevent false reporting of tags detected after
            # the end HTML tag.
            # self.parser.phase = self.parser.phases["inBody"]
            # return token

    class AfterAfterFramesetPhase(Phase):
        def __init__(self, parser, tree):
            Phase.__init__(self, parser, tree)

            self.startTagHandler = utils.MethodDispatcher([
                ("html", self.startTagHtml),
                ("noframes", self.startTagNoFrames)
            ])
            self.startTagHandler.default = self.startTagOther

        def processEOF(self):
            pass

        def processComment(self, token):
            self.tree.insertComment(token, self.tree.document)

        def processSpaceCharacters(self, token):
            return self.parser.phases["inBody"].processSpaceCharacters(token)

        def processCharacters(self, token):
            self.parser.parseError("expected-eof-but-got-char")

        def startTagHtml(self, token):
            return self.parser.phases["inBody"].processStartTag(token)

        def startTagNoFrames(self, token):
            return self.parser.phases["inHead"].processStartTag(token)

        def startTagOther(self, token):
            self.parser.parseError("expected-eof-but-got-start-tag",
                                   {"name": token["name"]})

        def processEndTag(self, token):
            self.parser.parseError("expected-eof-but-got-end-tag",
                                   {"name": token["name"]})

    return {
        "initial": InitialPhase,
        "beforeHtml": BeforeHtmlPhase,
        "beforeHead": BeforeHeadPhase,
        "inHead": InHeadPhase,
        # XXX "inHeadNoscript": InHeadNoScriptPhase,
        "afterHead": AfterHeadPhase,
        "inBody": InBodyPhase,
        "text": TextPhase,
        "inTable": InTablePhase,
        "inTableText": InTableTextPhase,
        "inCaption": InCaptionPhase,
        "inColumnGroup": InColumnGroupPhase,
        "inTableBody": InTableBodyPhase,
        "inRow": InRowPhase,
        "inCell": InCellPhase,
        "inSelect": InSelectPhase,
        "inSelectInTable": InSelectInTablePhase,
        "inForeignContent": InForeignContentPhase,
        "afterBody": AfterBodyPhase,
        "inFrameset": InFramesetPhase,
        "afterFrameset": AfterFramesetPhase,
        "afterAfterBody": AfterAfterBodyPhase,
        "afterAfterFrameset": AfterAfterFramesetPhase,
        # XXX after after frameset
    }


def impliedTagToken(name, type="EndTag", attributes=None,
                    selfClosing=False):
    if attributes is None:
        attributes = {}
    return {"type": tokenTypes[type], "name": name, "data": attributes,
            "selfClosing": selfClosing}


class ParseError(Exception):
    """Error in parsed document"""
    pass
