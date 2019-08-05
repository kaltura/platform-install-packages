<?php 
/**
 * @package plugins.crossKalturaDistribution
 * @subpackage admin
 */
class Form_CrossKalturaProfileConfiguration extends Form_ConfigurableProfileConfiguration
{
    const ELEMENT_METADATA_XPATHS_THAT_TRIGGER_UPDATE = 'metadata_xpaths_trigger_update';
    const ELEMENT_MAP_ACCESS_CONTROL_IDS = 'json_map_access_control_profile_ids';
    const ELEMENT_MAP_CONVERSION_PROFILE_IDS = 'json_map_conversion_profile_ids';
    const ELEMENT_MAP_METADATA_PROFILE_IDS = 'json_map_metadata_profile_ids';
    const ELEMENT_MAP_STORAGE_PROFILE_IDS = 'json_map_storage_profile_ids';
    const ELEMENT_MAP_FLAVOR_PARAMS_IDS = 'json_map_flavor_params_ids';
    const ELEMENT_MAP_THUMB_PARAMS_IDS = 'json_map_thumb_params_ids';
    const ELEMENT_MAP_CAPTION_PARAMS_IDS = 'json_map_caption_params_ids';
    const ELEMENT_MAP_ATTACHMENT_PARAMS_IDS = 'json_map_attachment_params_ids';
        
    private $metadataProfileFields;
    	
    public function init()
	{
		parent::init();
		$this->setDescription('Cross Kaltura Distribution Profile');
		$this->getView()->addBasePath(realpath(dirname(__FILE__)));
		$this->addDecorator('ViewScript', array(
			'viewScript' => 'cross-kaltura-distribution.phtml',
			'placement' => 'APPEND'
		));
	}
    
