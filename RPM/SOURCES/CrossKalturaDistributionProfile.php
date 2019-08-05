<?php
/**
 * @package plugins.crossKalturaDistribution
 * @subpackage model
 */
class CrossKalturaDistributionProfile extends ConfigurableDistributionProfile
{
	// custom data fields
    
    const CUSTOM_DATA_DISTRIBUTE_CAPTIONS = 'distributeCaptions';
    const CUSTOM_DATA_DISTRIBUTE_CATEGORIES = 'distributeCategories';
    const CUSTOM_DATA_DESIGNATED_CATEGORIES = 'designatedCategories';
    const CUSTOM_DATA_COLLABORATORS_CUSTOM_METADATA_PROFILE_ID = 'collaboratorsCustomMetadataProfileId';
    const CUSTOM_DATA_COLLABORATORS_FROM_CUSTOM_METADATA_PROFILE = 'collaboratorsFromCustomMetadataProfile';
    const CUSTOM_DATA_DISTRIBUTE_CUEPOINTS = 'distributeCuePoints';
    const CUSTOM_DATA_DISTRIBUTE_REMOTE_FLAVOR_ASSET_CONTENT = 'distributeRemoteFlavorAssetContent';
    const CUSTOM_DATA_DISTRIBUTE_REMOTE_THUMB_ASSET_CONTENT = 'distributeRemoteThumbAssetContent';
    const CUSTOM_DATA_DISTRIBUTE_REMOTE_CAPTION_ASSET_CONTENT = 'distributeRemoteCaptionAssetContent';   
    const CUSTOM_DATA_TARGET_SERVICE_URL = 'targetServiceUrl';
	const CUSTOM_DATA_TARGET_ACCOUNT_ID = 'targetAccountId';
	const CUSTOM_DATA_TARGET_LOGIN_ID = 'targetLoginId';
	const CUSTOM_DATA_TARGET_LOGIN_PASSWORD = 'targetLoginPassword';
    const CUSTOM_DATA_METADATA_XSLT = 'metadataXslt';
    const CUSTOM_DATA_ADDITIONAL_METADATA_XPATHS_TRIGGER_UPDATE = 'additionalMetadataXpathsTriggerUpdate'; 
    
    const CUSTOM_DATA_MAP_ACCESS_CONTROL_PROFILE_IDS = 'mapAccessControlProfileIds';
    const CUSTOM_DATA_MAP_CONVERSION_PROFILE_IDS = 'mapConversionProfileIds';
    const CUSTOM_DATA_MAP_METADATA_PROFILE_IDS = 'mapMetadataProfileIds';
    const CUSTOM_DATA_MAP_FLAVOR_PARAMS_IDS = 'mapFlavorParamsIds';
    const CUSTOM_DATA_MAP_THUMB_PARAMS_IDS = 'mapThumbParamsIds';
    const CUSTOM_DATA_MAP_CAPTION_PARAMS_IDS = 'mapCaptionParamsIds';
    const CUSTOM_DATA_MAP_ATTACHMENT_PARAMS_IDS = 'mapAttachmentParamsIds';
    const CUSTOM_DATA_MAP_STORAGE_PROFILE_IDS = 'mapStorageProfileIds';
    
    
    // custom data Getters / Setters
	
