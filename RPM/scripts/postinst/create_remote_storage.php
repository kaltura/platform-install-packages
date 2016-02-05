<?php

if (count($argv)<11){
    echo 'Usage:' .__FILE__ .' <service_url> <partnerid> <minus_2_admin_secret> <profile name> <delivery url> <storage host> <storage basedir> <remote storage username> <remote storage passwd> 
 <remote storage proto: FTP|SFTP|SCP|S3>
 <playback proto: APPLE_HTTP|HDS|RTMP|HTTP|AKAMAI_HD|AKAMAI_HDS>
 <delivery proto: APPLE_HTTP|HDS|HTTP|RTMP|AKAMAI_HD|AKAMAI_HDS|AKAMAI_HLS_DIRECT|AKAMAI_HLS_MANIFEST>'."\n";
    exit (1);
}
require_once('/opt/kaltura/web/content/clientlibs/php5/KalturaClient.php');

$protocols['FTP'] = KalturaStorageProfileProtocol::FTP;
$protocols['SFTP'] = KalturaStorageProfileProtocol::SFTP;
$protocols['SCP'] = KalturaStorageProfileProtocol::SCP;
$protocols['S3'] = KalturaStorageProfileProtocol::S3;


$deliveries['APPLE_HTTP'] = KalturaDeliveryProfileType::APPLE_HTTP; 
$deliveries['HDS'] = KalturaDeliveryProfileType::HDS;
$deliveries['HTTP'] = KalturaDeliveryProfileType::HTTP;
$deliveries['RTMP'] = KalturaDeliveryProfileType::RTMP;
$deliveries['AKAMAI_HD'] = KalturaDeliveryProfileType::AKAMAI_HD;
$deliveries['AKAMAI_HDS'] = KalturaDeliveryProfileType::AKAMAI_HDS;
$deliveries['AKAMAI_HLS_DIRECT'] = KalturaDeliveryProfileType::AKAMAI_HLS_DIRECT;
$deliveries['AKAMAI_HLS_MANIFEST'] = KalturaDeliveryProfileType::AKAMAI_HLS_MANIFEST;
$deliveries['AKAMAI_HLS_DIRECT'] = KalturaDeliveryProfileType::AKAMAI_HLS_DIRECT;
$deliveries['AKAMAI_HLS_MANIFEST'] = KalturaDeliveryProfileType::AKAMAI_HLS_MANIFEST;
$deliveries['AKAMAI_HD'] = KalturaDeliveryProfileType::AKAMAI_HD;
$deliveries['AKAMAI_HDS'] = KalturaDeliveryProfileType::AKAMAI_HDS;
$deliveries['AKAMAI_HTTP'] = KalturaDeliveryProfileType::AKAMAI_HTTP;
$deliveries['AKAMAI_RTMP'] = KalturaDeliveryProfileType::AKAMAI_RTMP;

$playbacks['APPLE_HTTP'] = KalturaPlaybackProtocol::APPLE_HTTP;
$playbacks['HDS'] = KalturaPlaybackProtocol::HDS;
$playbacks['RTMP'] = KalturaPlaybackProtocol::RTMP;
$playbacks['HTTP'] = KalturaPlaybackProtocol::HTTP;
$playbacks['AKAMAI_HD'] = KalturaPlaybackProtocol::AKAMAI_HD;
$playbacks['AKAMAI_HDS'] = KalturaPlaybackProtocol::AKAMAI_HDS;
         
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
	$ks = $client->session->start($secret, null, KalturaSessionType::ADMIN, -2, null,null);
	$client->setKs($ks);
	$config->partnerId=$partnerId;
	$client->setPartnerId($partnerId);
	$delivery = new KalturaDeliveryProfile();
	$delivery->name = $profile_name;
	$delivery->status = KalturaDeliveryStatus::ACTIVE;
	$delivery->type = KalturaDeliveryProfileType::HTTP;
	$delivery->streamerType = KalturaPlaybackProtocol::HTTP;
	$delivery->systemName = $profile_name;
	$delivery->url = $delivery_url;
	//$delivery->isDefault = KalturaNullableBoolean::FALSE_VALUE;
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
