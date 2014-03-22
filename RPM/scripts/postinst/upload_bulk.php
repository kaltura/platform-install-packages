<?php
require_once(dirname(__FILE__).'/create_session.php');
if (count($argv)<4){
    echo 'Usage:' .__FILE__ .' <service_url> <partner id> <secret> <uploader> </path/to/csv>'."\n";
    exit (1);
}
// relevant account user
$partnerId = $argv[2];
$config = new KalturaConfiguration($partnerId);
// URL of the API machine
$config->serviceUrl = $argv[1];
// sha1 secret
$secret = $argv[3];
$uploadedBy = $argv[4];
$userId = null;
$expiry = null;
$privileges = null;
//csv file to use
$csvFileData = $argv[5];
// type here is CSV but can also work with XML
$bulkUploadType = 'bulkUploadCsv.CSV';
$client=generate_ks($config->serviceUrl,$partnerId,$secret,$type=KalturaSessionType::ADMIN,$userId=null,$expiry = null,$privileges = null);
// conversion profile to be used
//if you want a specific one:
//$filter = new KalturaConversionProfileFilter();
//$filter->nameEqual = 'Name';                                                                                                                                        
//$pager = null;                                                                                                                                                      
//$result = $client->conversionProfile->listAction($filter, $pager);                                                                                                  
//                                                                                                                                                                    
//or just default:                                                                                                                                                    
$conversionProfileId = $client->conversionProfile->getDefault()->id;                                                                                                  
$results = $client-> bulkUpload ->add($conversionProfileId, $csvFileData, $bulkUploadType, $uploadedBy);                                                              
if (isset($results)){
	echo "Successfully uploaded";                                                                                                                               }else{
	echo "Failed to upload :(";
}                  
?>         
