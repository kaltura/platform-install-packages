<?php
if($argc<4){
    die('Usage: '.$argv[0] .' <partner id> <-2 admin secret> <service_url>'."\n");
}
require_once('/opt/kaltura/web/content/clientlibs/php5/KalturaClient.php');
$userId = null;
$expiry = null;
$privileges = null;
$partnerId=$argv[1];
$secret = $argv[2];
$type = KalturaSessionType::ADMIN;
$config = new KalturaConfiguration($partnerId);
$config->serviceUrl = $argv[3];
$client = new KalturaClient($config);
$config->partnerId=$partnerId;
$client->setPartnerId($partnerId);
$ks = $client->session->start($secret, $userId,KalturaSessionType::ADMIN , -2, $expiry, $privileges);
$client->setKs($ks);
$filter = null;
$pager = null;
$eventNotificationTemplate = new KalturaBusinessProcessStartNotificationTemplate();
/*$id = 35;
$eventnotificationPlugin = KalturaEventnotificationClientPlugin::get($client);
$result = $eventnotificationPlugin->eventNotificationTemplate->get($id);
 var_dump($result);
 exit();
*/
$eventNotificationTemplate->name = 'Flavor Status Equals';
$eventNotificationTemplate->systemName = 'Flavor Status Equals';
$eventNotificationTemplate->description = 'Flavor life-cycle';
$eventNotificationTemplate->type = KalturaEventNotificationTemplateType::BPM_START;
$eventNotificationTemplate->eventObjectType = 4;
$eventNotificationTemplate->manualDispatchEnabled = false;
$eventNotificationTemplate->automaticDispatchEnabled = 1;
$eventNotificationTemplate->eventType = KalturaEventNotificationEventType::OBJECT_CREATED;
$eventNotificationTemplate->eventConditions = array();
$cond=new KalturaEventFieldCondition();
$bool_field=new KalturaEvalBooleanField();
$bool_field->code='in_array(assetPeer::STATUS, $scope->getEvent()->getModifiedColumns())';
$cond->field=$bool_field;
$cond->type=null;
$cond->description='Status field modified';
$cond->not=false;
$cond1=new KalturaFieldMatchCondition();
$cond1->field=new KalturaEvalStringField();
$cond1->field->code='$scope->getEvent()->getObject()->getStatus()';
$ksv=new KalturaStringValue(array('value'=>'{trigger_status}','description'=>null));
$cond1->values=array($ksv);
$cond1->type=6;
$cond1->description="Status equals";
$cond1->not=false;
$cond2=new KalturaFieldMatchCondition();
$cond2->field=new KalturaEvalStringField();
$cond2->field->code='$scope->getEvent()->getObject()->getFlavorParamsId()';
$ksv=new KalturaStringValue(array('value'=>'{trigger_flavor_params_id}','description'=>null));
$cond2->values=array($ksv);
$cond2->type=6;
$cond2->description="Flavor-params-id equals";
$cond2->not=false;
$eventNotificationTemplate->eventConditions[0] = $cond;
$eventNotificationTemplate->eventConditions[1] = $cond1;
$eventNotificationTemplate->eventConditions[2] = $cond2;
$kenp=new KalturaEventNotificationParameter();
$kenp->key='endPoint';
$kenp->description='Server Host';
$kesf=new KalturaEvalStringField(array('code'=>"kConf::get('apphome_url')",'value'=>null,'description'=>null));
$kenp->value=$kesf;

$kenp1=new KalturaEventNotificationParameter();
$kenp1->key='partnerId';
$kenp1->description="Parnter ID";
$kesf1=new KalturaEvalStringField(array('code'=>'$scope->getEvent()->getObject()->getPartnerId()','value'=>null,'description'=>null));
$kenp1->value=$kesf1;

$kenp2=new KalturaEventNotificationParameter();
$kenp2->key='adminSecret';
$kenp2->description="Partner Administrator Secret";
$kesf2=new KalturaEvalStringField(array('code'=>'PartnerPeer::retrieveByPK($scope->getEvent()->getObject()->getPartnerId())->getAdminSecret()','value'=>null,'description'=>null));
$kenp2->value=$kesf2;

