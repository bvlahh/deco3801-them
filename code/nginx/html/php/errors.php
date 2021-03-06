<?php

class Errors
{
    /**
    * A mapping of error codes to their associated error message.
    */
    static $error_strings = array(
        
        1 => "No valid doctype was found. HTML files should start with <code><!DOCTYPE html></code>.",
        2 => "Found a duplicate instance of a singular tag.",
        3 => "A singular start tag was placed in the wrong location.",
        4 => "A singular closing tag was placed in the wrong location.",
        5 => "An invalid starting tag was placed before the head section.",
        6 => "An invalid closing tag was placed before the head section.",
        7 => "This starting tag is not valid within the head section. It should probably go in the body section instead, along with it's closing tag!",
        8 => "This closing tag is not valid within the head section. It should probably go in the body section instead, along with it's starting tag!",
        9 => "No <code><head></code> tag was found in the document.",
        10 => "No <code></head></code> tag was found in the document.",
        11 => "A <code></html></code> tag was found before the <code></body></code> tag. The <code></html></code> tag should be the final line of the HTML document.",
        12 => "A start tag was found after the expected <code></html></code> tag.",
        13 => "A closing tag was found after the expected <code></html></code> tag.",
        14 => "This closing tag is missing a matching start tag.",
        15 => "A misplaced closing tag was found after the <code></body></code> tag.",
        16 => "The document is missing a <code></html></code> tag.",
        17 => "The tag has a symbol in place of a valid tag name.",
        18 => "A closing angled bracket was found instead of a tag name.",
        19 => "A question mark was found instead of a tag name. This is not a valid tag name.",
        20 => "A closing tag cannot contain a self closing solidus symbol '/'. Closing tags have the form <code></tagname></code>.",
        21 => "This tag is not a self closing void tag type. It should have a closing tag in the form <code></tagname></code> and not be written as <code><tagname /></code>.",
        22 => "<code><br></code> tags are self closing and don't require a closing tag. Instead of <code><br></code><code></br></code>, you just need to use <code><br /></code>.",
        23 => "A void tag is missing the self closing backslash symbol. For example, <code><br></code> instead of <code><br /></code>, or <code><img src='img.png'></code> instead of <code><img src='img.png'/></code>",
        24 => "One or more attributes were found in a closing tag. Closing tags should not contain any attributes and should the resemble the form <code></tagname><code>.",
        25 => "A <code></html></code> tag was found before the head phase. The document has a misplaced <code></html></code> tag or it is missing the head and body sections.",
        26 => "A <code></html></code> tag was found in the head phase. The document has a misplaced <code></html></code> tag or it is missing a <code></head></code> tag.",
        27 => "A <code></html></code> tag was found before the body phase. The document has a misplaced <code></html></code> tag or it is missing the body section.",
        28 => "A <code></html></code> tag was found in the body phase. The document has a misplaced <code></html></code> tag or is missing a <code></body></code> tag.",
        29 => "This start tag is of a tag type which belongs within the head section. Move it to before the <code></head></code> tag!",
        30 => "Found a start tag after the <code></head></code> tag and before the <code><body></code> tag. It should be placed within either the head or body section.",
        31 => "Found a closing tag after the <code><head></code> tag and before the <code><body></code> phase. It should be placed within either the head or body section.",
        32 => "No <code><body></code> tag was found in the expected context, implying that no body section exists.",
        33 => "No <code></body></code> tag was found in the expected context, implying that no body section exists or it wasn't closed properly.",
        34 => "The document is missing a <code><html></code> tag. The <code><html></code> tag tells the browser that this is a HTML document, and is the container for all other HTML tags.",
        35 => "Invalid DOCTYPE. HTML5 uses <code><!DOCTYPE html></code> as the DOCTYPE declaration.",
        36 => "There is a missing space after the doctype declaration. Correct form: <code><!DOCTYPE html></code>.",
        37 => "No valid doctype was found. HTML files should start with <code><!DOCTYPE html></code>.",
        38 => "The document is empty.",
        39 => "The specified URL attribute doesn't match up with any of the filenames of the files contained within the given zip file. You may have misspelled the filepath, or the file may be missing.",
        40 => "This tag is deprecated under the HTML 5 specification. It should be removed or replaced with an alternative tag.",
        41 => "<code><frame></code> elements are obsolete under the HTML 5 specification. They cause accessibility and usability issues.",
        42 => "A <code><form></code> element was found outside of required enclosing <code><form></code> tags. These elements should always be enclosed by <code><form></code> opening and closing tags.",
        43 => "An <code><input></code> element is missing a required <code>type</code> attribute.",
        44 => "An <code><input></code> element is missing a required <code>value</code> attribute.",
        45 => "An <code><input></code> element is missing a required <code>name</code> attribute.",
        46 => "Input elements with a type <code>file</code> cannot have a value attribute as it is a potential security risk.",
        47 => "An input element is missing an associated <code><label></code> tag. The input element must either have a label with a <code>for</code> attribute matching the id of this input element or must be enclosed in label tags.",
        48 => "A previous starting tag uses this ID value. Please use a different ID value for this tag. ID values should unique within a document.",
        49 => "A duplicate <code><title></code> element was found in the head section. Only one <code><title></code> element is required.",
        50 => "No title element was found in the head section. A HTML document requires a title so that it can be diplayed in the browser's title bar or tag title.",
        51 => "An <code><img></code> starting tag is missing a required <code>alt</code> attribute. The <code>alt</code> attribute is used by screen readers to provide a description of the image to the blind. It is an accessbility requirement.",
        52 => "The <code>alt</code> attribute for this <code><img></code> start tag contains a blank string. Please enter a valid description of the image associated with this image tag.",
        53 => "Found an open start tag before the footer section. Either a closing tag has been placed after the <code><footer></code> tag or it is missing.",
        54 => "Found an open start tag within the footer section. Either a closing tag has been placed after the <code></footer></code> tag or it is missing.",
        55 => "This tag does not contain a valid tag name and therefore isn't valid HTML.",
        56 => "This start tag is missing a matching closing tag.",
        57 => "A <code><a></code> element is missing a required <code>href</code> attribute.",
        58 => "A <code><a></code> element's <code>href</code> attribute is empty. Please enter a valid link.",
        59 => "A <code><a></code> element is missing a required <code>name</code> attribute.",
        60 => "A <code><a></code> element's <code>name</code> attribute is empty. Please enter a valid name.",
        61 => "Only one instance of the <code><h1></code> tag should be used in a single HTML document.",
        62 => "Heading elements appear in order of <code><h1></code> being the most important and <code><h6></code> being the least important. This heading tag has skipped one or more of the sizings.",
        63 => "The HTML contains non-ascii characters. It's best to avoid the use of non-ascii characters unless necessary. If non-ascii characters are required, ensure UTF-8 encoding is used by including the following snippet in the head section: <code><meta http-equiv=\"Content-Type\" content=\"text/html; charset=utf-8\"></code>",
        64 => "It appears you may be using a HTML table for layout. You should only use a <code><table></code> element for tabular data.",
        65 => "A <code><a></code> element's <code>rel</code> attribute is empty. Please enter a valid value for rel.",
        66 => "A <code><link></code> element is missinga required <code>href</code> attribute.",
        67 => "A <code><link></code> element's <code>href</code> attribute is empty. Please enter a valid link.",
        68 => "A <code><a><code> element's <code>type</code> attribute is empty. Please enter a valid type.",
        69 => "A <code><link></code> element is missing a required <code>rel</code> attribute.",
        70 => "A <code><link></code> element's <code>rel</code> attribute is empty. Please enter a valid value for rel.",
        71 => "No <code><footer></code> tag was found in the expected context, implying that no body section exists.",
        72 => "No <code></footer></code> tag was found in the expected context, implying that no body section exists or it wasn't closed properly.",
        73 => "Characters were found before the <code><!DOCTYPE html></code> declaration. It is possible you were trying to add a comment before the <code><!DOCTYPE html></code> declaration. Comments in HTML are of the form <!-- Comment -->.",
        74 => "We didn't find any html tag or doctype at the start of this file. If this is a HTML file then please start the document with a <code><!DOCTYPE html></code> tag."
    );
    