    public function getMapAccessControlProfileIds()		{return $this->getFromCustomData(self::CUSTOM_DATA_MAP_ACCESS_CONTROL_PROFILE_IDS, null, array());}
    public function getMapConversionProfileIds()		{return $this->getFromCustomData(self::CUSTOM_DATA_MAP_CONVERSION_PROFILE_IDS, null, array());}
    public function getMapMetadataProfileIds()		    {return $this->getFromCustomData(self::CUSTOM_DATA_MAP_METADATA_PROFILE_IDS, null, array());}
    public function getMapFlavorParamsIds()		        {return $this->getFromCustomData(self::CUSTOM_DATA_MAP_FLAVOR_PARAMS_IDS, null, array());}
    public function getMapThumbParamsIds()		        {return $this->getFromCustomData(self::CUSTOM_DATA_MAP_THUMB_PARAMS_IDS, null, array());}
    public function getMapCaptionParamsIds()		    {return $this->getFromCustomData(self::CUSTOM_DATA_MAP_CAPTION_PARAMS_IDS, null, array());}
    public function getMapAttachmentParamsIds()		    {return $this->getFromCustomData(self::CUSTOM_DATA_MAP_ATTACHMENT_PARAMS_IDS, null, array());}
    public function getMapStorageProfileIds()		    {return $this->getFromCustomData(self::CUSTOM_DATA_MAP_STORAGE_PROFILE_IDS, null, array());}
    public function getDistributeCaptions()		        {return $this->getFromCustomData(self::CUSTOM_DATA_DISTRIBUTE_CAPTIONS);}
    public function getDistributeCategories()		        {return $this->getFromCustomData(self::CUSTOM_DATA_DISTRIBUTE_CATEGORIES);}
    public function getDesignatedCategories()		        {return $this->getFromCustomData(self::CUSTOM_DATA_DESIGNATED_CATEGORIES);}
    public function getCollaboratorsCustomMetadataProfileId()		        {return $this->getFromCustomData(self::CUSTOM_DATA_COLLABORATORS_CUSTOM_METADATA_PROFILE_ID);}
    public function getCollaboratorsFromCustomMetadataProfile()		        {return $this->getFromCustomData(self::CUSTOM_DATA_COLLABORATORS_FROM_CUSTOM_METADATA_PROFILE);}
	public function getDistributeCuePoints()            {return $this->getFromCustomData(self::CUSTOM_DATA_DISTRIBUTE_CUEPOINTS);}
	public function getDistributeRemoteFlavorAssetContent()		{return $this->getFromCustomData(self::CUSTOM_DATA_DISTRIBUTE_REMOTE_FLAVOR_ASSET_CONTENT);}
	public function getDistributeRemoteThumbAssetContent()		{return $this->getFromCustomData(self::CUSTOM_DATA_DISTRIBUTE_REMOTE_THUMB_ASSET_CONTENT);}
	public function getDistributeRemoteCaptionAssetContent()	{return $this->getFromCustomData(self::CUSTOM_DATA_DISTRIBUTE_REMOTE_CAPTION_ASSET_CONTENT);}
	public function getTargetServiceUrl()		        {return $this->getFromCustomData(self::CUSTOM_DATA_TARGET_SERVICE_URL);}
	public function getTargetAccountId()		        {return $this->getFromCustomData(self::CUSTOM_DATA_TARGET_ACCOUNT_ID);}
	public function getTargetLoginId()		            {return $this->getFromCustomData(self::CUSTOM_DATA_TARGET_LOGIN_ID);}
	public function getTargetLoginPassword()	        {return $this->getFromCustomData(self::CUSTOM_DATA_TARGET_LOGIN_PASSWORD);}
	public function getMetadataXslt()		            {return $this->getFromCustomData(self::CUSTOM_DATA_METADATA_XSLT);}
    public function getAdditionalMetadataXpathsTriggerUpdate()
    {
        return $this->getFromCustomData(self::CUSTOM_DATA_ADDITIONAL_METADATA_XPATHS_TRIGGER_UPDATE, null, array());
    }
	
	
    public function setMapAccessControlProfileIds($v)   {$this->putInCustomData(self::CUSTOM_DATA_MAP_ACCESS_CONTROL_PROFILE_IDS, $v);}
	public function setMapConversionProfileIds($v)      {$this->putInCustomData(self::CUSTOM_DATA_MAP_CONVERSION_PROFILE_IDS, $v);}
	public function setMapMetadataProfileIds($v)        {$this->putInCustomData(self::CUSTOM_DATA_MAP_METADATA_PROFILE_IDS, $v);}
	public function setMapFlavorParamsIds($v)           {$this->putInCustomData(self::CUSTOM_DATA_MAP_FLAVOR_PARAMS_IDS, $v);}
	public function setMapThumbParamsIds($v)            {$this->putInCustomData(self::CUSTOM_DATA_MAP_THUMB_PARAMS_IDS, $v);}
	public function setMapCaptionParamsIds($v)          {$this->putInCustomData(self::CUSTOM_DATA_MAP_CAPTION_PARAMS_IDS, $v);}
	public function setMapAttachmentParamsIds($v)          {$this->putInCustomData(self::CUSTOM_DATA_MAP_ATTACHMENT_PARAMS_IDS, $v);}
    public function setMapStorageProfileIds($v)         {$this->putInCustomData(self::CUSTOM_DATA_MAP_STORAGE_PROFILE_IDS, $v);}
    public function setDistributeCaptions($v)           {$this->putInCustomData(self::CUSTOM_DATA_DISTRIBUTE_CAPTIONS, $v);}
    public function setDistributeCategories($v)           {$this->putInCustomData(self::CUSTOM_DATA_DISTRIBUTE_CATEGORIES, $v);}
    public function setDesignatedCategories($v)		        {return $this->putInCustomData(self::CUSTOM_DATA_DESIGNATED_CATEGORIES, $v);}
    public function setCollaboratorsCustomMetadataProfileId($v)		        {return $this->putInCustomData(self::CUSTOM_DATA_COLLABORATORS_CUSTOM_METADATA_PROFILE_ID,$v);}
    public function setCollaboratorsFromCustomMetadataProfile($v)		        {return $this->putInCustomData(self::CUSTOM_DATA_COLLABORATORS_FROM_CUSTOM_METADATA_PROFILE,$v);}
	public function setDistributeCuePoints($v)          {$this->putInCustomData(self::CUSTOM_DATA_DISTRIBUTE_CUEPOINTS, $v);}
	public function setDistributeRemoteFlavorAssetContent($v)     {$this->putInCustomData(self::CUSTOM_DATA_DISTRIBUTE_REMOTE_FLAVOR_ASSET_CONTENT, $v);}
	public function setDistributeRemoteThumbAssetContent($v)      {$this->putInCustomData(self::CUSTOM_DATA_DISTRIBUTE_REMOTE_THUMB_ASSET_CONTENT, $v);}
	public function setDistributeRemoteCaptionAssetContent($v)    {$this->putInCustomData(self::CUSTOM_DATA_DISTRIBUTE_REMOTE_CAPTION_ASSET_CONTENT, $v);}
	public function setTargetServiceUrl($v)            	{$this->putInCustomData(self::CUSTOM_DATA_TARGET_SERVICE_URL, $v);}
	public function setTargetAccountId($v)		        {$this->putInCustomData(self::CUSTOM_DATA_TARGET_ACCOUNT_ID, $v);}
	public function setTargetLoginId($v)		        {$this->putInCustomData(self::CUSTOM_DATA_TARGET_LOGIN_ID, $v);}
	public function setTargetLoginPassword($v)	        {$this->putInCustomData(self::CUSTOM_DATA_TARGET_LOGIN_PASSWORD, $v);}
	public function setMetadataXslt($v)			        {$this->putInCustomData(self::CUSTOM_DATA_METADATA_XSLT, $v);}
    public function setAdditionalMetadataXpathsTriggerUpdate($v)	{$this->putInCustomData(self::CUSTOM_DATA_ADDITIONAL_METADATA_XPATHS_TRIGGER_UPDATE, $v);}
    
    
    