$kenp3=new KalturaEventNotificationParameter();
$kenp3->key='entryId';
$kenp3->description="Entry ID";
$kesf3=new KalturaEvalStringField(array('code'=>'$scope->getEvent()->getObject()->getEntryId()','value'=>null,'description'=>null));
$kenp3->value=$kesf3;

$kenp4=new KalturaEventNotificationParameter();
$kenp4->key='flavorId';
$kenp4->description="Flavor ID";
$kesf4=new KalturaEvalStringField(array('code'=>'$scope->getEvent()->getObject()->getId()','value'=>null,'description'=>null));
$kenp4->value=$kesf4;

$eventNotificationTemplate->contentParameters=array($kenp,$kenp1,$kenp2,$kenp3,$kenp4);

$kenp=new KalturaEventNotificationParameter();
$kenp->key='templateId';
$kenp->description='ID of the template to be passed to the process';
$ksv=new KalturaStringValue();
$ksv->value='';
$ksv->description=null;
$kenp->value=$ksv;

$kenp1=new KalturaEventNotificationParameter();
$kenp1->key='trigger_status';
$kenp1->description='Flavor-asset status that triggers the event, See:KalturaFlavorAssetStatus:/api_v3/testmeDoc/?object=KalturaFlavorAssetStatus';
$ksv1=new KalturaStringValue();
$ksv1->value=2;
$ksv1->description=null;
$kenp1->value=$ksv1;

$kenp2=new KalturaEventNotificationParameter();
$kenp2->key='trigger_flavor_params_id';
$kenp2->description='Flavor-asset params id that triggers the event';
$ksv2=new KalturaStringValue();
$ksv2->value=4;
$ksv2->description=null;
$kenp2->value=$ksv2;

$eventNotificationTemplate->userParameters=array($kenp,$kenp1,$kenp2);

$eventNotificationTemplate->serverId = 1;
$eventNotificationTemplate->processId = 'flow-transcript';
$eventNotificationTemplate->mainObjectCode = '$object->getentry()';
$eventNotificationTemplate->abortOnDeletion = false;
$eventnotificationPlugin = KalturaEventnotificationClientPlugin::get($client);
$result = $eventnotificationPlugin->eventNotificationTemplate->add($eventNotificationTemplate);

//var_dump($result);

$eventNotificationTemplate = new KalturaBusinessProcessStartNotificationTemplate();
$eventNotificationTemplate->name = 'entry_integration_job_finished';
$eventNotificationTemplate->systemName = 'entry_integration_job_finished';
$eventNotificationTemplate->description = 'entry_integration_job_finished';
$eventNotificationTemplate->type = 'businessProcessNotification.BusinessProcessSignal';
$eventNotificationTemplate->message='jobClosed';
$eventNotificationTemplate->eventId='jobClosedEvent';
$eventNotificationTemplate->eventObjectType = 1;
$eventNotificationTemplate->manualDispatchEnabled = false;
$eventNotificationTemplate->automaticDispatchEnabled = 1;
$eventNotificationTemplate->eventType = 'integrationEventNotifications.INTEGRATION_JOB_CLOSED';
$eventNotificationTemplate->eventConditions = null;
$kenp=new KalturaEventNotificationParameter();
$kenp->key='jobStatus';
$kenp->description='Job Status';
$kesf=new KalturaEvalStringField(array('code'=>'$scope->getEvent()->getBatchJob()->getStatus()','value'=>null,'description'=>null));
$kenp->value=$kesf;

$eventNotificationTemplate->contentParameters=array($kenp);
$eventNotificationTemplate->userParameters=array();

$eventNotificationTemplate->serverId = 1;
$eventNotificationTemplate->processId = 'kaltura-integrate';
$eventNotificationTemplate->mainObjectCode = NULL;
$eventNotificationTemplate->abortOnDeletion = false;
$eventnotificationPlugin = KalturaEventnotificationClientPlugin::get($client);
echo "pooooo\n";
$result = $eventnotificationPlugin->eventNotificationTemplate->add($eventNotificationTemplate);

?>
