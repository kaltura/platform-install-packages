DELIMITER $$

USE `kalturadw`$$

DROP VIEW IF EXISTS `ri_mapping_and_defaults`$$

CREATE ALGORITHM=UNDEFINED  SQL SECURITY DEFINER VIEW `ri_mapping_and_defaults` AS (
SELECT
  `m`.`table_name`          AS `table_name`,
  `m`.`column_name`         AS `column_name`,
  `m`.`date_id_column_name` AS `date_id_column_name`,
  `m`.`date_column_name`    AS `date_column_name`,
  `m`.`reference_table`     AS `reference_table`,
  `m`.`reference_column`    AS `reference_column`,
  `m`.`perform_check`       AS `perform_check`,
  `dg`.`default_fields`     AS `default_fields`,
  `dg`.`default_values`     AS `default_values`
FROM (`ri_mapping` `m`
   JOIN `ri_defaults_grouped` `dg`)
WHERE (CONVERT(`m`.`reference_table` USING utf8) = `dg`.`table_name`))$$

DELIMITER ;
