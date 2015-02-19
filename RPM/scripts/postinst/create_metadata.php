<?php
if($argc<5){
    die('Usage: '.$argv[0] .' <partner id> <admin secret> <service_url> <path/to/xsd>'."\n");
}
require_once('/opt/kaltura/web/content/clientlibs/php5/KalturaClient.php');
$userId = null;
$expiry = null;
$privileges = null;
$partnerId=$argv[1];
$secret = $argv[2];
$type = KalturaSessionType::ADMIN;
$config = new KalturaConfiguration($partnerId);
$config->serviceUrl = $argv[3];
$xsdData=file_get_contents($argv[4]);
$client = new KalturaClient($config);
$ks = $client->session->start($secret, $userId, $type, $partnerId, $expiry, $privileges);
$client->setKs($ks);
$metadataObjectType=1;
$viewsData = null;

$pager=null;
$filter = new KalturaMetadataProfileFilter();
$filter->partnerIdEqual = $partnerId;
$profile_name= 'Transcript';
$filter->nameEqual = $profile_name;
$results = $client->metadataProfile->listAction($filter, $pager);
if ($results->totalCount){
    echo "NOTICE: We already have $profile_name. Exiting w/o adding.\n";
	return true;
}
$metadataProfile=new KalturaMetadataProfile(); 
$metadataProfile->name = $profile_name;

$metadataProfile->createMode = KalturaMetadataProfileCreateMode::KMC;
$metadataProfile->systemName = $profile_name;
$metadataProfile->objectType = 1;
$metadataProfile->metadataObjectType = 1;

$results = $client->metadataProfile->add($metadataProfile, $xsdData, $viewsData);
?>
