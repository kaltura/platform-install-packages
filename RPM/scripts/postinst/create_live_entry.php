#!/usr/bin/php
<?php
if($argc<2){
    die('Usage: '.$argv[0] .'<query string in the following format: partner_id=&partner_secret=&service_url=&nginx_endpoint=&entry_name=>'."\n");
}
require_once('/opt/kaltura/web/content/clientlibs/php5/KalturaClient.php');
$userId = null;
$expiry = null;
$privileges = null;
$mandatory_args=array('partner_id','partner_secret','nginx_endpoint','entry_name','service_url');
parse_str($argv[1],$args_arr);
foreach ($mandatory_args as $arg){
        if(!isset($args_arr[$arg])){
                die("Missing arg: $arg\n");
        }
}
if(isset($args_arr['is_ssl']) && in_array(strtolower($args_arr['is_ssl']),array('1','y','true'))){
        $protocol='https';
}else{
        $protocol='http';
}
$partnerId = $args_arr['partner_id'];
$secret = $args_arr['partner_secret'];
$nginx_endpoint = $protocol.'://'.$args_arr['nginx_endpoint'];
$streamName = $args_arr['entry_name'];
$type = KalturaSessionType::ADMIN;
$config = new KalturaConfiguration($partnerId);
$config->serviceUrl = $protocol.'://'.$args_arr['service_url'];
$client = new KalturaClient($config);
$ks = $client->session->start($secret, $userId, $type, $partnerId, $expiry, $privileges);
$client->setKs($ks);
$liveStreamEntry = new KalturaLiveStreamEntry();
$liveStreamEntry->streamName = $streamName;
$liveStreamEntry->dvrStatus  = 1;
$liveStreamEntry->name = $streamName;
$liveStreamEntry->mediaType = KalturaMediaType::LIVE_STREAM_FLASH;
$liveStreamEntry->hlsStreamUrl = "$nginx_endpoint/hlsme/$streamName.m3u8";
$liveStreamEntry->liveStreamConfigurations[0] = new KalturaLiveStreamConfiguration();
$liveStreamEntry->liveStreamConfigurations[0]->protocol=KalturaPlaybackProtocol::APPLE_HTTP;
$liveStreamEntry->liveStreamConfigurations[0]->streamName=$streamName;
$liveStreamEntry->liveStreamConfigurations[0]->url= "$nginx_endpoint/hlsme/$streamName.m3u8";

$sourceType = KalturaSourceType::MANUAL_LIVE_STREAM;
$result = $client->liveStream->add($liveStreamEntry, $sourceType);

?>
