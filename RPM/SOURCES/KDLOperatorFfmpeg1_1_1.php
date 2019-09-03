<?php
/**
 * @package plugins.ffmpeg
 * @subpackage lib
 */
class KDLOperatorFfmpeg1_1_1 extends KDLOperatorFfmpeg0_10 {

	/* ---------------------------
	 * generateContainerParams
	 * 
	 */
	protected function generateContainerParams(KDLFlavor $design, KDLFlavor $target)
	{
		if(!isset($target->_container))
			return null;
		
$con = $target->_container;
		switch($con->_id){
	/*
		case KDLContainerTarget::APPLEHTTP:
			$cmdStr = " -hls_list_size 100000 -f hls";
			break;
	 */
		case KDLContainerTarget::ISMV:
		case KDLContainerTarget::ISMA:
				/*
				 * ISMV/SmoothStreaming needs following in order to support adptive-bitrate management
				 * - frag_keyframe - the media control meta data is written for each chunk/packet, 
				 * rather than appeares only at the end/beginning of the file
				 * - min_frag_duration (micro sec) - causes the fragmentation to be alligned cross 
				 * the various assets. Evaluated from gop and fr, if missing set to 2 sec. Relates to KF positioning 
				 */
			if(isset($target->_video) 
			&& (isset($target->_video->_gop) && $target->_video->_gop>0)
			&& (isset($target->_video->_frameRate) && $target->_video->_frameRate>0)){
				$min_frag = round(($target->_video->_gop/$target->_video->_frameRate)*1000000);
			}
			else {
				$min_frag = 20000000;
			}
			$cmdStr = " -movflags +frag_keyframe -min_frag_duration $min_frag -f ismv";
			break;
		default:
			$cmdStr = parent::generateContainerParams($design, $target);
			break;
		}
	/*		
	 * Right now the fastart option don't act properly, the resultant files are not complianr with QTP
		if($target->_container->_id==KDLContainerTarget::MP4){
			$cmdStr.= " -movflags +faststart";
		}
	*/
		return $cmdStr;
	}

	/* ---------------------------
	 * generateAudioParams
	 */
	protected function generateAudioParams(KDLFlavor $design, KDLFlavor $target)
	{
		if(!isset($target->_audio)) {
			return " -an";
		}
	
		$aud = $target->_audio;
		if($aud->_id==KDLAudioTarget::AACHE) {
		
			$cmdStr = " -acodec libfdk_aac -profile:a aac_he_v2";
			if($aud->_bitRate!==null && $aud->_bitRate>0){
				$cmdStr.= " -a:b ".$aud->_bitRate."k";
			}
			if($aud->_sampleRate!==null && $aud->_sampleRate>0){
				$cmdStr.= " -ar ".$aud->_sampleRate;
			}
			if($aud->_channels!==null && $aud->_channels>0){
				$cmdStr.= " -ac ".$aud->_channels;
			}
		
			return $cmdStr;
		}
		$cmdStr = parent::generateAudioParams($design, $target);
		
			/*
			 * Update params to match 'new' ffmpeg syntax
			 */
		$cmdValsArr = explode(' ', $cmdStr);
		if(in_array('-ab', $cmdValsArr)) {
			$key = array_search('-ab', $cmdValsArr);
			$cmdValsArr[$key] = '-b:a';
		}
		
		if(in_array('-acodec', $cmdValsArr)) {
			$key = array_search('-acodec', $cmdValsArr);
			$cmdValsArr[$key] = '-c:a';
		}
		
			/*
			 * Switch old libfaac to much superior FDK_AAC. The params are the same
			 */
		if(in_array('libfaac', $cmdValsArr)) {
			$key = array_search('libfaac', $cmdValsArr);
			$cmdValsArr[$key] = 'aac -strict -2';
		}
		
		$cmdStr = implode(" ", $cmdValsArr);
		
		return $cmdStr;
	}
	
	/* ---------------------------
	 * generateVideoParams
	 */
	protected function generateVideoParams(KDLFlavor $design, KDLFlavor $target)
	{
		$cmdStr = parent::generateVideoParams($design, $target);
		if(!isset($target->_video))
			return $cmdStr;
	
		$vid = $target->_video;
		$cmdValsArr = explode(' ', $cmdStr);
		
			/*
			 * Update params to match 'new' ffmpeg syntax
			 */
		if(in_array('-b', $cmdValsArr)) {
			$key = array_search('-b', $cmdValsArr);
			$cmdValsArr[$key] = '-b:v';
		}
		
		if(in_array('-vcodec', $cmdValsArr)) {
			$key = array_search('-vcodec', $cmdValsArr);
			$cmdValsArr[$key] = '-c:v';
		}
		
		if(isset($vid->_rotation) && $vid->_rotation!=0){
			if($vid->_rotation==270 || $vid->_rotation==-90 || $vid->_rotation==90) {
				if(in_array('-s', $cmdValsArr)) {
					$key = array_search('-s', $cmdValsArr);
					if($vid->_width!=null && $vid->_height!=null){
						$cmdValsArr[$key+1] = $vid->_height.'x'.$vid->_width;
					}
				}
			}
			$cmdValsArr[] = '-metadata:s:v rotate="0"';
		}
		
			/*
			 * Disabling of GOP in order to avoid duplicate KF's running through the whole file
			 * TEMPORARY - it will be done only for WV
			 */
		if(((isset($vid->_forWideVine) &&  $vid->_forWideVine = true) || $vid->_forcedKeyFramesMode==2)
		&& in_array('-force_key_frames', $cmdValsArr) && in_array('-g', $cmdValsArr)) {
			$key = array_search('-g', $cmdValsArr);
			$cmdValsArr[$key+1] = 3600*24; // set GOP to 24 hrs
		}
		
		$cmdStr = implode(" ", $cmdValsArr);

		return $cmdStr;
	}
	
	/* ---------------------------
	 * calcForcedKeyFrames
	 */
	protected function calcForcedKeyFrames($vidObj, KDLFlavor $target)
	{
		/*
		 * On 'follow source KF's' mode
		 */
		if($vidObj->_forcedKeyFramesMode==2) {
			return " -force_key_frames source";
		}
		
		return parent::calcForcedKeyFrames($vidObj, $target);
	}
}
	
