<?php
if (count($argv)<2){
    echo __FILE__ . ' <admin_secret> <service_url> '."\n";
    exit (1);
}
require_once('/opt/kaltura/web/content/clientlibs/php5/KalturaClient.php');
require_once(__DIR__.'/create_session.php');
$userId = null;
$expiry = null;
$privileges = null;
// get with:
// mysql> select admin_secret from partner where id=0\G
$secret = $argv[1];
$type = KalturaSessionType::ADMIN;
$partnerId=0;
$service_url= $argv[2];
$client=generate_ks($service_url,$partnerId,$secret,$type=KalturaSessionType::ADMIN,$userId=null,$expiry = null,$privileges = null);
$flavor_name='Flavor test II';
$filter = new KalturaFlavorParamsFilter();
$filter->systemNameEqual = $flavor_name;
$filter->formatEqual = KalturaContainerFormat::MP4;
$results = $client->flavorParams->listAction($filter, null);
if(!count($results->objects)){
	$flavorParams = new KalturaFlavorParams();
	$flavorParams->name = $flavor_name ;
	$flavorParams->systemName = $flavor_name;
	$flavorParams->description = 'Flavor test II';
	$flavorParams->tags = 'mobile,web,mbr,ipad,ipadnew';
	$flavorParams->videoCodec = KalturaVideoCodec::H264M;
	$flavorParams->videoBitrate = 900;
	$flavorParams->audioCodec = KalturaAudioCodec::AAC;
	$flavorParams->audioBitrate = 64;
	$flavorParams->width = 640;
	$flavorParams->height = 0;
	$flavorParams->isSystemDefault = false;
	$flavorParams->conversionEngines = '2,99,3';
	$flavorParams->conversionEnginesExtraParams = "-flags +loop+mv4 -cmp 256 -partitions +parti4x4+partp8x8+partb8x8 -trellis 1 -refs 1 -me_range 16 -keyint_min 20 -sc_threshold 40 -i_qfactor 0.71 -bt 300k -maxrate 900k -bufsize 1200k -rc_eq 'blurCplx^(1-qComp)' -level 31 -async 2  -vsync 1 -threads 4 | -flags +loop+mv4 -cmp 256 -partitions +parti4x4+partp8x8+partb8x8 -trellis 1 -refs 1 -me_range 16 -keyint_min 20 -sc_threshold 40 -i_qfactor 0.71 -bt 300k -maxrate 900k -bufsize 1200k -rc_eq 'blurCplx^(1-qComp)' -level 31 -async 2 -vsync 1 | -x264encopts qcomp=0.6:qpmin=10:qpmax=50:qpstep=4:frameref=1:bframes=0:threads=auto:level_idc=31:global_header:partitions=i4x4+p8x8+b8x8:trellis=1:me_range=16:keyint_min=20:scenecut=40:ipratio=0.71:ratetol=40:vbv-maxrate=900:vbv-bufsize=1200";

	$flavorParams->twoPass = 'true';
	$flavorParams->format = KalturaContainerFormat::MP4;

	$results = $client->flavorParams->add($flavorParams);
	$low_id=$results->id;
}else{	
	$low_id=$results->objects[0]->id;
	echo ("$flavor_name with ID $low_id already exists. Skipping.");
	exit (1);
}
echo("$low_id");

?>


