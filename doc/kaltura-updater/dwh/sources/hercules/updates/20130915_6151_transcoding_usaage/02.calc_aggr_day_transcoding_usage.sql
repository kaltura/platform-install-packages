DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `calc_aggr_day_transcoding_usage`$$

CREATE PROCEDURE `calc_aggr_day_transcoding_usage`(p_date_id INT(11))
BEGIN
	UPDATE aggr_managment SET start_time = NOW() WHERE aggr_name = 'transcoding_usage' AND date_id = p_date_id;
	
    UPDATE kalturadw.dwh_hourly_partner_usage SET count_transcoding_mb = 0 WHERE date_id = p_date_id AND bandwidth_source_id = 1;
	
	INSERT INTO kalturadw.dwh_hourly_partner_usage (partner_id, date_id, hour_id, bandwidth_source_id, count_transcoding_mb) 
	SELECT partner_id, p_date_id, 0 hour_id, 1, SUM(file_size)/1024/1024
	FROM kalturadw.dwh_dim_batch_job_sep
	WHERE created_date_id = p_date_id
	AND updated_date_id >= p_date_id
	AND job_type_id = 0
	AND status_id = 5
	AND file_size > 0
	GROUP BY partner_id
	ON DUPLICATE KEY UPDATE count_transcoding_mb=VALUES(count_transcoding_mb);
	
	UPDATE aggr_managment SET end_time = NOW() WHERE aggr_name = 'transcoding_usage' AND date_id = p_date_id;
END$$

DELIMITER ;