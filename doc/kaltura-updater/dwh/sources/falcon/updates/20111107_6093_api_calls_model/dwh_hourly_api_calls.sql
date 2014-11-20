USE kalturadw;

DROP TABLE IF EXISTS `dwh_hourly_api_calls`;
CREATE TABLE `dwh_hourly_api_calls` (
  `date_id` int(11) NOT NULL DEFAULT '0',
  `hour_id` tinyint(4) DEFAULT NULL,
  `partner_id` int(11) DEFAULT NULL,
  `action_id` int(11) NOT NULL DEFAULT '0',
  `count_calls` decimal(22,0) DEFAULT NULL,
  `count_success` decimal(23,0) DEFAULT NULL,
  `count_is_in_multi_request` decimal(23,0) DEFAULT NULL,
  `count_is_admin` decimal(14,4) DEFAULT NULL,
  `sum_duration_msecs` decimal(32,0) DEFAULT NULL,
  PRIMARY KEY (`partner_id`,`date_id`,`hour_id`, `action_id`),
  KEY (`date_id`,`hour_id`)
) ENGINE=INNODB DEFAULT CHARSET=utf8
/*!50100 PARTITION BY RANGE (date_id)
(PARTITION @PARTITION_NAME@ VALUES LESS THAN (@PARTITION_VALUE@) ENGINE = InnoDB) */;

CALL add_monthly_partition_for_table('dwh_hourly_api_calls');
