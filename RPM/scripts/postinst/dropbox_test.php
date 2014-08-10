<?php

if (count($argv)<3){
    echo 'Usage:' .__FILE__ .' <service_url> <partnerid> <-2 secret>'."\n";
    exit (1);
}
function create_dropbox($client,$partnerId)
{

	try{
		$dropFolder = new KalturaDropFolder();
		$dropFolder->partnerId = $partnerId;
		$dropFolder->name = 'sanity_drop';
		$dropFolder->description = 'done by kaltura-sanity.sh';
		$dropFolder->status = KalturaDropFolderStatus::ENABLED;
		$dropfolderPlugin = KalturaDropfolderClientPlugin::get($client);
		$dropFolder->type = KalturaDropFolderType::LOCAL;
		$dropFolder->dc = 0;
		$dropFolder->fileHandlerType = KalturaDropFolderFileHandlerType::CONTENT;
		$dropFolder->fileHandlerConfig = new KalturaDropFolderContentFileHandlerConfig();
		$dropFolder->fileHandlerConfig->contentMatchPolicy=KalturaDropFolderContentFileHandlerMatchPolicy::MATCH_EXISTING_OR_ADD_AS_NEW;
	
		$dropFolder->path='/tmp/dropme-kaltura';
		chown('kaltura',$dropFolder->path);
		chgrp('apache',$dropFolder->path);
		chmod(0775,$dropFolder->path);
		return $dropfolderPlugin->dropFolder->add($dropFolder);
	}catch(exception $e){
		throw $e;
	}
	 

}
$service_url = $argv[1];
$partnerId=$argv[2];
$minus_2_secret=$argv[3];
$basedir=dirname(__FILE__);
require_once($basedir.'/create_session.php');
$client=generate_ks($service_url,-2,$minus_2_secret,$type=KalturaSessionType::ADMIN,$userId=null);
var_dump(create_dropbox($client,$partnerId));
