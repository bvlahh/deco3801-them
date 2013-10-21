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
        19 => "A question mark was found instead of a tag name.",
        20 => "A closing tag cannot contain a self closing solidus symbol '/'.",
        21 => "This tag is not a self closing void tag type. It should have a closing tag, <code></tagname></code>, and not be written as <code><tagname /></code>.",
        22 => "<code><br></code> tags are self closing and don't require a closing tag. Instead of <code><br></code><code></br></code>, you just need to use <code><br /></code>.",
        23 => "A void tag is missing the self closing backslash symbol. For example, <code><br></code> instead of <code><br /></code>, or <code><img src='img.png'></code> instead of <code><img src='img.png'/></code>",
        24 => "One or more attributes were found in a closing tag. A closing tag should just be <code></tagname><code>.",
        25 => "A <code></html></code> tag was found before the head phase. The document has a misplaced <code></html></code> tag or it is missing the head and body sections.",
        26 => "A <code></html></code> tag was found in the head phase. The document has a misplaced <code></html></code> tag or it is missing a <code></head></code> tag.",
        27 => "A <code></html></code> tag was found before the body phase. The document has a misplaced <code></html></code> tag or it is missing the body section.",
        28 => "A <code></html></code> tag was found in the body phase. The document has a misplaced <code></html></code> tag or is missing a <code></body></code> tag.",
        29 => "This start tag is of a tag type which belongs within the head section. Move it to before the <code></head></code> tag!",
        30 => "Found a start tag after the head phase and before the body phase. It should be placed within either the head or body section.",
        31 => "Found a closing tag after the head phase and before the body phase. It should be placed within either the head or body section.",
        32 => "No starting body tag was found in the expected context, implying that no body section exists.",
        33 => "No closing body tag was found in the expected context, implying that no body section exists or it wasn't closed properly.",
        34 => "The document is missing a starting HTML tag.",
        35 => "Unknown DOCTYPE. HTML5 uses <!DOCTYPE html>.",
        36 => "There is a missing space after the doctype declaration. Correct form: <!DOCTYPE html>.",
        37 => "No valid doctype was found. HTML files should start with <!DOCTYPE html>.",
        38 => "The document is empty.",
        39 => "The specified URL attribute doesn't match up with any of the filenames of the files contained within the given zip file.",
        40 => "This tag is deprecated under the HTML 5 specification. It should be removed or replaced with an alternative tag.",
        41 => "Frame elements are obsolete under the HTML 5 specification. They cause accessibility and usability issues.",
        42 => "A form element was found outside of required enclosing form tags.",
        43 => "An input element is missing a required 'type' attribute.",
        44 => "An input element is missing a required 'value' attribute.",
        45 => "An input element is missing a required 'name' attribute.",
        46 => "Input elements with a type 'file' cannot have a value attribute as it is a potential security risk.",
        47 => "An input element is missing an associated label tag. The input element must either have a label with a 'for' attribute matching the id of this input element or must be enclosed in label tags.",
        48 => "A previous starting tag uses this ID value. Please use a different ID value for this tag.",
        49 => "A duplicate title element was found in the head section. Only one title element is required.",
        50 => "No title element was found in the head section. A HTML document requires a title so that it can be diplayed in the browser's title bar or tag title.",
        51 => "An img starting tag is missing a required 'alt' attribute. The 'alt' attribute is used by screen readers to provide a description of the image to the blind. It is an accessbility requirement.",
        52 => "The 'alt' attribute for this img start tag contains a blank string. Please enter a valid description of the image associated with this image tag.",
        53 => "Found an open start tag before the footer section. Either a closing tag has been placed after the opening footer tag or it is missing.",
        54 => "Found an open start tag within the footer section. Either a closing tag has been placed after the closing footer tag or it is missing.",
        55 => "This tag does not contain a valid tag name and therefore isn't valid HTML.",
        56 => "This start tag is missing a matching closing tag.",
        57 => "A link element is missing a required 'href' attribute.",
        58 => "A link element's href attribute is empty. Please enter a valid link.",
        59 => "A link element is missing a required 'name' attribute.",
        60 => "A link element's 'name' attribute is empty. Please enter a valid name.",
        61 => "Only one instance of the h1 tag should be used in a single HTML document.",
        62 => "Heading elements appear in order of h1 being the most important and h6 being the least important. This heading tag has skipped one or more of the sizings.",
        
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
        
        if (in_array($error_number, array(48, 61, 62))) {
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
