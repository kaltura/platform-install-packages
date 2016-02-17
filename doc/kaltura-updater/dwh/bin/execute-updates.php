<?PHP

echo "Globbing folders";

$sources = $argv[1];
$log = $argv[2];
$root = $argv[3];
$pw = $argv[4];

if ( !$sources || !$log || !$root || !$pw ){
	die("\nplease configure as follows: execute-updates.php [sources folder] [log output folder] [mysql super user] [mysql password]\n");
}

$files = glob("$sources/*/*.sql");
$c = count($files);
$date = date('d-m-Y-H-i-s');

shell_exec("mysql -u{$root} -p{$pw} -e \"grant all privileges on *.* to 'etl'@'localhost';\"");
shell_exec("mysql -u{$root} -p{$pw} -e \"grant all privileges on *.* to 'etl'@'127.0.0.1';'\"");

foreach ( $files as $i => $filename ){
   $process = round(($i+1)/$c*100,1);
   echo "Executing $filename, {$process}%\n";
   
   shell_exec("echo $filename >> {$log}/export_{$date}.log");
   shell_exec("mysql -u{$root} -p{$pw} < $filename >> {$log}/export_{$date}.log 2>&1");
   shell_exec("echo \n >> {$log}/export_{$date}.log");
} 
