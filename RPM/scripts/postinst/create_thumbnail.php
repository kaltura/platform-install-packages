<?php

if (count($argv)<6){
    echo 'Usage:' .__FILE__ .' <service_url> <partnerid> <partner admin secret> <entry_id> <offset>'."\n";
    exit (1);
}
function thumbit($client,$entry_id,$offset)
{
	try{
	}catch(exception $e){
		throw $e;
	}
}
$service_url = $argv[1];
$partnerId=$argv[2];
$secret=$argv[3];
$entry_id = $argv[4];
$basedir=dirname(__FILE__);
require_once($basedir.'/create_session.php');
$client=generate_ks($service_url,$partnerId,$secret,$type=KalturaSessionType::ADMIN,$userId=null);
$offset = $argv[5];
$result = $client->baseEntry->updatethumbnailfromsourceentry($entry_id, $entry_id, $offset);
echo ($result->thumbnailUrl);
