<?php
if (!class_exists('KChunkedEncodeSessionManager')) {
require_once "/opt/kaltura/app/batch/client/KalturaTypes.php";
require_once("/opt/kaltura/app/infra/chunkedEncode/KChunkedEncodeUtils.php");
require_once("/opt/kaltura/app/infra/chunkedEncode/KChunkedEncode.php");
require_once("/opt/kaltura/app/infra/chunkedEncode/KChunkedEncodeSessionManager.php");
}
/**
 * @package Scheduler
 * @subpackage Conversion.engines
 */
class KConversionEngineFfmpeg  extends KJobConversionEngine
{
	const FFMPEG = "ffmpeg";
	
	const TAG_VARIANT_A = 'watermark_a';
	const TAG_VARIANT_B = 'watermark_b';
	const TAG_VARIANT_PAIR_ID = 'watermark_pair_';
	const TAG_NGS_STUB = "stub";

	public function getName()
	{
		return self::FFMPEG;
	}
	
	public function getType()
	{
		return KalturaConversionEngineType::FFMPEG;
	}
	
	public function getCmd ()
	{
		return KBatchBase::$taskConfig->params->ffmpegCmd;
	}
	
	/**
	 *
	 */
	protected function getExecutionCommandAndConversionString ( KalturaConvertJobData $data )
	{
		$wmData = null;
		if(isset($data->flavorParamsOutput->watermarkData)){
			$wmData = json_decode($data->flavorParamsOutput->watermarkData);
			if(!isset($wmData)){
				KalturaLog::notice("Bad watermark JSON string($data->flavorParamsOutput->watermarkData), carry on without watermark");
			}
		}
		$subsData = null;
		if(isset($data->flavorParamsOutput->subtitlesData)){
			$subsData = json_decode($data->flavorParamsOutput->subtitlesData);
			if(!isset($subsData)){
				KalturaLog::notice("Bad subtitles JSON string(".$data->flavorParamsOutput->subtitlesData."), carry on without subtitles");
			}
		}
		$cmdLines =  parent::getExecutionCommandAndConversionString ($data);
		KalturaLog::log("cmdLines==>".print_r($cmdLines,1));
			/*
			 * The code below handles the ffmpeg 0.10 and higher option to set up 'forced_key_frame'.
			 * The ffmpeg cmd-line should contain list of all forced kf's, this list might be up to 40Kb for 2hr videos.
			 * Since the cmd-lines are stored in db records (flavor_params_output), it would blow it up.
			 * The solution is to setup a placeholer w/duration and step, the full cmd-line is generated over here
			 * just before the activation.
			 * Sample:
			 *    	__forceKeyframes__462_2
			 *		stands for duration of 462 seconds, gop size 2 seconds
			 */
		foreach($cmdLines as $k=>$cmdLine){
			if(KConversionEngineFfmpegVp8::FFMPEG_VP8==$this->getName()){
				$exec_cmd = self::experimentalFixing($cmdLine->exec_cmd, $data->flavorParamsOutput, $this->getCmd(), $this->inFilePath, $this->outFilePath);
			}
			else $exec_cmd = $cmdLine->exec_cmd;
			$exec_cmd = KDLOperatorFfmpeg::ExpandForcedKeyframesParams($exec_cmd);
			
			if(strstr($exec_cmd, "ffmpeg")==false) {
				$cmdLines[$k]->exec_cmd = $exec_cmd;
				continue;
			}
			
				// impersonite
			KBatchBase::impersonate($data->flavorParamsOutput->partnerId);
			
				/*
				 * Fetch watermark (visible, not forensic ...) 
				 */
			if(isset($wmData)){
				$fixedCmdLine = self::buildWatermarkedCommandLine($wmData, $data->destFileSyncLocalPath, $exec_cmd, 
								KBatchBase::$taskConfig->params->ffmpegCmd, KBatchBase::$taskConfig->params->mediaInfoCmd);
				if(isset($fixedCmdLine)) $exec_cmd = $fixedCmdLine;
			}
			
				/*
				 * Fetch subtitles 
				 */
			if(isset($subsData)){
				$jobMsg = null;
				$fixedCmdLine = self::buildSubtitlesCommandLine($subsData, $data, $exec_cmd, $jobMsg);
				if(isset($jobMsg)) $this->message = $jobMsg;
				if(isset($fixedCmdLine)) $exec_cmd = $fixedCmdLine;
			}
				/*
				 * 'watermark_pair_'/TAG_VARIANT_PAIR_ID tag for NGS digital/forensic signature watermarking flow
				 */
			if(isset($data->flavorParamsOutput->tags) && strstr($data->flavorParamsOutput->tags,KConversionEngineFfmpeg::TAG_VARIANT_PAIR_ID)!=false){
				$fixedCmdLine = self::buildNGSPairedDigitalWatermarkingCommandLine($exec_cmd, $data);
				if(isset($fixedCmdLine)) $exec_cmd = $fixedCmdLine;
			}
				// un-impersonite
			KBatchBase::unimpersonate();
				
			$cmdLines[$k]->exec_cmd = $exec_cmd;
			
		}
		return $cmdLines;
	}
	
