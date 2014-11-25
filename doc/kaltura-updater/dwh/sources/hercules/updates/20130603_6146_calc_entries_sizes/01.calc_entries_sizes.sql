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

