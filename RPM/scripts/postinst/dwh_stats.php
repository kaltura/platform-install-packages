<?php
if($argc<6){
    die('Usage: '.$argv[0] .' <partner id> <admin secret> <service_url> <start date i.e "01 Jul 2015"> <end date i.e "10 Jul 2015">'."\n");
}
require_once('/opt/kaltura/web/content/clientlibs/php5/KalturaClient.php');

// generate a KS
$userId = null;
$expiry = null;
$privileges = null;
$partnerId=$argv[1];
$secret = $argv[2];
$type = KalturaSessionType::ADMIN;
$config = new KalturaConfiguration($partnerId);
$config->serviceUrl = $argv[3];
$start_date=date_format(date_create($argv[4]), 'U');
$end_date=date_format(date_create($argv[5]), 'U');
$client = new KalturaClient($config);
$ks = $client->session->start($secret, $userId, $type, $partnerId, $expiry, $privileges);
$client->setKs($ks);

// set type to TOP_CONTENT
// reportType can be any of there:
// https://github.com/kaltura/server/blob/master/api_v3/lib/types/enums/KalturaReportType.php
$report_type_string='TOP_CONTENT';
$reportType = constant('KalturaReportType::'.$report_type_string);
$reportInputFilter = new KalturaReportInputFilter();
// epoch representation of the start and end dates
$reportInputFilter->fromDate = $start_date;
$reportInputFilter->toDate = $end_date;
// interval can also be KalturaReportInterval::MONTHS;
$reportInputFilter->interval = KalturaReportInterval::DAYS;
$dimension = null;
// objectIds: comma separated string of entry ids
$objectIds = null;
echo "Getting $report_type_string total info for ".$argv[4]." - ". $argv[5]."...\n\n";
$result = $client->report->gettotal($reportType, $reportInputFilter, $objectIds);
var_dump($result);

echo "Getting $report_type_string graph info for ".$argv[4]." - ". $argv[5]."...\n\n";
$result = $client->report->getgraphs($reportType, $reportInputFilter, $dimension, $objectIds);
var_dump($result);


// set type to OPERATION_SYSTEM
$report_type_string='OPERATION_SYSTEM';
$reportType = constant('KalturaReportType::'.$report_type_string);
$reportInputFilter = new KalturaReportInputFilter();
$reportInputFilter->fromDate = $start_date;
$reportInputFilter->toDate = $end_date;
$reportInputFilter->interval = KalturaReportInterval::DAYS;
$dimension = null;
$objectIds = null;
echo "Getting $report_type_string total info for ".$argv[4]." - ". $argv[5]."...\n\n";
$result = $client->report->gettotal($reportType, $reportInputFilter, $objectIds);
var_dump($result);

echo "Getting $report_type_string graph info for ".$argv[4]." - ". $argv[5]."...\n\n";
$result = $client->report->getgraphs($reportType, $reportInputFilter, $dimension, $objectIds);
var_dump($result);
?>