	/**
	 *
	 */
	protected function execute_conversion_cmdline($command, &$returnVar)
	{
		KalturaLog::log($command);
		if(isset(KBatchBase::$taskConfig->params->chunkedEncodeScriptPath) && strstr($command,KBatchBase::$taskConfig->params->ffmpegCmd)!==false) {
			$output=$this->execute_chunked_encode($command, $returnVar);
		}
		else {
			$output = system($command, $returnVar);
		}
		KalturaLog::log("rv($returnVar),".print_r($output,1));
		return $output;
	}

	/**
	 *
	 */
	protected function execute_chunked_encode($cmdLine, &$returnVar)
	{
		KalturaLog::log("Original cmdLine:$cmdLine");
			/*
			 * Clean up the cmd line - remove 'ffmpeg' and log file redirection instructions
			 * those will be handled by the Chunked flow
			 */
		{
			$cmdLineAdjusted = str_replace(KBatchBase::$taskConfig->params->ffmpegCmd, KDLCmdlinePlaceholders::BinaryName, $cmdLine);
			$cmdValsArr = explode(' ', $cmdLineAdjusted);
			if(($idx=array_search('>>', $cmdValsArr))!==false){
				$cmdValsArr = array_slice ($cmdValsArr,0,$idx);
			}
			if(($idx=array_search(KDLCmdlinePlaceholders::BinaryName, $cmdValsArr))!==false){
				unset($cmdValsArr[$idx]);
			}
			if(($idx=array_search('&&', $cmdValsArr))!==false){
				$cmdValsArr[$idx] = "ANDAND";
			}

			foreach($cmdValsArr as $idx=>$val){
				$val = trim($val);
				if(!isset($val) || $val==' ' || $val==""){
					unset($cmdValsArr[$idx]);
				}
			}
			$cmdLineAdjusted = implode(" ",$cmdValsArr);
			$cmdLineAdjusted = str_replace(KDLCmdlinePlaceholders::BinaryName, KBatchBase::$taskConfig->params->ffmpegCmd, $cmdLineAdjusted);
			KalturaLog::log("Cleaned up cmdLine:$cmdLineAdjusted");
		}
//		$cmdLineAdjusted = KChunkedEncodeSessionManager::quickFixCmdline($cmdLineAdjusted);
//		KalturaLog::log("Fixed cmdLine:$cmdLineAdjusted");
		
			/*
			 * Initialze the Chunked setup object
			 * Use task::params fields -
			 * - chunkedEncodeMaxConcurrent
			 * - chunkedEncodeMinConcurrent
			 * otherwise defaults will be used.
			 */
		{
			$setup = new KChunkedEncodeSetup();
			$setup->ffmpegBin = KBatchBase::$taskConfig->params->ffmpegCmd;
			$setup->cmd = $cmdLineAdjusted;

			if(isset(KBatchBase::$taskConfig->params->chunkedEncodeMaxConcurrent)){
				$setup->concurrent = KBatchBase::$taskConfig->params->chunkedEncodeMaxConcurrent;
			}
			else {
				$setup->concurrent = KBatchBase::$taskConfig->maxInstances;
			}
			if(isset(KBatchBase::$taskConfig->params->chunkedEncodeMinConcurrent)) {
				$setup->concurrentMin = KBatchBase::$taskConfig->params->chunkedEncodeMinConcurrent;
			}
			$chunkedEncodeScriptParams = " -cleanUp 0";//null; //
			$chunkedEncodeScriptParams.= " -concurrent $setup->concurrent";
			$chunkedEncodeScriptParams.= " -concurrentMin $setup->concurrentMin";
		}

			/*
			 * Initialize the Chunked Encode Session Manager -
			 * if failed ==> fallback to 'normal' ffmpeg transcoding.
			 * The output file should be 'signed' with 'chunkEncodeToken' to allow 
			 * the KChunkedEncodeSessionManager::concurrencyLogic to take it in account, 
			 * along with 'chunked' conversions. Otherwise the hosting server might get overloaded.
			 */
		$runChunkedEncode = new KChunkedEncodeSessionManager($setup);
		if($runChunkedEncode->Initialize()!=true){
			$output = $runChunkedEncode->ExecuteFallback($cmdLine, $returnVar);
			return $output;
		}
		$sessionFilename = $runChunkedEncode->chunker->getSessionName("session");
		
		$chunkedEncodeScriptCmdLine = "php ".KBatchBase::$taskConfig->params->chunkedEncodeScriptPath;
//		$chunkedEncodeScriptCmdLine.= " -sessionFile $sessionFilename >> ".$this->logFilePath." 2>&1";
		$chunkedEncodeScriptCmdLine.= "$chunkedEncodeScriptParams $cmdLineAdjusted >> ".$this->logFilePath." 2>&1";
		KalturaLog::log("Final cmdLine:$chunkedEncodeScriptCmdLine");

		$output = system($chunkedEncodeScriptCmdLine, $returnVar);
		KalturaLog::log("rv($returnVar),".print_r($output,1));
		return $output;
	}
	
