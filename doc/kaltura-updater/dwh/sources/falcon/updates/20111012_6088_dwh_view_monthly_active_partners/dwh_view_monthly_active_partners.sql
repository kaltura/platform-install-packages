DROP VIEW IF EXISTS `kalturadw`.`dwh_view_monthly_active_partners`;
CREATE VIEW `kalturadw`.`dwh_view_monthly_active_partners` 
    AS
(
	SELECT FLOOR(date_id/100) month_id, partner_id, 
		SUM(IFNULL(new_videos,0)) + SUM(IFNULL(new_images,0)) + SUM(IFNULL(new_audios,0)) + 
		SUM(IFNULL(new_playlists,0)) + SUM(IFNULL(new_livestreams,0)) + SUM(IFNULL(new_other_entries,0)) AS new_entries,
		SUM(count_plays) count_plays
	FROM kalturadw.dwh_hourly_partner
	GROUP BY month_id, partner_id
	HAVING new_entries > 10 AND count_plays > 100
);

