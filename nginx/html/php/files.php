<?php

//$res = $mysqli->query("SELECT NOW();");
//while ( $row = $res->fetch_assoc() )
//    print_r( $row );

function create_set($text) {
    
    $mysqli = new mysqli("localhost");
    $mysqli->select_db("validator");
    $text = $mysqli->real_escape_string($text);
    $res = $mysqli->query("call create_set(\"$text\");");
    $row = $res->fetch_array();
    return $row[0];
    
}

function add_file($upload_set, $filename, $document, $parse_data) {
    
    $mysqli = new mysqli("localhost");
    $mysqli->select_db("validator");
    $upload_set = (int)$upload_set;
    $filename = $mysqli->real_escape_string($filename);
    $document = $mysqli->real_escape_string($document);
    $parse_data = $mysqli->real_escape_string($parse_data);
    $res = $mysqli->query("call add_file($upload_set, \"$filename\", \"$document\", \"$parse_data\");");
    if (! $res)
        die($mysqli->error);
    $row = $res->fetch_array();
    return $row[0];
    
}

function cache_parse($file_id, $parse_data) {
    
    $mysqli = new mysqli("localhost");
    $mysqli->select_db("validator");
    $file_id = (int)$file_id;
    $parse_data = $mysqli->real_escape_string($parse_data);
    $res = $mysqli->query("call cache_parse($file_id, \"$parse_data\");");
    
}

function get_file($file_id) {
    
    $mysqli = new mysqli("localhost");
    $mysqli->select_db("validator");
    $file_id = $mysqli->real_escape_string($file_id);
    $res = $mysqli->query("call get_file(\"$file_id\");");
    $row = $res->fetch_assoc();
    return $row;
    
}

?>