	/**
	 * 
	 * @param unknown_type $cmdStr
	 * @param unknown_type $flavorParamsOutput
	 * @param unknown_type $binCmd
	 * @param unknown_type $srcFilePath
	 * @param unknown_type $outFilePath
	 * @return unknown|string
	 */
	public static function experimentalFixing($cmdStr, $flavorParamsOutput, $binCmd, $srcFilePath, $outFilePath)
	{
/*
 * Samples - 
 * Original 
 * ffmpeg -i SOURCE 
 * 	   -c:v libx265 
 * 		-pix_fmt yuv420p -aspect 640:360 -b:v 8000k -s 640x360 -r 30 -g 60 
 * 		-c:a libfdk_aac -b:a 128k -ar 44100 -f mp4 -y OUTPUT
 * 
 * Switched - 
 * ffmpeg -i SOURCE 
 * 		-pix_fmt yuv420p -aspect 640:360 -b:v 8000k -s 640x360 -r 30 -g 60 -f yuv4mpegpipe -an - 
 * 		-vn 
 * 		-c:a libfdk_aac -b:a 128k -ar 44100 -f mp4 -y OUTPUT.aac 
 * 		| /home/dev/x265 - --y4m --scenecut 40 --keyint 60 --min-keyint 1 --bitrate 2000 --qpfile OUTPUT.qp OUTPUT.h265 
 * 		&& ~/ffmpeg-2.4.3 -i OUTPUT.aac -r 30 -i OUTPUT.h265 -c copy -f mp4 -y OUTPUT
 * 
 */

		/*
		 * New binaries/aliases on transcoding servers
		 */
$x265bin = "x265";
$ffmpegExperimBin = "ffmpeg-experim";

		if($flavorParamsOutput->videoCodec==KDLVideoTarget::H265){ //video_codec	!!!flavorParamsOutput->videoCodec
			KalturaLog::log("trying to fix H265 conversion");
			$gop = $flavorParamsOutput->gopSize; 					//gop_size	!!!$flavorParamsOutput->gopSize;
			$vBr = $flavorParamsOutput->videoBitrate; 				//video_bitrate	!!!$flavorParamsOutput->videoBitrate;
			$frameRate = $flavorParamsOutput->frameRate; 			//frame_rate	!!!$flavorParamsOutput->frameRate;
				
$threads = 4;
$pixFmt = "yuv420p";
			$cmdValsArr = explode(' ', $cmdStr);
			
			/*
			 * Rearrange the ffmpeg cmd-line into a complex pipe and multiple command
			 * - ffmpeg transcodes audio into an output.AAC file and decodes video into a raw resized video to be piped
			 * - into x265 that encodes raw output.h265
			 * - upon completion- mux into an out.mp4
			 * 
			 * To Do's
			 * - support other audio
			 * - support other formats
			 * 
			 */
			
				/*
				 * remove video codec
				 */
			if(in_array('-c:v', $cmdValsArr)) {
				$key = array_search('-c:v', $cmdValsArr);
				unset($cmdValsArr[$key+1]);
				unset($cmdValsArr[$key]);
			}
			if(in_array('-threads', $cmdValsArr)) {
				$key = array_search('-threads', $cmdValsArr);
				$threads = $cmdValsArr[$key+1];
			}
				/*
				 * add dual stream generation
				 */
			if(in_array('-c:a', $cmdValsArr)) {
				$key = array_search('-c:a', $cmdValsArr);
				$cmdValsArr[$key] = "-f yuv4mpegpipe -an - -vn -c:a";
			}
				/*
				 * handle pix-format (main vs main10)
				 */
			if(in_array('-pix_fmt', $cmdValsArr)) {
				$key = array_search('-pix_fmt', $cmdValsArr);
				$pixFmt = $cmdValsArr[$key+1];
			}
			switch($pixFmt){
				case "yuv420p10":
				case "yuv422p":
					$profile = "main10";
					break;
				case "yuv420p":
				default:
					$profile = "main";
					break;
			}

				/*
				 * Get source duration
				 */
			$ffParser = new KFFMpegMediaParser($srcFilePath);
			$ffMi = null;
			try {
				$ffMi = $ffParser->getMediaInfo();
			}
			catch(Exception $ex)
			{
				KalturaLog::log(print_r($ex,1));
			}
			if(isset($ffMi->containerDuration) && $ffMi->containerDuration>0)
				$duration = $ffMi->containerDuration/1000;
			else if(isset($ffMi->videoDuration) && $ffMi->videoDuration>0)
				$duration = $ffMi->videoDuration/1000;
			else if(isset($ffMi->audioDuration) && $ffMi->audioDuration>0)
				$duration = $ffMi->audioDuration/1000;
			else
				$duration = 0;
			
			$keyFramesArr = array();
			/*
			 * Generate x265 qpfile with forced key-frames
			 */
			if(isset($gop) && $gop>0 && isset($frameRate) && $frameRate>0 && isset($duration) && $duration>0){
				$gopInSec 	= $gop/round($frameRate);
				$frameDur 	= 1/$frameRate;
				for($kfTime=0,$kfId=0,$kfTimeGop=0;$kfTime<$duration; ){
					$keyFramesArr[] = $kfId;
					$kfId+=$gop;
					$kfTime=$kfId*$frameDur;
					$kfTimeGop+=$gopInSec;
					$kfTimeDelta = $kfTime-$kfTimeGop;
						/*
						 * Check for time derift conditions (for float fps, 29.97/23.947/etc) and fix when required
						 */
					if(abs($kfTimeDelta)>$frameDur){
						$aaa = $kfId;
						if($kfTimeDelta>0)
							$kfId--;
						else
							$kfId++;
					}
				}
				$keyFramesStr = implode(" I\n",$keyFramesArr)." I\n";
				file_put_contents("$outFilePath.qp", $keyFramesStr);
			}
			else {
				KalturaLog::log("Missing gop($gop) or frameRate($frameRate) or duration($duration) - will be generated without fixed keyframes!");
			}

			if(!in_array($outFilePath, $cmdValsArr)) {
				return $cmdStr;
			}
			
			$key = array_search($outFilePath, $cmdValsArr);
			$cmdValsArr[$key] = "$outFilePath.aac |"; 
			$cmdValsArr[$key].= " $x265bin - --profile $profile --y4m --scenecut 40 --min-keyint 1";
			if(isset($gop)) $cmdValsArr[$key].= " --keyint $gop";
			if(isset($vBr)) $cmdValsArr[$key].= " --bitrate $vBr";
			if(count($keyFramesArr)>0) $cmdValsArr[$key].= " --qpfile $outFilePath.qp";
			$cmdValsArr[$key].= " --threads $threads $outFilePath.h265";
			$cmdValsArr[$key].= " && $ffmpegExperimBin -i $outFilePath.aac -r $frameRate -i $outFilePath.h265 -c copy -f mp4 -y $outFilePath";
	
			$cmdStr = implode(" ", $cmdValsArr);
		}
		
		return $cmdStr;
	}
	
