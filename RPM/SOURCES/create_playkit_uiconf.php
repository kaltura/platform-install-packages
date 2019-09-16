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
$tags="autodeploy,playerV3Versions_latest,playerV3Versions_list,7.5,playerV3Versions,latest";
 // I'm somewhat hopeful the version for the other plugins won't change very often but we may have to modify the code so that their versions are passed as args as well later on..
$config="{\"kaltura-ovp-player\":\"$playerVersion\",\"playkit-ima\":\"0.17.2\",\"playkit-youbora\":\"1.1.1\",\"playkit-google-analytics\":\"0.1.5\",\"playkit-offline-manager\":\"1.2.0\",\"playkit-cast-sender\":\"0.2.5\",\"playkit-cast-receiver\":\"0.3.0\",\"playkit-vr\":\"1.3.0\",\"path\":\"0.1.7\",\"playkit-flash\":\"1.4.0\",\"playkit-youtube\":\"1.2.1\",\"playkit-bumper\":\"1.3.2\"}";
$filter = new KalturaUiConfFilter();
$filter->tagsMultiLikeAnd = $tags;
$pager = new KalturaFilterPager();
$uiConf = new KalturaUiConf();
$uiConf->config = $config;
$uiConf->tags = $tags;

try {
        $result = $client->uiConf->listAction($filter, $pager);
        // if we already have one or more of these, let's upgrade them to the latest version
        if ($result->totalCount > 0 ){
                foreach ($result->objects as $v3uiConf){
                        $result = $client->uiConf->update($v3uiConf->id, $uiConf);
                }
        // otherwise, let's create one
        }else{
                $uiConf->creationMode = KalturaUiConfCreationMode::ADVANCED;
                $uiConf->objType = KalturaUiConfObjType::APP_STUDIO;
                $uiConf->name = "playkitVersions";
                $uiConf->useCdn = true;
                $uiConf->isPublic = true;
                $uiConf->swfUrl = "/";
                try {
                        $result = $client->uiConf->add($uiConf);
                } catch (Exception $e) {
                        echo $e->getMessage();
			exit (2);
                }
        }
} catch (Exception $e) {
        echo $e->getMessage();
	exit (1);
}
?>
