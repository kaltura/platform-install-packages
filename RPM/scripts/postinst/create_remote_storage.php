<?php

if (count($argv)<4){
    echo 'Usage:' .__FILE__ .' <service_url> <partnerid> <minus_2_secret> <delivery profile name> <delivery url> <storage profile name> <storage host> <storage basedir> <remote storage username> <remote storage passwd> <playback proto>'."\n";
    exit (1);
}

$service_url = $argv[1];
$partnerId=$argv[2];
$secret=$argv[3];
$basedir=dirname(__FILE__);
$config = new KalturaConfiguration($partnerId);
$config->serviceUrl = $service_url;  
$client = new KalturaClient($config);
$config->partnerId=$partnerId;
$client->setConfig($config);
$ks = $client->session->start($secret, null, KalturaSessionType::ADMIN, -2, null,null);
$client->setKs($ks);
$delivery = new KalturaDeliveryProfile();
$delivery->name = 'jess0_testme';
$delivery->type = KalturaDeliveryProfileType::HTTP;
$delivery->systemName = 'jess0_testme';
$delivery->url = 'http://ce-csi.dev.kaltura.com:73';
$delivery->isDefault = KalturaNullableBoolean::TRUE_VALUE;
var_dump($client->deliveryProfile->add($delivery));

$storageProfile = new KalturaStorageProfile();
$storageProfile->name = 'stor';
$storageProfile->systemName = 'stor';
$storageProfile->status = KalturaStorageProfileStatus::AUTOMATIC;
$storageProfile->protocol = KalturaStorageProfileProtocol::SFTP;
$storageProfile->storageUrl = 'ce-csi.dev.kaltura.com';
$storageProfile->storageBaseDir = '/home/jess';
$storageProfile->storageUsername = 'jess';
$storageProfile->storagePassword = 'jessport';
$storageProfile->deliveryProfileIds = array();
$storageProfile->deliveryProfileIds[0] = new KalturaKeyValue();
$storageProfile->deliveryProfileIds[0]->key = 'http';
$storageProfile->deliveryProfileIds[0]->value = '3';
$result = $client->storageProfile->add($storageProfile);
var_dump($result);