	protected function addProviderElements()
	{
        $element = new Zend_Form_Element_Hidden('providerElements');
		$element->setLabel('Cross Kaltura Specific Configuration');
		$element->setDecorators(array('ViewHelper', array('Label', array('placement' => 'append')), array('HtmlTag',  array('tag' => 'b'))));
		
		
		// add elements
		
	    $this->addElement('text', 'target_service_url', array(
			'label'			=> 'Target Service URL:',
			'filters'		=> array('StringTrim'),
			'required'		=> true,
		));
		
	    $this->addElement('text', 'target_account_id', array(
			'label'			=> 'Target Account ID:',
			'filters'		=> array('StringTrim'),
			'required'		=> true,
		));
		
	    $this->addElement('text', 'target_login_id', array(
			'label'			=> 'Target Login ID:',
			'filters'		=> array('StringTrim'),
			'required'		=> true,
		));
		
	    $this->addElement('text', 'target_login_password', array(
			'label'			=> 'Target Login Password:',
			'filters'		=> array('StringTrim'),
			'required'		=> true,
		));
				
	    $this->addElement('textarea', 'metadata_xslt', array(
			'label'			=> 'Metadata XSLT:',
			'filters'		=> array('StringTrim'),
		));

	    	$this->addElement('text', 'designated_categories', array(
			'label'			=> 'Designated Categories:',
			'filters'		=> array('StringTrim'),
		));
	    	$this->addElement('text', 'collaborators_custom_metadata_profile_id', array(
			'label'			=> 'Collaborators custom metadata profile ID:',
			'filters'		=> array('StringTrim'),
		));
		
		$this->addElement('checkbox', 'distribute_remote_flavor_asset_content', array(
			'label'			=> 'Distribute Remote Flavor Asset Content Instead Of Local:',
		));
		
		$this->addElement('checkbox', 'distribute_remote_thumb_asset_content', array(
			'label'			=> 'Distribute Remote Thumb Asset Content Instead Of Local:',
		));
		
		$this->addElement('checkbox', 'distribute_remote_caption_asset_content', array(
			'label'			=> 'Distribute Remote Caption Asset Content Instead Of Local:',
		));
		
		
		$this->addElement('checkbox', 'distribute_captions', array(
			'label'			=> 'Distribute Captions:',
		));
		
		$this->addElement('checkbox', 'distribute_cue_points', array(
			'label'			=> 'Distribute Cue Points:',
		));
		
		$this->addElement('checkbox', 'distribute_categories', array(
			'label'			=> 'Distribute Categories?',
		));
		$this->addElement('checkbox', 'collaborators_from_custom_metadata_profile', array(
			'label'			=> 'Set collaborators based on custom metadata profile?',
		));
		
		// add metadata fields that trigger update
		
	    $metadataFields = $this->getMetadataFields();
		
		if (count($metadataFields))
        {
    		$xpathsElement = new Zend_Form_Element_MultiCheckbox(self::ELEMENT_METADATA_XPATHS_THAT_TRIGGER_UPDATE);
    		$xpathsElement->setLabel('Metadata Fields That Trigger Update:');
    		$xpathsElement->setMultiOptions($this->getMetadataFields());
    		$this->addElement($xpathsElement);
        }
        
        // add source to target mapping tables
		$this->addElement('textarea', self::ELEMENT_MAP_ACCESS_CONTROL_IDS, array(
			'label'			=> 'Access Control Profile IDs map:',
			'filters'		=> array('StringTrim'),
		));
		
		$this->addElement('textarea', self::ELEMENT_MAP_CONVERSION_PROFILE_IDS, array(
			'label'			=> 'Conversion Profile IDs map:',
			'filters'		=> array('StringTrim'),
		));
		
		$this->addElement('textarea', self::ELEMENT_MAP_METADATA_PROFILE_IDS, array(
			'label'			=> 'Metadata Profile IDs map:',
			'filters'		=> array('StringTrim'),
		));
		
		$this->addElement('textarea', self::ELEMENT_MAP_STORAGE_PROFILE_IDS, array(
			'label'			=> 'Storage Profile IDs map:',
			'filters'		=> array('StringTrim'),
		));
		
		$this->addElement('textarea', self::ELEMENT_MAP_FLAVOR_PARAMS_IDS, array(
			'label'			=> 'Flavor Params IDs map:',
			'filters'		=> array('StringTrim'),
		));
		
		$this->addElement('textarea', self::ELEMENT_MAP_THUMB_PARAMS_IDS, array(
			'label'			=> 'Thumb Params IDs map:',
			'filters'		=> array('StringTrim'),
		));
		
		$this->addElement('textarea', self::ELEMENT_MAP_CAPTION_PARAMS_IDS, array(
			'label'			=> 'Caption Params IDs map:',
			'filters'		=> array('StringTrim'),
		));

		$this->addElement('textarea', self::ELEMENT_MAP_ATTACHMENT_PARAMS_IDS, array(
			'label'			=> 'Caption Params IDs map:',
			'filters'		=> array('StringTrim'),
		));
        
        
		// add display groups
		
		$this->addDisplayGroup(
			array('target_service_url', 'target_account_id', 'target_login_id', 'target_login_password'),
			'target_account', 
			array('legend' => 'Target', 'decorators' => array('FormElements', 'Fieldset'))
		);
		
		$this->addDisplayGroup(
			array('distribute_captions', 'distribute_cue_points', 'distribute_remote_flavor_asset_content', 'distribute_remote_thumb_asset_content', 'distribute_remote_caption_asset_content'),
			'distribution_behaviour', 
			array('legend' => 'Distribution Behaviour', 'decorators' => array('FormElements', 'Fieldset'))
		);
		$this->addDisplayGroup(
			array('distribute_categories','designated_categories'),
			'categories_behaviour', 
			array('legend' => 'Categories Behaviour', 'decorators' => array('FormElements', 'Fieldset'))
		);
		
		$this->addDisplayGroup(
			array('collaborators_from_custom_metadata_profile','collaborators_custom_metadata_profile_id'),
			'collaboration_settings', 
			array('legend' => 'Apply collaboration settings', 'decorators' => array('FormElements', 'Fieldset'))
		);
		
		$this->addDisplayGroup(
			array('metadata_xslt', self::ELEMENT_METADATA_XPATHS_THAT_TRIGGER_UPDATE),
			'metadata_modifications', 
			array('legend' => 'Metadata Modifications', 'decorators' => array('FormElements', 'Fieldset'))
		);
		
		$this->addDisplayGroup(
			array(self::ELEMENT_MAP_ACCESS_CONTROL_IDS, self::ELEMENT_MAP_CONVERSION_PROFILE_IDS, self::ELEMENT_MAP_METADATA_PROFILE_IDS,
				  self::ELEMENT_MAP_STORAGE_PROFILE_IDS, self::ELEMENT_MAP_FLAVOR_PARAMS_IDS, self::ELEMENT_MAP_THUMB_PARAMS_IDS, self::ELEMENT_MAP_CAPTION_PARAMS_IDS),
			'object_id_maps', 
			array('legend' => 'Source/Target ID Mapping', 'decorators' => array('FormElements', 'Fieldset'))
		);
		
	}
	
	
    protected function getMetadataFields()
	{
		if(is_array($this->metadataProfileFields))
			return $this->metadataProfileFields;
			
		$this->metadataProfileFields = array();
		
		Infra_ClientHelper::impersonate($this->partnerId);
		$client = Infra_ClientHelper::getClient();
		$metadataPlugin = Kaltura_Client_Metadata_Plugin::get($client);
		
		try
		{
			$metadataProfileFilter = new Kaltura_Client_Metadata_Type_MetadataProfileFilter();
			$metadataProfileFilter->partnerIdEqual = $this->partnerId;
			$metadataProfileList = $metadataPlugin->metadataProfile->listAction($metadataProfileFilter);
			if($metadataProfileList->totalCount)
			{
				$client->startMultiRequest();
				foreach($metadataProfileList->objects as $metadataProfile)
				{
					$metadataFieldList = $metadataPlugin->metadataProfile->listFields($metadataProfile->id);
				}
				$results = $client->doMultiRequest();
				foreach($results as $metadataFieldList)
				{
					foreach($metadataFieldList->objects as $metadataField)
						$this->metadataProfileFields[$metadataField->xPath] = $metadataField->label;
				}
			}
		}
		catch (Exception $e)
		{
			Infra_ClientHelper::unimpersonate();
			throw $e;
		}
		
		Infra_ClientHelper::unimpersonate();

		return $this->metadataProfileFields;
	}
	
	
	
