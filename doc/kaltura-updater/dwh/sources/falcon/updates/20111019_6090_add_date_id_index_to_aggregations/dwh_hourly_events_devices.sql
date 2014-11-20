USE kalturadw;

DROP TABLE IF EXISTS `dwh_hourly_events_devices_new`;
CREATE TABLE `dwh_hourly_events_devices_new` (
`partner_id` int(11) NOT NULL DEFAULT '-1',
  `date_id` int(11) NOT NULL,
  `hour_id` int(11) NOT NULL,
  `location_id` int(11) NOT NULL DEFAULT '-1',
  `country_id` int(11) NOT NULL DEFAULT '-1',
  `os_id` int(11) NOT NULL DEFAULT '-1',
  `browser_id` int(11) NOT NULL DEFAULT '-1',
  `ui_conf_id` int(11) NOT NULL DEFAULT '-1',
  `entry_id` varchar(20) NOT NULL DEFAULT '-1',
  `sum_time_viewed` decimal(20,3) DEFAULT NULL,
  `count_time_viewed` int(11) DEFAULT NULL,
  `count_plays` int(11) DEFAULT NULL,
  `count_loads` int(11) DEFAULT NULL,
  `count_plays_25` int(11) DEFAULT NULL,
  `count_plays_50` int(11) DEFAULT NULL,
  `count_plays_75` int(11) DEFAULT NULL,
  `count_plays_100` int(11) DEFAULT NULL,
  `count_edit` int(11) DEFAULT NULL,
  `count_viral` int(11) DEFAULT NULL,
  `count_download` int(11) DEFAULT NULL,
  `count_report` int(11) DEFAULT NULL,
  `count_buf_start` int(11) DEFAULT NULL,
  `count_buf_end` int(11) DEFAULT NULL,
  `count_open_full_screen` int(11) DEFAULT NULL,
  `count_close_full_screen` int(11) DEFAULT NULL,
  `count_replay` int(11) DEFAULT NULL,
  `count_seek` int(11) DEFAULT NULL,
  `count_open_upload` int(11) DEFAULT NULL,
  `count_save_publish` int(11) DEFAULT NULL,
  `count_close_editor` int(11) DEFAULT NULL,
  `count_pre_bumper_played` int(11) DEFAULT NULL,
  `count_post_bumper_played` int(11) DEFAULT NULL,
  `count_bumper_clicked` int(11) DEFAULT NULL,
  `count_preroll_started` int(11) DEFAULT NULL,
  `count_midroll_started` int(11) DEFAULT NULL,
  `count_postroll_started` int(11) DEFAULT NULL,
  `count_overlay_started` int(11) DEFAULT NULL,
  `count_preroll_clicked` int(11) DEFAULT NULL,
  `count_midroll_clicked` int(11) DEFAULT NULL,
  `count_postroll_clicked` int(11) DEFAULT NULL,
  `count_overlay_clicked` int(11) DEFAULT NULL,
  `count_preroll_25` int(11) DEFAULT NULL,
  `count_preroll_50` int(11) DEFAULT NULL,
  `count_preroll_75` int(11) DEFAULT NULL,
  `count_midroll_25` int(11) DEFAULT NULL,
  `count_midroll_50` int(11) DEFAULT NULL,
  `count_midroll_75` int(11) DEFAULT NULL,
  `count_postroll_25` int(11) DEFAULT NULL,
  `count_postroll_50` int(11) DEFAULT NULL,
  `count_postroll_75` int(11) DEFAULT NULL,
  `count_bandwidth_kb` int(11) DEFAULT NULL,
  `total_admins` int(11) DEFAULT NULL,
  `total_media_entries` int(11) DEFAULT NULL,
  PRIMARY KEY (`partner_id`,`date_id`,`hour_id`,`location_id`,`country_id`,`os_id`,`browser_id`,`ui_conf_id`,`entry_id`),
  KEY (`date_id`, `hour_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
/*!50100 PARTITION BY RANGE (date_id)
(PARTITION p_0 VALUES LESS THAN (1) ENGINE = InnoDB)*/;

CALL kalturadw.apply_table_partitions_to_target_table('dwh_hourly_events_devices');

INSERT INTO dwh_hourly_events_devices_new
SELECT * FROM dwh_hourly_events_devices;

RENAME TABLE dwh_hourly_events_devices TO dwh_hourly_events_devices_old;
RENAME TABLE dwh_hourly_events_devices_new TO dwh_hourly_events_devices;