	/**
	 * 
	 * @param         $wmData
	 * @param string  $destFileSyncLocalPath
	 * @param string  $cmdLine
	 * @param string  $ffmpegBin
	 * @param string  $mediaInfoBin
	 * @return string
	 */
	public static function buildWatermarkedCommandLine($watermMarkData, $destFileSyncLocalPath, $cmdLine, $ffmpegBin = "ffmpeg", $mediaInfoBin = "mediainfo")
	{
		KalturaLog::log("In:cmdline($cmdLine)");
		if(!isset($mediaInfoBin) || strlen($mediaInfoBin)==0)
			$mediaInfoBin = "mediainfo";

		if(is_array($watermMarkData))
			$watermMarkDataArr = $watermMarkData;
		else
			$watermMarkDataArr = array($watermMarkData);
		$wmImgIdx = 1;
		foreach ($watermMarkDataArr as $wmData){
			KalturaLog::log("Watermark data($mediaInfoBin):\n".print_r($wmData,1));
				/*
			 	 * Retrieve watermark image file,
			 	 * either from image entry or from external url
			 	 * If both set, prefer image entry
			 	 */
			$imageDownloadUrl = null;
			$errStr = null;
			if(isset($wmData->imageEntry)){
				$version = null;
				try {
					$imgEntry = KBatchBase::$kClient->baseEntry->get($wmData->imageEntry, $version);
				}
				catch ( Exception $ex ) {
					$imgEntry = null;
					$errStr = "Exception on retrieval of an image entry($wmData->imageEntry),\nexception:".print_r($ex,1);
				}
				if(isset($imgEntry)){
					KalturaLog::log("Watermark entry: $wmData->imageEntry");
					$imageDownloadUrl = $imgEntry->downloadUrl;
				}
				else if(!isset($errStr)){
					$errStr = "Failed to retrieve an image entry($wmData->imageEntry)";
				}
				if(!isset($imgEntry))
					KalturaLog::notice($errStr);
			}
			
			if(!isset($imageDownloadUrl)){
				if(isset($wmData->url)) {
					$imageDownloadUrl = $wmData->url;
				}
				else {
					KalturaLog::notice("Missing watermark image data, neither via image-entry-id nor via external url.");
					return null;
				}
			}
			
			$wmTmpFilepath = $destFileSyncLocalPath."_$wmImgIdx.wmtmp";
			KalturaLog::log("imageDownloadUrl($imageDownloadUrl), wmTmpFilepath($wmTmpFilepath)");
				/*
				 * Get the watermark image file
				 */
			$curlWrapper = new KCurlWrapper();
			$res = $curlWrapper->exec($imageDownloadUrl, $wmTmpFilepath);
			KalturaLog::debug("Curl results: $res");
			if(!$res || $curlWrapper->getError()) {
				$errDescription = "Error: " . $curlWrapper->getError();
				$curlWrapper->close();
				KalturaLog::notice("Failed to curl the caption file url($imageDownloadUrl). Error ($errDescription)");
				return null;
			}
			$curlWrapper->close();
			
			if(!file_exists($wmTmpFilepath))
			{
				KalturaLog::notice("Error: output file ($wmTmpFilepath) doesn't exist");
				return null;
			}
			KalturaLog::log("Successfully retrieved the watermark image file ($wmTmpFilepath) ");
			
				/*
				 * Query the image file for format and dims
				 */
			$medPrsr = new KMediaInfoMediaParser($wmTmpFilepath, $mediaInfoBin);
			$imageMediaInfo=$medPrsr->getMediaInfo();
			if(!isset($imageMediaInfo)){
				KalturaLog::notice("Failed to retrieve media data from watermark file ($wmTmpFilepath). Carry on without watermark.");
				return null;
			}
			if(isset($imageMediaInfo->containerFormat)) $wmData->format = $imageMediaInfo->containerFormat;
			if(isset($imageMediaInfo->videoHeight)) $wmData->height = $imageMediaInfo->videoHeight;
			if(isset($imageMediaInfo->videoWidth))  {
				if(isset($wmData->fixImageDar) && $wmData->fixImageDar>0){
					$wmData->width = round($imageMediaInfo->videoWidth/$wmData->fixImageDar);
				}
				else {
					$wmData->width = $imageMediaInfo->videoWidth;
				}
			}
			
			if(strstr($wmData->format, "jpeg")!==false || strstr($wmData->format, "jpg")!==false) {
				$wmData->format = "jpg";
			}
			else if(strstr($wmData->format, "png")!==false){
				$wmData->format = "png";
			}
			rename($wmTmpFilepath, "$wmTmpFilepath.$wmData->format");
			$wmTmpFilepath = "$wmTmpFilepath.$wmData->format";

			KalturaLog::log("Updated Watermark data:".json_encode($wmData));

			$cmdLine = KDLOperatorFfmpeg::AdjustCmdlineWithWatermarkData($cmdLine, $wmData, $wmTmpFilepath, $wmImgIdx);
			$wmImgIdx++;
		}
		return $cmdLine;
	}
	
