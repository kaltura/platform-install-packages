<?php

if (count($argv)<11){
    echo 'Usage:' .__FILE__ .' <service_url> <partnerid> <minus_2_secret> <profile name> <delivery url> <storage host> <storage basedir> <remote storage username> <remote storage passwd> <remote storage protocol;i.e: FTP|SFTP|SCP|S3> <playback proto>'."\n";
    exit (1);
}
require_once('/opt/kaltura/web/content/clientlibs/php5/KalturaClient.php');

$protocols['FTP'] = KalturaStorageProfileProtocol::FTP;
$protocols['SFTP'] = KalturaStorageProfileProtocol::SFTP;
$protocols['SCP'] = KalturaStorageProfileProtocol::SCP;
$protocols['S3'] = KalturaStorageProfileProtocol::S3;



$service_url = $argv[1];
$partnerId=$argv[2];
$secret=$argv[3];
$profile_name=$argv[4];
$delivery_url=$argv[5];
$storage_host=$argv[6];
$storage_basedir=$argv[7];
$storage_user=$argv[8];
$storage_passwd=$argv[9];
$basedir=dirname(__FILE__);
$storage_protocol=$argv[10];
$playback_protocol=$argv[11];

try{
	$config = new KalturaConfiguration($partnerId);
	$config->serviceUrl = $service_url;  
	$client = new KalturaClient($config);
	$config->partnerId=$partnerId;
	$client->setConfig($config);
	$ks = $client->session->start($secret, null, KalturaSessionType::ADMIN, -2, null,null);
	$client->setKs($ks);
	$delivery = new KalturaDeliveryProfile();
	$delivery->name = $profile_name;
	$delivery->status = KalturaDeliveryStatus::ACTIVE;
	$delivery->type = KalturaDeliveryProfileType::HTTP;
	$delivery->streamerType = KalturaPlaybackProtocol::HTTP;
	$delivery->systemName = $profile_name;
	$delivery->url = $delivery_url;
	$delivery->isDefault = KalturaNullableBoolean::FALSE_VALUE;
	$delivery_obj=$client->deliveryProfile->add($delivery);
	if ($protocols[$storage_protocol] === 'S3'){
		$storageProfile = new KalturaAmazonS3StorageProfile();
		$storageProfile->filesPermissionInS3 = KalturaAmazonS3StorageProfileFilesPermissionLevel::ACL_PUBLIC_READ;
	}else{
		$storageProfile = new KalturaStorageProfile();
	}

	$storageProfile->name = $profile_name;
	$storageProfile->systemName = $profile_name;
	$storageProfile->status = KalturaStorageProfileStatus::AUTOMATIC;
	$storageProfile->protocol = $protocols[$storage_protocol];
	$storageProfile->storageUrl = $storage_host;
	$storageProfile->storageBaseDir = $storage_basedir;
	$storageProfile->storageUsername = $storage_user;
	$storageProfile->storagePassword = $storage_passwd;
	$storageProfile->deliveryProfileIds = array();
	$storageProfile->deliveryProfileIds[0] = new KalturaKeyValue();
	$storageProfile->deliveryProfileIds[0]->key = $playback_protocol;
	$storageProfile->deliveryProfileIds[0]->value = $delivery_obj->id;
	$result = $client->storageProfile->add($storageProfile);
	return($result);
}catch(exception $e){
	var_dump($e);
}
