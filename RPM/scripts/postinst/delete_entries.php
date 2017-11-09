<?php
if ($argc < 4){
        echo 'Usage:' .__FILE__ .' <service_url> <partner_id> <admin_secret>'."\n";
        exit (1); 
}

require_once('/opt/kaltura/web/content/clientlibs/php5/KalturaClient.php');
$userId = null;
$expiry = null;
$privileges = null;
$secret = $argv[3];
$type = KalturaSessionType::ADMIN;
$partnerId=$argv[2];
$config = new KalturaConfiguration($partnerId);
$config->serviceUrl = $argv[1];
$client = new KalturaClient($config);
$ks = $client->session->start($secret, $userId, $type, $partnerId, $expiry, $privileges);
$client->setKs($ks);
try{
    $pager = new KalturaFilterPager();
    // since this is meant to be triggered from kaltura-sanity.sh, one page with size 100 is plenty.
    $pager->pageSize = 100;
    $pager->pageIndex = 1;
    $filter = new KalturaBaseEntryFilter();
    // we want to get all entries but the deleted ones, since we're about to delete them all.
    $filter->statusNotEqual=2;
    $entryList = $client->baseEntry->listAction($filter, $pager);
}catch(KalturaException $ex){
    $message=$ex->getMessage();
    $error_code=$ex->getCode();
    echo("Failed with message: $message, error code: $error_code\n");
    exit(255);
}
if (!$entryList->totalCount){
    echo "No entries to delete.\n";
    exit(0);
}
foreach ($entryList->objects as $entry){
    try{
	$client->baseEntry->delete($entry->id);
    }catch(KalturaException $ex){
	$message=$ex->getMessage();
        $error_code=$ex->getCode();
	echo("Failed with message: $message, error code: $error_code\n");
        exit(254);
    }
}
echo "Entries for partner $partnerId deleted successfully.\n";
?>