	/**
	 * 
	 */
	protected static function buildNGSPairedDigitalWatermarkingCommandLine($cmdLine, $data)
	{
			/*
			 * Get source mediainfo for NGS prepprocessor params
			 * Use default 'NGS_FragmentPreprocessorYUV' if batch config does not contain 'ngsPreprocessorCmd'
			 */
		if(count($data->srcFileSyncs)>0 && isset($data->srcFileSyncs[0]->assetId)) { 
			$mediaInfoFilter = new KalturaMediaInfoFilter();
			$mediaInfoFilter->flavorAssetIdEqual = $data->srcFileSyncs[0]->assetId;
			try {
				$mediaInfoList = KBatchBase::$kClient->mediaInfo->listAction($mediaInfoFilter);
			}
			catch (Exception $ex) {
				$mediaInfoList = null;
				$errStr = "Exception on retrieval of an mediaInfo List ($mediaInfoFilter->flavorAssetIdEqual),\nexception:".print_r($ex,1);
			}

			if(!(isset($mediaInfoList) && isset($mediaInfoList->objects) && count($mediaInfoList->objects)>0)){
				if(!isset($errStr))
					$errStr = "Bad source media info object";
				KalturaLog::notice($errStr);
				return null;
			}
			
			$mediaInfo = $mediaInfoList->objects[0];
			$ngsBin = isset(KBatchBase::$taskConfig->params->ngsPreprocessorCmd)? KBatchBase::$taskConfig->params->ngsPreprocessorCmd: "NGS_FragmentPreprocessorYUV";
			$srcWid = $mediaInfo->videoWidth;
			$srcHgt = $mediaInfo->videoHeight;
			$srcFps = $mediaInfo->videoFrameRate;
			if(strstr($data->flavorParamsOutput->tags,KConversionEngineFfmpeg::TAG_VARIANT_A)!=false) 
				$prepMode='A';
			else if(strstr($data->flavorParamsOutput->tags,KConversionEngineFfmpeg::TAG_VARIANT_B)!=false)
				$prepMode='APrime';
			else
				return null;
		}

$stub=null;
		if(strstr($data->flavorParamsOutput->tags,KConversionEngineFfmpeg::TAG_NGS_STUB)!=false)
			$stub="--stub";
	
		$digSignStub = "-f rawvideo -pix_fmt yuv420p - | %s -w %d -h %d -f %s %s --%s| %s -f rawvideo -s %dx%d -r %s -i -";
		$digSignStr = sprintf($digSignStub, $ngsBin, $srcWid, $srcHgt, $srcFps, $stub, $prepMode,KDLCmdlinePlaceholders::BinaryName, $srcWid, $srcHgt, $srcFps);
		$cmdLine = KDLOperatorFfmpeg::SplitCommandLineForVideoPiping($cmdLine, $digSignStr);
		KalturaLog::log("After:cmdLine($cmdLine)");
		return $cmdLine;
	}

