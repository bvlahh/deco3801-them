
// set mime type with php: header("Content-type: application/x-javascript");

function set_message(text) {
    
    document.getElementById("infobox").innerHTML = text;
    
}

function messagebox(number) {
    
    if (number == 1)
        set_message("$err_test");
    
}
