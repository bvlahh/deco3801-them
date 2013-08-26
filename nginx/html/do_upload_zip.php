<?php

require_once "misc.php";
require_once "header.php";
require_once "footer.php";
require_once "rpc_client.php";

if (! array_key_exists("archive", $_FILES) )
    redirect("/upload_zip");

$filename = $_FILES["archive"]["name"];
$file = $_FILES["archive"]["tmp_name"];

$zip = new ZipArchive();

if (! $zip->open($file) )
    redirect("/upload_zip?upload_failed");

draw_header("THEM prototype - Uploaded ZIP");

$archive_name = $filename;
$num_files = $zip->numFiles;

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

$filenames = array();
for ($i=0; $i<($zip->numFiles);$i++)
	$filenames[] = $zip->getNameIndex($i);

for ($i=0; $i<($zip->numFiles);$i++) {
    
    $file_name = $zip->getNameIndex($i);
    $file_stat = $zip->statIndex($i);
    
    $file_data = $zip->getFromIndex($i);
    $len = strlen($file_data);
    
    //$rpc = htmlspecialchars( rpc_validate($filenames, base64_encode($file_data)) );
    $rpc = "";
    
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

$zip->close();

draw_footer();

?>
