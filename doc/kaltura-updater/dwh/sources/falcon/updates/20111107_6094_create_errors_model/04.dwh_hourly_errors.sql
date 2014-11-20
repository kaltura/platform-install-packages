USE kalturadw;

DROP TABLE IF EXISTS dwh_hourly_errors;

CREATE TABLE dwh_hourly_errors (
	partner_id INT(11) NOT NULL,
	date_id int NOT NULL,
	hour_id int NOT NULL,
	error_code_id INT(11) NOT NULL,
	count_errors INT(11) NOT NULL,
	PRIMARY KEY (`partner_id`,`date_id`,`hour_id`,`error_code_id`),
	KEY (`date_id`, `hour_id`)
	) ENGINE=INNODB DEFAULT CHARSET=latin1
	/*!50100 PARTITION BY RANGE (date_id)
	(PARTITION @PARTITION_NAME@ VALUES LESS THAN (@PARTITION_VALUE@) ENGINE = INNODB)*/;

CALL add_monthly_partition_for_table('dwh_hourly_errors');
