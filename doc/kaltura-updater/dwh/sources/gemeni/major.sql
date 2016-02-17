/*6140*/
USE kalturadw_ds;

DROP TABLE IF EXISTS kalturadw_ds.fact_tables;
CREATE TABLE kalturadw_ds.fact_tables
	(fact_table_id INT NOT NULL,
	fact_table_name VARCHAR(50),
	UNIQUE KEY (fact_table_id));
	
INSERT INTO kalturadw_ds.fact_tables VALUES (1,'kalturadw.dwh_fact_events'), 
				(2,'kalturadw.dwh_fact_bandwidth_usage'),
				(3,'kalturadw.dwh_fact_fms_session_events'),
				(4,'kalturadw.dwh_fact_api_calls'),
				(5,'kalturadw.dwh_fact_incomplete_api_calls'),
				(6,'kalturadw.dwh_fact_errors');
	
DROP TABLE IF EXISTS kalturadw_ds.fact_stats;	
CREATE TABLE kalturadw_ds.fact_stats
	(fact_table_id int not null,
	date_id int not null,
	hour_id int not null,
	total_records int not null,
	uncalculated_records int not null default 0,
	unique key (fact_table_id, date_id, hour_id));
	
ALTER TABLE kalturadw_ds.staging_areas
		ADD COLUMN target_table_id INT AFTER target_table,
		ADD COLUMN reaggr_percent_trigger INT NOT NULL DEFAULT 0;

UPDATE kalturadw_ds.staging_areas s, kalturadw_ds.fact_tables f
SET s.target_table_id = f.fact_table_id
WHERE s.target_table = f.fact_table_name;

ALTER TABLE kalturadw_ds.staging_areas
	CHANGE COLUMN target_table_id target_table_id INT NOT NULL,
	DROP COLUMN target_table;
	
	
	
DELIMITER $$

USE `kalturadw_ds`$$

DROP PROCEDURE IF EXISTS `transfer_cycle_partition`$$

