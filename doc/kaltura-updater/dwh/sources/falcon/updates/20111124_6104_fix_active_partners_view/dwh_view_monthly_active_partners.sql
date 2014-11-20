DELIMITER $$

USE `kalturadw`$$

DROP VIEW IF EXISTS `dwh_view_monthly_active_partners`$$

CREATE ALGORITHM=UNDEFINED DEFINER=`etl`@`%` SQL SECURITY DEFINER VIEW `dwh_view_monthly_active_partners` AS (
SELECT
  FLOOR((CAST(`dwh_hourly_partner`.`date_id` AS SIGNED) / 100)) AS `month_id`,
  `dwh_hourly_partner`.`partner_id` AS `partner_id`,
  SUM((((((IFNULL(`dwh_hourly_partner`.`new_videos`,0) + IFNULL(`dwh_hourly_partner`.`new_images`,0)) + IFNULL(`dwh_hourly_partner`.`new_audios`,0)) + IFNULL(`dwh_hourly_partner`.`new_playlists`,0)) + IFNULL(`dwh_hourly_partner`.`new_livestreams`,0)) + IFNULL(`dwh_hourly_partner`.`new_other_entries`,0))) AS `new_entries`,
  SUM(`dwh_hourly_partner`.`count_plays`) AS `count_plays`
FROM `dwh_hourly_partner`
GROUP BY CAST(FLOOR((`dwh_hourly_partner`.`date_id` / 100)) AS SIGNED INTEGER),`dwh_hourly_partner`.`partner_id`
HAVING ((`new_entries` > 10)
        AND (`count_plays` > 100)))$$

DELIMITER ;
