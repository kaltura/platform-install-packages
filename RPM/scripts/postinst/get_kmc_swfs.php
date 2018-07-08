<?php
$config = null;
$clientConfig = null;
/* @var $clientConfig KalturaConfiguration */

require_once __DIR__ . '/init.php';

$kmcUrl = $clientConfig->serviceUrl . 'kmc';
stream_wrapper_restore('http');
stream_wrapper_restore('https');
$kmcHtmlContent = file_get_contents($kmcUrl);
stream_wrapper_unregister('http');
stream_wrapper_unregister('https');
if(!$kmcHtmlContent)
{
	echo "Fetching URL [$kmcUrl] failed\n";
	exit(-1);
}

$swfPaths = array(
	'/flash/kmc/login/' . $config['kmc']['login_version'] . '/login.swf',
	'/flash/kmc/' . $config['kmc']['version'] . '/kmc.swf',
);

foreach($swfPaths as $swfPath)
{
	$url = $clientConfig->serviceUrl . $swfPath;
	$ch = curl_init($url);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	curl_setopt($ch, CURLOPT_FOLLOWLOCATION, true);
	curl_setopt($ch, CURLOPT_HEADER, true);
	curl_setopt($ch, CURLOPT_NOBODY, true);
	curl_setopt($ch, CURLOPT_SSL_VERIFYPEER, false);
	curl_setopt($ch, CURLOPT_SSL_VERIFYHOST, 2);
	$content = curl_exec($ch);
	$code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
	if($code != 200)
	{
		echo "Fetching URL [$url] failed with HTTP error code [$code]\n";
		exit(-1);
	}
	
	$lines = explode("\r\n", $content);
	$headers = array();
	foreach($lines as $line)
	{
		if(!strstr($line, ':'))
			continue;
			
		list($name, $value) = explode(':', $line, 2);
		$headers[trim(strtolower($name))] = trim($value);
	}
	
	if(!isset($headers['content-length']) || !$headers['content-length']){
		echo "Fetching URL [$url] failed, no content returned\n";
		exit(-1);
	}else{
		echo "Content returned for [$url]\n";
	}
	
	if(!isset($headers['content-type']) || $headers['content-type'] != 'application/x-shockwave-flash'){
		echo "Fetching URL [$url] failed, wrong content type [" . $headers['content-type'] . "]\n";
		exit(-2);
	}else{
		echo "content type for $url is Flash SWF as expected.\n";
	}
}
exit(0);
