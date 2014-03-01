<?php
require_once('/usr/local/lib/php5/KalturaClient.php');
function generate_ks($service_url,$partnerId,$secret,$type=KalturaSessionType::ADMIN,$userId=null,$expiry = null,$privileges = null)
{
    $config = new KalturaConfiguration($partnerId);
    $config->serviceUrl = $service_url;  
    $client = new KalturaClient($config);
    $ks = $client->session->start($secret, $userId, $type, $partnerId, $expiry, $privileges);
    $client->setKs($ks);
    return ($client);
}
?>
