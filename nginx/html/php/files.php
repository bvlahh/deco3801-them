<?php

function create_set() {
    create_set(in php_session text)
}

function add_file() {
    add_file(in upload_set int, in filename text, in document text, in cached_parse text)
}

function cache_parse() {
    cache_parse(in file int, in parse_data text) 
}

function get_file() {
    get_file(in file int)
}

function touch_set() {
    touch_set(in set_id int)
}

function touch_file() {
    touch_file(in file_id int)
}

?>
