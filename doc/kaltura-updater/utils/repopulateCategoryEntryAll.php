<?PHP

$rootuser = @$argv[1];
$rootpw = @$argv[2];

if ( !$rootuser || !$rootpw ) {
  echo "Please run script as repopulateCategoryEntryPartner.php <rootuser> <rootpw>\n";
  die();
}

$dbh = @mysql_connect('localhost',$rootuser, $rootpw);

if ( !$dbh ) {
 echo "Could not connect to mysql, wrong credentials?\n";
 die();
}

mysql_select_db('kaltura');

$partners = mysql_query("select * from partner");

while($partner = mysql_fetch_object($partners)){
  echo "Executing repopulation for {$partner->partner_name}: {$partner->id};\n";
  shell_exec("php repopulateCategoryEntryPartner.php $rootuser $rootpw {$partner->id}");
}

