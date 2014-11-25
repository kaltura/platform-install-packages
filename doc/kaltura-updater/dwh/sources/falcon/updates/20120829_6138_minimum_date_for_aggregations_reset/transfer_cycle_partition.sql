DELIMITER $$

USE `kalturadw_ds`$$

DROP PROCEDURE IF EXISTS `transfer_cycle_partition`$$

CREATE DEFINER=`etl`@`localhost` PROCEDURE `transfer_cycle_partition`(p_cycle_id VARCHAR(10))
BEGIN
	DECLARE src_table VARCHAR(45);
	DECLARE tgt_table VARCHAR(45);
	DECLARE dup_clause VARCHAR(4000);
	DECLARE partition_field VARCHAR(45);
	DECLARE select_fields VARCHAR(4000);
	DECLARE post_transfer_sp_val VARCHAR(4000);
	DECLARE v_ignore_duplicates_on_transfer BOOLEAN;	
	DECLARE aggr_date VARCHAR(400);
	DECLARE aggr_hour VARCHAR(400);
	DECLARE aggr_names VARCHAR(4000);
	DECLARE reset_aggr_min_date DATETIME;
	
	
	DECLARE done INT DEFAULT 0;
	DECLARE staging_areas_cursor CURSOR FOR SELECT 	source_table, target_table, IFNULL(on_duplicate_clause,''),	staging_partition_field, post_transfer_sp, aggr_date_field, hour_id_field, post_transfer_aggregations, reset_aggregations_min_date, ignore_duplicates_on_transfer
											FROM staging_areas s, cycles c
											WHERE s.process_id=c.process_id AND c.cycle_id = p_cycle_id;
											
	DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
	OPEN staging_areas_cursor;
	
	read_loop: LOOP
		FETCH staging_areas_cursor INTO src_table, tgt_table, dup_clause, partition_field, post_transfer_sp_val, aggr_date, aggr_hour, aggr_names, reset_aggr_min_date, v_ignore_duplicates_on_transfer;
		IF done THEN
			LEAVE read_loop;
		END IF;
		
		IF ((LENGTH(AGGR_DATE) > 0) && (LENGTH(aggr_names) > 0)) THEN
		
			SET @s = CONCAT(
				'INSERT INTO kalturadw.aggr_managment(aggr_name, date_id, hour_id, data_insert_time)
				SELECT aggr_name, aggr_date, aggr_hour, now() 
				FROM kalturadw_ds.aggr_name_resolver a, 
					(select distinct ',aggr_date, ' aggr_date,' ,aggr_hour,' aggr_hour 
					 from ',src_table,
					' where ',partition_field,' = ',p_cycle_id,') ds
				WHERE 	aggr_name in ', aggr_names,'
					AND aggr_date >= date(\'', reset_aggr_min_date, '\')
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
			
		IF LENGTH(POST_TRANSFER_SP_VAL)>0 THEN
				SET @s = CONCAT('CALL ',post_transfer_sp_val,'(',p_cycle_id,')');
				
				PREPARE stmt FROM  @s;
				EXECUTE stmt;
				DEALLOCATE PREPARE stmt;
		END IF;
	END LOOP;

	CLOSE staging_areas_cursor;
END$$

DELIMITER ;