DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `get_data_for_operational`$$

CREATE PROCEDURE `get_data_for_operational`(p_sync_type VARCHAR(55))
BEGIN
	DECLARE v_execution_start_time DATETIME;
	
	DECLARE v_group_column VARCHAR(1024);
	DECLARE v_entity_table VARCHAR(1024);
	DECLARE v_aggregation_phrase VARCHAR(1024);
	DECLARE v_aggregation_table VARCHAR(1024);
	DECLARE v_bridge_entity VARCHAR(1024);
	DECLARE v_bridge_table VARCHAR(1024);
	DECLARE v_last_execution_parameter_id INT;
	DECLARE v_execution_start_time_parameter_id INT;
	
	SET v_execution_start_time = NOW();
   
	SELECT group_column, entity_table, aggregation_phrase, aggregation_table, 
            bridge_entity, bridge_table, last_execution_parameter_id, execution_start_time_parameter_id
        INTO	v_group_column, v_entity_table, v_aggregation_phrase, v_aggregation_table, 
            v_bridge_entity, v_bridge_table, v_last_execution_parameter_id, v_execution_start_time_parameter_id
        FROM kalturadw_ds.operational_syncs WHERE operational_sync_name = p_sync_type;
        UPDATE kalturadw_ds.parameters	SET date_value = v_execution_start_time WHERE id = v_execution_start_time_parameter_id;
    
    IF p_sync_type='entry' THEN 
    
	SELECT e.entry_id, e.plays, e.views
        FROM dwh_entry_plays_views e, kalturadw_ds.parameters p, kalturadw.dwh_dim_entries d
        WHERE e.updated_at > p.date_value AND p.id = 4 AND e.entry_id = d.entry_id;
    
    ELSE
    
        SET @s = CONCAT('SELECT dim.', v_group_column,', ', v_aggregation_phrase, 
                ' FROM ', v_aggregation_table ,' aggr, ', IF (v_bridge_table IS NULL, '', CONCAT(v_bridge_table, ' bridge, ')), v_entity_table, ' dim, kalturadw_ds.parameters p',
                ' WHERE aggr.', IF(v_bridge_entity IS NULL, v_group_column, 
                            CONCAT(v_bridge_entity, ' = bridge.',v_bridge_entity, ' AND bridge.', v_group_column)), 
                ' = dim.', v_group_column, ' AND dim.operational_measures_updated_at > p.date_value AND p.id = ', v_last_execution_parameter_id,
                ' GROUP BY dim.',v_group_column);
        
        PREPARE stmt FROM  @s;
        EXECUTE stmt;
        DEALLOCATE PREPARE stmt;
        
    END IF;
END$$

DELIMITER ;

ALTER TABLE kalturadw_ds.locks MODIFY lock_name varchar(265) DEFAULT NULL;

-- 6147
UPDATE kalturadw.dwh_dim_bandwidth_source SET bandwidth_source_name = 'akamai_HD_1.0' WHERE bandwidth_source_id = 7;
REPLACE INTO kalturadw.dwh_dim_bandwidth_source (bandwidth_source_id,bandwidth_source_name, is_live) values (8,'akamai_HD_2.0(HDS)', 0);

DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `calc_aggr_day_bandwidth`$$

