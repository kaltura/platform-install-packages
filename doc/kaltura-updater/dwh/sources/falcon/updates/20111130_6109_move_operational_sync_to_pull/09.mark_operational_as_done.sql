DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `mark_operational_sync_as_done`$$

CREATE DEFINER=`etl`@`localhost` PROCEDURE `mark_operational_sync_as_done`(p_sync_type VARCHAR(55))
BEGIN
	DECLARE v_last_execution_parameter_id INT;
	DECLARE v_execution_start_time_parameter_id INT;
	
	SELECT last_execution_parameter_id, execution_start_time_parameter_id
	INTO	v_last_execution_parameter_id, v_execution_start_time_parameter_id
	FROM kalturadw_ds.operational_syncs WHERE operational_sync_name = p_sync_type;

	UPDATE kalturadw_ds.parameters main, kalturadw_ds.parameters start_time	
	SET main.date_value = start_time.date_value
	WHERE main.id = v_last_execution_parameter_id AND start_time.id = v_execution_start_time_parameter_id;
END$$

DELIMITER ;
