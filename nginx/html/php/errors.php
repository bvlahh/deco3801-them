<?php

class Errors
{
    
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
        15=> "A misplaced closing tag was found after the closing body tag.",
        
    );
    
    static function errorString($error_number) {
        
        return Errors::$error_strings[$error_number];
        
    }
    
    static function errorColor($error_number) {
        
        return "#ff7f7f";
        
    }
    
}

?>
