<?php

class Errors
{
    /**
    * A mapping of error codes to their associated error message.
    */
    static $error_strings = array(
        
        1 => "No valid doctype was found.",
        2 => "Multiple instance of a singular tag.",
        3 => "A singular start tag was placed in the wrong location.",
        4 => "A singular closing tag was placed in the wrong location.",
        5 => "A starting tag was placed before the head section.",
        6 => "A closing tag was placed before the head section.",
        7 => "This starting tag is not valid within the head section.",
        8 => "This closing tag is not valid within the head section.",
        9 => "No start head tag was found in the document.",
        10 => "No closing head tag was found in the document.",
        11 => "A closing HTML tag was found before the closing body tag.",
        12 => "A start tag was found after the expected closing HTML tag.",
        13 => "A closing tag was found after the expected closing HTML tag.",
        14 => "This closing tag is missing a matching start tag.",
        15 => "A misplaced closing tag was found after the closing body tag.",
        16 => "The document is missing a closing HTML tag.",
        17 => "The tag has a symbol in place of a valid tag name.",
        18 => "A closing angled bracket was found instead of a tag name.",
        19 => "A question mark was found instead of a tag name.",
        20 => "A closing tag cannot contain a self closing solidus symbol '/'.",
        21 => "This tag is not a self closing void tag type.",
        22 => "Br tags are self closing and don't require a closing tag.",
        23 => "A void tag is missing the self closing backslash symbol.",
        24 => "One or more attributes were found in a closing tag.",
        25 => "Closing HTML tag found before the head phase. Misplaced closing HTML tag or missing head and body sections.",
        26 => "Closing HTML tag found in head phase. Misplaced closing HTML tag or missing closing head tag.",
        27 => "Closing HTML tag found before body phase. Misplaced closing HTML tag or missing body tags.",
        28 => "Closing HTML tag found in the body phase. Misplaced closing HTML tag or missing closing body tag.",
        29 => "This start tag is of a tag type which belongs within the head section.",
        30 => "Found a start tag after the head phase and before the body phase, implying that it is misplaced.",
        31 => "Found a closing tag after the head phase and before the body phase, implying that it is misplaced.",
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
        if ($error_number == 1)
            return "#7f7fff";
        
        return "#ff7f7f";
        
    }
    
}

?>
