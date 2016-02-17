<?php
if($argc<7){
    die('Usage: '.$argv[0] .' <partner id> <admin secret> <service_url> <entry_id> <captions_file> <language>'."\n");
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
$entryId = $argv[4];
$captions=file_get_contents($argv[5]);
$language=strtoupper($argv[6]);
$client = new KalturaClient($config);
$ks = $client->session->start($secret, $userId, $type, $partnerId, $expiry, $privileges);
$client->setKs($ks);

$captionAsset = new KalturaCaptionAsset();
$captionAsset->language = constant("KalturaLanguage::".$language);
$captionPlugin = KalturaCaptionClientPlugin::get($client);
$result = $captionPlugin->captionAsset->add($entryId, $captionAsset);
$id = $result->id;
$contentResource = new KalturaStringResource();
$contentResource->content = $captions;
$captionPlugin = KalturaCaptionClientPlugin::get($client);
$result = $captionPlugin->captionAsset->setContent($id, $contentResource);
echo($result->id);
?>
