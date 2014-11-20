USE `kalturadw`;

DROP TABLE IF EXISTS kalturadw.`dwh_hourly_user_usage`;

CREATE TABLE kalturadw.`dwh_hourly_user_usage` (
  `partner_id` INT(11) NOT NULL,
  `kuser_id` INT(11) NOT NULL,
  `date_id` INT(11) NOT NULL,
  `hour_id` INT(11) NOT NULL,
  `added_storage_kb`  DECIMAL(19,4) DEFAULT 0.0000,
  `total_storage_kb` DECIMAL(19,4) ,
  `added_entries`  INT(11) DEFAULT 0,
  `total_entries` INT(11) ,
  `added_msecs`  INT(11) DEFAULT 0,
  `total_msecs` INT(11) ,
  PRIMARY KEY (`partner_id`, `kuser_id`,`date_id`, `hour_id`),
  KEY (`date_id`, `hour_id`)
) ENGINE=INNODB DEFAULT CHARSET=utf8
PARTITION BY RANGE (date_id)
(PARTITION @PARTITION_NAME@ VALUES LESS THAN (@PARTITION_VALUE@) ENGINE = INNODB);
 
 CALL kalturadw.add_monthly_partition_for_table('dwh_hourly_user_usage');