	/**
	 */
	public static function buildSubtitlesCommandLine($subtitlesData, $data, $cmdLine, &$jobMsg)
	{
		/*
		 * Currently the precessing of action 'render'(burn-in) and 'embed'
		 * is the same.
		 * It will be separated in the future to support embedding of multiple subs languages 
		 * (this option is irrelevant for rendering)
		 */
		KalturaLog::log("subtitlesData:".json_encode($subtitlesData));
		$captionsArr = self::fetchEntryCaptionList($data, $jobMsg);
		if(!isset($captionsArr) || count($captionsArr)==0){
			KalturaLog::log("No captions for that entry!!!");
			$cmdLine=KDLOperatorFfmpeg::RemoveFilter($cmdLine, 'subtitles');
			return $cmdLine;
		}
		$captionFilePath = null;
		foreach($captionsArr as $lang=>$captionFileUrl){
			if($subtitlesData->language==$lang){
				KalturaLog::log("Found required language($lang)");
				$captionFilePath = self::fetchCaptionFile($captionFileUrl, $data->destFileSyncLocalPath.".temp.$lang.srt");
				break;
			}
		}
		if(!isset($captionFilePath)){
			KalturaLog::notice("No captions for ($subtitlesData->language)");
			$cmdLine=KDLOperatorFfmpeg::RemoveFilter($cmdLine, 'subtitles');
			return $cmdLine;
		}
		$cmdLine = str_replace(KDLCmdlinePlaceholders::SubTitlesFileName, $captionFilePath, $cmdLine);

		KalturaLog::log($cmdLine);
		return $cmdLine;
	}

