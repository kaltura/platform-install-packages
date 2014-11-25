DELIMITER $$

USE `kalturadw`$$

DROP VIEW IF EXISTS `dwh_dim_entries_v`$$

CREATE ALGORITHM=UNDEFINED  SQL SECURITY DEFINER VIEW `dwh_dim_entries_v` AS 
SELECT
  `a`.`entry_id`              AS `entry_id`,
  `a`.`entry_name`            AS `entry_name`,
  `a`.`partner_id`            AS `partner_id`,
  `a`.`entry_source_id`       AS `entry_source_id`,
  `a`.`created_at`            AS `created_at`,
  `a`.`created_date_id`       AS `created_date_id`,
  `a`.`created_hour_id`       AS `created_hour_id`,
  `a`.`updated_date_id`       AS `updated_date_id`,
  `a`.`updated_hour_id`       AS `updated_hour_id`,
  `a`.`entry_type_id`         AS `entry_type_id`,
  `c`.`entry_type_name`       AS `entry_type_Name`,
  `b`.`entry_status_id`       AS `entry_status_id`,
  `b`.`entry_status_name`     AS `entry_status_Name`,
  `d`.`entry_media_type_id`   AS `entry_media_type_id`,
  `e`.`partner_name`          AS `partner_name`,
  `d`.`entry_media_type_name` AS `entry_media_type_name` 
  from ((((`dwh_dim_entries` `a` 
            left join `dwh_dim_entry_status` `b` on((`a`.`entry_status_id` = `b`.`entry_status_id`))) 
            left join `dwh_dim_entry_type` `c` on((`a`.`entry_type_id` = `c`.`entry_type_id`))) 
            left join `dwh_dim_entry_media_type` `d` on((`a`.`entry_media_type_id` = `d`.`entry_media_type_id`))) 
            left join `dwh_dim_partners` `e` on((`a`.`partner_id` = `e`.`partner_id`)))$$

DELIMITER ;