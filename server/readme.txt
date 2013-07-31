
The server is already set up as per the configs in ./setup_and_config

./load.sh copies the ./html directory onto the server. This works on
linux/unix (probably including mac), windows guys try cygwin or a
scp/sftp client to manually copy the html directory over. On the server
it lives at /usr/share/nginx/html/

With the current config:
The server takes the request '/REQUEST' and looks for the file:
html/REQUEST
html/REQUESTindex.html
html/REQUEST.html
html/REQUEST.php [evaluated for php]
html/REQUESTindex.php [evaluated for php]

Whichever it finds first is what it serves, otherwise 404 error.
It's set to return 404 if you ask for a .html or .php directly.
This makes nice urls without a file extension on the end.
eg:
teamthem.com/
teamthem.com/direct_input
teamthem.com/upload_file
teamthem.com/upload_zip
