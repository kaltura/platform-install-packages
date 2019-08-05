<?php
/**
 * @package plugins.crossKalturaDistribution
 * @subpackage api.objects
 */
class KalturaCrossKalturaDistributionJobProviderData extends KalturaConfigurableDistributionJobProviderData
{
    /**
     * Key-value array where the keys are IDs of distributed flavor assets in the source account and the values are the matching IDs in the target account
     * @var string
     */
    public $distributedFlavorAssets;
    
    /**
     * Key-value array where the keys are IDs of distributed thumb assets in the source account and the values are the matching IDs in the target account
     * @var string
     */
    public $distributedThumbAssets;
    
    /**
     * Key-value array where the keys are IDs of distributed metadata objects in the source account and the values are the matching IDs in the target account
     * @var string
     */
    public $distributedMetadata;
    
    /**
     * Key-value array where the keys are IDs of distributed caption assets in the source account and the values are the matching IDs in the target account
     * @var string
     */
    public $distributedCaptionAssets;

    /**
     * Key-value array where the keys are IDs of distributed caption assets in the source account and the values are the matching IDs in the target account
     * @var string
     */
    public $distributedAttachmentAssets;
    
    
    /**
     * Key-value array where the keys are IDs of distributed cue points in the source account and the values are the matching IDs in the target account
     * @var string
     */
    public $distributedCuePoints;

	/**
	 * Key-value array where the keys are IDs of distributed thumb cue points in the source account and the values are the matching IDs in the target account
	 * @var string
	 */
	public $distributedThumbCuePoints;

	/**
	 * Key-value array where the keys are IDs of distributed timed thumb assets in the source account and the values are the matching IDs in the target account
	 * @var string
	 */
	public $distributedTimedThumbAssets;
    
    public function __construct(KalturaDistributionJobData $distributionJobData = null)
	{			   
		parent::__construct($distributionJobData);
	    
		if (!$distributionJobData) {
			return;
		}
			
		if (!($distributionJobData->distributionProfile instanceof KalturaCrossKalturaDistributionProfile)) {
			return;
		}
					
		// load previously distributed data from entry distribution	
		$entryDistributionDb = EntryDistributionPeer::retrieveByPK($distributionJobData->entryDistributionId);
		if (!$entryDistributionDb)
		{
		    KalturaLog::err('Entry distribution ['.$distributionJobData->entryDistributionId.'] not found');
		    return;
		}
		
		$this->distributedFlavorAssets = $entryDistributionDb->getFromCustomData(CrossKalturaDistributionCustomDataField::DISTRIBUTED_FLAVOR_ASSETS);
		$this->distributedThumbAssets = $entryDistributionDb->getFromCustomData(CrossKalturaDistributionCustomDataField::DISTRIBUTED_THUMB_ASSETS);
		$this->distributedMetadata = $entryDistributionDb->getFromCustomData(CrossKalturaDistributionCustomDataField::DISTRIBUTED_METADATA);
		$this->distributedCaptionAssets = $entryDistributionDb->getFromCustomData(CrossKalturaDistributionCustomDataField::DISTRIBUTED_CAPTION_ASSETS);
		$this->distributedCuePoints = $entryDistributionDb->getFromCustomData(CrossKalturaDistributionCustomDataField::DISTRIBUTED_CUE_POINTS);
		$this->distributedThumbCuePoints = $entryDistributionDb->getFromCustomData(CrossKalturaDistributionCustomDataField::DISTRIBUTED_THUMB_CUE_POINTS);
		$this->distributedTimedThumbAssets = $entryDistributionDb->getFromCustomData(CrossKalturaDistributionCustomDataField::DISTRIBUTED_TIMED_THUMB_ASSETS);
	}
	
	
    private static $map_between_objects = array
	(
		'distributedFlavorAssets',
		'distributedThumbAssets',
		'distributedMetadata',
		'distributedCaptionAssets',
    	'distributedCuePoints',
    	'distributedThumbCuePoints',
	    'distributedTimedThumbAssets',
	);

	public function getMapBetweenObjects()
	{
		return array_merge(parent::getMapBetweenObjects(), self::$map_between_objects);
	}
	
	public function toObject($dbObject = null, $skip = array())
	{
		if (is_null($dbObject))
			$dbObject = new kCrossKalturaDistributionJobProviderData();
			
		return parent::toObject($dbObject, $skip);
	}
    
}
