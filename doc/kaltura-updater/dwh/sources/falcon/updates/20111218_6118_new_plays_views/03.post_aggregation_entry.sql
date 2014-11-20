DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `post_aggregation_entry`$$

CREATE DEFINER=`etl`@`localhost` PROCEDURE `post_aggregation_entry`(date_val DATE, p_hour_id INT(11))
BEGIN
	CALL add_plays_views(date_val*1, p_hour_id);
END$$

DELIMITER ;
