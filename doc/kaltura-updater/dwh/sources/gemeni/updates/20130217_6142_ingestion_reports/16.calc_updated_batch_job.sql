DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `calc_updated_batch_job`$$

CREATE DEFINER=`etl`@`localhost` PROCEDURE `calc_updated_batch_job`(p_start_date INT(11), p_end_date INT(11))
BEGIN
                                
                BEGIN
				
                                DECLARE v_date_id INT(11);
                                DECLARE done INT DEFAULT 0;
                                DECLARE days_to_update CURSOR FOR 
                                SELECT day_id FROM kalturadw.dwh_dim_time WHERE day_id BETWEEN p_start_date AND p_end_date;
                                DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
                                
                                OPEN days_to_update;
								
                                read_loop: LOOP
                                                FETCH days_to_update INTO v_date_id;
                                                IF done THEN
                                                                LEAVE read_loop;
                                                END IF;
                                                CALL kalturadw.calc_updated_batch_job_day(v_date_id);
                                END LOOP;
                                CLOSE days_to_update;
                END;
				
END$$

DELIMITER ;