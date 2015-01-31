DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `post_aggregation_entry`$$

CREATE DEFINER=`etl`@`localhost` PROCEDURE `post_aggregation_entry`(date_val DATE, p_hour_id INT(11))
BEGIN
	UPDATE kalturadw.dwh_dim_entries dim, kalturadw.dwh_hourly_events_entry aggr
	SET operational_measures_updated_at = NOW()
	WHERE aggr.date_id = DATE(date_val)*1 AND aggr.hour_id = p_hour_id AND dim.entry_id = aggr.entry_id;
END$$

DELIMITER ;
