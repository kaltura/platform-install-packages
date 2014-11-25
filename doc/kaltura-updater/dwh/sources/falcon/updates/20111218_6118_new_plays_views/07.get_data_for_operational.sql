DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `get_data_for_operational`$$

CREATE DEFINER=`etl`@`localhost` PROCEDURE `get_data_for_operational`(p_sync_type VARCHAR(55))
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
   
    UPDATE kalturadw_ds.parameters	
    SET date_value = v_execution_start_time 
    WHERE id = v_execution_start_time_parameter_id;

    IF p_sync_type='entry' THEN -- HACK. When KUSERS move to the same mechanism as ENTRIES, need to rewrite the entire procedure.
    
        SELECT e.entry_id, e.plays, e.views
        FROM dwh_entry_plays_views e, kalturadw_ds.parameters p
        WHERE e.updated_at > p.date_value AND p.id = 4;
    
    ELSE
    
        SELECT group_column, entity_table, aggregation_phrase, aggregation_table, 
            bridge_entity, bridge_table, last_execution_parameter_id, execution_start_time_parameter_id
        INTO	v_group_column, v_entity_table, v_aggregation_phrase, v_aggregation_table, 
            v_bridge_entity, v_bridge_table, v_last_execution_parameter_id, v_execution_start_time_parameter_id
        FROM kalturadw_ds.operational_syncs WHERE operational_sync_name = p_sync_type;

        UPDATE kalturadw_ds.parameters	SET date_value = v_execution_start_time WHERE id = v_execution_start_time_parameter_id;

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
