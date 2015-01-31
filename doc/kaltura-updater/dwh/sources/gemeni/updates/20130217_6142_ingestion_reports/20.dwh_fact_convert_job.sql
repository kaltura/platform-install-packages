USE `kalturadw`;

DROP TABLE IF EXISTS `dwh_fact_convert_job`;

CREATE TABLE `dwh_fact_convert_job` (
  `id` int(11) NOT NULL,
  `job_type_id` int(11) DEFAULT NULL,
  `status_id` int(11) DEFAULT NULL,
  `partner_id` int(11) DEFAULT NULL,
  `created_date_id` int(11) DEFAULT '-1',
  `updated_date_id` int(11) DEFAULT '-1',
  `finish_date_id` int(11) DEFAULT '-1',
  `entry_id` varchar(20) DEFAULT NULL,
  `dc` int(11) DEFAULT NULL,
  `wait_time` int(22) DEFAULT NULL,
  `conversion_time` int(22) DEFAULT NULL,
  `is_ff` int(2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `dwh_created_date_id` (`created_date_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8