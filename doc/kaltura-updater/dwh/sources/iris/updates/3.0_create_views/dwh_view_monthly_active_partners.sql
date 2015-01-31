DELIMITER $$

USE `kalturadw`$$

DROP VIEW IF EXISTS `dwh_view_monthly_active_partners`$$

CREATE ALGORITHM=UNDEFINED  SQL SECURITY DEFINER VIEW `dwh_view_monthly_active_partners` AS (
select
  CAST(substr(date_id, 1, 6) as SIGNED INT) as month_id,
  `partner_id` AS `partner_id`,
  sum((((((ifnull(`new_videos`,0) + ifnull(`new_images`,0)) + ifnull(`new_audios`,0)) + ifnull(`new_playlists`,0)) + ifnull(`new_livestreams`,0)) + ifnull(`new_other_entries`,0))) AS `new_entries`,
  sum(`count_plays`) AS `count_plays`
from `dwh_hourly_partner` `hourly`
group by `month_id`,`partner_id`
having ((`new_entries` > 10)
        and (`count_plays` > 100)))$$

DELIMITER ;