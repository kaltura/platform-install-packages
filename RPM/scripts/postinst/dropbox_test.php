<?php

if (count($argv)<3){
    echo 'Usage:' .__FILE__ .' <service_url> <partnerid> <-2 secret>'."\n";
    exit (1);
}

function enable_dropbox_permission($client,$config,$partner_id)
{

	$config->partnerId=$partner_id;
	$client->setConfig($config);
	$permission = new KalturaPermission();
	$permission->name = 'DROPFOLDER_PLUGIN_PERMISSION';
	$result = $client->permission->add($permission);
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
	
		$dropFolder->path='/tmp/dropme-kaltura3';
		mkdir($dropFolder->path);
		chown($dropFolder->path,'kaltura');
		chgrp($dropFolder->path,'apache');
		chmod($dropFolder->path,0775);
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
//$client=generate_ks($service_url,-2,$minus_2_secret,$type=KalturaSessionType::ADMIN,$userId=null);


    $config = new KalturaConfiguration(-2);
    $config->serviceUrl = $service_url;  
    $client = new KalturaClient($config);
    $ks = $client->session->start($minus_2_secret, null, KalturaSessionType::ADMIN, -2, null,null);
    $client->setKs($ks);
enable_dropbox_permission($client,$config,$partnerId);
//die();
/*$filter = new KalturaPermissionFilter();

$filter->typeEqual = KalturaPermissionType::NORMAL;
$filter->name = 'dropFolder.SYSTEM_ADMIN_DROP_FOLDER_BASE';
$pager = null;
$result = $client->permission->listAction($filter, $pager);
var_dump($result) ;exit(0);*/

$drop_obj=create_dropbox($client,$partnerId);
echo "'".$drop_obj->name.'successfully created for partner:' .$drop_obj->partnerId;
