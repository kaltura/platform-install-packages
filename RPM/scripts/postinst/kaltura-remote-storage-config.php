<?php
if ($argc < 7 ) {
	echo 'Usage: ' . __FILE__ . ' <service_url> <partner_id> <admin@mail> <admin passwd> <FTP|SFTP|SCP|S3> <storage_display_name> <storage_url> <storage_base_dir> <delivery_url> <username> <passwd> <storage_type>'."\n";
	exit (1);
}
require_once('/opt/kaltura/web/content/clientlibs/php5/KalturaClient.php');

$protocols['FTP'] = KalturaStorageProfileProtocol::FTP;
$protocols['SFTP'] = KalturaStorageProfileProtocol::SFTP;
$protocols['SCP'] = KalturaStorageProfileProtocol::SCP;
$protocols['S3'] = KalturaStorageProfileProtocol::S3;

define('AKAMAI', 1);
define('S3', 0);

$service_url=$argv[1];
$partner_id=$argv[2];
$minus2_mail=$argv[3];
$minus2_passwd=$argv[4];
$protocol=$argv[5];
$storage_display_name=$argv[6];
$storage_url=$argv[7];
$storage_base_dir=$argv[8];
$delivery_url=$argv[9];
$username=$argv[10];
$passwd=$argv[11];
$storage_type=$argv[12];
$config = new KalturaConfiguration($partner_id);
$config->serviceUrl = $service_url;
$client = new KalturaClient($config);
$user_id=null;
$expiry=null;
$privileges=null;
$type = KalturaSessionType::ADMIN;
$ks = $client->user->login(-2,$minus2_mail, $minus2_passwd, $expiry, $privileges);

$client->setKs($ks);
$config->partnerId=$partner_id;
$client->setPartnerId($partner_id);
if ($storage_type == S3){
	$storageProfile = new KalturaAmazonS3StorageProfile();
	$storageProfile->filesPermissionInS3 = KalturaAmazonS3StorageProfileFilesPermissionLevel::ACL_PUBLIC_READ;
}else{
	$storageProfile = new KalturaStorageProfile();
}
$storageProfile->name = $storage_display_name;
$storageProfile->systemName = $storage_display_name;
$storageProfile->desciption = $storage_display_name.' - auto generated by '. __FILE__."\n";
$storageProfile->pathManagerClass = 'kPathManager';
$storageProfile->status = KalturaStorageProfileStatus::AUTOMATIC;
$storageProfile->protocol = $protocols[$protocol];
$storageProfile->storageUrl = $storage_url;
$storageProfile->storageBaseDir = $storage_base_dir;
$storageProfile->storageUsername = $username;
$storageProfile->storagePassword = $passwd;
$storageProfile->deliveryHttpsBaseUrl = $delivery_url;
$storageProfile->deliveryHttpBaseUrl = $delivery_url;
$storageProfile->deliveryRmpBaseUrl = null;
$storageProfile->flavorParamsIds = 0;
$storageProfile->deliveryPriority = 0;
//$storageProfile->urlManagerClass = 'MANAGER_CLASS';
$storageProfile->urlManagerParams = array();
$storageProfile->urlManagerParams[0] = null;
$storageProfile->readyBehavior = null;
$result = $client->storageProfile->add($storageProfile);
?>
