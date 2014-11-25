DELIMITER $$

USE `kalturadw`$$

DROP FUNCTION IF EXISTS `calc_median_ff_convert_job_wait_time`$$

CREATE DEFINER=`etl`@`localhost` FUNCTION `calc_median_ff_convert_job_wait_time`(p_date_id INT(11)) RETURNS INT(11)
    DETERMINISTIC
BEGIN
	DECLARE v_median INT(11);
	SET v_median = 0;
	SELECT t1.wait_time AS median_val INTO v_median FROM (
	SELECT @rownum:=@rownum+1 AS `row_number`, IF(d.wait_time>0, d.wait_time, 0) wait_time
	FROM kalturadw.dwh_fact_convert_job d,  (SELECT @rownum:=0) r
	WHERE created_date_id = p_date_id AND is_ff = 1 
	ORDER BY d.wait_time
	) AS t1, 
	(
	SELECT COUNT(*) AS total_rows
	FROM kalturadw.dwh_fact_convert_job d
	WHERE created_date_id = p_date_id AND is_ff = 1 
	) AS t2
	WHERE 1
	AND t1.row_number=FLOOR(total_rows/2)+1;
	
	RETURN v_median;
    END$$

DELIMITER ;