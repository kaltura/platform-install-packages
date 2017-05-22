<?php

 /*****************************
 * Includes & Globals
 */
//ini_set("memory_limit","2048M");

	/********************
	 * Session exit statuses
	 */
	class KChunkedEncodeReturnStatus {
		const OK = 0;
		const InitializeError = 1000;
		const GenerateVideoError = 1001;
		const GenerateAudioError = 1002;
		const FixDriftError = 1003;
		const AnalyzeError = 1004;
		const MergeError = 1005;
		const MergeAttemptsError = 1006;
		const MergeThreshError = 1007;
	}
	
	/********************
	 * Chunked Encoding Session Manager module
	 */
	class KChunkedEncodeSessionManager {
		
		public $chunker = null;
		
		public $chunkExecutionDataArr = array();
		public $processArr = array();	// Chunk process ids array
		public $audioProcess = null;	// Audio porcess id

		public $returnStatus = null;	// KChunkedEncodeReturnStatus
		public $returnMessages = array();
		
		public $startedAt = null;
		public $funishedAt = null;
		
		public $dry = 0;				// 'Dry'/test runs - 0:'wet' run, 1:skip vid/aud encoding,just concat&merge, 2:same as 1, but regenerate stats

		/********************
		 *
		 */
		public function __construct(KChunkedEncodeSetup $setup)
		{
			$this->chunker = new KChunkedEncode($setup);
			KalturaLog::log(date("Y-m-d H:i:s"));
			KalturaLog::log("sessionData:".print_r($this,1));
		}
		
		/********************
		 *
		 */
		public static function LoadFromCmdLineArgs(array $argv)
		{
			$setup = new KChunkedEncodeSetup();
			self::parseArgsToSetup($argv,$setup);

				/*
				 * Otherwise - start Chunked Encode session
				 */
			$sessionManager = new KChunkedEncodeSessionManager($setup);
			if(isset($setup->dry)){
				$sessionManager->dry = $setup->dry;
				unset($setup->dry);
			}
			return $sessionManager;
		}
		
		/********************
		 * 
		 */
		public static function LoadFromSessionFile($sessionFilename)
		{
			if(file_exists($sessionFilename)!=true){
				return null;
			}
			$sessionData =  unserialize(file_get_contents($sessionFilename));
			KalturaLog::log("sessionData:".print_r($sessionData,1));
			$setup = new KChunkedEncodeSetup();
			$sessionManager = new KChunkedEncodeSessionManager($setup);
			$fldsArr = get_object_vars($sessionData);
			foreach($fldsArr as $fld=>$val){
				$sessionManager->$fld = $val;
			}
			return $sessionManager;
		}
		
		/********************
		 * Initialize the chunked encode session
		 */
		public function Initialize()
		{
			$this->startedAt = date_create();
			
			$mergedFilenameSession = $this->chunker->getSessionName("session");
			if((isset($this->chunker->setup->restore) && $this->chunker->setup->restore==1) 
			&& file_exists($mergedFilenameSession)==true){
				$sessionData =  unserialize(file_get_contents($mergedFilenameSession));
				$fldsArr = get_object_vars($sessionData);
				foreach($fldsArr as $fld=>$val){
					$this->$fld = $val;
				}

				KalturaLog::log("sessionData:".print_r($this,1));
				KalturaLog::log("duration(".$this->chunker->params->duration."), frameDuration(".$this->chunker->params->frameDuration.")\n");
				return true;
			}

			$rv = $this->chunker->Initialize();
			if($rv!=true){
				$this->SerializeSession();
				$this->returnStatus = KChunkedEncodeReturnStatus::InitializeError;
				return $rv;
			}
			
			if(!isset($this->chunker->setup->commandExecitionScript)) {
				$this->chunker->setup->commandExecitionScript = $this->chunker->setup->output."execitionScript.sh";
				file_put_contents($this->chunker->setup->commandExecitionScript, 'echo $@'."\n".'echo $1'."\n".'eval "$1"'."\n"."echo exit_code:".'$?');
				chmod($this->chunker->setup->commandExecitionScript,0755);
				sleep(2);
			}
			$this->SerializeSession();
			return $rv;
		}
		
		/********************
		 *
		 */
		public function Generate()
		{
			if($this->GenerateAudioStart()!=true){
				return false;
			}
			
			if($this->GenerateVideo()!=true){
				return false;
			}

			if($this->GenerateAudioFinish()!=true){
				return false;
			}

			if($this->Analyze()!=true){
				return false;
			}
			
			if($this->Merge()!=true){
				return false;
			}
			
			if(isset($this->chunker->setup->cleanUp) && $this->chunker->setup->cleanUp){
				$this->CleanUp();
			}
			
			$this->returnStatus = KChunkedEncodeReturnStatus::OK;
			
			return true;
		}
		
		/********************
		 *
		 */
		public function GenerateVideo()
		{
			while(1)	{
				if($this->IsFinished()) {
					break;
				}
				if($this->GenerateVideoChunk()!=true) {
					return false;
				}
			}
			$rv = $this->GenerateVideoFinish();
			if($rv!=true) 
				return $rv;
			$this->SerializeSession();
			return true;
		}
		
		/********************
		 *
		 */
		public function IsFinished()
		{
			return ($this->chunker->chunkDataIdx>=count($this->chunker->chunkDataArr));
		}
		
		/********************
		 * Analyze and fix chunks
		 */
		public function Analyze()
		{
			$setup = $this->chunker->setup;

			$toFixCnt = $this->chunker->CheckChunksContinuity();
			if($toFixCnt==0) 
				return true;
				
			$processArr = array();
			foreach($this->chunker->chunkDataArr as $badChunkIdx=>$chunkData){
				if(!isset($chunkData->toFix) || $chunkData->toFix==0)
					continue;

				$chunkFixName = $this->chunker->getChunkName($badChunkIdx, "fix");
				$cmdLine = $this->chunker->BuildFixVideoCommandLine($badChunkIdx);
				$process = self::executeCmdline($cmdLine, 0, "$chunkFixName.log", $setup->commandExecitionScript);
				if($process==false){
					KalturaLog::log($msgStr="Chunk ($chunkFixName) fix FAILED !");
					$this->returnMessages[] = $msgStr;
					$this->returnStatus = KChunkedEncodeReturnStatus::AnalyzeError;
					return false;
				}
				$processArr[$badChunkIdx] = $process;

			}
			KalturaLog::log("waiting ...");
			foreach($processArr as $idx=>$process) {
				self::waitForCompletion($process);
				$chunkFixName = $this->chunker->getChunkName($idx, "fix");
				$execData = new KProcessExecutionData($process, $chunkFixName.".log");
				if($execData->exitCode!=0) {
					KalturaLog::log($msgStr="Chunk ($idx) fix FAILED, exitCode($execData->exitCode)!");
					$this->returnMessages[] = $msgStr;
					$this->returnStatus = KChunkedEncodeReturnStatus::AnalyzeError;
					return false;
				}
			}
			return true;
		}
		
		/********************
		 *
		 */
		public function GenerateVideoChunk() 
		{
			list($start,$chunkIdx) = $this->GetNext();
			if(!isset($start))
				return true;
				
			KalturaLog::log("chunk $chunkIdx:".date("Y-m-d H:i:s"));
			$rv = $this->startVideoChunkConvert($start, $chunkIdx);
			if($rv==false) {
				KalturaLog::log($msgStr="Failed to convert chunk $chunkIdx!");
				$this->returnMessages[] = $msgStr;
				$this->returnStatus = KChunkedEncodeReturnStatus::GenerateVideoError;
				return false;
			}

			$rv = $this->waitForChunksCompletion();
			if($rv==false){
				KalturaLog::log($msgStr="Failed to convert chunks 1(".serialize($this->processArr).")!");
				$this->returnMessages[] = $msgStr;
				$this->returnStatus = KChunkedEncodeReturnStatus::GenerateVideoError;
				return false;
			}
			$this->SerializeSession();

			return true;
		}

		/********************
		 *
		 */
		public function GenerateVideoFinish() 
		{
			KalturaLog::log("Inside");
			if(count($this->processArr)!=0) {
				$rv = $this->waitForChunksCompletion();
				if($rv==false){
					KalturaLog::log($msgStr="Failed to convert chunks 2(".serialize($this->processArr).")!");
					$this->returnMessages[] = $msgStr;
					$this->returnStatus = KChunkedEncodeReturnStatus::GenerateVideoError;
					return false;
				}
			}
			$this->getChunkArrFileStatData(0);
			
			$this->SerializeSession();
			
			return true;

		}
		
		/********************
		 *
		 */
		public function GenerateAudioStart() 
		{
			/*
			 * Generate audio stream
			 */
			if(isset($this->audioProcess)) {
				$mergedFilenameAudio = $this->chunker->getSessionName("audio");
				if($this->audioProcess!=0 && file_exists("$mergedFilenameAudio.rv")) {
					$rv = file_get_contents("$mergedFilenameAudio.rv");
				}
			}
			else
				$rv = 1;
			if($rv) {
				$this->audioProcess = $this->generateAudioStream();
				if($this->audioProcess==false) {
					KalturaLog::log($msgStr="Audio convert: FAILED!");
					$this->returnMessages[] = $msgStr;
					$this->returnStatus = KChunkedEncodeReturnStatus::GenerateAudioError;
					return false;
				}
			}
			return true;
		}
		
		/********************
		 *
		 */
		public function GenerateAudioFinish() 
		{
			if(!(isset($this->audioProcess) && $this->audioProcess!=0))
				return true;

			KalturaLog::log("Audio convert: waiting ...");
			$mergedFilenameAudio = $this->chunker->getSessionName("audio");
			self::waitForCompletion($this->audioProcess);
			$execData = new KProcessExecutionData($this->audioProcess, $mergedFilenameAudio.".log");
			if($execData->exitCode!=0) {
				KalturaLog::log($msgStr="Audio convert: FAILED, exitCode($execData->exitCode)!");
				$this->returnMessages[] = $msgStr;
				$this->returnStatus = KChunkedEncodeReturnStatus::GenerateAudioError;
				return false;
			}
			$this->audioProcess = 0;
			KalturaLog::log("Audio convert: OK!");
			
			$this->SerializeSession();
			
			return true;
		}
		
		/********************
		 *
		 */
		public function Merge()
		{
			$setup = $this->chunker->setup;

			$concatFilenameLog = $this->chunker->getSessionName("concat");

			$mergeCmd = $this->chunker->BuildMergeCommandLine();

			if($this->dry<4) {
				$maxAttempts = 3;
				for($attempt=0; $attempt<$maxAttempts; $attempt++) {

					$process = self::executeCmdline($mergeCmd, 0, $concatFilenameLog, $setup->commandExecitionScript);
					if($process==false) {
						KalturaLog::log("FAILED to merge (attempt:$attempt)!");
						sleep(5);
						continue;
					}
					KalturaLog::log("waiting ...");
					self::waitForCompletion($process);
					$execData = new KProcessExecutionData($process, $concatFilenameLog);
					if($execData->exitCode!=0) {
						KalturaLog::log("FAILED to merge (attempt:$attempt, exitCode:$execData->exitCode)!");
						sleep(5);
						continue;
					}
					break;
				}
				if($attempt==$maxAttempts){
					KalturaLog::log($msgStr="FAILED to merge, leaving!");
					$this->returnMessages[] = $msgStr;
					$this->returnStatus = KChunkedEncodeReturnStatus::MergeAttemptsError;
					return false;
				}
			}
			if($this->chunker->ValidateMergedFile($msgStr)!=true){
				$this->returnMessages[] = $msgStr;
				$this->returnStatus = KChunkedEncodeReturnStatus::MergeThreshError;
				return false;
			}
			return true;
		}
		
		/********************
		 *
		 */
		public function CleanUp()
		{
			$setup = $this->chunker->setup;
			foreach($this->chunker->chunkDataArr as $idx=>$chunkData){
				$chunkName_wc = $this->chunker->getChunkName($idx,"*");
				$cmd = "rm -f $chunkName_wc";
				KalturaLog::log("cleanup cmd:$cmd");
				$rv = null; $op = null;
				$output = exec($cmd, $op, $rv);
			}
			$mergedFilenameAudio = $this->chunker->getSessionName("audio");
			$cmd = "rm -f $mergedFilenameAudio* ".$concatFilenameLog = $this->chunker->getSessionName("concat");
			KalturaLog::log("cleanup cmd:$cmd");
			$rv = null; $op = null;
			$output = exec($cmd, $op, $rv);
			return;
			$cmd = "rm -f $setup->output*.$this->videoChunkPostfix*";
			$cmd.= " ".$this->chunker->getSessionName("audio")."*";
			$cmd.= " ".$this->chunker->getSessionName("session");
			KalturaLog::log("cleanup cmd:$cmd");
			$rv = null; $op = null;
			$output = exec($cmd, $op, $rv);
		}
		
		/********************
		 *
		 */
		public function GetNext()
		{
			return $this->chunker->GetNext();
		}
		
		/********************
		 * Evaluate the ad-hock concurrency level
		 * - Check whether there are active jobs (linux) that do not belong to the current session,
		 * - Evaluate how many other sessions are running.
		 * - Set the next concurrency level to match the max-concurrency and number of running sessions
		 */
		protected function evaluateConcurrency()
		{
// ps -ef | grep "ffmpeg.*chunkenc" | grep -v 'reference\|sh \|php\|grep\|audio' | '
// Previous - 
// ps -ef | grep ffmpeg | grep -v "sh \|grep\|"/web2/content/shared/tmp/qualityTest/TestBench.9/conversions/Dec24/1_snny9faa_400_1_b79i4vhn_29.97fps | grep chunkenc | awk 'NF>1{print $NF}'
			$setup = $this->chunker->setup;

				/*
				 * Filter in - ffmpeg & chunkenc
				 */
			$cmdLine = "ps -ef | grep \"$setup->ffmpegBin.*".$this->chunker->chunkEncodeToken."\"";
				/*
				 * Filter out - reference & sh & php & grep & audio & current-session-name
				 */
			$cmdLine.= "| grep -v 'reference\|sh \|php\|grep\|audio\|time'";

			$lastLine=exec($cmdLine , $outputArr, $rv);
			if($rv!=0) {
				KalturaLog::log("No other chunk sessions (rv:$rv).");
			}
			$chunkedSesssionsArr = array();
			$fallbackSesssionsArr = array();
			$thisChunks = 0;
			foreach($outputArr as $idx=>$line) {
				$line = trim($line);
				if(strlen($line)==0)
					continue;
				$lineArr = explode(' ', $line);
				if(count($lineArr)==0)
					continue;
				if(($key=array_search('-pass', $lineArr))!==false && $lineArr[$key+1]==1) {
					if(($key=array_search('-passlogfile', $lineArr))!==false) {
						$fileName = basename($lineArr[$key+1]);
					}
				}
				else
					$fileName = basename(end($lineArr));
				if(($sessionName=strstr($fileName,"_".$this->chunker->chunkEncodeToken, true))===false)
					continue;
				if(strstr($fileName,"_fallback")===false){
					if(key_exists($sessionName,$chunkedSesssionsArr))
						$chunkedSesssionsArr[$sessionName] = $chunkedSesssionsArr[$sessionName]+1;
					else 
						$chunkedSesssionsArr[$sessionName] = 1;
					if(strstr($setup->output,$sessionName)!==false)
						$thisChunks++;
				}
				else {
					if(key_exists($sessionName,$fallbackSesssionsArr))
						$fallbackSesssionsArr[$sessionName] = $fallbackSesssionsArr[$sessionName]+1;
					else 
						$fallbackSesssionsArr[$sessionName] = 1;
				}
			}
			$allChunks = array_sum($chunkedSesssionsArr);
			$chunkedSesssionsCnt = count($chunkedSesssionsArr);
			$fallbackSesssionsCnt = count($fallbackSesssionsArr);
			if($thisChunks==0)
				$chunkedSesssionsCnt+= 1;
			$toSet = round(($setup->concurrent-$fallbackSesssionsCnt)/$chunkedSesssionsCnt);
			if(($allChunks-$thisChunks)+$toSet>$setup->concurrent)
				$toSet = $setup->concurrent - ($allChunks-$thisChunks);
			if($toSet<$setup->concurrentMin)
				$toSet = $setup->concurrentMin;
			KalturaLog::log("maxConcurrent($toSet),sessions($chunkedSesssionsCnt),chunks($allChunks),this($thisChunks),fallbacks($fallbackSesssionsCnt),".serialize($chunkedSesssionsArr));

			return $toSet;
		}

		/********************
		 * 
		 */
		public function ExecuteFallback($cmdLine, &$returnVar)
		{
			$outputName = $this->chunker->params->output;
			$tmpOutputName = $outputName."_".$this->chunker->chunkEncodeToken."_fallback";
			$cmdLineAdjusted = str_replace ($outputName, $tmpOutputName, $cmdLine);
			KalturaLog::log("Cannot run chunked, fallback to normal - cmdLine($cmdLineAdjusted)");

			$output = system($cmdLineAdjusted, $returnVar);
			if(file_exists($tmpOutputName)) {
				copy($tmpOutputName, $outputName);
			}
			return $output;
		}
		
		/********************
		 * rv - bool
		 */
		protected function waitForChunksCompletion($sleepTime=2)
		{
			if($this->dry>0)
				return true;
			$runningArr = array();
			$processCnt = 0;

			$runningArr = $this->getRunningArray($processCnt);

			$this->processArr = $runningArr;
			$runningCnt = count($runningArr);
			while(1) {
				if($processCnt<count($this->chunker->chunkDataArr)) {
					$concurrent = $this->evaluateConcurrency();
					if($runningCnt<$concurrent) {
						KalturaLog::log("Available(".($concurrent-$runningCnt).") processing slots (runningCnt:$runningCnt, maxConcurrent:$concurrent)");
						break;
					}
				}
				if($this->monitorFinished($runningArr)!=true){
					return false;
				}

				$runningCnt = count($runningArr);
					// If none of the processes got finished and there are still running process - sleep for a while ...
					// otherwise - get out to run a new chunk;
				if($runningCnt==0) {
					KalturaLog::log("Finished - No running processes!!");
					break;
				}
				KalturaLog::log("Running($runningCnt):".implode(',',$runningArr));
				if($this->getChunkArrFileStatData()==0)
					sleep($sleepTime);
			}
			KalturaLog::log("Running($runningCnt):".implode(',',$runningArr));
			$this->processArr = $runningArr;
			return true;
		}

		/********************
		 *
		 */
		public static function waitForCompletion($process, $sleepTime=2)
		{
			KalturaLog::log("process($process), sleepTime($sleepTime)");
			while(1) {
				if($process=="Dry_Mode") {
					break;
				}
				if(self::isProcessRunning($process)==false){
					break;
				}
				sleep($sleepTime);
			}
			KalturaLog::log("process($process)==>finished");
		}

		/********************
		 *
		 */
		protected function monitorFinished(&$runningArr)
		{
			foreach($runningArr as $idx=>$process) {
				if(self::isProcessRunning($process)==true){
					continue;
				}
				
				$executionData = $this->chunkExecutionDataArr[$idx];
				if($process=="Dry_Mode") {
					$executionData->exitCode =  0;
				}
				else {
					$logFileName = $this->chunker->getChunkName($idx,".log");
					$executionData->parseLogFile($logFileName);
					KalturaLog::log(print_r($executionData,1));
				}
				unset($runningArr[$idx]);
				if($executionData->exitCode!=0) {
					KalturaLog::log("Failed to convert chunk($idx),process($process)==>exitCode($executionData->exitCode)!");
					$this->processArr = $runningArr;
					return false;
				}
				KalturaLog::log("chunk($idx),process($process)==>exitCode($executionData->exitCode)");
				break;
			}
			return true;
		}

		/********************
		 *
		 */
		protected static function isProcessRunning($process)
		{
			if(file_exists( "/proc/$process" )){
				return true;
			}
			return false;
		}
		
		/********************
		 *
		 */
		protected static function executeCmdline($cmdLine, $dry, $logFile, $executionScript=null)
		{

			if($dry>0) {
				KalturaLog::log("cmdLine:\n$cmdLine\n");
				return "Dry_Mode";
			}
			
//			$cmdLine = "$executionScript \"time $cmdLine\" -rvFile $rvFile >> $logFile 2>&1 & echo $!";
//			$cmdLine = "$executionScript \"time ./ffmpeg_wrapper.sh $cmdLine\" -rvFile $rvFile >> $logFile 2>&1 & echo $!";q
//			$cmdLine = "nohup ./ffmpeg_wrapper.sh time $cmdLine >> $logFile 2>&1 & echo $! ";
			$cmdLine = str_replace("&& ", "&& time ", $cmdLine);
			$cmdLine = "$executionScript \"time $cmdLine \" >> $logFile 2>&1 & echo $! ";
			$started = date_create();
			file_put_contents($logFile, "Started:".$started->format('Y-m-d H:i:s')."\n");
			KalturaLog::log("cmdLine:\n$cmdLine\n");

			$rv = 0;
			$op = null;
			exec($cmdLine,$op,$rv);
			if($rv!=0) {
				return false;
			}
			$pid = implode("\n",$op);
			KalturaLog::log("pid($pid), rv($rv)");
			return $pid;
		}

		/********************
		 * rv  - PID, 0(dry), -1(error)
		 */
		protected function startVideoChunkConvert($start, $chunkIdx)
		{
			$chunkFilename = $this->chunker->getChunkName($chunkIdx,"base");
			KalturaLog::log("start($start), chunkIdx($chunkIdx), chunkFilename($chunkFilename) :".date("Y-m-d H:i:s"));

			$cmdLine = $this->chunker->BuildVideoCommandLine($start, $chunkIdx);

			$process = self::executeCmdline($cmdLine, $this->dry, "$chunkFilename.log", $this->chunker->setup->commandExecitionScript);
			$execData = new KProcessExecutionData($process);
			$this->chunkExecutionDataArr[$chunkIdx] = $execData;
			if($process==false) {
				KalturaLog::log("Failed to convert chunk $chunkIdx!");
				return false;
			}

			$this->processArr[$chunkIdx] = $process;
			
			return true;
		}

		/********************
		 * rv  - PID, 0(dry), -1(error), null(no audio)
		 */
		protected function generateAudioStream()
		{
			KalturaLog::log(date("Y-m-d H:i:s"));
			$cmdLine = $this->chunker->BuildAudioCommandLine();
			if(!isset($cmdLine))
				return null;

			$mergedFilenameAudio = $this->chunker->getSessionName("audio");
			$createAudioFile = file_exists($mergedFilenameAudio)? $this->dry: 0;
			$process = self::executeCmdline($cmdLine, $createAudioFile, "$mergedFilenameAudio.log", $this->chunker->setup->commandExecitionScript);
			KalturaLog::log("pid:".print_r($process,1));
			return $process;
		}

		/********************
		 *
		 */
		protected function getChunkArrFileStatData($maxCnt=4)
		{
			if($maxCnt==0) $maxCnt = PHP_INT_MAX;
			$cnt = 0;
			foreach($this->chunker->chunkDataArr as $idx=>$chunkData){
				if(key_exists($idx,$this->chunkExecutionDataArr)) {
					$execData = $this->chunkExecutionDataArr[$idx];
					if((isset($execData->exitCode) && $execData->exitCode==0 && !isset($chunkData->stat))
					|| $this->dry==2){
						$this->updateChunkFileStatData($idx);
						if(++$cnt>=$maxCnt) break;
					}
				}
			}
			return($cnt);
		}
		
		/********************
		 * updateChunkFileStatData
		 *	
		 */
		protected function updateChunkFileStatData($idx)
		{
			$chunkFileName = $this->chunker->getChunkName($idx);
			$dry = $this->dry;
			
			$statFileName = "$chunkFileName.stat";
			if($dry==1 && file_exists($statFileName)){
				$jsonStr = file_get_contents($statFileName);
				$stat = json_decode($jsonStr);
				return $stat;
			}

			$stat = $this->chunker->updateChunkFileStatData($idx); 
			$jsonStr = json_encode($stat);
			if($dry>0 || !file_exists($statFileName)){
				file_put_contents($statFileName, $jsonStr);
			}
			return $stat;
		}

		/********************
		 *
		 */
		public static function quickFixCmdline($cmdLine)
		{
			$cmdLineArr = explode(" ",$cmdLine);
			
			$toFixArr = array("-force_key_frames","-filter_complex","-rc_eq");
			foreach($toFixArr as $param){
				if(($key=array_search($param, $cmdLineArr))!==false){
					if(strstr($cmdLineArr[$key+1], "'")===false) {
						$cmdLineArr[$key+1] = "'".$cmdLineArr[$key+1]."'";
					}
				}
			}
			$cmdLine = implode(" ", $cmdLineArr);
			return $cmdLine;
		}
		
		/********************
		 *
		 */
		protected function getRunningArray(&$processCnt)
		{
			$runningArr = array();
			foreach($this->chunkExecutionDataArr as $idx=>$execData) {
				if(isset($execData->process)){
					if(!isset($execData->exitCode))
						$runningArr[$idx] = $execData->process;
					$processCnt++;
				}
			}
			return $runningArr;
		}
		
		/********************
		 *
		 */
		public function Report()
		{
			$this->finishedAt = date_create();
			$sessionData = $this;
			$chunker = $this->chunker;
			KalturaLog::log("sessionData:".print_r($sessionData,1));
			  // messages for logs
			$frmCnt = 0;
			$genChkDur = 0;
			{
				foreach($chunker->chunkDataArr as $chunkData){
					if(isset($stat)){
						$frmCnt+= $stat->cnt;
						$genChkDur+= $stat->dur;
					}
				}
			}
			$msgStr = "Merged:generated(frames:$frmCnt,dur:$genChkDur)";
			$durStr = null;
			$fileDtMrg = $chunker->mergedFileDt;
			if(isset($fileDtMrg)){
				KalturaLog::log("merged:".print_r($fileDtMrg,1));
				$msgStr.= ",file dur(v:".round($fileDtMrg->videoDuration/1000,4).",a:".round($fileDtMrg->audioDuration/1000,4).")";
			}
			if(isset($sessionData->refFileDt)) {
				$fileDtRef = $sessionData->refFileDt;
				KalturaLog::log("reference:".print_r($fileDtRef,1));
			}
			$fileDtSrc = $chunker->sourceFileDt;
			if(isset($fileDtSrc)){
				KalturaLog::log("source:".print_r($fileDtSrc,1));
			}
			
			{
				KalturaLog::log("CSV,idx,startedAt,user,system,elapsed,cpu");
				$userAcc = $systemAcc = $elapsedAcc = $cpuAcc = 0;
				foreach($this->chunkExecutionDataArr as $idx=>$execData){
					$userAcc+= $execData->user;
					$systemAcc+= $execData->system;
					$elapsedAcc+= $execData->elapsed;
					$cpuAcc+= $execData->cpu;
					
					KalturaLog::log("CSV,$idx,$execData->startedAt,$execData->user,$execData->system,$execData->elapsed,$execData->cpu");
				}
				$cnt = count($chunker->chunkDataArr);
				$userAvg 	= round($userAcc/$cnt,3);
				$systemAvg 	= round($systemAcc/$cnt,3);
				$elapsedAvg = round($elapsedAcc/$cnt,3);
				$cpuAvg 	= round($cpuAcc/$cnt,3);
			}
			
//			KalturaLog::log("LogFile: ".$chunker->getSessionName("log"));
			KalturaLog::log("***********************************************************");
			KalturaLog::log("* Session Summary (".date("Y-m-d H:i:s").")");
			KalturaLog::log("* ");
			KalturaLog::log("ExecutionStats:chunks($cnt),accum(elapsed:$elapsedAcc,user:$userAcc,system:$systemAcc),average(elapsed:$elapsedAvg,user:$userAvg,system:$systemAvg,cpu:$cpuAvg)");
			if($sessionData->returnStatus==KChunkedEncodeReturnStatus::AnalyzeError){
				$msgStr.= ",analyze:BAD";
			}
			if($sessionData->returnStatus==KChunkedEncodeReturnStatus::OK){
				$msgStr.= ",analyze:OK";
				$frameRateMode = stristr($fileDtMrg->rawData,"Frame rate mode                          : ");
				$frameRateMode = strtolower(substr($frameRateMode, strlen("Frame rate mode                          : ")));
				$frameRateMode = strncmp($frameRateMode,"constant",8);
				if($frameRateMode==0) {
					$msgStr.= ",frameRateMode(constant)";
				}
				else
					$msgStr.= ",frameRateMode(variable)";
			}
			if(isset($chunker->sourceFileDt)
			&& (!isset($chunker->setup->duration) || $chunker->setup->duration<=0 || abs($chunker->setup->duration-round($chunker->sourceFileDt->containerDuration/1000,4))<0.1)) {
				if(isset($fileDtMrg)){
					$deltaStr = null;
					if(isset($fileDtRef)){
						$vidDelta = round(($fileDtMrg->videoDuration - $fileDtRef->videoDuration)/1000,4);
						$audDelta = round(($fileDtMrg->audioDuration - $fileDtRef->audioDuration)/1000,4);
						$deltaStr = "MergedToRef:(v:$vidDelta,a:$audDelta)";
						$videoOk = (abs($vidDelta)<$chunker->maxInaccuracyValue);
						$deltaStr.=$videoOk?",video:OK":",video:BAD";
						$audioOk = (abs($audDelta)<$chunker->maxInaccuracyValue);
						$deltaStr.=$audioOk?",audio:OK":",audio:BAD";
						$deltaStr.=($audioOk && $videoOk)?",delta:OK":",delta:BAD";
						$deltaStr.= ",dur(v:".round($fileDtRef->videoDuration/1000,4).",a:".round($fileDtRef->audioDuration/1000,4).")";
						KalturaLog::log("$deltaStr");
					}

					$deltaStr = null;
					if(isset($fileDtSrc)){
						$dur=$fileDtSrc->videoDuration = ($fileDtSrc->videoDuration>0)? $fileDtSrc->videoDuration: $dur=$fileDtSrc->containerDuration;
						$vidDelta = ($fileDtMrg->videoDuration - $dur)/1000;//round(($fileDtMrg->videoDuration - $dur)/1000,6);
						$dur=$fileDtSrc->audioDuration = ($fileDtSrc->audioDuration>0)? $fileDtSrc->audioDuration: $dur=$fileDtSrc->containerDuration;
						$audDelta = ($fileDtMrg->audioDuration - $dur)/1000;//round(($fileDtMrg->audioDuration - $dur)/1000,6);
						$deltaStr = "MergedToSrc:(v:$vidDelta,a:$audDelta)";
						$videoOk = (abs($vidDelta)<$chunker->maxInaccuracyValue);
						$deltaStr.=$videoOk?",video:OK":",video:BAD";
						$audioOk = (abs($audDelta)<$chunker->maxInaccuracyValue);
						$deltaStr.=$audioOk?",audio:OK":",audio:BAD";
						$deltaStr.=($audioOk && $videoOk)?",delta:OK":",delta:BAD";
						$deltaStr.= ",dur(v:".round($fileDtSrc->videoDuration/1000,6).",a:".round($fileDtSrc->audioDuration/1000,6).")";
						KalturaLog::log("$deltaStr");
					}
				}
			}
			
			KalturaLog::log("$msgStr");
			KalturaLog::log("OutputFile: ".realpath($chunker->getSessionName()));
			
			$errStr = null;
			$lasted = date_diff($this->startedAt,$this->finishedAt);
				
			if($sessionData->returnStatus==KChunkedEncodeReturnStatus::OK) {
				$msgStr = "RESULT:Success"."  Lasted:".$lasted->format('%h:%i:%s')."/".($lasted->s+60*$lasted->i+3600*$lasted->h)."secs";
			}
			else {
				switch($sessionData->returnStatus){
				case KChunkedEncodeReturnStatus::InitializeError: 	 $errStr = "InitializeError"; break;
				case KChunkedEncodeReturnStatus::GenerateVideoError: $errStr = "GenerateVideoError"; break;
				case KChunkedEncodeReturnStatus::GenerateAudioError: $errStr = "GenerateAudioError"; break;
				case KChunkedEncodeReturnStatus::FixDriftError: 	 $errStr = "FixDriftError"; break;
				case KChunkedEncodeReturnStatus::AnalyzeError: 		 $errStr = "AnalyzeError"; break;
				case KChunkedEncodeReturnStatus::MergeError: 		 $errStr = "MergeError"; break;
				case KChunkedEncodeReturnStatus::MergeAttemptsError: $errStr = "MergeAttemptsError"; break;
				case KChunkedEncodeReturnStatus::MergeThreshError:   $errStr = "MergeThreshError"; break;
				}
				$msgStr = "RESULT:Failure - error($errStr/$sessionData->returnStatus),message(".implode(',',$sessionData->returnMessages).")";
			}
			KalturaLog::log($msgStr);
			KalturaLog::log("***********************************************************");
			
			$this->SerializeSession();
		}
		
		/*****************************
		 * parseArgsToSetup
		 */
		protected static function parseArgsToSetup($argv, $setup)
		{
			unset($argv[0]);
			if(($idx=array_search("ANDAND", $argv))!==false){
				$argv[$idx] = '&&';
			}
			$setupArr = get_object_vars($setup);
			foreach($setupArr as $fld=>$val){
				if(($idx=array_search("-$fld", $argv))!==false){
					$setup->$fld = $argv[$idx+1];
					unset($argv[$idx+1]);
					unset($argv[$idx]);
				}
			}
			KalturaLog::log($setup);

			if(!isset($setup->startFrom)) 		$setup->startFrom = 0;
			if(!isset($setup->dry)) 			$setup->dry = 0;
			if(!isset($setup->createFolder))	$setup->createFolder = 1;
			
			$setup->cmd = implode(' ',$argv);
			
			KalturaLog::log("Setup:".print_r($setup,1));
		}

		/********************
		 * Save the sessionData to .ses file
		 */
		public function SerializeSession()
		{
			file_put_contents($this->chunker->getSessionName("session"), serialize($this));
		}
		
	}

	/********************
	 * Process stat data
	 */
	class KProcessExecutionData {
		public $process = null;	// ...
		public $exitCode = null;// ...
		public $startedAt = null;
		
		public $user = null;
		public $system = null;
		public $elapsed = null;
		public $cpu = null;
		
		/********************
		 *
		 */
		public function __construct($process = null, $logFileName = null)
		{
			if(isset($process)){
				$this->process = $process;
			}
			if(isset($logFileName)){
				$this->parseLogFile($logFileName);
			}
		}
		
		/********************
		 *
		 */
		public function parseLogFile($logFileName)
		{
			$fp = fopen($logFileName, 'r');
			$line = fgets($fp);
			$logLines = null;
			$logLines = $this->readLastLines($fp, 300);							
			$logLines[] = $line;
			fclose($fp);
			foreach($logLines as $line){
				if(strstr($line, "elapsed")!==false) {
					$tmpArr = explode(" ",$line);
					foreach($tmpArr as $tmpStr){
						if(($pos=strpos($tmpStr, "user"))!==false) {
							$this->user = substr($tmpStr,0,$pos);
						}
						else if(($pos=strpos($tmpStr, "system"))!==false) {
							$this->system = substr($tmpStr,0,$pos);
						}
						else if(($pos=strpos($tmpStr, "elapsed"))!==false) {
							$elapsed = substr($tmpStr,0,$pos);
							$tmpTmArr = array_reverse(explode(":",$elapsed));
							$this->elapsed = 0;
							foreach($tmpTmArr as $i=>$tm){
								$this->elapsed+= $tm*pow(60,$i);
							}
						}
						else if(($pos=strpos($tmpStr, "%CPU"))!==false) {
							$this->cpu = substr($tmpStr,0,$pos);
						}
					}
				}
				else if(strstr($line, "Started:")!==false){
					$this->startedAt = trim(substr($line,strlen("started:2017-03-15 ")));
				}
				else if(strstr($line, "exit_code:")!==false){
					$this->exitCode = trim(substr($line,strlen("exit_code:")));
				}
			}
		}
		
		/********************
		 *
		 */
		private function readLastLines($fp, $length)
		{
			fseek($fp, -$length, SEEK_END);
			$lines=array();
			while(!feof($fp)){
				$line = fgets($fp);
				$lines[] = $line;
			}
			return $lines;
		}
	}

