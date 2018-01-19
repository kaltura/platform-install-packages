<?php
if (count($argv)<4){
        echo "Usage: ".__FILE__ ."<service_url> <partner_id> <admin_secret> <entry_id>\n";
        exit (1); 
}
$basedir=dirname(__FILE__);
require_once($basedir.'/create_session.php');
$userId = null;
$expiry = null;
$privileges = null;
$secret = $argv[3];
$partnerId=$argv[2];
$config = new KalturaConfiguration($partnerId);
$service_url= $argv[1];
$config->serviceUrl = $service_url;
$client=generate_ks($service_url,$partnerId,$secret,KalturaSessionType::ADMIN,$userId);
$entryId = $argv[4];
$conversionProfileId =null ;
$dynamicConversionAttributes=null;
$results = $client->media->convert($entryId, $conversionProfileId, $dynamicConversionAttributes);
?>
