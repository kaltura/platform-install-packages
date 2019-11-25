<?php
/**
 * @package plugins.crossKalturaDistribution
 * @subpackage lib.batch
 */
class Categorymemberscollaboration_Model_Entity_CollaborationSettings implements Serializable
{

    const CO_PUBLISH = 1;
    const CO_EDIT = 2;
    const ALL = 3;
    const CO_VIEW = 4;
    /** @var array */
    public $roles;

    /** @var array */
    public $permissions;
    public function serialize()
    {    
        return serialize([
            'roles'       => $this->roles,
            'permissions' => $this->permissions,
        ]);  
    }    

    public function unserialize($serialized)
    {    
        $data = unserialize($serialized);

        $this->roles       = $data['roles'];
        $this->permissions = $data['permissions'];
    }    

}

class CrossKalturaDistributionEngine extends DistributionEngine implements
	IDistributionEngineSubmit,
	IDistributionEngineUpdate,
	IDistributionEngineDelete,
	IKalturaLogger
{

	const DISTRIBUTED_INFO_SOURCE_ID = 'sourceId';
	const DISTRIBUTED_INFO_TARGET_ID = 'targetId';
	const DISTRIBUTED_INFO_SOURCE_VERSION = 'sourceVersion';
	const DISTRIBUTED_INFO_SOURCE_UPDATED_AT = 'sourceUpdatedAt';
	const COLLABORATION_CUSTOM_METADATA_SETTINGS_KEY = 'categorymemberscollaboration_settings';


	/**
	 * @var KalturaClient
	 */
	protected $targetClient = null;

	/**
	 * @var KalturaClient
	 */
	protected $sourceClient = null;

	/**
	 * @var KalturaCrossKalturaDistributionProfile
	 */
	protected $distributionProfile = null;

	/**
	 * Should distribute caption assets ?
	 * @var bool
	 */
	protected $distributeCaptions = false;

	/**
	 * Should distribute to designated categories only ?
	 * @var bool
	 */
	protected $distributeCategories = false;
	
	/**
	 * Should we set entitledUsersPublish and entitledUsersEdit on the target entry based on the collaboratorsCustomMetadataProfileId settings?
	 * @var bool
	 */
	protected $collaboratorsFromCustomMetadataProfile = false;


	/**
	 * Should distribute cue points ?
	 * @var bool
	 */
	protected $distributeCuePoints = false;


	/**
	 * Will hold the target entry ID once created
	 * @var string
	 */
	protected $targetEntryId;

	protected $fieldValues = array();


	protected $mapAccessControlIds = array();
	protected $mapConversionProfileIds = array();
	protected $mapMetadataProfileIds = array();
	protected $mapStorageProfileIds = array();
	protected $mapFlavorParamsIds = array();
	protected $mapThumbParamsIds = array();
	protected $mapCaptionParamsIds = array();
	protected $mapAttachmentParamsIds = array();

	/**
	 * @var CrossKalturaEntryObjectsContainer
	 */
	protected $sourceObjects = null;

	// ------------------------------
	//  initialization methods
	// ------------------------------


	public function __construct()
	{
		$this->targetClient = null;
		$this->distributeCaptions = false;
		$this->distributeCategories = false;
		$this->collaboratorsFromCustomMetadataProfile = false;
		$this->distributeCuePoints = false;
		$this->mapAccessControlIds = array();
		$this->mapConversionProfileIds = array();
		$this->mapMetadataProfileIds = array();
		$this->mapStorageProfileIds = array();
		$this->mapFlavorParamsIds = array();
		$this->mapThumbParamsIds = array();
		$this->mapCaptionParamsIds = array();
		$this->mapAttachmentParamsIds = array();
		$this->fieldValues = array();
		$this->sourceObjects = null;
	}

	/**
	 * Initialize
	 * @param KalturaDistributionJobData $data
	 * @throws Exception
	 */
	protected function init(KalturaDistributionJobData $data)
	{
		// validate objects
		if(!$data->distributionProfile instanceof KalturaCrossKalturaDistributionProfile)
			throw new Exception('Distribution profile must be of type KalturaCrossKalturaDistributionProfile');

		if (!$data->providerData instanceof KalturaCrossKalturaDistributionJobProviderData)
			throw new Exception('Provider data must be of type KalturaCrossKalturaDistributionJobProviderData');

		$this->distributionProfile = $data->distributionProfile;

		// init target kaltura client
		$this->initClients($this->distributionProfile);

		// check for plugins availability
		$this->initPlugins($this->distributionProfile);

		// init mapping arrays
		$this->initMapArrays($this->distributionProfile);

		// init field values
		$this->fieldValues = unserialize($data->providerData->fieldValues);
		if (!$this->fieldValues) {
			$this->fieldValues = array();
		}
	}

	/**
	 * Init a KalturaClient object for the target account
	 * @param KalturaCrossKalturaDistributionProfile $distributionProfile
	 * @throws Exception
	 */
	protected function initClients(KalturaCrossKalturaDistributionProfile $distributionProfile)
	{
		// init source client
		$sourceClientConfig = new KalturaConfiguration($distributionProfile->partnerId);
		$sourceClientConfig->serviceUrl = KBatchBase::$kClient->getConfig()->serviceUrl; // copy from static batch client
		$sourceClientConfig->setLogger($this);
		$this->sourceClient = new KalturaClient($sourceClientConfig);
		$this->sourceClient->setKs(KBatchBase::$kClient->getKs()); // copy from static batch client

		// init target client
		$targetClientConfig = new KalturaConfiguration($distributionProfile->targetAccountId);
		$targetClientConfig->serviceUrl = $distributionProfile->targetServiceUrl;
		$targetClientConfig->setLogger($this);
		$this->targetClient = new KalturaClient($targetClientConfig);
		$ks = $this->targetClient->user->loginByLoginId($distributionProfile->targetLoginId, $distributionProfile->targetLoginPassword, $distributionProfile->targetAccountId, 86400, 'disableentitlement');
		$this->targetClient->setKs($ks);
	}

	/**
	 * Check which server plugins should be used
	 * @param KalturaCrossKalturaDistributionProfile $distributionProfile
	 * @throws Exception
	 */
	protected function initPlugins(KalturaCrossKalturaDistributionProfile $distributionProfile)
	{
		// check if should distribute caption assets
		$this->distributeCaptions = false;
		if ($distributionProfile->distributeCaptions == true)
		{
			if (class_exists('CaptionPlugin') && class_exists('KalturaCaptionClientPlugin') && KalturaPluginManager::getPluginInstance(CaptionPlugin::getPluginName()))
			{
				$this->distributeCaptions = true;
			}
			else
			{
				throw new Exception('Missing CaptionPlugin');
			}
		}

		if ($distributionProfile->distributeCategories == true)
		{
			$this->distributeCategories = true;
			$this->designatedCategories = $distributionProfile->designatedCategories;
		}
		if ($distributionProfile->collaboratorsFromCustomMetadataProfile == true)
		{
			$this->collaboratorsFromCustomMetadataProfile = true;
			$this->collaboratorsCustomMetadataProfileId = $distributionProfile->collaboratorsCustomMetadataProfileId;
		}
		// check if should distribute cue points
		$this->distributeCuePoints = false;
		if ($distributionProfile->distributeCuePoints == true)
		{
			if (class_exists('CuePointPlugin') && class_exists('KalturaCuePointClientPlugin') && KalturaPluginManager::getPluginInstance(CuePointPlugin::getPluginName()))
			{
				$this->distributeCuePoints = true;
			}
			else
			{
				throw new Exception('Missing CuePointPlugin');
			}
		}
	}


	protected function initMapArrays(KalturaCrossKalturaDistributionProfile $distributionProfile)
	{
		$this->mapAccessControlIds = $this->toKeyValueArray($distributionProfile->mapAccessControlProfileIds);
		$this->mapConversionProfileIds = $this->toKeyValueArray($distributionProfile->mapConversionProfileIds);
		$this->mapMetadataProfileIds = $this->toKeyValueArray($distributionProfile->mapMetadataProfileIds);
		$this->mapStorageProfileIds = $this->toKeyValueArray($distributionProfile->mapStorageProfileIds);
		$this->mapFlavorParamsIds = $this->toKeyValueArray($distributionProfile->mapFlavorParamsIds);
		$this->mapThumbParamsIds = $this->toKeyValueArray($distributionProfile->mapThumbParamsIds);
		$this->mapCaptionParamsIds = $this->toKeyValueArray($distributionProfile->mapCaptionParamsIds);
		$this->mapAttachmentParamsIds = $this->toKeyValueArray($distributionProfile->mapAttachmentParamsIds);
	}


	// ------------------------------
	//  get existing objects via api
	// ------------------------------



	/**
	 * @param KalturaDistributionJobData $data
	 * @return CrossKalturaEntryObjectsContainer
	 */
	protected function getSourceObjects(KalturaDistributionJobData $data)
	{
		$sourceEntryId = $data->entryDistribution->entryId;
		KBatchBase::impersonate($this->distributionProfile->partnerId);
		$sourceObjects = $this->getEntryObjects(KBatchBase::$kClient, $sourceEntryId, $data);
		KBatchBase::unimpersonate();
		return $sourceObjects;
	}

	/**
	 * Get entry objects for distribution
	 * @param KalturaClient $client
	 * @param string $entryId
	 * @param KalturaDistributionJobData $data
	 * @return CrossKalturaEntryObjectsContainer
	 */
	protected function getEntryObjects(KalturaClient $client, $entryId, KalturaDistributionJobData $data)
	{
		$remoteFlavorAssetContent = $data->distributionProfile->distributeRemoteFlavorAssetContent;
		$remoteThumbAssetContent = $data->distributionProfile->distributeRemoteThumbAssetContent;
		$remoteCaptionAssetContent = $data->distributionProfile->distributeRemoteCaptionAssetContent;
		$remoteAttachmentAssetContent = false;

		// get entry
		$entry = $client->baseEntry->get($entryId);

		// get entry's flavor assets chosen for distribution
		$flavorAssets = array();
		if (!empty($data->entryDistribution->flavorAssetIds))
		{
			$flavorAssetFilter = new KalturaFlavorAssetFilter();
			// only export the source flavour, let KDL do the rest
			$flavorAssetFilter->flavorParamsIdEqual = "0";
			$flavorAssetFilter->idIn = $data->entryDistribution->flavorAssetIds;
			$flavorAssetFilter->entryIdEqual = $entryId;
			try {
				$flavorAssetsList = $client->flavorAsset->listAction($flavorAssetFilter);
				foreach ($flavorAssetsList->objects as $asset)
				{
					$twoLetterCode = languageCodeManager::getLanguageKey($asset->language);
					$obj = languageCodeManager::getObjectFromTwoCode($twoLetterCode);
					$asset->language = !is_null($obj) ? $obj[languageCodeManager::KALTURA_NAME] : null;

					$flavorAssets[$asset->id] = $asset;
				}
				
			}
			catch (Exception $e) {
				KalturaLog::err('Cannot get list of flavor assets - '.$e->getMessage());
				throw $e;
			}
		}
		else
		{
			KalturaLog::log('No flavor assets set for distribution!');
		}

		// get flavor assets content
		$flavorAssetsContent = array();
		foreach ($flavorAssets as $flavorAsset)
		{
			$flavorAssetsContent[$flavorAsset->id] = $this->getAssetContentResource($flavorAsset->id, $client->flavorAsset, $remoteFlavorAssetContent);
		}


		// get entry's thumbnail assets chosen for distribution
		$thumbAssets = array();
		$timedThumbAssets = array();
			$thumbAssetFilter = new KalturaThumbAssetFilter();
			$thumbAssetFilter->idIn = $data->entryDistribution->thumbAssetIds;
			//KalturaLog::info("Zoe and James thumbassets " .print_r($data->entryDistribution->thumbAssetIds,true));	
			$thumbAssetFilter->entryIdEqual = $entryId;
			try {
				$thumbAssetsList = $client->thumbAsset->listAction($thumbAssetFilter);
				foreach ($thumbAssetsList->objects as $asset)
				{
					if (isset($asset->cuePointId)){
						$timedThumbAssets[$asset->id] = $asset;
					}else{
						$thumbAssets[$asset->id] = $asset;
					}
				}
			}
			catch (Exception $e) {
				KalturaLog::err('Cannot get list of thumbnail assets - '.$e->getMessage());
				throw $e;
			}

		// get thumb assets content
		$thumbAssetsContent = array();
		foreach ($thumbAssets as $thumbAsset)
		{
			$thumbAssetsContent[$thumbAsset->id] = $this->getAssetContentResource($thumbAsset->id, $client->thumbAsset, $remoteThumbAssetContent);
		}
		foreach ($timedThumbAssets as $thumbAsset)
		{
			$thumbAssetsContent[$thumbAsset->id] = $this->getAssetContentResource($thumbAsset->id, $client->thumbAsset, $remoteThumbAssetContent);
		}

		// get entry's custom metadata objects
		$metadataObjects = array();
		$metadataFilter = new KalturaMetadataFilter();
		$metadataFilter->metadataObjectTypeEqual = KalturaMetadataObjectType::ENTRY;
		$metadataFilter->objectIdEqual = $entryId;
		try {
			$metadataClient = KalturaMetadataClientPlugin::get($client);
			$metadataObjectsList = $metadataClient->metadata->listAction($metadataFilter);
			foreach ($metadataObjectsList->objects as $metadata)
			{
				$metadataObjects[$metadata->id] = $metadata;
			}
		}
		catch (Exception $e) {
			KalturaLog::err('Cannot get list of metadata objects - '.$e->getMessage());
			throw $e;
		}
		// right now, there can only be one quiz per entry, the array and the looping over the list() results is done to be consistent with the rest of the code.. also, who knows what they'll add tomorrow
		$quizObjects = array();
		$quizClient = KalturaQuizClientPlugin::get($client);
		$quizFilter = new KalturaQuizFilter();
		$quizFilter->entryIdEqual = $entryId;
		$pager = new KalturaFilterPager();
		try {
		    $quizObjectsList = $quizClient->quiz->listAction($quizFilter, $pager);
			foreach ($quizObjectsList->objects as $quiz)
			{
				$quizObjects[] = $quiz;
			}
		} catch (Exception $e) {
		   KalturaLog::err('Failed to list quiz objects on source entry - ' . $entryId .': ' .$e->getMessage());
		}

		// get entry's caption assets
		$captionAssetClient = KalturaCaptionClientPlugin::get($client);
		$captionAssets = array();
		if ($this->distributeCaptions == true)
		{
			$captionAssetFilter = new KalturaCaptionAssetFilter();
			$captionAssetFilter->entryIdEqual = $entryId;
			try {
				$captionAssetsList = $captionAssetClient->captionAsset->listAction($captionAssetFilter);
				foreach ($captionAssetsList->objects as $asset)
				{
					$captionAssets[$asset->id] = $asset;
				}
			}
			catch (Exception $e) {
				KalturaLog::err('Cannot get list of caption assets - '.$e->getMessage());
				throw $e;
			}
		}


		// get caption assets content
		$captionAssetsContent = array();
		foreach ($captionAssets as $captionAsset)
		{
			$captionAssetsContent[$captionAsset->id] = $this->getAssetContentResource($captionAsset->id, $captionAssetClient->captionAsset, $remoteCaptionAssetContent);
		}

		$attachmentAssetClient = KalturaAttachmentClientPlugin::get($client);
	  	$attachmentFilter = new KalturaAttachmentAssetFilter();
  		$attachmentFilter->entryIdEqual = $entryId;
		$attachmentFilter->statusEqual = KalturaAttachmentAssetStatus::READY;
		try {
			$attachmentAssetsList = $attachmentAssetClient->attachmentAsset->listAction($attachmentFilter);
			foreach ($attachmentAssetsList->objects as $asset)
			{
				$attachmentAssets[$asset->id] = $asset;
			}
		}
		catch (Exception $e) {
			KalturaLog::err('Cannot get list of attachment assets - '.$e->getMessage());
			throw $e;
		}

		// get attachment assets content
		$attachmentAssetsContent = array();
		foreach ($attachmentAssets as $attachmentAsset)
		{
			$attachmentAssetsContent[$attachmentAsset->id] = $this->getAssetContentResource($attachmentAsset->id, $attachmentAssetClient->attachmentAsset, $remoteAttachmentAssetContent);
		}

		// get entry's cue points
		$cuePoints = array();
		$thumbCuePoints = array();
		if ($this->distributeCuePoints == true)
		{
			$cuePointFilter = new KalturaCuePointFilter();
			$cuePointFilter->entryIdEqual = $entryId;
			try {
				$cuePointClient = KalturaCuePointClientPlugin::get($client);
				$cuePointsList = $cuePointClient->cuePoint->listAction($cuePointFilter);
				foreach ($cuePointsList->objects as $cuePoint)
				{
					/**
					 * @var $cuePoint KalturaCuePoint
					 */
					if ($cuePoint->cuePointType != KalturaCuePointType::THUMB){
						if ($cuePoint->cuePointType == KalturaCuePointType::ANNOTATION && $cuePoint->tags =='KMS_public_comment'){
							continue;
						}
						$cuePoints[$cuePoint->id] = $cuePoint;
					}else{
						if ($cuePoint->subType == ThumbCuePointSubType::CHAPTER){
							$cuePoint->subType = ThumbCuePointSubType::SLIDE;
						}
						$thumbCuePoints[$cuePoint->id] = $cuePoint;
					}
				}
			}
			catch (Exception $e) {
				KalturaLog::err('Cannot get list of cue points - '.$e->getMessage());
				throw $e;
			}
		}

		$entryObjects = new CrossKalturaEntryObjectsContainer();
		$entryObjects->entry = $entry;
		$entryObjects->metadataObjects = $metadataObjects;
		$entryObjects->quizObjects = $quizObjects;
		$entryObjects->flavorAssets = $flavorAssets;
		$entryObjects->flavorAssetsContent = $flavorAssetsContent;
		$entryObjects->thumbAssets = $thumbAssets;
		$entryObjects->timedThumbAssets = $timedThumbAssets;
		$entryObjects->thumbAssetsContent = $thumbAssetsContent;
		$entryObjects->captionAssets = $captionAssets;
		$entryObjects->captionAssetsContent = $captionAssetsContent;
		$entryObjects->attachmentAssets = $attachmentAssets;
		$entryObjects->attachmentAssetsContent = $attachmentAssetsContent;
		$entryObjects->cuePoints = $cuePoints;
		$entryObjects->thumbCuePoints = $thumbCuePoints;

		return $entryObjects;
	}


	/**
	 * @return KalturaContentResource content resource for the given asset in the target account
	 * @param string $assetId
	 * @param KalturaServiceBase $assetService
	 * @param bool $remote
	 */
	protected function getAssetContentResource($assetId, KalturaServiceBase $assetService, $remote)
	{
		$contentResource = null;

		if ($remote)
		{
			// get remote resource

			$contentResource = new KalturaRemoteStorageResources();
			$contentResource->resources = array();

			$remotePaths = $assetService->getRemotePaths($assetId);
			$remotePaths = $remotePaths->objects;
			foreach ($remotePaths as $remotePath)
			{
				/* @var $remotePath KalturaRemotePath */
				$res = new KalturaRemoteStorageResource();
				if (!isset($this->mapStorageProfileIds[$remotePath->storageProfileId]))
				{
					throw new Exception('Cannot map storage profile ID ['.$remotePath->storageProfileId.']');
				}
				$res->storageProfileId = $this->mapStorageProfileIds[$remotePath->storageProfileId];
				$res->url = $remotePath->uri;

				$contentResource->resources[] = $res;
			}
		}
		else
		{
			// get local resource
			$contentResource = new KalturaUrlResource();
			$contentResource->url = $this->getAssetUrlByAssetId($assetId, $assetService);
		}
		return $contentResource;
	}

	protected function getCollaborators($metadataProfile, $categoryId)
	{
		  KalturaLog::info("Got $metadataProfile, $categoryId");
		  
		  $metadataPlugin = KalturaMetadataClientPlugin::get($this->targetClient);
		  $filter = new KalturaMetadataFilter();
		  $filter->metadataObjectTypeEqual = KalturaMetadataObjectType::CATEGORY;
		  $filter->metadataProfileIdEqual = $metadataProfile;
		  $filter->objectIdIn = $categoryId;
		  $pager = new KalturaFilterPager();
		  try {
		    	$metadata = $metadataPlugin->metadata->listAction($filter, $pager);
			$metadataObject = $metadata->objects[0];

			$xmlObj = new SimpleXMLElement($metadataObject->xml);
			$xmlKeys = $xmlObj->xpath('Detail');

			foreach ($xmlKeys as $obj)
			{
				$details[(string)$obj->Key] = (string)$obj->Value;
			}
			if (is_array($details) && array_key_exists(self::COLLABORATION_CUSTOM_METADATA_SETTINGS_KEY, $details)){
				$collaborationNode = ($details[self::COLLABORATION_CUSTOM_METADATA_SETTINGS_KEY]);
				$collaborationConfig = unserialize($collaborationNode);
				return $collaborationConfig;
			}

			return false;
		  } catch (Exception $e) {
		    KalturaLog::warning("Couldn't get collaboration info: " . $e->getMessage());
		  }

	}	

	protected function getAssetUrlByAssetId($assetId, $assetService)
	{
		if ( $assetService instanceof KalturaFlavorAssetService ) {
			$options = new KalturaFlavorAssetUrlOptions();
			$options->fileName = $assetId;
			return $assetService->getUrl($assetId, null, false, $options);
		}
		
		return $assetService->getUrl($assetId);
	}

	// -----------------------------------------------
	//  methods to transform source to target objects
	// -----------------------------------------------

	/**
	 * Transform source entry object to a target object ready for insert/update
	 * @param KalturaBaseEntry $sourceEntry
	 * @param bool $forUpdate
	 * @return KalturaBaseEntry
	 */
	protected function transformEntry(KalturaBaseEntry $sourceEntry, $forUpdate = false)
	{
		// remove readonly/insertonly parameters
		/* @var $targetEntry KalturaBaseEntry */
		$targetEntry = $this->copyObjectForInsertUpdate($sourceEntry);

		// switch to target account's object ids
		if ($forUpdate)
		{
			$targetEntry = $this->removeInsertOnly($targetEntry);
			$targetEntry->conversionProfileId = null;
		}
		else
		{
			if (!is_null($sourceEntry->conversionProfileId))
			{
				if (!isset($this->mapConversionProfileIds[$sourceEntry->conversionProfileId]))
				{
					throw new Exception('Cannot map conversion profile ID ['.$sourceEntry->conversionProfileId.']');
				}
				$targetEntry->conversionProfileId = $this->mapConversionProfileIds[$sourceEntry->conversionProfileId];
			}
		}

		if (!is_null($sourceEntry->accessControlId))
		{
			if (!isset($this->mapAccessControlIds[$sourceEntry->accessControlId]))
			{
				throw new Exception('Cannot map access control ID ['.$sourceEntry->accessControlId.']');
			}
			$targetEntry->accessControlId = $this->mapAccessControlIds[$sourceEntry->accessControlId];
		}

		// transform metadata according to fields configuration
		$targetEntry->name = $this->getValueForField(KalturaCrossKalturaDistributionField::BASE_ENTRY_NAME);
		$targetEntry->description = $this->getValueForField(KalturaCrossKalturaDistributionField::BASE_ENTRY_DESCRIPTION);
		$targetEntry->userId = $this->getValueForField(KalturaCrossKalturaDistributionField::BASE_ENTRY_USER_ID);
		$targetEntry->tags = $this->getValueForField(KalturaCrossKalturaDistributionField::BASE_ENTRY_TAGS);
		//KalturaLog::info("Zoe and James dist to categories: " . print_r($this->distributeCategories,true) . "\n");
		if ($this->distributeCategories){
			$targetEntry->categories = $this->designatedCategories;
			//KalturaLog::info("Zoe and James dist to des categories: " . print_r($this->designatedCategories,true) . "\n");
		}else{
			$targetEntry->categories = $this->getValueForField(KalturaCrossKalturaDistributionField::BASE_ENTRY_CATEGORIES);

			//KalturaLog::info("Zoe and James: " . $targetEntry->categories . "\n");
		}
		$targetEntry->categoriesIds = null;
		if ($sourceEntry->sourceType == 37 || $sourceEntry->sourceType == 36 || $sourceEntry->sourceType == 35){
                        $targetEntry->sourceType = 1;
                }  
		//KalturaLog::info("Zoe and James: " . $targetEntry->categoriesIds . "\n");
		$targetEntry->partnerData = $this->getValueForField(KalturaCrossKalturaDistributionField::BASE_ENTRY_PARTNER_DATA);
		$targetEntry->startDate = $this->getValueForField(KalturaCrossKalturaDistributionField::BASE_ENTRY_START_DATE);
		$targetEntry->endDate = $this->getValueForField(KalturaCrossKalturaDistributionField::BASE_ENTRY_END_DATE);
		$targetEntry->referenceId = $this->getValueForField(KalturaCrossKalturaDistributionField::BASE_ENTRY_REFERENCE_ID);
		$targetEntry->licenseType = $this->getValueForField(KalturaCrossKalturaDistributionField::BASE_ENTRY_LICENSE_TYPE);
		$catFilter = new KalturaCategoryFilter();
		$catFilter->fullNameIn = $targetEntry->categories;
		$targetCategories = $this->targetClient->category->listAction($catFilter,null);
		//KalturaLog::info("Zoe and James target categories " . print_r($targetCategories,true));
		if ($this->collaboratorsFromCustomMetadataProfile && is_numeric($this->collaboratorsCustomMetadataProfileId)){
			foreach ($targetCategories->objects as $targetCategory){
				$collaborators = $this->getCollaborators($this->collaboratorsCustomMetadataProfileId, $targetCategory->id);
				// $collaborators should be an object of type Categorymemberscollaboration_Model_Entity_CollaborationSettings, if it isn't, let's stop
				if(!$collaborators instanceof Categorymemberscollaboration_Model_Entity_CollaborationSettings){
					break;
				}
				//KalturaLog::info("Zoe and James collaborators " . print_r($collaborators,true));
				$filter = new KalturaCategoryUserFilter();
				$filter->categoryIdEqual = $targetCategory->id ;
				$catUsers = $this->targetClient->categoryUser->listAction($filter, null);
				//KalturaLog::info("Zoe and James cu " . print_r($catUsers,true));
				foreach ($catUsers->objects as $catUser){
					if (in_array($catUser->permissionLevel,$collaborators->roles)){
						if (in_array(Categorymemberscollaboration_Model_Entity_CollaborationSettings::CO_PUBLISH,$collaborators->permissions)){
							if (isset($entitledUsersPublishers)){
								$entitledUsersPublishers = $entitledUsersPublishers . ',' . $catUser->userId ;
							}else{
								$entitledUsersPublishers = $catUser->userId;
							}
						}
						if (in_array(Categorymemberscollaboration_Model_Entity_CollaborationSettings::CO_EDIT,$collaborators->permissions)){
							if (isset($entitledUsersEditors)){
								$entitledUsersEditors = $entitledUsersEditors . ',' . $catUser->userId;
							}else{
								$entitledUsersEditors = $catUser->userId . ',';
							}
						}
					}
				}
				if (isset($entitledUsersPublishers)){
					$targetEntry->entitledUsersPublish = $entitledUsersPublishers;
				}
				if (isset($entitledUsersEditors)){
					$targetEntry->entitledUsersEdit = $entitledUsersEditors;
				}
			}
		}
		if (isset($targetEntry->conversionQuality)) {
			$targetEntry->conversionQuality = null;
		}

		// turn problematic empty fields to null
		if (!$targetEntry->startDate) { $targetEntry->startDate = null; }
		if (!$targetEntry->endDate) { $targetEntry->endDate = null; }
		if (!$targetEntry->referenceId) { $targetEntry->referenceId = null; }
		// return transformed entry object
		return $targetEntry;
	}


	/**
	 * Transform source metadata objects to target objects ready for insert/update
	 * @param array<KalturaMetadata> $sourceMetadatas
	 * @return array<KalturaMetadata>
	 */
	protected function transformMetadatas(array $sourceMetadatas)
	{
		if (!count($sourceMetadatas)) {
			return array();
		}

		$targetMetadatas = array();
		foreach ($sourceMetadatas as $sourceMetadata)
		{
			/* @var $sourceMetadata KalturaMetadata */

			if (!isset($this->mapMetadataProfileIds[$sourceMetadata->metadataProfileId]))
			{
				//throw new Exception('Cannot map metadata profile ID ['.$sourceMetadata->metadataProfileId.']');
				KalturaLog::info('Cannot map metadata profile ID ['.$sourceMetadata->metadataProfileId.'].. skipping');
				continue;
			}
			if($this->mapMetadataProfileIds[$sourceMetadata->metadataProfileId] == 0)
			{
				continue;
			}

			$targetMetadata = new KalturaMetadata();
			$targetMetadata->metadataProfileId = $this->mapMetadataProfileIds[$sourceMetadata->metadataProfileId];

			$xsltStr = $this->distributionProfile->metadataXslt;
			if (!is_null($xsltStr) && strlen($xsltStr) > 0)
			{
				$targetMetadata->xml = $this->transformXml($sourceMetadata->xml, $xsltStr);
			}
			else
			{
				$targetMetadata->xml = $sourceMetadata->xml;
			}

			$targetMetadatas[$sourceMetadata->id] = $targetMetadata;
		}

		return $targetMetadatas;
	}


	/**
	 * Transform source flavor assets to target objects ready for insert/update
	 * @param array<KalturaFlavorAsset> $sourceFlavorAssets
	 * @return array<KalturaFlavorAsset>
	 */
	protected function transformFlavorAssets(array $sourceFlavorAssets)
	{
		return $this->transformAssets($sourceFlavorAssets, $this->mapFlavorParamsIds, 'flavorParamsId');
	}

	/**
	 * Transform source thumbnail assets to target objects ready for insert/update
	 * @param array<KalturaThumbAsset> $sourceThumbAssets
	 * @return array<KalturaThumbAsset>
	 */
	protected function transformThumbAssets(array $sourceThumbAssets)
	{
		return $this->transformAssets($sourceThumbAssets, $this->mapThumbParamsIds, 'thumbParamsId');
	}

	/**
	 * Transform source caption assets to target objects ready for insert/update
	 * @param array<KalturaCaptionAsset> $sourceCaptionAssets
	 * @return array<KalturaCaptionAsset>
	 */
	protected function transformCaptionAssets(array $sourceCaptionAssets)
	{
		return $this->transformAssets($sourceCaptionAssets, $this->mapCaptionParamsIds, 'captionParamsId');
	}

	/**
	 * Transform source attachment assets to target objects ready for insert/update
	 * @param array<KalturaAttachmentAsset> $sourceAttachmentAssets
	 * @return array<KalturaAttachmentAsset>
	 */
	protected function transformAttachmentAssets(array $sourceAttachmentAssets)
	{
		return $this->transformAssets($sourceAttachmentAssets, $this->mapAttachmentParamsIds);
	}

	/**
	 *
	 * Transform source assets to target assets ready for insert/update
	 * @param array<KalturaAsset> $sourceAssets
	 * @param array $mapParams
	 * @param string $paramsFieldName
	 * @return array<KalturaAsset>
	 */
	protected function transformAssets(array $sourceAssets, array $mapParams, $paramsFieldName = null)
	{
		if (!count($sourceAssets)) {
			return array();
		}

		$targetAssets = array();
		foreach ($sourceAssets as $sourceAsset)
		{
			// remove readonly/insertonly parameters
			$targetAsset = $this->copyObjectForInsertUpdate($sourceAsset);
			if ($paramsFieldName){
				// switch to target params id if defined, else leave same as source
				if (isset($mapParams[$sourceAsset->{$paramsFieldName}]))
				{
					$targetAsset->{$paramsFieldName} = $mapParams[$sourceAsset->{$paramsFieldName}];
				}
				else
				{
					$targetAsset->{$paramsFieldName} = $sourceAsset->{$paramsFieldName};
				}
			}
			$targetAssets[$sourceAsset->id] = $targetAsset;
		}

		return $targetAssets;
	}


	/**
	 * Transform source cue points to target objects ready for insert/update
	 * @param array<KalturaCuePoint> $sourceCuePoints
	 * @return array<KalturaCuePoint>
	 */
	protected function transformCuePoints(array $sourceCuePoints)
	{
		if (!count($sourceCuePoints)) {
			return array();
		}

		$targetCuePoints = array();
		foreach ($sourceCuePoints as $sourceCuePoint)
		{
			// remove readonly/insertonly parameters
			$targetCuePoint = $this->copyObjectForInsertUpdate($sourceCuePoint);
			$targetCuePoints[$sourceCuePoint->id] = $targetCuePoint;
		}

		return $targetCuePoints;
	}


	protected function transformAssetContent(array $assetContent)
	{
		if (!count($assetContent)) {
			return array();
		}

		$targetAssetContent = null;

	}


	/**
	 * Transform source objects to target objects ready for insert/update
	 * @param CrossKalturaEntryObjectsContainer $sourceObjects
	 * @param bool $forUpdate
	 * @return CrossKalturaEntryObjectsContainer target objects
	 */
	protected function transformSourceToTarget(CrossKalturaEntryObjectsContainer $sourceObjects, $forUpdate = false)
	{
		$targetObjects = new CrossKalturaEntryObjectsContainer();
		$targetObjects->entry = $this->transformEntry($sourceObjects->entry, $forUpdate); // basic entry object
		$targetObjects->metadataObjects = $this->transformMetadatas($sourceObjects->metadataObjects); // metadata objects
		$targetObjects->flavorAssets = $this->transformFlavorAssets($sourceObjects->flavorAssets); // flavor assets
		$targetObjects->flavorAssetsContent = $sourceObjects->flavorAssetsContent; // flavor assets content - already transformed
		$targetObjects->thumbAssets = $this->transformThumbAssets($sourceObjects->thumbAssets); // thumb assets
		$targetObjects->timedThumbAssets = $this->transformThumbAssets($sourceObjects->timedThumbAssets); // timed thumb assets
		$targetObjects->thumbAssetsContent = $sourceObjects->thumbAssetsContent; // thumb assets content - already transformed
		if ($this->distributeCaptions)
		{
			$targetObjects->captionAssets = $this->transformCaptionAssets($sourceObjects->captionAssets); // caption assets
			$targetObjects->captionAssetsContent = $sourceObjects->captionAssetsContent; // caption assets content - already transformed
		}
		if ($this->distributeCuePoints)
		{
			$targetObjects->cuePoints = $this->transformCuePoints($sourceObjects->cuePoints); // cue points
			$targetObjects->thumbCuePoints  = $this->transformCuePoints($sourceObjects->thumbCuePoints); // thumb cue points
		}
		if (isset ($sourceObjects->attachmentAssets)){
			$targetObjects->attachmentAssets = $this->transformAttachmentAssets($sourceObjects->attachmentAssets); 
			$targetObjects->attachmentAssetsContent = $sourceObjects->attachmentAssetsContent; 
		}
		return $targetObjects;
	}



	// ------------------------------------------------------------
	//  special methods to extract object arguments for add/update
	// ------------------------------------------------------------

	/**
	 * @return array of arguments that should be passed to metadata->update api action
	 * @param string $existingObjId
	 * @param KalturaMetadata $newObj
	 */
	protected function getMetadataUpdateArgs($existingObjId, KalturaMetadata $newObj)
	{
		return array(
			$existingObjId,
			$newObj->xml
		);
	}

	/**
	 * @return array of arguments that should be passed to metadata->add api action
	 * @param KalturaMetadata $newObj
	 */
	protected function getMetadataAddArgs(KalturaMetadata $newObj)
	{
		return array(
			$newObj->metadataProfileId,
			KalturaMetadataObjectType::ENTRY,
			$newObj->objectId,
			$newObj->xml
		);
	}

	/**
	 * @return array of arguments that should be passed to cuepoint->add api action
	 * @param KalturaCuePoint $newObj
	 */
	protected function getCuePointAddArgs(KalturaCuePoint $newObj)
	{
		return array(
			$newObj
		);
	}


	// ----------------------
	//  distribution actions
	// ----------------------

	/**
	 * Fill provider data with map of distributed objects
	 * @param KalturaDistributionJobData $data
	 * @param CrossKalturaEntryObjectsContainer $syncedObjects
	 */
	protected function getDistributedMap(KalturaDistributionJobData $data, CrossKalturaEntryObjectsContainer $syncedObjects)
	{
		$data->providerData->distributedFlavorAssets = $this->getDistributedMapForObjects($this->sourceObjects->flavorAssets, $syncedObjects->flavorAssets);

		$data->providerData->distributedThumbAssets = $this->getDistributedMapForObjects($this->sourceObjects->thumbAssets, $syncedObjects->thumbAssets);
		$data->providerData->distributedTimedThumbAssets = $this->getDistributedMapForObjects($this->sourceObjects->timedThumbAssets, $syncedObjects->timedThumbAssets);

		$data->providerData->distributedMetadata = $this->getDistributedMapForObjects($this->sourceObjects->metadataObjects, $syncedObjects->metadataObjects);
		$data->providerData->distributedQuiz = $this->getDistributedMapForObjects($this->sourceObjects->quizObjects, $syncedObjects->quizObjects);
		$data->providerData->distributedCaptionAssets = $this->getDistributedMapForObjects($this->sourceObjects->captionAssets, $syncedObjects->captionAssets);

		$data->providerData->distributedAttachmentAssets = $this->getDistributedMapForObjects($this->sourceObjects->attachmentAssets, $syncedObjects->attachmentAssets);
		$data->providerData->distributedCuePoints = $this->getDistributedMapForObjects($this->sourceObjects->cuePoints, $syncedObjects->cuePoints);
		$data->providerData->distributedThumbCuePoints = $this->getDistributedMapForObjects($this->sourceObjects->thumbCuePoints, $syncedObjects->thumbCuePoints);

		return $data;
	}


	/**
	 * Get distributed map for the given objects
	 * @param unknown_type $sourceObjects
	 * @param unknown_type $syncedObjects
	 */
	protected function getDistributedMapForObjects($sourceObjects, $syncedObjects)
	{
		$info = array();
		foreach ($syncedObjects as $sourceId => $targetObj)
		{
			$sourceObj = $sourceObjects[$sourceId];
			$objInfo = array();
			$objInfo[self::DISTRIBUTED_INFO_SOURCE_ID] = $sourceId;
			$objInfo[self::DISTRIBUTED_INFO_TARGET_ID] = $targetObj->id;
			if (isset($sourceObj->version)){
				$objInfo[self::DISTRIBUTED_INFO_SOURCE_VERSION] = $sourceObj->version;
			}
			$objInfo[self::DISTRIBUTED_INFO_SOURCE_UPDATED_AT] = $sourceObj->updatedAt;

			$info[$sourceId] = $objInfo;
		}
		return serialize($info);
	}



	/**
	 * Sync objects between the source and target accounts
	 * @param KalturaServiceBase $targetClientService API service for the current object type
	 * @param array $newObjects array of target objects that should be added/updated
	 * @param array $sourceObjects array of source objects
	 * @param array $distributedMap array of information about previously distributed objects
	 * @param string $targetEntryId
	 * @param string $addArgsFunc special function to extract arguments for the ADD api action
	 * @param string $updateArgsFunc special function to extract arguments for the UPDATE api action
	 * @return array of the synced objects
	 */
	protected function syncTargetEntryObjects(KalturaServiceBase $targetClientService, $newObjects, $sourceObjects, $distributedMap, $targetEntryId, $addArgsFunc = null, $updateArgsFunc = null)
	{
		//KalturaLog::info('ZFP: ' . print_r($distributedMap,true));
		$syncedObjects = array();
		$distributedMap = empty($distributedMap) ? array() : unserialize($distributedMap);

		// walk through all new target objects and add/update on target as necessary
		if (count($newObjects))
		{
			KalturaLog::info('Syncing target objects for source IDs ['.implode(',', array_keys($newObjects)).']');
			foreach ($newObjects as $sourceObjectId => $targetObject)
			{
				if (is_array($distributedMap) && array_key_exists($sourceObjectId, $distributedMap))
				{
					// this object was previously distributed
					KalturaLog::info('Source object id ['.$sourceObjectId.'] was previously distributed');

					$lastDistributedUpdatedAt = isset($distributedMap[$sourceObjectId][self::DISTRIBUTED_INFO_SOURCE_UPDATED_AT]) ? $distributedMap[$sourceObjectId][self::DISTRIBUTED_INFO_SOURCE_UPDATED_AT] : null;
					$currentSourceUpdatedAt = isset($sourceObjects[$sourceObjectId]->updatedAt)	? $sourceObjects[$sourceObjectId]->updatedAt : null;

					$targetObjectId = isset($distributedMap[$sourceObjectId][self::DISTRIBUTED_INFO_TARGET_ID]) ? $distributedMap[$sourceObjectId][self::DISTRIBUTED_INFO_TARGET_ID] : null;
					if (is_null($targetObjectId))
					{
						throw new Exception('Missing previously distributed target object id for source id ['.$sourceObjectId.']');
					}

					if (!is_null($lastDistributedUpdatedAt) && !is_null($currentSourceUpdatedAt) && $currentSourceUpdatedAt <= $lastDistributedUpdatedAt)
					{
						// object wasn't updated since last distributed - just return existing info
						KalturaLog::info('No need to re-distributed object since it was not updated since last distribution - returning dummy object with target id ['.$targetObjectId.']');
						$targetObject->id = $targetObjectId;
						$syncedObjects[$sourceObjectId] = $targetObject;
					}
					else
					{
						// should update existing target object
						$targetObjectForUpdate = $this->removeInsertOnly($targetObject);
						$updateArgs = null;
						if (is_null($updateArgsFunc)) {
							$updateArgs = array($targetObjectId, $targetObjectForUpdate);
						}
						else {
							$updateArgs = call_user_func_array(array($this, $updateArgsFunc), array($targetObjectId, $targetObjectForUpdate));
						}
						$syncedObjects[$sourceObjectId] = call_user_func_array(array($targetClientService, 'update'), $updateArgs);
					}

					unset($distributedMap[$sourceObjectId]);
				}
				else
				{
						// this object was not previously distributed - should add new target object
						$addArgs = null;
						if (is_null($addArgsFunc)) {
							$addArgs = array($targetEntryId, $targetObject);
						}
						else {
							$addArgs = call_user_func_array(array($this, $addArgsFunc), array($targetObject));
						}

					$syncedObjects[$sourceObjectId] = call_user_func_array(array($targetClientService, 'add'), $addArgs);
				}
			}
		}

		// check if previously distributed objects should be deleted from the target account
		if (count($distributedMap))
		{
			KalturaLog::info('Deleting target objects that were deleted in source with IDs ['.implode(',', array_keys($distributedMap)).']');
			foreach ($distributedMap as $sourceId => $objInfo)
			{
				// delete from target account
				$targetId = isset($objInfo[self::DISTRIBUTED_INFO_TARGET_ID]) ? $objInfo[self::DISTRIBUTED_INFO_TARGET_ID] : null;
				KalturaLog::info('Deleting previously distributed source object id ['.$sourceId.'] target object id ['.$targetId.']');
				if (is_null($targetId))
				{
					throw new Exception('Missing previously distributed target object id for source id ['.$sourceId.']');
				}
				try {
					$targetClientService->delete($targetId);
				}
				catch (Exception $e)
				{
					$acceptableErrorCodes = array(
						'FLAVOR_ASSET_ID_NOT_FOUND',
						'THUMB_ASSET_ID_NOT_FOUND',
						'INVALID_OBJECT_ID',
						'CAPTION_ASSET_ID_NOT_FOUND',
						'INVALID_CUE_POINT_ID',
					);
					if (in_array($e->getCode(), $acceptableErrorCodes))
					{
						KalturaLog::warning('Object with id ['.$targetId.'] is already deleted - ignoring exception');
					}
					else
					{
						throw $e;
					}
				}

			}
		}

		return $syncedObjects;
	}


	protected function syncAssetsContent(KalturaServiceBase $targetClientService, $targetAssetsContent, $targetAssets, $distributedMap, $sourceAssets)
	{
		$distributedMap = empty($distributedMap) ? array() : unserialize($distributedMap);

		foreach ($targetAssetsContent as $sourceAssetId => $targetAssetContent)
		{
			$targetAssetId = isset($targetAssets[$sourceAssetId]->id) ? $targetAssets[$sourceAssetId]->id : null;
			if (is_null($targetAssetId))
			{
				throw new Exception('Missing target id of source asset id ['.$sourceAssetId.']');
			}

			$currentSourceVersion = isset($sourceAssets[$sourceAssetId]->version) ? $sourceAssets[$sourceAssetId]->version : null;
			$lastDistributedSourceVersion = isset($distributedMap[$sourceAssetId][self::DISTRIBUTED_INFO_SOURCE_VERSION]) ? $distributedMap[$sourceAssetId][self::DISTRIBUTED_INFO_SOURCE_VERSION] : null;

			if (!is_null($currentSourceVersion) && !is_null($lastDistributedSourceVersion) && $currentSourceVersion <= $lastDistributedSourceVersion)
			{
				KalturaLog::info('No need to update content of source asset id ['.$sourceAssetId.'] target id ['.$targetAssetId.'] since it was not updated since last distribution');
			}
			else
			{
				KalturaLog::info('Updating content for source asset id ['.$sourceAssetId.'] target id ['.$targetAssetId.']');
				$targetClientService->setContent($targetAssetId, $targetAssetContent);
			}
		}
	}

	/**
	 * Sync target objects
	 * @param KalturaDistributionJobData $jobData
	 * @param CrossKalturaEntryObjectsContainer $targetObjects
	 */
	protected function sync(KalturaDistributionJobData $jobData, CrossKalturaEntryObjectsContainer $targetObjects)
	{
		$syncedObjects = new CrossKalturaEntryObjectsContainer();

		$targetEntryId = $jobData->remoteId;

		// add/update entry
		if ($targetEntryId)
		{
			// update entry
			KalturaLog::info('Updating target entry id ['.$targetEntryId.']');
			$syncedObjects->entry = $this->targetClient->baseEntry->update($targetEntryId, $targetObjects->entry);
		}
		else
		{
			// add entry
			$syncedObjects->entry = $this->targetClient->baseEntry->add($targetObjects->entry);
			$targetEntryId = $syncedObjects->entry->id;
			KalturaLog::info('New target entry added with id ['.$targetEntryId.']');
		}
		$this->targetEntryId = $targetEntryId;

		// sync metadata objects
		foreach ($targetObjects->metadataObjects as $metadataObj)
		{
			/* @var $metadataObj KalturaMetadata */
			$metadataObj->objectId = $targetEntryId;
		}
		$targetMetadataClient = KalturaMetadataClientPlugin::get($this->targetClient);
		$syncedObjects->metadataObjects = $this->syncTargetEntryObjects(
			$targetMetadataClient->metadata,
			$targetObjects->metadataObjects,
			$this->sourceObjects->metadataObjects,
			$jobData->providerData->distributedMetadata,
			$targetEntryId,
			'getMetadataAddArgs',
			'getMetadataUpdateArgs'
		);
		// sync quiz objects
		if (isset($this->sourceObjects->quizObjects[0])){
		$targetQuizClient = KalturaQuizClientPlugin::get($this->targetClient);
		  try {
   			 $targetQuizClient->quiz->add($targetEntryId, $this->sourceObjects->quizObjects[0]);
		  } catch (Exception $e) {
			KalturaLog::err('Failed to create quiz obj on ' . $targetEntryId);
		  }
		}


		// sync flavor assets
		$syncedObjects->flavorAssets = $this->syncTargetEntryObjects(
			$this->targetClient->flavorAsset,
			$targetObjects->flavorAssets,
			$this->sourceObjects->flavorAssets,
			$jobData->providerData->distributedFlavorAssets,
			$targetEntryId
		);


		// sync flavor content
		$this->syncAssetsContent(
			$this->targetClient->flavorAsset,
			$targetObjects->flavorAssetsContent,
			$syncedObjects->flavorAssets,
			$jobData->providerData->distributedFlavorAssets,
			$this->sourceObjects->flavorAssets
		);

		// sync thumbnail assets
		$syncedObjects->thumbAssets = $this->syncTargetEntryObjects(
			$this->targetClient->thumbAsset,
			$targetObjects->thumbAssets,
			$this->sourceObjects->thumbAssets,
			$jobData->providerData->distributedThumbAssets,
			$targetEntryId
		);

		// sync caption assets
		if ($this->distributeCaptions)
		{
			$targetCaptionClient = KalturaCaptionClientPlugin::get($this->targetClient);
			$syncedObjects->captionAssets = $this->syncTargetEntryObjects(
				$targetCaptionClient->captionAsset,
				$targetObjects->captionAssets,
				$this->sourceObjects->captionAssets,
				$jobData->providerData->distributedCaptionAssets,
				$targetEntryId
			);


			// sync caption content
			$this->syncAssetsContent(
				$targetCaptionClient->captionAsset,
				$targetObjects->captionAssetsContent,
				$syncedObjects->captionAssets,
				$jobData->providerData->distributedCaptionAssets,
				$this->sourceObjects->captionAssets
			);
		}


		// sync cue points
		if ($this->distributeCuePoints)
		{
			foreach ($targetObjects->cuePoints as $cuePoint)
			{
				/* @var $cuePoint KalturaCuePoint */
				$cuePoint->entryId = $targetEntryId;
			}
			$targetCuePointClient = KalturaCuePointClientPlugin::get($this->targetClient);
			$syncedObjects->cuePoints = $this->syncTargetEntryObjects(
				$targetCuePointClient->cuePoint,
				$targetObjects->cuePoints,
				$this->sourceObjects->cuePoints,
				$jobData->providerData->distributedCuePoints,
				$targetEntryId,
				'getCuePointAddArgs'
			);

			$distributedThumbCuePointsMap = empty($jobData->providerData->distributedThumbCuePoints) ? array() : unserialize($jobData->providerData->distributedThumbCuePoints);
			$distributedTimedThumbAssetsMap = empty($jobData->providerData->distributedTimedThumbAssets) ? array() : unserialize($jobData->providerData->distributedTimedThumbAssets);
			foreach ($targetObjects->thumbCuePoints as $id => $thumbCuePoint)
			{
				$thumbCuePoint->entryId = $targetEntryId;
				
				//Clear cuePoint assetId only if it was previously distributed but its associated timedThumbASset was not.  
				if(isset($distributedThumbCuePointsMap[$id])
						&& !isset($distributedTimedThumbAssetsMap[$thumbCuePoint->assetId]))
					$thumbCuePoint->assetId = "";
				else
					$thumbCuePoint->assetId = null;
			}
			
			$targetCuePointClient = KalturaCuePointClientPlugin::get($this->targetClient);
			$syncedObjects->thumbCuePoints = $this->syncTargetEntryObjects(
				$targetCuePointClient->cuePoint,
				$targetObjects->thumbCuePoints,
				$this->sourceObjects->thumbCuePoints,
				$jobData->providerData->distributedThumbCuePoints,
				$targetEntryId,
				'getCuePointAddArgs'
			);

			foreach ($targetObjects->timedThumbAssets as $timedThumbAsset)
			{
				$timedThumbAsset->cuePointId = $syncedObjects->thumbCuePoints[$timedThumbAsset->cuePointId]->id;
			}

			// sync Timed thumbnail assets
			$syncedObjects->timedThumbAssets = $this->syncTargetEntryObjects(
				$this->targetClient->thumbAsset,
				$targetObjects->timedThumbAssets,
				$this->sourceObjects->timedThumbAssets,
				$jobData->providerData->distributedTimedThumbAssets,
				$targetEntryId
			);
		}

		// sync thumbnail content
		$this->syncAssetsContent(
			$this->targetClient->thumbAsset,
			$targetObjects->thumbAssetsContent,
			array_merge($syncedObjects->thumbAssets,$syncedObjects->timedThumbAssets),
			$jobData->providerData->distributedThumbAssets,
			$this->sourceObjects->thumbAssets
		);

		$targetAttachmentClient = KalturaAttachmentClientPlugin::get($this->targetClient);
		$syncedObjects->attachmentAssets = $this->syncTargetEntryObjects(
			$targetAttachmentClient->attachmentAsset,
			$targetObjects->attachmentAssets,
			$this->sourceObjects->attachmentAssets,
			$jobData->providerData->distributedAttachmentAssets,
			$targetEntryId
		);


		// sync attachment content
		$this->syncAssetsContent(
			$targetAttachmentClient->attachmentAsset,
			$targetObjects->attachmentAssetsContent,
			$syncedObjects->attachmentAssets,
			$jobData->providerData->distributedAttachmentAssets,
			$this->sourceObjects->attachmentAssets
		);

		return $syncedObjects;
	}


	/* (non-PHPdoc)
     * @see IDistributionEngineSubmit::submit()
     */
	public function submit(KalturaDistributionSubmitJobData $data)
	{
		// initialize
		$this->init($data);

		try {
			// get source entry objects
			$this->sourceObjects = $this->getSourceObjects($data);

			// transform source objects to target objects ready for insert
			$targetObjects = $this->transformSourceToTarget($this->sourceObjects, false);

			// add objects to target account
			$addedTargetObjects = $this->sync($data, $targetObjects);

			// save target entry id
			$data->remoteId = $addedTargetObjects->entry->id;

			// get info about distributed objects
			$data = $this->getDistributedMap($data, $addedTargetObjects);

			// all done - no need for closer
		}
		catch (Exception $e)
		{
			// if a new target entry was created - delete it before failing distribution
			if ($this->targetEntryId)
			{
				KalturaLog::info('Deleting partial new target entry ['.$this->targetEntryId.']');
				// delete entry from target account - may throw an exception
				try {
					$deleteResult = $this->targetClient->baseEntry->delete($this->targetEntryId);
				}
				catch (Exception $ignoredException)
				{
					KalturaLog::err('Failed deleting partial entry ['.$this->targetEntryId.'] - '.$ignoredException->getMessage());
				}
			}

			// delete original exception
			throw $e;
		}

		return true;
	}



	/* (non-PHPdoc)
     * @see IDistributionEngineUpdate::update()
     */
	public function update(KalturaDistributionUpdateJobData $data)
	{
		// initialize
		$this->init($data);

		// cannot update if remoteId is missing
		$targetEntryId = $data->remoteId;
		if (!$targetEntryId) {
			throw new Exception('Cannot delete remote entry - remote entry ID is empty');
		}

		// get source entry objects
		$this->sourceObjects = $this->getSourceObjects($data);

		// transform source objects to target objects ready for update
		$targetObjects = $this->transformSourceToTarget($this->sourceObjects, true);

		// update objects on the target account
		$updatedTargetObjects = $this->sync($data, $targetObjects);

		// get info about distributed objects
		$data = $this->getDistributedMap($data, $updatedTargetObjects);
		// update default thumbnail
		$thumbFilter = new KalturaFlavorAssetFilter();
		$thumbFilter->entryIdEqual = $targetEntryId;
		$thumbAsset = $this->targetClient->thumbAsset->listAction($thumbFilter, null);
		$this->targetClient->thumbAsset->setAsDefault($thumbAsset->objects[0]->id);

		// all done - no need for closer
		return true;
	}



	/* (non-PHPdoc)
     * @see IDistributionEngineDelete::delete()
     */
	public function delete(KalturaDistributionDeleteJobData $data)
	{
		// initialize
		$this->init($data);

		// cannot delete if remoteId is missing
		$targetEntryId = $data->remoteId;
		if (!$targetEntryId) {
			throw new Exception('Cannot delete remote entry - remote entry ID is empty');
		}

		// delete entry from target account - may throw an exception
		$deleteResult = $this->targetClient->baseEntry->delete($targetEntryId);

		// all done - no need for closer
		return true;
	}



	// ----------------
	//  helper methods
	// ----------------

	/**
	 * Copy an object for later inserting/updating through the API
	 * @param unknown_type $sourceObject
	 */
	protected function copyObjectForInsertUpdate ($sourceObject)
	{
		$reflect = new ReflectionClass($sourceObject);
		$props = $reflect->getProperties(ReflectionProperty::IS_PUBLIC);
		$newObjectClass = get_class($sourceObject);
		$newObject = new $newObjectClass;
		foreach ($props as $prop)
		{
			$docComment = $prop->getDocComment();
			$propReadOnly = preg_match("/\\@readonly/i", $docComment);
			$deprecated = preg_match("/\\DEPRECATED/i", $docComment);

			$copyProperty = !$deprecated && !$propReadOnly && $prop->name!="displayInSearch";

			if ($copyProperty) {
				$propertyName = $prop->name;
				$newObject->{$propertyName} = $sourceObject->{$propertyName};
			}
		}
		return $newObject;
	}


	/**
	 * Set to 'null' parameters marked as @insertonly
	 * @param $object
	 */
	protected function removeInsertOnly($object)
	{
		$reflect = new ReflectionClass($object);
		$props = $reflect->getProperties(ReflectionProperty::IS_PUBLIC);
		foreach ($props as $prop)
		{
			$docComment = $prop->getDocComment();
			$propInsertOnly = preg_match("/\\@insertonly/i", $docComment);

			if ($propInsertOnly) {
				$propertyName = $prop->name;
				$object->{$propertyName} = null;
			}
		}
		return $object;
	}

	/**
	 * @param string $fieldName
	 * @return value for field from $this->fieldValues, or null if no value defined
	 */
	protected function getValueForField($fieldName)
	{
		if (isset($this->fieldValues[$fieldName])) {
			return $this->fieldValues[$fieldName];
		}
		return null;
	}


	protected function toKeyValueArray($apiKeyValueArray)
	{
		$keyValueArray = array();
		if (count($apiKeyValueArray))
		{
			foreach($apiKeyValueArray as $keyValueObj)
			{
				/* @var $keyValueObj KalturaKeyValue */
				$keyValueArray[$keyValueObj->key] = $keyValueObj->value;
			}
		}
		return $keyValueArray;
	}


	/**
	 * Transform XML using XSLT
	 * @param string $xmlStr
	 * @param string $xslStr
	 * @return string the result XML
	 */
	protected function transformXml($xmlStr, $xslStr)
	{
		$xmlObj = new DOMDocument();
		if (!$xmlObj->loadXML($xmlStr))
		{
			throw new Exception('Error loading source XML');
		}

		$xslObj = new DOMDocument();
		if(!$xslObj->loadXML($xslStr))
		{
			throw new Exception('Error loading XSLT');
		}

		$proc = new XSLTProcessor;
		$proc->registerPHPFunctions(kXml::getXslEnabledPhpFunctions());
		$proc->importStyleSheet($xslObj);

		$resultXmlObj = $proc->transformToDoc($xmlObj);
		if (!$resultXmlObj)
		{
			throw new Exception('Error transforming XML');
			return null;
		}

		$resultXmlStr = $resultXmlObj->saveXML();
		return $resultXmlStr;
	}

	function log($message)
	{
		KalturaLog::log($message);
	}

}
