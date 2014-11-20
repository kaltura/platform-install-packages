DELIMITER $$

DROP VIEW IF EXISTS `kalturalog`.`last_job_run`$$

CREATE ALGORITHM=UNDEFINED  SQL SECURITY DEFINER 
	VIEW kalturalog.`last_job_run` AS (
	SELECT `l1`.`JOBNAME` AS `JOBNAME`,`l1`.`STATUS` AS `status`,`l1`.`ERRORS` AS `HAD_ERRORS`,
		`l1`.`DEPDATE` AS `LAST_RUN_START`,`l1`.`LOGDATE` AS `LAST_RUN_END`,
		`l1`.`LINES_INPUT` AS `LINES_INPUT`,`l1`.`LINES_OUTPUT` AS `LINES_OUTPUT`,
		`l1`.`LINES_UPDATED` AS `LINES_UPDATED`,
		`l1`.`LOG_FIELD` AS `LOG_FIELD` 
	FROM (kalturalog.`etl_log` `l1` JOIN kalturalog.`etl_log` `l2`) 
	WHERE (`l1`.`JOBNAME` = `l2`.`JOBNAME`) 
	GROUP BY `l1`.`ID_JOB`,`l1`.`JOBNAME`,`l1`.`ERRORS`,`l1`.`LOGDATE`,`l1`.`LOG_FIELD`
	 HAVING (`l1`.`LOGDATE` = MAX(`l2`.`LOGDATE`))
	 )$$

DELIMITER ;