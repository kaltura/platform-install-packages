<?php
/**
 * @package plugins.crossKalturaDistribution
 * @subpackage api.objects
 */
class KalturaCrossKalturaDistributionProfile extends KalturaConfigurableDistributionProfile
{
	/**
	 * @var string
	 */
	public $targetServiceUrl;
	
	/**
	 * @var int
	 */
	public $targetAccountId;
	
	/**
	 * @var string
	 */
	public $targetLoginId;
	
	/**
	 * @var string
	 */
	public $targetLoginPassword;
	
	/**
	 * @var string
	 */
	 public $metadataXslt;
	 
 	/**
	 * @var KalturaStringValueArray
	 */
	 public $metadataXpathsTriggerUpdate;
	 
	 /**
	  * @var bool
	  */
	 public $distributeCaptions;
	 
	 /**
	  * @var string
	  */
	 public $designatedCategories;
	 
	 /**
	  * @var bool
	  */
	 public $distributeCategories;
	 
	 /**
	  * @var string
	  */
	 public $collaboratorsCustomMetadataProfileId;
	 
	 /**
	  * @var bool
	  */
	 public $collaboratorsFromCustomMetadataProfile;
	 
	
	 /**
	  * @var bool
	  */
	 public $distributeCuePoints;
	 
	 /**
	  * @var bool
	  */
	 public $distributeRemoteFlavorAssetContent;
	 
	 /**
	  * @var bool
	  */
	 public $distributeRemoteThumbAssetContent;
	 
	 /**
	  * @var bool
	  */
	 public $distributeRemoteCaptionAssetContent;
	 
	 /**
	  * @var KalturaKeyValueArray
	  */
	 public $mapAccessControlProfileIds;
	 
	 /**
	  * @var KalturaKeyValueArray
	  */
	 public $mapConversionProfileIds;
	 
	 /**
	  * @var KalturaKeyValueArray
	  */
	 public $mapMetadataProfileIds;
	 
	 /**
	  * @var KalturaKeyValueArray
	  */
	 public $mapStorageProfileIds;
	 
	 /**
	  * @var KalturaKeyValueArray
	  */
	 public $mapFlavorParamsIds;
	 
	 /**
	  * @var KalturaKeyValueArray
	  */
	 public $mapThumbParamsIds;
	 
	 /**
	  * @var KalturaKeyValueArray
	  */
	 public $mapCaptionParamsIds;
	 	  
	 /**
	  * @var KalturaKeyValueArray
	  */
	 public $mapAttachmentParamsIds;
	 	  
	 
	 
	/*
	 * mapping between the field on this object (on the left) and the setter/getter on the object (on the right)  
	 */
	private static $map_between_objects = array 
	(
		'targetServiceUrl',
		'targetAccountId',
	    	'targetLoginId',
		'targetLoginPassword',
	    	'distributeCaptions',
	    	'distributeCuePoints',
	 	'distributeRemoteFlavorAssetContent',
	 	'distributeRemoteThumbAssetContent',
	 	'distributeRemoteCaptionAssetContent',
	    	'distributeCategories',
	    	'designatedCategories',
		'collaboratorsFromCustomMetadataProfile',
		'collaboratorsCustomMetadataProfileId',
		'metadataXslt',
	    'metadataXpathsTriggerUpdate' => 'additionalMetadataXpathsTriggerUpdate',
	);
		 
	public function getMapBetweenObjects()
	{
		return array_merge(parent::getMapBetweenObjects(), self::$map_between_objects);
	}
	
    public function toObject ( $object_to_fill = null , $props_to_skip = array() )
	{
		if(is_null($object_to_fill))
			$object_to_fill = new CrossKalturaDistributionProfile();
		
		/* @var $object_to_fill CrossKalturaDistributionProfile */
		$object_to_fill =  parent::toObject($object_to_fill, $props_to_skip);
		
		if (!is_null($this->mapAccessControlProfileIds)) {
		    $object_to_fill->setMapAccessControlProfileIds($this->toKeyValueArray($this->mapAccessControlProfileIds));
		}
		if (!is_null($this->mapConversionProfileIds)) {
		    $object_to_fill->setMapConversionProfileIds($this->toKeyValueArray($this->mapConversionProfileIds));
	    }
		if (!is_null($this->mapMetadataProfileIds)) {
		    $object_to_fill->setMapMetadataProfileIds($this->toKeyValueArray($this->mapMetadataProfileIds));    
		}
		if (!is_null($this->mapStorageProfileIds)) {
		    $object_to_fill->setMapStorageProfileIds($this->toKeyValueArray($this->mapStorageProfileIds));
	    }
		if (!is_null($this->mapFlavorParamsIds)) {
		    $object_to_fill->setMapFlavorParamsIds($this->toKeyValueArray($this->mapFlavorParamsIds));
		}
		if (!is_null($this->mapThumbParamsIds)) {
		    $object_to_fill->setMapThumbParamsIds($this->toKeyValueArray($this->mapThumbParamsIds));
		}
		if (!is_null($this->mapCaptionParamsIds)) {
		    $object_to_fill->setMapCaptionParamsIds($this->toKeyValueArray($this->mapCaptionParamsIds));
		}
		if (!is_null($this->mapAttachmentParamsIds)) {
		    $object_to_fill->setMapAttachmentParamsIds($this->toKeyValueArray($this->mapAttachmentParamsIds));
		}
		
		return $object_to_fill;
	}
	
	public function doFromObject($source_object, KalturaDetachedResponseProfile $responseProfile = null)
	{
	    parent::doFromObject($source_object, $responseProfile);
	    
	    /* @var $source_object CrossKalturaDistributionProfile */
	    $this->mapAccessControlProfileIds = KalturaKeyValueArray::fromKeyValueArray($source_object->getMapAccessControlProfileIds());
	    $this->mapConversionProfileIds = KalturaKeyValueArray::fromKeyValueArray($source_object->getMapConversionProfileIds());
	    $this->mapMetadataProfileIds = KalturaKeyValueArray::fromKeyValueArray($source_object->getMapMetadataProfileIds());
	    $this->mapStorageProfileIds = KalturaKeyValueArray::fromKeyValueArray($source_object->getMapStorageProfileIds());
	    $this->mapFlavorParamsIds = KalturaKeyValueArray::fromKeyValueArray($source_object->getMapFlavorParamsIds());
	    $this->mapThumbParamsIds = KalturaKeyValueArray::fromKeyValueArray($source_object->getMapThumbParamsIds());
	    $this->mapCaptionParamsIds = KalturaKeyValueArray::fromKeyValueArray($source_object->getMapCaptionParamsIds());
	    $this->mapAttachmentParamsIds = KalturaKeyValueArray::fromKeyValueArray($source_object->getMapAttachmentParamsIds());
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

}
