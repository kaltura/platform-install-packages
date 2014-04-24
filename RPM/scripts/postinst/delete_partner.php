<?php
$config = null;
$clientConfig = null;
/* @var $clientConfig KalturaConfiguration */
$client = null;
/* @var $client KalturaClient */

require_once __DIR__ . '/init.php';


/**
 * Start a new session
 */
$adminSecretForSigning = $config['adminConsoleSession']['adminConsoleSecret'];
$client->setKs($client->generateSessionV2($adminSecretForSigning, null, KalturaSessionType::ADMIN, -2, 86400, ''));


$partnerId = $config['session']['partnerId'];
/**
 * Delete the partner
 */
$systemPartnerClient = KalturaSystemPartnerClientPlugin::get($client);
$systemPartnerClient->systemPartner->updateStatus($partnerId, KalturaPartnerStatus::FULL_BLOCK,'Test partner');
//if ($systemPartnerClient->systemPartner->updateStatus($partnerId, KalturaPartnerStatus::FULL_BLOCK,'Test partner')){
echo "Partner [$partnerId] deleted\n";

