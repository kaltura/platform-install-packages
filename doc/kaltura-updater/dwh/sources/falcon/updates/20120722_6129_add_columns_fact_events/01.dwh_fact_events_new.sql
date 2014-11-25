USE kalturadw;

DROP TABLE IF EXISTS kalturadw.dwh_fact_events_new;

CREATE TABLE kalturadw.dwh_fact_events_new (
  `file_id` int(11) NOT NULL,
  `event_id` int(11) NOT NULL,
  `event_type_id` smallint(6) NOT NULL,
  `client_version` varchar(31) DEFAULT NULL,
  `event_time` datetime DEFAULT NULL,
  `event_date_id` int(11) NOT NULL DEFAULT '0',
  `event_hour_id` tinyint(4) DEFAULT NULL,
  `session_id` varchar(50) DEFAULT NULL,
  `partner_id` int(11) DEFAULT NULL,
  `entry_id` varchar(20) DEFAULT NULL,
  `unique_viewer` varchar(40) DEFAULT NULL,
  `widget_id` varchar(31) DEFAULT NULL,
  `ui_conf_id` int(11) DEFAULT NULL,
  `uid` varchar(64) DEFAULT NULL,
  `current_point` int(11) DEFAULT NULL,
  `duration` int(11) DEFAULT NULL,
  `user_ip` varchar(15) DEFAULT NULL,
  `user_ip_number` int(10) unsigned DEFAULT NULL,
  `country_id` int(11) DEFAULT NULL,
  `location_id` int(11) DEFAULT NULL,
  `process_duration` int(11) DEFAULT NULL,
  `control_id` varchar(15) DEFAULT NULL,
  `seek` int(11) DEFAULT NULL,
  `new_point` int(11) DEFAULT NULL,
  `domain_id` int(11) DEFAULT NULL,
  `entry_media_type_id` int(11) DEFAULT NULL,
  `entry_partner_id` int(11) DEFAULT NULL,
  `referrer_id` int(11) DEFAULT NULL,
  `os_id` int(11) DEFAULT NULL,
  `browser_id` int(11) DEFAULT NULL,
  `context_id` int(11) DEFAULT NULL,
  `user_id` int(11) DEFAULT NULL,
  `application_id` int(11) DEFAULT NULL,
  `feature_type` int(11) DEFAULT NULL,
  PRIMARY KEY (`file_id`,`event_id`,`event_date_id`),
  KEY `Entry_id` (`entry_id`),
  KEY `event_hour_id_event_date_id_partner_id` (`event_hour_id`,`event_date_id`,`partner_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
/*!50100 PARTITION BY RANGE (event_date_id)
(PARTITION p_0 VALUES LESS THAN (1) ENGINE = INNODB) */;
