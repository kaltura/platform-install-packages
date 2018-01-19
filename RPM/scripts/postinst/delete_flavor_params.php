<?php
if (count($argv)<2){
    echo __FILE__ . ' <admin_secret> <service_url> <flavor_id>'."\n";
    exit (1);
}
require_once('/opt/kaltura/web/content/clientlibs/php5/KalturaClient.php');
require_once(__DIR__.'/create_session.php');
$userId = null;
$expiry = null;
$privileges = null;
// get with:
// mysql> select admin_secret from partner where id=0\G
$secret = $argv[1];
$type = KalturaSessionType::ADMIN;
$partnerId=0;
$service_url= $argv[2];
$flavor_id=$argv[3];
$client=generate_ks($service_url,$partnerId,$secret,$type,null,null,null);
$flavorParams = new KalturaFlavorParams();
try{
$results = $client->flavorParams->delete($flavor_id);
}catch(KalturaException $ex){
	echo $ex->getMessage();
	exit (1);
}
$filter = new KalturaFlavorParamsFilter();
$filter->idEqual = $flavor_id;
try{
	$results = $client->flavorParams->listAction($filter, null);
}catch(KalturaException $ex){
	echo $ex->getMessage();
	exit (1);
}
echo "flavor ID $flavor_id deleted successfully.";

?>


