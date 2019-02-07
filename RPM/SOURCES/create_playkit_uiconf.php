<?php
if($argc<5){
    die('Usage: '.$argv[0] .' <partner id> <admin secret> <service_url> <player version>'."\n");
}
require_once('/opt/kaltura/web/content/clientlibs/php5/KalturaClient.php');
$partnerId=$argv[1];
$secret = $argv[2];
$config = new KalturaConfiguration($partnerId);
$config->serviceUrl = $argv[3];
$playerVersion=$argv[4];

$client = new KalturaClient($config);
$ks = $client->session->start(
$secret,
null,
KalturaSessionType::ADMIN,
$partnerId);
$client->setKS($ks);

$uiConf = new KalturaUiConf();
$uiConf->creationMode = KalturaUiConfCreationMode::ADVANCED;
$uiConf->objType = KalturaUiConfObjType::APP_STUDIO;
$uiConf->name = "playkitVersions";
$uiConf->useCdn = true;
$uiConf->isPublic = true;
$uiConf->swfUrl = "/";
$uiConf->tags = "autodeploy, playerV3Versions_latest, playerV3Versions_list,7.5,playerV3Versions,latest";
// I'm somewhat hopeful the version for the other plugins won't change very often but we may have to modify the code so that their versions are passed as args as well later on..
$uiConf->config = "{\"kaltura-ovp-player\":\"$playerVersion\",\"playkit-ima\":\"0.8.7\",\"playkit-youbora\":\"0.4.2\",\"playkit-comscore\":\"2.1.4\",\"playkit-google-analytics\":\"0.1.3\",\"playkit-offline-manager\":\"1.2.0\",\"playkit-cast-sender\":\"0.2.2\",\"playkit-cast-receiver\":\"0.2.0\",\"playkit-vr\":\"1.1.8\",\"playkit-flash\":\"1.2.1\"}";

try {
        $result = $client->uiConf->add($uiConf);
        var_dump($result);
} catch (Exception $e) {
        echo $e->getMessage();
}
?>
