#!/usr/bin/php
<?php

require_once('/opt/kaltura/app/clients/php5/KalturaClient.php');

$xml_file_path="/usr/local/WowzaStreamingEngine/conf/Server.xml";


/**
 * @param $xml_file_path
 * @param $admin_secret
 * @return KalturaClient
 */
function initClient ($xml_file_path, $partner_id, $admin_secret) {
    $config = new KalturaConfiguration();
    $config->serviceUrl = getValueFromXml($xml_file_path,"Server/Properties/Property[1]/Value").'/';
    $client = new KalturaClient($config);
    $result = $client->session->start($admin_secret, null, KalturaSessionType::ADMIN, $partner_id, null, null);
    $client->setKs($result);
    return $client;
}


/**
 * @param $xml_file_path
 * @param $client
 */
function registerMediaServer ($xml_file_path, $client, $sys_hostname) {
    $media_server_tag = "_media_server";
    $media_server_default_port = 1935;
    $media_server_default_protocol = "http";

    $serverNode = new KalturaWowzaMediaServerNode();
    $serverNode->name = $sys_hostname.$media_server_tag;
    $serverNode->systemName = '';
    $serverNode->description = 'Registered using '. __FILE__;
    $serverNode->hostName = $sys_hostname;
    $serverNode->liveServicePort = $media_server_default_port;
    $serverNode->liveServiceProtocol = $media_server_default_protocol;
    try {
        (array)$res = $client->serverNode->add($serverNode);
    } catch (KalturaException $ex) {
                if ($ex->getCode() == 'HOST_NAME_ALREADY_EXISTS'){
                        logToFIle($ex->getMessage());
                        exit(0);
                }else{
                        logToFIle('ERROR! CODE: ' .$ex->getCode() . ' Message: '. $ex->getMessage());
                        exit(1);
                }
    }
    $client->serverNode->enable($res->id);
    logToFIle ('['.$sys_hostname."] registered with id: ".$res->id.PHP_EOL);
}

function logToFIle ($message) {
    echo "$message\n";
}


/**
 * @param $xml_file
 * @param $xml_path
 * @return SimpleXMLElement
 */
function getValueFromXml ($xml_file, $xml_path) {
    $xml = simplexml_load_file($xml_file);
    $result = $xml->xpath($xml_path);
    return $result[0];
}

// main
$partner_id = getValueFromXml($xml_file_path, "Server/Properties/Property[2]/Value");
$xml_admin_secret = getValueFromXml($xml_file_path, "Server/Properties/Property[3]/Value");
$new_client = initClient($xml_file_path, $partner_id,$xml_admin_secret);
if(isset($argv[1])){
        $node_hostname=$argv[1];
}else{
    $node_hostname = php_uname('n');
}
registerMediaServer ($xml_file_path, $new_client,$node_hostname);

