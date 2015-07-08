<?php
if($argc<4){
    die('Usage: '.$argv[0] .' <partner id> <admin secret> <service_url>'."\n");
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
$ks = $client->session->start($secret, $userId, $type, $partnerId, $expiry, $privileges);
$client->setKs($ks);

// list available email templates:
$filter = new KalturaEmailNotificationTemplateFilter();
$filter->systemNameEqual = 'Entry_Ready';
$pager = null;
$eventNotificationTemplate = new KalturaEmailNotificationTemplate();
$eventnotificationPlugin = KalturaEventnotificationClientPlugin::get($client);
$notification_templates = $eventnotificationPlugin->eventNotificationTemplate->listTemplates($filter, $pager);
// will return all available
$template_id=$notification_templates->objects[0]->id;
// clone the template to partner:
$result = $eventnotificationPlugin->eventNotificationTemplate->cloneAction($template_id, $eventNotificationTemplate);
$notification_id = $result->id;

// activate template
$status = KalturaEventNotificationTemplateStatus::ACTIVE;
$eventnotificationPlugin = KalturaEventnotificationClientPlugin::get($client);
$result = $eventnotificationPlugin->eventNotificationTemplate->updateStatus($notification_id, $status);

// update mail subject and body:

$eventNotificationTemplate->type = KalturaEventNotificationTemplateType::EMAIL;
$eventNotificationTemplate->eventType = KalturaEventNotificationEventType::BATCH_JOB_STATUS;
$eventNotificationTemplate->eventObjectType = KalturaEventNotificationEventObjectType::ENTRY;
$eventNotificationTemplate->contentParameters = array();
$eventNotificationTemplate->contentParameters[0] = new KalturaEventNotificationParameter();
$eventNotificationTemplate->contentParameters[1] = new KalturaEventNotificationParameter();
$eventNotificationTemplate->contentParameters[2] = new KalturaEventNotificationParameter();
$eventNotificationTemplate->contentParameters[3] = new KalturaEventNotificationParameter();
$eventNotificationTemplate->subject = 'Your video is ready to be played!';
$eventNotificationTemplate->body = 'Hello world:)';
$eventnotificationPlugin = KalturaEventnotificationClientPlugin::get($client);
$result = $eventnotificationPlugin->eventNotificationTemplate->update($notification_id, $eventNotificationTemplate);
echo('ID: '. $result->id. ', Subject: "'.$result->subject.'", Mail body: "'.$result->body.'"');
?>
