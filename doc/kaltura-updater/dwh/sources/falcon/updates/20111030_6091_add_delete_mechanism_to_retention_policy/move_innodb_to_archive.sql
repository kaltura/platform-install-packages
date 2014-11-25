DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `move_innodb_to_archive`$$

CREATE DEFINER=`etl`@`localhost` PROCEDURE `move_innodb_to_archive`()
BEGIN
	DECLARE v_table_name VARCHAR(256);
	DECLARE v_archive_name VARCHAR(256);	
	DECLARE v_partition_name VARCHAR(256);
	DECLARE v_partition_date_id INT;
	DECLARE v_column VARCHAR(256);
	DECLARE v_is_archived INT;
	DECLARE v_is_in_fact INT;
	
	DECLARE v_drop_from_archive INT DEFAULT 0;
	DECLARE v_drop_from_fact INT DEFAULT 0;
	DECLARE v_migrate_from_fact INT DEFAULT 0;
		
	DECLARE v_done INT DEFAULT 0;
	
	DECLARE c_partitions 
	CURSOR FOR 	
	SELECT 	r.table_name, 
		CONCAT(r.table_name, '_archive') archive_name,
		partition_name, 
		DATE(partition_description)*1 partition_date_id, 
		partition_expression column_name,
		MAX(IF(CONCAT(r.table_name, '_archive') = p.table_name,1,0)) is_archived, 
		MAX(IF(r.table_name=p.table_name,1,0)) is_in_fact
	FROM information_schema.PARTITIONS p, kalturadw_ds.retention_policy r
	WHERE LENGTH(partition_description) = 8 
	AND DATE(partition_description)*1 IS NOT NULL
	AND (p.table_name = r.table_name OR CONCAT(r.table_name, '_archive') = p.table_name)
	GROUP BY r.table_name, partition_name, partition_date_id, column_name
	ORDER BY partition_date_id;
	
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_done = 1;
	
	OPEN c_partitions;
	
	read_loop: LOOP
		FETCH c_partitions INTO v_table_name, v_archive_name, v_partition_name, v_partition_date_id, v_column, v_is_archived, v_is_in_fact;

		IF v_done = 1 THEN
		  LEAVE read_loop;
		END IF;

		SET v_drop_from_archive = 0;
		SET v_drop_from_fact = 0;
		SET v_migrate_from_fact = 0;

		-- Check if a partition exists in the archive or the fact and is older than the delete policy
		SELECT if(count(*)=0,0,v_is_archived), if(count(*)=0, 0,v_is_in_fact)
		INTO v_drop_from_archive, v_drop_from_fact
		FROM kalturadw_ds.retention_policy
		WHERE DATE(NOW() - INTERVAL archive_delete_days_back DAY)*1 >= v_partition_date_id
		AND table_name = v_table_name;

		IF (v_drop_from_archive > 0) THEN 
			SET @s = CONCAT('ALTER TABLE ',v_archive_name,' DROP PARTITION ', v_partition_name);
			
			PREPARE stmt FROM @s;
                        EXECUTE stmt;
                        DEALLOCATE PREPARE stmt;
		END IF;

		-- Check if a partition exists in the fact and is older than the archive policy
		SELECT if(count(*)=0,0, v_is_in_fact)
		INTO v_migrate_from_fact
		FROM kalturadw_ds.retention_policy
		WHERE DATE(NOW() - INTERVAL archive_start_days_back DAY)*1 >= v_partition_date_id
		AND table_name = v_table_name
		AND v_is_in_fact > 0;
		
		-- If the partition exists in the fact and is older than the archive policy (and not older than the delete policy)
		IF (v_migrate_from_fact > 0 AND v_drop_from_fact = 0) THEN
			-- Check if the archive already has a partition convering this time period (drop it)
			IF (v_is_archived > 0) THEN
				SET @s = CONCAT('ALTER TABLE ',v_archive_name,' DROP PARTITION ', v_partition_name);
		
				PREPARE stmt FROM @s;
				EXECUTE stmt;
				DEALLOCATE PREPARE stmt;
			END IF;
			
			-- Migrate it to the archive
			SET @s = CONCAT('ALTER TABLE ',v_archive_name,' ADD PARTITION (PARTITION ',v_partition_name,' VALUES LESS THAN (',v_partition_date_id,'))');
			
			PREPARE stmt FROM @s;
			EXECUTE stmt;
			DEALLOCATE PREPARE stmt;
			
			SET @s = CONCAT('INSERT INTO ',v_archive_name,' SELECT * FROM ',v_table_name,' WHERE ', v_column ,' < ',v_partition_date_id);
			
			PREPARE stmt FROM @s;
			EXECUTE stmt;
			DEALLOCATE PREPARE stmt;
			
			UPDATE kalturadw_ds.retention_policy
			SET archive_last_partition = DATE(v_partition_date_id)
			WHERE table_name = v_table_name;

			SET v_drop_from_fact = 1;
		END IF;

		-- If partition has migrated from the fact or should be dropped due to the fact that it's older than the delete policy
		IF (v_drop_from_fact > 0) THEN
			SET @s = CONCAT('ALTER TABLE ',v_table_name,' DROP PARTITION ',v_partition_name);
			
			PREPARE stmt FROM @s;
			EXECUTE stmt;
			DEALLOCATE PREPARE stmt;
		END IF;
	END LOOP read_loop;

	CLOSE c_partitions;
END$$

DELIMITER ;
