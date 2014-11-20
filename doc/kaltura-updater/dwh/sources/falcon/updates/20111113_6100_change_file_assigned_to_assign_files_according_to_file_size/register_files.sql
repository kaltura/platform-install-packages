DELIMITER $$

USE `kalturadw_ds`$$

DROP PROCEDURE IF EXISTS `register_file`$$

CREATE DEFINER=`etl`@`localhost` PROCEDURE `register_file`(p_file_name VARCHAR(750), p_process_id INT, p_file_size_kb INT(11), p_compression_suffix VARCHAR(10), p_subdir VARCHAR(1024))
BEGIN
	DECLARE v_assigned_server_id INT;
	DECLARE v_cycle_id INT;
	DECLARE v_file_id INT;
	
	SELECT file_id INTO v_file_id FROM kalturadw_ds.files WHERE file_name = p_file_name AND process_id = p_process_id AND compression_suffix = p_compression_suffix;
	
	IF (v_file_id IS NULL) THEN
		SELECT etl_server_id INTO v_assigned_server_id
			FROM kalturadw_ds.etl_servers s  
				LEFT OUTER JOIN kalturadw_ds.cycles c 
					ON (s.etl_server_id = c.assigned_server_id AND c.STATUS = 'REGISTERED' AND c.process_id = p_process_id)
				LEFT OUTER JOIN kalturadw_ds.files f
					ON (c.cycle_id = f.cycle_id)		
			GROUP BY etl_server_id
			ORDER BY SUM(file_size_kb) LIMIT 1;
		
		IF (v_assigned_server_id IS NOT NULL) THEN
			SELECT c.cycle_id INTO v_cycle_id 
				FROM kalturadw_ds.processes p INNER JOIN kalturadw_ds.cycles c ON (c.process_id = p.id) LEFT OUTER JOIN kalturadw_ds.files f ON (c.cycle_id = f.cycle_id)
				WHERE 	p.id = p_process_id AND
					c.STATUS='REGISTERED' AND
					c.assigned_server_id = v_assigned_server_id
				GROUP BY c.cycle_id
				HAVING COUNT(file_id)<MAX(max_files_per_cycle) LIMIT 1;
			
			
			IF (v_cycle_id IS NOT NULL) THEN 
				INSERT INTO kalturadw_ds.files 	(file_name, file_status, insert_time, file_size_kb, process_id, cycle_id, compression_suffix, subdir)
							VALUES	(p_file_name, 'IN_CYCLE', NOW(), p_file_size_kb, p_process_id, v_cycle_id, p_compression_suffix, p_subdir);
			ELSE
				INSERT INTO kalturadw_ds.cycles (STATUS, insert_time, process_id, assigned_server_id)
							VALUES	('REGISTERED', NOW(), p_process_id, v_assigned_server_id);
				SET v_cycle_id = LAST_INSERT_ID();
				CALL add_cycle_partition(v_cycle_id);
				INSERT INTO kalturadw_ds.files 	(file_name, file_status, insert_time, file_size_kb, process_id, cycle_id, compression_suffix, subdir)
							VALUES	(p_file_name, 'IN_CYCLE', NOW(), p_file_size_kb, p_process_id, v_cycle_id, p_compression_suffix, p_subdir);
			END IF;
		END IF;
	END IF;
END$$

DELIMITER ;
