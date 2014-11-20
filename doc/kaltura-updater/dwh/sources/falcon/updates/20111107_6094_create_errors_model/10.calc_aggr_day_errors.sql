DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `calc_aggr_day_errors`$$

CREATE DEFINER=`etl`@`localhost` PROCEDURE `calc_aggr_day_errors`(p_date_val DATE, p_hour_id INT)
BEGIN
        DECLARE v_ignore DATE;
        DECLARE v_from_archive DATE;
        DECLARE v_table_name VARCHAR(100);
        DECLARE v_aggr_table VARCHAR(100);
        DECLARE v_aggr_id_field_str VARCHAR(100);
 
        SELECT aggr_table, IF(IFNULL(aggr_id_field,'')='','', CONCAT(', ', aggr_id_field)) aggr_id_field
        INTO  v_aggr_table, v_aggr_id_field_str
        FROM kalturadw_ds.aggr_name_resolver
        WHERE aggr_name = 'errors';
 
 
        UPDATE aggr_managment SET is_calculated = 0, start_time = NOW() WHERE aggr_name = 'errors' AND aggr_day_int = DATE(p_date_val)*1 AND hour_id = p_hour_id;
 
        SELECT MAX(DATE(NOW() - INTERVAL archive_delete_days_back DAY))
        INTO v_ignore
        FROM kalturadw_ds.retention_policy
        WHERE table_name IN ('dwh_fact_errors');
 
        IF (p_date_val >= v_ignore) THEN
                SET @s = CONCAT('DELETE FROM kalturadw.',v_aggr_table, ' WHERE date_id = DATE(\'',p_date_val,'\')*1 and hour_id = ', p_hour_id);
		
                PREPARE stmt FROM  @s;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;
                SELECT DATE(archive_last_partition)
                INTO v_from_archive
                FROM kalturadw_ds.retention_policy
                WHERE table_name = 'dwh_fact_errors';
 
                IF (p_date_val >= v_from_archive) THEN
                        SET v_table_name = 'dwh_fact_errors';
                ELSE
                        SET v_table_name = 'dwh_fact_errors_archive';
                END IF;
                SET @s = CONCAT('INSERT INTO kalturadw.', v_aggr_table, ' (partner_id, date_id, hour_id ', v_aggr_id_field_str,', count_errors)'
				'SELECT partner_id, error_date_id, error_hour_id hour_id', v_aggr_id_field_str,', count(*)
				FROM ', v_table_name, '    WHERE error_date_id=date(\'',p_date_val,'\')*1 AND error_hour_id = ',p_hour_id,'
				GROUP BY partner_id', v_aggr_id_field_str);
		
                PREPARE stmt FROM  @s;
                EXECUTE stmt;
                DEALLOCATE PREPARE stmt;
        END IF;
        UPDATE aggr_managment SET is_calculated = 1, end_time = NOW() WHERE aggr_name = 'errors' AND aggr_day_int = DATE(p_date_val)*1 AND hour_id = p_hour_id;
END$$

DELIMITER ;
