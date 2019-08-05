<?php
/**
 * @package plugins.crossKalturaDistribution
 * @subpackage model.data
 */
class kCrossKalturaDistributionJobProviderData extends kDistributionJobProviderData
{

    /**
     * array of information about distributed flavor assets
     * @var string
     */
    protected $distributedFlavorAssets;
    
    /**
     * array of information about distributed thumb assets
     * @var string
     */
    protected $distributedThumbAssets;
    
    /**
     * array of information about distributed metadata
     * @var string
     */
    protected $distributedMetadata;
    
    /**
     * array of information about distributed caption assets
     * @var string
     */
    protected $distributedCaptionAssets;

    /**
     * array of information about distributed caption assets
     * @var string
     */
    protected $distributedAttachmentAssets;
    
    /**
     * array of information about distributed cue points
     * @var string
     */
    protected $distributedCuePoints;

    /**
     * array of information about distributed thumb cue points
     * @var string
     */
    protected $distributedThumbCuePoints;

    /**
     * array of information about distributed timed thumb assets
     * @var string
     */
    protected $distributedTimedThumbAssets;

	/**
     * @return the $distributedFlavorAssets
     */
    public function getDistributedFlavorAssets ()
    {
        return $this->distributedFlavorAssets;
    }

	/**
     * @param string $distributedFlavorAssets
     */
    public function setDistributedFlavorAssets ($distributedFlavorAssets)
    {
        $this->distributedFlavorAssets = $distributedFlavorAssets;
    }

	/**
     * @return the $distributedThumbAssets
     */
    public function getDistributedThumbAssets ()
    {
        return $this->distributedThumbAssets;
    }

	/**
     * @param string $distributedThumbAssets
     */
    public function setDistributedThumbAssets ($distributedThumbAssets)
    {
        $this->distributedThumbAssets = $distributedThumbAssets;
    }

	/**
     * @return the $distributedMetadata
     */
    public function getDistributedMetadata ()
    {
        return $this->distributedMetadata;
    }

	/**
     * @param string $distributedMetadata
     */
    public function setDistributedMetadata ($distributedMetadata)
    {
        $this->distributedMetadata = $distributedMetadata;
    }

	/**
     * @return the $distributedCaptionAssets
     */
    public function getDistributedCaptionAssets ()
    {
        return $this->distributedCaptionAssets;
    }

	/**
     * @param string $distributedCaptionAssets
     */
    public function setDistributedCaptionAssets ($distributedCaptionAssets)
    {
        $this->distributedCaptionAssets = $distributedCaptionAssets;
    }


	/**
     * @return the $distributedAttachmentAssets
     */
    public function getDistributedAttachmentAssets ()
    {
        return $this->distributedAttachmentAssets;
    }

	/**
     * @param string $distributedAttachmentAssets
     */
    public function setDistributedAttachmentAssets ($distributedAttachmentAssets)
    {
        $this->distributedAttachmentAssets = $distributedAttachmentAssets;
    }

	/**
     * @return the $distributedCuePoints
     */
    public function getDistributedCuePoints ()
    {
        return $this->distributedCuePoints;
    }

	/**
     * @param string $distributedCuePoints
     */
    public function setDistributedCuePoints ($distributedCuePoints)
    {
        $this->distributedCuePoints = $distributedCuePoints;
    }

    /**
     * @return the $distributedCuePoints
     */
    public function getDistributedThumbCuePoints ()
    {
        return $this->distributedThumbCuePoints;
    }

    /**
     * @param string $distributedCuePoints
     */
    public function setDistributedThumbCuePoints ($distributedThumbCuePoints)
    {
        $this->distributedThumbCuePoints = $distributedThumbCuePoints;
    }

    /**
     * @return the $distributedThumbAssets
     */
    public function getDistributedTimedThumbAssets ()
    {
        return $this->distributedTimedThumbAssets;
    }

    /**
     * @param string $distributedThumbAssets
     */
    public function setDistributedTimedThumbAssets ($distributedTimedThumbAssets)
    {
        $this->distributedTimedThumbAssets = $distributedTimedThumbAssets;
    }

}