    /**
    * Returns the error message associated with the given error code.
    *
    * @param int $error_number The error code.
    */
    static function errorString($error_number) {
        
        return Errors::$error_strings[$error_number];
        
    }
    
    /**
    * Returns a hexadecimal colour value associated with the given error code.
    *
    * @param int $error_number The error code.
    */
    static function errorColour($error_number) {
        
        if (in_array($error_number, array(48, 61, 62, 63, 64, 74))) {
            /* poor practice */
            return "#ffff7f";
        } else if (in_array($error_number, array(47, 51))) {
            /* accessibiity */
            return "#7f7fff";
        } else if (in_array($error_number, array(40, 41))) {
            /* deprecated tags */
            return "#ffbb77";
        } else {
            /* syntax, semantics */
            return "#ff7f7f";
        }
        
    }
    
    static function documentErrorColour($error_number) {
        
        static $colour_toggle = false;
        $colour_toggle = ($colour_toggle xor true);
        
        if (in_array($error_number, array(48, 61, 62))) {
            /* poor practice */
            if ($colour_toggle)
                return "#ffff6f";
            else
                return "#ffff7f";
        } else if (in_array($error_number, array(47, 51))) {
            /* accessibiity */
            if ($colour_toggle)
                return "#6f6fff";
            else
                return "#7f7fff";
        } else if (in_array($error_number, array(40, 41))) {
            /* deprecated tags */
            if ($colour_toggle)
                return "#ffbb66";
            else
                return "#ffbb77";
        } else {
            /* syntax, semantics */
            if ($colour_toggle)
                return "#ff6f6f";
            else
                return "#ff7f7f";
        }
        
    }
    
}

?>
