USE `kalturadw`;

DROP TABLE IF EXISTS `dwh_daily_ingestion`;


CREATE TABLE `dwh_daily_ingestion` (
  `date_id` int(11) NOT NULL,
  `normal_wait_time_count` int(11) NOT NULL,
  `medium_wait_time_count` int(11) NOT NULL,
  `long_wait_time_count` int(11) NOT NULL,
  `extremely_long_wait_time_count` int(11) NOT NULL,
  `stuck_wait_time_count` int(11) NOT NULL,
  `success_entries_count` int(11) NOT NULL,
  `failed_entries_count` int(11) NOT NULL,
  `success_convert_job_count` int(11) NOT NULL,
  `failed_convert_job_count` int(11) NOT NULL,
  `all_conversion_job_entries_count` int(11) NOT NULL,
  `failed_conversion_job_entries_count` int(11) NOT NULL,
  `total_wait_time_sec` bigint(22) DEFAULT '0',
  `total_ff_wait_time_sec` bigint(22) DEFAULT '0',
  `convert_jobs_count` int(11) NOT NULL,
  `median_ff_wait_time_sec` bigint(22) DEFAULT '0',
  PRIMARY KEY (`date_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8
PARTITION BY RANGE (date_id)
(PARTITION @PARTITION_NAME@ VALUES LESS THAN (@PARTITION_VALUE@) ENGINE = InnoDB);

CALL kalturadw.add_monthly_partition_for_table('dwh_daily_ingestion');

