USE `kalturadw`;

DROP TABLE IF EXISTS `dwh_daily_partner_ingestion`;


CREATE TABLE `dwh_daily_partner_ingestion` (
  `date_id` int(11) NOT NULL,
  `partner_id` int(11) NOT NULL,
  `total_conversion_sec` int(22) DEFAULT '0',
  PRIMARY KEY (`date_id`,`partner_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
PARTITION BY RANGE (date_id)
(PARTITION @PARTITION_NAME@ VALUES LESS THAN (@PARTITION_VALUE@) ENGINE = InnoDB);

CALL kalturadw.add_monthly_partition_for_table('dwh_daily_partner_ingestion');

