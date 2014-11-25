DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `calc_partner_usage_data`$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `calc_partner_usage_data`(p_date_id INT(11),p_partner_id INT,p_total BOOL)
BEGIN
    IF(p_total) THEN
    
	    SELECT 
		month_id,
	    SUM(free.avg_continuous_aggr_storage_mb) avg_continuous_aggr_storage_mb,
	    SUM(free.sum_partner_bandwidth_kb) sum_partner_bandwidth_kb
	    FROM 
	    (SELECT
		FLOOR(date_id/100) month_id,
		SUM(aggr_storage_mb/IF(FLOOR(date_id/100)=FLOOR(LEAST(p_date_id,DATE(NOW())*1)),DAY(LEAST(p_date_id,DATE(NOW())*1)),DAY(LAST_DAY(date_id)))) avg_continuous_aggr_storage_mb,
		SUM(count_bandwidth_kb) sum_partner_bandwidth_kb
	    FROM dwh_hourly_partner_usage 
	    WHERE partner_id=p_partner_id AND hour_id = 0
	    AND date_id <= LEAST(p_date_id,DATE(NOW())*1)
	    GROUP BY month_id) AS free;
     ELSE
	
	SELECT
		FLOOR(date_id/100) month_id,
		SUM(aggr_storage_mb)/DAY(LEAST(p_date_id,DATE(NOW())*1)) avg_continuous_aggr_storage_mb,
		SUM(count_bandwidth_kb) sum_partner_bandwidth_kb
	    FROM dwh_hourly_partner_usage 
	    WHERE partner_id=p_partner_id AND hour_id = 0
	    AND FLOOR(date_id/100) = FLOOR(LEAST(p_date_id,DATE(NOW())*1)/100);
     END IF;
END$$

DELIMITER ;