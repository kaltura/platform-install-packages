<?php

if (count($argv)<5){
    echo 'Usage:' .__FILE__ .' <service_url> <partnerid> <admin_secret> <entry_id to clip>'."\n";
    exit (1);
}
function clipi($client,$entry_id,$overwrite)
{
	try{
	// Params
	$overwrite=false; //Decides whether to trim the entry or clip it

	// Entry Data
	$startTime = 100; //Set the start time of the clip / trim in milliseconds
	$endTime = 5000; //Set the end time of the clip / trim in milliseconds
	$clipDuration = $endTime - $startTime;

	// Create New Clip
	$operation1 = new KalturaClipAttributes();
	$operation1->offset = $startTime;
	$operation1->duration = $clipDuration;

	// Add New Resource
	$resource = new KalturaOperationResource();
	$resource->resource = new KalturaEntryResource();
	$resource->resource->entryId = $entry_id;
	$resource->operationAttributes = array($operation1);

	if( $overwrite ) {
		// Trim Entry
		try {
			$resultEntry = $client->media->updateContent($entry_id, $resource);
			return $resultEntry->id;
		} catch( Exception $e ){
			die('{"error": "' . $e->getMessage() . '"}');
		}
	} else {
		// Create New Media Entry
		$entry = new KalturaMediaEntry();
		$entry->name = "New Clipped sanity";
		$entry->description = "Run by kaltura-sanity.sh";
		$entry->mediaType = 1; //The new media type

		// New Clip
		$clipped_one = $client->media->add($entry);
		$clipped_one = $client->media->addContent($clipped_one->id, $resource);
		return $clipped_one->id;
	}
	
	}catch(exception $e){
		throw $e;
	}
}
$service_url = $argv[1];
$partnerId=$argv[2];
$secret=$argv[3];
$entry_id = $argv[4];
$overwrite = $argv[5];
$basedir=dirname(__FILE__);
require_once($basedir.'/create_session.php');
$client=generate_ks($service_url,$partnerId,$secret,$type=KalturaSessionType::ADMIN,$userId=null);
echo(clipi($client,$entry_id,$overwrite)). " was created.\n";
