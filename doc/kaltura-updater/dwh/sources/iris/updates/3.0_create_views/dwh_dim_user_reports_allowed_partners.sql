DELIMITER $$

USE `kalturadw`$$

DROP VIEW IF EXISTS `dwh_dim_user_reports_allowed_partners`$$


CREATE ALGORITHM=UNDEFINED  SQL SECURITY DEFINER VIEW `dwh_dim_user_reports_allowed_partners` AS (
SELECT  `dwh_dim_permissions`.`partner_id` AS `partner_id`,
		DATE(STR_TO_DATE(`dwh_dim_permissions`.`created_at`, '%Y-%m-%d %H:%i:%S.%f'))*1 AS `created_date_id`,
		HOUR(STR_TO_DATE(`dwh_dim_permissions`.`created_at`, '%Y-%m-%d %H:%i:%S.%f')) AS `created_hour_id`
FROM `dwh_dim_permissions` 
WHERE ((`dwh_dim_permissions`.`name` = 'FEATURE_END_USER_REPORTS') AND (`dwh_dim_permissions`.`status` = 1)))$$

DELIMITER ;



