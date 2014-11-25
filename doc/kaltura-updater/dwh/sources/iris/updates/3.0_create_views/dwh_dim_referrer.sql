DELIMITER $$

USE `kalturadw`$$

DROP VIEW IF EXISTS `dwh_dim_referrer`$$

CREATE ALGORITHM=UNDEFINED  SQL SECURITY DEFINER VIEW `dwh_dim_referrer` AS 
SELECT
  `r`.`referrer_id` AS `referrer_id`, IF(TRIM(IFNULL(`d`.`domain_name`,'')) = '',`r`.`referrer`,CONCAT(`d`.`domain_name`,'/',IFNULL(`r`.`referrer`,'')))  AS `referrer`
FROM (`dwh_dim_domain_referrer` `r`
   JOIN `dwh_dim_domain` `d`)
WHERE (`r`.`domain_id` = `d`.`domain_id`)$$

DELIMITER ;
