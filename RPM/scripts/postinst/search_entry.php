<?php
if($argc<4){
    die('Usage: '.$argv[0] .' <partner id> <user secret> <service_url> <search string> '."\n");
}
require_once('/opt/kaltura/web/content/clientlibs/php5/KalturaClient.php');
$userId = null;
$expiry = null;
$privileges = null;
$partnerId=$argv[1];
$secret = $argv[2];
$type = KalturaSessionType::USER;
$config = new KalturaConfiguration($partnerId);
$config->serviceUrl = $argv[3];
$search_string=$argv[4];
$client = new KalturaClient($config);
$ks = $client->session->start($secret, $userId, $type, $partnerId, $expiry, $privileges);
$client->setKs($ks);

$filter = new KalturaBaseEntryFilter();
$filter->searchTextMatchOr = $search_string;
$pager = null;
$result = $client->baseEntry->listAction($filter, $pager);
echo "The string '$search_string' was found in the tags of these entries:
===================================================================================================================================
";
foreach($result->objects as $entry){
	echo "Entry ID: " . $entry->id."\nName: ". $entry->name."\nDescription: ".$entry->description."\nTags: ".$entry->tags."\n\n\n";
}

$entryFilter = new KalturaBaseEntryFilter();
$entryFilter->advancedSearch = new KalturaCategoryEntryAdvancedFilter();
$captionAssetItemFilter = new KalturaCaptionAssetItemFilter();
$captionAssetItemFilter->contentMultiLikeOr = $search_string;
$captionAssetItemPager = null;
$captionsearchPlugin = KalturaCaptionsearchClientPlugin::get($client);
$result = $captionsearchPlugin->captionAssetItem->searchEntries($entryFilter, $captionAssetItemFilter, $captionAssetItemPager);
echo "The string '$search_string' was also found is caption assets of these entries:
==============================================================================================================================
";
foreach($result->objects as $entry){
	$filter = new KalturaAssetFilter();
	$filter->advancedSearch = new KalturaEntryCaptionAssetSearchItem();
	$filter->entryIdEqual = $entry->id;
	$pager = null;
	$captionPlugin = KalturaCaptionClientPlugin::get($client);
	$result = $captionPlugin->captionAsset->listAction($filter, $pager);
	$storageId = null;
	$url = $captionPlugin->captionAsset->geturl($result->objects[0]->id, $storageId);
	echo "Entry ID: " . $entry->id."\nName: ". $entry->name."\nDescription: ".$entry->description."\nCaption file URL: $url\n\n\n";
}
?>
