DELIMITER $$

USE `kalturadw`$$

DROP FUNCTION IF EXISTS `calc_partner_storage_data_time_range`$$

CREATE DEFINER=`root`@`localhost` FUNCTION `calc_partner_storage_data_time_range`(p_start_date_id INT, p_end_date_id INT ,p_partner_id INT ) RETURNS DECIMAL(19,4)
    DETERMINISTIC
BEGIN	
	DECLARE total_billable_storage_mb DECIMAL (19,4);
  	
    SELECT SUM(aggr_p.billable_storage_mb)
    INTO total_billable_storage_mb
    FROM dwh_hourly_partner_usage aggr_p
    WHERE date_id between p_start_date_id AND p_end_date_id
    AND aggr_p.partner_id = p_partner_id
    AND aggr_p.hour_id = 0
		  AND aggr_p.bandwidth_source_id = 1;
    
	RETURN total_billable_storage_mb;
END$$

DELIMITER ;
