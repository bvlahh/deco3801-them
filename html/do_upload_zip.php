<?

require_once "misc.php";
require_once "header.php";
require_once "footer.php";

if (! array_key_exists("archive", $_FILES) )
    redirect("/upload_zip");

$filename = $_FILES["archive"]["name"];
$file = $_FILES["archive"]["tmp_name"];

$za = new ZipArchive();

$za->open($file);

draw_header("");

print "<pre>";

print_r($za);

var_dump($za);

echo "numFiles: " . $za->numFiles . "\n";
echo "status: " . $za->status  . "\n";
echo "statusSys: " . $za->statusSys . "\n";
echo "filename: " . $za->filename . "\n";
echo "comment: " . $za->comment . "\n";

for ($i=0; $i<$za->numFiles;$i++) {
    echo "index: $i\n";
    print_r($za->statIndex($i));
}

echo "numFile:" . $za->numFiles . "\n";

print "</pre>";

draw_footer();

?>
