DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `calc_aggr_day_bandwidth`$$

CREATE DEFINER=`etl`@`localhost` PROCEDURE `calc_aggr_day_bandwidth`(p_date_val DATE, p_aggr_name VARCHAR(100))
BEGIN
	DECLARE v_ignore DATE;
	DECLARE v_from_archive DATE;
        DECLARE v_table_name VARCHAR(100);
	DECLARE v_aggr_table VARCHAR(100);
	DECLARE v_aggr_id_field_str VARCHAR(100);
	
	UPDATE aggr_managment SET start_time = NOW() WHERE aggr_name = p_aggr_name AND date_id = DATE(p_date_val)*1;
	SELECT MAX(DATE(NOW() - INTERVAL archive_delete_days_back DAY))
	INTO v_ignore
	FROM kalturadw_ds.retention_policy
	WHERE table_name IN('dwh_fact_bandwidth_usage', 'dwh_fact_fms_sessions');
	
	IF (p_date_val >= v_ignore) THEN -- not so old, we don't have any data
		
		SELECT aggr_table, IF(IFNULL(aggr_id_field,'')='','', CONCAT(', ', aggr_id_field)) aggr_id_field
		INTO  v_aggr_table, v_aggr_id_field_str
		FROM kalturadw_ds.aggr_name_resolver
		WHERE aggr_name = p_aggr_name;
		
		SET @s = CONCAT('UPDATE kalturadw.',v_aggr_table, ' SET count_bandwidth_kb = NULL WHERE date_id = DATE(\'',p_date_val,'\')*1');
		PREPARE stmt FROM  @s;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;
		
		/* HTTP */
		SELECT DATE(archive_last_partition)
		INTO v_from_archive
		FROM kalturadw_ds.retention_policy
		WHERE table_name = 'dwh_fact_bandwidth_usage';
	
                IF (p_date_val >= v_from_archive) THEN -- aggr from archive or from events
                        SET v_table_name = 'dwh_fact_bandwidth_usage';
                ELSE
                        SET v_table_name = 'dwh_fact_bandwidth_usage_archive';
                END IF;
                
		SET @s = CONCAT('INSERT INTO kalturadw.', v_aggr_table, ' (partner_id, date_id, hour_id ', v_aggr_id_field_str,', count_bandwidth_kb)'
				'SELECT partner_id, MAX(activity_date_id), 0 hour_id', v_aggr_id_field_str,', SUM(bandwidth_bytes)/1024 count_bandwidth
				FROM ', v_table_name, '	WHERE activity_date_id=date(\'',p_date_val,'\')*1
				GROUP BY partner_id', v_aggr_id_field_str,'
				ON DUPLICATE KEY UPDATE	count_bandwidth_kb=VALUES(count_bandwidth_kb)');
	

		PREPARE stmt FROM  @s;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;
			
		/* FMS */
		SELECT DATE(archive_last_partition)
		INTO v_from_archive
		FROM kalturadw_ds.retention_policy
		WHERE table_name = 'dwh_fact_fms_sessions';
		
		IF (p_date_val >= v_from_archive) THEN -- aggr from archive or from events
                        SET v_table_name = 'dwh_fact_fms_sessions';
                ELSE
                        SET v_table_name = 'dwh_fact_fms_sessions_archive';
                END IF;

		SET @s = CONCAT('INSERT INTO kalturadw.', v_aggr_table, ' (partner_id, date_id, hour_id', v_aggr_id_field_str,', count_bandwidth_kb)
				SELECT session_partner_id, MAX(session_date_id), 0 hour_id', v_aggr_id_field_str,', SUM(total_bytes)/1024 count_bandwidth 
				FROM kalturadw.dwh_fact_fms_sessions WHERE session_date_id=date(\'',p_date_val,'\')*1
				GROUP BY session_partner_id', v_aggr_id_field_str,'
				ON DUPLICATE KEY UPDATE	count_bandwidth_kb=VALUES(count_bandwidth_kb)');
		PREPARE stmt FROM  @s;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;
	
	END IF;
	
	UPDATE aggr_managment SET end_time = NOW() WHERE aggr_name = p_aggr_name AND date_id = DATE(p_date_val)*1;
END$$

DELIMITER ;