	/**
	 */
	public static function fetchEntryCaptionList($data, $jobMsg)
	{
		KalturaLog::log("asset:$data->flavorAssetId");
		try {
			KBatchBase::$kClient->getConfig()->partnerId = $data->flavorParamsOutput->partnerId;
			
			$flavorAsset = KBatchBase::$kClient->flavorAsset->get($data->flavorAssetId);
			if(!isset($flavorAsset)){
				$jobMsg = "Failed to retrieve the flavor asset object (".$data->flavorAssetId.")";
				KalturaLog::notice("ERROR:".$jobMsg);
				return null;
			}
		KalturaLog::log("entry:$flavorAsset->entryId");
			$filter = new KalturaAssetFilter();
			$filter->entryIdEqual = $flavorAsset->entryId;
			$captionAssetList = KBatchBase::$kClient->captionAsset->listAction($filter, null); 
			if(!isset($captionAssetList) || count($captionAssetList->objects)==0){
				$jobMsg = "No caption assets for entry (".$flavorAsset->entryId.")";
				KalturaLog::notice("ERROR:".$jobMsg);
				return null;
			}
		}
		catch( Exception $ex){
			$jobMsg = "Exception on captions list retrieval  (".print_r($ex,1).")";
			KalturaLog::notice("ERROR:".$jobMsg);
			return null;
		}
		
		KalturaLog::log("Fetching captions (#".count($captionAssetList->objects).")");
		$captionsArr = array();
		foreach($captionAssetList->objects as $captionObj) {
			try{
				$captionsUrl = KBatchBase::$kClient->captionAsset->getUrl($captionObj->id, null);
			}
			catch ( Exception $ex ) {
				$captionsUrl = null;
				KalturaLog::notice("Exception on retrieve caption asset url retrieval (".$captionObj->id."),\nexception:".print_r($ex,1));
			}		
			if(!isset($captionsUrl)){
				KalturaLog::notice("Failed to retrieve caption asset url (".$captionObj->id.")");
				continue;
			}
			$captionsArr[$captionObj->languageCode] = $captionsUrl;
			KalturaLog::log("Caption - lang($captionObj->languageCode), url($captionsUrl)");
		}
		
		if(count($captionsArr)==0) {
			$jobMsg = "No captions for that entry ($flavorAsset->entryId)!!!";
			KalturaLog::log($jobMsg);
			return null;
		}
		
		KalturaLog::log("Fetched:".serialize($captionsArr));
		return $captionsArr;
	}

	/***************************
	 * fetchCaptionFile
	 *
	 * @param $languageCode
	 * @param $destFolder
	 * @return $localCaptionFilePath
	 */
	public static function fetchCaptionFile($captionUrl, $captionFilePath)
	{
		KalturaLog::log("Executing curl to retrieve caption asset file from - $captionUrl");
		$curlWrapper = new KCurlWrapper();
		KalturaLog::log("captionFilePath:$captionFilePath");
		$res = $curlWrapper->exec($captionUrl, $captionFilePath);
		KalturaLog::log("Curl results: $res");
		if(!$res || $curlWrapper->getError()){
			$errDescription = "Error: " . $curlWrapper->getError();
			$curlWrapper->close();
			KalturaLog::notice("Failed to curl the caption file url($captionUrl). Error ($errDescription)");
			return null;
		}
		$curlWrapper->close();
		
		if(!file_exists($captionFilePath)) {
			KalturaLog::notice("Error: output file ($captionFilePath) doesn't exist");
			return null;
		}
		KalturaLog::log("Successfully retrieved $captionFilePath!");
		return $captionFilePath;
	}
}

