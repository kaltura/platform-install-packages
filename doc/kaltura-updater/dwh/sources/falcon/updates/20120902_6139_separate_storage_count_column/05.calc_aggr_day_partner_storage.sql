DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `calc_aggr_day_partner_storage`$$

CREATE DEFINER=`etl`@`localhost` PROCEDURE `calc_aggr_day_partner_storage`(date_val DATE)
BEGIN
    DELETE FROM kalturadw.dwh_hourly_partner_usage WHERE date_id = DATE(date_val)*1 AND IFNULL(count_bandwidth_kb,0) = 0 AND bandwidth_source_id = 1;
    UPDATE kalturadw.dwh_hourly_partner_usage SET added_storage_mb = 0, deleted_storage_mb = 0, aggr_storage_mb=NULL WHERE date_id = DATE(date_val)*1 AND IFNULL(count_bandwidth_kb,0) > 0;
	
	DROP TABLE IF EXISTS temp_aggr_storage;
	CREATE TEMPORARY TABLE temp_aggr_storage(
		partner_id      	INT(11) NOT NULL,
		date_id     		INT(11) NOT NULL,
		hour_id	 		TINYINT(4) NOT NULL,
		added_storage_mb	DECIMAL(19,4) NOT NULL,
		deleted_storage_mb      DECIMAL(19,4) NOT NULL
	) ENGINE = MEMORY;
      
	INSERT INTO 	temp_aggr_storage (partner_id, date_id, hour_id, added_storage_mb, deleted_storage_mb)
   	SELECT 		partner_id, MAX(entry_size_date_id), 0 hour_id, SUM(IF(entry_additional_size_kb>0,entry_additional_size_kb,0))/1024 added_storage_mb, SUM(IF(entry_additional_size_kb<0,entry_additional_size_kb*-1,0))/1024 deleted_storage_mb 
	FROM 		dwh_fact_entries_sizes
	WHERE		entry_size_date_id=DATE(date_val)*1
	GROUP BY 	partner_id;
	
	INSERT INTO 	kalturadw.dwh_hourly_partner_usage (partner_id, date_id, hour_id, bandwidth_source_id, added_storage_mb, deleted_storage_mb, aggr_storage_mb)
	SELECT		partner_id, DATE(date_val)*1, 0 hour_id, 1, 0, 0, aggr_storage_mb
	FROM        kalturadw.dwh_hourly_partner_usage
	WHERE       date_id = DATE(date_val - INTERVAL 1 DAY)*1
	AND         bandwidth_source_id = 1
	ON DUPLICATE KEY UPDATE added_storage_mb=VALUES(added_storage_mb), deleted_storage_mb=VALUES(deleted_storage_mb), aggr_storage_mb = VALUES(aggr_storage_mb);
	
	INSERT INTO 	kalturadw.dwh_hourly_partner_usage (partner_id, date_id, hour_id, bandwidth_source_id, added_storage_mb, deleted_storage_mb, aggr_storage_mb)
	SELECT		aggr.partner_id, aggr.date_id, aggr.hour_id, 1, aggr.added_storage_mb, aggr.deleted_storage_mb, aggr.added_storage_mb - aggr.deleted_storage_mb
	FROM		temp_aggr_storage aggr 
	ON DUPLICATE KEY UPDATE added_storage_mb=VALUES(added_storage_mb), deleted_storage_mb=VALUES(deleted_storage_mb), aggr_storage_mb=IFNULL(aggr_storage_mb,0) + VALUES(aggr_storage_mb) ;
	
END$$

DELIMITER ;
