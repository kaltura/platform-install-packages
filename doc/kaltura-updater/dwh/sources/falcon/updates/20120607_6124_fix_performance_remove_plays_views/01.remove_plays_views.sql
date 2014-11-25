DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `remove_plays_views`$$

CREATE DEFINER=`etl`@`localhost` PROCEDURE `remove_plays_views`(p_date_id INT, p_hour_id INT)
BEGIN
	  DECLARE v_done INT DEFAULT FALSE;
  DECLARE v_entry_id VARCHAR(20);
  DECLARE v_plays INT;
  
  DECLARE entries CURSOR FOR SELECT entry_id, count_plays FROM dwh_hourly_events_entry WHERE date_id = p_date_id AND hour_id = p_hour_id;
  
  DECLARE CONTINUE HANDLER FOR NOT FOUND SET v_done = TRUE;

  OPEN entries;
  
  read_loop: LOOP
    FETCH entries INTO v_entry_id, v_plays;
     
    IF v_done THEN
      LEAVE read_loop;
    END IF;
    
    UPDATE dwh_entry_plays_views
	SET plays = 
		IF((IFNULL(plays, 0) - IFNULL(v_plays, 0))<0, 
			0, 
			IFNULL(plays, 0) - IFNULL(v_plays, 0))
	WHERE v_entry_id = entry_id;	

  END LOOP;

  CLOSE entries;

END$$

DELIMITER ;