    public function getObject($objectType, array $properties, $add_underscore = true, $include_empty_fields = false)
	{
		/* @var $object Kaltura_Client_CrossKalturaDistribution_Type_CrossKalturaDistributionProfile */
		$object = parent::getObject($objectType, $properties, $add_underscore, true);
        
		// transform the regular metadataXpathsTriggerUpdate array to a KalturaStringValueArray
		$xpathsKalturaArray = array();
		$uniqXpaths = is_array($object->metadataXpathsTriggerUpdate) ? array_unique($object->metadataXpathsTriggerUpdate) : array();
		foreach ($uniqXpaths as $xpath)
		{
		    $xpathStringValue = new Kaltura_Client_Type_StringValue();
		    $xpathStringValue->value = $xpath;
		    $xpathsKalturaArray[] = $xpathStringValue;
		}
		$object->metadataXpathsTriggerUpdate = $xpathsKalturaArray;

		// transform source/target map fields
		$object->mapAccessControlProfileIds = isset($properties[self::ELEMENT_MAP_ACCESS_CONTROL_IDS]) ? json_decode($properties[self::ELEMENT_MAP_ACCESS_CONTROL_IDS], true) : array();
		$object->mapConversionProfileIds = isset($properties[self::ELEMENT_MAP_CONVERSION_PROFILE_IDS]) ? json_decode($properties[self::ELEMENT_MAP_CONVERSION_PROFILE_IDS], true) : array();
		$object->mapMetadataProfileIds = isset($properties[self::ELEMENT_MAP_METADATA_PROFILE_IDS]) ? json_decode($properties[self::ELEMENT_MAP_METADATA_PROFILE_IDS], true) : array();
		$object->mapStorageProfileIds = isset($properties[self::ELEMENT_MAP_STORAGE_PROFILE_IDS]) ? json_decode($properties[self::ELEMENT_MAP_STORAGE_PROFILE_IDS], true) : array();
		$object->mapFlavorParamsIds = isset($properties[self::ELEMENT_MAP_FLAVOR_PARAMS_IDS]) ? json_decode($properties[self::ELEMENT_MAP_FLAVOR_PARAMS_IDS], true) : array();
		$object->mapThumbParamsIds = isset($properties[self::ELEMENT_MAP_THUMB_PARAMS_IDS]) ? json_decode($properties[self::ELEMENT_MAP_THUMB_PARAMS_IDS], true) : array();
		$object->mapCaptionParamsIds = isset($properties[self::ELEMENT_MAP_CAPTION_PARAMS_IDS]) ? json_decode($properties[self::ELEMENT_MAP_CAPTION_PARAMS_IDS], true) : array();
		$object->mapAttachmentParamsIds = isset($properties[self::ELEMENT_MAP_ATTACHMENT_PARAMS_IDS]) ? json_decode($properties[self::ELEMENT_MAP_ATTACHMENT_PARAMS_IDS], true) : array();
		
		return $object;
	}
	
	public function populateFromObject($object, $add_underscore = true)
	{
        /* @var Kaltura_Client_CrossKalturaDistribution_Type_CrossKalturaDistributionProfile $object */
		parent::populateFromObject($object, $add_underscore);
		
		// transform the KalturaStringValue array to a normal array
		$xpathsArray = array();
		foreach ($object->metadataXpathsTriggerUpdate as $xpathStringValue)
		{
		    $xpathsArray[] = $xpathStringValue->value;
		}
		$this->setDefault(self::ELEMENT_METADATA_XPATHS_THAT_TRIGGER_UPDATE, array_unique($xpathsArray));		
		
		// transform source/target map fields
		$this->setDefault(self::ELEMENT_MAP_ACCESS_CONTROL_IDS, json_encode($object->mapAccessControlProfileIds));
		$this->setDefault(self::ELEMENT_MAP_CONVERSION_PROFILE_IDS, json_encode($object->mapConversionProfileIds));
		$this->setDefault(self::ELEMENT_MAP_METADATA_PROFILE_IDS, json_encode($object->mapMetadataProfileIds));
		$this->setDefault(self::ELEMENT_MAP_STORAGE_PROFILE_IDS, json_encode($object->mapStorageProfileIds));
		$this->setDefault(self::ELEMENT_MAP_FLAVOR_PARAMS_IDS, json_encode($object->mapFlavorParamsIds));
		$this->setDefault(self::ELEMENT_MAP_THUMB_PARAMS_IDS, json_encode($object->mapThumbParamsIds));
		$this->setDefault(self::ELEMENT_MAP_CAPTION_PARAMS_IDS, json_encode($object->mapCaptionParamsIds));
		$this->setDefault(self::ELEMENT_MAP_ATTACHMENT_PARAMS_IDS, json_encode($object->mapAttachmentParamsIds));
	}
	
		
}
