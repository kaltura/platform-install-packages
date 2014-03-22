<?php
if (count($argv)<5){
    echo 'Usage:' .__FILE__ .' <service_url> <partnerid> <secret> </path/to/asset>'."\n";
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
		if (isset($conv_profile)){
			$entry->conversionProfileId = $conv_profile;	
		}
		if (!isset($type)){
			$type = KalturaEntryType::AUTOMATIC;
		}
		$result = $client->baseEntry->addfromuploadedfile($entry, $tok, $type);
		$id=$result->id;
		$xme1=$client->getResponseHeaders();
		$xme2=split(": ",$xme1[3]);
		$xme=trim($xme2[1]);
		echo $xme . " " .$title .' ';
		return($id);
	}catch(exception $e){
		$xme1=$client->getResponseHeaders();
		$xme2=split(": ",$xme1[3]);
		$xme=trim($xme2[1]);
		echo $xme . " " .$title .' ';
		throw $e;
	}
}
//$rc_file='functions.rc';
$entry_queue='/tmp/upload_test_queue';
$service_url = $argv[1];
$partnerId=$argv[2];
$secret=$argv[3];
/*exec(". $rc_file ;echo \$MON_PARTNER",$partnerId,$rc);
// sha1 secret
exec(". $rc_file ;echo \$MON_PARTNER_SECRET",$secret,$rc);
if (empty($partnerId) || empty($secret)){
    die("No partner ID and pass, check $rc_file\n");
}*/
$asset_file = $argv[4];
$basedir=dirname(__FILE__);
require_once($basedir.'/create_session.php');
$client=generate_ks($service_url,$partnerId,$secret,$type=KalturaSessionType::USER,$userId=null);
$ext=split("\.",$asset_file);
$id=upload($client,$asset_file,date ("U",time()).'.'.$ext[1],null,null);
error_log($id."\n",3,$entry_queue);
echo $id."\n";
