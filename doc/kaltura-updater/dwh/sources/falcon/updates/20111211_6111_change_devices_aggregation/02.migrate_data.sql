USE kalturadw;
DROP TABLE IF EXISTS tmp_devices_migration;
CREATE TABLE tmp_devices_migration
SELECT day_id, DATE(19700101) start_time, DATE(19700101) end_time, 0 is_copied FROM kalturadw.dwh_dim_time
WHERE day_id BETWEEN 20111001 AND DATE(NOW())*1;

DELIMITER $$

USE `kalturadw`$$

DROP PROCEDURE IF EXISTS `tmp_fix_devices`$$

CREATE DEFINER=`etl`@`localhost` PROCEDURE `tmp_fix_devices`()
BEGIN
        DECLARE v_date_id INT;
        DECLARE done INT DEFAULT 0;
        DECLARE fix_devices_cursor CURSOR FOR SELECT day_id FROM kalturadw.tmp_devices_migration WHERE is_copied = 0 ORDER BY day_id;
        DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = 1;
        OPEN fix_devices_cursor ;

        read_loop: LOOP
                FETCH fix_devices_cursor  INTO v_date_id;
                IF done THEN
                        LEAVE read_loop;
                END IF;

                UPDATE kalturadw.tmp_devices_migration SET start_time = NOW() WHERE day_id = v_date_id;

                INSERT INTO kalturadw.dwh_hourly_events_devices_new
			SELECT fact.partner_id AS partner_id,
			date_id,
			hour_id,
			location_id,
			country_id,
			os_id,
			browser_id,
			ui_conf_id,
			entry_media_type_id,
			SUM(sum_time_viewed) AS sum_time_viewed,
			SUM(count_time_viewed) AS count_time_viewed,
			SUM(count_plays) AS count_plays,
			SUM(count_loads) AS count_loads,
			SUM(count_plays_25) AS count_plays_25,
			SUM(count_plays_50) AS count_plays_50,
			SUM(count_plays_75) AS count_plays_75,
			SUM(count_plays_100) AS count_plays_100,
			SUM(count_edit) AS count_edit,
			SUM(count_viral) AS count_viral,
			SUM(count_download) AS count_download,
			SUM(count_report) AS count_report,
			SUM(count_buf_start) AS count_buf_start,
			SUM(count_buf_end) AS count_buf_end,
			SUM(count_open_full_screen) AS count_open_full_screen,
			SUM(count_close_full_screen) AS count_close_full_screen,
			SUM(count_replay) AS count_replay,
			SUM(count_seek) AS count_seek,
			SUM(count_open_upload) AS count_open_upload,
			SUM(count_save_publish) AS count_save_publish,
			SUM(count_close_editor) AS count_close_editor,
			SUM(count_pre_bumper_played) AS count_pre_bumper_played,
			SUM(count_post_bumper_played) AS count_post_bumper_played,
			SUM(count_bumper_clicked) AS count_bumper_clicked,
			SUM(count_preroll_started) AS count_preroll_started,
			SUM(count_midroll_started) AS count_midroll_started,
			SUM(count_postroll_started) AS count_postroll_started,
			SUM(count_overlay_started) AS count_overlay_started,
			SUM(count_preroll_clicked) AS count_preroll_clicked,
			SUM(count_midroll_clicked) AS count_midroll_clicked,
			SUM(count_postroll_clicked) AS count_postroll_clicked,
			SUM(count_overlay_clicked) AS count_overlay_clicked,
			SUM(count_preroll_25) AS count_preroll_25,
			SUM(count_preroll_50) AS count_preroll_50,
			SUM(count_preroll_75) AS count_preroll_75,
			SUM(count_midroll_25) AS count_midroll_25,
			SUM(count_midroll_50) AS count_midroll_50,
			SUM(count_midroll_75) AS count_midroll_75,
		       SUM(count_postroll_25) AS count_postroll_25,
			SUM(count_postroll_50) AS count_postroll_50,
			SUM(count_postroll_75) AS count_postroll_75,
			SUM(count_bandwidth_kb) AS count_bandwidth_kb,
			SUM(total_admins) AS total_admins,
			SUM(total_media_entries) AS total_media_entries
			FROM kalturadw.dwh_hourly_events_devices fact, kalturadw.dwh_dim_entries dim
			WHERE fact.entry_id = dim.entry_id
			AND fact.date_id = v_date_id
			GROUP BY partner_id, date_id, hour_id, location_id, country_id, os_id, browser_id, ui_conf_id, entry_media_type_id;


                UPDATE kalturadw.tmp_devices_migration SET end_time = NOW(), is_copied = 1 WHERE day_id = v_date_id;
        END LOOP;
        CLOSE fix_devices_cursor;

    END$$

DELIMITER ;

CALL kalturadw.tmp_fix_devices();

DROP TABLE tmp_devices_migration;
DROP PROCEDURE IF EXISTS `tmp_fix_devices`;