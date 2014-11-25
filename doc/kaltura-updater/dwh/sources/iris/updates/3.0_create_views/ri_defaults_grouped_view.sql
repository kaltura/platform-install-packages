DELIMITER $$

USE `kalturadw`$$

DROP VIEW IF EXISTS `ri_defaults_grouped`$$

CREATE ALGORITHM=UNDEFINED  SQL SECURITY DEFINER VIEW `ri_defaults_grouped` AS (
SELECT
  `ri_defaults`.`table_name` AS `table_name`,
  GROUP_CONCAT(`ri_defaults`.`default_field` ORDER BY `ri_defaults`.`default_field` ASC SEPARATOR ',') AS `default_fields`,
  GROUP_CONCAT(`ri_defaults`.`default_value` ORDER BY `ri_defaults`.`default_field` ASC SEPARATOR ',') AS `default_values`
FROM `ri_defaults`
GROUP BY `ri_defaults`.`table_name`)$$

DELIMITER ;
