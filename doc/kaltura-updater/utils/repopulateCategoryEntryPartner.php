<?PHP

$rootuser = @$argv[1];
$rootpw = @$argv[2];

if ( !$rootuser || !$rootpw ) {
  echo "Please run script as repopulateCategoryEntryPartner.php <rootuser> <rootpw> <partnerid>\n";
  die();
}

$dbh = @mysql_connect('localhost',$rootuser, $rootpw);

if ( !$dbh ) {
 echo "Could not connect to mysql, wrong credentials?\n";
 die();
}

mysql_select_db('kaltura');

$partner_id = @$argv[3];  
if ( $partner_id == null ) {
  echo "Please specify a partner id\n";
  die();
}

$partner = mysql_fetch_object(mysql_query("SELECT * FROM partner where id = {$partner_id}"));

if ( $partner ) {
   echo "Found {$partner->id}: {$partner->partner_name}\n";
}else{
   echo "Invalid partnerid\n";
   die();	
}	

mysql_query('delete from category_entry where partner_id ='.$partner->id);

$q = 'select partner_id, id, full_name, full_ids from category where partner_id ='.$partner->id;
$r = mysql_query($q);
echo mysql_error();


$pattern = "(%d,'%s',%d,now(),now(),'%s',2)";

$categoriesCache = array();
while ($category = mysql_fetch_object($r)){
  $categoriesCache[$category->id] = $category;
}

echo count($categoriesCache);

$values = array();

$q2 = 'select id, name, partner_id, categories_ids from entry where partner_id ='. $partner->id;
$r = mysql_query($q2);

while ( $entry = mysql_fetch_object($r) ) {
  echo $entry->name. ":". $entry->categories_ids ."\n";
   
  $categories = explode(',',$entry->categories_ids);

  if ( $categories[0] == '' ){
     echo "Empty category ids, skipping\n\n";
     continue;
  }


  foreach ( $categories as $category ) {
     if ( !isset($categoriesCache[$category]) ){ 
	echo "missing category: $category\n\n";
        continue;
     }
     $values[] = sprintf($pattern,$entry->partner_id,$entry->id,$category,$categoriesCache[$category]->full_ids);
  }
  echo "\n";
}

$val = implode(',',$values);

$q3 = "insert into category_entry(partner_id,entry_id,category_id,created_at,updated_at,category_full_ids, status) values";

mysql_query($q3.$val);