CREATE PROCEDURE `transfer_cycle_partition`(p_cycle_id VARCHAR(10))
BEGIN
	DECLARE src_table VARCHAR(45);
	DECLARE tgt_table VARCHAR(45);
	DECLARE tgt_table_id INT;
	DECLARE dup_clause VARCHAR(4000);
	DECLARE partition_field VARCHAR(45);
	DECLARE select_fields VARCHAR(4000);
	DECLARE post_transfer_sp_val VARCHAR(4000);
	DECLARE v_ignore_duplicates_on_transfer BOOLEAN;	
	DECLARE aggr_date VARCHAR(400);
	DECLARE aggr_hour VARCHAR(400);
	DECLARE aggr_names VARCHAR(4000);
	DECLARE reset_aggr_min_date DATETIME;
	DECLARE v_reaggr_percent_trigger INT;
	
	
	DECLARE done INT DEFAULT 0;
	DECLARE staging_areas_cursor CURSOR FOR SELECT 	source_table, target_table_id, fact_table_name, IFNULL(on_duplicate_clause,''),	staging_partition_field, post_transfer_sp, aggr_date_field, hour_id_field, post_transfer_aggregations, reset_aggregations_min_date, ignore_duplicates_on_transfer, reaggr_percent_trigger
											FROM staging_areas s, cycles c, fact_tables f
											WHERE s.process_id=c.process_id AND c.cycle_id = p_cycle_id AND f.fact_table_id = s.target_table_id;
											
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
	OPEN staging_areas_cursor;
	
	read_loop: LOOP
		FETCH staging_areas_cursor INTO src_table, tgt_table_id, tgt_table, dup_clause, partition_field, post_transfer_sp_val, aggr_date, aggr_hour, aggr_names, reset_aggr_min_date, v_ignore_duplicates_on_transfer, v_reaggr_percent_trigger;
		IF done THEN
			LEAVE read_loop;
		END IF;
	
		DROP TABLE IF EXISTS tmp_stats;
	
		SET @s = CONCAT('CREATE TEMPORARY TABLE tmp_stats '
				'SELECT ds.date_id, ds.hour_id, new_rows+IFNULL(uncalculated_records,0) as uncalculated_records, ',
				'IFNULL(total_records, 0) calculated_records from ',
				'(SELECT ', aggr_date, ' date_id, ', aggr_hour, ' hour_id, count(*) new_rows FROM ',src_table,
				' WHERE ', partition_field,'  = ',p_cycle_id, ' group by date_id, hour_id) ds ',
				'LEFT OUTER JOIN kalturadw_ds.fact_stats fs on ds.date_id = fs.date_id AND ds.hour_id = fs.hour_id
				AND fs.fact_table_id = ', tgt_table_id);
		PREPARE stmt FROM @s;
		EXECUTE stmt;
		DEALLOCATE PREPARE stmt;
		
		
		IF ((LENGTH(AGGR_DATE) > 0) && (LENGTH(aggr_names) > 0)) THEN
			SET @s = CONCAT('INSERT INTO kalturadw.aggr_managment(aggr_name, date_id, hour_id, data_insert_time)
					SELECT aggr_name, date_id, hour_id, now() 
					FROM kalturadw_ds.aggr_name_resolver a, tmp_stats ts
					WHERE 	aggr_name in ', aggr_names, '
					AND date_id >= date(\'',reset_aggr_min_date,'\')
					AND if(calculated_records=0,100, uncalculated_records*100/(calculated_records+uncalculated_records)) > ', v_reaggr_percent_trigger, '
					ON DUPLICATE KEY UPDATE data_insert_time = now()');
			PREPARE stmt FROM @s;
			EXECUTE stmt;
			DEALLOCATE PREPARE stmt;
		END IF;
		
		SELECT 	GROUP_CONCAT(column_name ORDER BY ordinal_position)
		INTO 	select_fields
		FROM information_schema.COLUMNS
		WHERE CONCAT(table_schema,'.',table_name) = tgt_table;
			
		SET @s = CONCAT('INSERT ', IF(v_ignore_duplicates_on_transfer=1, 'IGNORE', '') ,' INTO ',tgt_table, ' (',select_fields,') ',
						' SELECT ',select_fields,
						' FROM ',src_table,
						' WHERE ',partition_field,'  = ',p_cycle_id,
						' ',dup_clause );
		PREPARE stmt FROM @s;
		EXECUTE stmt;
		DEALLOCATE PREPARE stmt;
			
		INSERT INTO kalturadw_ds.fact_stats (fact_table_id, date_id, hour_id, total_records, uncalculated_records)
			SELECT tgt_table_id, date_id, hour_id,
				IF(calculated_records=0 OR uncalculated_records*100/(calculated_records+uncalculated_records) > v_reaggr_percent_trigger,
					calculated_records + uncalculated_records, calculated_records),
				IF(calculated_records=0 OR uncalculated_records*100/(calculated_records+uncalculated_records) > v_reaggr_percent_trigger,
					0, uncalculated_records)
			FROM tmp_stats t
		ON DUPLICATE KEY UPDATE 
			total_records = IF(t.calculated_records=0 OR t.uncalculated_records*100/(t.calculated_records+t.uncalculated_records) > v_reaggr_percent_trigger,
					t.calculated_records + t.uncalculated_records, t.calculated_records),
			uncalculated_records = IF(t.calculated_records=0 OR t.uncalculated_records*100/(t.calculated_records+t.uncalculated_records) > v_reaggr_percent_trigger,
					0, t.uncalculated_records);
	
		
		IF LENGTH(POST_TRANSFER_SP_VAL)>0 THEN
			SET @s = CONCAT('CALL ',post_transfer_sp_val,'(',p_cycle_id,')');
			PREPARE stmt FROM @s;
			EXECUTE stmt;
			DEALLOCATE PREPARE stmt;
		END IF;
	END LOOP;
	CLOSE staging_areas_cursor;
END$$

DELIMITER ;

/* 6141 */
DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `calc_partner_billing_storage_per_category`$$

CREATE PROCEDURE `calc_partner_billing_storage_per_category`(p_start_date_id INT, p_end_date_id INT ,p_partner_id INT)
BEGIN
   
    
    DROP TEMPORARY TABLE IF EXISTS temp_storage;
    CREATE TEMPORARY TABLE temp_storage(
        category_name       VARCHAR(255) ,
        date_id             INT(11) NOT NULL,
        count_storage_mb    DECIMAL(19,4) NOT NULL
    ) ENGINE = MEMORY;
      
    INSERT INTO     temp_storage (category_name, date_id, count_storage_mb)
    SELECT  IF(ec.updated_at IS NULL OR c.category_name IS NULL,'-', c.category_name) category_name,  
        entry_size_date_id, 
        SUM(entry_additional_size_kb)/1024 aggr_storage_mb
    FROM    kalturadw.dwh_fact_entries_sizes es
        LEFT OUTER JOIN kalturadw.dwh_dim_entry_categories ec ON (ec.entry_id = es.entry_id AND ec.partner_id = es.partner_id)     
        LEFT OUTER JOIN kalturadw.dwh_dim_categories c ON (ec.category_id = c.category_id)
        LEFT OUTER JOIN kalturadw.dwh_dim_entries e ON (ec.partner_id = e.partner_id AND ec.entry_id = e.entry_id AND ec.updated_at = e.updated_at)
    WHERE es.partner_id = p_partner_id
    AND es.entry_size_date_id <= p_end_date_id    
    GROUP BY  IF(ec.updated_at IS NULL OR c.category_name IS NULL,'-', c.category_name) ,  es.entry_size_date_id;
      
 
    DROP TABLE IF EXISTS snapshot_storage;
    CREATE TEMPORARY TABLE snapshot_storage
    SELECT category_name, SUM(count_storage_mb) count_storage_mb
    FROM temp_storage
    GROUP BY category_name;

    DROP TABLE IF EXISTS avg_storage;
    CREATE TEMPORARY TABLE avg_storage
    SELECT s.category_name, SUM(s.count_storage_mb)/DAY(LAST_DAY(DATE(all_times.day_id))) avg_continuous_aggr_storage_mb
    FROM   dwh_dim_time all_times, temp_storage s 
    WHERE  all_times.day_id BETWEEN p_start_date_id AND p_end_date_id 
    AND all_times.day_id >= s.date_id 
    AND s.count_storage_mb<>0
    GROUP BY s.category_name;

    SELECT s.category_name, avg_continuous_aggr_storage_mb avg_storage_mb, count_storage_mb snapshot_storage_mb FROM avg_storage a 
    LEFT OUTER JOIN snapshot_storage s
    ON a.category_name = s.category_name;
        
END$$

DELIMITER ;

/* 6142 */
INSERT INTO kalturadw_ds.parameters (id, parameter_name, int_value, date_value) VALUES (10, 'convert_job_fact_last_update', 0, NOW());

use `kalturadw_bisources`;

DROP TABLE IF EXISTS `bisources_batch_job_exec_status`;

CREATE TABLE `bisources_batch_job_exec_status` (
  `batch_job_exec_status_id` INT(11) NOT NULL,
  `batch_job_exec_status_name` VARCHAR(100) DEFAULT 'missing value',
  PRIMARY KEY (`batch_job_exec_status_id`)
);

INSERT INTO `bisources_batch_job_exec_status`
VALUES 	(0,'NORMAL'),(1,'ABORTED');

DROP TABLE IF EXISTS `bisources_batch_job_object_type`;

CREATE TABLE `bisources_batch_job_object_type` (
  `batch_job_object_type_id` INT(11) NOT NULL,
  `batch_job_object_type_name` VARCHAR(100) DEFAULT 'missing value',
  PRIMARY KEY (`batch_job_object_type_id`)
);

INSERT INTO `bisources_batch_job_object_type` (`batch_job_object_type_id`,`batch_job_object_type_name`) 
VALUES  (1,'ENTRY'),(2,'CATEGORY'),(3,'FILE_SYNC'),(4,'ASSET');
			
DROP TABLE IF EXISTS `bisources_upload_token_status`;

CREATE TABLE `bisources_upload_token_status` (
  `upload_token_status_id` INT(11) NOT NULL,
  `upload_token_status_name` VARCHAR(100) DEFAULT 'missing value',
  PRIMARY KEY (`upload_token_status_id`)
);

INSERT INTO `bisources_upload_token_status`(`upload_token_status_id`,`upload_token_status_name`) 		
VALUES 	(0,'PENDING'),(1,'PARTIAL_UPLOAD'),(2,'FULL_UPLOAD'),(3,'CLOSED'),(4,'TIMED_OUT'),(5,'DELETED');
			
INSERT INTO `kalturadw`.`bisources_tables` (`table_name`, `to_update`) VALUES('batch_job_object_type',1);
INSERT INTO `kalturadw`.`bisources_tables` (`table_name`, `to_update`) VALUES('batch_job_exec_status',1);
INSERT INTO `kalturadw`.`bisources_tables` (`table_name`, `to_update`) VALUES('upload_token_status',1);

use `kalturadw`;

DROP TABLE IF EXISTS `dwh_dim_batch_job_exec_status`;

CREATE TABLE `dwh_dim_batch_job_exec_status` (
  `batch_job_exec_status_id` int(11) NOT NULL,
  `batch_job_exec_status_name` VARCHAR(100) DEFAULT 'missing value',
  `dwh_creation_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `dwh_update_date` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
  `ri_ind` TINYINT(4) NOT NULL DEFAULT '1',
  PRIMARY KEY (`batch_job_exec_status_id`)
) ENGINE=MYISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `dwh_dim_batch_job_object_type`;

CREATE TABLE `dwh_dim_batch_job_object_type` (
  `batch_job_object_type_id` int(11) NOT NULL,
  `batch_job_object_type_name` VARCHAR(100) DEFAULT 'missing value',
  `dwh_creation_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `dwh_update_date` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
  `ri_ind` TINYINT(4) NOT NULL DEFAULT '1',
  PRIMARY KEY (`batch_job_object_type_id`)
) ENGINE=MYISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `dwh_dim_upload_token_status`;

CREATE TABLE `dwh_dim_upload_token_status` (
  `upload_token_status_id` int(11) NOT NULL,
  `upload_token_status_name` VARCHAR(100) DEFAULT 'missing value',
  `dwh_creation_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `dwh_update_date` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
  `ri_ind` TINYINT(4) NOT NULL DEFAULT '1',
  PRIMARY KEY (`upload_token_status_id`)
) ENGINE=MYISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `dwh_dim_upload_token_object_type`;
CREATE TABLE `dwh_dim_upload_token_object_type` (
  `upload_token_object_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `upload_token_object_type_name` varchar(127) NOT NULL,
  PRIMARY KEY (`upload_token_object_type_id`),
  UNIQUE KEY `browser` (`upload_token_object_type_name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

USE kalturadw_ds;

INSERT INTO kalturadw_ds.pentaho_sequences VALUES(11,'dimensions/update_batch_job_sep.ktr',1,TRUE);
INSERT INTO kalturadw_ds.pentaho_sequences VALUES(12,'dimensions/update_upload_token.ktr',1,TRUE);

USE `kalturadw`;

DROP TABLE IF EXISTS `dwh_dim_batch_job_sep`;

CREATE TABLE `dwh_dim_batch_job_sep` (
  `dwh_id` INT(11) NOT NULL AUTO_INCREMENT,
  `id` INT(11) NOT NULL,
  `job_type_id` INT(6) DEFAULT NULL,
  `job_sub_type_id` INT(6) DEFAULT NULL,
  `object_id` VARCHAR(20) DEFAULT NULL,
  `object_type_id` INT(6) DEFAULT NULL,
  `data` VARCHAR(8192) DEFAULT NULL,
  `status_id` INT(11) DEFAULT NULL,
  `message` VARCHAR(1024) DEFAULT NULL,
  `description` VARCHAR(1024) DEFAULT NULL,
  `created_at` DATETIME DEFAULT NULL,
  `created_date_id` INT(11) DEFAULT '-1',
  `updated_at` DATETIME DEFAULT NULL,
  `updated_date_id` INT(11) DEFAULT '-1',
  `priority` TINYINT(4) NOT NULL,
  `queue_time` DATETIME DEFAULT NULL,
  `finish_time` DATETIME DEFAULT NULL,
  `entry_id` VARCHAR(20) DEFAULT NULL,
  `partner_id` INT(11) DEFAULT NULL,
  `last_scheduler_id` INT(11) DEFAULT NULL,
  `last_worker_id` INT(11) DEFAULT NULL,
  `parent_job_id` INT(11) DEFAULT NULL,
  `bulk_job_id` INT(11) DEFAULT NULL,
  `root_job_id` INT(11) DEFAULT NULL,
  `dc` VARCHAR(2) DEFAULT NULL,
  `error_type_id` INT(11) DEFAULT '0',
  `err_number` INT(11) DEFAULT '0',
  `execution_status_id` SMALLINT(6) DEFAULT NULL,
  `batch_job_lock_id` INT(20) DEFAULT NULL,
  `custom_data` TEXT,
  `lock_info` TEXT,
  `file_size` BIGINT(20) NOT NULL DEFAULT '-1',
  `dwh_creation_date` TIMESTAMP NOT NULL DEFAULT '0000-00-00 00:00:00',
  `dwh_update_date` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `ri_ind` TINYINT(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`dwh_id`),
  UNIQUE KEY `id` (`id`),
  KEY `dwh_update_date` (`dwh_update_date`),
  KEY `updated_date_id` (`updated_date_id`,`job_type_id`)
) ENGINE=MYISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `dwh_dim_upload_token`;

CREATE TABLE `dwh_dim_upload_token` (
  `dwh_id` int(11) NOT NULL AUTO_INCREMENT,
  `id` varchar(35) NOT NULL,
  `int_id` varchar(11) NOT NULL,
  `partner_id` int(11) DEFAULT NULL,
  `kuser_id` int(11) DEFAULT NULL,
  `status_id` int(11) DEFAULT NULL,
  `file_name` varchar(256) DEFAULT NULL,
  `file_size` bigint(20) DEFAULT NULL,
  `uploaded_file_size` bigint(20) DEFAULT NULL,
  `uploaded_temp_path` varchar(256) DEFAULT NULL,
  `user_ip` varchar(39) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `created_date_id` int(11) DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `updated_date_id` int(11) DEFAULT NULL,
  `dc` varchar(2) DEFAULT NULL,
  `object_id` varchar(31) DEFAULT NULL,
  `object_type_id` varchar(127) DEFAULT NULL,
  `dwh_creation_date` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  `dwh_update_date` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `ri_ind` tinyint(4) NOT NULL DEFAULT '0',
  PRIMARY KEY (`dwh_id`),
  UNIQUE KEY `id` (`id`),
  KEY `dwh_update_date` (`dwh_update_date`),
  KEY `updated_date_id` (`updated_date_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

DROP TABLE IF EXISTS `dwh_daily_ingestion`;

CREATE TABLE `dwh_daily_ingestion` (
  `date_id` int(11) NOT NULL,
  `normal_wait_time_count` int(11) NOT NULL,
  `medium_wait_time_count` int(11) NOT NULL,
  `long_wait_time_count` int(11) NOT NULL,
  `extremely_long_wait_time_count` int(11) NOT NULL,
  `stuck_wait_time_count` int(11) NOT NULL,
  `success_entries_count` int(11) NOT NULL,
  `failed_entries_count` int(11) NOT NULL,
  `success_convert_job_count` int(11) NOT NULL,
  `failed_convert_job_count` int(11) NOT NULL,
  `all_conversion_job_entries_count` int(11) NOT NULL,
  `failed_conversion_job_entries_count` int(11) NOT NULL,
  `total_wait_time_sec` bigint(22) DEFAULT '0',
  `total_ff_wait_time_sec` bigint(22) DEFAULT '0',
  `convert_jobs_count` int(11) NOT NULL,
  `median_ff_wait_time_sec` bigint(22) DEFAULT '0',
  PRIMARY KEY (`date_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
PARTITION BY RANGE (date_id)
(PARTITION @PARTITION_NAME@ VALUES LESS THAN (@PARTITION_VALUE@) ENGINE = InnoDB);

CALL kalturadw.add_monthly_partition_for_table('dwh_daily_ingestion');

DROP TABLE IF EXISTS `dwh_daily_partner_ingestion`;

CREATE TABLE `dwh_daily_partner_ingestion` (
  `date_id` int(11) NOT NULL,
  `partner_id` int(11) NOT NULL,
  `total_conversion_sec` int(22) DEFAULT '0',
  PRIMARY KEY (`date_id`,`partner_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
PARTITION BY RANGE (date_id)
(PARTITION @PARTITION_NAME@ VALUES LESS THAN (@PARTITION_VALUE@) ENGINE = InnoDB);

CALL kalturadw.add_monthly_partition_for_table('dwh_daily_partner_ingestion');

DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `add_partitions`$$

CREATE PROCEDURE `add_partitions`()
BEGIN
	CALL add_daily_partition_for_table('dwh_fact_events');
	CALL add_daily_partition_for_table('dwh_fact_fms_session_events');
	CALL add_daily_partition_for_table('dwh_fact_fms_sessions');
	CALL add_daily_partition_for_table('dwh_fact_bandwidth_usage');
	CALL add_daily_partition_for_table('dwh_fact_api_calls');
	CALL add_daily_partition_for_table('dwh_fact_incomplete_api_calls');
    CALL add_daily_partition_for_table('dwh_fact_errors');
    CALL add_daily_partition_for_table('dwh_fact_file_sync');
	CALL add_monthly_partition_for_table('dwh_fact_entries_sizes');
	CALL add_monthly_partition_for_table('dwh_hourly_events_entry');
	CALL add_monthly_partition_for_table('dwh_hourly_events_domain');
	CALL add_monthly_partition_for_table('dwh_hourly_events_country');
	CALL add_monthly_partition_for_table('dwh_hourly_events_widget');
	CALL add_monthly_partition_for_table('dwh_hourly_events_uid');
	CALL add_monthly_partition_for_table('dwh_hourly_events_domain_referrer');
	CALL add_monthly_partition_for_table('dwh_hourly_partner');
	CALL add_monthly_partition_for_table('dwh_hourly_partner_usage');
	CALL add_monthly_partition_for_table('dwh_hourly_events_devices');
	CALL add_monthly_partition_for_table('dwh_hourly_api_calls');
    CALL add_monthly_partition_for_table('dwh_hourly_errors');
	CALL add_monthly_partition_for_table('dwh_hourly_events_context_entry_user_app');
	CALL add_monthly_partition_for_table('dwh_hourly_events_context_app');
	CALL add_monthly_partition_for_table('dwh_hourly_user_usage');
	CALL add_monthly_partition_for_table('dwh_daily_ingestion');
	CALL add_monthly_partition_for_table('dwh_daily_partner_ingestion');
END$$

DELIMITER ;

DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `calc_updated_batch_job`$$

CREATE PROCEDURE `calc_updated_batch_job`(p_start_date INT(11), p_end_date INT(11))
BEGIN
                                
                BEGIN
				
                                DECLARE v_date_id INT(11);
                                DECLARE done INT DEFAULT 0;
                                DECLARE days_to_update CURSOR FOR 
                                SELECT day_id FROM kalturadw.dwh_dim_time WHERE day_id BETWEEN p_start_date AND p_end_date;
                                DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
                                
                                OPEN days_to_update;
								
                                read_loop: LOOP
                                                FETCH days_to_update INTO v_date_id;
                                                IF done THEN
                                                                LEAVE read_loop;
                                                END IF;
                                                CALL kalturadw.calc_updated_batch_job_day(v_date_id);
                                END LOOP;
                                CLOSE days_to_update;
                END;
				
END$$

DELIMITER ;

DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `calc_updated_batch_job_day`$$

CREATE PROCEDURE `calc_updated_batch_job_day`(p_date_id INT(11))
BEGIN
                DECLARE v_date DATETIME;
                DECLARE v_ignore_partner_ids TEXT;
                SET v_ignore_partner_ids = '';
				
                
                SELECT IFNULL(GROUP_CONCAT(ignore_partner.partner_id),'')
				INTO v_ignore_partner_ids
				FROM 
				(SELECT partner_id FROM kalturadw.dwh_dim_batch_job_sep WHERE job_type_id = 0 AND job_sub_type_id IN (1,2,3,99) AND updated_date_id = p_date_id
				GROUP BY partner_id
				HAVING COUNT(*) > 1000) ignore_partner;
                                
                
                SET @s = CONCAT("INSERT INTO kalturadw.dwh_fact_convert_job(id, job_type_id, status_id, created_date_id, updated_date_id, finish_date_id, partner_id, entry_id, dc, wait_time, conversion_time, is_ff)
				SELECT id, job_type_id, status_id, created_date_id, updated_date_id, DATE(finish_time)*1, partner_id, entry_id, dc, time_to_sec(timediff(queue_time, created_at)) wait_time, IF(finish_time IS NULL, -1, time_to_sec(timediff(finish_time, queue_time))) conversion_time, 0
				FROM kalturadw.dwh_dim_batch_job_sep WHERE job_type_id = 0 AND job_sub_type_id IN (1,2,3,99) AND priority <> 10 AND queue_time IS NOT NULL AND updated_date_id = ", p_date_id, IF(LENGTH(v_ignore_partner_ids)=0,"",CONCAT(" AND partner_id NOT IN (" , v_ignore_partner_ids, ")")),
				" ON DUPLICATE KEY UPDATE 
					status_id = VALUES(status_id),
					updated_date_id = VALUES(updated_date_id),
					finish_date_id = VALUES(finish_date_id),
					wait_time = VALUES(wait_time),
					conversion_time = VALUES(conversion_time);");
					
				PREPARE stmt FROM  @s;
				EXECUTE stmt;
				DEALLOCATE PREPARE stmt;	
					
				SELECT IFNULL(GROUP_CONCAT(ignore_partner.partner_id),'')
				INTO v_ignore_partner_ids
				FROM 
				(SELECT partner_id FROM kalturadw.dwh_dim_batch_job_sep WHERE job_type_id = 10 AND updated_date_id = p_date_id
				GROUP BY partner_id
				HAVING COUNT(*) > 1000) ignore_partner;
			
		DROP TABLE IF EXISTS kalturadw.tmp_convert_job_ids;
			
		SET @s = CONCAT("CREATE TEMPORARY TABLE kalturadw.tmp_convert_job_ids AS SELECT id FROM kalturadw.dwh_dim_batch_job_sep WHERE job_type_id = 10 AND priority <> 10 AND updated_date_id = ", p_date_id,
		IF(LENGTH(v_ignore_partner_ids)=0,"",CONCAT(" AND partner_id NOT IN (" , v_ignore_partner_ids, ")")), ";");
		
		PREPARE stmt FROM  @s;
		EXECUTE stmt;
		DEALLOCATE PREPARE stmt;	
				
                INSERT INTO kalturadw.dwh_fact_convert_job(id, job_type_id, status_id, created_date_id, updated_date_id, finish_date_id, partner_id, entry_id, dc, wait_time, conversion_time, is_ff)
                                SELECT id, job_type_id, status_id, created_date_id, updated_date_id, DATE(finish)*1, partner_id, c.entry_id, dc, TIME_TO_SEC(TIMEDIFF(queue_time, created_at)) wait_time, IF(finish IS NULL, -1, TIME_TO_SEC(TIMEDIFF(finish, queue_time))) conversion_time, 1 
				FROM (SELECT entry_id, root_job_id, MIN(finish_time) AS finish 
                FROM kalturadw.dwh_dim_batch_job_sep, tmp_convert_job_ids t WHERE root_job_id = t.id AND job_type_id = 0 AND job_sub_type_id IN (1,2,3,99) GROUP BY entry_id)
                AS c INNER JOIN kalturadw.dwh_dim_batch_job_sep batch_job ON c.root_job_id = batch_job.root_job_id AND c.finish =  batch_job.finish_time
                GROUP BY c.entry_id
				ON DUPLICATE KEY UPDATE 
					status_id = VALUES(status_id),
					updated_date_id = VALUES(updated_date_id),
					finish_date_id = VALUES(finish_date_id),
					wait_time = VALUES(wait_time),
					conversion_time = VALUES(conversion_time),
					is_ff = VALUES(is_ff);
                		
                                
                BEGIN
                                DECLARE v_created_date_id INT(11);
                                DECLARE done INT DEFAULT 0;
                                DECLARE days_to_aggregate CURSOR FOR 
                                SELECT DISTINCT(created_date_id) FROM kalturadw.dwh_fact_convert_job WHERE updated_date_id = p_date_id
                                AND MONTH(DATE(created_date_id) + INTERVAL 1 MONTH) >=  MONTH(DATE(p_date_id));
                                DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
                                
                                OPEN days_to_aggregate;
								
                                read_loop: LOOP
                                                FETCH days_to_aggregate INTO v_created_date_id;
                                                IF done THEN
                                                                LEAVE read_loop;
                                                END IF;
                                                INSERT INTO kalturadw.aggr_managment(aggr_name,date_id,hour_id,data_insert_time) 
												VALUES ("ingestion", v_created_date_id, 0 ,NOW())
                                                ON DUPLICATE KEY UPDATE
                                                                data_insert_time = VALUES(data_insert_time);
                                END LOOP;
                                CLOSE days_to_aggregate;
                END;
				
END$$

DELIMITER ;

DELIMITER $$

USE `kalturadw`$$

DROP FUNCTION IF EXISTS `calc_median_ff_convert_job_wait_time`$$

CREATE FUNCTION `calc_median_ff_convert_job_wait_time`(p_date_id INT(11)) RETURNS INT(11)
    DETERMINISTIC
BEGIN
	DECLARE v_median INT(11);
	SET v_median = 0;
	SELECT t1.wait_time AS median_val INTO v_median FROM (
	SELECT @rownum:=@rownum+1 AS `row_number`, IF(d.wait_time>0, d.wait_time, 0) wait_time
	FROM kalturadw.dwh_fact_convert_job d,  (SELECT @rownum:=0) r
	WHERE created_date_id = p_date_id AND is_ff = 1 
	ORDER BY d.wait_time
	) AS t1, 
	(
	SELECT COUNT(*) AS total_rows
	FROM kalturadw.dwh_fact_convert_job d
	WHERE created_date_id = p_date_id AND is_ff = 1 
	) AS t2
	WHERE 1
	AND t1.row_number=FLOOR(total_rows/2)+1;
	
	RETURN v_median;
    END$$

DELIMITER ;

DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `calc_aggr_day_ingestion`$$

CREATE PROCEDURE `calc_aggr_day_ingestion`(p_date_id INT(11))
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

USE `kalturadw`;

DROP TABLE IF EXISTS `dwh_fact_convert_job`;

CREATE TABLE `dwh_fact_convert_job` (
  `id` int(11) NOT NULL,
  `job_type_id` int(11) DEFAULT NULL,
  `status_id` int(11) DEFAULT NULL,
  `partner_id` int(11) DEFAULT NULL,
  `created_date_id` int(11) DEFAULT '-1',
  `updated_date_id` int(11) DEFAULT '-1',
  `finish_date_id` int(11) DEFAULT '-1',
  `entry_id` varchar(20) DEFAULT NULL,
  `dc` int(11) DEFAULT NULL,
  `wait_time` int(22) DEFAULT NULL,
  `conversion_time` int(22) DEFAULT NULL,
  `is_ff` int(2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `dwh_created_date_id` (`created_date_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

/* 6143 */
USE `kalturadw`;

DROP TABLE IF EXISTS kalturadw.`dwh_hourly_events_context_app_devices`;

CREATE TABLE kalturadw.`dwh_hourly_events_context_app_devices` (
  `partner_id` INT NOT NULL DEFAULT -1,
  `date_id` INT NOT NULL,
  `hour_id` INT NOT NULL,
  `context_id` INT NOT NULL DEFAULT -1,
  `application_id` INT NOT NULL DEFAULT -1,
  `os_id` INT NOT NULL DEFAULT -1,
  `browser_id` INT NOT NULL DEFAULT -1,
  `sum_time_viewed` DECIMAL(20,3) DEFAULT NULL,
  `count_time_viewed` INT DEFAULT NULL,
  `count_plays` INT DEFAULT NULL,
  `count_loads` INT DEFAULT NULL,
  `count_plays_25` INT DEFAULT NULL,
  `count_plays_50` INT DEFAULT NULL,
  `count_plays_75` INT DEFAULT NULL,
  `count_plays_100` INT DEFAULT NULL,
  `count_edit` INT DEFAULT NULL,
  `count_viral` INT DEFAULT NULL,
  `count_download` INT DEFAULT NULL,
  `count_report` INT DEFAULT NULL,
  `count_buf_start` INT DEFAULT NULL,
  `count_buf_end` INT DEFAULT NULL,
  `count_open_full_screen` INT DEFAULT NULL,
  `count_close_full_screen` INT DEFAULT NULL,
  `count_replay` INT DEFAULT NULL,
  `count_seek` INT DEFAULT NULL,
  `count_open_upload` INT DEFAULT NULL,
  `count_save_publish` INT DEFAULT NULL,
  `count_close_editor` INT DEFAULT NULL,    
  `count_pre_bumper_played` INT DEFAULT NULL,
  `count_post_bumper_played` INT DEFAULT NULL,
  `count_bumper_clicked` INT DEFAULT NULL,
  `count_preroll_started` INT DEFAULT NULL,
  `count_midroll_started` INT DEFAULT NULL,
  `count_postroll_started` INT DEFAULT NULL,
  `count_overlay_started` INT DEFAULT NULL,
  `count_preroll_clicked` INT DEFAULT NULL,
  `count_midroll_clicked` INT DEFAULT NULL,
  `count_postroll_clicked` INT DEFAULT NULL,
  `count_overlay_clicked` INT DEFAULT NULL,
  `count_preroll_25` INT DEFAULT NULL,
  `count_preroll_50` INT DEFAULT NULL,
  `count_preroll_75` INT DEFAULT NULL,
  `count_midroll_25` INT DEFAULT NULL,
  `count_midroll_50` INT DEFAULT NULL,
  `count_midroll_75` INT DEFAULT NULL,
  `count_postroll_25` INT DEFAULT NULL,
  `count_postroll_50` INT DEFAULT NULL,
  `count_postroll_75` INT DEFAULT NULL,
  `count_bandwidth_kb` INT DEFAULT NULL,
  `total_admins` INT DEFAULT NULL,
  `total_media_entries` INT DEFAULT NULL,
  PRIMARY KEY `partner_id` (`partner_id`,`date_id`,`hour_id`,`context_id`,`application_id`,`os_id`,`browser_id`),
  KEY (`date_id`, `hour_id`)
) ENGINE=INNODB DEFAULT CHARSET=utf8
PARTITION BY RANGE (date_id)
(PARTITION @PARTITION_NAME@ VALUES LESS THAN (@PARTITION_VALUE@) ENGINE = INNODB);

CALL kalturadw.add_monthly_partition_for_table('dwh_hourly_events_context_app_devices');

DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `add_partitions`$$

CREATE PROCEDURE `add_partitions`()
BEGIN
	CALL add_daily_partition_for_table('dwh_fact_events');
	CALL add_daily_partition_for_table('dwh_fact_fms_session_events');
	CALL add_daily_partition_for_table('dwh_fact_fms_sessions');
	CALL add_daily_partition_for_table('dwh_fact_bandwidth_usage');
	CALL add_daily_partition_for_table('dwh_fact_api_calls');
	CALL add_daily_partition_for_table('dwh_fact_incomplete_api_calls');
    CALL add_daily_partition_for_table('dwh_fact_errors');
    CALL add_daily_partition_for_table('dwh_fact_file_sync');
	CALL add_monthly_partition_for_table('dwh_fact_entries_sizes');
	CALL add_monthly_partition_for_table('dwh_hourly_events_entry');
	CALL add_monthly_partition_for_table('dwh_hourly_events_domain');
	CALL add_monthly_partition_for_table('dwh_hourly_events_country');
	CALL add_monthly_partition_for_table('dwh_hourly_events_widget');
	CALL add_monthly_partition_for_table('dwh_hourly_events_uid');
	CALL add_monthly_partition_for_table('dwh_hourly_events_domain_referrer');
	CALL add_monthly_partition_for_table('dwh_hourly_partner');
	CALL add_monthly_partition_for_table('dwh_hourly_partner_usage');
	CALL add_monthly_partition_for_table('dwh_hourly_events_devices');
	CALL add_monthly_partition_for_table('dwh_hourly_api_calls');
    CALL add_monthly_partition_for_table('dwh_hourly_errors');
	CALL add_monthly_partition_for_table('dwh_hourly_events_context_entry_user_app');
	CALL add_monthly_partition_for_table('dwh_hourly_events_context_app');
	CALL add_monthly_partition_for_table('dwh_hourly_user_usage');
	CALL add_monthly_partition_for_table('dwh_daily_ingestion');
	CALL add_monthly_partition_for_table('dwh_daily_partner_ingestion');
	CALL add_monthly_partition_for_table('dwh_hourly_events_context_app_devices');
	
END$$

DELIMITER ;

INSERT INTO kalturadw_ds.aggr_name_resolver (aggr_name, aggr_table, aggr_id_field, dim_id_field, aggr_type)
VALUES ('app_devices', 'dwh_hourly_events_context_app_devices', 'context_id,application_id,os_id,browser_id', '', 'events');

UPDATE kalturadw_ds.staging_areas  SET post_transfer_aggregations = REPLACE(post_transfer_aggregations, ')',',\'app_devices\')') WHERE process_id in (1,3);

/* 6145 */ 
ALTER TABLE kalturadw.dwh_dim_file_sync 
CHANGE COLUMN id id BIGINT(20),
ADD COLUMN deleted_id BIGINT(20) DEFAULT '0' AFTER `ri_ind`;

ALTER TABLE kalturadw.dwh_dim_file_sync 
DROP INDEX unique_key;

ALTER TABLE kalturadw.dwh_dim_file_sync 
ADD UNIQUE KEY unique_index (object_id,object_type,object_sub_type,version,dc,deleted_id);

/* 6146 */
DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `calc_entries_sizes`$$

CREATE PROCEDURE `calc_entries_sizes`(p_date_id INT(11))
BEGIN
                DECLARE v_date DATETIME;
                SET v_date = DATE(p_date_id);
                UPDATE aggr_managment SET start_time = NOW() WHERE aggr_name = 'storage_usage' AND date_id = p_date_id;
                
                DELETE FROM kalturadw.dwh_fact_entries_sizes WHERE entry_size_date_id = p_date_id;
                
                DROP TABLE IF EXISTS today_file_sync_subset; 
                
                CREATE TEMPORARY TABLE today_file_sync_subset AS
                SELECT DISTINCT s.id, s.partner_id, IFNULL(a.entry_id, object_id) entry_id, object_id, object_type, object_sub_type, s.created_at, s.status, IFNULL(file_size, 0) file_size
                FROM kalturadw.dwh_dim_file_sync s LEFT OUTER JOIN kalturadw.dwh_dim_flavor_asset a
                ON (object_type = 4 AND s.object_id = a.id AND a.entry_id IS NOT NULL AND a.ri_ind =0 AND s.partner_id = a.partner_id)
                WHERE s.ready_at BETWEEN v_date AND v_date + INTERVAL 1 DAY
                AND object_type IN (1,4)
                AND original = 1
                AND s.STATUS IN (2,3,4)
				AND s.dc IN (0,1)
                AND s.partner_id NOT IN ( -1  , -2  , 0 , 99 );
                
                ALTER TABLE today_file_sync_subset ADD INDEX id (`id`);            
                
                DROP TABLE IF EXISTS today_latest_file_sync;
                CREATE TEMPORARY TABLE today_latest_file_sync AS
                SELECT MAX(created_at) created_at, partner_id, entry_id, object_id, object_type, object_sub_type FROM today_file_sync_subset
                GROUP BY partner_id, entry_id, object_id, object_type, object_sub_type;
                
                DROP TABLE IF EXISTS today_file_sync_max_version_ids;
                
                CREATE TEMPORARY TABLE today_file_sync_max_version_ids AS
				SELECT today_file_sync_subset.id
				FROM today_file_sync_subset, today_latest_file_sync
				WHERE today_latest_file_sync.created_at = today_file_sync_subset.created_at
				AND today_latest_file_sync.partner_id = today_file_sync_subset.partner_id
				AND today_latest_file_sync.entry_id = today_file_sync_subset.entry_id
				AND today_latest_file_sync.object_id = today_file_sync_subset.object_id
				AND today_latest_file_sync.object_type = today_file_sync_subset.object_type
				AND today_latest_file_sync.object_sub_type = today_file_sync_subset.object_sub_type;
                
				
		DROP TABLE IF EXISTS today_sizes;
		CREATE TEMPORARY TABLE today_sizes(
			partner_id          INT(11) NOT NULL,
			entry_id 			VARCHAR(60) NOT NULL,
			object_id 			VARCHAR(60) NOT NULL,
			object_type         TINYINT(4) NOT NULL,
			object_sub_type     TINYINT(4) NOT NULL,
			created_at          DATETIME NOT NULL,        
			STATUS              TINYINT(4) NOT NULL,
			file_size           BIGINT (20),
			UNIQUE KEY `unique_key` (`partner_id`, `entry_id`, `object_id`, `object_type`, `object_sub_type`)
		) ENGINE = MEMORY; 

                
		INSERT INTO today_sizes(partner_id, entry_id, object_id, object_type, object_sub_type, created_at, STATUS, file_size)
                SELECT original.partner_id, original.entry_id, original.object_id, original.object_type, original.object_sub_type, original.created_at, original.status, original.file_size 
                FROM today_file_sync_max_version_ids max_id, today_file_sync_subset original
                WHERE max_id.id = original.id
				ORDER BY original.status DESC
				ON DUPLICATE KEY UPDATE 
					STATUS = VALUES(STATUS),
					file_size = VALUES(file_size);

                
           
                INSERT INTO today_sizes
                                SELECT s.partner_id, IFNULL(a.entry_id, object_id) entry_id, object_id, object_type, object_sub_type, s.created_at, s.status, 0 file_size
                                FROM kalturadw.dwh_dim_file_sync s LEFT OUTER JOIN kalturadw.dwh_dim_flavor_asset a
                                ON (object_type = 4 AND s.object_id = a.id AND a.entry_id IS NOT NULL AND a.ri_ind =0 AND s.partner_id = a.partner_id)
                                WHERE s.updated_at BETWEEN v_date AND v_date + INTERVAL 1 DAY
                                AND object_type IN (1,4)
                                AND original = 1
                                AND s.STATUS IN (3,4)
                                AND s.partner_id NOT IN ( -1  , -2  , 0 , 99 )
                ON DUPLICATE KEY UPDATE
                                file_size = IF((VALUES(created_at) > today_sizes.created_at) OR (VALUES(created_at)=today_sizes.created_at AND today_sizes.STATUS IN (3,4)), 0, today_sizes.file_size);       			
                                
                DROP TABLE IF EXISTS deleted_flavors;
                
                CREATE TEMPORARY TABLE deleted_flavors AS 
                SELECT DISTINCT partner_id, entry_id, id
                FROM kalturadw.dwh_dim_flavor_asset FORCE INDEX (deleted_at)
                WHERE STATUS = 3 AND deleted_at BETWEEN v_date AND v_date + INTERVAL 1 DAY
                AND partner_id NOT IN (100  , -1  , -2  , 0 , 99 );
                                
                BEGIN
                                DECLARE v_deleted_flavor_partner_id INT;
                                DECLARE v_deleted_flavor_entry_id VARCHAR(60);
                                DECLARE v_deleted_flavor_id VARCHAR(60);
                                DECLARE done INT DEFAULT 0;
				DECLARE v_status TINYINT(4);
                                DECLARE deleted_flavors_cursor CURSOR FOR 
                                SELECT partner_id, entry_id, id  FROM deleted_flavors;
                                DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
                                
                                OPEN deleted_flavors_cursor;
								
                                read_loop: LOOP
                                                FETCH deleted_flavors_cursor INTO v_deleted_flavor_partner_id, v_deleted_flavor_entry_id, v_deleted_flavor_id;
                                                IF done THEN
                                                                LEAVE read_loop;
                                                END IF;
												
												SELECT entry_status_id
												INTO v_status
												FROM kalturadw.dwh_dim_entries
												WHERE entry_id = v_deleted_flavor_entry_id;
												
												IF v_STATUS <> 3 THEN
													INSERT INTO today_sizes
																	SELECT v_deleted_flavor_partner_id, v_deleted_flavor_entry_id, object_id, object_type, object_sub_type, MAX(created_at), 3 STATUS, 0 file_size
																	FROM kalturadw.dwh_dim_file_sync
																	WHERE object_id = v_deleted_flavor_id AND object_type = 4 AND ready_at < v_date AND file_size > 0
																	GROUP BY object_id, object_type, object_sub_type
													ON DUPLICATE KEY UPDATE
																	file_size = VALUES(file_size);
												END IF;
                                END LOOP;
                                CLOSE deleted_flavors_cursor;
                END;
                
                
                
                DROP TABLE IF EXISTS today_deleted_entries;
                CREATE TEMPORARY TABLE today_deleted_entries AS 
                SELECT entry_id, partner_id FROM kalturadw.dwh_dim_entries
                WHERE modified_at BETWEEN v_date AND v_date + INTERVAL 1 DAY
                AND partner_id NOT IN (100  , -1  , -2  , 0 , 99 )
                AND entry_status_id = 3
                AND entry_type_id = 1;                
                
                DELETE today_sizes FROM today_sizes, today_deleted_entries e 
                                WHERE today_sizes.entry_id = e.entry_id;
                
                ALTER TABLE today_sizes DROP INDEX unique_key;
                
                DROP TABLE IF EXISTS yesterday_file_sync_subset; 
                CREATE TEMPORARY TABLE yesterday_file_sync_subset AS
                SELECT f.id, f.partner_id, f.object_id, f.object_type, f.object_sub_type, f.created_at, IFNULL(f.file_size, 0) file_size
                FROM today_sizes today, kalturadw.dwh_dim_file_sync f
                WHERE f.object_id = today.object_id
                AND f.partner_id = today.partner_id
                AND f.object_type = today.object_type
                AND f.object_sub_type = today.object_sub_type
                AND f.ready_at < v_date
                AND f.original = 1
				AND f.dc IN (0,1)
                AND f.STATUS IN (2,3,4);
                
                
                
		DROP TABLE IF EXISTS yesterday_latest_file_sync;
                CREATE TEMPORARY TABLE yesterday_latest_file_sync AS
                SELECT MAX(created_at) created_at, partner_id, object_id, object_type, object_sub_type FROM yesterday_file_sync_subset
                GROUP BY partner_id, object_id, object_type, object_sub_type;
                
                DROP TABLE IF EXISTS yesterday_file_sync_max_version_ids;
                
                CREATE TEMPORARY TABLE yesterday_file_sync_max_version_ids AS
				SELECT yesterday_file_sync_subset.id
				FROM yesterday_file_sync_subset, yesterday_latest_file_sync
				WHERE yesterday_latest_file_sync.created_at = yesterday_file_sync_subset.created_at
				AND yesterday_latest_file_sync.partner_id = yesterday_file_sync_subset.partner_id
				AND yesterday_latest_file_sync.object_id = yesterday_file_sync_subset.object_id
				AND yesterday_latest_file_sync.object_type = yesterday_file_sync_subset.object_type
				AND yesterday_latest_file_sync.object_sub_type = yesterday_file_sync_subset.object_sub_type;
                
		
                DROP TABLE IF EXISTS yesterday_sizes;
                CREATE TEMPORARY TABLE yesterday_sizes AS
                SELECT original.partner_id, original.object_id, original.object_type, original.object_sub_type, original.file_size 
                FROM yesterday_file_sync_max_version_ids max_id, yesterday_file_sync_subset original
                WHERE max_id.id = original.id;
                
                
                INSERT INTO kalturadw.dwh_fact_entries_sizes (partner_id, entry_id, entry_additional_size_kb, entry_size_date, entry_size_date_id)
                SELECT t.partner_id, t.entry_id, ROUND(SUM(t.file_size - IFNULL(Y.file_size, 0))/1024, 3) entry_additional_size_kb, v_date, p_date_id 
                FROM today_sizes t LEFT OUTER JOIN yesterday_sizes Y 
                ON t.object_id = Y.object_id
                AND t.partner_id = Y.partner_id
                AND t.object_type = Y.object_type
                AND t.object_sub_type = Y.object_sub_type
                AND t.file_size <> Y.file_size
                GROUP BY t.partner_id, t.entry_id
                HAVING entry_additional_size_kb <> 0
                ON DUPLICATE KEY UPDATE 
                                entry_additional_size_kb = VALUES(entry_additional_size_kb);
                
                
                DROP TABLE IF EXISTS deleted_entries;
                CREATE TEMPORARY TABLE deleted_entries AS
                                SELECT es.partner_id partner_id, es.entry_id entry_id, v_date entry_size_date, p_date_id entry_size_date_id, -SUM(entry_additional_size_kb) entry_additional_size_kb
                                FROM today_deleted_entries e, kalturadw.dwh_fact_entries_sizes es
                                WHERE e.entry_id = es.entry_id 
                                                AND e.partner_id = es.partner_id 
                                                AND es.entry_size_date_id < p_date_id
                                GROUP BY es.partner_id, es.entry_id
                                HAVING SUM(entry_additional_size_kb) > 0;
                
                INSERT INTO kalturadw.dwh_fact_entries_sizes (partner_id, entry_id, entry_size_date, entry_size_date_id, entry_additional_size_kb)
                                SELECT partner_id, entry_id, entry_size_date, entry_size_date_id, entry_additional_size_kb FROM deleted_entries
                ON DUPLICATE KEY UPDATE 
                                entry_additional_size_kb = VALUES(entry_additional_size_kb);
                
                CALL kalturadw.calc_aggr_day_partner_storage(v_date);
                UPDATE aggr_managment SET end_time = NOW() WHERE aggr_name = 'storage_usage' AND date_id = p_date_id;
END$$

DELIMITER ;



CALL kalturadw.add_partitions();