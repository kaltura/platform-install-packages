DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `remove_plays_views`$$

CREATE DEFINER=`etl`@`localhost` PROCEDURE `remove_plays_views`(p_date_id INT, p_hour_id INT)
BEGIN
	UPDATE kalturadw.dwh_hourly_events_entry h_entry, dwh_entry_plays_views entry_plays_views
	SET entry_plays_views.plays = 
		IF((IFNULL(entry_plays_views.plays, 0) - IFNULL(h_entry.count_plays, 0))<0, 
			0, 
			IFNULL(entry_plays_views.plays, 0) - IFNULL(h_entry.count_plays, 0))
	WHERE h_entry.entry_id = entry_plays_views.entry_id AND date_id = p_date_id AND hour_id = p_hour_id;
END$$

DELIMITER ;
