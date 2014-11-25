USE kalturadw;

DROP TABLE IF EXISTS `dwh_hourly_partner_usage_new`;
CREATE TABLE `dwh_hourly_partner_usage_new` (
  `partner_id` int(11) NOT NULL,
  `date_id` int(11) NOT NULL,
  `hour_id` int(11) NOT NULL,
  `bandwidth_source_id` int(11) NOT NULL,
  `count_bandwidth_kb` decimal(19,4) DEFAULT '0.0000',
  `count_storage_mb` decimal(19,4) DEFAULT '0.0000',
  `aggr_storage_mb` decimal(19,4) DEFAULT NULL,
  PRIMARY KEY (`partner_id`,`date_id`,`hour_id`,`bandwidth_source_id`),
  KEY (`date_id`, `hour_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
/*!50100 PARTITION BY RANGE (date_id)
(PARTITION p_0 VALUES LESS THAN (1) ENGINE = InnoDB)*/;

CALL kalturadw.apply_table_partitions_to_target_table('dwh_hourly_partner_usage');

INSERT INTO dwh_hourly_partner_usage_new
SELECT * FROM dwh_hourly_partner_usage;

RENAME TABLE dwh_hourly_partner_usage TO dwh_hourly_partner_usage_old;
RENAME TABLE dwh_hourly_partner_usage_new TO dwh_hourly_partner_usage;
