<?php
if (count($argv)<3){
        echo 'Usage:' .__FILE__ .' <service_url> <partner_id> <admin_secret> <entry_id>'."\n";
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
$entryId = $argv[4];
$client = new KalturaClient($config);
$ks = $client->session->start($secret, $userId, $type, $partnerId, $expiry, $privileges);
$client->setKs($ks);
try{
    $result = $client->baseEntry->delete($entryId);
}catch(KalturaException $ex){
    $message=$ex->getMessage();
    $error_code=$ex->getCode();
    echo("Failed with message: $message, error code: $error_code\n");
    exit(255);
}
?>
