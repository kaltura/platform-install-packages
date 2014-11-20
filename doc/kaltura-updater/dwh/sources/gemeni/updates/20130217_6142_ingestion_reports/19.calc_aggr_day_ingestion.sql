DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `calc_aggr_day_ingestion`$$

CREATE DEFINER=`etl`@`localhost` PROCEDURE `calc_aggr_day_ingestion`(p_date_id INT(11))
BEGIN
	DECLARE v_entry_with_flavor_failed_count INT(11);
	DECLARE v_all_convert_entries_count INT(11);
	
	UPDATE aggr_managment SET start_time = NOW() WHERE aggr_name = 'ingestion' AND date_id = p_date_id;
		
	            
	SET @s = CONCAT('INSERT INTO kalturadw.dwh_daily_ingestion (date_id, normal_wait_time_count, medium_wait_time_count, long_wait_time_count, extremely_long_wait_time_count, stuck_wait_time_count, total_ff_wait_time_sec, median_ff_wait_time_sec) '
					'SELECT created_date_id, COUNT(IF(wait_time< 5,1,null)) normal_wait_time, COUNT(IF(wait_time>=5 AND wait_time < 180,1,null)) medium_wait_time, COUNT(IF(wait_time>=180 AND wait_time<900,1,null)) long_wait_time,
					COUNT(IF(wait_time>=900 AND wait_time < 3600,1,null)) extremely_long_wait_time_count, COUNT(IF(wait_time>=3600,1,null)) stuck, SUM(IF(wait_time>0,wait_time, 0)), calc_median_ff_convert_job_wait_time(' , p_date_id ,')'
					' FROM kalturadw.dwh_fact_convert_job
					WHERE is_ff = 1 
					AND created_date_id = ' ,p_date_id , 
					' ON DUPLICATE KEY UPDATE	
						normal_wait_time_count=VALUES(normal_wait_time_count),
						medium_wait_time_count=VALUES(medium_wait_time_count),
						long_wait_time_count=VALUES(long_wait_time_count),
						extremely_long_wait_time_count=VALUES(extremely_long_wait_time_count),
						stuck_wait_time_count=VALUES(stuck_wait_time_count),
						total_ff_wait_time_sec=VALUES(total_ff_wait_time_sec),
						median_ff_wait_time_sec=VALUES(median_ff_wait_time_sec);');
	
		
	PREPARE stmt FROM  @s;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
	
	SET @s = CONCAT('INSERT INTO kalturadw.dwh_daily_ingestion (date_id, success_entries_count, failed_entries_count)'
					'SELECT ' , p_date_id, ' ,COUNT(IF(entry_status_id=2, 1, NULL)) entries_success, COUNT(IF(entry_status_id=-1, 1, NULL)) entries_failure
					FROM 
					(SELECT distinct(entry.entry_id), entry_status_id
					FROM kalturadw.dwh_dim_entries entry, kalturadw.dwh_dim_batch_job_sep job
					WHERE entry.entry_id = job.entry_id
					AND entry.created_at BETWEEN DATE(' , p_date_id, ') AND DATE(', p_date_id, ') + INTERVAL 1 DAY',
					' AND entry.entry_media_type_id IN (1,5)
					AND job_type_id = 10) e
					ON DUPLICATE KEY UPDATE	
						success_entries_count=VALUES(success_entries_count),
						failed_entries_count=VALUES(failed_entries_count);');
	
		
	PREPARE stmt FROM  @s;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
	
	SET @s = CONCAT('INSERT INTO kalturadw.dwh_daily_ingestion (date_id, success_convert_job_count, failed_convert_job_count)'
					'SELECT created_date_id, COUNT(IF(status_id=5,1,NULL)) convert_job_success, COUNT(IF(status_id=6 OR status_id = 10,1,NULL)) convert_job_failure 
					 FROM kalturadw.dwh_fact_convert_job
					 WHERE created_date_id = ', p_date_id,
					 ' ON DUPLICATE KEY UPDATE	
						success_convert_job_count=VALUES(success_convert_job_count),
						failed_convert_job_count=VALUES(failed_convert_job_count);');
						
	PREPARE stmt FROM  @s;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
	
	
    SELECT COUNT(DISTINCT(entry_id))
    INTO v_entry_with_flavor_failed_count
    FROM kalturadw.dwh_fact_convert_job
    WHERE created_date_id = p_date_id
    AND status_id IN (6,10);
    
    SELECT COUNT(DISTINCT(entry_id))
    INTO v_all_convert_entries_count
    FROM kalturadw.dwh_fact_convert_job
    WHERE created_date_id = p_date_id;
				
    
    SET @s = CONCAT('INSERT INTO kalturadw.dwh_daily_ingestion (date_id, all_conversion_job_entries_count, failed_conversion_job_entries_count)'
			' VALUES (', p_date_id, ",", v_all_convert_entries_count, ",", v_entry_with_flavor_failed_count, ")"
			' ON DUPLICATE KEY UPDATE	
			all_conversion_job_entries_count=VALUES(all_conversion_job_entries_count),
			failed_conversion_job_entries_count=VALUES(failed_conversion_job_entries_count);');
	
		
    PREPARE stmt FROM  @s;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    
    
			
	SET @s = CONCAT('INSERT INTO kalturadw.dwh_daily_ingestion (date_id, total_wait_time_sec, convert_jobs_count)'
					'SELECT created_date_id, SUM(IF(wait_time>0, wait_time, 0)), COUNT(id)
					 FROM kalturadw.dwh_fact_convert_job
					 WHERE created_date_id = ' ,p_date_id,
					 ' ON DUPLICATE KEY UPDATE	
						total_wait_time_sec=VALUES(total_wait_time_sec),
						convert_jobs_count=VALUES(convert_jobs_count);');
	
		
	PREPARE stmt FROM  @s;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    
    SET @s = CONCAT('INSERT INTO kalturadw.dwh_daily_partner_ingestion (date_id, partner_id, total_conversion_sec)'
					'SELECT created_date_id, partner_id, SUM(conversion_time)
					 FROM kalturadw.dwh_fact_convert_job
					 WHERE created_date_id = ' ,p_date_id,
					 ' AND conversion_time > 0
					 GROUP BY partner_id' ,
					 ' ON DUPLICATE KEY UPDATE	
						total_conversion_sec=VALUES(total_conversion_sec);');
	
		
	PREPARE stmt FROM  @s;
    EXECUTE stmt;
    DEALLOCATE PREPARE stmt;
    
    
		
	UPDATE aggr_managment SET end_time = NOW() WHERE aggr_name = 'ingestion' AND date_id = p_date_id;
END$$

DELIMITER ;