	// distribution related methods
    
	
	/* (non-PHPdoc)
	 * @see DistributionProfile::getProvider()
	 */
	public function getProvider()
	{
		return CrossKalturaDistributionPlugin::getProvider();
	}
	
	
	/* (non-PHPdoc)
	 * @see IDistributionProvider::getUpdateRequiredMetadataXPaths()
	 */
	public function getUpdateRequiredMetadataXPaths()
	{
	    $updateRequired = parent::getUpdateRequiredMetadataXPaths();
	    $additionalXpaths = $this->getAdditionalMetadataXpathsTriggerUpdate();
	    if (count($additionalXpaths))
	    {
		    foreach ($additionalXpaths as $xpathStringValue)
		    {
		        /* @var $xpathStringValue kStringValue */
		        $updateRequired[] = $xpathStringValue->getValue();
		    }
	    }
        return $updateRequired;
	}
	
	/* (non-PHPdoc)
	 * @see DistributionProfile::validateForSubmission()
	 */
	public function validateForSubmission(EntryDistribution $entryDistribution, $action)
	{
		$validationErrors = parent::validateForSubmission($entryDistribution, $action);

		// make sure that all flavor assets marked for distribution have a flavor params id assigned to them
		$flavorAssetIds = explode(',', $entryDistribution->getFlavorAssetIds());
		if (count($flavorAssetIds))
		{
		    $c = new Criteria();
		    $c->addAnd(assetPeer::ID, $flavorAssetIds, Criteria::IN);
    		$flavorTypes = assetPeer::retrieveAllFlavorsTypes();
    		$c->add(assetPeer::TYPE, $flavorTypes, Criteria::IN);
    		$flavorAssets = assetPeer::doSelect($c);
		
		    foreach ($flavorAssets as $asset)
		    {
		        /* @var $asset flavorAsset */
		        if (strlen($asset->getFlavorParamsId()) <= 0)
		        {
		            $validationErrors[] = $this->createValidationError($action, DistributionErrorType::INVALID_DATA, 'flavor asset', 'flavor asset must be assigned to a flavor params id');		        
		        }
		    }
		}

		return $validationErrors;
	}
	
	
	/* (non-PHPdoc)
	 * @see ConfigurableDistributionProfile::getDefaultFieldConfigArray()
	 */
	protected function getDefaultFieldConfigArray()
	{	    
	    $fieldConfigArray = parent::getDefaultFieldConfigArray();

	    // entry name
	    $fieldConfig = new DistributionFieldConfig();
	    $fieldConfig->setFieldName(CrossKalturaDistributionField::BASE_ENTRY_NAME);
	    $fieldConfig->setUserFriendlyFieldName('Name');
	    $fieldConfig->setEntryMrssXslt('<xsl:value-of select="string(title)" />');
	    $fieldConfig->setUpdateOnChange(true);
	    $fieldConfig->setUpdateParams(array(entryPeer::NAME));
	    $fieldConfig->setIsRequired(DistributionFieldRequiredStatus::REQUIRED_BY_PROVIDER);
	    $fieldConfigArray[$fieldConfig->getFieldName()] = $fieldConfig;
	    
	    // entry description
	    $fieldConfig = new DistributionFieldConfig();
	    $fieldConfig->setFieldName(CrossKalturaDistributionField::BASE_ENTRY_DESCRIPTION);
	    $fieldConfig->setUserFriendlyFieldName('Description');
	    $fieldConfig->setEntryMrssXslt('<xsl:value-of select="string(description)" />');
	    $fieldConfig->setUpdateOnChange(true);
	    $fieldConfig->setUpdateParams(array(entryPeer::DESCRIPTION));
	    $fieldConfig->setIsRequired(DistributionFieldRequiredStatus::NOT_REQUIRED);
	    $fieldConfigArray[$fieldConfig->getFieldName()] = $fieldConfig;
	    
	    // entry user id
	    $fieldConfig = new DistributionFieldConfig();
	    $fieldConfig->setFieldName(CrossKalturaDistributionField::BASE_ENTRY_USER_ID);
	    $fieldConfig->setUserFriendlyFieldName('User ID');
	    $fieldConfig->setEntryMrssXslt('<xsl:value-of select="string(userId)" />');
	    $fieldConfig->setUpdateOnChange(true);
	    $fieldConfig->setUpdateParams(array(entryPeer::PUSER_ID));
	    $fieldConfig->setIsRequired(DistributionFieldRequiredStatus::NOT_REQUIRED);
	    $fieldConfigArray[$fieldConfig->getFieldName()] = $fieldConfig;
	    
	    // entry tags
	    $fieldConfig = new DistributionFieldConfig();
	    $fieldConfig->setFieldName(CrossKalturaDistributionField::BASE_ENTRY_TAGS);
	    $fieldConfig->setUserFriendlyFieldName('Tags');
	    $fieldConfig->setEntryMrssXslt('<xsl:for-each select="tags/tag">
                                			<xsl:if test="position() &gt; 1">
                                				<xsl:text>,</xsl:text>
                                			</xsl:if>
                                			<xsl:value-of select="normalize-space(.)" />
                                		</xsl:for-each>');
	    $fieldConfig->setUpdateOnChange(true);
	    $fieldConfig->setUpdateParams(array(entryPeer::TAGS));
	    $fieldConfig->setIsRequired(DistributionFieldRequiredStatus::NOT_REQUIRED);
	    $fieldConfigArray[$fieldConfig->getFieldName()] = $fieldConfig;
	    
	    // entry categories
	    $fieldConfig = new DistributionFieldConfig();
	    $fieldConfig->setFieldName(CrossKalturaDistributionField::BASE_ENTRY_CATEGORIES);
	    $fieldConfig->setUserFriendlyFieldName('Categories');
	    $fieldConfig->setEntryMrssXslt('<xsl:for-each select="category">
                                			<xsl:if test="position() &gt; 1">
                                				<xsl:text>,</xsl:text>
                                			</xsl:if>
                                			<xsl:value-of select="normalize-space(.)" />
                                		</xsl:for-each>');
	    $fieldConfig->setUpdateOnChange(true);
	    $fieldConfig->setUpdateParams(array(entryPeer::CATEGORIES));
	    $fieldConfig->setIsRequired(DistributionFieldRequiredStatus::NOT_REQUIRED);
	    $fieldConfigArray[$fieldConfig->getFieldName()] = $fieldConfig;
	    
	    // entry partner data
	    $fieldConfig = new DistributionFieldConfig();
	    $fieldConfig->setFieldName(CrossKalturaDistributionField::BASE_ENTRY_PARTNER_DATA);
	    $fieldConfig->setUserFriendlyFieldName('Entry Partner Data');
	    $fieldConfig->setEntryMrssXslt('<xsl:value-of select="string(partnerData)" />');
	    $fieldConfig->setUpdateOnChange(true);
	    $fieldConfig->setUpdateParams(array(entryPeer::PARTNER_DATA));
	    $fieldConfig->setIsRequired(DistributionFieldRequiredStatus::NOT_REQUIRED);
	    $fieldConfigArray[$fieldConfig->getFieldName()] = $fieldConfig;
	    
	    // entry start date
	    $fieldConfig = new DistributionFieldConfig();
	    $fieldConfig->setFieldName(CrossKalturaDistributionField::BASE_ENTRY_START_DATE);
	    $fieldConfig->setUserFriendlyFieldName('Distribution sunrise');
	    $fieldConfig->setEntryMrssXslt('<xsl:value-of select="distribution[@entryDistributionId=$entryDistributionId]/sunrise" />');
	    $fieldConfigArray[$fieldConfig->getFieldName()] = $fieldConfig;
	    
	    // entry end date
	    $fieldConfig = new DistributionFieldConfig();
	    $fieldConfig->setFieldName(CrossKalturaDistributionField::BASE_ENTRY_END_DATE);
	    $fieldConfig->setUserFriendlyFieldName('Distribution sunset');
	    $fieldConfig->setEntryMrssXslt('<xsl:value-of select="distribution[@entryDistributionId=$entryDistributionId]/sunset" />');
	    $fieldConfigArray[$fieldConfig->getFieldName()] = $fieldConfig;
	    	    
	    // entry reference id
	    $fieldConfig = new DistributionFieldConfig();
	    $fieldConfig->setFieldName(CrossKalturaDistributionField::BASE_ENTRY_REFERENCE_ID);
	    $fieldConfig->setUserFriendlyFieldName('Reference ID');
	    $fieldConfig->setEntryMrssXslt('<xsl:value-of select="string(referenceID)" />');
	    $fieldConfig->setUpdateOnChange(true);
	    $fieldConfig->setIsRequired(DistributionFieldRequiredStatus::NOT_REQUIRED);
	    $fieldConfigArray[$fieldConfig->getFieldName()] = $fieldConfig;
	    
	    // entry license type
	    $fieldConfig = new DistributionFieldConfig();
	    $fieldConfig->setFieldName(CrossKalturaDistributionField::BASE_ENTRY_LICENSE_TYPE);
	    $fieldConfig->setUserFriendlyFieldName('License type');
	    $fieldConfig->setEntryMrssXslt('<xsl:value-of select="string(licenseType)" />');
	    $fieldConfig->setUpdateOnChange(true);
	    $fieldConfig->setUpdateParams(array(entryPeer::LICENSE_TYPE));
	    $fieldConfig->setIsRequired(DistributionFieldRequiredStatus::NOT_REQUIRED);
	    $fieldConfigArray[$fieldConfig->getFieldName()] = $fieldConfig;
	    
	    return $fieldConfigArray;
	}
}
