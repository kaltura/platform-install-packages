<?php
if (count($argv)<2){
    echo __FILE__ . ' <-2 partner admin secret> <partner ID> '."\n";
    exit (1);
}
$adminSecretForSigning = $argv[1];
$partnerId = $argv[2];
$config = null;
$clientConfig = null;
/* @var $clientConfig KalturaConfiguration */
$client = null;
/* @var $client KalturaClient */

require_once __DIR__ . '/init.php';


/**
 * Start a new session
 */
$client->setKs($client->generateSessionV2($adminSecretForSigning, null, KalturaSessionType::ADMIN, -2, 86400, ''));


/**
 * Delete the partner
 */
$systemPartnerClient = KalturaSystemPartnerClientPlugin::get($client);
$systemPartnerClient->systemPartner->updateStatus($partnerId, KalturaPartnerStatus::FULL_BLOCK,'Test partner');
//if ($systemPartnerClient->systemPartner->updateStatus($partnerId, KalturaPartnerStatus::FULL_BLOCK,'Test partner')){
echo "Partner [$partnerId] deleted\n";

