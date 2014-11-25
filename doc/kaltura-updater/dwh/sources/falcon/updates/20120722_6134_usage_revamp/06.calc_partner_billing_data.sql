DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `calc_partner_billing_data`$$

CREATE DEFINER=`root`@`localhost` PROCEDURE `calc_partner_billing_data`(p_date_id INT(11),p_partner_id INT)
BEGIN
	SELECT
        FLOOR(date_id/100) month_id,
        SUM(aggr_storage_mb)/(IF(FLOOR(date_id/100)=FLOOR(LEAST(p_date_id,DATE(NOW())*1)/100),DAY(LEAST(p_date_id,DATE(NOW())*1)),DAY(LAST_DAY(date_id)))) avg_continuous_aggr_storage_mb,
        SUM(count_bandwidth_kb) sum_partner_bandwidth_kb
    FROM dwh_hourly_partner_usage 
    WHERE partner_id=p_partner_id AND hour_id = 0
    AND date_id <= LEAST(p_date_id,DATE(NOW())*1)
    GROUP BY month_id
	WITH ROLLUP;	
END$$

DELIMITER ;	
