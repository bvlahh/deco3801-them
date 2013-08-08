<?php

require_once "misc.php";
require_once "header.php";
require_once "footer.php";
require_once "JsonRpcClient.php";

if (! array_key_exists("archive", $_FILES) )
    redirect("/upload_zip");

$filename = $_FILES["archive"]["name"];
$file = $_FILES["archive"]["tmp_name"];

$z = new ZipArchive();

if (! $z->open($file) )
    redirect("/upload_zip?upload_failed");

$parser = new JsonRpcClient("http://localhost:8080");

draw_header("Uploaded ZIP");

$archive_name = $filename;
$num_files = $z->numFiles;

$files = $num_files == 1 ? "file" : "files";

print <<<END
    
    <span style="font-weight: bold;">$archive_name</span><br/>
    $num_files $files<br/>
    <table>
        <tr>
            <th>
                Filename
            </th>
            <th>
                Size
            </th>
            <th>
                RPC Says
            </th>
        </tr>
END;

for ($i=0; $i<($z->numFiles);$i++) {
    
    $file_name = $z->getNameIndex($i);
    $file_stat = $z->statIndex($i);
    
    $file_data = $z->getFromIndex($i);
    $len = strlen($file_data);
    
    $rpc = htmlspecialchars( $parser->parse_html($file_data) );
    
    print <<<END
        
        <tr>
            <td>
                $file_name
            </td>
            <td>
                $len
            </td>
            <td>
                $rpc
            </td>
        </tr>
        
END;
    
}

print <<<END
    
    </table>
    
END;

$z->close();

draw_footer();

?>