CREATE PROCEDURE `calc_aggr_day_bandwidth`(p_date_val DATE, p_aggr_name VARCHAR(100))
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
	
	IF (p_date_val >= v_ignore) THEN 
		
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
	
                IF (p_date_val >= v_from_archive) THEN 
                        SET v_table_name = 'dwh_fact_bandwidth_usage';
                ELSE
                        SET v_table_name = 'dwh_fact_bandwidth_usage_archive';
                END IF;
                
		SET @s = CONCAT('INSERT INTO kalturadw.', v_aggr_table, ' (partner_id, date_id, hour_id ', v_aggr_id_field_str,', count_bandwidth_kb)'
				'SELECT partner_id, MAX(activity_date_id), 0 hour_id', v_aggr_id_field_str,', SUM(bandwidth_bytes)/1024 count_bandwidth
				FROM ', v_table_name, '	WHERE activity_date_id=date(\'',p_date_val,'\')*1
				GROUP BY partner_id', v_aggr_id_field_str,'
				ON DUPLICATE KEY UPDATE	count_bandwidth_kb=IFNULL(count_bandwidth_kb,0) + VALUES(count_bandwidth_kb)');
	

		PREPARE stmt FROM  @s;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;
			
		/* FMS */
		SELECT DATE(archive_last_partition)
		INTO v_from_archive
		FROM kalturadw_ds.retention_policy
		WHERE table_name = 'dwh_fact_fms_sessions';
		
		IF (p_date_val >= v_from_archive) THEN 
                        SET v_table_name = 'dwh_fact_fms_sessions';
                ELSE
                        SET v_table_name = 'dwh_fact_fms_sessions_archive';
                END IF;

		SET @s = CONCAT('INSERT INTO kalturadw.', v_aggr_table, ' (partner_id, date_id, hour_id', v_aggr_id_field_str,', count_bandwidth_kb)
				SELECT session_partner_id, MAX(session_date_id), 0 hour_id', v_aggr_id_field_str,', SUM(total_bytes)/1024 count_bandwidth 
				FROM ', v_table_name, ' WHERE session_date_id=date(\'',p_date_val,'\')*1
				GROUP BY session_partner_id', v_aggr_id_field_str,'
				ON DUPLICATE KEY UPDATE	count_bandwidth_kb=IFNULL(count_bandwidth_kb,0) + VALUES(count_bandwidth_kb)');
		PREPARE stmt FROM  @s;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;
	
	END IF;
	
	UPDATE aggr_managment SET end_time = NOW() WHERE aggr_name = p_aggr_name AND date_id = DATE(p_date_val)*1;
END$$

DELIMITER ;

DROP TABLE IF EXISTS kalturadw.`dwh_dim_http_delivery_source`;

CREATE TABLE kalturadw.`dwh_dim_http_delivery_source` (
  `process_id` INT(10) NOT NULL,
  `bandwidth_source_id` INT(11) NOT NULL,
  `file_regex` VARCHAR(100) NOT NULL DEFAULT '.*',
  UNIQUE KEY (`process_id`,`bandwidth_source_id`, `file_regex`)
);

REPLACE INTO kalturadw.`dwh_dim_http_delivery_source`
			(`process_id`,`bandwidth_source_id`,`file_regex`) 
VALUES 		(4,4,'_77660\\.|_113110\.|_146829\\.'),(4,7,'_105515\\.|_146836\\.|_146832\\.'),(4,8,'_159949\.'),(6,3,'.*');

-- 6148

DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `calc_aggr_day_user_usage`$$

CREATE PROCEDURE `calc_aggr_day_user_usage`(p_date_id INT(11))
BEGIN
    DECLARE v_date DATETIME;
    SET v_date = DATE(p_date_id);
	
    UPDATE aggr_managment SET start_time = NOW() WHERE aggr_name = 'user_storage_usage' AND date_id = p_date_id;
    
    DROP TABLE IF EXISTS temp_aggr_storage;
    CREATE TEMPORARY TABLE temp_aggr_storage(
        partner_id          INT(11) NOT NULL,
        kuser_id            INT(11) NOT NULL,
        added_storage_kb    DECIMAL(19,4) NOT NULL DEFAULT 0.0000,
        deleted_storage_kb  DECIMAL(19,4) NOT NULL DEFAULT 0.0000
    ) ENGINE = MEMORY;
    
    ALTER TABLE temp_aggr_storage ADD INDEX index_1 (kuser_id);  
    
    INSERT INTO     temp_aggr_storage (partner_id, kuser_id, added_storage_kb, deleted_storage_kb)
    SELECT         e.partner_id, e.kuser_id, SUM(IF(f.entry_additional_size_kb > 0,entry_additional_size_kb,0)),SUM(IF(f.entry_additional_size_kb < 0,entry_additional_size_kb*-1,0))
    FROM         dwh_fact_entries_sizes f, dwh_dim_entries e
    WHERE        entry_size_date_id=p_date_id
    AND          f.entry_id = e.entry_id
    AND          e.entry_type_id IN (1,2,7,10)
    GROUP BY     e.kuser_id, e.partner_id;
    
    DROP TABLE IF EXISTS entries_prev_owner;
    CREATE TEMPORARY TABLE entries_prev_owner AS
    SELECT partner_id, entry_id, prev_kuser_id, kuser_id 
    FROM dwh_dim_entries
    WHERE prev_kuser_id IS NOT NULL
	AND updated_at >= v_date
    AND IFNULL(kuser_updated_date_id,-1) = p_date_id
    AND IFNULL(created_date_id, -1) <> p_date_id
    AND entry_type_id IN (1,2,7,10);
 
    ALTER TABLE entries_prev_owner ADD INDEX index_1 (kuser_id);
    
    INSERT INTO  temp_aggr_storage (partner_id, kuser_id, added_storage_kb, deleted_storage_kb)
    SELECT       o.partner_id, o.prev_kuser_id, 0, SUM(f.entry_additional_size_kb)
    FROM         dwh_fact_entries_sizes f, entries_prev_owner o
    WHERE        f.entry_id = o.entry_id
    AND          f.entry_size_date_id < p_date_id
	AND          o.prev_kuser_id <> -1
    GROUP BY     o.prev_kuser_id, o.partner_id;
    
    
    INSERT INTO  temp_aggr_storage (partner_id, kuser_id, added_storage_kb, deleted_storage_kb)
    SELECT       o.partner_id, o.kuser_id, SUM(f.entry_additional_size_kb), 0
    FROM         dwh_fact_entries_sizes f, entries_prev_owner o
    WHERE        f.entry_id = o.entry_id
    AND          f.entry_size_date_id < p_date_id
	AND          o.kuser_id <> -1
    GROUP BY     o.kuser_id, o.partner_id;
    
    DROP TABLE IF EXISTS temp_aggr_entries;
    CREATE TEMPORARY TABLE temp_aggr_entries(
        partner_id          INT(11) NOT NULL,
        kuser_id             INT(11) NOT NULL,
        added_entries    INT(11) NOT NULL DEFAULT 0,
        deleted_entries  INT(11) NOT NULL DEFAULT 0,
        added_msecs INT(11) NOT NULL DEFAULT 0,
        deleted_msecs INT(11) NOT NULL DEFAULT 0
        
    ) ENGINE = MEMORY; 
    
    ALTER TABLE temp_aggr_entries ADD INDEX index_1 (`kuser_id`);
    
    INSERT INTO temp_aggr_entries(partner_id, kuser_id, added_entries, deleted_entries, added_msecs, deleted_msecs)
    SELECT partner_id, kuser_id,
    SUM(IF((entry_status_id <> 3 AND ((IFNULL(created_date_id,-1) = p_date_id AND IFNULL(created_date_id,-1) >= IFNULL(kuser_updated_date_id,-1)) OR IFNULL(kuser_updated_date_id,-1) = p_date_id))
		OR (entry_status_id = 3 AND IFNULL(updated_date_id,-1) <> p_date_id AND ((IFNULL(created_date_id,-1) = p_date_id AND IFNULL(created_date_id,-1) >= IFNULL(kuser_updated_date_id,-1)) OR IFNULL(kuser_updated_date_id,-1) = p_date_id)),1,0)),
    SUM(IF(entry_status_id = 3 AND (IFNULL(created_date_id,-1) <> p_date_id AND IFNULL(kuser_updated_date_id,-1) <> p_date_id),1,0)),
    SUM(IF((entry_status_id <> 3 AND ((IFNULL(created_date_id,-1) = p_date_id AND IFNULL(created_date_id,-1) >= IFNULL(kuser_updated_date_id,-1)) OR IFNULL(kuser_updated_date_id,-1) = p_date_id))
		OR (entry_status_id = 3 AND IFNULL(updated_date_id,-1) <> p_date_id AND ((IFNULL(created_date_id,-1) = p_date_id AND IFNULL(created_date_id,-1) >= IFNULL(kuser_updated_date_id,-1)) OR IFNULL(kuser_updated_date_id,-1) = p_date_id)),length_in_msecs,0)),
    SUM(IF(entry_status_id = 3 AND (IFNULL(created_date_id,-1) <> p_date_id AND IFNULL(kuser_updated_date_id,-1) <> p_date_id),length_in_msecs,0))
    FROM dwh_dim_entries e
    WHERE updated_at >= v_date AND (updated_at <= v_date + INTERVAL 1 DAY 
			OR IFNULL(created_date_id , -1) = p_date_id
			OR IFNULL(kuser_updated_date_id,-1) = p_date_id)
    AND e.entry_type_id IN (1,2,7,10)
    GROUP BY kuser_id, partner_id;
    
    INSERT INTO temp_aggr_entries(partner_id, kuser_id, added_entries, deleted_entries, added_msecs, deleted_msecs)
    SELECT o.partner_id, o.prev_kuser_id, 0, COUNT(*), 0, SUM(length_in_msecs)
    FROM entries_prev_owner o, dwh_dim_entries e
    WHERE o.entry_id = e.entry_id
    GROUP BY o.prev_kuser_id, o.partner_id;
   
    
    DELETE FROM dwh_hourly_user_usage USING temp_aggr_storage, dwh_hourly_user_usage
    WHERE dwh_hourly_user_usage.partner_id = temp_aggr_storage.partner_id 
    AND dwh_hourly_user_usage.kuser_id = temp_aggr_storage.kuser_id 
    AND dwh_hourly_user_usage.date_id = p_date_id;
    
    DROP TABLE IF EXISTS latest_total;
    CREATE TEMPORARY TABLE latest_total(
        partner_id          INT(11) NOT NULL,
        kuser_id             INT(11) NOT NULL,
        total_storage_kb    DECIMAL(19,4) NOT NULL DEFAULT 0,
        total_entries  INT(11) NOT NULL DEFAULT 0,
        total_msecs INT(11) NOT NULL DEFAULT 0
        
    ) ENGINE = MEMORY; 
    ALTER TABLE latest_total ADD INDEX index_1 (kuser_id);


    INSERT INTO latest_total (partner_id, kuser_id, total_storage_kb, total_entries, total_msecs)
    SELECT u.partner_id, u.kuser_id, IFNULL(u.total_storage_kb,0), IFNULL(u.total_entries,0), IFNULL(u.total_msecs,0)
    FROM dwh_hourly_user_usage u JOIN (SELECT kuser_id, partner_id, MAX(date_id) AS date_id FROM dwh_hourly_user_usage WHERE date_id < p_date_id GROUP BY kuser_id, partner_id) MAX
          ON u.kuser_id = max.kuser_id AND u.date_id = max.date_id AND u.partner_id = max.partner_id; 
          
    INSERT INTO dwh_hourly_user_usage (partner_id, kuser_id, date_id, hour_id, added_storage_kb, deleted_storage_kb, total_storage_kb, added_entries, deleted_entries, total_entries, added_msecs, deleted_msecs, total_msecs)
    SELECT      aggr.partner_id, aggr.kuser_id, p_date_id, 0, SUM(added_storage_kb), SUM(deleted_storage_kb), SUM(added_storage_kb) - SUM(deleted_storage_kb) + IFNULL(latest_total.total_storage_kb,0),
                0, 0, IFNULL(latest_total.total_entries,0), 0, 0,  IFNULL(latest_total.total_msecs,0)
    FROM        temp_aggr_storage aggr LEFT JOIN latest_total ON aggr.kuser_id = latest_total.kuser_id AND aggr.partner_id = latest_total.partner_id
    WHERE added_storage_kb <> 0 OR deleted_storage_kb <> 0
    GROUP BY    aggr.kuser_id, aggr.partner_id;
        
    INSERT INTO dwh_hourly_user_usage (partner_id, kuser_id, date_id, hour_id, added_storage_kb, deleted_storage_kb, total_storage_kb, added_entries, deleted_entries, total_entries, added_msecs, deleted_msecs, total_msecs)
    SELECT         aggr.partner_id, aggr.kuser_id, p_date_id, 0, 0, 0, IFNULL(latest_total.total_storage_kb,0), SUM(added_entries), SUM(deleted_entries), SUM(added_entries) - SUM(deleted_entries) + IFNULL(latest_total.total_entries,0),
            SUM(added_msecs), SUM(deleted_msecs), SUM(added_msecs) - SUM(deleted_msecs) + IFNULL(latest_total.total_msecs,0)
    FROM         temp_aggr_entries aggr LEFT JOIN latest_total ON aggr.kuser_id = latest_total.kuser_id AND aggr.partner_id = latest_total.partner_id
    WHERE added_entries <> 0 OR added_msecs <> 0 OR deleted_entries <> 0 OR deleted_msecs <> 0
    GROUP BY     aggr.kuser_id, aggr.partner_id
    ON DUPLICATE KEY UPDATE added_entries = VALUES(added_entries), deleted_entries = VALUES(deleted_entries), total_entries=VALUES(total_entries), 
                            added_msecs=VALUES(added_msecs), deleted_msecs=VALUES(deleted_msecs), total_msecs=VALUES(total_msecs);
    
    
    UPDATE aggr_managment SET end_time = NOW() WHERE aggr_name = 'user_storage_usage' AND date_id = p_date_id; 
 
END$$

DELIMITER ;

-- 6149

REPLACE INTO kalturadw_ds.processes (id, process_name, max_files_per_cycle) VALUES (10, 'bandwidth_usage_AKAMAI_LIVE_URTMP', 50);


REPLACE INTO kalturadw.dwh_dim_bandwidth_source (bandwidth_source_id,bandwidth_source_name, is_live) VALUES (9, 'akamai_live_urtmp',1);

REPLACE INTO kalturadw.dwh_dim_http_delivery_source(process_id,bandwidth_source_id,file_regex)
VALUES (10,9,'_172678\\.|_213019\\.');

REPLACE INTO kalturadw_ds.staging_areas
        (id,
        process_id,
        source_table,
        target_table_id,
        on_duplicate_clause,
        staging_partition_field,
        post_transfer_sp,
		post_transfer_aggregations,
		aggr_date_field,
		hour_id_field)
VALUES
        (12,      10,
         'ds_bandwidth_usage',
         2,
         NULL,
         'cycle_id',
         NULL,
	'(\'bandwidth_usage\',\'devices_bandwidth_usage\')',
	'activity_date_id',
	'activity_hour_id');

-- 6150

REPLACE INTO kalturadw_ds.processes (id, process_name, max_files_per_cycle) VALUE (11, 'bandwidth_usage_unrecognized_files', 50);

-- 6151

ALTER TABLE kalturadw.dwh_hourly_partner_usage ADD COLUMN count_transcoding_mb DECIMAL(19,4) DEFAULT 0;

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

DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `calc_aggr_day_partner_storage`$$

CREATE PROCEDURE `calc_aggr_day_partner_storage`(date_val DATE)
BEGIN
    DELETE FROM kalturadw.dwh_hourly_partner_usage WHERE date_id = DATE(date_val)*1 AND IFNULL(count_bandwidth_kb,0) = 0 AND IFNULL(count_transcoding_mb,0) = 0 AND bandwidth_source_id = 1;
    UPDATE kalturadw.dwh_hourly_partner_usage SET added_storage_mb = 0, deleted_storage_mb = 0, aggr_storage_mb=NULL WHERE date_id = DATE(date_val)*1 AND (IFNULL(count_bandwidth_kb,0) > 0 OR IFNULL(count_transcoding_mb,0) > 0);
	
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

-- 6152
DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `calc_aggr_day`$$

CREATE PROCEDURE `calc_aggr_day`(p_date_val DATE,p_hour_id INT(11), p_aggr_name VARCHAR(100))
BEGIN
	DECLARE v_aggr_table VARCHAR(100);
	DECLARE v_aggr_id_field VARCHAR(100);
	DECLARE extra VARCHAR(100);
	DECLARE v_from_archive DATE;
	DECLARE v_ignore DATE;
	DECLARE v_table_name VARCHAR(100);
	DECLARE v_join_table VARCHAR(100);
	DECLARE v_join_condition VARCHAR(200);
	DECLARE v_use_index VARCHAR(100);
    		
	SELECT DATE(NOW() - INTERVAL archive_delete_days_back DAY), DATE(archive_last_partition)
	INTO v_ignore, v_from_archive
	FROM kalturadw_ds.retention_policy
	WHERE table_name = 'dwh_fact_events';	
	
	IF (p_date_val >= v_ignore) THEN 
		IF (DATE(p_date_val)*1 > 20120709) THEN 
			SELECT aggr_table, aggr_id_field
			INTO  v_aggr_table, v_aggr_id_field
			FROM kalturadw_ds.aggr_name_resolver
			WHERE aggr_name = p_aggr_name;	
			
			SET extra = CONCAT('pre_aggregation_',p_aggr_name);
			IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE ROUTINE_NAME=extra) THEN
			    SET @ss = CONCAT('CALL ',extra,'(''', p_date_val,''',',p_hour_id,');'); 
			    PREPARE stmt1 FROM  @ss;
			    EXECUTE stmt1;
			    DEALLOCATE PREPARE stmt1;
			END IF ;
		
			IF (v_aggr_table <> '') THEN 
				SET @s = CONCAT('delete from ',v_aggr_table,' where date_id = DATE(''',p_date_val,''')*1 and hour_id = ',p_hour_id);
				PREPARE stmt FROM  @s;
				EXECUTE stmt;
				DEALLOCATE PREPARE stmt;	
			END IF;
			
			SET @s = CONCAT('INSERT INTO aggr_managment(aggr_name, date_id, hour_id, data_insert_time)
					VALUES(''',p_aggr_name,''',''',DATE(p_date_val)*1,''',',p_hour_id,',NOW())
					ON DUPLICATE KEY UPDATE data_insert_time = values(data_insert_time)');
			PREPARE stmt FROM  @s;
			EXECUTE stmt;
			DEALLOCATE PREPARE stmt;
		
			IF (p_date_val >= v_from_archive) THEN 
				SET v_table_name = 'dwh_fact_events';
				SET v_use_index = 'USE INDEX (event_hour_id_event_date_id_partner_id)';
			ELSE
				SET v_table_name = 'dwh_fact_events_archive';
				SET v_use_index = '';
			END IF;
			
			SELECT aggr_table, CONCAT(
							IF(aggr_id_field <> '', CONCAT(',', aggr_id_field),'') ,
							IF(dim_id_field <> '', 	CONCAT(', e.', REPLACE(dim_id_field,',',', e.')), '')
						  )
			INTO  v_aggr_table, v_aggr_id_field
			FROM kalturadw_ds.aggr_name_resolver
			WHERE aggr_name = p_aggr_name;
			
			SELECT IF(join_table <> '' , CONCAT(',', join_table), ''), IF(join_table <> '', CONCAT(' AND ev.' ,join_id_field,'=',join_table,'.',join_id_field), '')
			INTO v_join_table, v_join_condition
			FROM kalturadw_ds.aggr_name_resolver
			WHERE aggr_name = p_aggr_name;
			
			
			SET @s = CONCAT('UPDATE aggr_managment SET start_time = NOW()
					WHERE aggr_name = ''',p_aggr_name,''' AND date_id = ''',DATE(p_date_val)*1,''' AND hour_id = ',p_hour_id);
			PREPARE stmt FROM  @s;
			EXECUTE stmt;
			DEALLOCATE PREPARE stmt;
			
			IF ( v_aggr_table <> '' ) THEN
				SET @s = CONCAT('INSERT INTO ',v_aggr_table,'
					(partner_id
					,date_id
					,hour_id
					',REPLACE(v_aggr_id_field,'e.',''),' 
					,count_loads
					,count_plays 
					,count_plays_25 
					,count_plays_50 
					,count_plays_75 
					,count_plays_100 
					,count_edit
					,count_viral 
					,count_download 
					,count_report
					,count_buf_start
					,count_buf_end
					,count_open_full_screen
					,count_close_full_screen
					,count_replay
					,count_seek
					,count_open_upload
					,count_save_publish 
					,count_close_editor
					,count_pre_bumper_played
					,count_post_bumper_played
					,count_bumper_clicked
					,count_preroll_started
					,count_midroll_started
					,count_postroll_started
					,count_overlay_started
					,count_preroll_clicked
					,count_midroll_clicked
					,count_postroll_clicked
					,count_overlay_clicked
					,count_preroll_25
					,count_preroll_50
					,count_preroll_75
					,count_midroll_25
					,count_midroll_50
					,count_midroll_75
					,count_postroll_25
					,count_postroll_50
					,count_postroll_75
					) 
				SELECT  ev.partner_id,ev.event_date_id, event_hour_id',v_aggr_id_field,',
				SUM(IF(ev.event_type_id = 2, 1,NULL)) count_loads,
				SUM(IF(ev.event_type_id = 3, 1,NULL)) count_plays,
				SUM(IF(ev.event_type_id = 4, 1,NULL)) count_plays_25,
				SUM(IF(ev.event_type_id = 5, 1,NULL)) count_plays_50,
				SUM(IF(ev.event_type_id = 6, 1,NULL)) count_plays_75,
				SUM(IF(ev.event_type_id = 7, 1,NULL)) count_plays_100,
				SUM(IF(ev.event_type_id = 8, 1,NULL)) count_edit,
				SUM(IF(ev.event_type_id = 9, 1,NULL)) count_viral,
				SUM(IF(ev.event_type_id = 10, 1,NULL)) count_download,
				SUM(IF(ev.event_type_id = 11, 1,NULL)) count_report,
				SUM(IF(ev.event_type_id = 12, 1,NULL)) count_buf_start,
				SUM(IF(ev.event_type_id = 13, 1,NULL)) count_buf_end,
				SUM(IF(ev.event_type_id = 14, 1,NULL)) count_open_full_screen,
				SUM(IF(ev.event_type_id = 15, 1,NULL)) count_close_full_screen,
				SUM(IF(ev.event_type_id = 16, 1,NULL)) count_replay,
				SUM(IF(ev.event_type_id = 17, 1,NULL)) count_seek,
				SUM(IF(ev.event_type_id = 18, 1,NULL)) count_open_upload,
				SUM(IF(ev.event_type_id = 19, 1,NULL)) count_save_publish,
				SUM(IF(ev.event_type_id = 20, 1,NULL)) count_close_editor,
				SUM(IF(ev.event_type_id = 21, 1,NULL)) count_pre_bumper_played,
				SUM(IF(ev.event_type_id = 22, 1,NULL)) count_post_bumper_played,
				SUM(IF(ev.event_type_id = 23, 1,NULL)) count_bumper_clicked,
				SUM(IF(ev.event_type_id = 24, 1,NULL)) count_preroll_started,
				SUM(IF(ev.event_type_id = 25, 1,NULL)) count_midroll_started,
				SUM(IF(ev.event_type_id = 26, 1,NULL)) count_postroll_started,
				SUM(IF(ev.event_type_id = 27, 1,NULL)) count_overlay_started,
				SUM(IF(ev.event_type_id = 28, 1,NULL)) count_preroll_clicked,
				SUM(IF(ev.event_type_id = 29, 1,NULL)) count_midroll_clicked,
				SUM(IF(ev.event_type_id = 30, 1,NULL)) count_postroll_clicked,
				SUM(IF(ev.event_type_id = 31, 1,NULL)) count_overlay_clicked,
				SUM(IF(ev.event_type_id = 32, 1,NULL)) count_preroll_25,
				SUM(IF(ev.event_type_id = 33, 1,NULL)) count_preroll_50,
				SUM(IF(ev.event_type_id = 34, 1,NULL)) count_preroll_75,
				SUM(IF(ev.event_type_id = 35, 1,NULL)) count_midroll_25,
				SUM(IF(ev.event_type_id = 36, 1,NULL)) count_midroll_50,
				SUM(IF(ev.event_type_id = 37, 1,NULL)) count_midroll_75,
				SUM(IF(ev.event_type_id = 38, 1,NULL)) count_postroll_25,
				SUM(IF(ev.event_type_id = 39, 1,NULL)) count_postroll_50,
				SUM(IF(ev.event_type_id = 40, 1,NULL)) count_postroll_75
				FROM ',v_table_name,' as ev ', v_use_index, ' , dwh_dim_entries e',v_join_table,
					' WHERE ev.event_type_id BETWEEN 2 AND 40 
					AND ev.event_date_id  = DATE(''',p_date_val,''')*1
					AND ev.event_hour_id = ',p_hour_id,'
					AND e.entry_media_type_id IN (1,2,5,6)  /* allow only video & audio & mix */
				AND e.entry_id = ev.entry_id ' ,v_join_condition, 
				' GROUP BY partner_id,event_date_id, event_hour_id',v_aggr_id_field,';');
			
			PREPARE stmt FROM  @s;
			EXECUTE stmt;
			DEALLOCATE PREPARE stmt;
						
			SET @s = CONCAT('INSERT INTO ',v_aggr_table,'
					(partner_id
					,date_id
					,hour_id
					',REPLACE(v_aggr_id_field,'e.',''),'
					,sum_time_viewed
					,count_time_viewed)
					SELECT partner_id, event_date_id, event_hour_id',v_aggr_id_field,',
					SUM(duration / 60 / 4 * (if(v_25>v_play,v_play,v_25)
					                      +if(v_50>v_play,v_play,v_50)
					                      +if(v_75>v_play,v_play,v_75)
					                      +if(v_100>v_play,v_play,v_100))) sum_time_viewed,
					COUNT(DISTINCT s_play) count_time_viewed
					FROM(
					SELECT ev.partner_id, ev.event_date_id, ev.event_hour_id',v_aggr_id_field,', ev.session_id,
						MAX(duration) duration,
						COUNT(IF(ev.event_type_id IN (4),1,NULL)) v_25,
						COUNT(IF(ev.event_type_id IN (5),1,NULL)) v_50,
						COUNT(IF(ev.event_type_id IN (6),1,NULL)) v_75,
						COUNT(IF(ev.event_type_id IN (7),1,NULL)) v_100,
						COUNT( IF(ev.event_type_id IN (3),1,NULL)) v_play,
						MAX(IF(event_type_id IN (3),session_id,NULL)) s_play
					FROM ',v_table_name,' as ev ', v_use_index, ' , dwh_dim_entries e',v_join_table,
					' WHERE ev.event_date_id  = DATE(''',p_date_val,''')*1
						AND ev.event_hour_id = ',p_hour_id,'
						AND e.entry_media_type_id IN (1,2,5,6)  /* allow only video & audio & mix */
						AND e.entry_id = ev.entry_id
						AND ev.event_type_id IN(3,4,5,6,7) /* time viewed only when player reaches 25,50,75,100 */ ',v_join_condition,
					' GROUP BY ev.partner_id, ev.event_date_id, ev.event_hour_id , ev.entry_id',v_aggr_id_field,',ev.session_id) e
					GROUP BY partner_id, event_date_id, event_hour_id',v_aggr_id_field,'
					ON DUPLICATE KEY UPDATE
					sum_time_viewed = values(sum_time_viewed), count_time_viewed=values(count_time_viewed);');
			
				PREPARE stmt FROM  @s;
				EXECUTE stmt;
				DEALLOCATE PREPARE stmt;
				
				SET extra = CONCAT('post_aggregation_',p_aggr_name);
				IF EXISTS (SELECT * FROM INFORMATION_SCHEMA.ROUTINES WHERE ROUTINE_NAME=extra) THEN
					SET @ss = CONCAT('CALL ',extra,'(''', p_date_val,''',',p_hour_id,');'); 
					PREPARE stmt1 FROM  @ss;
					EXECUTE stmt1;
					DEALLOCATE PREPARE stmt1;
				END IF ;
				
			END IF;	  
			
		END IF; 
	END IF;
	
	SET @s = CONCAT('UPDATE aggr_managment SET end_time = NOW() WHERE aggr_name = ''',p_aggr_name,''' AND date_id = ''',DATE(p_date_val)*1,''' AND hour_id =',p_hour_id);
	PREPARE stmt FROM  @s;
	EXECUTE stmt;
	DEALLOCATE PREPARE stmt;
		
END$$

DELIMITER ;

-- 6153

ALTER TABLE kalturadw.dwh_dim_batch_job_sep MODIFY dwh_id bigint NOT NULL AUTO_INCREMENT,
MODIFY id bigint DEFAULT NULL,
MODIFY parent_job_id bigint DEFAULT NULL,
MODIFY bulk_job_id bigint DEFAULT NULL,
MODIFY root_job_id bigint DEFAULT NULL,
MODIFY batch_job_lock_id bigint DEFAULT NULL;

UPDATE kalturadw_ds.pentaho_sequences SET is_active = 0 WHERE job_name = 'dimensions/update_batch_job.ktr';

ALTER TABLE kalturadw.dwh_dim_entries ADD COLUMN stream_id int(11),
ADD INDEX stream_id (stream_id);


