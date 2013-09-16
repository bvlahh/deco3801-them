<?php

class Errors
{
    /**
    * A mapping of error codes to their associated error message.
    */
    static $error_strings = array(
        
        1 => "No valid doctype was found. HTML files should start with <!DOCTYPE html>.",
        2 => "Multiple instance of a singular tag.",
        3 => "A singular start tag was placed in the wrong location.",
        4 => "A singular closing tag was placed in the wrong location.",
        5 => "A starting tag was placed before the head section.",
        6 => "A closing tag was placed before the head section.",
        7 => "This starting tag is not valid within the head section. It should probably go in the body section instead, along with its closing tag!",
        8 => "This closing tag is not valid within the head section. It should probably go in the body section instead, along with its starting tag!",
        9 => "No start head tag was found in the expected context, implying that no head section exists.",
        10 => "No closing head tag was found in the expected context, implying that the head section doesn't exist or that it wasn't closed correctly.",
        11 => "A closing HTML tag was found in an unexpected location. Closing the HTML tag is usually the final line of the webpage.",
        12 => "A start tag was found after the expected closing HTML tag.",
        13 => "A closing tag was found after the expected closing HTML tag.",
        14 => "This closing tag is missing a matching start tag.",
        15 => "A misplaced closing tag was found after the closing body tag.",
        16 => "The document is missing a closing HTML tag.",
        17 => "The tag has a symbol in place of a valid tag name.",
        18 => "A closing angled bracket was found instead of a tag name.",
        19 => "A question mark was found instead of a tag name.",
        20 => "A closing tag cannot contain a self closing solidus symbol '/'.",
        21 => "This tag is not a self closing void tag type. It should have a closing tag, </tagname>, and not be written as <tagname />.",
        22 => "Br tags are self closing and don't require a closing tag. Instead of <br></br>, you just need to use <br />.",
        23 => "A void tag is missing the self closing backslash symbol. For example, <br> instead of <br />, or <img src='img.png'> instead of <img src='img.png'/>",
        24 => "One or more attributes were found in a closing tag. A closing tag should just be </tagname>.",
        25 => "Closing HTML tag found before the head phase. Misplaced closing HTML tag or missing head and body sections.",
        26 => "Closing HTML tag found in head phase. Misplaced closing HTML tag or missing closing head tag.",
        27 => "Closing HTML tag found before body phase. Misplaced closing HTML tag or missing body tags.",
        28 => "Closing HTML tag found in the body phase. Misplaced closing HTML tag or missing closing body tag.",
        29 => "This start tag is of a tag type which belongs within the head section. Move it to before the </head> closing tag!",
        30 => "Found a start tag after the head phase and before the body phase, implying that it is misplaced.",
        31 => "Found a closing tag after the head phase and before the body phase, implying that it is misplaced.",
        32 => "No starting body tag was found in the expected context, implying that no body section exists.",
        33 => "No closing body tag was found in the expected context, implying that no body section exists or it wasn't closed properly.",
        34 => "The document is missing a starting HTML tag.",
        35 => "Unknown DOCTYPE. HTML5 uses <!DOCTYPE html>.",
        36 => "There is a missing space after the doctype declaration. Correct form: <!DOCTYPE html>.",
        37 => "No valid doctype was found. HTML files should start with <!DOCTYPE html>.",
        38 => "The document is empty.",
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
    static function errorColor($error_number) {
        
        // hacked testing
        /*if ($error_number == 1)
            return "#7f7fff";*/
        
        return "#ff7f7f";
        
    }
    
}

?>
