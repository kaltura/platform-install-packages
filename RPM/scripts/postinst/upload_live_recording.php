#!/usr/bin/php
<?php

if (count($argv)<3){
    echo 'Usage:' .__FILE__ .' <query string in the following format: partner_id=&partner_secret=&service_url=&entry_name=> </path/to/recording>'."\n";
    exit (1);
}

function upload($client,$fileData,$title,$conv_profile=null,$type=null)
{
        try{
                $uploadToken = new KalturaUploadToken();
                $result = $client->uploadToken->add($uploadToken);
                $tok=$result->id;
                $resume = null;
                $finalChunk = null;
                $resumeAt = null;
                $result = $client->uploadToken->upload($tok, $fileData, $resume, $finalChunk, $resumeAt);
                $entry = new KalturaBaseEntry();
                $entry->name = $title;
                $entry->tags = 'Example';
                $entry->description = 'Example Entry Description';
                if (isset($conv_profile)){
                        $entry->conversionProfileId = $conv_profile;
                }
                if (!isset($type)){
                        $type = KalturaEntryType::AUTOMATIC;
                }
                $result = $client->baseEntry->addfromuploadedfile($entry, $tok, $type);
                $id=$result->id;
                return($id);
        }catch(KalturaException $ex){
            $message=$ex->getMessage();
            $error_code=$ex->getCode();
            echo("Failed with message: $message, error code: $error_code\n");
            exit(255);
        }
}
$mandatory_args=array('partner_id','partner_secret','entry_name','service_url');
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
$entryName = $args_arr['entry_name'].'-VOD';
$service_url = $protocol.'://'.$args_arr['service_url'];
$asset_file = $argv[2];
$basedir=dirname(__FILE__);
require_once($basedir.'/create_session.php');
$client=generate_ks($service_url,$partnerId,$secret,KalturaSessionType::ADMIN,null);
$id=upload($client,$asset_file,$entryName,null,null);
